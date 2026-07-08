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
- Grower SubAgent v2 — 5-phase gated workflow (Analyze → Growth Plan →
  Human Approval → Experiment/Implementation Handoff → Verify/Learn),
  mandatory docs/growth-plan.md, growth decisions appended to
  docs/growth-decisions.md, Definition of Done
  (2026-07-08, Builder/Sweeper v2 と同一思想で役割分離を維持;
  100Lists専用ではなくテンプレート全体の改善として実施)
- Product Strategist SubAgent v2 — 5-phase gated workflow (Discover →
  Product Definition → Human Approval → Readiness Assessment →
  Decision Log), mandatory docs/product-definition.md, Builder
  readiness verdict (READY / NOT READY / READY WITH RISKS),
  docs/product-decisions.md as SSOT for product decisions, Product
  Decision ONLY
  (2026-07-08, Builder/Sweeper/Grower v2 と同一思想で役割分離を維持;
  100Lists専用ではなくテンプレート全体の改善として実施)