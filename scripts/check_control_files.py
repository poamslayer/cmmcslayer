#!/usr/bin/env python3
"""Validate the control files under control-evidence-lookup against their schema.

Every control file describes one NIST SP 800-171 Rev 2 requirement in the shape
that CONTROL-FILE-FORMAT.md fixes. The audit flow, over-engineering-guard, and
evidence-package-builder all read these files positionally, so a file with a
missing section or a wrong point value is a silent failure at assessment time.

Run it with no arguments to check every control file:

    python3 scripts/check_control_files.py

Exit status is 1 when any file fails.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CONTROLS_DIR = Path("skills/domain/gap/control-evidence-lookup/controls")
REQUIREMENTS = Path("reference/nist-800-171r2-requirements.json")

REQUIRED_KEYS = (
    "requirement",
    "family",
    "title",
    "points",
    "poam_eligible",
    "confidence",
    "as_of",
    "vault_sources",
    "public_sources",
)

REQUIRED_SECTIONS = (
    "Requirement",
    "Objectives",
    "Sufficient",
    "Insufficient",
    "Over-engineering",
    "Edge cases",
    "Evidence examples",
    "Related requirements",
)

VALID_CONFIDENCE = {"high", "medium", "low"}


def parse_frontmatter(text: str) -> dict[str, object]:
    """Read the leading YAML block well enough for this file's fixed shape.

    Only scalars and simple string lists appear in a control file, so a small
    reader avoids a dependency. Values keep their raw spelling apart from
    surrounding quotes.
    """
    if not text.startswith("---"):
        return {}
    _, block, _ = text.split("---", 2)
    data: dict[str, object] = {}
    current_list: list[str] | None = None
    key = ""
    for line in block.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list is not None:
            current_list.append(line[4:].strip().strip('"').strip("'"))
            continue
        match = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if value:
            data[key] = value.strip('"').strip("'")
            current_list = None
        else:
            current_list = []
            data[key] = current_list
    return data


def section_names(text: str) -> list[str]:
    """Return the level-two headings in the order they appear."""
    return re.findall(r"^## (.+?)\s*$", text, re.MULTILINE)


def objective_letters(text: str) -> list[str]:
    """Return the objective letters listed in the Objectives section."""
    match = re.search(r"^## Objectives\s*$(.*?)^## ", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    return re.findall(r"\[([a-z]+)\]", match.group(1))


def check_file(path: Path, expected: dict[str, dict]) -> list[str]:
    """Return a list of problems with one control file, empty when it passes."""
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    front = parse_frontmatter(text)

    for key in REQUIRED_KEYS:
        if key not in front:
            problems.append(f"missing frontmatter key: {key}")
    if problems:
        return problems

    requirement = str(front["requirement"])
    if requirement != path.stem:
        problems.append(f"requirement {requirement} does not match filename {path.stem}")
    if requirement not in expected:
        problems.append(f"requirement {requirement} is not in the requirements index")
        return problems

    reference = expected[requirement]
    if str(front["family"]) != reference["family"]:
        problems.append(
            f"family {front['family']} should be {reference['family']}"
        )
    if str(front["points"]) != str(reference["points"]):
        problems.append(
            f"points {front['points']} should be {reference['points']}"
        )
    declared_eligible = str(front["poam_eligible"]).lower() in {"true", "yes"}
    if declared_eligible != bool(reference["poam_eligible"]):
        problems.append(
            f"poam_eligible {front['poam_eligible']} should be "
            f"{str(bool(reference['poam_eligible'])).lower()}"
        )
    if str(front["confidence"]) not in VALID_CONFIDENCE:
        problems.append(f"confidence {front['confidence']} is not high, medium, or low")
    if not isinstance(front["vault_sources"], list) or not front["vault_sources"]:
        problems.append("vault_sources is empty")
    if not isinstance(front["public_sources"], list) or not front["public_sources"]:
        problems.append("public_sources is empty")

    found = section_names(text)
    for wanted in REQUIRED_SECTIONS:
        if wanted not in found:
            problems.append(f"missing section: {wanted}")
    ordered = [name for name in found if name in REQUIRED_SECTIONS]
    if ordered != list(REQUIRED_SECTIONS) and not [
        problem for problem in problems if problem.startswith("missing section")
    ]:
        problems.append(f"sections out of order: {ordered}")

    letters = objective_letters(text)
    wanted_letters = [objective["letter"] for objective in reference["objectives"]]
    if letters != wanted_letters:
        problems.append(f"objective letters {letters} should be {wanted_letters}")

    # The judgment sections tag each bullet with the objective letters it bears
    # on, and those tags are what lets an audit report a specific NOT MET
    # objective. A tag for a letter the requirement does not have points the
    # reader at an objective that does not exist.
    body = text.split("## Sufficient", 1)[-1]
    tagged = set(re.findall(r"\[([a-z])\](?!\()", body))
    stray = sorted(letter for letter in tagged if letter not in set(wanted_letters))
    if stray:
        problems.append(
            f"tags objective letters {stray} that {requirement} does not have"
        )

    # A Related requirements section pointing at a requirement id that is not
    # one of the 110 sends the reader to a control file that will never exist.
    related = re.search(r"^## Related requirements\s*$(.*)", text, re.MULTILINE | re.DOTALL)
    if related:
        referenced = set(re.findall(r"\b(3\.\d{1,2}\.\d{1,2})\b", related.group(1)))
        dead = sorted(ref for ref in referenced if ref not in expected)
        if dead:
            problems.append(f"Related requirements points at {dead}, which do not exist")

    return problems


def main() -> int:
    """Check every control file and report the failures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="control files to check")
    parser.add_argument("--controls-dir", default=str(CONTROLS_DIR))
    parser.add_argument("--requirements", default=str(REQUIREMENTS))
    args = parser.parse_args()

    index = json.loads(Path(args.requirements).read_text(encoding="utf-8"))
    expected = {entry["id"]: entry for entry in index}

    # The index itself is checked first. NIST SP 800-171A defines 320 assessment
    # objectives across the 110 Rev 2 requirements, and an index that parsed two
    # objectives into one is a defect that reaches the SPRS scoring and the
    # catalog text check that holds the SSP's objectives to this file, where a
    # missing objective is an objective nobody ever writes a statement for.
    objective_count = sum(len(entry["objectives"]) for entry in index)
    if len(index) != 110 or objective_count != 320:
        print(
            f"FAIL {args.requirements}: {len(index)} requirements and "
            f"{objective_count} objectives, expected 110 and 320"
        )
        return 1
    for entry in index:
        letters = [objective["letter"] for objective in entry["objectives"]]
        wanted = [chr(ord("a") + offset) for offset in range(len(letters))]
        if letters != wanted:
            print(
                f"FAIL {args.requirements}: {entry['id']} objective letters "
                f"{letters} are not consecutive from a"
            )
            return 1

    if args.paths:
        files = [Path(path) for path in args.paths]
    else:
        files = sorted(Path(args.controls_dir).glob("*.md"))

    failures = 0
    for path in files:
        problems = check_file(path, expected)
        if problems:
            failures += 1
            for problem in problems:
                print(f"FAIL {path}: {problem}")

    present = {path.stem for path in files}
    if not args.paths:
        missing = sorted(set(expected) - present, key=lambda rid: tuple(
            int(part) for part in rid.split(".")[1:]
        ))
        print(
            f"controls: {len(files)} of {len(expected)} written, "
            f"{failures} failing, {len(missing)} not yet started"
        )
    else:
        print(f"controls: {len(files)} checked, {failures} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
