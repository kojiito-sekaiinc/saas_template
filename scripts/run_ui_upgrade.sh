#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# run_ui_upgrade.sh
#
# Semi‑automatic UI upgrade workflow for Sekai UI System
#
# Steps:
# 1. Detect UI changes
# 2. Find affected templates
# 3. Run impact analysis prompt
# 4. Run minimal fix prompt
# 5. Run final review prompt
#
# NOTE:
# This script prepares context and prompts for AI.
# It does NOT modify code automatically.
# ============================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROMPTS_DIR="$PROJECT_ROOT/prompts"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"
TEMPLATES_DIR="$PROJECT_ROOT/templates"
UI_DIR="$PROJECT_ROOT/ui"
REPORT_DIR="$PROJECT_ROOT/ui-upgrade-report"

mkdir -p "$REPORT_DIR"

echo "========================================"
echo "Sekai UI Upgrade Assistant"
echo "========================================"
echo ""

# ------------------------------------------------------------
# Step 1: Detect UI changes
# ------------------------------------------------------------

echo "1️⃣ Detecting UI changes..."

git diff --name-only HEAD | grep "^ui/" > "$REPORT_DIR/ui_changes.txt" || true

if [[ ! -s "$REPORT_DIR/ui_changes.txt" ]]; then
    echo "No UI changes detected."
else
    echo "Changed UI files:"
    cat "$REPORT_DIR/ui_changes.txt"
fi

echo ""

# ------------------------------------------------------------
# Step 2: Find affected templates
# ------------------------------------------------------------

echo "2️⃣ Searching for templates using UI components..."

"$SCRIPTS_DIR/find_ui_usage.sh" > "$REPORT_DIR/template_usage.txt"

echo "Template usage report saved:"
echo "$REPORT_DIR/template_usage.txt"

echo ""

# ------------------------------------------------------------
# Step 3: Impact analysis
# ------------------------------------------------------------

echo "3️⃣ Impact analysis prompt"
echo "----------------------------------------"
echo ""
cat "$PROMPTS_DIR/ui-impact-analysis.md"
echo ""
echo "----------------------------------------"
echo ""
echo "👉 Copy the above prompt and run it in Claude/GPT."
echo ""

# ------------------------------------------------------------
# Step 4: Minimal fix prompt
# ------------------------------------------------------------

echo "4️⃣ Minimal fix prompt"
echo "----------------------------------------"
echo ""
cat "$PROMPTS_DIR/ui-minimal-fix.md"
echo ""
echo "----------------------------------------"
echo ""
echo "👉 Apply only minimal fixes suggested by AI."
echo ""

# ------------------------------------------------------------
# Step 5: Final review prompt
# ------------------------------------------------------------

echo "5️⃣ Final review prompt"
echo "----------------------------------------"
echo ""
cat "$PROMPTS_DIR/ui-final-review.md"
echo ""
echo "----------------------------------------"
echo ""
echo "👉 Run final safety review using AI."
echo ""

# ------------------------------------------------------------
# Step 6: Manual verification reminder
# ------------------------------------------------------------

echo "6️⃣ Manual checks required:"
echo ""
echo "• Open affected pages"
echo "• Verify sidebar, header, tables"
echo "• Check pagination"
echo "• Confirm no TemplateSyntaxError"
echo ""

echo "========================================"
echo "UI upgrade workflow completed."
echo "Reports saved in: $REPORT_DIR"
echo "========================================"
