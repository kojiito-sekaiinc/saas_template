# Template Evolution

このドキュメントは、個別プロダクトの開発を通じて見つかった、
テンプレート全体を改善すべき項目を管理する。

## Proposed

- Billing Strategy abstraction
- Feature Gate support
- Usage Limit support

## Accepted

-

## Implemented

- Builder SubAgent v2 — 5-phase gated workflow
  (Explore → Plan → Human Approval → Implement → Verify),
  mandatory docs/implementation-plan.md, Definition of Done
  (2026-07-07, 100Lists開発の知見をテンプレートへ還元)
- Sweeper SubAgent v2 — 5-phase gated workflow
  (Analyze → Sweep Plan → Human Approval → Sweep → Verify),
  mandatory docs/sweep-plan.md, Delete-over-Add Definition of Done
  (2026-07-07, Builder v2 と同一思想で役割分離を維持)