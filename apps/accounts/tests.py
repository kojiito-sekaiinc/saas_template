"""
apps/accounts/tests.py

認証・サインアップ・レートリミット・オープンリダイレクトのテスト。
スタイル: 純 pytest（TestCase 不使用）。
"""
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, override_settings

User = get_user_model()

LOGIN_URL = "/accounts/login/"
SIGNUP_URL = "/accounts/signup/"


# ---------------------------------------------------------------------------
# ログインロックアウト（django-axes）
# ---------------------------------------------------------------------------

@pytest.mark.django_db
@override_settings(AXES_FAILURE_LIMIT=5, AXES_COOLOFF_TIME=1, AXES_RESET_ON_SUCCESS=True)
def test_login_lockout_after_max_failures(client):
    """5回失敗後、正しいパスワードでもログイン不可"""
    User.objects.create_user(email="lock@example.com", password="Correct!Pass1")

    def attempt(password="wrong"):
        return client.post(LOGIN_URL, {"email": "lock@example.com", "password": password})

    for _ in range(settings.AXES_FAILURE_LIMIT):
        resp = attempt()
        assert resp.status_code in (200, 429)

    resp = attempt(password="Correct!Pass1")
    assert resp.status_code == 429
    assert not resp.wsgi_request.user.is_authenticated


@pytest.mark.django_db
@override_settings(AXES_FAILURE_LIMIT=5, AXES_COOLOFF_TIME=1, AXES_RESET_ON_SUCCESS=True)
def test_lockout_is_per_email(client):
    """ロックアウトはメールアドレス単位。別ユーザーに波及しない"""
    User.objects.create_user(email="lock@example.com", password="Correct!Pass1")
    User.objects.create_user(email="other@example.com", password="Correct!Pass1")

    def attempt(email, password="wrong"):
        return client.post(LOGIN_URL, {"email": email, "password": password})

    for _ in range(settings.AXES_FAILURE_LIMIT):
        attempt("lock@example.com")

    resp_a = attempt("lock@example.com", password="Correct!Pass1")
    assert resp_a.status_code == 429

    resp_b = attempt("other@example.com")
    assert resp_b.status_code != 429


# ---------------------------------------------------------------------------
# メール列挙防止
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_signup_does_not_reveal_existing_email(client):
    """エラーメッセージに 'registered' が含まれない"""
    User.objects.create_user(email="existing@example.com", password="TestPass123!")
    resp = client.post(
        SIGNUP_URL,
        {
            "email": "existing@example.com",
            "password": "AnotherPass1!",
            "password_confirm": "AnotherPass1!",
        },
    )
    assert resp.status_code == 200
    content = resp.content.decode()
    assert "registered" not in content.lower()
    assert "Unable to register with this email" in content


# ---------------------------------------------------------------------------
# サインアップ・ログイン成功
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_successful_signup_creates_user_and_redirects(client):
    """正常なサインアップでユーザー作成・リダイレクト"""
    resp = client.post(
        SIGNUP_URL,
        {
            "email": "new@example.com",
            "password": "StrongPass1!",
            "password_confirm": "StrongPass1!",
        },
    )
    assert resp.status_code == 302
    assert User.objects.filter(email="new@example.com").exists()


@pytest.mark.django_db
def test_successful_login_redirects(client):
    """正常なログインでデフォルト URL にリダイレクト"""
    User.objects.create_user(email="login@example.com", password="TestPass1!")
    resp = client.post(LOGIN_URL, {"email": "login@example.com", "password": "TestPass1!"})
    assert resp.status_code == 302
    assert resp.url == settings.LOGIN_REDIRECT_URL


@pytest.mark.django_db
def test_successful_login_with_next_url(client):
    """next パラメータ付きログインで指定 URL にリダイレクト"""
    User.objects.create_user(email="next@example.com", password="TestPass1!")
    resp = client.post(
        f"{LOGIN_URL}?next=/app/dashboard/",
        {"email": "next@example.com", "password": "TestPass1!"},
    )
    assert resp.status_code == 302
    assert resp.url == "/app/dashboard/"


# ---------------------------------------------------------------------------
# サインアップ IP レートリミット
# ---------------------------------------------------------------------------

_VALID_POST = {
    "email": "ratelimit@example.com",
    "password": "StrongPass1!",
    "password_confirm": "StrongPass1!",
}


@pytest.fixture
def cleared_cache():
    """テスト前後でレートリミットキャッシュをクリアする"""
    cache.clear()
    yield
    cache.clear()


