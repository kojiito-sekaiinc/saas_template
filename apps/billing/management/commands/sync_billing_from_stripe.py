"""
apps/billing/management/commands/sync_billing_from_stripe.py

Stripe を正本として BillingProfile を再同期する management command。
Webhook 未達・障害時の整合性回復手段として使用する。

使用例:
    python manage.py sync_billing_from_stripe --user-id 1
    python manage.py sync_billing_from_stripe --email user@example.com
    python manage.py sync_billing_from_stripe --all --dry-run

出力形式（1 行 = 1 ユーザー）:
    UPDATED      {"user_id": 1, "email": "...", "diffs": {...}}
    NO_CHANGE    {"user_id": 2, ...}
    WOULD_UPDATE {"user_id": 3, ...}  # dry-run 時
    ERROR        user_id=4 email=... error=...
"""
import json
import logging

import stripe
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.billing.models import BillingProfile
from apps.billing.services import sync_billing_profile_from_stripe

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Stripe を正本として BillingProfile を再同期する（Webhook 未達時の整合性回復）"

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--user-id",
            type=int,
            metavar="USER_ID",
            help="同期対象ユーザーの ID",
        )
        group.add_argument(
            "--email",
            type=str,
            metavar="EMAIL",
            help="同期対象ユーザーのメールアドレス",
        )
        group.add_argument(
            "--all",
            action="store_true",
            help="全 BillingProfile を対象に同期する",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="差分を表示するのみで DB は更新しない",
        )

    def handle(self, *args, **options):
        dry_run: bool = options["dry_run"]

        if dry_run:
            self.stdout.write("--- DRY RUN: DB は更新されません ---")

        billing_profiles = self._get_billing_profiles(options)

        for bp in billing_profiles:
            self._sync_one(bp, dry_run=dry_run)

    # ------------------------------------------------------------------
    # 対象 BillingProfile の取得
    # ------------------------------------------------------------------

    def _get_billing_profiles(self, options):
        """
        コマンド引数に応じて同期対象の BillingProfile を返す。
        --user-id / --email の場合、BillingProfile が未作成なら get_or_create する。
        """
        if options["user_id"] is not None:
            user = self._get_user_by_id(options["user_id"])
            bp, created = BillingProfile.objects.get_or_create(user=user)
            if created:
                logger.info(
                    "sync: BillingProfile を新規作成 user_id=%s email=%s",
                    user.pk, user.email,
                )
            return [bp]

        if options["email"] is not None:
            user = self._get_user_by_email(options["email"])
            bp, created = BillingProfile.objects.get_or_create(user=user)
            if created:
                logger.info(
                    "sync: BillingProfile を新規作成 user_id=%s email=%s",
                    user.pk, user.email,
                )
            return [bp]

        # --all: 全件を select_related で取得（N+1 回避）
        return BillingProfile.objects.select_related("user").all()

    def _get_user_by_id(self, user_id: int):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise CommandError(f"ユーザーが見つかりません: user_id={user_id}")

    def _get_user_by_email(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f"ユーザーが見つかりません: email={email}")

    # ------------------------------------------------------------------
    # 1 ユーザーの同期と出力
    # ------------------------------------------------------------------

    def _sync_one(self, bp: BillingProfile, *, dry_run: bool) -> None:
        """
        1 件の BillingProfile を同期し、結果を stdout に出力する。
        エラーが発生しても他のユーザーの処理を継続する。
        """
        user_id = bp.user_id
        email = bp.user.email

        try:
            result = sync_billing_profile_from_stripe(bp, dry_run=dry_run)
        except stripe.StripeError as e:
            logger.error(
                "sync: Stripe API エラー user_id=%s email=%s error=%s",
                user_id, email, e,
            )
            self.stdout.write(
                f"ERROR user_id={user_id} email={email} error={e}"
            )
            return
        except Exception as e:
            logger.error(
                "sync: 予期しないエラー user_id=%s email=%s error=%s",
                user_id, email, e,
            )
            self.stdout.write(
                f"ERROR user_id={user_id} email={email} error={e}"
            )
            return

        diffs = result["diffs"]
        stripe_state = result["stripe_state"]

        payload: dict = {
            "user_id": user_id,
            "email": email,
            "stripe_customer_id": stripe_state["stripe_customer_id"],
            "stripe_subscription_id": stripe_state["stripe_subscription_id"],
            "source": stripe_state["source"],
        }

        if diffs:
            # datetime を文字列に変換して JSON 化できるようにする
            payload["diffs"] = {
                field: {
                    "before": _serialize_value(v["before"]),
                    "after": _serialize_value(v["after"]),
                }
                for field, v in diffs.items()
            }
            label = "WOULD_UPDATE" if dry_run else "UPDATED"
        else:
            label = "NO_CHANGE"

        self.stdout.write(f"{label} {json.dumps(payload, ensure_ascii=False)}")


# ---------------------------------------------------------------------------
# ユーティリティ
# ---------------------------------------------------------------------------

def _serialize_value(value) -> str | None:
    """
    JSON 出力用の値変換。datetime は ISO 8601 文字列に変換する。
    """
    if value is None:
        return None
    return str(value) if not isinstance(value, str) else value
