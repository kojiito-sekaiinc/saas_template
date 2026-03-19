# apps/billing/test_sync.py
"""
sync_billing_from_stripe のテスト。

受け入れ条件:
- subscription_id で同期できる
- customer_id fallback が動く
- dry-run が DB を書き換えない
- 差分が正しく出る
- last_stripe_event_created が変更されない
"""
import time
from datetime import datetime, timezone as dt_timezone
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model

from apps.billing.models import BillingProfile
from apps.billing.services import (
    diff_billing_profile,
    get_stripe_billing_state,
    sync_billing_profile_from_stripe,
)

User = get_user_model()

# ---------------------------------------------------------------------------
# フィクスチャ
# ---------------------------------------------------------------------------

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="sync-test@example.com",
        password="password123",
    )


@pytest.fixture
def billing_profile(user):
    return BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_sync_test",
        stripe_subscription_id="sub_sync_test",
        status="not_subscribed",
        last_stripe_event_created=9999,  # この値が変わらないことを確認する
    )


def _make_stripe_subscription(
    sub_id="sub_sync_test",
    customer_id="cus_sync_test",
    status="active",
    price_id="price_test_sync",
    period_end: int | None = None,
) -> MagicMock:
    """Stripe Subscription オブジェクトのモックを作る。"""
    sub = MagicMock()
    sub.get = lambda key, default=None: {
        "id": sub_id,
        "customer": customer_id,
        "status": status,
        "current_period_end": period_end or (int(time.time()) + 3600),
        "items": {"data": [{"price": {"id": price_id}}]},
    }.get(key, default)
    return sub


