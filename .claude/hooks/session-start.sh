#!/bin/bash
# Prepare a web session:
#   1. Install the pinned oscal-cli (ADR-0007), which verify.sh and scribe need,
#      and put ~/.local/bin on PATH for the session.
#   2. Install mattpocock/skills into the user-level Claude Code skills folder
#      (~/.claude/skills) without touching the repository's working tree.
# A failed oscal-cli install does not stop the skills install, but the hook
# still exits non-zero so the failure is seen.
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

status=0
project_dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"

if ! bash "$project_dir/scripts/install_oscal_cli.sh"; then
  echo "session-start: oscal-cli install failed; verify.sh will fail until it is installed" >&2
  status=1
fi
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$CLAUDE_ENV_FILE"
fi

npx -y skills@latest add mattpocock/skills --global --yes --agent claude-code --skill '*' || status=1

exit "$status"
