# apps/common/test_check_deploy_config.py
"""
check_deploy_config management command のテスト。

各チェック関数の単体テストと、management command の統合テスト
（出力フォーマット・exit code）を含む。
"""
import json
import sys
from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.test import override_settings

from apps.common.management.commands.check_deploy_config import (
    ERROR,
    OK,
    WARNING,
    check_allowed_hosts,
    check_csrf_trusted_origins,
    check_debug_and_secret_key,
    check_default_from_email,
    check_email_backend,
    check_site_url,
    check_site_url_in_allowed_hosts,
    check_stripe_price_id,
    check_stripe_secret_key,
    check_stripe_webhook_secret,
)

_CONSOLE_BACKEND = "django.core.mail.backends.console.EmailBackend"
_SMTP_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# ---------------------------------------------------------------------------
# check_debug_and_secret_key
# ---------------------------------------------------------------------------

@override_settings(DEBUG=False, SECRET_KEY="real-secret")
def test_debug_false_with_key_is_ok():
    level, name, _ = check_debug_and_secret_key()
    assert level == OK
    assert name == "DEBUG"


@override_settings(DEBUG=True, SECRET_KEY="dev-key")
def test_debug_true_is_warning():
    level, name, _ = check_debug_and_secret_key()
    assert level == WARNING
    assert name == "DEBUG"


# NOTE: "DEBUG=False かつ SECRET_KEY 空" は Django 起動時に ImproperlyConfigured で
# 阻止されるため、@override_settings(SECRET_KEY="") でのテストは到達不可。
# check_debug_and_secret_key の ERROR 分岐は防衛的実装であり、単体テストは省略する。


# ---------------------------------------------------------------------------
# check_site_url
# ---------------------------------------------------------------------------

@override_settings(SITE_URL="https://example.com")
def test_site_url_https_is_ok():
    level, name, _ = check_site_url()
    assert level == OK
    assert name == "SITE_URL"


@override_settings(SITE_URL="")
def test_site_url_empty_is_error():
    level, _, message = check_site_url()
    assert level == ERROR
    assert "not set" in message


@override_settings(SITE_URL="http://localhost:8000")
def test_site_url_localhost_is_warning():
    level, _, message = check_site_url()
    assert level == WARNING
    assert "localhost" in message


@override_settings(SITE_URL="http://example.com")
def test_site_url_http_non_local_is_warning():
    level, _, message = check_site_url()
    assert level == WARNING
    assert "http" in message


# ---------------------------------------------------------------------------
# check_allowed_hosts
# ---------------------------------------------------------------------------

@override_settings(ALLOWED_HOSTS=["example.com"])
def test_allowed_hosts_with_real_host_is_ok():
    level, name, _ = check_allowed_hosts()
    assert level == OK
    assert name == "ALLOWED_HOSTS"


@override_settings(ALLOWED_HOSTS=[])
def test_allowed_hosts_empty_is_error():
    level, _, message = check_allowed_hosts()
    assert level == ERROR
    assert "empty" in message


@override_settings(ALLOWED_HOSTS=["localhost", "127.0.0.1"])
def test_allowed_hosts_local_only_is_warning():
    level, _, message = check_allowed_hosts()
    assert level == WARNING
    assert "local" in message


# ---------------------------------------------------------------------------
# check_site_url_in_allowed_hosts
# ---------------------------------------------------------------------------

@override_settings(SITE_URL="https://example.com", ALLOWED_HOSTS=["api.example.com"])
def test_site_url_hostname_not_in_allowed_hosts_is_warning():
    level, name, message = check_site_url_in_allowed_hosts()
    assert level == WARNING
    assert name == "SITE_URL_IN_ALLOWED_HOSTS"
    assert "example.com" in message


@override_settings(SITE_URL="https://example.com", ALLOWED_HOSTS=["example.com"])
def test_site_url_hostname_in_allowed_hosts_is_ok():
    level, name, _ = check_site_url_in_allowed_hosts()
    assert level == OK
    assert name == "SITE_URL_IN_ALLOWED_HOSTS"


