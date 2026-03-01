# apps/common/tests.py

from datetime import timedelta
from urllib.parse import urlparse, parse_qs

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import RequestFactory, override_settings
from django.utils import timezone

from apps.billing.models import BillingProfile
from apps.common.utils import get_client_ip

User = get_user_model()


@pytest.mark.django_db
def test_app_access_redirects_when_not_logged_in(client):
    """
    未ログイン状態で /app/ にアクセスすると
    LOGIN_URL に next パラメータ付きでリダイレクトされる
    """
    response = client.get("/app/")

    assert response.status_code == 302

    # 実際の LOGIN_URL（通常は /accounts/login/）を使って比較
    parsed = urlparse(response.url)
    qs = parse_qs(parsed.query)

    expected_login_path = urlparse(settings.LOGIN_URL).path or settings.LOGIN_URL
    assert parsed.path == expected_login_path

    # next=/app/ がクエリに入っていること（URLエンコードは pytest 側でデコード）
    assert qs.get("next") == ["/app/"]


@pytest.mark.django_db
def test_app_access_allowed_during_free_period(client):
    """
    ログイン済み & free期間内なら /app/ にアクセス可能
    """
    user = User.objects.create_user(
        email="free@example.com",
        password="password123",
    )

    profile = user.profile
    profile.free_until = timezone.now() + timedelta(days=3)
    profile.save()

    client.force_login(user)
    response = client.get("/app/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_app_access_allowed_when_subscription_active_after_free_period(client):
    """
    free期間が終わっていても、有効なサブスクリプションがあれば /app/ にアクセス可能
    """
    user = User.objects.create_user(
        email="active-sub@example.com",
        password="password123",
    )

    profile = user.profile
    profile.free_until = timezone.now() - timedelta(days=1)
    profile.save()

    BillingProfile.objects.create(
        user=user,
        stripe_customer_id="cus_active_123",
        stripe_subscription_id="sub_active_123",
        status="active",  # BillingProfile.is_active が True になる状態
    )

    client.force_login(user)
    response = client.get("/app/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_app_access_redirects_to_pricing_when_free_expired_and_not_subscribed(client):
    """
    free期間が終了していて、サブスクリプションも active でない場合は
    /billing/pricing( / ) にリダイレクトされる
    """
    user = User.objects.create_user(
        email="no-sub@example.com",
        password="password123",
    )

    profile = user.profile
    profile.free_until = timezone.now() - timedelta(days=1)
    profile.save()

    client.force_login(user)
    response = client.get("/app/")

    assert response.status_code == 302
    # 末尾スラッシュ有無の両方を許可
    assert response.url in ("/billing/pricing", "/billing/pricing/")


@pytest.mark.django_db
def test_app_access_no_500_when_profile_missing(client):
    """
    Profile が存在しないユーザーで /app/ にアクセスしても
    500 にならず /billing/pricing にリダイレクトされる
    """
    user = User.objects.create_user(
        email="no-profile@example.com",
        password="password123",
    )

    # signal で自動作成された Profile を削除
    user.profile.delete()

    client.force_login(user)
    response = client.get("/app/")

    assert response.status_code == 302
    assert response.url in ("/billing/pricing", "/billing/pricing/")


@pytest.mark.django_db
def test_app_access_no_500_when_billing_profile_missing(client):
    """
    BillingProfile が存在しない & free期間切れのユーザーで /app/ にアクセスしても
    500 にならず /billing/pricing にリダイレクトされる
    """
    user = User.objects.create_user(
        email="no-billing@example.com",
        password="password123",
    )

    profile = user.profile
    profile.free_until = timezone.now() - timedelta(days=1)
    profile.save()

    # BillingProfile は作成しない

    client.force_login(user)
    response = client.get("/app/")

    assert response.status_code == 302
    assert response.url in ("/billing/pricing", "/billing/pricing/")


@pytest.mark.django_db
def test_whitelisted_paths_are_not_blocked(client):
    """
    ホーム / は paywall の対象外（/app/ 以外はこの middleware ではブロックしない）
    """
    response = client.get("/")

    # 少なくとも login や billing/pricing にリダイレクトされていないことを確認
    if response.status_code == 302:
        assert not response.url.startswith("/accounts/login")
        assert not response.url.startswith("/billing/pricing")


# ---------------------------------------------------------------------------
# get_client_ip ユニットテスト
# ---------------------------------------------------------------------------

@pytest.fixture
def rf():
    return RequestFactory()


@override_settings(TRUSTED_PROXY_COUNT=0)
def test_get_client_ip_no_proxy_returns_remote_addr(rf):
    """TRUSTED_PROXY_COUNT=0 では REMOTE_ADDR をそのまま返す"""
    req = rf.get("/", REMOTE_ADDR="1.2.3.4")
    assert get_client_ip(req) == "1.2.3.4"


@override_settings(TRUSTED_PROXY_COUNT=1)
def test_get_client_ip_single_xff_entry(rf):
    """XFF が 1 エントリ、TRUSTED_PROXY_COUNT=1 → XFF の値を返す"""
    req = rf.get("/", REMOTE_ADDR="proxy", HTTP_X_FORWARDED_FOR="9.9.9.9")
    assert get_client_ip(req) == "9.9.9.9"


@override_settings(TRUSTED_PROXY_COUNT=1)
def test_get_client_ip_xff_spoofed_prefix_is_ignored(rf):
    """クライアントが XFF 先頭に偽装 IP を挿入しても、右から N 番目を返す"""
    req = rf.get("/", REMOTE_ADDR="proxy", HTTP_X_FORWARDED_FOR="evil, 9.9.9.9")
    assert get_client_ip(req) == "9.9.9.9"


@override_settings(TRUSTED_PROXY_COUNT=2)
def test_get_client_ip_trusted_exceeds_xff_falls_back_to_remote_addr(rf):
    """XFF エントリ数 < TRUSTED_PROXY_COUNT → fail-open を避け REMOTE_ADDR にフォールバック"""
    req = rf.get("/", REMOTE_ADDR="1.2.3.4", HTTP_X_FORWARDED_FOR="9.9.9.9")
    # ips=["9.9.9.9"] (1 entry) < trusted=2 → REMOTE_ADDR を返す
    assert get_client_ip(req) == "1.2.3.4"


@override_settings(TRUSTED_PROXY_COUNT=1)
def test_get_client_ip_no_xff_falls_back_to_remote_addr(rf):
    """XFF ヘッダーがない場合は REMOTE_ADDR にフォールバック"""
    req = rf.get("/", REMOTE_ADDR="1.2.3.4")
    assert get_client_ip(req) == "1.2.3.4"


@override_settings(TRUSTED_PROXY_COUNT=1)
def test_get_client_ip_xff_empty_entries_are_ignored(rf):
    """XFF に空要素が含まれても空文字を返さない（例: 'a,,b' や ', 9.9.9.9'）"""
    req = rf.get("/", REMOTE_ADDR="proxy", HTTP_X_FORWARDED_FOR=", 9.9.9.9")
    # ips（空除外後）= ["9.9.9.9"], len=1 == trusted=1 → "9.9.9.9"
    assert get_client_ip(req) == "9.9.9.9"
    assert get_client_ip(req) != ""