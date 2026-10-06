#!/usr/bin/env python3
"""Set up a scratch copy of the fixture engagement for a cold run.

Every skill in this repo is tested by running it against `docs/fixture/`, and
the fixture must never be edited in place: its mistakes are deliberate and the
answer key describes them. This script makes the throwaway copy each run needs,
so that step is one command instead of a thing people improvise.

    python3 scripts/cold_run.py --skill audit

prints the scratch path it created and the files a tester is allowed to read.
Add --keep to reuse an existing directory rather than starting clean.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from datetime import date
from pathlib import Path

FIXTURE = Path("docs/fixture")
ENGAGEMENT = FIXTURE / "engagement"
COMPANY = FIXTURE / "company"
SKILLS = Path("skills")
SCRIBE = SKILLS / "flows" / "scribe"


def records_through_scribe(skill: str) -> bool:
    """True when the skill under test calls scribe, so the tester needs scribe to write or show the record."""
    if skill == "scribe":
        return False
    return any(
        "Skill tool with `scribe`" in path.read_text(encoding="utf-8")
        for path in SKILLS.glob(f"**/{skill}/SKILL.md")
    )


def scratch_root() -> Path:
    """Return the directory cold-run copies live in, outside the repo."""
    return Path("/tmp") / "poamslayer-cold-runs"


def prepare(skill: str, keep: bool) -> Path:
    """Copy the fixture engagement to a scratch directory and init a git repo."""
    target = scratch_root() / f"{date.today().isoformat()}-{skill}"
    if target.exists() and not keep:
        shutil.rmtree(target)
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(ENGAGEMENT, target)
        subprocess.run(["git", "init", "-q"], cwd=target, check=True)
        subprocess.run(["git", "add", "-A"], cwd=target, check=True)
        subprocess.run(
            ["git", "-c", "user.email=cold-run@example", "-c", "user.name=cold run",
             "commit", "-q", "-m", "fixture engagement, starting state"],
            cwd=target,
            check=True,
        )
    return target


def main() -> int:
    """Create the scratch copy and print what the tester may read."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", required=True, help="the skill under test")
    parser.add_argument(
        "--keep",
        action="store_true",
        help="reuse the directory if it already exists instead of starting clean",
    )
    args = parser.parse_args()

    if not ENGAGEMENT.is_dir():
        print(f"fixture engagement not found at {ENGAGEMENT}; run from the repo root")
        return 1

    target = prepare(args.skill, args.keep)
    needs_scribe = records_through_scribe(args.skill)

    print(f"scratch engagement: {target}")
    print()
    print("The tester may read, and nothing else:")
    print(f"  the skill under test and any file inside its own folder")
    print(f"  {target}  (the engagement, writable)")
    print(f"  {COMPANY}  (the company, read only)")
    if needs_scribe:
        print(f"  {SCRIBE}  (scribe's SKILL.md and edit command: the skill records or reads the SSP through it)")
    print()
    print("The tester must NOT read:")
    print(f"  {FIXTURE / 'known-answers.md'}")
    print(f"  {FIXTURE / 'grader-rubric.md'}")
    print("  any other skill in this repo" + (", except scribe" if needs_scribe else ""))
    print()
    print("Afterwards, grade with a second agent given only the scratch directory,")
    print(f"  {FIXTURE / 'known-answers.md'} and {FIXTURE / 'grader-rubric.md'},")
    print("and record the result in docs/cold-runs/. The grader scores the record with:")
    print(f"  python3 scripts/check_record.py {target} --baseline {ENGAGEMENT}")
    print()
    print(f"Diff what the run changed:  git -C {target} diff HEAD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
