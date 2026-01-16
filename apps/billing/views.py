import os

import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import BillingProfile

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")


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
    price_id = os.environ.get("STRIPE_PRICE_ID", "")

    if not price_id:
        return HttpResponse("Stripe is not configured", status=500)

    # Get or create BillingProfile
    billing_profile, _ = BillingProfile.objects.get_or_create(user=request.user)

    # Build absolute URLs for success/cancel
    scheme = "https" if request.is_secure() else "http"
    host = request.get_host()
    success_url = f"{scheme}://{host}/billing/success/"
    cancel_url = f"{scheme}://{host}/billing/cancel/"

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
    """Stripe webhook endpoint (stub - will be implemented in next commit)."""
    return HttpResponse(status=200)
