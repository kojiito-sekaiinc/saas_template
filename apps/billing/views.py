import logging
import os
from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import BillingProfile

User = get_user_model()
logger = logging.getLogger(__name__)

# Stripe configuration (loaded once at import time)
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_ID = os.environ.get("STRIPE_PRICE_ID", "")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


def pricing(request):
    context = {
        "price": 980,
        "currency": "JPY",
    }
    return render(request, "billing/pricing.html", context)


@login_required
@require_POST
def checkout(request):
    if not STRIPE_SECRET_KEY or not STRIPE_PRICE_ID:
        return HttpResponse("Stripe is not configured", status=500)

    billing_profile, _ = BillingProfile.objects.get_or_create(user=request.user)

    site_url = settings.SITE_URL.rstrip("/")
    success_url = f"{site_url}/billing/success/"
    cancel_url = f"{site_url}/billing/cancel/"

    try:
        if billing_profile.stripe_customer_id:
            customer_id = billing_profile.stripe_customer_id
        else:
            customer = stripe.Customer.create(
                email=request.user.email,
                metadata={"user_id": str(request.user.id)},
            )
            billing_profile.stripe_customer_id = customer.id
            billing_profile.save()
            customer_id = customer.id

        session = stripe.checkout.Session.create(
            customer=customer_id,
            mode="subscription",
            line_items=[
                {
                    "price": STRIPE_PRICE_ID,
                    "quantity": 1,
                }
            ],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"user_id": str(request.user.id)},
        )

        return redirect(session.url)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe Checkout error: {e}")
        return HttpResponse(f"Stripe error: {e}", status=500)


@login_required
def portal(request):
    if not STRIPE_SECRET_KEY:
        return HttpResponse("Stripe is not configured", status=500)

    try:
        billing_profile = BillingProfile.objects.get(user=request.user)
    except BillingProfile.DoesNotExist:
        return redirect("billing:pricing")

    if not billing_profile.stripe_customer_id:
        return redirect("billing:pricing")

    site_url = settings.SITE_URL.rstrip("/")
    return_url = f"{site_url}/billing/pricing/"

    try:
        session = stripe.billing_portal.Session.create(
            customer=billing_profile.stripe_customer_id,
            return_url=return_url,
        )
        return redirect(session.url)
    except stripe.error.StripeError as e:
        logger.error(f"Stripe portal error: {e}")
        return HttpResponse(f"Stripe error: {e}", status=500)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Stripe webhook endpoint - single source of truth for billing state."""
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    if not webhook_secret:
        logger.error("STRIPE_WEBHOOK_SECRET not configured")
        return HttpResponse("Webhook secret not configured", status=500)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        logger.warning("Stripe webhook: invalid payload")
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
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
        subscription = event["data"]["object"]
        _handle_subscription_event(subscription, event_id)

    return HttpResponse(status=200)


def _handle_subscription_event(subscription, event_id: str | None):
    stripe_subscription_id = subscription["id"]
    stripe_customer_id = subscription["customer"]
    status = subscription["status"]
    current_period_end_ts = subscription.get("current_period_end")

    if not _is_valid_subscription(subscription, STRIPE_PRICE_ID):
        logger.info(
            "Stripe subscription ignored (price mismatch): "
            f"event_id={event_id}, subscription_id={stripe_subscription_id}"
        )
        return

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

    billing_profile, _ = BillingProfile.objects.get_or_create(user=user)
    billing_profile.stripe_customer_id = stripe_customer_id
    billing_profile.stripe_subscription_id = stripe_subscription_id
    billing_profile.status = status
    billing_profile.current_period_end = current_period_end
    billing_profile.save()

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


def _is_valid_subscription(subscription, expected_price_id):
    if not expected_price_id:
        logger.warning("STRIPE_PRICE_ID not configured - skipping price validation")
        return True

    items = subscription.get("items", {}).get("data", [])
    for item in items:
        price = item.get("price", {})
        if price.get("id") == expected_price_id:
            return True

    return False