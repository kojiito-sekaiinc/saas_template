# Claude Instructions — HIGHEST PRIORITY

This document defines the **authoritative, highest-priority rules**
for this repository.

ALL instructions, prompts, and code changes MUST strictly follow
this document.

If there is any conflict between:
- this document
- skill definitions
- guidelines
- prompts or suggestions

**THIS DOCUMENT ALWAYS TAKES PRECEDENCE.**

---

## 1. Purpose of This Repository

This repository is a **reusable SaaS TEMPLATE**.

Its goals are:
- Rapid SaaS releases (≈ 2-week cycles)
- Validation of real user demand via **paid subscriptions**
- Safe duplication and reuse for many future services

This is NOT a one-off application.
This repository must remain **stable, safe, and reusable**.

---

## 2. Applied Skills (MANDATORY)

All implementation MUST comply with the following skill definitions.
These skills define your **role, mindset, and decision boundaries**.

You must continuously reference and respect them.

### Applied Skill Files
- `.claude/skills/django-saas-engineer/SKILL.md`
- `.claude/skills/subscription-saas-billing-specialist/SKILL.md`
- `.claude/skills/template-oriented-developer/SKILL.md`

Violation of any skill is considered a violation of this specification.

---

## 3. Fixed Technology Stack (NON-NEGOTIABLE)

The technology stack is **fixed**:

- Backend: Django
- Frontend: Django Templates + Tailwind CSS
- Authentication: Email + Password (Django standard auth)
- Database: PostgreSQL (Railway, Django ORM)
- Payments: Stripe (subscription model)
- Deployment: Railway
- Dependency management: requirements.txt

No substitutions or architectural changes are allowed unless explicitly instructed.

---

## 4. Core Business Rules (DEFAULT)

This section defines the **default billing model** for this template:
**Trial-based Subscription**. It applies unless an alternative Billing
Strategy has been through the governance process in **Section 4-bis**.

### Subscription (Default)
- Subscription billing ONLY
- Monthly billing ONLY
- Single plan ONLY
- Price: **980 JPY / month**

### Free Access (Default)
- Free usage for **7 days after signup**
- No credit card required during free period
- Free period is managed by application logic (`Profile.free_until`)
- Stripe trial feature MUST NOT be used

These defaults are what Claude Code MUST implement unless Section
4-bis's approval process has been completed for this product.

---

## 4-bis. Billing Strategy Governance (Template Evolution)

This template must stay safe to duplicate and reuse, while still
letting individual SaaS products adopt a different billing model than
the Trial-based Subscription default (e.g. Freemium, Usage-based,
Feature-based, or tiered plans).

### When an Alternative Billing Strategy May Be Used

An alternative Billing Strategy is allowed for a derived product ONLY
when **all** of the following are true:

1. The strategy is explicitly documented in `docs/product-context.md`
   under its `## Billing Strategy` section (e.g. `Freemium`,
   `Usage-based`, `Feature-based`).
2. The **template owner** has explicitly approved adopting that
   strategy for this product. Approval MUST be recorded — e.g. by
   moving the item from *Proposed* to *Accepted* in
   `docs/template-evolution.md`, or via explicit written approval from
   the user in the conversation/PR.
3. Design, implementation, and documentation are updated together as
   a single approved change set (billing/paywall design, the
   `apps/billing` implementation and paywall middleware, and this
   document / relevant skill files) — not implemented ad hoc or split
   across unrelated commits.

### What Claude Code MUST Do

- Claude Code (including the Builder role) MUST NOT change
  billing/paywall logic (`apps/billing`, `Profile.free_until`, the
  paywall middleware, or the rules in Sections 4-8) based solely on
  its own judgment or on an unapproved `docs/product-context.md`
  entry.
- If `docs/product-context.md` names a Billing Strategy different
  from the default and no recorded template-owner approval exists,
  Claude Code MUST stop and ask the user for explicit approval before
  implementing anything.
- Once approval is recorded, follow the normal Explore → Plan →
  Implement workflow (Section 10-bis) to design and implement the
  approved strategy, and update this document (or a linked ADR) to
  reflect the new default for that product.

In short: billing/paywall rules are **not permanently frozen** — they
**cannot be changed without explicit, recorded template-owner
approval.**

---

## 5. Paywall Rules (CRITICAL)

_Default model, governed by Section 4-bis. Do not change without
recorded template-owner approval._

### Paid Feature Boundary
- ALL paid features MUST live under `/app/`
- No exceptions