# ---------------------------------------------------------------------------
# 1. subscription_id で同期できる
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_sync_via_subscription_id_updates_status(billing_profile, monkeypatch):
    """subscription_id 直接取得で status が更新される。"""
    monkeypatch.setattr("django.conf.settings.STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr("django.conf.settings.STRIPE_PRICE_ID", "price_test_sync")

    mock_sub = _make_stripe_subscription(status="active")

    with patch("stripe.Subscription.retrieve", return_value=mock_sub):
        result = sync_billing_profile_from_stripe(billing_profile)

    billing_profile.refresh_from_db()
    assert billing_profile.status == "active"
    assert result["updated"] is True
    assert result["stripe_state"]["source"] == "subscription_id"


# ---------------------------------------------------------------------------
# 2. customer_id fallback が動く
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_sync_falls_back_to_customer_id_when_subscription_not_found(
    billing_profile, monkeypatch
):
    """subscription_id が Stripe に存在しない場合、customer_id から検索する。"""
    import stripe as stripe_mod

    monkeypatch.setattr("django.conf.settings.STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr("django.conf.settings.STRIPE_PRICE_ID", "price_test_sync")

    mock_sub = _make_stripe_subscription(status="past_due")
    mock_list = MagicMock()
    mock_list.get = lambda key, default=None: (
        [mock_sub] if key == "data" else default
    )

    with patch(
        "stripe.Subscription.retrieve",
        side_effect=stripe_mod.InvalidRequestError("No such subscription", param="id"),
    ), patch("stripe.Subscription.list", return_value=mock_list):
        result = sync_billing_profile_from_stripe(billing_profile)

    billing_profile.refresh_from_db()
    assert billing_profile.status == "past_due"
    assert result["stripe_state"]["source"] == "customer_id"


# ---------------------------------------------------------------------------
# 3. dry-run が DB を書き換えない
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_dry_run_does_not_update_db(billing_profile, monkeypatch):
    """dry_run=True の場合、差分があっても DB は更新されない。"""
    monkeypatch.setattr("django.conf.settings.STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr("django.conf.settings.STRIPE_PRICE_ID", "price_test_sync")

    mock_sub = _make_stripe_subscription(status="active")

    with patch("stripe.Subscription.retrieve", return_value=mock_sub):
        result = sync_billing_profile_from_stripe(billing_profile, dry_run=True)

    billing_profile.refresh_from_db()
    assert billing_profile.status == "not_subscribed"  # DB は変わらない
    assert result["updated"] is False
    assert result["dry_run"] is True
    assert "status" in result["diffs"]  # 差分は検出されている


# ---------------------------------------------------------------------------
# 4. 差分が正しく出る
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_diff_billing_profile_returns_changed_fields(billing_profile):
    """diff_billing_profile が変更フィールドのみ返す。"""
    new_end = datetime(2030, 1, 1, tzinfo=dt_timezone.utc)
    stripe_state = {
        "found": True,
        "stripe_customer_id": "cus_sync_test",       # 変化なし
        "stripe_subscription_id": "sub_sync_test",   # 変化なし
        "status": "active",                           # not_subscribed → active
        "current_period_end": new_end,                # None → datetime
        "source": "subscription_id",
    }

    diffs = diff_billing_profile(billing_profile, stripe_state)

    assert "status" in diffs
    assert diffs["status"]["before"] == "not_subscribed"
    assert diffs["status"]["after"] == "active"
    assert "current_period_end" in diffs
    # 変化のないフィールドは含まれない
    assert "stripe_customer_id" not in diffs
    assert "stripe_subscription_id" not in diffs


@pytest.mark.django_db
def test_diff_billing_profile_returns_empty_when_no_change(billing_profile, monkeypatch):
    """状態が同一なら空の dict を返す。"""
    monkeypatch.setattr("django.conf.settings.STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr("django.conf.settings.STRIPE_PRICE_ID", "price_test_sync")

    # DB と同じ状態を Stripe が返す
    billing_profile.status = "active"
    billing_profile.save()

    stripe_state = {
        "found": True,
        "stripe_customer_id": billing_profile.stripe_customer_id,
        "stripe_subscription_id": billing_profile.stripe_subscription_id,
        "status": "active",
        "current_period_end": billing_profile.current_period_end,
        "source": "subscription_id",
    }

    diffs = diff_billing_profile(billing_profile, stripe_state)
    assert diffs == {}


# ---------------------------------------------------------------------------
# 5. last_stripe_event_created が変更されない
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_last_stripe_event_created_is_not_modified(billing_profile, monkeypatch):
    """同期後も last_stripe_event_created は元の値のまま。"""
    monkeypatch.setattr("django.conf.settings.STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr("django.conf.settings.STRIPE_PRICE_ID", "price_test_sync")

    original_value = billing_profile.last_stripe_event_created  # 9999

    mock_sub = _make_stripe_subscription(status="active")

    with patch("stripe.Subscription.retrieve", return_value=mock_sub):
        sync_billing_profile_from_stripe(billing_profile)

    billing_profile.refresh_from_db()
    assert billing_profile.last_stripe_event_created == original_value


# ---------------------------------------------------------------------------
# 6. subscription が見つからない場合は not_subscribed になる
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_sync_sets_not_subscribed_when_no_subscription_found(
    billing_profile, monkeypatch
):
    """Stripe にサブスクリプションが見つからない場合、status が not_subscribed になる。"""
    import stripe as stripe_mod

    monkeypatch.setattr("django.conf.settings.STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr("django.conf.settings.STRIPE_PRICE_ID", "price_test_sync")

    # sub 取得失敗 → list も空
    mock_list = MagicMock()
    mock_list.get = lambda key, default=None: [] if key == "data" else default

    billing_profile.status = "active"
    billing_profile.save()

    with patch(
        "stripe.Subscription.retrieve",
        side_effect=stripe_mod.InvalidRequestError("no such subscription", param="id"),
    ), patch("stripe.Subscription.list", return_value=mock_list):
        result = sync_billing_profile_from_stripe(billing_profile)

    billing_profile.refresh_from_db()
    assert billing_profile.status == "not_subscribed"
    assert result["stripe_state"]["source"] == "none"


# ---------------------------------------------------------------------------
# 7. management command: dry-run 出力に WOULD_UPDATE が含まれる
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_management_command_dry_run_outputs_would_update(
    billing_profile, monkeypatch
):
    from io import StringIO
    from django.core.management import call_command

    monkeypatch.setattr("django.conf.settings.STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr("django.conf.settings.STRIPE_PRICE_ID", "price_test_sync")

    mock_sub = _make_stripe_subscription(status="active")

    out = StringIO()
    with patch("stripe.Subscription.retrieve", return_value=mock_sub):
        call_command(
            "sync_billing_from_stripe",
            user_id=billing_profile.user_id,
            dry_run=True,
            stdout=out,
        )

    output = out.getvalue()
    assert "WOULD_UPDATE" in output
    billing_profile.refresh_from_db()
    assert billing_profile.status == "not_subscribed"  # DB は更新されない


# ---------------------------------------------------------------------------
# 8. management command: 実際に更新されると UPDATED が出る
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_management_command_outputs_updated(billing_profile, monkeypatch):
    from io import StringIO
    from django.core.management import call_command

    monkeypatch.setattr("django.conf.settings.STRIPE_SECRET_KEY", "sk_test_xxx")
    monkeypatch.setattr("django.conf.settings.STRIPE_PRICE_ID", "price_test_sync")

    mock_sub = _make_stripe_subscription(status="active")

    out = StringIO()
    with patch("stripe.Subscription.retrieve", return_value=mock_sub):
        call_command(
            "sync_billing_from_stripe",
            user_id=billing_profile.user_id,
            stdout=out,
        )

    output = out.getvalue()
    assert "UPDATED" in output
    billing_profile.refresh_from_db()
    assert billing_profile.status == "active"
