# Workflows

This document defines the two mandatory workflows for this repository:
1) Commit-Based Incremental Build
2) Spec → Code → Review

These workflows exist to prevent template breakage and enable fast iteration.

---

## Workflow 1: Commit-Based Incremental Build

### Goal
Build features in small, reversible increments with clear intent.

### Rules (Non-negotiable)
- 1 commit = 1 purpose
- No “mixed” commits (unrelated changes)
- Each commit must keep the repo runnable (or at minimum compilable)
- Prefer small diffs. If a diff is large, split it.
- Avoid modifying locked areas (apps/billing, apps/common) unless explicitly required

### Standard Cycle
1. Pick one task (e.g., “add signup page”)
2. Implement only what is needed for that task
3. Run local quality gates:
   - python -m compileall -q .
   - python manage.py check
4. Commit with a conventional message:
   - feat(accounts): ...
   - feat(billing): ...
   - chore: ...
5. Push

### If something breaks
- Immediately revert or fix in a new small commit
- Do not continue piling changes on top of broken state

---

## Workflow 2: Spec → Code → Review

### Goal
Keep implementation aligned with the spec and prevent silent drift.

### Roles
- Spec owner: claude.md + skills + docs/Guidelines.md
- Implementer: Claude Code
- Reviewer: Codex (and/or human)

### Standard Cycle
1. Spec
   - Confirm the task is consistent with claude.md and skills
   - Confirm the change is in the correct scope (usually apps/app only)

2. Code
   - Use Claude Code to implement in small commits
   - Do not add features beyond instructions
   - Respect locked areas (billing/paywall)

3. Review
   - Open PR (recommended) or do self-review using PR template
   - Run quick checks:
     - ./scripts/checks/quick_check.sh
   - Ask Codex to review using the standard Codex prompt
   - Apply fixes in small commits

### Done (Definition)
A change is “done” only when:
- It follows claude.md + skills + guidelines
- It passes the local quality gates
- Review confirms no billing/paywall/template integrity violations