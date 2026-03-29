# RUNBOOK — Django SaaS Template

本番運用時のトラブル対応手順書。課金・アクセス制御は事故が致命傷になりやすいため、**このドキュメントを正として運用**してください。

---

## 0. アーキテクチャ概要（運用者向け）

### 責務分離

| 機能 | 担当 |
|---|---|
| 認証 | `apps/accounts`（メール＋パスワード、カスタム User） |
| 無料期間 | `accounts.Profile.free_until`（登録後 7 日） |
| 有料ゾーン | `/app/` 配下（`PaywallMiddleware` が保護） |
| 課金状態 | `billing.BillingProfile.status` |
| **課金状態の正本** | **Stripe Webhook**（署名検証あり） |
| 解約・支払い変更 | Stripe Customer Portal（`/billing/portal/`） |

### Paywall アクセス制御ルール

`/app/` にアクセスした際：

1. 未ログイン → `/accounts/login/?next=...`
2. ログイン済み & `now <= Profile.free_until` → **許可**
3. ログイン済み & `BillingProfile.status == "active"` → **許可**
4. それ以外 → `/billing/pricing/`

---

## 1. 重要なエンドポイント

| エンドポイント | 説明 |
|---|---|
| `GET /billing/pricing/` | 価格表示 |
| `POST /billing/checkout/` | 決済開始（ログイン必須） |
| `GET /billing/success/` | 決済完了画面（表示のみ） |
| `GET /billing/cancel/` | 決済キャンセル画面（表示のみ） |
| `GET /billing/portal/` | Customer Portal（ログイン必須） |
| `POST /stripe/webhook` | Webhook 受信（CSRF exempt + 署名検証） |

---

## 2. トラブル時に最初に見る「一次情報」

### 優先順位

**1. Django Admin**
- `accounts.User`（対象ユーザー）
- `accounts.Profile`（`free_until`）
- `billing.BillingProfile`（`status` / `stripe_customer_id` / `stripe_subscription_id` / `current_period_end`）

**2. Stripe Dashboard**
- Customer（email で検索）
- Subscription（`status` / `items` / `price`）
- Webhook Logs（イベントが届いているか、レスポンスコードは何か）

**3. アプリ側ログ**

| ログメッセージ | 意味 |
|---|---|
| `Stripe webhook received: event_id=...` | Webhook がアプリに到達した |
| `BillingProfile updated from Stripe webhook` | DB 更新が実行された |
| `Ignoring subscription ... does not match expected price ID` | Price ID 不一致でスキップされた |
| `Invalid payload` / `Invalid signature` | Webhook 署名検証失敗 |

---

## 3. よくあるトラブルと対応手順

### ケース A：課金したのに `/app/` に入れない

**症状**: ユーザーは決済完了したと言うが、`/app/` が `/billing/pricing/` に飛ぶ。

**確認手順**:
1. Admin → `BillingProfile` を確認
   - `status` が `"active"` か？
   - `stripe_customer_id` / `stripe_subscription_id` は入っているか？
2. Stripe Dashboard → Subscription を確認
   - `status` は何か？
   - `items` に **このアプリの Price**（`STRIPE_PRICE_ID`）が入っているか？
3. Stripe Webhook Logs
   - `customer.subscription.updated` 等が **200** で配信されているか？
