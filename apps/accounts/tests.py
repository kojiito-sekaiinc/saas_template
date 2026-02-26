from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

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
