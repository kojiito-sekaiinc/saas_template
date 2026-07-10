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
- Reviewer SubAgent v2 — 5-phase gated workflow (Analyze → Review
  Plan → Human Approval → Review Execution → Verification), mandatory
  docs/review-plan.md, review decision log
  (docs/review-decisions.md), governance review (CLAUDE.md /
  docs/BOUNDARIES.md / Section 4-bis), release readiness verdict
  (APPROVED / APPROVED WITH RISKS / CHANGES REQUIRED / BLOCKED),
  Review ONLY
  (2026-07-08, Builder/Sweeper/Grower/Product Strategist v2 と
  同一思想で役割分離を維持; 100Lists専用ではなくテンプレート全体の
  改善として実施)
- Agent Orchestrator v1 — artifact-driven multi-agent workflow, role
  boundaries, standard development flow, and release coordination
  across Product Strategist, Builder, Sweeper, Grower, and Reviewer
  (2026-07-08)
- Template Sync Agent v1 — 5-phase gated workflow (Analyze → Sync
  Plan → Human Approval → Sync Execution → Verification), Template
  Drift Management ONLY, Apply / Preserve / Conflict / Ignore
  classification, mandatory docs/template-sync-plan.md,
  template-sync decision log (docs/template-sync-decisions.md),
  protects derived app-specific files and approved billing
  strategies
  (2026-07-10, 100Lists Template Sync作業の知見をテンプレートへ還元)