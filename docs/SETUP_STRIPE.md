# SETUP_STRIPE — Stripe設定手順（Subscription + Webhook + Portal）

このドキュメントは、本プロジェクトで **Stripeサブスクリプション課金を正しく動作させるための設定手順**をまとめたものです。

本テンプレでは、**Stripeを唯一の課金状態の真実の源泉**とし、  
アプリ側では Webhook を通じて状態を反映します。

---

## 0. 前提

- Stripe アカウントを作成済み
- Stripe Dashboard にログイン可能
- 本プロジェクトをローカルで起動できる状態

---

## 1. Stripe Dashboard のモード確認（重要）

Stripe Dashboard 右上で以下を確認してください：

- 🧪 **Test mode**：ローカル・検証用
- 🚀 **Live mode**：本番用

**最初は必ず Test mode で作業してください。**

---

## 2. Product / Price（サブスクリプション）の作成

### 2.1 Product 作成

1. Stripe Dashboard → **Products**
2. **Add product**
3. 設定例：
   - Name：任意（例：`Monthly Plan`）
   - Description：任意

### 2.2 Price 作成（重要）

- Pricing model：**Standard pricing**
- Price type：**Recurring**
- Billing period：**Monthly**
- Currency：**JPY**
- Unit amount：**980**（テンプレ初期値）
- Trial period：**設定しない**（無料期間はアプリ側で制御）

保存後、**Price ID（`price_xxx`）を控える**。

---

## 3. APIキーの取得

Stripe Dashboard → **Developers → API keys**

### Test mode（開発用）
- Publishable key：`pk_test_...`
- Secret key：`sk_test_...`

Secret key を `.env` に設定します。
Publishable key はこのテンプレでは未使用です（Stripe Checkout のサーバーサイドリダイレクトのみ使用）。

```env
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PRICE_ID=price_xxx
```

4. Webhook の設定（最重要）

4.1 Webhook エンドポイント作成

Stripe Dashboard → Developers → Webhooks → Add endpoint

Endpoint URL
```
<SITE_URL>/stripe/webhook
```

例（ローカル）：
```
https://xxxx.ngrok.io/stripe/webhook
```

例（本番）：
```
https://your-domain.com/stripe/webhook
```

Events to send（必須）
以下を 必ず指定してください：
	•	customer.subscription.created
	•	customer.subscription.updated
	•	customer.subscription.deleted

👉 それ以外は不要です

4.2 Signing secret の設定

Webhook 作成後に表示される：
```
whsec_xxxxxxxxx
```
を .env に設定します。

```
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

5. ローカル開発時の Webhook 受信（ngrok）

Stripe は localhost に直接 Webhook を送れないため、
ngrok 等のトンネリングツールを使用します。

5.1 ngrok 起動
```
ngrok http 8000
```

表示された URL（例）：
```
https://abcd1234.ngrok.io/stripe/webhook
```

5.2 Webhook URL 更新

Stripe Dashboard の Webhook Endpoint を：
```
https://abcd1234.ngrok.io/stripe/webhook
```
に変更します。

6. 動作確認フロー（必ず実施）

6.1 課金フロー確認
	1.	アプリ起動
	2.	新規ユーザー登録 → ログイン
	3.	/billing/pricing/ にアクセス
	4.	Subscribe Now
	5.	Stripe Checkout へ遷移

テストカード
```
カード番号: 4242 4242 4242 4242
有効期限: 任意（未来）
CVC: 任意
```

	6.	決済完了 → /billing/success/

6.2 Webhook 確認（超重要）
	1.	Stripe Dashboard → Webhooks → 該当エンドポイント
	2.	customer.subscription.created / updated が 200 OK になっている
	3.	Django Admin → BillingProfile を確認
	•	status：active
	•	stripe_customer_id / stripe_subscription_id が入っている
	4.	/app/ にアクセスできることを確認

7. Customer Portal の確認
	1.	ログインした状態で以下にアクセス：
    ```
    /billing/portal/
    ```

    	2.	Stripe Customer Portal にリダイレクトされる
	3.	以下が可能なことを確認：
	•	サブスクリプション解約
	•	支払い方法の変更
	•	請求履歴の確認
	4.	解約後：
	•	Stripe Webhook が届く
	•	BillingProfile.status が canceled 等に変わる
	•	/app/ に入れなくなる（Paywall）

8. よくあるミスと注意点

❌ success / cancel 画面で課金を確定しない
	•	課金状態の確定は Webhookのみ
	•	success ページは informational only

❌ フロントから金額・Price ID を渡さない
	•	金額・Price ID は 必ずサーバ側 env から参照

❌ Webhook 署名検証を外さない
	•	セキュリティ事故の原因になります

❌ Test / Live の混在
	•	Test mode のキーと Live mode の Price ID を混ぜない

❌ 複数の SaaS で同一 Stripe アカウントを共有しない
	•	このテンプレートは複数サービスへの複製を前提としている。
		複製した各サービスは 原則としてサービスごとに別の Stripe アカウント
		（または少なくとも別の Webhook Endpoint + 別の Price）を使うこと。
	•	理由：Webhook イベントはアカウント単位で配信される。
		同一アカウントを共有すると、サービスAの解約
		（customer.subscription.deleted 等）がサービスBの
		Webhook にも届き、customer_id 経由で B 側のユーザーに
		紐づいて課金状態を誤って上書きするリスクがある。
	•	特に customer.subscription.deleted は Price 検証を通らない経路が
		あるため、アカウント共有時の混在イベントは事故に直結する。
	•	やむを得ず共有する場合は、Webhook Endpoint の対象イベントを絞り、
		自サービスの Price / Subscription ID 以外を無視することを確認してから
		運用すること。

⸻

9. 本番移行チェックリスト（簡易）
	•	Stripe Dashboard を Live mode に切替
	•	Live用 Product / Price を作成
	•	.env を Live 用キーに更新
	•	本番 Webhook Endpoint 作成
	•	SITE_URL が本番URL
	•	本番でテスト決済（少額）を実施
	•	Webhook が 200 で処理されている

⸻

10. 関連ドキュメント
	•	運用手順：docs/RUNBOOK.md
	•	テンプレ起動：README.md
	•	再利用チェック：docs/TEMPLATE_CHECKLIST.md
	•	境界線：docs/BOUNDARIES.md