#!/usr/bin/env bash
set -euo pipefail

# Claude Code hook: validate bash commands before execution.
# Expects the tool payload on STDIN (JSON). We extract a "command" field if present.
# If we can't parse it, we fail open (allow) to avoid blocking legitimate work.

payload="$(cat || true)"

# Try to extract the command string.
cmd="$(
  printf "%s" "$payload" \
  | python3 -c '
import json,sys
try:
    data=json.load(sys.stdin)
    if isinstance(data, dict):
        if "command" in data and isinstance(data["command"], str):
            print(data["command"])
        elif "input" in data and isinstance(data["input"], dict) and isinstance(data["input"].get("command"), str):
            print(data["input"]["command"])
except Exception:
    pass
' 2>/dev/null || true
)"

# If command is empty/unparseable, allow.
if [[ -z "${cmd:-}" ]]; then
  exit 0
fi

# Normalize whitespace for matching.
cmd_one_line="$(echo "$cmd" | tr '\n' ' ' | sed -E 's/[[:space:]]+/ /g' | sed -E 's/^ //; s/ $//')"

# Blocklist patterns (conservative). Add/remove as your comfort level.
# NOTE: This blocks obviously destructive operations. You can tune later.
blocked_patterns=(
  # destructive deletes
  '(^|[[:space:]])rm[[:space:]]+-rf([[:space:]]+|$)'
  '(^|[[:space:]])rm[[:space:]]+-fr([[:space:]]+|$)'
  '(^|[[:space:]])rm[[:space:]]+-r[[:space:]]+-f([[:space:]]+|$)'
  # dangerous root/absolute deletes
  'rm[[:space:]].*/\*'
  'rm[[:space:]]+-rf[[:space:]]+/$'
  'rm[[:space:]]+-rf[[:space:]]+/\*'
  # disk wipe / partition
  '(^|[[:space:]])dd[[:space:]].*of=/dev/'
  '(^|[[:space:]])mkfs(\.|[[:space:]])'
  '(^|[[:space:]])wipefs[[:space:]]'
  # privilege escalation
  '(^|[[:space:]])sudo[[:space:]]+rm[[:space:]]'
  # git foot-guns
  '(^|[[:space:]])git[[:space:]]+push[[:space:]].*--force'
  '(^|[[:space:]])git[[:space:]]+push[[:space:]].*-f([[:space:]]+|$)'
  '(^|[[:space:]])git[[:space:]]+reset[[:space:]]+--hard'
  '(^|[[:space:]])git[[:space:]]+clean[[:space:]]+-fd'
  '(^|[[:space:]])git[[:space:]]+clean[[:space:]]+-xdf'
  # curl|sh / wget|sh (supply-chain risk)
  'curl[[:space:]].*\|[[:space:]]*sh'
  'wget[[:space:]].*\|[[:space:]]*sh'
)

for pat in "${blocked_patterns[@]}"; do
  if echo "$cmd_one_line" | grep -Eiq "$pat"; then
    echo "❌ BLOCKED by validate_bash.sh" >&2
    echo "Reason: command matched a dangerous pattern." >&2
    echo "Command: $cmd_one_line" >&2
    echo "" >&2
    echo "If you really intended this, run it manually yourself (outside Claude) or relax the hook pattern." >&2
    exit 2
  fi
done

# Allow
exit 0