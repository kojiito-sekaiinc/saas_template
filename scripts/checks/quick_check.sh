#!/usr/bin/env bash
set -euo pipefail

# プロジェクトルートに移動（scripts/checks/ からの相対パス）
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "===================================="
echo " Running quick checks for this repo "
echo "===================================="
echo

# 1. Python バイトコードコンパイル（構文エラー検出）
echo "[1/3] python -m compileall -q ."
python -m compileall -q .
echo "      OK"
echo

# 2. Django システムチェック
echo "[2/3] python manage.py check"
python manage.py check
echo "      OK"
echo

# 3. pytest
echo "[3/3] pytest -q"
pytest -q
echo "      OK"
echo

echo "===================================="
echo " All quick checks passed successfully"
echo "===================================="