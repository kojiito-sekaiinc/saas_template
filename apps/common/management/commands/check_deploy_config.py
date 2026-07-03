"""
apps/common/management/commands/check_deploy_config.py

本番デプロイ前の設定不備を検出する management command。

制約:
- DB 更新しない
- 外部 API を呼ばない
- settings から値を取得する
- 既存コードを変更しない

使用例:
    python manage.py check_deploy_config
    python manage.py check_deploy_config --json
    python manage.py check_deploy_config --fail-on-warning
"""
import json
import sys
from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand

# 出力レベル定数
OK = "OK"
WARNING = "WARNING"
ERROR = "ERROR"


# ---------------------------------------------------------------------------
# チェック関数群（各関数は (level, name, message) のタプルを返す）
# ---------------------------------------------------------------------------

def check_debug_and_secret_key() -> tuple[str, str, str]:
    """
    DEBUG=False のとき SECRET_KEY が設定されているか確認する。

    注意: Django は SECRET_KEY が空の状態でアクセスすると ImproperlyConfigured を
    raise するため、「DEBUG=False かつ SECRET_KEY 空」という状態は起動時点で
    既に阻止されている。このチェックは、将来的な設定変更に備えた防衛的実装。
    """
    debug = getattr(settings, "DEBUG", False)
    secret_key = getattr(settings, "SECRET_KEY", "")

    if not debug and not secret_key:
        return ERROR, "SECRET_KEY", "SECRET_KEY=<empty>"
    if debug:
        return WARNING, "DEBUG", "DEBUG=True"
    return OK, "DEBUG", "DEBUG=False"


def check_site_url() -> tuple[str, str, str]:
    site_url = getattr(settings, "SITE_URL", "")

    if not site_url:
        return ERROR, "SITE_URL", "<not set>"

    hostname = urlparse(site_url).hostname or ""
    _local = {"localhost", "127.0.0.1"}

    if hostname in _local:
        return WARNING, "SITE_URL", hostname

    if site_url.startswith("http://"):
        return WARNING, "SITE_URL", site_url

    if site_url.startswith("https://"):
        return OK, "SITE_URL", site_url

    return WARNING, "SITE_URL", site_url


def check_allowed_hosts() -> tuple[str, str, str]:
    allowed_hosts = getattr(settings, "ALLOWED_HOSTS", [])

    if not allowed_hosts:
        return ERROR, "ALLOWED_HOSTS", "<empty>"

    _local = {"localhost", "127.0.0.1"}
    non_local = [h for h in allowed_hosts if h not in _local]

    if not non_local:
        return WARNING, "ALLOWED_HOSTS", ",".join(allowed_hosts)

    return OK, "ALLOWED_HOSTS", ",".join(allowed_hosts)


def check_csrf_trusted_origins() -> tuple[str, str, str]:
    site_url = getattr(settings, "SITE_URL", "")
    csrf_origins = getattr(settings, "CSRF_TRUSTED_ORIGINS", [])

    # HTTPS の SITE_URL が CSRF_TRUSTED_ORIGINS に含まれていなければ WARNING
    if site_url.startswith("https://"):
        normalized = site_url.rstrip("/")
        if normalized not in csrf_origins:
            return WARNING, "CSRF_TRUSTED_ORIGINS", "SITE_URL not in CSRF_TRUSTED_ORIGINS"

    return OK, "CSRF_TRUSTED_ORIGINS", "ok"


def check_site_url_in_allowed_hosts() -> tuple[str, str, str]:
    """
    SITE_URL のホスト名が ALLOWED_HOSTS に含まれるか確認する。

    SITE_URL 未設定・ALLOWED_HOSTS 空など前提が崩れている場合はスキップ（OK を返す）。
    それぞれの個別チェックで既に ERROR が出るため、二重報告を避けるため。
    ALLOWED_HOSTS に "*" が含まれる場合は全ホスト許可とみなし OK。
    """
    site_url = getattr(settings, "SITE_URL", "")
    allowed_hosts = getattr(settings, "ALLOWED_HOSTS", [])

    # 前提が崩れている場合はスキップ
    if not site_url or not allowed_hosts:
        return OK, "SITE_URL_IN_ALLOWED_HOSTS", "skip"

    hostname = urlparse(site_url).hostname
    if not hostname:
        return OK, "SITE_URL_IN_ALLOWED_HOSTS", "skip"

    if "*" in allowed_hosts or hostname in allowed_hosts:
        return OK, "SITE_URL_IN_ALLOWED_HOSTS", f"{hostname} in ALLOWED_HOSTS"

    return WARNING, "SITE_URL_IN_ALLOWED_HOSTS", f"{hostname} not in ALLOWED_HOSTS"