### Access Rules for `/app/` (Default)
Access is allowed ONLY if:
- Current time ≤ `Profile.free_until`
- OR subscription status == `active`

Otherwise:
- Redirect to `/billing/pricing`

---

## 6. Stripe & Billing Rules (STRICT)

_These rules are strategy-agnostic: they apply regardless of which
Billing Strategy is active under Section 4-bis._

- Stripe Checkout MUST be used for subscription creation
- Stripe Customer Portal MUST be used for cancellation and payment updates
- Stripe Webhook is the **SINGLE SOURCE OF TRUTH**
- Subscription state MUST NEVER be derived from frontend redirects or query params

### Webhook Handling
- Webhook signatures MUST be verified using `STRIPE_WEBHOOK_SECRET`
- Duplicate and delayed events MUST be handled safely
- Minimum required events:
  - `customer.subscription.created`
  - `customer.subscription.updated`
  - `customer.subscription.deleted`

Only `status == active` grants paid access.

---

## 7. Application Structure (FIXED)

The project MUST follow this structure:

- `apps/accounts`
  - Authentication
  - Profile (`free_until`)
- `apps/billing`
  - Stripe Checkout
  - Stripe Webhook
  - Customer Portal
  - BillingProfile
- `apps/app`
  - Service-specific functionality (ONLY place for new features)
- `apps/common`
  - Middleware
  - Shared utilities
  - Base templates

When creating new services:
- Modify ONLY `apps/app`
- Core systems MUST remain unchanged

---

## 8. Paywall Middleware Rules

- Implemented as Django Middleware
- Applied ONLY to `/app/` paths

### Whitelisted Paths (Always Allowed)
- `/` (exact match only)
- `/accounts/`
- `/billing/`
- `/stripe/webhook`
- `/static/`
- `/admin/` (optional)

### Behavior
- Not logged in → redirect to login with `next`
- Logged in:
  - Free period valid → allow
  - Subscription `active` → allow
  - Otherwise → redirect to `/billing/pricing`

---

## 9. Forbidden Actions

### Always Forbidden (ABSOLUTE — no approval overrides these)

- Introducing React, Next.js, Vue, or any frontend framework
- Splitting frontend and backend into separate applications
- Activating subscriptions outside Stripe Webhook
- Adding paid features outside `/app/`
- Changing folder structure without instruction
- Adding advanced CI/CD pipelines or heavy automation
- Over-engineering abstractions or future-proofing

### Forbidden Without Recorded Template-Owner Approval (see Section 4-bis)

- Using Stripe trial features instead of application-managed free
  access
- Creating multiple pricing plans or tiers
- Changing the billing model away from Trial-based Subscription
  (e.g. to Freemium, Usage-based, Feature-based)

If uncertain:
> **DELETE code rather than add complexity.**

---

## 10. Development Workflow (ENFORCED)

### Implementation
- Claude Code is used for **implementation only**
- Work must be split into **small, purpose-specific commits**
- **1 commit = 1 purpose**

### Review
- Codex is used for **review and verification**
- Codex must NOT be used for bulk re-implementation

### Quality Gates
- `python -m compileall -q .`
- `python manage.py check`
- `pytest -q` (when applicable)

Hooks may enforce parts of this automatically.

## 10-bis. Explore → Plan → Implement Workflow (MANDATORY for non-trivial changes)

For any **non-trivial change** (multi-file edits, new features, unfamiliar code),
Claude MUST follow this 4-phase workflow:

1. **Explore (Plan mode, READ-ONLY)**
   - Enter `/plan` mode.
   - Read relevant files and answer questions.
   - DO NOT edit files or run commands.
   - Goal: understand existing behavior and constraints.

2. **Plan (still Plan mode)**
   - Produce a short, concrete implementation plan that MUST include:
     - Files to modify / create (with paths)
     - Step-by-step tasks in execution order
     - Tests & commands to run (e.g.
       - `pytest apps/billing/tests.py -q`
       - `pytest apps/common/tests.py -q`
       - `./scripts/checks/quick_check.sh`
     )
     - Possible edge cases / risks
   - Ask the user for confirmation if the plan is ambiguous.

3. **Implement (normal mode)**
   - Switch back from `/plan` to normal mode.
   - Implement strictly according to the approved plan.
   - After each logical step, run the planned tests/commands.
   - Fix all failures before proceeding.

4. **Commit**
   - Summarize the actual changes vs. the original plan.
   - Propose a descriptive commit message (1 purpose = 1 commit).
   - Optionally propose PR description based on the plan and test results.

