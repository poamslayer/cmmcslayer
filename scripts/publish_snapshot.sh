#!/usr/bin/env bash
# Copy main, without docs/specs, into a folder for the public repository.
# Usage: bash scripts/publish_snapshot.sh <target-folder>
# The target must be a checkout of the public repository. Everything in it except
# .git is replaced, so the public side is never edited by hand.
set -euo pipefail
target="${1:?usage: publish_snapshot.sh <public-checkout>}"
[ -d "$target/.git" ] || { echo "not a git checkout: $target" >&2; exit 1; }
if git -C "$target" remote get-url origin | grep -q "cmmcslayer-private"; then
  echo "refusing: $target points at the private repository" >&2; exit 1
fi
find "$target" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
git archive main | tar -x -C "$target" --exclude 'docs/specs'
cd "$target"
python3 scripts/scrub_check.py --no-verbatim
python3 scripts/check_publish_safety.py
echo "snapshot written to $target; review, commit, and push from there"
