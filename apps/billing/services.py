"""
apps/billing/services.py

Stripe を正本として BillingProfile を再同期するサービス層。
Webhook 未達・障害時の整合性回復手段として使用する。

制約:
- Stripe 側の状態は変更しない（read-only）
- last_stripe_event_created は更新しない
- Webhook ロジック（views.py）は変更しない
"""
import logging
from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings
from django.db import transaction

from .models import BillingProfile

logger = logging.getLogger(__name__)

# サブスクリプション選択優先度（複数ヒット時に「最も生きている」ものを選ぶ）
# 小さい値ほど優先度が高い
_STATUS_PRIORITY: dict[str, int] = {
    "active": 0,
    "trialing": 1,
    "past_due": 2,
    "unpaid": 3,
    "incomplete": 4,
    "incomplete_expired": 5,
    "canceled": 6,
}

# diff_billing_profile / apply_stripe_state_to_billing_profile が扱うフィールド
_SYNC_FIELDS = [
    "stripe_customer_id",
    "stripe_subscription_id",
    "status",
    "current_period_end",
]


# ---------------------------------------------------------------------------
# 内部ユーティリティ
# ---------------------------------------------------------------------------

def _parse_subscription(sub) -> dict:
    """
    Stripe Subscription オブジェクトから同期に必要なフィールドを抽出する。
    """
    ts = sub.get("current_period_end")
    current_period_end = (
        datetime.fromtimestamp(ts, tz=dt_timezone.utc) if ts else None
    )
    return {
        "stripe_customer_id": sub.get("customer"),
        "stripe_subscription_id": sub.get("id"),
        "status": sub.get("status", "not_subscribed"),
        "current_period_end": current_period_end,
    }


def _has_expected_price(sub, expected_price_id: str) -> bool:
    """subscription が expected_price_id を含むか確認する。"""
    items = sub.get("items", {}).get("data", [])
    return any(
        item.get("price", {}).get("id") == expected_price_id
        for item in items
    )


# ---------------------------------------------------------------------------
# 公開サービス関数
# ---------------------------------------------------------------------------

