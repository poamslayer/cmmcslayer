#!/bin/bash
# Prepare a web session: install mattpocock/skills into the user-level Claude
# Code skills folder (~/.claude/skills) without touching the repository's
# working tree. verify.sh needs only Python, so nothing else is installed.
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

npx -y skills@latest add mattpocock/skills --global --yes --agent claude-code --skill '*'