def _post_signup(email_suffix=0, remote_addr="1.2.3.4", xff=None):
    """毎回新規クライアントを使い、ログイン状態が持ち越されないようにする"""
    c = Client()
    kwargs = {"REMOTE_ADDR": remote_addr}
    if xff is not None:
        kwargs["HTTP_X_FORWARDED_FOR"] = xff
    return c.post(
        SIGNUP_URL,
        {**_VALID_POST, "email": f"u{email_suffix}@example.com"},
        **kwargs,
    )


@pytest.mark.django_db
@override_settings(TRUSTED_PROXY_COUNT=0)
def test_signup_rate_limit_blocks_after_limit(cleared_cache):
    """10回ポスト後に 429 が返ること"""
    for i in range(10):
        resp = _post_signup(email_suffix=i, remote_addr="1.2.3.4")
        assert resp.status_code != 429, f"blocked too early at attempt {i + 1}"

    resp = _post_signup(email_suffix=99, remote_addr="1.2.3.4")
    assert resp.status_code == 429


@pytest.mark.django_db
@override_settings(TRUSTED_PROXY_COUNT=0)
def test_signup_rate_limit_different_ips_independent(cleared_cache):
    """IP が異なれば別カウント（TRUSTED_PROXY_COUNT=0 で REMOTE_ADDR を使用）"""
    for i in range(10):
        _post_signup(email_suffix=i, remote_addr="1.2.3.4")

    resp = _post_signup(email_suffix=50, remote_addr="5.6.7.8")
    assert resp.status_code != 429


@pytest.mark.django_db
@override_settings(TRUSTED_PROXY_COUNT=1)
def test_signup_rate_limit_xff_with_trusted_proxy(cleared_cache):
    """TRUSTED_PROXY_COUNT=1 設定時、XFF の正規化 IP でカウントされること"""
    for i in range(10):
        resp = _post_signup(
            email_suffix=i,
            remote_addr="proxy.railway.internal",
            xff="9.9.9.9",
        )
        assert resp.status_code != 429, f"blocked too early at attempt {i + 1}"

    resp = _post_signup(
        email_suffix=99,
        remote_addr="proxy.railway.internal",
        xff="9.9.9.9",
    )
    assert resp.status_code == 429


@pytest.mark.django_db
@override_settings(TRUSTED_PROXY_COUNT=1)
def test_signup_xff_spoofing_is_blocked(cleared_cache):
    """TRUSTED_PROXY_COUNT=1 時にクライアントが XFF を偽装しても正しい IP が使われること"""
    # クライアントが "evil_ip" を先頭に挿入するが、プロキシが "real_client" を末尾追加
    # → ips = ["evil_ip", "real_client"], idx = max(0, 2-1) = 1 → "real_client"
    for i in range(10):
        resp = _post_signup(
            email_suffix=i,
            remote_addr="proxy.railway.internal",
            xff="evil_ip, real_client",
        )
        assert resp.status_code != 429, f"blocked too early at attempt {i + 1}"

    resp = _post_signup(
        email_suffix=99,
        remote_addr="proxy.railway.internal",
        xff="evil_ip, real_client",
    )
    assert resp.status_code == 429

    # "evil_ip" 単独では別カウント → まだブロックされない
    cache.clear()
    resp = _post_signup(
        email_suffix=100,
        remote_addr="proxy.railway.internal",
        xff="evil_ip",
    )
    assert resp.status_code != 429


# ---------------------------------------------------------------------------
# オープンリダイレクト防御
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_open_redirect_blocked_on_login(client):
    """ログイン時に外部 URL へのリダイレクトがブロックされる"""
    User.objects.create_user(email="redir@example.com", password="TestPass1!")
    resp = client.post(
        f"{LOGIN_URL}?next=https://evil.com/steal",
        {"email": "redir@example.com", "password": "TestPass1!"},
    )
    assert resp.status_code == 302
    assert resp.url == settings.LOGIN_REDIRECT_URL


@pytest.mark.django_db
def test_open_redirect_blocked_on_signup(client):
    """サインアップ時に外部 URL へのリダイレクトがブロックされる"""
    resp = client.post(
        f"{SIGNUP_URL}?next=https://evil.com/steal",
        {
            "email": "redir-signup@example.com",
            "password": "StrongPass1!",
            "password_confirm": "StrongPass1!",
        },
    )
    assert resp.status_code == 302
    assert "evil.com" not in resp.url