Exceptions (Plan may be skipped):
- Purely mechanical edits:
  - typos
  - renaming a variable
  - adding a single log line
- In these cases, Claude may implement directly, but MUST still:
  - run the relevant tests
  - run `./scripts/checks/quick_check.sh` for billing/paywall changes

---

## 11. Documentation & Guidelines

The following documents must be respected:

- `docs/Guidelines.md` (day-to-day development rules)
- `.github/pull_request_template.md` (review checklist)
- `.editorconfig` (formatting consistency)

They complement this document but do not override it.

---

## 12. Language & Output Rules

- Code: English
- Comments and explanations: Japanese allowed
- Rules and constraints: Defined in this document and skill files (English)

All rules apply regardless of output language.

---

## 13. Mandatory Self-Check

Before completing any task, you MUST verify:

- This document is fully respected
- All applied skills are respected
- No forbidden actions were taken
- No unnecessary features were added
- The template remains safe to copy and reuse

---

- Development environment assumes Python 3.11+
- Do not upgrade Python without running full test suite

- This repository is a TEMPLATE. Modify only apps/app for new services.
- Do not change billing or paywall logic unless absolutely necessary.
- If unsure, prefer deletion over addition.


## Product Development Roles

This SaaS template uses five product development roles:

1. Product Strategist

   - Decide what should be built.

   - Define MVP scope.

   - Clarify what not to build.

   - Product Decision ONLY. Product Strategist MUST NOT implement
     code, change UI, refactor, or execute growth experiments — those
     belong to Builder, Sweeper, and Grower respectively.

   - Follows the 5-phase gated workflow defined in
     `.claude/agents/product-strategist.md`:
     Discover → Product Definition → Human Approval → Readiness
     Assessment → Decision Log.
     Product Strategist stops at every phase gate and never declares
     Builder readiness before explicit user approval.

   - docs/product-decisions.md is the Single Source of Truth (SSOT)
     for product decisions; Builder should treat it, alongside
     docs/product-definition.md, as authoritative context before
     starting its own Explore phase.

2. Prototyper

   - Build the fastest working version.

3. Builder

   - Convert prototype into production-quality implementation.

   - Implementation ONLY. Builder MUST NOT make product decisions.

   - Follows the 5-phase gated workflow defined in
     `.claude/agents/builder.md`:
     Explore → Plan → Human Approval → Implement → Verify.
     Builder stops at every phase gate and never implements
     before explicit user approval.

4. Sweeper

   - Simplify UI and code.

   - Remove unnecessary features.

   - Reduce complexity.

   - Simplification ONLY. Sweeper MUST NOT add features or make
     product decisions. "Delete over Add" is its guiding principle:
     reduce complexity, not merely line count.

   - Follows the 5-phase gated workflow defined in
     `.claude/agents/sweeper.md`:
     Analyze → Sweep Plan → Human Approval → Sweep → Verify.
     Sweeper stops at every phase gate and never modifies code
     before explicit user approval.

5. Grower

   - Improve activation, retention, pricing, conversion, and PMF.

   - Growth diagnosis and experiment design ONLY. Grower MUST NOT
     decide MVP scope, make new product decisions, implement code,
     delete code, or overhaul UI. Growth experiments and any handoff
     to Builder proceed only after explicit human approval.

   - Follows the 5-phase gated workflow defined in
     `.claude/agents/grower.md`:
     Analyze → Growth Plan → Human Approval → Experiment /
     Implementation Handoff → Verify / Learn.
     Grower stops at every phase gate and never starts an experiment,
     or hands work to Builder, before explicit user approval. Code
     changes coming out of an approved growth hypothesis are
     implemented by Builder, not Grower.

## Standard Workflow

Before implementing a new feature:

1. Use product-strategist
   (approve its output in docs/product-definition.md before Builder
   readiness is assessed).

2. Update docs/mvp-scope.md if needed.

3. Use prototyper for the smallest working version.

4. Use builder to harden the implementation
   (approve its plan in docs/implementation-plan.md before it implements).

5. Use sweeper before merging
   (approve its plan in docs/sweep-plan.md before it modifies code).

6. Use grower before deciding the next feature
   (approve its plan in docs/growth-plan.md before any experiment
   starts or work is handed to Builder).

Do not build features only because they are easy.

Always identify what should not be built.


## Testing Rules

After UI changes:

1. Run Playwright tests

npx playwright test

2. Check:

- console errors

- failed network requests

- visual layout problems

3. Do not mark task complete until Playwright passes



Never say "implementation completed"

before Playwright E2E tests pass.