@override_settings(SITE_URL="https://example.com:8443", ALLOWED_HOSTS=["example.com"])
def test_site_url_with_port_hostname_matches_allowed_hosts():
    # urlparse で hostname を抽出するためポートは除去される
    level, _, _ = check_site_url_in_allowed_hosts()
    assert level == OK


@override_settings(SITE_URL="", ALLOWED_HOSTS=["example.com"])
def test_site_url_empty_skips_check():
    # SITE_URL 未設定は他チェックで ERROR 済み → このチェックはスキップ
    level, _, message = check_site_url_in_allowed_hosts()
    assert level == OK
    assert message == "skip"


@override_settings(SITE_URL="https://example.com", ALLOWED_HOSTS=[])
def test_allowed_hosts_empty_skips_check():
    # ALLOWED_HOSTS 空は他チェックで ERROR 済み → このチェックはスキップ
    level, _, message = check_site_url_in_allowed_hosts()
    assert level == OK
    assert message == "skip"


@override_settings(SITE_URL="https://example.com", ALLOWED_HOSTS=["*"])
def test_wildcard_in_allowed_hosts_is_ok():
    level, _, _ = check_site_url_in_allowed_hosts()
    assert level == OK


# ---------------------------------------------------------------------------
# check_csrf_trusted_origins
# ---------------------------------------------------------------------------

@override_settings(
    SITE_URL="https://example.com",
    CSRF_TRUSTED_ORIGINS=["https://example.com"],
)
def test_csrf_trusted_origins_ok_when_site_url_included():
    level, name, _ = check_csrf_trusted_origins()
    assert level == OK
    assert name == "CSRF_TRUSTED_ORIGINS"


@override_settings(
    SITE_URL="https://example.com",
    CSRF_TRUSTED_ORIGINS=[],
)
def test_csrf_trusted_origins_warning_when_https_site_url_missing():
    level, _, message = check_csrf_trusted_origins()
    assert level == WARNING
    assert message == "SITE_URL not in CSRF_TRUSTED_ORIGINS"


@override_settings(
    SITE_URL="http://localhost:8000",
    CSRF_TRUSTED_ORIGINS=[],
)
def test_csrf_trusted_origins_ok_when_site_url_is_http():
    # http の SITE_URL は CSRF チェック対象外 → OK
    level, _, _ = check_csrf_trusted_origins()
    assert level == OK


# ---------------------------------------------------------------------------
# check_stripe_*
# ---------------------------------------------------------------------------

@override_settings(STRIPE_SECRET_KEY="sk_live_xxx")
def test_stripe_secret_key_set_is_ok():
    level, name, _ = check_stripe_secret_key()
    assert level == OK
    assert name == "STRIPE_SECRET_KEY"


@override_settings(STRIPE_SECRET_KEY="")
def test_stripe_secret_key_empty_is_error():
    level, _, message = check_stripe_secret_key()
    assert level == ERROR
    assert "not set" in message


@override_settings(STRIPE_PRICE_ID="price_live_xxx")
def test_stripe_price_id_set_is_ok():
    level, name, _ = check_stripe_price_id()
    assert level == OK
    assert name == "STRIPE_PRICE_ID"


@override_settings(STRIPE_PRICE_ID="")
def test_stripe_price_id_empty_is_error():
    level, _, message = check_stripe_price_id()
    assert level == ERROR
    assert "not set" in message


@override_settings(STRIPE_WEBHOOK_SECRET="whsec_xxx")
def test_stripe_webhook_secret_set_is_ok():
    level, name, _ = check_stripe_webhook_secret()
    assert level == OK
    assert name == "STRIPE_WEBHOOK_SECRET"


