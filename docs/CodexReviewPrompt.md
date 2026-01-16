# Codex Review Prompt (Template Safety)

> Usage:
> 1) Give Codex the PR diff (or repo link + changed files).
> 2) Paste the prompt below.

---

## PROMPT (copy & paste)

You are a strict code reviewer. Your job is to verify that this repository remains a safe, reusable SaaS template.

### Non-negotiable invariants
- Paid features must exist ONLY under `/app/`
- Billing truth must come ONLY from Stripe Webhooks (never from success pages or redirects)
- Free period is managed by app logic: `Profile.free_until = signup + 7 days` (Stripe trial is forbidden)
- Paid access is allowed ONLY when `BillingProfile.status == "active"`
- For new services, changes should be limited to `apps/app/` (billing/paywall/core should not be casually modified)
- Dependencies are managed via `requirements.txt` (no pyproject switch)

### Review priorities (in order)
1) Security: secrets or .env committed? API keys hard-coded?
2) Paywall integrity: any paid features outside `/app/`? routes outside `/app/` that behave like features?
3) Billing correctness: webhook signature verification exists? any subscription state update outside webhook?
4) Spec drift: trial usage, multiple plans, frontend frameworks, API-first architecture, over-engineering
5) Template integrity: product-specific logic added outside `apps/app/`?

### Output format (MUST)
- ✅ What looks correct
- ❌ Issues (severity: Critical / High / Medium / Low)
  - For each issue: evidence (file + line / snippet) and why it violates the invariants
- 🛠 Fix plan (minimum-change approach, file-by-file)
- ✅/❌ Final verdict: Is this safe to merge? (Yes/No)

If uncertain, state the risk clearly and propose the smallest verification step.

---

## Optional follow-up prompt (after the review)

For the issues you identified, propose the smallest possible patch plan:
- List files to change
- Describe exact code edits (pseudo-diff is fine)
- Ensure invariants are preserved