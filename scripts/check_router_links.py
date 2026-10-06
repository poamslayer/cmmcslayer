#!/usr/bin/env python3
"""Check that every skill the router names actually exists.

`ask-poamslayer` is the map of this repo. A skill it routes to that was never
written, or one that was renamed underneath it, is a router that lies, which is
worse than no router at all. This script reads the skill names out of the
router's prose and compares them against the skill folders on disk.

Names that are not skills (triage labels, harness commands like `/clear`) are
listed in NOT_SKILLS and skipped.

    python3 scripts/check_router_links.py            # allow not-yet-written skills
    python3 scripts/check_router_links.py --strict   # fail on any missing skill

Use --strict once every skill is meant to exist. Exit status is 1 on a failure.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROUTER = Path("skills/flows/ask-poamslayer/SKILL.md")
SKILLS_ROOT = Path("skills")

# Backticked names in the router that are not skills.
NOT_SKILLS = {
    # harness commands
    "clear",
    "compact",
    # triage label strings
    "needs-triage",
    "needs-info",
    "ready-for-agent",
    "ready-for-human",
    "wontfix",
    # the two seats
    "consultant",
    # engagement repo paths and files
    "context",
    "data-flow",
    "asset-inventory",
    "network-diagram",
    "esp-responsibility-matrix",
    "continuous-monitoring-calendar",
}


def router_names(text: str) -> set[str]:
    """Return every backticked token in the router that looks like a skill name."""
    names = set()
    for match in re.finditer(r"`/?([a-z][a-z0-9-]*)`", text):
        name = match.group(1)
        if name in NOT_SKILLS or "-" not in name and len(name) < 5:
            continue
        names.add(name)
    return names


def installed_skills(root: Path) -> set[str]:
    """Return the name of every skill folder holding a SKILL.md."""
    return {path.parent.name for path in root.rglob("SKILL.md")}


def main() -> int:
    """Compare the router's named skills against the filesystem."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail when any named skill is missing, not just when one is unplanned",
    )
    parser.add_argument("--router", default=str(ROUTER))
    parser.add_argument("--skills-root", default=str(SKILLS_ROOT))
    args = parser.parse_args()

    router_path = Path(args.router)
    if not router_path.is_file():
        print(f"FAIL router not found at {router_path}")
        return 1

    named = router_names(router_path.read_text(encoding="utf-8"))
    present = installed_skills(Path(args.skills_root))

    # Names the repo plans to write, taken from the bucket READMEs.
    planned: set[str] = set()
    for readme in Path(args.skills_root).rglob("README.md"):
        # Bucket READMEs list every planned skill, in tables and in prose. Single
        # word names (audit, triage, wayfinder) count as much as hyphenated ones.
        planned |= set(
            re.findall(r"\b([a-z][a-z0-9-]{3,})\b", readme.read_text(encoding="utf-8"))
        )

    missing = sorted(named - present)
    unplanned = [name for name in missing if name not in planned]

    for name in unplanned:
        print(f"FAIL {name}: routed to, but not written and not planned in any README")
    if not args.strict:
        for name in missing:
            if name in planned:
                print(f"note {name}: planned, not yet written")

    print(
        f"router: {len(named)} skills named, {len(named) - len(missing)} written, "
        f"{len(missing)} outstanding, {len(unplanned)} unplanned"
    )
    if unplanned:
        return 1
    if args.strict and missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