@override_settings(STRIPE_WEBHOOK_SECRET="")
def test_stripe_webhook_secret_empty_is_error():
    # Webhook は課金状態の正本。未設定はテンプレートの前提が崩れるため ERROR。
    level, _, message = check_stripe_webhook_secret()
    assert level == ERROR
    assert "not set" in message


# ---------------------------------------------------------------------------
# check_email_backend / check_default_from_email（C-2）
# ---------------------------------------------------------------------------

@override_settings(DEBUG=False, EMAIL_BACKEND=_CONSOLE_BACKEND)
def test_email_backend_console_in_production_is_error():
    # 本番で console のままだとリセットトークンがログに平文で残るため ERROR
    level, name, message = check_email_backend()
    assert level == ERROR
    assert name == "EMAIL_BACKEND"
    assert "console" in message


@override_settings(DEBUG=True, EMAIL_BACKEND=_CONSOLE_BACKEND)
def test_email_backend_console_in_debug_is_ok():
    level, _, _ = check_email_backend()
    assert level == OK


@override_settings(DEBUG=False, EMAIL_BACKEND=_SMTP_BACKEND)
def test_email_backend_smtp_in_production_is_ok():
    level, name, _ = check_email_backend()
    assert level == OK
    assert name == "EMAIL_BACKEND"


@override_settings(DEFAULT_FROM_EMAIL="noreply@example.com")
def test_default_from_email_placeholder_is_warning():
    level, name, message = check_default_from_email()
    assert level == WARNING
    assert name == "DEFAULT_FROM_EMAIL"
    assert "noreply@example.com" in message


@override_settings(DEFAULT_FROM_EMAIL="noreply@myservice.jp")
def test_default_from_email_custom_is_ok():
    level, _, _ = check_default_from_email()
    assert level == OK


# ---------------------------------------------------------------------------
# management command: 出力フォーマット
# ---------------------------------------------------------------------------

@override_settings(
    DEBUG=False,
    SECRET_KEY="real-secret",
    SITE_URL="https://example.com",
    ALLOWED_HOSTS=["example.com"],
    CSRF_TRUSTED_ORIGINS=["https://example.com"],
    STRIPE_SECRET_KEY="sk_live_xxx",
    STRIPE_PRICE_ID="price_live_xxx",
    STRIPE_WEBHOOK_SECRET="whsec_xxx",
    EMAIL_BACKEND=_SMTP_BACKEND,
    DEFAULT_FROM_EMAIL="noreply@myservice.jp",
)
def test_command_text_output_all_ok():
    out = StringIO()
    call_command("check_deploy_config", stdout=out)
    output = out.getvalue()

    assert "OK" in output
    assert "Summary:" in output
    assert "error=0" in output
    assert "warning=0" in output


@override_settings(
    DEBUG=False,
    SECRET_KEY="real-secret",
    SITE_URL="https://example.com",
    ALLOWED_HOSTS=["example.com"],
    CSRF_TRUSTED_ORIGINS=["https://example.com"],
    STRIPE_SECRET_KEY="sk_live_xxx",
    STRIPE_PRICE_ID="price_live_xxx",
    STRIPE_WEBHOOK_SECRET="whsec_xxx",
    EMAIL_BACKEND=_SMTP_BACKEND,
    DEFAULT_FROM_EMAIL="noreply@myservice.jp",
)
def test_command_json_output_is_valid_json():
    out = StringIO()
    call_command("check_deploy_config", output_json=True, stdout=out)
    data = json.loads(out.getvalue())

    assert "results" in data
    assert "summary" in data
    assert isinstance(data["results"], list)
    assert {"ok", "warning", "error"} == set(data["summary"].keys())

    # C-2: EMAIL 系チェックが JSON 出力にも含まれる
    names = {r["name"] for r in data["results"]}
    assert "EMAIL_BACKEND" in names
    assert "DEFAULT_FROM_EMAIL" in names


