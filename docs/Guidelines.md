# Development Guidelines for This SaaS Template

This document defines the **day-to-day development guidelines**
for this repository.

These guidelines exist to:
- Prevent template corruption
- Maintain fast iteration (≈2-week cycles)
- Ensure safe billing and paywall behavior
- Enable long-term reuse of this repository

This document complements (but does not override):
- `CLAUDE.md` (highest priority rules)
- Skill definitions under `.claude/skills/*/SKILL.md`

---

## 1. Template-First Principle (MOST IMPORTANT)

This repository is a **SaaS TEMPLATE**, not a single product.

### Golden Rule
> **When creating a new service, modify ONLY `apps/app/`.**

All other directories are considered **core template infrastructure**.

---

## 2. Allowed Change Areas

### 🟢 High-Change Area (Expected to change per service)
- `apps/app/`
- UI copy / text
- Templates under `templates/app/`

### 🟡 Low-Change Area (Change only with justification)
- `apps/accounts/`
- Authentication-related templates

### 🔴 Locked Areas (Do NOT change without strong reason)
- `apps/billing/`
- `apps/common/middleware.py`
- Paywall logic
- Stripe webhook handling
- Subscription state handling

If you must change a locked area, you MUST document:
- Why the change is necessary
- Why it benefits the template (not just one service)
- What alternatives were considered

---

## 3. Routing & Feature Placement Rules

- All **paid features** MUST live under `/app/`
- `/` is reserved for the free home page
- Billing entry point is ALWAYS `/billing/pricing`
- No business logic or features outside `/app/`

This rule is enforced to prevent paywall bypasses.

---

## 4. Billing & Subscription Rules

### Source of Truth
- **Stripe Webhook is the ONLY source of truth**
- Frontend redirects (`success`, `cancel`) are informational only

### Prohibited Patterns
- Activating subscriptions on frontend
- Trusting query parameters for billing state
- Multiple pricing tiers
- Stripe trial usage

### Subscription Interpretation
- Only `status = active` grants paid access
- All other states deny paid access

---

## 5. Commit & Work Style (2-Week Cycle Optimized)

### Commit Rules
- **1 commit = 1 purpose**
- Keep commits small and reversible

### Commit Message Examples
- `feat(accounts): add email-based signup`
- `feat(billing): create checkout session`
- `chore: configure whitenoise`

Avoid mixing unrelated changes in one commit.

---

## 6. Local Quality Gates (Minimum)

After meaningful changes, ensure:
- `python -m compileall -q .`
- `python manage.py check`

Before declaring the template “ready”:
- `pytest -q` (minimal tests)

These checks are partially automated via Claude Code hooks.

---

## 7. Security Baseline

You MUST:
- Never commit `.env`
- Never hardcode secrets (Stripe keys, webhook secrets)
- Use environment variables for all sensitive values
- Assume `DEBUG = false` in production
- Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` explicitly

---

## 8. settings.py Rules

- All environment-dependent values MUST come from env vars
- Avoid hard-coded service-specific values
- `.env.example` is the canonical reference
- Keep settings explicit and readable

---

## 9. Dependency Management

- Dependencies are managed via `requirements.txt`
- When adding a dependency:
  - Ensure it is strictly necessary
  - Prefer well-known, stable libraries
  - Add a brief note to `README.md` explaining why it exists

Avoid speculative or “nice-to-have” dependencies.

---

## 10. AI Usage Rules (Claude Code / Codex)

### Claude Code
- Used for **implementation**
- Must follow `CLAUDE.md` and skill definitions
- Must not introduce features beyond instructions
- Must not refactor locked areas casually

### Codex
- Used for **review and verification**
- Must not be used for bulk re-implementation
- Focus on:
  - Paywall safety
  - Billing correctness
  - Template integrity

Do NOT mix roles.

---

## 11. Decision Heuristics

When uncertain about a change, ask:

1. Does this make the template harder to reuse?
2. Would a future copy want to delete this?
3. Is this specific to one service?

If any answer is “yes”:
> **Do not implement the change.**

Prefer deletion over addition.

---

## 12. Final Checklist Before Shipping

Before considering the template (or a service built from it) ready:

- [ ] Free users can access `/app/` during free period
- [ ] Expired free users are redirected to `/billing/pricing`
- [ ] Stripe Checkout starts a subscription correctly
- [ ] Stripe Webhook updates subscription state
- [ ] Only `active` users access paid features
- [ ] No secrets are committed
- [ ] Core template logic remains unchanged

---

## 13. Guideline Enforcement Philosophy

These guidelines exist to:
- Reduce cognitive load
- Prevent expensive mistakes
- Enable fast, confident iteration


## Validation Rules (Mandatory)

- Any change to billing logic MUST pass:
  - pytest apps/billing/tests.py -q
  - ./scripts/checks/quick_check.sh

- Billing state MUST be derived ONLY from Stripe Webhook events.
- Never infer subscription state from frontend redirects.

- Billing や paywall に変更を加えた場合は、必ず以下を実行すること:
  - pytest apps/billing/tests.py -q
  - pytest apps/common/tests.py -q
  - ./scripts/checks/quick_check.sh

When in doubt:
> **Choose safety and simplicity over speed.**

---

## 14. Testing Conventions

### テストランナー

- **pytest 統一**。`django.test.TestCase` は使用しない。
- `python manage.py test` も使用しない。
- 実行コマンド: `pytest` / `pytest apps/billing/` / `pytest -v`

### テストスタイル

```python
# ✅ 正しいスタイル
import pytest

@pytest.mark.django_db
def test_something(client):
    assert True

# ❌ 使用しない
from django.test import TestCase

class SomeTest(TestCase):
    def test_something(self):
        self.assertTrue(True)
```

### DB アクセス

- DB を使うテストには `@pytest.mark.django_db` を付ける。
- フィクスチャで DB が必要な場合は `db` または `django_db_setup` を引数に取る。

### フィクスチャの配置ルール

| 配置場所 | 用途 |
|---|---|
| `conftest.py`（プロジェクトルート） | 複数モジュールで共用するフィクスチャ（`make_user` 等） |
| 各テストモジュール先頭 | そのモジュール固有のフィクスチャ |

### ファクトリパターン

- 単純なオブジェクト生成は `User.objects.create_user()` 等を直接呼ぶ。
- 引数違いで複数生成する場合は `make_user` ファクトリフィクスチャ（`conftest.py` 参照）を使う。
- `factory_boy` 等の外部ファクトリライブラリは現時点では導入しない。

### 設定のオーバーライド

```python
# 関数単位
@override_settings(DEBUG=True)
def test_debug_mode(client):
    ...

# フィクスチャ単位（複数テストに共通する場合）
@pytest.fixture(autouse=True)
def lockout_settings(settings):
    settings.AXES_FAILURE_LIMIT = 3
```

### モック

- Stripe 等の外部 API は `unittest.mock.patch()` でモックする。
- `settings` の一時変更には `monkeypatch.setattr(settings, "KEY", value)` も可。