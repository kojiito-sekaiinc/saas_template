"""
config/settings_test.py

テスト専用設定。pytest 実行時のみ使用する（pytest.ini で指定）。

責務:
- .env がなくても pytest が起動できるよう、必要な値をダミーで補う。
- 本番設定（config.settings）の fail-closed な思想は崩さない。
  テスト設定を本番で使うことを意図的に防ぐため、ダミー値は明示的に安全でない名前にする。
- 本番設定の動作を変えないために、テスト専用の差分のみをここに記述する。

使い方:
    pytest                            # settings_test を使用（pytest.ini で設定済み）
    pytest apps/billing/              # 同上
    python manage.py runserver        # config.settings を使用（.env が必要）
"""
import os

# ---------------------------------------------------------------------------
# settings.py を import する前に env デフォルトを設定する
#
# settings.py の SECRET_KEY チェックは:
#   if not SECRET_KEY and not DEBUG: raise ImproperlyConfigured(...)
#
# .env がない環境での pytest 起動を可能にするため、import 前に setdefault で補う。
# すでに env var が設定されている場合（CI、ローカル .env）は setdefault が上書きしないため、
# 本番設定との二重管理にはならない。
# ---------------------------------------------------------------------------
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("SECRET_KEY", "test-secret-key-unsafe-do-not-use-in-production")

from config.settings import *  # noqa: F401, F403

# ---------------------------------------------------------------------------
# Stripe: テスト時はダミー値で補う（実際の API は呼ばない）
# env var が設定されていれば（CI 等）そちらを優先する。
# ---------------------------------------------------------------------------
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_dummy")
STRIPE_PRICE_ID = os.environ.get("STRIPE_PRICE_ID", "price_dummy")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_dummy")

# ---------------------------------------------------------------------------
# パスワードハッシュを軽量化（テスト高速化）
# MD5PasswordHasher は本番用途には使用しない。テスト限定。
# ---------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# ---------------------------------------------------------------------------
# WhiteNoise の静的ファイルストレージをシンプル化
# collectstatic 未実行の状態でも警告が出ないようにする。
# ---------------------------------------------------------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
