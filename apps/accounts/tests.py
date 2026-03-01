from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings

from axes.helpers import get_client_cache_keys

User = get_user_model()


@override_settings(
    AXES_FAILURE_LIMIT=5,
    AXES_COOLOFF_TIME=1,
    AXES_RESET_ON_SUCCESS=True,
)
class LoginLockoutTest(TestCase):
    """django-axes によるログイン試行回数制限のテスト"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="lock@example.com", password="Correct!Pass1"
        )
        self.login_url = "/accounts/login/"

    def _attempt_login(self, email="lock@example.com", password="wrong"):
        return self.client.post(
            self.login_url, {"email": email, "password": password}
        )

    def test_login_lockout_after_max_failures(self):
        """5回失敗後、正しいパスワードでもログイン不可"""
        for i in range(settings.AXES_FAILURE_LIMIT):
            resp = self._attempt_login()
            # axes はロックアウト時に 429 を返す
            self.assertIn(resp.status_code, (200, 429))

        # ロックアウト後: 正しいパスワードでも 429
        resp = self._attempt_login(password="Correct!Pass1")
        self.assertEqual(resp.status_code, 429)
        self.assertFalse(resp.wsgi_request.user.is_authenticated)

    def test_lockout_is_per_email(self):
        """ロックアウトはメールアドレス単位。別ユーザーに波及しない"""
        User.objects.create_user(
            email="other@example.com", password="Correct!Pass1"
        )

        # user_a (lock@example.com) を5回失敗させてロックアウト
        for _ in range(settings.AXES_FAILURE_LIMIT):
            self._attempt_login(email="lock@example.com", password="wrong")

        # user_a はロックアウト済み
        resp_a = self._attempt_login(email="lock@example.com", password="Correct!Pass1")
        self.assertEqual(resp_a.status_code, 429)

        # user_b (other@example.com) は影響を受けない
        resp_b = self._attempt_login(email="other@example.com", password="wrong")
        self.assertNotEqual(resp_b.status_code, 429)


class SignupEmailEnumerationTest(TestCase):
    """signup フォームがメール列挙に利用されないことを確認"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="existing@example.com", password="TestPass123!"
        )
        self.signup_url = "/accounts/signup/"

    def test_signup_does_not_reveal_existing_email(self):
        """エラーメッセージに 'registered' が含まれない"""
        resp = self.client.post(
            self.signup_url,
            {
                "email": "existing@example.com",
                "password": "AnotherPass1!",
                "password_confirm": "AnotherPass1!",
            },
        )
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertNotIn("registered", content.lower())
        self.assertIn("Unable to register with this email", content)


