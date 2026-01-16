## 📌 Summary
<!--
このPRで何をしたかを簡潔に記載してください。
例：
- ユーザー登録（メール＋PW）を追加
- Stripe Checkout セッション作成を実装
-->

---

## 🎯 Purpose
<!--
なぜこの変更が必要か。
テンプレ全体にとっての意味も意識してください。
-->

---

## 🧱 Change Scope
該当するものにチェックを入れてください。

- [ ] `apps/app/` のみ（通常のサービス開発）
- [ ] 認証まわり（`apps/accounts/`）
- [ ] 課金・請求（`apps/billing/`）※原則変更不可
- [ ] 共通基盤 / Middleware（`apps/common/`）※原則変更不可
- [ ] 設定・ドキュメントのみ

> ⚠️ `apps/billing/` や paywall / middleware を変更した場合は、
> 下の **Justification** に必ず理由を記載してください。

---

## 📝 Justification (Required if touching locked areas)
<!--
以下を必ず明記してください：
- なぜ変更が必要だったか
- なぜテンプレ全体にとって有益か
- 代替案を検討したか
-->
- Reason:
- Template-wide benefit:
- Alternatives considered:

---

## 🔐 Billing & Paywall Safety Check (CRITICAL)

- [ ] Stripe Webhook以外で課金状態を更新していない
- [ ] success / cancel 画面で subscription を有効化していない
- [ ] `/app/` 以外に有料機能を追加していない
- [ ] `status == active` のみが有料アクセス条件になっている
- [ ] Stripe trial 機能を使用していない
- [ ] 価格・プランは単一（月980円）のまま

---

## 🛡 Template Integrity Check

- [ ] 新サービス向けの変更は `apps/app/` に閉じている
- [ ] テンプレ固有ロジックを他appに混入させていない
- [ ] 将来コピーした際に削除したくなるコードを追加していない
- [ ] フォルダ構成を勝手に変更していない

---

## ⚙️ Local Quality Checks

以下をローカルで実行しましたか？

- [ ] `python -m compileall -q .`
- [ ] `python manage.py check`
- [ ] `pytest -q`（該当する場合）

---

## 🔒 Security Checklist

- [ ] `.env` や秘密情報をコミットしていない
- [ ] Stripeキー・Webhook Secret をコードに直書きしていない
- [ ] `DEBUG` 前提のコードを本番向けに残していない
- [ ] 設定値は環境変数から取得している

---

## 🤖 AI Compliance

- [ ] `claude.md` のルールに準拠している
- [ ] `skills/*/Skill.md` の思想に反していない
- [ ] `docs/Guidelines.md` を確認した
- [ ] 不要な機能追加や改善提案を実装していない

---

## 🧪 How to Test
<!--
レビューアが動作確認するための手順を簡潔に記載してください。
例：
1. サインアップ
2. free_until を過去に変更
3. /app/ にアクセス → pricing にリダイレクト
-->

---

## 📎 Notes (Optional)
<!--
補足事項、注意点、今後の課題などがあれば記載。
-->