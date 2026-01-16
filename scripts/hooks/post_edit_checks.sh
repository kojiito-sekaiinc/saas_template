#!/usr/bin/env bash
set -euo pipefail

cd "${CLAUDE_PROJECT_DIR:-.}"

# Only run checks if this looks like a Python/Django repo.
if [[ ! -f "manage.py" ]]; then
  exit 0
fi

echo "🔎 post_edit_checks: python compileall"
python -m compileall -q .

# If Django isn't installed yet (fresh repo), don't fail hard.
if ! python -c "import django" >/dev/null 2>&1; then
  echo "⚠️ Django not installed yet; skipping 'manage.py check'"
  exit 0
fi

# Skip manage.py check if .env isn't ready to avoid noise (optional).
# We keep it permissive: run even without .env, but don't fail the whole hook
# on missing env vars. If you prefer strict mode, remove the '|| true'.
echo "🔎 post_edit_checks: django check"
python manage.py check || true

exit 0