class SignupLoginSuccessTest(TestCase):
    """サインアップ・ログイン成功時のテスト (#9)"""

    def setUp(self):
        self.signup_url = "/accounts/signup/"
        self.login_url = "/accounts/login/"

    def test_successful_signup_creates_user_and_redirects(self):
        """正常なサインアップでユーザー作成・リダイレクト"""
        resp = self.client.post(
            self.signup_url,
            {
                "email": "new@example.com",
                "password": "StrongPass1!",
                "password_confirm": "StrongPass1!",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_successful_login_redirects(self):
        """正常なログインでデフォルトURLにリダイレクト"""
        User.objects.create_user(email="login@example.com", password="TestPass1!")
        resp = self.client.post(
            self.login_url,
            {"email": "login@example.com", "password": "TestPass1!"},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, settings.LOGIN_REDIRECT_URL)

    def test_successful_login_with_next_url(self):
        """next パラメータ付きログインで指定URLにリダイレクト"""
        User.objects.create_user(email="next@example.com", password="TestPass1!")
        resp = self.client.post(
            f"{self.login_url}?next=/app/dashboard/",
            {"email": "next@example.com", "password": "TestPass1!"},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/app/dashboard/")


@override_settings(TRUSTED_PROXY_COUNT=0)
class SignupRateLimitTest(TestCase):
    """signup IP レート制限のテスト"""

    SIGNUP_URL = "/accounts/signup/"
    VALID_POST = {
        "email": "ratelimit@example.com",
        "password": "StrongPass1!",
        "password_confirm": "StrongPass1!",
    }

    def setUp(self):
        cache.clear()

    def _post_signup(self, email_suffix=0, remote_addr="1.2.3.4", xff=None):
        # 毎回新規クライアントを使い、ログイン状態が持ち越されないようにする
        c = Client()
        kwargs = {"REMOTE_ADDR": remote_addr}
        if xff is not None:
            kwargs["HTTP_X_FORWARDED_FOR"] = xff
        return c.post(
            self.SIGNUP_URL,
            {**self.VALID_POST, "email": f"u{email_suffix}@example.com"},
            **kwargs,
        )

    def test_signup_rate_limit_blocks_after_limit(self):
        """10回ポスト後に 429 が返ること"""
        for i in range(10):
            resp = self._post_signup(email_suffix=i, remote_addr="1.2.3.4")
            self.assertNotEqual(resp.status_code, 429, f"blocked too early at attempt {i+1}")

        resp = self._post_signup(email_suffix=99, remote_addr="1.2.3.4")
        self.assertEqual(resp.status_code, 429)

    def test_signup_rate_limit_different_ips_independent(self):
        """IP が異なれば別カウント（TRUSTED_PROXY_COUNT=0 で REMOTE_ADDR を使用）"""
        # 1.2.3.4 を 10 回使い切る
        for i in range(10):
            self._post_signup(email_suffix=i, remote_addr="1.2.3.4")

        # 別 IP はまだブロックされない
        resp = self._post_signup(email_suffix=50, remote_addr="5.6.7.8")
        self.assertNotEqual(resp.status_code, 429)

    @override_settings(TRUSTED_PROXY_COUNT=1)
    def test_signup_rate_limit_xff_with_trusted_proxy(self):
        """TRUSTED_PROXY_COUNT=1 設定時、XFF の正規化 IP でカウントされること"""
        cache.clear()
        # XFF に client_ip だけ → ips[max(0, 1-1)] = ips[0] = "9.9.9.9"
        for i in range(10):
            resp = self._post_signup(
                email_suffix=i,
                remote_addr="proxy.railway.internal",
                xff="9.9.9.9",
            )
            self.assertNotEqual(resp.status_code, 429, f"blocked too early at attempt {i+1}")

        resp = self._post_signup(
            email_suffix=99,
            remote_addr="proxy.railway.internal",
            xff="9.9.9.9",
        )
        self.assertEqual(resp.status_code, 429)

    @override_settings(TRUSTED_PROXY_COUNT=1)
    def test_signup_xff_spoofing_is_blocked(self):
        """TRUSTED_PROXY_COUNT=1 時にクライアントが XFF を偽装しても正しい IP が使われること"""
        cache.clear()
        # クライアントが "evil_ip" を先頭に挿入するが、プロキシが "real_client" を末尾追加
        # → ips = ["evil_ip", "real_client"], idx = max(0, 2-1) = 1 → "real_client"
        for i in range(10):
            resp = self._post_signup(
                email_suffix=i,
                remote_addr="proxy.railway.internal",
                xff="evil_ip, real_client",
            )
            self.assertNotEqual(resp.status_code, 429, f"blocked too early at attempt {i+1}")

        resp = self._post_signup(
            email_suffix=99,
            remote_addr="proxy.railway.internal",
            xff="evil_ip, real_client",
        )
        self.assertEqual(resp.status_code, 429)

        # "evil_ip" 単独では別カウント → まだブロックされない
        cache.clear()
        resp = self._post_signup(
            email_suffix=100,
            remote_addr="proxy.railway.internal",
            xff="evil_ip",
        )
        self.assertNotEqual(resp.status_code, 429)


class OpenRedirectTest(TestCase):
    """オープンリダイレクト防御テスト (#10)"""

    def setUp(self):
        self.signup_url = "/accounts/signup/"
        self.login_url = "/accounts/login/"

    def test_open_redirect_blocked_on_login(self):
        """ログイン時に外部URLへのリダイレクトがブロックされる"""
        User.objects.create_user(email="redir@example.com", password="TestPass1!")
        resp = self.client.post(
            f"{self.login_url}?next=https://evil.com/steal",
            {"email": "redir@example.com", "password": "TestPass1!"},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, settings.LOGIN_REDIRECT_URL)

    def test_open_redirect_blocked_on_signup(self):
        """サインアップ時に外部URLへのリダイレクトがブロックされる"""
        resp = self.client.post(
            f"{self.signup_url}?next=https://evil.com/steal",
            {
                "email": "redir-signup@example.com",
                "password": "StrongPass1!",
                "password_confirm": "StrongPass1!",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn("evil.com", resp.url)
