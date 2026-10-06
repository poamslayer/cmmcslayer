#!/usr/bin/env python3
"""Report whether the CMMC regulatory status brief is current."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Sequence


MISSING_MESSAGE = (
    "status brief: not installed "
    "(skills/domain/engagement/cmmc-regulatory-status-brief/SKILL.md not found)"
)
AS_OF_PATTERN = re.compile(
    r"^as_of:\s*(?P<quote>[\"']?)(?P<date>\d{4}-\d{2}-\d{2})(?P=quote)\s*$"
)


def iso_date(value: str) -> date:
    """Parse an ISO date for argparse."""
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"invalid date: {value}") from error


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check the age of the CMMC regulatory status brief."
    )
    parser.add_argument("--brief", type=Path, help="Alternate status brief path.")
    parser.add_argument(
        "--today",
        type=iso_date,
        default=date.today(),
        help="Date to compare in YYYY-MM-DD form. Defaults to today.",
    )
    return parser.parse_args(argv)


def default_brief_path() -> Path:
    """Return the repository-relative regulatory status brief path."""
    return (
        Path(__file__).resolve().parents[3]
        / "skills"
        / "domain"
        / "engagement"
        / "cmmc-regulatory-status-brief"
        / "SKILL.md"
    )


def frontmatter_as_of(text: str) -> date:
    """Extract the as_of date from the first YAML frontmatter block."""
    lines = text.splitlines()
    delimiters = [index for index, line in enumerate(lines) if line.strip() == "---"]
    if len(delimiters) < 2:
        raise ValueError("status brief has no complete YAML frontmatter block")

    start, end = delimiters[:2]
    for line in lines[start + 1 : end]:
        match = AS_OF_PATTERN.fullmatch(line.strip())
        if match:
            try:
                return date.fromisoformat(match.group("date"))
            except ValueError as error:
                raise ValueError("status brief has an invalid as_of date") from error
    raise ValueError("status brief frontmatter has no as_of date")


def check_status(brief_path: Path, today: date) -> int:
    """Print the brief age and return its status code."""
    if not brief_path.is_file():
        print(MISSING_MESSAGE)
        return 0

    try:
        as_of = frontmatter_as_of(brief_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    age = (today - as_of).days
    if age > 60:
        print(
            "WARNING: cmmc-regulatory-status-brief is "
            f"{age} days old (as_of {as_of.isoformat()}). "
            "Re-check the regulatory posture before advising a client."
        )
        return 2

    print(f"status brief as_of {as_of.isoformat()} ({age} days old): current")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the status check command."""
    args = parse_args(argv)
    brief_path = (
        args.brief.expanduser().resolve() if args.brief is not None else default_brief_path()
    )
    return check_status(brief_path, args.today)


if __name__ == "__main__":
    raise SystemExit(main())
