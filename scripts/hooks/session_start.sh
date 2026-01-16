#!/usr/bin/env bash
set -euo pipefail

cd "${CLAUDE_PROJECT_DIR:-.}"

echo "✅ session_start: environment quick check"
echo "- project_dir: $(pwd)"
echo "- python: $(python -V 2>&1 || true)"
echo "- pip: $(pip -V 2>&1 || true)"

if [[ -f ".env" ]]; then
  echo "- .env: present"
else
  echo "- .env: NOT found (you can copy from .env.example when ready)"
fi

if [[ -f "requirements.txt" ]]; then
  echo "- requirements.txt: present"
else
  echo "- requirements.txt: NOT found (expected for this template)"
fi

# Check core imports (non-fatal)
python - <<'PY' || true
mods = ["django", "stripe", "psycopg", "whitenoise"]
for m in mods:
    try:
        __import__(m)
        print(f"- import {m}: OK")
    except Exception as e:
        print(f"- import {m}: NOT OK ({e.__class__.__name__})")
PY

exit 0