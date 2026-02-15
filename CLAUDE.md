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
- Frontend: Django Templates + HTMX + Tailwind CSS (static)
- Authentication: Email + Password (Django standard auth)
- Database: Supabase PostgreSQL (DB only, Django ORM)
- Payments: Stripe (subscription model)
- Deployment: Railway
- Dependency management: requirements.txt

No substitutions or architectural changes are allowed unless explicitly instructed.

---

## 4. Core Business Rules (FIXED)

### Subscription
- Subscription billing ONLY
- Monthly billing ONLY
- Single plan ONLY
- Price: **980 JPY / month**

### Free Access
- Free usage for **7 days after signup**
- No credit card required during free period
- Free period is managed by application logic (`Profile.free_until`)
- Stripe trial feature MUST NOT be used

---

## 5. Paywall Rules (CRITICAL)

### Paid Feature Boundary
- ALL paid features MUST live under `/app/`
- No exceptions

### Access Rules for `/app/`
Access is allowed ONLY if:
- Current time ≤ `Profile.free_until`
- OR subscription status == `active`

Otherwise:
- Redirect to `/billing/pricing`

---

## 6. Stripe & Billing Rules (STRICT)

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

## 9. Forbidden Actions (ABSOLUTE)

The following actions are strictly forbidden:

- Introducing React, Next.js, Vue, or any frontend framework
- Splitting frontend and backend into separate applications
- Using Supabase Auth or RLS
- Using Stripe trial features
- Creating multiple pricing plans or tiers
- Activating subscriptions outside Stripe Webhook
- Adding paid features outside `/app/`
- Changing folder structure without instruction
- Adding advanced CI/CD pipelines or heavy automation
- Over-engineering abstractions or future-proofing

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