def get_stripe_billing_state(
    *,
    subscription_id: str | None,
    customer_id: str | None,
    expected_price_id: str,
) -> dict:
    """
    Stripe から現在の課金状態を取得して正規化した dict を返す。

    取得優先度:
    1. subscription_id が指定されていれば直接取得
    2. price_id 不一致または取得失敗の場合は customer_id から一覧取得
    3. どちらも見つからない場合は not_subscribed を返す

    返り値:
        {
            "found": bool,
            "stripe_customer_id": str | None,
            "stripe_subscription_id": str | None,
            "status": str,                   # not_subscribed を含む
            "current_period_end": datetime | None,
            "source": "subscription_id" | "customer_id" | "none",
        }

    例外:
        stripe.StripeError: API 呼び出しが一時的に失敗した場合に再送出する。
        呼び出し側でユーザー単位のエラーハンドリングを行うこと。
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    _not_found = {
        "found": False,
        "stripe_customer_id": customer_id,
        "stripe_subscription_id": None,
        "status": "not_subscribed",
        "current_period_end": None,
        "source": "none",
    }

    # --- 1. subscription_id 直接取得 ---
    if subscription_id:
        try:
            sub = stripe.Subscription.retrieve(subscription_id)
            if _has_expected_price(sub, expected_price_id):
                return {
                    "found": True,
                    **_parse_subscription(sub),
                    "source": "subscription_id",
                }
            logger.warning(
                "sync: subscription_id=%s は price_id 不一致のため customer_id 検索へ fallback",
                subscription_id,
            )
        except stripe.InvalidRequestError:
            logger.warning(
                "sync: subscription_id=%s は Stripe に存在しない。customer_id 検索へ fallback",
                subscription_id,
            )
        except stripe.StripeError as e:
            logger.error(
                "sync: Stripe API エラー (subscription_id=%s): %s", subscription_id, e
            )
            raise

    # --- 2. customer_id からサブスクリプション一覧取得 ---
    if customer_id:
        try:
            response = stripe.Subscription.list(
                customer=customer_id,
                status="all",
                limit=100,
            )
        except stripe.InvalidRequestError:
            logger.warning(
                "sync: customer_id=%s は Stripe に存在しない", customer_id
            )
            return _not_found
        except stripe.StripeError as e:
            logger.error(
                "sync: Stripe API エラー (customer_id=%s): %s", customer_id, e
            )
            raise

        # expected_price_id に一致するものだけに絞り込む
        matched = [
            sub for sub in response.get("data", [])
            if _has_expected_price(sub, expected_price_id)
        ]

        if not matched:
            logger.info(
                "sync: customer_id=%s に expected_price_id と一致するサブスクリプションなし",
                customer_id,
            )
            return _not_found

        # 「最も生きている」サブスクリプションを選択
        best = min(
            matched,
            key=lambda s: _STATUS_PRIORITY.get(s.get("status", ""), 99),
        )
        return {
            "found": True,
            **_parse_subscription(best),
            "source": "customer_id",
        }

    return _not_found


def diff_billing_profile(
    billing_profile: BillingProfile,
    stripe_state: dict,
) -> dict[str, dict]:
    """
    BillingProfile の現在値と Stripe 状態の差分を返す。

    返り値:
        差分があるフィールドのみ含む dict。
        例: {"status": {"before": "not_subscribed", "after": "active"}}
        差分がない場合は空の dict。
    """
    diffs: dict[str, dict] = {}
    for field in _SYNC_FIELDS:
        before = getattr(billing_profile, field)
        after = stripe_state.get(field)
        if before != after:
            diffs[field] = {"before": before, "after": after}
    return diffs


def apply_stripe_state_to_billing_profile(
    billing_profile: BillingProfile,
    stripe_state: dict,
) -> None:
    """
    Stripe 状態を BillingProfile に反映して保存する。

    注意: last_stripe_event_created は更新しない。
    この関数は select_for_update() でロックされた billing_profile に対して呼ぶこと。
    """
    billing_profile.stripe_customer_id = stripe_state["stripe_customer_id"]
    billing_profile.stripe_subscription_id = stripe_state["stripe_subscription_id"]
    billing_profile.status = stripe_state["status"]
    billing_profile.current_period_end = stripe_state["current_period_end"]
    # last_stripe_event_created には触れない（仕様: Webhook が更新する値）
    billing_profile.save()


def sync_billing_profile_from_stripe(
    billing_profile: BillingProfile,
    *,
    dry_run: bool = False,
) -> dict:
    """
    1 件の BillingProfile を Stripe の状態と同期する。

    処理:
    1. select_for_update でロックを取得
    2. Stripe から現在状態を取得
    3. 差分を算出
    4. 差分がある場合、dry_run=False なら DB を更新

    引数:
        billing_profile: 同期対象の BillingProfile
        dry_run: True の場合、差分を計算するが DB は更新しない

    返り値:
        {
            "updated": bool,       # 実際に DB を更新したか
            "diffs": dict,         # diff_billing_profile の返り値
            "stripe_state": dict,  # get_stripe_billing_state の返り値
            "dry_run": bool,
        }

    例外:
        ValueError: STRIPE_PRICE_ID が未設定の場合
        stripe.StripeError: Stripe API エラー
    """
    expected_price_id = settings.STRIPE_PRICE_ID
    if not expected_price_id:
        raise ValueError("STRIPE_PRICE_ID が設定されていません")

    with transaction.atomic():
        bp = BillingProfile.objects.select_for_update().get(pk=billing_profile.pk)

        stripe_state = get_stripe_billing_state(
            subscription_id=bp.stripe_subscription_id,
            customer_id=bp.stripe_customer_id,
            expected_price_id=expected_price_id,
        )

        diffs = diff_billing_profile(bp, stripe_state)

        if diffs and not dry_run:
            apply_stripe_state_to_billing_profile(bp, stripe_state)
            logger.info(
                "sync: BillingProfile 更新 user_id=%s email=%s "
                "customer_id=%s subscription_id=%s status=%s source=%s diffs=%s",
                bp.user_id,
                bp.user.email,
                stripe_state["stripe_customer_id"],
                stripe_state["stripe_subscription_id"],
                stripe_state["status"],
                stripe_state["source"],
                diffs,
            )

    return {
        "updated": bool(diffs) and not dry_run,
        "diffs": diffs,
        "stripe_state": stripe_state,
        "dry_run": dry_run,
    }
