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


def pricing(request):
    """Pricing page showing subscription plan."""
    context = {
        "price": 980,
        "currency": "JPY",
    }
    return render(request, "billing/pricing.html", context)


@login_required
@require_POST
def checkout(request):
    """Create Stripe Checkout Session for subscription."""
    # Configure Stripe API key
    stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY", "")
    if not stripe_secret_key:
        return HttpResponse("Stripe is not configured", status=500)
    stripe.api_key = stripe_secret_key

    price_id = os.environ.get("STRIPE_PRICE_ID", "")
    if not price_id:
        return HttpResponse("Stripe is not configured", status=500)

    # Get or create BillingProfile
    billing_profile, _ = BillingProfile.objects.get_or_create(user=request.user)

    # Build absolute URLs for success/cancel using SITE_URL
    site_url = settings.SITE_URL.rstrip("/")
    success_url = f"{site_url}/billing/success/"
    cancel_url = f"{site_url}/billing/cancel/"

    try:
        # Create or retrieve Stripe Customer
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

        # Create Checkout Session
        session = stripe.checkout.Session.create(
            customer=customer_id,
            mode="subscription",
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"user_id": str(request.user.id)},
        )

        return redirect(session.url)

    except stripe.error.StripeError as e:
        return HttpResponse(f"Stripe error: {e}", status=500)


def success(request):
    """Checkout success page (informational only)."""
    return render(request, "billing/success.html")


def cancel(request):
    """Checkout cancel page (informational only)."""
    return render(request, "billing/cancel.html")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Stripe webhook endpoint - single source of truth for billing state."""
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    # Verify webhook signature
    if not webhook_secret:
        logger.error("STRIPE_WEBHOOK_SECRET not configured")
        return HttpResponse("Webhook secret not configured", status=500)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        logger.warning("Invalid webhook payload")
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        logger.warning("Invalid webhook signature")
        return HttpResponse("Invalid signature", status=400)

    # Handle subscription events
    event_type = event["type"]
    if event_type in (
        "customer.subscription.created",
        "customer.subscription.updated",
        "customer.subscription.deleted",
    ):
        subscription = event["data"]["object"]
        _handle_subscription_event(subscription)

    return HttpResponse(status=200)


def _handle_subscription_event(subscription):
    """Process subscription event and update BillingProfile."""
    stripe_subscription_id = subscription["id"]
    stripe_customer_id = subscription["customer"]
    status = subscription["status"]
    current_period_end_ts = subscription.get("current_period_end")

    # Verify this subscription belongs to our product (Price ID check)
    expected_price_id = os.environ.get("STRIPE_PRICE_ID", "")
    if not _is_valid_subscription(subscription, expected_price_id):
        logger.info(
            f"Ignoring subscription {stripe_subscription_id} - "
            f"does not match expected price ID"
        )
        return

    # Convert timestamp to datetime
    current_period_end = None
    if current_period_end_ts:
        current_period_end = datetime.fromtimestamp(
            current_period_end_ts, tz=dt_timezone.utc
        )

    # Find user by metadata.user_id or stripe_customer_id
    user = _find_user_for_subscription(subscription, stripe_customer_id)
    if not user:
        logger.warning(
            f"No user found for subscription {stripe_subscription_id}, "
            f"customer {stripe_customer_id}"
        )
        return

    # Get or create BillingProfile and update (idempotent)
    billing_profile, _ = BillingProfile.objects.get_or_create(user=user)
    billing_profile.stripe_customer_id = stripe_customer_id
    billing_profile.stripe_subscription_id = stripe_subscription_id
    billing_profile.status = status
    billing_profile.current_period_end = current_period_end
    billing_profile.save()

    logger.info(
        f"Updated BillingProfile for user {user.id}: status={status}, "
        f"subscription={stripe_subscription_id}"
    )


def _find_user_for_subscription(subscription, stripe_customer_id):
    """Find user by metadata.user_id or stripe_customer_id."""
    # Try metadata.user_id first
    metadata = subscription.get("metadata", {})
    user_id = metadata.get("user_id")
    if user_id:
        try:
            return User.objects.get(id=int(user_id))
        except (User.DoesNotExist, ValueError):
            pass

    # Fallback to stripe_customer_id
    try:
        billing_profile = BillingProfile.objects.get(
            stripe_customer_id=stripe_customer_id
        )
        return billing_profile.user
    except BillingProfile.DoesNotExist:
        pass

    return None


def _is_valid_subscription(subscription, expected_price_id):
    """
    Verify that subscription contains the expected price ID.

    Returns True if any of the subscription items matches expected_price_id.
    """
    if not expected_price_id:
        logger.warning("STRIPE_PRICE_ID not configured - skipping price validation")
        return True

    items = subscription.get("items", {}).get("data", [])
    for item in items:
        price = item.get("price", {})
        if price.get("id") == expected_price_id:
            return True

    return False
