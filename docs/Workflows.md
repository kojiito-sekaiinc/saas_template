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
- Spec owner: CLAUDE.md + .claude/skills/*/SKILL.md + docs/Guidelines.md
- Implementer: Claude Code
- Reviewer: Codex (and/or human)

### Standard Cycle
1. Spec
   - Confirm the task is consistent with CLAUDE.md and skills
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
- It follows CLAUDE.md + skills + guidelines
- It passes the local quality gates
- Review confirms no billing/paywall/template integrity violations


---

## Workflow 3: Explore → Plan → Implement → Commit (Claude Code)

### Goal
Reduce wrong implementations by separating understanding, design, and coding.
This workflow is mandatory for non-trivial or high-risk changes.

---

### When this workflow is REQUIRED

Use this workflow when:
- The change touches multiple files
- The change affects `apps/billing` or `apps/common`
- The change introduces new behavior or business rules
- The codebase area is unfamiliar
- The correct approach is not obvious upfront

You MAY skip the Explore/Plan phases only for:
- Typos
- Simple renames
- Purely mechanical changes

---

### Phase 1: Explore (Plan Mode, Read-Only)

- Enter Claude **/plan** mode
- Read relevant files only
- Ask Claude to explain:
  - Current behavior
  - Existing constraints (CLAUDE.md, skills, locked areas)
  - Related flows (auth, billing, middleware, etc.)
- ❌ No file edits
- ❌ No command execution

Goal: shared understanding, not solutions.

---

### Phase 2: Plan (Still Plan Mode)

Claude must produce a concrete plan that includes:

1. Files to modify or create (with paths)
2. Step-by-step implementation order
3. Affected workflows (billing, paywall, auth, etc.)
4. Edge cases and risks
5. Verification steps, including required commands:
   - pytest apps/billing/tests.py -q (if applicable)
   - pytest apps/common/tests.py -q (if applicable)
   - ./scripts/checks/quick_check.sh

Implementation MUST NOT start until the plan is explicitly approved.

---

### Phase 3: Implement (Normal Mode)

- Exit `/plan` mode
- Implement strictly according to the approved plan
- Follow **Workflow 1 (Commit-Based Incremental Build)**
- After each logical step:
  - Run the planned tests
  - Fix failures before proceeding

No scope creep is allowed.

---

### Phase 4: Commit

- Ensure all verification steps are green
- Summarize:
  - What was planned
  - What was actually implemented
  - Any deviations and why
- Commit with:
  - 1 commit = 1 purpose
  - Clear, descriptive message

This phase must still comply with:
- Workflow 1 (Commit discipline)
- Workflow 2 (Spec → Code → Review)

## Relationship Between Workflows

Workflow 1 governs how changes are split and committed
Workflow 2 governs what is allowed and how correctness is judged
Workflow 3 governs how Claude reasons before writing code

They are complementary and MUST be used together.

## Final Note

These workflows are intentionally strict.
This repository is a reusable SaaS template, not a one-off project.

When in doubt:
Prefer understanding over speed
Prefer deletion over complexity
Prefer safety over cleverness