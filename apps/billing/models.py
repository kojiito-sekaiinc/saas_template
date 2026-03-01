from django.conf import settings
from django.db import models


class ProcessedEvent(models.Model):
    """Processed Stripe event log for deduplication."""

    event_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "billing_processed_events"

    def __str__(self):
        return self.event_id


class BillingProfile(models.Model):
    """User billing profile for Stripe subscription management."""

    STATUS_CHOICES = [
        # アプリ内部状態（Stripe 連携前）
        ("not_subscribed", "Not Subscribed"),
        # Stripe サブスクリプションステータス
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
    stripe_customer_id = models.CharField(
        max_length=255, blank=True, null=True, unique=True, default=None
    )
    stripe_subscription_id = models.CharField(
        max_length=255, blank=True, null=True, unique=True, default=None
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_subscribed",
    )
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_stripe_event_created = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "billing_profiles"

    def __str__(self):
        return f"BillingProfile for {self.user.email}"

    @property
    def is_active(self):
        """Check if subscription grants paid access (CLAUDE.md Section 6)."""
        # Only 'active' grants paid access. 'trialing' is NOT treated as paid.
        return self.status == "active"
