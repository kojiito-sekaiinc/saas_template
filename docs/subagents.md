# SubAgents Reference

各 SubAgent の Purpose / Responsibilities / Inputs / Outputs /
Typical Usage / Common Mistakes をまとめたリファレンスです。実行順序や
成果物の受け渡しは [docs/agent-workflow.md](agent-workflow.md) を、
実際の Agent 定義（プロンプト仕様そのもの）は `.claude/agents/*.md`
を参照してください。

---

## Product Strategist

**Purpose**: 何を作るかを決める。MVP スコープ・課金戦略の提案・Builder
着手可否判定を担う。Product Decision ONLY — 実装はしない。

**Responsibilities**: MVP scope 定義、Product Decision、ユーザーペルソナ、
価値仮説、課金戦略提案（CLAUDE.md Section 4-bis 対象）、Builder
Readiness 判定、曖昧さ・矛盾・不足情報の検出。

**Inputs**: docs/product-context.md, docs/mvp-scope.md,
docs/growth-decisions.md, docs/pricing.md, docs/vision.md,
docs/user-feedback.md, 過去の docs/product-decisions.md エントリ。

**Outputs**: docs/product-definition.md, Readiness verdict
（READY / NOT READY / READY WITH RISKS）, docs/product-decisions.md
の新規エントリ。

**Typical Usage**: 新機能・新サービスの立ち上げ時に最初に呼ぶ。
「何を作るか」が曖昧・矛盾しているときに呼ぶ。

**Common Mistakes**:
- 実装の詳細（モデル・URL・UI）まで決めようとしてしまう
  （それは Builder の責務）
- 承認前に Builder Readiness を勝手に READY と判定してしまう
- 過去の docs/product-decisions.md の決定を確認せず、矛盾する新しい
  決定をしてしまう

---

## Builder

**Purpose**: 承認済みの product-definition を、テンプレートのフル
スタック（Django / Stripe / paywall 等）に沿って実装する。
Implementation ONLY。

**Responsibilities**: モデル・ビュー・テンプレート・テストの実装、
小さな目的別コミット。

**Inputs**: docs/product-definition.md と docs/product-decisions.md
（最優先で読む）、docs/product-context.md, docs/mvp-scope.md,
docs/growth-decisions.md, apps/, templates/, tests/,
docs/BOUNDARIES.md。

**Outputs**: docs/implementation-plan.md, コミット済みコード,
Implementation Report。

**Typical Usage**: Product Strategist の承認が下りた直後、または
承認済みの Grower Handoff（Builder Handoff Items）を受け取った直後に
呼ぶ。

**Common Mistakes**:
- 製品判断（何を作るべきか）を自分で決めてしまう
- docs/implementation-plan.md の承認前に実装を始めてしまう
- billing / paywall のコアロジックを無承認で変更してしまう
  （CLAUDE.md Section 4-bis 違反）
- Sweeper の仕事（不要コード削除）まで一緒にやってしまう

---

## Reviewer

**Purpose**: 実装品質・アーキテクチャ・セキュリティ・テスト品質・
ガバナンス・リリース可否を評価する。Review ONLY — 修正はしない。

**Responsibilities**: 実装品質 / アーキテクチャ / セキュリティ /
テスト品質レビュー、CLAUDE.md・docs/BOUNDARIES.md 準拠確認、Product
Decision 逸脱検知、CLAUDE.md Section 4-bis ガバナンス違反検知、
Technical Debt 可視化、リリース判定。

**Inputs**: CLAUDE.md, docs/BOUNDARIES.md, docs/product-definition.md,
docs/product-decisions.md, docs/implementation-plan.md,
docs/sweep-plan.md, docs/growth-plan.md, docs/growth-decisions.md,
docs/review-decisions.md（あれば）, apps/, templates/, tests/, CI 設定,
billing / paywall コード。

**Outputs**: docs/review-plan.md, Review Report + Release
Recommendation, docs/review-decisions.md の新規エントリ。

**Typical Usage**: Builder の実装完了直後、または簡素化後・リリース前に
必ず呼ぶ。

**Common Mistakes**:
- 指摘した問題を自分で直接修正してしまう（Reviewer は指摘のみ、
  修正は Builder / Sweeper が行う）
- Bash で一時ファイル以上の変更（コミット・push・追跡ファイルの変更）
  をしてしまう
- Critical findings が残ったまま APPROVED にしてしまう

---

## Sweeper

**Purpose**: 実装後の不要なコード・重複・複雑さを削る。
Simplification ONLY — 機能は追加しない。

