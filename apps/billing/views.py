import logging
from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import BillingProfile, ProcessedEvent

User = get_user_model()
logger = logging.getLogger(__name__)

# checkout() で Portal に誘導するサブスクリプション状態。
# これらの状態は「購読は存在するが支払いが詰まっている」ケースであり、
# Checkout で新規 subscription を作ると Stripe 側に並存状態が生じる可能性がある。
# stripe_subscription_id がある場合のみ Portal へ送る（痕跡がない場合は Checkout へ）。
#
# incomplete_expired は初回支払いが失効済みで subscription が存在しない扱いのため
# canceled と同様に Checkout へ進む（このセットに含めない）。
_PORTAL_STATUSES = {"active", "past_due", "unpaid", "incomplete"}


def pricing(request):
    context = {
        "price": 980,
        "currency": "JPY",
    }
    return render(request, "billing/pricing.html", context)


@login_required
@require_POST
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_PRICE_ID:
        return HttpResponse("Stripe is not configured", status=500)

    site_url = settings.SITE_URL.rstrip("/")
    success_url = f"{site_url}/billing/success/"
    cancel_url = f"{site_url}/billing/cancel/"

    # --- フェーズ1: 現在の状態を読み取る（短いトランザクション）---
    with transaction.atomic():
        billing_profile, _ = BillingProfile.objects.select_for_update().get_or_create(
            user=request.user
        )
        if (
            billing_profile.status in _PORTAL_STATUSES
            and billing_profile.stripe_subscription_id
        ):
            return redirect("billing:portal")
        existing_customer_id = billing_profile.stripe_customer_id

    # --- フェーズ2: Stripe 顧客を作成（トランザクション外）---
    # idempotency_key により、短時間の並行リクエストでも Stripe 側の重複作成を抑制する。
    # ただし Stripe の冪等性保証は短時間に限られるため、フェーズ3 の DB ロックを正本とする。
    customer_id = existing_customer_id
    if not customer_id:
        try:
            customer = stripe.Customer.create(
                email=request.user.email,
                metadata={"user_id": str(request.user.id)},
                idempotency_key=f"create_customer_{request.user.id}",
            )
            new_customer_id = customer.id
        except stripe.StripeError as e:
            logger.error(f"Stripe Customer create error: {e}")
            return HttpResponse("An error occurred. Please try again later.", status=500)

        # --- フェーズ3: 再ロックして保存（並行リクエストの race 防止）---
        # 別リクエストが先に stripe_customer_id を書き込んでいた場合は DB 上の値を正本として採用する。
        try:
            with transaction.atomic():
                billing_profile = BillingProfile.objects.select_for_update().get(
                    user=request.user
                )
                if billing_profile.stripe_customer_id:
                    logger.info(
                        "checkout: stripe_customer_id already set by concurrent request "
                        f"for user_id={request.user.id}; using existing value"
                    )
                    customer_id = billing_profile.stripe_customer_id
                else:
                    billing_profile.stripe_customer_id = new_customer_id
                    billing_profile.save()
                    customer_id = new_customer_id
        except BillingProfile.DoesNotExist:
            logger.error(
                f"checkout: BillingProfile disappeared for user_id={request.user.id}"
            )
            return HttpResponse("An error occurred. Please try again later.", status=500)

    # --- フェーズ4: Stripe Checkout セッション作成（トランザクション外）---
    hour_bucket = int(datetime.now(dt_timezone.utc).timestamp()) // 3600
    idempotency_key = f"checkout_{request.user.id}_{hour_bucket}"

    try:
        session = stripe.checkout.Session.create(
            customer=customer_id,
            mode="subscription",
            line_items=[
                {
                    "price": settings.STRIPE_PRICE_ID,
                    "quantity": 1,
                }
            ],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"user_id": str(request.user.id)},
            idempotency_key=idempotency_key,
        )
        return redirect(session.url)

    except stripe.StripeError as e:
        logger.error(f"Stripe Checkout error: {e}")
        return HttpResponse("An error occurred. Please try again later.", status=500)


@login_required
def success(request):
    return render(request, "billing/success.html")


@login_required
def cancel(request):
    return render(request, "billing/cancel.html")


