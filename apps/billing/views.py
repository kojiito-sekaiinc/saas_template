from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def pricing(request):
    """Pricing page (stub)."""
    return render(request, "billing/pricing.html")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Stripe webhook endpoint (stub)."""
    return HttpResponse(status=200)
