"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import include, path

from apps.billing.views import stripe_webhook
from apps.common.views import home

urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("apps.accounts.urls")),
    path("billing/", include("apps.billing.urls")),
    path("app/", include("apps.app.urls")),
    path("stripe/webhook", stripe_webhook, name="stripe_webhook"),
    path("admin/", admin.site.urls),
]
