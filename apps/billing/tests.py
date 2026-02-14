# apps/billing/tests.py

import time

import pytest
from django.contrib.auth import get_user_model

from apps.billing.models import BillingProfile
from apps.billing.views import _handle_subscription_event

User = get_user_model()


def _build_subscription_payload(
    *,
    user_id: int,
    status: str,
    customer_id: str = "cus_test_123",
    subscription_id: str = "sub_test_123",
    price_id: str = "price_test_123",
) -> dict:
    """
    apps.billing.views._handle_subscription_event が期待する
    subscription オブジェクトに近い dict を組み立てる。
    """
    return {
        "id": subscription_id,
        "status": status,
        "customer": customer_id,
        "current_period_end": int(time.time()) + 3600,
        "metadata": {
            "user_id": str(user_id),
        },
        "items": {
            "data": [
                {
                    "price": {
                        "id": price_id,
                    }
                }
            ]
        },
    }


@pytest.fixture
def user():
    return User.objects.create_user(
        email="billing-test@example.com",
        password="password123",
    )


# ====================================================
# 1. created(active) → BillingProfile がアクティブになる
# ====================================================

@pytest.mark.django_db
def test_handle_subscription_created_active_marks_profile_active(user, monkeypatch):
    # 環境変数 STRIPE_PRICE_ID をセット（_is_valid_subscription 用）
    monkeypatch.setattr("apps.billing.views.STRIPE_PRICE_ID", "price_test_123")

    subscription = _build_subscription_payload(
        user_id=user.id,
        status="active",
        subscription_id="sub_created_123",
        customer_id="cus_created_123",
        price_id="price_test_123",
    )

    _handle_subscription_event(subscription, "evt_test_123")

    bp = BillingProfile.objects.get(user=user)
    assert bp.stripe_customer_id == "cus_created_123"
    assert bp.stripe_subscription_id == "sub_created_123"
    assert bp.status == "active"
    assert bp.is_active is True
    assert bp.current_period_end is not None


# ====================================================
# 2. updated(canceled) → 非アクティブになる
# ====================================================

@pytest.mark.django_db
def test_handle_subscription_updated_to_canceled_makes_profile_inactive(user, monkeypatch):
    monkeypatch.setattr("apps.billing.views.STRIPE_PRICE_ID", "price_test_123")

    # まず active 状態の BillingProfile を用意
    bp = BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_update_123",
        stripe_subscription_id="sub_update_123",
        status="active",
    )

    subscription = _build_subscription_payload(
        user_id=user.id,
        status="canceled",
        subscription_id="sub_update_123",
        customer_id="cus_update_123",
        price_id="price_test_123",
    )

    _handle_subscription_event(subscription, "evt_test_123")

    bp.refresh_from_db()
    assert bp.status == "canceled"
    assert bp.is_active is False


# ====================================================
# 3. deleted → 非アクティブになる（ここでは status を確認）
# ====================================================

@pytest.mark.django_db
def test_handle_subscription_deleted_makes_profile_inactive(user, monkeypatch):
    monkeypatch.setattr("apps.billing.views.STRIPE_PRICE_ID", "price_test_123")

    bp = BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_delete_123",
        stripe_subscription_id="sub_delete_123",
        status="active",
    )

    subscription = _build_subscription_payload(
        user_id=user.id,
        status="canceled",  # deleted イベントでも status は canceled などになる
        subscription_id="sub_delete_123",
        customer_id="cus_delete_123",
        price_id="price_test_123",
    )

    _handle_subscription_event(subscription, "evt_test_123")

    bp.refresh_from_db()
    assert bp.status == "canceled"
    assert bp.is_active is False


# ====================================================
# 4. 同じ subscription を2回処理しても壊れない（冪等性）
# ====================================================

@pytest.mark.django_db
def test_handle_subscription_is_idempotent_for_same_subscription(user, monkeypatch):
    monkeypatch.setattr("apps.billing.views.STRIPE_PRICE_ID", "price_test_123")

    subscription = _build_subscription_payload(
        user_id=user.id,
        status="active",
        subscription_id="sub_repeat_123",
        customer_id="cus_repeat_123",
        price_id="price_test_123",
    )

    # 1回目
    _handle_subscription_event(subscription, "evt_test_123")
    # 2回目（重複）
    _handle_subscription_event(subscription, "evt_test_123")

    bp_list = BillingProfile.objects.filter(user=user)
    assert bp_list.count() == 1

    bp = bp_list.first()
    assert bp.stripe_subscription_id == "sub_repeat_123"
    assert bp.status == "active"
    assert bp.is_active is True


# 動作確認用・お守り的なテスト（残しておいてOK）
@pytest.mark.django_db
def test_pytest_django_is_working():
    assert User.objects.count() >= 0