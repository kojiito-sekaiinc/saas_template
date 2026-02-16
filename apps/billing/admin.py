from django.contrib import admin

from .models import BillingProfile, ProcessedEvent


@admin.register(BillingProfile)
class BillingProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "current_period_end", "stripe_customer_id", "created_at")
    list_filter = ("status",)
    search_fields = ("user__email", "stripe_customer_id", "stripe_subscription_id")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("user",)


@admin.register(ProcessedEvent)
class ProcessedEventAdmin(admin.ModelAdmin):
    list_display = ("event_id", "created_at")
    search_fields = ("event_id",)
