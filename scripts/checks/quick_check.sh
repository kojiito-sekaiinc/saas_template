#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

echo "== quick_check =="

if [[ ! -f "manage.py" ]]; then
  echo "ERROR: manage.py not found. Run from repo root." >&2
  exit 1
fi

echo "[1/4] Python compile check"
python -m compileall -q .

echo "[2/4] Django system check"
python manage.py check

echo "[3/4] Django migrations check (no changes)"
# This will exit non-zero if migrations are missing.
python manage.py makemigrations --check --dry-run

echo "[4/4] Pytest (if tests exist)"
if ls -1q tests 2>/dev/null | grep -q . || find . -maxdepth 3 -type f -name "test_*.py" | grep -q .; then
  pytest -q
else
  echo "No tests detected; skipping pytest."
fi

echo "✅ quick_check passed."