@override_settings(
    DEBUG=False,
    SECRET_KEY="real-secret",
    SITE_URL="https://example.com",
    ALLOWED_HOSTS=["example.com"],
    CSRF_TRUSTED_ORIGINS=["https://example.com"],
    STRIPE_SECRET_KEY="",  # ERROR
    STRIPE_PRICE_ID="price_live_xxx",
    STRIPE_WEBHOOK_SECRET="whsec_xxx",
)
def test_command_json_output_has_correct_summary_counts():
    out = StringIO()
    # ERROR があるので SystemExit(1) が上がる。出力は exit 前に書き込み済み。
    with pytest.raises(SystemExit):
        call_command("check_deploy_config", output_json=True, stdout=out)
    data = json.loads(out.getvalue())

    assert data["summary"]["error"] >= 1


# ---------------------------------------------------------------------------
# management command: exit code
# ---------------------------------------------------------------------------

@override_settings(
    DEBUG=False,
    SECRET_KEY="real-secret",
    SITE_URL="https://example.com",
    ALLOWED_HOSTS=["example.com"],
    CSRF_TRUSTED_ORIGINS=["https://example.com"],
    STRIPE_SECRET_KEY="sk_live_xxx",
    STRIPE_PRICE_ID="price_live_xxx",
    STRIPE_WEBHOOK_SECRET="whsec_xxx",
    EMAIL_BACKEND=_SMTP_BACKEND,
    DEFAULT_FROM_EMAIL="noreply@myservice.jp",
)
def test_exit_code_0_when_no_error_no_warning():
    out = StringIO()
    # エラーなし → sys.exit が呼ばれないか exit(0) のまま
    try:
        call_command("check_deploy_config", stdout=out)
    except SystemExit as e:
        assert e.code == 0 or e.code is None


@override_settings(
    DEBUG=False,
    SECRET_KEY="real-secret",
    SITE_URL="https://example.com",
    ALLOWED_HOSTS=["example.com"],
    CSRF_TRUSTED_ORIGINS=["https://example.com"],
    STRIPE_SECRET_KEY="",  # ERROR
    STRIPE_PRICE_ID="price_live_xxx",
    STRIPE_WEBHOOK_SECRET="whsec_xxx",
)
def test_exit_code_1_when_error_exists():
    out = StringIO()
    with pytest.raises(SystemExit) as exc_info:
        call_command("check_deploy_config", stdout=out)
    assert exc_info.value.code == 1


@override_settings(
    DEBUG=False,
    SECRET_KEY="real-secret",
    SITE_URL="http://example.com",  # http（非 localhost）→ WARNING のみ
    ALLOWED_HOSTS=["example.com"],
    CSRF_TRUSTED_ORIGINS=[],
    STRIPE_SECRET_KEY="sk_live_xxx",
    STRIPE_PRICE_ID="price_live_xxx",
    STRIPE_WEBHOOK_SECRET="whsec_xxx",
)
def test_exit_code_0_when_warning_only_without_flag():
    out = StringIO()
    # --fail-on-warning なし → WARNING だけなら exit(0)
    try:
        call_command("check_deploy_config", stdout=out)
    except SystemExit as e:
        assert e.code == 0 or e.code is None


@override_settings(
    DEBUG=False,
    SECRET_KEY="real-secret",
    SITE_URL="http://example.com",  # http（非 localhost）→ WARNING のみ
    ALLOWED_HOSTS=["example.com"],
    CSRF_TRUSTED_ORIGINS=[],
    STRIPE_SECRET_KEY="sk_live_xxx",
    STRIPE_PRICE_ID="price_live_xxx",
    STRIPE_WEBHOOK_SECRET="whsec_xxx",
)
def test_exit_code_1_when_warning_and_fail_on_warning():
    out = StringIO()
    with pytest.raises(SystemExit) as exc_info:
        call_command("check_deploy_config", fail_on_warning=True, stdout=out)
    assert exc_info.value.code == 1
