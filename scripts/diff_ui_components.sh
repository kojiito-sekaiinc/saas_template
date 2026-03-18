#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# diff_ui_components.sh
#
# Detects which parts of the Sekai UI System changed between
# the current working tree and a comparison target (default: HEAD).
#
# Purpose:
#   Help determine which templates might be affected by UI changes.
#
# Usage:
#   ./scripts/diff_ui_components.sh
#   ./scripts/diff_ui_components.sh HEAD~1
#   ./scripts/diff_ui_components.sh main
#
# Output:
#   - lists changed UI files
#   - categorizes changes (components / layouts / tokens)
# ============================================================

COMPARE_TARGET="${1:-HEAD}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UI_DIR="$PROJECT_ROOT/ui"
REPORT_DIR="$PROJECT_ROOT/ui-upgrade-report"

mkdir -p "$REPORT_DIR"

echo "========================================"
echo "Sekai UI Component Diff"
echo "========================================"
echo ""

echo "Comparing against: $COMPARE_TARGET"
echo ""

# ------------------------------------------------------------
# Detect changed files
# ------------------------------------------------------------

git diff --name-only "$COMPARE_TARGET" | grep "^ui/" > "$REPORT_DIR/ui_changed_files.txt" || true

if [[ ! -s "$REPORT_DIR/ui_changed_files.txt" ]]; then
    echo "No UI changes detected."
    exit 0
fi

echo "Changed UI files:"
cat "$REPORT_DIR/ui_changed_files.txt"
echo ""

# ------------------------------------------------------------
# Categorize changes
# ------------------------------------------------------------

echo "Categorizing changes..."
echo ""

grep "^ui/components/" "$REPORT_DIR/ui_changed_files.txt" > "$REPORT_DIR/components_changed.txt" || true
grep "^ui/layouts/" "$REPORT_DIR/ui_changed_files.txt" > "$REPORT_DIR/layouts_changed.txt" || true
grep "^ui/design/" "$REPORT_DIR/ui_changed_files.txt" > "$REPORT_DIR/design_changed.txt" || true

echo "Components changed:"
if [[ -s "$REPORT_DIR/components_changed.txt" ]]; then
    cat "$REPORT_DIR/components_changed.txt"
else
    echo "None"
fi
echo ""

echo "Layouts changed:"
if [[ -s "$REPORT_DIR/layouts_changed.txt" ]]; then
    cat "$REPORT_DIR/layouts_changed.txt"
else
    echo "None"
fi
echo ""

echo "Design tokens changed:"
if [[ -s "$REPORT_DIR/design_changed.txt" ]]; then
    cat "$REPORT_DIR/design_changed.txt"
else
    echo "None"
fi
echo ""

# ------------------------------------------------------------
# Extract component names
# ------------------------------------------------------------

echo "Affected components:"
if [[ -s "$REPORT_DIR/components_changed.txt" ]]; then
    sed 's|ui/components/||' "$REPORT_DIR/components_changed.txt" | sed 's|\.html||' > "$REPORT_DIR/component_names.txt"
    cat "$REPORT_DIR/component_names.txt"
else
    echo "None"
fi
echo ""

# ------------------------------------------------------------
# Extract layout names
# ------------------------------------------------------------

echo "Affected layouts:"
if [[ -s "$REPORT_DIR/layouts_changed.txt" ]]; then
    sed 's|ui/layouts/||' "$REPORT_DIR/layouts_changed.txt" | sed 's|\.html||' > "$REPORT_DIR/layout_names.txt"
    cat "$REPORT_DIR/layout_names.txt"
else
    echo "None"
fi
echo ""

echo "========================================"
echo "Report saved to:"
echo "$REPORT_DIR"
echo "========================================"
