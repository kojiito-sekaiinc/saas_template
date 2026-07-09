# Quick Start — ユースケース別エージェント利用ガイド

このドキュメントは、目的別に「どの SubAgent を、どの順番で呼ぶか」を
示す実践ガイドです。各 Agent の詳細は [docs/subagents.md](subagents.md)、
全体像は [docs/agent-workflow.md](agent-workflow.md) を参照してください。

---

## 新機能開発フロー

1. **Product Strategist** を起動し Phase 1 (Discover) を実行する。
   Product Discovery Report を確認する。
2. 承認後、Phase 2 (Product Definition) を実行する。
   `docs/product-definition.md` の内容を確認・承認する。
3. Phase 4 (Readiness Assessment) を実行し、READY / READY WITH RISKS
   であることを確認する。NOT READY の場合はここで止まる。
4. **Builder** を起動し Phase 1 (Explore) を実行する。
   `docs/product-definition.md` と `docs/product-decisions.md` を
   最優先で読んでいることを確認する。
5. Phase 2 (Plan) を実行し、`docs/implementation-plan.md` を承認する。
6. Phase 4 (Implement) を実行する。小さな目的別コミットで実装される。
7. **Reviewer** を起動し Phase 1 (Analyze) → Phase 2 (Review Plan) →
   承認 → Phase 4 (Review Execution) を実行する。
8. Release Recommendation が **APPROVED** / **APPROVED WITH RISKS**
   ならリリース候補。**CHANGES REQUIRED** / **BLOCKED** なら Builder
   に差し戻して 4〜7 を繰り返す。

---

## 簡素化フロー（コード簡素化）

1. **Sweeper** を起動し Phase 1 (Analyze) を実行する。削除候補・重複
   候補を確認する。
2. Phase 2 (Sweep Plan) を実行し、`docs/sweep-plan.md` を承認する
   （部分承認可）。
3. Phase 4 (Sweep) を実行する。実行結果と net diff を確認する。
4. **Reviewer** を Phase 1〜4 まで再度実行し、簡素化後のコードを
   レビューする。

---

## 成長施策フロー

1. **Grower** を起動し Phase 1 (Analyze) を実行する。Growth Analysis
   Report を確認する。
2. Phase 2 (Growth Plan) を実行し、`docs/growth-plan.md` を承認する
   （部分承認可。例: 「Experiment A のみ承認」）。
3. Phase 4 (Experiment / Implementation Handoff) を実行する。
   コード変更が不要な施策はそのまま実行し、コードが必要な施策は
   Builder Handoff Brief を作成する。
4. コードが必要な場合は、Builder の Explore → Plan → Human Approval
   → Implement サイクル（上記「新機能開発フロー」の 4〜6）へ進み、
   その後 Reviewer を実行する。
5. Phase 5 (Verify / Learn) を実行し、`docs/growth-decisions.md` に
   結果を記録する。

---

## リリースフロー

1. **Reviewer** を起動し Phase 1 (Analyze) → Phase 2 (Review Plan)
   → 承認 → Phase 4 (Review Execution) を実行する。
2. Release Recommendation を確認する
   （APPROVED / APPROVED WITH RISKS / CHANGES REQUIRED / BLOCKED）。
3. [docs/agent-workflow.md](agent-workflow.md) の Release Checklist
   の全項目を確認する。
4. 問題なければ Phase 5 (Verification) を実行し、
   `docs/review-decisions.md` に記録した上でリリースする。
