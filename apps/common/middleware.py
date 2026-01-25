from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone


class PaywallMiddleware:
    """
    Middleware to protect paid features under /app/.

    Access rules:
    - Not logged in → redirect to login with next
    - Logged in:
      - now <= Profile.free_until → allow
      - BillingProfile.status in ("active", "trialing") → allow
      - otherwise → redirect to /billing/pricing/
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._requires_paywall(request.path):
            redirect_response = self._check_access(request)
            if redirect_response:
                return redirect_response

        return self.get_response(request)

    def _requires_paywall(self, path):
        """Check if path requires paywall protection."""
        return path.startswith("/app/")

    def _check_access(self, request):
        """
        Check if user has access to paid features.
        Returns redirect response if access denied, None if allowed.
        """
        # Not logged in → redirect to login
        if not request.user.is_authenticated:
            login_url = settings.LOGIN_URL
            next_url = request.get_full_path()
            return redirect(f"{login_url}?{urlencode({'next': next_url})}")

        # Check free trial
        if self._is_in_free_trial(request.user):
            return None

        # Check active subscription
        if self._has_active_subscription(request.user):
            return None

        # No access → redirect to pricing
        return redirect("/billing/pricing/")

    def _is_in_free_trial(self, user):
        """Check if user is in free trial period."""
        # user.get_or_create_profile() に依存すると AnonymousUser などで壊れやすいので、
        # 素直に profile プロパティを見る。
        profile = getattr(user, "profile", None)
        if not profile or not getattr(profile, "free_until", None):
            return False

        return timezone.now() <= profile.free_until

    def _has_active_subscription(self, user):
        """
        Check if user has active subscription.

        BillingProfile is expected to have:
        - status field (string)
        - "active" or "trialing" grants access
        """
        billing_profile = getattr(user, "billing_profile", None)
        if not billing_profile:
            return False
        return getattr(billing_profile, "status", None) in ("active", "trialing")
