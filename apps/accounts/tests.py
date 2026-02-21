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
