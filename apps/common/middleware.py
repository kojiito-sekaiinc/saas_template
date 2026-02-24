from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone

from apps.accounts.models import Profile
from apps.billing.models import BillingProfile


class PaywallMiddleware:
    """
    Middleware to protect paid features under /app/.

    Access rules:
    - Not logged in → redirect to login with next
    - Logged in:
      - now <= Profile.free_until → allow
      - BillingProfile.status == "active" → allow
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
        try:
            profile = user.profile
        except (Profile.DoesNotExist, AttributeError):
            return False
        if not profile.free_until:
            return False
        return timezone.now() <= profile.free_until

    def _has_active_subscription(self, user):
        """
        Check if user has active subscription.

        NOTE:
        - Only 'active' grants paid access (see CLAUDE.md Section 6).
        """
        try:
            billing_profile = user.billing_profile
        except (BillingProfile.DoesNotExist, AttributeError):
            return False
        return billing_profile.is_active
