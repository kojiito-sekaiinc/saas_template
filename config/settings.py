"""
Django settings for config project.
"""

import os
from pathlib import Path
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
# Default is False (fail-closed) — must explicitly set DEBUG=True for development.
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

# SECURITY WARNING: keep the secret key used in production secret!
# In production (DEBUG=False), SECRET_KEY must be set via environment variable.
# In development (DEBUG=True), a fallback key is used for convenience.
SECRET_KEY = os.environ.get("SECRET_KEY") or ""
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-dev-only-key"
    else:
        raise ImproperlyConfigured(
            "SECRET_KEY environment variable is required when DEBUG=False"
        )

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

# Site URL for absolute URLs (used in Stripe Checkout, emails, etc.)
SITE_URL = os.environ.get("SITE_URL", "http://localhost:8000")

# CSRF trusted origins (comma-separated, e.g. "https://example.com,https://www.example.com")
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "axes",
    # Local apps
    "apps.accounts",
    "apps.billing",
    "apps.app",
    "apps.common",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "axes.middleware.AxesMiddleware",
    "apps.common.middleware.PaywallMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Security settings for production (HTTPS)
IS_PROD = not DEBUG

if IS_PROD:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_CONTENT_TYPE_NOSNIFF = True

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    url = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": (url.path or "").lstrip("/"),
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port or 5432,
        }
    }
else:
    # Development: use SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Tokyo")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise configuration
# 開発・テスト: manifest なし (CompressedStaticFilesStorage)
# 本番: 環境変数で manifest を有効化する
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# 本番で manifest を使いたい場合だけ、環境変数で上書き
if os.environ.get("DJANGO_STATICFILES_MANIFEST", "0") == "1":
    STORAGES["staticfiles"]["BACKEND"] = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Authentication
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/app/"
LOGOUT_REDIRECT_URL = "/"

# django-axes: ブルートフォース防御
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # 1時間後に自動解除
AXES_LOCKOUT_PARAMETERS = [["username"]]  # axes 内部キー "username" = email（下記設定で明示）
AXES_USERNAME_FORM_FIELD = "email"  # authenticate() に渡すキーワードと一致させる
AXES_RESET_ON_SUCCESS = True

# Stripe configuration (centralized)
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_ID = os.environ.get("STRIPE_PRICE_ID", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

# CSRF_TRUSTED_ORIGINS fallback: HTTPS の SITE_URL を自動追加
if not CSRF_TRUSTED_ORIGINS and SITE_URL.startswith("https://"):
    CSRF_TRUSTED_ORIGINS = [SITE_URL.rstrip("/")]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Cache (used for rate limiting etc.)
#
# 【前提条件】LocMemCache はプロセスローカルなため、以下の条件を満たす場合のみ有効:
#   - Gunicorn シングルワーカー（--workers 1）
#   - Railway シングルインスタンス（スケールアウトなし）
#
# 【Redis への移行が必要な条件】以下のいずれかに該当する場合は django-redis に切り替えること:
#   - Gunicorn ワーカーを 2 以上に増やすとき
#   - Railway でインスタンスを複数に増やすとき（水平スケール）
#   - レート制限をプロセス間で確実に共有する必要が生じたとき
#
# 移行手順の概要:
#   1. Railway に Redis プラグインを追加し REDIS_URL を取得
#   2. django-redis を requirements.txt に追加
#   3. BACKEND を "django_redis.cache.RedisCache" に変更し LOCATION に REDIS_URL を設定
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# リバースプロキシ数（Railway 本番: 1, ローカル開発: 0）
# get_client_ip() が X-Forwarded-For を正規化する際に使用する
TRUSTED_PROXY_COUNT = int(os.environ.get("TRUSTED_PROXY_COUNT", "0"))