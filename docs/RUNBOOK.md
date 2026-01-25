# RUNBOOK — Django SaaS Template (Auth + Free Trial + Stripe Subscription + Portal)

このドキュメントは、このテンプレートで構築された SaaS の **本番運用時のトラブル対応手順**をまとめたものです。
「課金・アクセス制御」は事故が致命傷になりやすいため、**このRUNBOOKを正として運用**してください。

---

## 0. アーキテクチャ概要（運用者向け）

### 認証・無料期間・課金の責務分離
- **認証**：`accounts`（メール＋パスワード、カスタムUser）
- **無料期間**：`accounts.Profile.free_until`（初回ログイン/アクセス時に自動作成、7日）
- **有料ゾーン**：`/app/` 配下（`PaywallMiddleware` が保護）
- **課金状態**：`billing.BillingProfile.status`（Stripeの subscription status を保存）
- **課金状態の真実の源泉**：**Stripe Webhook**（署名検証あり）
- **課金の編集（解約/支払い方法変更）**：**Stripe Customer Portal**（`/billing/portal/`）

### アクセス制御ルール（Paywall）
`/app/` へアクセスした際：
1. 未ログイン → `/accounts/login/?next=...`
2. ログイン済み & `now <= Profile.free_until` → 許可
3. ログイン済み & `BillingProfile.status in ("active","trialing")` → 許可
4. それ以外 → `/billing/pricing/`

---

## 1. 重要なエンドポイント一覧

- 価格表示：`GET /billing/pricing/`
- 決済開始：`POST /billing/checkout/`（ログイン必須）
- 決済完了画面：`GET /billing/success/`（informational only）
- 決済キャンセル画面：`GET /billing/cancel/`（informational only）
- ポータル：`GET /billing/portal/`（ログイン必須）
- Webhook：`POST /stripe/webhook`（CSRF exempt + 署名検証）

---

## 2. まず見るべき「一次情報」（最優先）

トラブル時は次の順で確認します。

1) **Django Admin**
- `accounts.User`（対象ユーザー）
- `accounts.Profile`（free_until）
- `billing.BillingProfile`（status / stripe_customer_id / stripe_subscription_id / current_period_end）

2) **Stripe Dashboard**
- Customer（emailで検索）
- Subscription（status / items / price）
- Webhook Logs（イベントが届いているか）

3) **アプリ側ログ**
- `stripe_webhook` の受信ログ（署名エラー/400/500 など）
- ★ `Stripe webhook received: event_id=... , type=...` が出ているか（Webhookがアプリに到達しているかの一次確認）
- ★ `BillingProfile updated from Stripe webhook` が出ているか（DB更新が行われたか）
- `Ignoring subscription ... does not match expected price ID` が出ていないか
- Webhook調査時は、ログに出力される `event_id` をキーに Stripe Dashboard の Webhook Logs と突合する

---

## 3. よくあるトラブルと対応手順

### ケースA：課金したのに /app/ に入れない
**症状**
- ユーザーは決済完了したと言うが、`/app/` が `/billing/pricing/` に飛ぶ。

**原因候補**
- Webhookが届いていない
- BillingProfile.status が active になっていない
- Stripe側は別Priceのサブスク（Price ID チェックで無視されている）
- free trial が切れている

**手順**
1. Django Admin → `BillingProfile` を確認
   - `status` が `"active"` or `"trialing"` か？
   - `stripe_customer_id` / `stripe_subscription_id` は入っているか？
2. Stripe Dashboard → Subscription を確認
   - `status` は何か？
   - `items` に **このアプリの Price**（`STRIPE_PRICE_ID`）が入っているか？
3. Stripe Webhook Logs
   - `customer.subscription.updated` 等が **200** で配信されているか？
4. もし Stripe側が active なのに DB が更新されない場合
   - Webhook secret / endpoint URL / サーバログを確認（ケースCへ）

**緊急回避（例外）**
- Stripe側で active であることが確認できた場合のみ、Admin で一時的に `BillingProfile.status="active"` にして救済。
- 後で必ず Webhook を復旧し、整合性を取る。

