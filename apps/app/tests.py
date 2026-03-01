from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

APP_URL = "/app/"

# ---------------------------------------------------------------------------
# アクセス制御の境界テスト
#
# apps/app はサービスごとに差し替える領域だが、Paywall（PaywallMiddleware）に
# よるアクセス制御はテンプレート固定の挙動である。
# ここでは「誰が /app/ にアクセスできるか」という境界だけを検証する。
# サービス固有の機能テストは各サービスの開発者が追記すること。
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_app_dashboard_redirects_when_not_logged_in(client):
    """未ログインで /app/ にアクセスするとログインページにリダイレクト"""
    response = client.get(APP_URL)

    assert response.status_code == 302
    assert "/accounts/login/" in response.url


@pytest.mark.django_db
def test_app_dashboard_accessible_during_free_period(client):
    """無料期間中のログインユーザーは /app/ にアクセスできる"""
    user = User.objects.create_user(email="free@example.com", password="pass")
    user.profile.free_until = timezone.now() + timedelta(days=1)
    user.profile.save()

    client.force_login(user)
    response = client.get(APP_URL)

    assert response.status_code == 200


@pytest.mark.django_db
def test_app_dashboard_redirects_to_pricing_when_paywall_blocks(client):
    """無料期間切れ・未購読のユーザーは /billing/pricing にリダイレクト"""
    user = User.objects.create_user(email="blocked@example.com", password="pass")
    user.profile.free_until = timezone.now() - timedelta(days=1)
    user.profile.save()

    client.force_login(user)
    response = client.get(APP_URL)

    assert response.status_code == 302
    assert response.url in ("/billing/pricing", "/billing/pricing/")
