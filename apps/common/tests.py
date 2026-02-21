# apps/common/tests.py

from datetime import timedelta
from urllib.parse import urlparse, parse_qs

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.billing.models import BillingProfile

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
def test_whitelisted_paths_are_not_blocked(client):
    """
    ホーム / は paywall の対象外（/app/ 以外はこの middleware ではブロックしない）
    """
    response = client.get("/")

    # 少なくとも login や billing/pricing にリダイレクトされていないことを確認
    if response.status_code == 302:
        assert not response.url.startswith("/accounts/login")
        assert not response.url.startswith("/billing/pricing")