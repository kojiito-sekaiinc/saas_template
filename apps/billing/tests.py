# apps/billing/tests.py

import time

import pytest
from django.conf import settings as django_settings
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
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

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
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

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
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

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
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

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
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

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

    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

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


# ====================================================
# 7. active なユーザーが checkout → portal へリダイレクト
# ====================================================

@pytest.mark.django_db
def test_checkout_redirects_to_portal_when_already_active(user, monkeypatch, client):
    monkeypatch.setattr(django_settings, "STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_active_123",
        stripe_subscription_id="sub_active_123",
        status="active",
    )

    client.force_login(user)
    response = client.post("/billing/checkout/")
    assert response.status_code == 302
    assert "/billing/portal/" in response.url


# ====================================================
# 8. checkout が idempotency_key を Stripe に渡す
# ====================================================

@pytest.mark.django_db
def test_checkout_uses_idempotency_key(user, monkeypatch, client):
    from unittest.mock import MagicMock, patch

    monkeypatch.setattr(django_settings, "STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_idem_123",
        status="not_subscribed",
    )

    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/test"

    client.force_login(user)
    with patch("stripe.checkout.Session.create", return_value=mock_session) as mock_create:
        response = client.post("/billing/checkout/")

    assert response.status_code == 302
    call_kwargs = mock_create.call_args[1]
    assert "idempotency_key" in call_kwargs
    assert call_kwargs["idempotency_key"].startswith(f"checkout_{user.id}_")


# ====================================================
# 9. past_due + stripe_subscription_id あり → Portal へリダイレクト
# ====================================================

@pytest.mark.django_db
def test_checkout_redirects_to_portal_when_past_due_with_subscription(
    user, monkeypatch, client
):
    monkeypatch.setattr(django_settings, "STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")

    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_pastdue_123",
        stripe_subscription_id="sub_pastdue_123",
        status="past_due",
    )

    client.force_login(user)
    response = client.post("/billing/checkout/")
    assert response.status_code == 302
    assert "/billing/portal/" in response.url


# ====================================================
# 10. canceled + stripe_subscription_id あり → Checkout 継続（Portal に送らない）
# ====================================================

@pytest.mark.django_db
def test_checkout_proceeds_when_canceled_with_existing_subscription(
    user, monkeypatch, client
):
    """
    canceled は subscription 終了済みなので再購読を Checkout で受け付ける。
    stripe_subscription_id が残っていても Portal には送らない。
    """
    from unittest.mock import MagicMock, patch

    monkeypatch.setattr(django_settings, "STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")
    monkeypatch.setattr(django_settings, "SITE_URL", "http://localhost:8000")

    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_canceled_123",
        stripe_subscription_id="sub_canceled_123",
        status="canceled",
    )

    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/test"

    client.force_login(user)
    with patch("stripe.checkout.Session.create", return_value=mock_session):
        response = client.post("/billing/checkout/")

    assert response.status_code == 302
    assert "checkout.stripe.com" in response.url


# ====================================================
# 12. stripe_customer_id 未設定時に Customer.create() が呼ばれ
#    user スコープの idempotency_key が渡される
# ====================================================

@pytest.mark.django_db
def test_checkout_creates_customer_with_idempotency_key_when_no_customer_exists(
    user, monkeypatch, client
):
    from unittest.mock import MagicMock, patch

    monkeypatch.setattr(django_settings, "STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")
    monkeypatch.setattr(django_settings, "SITE_URL", "http://localhost:8000")

    BillingProfile.objects.create(user=user, status="not_subscribed")

    mock_customer = MagicMock()
    mock_customer.id = "cus_new_123"

    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/test"

    client.force_login(user)
    with patch("stripe.Customer.create", return_value=mock_customer) as mock_create, \
            patch("stripe.checkout.Session.create", return_value=mock_session):
        response = client.post("/billing/checkout/")

    assert response.status_code == 302
    mock_create.assert_called_once()
    call_kwargs = mock_create.call_args[1]
    assert call_kwargs["idempotency_key"] == f"create_customer_{user.id}"

    bp = BillingProfile.objects.get(user=user)
    assert bp.stripe_customer_id == "cus_new_123"


# ====================================================
# 13. フェーズ3で別リクエストが先に stripe_customer_id を保存していた場合、
#     DB 上の既存値を正本として checkout session を作成する
# ====================================================

@pytest.mark.django_db
def test_checkout_uses_db_customer_id_on_concurrent_race(user, monkeypatch, client):
    """
    フェーズ2（Stripe Customer.create）とフェーズ3（DB 保存）の間に
    別リクエストが stripe_customer_id を書き込んだ場合、
    フェーズ3 は DB 上の既存値を正本として採用し、
    checkout session はその値で作成される。
    """
    from unittest.mock import MagicMock, patch

    monkeypatch.setattr(django_settings, "STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr(django_settings, "STRIPE_PRICE_ID", "price_test_123")
    monkeypatch.setattr(django_settings, "SITE_URL", "http://localhost:8000")

    BillingProfile.objects.create(user=user, status="not_subscribed")

    def concurrent_customer_create(**kwargs):
        # 別リクエストが先に stripe_customer_id を書き込んだことをシミュレート
        BillingProfile.objects.filter(user=user).update(
            stripe_customer_id="cus_concurrent_123"
        )
        mock = MagicMock()
        mock.id = "cus_new_999"
        return mock

    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/test"

    client.force_login(user)
    with patch("stripe.Customer.create", side_effect=concurrent_customer_create), \
            patch("stripe.checkout.Session.create", return_value=mock_session) as mock_session_create:
        response = client.post("/billing/checkout/")

    assert response.status_code == 302

    # checkout session は DB 上の既存値（cus_concurrent_123）で作成される
    session_kwargs = mock_session_create.call_args[1]
    assert session_kwargs["customer"] == "cus_concurrent_123"

    # DB の stripe_customer_id は並行リクエストが保存した値のまま
    bp = BillingProfile.objects.get(user=user)
    assert bp.stripe_customer_id == "cus_concurrent_123"


# 動作確認用・お守り的なテスト（残しておいてOK）
@pytest.mark.django_db
def test_pytest_django_is_working():
    assert User.objects.count() >= 0
