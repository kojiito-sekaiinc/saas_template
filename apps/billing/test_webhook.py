# apps/billing/test_webhook.py

import json
import time

import pytest
from django.test import Client
from django.utils import timezone
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_stripe_webhook_logs_event_id(monkeypatch, caplog):
    """
    Stripe webhook が呼ばれたときに、event_id を含むログが出力されることを検証する。
    """

    # 遅延 import にしておくと、views.py の修正を反映しやすい
    from apps.billing import views as billing_views

    User = get_user_model()
    user = User.objects.create_user(
        email="webhook-test@example.com",
        password="testpass123",
    )

    # Stripeのsubscriptionオブジェクトをモック
    subscription = {
        "id": "sub_test_123",
        "customer": "cus_test_123",
        "status": "active",
        "current_period_end": int(time.time()),
        "metadata": {"user_id": str(user.id)},
        "items": {"data": []},
    }

    # stripe.Webhook.construct_event を差し替え
    def fake_construct_event(payload, sig_header, secret):
        return {
            "id": "evt_test_123",
            "type": "customer.subscription.updated",
            "data": {"object": subscription},
        }

    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test_secret")
    monkeypatch.setattr(
        billing_views.stripe.Webhook,
        "construct_event",
        staticmethod(fake_construct_event),
    )

    client = Client()

    # apps.billing.views ロガーの INFO を caplog で捕まえる
    with caplog.at_level("INFO", logger="apps.billing.views"):
        response = client.post(
            "/stripe/webhook",
            data=json.dumps({}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )

    assert response.status_code == 200

    # event_id を含むログが出ていることを検証
    assert "Stripe webhook received: event_id=evt_test_123" in caplog.text