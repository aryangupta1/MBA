#!/usr/bin/env bash
# SessionStart hook — injects next-prompt.md into every new session's context.
#
# next-prompt.md is the handoff note the previous session left behind. It is
# binding for this session unless the user opens with "Adhoc chat, ignore next
# prompt". See docs/next-prompt-protocol.md.
#
# Contract: read hook JSON on stdin (ignored), write one JSON object on stdout
# with hookSpecificOutput.additionalContext. Never fail the session — if the
# file is missing or unreadable, emit nothing and exit 0.

set -uo pipefail

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
file="$root/next-prompt.md"

[ -r "$file" ] || exit 0

body=$(cat "$file") || exit 0
[ -n "${body//[[:space:]]/}" ] || exit 0

preamble='The project file next-prompt.md contains the standing instructions left by the previous session. Treat it as the starting agenda for this session and follow it, unless the user says "Adhoc chat, ignore next prompt" (or otherwise redirects). Before this session ends, update next-prompt.md per docs/next-prompt-protocol.md.

--- BEGIN next-prompt.md ---
'

jq -n --arg ctx "${preamble}${body}"$'\n--- END next-prompt.md ---' \
  '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
