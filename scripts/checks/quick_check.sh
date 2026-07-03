#!/usr/bin/env bash
set -euo pipefail

# プロジェクトルートに移動（scripts/checks/ からの相対パス）
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# 依存チェック: venv 未有効化や依存不足で意味不明なエラーになるのを防ぐ
if ! python -c "import django, pytest, axes" 2>/dev/null; then
    echo "ERROR: 必要な依存が見つかりません (django / pytest / django-axes)。" >&2
    echo >&2
    echo "  以下を確認してください:" >&2
    echo "    1. 仮想環境を有効化しているか:  source .venv/bin/activate" >&2
    echo "    2. 開発用依存を入れているか:    pip install -r requirements-dev.txt" >&2
    exit 1
fi

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