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


# ---------------------------------------------------------------------------
# パスワードリセット（Django 標準ビュー）
# ---------------------------------------------------------------------------

PASSWORD_RESET_URL = "/accounts/password-reset/"


@pytest.mark.django_db
def test_login_page_has_password_reset_link(client):
    """ログイン画面に「パスワードを忘れた方」リンクが表示される"""
    resp = client.get(LOGIN_URL)

    assert resp.status_code == 200
    assert PASSWORD_RESET_URL in resp.content.decode()


@pytest.mark.django_db
def test_password_reset_page_renders(client):
    """リセット申請フォームが表示される"""
    resp = client.get(PASSWORD_RESET_URL)

    assert resp.status_code == 200


@pytest.mark.django_db
def test_password_reset_sends_email_for_existing_user(client, cleared_cache):
    """登録済みメールアドレスにはリセットメールが送信される"""
    from django.core import mail

    User.objects.create_user(email="reset-me@example.com", password="oldpass123")

    resp = client.post(PASSWORD_RESET_URL, {"email": "reset-me@example.com"})

    assert resp.status_code == 302
    assert resp.url == "/accounts/password-reset/done/"
    assert len(mail.outbox) == 1
    assert "reset-me@example.com" in mail.outbox[0].to
    assert "/accounts/reset/" in mail.outbox[0].body


@pytest.mark.django_db
def test_password_reset_unknown_email_no_enumeration(client, cleared_cache):
    """未登録メールでも同じ画面に遷移する（メールアドレス列挙の防止）"""
    from django.core import mail

    resp = client.post(PASSWORD_RESET_URL, {"email": "nobody@example.com"})

    assert resp.status_code == 302
    assert resp.url == "/accounts/password-reset/done/"
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_password_reset_full_flow_allows_login_with_new_password(client, cleared_cache):
    """メール内リンクから新パスワードを設定し、ログインできる（E2E フロー）"""
    import re

    from django.core import mail

    user = User.objects.create_user(email="flow@example.com", password="oldpass123")

    # 1. リセット申請 → メール送信
    client.post(PASSWORD_RESET_URL, {"email": "flow@example.com"})
    assert len(mail.outbox) == 1

    # 2. メール本文からリセットリンクを抽出
    match = re.search(r"(/accounts/reset/[^/]+/[^/]+/)", mail.outbox[0].body)
    assert match, "リセットリンクがメール本文に見つからない"
    reset_path = match.group(1)

    # 3. リンクにアクセス（Django はトークンをセッションに保存してリダイレクトする）
    resp = client.get(reset_path)
    assert resp.status_code == 302
    set_password_path = resp.url

    # 4. 新パスワードを設定
    resp = client.post(
        set_password_path,
        {"new_password1": "NewStrongPass1!", "new_password2": "NewStrongPass1!"},
    )
    assert resp.status_code == 302
    assert resp.url == "/accounts/reset/done/"

    # 5. 新パスワードでログインできる
    user.refresh_from_db()
    assert user.check_password("NewStrongPass1!")

    resp = client.post(
        LOGIN_URL, {"email": "flow@example.com", "password": "NewStrongPass1!"}
    )
    assert resp.status_code == 302


@pytest.mark.django_db
def test_password_reset_confirm_invalid_token_shows_expired(client):
    """無効なトークンでは再申請への導線が表示される"""
    resp = client.get("/accounts/reset/Mg/invalid-token/")

    assert resp.status_code == 200
    assert PASSWORD_RESET_URL in resp.content.decode()


# ---------------------------------------------------------------------------
# パスワードリセット IP レートリミット（W-a）
# ---------------------------------------------------------------------------

PASSWORD_RESET_DONE_URL = "/accounts/password-reset/done/"


def _post_password_reset(email, remote_addr):
    """毎回新規クライアントで REMOTE_ADDR を指定して申請する"""
    c = Client()
    return c.post(PASSWORD_RESET_URL, {"email": email}, REMOTE_ADDR=remote_addr)


@pytest.mark.django_db
@override_settings(TRUSTED_PROXY_COUNT=0)
def test_password_reset_rate_limit_allows_within_limit(cleared_cache):
    """制限内（5回/時）はすべてメールが送信される"""
    from django.core import mail

    User.objects.create_user(email="rl-reset1@example.com", password="oldpass123")

    for i in range(5):
        resp = _post_password_reset("rl-reset1@example.com", remote_addr="10.0.0.1")
        assert resp.status_code == 302, f"unexpected status at attempt {i + 1}"
        assert resp.url == PASSWORD_RESET_DONE_URL

    assert len(mail.outbox) == 5


@pytest.mark.django_db
@override_settings(TRUSTED_PROXY_COUNT=0)
def test_password_reset_rate_limit_blocks_after_limit(cleared_cache):
    """制限超過後はメールを送らず、通常と同じ done 画面へ遷移する"""
    from django.core import mail

    User.objects.create_user(email="rl-reset2@example.com", password="oldpass123")

    for _ in range(5):
        _post_password_reset("rl-reset2@example.com", remote_addr="10.0.0.2")
    assert len(mail.outbox) == 5

    resp = _post_password_reset("rl-reset2@example.com", remote_addr="10.0.0.2")
    assert resp.status_code == 302
    assert resp.url == PASSWORD_RESET_DONE_URL  # 429 ではなく通常の done 画面
    assert len(mail.outbox) == 5  # 追加送信されない


@pytest.mark.django_db
@override_settings(TRUSTED_PROXY_COUNT=0)
def test_password_reset_rate_limit_no_enumeration_difference(cleared_cache):
    """制限超過時、登録済み/未登録メールで応答に差がない（列挙防止）"""
    from django.core import mail

    User.objects.create_user(email="rl-reset3@example.com", password="oldpass123")

    for _ in range(5):
        _post_password_reset("rl-reset3@example.com", remote_addr="10.0.0.3")

    resp_known = _post_password_reset(
        "rl-reset3@example.com", remote_addr="10.0.0.3"
    )
    resp_unknown = _post_password_reset(
        "nobody-rl@example.com", remote_addr="10.0.0.3"
    )

    assert resp_known.status_code == resp_unknown.status_code == 302
    assert resp_known.url == resp_unknown.url == PASSWORD_RESET_DONE_URL
    assert len(mail.outbox) == 5


@pytest.mark.django_db
@override_settings(TRUSTED_PROXY_COUNT=0)
def test_password_reset_rate_limit_different_ips_independent(cleared_cache):
    """IP が異なれば別カウントで、制限に達しない IP からは送信される"""
    from django.core import mail

    User.objects.create_user(email="rl-reset4@example.com", password="oldpass123")

    for _ in range(5):
        _post_password_reset("rl-reset4@example.com", remote_addr="10.0.0.4")
    assert len(mail.outbox) == 5

    resp = _post_password_reset("rl-reset4@example.com", remote_addr="10.0.0.5")
    assert resp.status_code == 302
    assert len(mail.outbox) == 6
