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

これらを `.env` に設定します。

```env
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_PRICE_ID=price_xxx