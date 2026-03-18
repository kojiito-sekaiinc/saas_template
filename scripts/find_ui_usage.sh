#!/usr/bin/env bash
set -euo pipefail

# find_ui_usage.sh
#
# Purpose:
#   Scan Django templates and report which templates may be affected by
#   Sekai UI System updates.
#
# What it detects:
#   - templates extending layouts/*
#   - templates including components/*
#   - templates using table components
#   - templates using pagination-like patterns
#
# Usage examples:
#   ./scripts/find_ui_usage.sh
#   ./scripts/find_ui_usage.sh table
#   ./scripts/find_ui_usage.sh component table
#   ./scripts/find_ui_usage.sh layout app_shell
#   ./scripts/find_ui_usage.sh token
#
# Assumptions:
#   - Run from the project root
#   - Django templates live under ./templates
#   - UI system files live under ./ui
#
# Exit behavior:
#   - Returns 0 even if no matches are found
#   - Prints readable sections to stdout

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES_DIR="${PROJECT_ROOT}/templates"
UI_DIR="${PROJECT_ROOT}/ui"

if [[ ! -d "${TEMPLATES_DIR}" ]]; then
  echo "ERROR: templates directory not found: ${TEMPLATES_DIR}" >&2
  exit 1
fi

print_header() {
  local title="$1"
  echo
  echo "============================================================"
  echo "${title}"
  echo "============================================================"
}

print_subheader() {
  local title="$1"
  echo
  echo "---- ${title} ----"
}

safe_grep() {
  # Grep wrapper that never fails the whole script on no match.
  grep -RInE "$1" "$2" 2>/dev/null || true
}

list_all_layout_usage() {
  print_header "Templates extending layouts/*"
  safe_grep '\{%\s*extends\s+"layouts/[^"]+"\s*%\}' "${TEMPLATES_DIR}"
}

list_all_component_usage() {
  print_header "Templates including components/*"
  safe_grep '\{%\s*include\s+"components/[^"]+"\s*.*%\}' "${TEMPLATES_DIR}"
}

list_table_usage() {
  print_header "Templates using components/table.html"
  safe_grep '\{%\s*include\s+"components/table\.html"\s*.*%\}' "${TEMPLATES_DIR}"
}

list_pagination_patterns() {
  print_header "Templates using pagination-like patterns"

  print_subheader "page_obj usage"
  safe_grep 'page_obj' "${TEMPLATES_DIR}"

  print_subheader "Paginator page range usage"
  safe_grep 'paginator\.page_range|page_range_items' "${TEMPLATES_DIR}"

  print_subheader "Inline page query construction"
  safe_grep 'href=.*\?page=|previous_page_number|next_page_number' "${TEMPLATES_DIR}"
}

list_token_related_usage() {
  print_header "Templates using Sekai token-based classes"

  print_subheader "text-token-* / px-token-* / rounded-token-*"
  safe_grep '(text-token-|px-token-|py-token-|pt-token-|pb-token-|pl-token-|pr-token-|mt-token-|mb-token-|ml-token-|mr-token-|gap-token-|rounded-token-)' "${TEMPLATES_DIR}"

  print_subheader "sekai color classes"
  safe_grep '(bg-sekai-|text-sekai-|border-sekai-|ring-sekai-)' "${TEMPLATES_DIR}"
}

find_component_usage() {
  local component_name="$1"
  print_header "Templates using component: components/${component_name}.html"
  safe_grep "\\{%\\s*include\\s+\"components/${component_name}\\.html\"\\s*.*%\\}" "${TEMPLATES_DIR}"
}

find_layout_usage() {
  local layout_name="$1"
  print_header "Templates extending layout: layouts/${layout_name}.html"
  safe_grep "\\{%\\s*extends\\s+\"layouts/${layout_name}\\.html\"\\s*%\\}" "${TEMPLATES_DIR}"
}

find_block_usage() {
  local block_name="$1"
  print_header "Templates referencing block: ${block_name}"

  print_subheader "block declarations"
  safe_grep "\\{%\\s*block\\s+${block_name}\\s*%\\}" "${TEMPLATES_DIR}"

  print_subheader "endblock comments or mentions"
  safe_grep "endblock\\s+${block_name}|${block_name}" "${TEMPLATES_DIR}"
}

show_ui_summary() {
  print_header "Sekai UI System summary"

  if [[ -d "${UI_DIR}" ]]; then
    echo "UI directory found: ${UI_DIR}"
  else
    echo "WARNING: ui directory not found: ${UI_DIR}"
    return 0
  fi

  print_subheader "Layouts"
  find "${UI_DIR}/layouts" -maxdepth 1 -type f 2>/dev/null | sort || true

  print_subheader "Components"
  find "${UI_DIR}/components" -maxdepth 1 -type f 2>/dev/null | sort || true

  print_subheader "Examples"
  find "${UI_DIR}/examples" -maxdepth 1 -type f 2>/dev/null | sort || true
}

show_help() {
  cat <<'EOF'
find_ui_usage.sh

Usage:
  ./scripts/find_ui_usage.sh
  ./scripts/find_ui_usage.sh summary
  ./scripts/find_ui_usage.sh table
  ./scripts/find_ui_usage.sh token
  ./scripts/find_ui_usage.sh component <name>
  ./scripts/find_ui_usage.sh layout <name>
  ./scripts/find_ui_usage.sh block <name>

Commands:
  (no args)         Run the full report
  summary           Show UI directory summary
  table             Show templates using the table component
  token             Show token/class usage in templates
  component <name>  Find templates using components/<name>.html
  layout <name>     Find templates extending layouts/<name>.html
  block <name>      Find templates referencing a block name

Examples:
  ./scripts/find_ui_usage.sh
  ./scripts/find_ui_usage.sh component table
  ./scripts/find_ui_usage.sh component button
  ./scripts/find_ui_usage.sh layout app_shell
  ./scripts/find_ui_usage.sh block page_content
EOF
}

run_full_report() {
  show_ui_summary
  list_all_layout_usage
  list_all_component_usage
  list_table_usage
  list_pagination_patterns
  list_token_related_usage
}

main() {
  local cmd="${1:-}"

  case "${cmd}" in
    "")
      run_full_report
      ;;
    help|-h|--help)
      show_help
      ;;
    summary)
      show_ui_summary
      ;;
    table)
      list_table_usage
      ;;
    token)
      list_token_related_usage
      ;;
    component)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: component name required" >&2
        echo "Example: ./scripts/find_ui_usage.sh component table" >&2
        exit 1
      fi
      find_component_usage "$2"
      ;;
    layout)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: layout name required" >&2
        echo "Example: ./scripts/find_ui_usage.sh layout app_shell" >&2
        exit 1
      fi
      find_layout_usage "$2"
      ;;
    block)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: block name required" >&2
        echo "Example: ./scripts/find_ui_usage.sh block page_content" >&2
        exit 1
      fi
      find_block_usage "$2"
      ;;
    *)
      echo "ERROR: unknown command: ${cmd}" >&2
      echo
      show_help
      exit 1
      ;;
  esac
}

main "$@"