@login_required
def portal(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if not settings.STRIPE_SECRET_KEY:
        return HttpResponse("Stripe is not configured", status=500)

    try:
        billing_profile = BillingProfile.objects.get(user=request.user)
    except BillingProfile.DoesNotExist:
        return redirect("billing:pricing")

    if not billing_profile.stripe_customer_id:
        return redirect("billing:pricing")

    site_url = settings.SITE_URL.rstrip("/")
    # Portal から戻る先: アクティブ会員はアプリへ、それ以外は pricing へ
    if billing_profile.status == "active":
        return_url = f"{site_url}/app/"
    else:
        return_url = f"{site_url}/billing/pricing/"

    try:
        session = stripe.billing_portal.Session.create(
            customer=billing_profile.stripe_customer_id,
            return_url=return_url,
        )
        return redirect(session.url)
    except stripe.StripeError as e:
        logger.error(f"Stripe portal error: {e}")
        return HttpResponse("An error occurred. Please try again later.", status=500)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Stripe webhook endpoint - single source of truth for billing state."""
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    if not webhook_secret:
        logger.error("STRIPE_WEBHOOK_SECRET not configured")
        return HttpResponse("Webhook secret not configured", status=400)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        logger.warning("Stripe webhook: invalid payload")
        return HttpResponse("Invalid payload", status=400)
    except stripe.SignatureVerificationError:
        logger.warning("Stripe webhook: invalid signature")
        return HttpResponse("Invalid signature", status=400)

    event_id = event.get("id")
    event_type = event.get("type")

    logger.info(
        f"Stripe webhook received: event_id={event_id}, type={event_type}"
    )

    if event_type in (
        "customer.subscription.created",
        "customer.subscription.updated",
        "customer.subscription.deleted",
    ):
        subscription = event.get("data", {}).get("object")
        if not subscription:
            logger.warning(
                "Stripe webhook: unexpected event structure (missing data.object): "
                f"event_id={event_id}, type={event_type}"
            )
            return HttpResponse(status=200)
        event_created = event.get("created")
        _handle_subscription_event(subscription, event_id, event_created, event_type)

    return HttpResponse(status=200)


def _handle_subscription_event(
    subscription, event_id: str | None, event_created: int | None = None,
    event_type: str | None = None,
):
    stripe_subscription_id = subscription.get("id")
    stripe_customer_id = subscription.get("customer")
    status = subscription.get("status")

    if not all([stripe_subscription_id, stripe_customer_id, status]):
        logger.warning(
            "Stripe subscription event missing required fields: "
            f"event_id={event_id}, "
            f"id={stripe_subscription_id}, customer={stripe_customer_id}, status={status}"
        )
        return
    current_period_end_ts = subscription.get("current_period_end")

    if event_type != "customer.subscription.deleted":
        if not _is_valid_subscription(subscription, settings.STRIPE_PRICE_ID):
            # 既知のサブスクなら status 更新を許可（past_due, unpaid 等を拾う）
            if not BillingProfile.objects.filter(
                stripe_subscription_id=stripe_subscription_id
            ).exists():
                logger.info(
                    "Stripe subscription ignored (price mismatch, unknown subscription): "
                    f"event_id={event_id}, subscription_id={stripe_subscription_id}"
                )
                return
            logger.info(
                "Price mismatch but known subscription — processing: "
                f"event_id={event_id}, subscription_id={stripe_subscription_id}"
            )

    current_period_end = None
    if current_period_end_ts:
        current_period_end = datetime.fromtimestamp(
            current_period_end_ts, tz=dt_timezone.utc
        )

    user = _find_user_for_subscription(subscription, stripe_customer_id)
    if not user:
        logger.warning(
            "Stripe subscription received but no user found: "
            f"event_id={event_id}, subscription_id={stripe_subscription_id}, "
            f"customer_id={stripe_customer_id}"
        )
        return

    try:
        with transaction.atomic():
            billing_profile, _ = BillingProfile.objects.get_or_create(user=user)
            billing_profile = (
                BillingProfile.objects.select_for_update().get(pk=billing_profile.pk)
            )

            # Out-of-order guard: skip if event is older than last processed
            if (
                event_created is not None
                and billing_profile.last_stripe_event_created is not None
                and event_created < billing_profile.last_stripe_event_created
            ):
                logger.info(
                    "Out-of-order Stripe event skipped: "
                    f"event_id={event_id}, event_created={event_created}, "
                    f"last={billing_profile.last_stripe_event_created}"
                )
                return

            # Deduplication: reject already-processed events
            if event_id:
                try:
                    ProcessedEvent.objects.create(event_id=event_id)
                except IntegrityError:
                    logger.info(
                        f"Duplicate Stripe event skipped: event_id={event_id}"
                    )
                    return

            billing_profile.stripe_customer_id = stripe_customer_id
            billing_profile.stripe_subscription_id = stripe_subscription_id
            billing_profile.status = status
            billing_profile.current_period_end = current_period_end
            if event_created is not None:
                billing_profile.last_stripe_event_created = event_created
            billing_profile.save()

    except IntegrityError:
        logger.warning(
            f"Unexpected IntegrityError for event_id={event_id}"
        )
        return

    logger.info(
        "BillingProfile updated from Stripe webhook: "
        f"event_id={event_id}, user_id={user.id}, "
        f"subscription_id={stripe_subscription_id}, status={status}"
    )


def _find_user_for_subscription(subscription, stripe_customer_id):
    metadata = subscription.get("metadata", {})
    user_id = metadata.get("user_id")

    if user_id:
        try:
            return User.objects.get(id=int(user_id))
        except (User.DoesNotExist, ValueError):
            pass

    try:
        billing_profile = BillingProfile.objects.get(
            stripe_customer_id=stripe_customer_id
        )
        return billing_profile.user
    except BillingProfile.DoesNotExist:
        return None
    except BillingProfile.MultipleObjectsReturned:
        logger.error(
            "Multiple BillingProfiles found for stripe_customer_id=%s "
            "(data integrity issue - returning None for safety)",
            stripe_customer_id,
        )
        return None


def _is_valid_subscription(subscription, expected_price_id):
    if not expected_price_id:
        logger.error("STRIPE_PRICE_ID not configured - rejecting event (fail-closed)")
        return False

    items = subscription.get("items", {}).get("data", [])
    for item in items:
        price = item.get("price", {})
        if price.get("id") == expected_price_id:
            return True

    return False