from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.billing.models import BillingProfile

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


# ---------------------------------------------------------------------------
# テンプレート解決の回帰テスト
#
# /app/customers/ は ui/templates/ 配下の layouts/ components/ に依存する。
# TEMPLATES.DIRS の設定漏れ（例: ui/ 再編時の更新忘れ）があると、認可を
# 通過したユーザーだけが TemplateDoesNotExist で 500 を踏む。
# ページを実際に GET してレンダリングまで通ることを検証する。
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_app_customers_renders_during_free_period(client):
    """無料期間中のユーザーは /app/customers/ が 200 で描画される"""
    user = User.objects.create_user(email="free2@example.com", password="pass")
    user.profile.free_until = timezone.now() + timedelta(days=1)
    user.profile.save()

    client.force_login(user)
    response = client.get("/app/customers/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_app_customers_renders_with_active_subscription(client):
    """課金有効（status=active）のユーザーは /app/customers/ が 200 で描画される"""
    user = User.objects.create_user(email="paid@example.com", password="pass")
    user.profile.free_until = timezone.now() - timedelta(days=1)
    user.profile.save()
    BillingProfile.objects.create(user=user, status="active")

    client.force_login(user)
    response = client.get("/app/customers/")

    assert response.status_code == 200
