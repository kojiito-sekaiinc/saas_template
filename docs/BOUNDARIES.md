# BOUNDARIES — Safe Zones / Danger Zones (AI-friendly)

このテンプレは「量産」を前提にしているため、変更可能領域と要注意領域を明確にします。
AI（Claude/Codex/Cursor）にもこの境界を必ず守らせてください。

---

## 1) 変更OKゾーン（自由にいじってよい）
- `apps/app/**`：あなたのサービスの本体（機能・UI）
- `templates/app/**`：アプリUI
- `templates/billing/**`：文言・デザイン（※決済ロジックは触らない）
- `static/**`：スタイル
- `docs/**`：仕様/運用（更新推奨）

---

## 2) 要注意ゾーン（変更は慎重に。変えるなら設計から）
### 課金・アクセス制御（事故りやすい）
- `apps/common/middleware.py`（PaywallMiddleware）
- `apps/billing/views.py`
  - `checkout`
  - `portal`
  - `stripe_webhook` / `_handle_subscription_event`
- `apps/billing/models.py`（BillingProfileのコアフィールド）

変更する場合は：
- 目的・仕様を文章で確定
- RUNBOOK更新
- テストシナリオ（無料→課金→解約）を必ず実行

---

## 3) 禁止事項（テンプレ破壊の原因）
- フロントやクエリから「金額」「Price ID」「status」を受け取って決済に使う
- success/cancel 画面で課金状態を確定する（確定はWebhookのみ）
- Webhook署名検証を外す
- Paywall を「画面側の制御」だけにする（必ず middleware/server-side）

---

## 4) AIに作業させるときの許可範囲
### AIに任せてよい
- `apps/app/**` の機能追加
- `templates/**` のUI改善
- `docs/**` の追記・整備

### AIに任せるが、必ず人間レビュー
- `apps/billing/**`（課金は事故が高い）
- `apps/common/middleware.py`（アクセス制御）
- `config/settings.py`（環境差分が出やすい）

### AIに任せない（原則）
- 本番Stripeダッシュボード操作（人間が実施）
- 料金・プラン設計の最終判断（人間が決める）

---