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
    # price mismatch + unknown subscription → 無視ログ
    assert "price mismatch, unknown subscription" in caplog.text


@pytest.mark.django_db
def test_stripe_webhook_missing_data_object_returns_200(monkeypatch, caplog):
    """
    署名検証済みだが data.object が欠損している場合、
    500 ではなく warning ログ + 200 で安全に終了することを検証する。
    """
    from apps.billing import views as billing_views

    def fake_construct_event(payload, sig_header, secret):
        return {
            "id": "evt_bad_structure",
            "type": "customer.subscription.updated",
            "data": {},
        }

    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test_secret")
    monkeypatch.setattr(
        billing_views.stripe.Webhook,
        "construct_event",
        staticmethod(fake_construct_event),
    )

    client = Client()

    with caplog.at_level("WARNING", logger="apps.billing.views"):
        response = client.post(
            "/stripe/webhook",
            data=json.dumps({}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )

    assert response.status_code == 200
    assert "unexpected event structure" in caplog.text


@pytest.mark.django_db
def test_stripe_webhook_missing_required_fields_returns_200(monkeypatch, caplog):
    """
    subscription に必須キー（id）が欠損している場合、
    KeyError ではなく warning ログ + 200 で安全に終了することを検証する。
    """
    from apps.billing import views as billing_views

    # "id" キーを除去した subscription
    subscription = {
        "customer": "cus_test_456",
        "status": "active",
        "current_period_end": int(time.time()),
        "metadata": {},
        "items": {"data": []},
    }

    def fake_construct_event(payload, sig_header, secret):
        return {
            "id": "evt_missing_fields",
            "type": "customer.subscription.created",
            "data": {"object": subscription},
        }

    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test_secret")
    monkeypatch.setattr(
        billing_views.stripe.Webhook,
        "construct_event",
        staticmethod(fake_construct_event),
    )

    client = Client()

    with caplog.at_level("WARNING", logger="apps.billing.views"):
        response = client.post(
            "/stripe/webhook",
            data=json.dumps({}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )

    assert response.status_code == 200
    assert "missing required fields" in caplog.text


@pytest.mark.django_db
def test_deleted_event_bypasses_price_mismatch(monkeypatch, caplog):
    """
    deleted イベントは price_id チェックをバイパスし、
    items.data が空でも BillingProfile.status が更新されることを検証する。
    """
    from apps.billing import views as billing_views
    from apps.billing.models import BillingProfile

    User = get_user_model()
    user = User.objects.create_user(
        email="deleted-bypass@example.com",
        password="testpass123",
    )

    # active 状態の BillingProfile を事前作成
    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_del_123",
        stripe_subscription_id="sub_del_123",
        status="active",
    )

    # items.data が空の deleted イベント
    subscription = {
        "id": "sub_del_123",
        "customer": "cus_del_123",
        "status": "canceled",
        "current_period_end": int(time.time()),
        "metadata": {"user_id": str(user.id)},
        "items": {"data": []},
    }

    def fake_construct_event(payload, sig_header, secret):
        return {
            "id": "evt_deleted_bypass",
            "type": "customer.subscription.deleted",
            "created": int(time.time()),
            "data": {"object": subscription},
        }

    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test_secret")
    monkeypatch.setattr(
        billing_views.stripe.Webhook,
        "construct_event",
        staticmethod(fake_construct_event),
    )

    client = Client()

    with caplog.at_level("INFO", logger="apps.billing.views"):
        response = client.post(
            "/stripe/webhook",
            data=json.dumps({}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )

    assert response.status_code == 200

    bp = BillingProfile.objects.get(user=user)
    assert bp.status == "canceled"


@pytest.mark.django_db
def test_deleted_event_works_without_stripe_price_id(monkeypatch, caplog):
    """
    STRIPE_PRICE_ID が未設定でも deleted イベントで
    BillingProfile.status が更新されることを検証する。
    """
    from apps.billing import views as billing_views
    from apps.billing.models import BillingProfile

    User = get_user_model()
    user = User.objects.create_user(
        email="deleted-noprice@example.com",
        password="testpass123",
    )

    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_noprice_123",
        stripe_subscription_id="sub_noprice_123",
        status="active",
    )

    subscription = {
        "id": "sub_noprice_123",
        "customer": "cus_noprice_123",
        "status": "canceled",
        "current_period_end": int(time.time()),
        "metadata": {"user_id": str(user.id)},
        "items": {"data": [{"price": {"id": "price_other"}}]},
    }

    def fake_construct_event(payload, sig_header, secret):
        return {
            "id": "evt_deleted_noprice",
            "type": "customer.subscription.deleted",
            "created": int(time.time()),
            "data": {"object": subscription},
        }

    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test_secret")
    # STRIPE_PRICE_ID をモジュールレベルで空文字に差し替え
    monkeypatch.setattr(billing_views, "STRIPE_PRICE_ID", "")
    monkeypatch.setattr(
        billing_views.stripe.Webhook,
        "construct_event",
        staticmethod(fake_construct_event),
    )

    client = Client()

    with caplog.at_level("INFO", logger="apps.billing.views"):
        response = client.post(
            "/stripe/webhook",
            data=json.dumps({}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )

    assert response.status_code == 200

    bp = BillingProfile.objects.get(user=user)
    assert bp.status == "canceled"


@pytest.mark.django_db
def test_price_mismatch_known_subscription_updates_status(monkeypatch, caplog):
    """
    price 不一致でも stripe_subscription_id が既存 BillingProfile に一致する場合、
    status が更新されることを検証する（past_due 等の反映）。
    """
    from apps.billing import views as billing_views
    from apps.billing.models import BillingProfile

    User = get_user_model()
    user = User.objects.create_user(
        email="known-sub@example.com",
        password="testpass123",
    )

    # active 状態の BillingProfile を事前作成
    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_known_123",
        stripe_subscription_id="sub_known_123",
        status="active",
    )

    # price 不一致の updated イベント（status=past_due）
    subscription = {
        "id": "sub_known_123",
        "customer": "cus_known_123",
        "status": "past_due",
        "current_period_end": int(time.time()),
        "metadata": {"user_id": str(user.id)},
        "items": {"data": [{"price": {"id": "price_other_service"}}]},
    }

    def fake_construct_event(payload, sig_header, secret):
        return {
            "id": "evt_known_mismatch",
            "type": "customer.subscription.updated",
            "created": int(time.time()),
            "data": {"object": subscription},
        }

    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test_secret")
    monkeypatch.setattr(billing_views, "STRIPE_PRICE_ID", "price_expected_123")
    monkeypatch.setattr(
        billing_views.stripe.Webhook,
        "construct_event",
        staticmethod(fake_construct_event),
    )

    client = Client()

    with caplog.at_level("INFO", logger="apps.billing.views"):
        response = client.post(
            "/stripe/webhook",
            data=json.dumps({}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )

    assert response.status_code == 200

    bp = BillingProfile.objects.get(user=user)
    assert bp.status == "past_due"
    assert "Price mismatch but known subscription" in caplog.text


@pytest.mark.django_db
def test_price_mismatch_unknown_subscription_is_ignored(monkeypatch, caplog):
    """
    price 不一致かつ stripe_subscription_id が BillingProfile に存在しない場合、
    イベントが無視されることを検証する（別サービスの混入防止）。
    """
    from apps.billing import views as billing_views
    from apps.billing.models import BillingProfile

    User = get_user_model()
    user = User.objects.create_user(
        email="unknown-sub@example.com",
        password="testpass123",
    )

    # 別の subscription_id を持つ BillingProfile
    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_existing_456",
        stripe_subscription_id="sub_existing_456",
        status="active",
    )

    # 別の subscription_id + price 不一致の updated イベント
    subscription = {
        "id": "sub_other_service_789",
        "customer": "cus_existing_456",
        "status": "past_due",
        "current_period_end": int(time.time()),
        "metadata": {"user_id": str(user.id)},
        "items": {"data": [{"price": {"id": "price_other_service"}}]},
    }

    def fake_construct_event(payload, sig_header, secret):
        return {
            "id": "evt_unknown_mismatch",
            "type": "customer.subscription.updated",
            "created": int(time.time()),
            "data": {"object": subscription},
        }

    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test_secret")
    monkeypatch.setattr(billing_views, "STRIPE_PRICE_ID", "price_expected_123")
    monkeypatch.setattr(
        billing_views.stripe.Webhook,
        "construct_event",
        staticmethod(fake_construct_event),
    )

    client = Client()

    with caplog.at_level("INFO", logger="apps.billing.views"):
        response = client.post(
            "/stripe/webhook",
            data=json.dumps({}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )

    assert response.status_code == 200

    # status は active のまま変わらないことを検証
    bp = BillingProfile.objects.get(user=user)
    assert bp.status == "active"
    assert "price mismatch, unknown subscription" in caplog.text