4. Stripe 側が `active` なのに DB が更新されない → [ケース C](#ケース-c-webhook-が機能していない)

**緊急回避**:
- Stripe 側で `active` が確認できた場合のみ、Admin で一時的に `BillingProfile.status = "active"` に救済。
- 後で必ず Webhook を復旧し、`sync_billing_from_stripe` で整合性を確認する。

---

### ケース B：解約したのに `/app/` に入れてしまう

**原因候補**:
- Webhook が届いていない（`status` が `active` のまま）
- Stripe 側の cancellation が「期末まで有効」で、まだ `active` 扱い
- Portal で操作したが反映待ち

**確認手順**:
1. Stripe Dashboard → Subscription の `status` と `current_period_end` を確認
2. Admin → `BillingProfile.status` と `current_period_end` を確認
3. Webhook Logs で `customer.subscription.updated` / `deleted` が届いているか確認
4. Stripe 側で `canceled` なのに DB が `active` → [ケース C](#ケース-c-webhook-が機能していない)

---

### ケース C：Webhook が機能していない

**症状**: 課金反映が遅れる / 反映されない / 解約が反映されない。

**確認手順**:
1. 環境変数チェック
   - `STRIPE_WEBHOOK_SECRET` が正しいか（Stripe 側の signing secret と一致しているか）
   - `STRIPE_PRICE_ID` が設定されているか（未設定だと price 検証がスキップされる）
2. Stripe Dashboard → Webhook endpoint
   - URL が `{SITE_URL}/stripe/webhook` と一致しているか
   - イベントが 2xx で処理されているか（4xx/5xx ならレスポンス内容確認）
3. アプリ側ログで `Invalid payload` / `Invalid signature` が出ていないか
4. よくあるミス
   - `SITE_URL` / ドメイン変更後に Webhook URL を更新し忘れ
   - test / live の混在（Price ID / secret key / webhook secret が環境と不一致）

**復旧後**: `sync_billing_from_stripe` で乖離したレコードを修正する（→ [セクション 4](#4-webhook-未達時の手動再同期)）。

---

### ケース D：`/billing/portal/` に行っても pricing に戻される

**原因候補**:
- `BillingProfile` が存在しない
- `stripe_customer_id` が未作成（checkout を踏んでいない）

**確認手順**:
1. Admin で `BillingProfile` を確認
2. `stripe_customer_id` が空なら、`POST /billing/checkout/` を正しく通して Customer を作成する
3. それでも不整合ならログで `StripeError` を確認

---

## 4. Webhook 未達時の手動再同期

Webhook が届かず `BillingProfile` が Stripe と乖離した場合、`sync_billing_from_stripe` コマンドで整合性を回復できます。

**特性**:
- Stripe に対して read-only（Stripe 側のデータは変更しない）
- `last_stripe_event_created` は更新しない（Webhook ロジックの管理外）
- 1 ユーザーずつ独立して処理（一部失敗しても他は継続）

### 使い方

```bash
# 差分確認（DB は更新しない）
python manage.py sync_billing_from_stripe --user-id 1 --dry-run
python manage.py sync_billing_from_stripe --email user@example.com --dry-run

# 1 ユーザーを同期
python manage.py sync_billing_from_stripe --user-id 1
python manage.py sync_billing_from_stripe --email user@example.com

# 全ユーザーを一括同期（本番では必ず --dry-run で確認後に実行）
python manage.py sync_billing_from_stripe --all --dry-run
python manage.py sync_billing_from_stripe --all
```

### 出力の読み方

```
UPDATED      {"user_id": 1, "diffs": {"status": {"before": "not_subscribed", "after": "active"}}}
NO_CHANGE    {"user_id": 2, ...}
WOULD_UPDATE {"user_id": 3, ...}   # --dry-run 時（実際には更新しない）
ERROR        user_id=4 error=...    # このユーザーはスキップして次へ
```

### 注意事項

- 本番での `--all` 実行前には必ず `--dry-run` で差分を確認する
- 大量ユーザーに実行する場合は Stripe API レートリミットに注意
- 手動修正後は Webhook 経路の復旧を忘れずに行う

---

## 5. 手動復旧ポリシー

- **原則**: Stripe + Webhook が真実の源泉。手動 DB 更新は例外。
- **例外対応する場合**:
  - Stripe 側の状態（Customer / Subscription）を必ず確認してから変更する
  - Admin で変更したら「いつ」「誰が」「何を」変えたかを Issue / メモに残す

---

## 6. デプロイ前後チェック

### デプロイ前チェック

```bash
# 設定不備を一括確認
python manage.py check_deploy_config

# WARNING でも失敗扱いにしたい場合（CI 推奨）
python manage.py check_deploy_config --fail-on-warning

# JSON 形式（スクリプト連携用）
python manage.py check_deploy_config --json
```

**正常時の出力例:**

```
OK       DEBUG                    DEBUG=False
OK       SITE_URL                 https://example.com
OK       ALLOWED_HOSTS            example.com
OK       SITE_URL_IN_ALLOWED_HOSTS example.com in ALLOWED_HOSTS
OK       CSRF_TRUSTED_ORIGINS     ok
OK       STRIPE_SECRET_KEY        set
OK       STRIPE_PRICE_ID          price_live_xxx
OK       STRIPE_WEBHOOK_SECRET    set

Summary: ok=8 warning=0 error=0
```

ERROR が 1 件でもあると exit(1)。

### テスト実行

テストランナーは **pytest** に統一されています（`python manage.py test` は使用しない）。

```bash
# 全テスト
pytest

# billing ロジックのみ
pytest apps/billing/

# 全品質チェック（compile + Django check + pytest）
./scripts/checks/quick_check.sh
```

**主なテスト実行タイミング:**

| タイミング | コマンド |
|---|---|
| デプロイ前 | `./scripts/checks/quick_check.sh` |
| billing / paywall 変更後 | `pytest apps/billing/ apps/common/` |
| 再同期コマンド実行前 | `pytest apps/billing/test_sync.py` |
| 障害調査時 | `pytest apps/billing/ -v` |

### デプロイ前チェックリスト

- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` に本番ドメイン
- [ ] `SITE_URL=https://<prod-domain>`
- [ ] Stripe 本番キー一式（live）に切替済み
- [ ] `STRIPE_PRICE_ID` は本番 Price
- [ ] 本番 Webhook endpoint 登録済み（events: subscription.created / updated / deleted）
- [ ] `python manage.py migrate`
- [ ] `./scripts/checks/quick_check.sh`

### デプロイ後スモークテスト

- [ ] 新規登録 → `/app/` に入れる（free trial）
- [ ] Admin で `free_until` を過去に変更 → `/app/` が pricing に飛ぶ
- [ ] 決済 → Webhook 反映 → `/app/` に入れる
- [ ] Portal で解約 → Webhook 反映 → `/app/` に入れなくなる

---

## 7. 要注意ファイル（変更は慎重に）

| ファイル | 内容 |
|---|---|
| `apps/common/middleware.py` | Paywall ロジック |
| `apps/billing/views.py` | checkout / portal / stripe_webhook |
| `apps/billing/models.py` | BillingProfile |
| `apps/billing/services.py` | Stripe 連携ビジネスロジック |
| `.env` | Stripe キー等の秘匿情報 |

---

## 8. セキュリティ

### HTTPS / HSTS

- `DEBUG=False` にすると HTTPS 強制 & HSTS 有効になる
- Railway 本番は必ず HTTPS で公開する前提

### ログイン防御の設計方針

**有効な防御**: `django-axes` をアカウント（email アドレス）単位でロックアウト設定済み。

- 5 回失敗 → 1 時間ロック（`AXES_FAILURE_LIMIT=5`, `AXES_COOLOFF_TIME=1`）
- ログイン成功時に失敗カウントをリセット（`AXES_RESET_ON_SUCCESS=True`）
- 対象：特定アカウントへの総当たり攻撃・パスワードスプレー攻撃

**カバーしない脅威**: IP を変えながら多数アカウントを試す **credential stuffing** には対応していない。

> IP ベースの制限追加を検討した結果、`django-axes` は全軸に同じ `AXES_FAILURE_LIMIT` が適用されるため、IP 軸を追加すると企業ネットワーク・共有 IP・モバイル回線の正当ユーザーが誤ってロックアウトされるリスクがある。これは意図的なトレードオフ。

**credential stuffing への将来的な対処**:
- CDN / WAF（Cloudflare 等）での IP レートリミット
- リバースプロキシでのリクエスト制限
- ログイン失敗ログの監視とアラート

---

変更する場合は、同時にこの RUNBOOK も更新してください。
