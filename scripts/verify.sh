#!/usr/bin/env bash
# Run every check this repository enforces, in the order that fails cheapest first.
#
#   bash scripts/verify.sh           # allow skills the router names but nobody has written
#   bash scripts/verify.sh --strict  # every named skill must exist; the release gate
#
# Exit status is 1 if any check fails.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

strict=""
publish=""
for arg in "$@"; do
  case "$arg" in
    --strict) strict="--strict" ;;
    --publish) strict="--strict"; publish="yes" ;;
  esac
done

failed=0

run() {
  local name="$1"
  shift
  echo "== $name"
  if "$@"; then
    :
  else
    echo "   FAILED: $name"
    failed=1
  fi
  echo
}

run "skill frontmatter and harness metadata" python3 scripts/check_skills.py
run "control file schema and the requirements index" python3 scripts/check_control_files.py
run "router links" python3 scripts/check_router_links.py $strict
run "authorities register" python3 scripts/check_authorities.py
# scribe's check and renderer, run on scratch engagements under a temporary
# folder: a valid SSP passes and renders, and each rule fails once. A few seconds.
run "scribe check and render" python3 scripts/check_scribe.py

# The setup skill's scaffold, run in a scratch folder: it lays out the
# engagement and writes the Markdown SSP, which must pass scribe's check.
run "setup scaffold" python3 scripts/check_setup.py

# The fixture engagement's record: scribe's check on its SSP, its assets and
# statements as the answer key states them, a current view, and proof that
# the grader rubric's record check fails an invalid SSP.
run "fixture record" python3 scripts/check_fixture_record.py

# The scrub check is last because it is the slowest: it builds an n-gram set
# from the whole private wiki before it can compare anything.
run "scrub check" python3 scripts/scrub_check.py

echo "== em dashes in prose"
# Two exemptions, both recorded in AGENTS.md. reference/ reproduces outside
# material and keeps the source's own punctuation. docs/specs/ holds the spec
# and the vault inventory as they were written, and editing them would falsify
# the record of what this build was actually specified from.
# The pattern is built from its code point so this script does not contain the
# character it forbids, and so a careless search-and-replace cannot blunt it.
DASH=$(printf '\xe2\x80\x94')
if grep -rln "$DASH" --include='*.md' skills docs README.md CONTEXT.md AGENTS.md 2>/dev/null \
   | grep -v '^docs/specs/'; then
  echo "   FAILED: em dashes found in the files listed above"
  failed=1
else
  echo "none"
fi
echo

# The publish gate. docs/specs/ holds the original spec and the vault inventory,
# which are internal working documents: they name the private community, its
# members' handles, and real people, because they were written to plan the build
# rather than to ship. They are deliberately outside the scrub's default paths
# so day-to-day work is not drowned in hits about them, and that exclusion is
# exactly why publishing has to check them on purpose. See ADR-0001.
if [ -n "$publish" ]; then
  echo "== publish gate: private material in docs/specs"
  if [ ! -d docs/specs ]; then
    echo "docs/specs is not in this repository"
  elif python3 scripts/scrub_check.py docs/specs > /dev/null 2>&1; then
    echo "docs/specs is clean in the working tree"
  else
    echo "   FAILED: docs/specs still contains private names, handles, or"
    echo "   verbatim source text. Run:"
    echo "     python3 scripts/scrub_check.py docs/specs"
    failed=1
  fi
  echo

  # The working tree is only half the question. Deleting a file does not remove
  # it from a git repository, so a repo published after a tidy-up commit still
  # hands over everything it ever held.
  echo "== publish gate: private material reachable from history"
  if python3 scripts/check_publish_safety.py; then
    :
  else
    failed=1
  fi
  echo
fi

if [ "$failed" -eq 0 ]; then
  echo "verify: all checks passed"
else
  echo "verify: at least one check failed"
fi
exit "$failed"
