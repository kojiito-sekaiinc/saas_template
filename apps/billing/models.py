from django.conf import settings
from django.db import models


class BillingProfile(models.Model):
    """User billing profile for Stripe subscription management."""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("trialing", "Trialing"),
        ("canceled", "Canceled"),
        ("past_due", "Past Due"),
        ("unpaid", "Unpaid"),
        ("incomplete", "Incomplete"),
        ("incomplete_expired", "Incomplete Expired"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="billing_profile",
    )
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_profiles"

    def __str__(self):
        return f"BillingProfile for {self.user.email}"

    @property
    def is_active(self):
        """Check if subscription grants paid access (CLAUDE.md Section 6)."""
        # Only 'active' grants paid access. 'trialing' is NOT treated as paid.
        return self.status == "active"
