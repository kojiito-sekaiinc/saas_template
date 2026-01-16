from django.contrib import admin

from .models import BillingProfile


@admin.register(BillingProfile)
class BillingProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "stripe_customer_id", "created_at")
    list_filter = ("status",)
    search_fields = ("user__email", "stripe_customer_id", "stripe_subscription_id")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("user",)