---

### ケースB：解約したのに /app/ に入れてしまう
**原因候補**
- Webhookが届いていない（status が active のまま）
- Stripe側の cancellation が「期末まで有効」で、まだ active 扱い
- Portalで操作したが戻り後に反映待ち

**手順**
1. Stripe Dashboard → Subscription の `status` と `current_period_end` を確認
2. Django Admin → `BillingProfile.status` と `current_period_end` を確認
3. Webhook logs で `customer.subscription.updated`/`deleted` が届いているか確認
4. Stripe側で `canceled` なのに DB が active の場合
   - Webhook復旧（ケースC）
   - 緊急なら Admin で status を `canceled` 等に更新

---

### ケースC：Webhookが機能していない（課金状態が更新されない）
**症状**
- 多人数で課金反映が遅れる/反映されない、解約が反映されない。

**手順**
1. 環境変数チェック
   - `STRIPE_WEBHOOK_SECRET` が正しいか（Stripe側の signing secret と一致）
   - `STRIPE_PRICE_ID` が設定されているか（未設定だと price 検証がスキップされる）
2. Stripe Dashboard → Webhook endpoint
   - URL が `SITE_URL + "/stripe/webhook"` と一致しているか
   - イベントが 2xx で処理されているか（4xx/5xx ならレスポンス内容確認）
3. アプリ側ログ
   - `Invalid payload` / `Invalid signature` が出ていないか
   - `Ignoring subscription ... does not match expected price ID` が出ていないか
4. よくあるミス
   - `SITE_URL` / ドメイン変更後に Webhook URL を更新し忘れ
   - test / live の混在（Price ID / secret key / webhook secret が環境と一致していない）

---

### ケースD：/billing/portal/ に行っても pricing に戻される
**原因候補**
- `BillingProfile` が無い
- `stripe_customer_id` が未作成（checkout を踏んでいない）
- checkout はしたが customer_id 保存前に失敗

**手順**
1. Admin で `BillingProfile` を確認
2. `stripe_customer_id` が空なら、
   - 一度 `POST /billing/checkout/` を正しく通して Customer を作る
   - Stripe側でCustomerを作ったなら、Webhookでなくここはアプリが保存する仕様（checkout内）
3. それでも不整合ならログ確認（StripeError）

---

## 4. 手動復旧ポリシー（重要）
- 原則：**Stripe + Webhook が真実の源泉**。手動DB更新は例外。
- 例外対応する場合：
  - Stripe側の状態（Customer/Subscription）を必ず確認
  - Adminで変更したら、必ず「いつ」「誰が」「何を」変えたかを残す（メモ/Issue/PR）

---

## 5. デプロイ前後チェック（本番運用）
### デプロイ前
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` に本番ドメイン
- [ ] `SITE_URL=https://<prod-domain>`
- [ ] Stripe 本番キー一式（live）に切替済み
- [ ] `STRIPE_PRICE_ID` は本番Price
- [ ] 本番Webhook endpoint 登録済み（events: subscription.created/updated/deleted）
- [ ] `python manage.py migrate`
- [ ] `./scripts/checks/quick_check.sh`

### デプロイ後スモークテスト
- [ ] 新規登録 → `/app/` へ入れる（free trial）
- [ ] free trial を過去に（Adminで free_until を過去へ） → `/app/` が pricing に飛ぶ
- [ ] 決済（テスト/本番） → Webhook 反映 → `/app/` に入れる
- [ ] Portal で解約 → Webhook 反映 → `/app/` に入れなくなる（必要なら）

---

## 6. 要注意ファイル（変更は慎重に）
- `apps/common/middleware.py`（Paywall）
- `apps/billing/views.py`（checkout / portal / stripe_webhook）
- `apps/billing/models.py`（BillingProfile）
- `.env`（Stripe関連）

## 7. セキュリティ関連の補足
- DEBUG=False にすると HTTPS 強制 & HSTS 有効になる
- Railway 本番は必ず https で公開する前提であること

変更する場合は、同時にこのRUNBOOKも更新すること。