**Responsibilities**: 不要な View / URL / Template / 重複コード /
過剰な抽象化の削除、可読性改善。

**Inputs**: docs/implementation-plan.md, docs/mvp-scope.md,
docs/growth-decisions.md, docs/BOUNDARIES.md, apps/, templates/,
tests/。

**Outputs**: docs/sweep-plan.md, Sweep Report（net diff 付き）。

**Typical Usage**: Reviewer の承認後、マージ前に呼ぶ。

**Common Mistakes**:
- 新機能や新しい抽象化を追加してしまう（Sweeper は削除・簡素化のみ）
- MVP スコープ外に見えるものを自分の判断だけで削除してしまう
  （リスクとして報告し、判断は人間に委ねる）
- 削除したコードのテスト・URL・import を消し忘れる

---

## Grower

**Purpose**: 活性化・定着・転換率・価格・オンボーディングの改善仮説を
立て、検証する。Growth diagnosis and experiment design ONLY —
実装はしない。

**Responsibilities**: Growth diagnosis、Growth Hypothesis / Experiment
設計、Metrics 定義、User Feedback 整理、MVP 後の優先順位付け。

**Inputs**: docs/product-context.md, docs/mvp-scope.md,
docs/growth-decisions.md, docs/implementation-plan.md,
docs/sweep-plan.md, docs/metrics.md, docs/pricing.md,
docs/user-feedback.md, docs/experiments.md。

**Outputs**: docs/growth-plan.md, Handoff Report（非コード施策 or
Builder Handoff Brief）, docs/growth-decisions.md の新規エントリ。

**Typical Usage**: MVP が一通り実装・レビュー・簡素化された後、次に
何を改善するか決めるときに呼ぶ。

**Common Mistakes**:
- 自分でコード・テンプレートを変更してしまう（コピー修正であっても
  Builder / 人間に委譲する）
- 承認前に施策を実行してしまう
- 課金・Paywall の変更を Section 4-bis 承認なしに Builder へ引き継いで
  しまう

---

## Agent Orchestrator

**Purpose**: どの Agent を使うか、どの順番で、どの成果物を受け渡すかを
定義する「交通整理役」。SubAgent ではない — 自らは何も決定・実装・レビュー
・成長判断をしない。

**Responsibilities**: Agent 実行順序の定義、成果物受け渡しの定義、
責務境界の明文化、リリースまでの標準フローの定義。

**Inputs**: なし（他 Agent の成果物一覧を横断的に参照するのみ）。

**Outputs**: docs/agent-workflow.md。

**Typical Usage**: 複数の Agent が関わる変更に着手する前に、まずこの
ドキュメントで全体の流れを確認する。

**Common Mistakes**:
- Orchestrator がそのまま製品判断・実装・レビュー・成長判断をして
  しまう（Orchestrator は判断しない）
- docs/agent-workflow.md を実際の Agent 運用と乖離させたまま放置して
  しまう

---

## Template Sync

**Purpose**: テンプレート本体と派生アプリの差分（Template Drift）を
安全に管理する。Template Drift Management ONLY — 製品判断・新機能実装・
リファクタリング・成長施策・レビュー代行・テンプレート自体の改善提案は
行わない。

**Responsibilities**: Template Drift Analysis、Apply / Preserve /
Conflict / Ignore への分類、Sync Plan 作成、派生アプリ固有実装・
承認済み課金戦略の保護、同期後の検証、同期履歴の記録。

**Inputs**: テンプレート本体（Analyze フェーズで Repository / Branch /
Commit SHA / Fetch Time を固定）、CLAUDE.md, docs/agent-workflow.md,
docs/template-evolution.md, `.claude/agents/**`, README.md, docs/**,
apps/**, templates/**, tests/**, CI設定, billing/paywall 関連コード。

**Outputs**: docs/template-sync-plan.md, Sync Execution 結果
（承認済み Apply 項目のみ）, docs/template-sync-decisions.md の新規
エントリ。

**Typical Usage**: テンプレート本体が更新され、既存の派生アプリへ
その更新を安全に取り込みたいときに呼ぶ。

**Common Mistakes**:
- Preserve 対象（apps/app、templates/app、tests/e2e、Product Docs、
  承認済み Freemium など）を無承認で変更してしまう
- Conflict 対象（billing/paywall、middleware.py、settings.py、CI
  設定など）を人間の判断なしに Apply してしまう
- Analyze フェーズで固定した Commit SHA ではなく、動く `main`
  ブランチを Sync Execution で再取得してしまう
- Sync Execution フェーズで承認なく `git push` してしまう
  （push は Verification フェーズで、明示的な承認がある場合のみ）