def check_stripe_secret_key() -> tuple[str, str, str]:
    key = getattr(settings, "STRIPE_SECRET_KEY", "")
    if not key:
        return ERROR, "STRIPE_SECRET_KEY", "<not set>"
    return OK, "STRIPE_SECRET_KEY", "set"


def check_stripe_price_id() -> tuple[str, str, str]:
    price_id = getattr(settings, "STRIPE_PRICE_ID", "")
    if not price_id:
        return ERROR, "STRIPE_PRICE_ID", "<not set>"
    return OK, "STRIPE_PRICE_ID", price_id


def check_stripe_webhook_secret() -> tuple[str, str, str]:
    secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")
    if not secret:
        return ERROR, "STRIPE_WEBHOOK_SECRET", "<not set>"
    return OK, "STRIPE_WEBHOOK_SECRET", "set"


_CONSOLE_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
_DEFAULT_FROM_EMAIL_PLACEHOLDER = "noreply@example.com"


def check_email_backend() -> tuple[str, str, str]:
    """
    本番（DEBUG=False）で console backend のままだと、パスワードリセットメールが
    ユーザーに届かず、リセットリンク（トークン付き）が標準出力ログに平文で残る。
    ログ閲覧権限者が任意アカウントのパスワードを変更できるため ERROR とする。
    """
    debug = getattr(settings, "DEBUG", False)
    backend = getattr(settings, "EMAIL_BACKEND", "")

    if not debug and backend == _CONSOLE_EMAIL_BACKEND:
        return ERROR, "EMAIL_BACKEND", "console backend in production"
    return OK, "EMAIL_BACKEND", backend or "<not set>"


def check_default_from_email() -> tuple[str, str, str]:
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "")
    if from_email == _DEFAULT_FROM_EMAIL_PLACEHOLDER:
        return WARNING, "DEFAULT_FROM_EMAIL", f"{from_email} (default placeholder)"
    return OK, "DEFAULT_FROM_EMAIL", from_email


# チェック実行順序（仕様書に準拠）
_CHECKS = [
    check_debug_and_secret_key,
    check_site_url,
    check_allowed_hosts,
    check_site_url_in_allowed_hosts,
    check_csrf_trusted_origins,
    check_stripe_secret_key,
    check_stripe_price_id,
    check_stripe_webhook_secret,
    check_email_backend,
    check_default_from_email,
]


# ---------------------------------------------------------------------------
# Management Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = "本番デプロイ前の設定不備を検出する"

    def add_arguments(self, parser):
        parser.add_argument(
            "--json",
            action="store_true",
            dest="output_json",
            help="結果を JSON 形式で出力する",
        )
        parser.add_argument(
            "--fail-on-warning",
            action="store_true",
            help="WARNING がある場合も exit(1) にする",
        )

    def handle(self, *args, **options):
        results = self._run_checks()
        summary = self._build_summary(results)

        if options["output_json"]:
            self._print_json(results, summary)
        else:
            self._print_text(results, summary)

        # 終了コード
        has_error = summary["error"] > 0
        has_warning = summary["warning"] > 0

        if has_error or (options["fail_on_warning"] and has_warning):
            sys.exit(1)

    # ------------------------------------------------------------------
    # チェック実行
    # ------------------------------------------------------------------

    def _run_checks(self) -> list[dict]:
        results = []
        for check_fn in _CHECKS:
            level, name, message = check_fn()
            results.append({"level": level, "name": name, "message": message})
        return results

    def _build_summary(self, results: list[dict]) -> dict:
        counts = {OK: 0, WARNING: 0, ERROR: 0}
        for r in results:
            counts[r["level"]] += 1
        return {
            "ok": counts[OK],
            "warning": counts[WARNING],
            "error": counts[ERROR],
        }

    # ------------------------------------------------------------------
    # テキスト出力
    # ------------------------------------------------------------------

    def _print_text(self, results: list[dict], summary: dict) -> None:
        for r in results:
            # 左揃えでカラム幅を揃える（仕様書の例に合わせる）
            level_col = r["level"].ljust(8)
            name_col = r["name"].ljust(24)
            self.stdout.write(f"{level_col} {name_col} {r['message']}")

        self.stdout.write(
            f"\nSummary: ok={summary['ok']} "
            f"warning={summary['warning']} "
            f"error={summary['error']}"
        )

    # ------------------------------------------------------------------
    # JSON 出力
    # ------------------------------------------------------------------

    def _print_json(self, results: list[dict], summary: dict) -> None:
        output = {"results": results, "summary": summary}
        self.stdout.write(json.dumps(output, indent=2, ensure_ascii=False))
