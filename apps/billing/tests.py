# apps/billing/tests.py

import time

import pytest
from django.contrib.auth import get_user_model

from apps.billing.models import BillingProfile, ProcessedEvent
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
    monkeypatch.setattr("apps.billing.views.STRIPE_PRICE_ID", "price_test_123")

    subscription = _build_subscription_payload(
        user_id=user.id,
        status="active",
        subscription_id="sub_created_123",
        customer_id="cus_created_123",
        price_id="price_test_123",
    )

    _handle_subscription_event(subscription, "evt_test_001", int(time.time()))

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

    _handle_subscription_event(subscription, "evt_test_002", int(time.time()))

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
        status="canceled",
        subscription_id="sub_delete_123",
        customer_id="cus_delete_123",
        price_id="price_test_123",
    )

    _handle_subscription_event(subscription, "evt_test_003", int(time.time()))

    bp.refresh_from_db()
    assert bp.status == "canceled"
    assert bp.is_active is False


# ====================================================
# 4. 同じ event_id を2回処理 → 重複排除（冪等性）
# ====================================================

@pytest.mark.django_db
def test_duplicate_event_id_is_rejected(user, monkeypatch):
    monkeypatch.setattr("apps.billing.views.STRIPE_PRICE_ID", "price_test_123")

    # 1回目: active で処理
    sub_active = _build_subscription_payload(
        user_id=user.id,
        status="active",
        subscription_id="sub_dup_123",
        customer_id="cus_dup_123",
        price_id="price_test_123",
    )
    _handle_subscription_event(sub_active, "evt_dup_001", int(time.time()))

    bp = BillingProfile.objects.get(user=user)
    assert bp.status == "active"

    # 2回目: 同じ event_id で canceled を送信（重複なのでスキップされるべき）
    sub_canceled = _build_subscription_payload(
        user_id=user.id,
        status="canceled",
        subscription_id="sub_dup_123",
        customer_id="cus_dup_123",
        price_id="price_test_123",
    )
    _handle_subscription_event(sub_canceled, "evt_dup_001", int(time.time()))

    # ProcessedEvent は1件のみ
    assert ProcessedEvent.objects.filter(event_id="evt_dup_001").count() == 1

    # BillingProfile は active のまま（2回目は無視）
    bp.refresh_from_db()
    assert bp.status == "active"


# ====================================================
# 5. 順不同ガード: 古いイベントで上書きされない
# ====================================================

@pytest.mark.django_db
def test_out_of_order_event_does_not_overwrite(user, monkeypatch):
    monkeypatch.setattr("apps.billing.views.STRIPE_PRICE_ID", "price_test_123")

    # 新しいイベント (event_created=2000): canceled
    sub_new = _build_subscription_payload(
        user_id=user.id,
        status="canceled",
        subscription_id="sub_ooo_123",
        customer_id="cus_ooo_123",
        price_id="price_test_123",
    )
    _handle_subscription_event(sub_new, "evt_ooo_002", 2000)

    bp = BillingProfile.objects.get(user=user)
    assert bp.status == "canceled"
    assert bp.last_stripe_event_created == 2000

    # 古いイベント (event_created=1000): active（遅延到着）
    sub_old = _build_subscription_payload(
        user_id=user.id,
        status="active",
        subscription_id="sub_ooo_123",
        customer_id="cus_ooo_123",
        price_id="price_test_123",
    )
    _handle_subscription_event(sub_old, "evt_ooo_001", 1000)

    # status は canceled のまま（古いイベントは無視）
    bp.refresh_from_db()
    assert bp.status == "canceled"
    assert bp.is_active is False
    assert bp.last_stripe_event_created == 2000


# ====================================================
# 6. MultipleObjectsReturned で fail-closed（None返却）
# ====================================================

@pytest.mark.django_db
def test_multiple_objects_returned_is_handled_safely(user, monkeypatch):
    """stripe_customer_id 重複時、_find_user_for_subscription が None を返す。"""
    from unittest.mock import patch

    monkeypatch.setattr("apps.billing.views.STRIPE_PRICE_ID", "price_test_123")

    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_multi_123",
        stripe_subscription_id="sub_multi_123",
        status="active",
    )

    # metadata に user_id がないサブスクリプション（customer_id フォールバック経路）
    subscription = {
        "id": "sub_multi_new",
        "status": "canceled",
        "customer": "cus_multi_123",
        "current_period_end": 9999999999,
        "metadata": {},  # user_id なし → customer_id で検索
        "items": {"data": [{"price": {"id": "price_test_123"}}]},
    }

    # BillingProfile.objects.get が MultipleObjectsReturned を返すようモック
    with patch.object(
        BillingProfile.objects, "get",
        side_effect=BillingProfile.MultipleObjectsReturned,
    ):
        from apps.billing.views import _find_user_for_subscription
        result = _find_user_for_subscription(subscription, "cus_multi_123")
        assert result is None


# 動作確認用・お守り的なテスト（残しておいてOK）
@pytest.mark.django_db
def test_pytest_django_is_working():
    assert User.objects.count() >= 0
