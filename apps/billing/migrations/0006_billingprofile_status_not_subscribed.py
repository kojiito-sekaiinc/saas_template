"""
BillingProfile.status の初期値を "not_subscribed" に統一する。

変更内容:
  1. 既存の status="" レコードを "not_subscribed" に更新（データ移行）
  2. STATUS_CHOICES に "not_subscribed" を追加
  3. blank=True を削除、default="not_subscribed" を追加

背景:
  CharField(blank=True) かつ default なしだと、Stripe 連携前の BillingProfile に
  空文字列が保存され、choices との整合性が取れなかった。
  "not_subscribed" はアプリ内部状態として Stripe ステータスと明確に区別される。
"""

from django.db import migrations, models


def set_not_subscribed_for_empty_status(apps, schema_editor):
    """既存の status="" レコードを "not_subscribed" に移行する。"""
    BillingProfile = apps.get_model("billing", "BillingProfile")
    updated = BillingProfile.objects.filter(status="").update(status="not_subscribed")
    if updated:
        print(f"  Migrated {updated} BillingProfile(s) from status='' to 'not_subscribed'")


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0005_alter_processedevent_created_at"),
    ]

    operations = [
        # 1. 既存データ移行（スキーマ変更より先に実行）
        migrations.RunPython(
            set_not_subscribed_for_empty_status,
            reverse_code=migrations.RunPython.noop,
        ),
        # 2. フィールド定義更新
        migrations.AlterField(
            model_name="billingprofile",
            name="status",
            field=models.CharField(
                choices=[
                    ("not_subscribed", "Not Subscribed"),
                    ("active", "Active"),
                    ("trialing", "Trialing"),
                    ("canceled", "Canceled"),
                    ("past_due", "Past Due"),
                    ("unpaid", "Unpaid"),
                    ("incomplete", "Incomplete"),
                    ("incomplete_expired", "Incomplete Expired"),
                ],
                default="not_subscribed",
                max_length=20,
            ),
        ),
    ]
