#!/usr/bin/env python3
"""Grade an engagement's record, the SSP under ssp/ (ADR-0012), for a cold run.

The grader rubric's two record checks (docs/fixture/grader-rubric.md) start
here:

1. The record passes scribe's check, skills/flows/scribe/check_ssp.py. This
   is the whole of rubric check 4, and a failure scores it 0, which fails the
   run.
2. What the record holds, printed in the answer key's terms (components,
   assets and their categories, providers with role and FedRAMP status, and
   every written statement by objective), so a grader can compare it with
   known-answers.md 6.14 for rubric check 5. With --baseline, only what the
   run changed against the starting record is printed.

    python3 scripts/check_record.py /tmp/poamslayer-cold-runs/<run>
    python3 scripts/check_record.py /tmp/poamslayer-cold-runs/<run> --baseline docs/fixture/engagement

Exit status is 1 when the record, or the baseline, fails the check.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "flows" / "scribe"))

from check_ssp import problems  # noqa: E402
from ssp_record import PLACEHOLDER, Record, default_requirements, is_unwritten, load_requirements  # noqa: E402


def contents(record: Record) -> list[str]:
    """The record as lines a grader compares with the answer key."""
    lines = []
    components = sorted(record.components.values(), key=lambda c: c.title.lower())
    for c in components:
        line = f"component: {c.title} ({c.data.get('type')})"
        if c.data.get("category"):
            line += f", category {c.data['category']}"
        if c.provider:
            line += f", provider role {c.provider.get('role')}"
            if c.provider.get("fedramp-status"):
                line += f", FedRAMP {c.provider['fedramp-status']}"
        lines.append(line)
    for c in components:
        for asset in c.assets:
            kind = asset.get("kind")
            line = f"asset: {asset.get('id')}: {c.asset_category(asset)}{f' ({kind})' if kind else ''}, component {c.title}"
            if asset.get("justification"):
                line += f"; justification: {asset['justification']}"
            if asset.get("remarks"):
                line += f"; remarks: {asset['remarks']}"
            lines.append(line)
    for requirement in record.requirements:
        for objective in requirement["objectives"]:
            label = f"{requirement['id']}[{objective['letter']}]"
            for e in record.objective_entries(requirement["id"], objective["letter"]):
                component = e.get("component")
                if is_unwritten(e):
                    # The placeholder is the default and says nothing. A cleared
                    # statement left on a named component is a claim that the
                    # component still owes the objective, so a grader must see it.
                    if component != PLACEHOLDER:
                        lines.append(f"statement: {label} by {record.title_of(component)}: planned, not yet written")
                    continue
                line = f"statement: {label} by {record.title_of(component)}: {e.get('status')}: {e.get('statement')}"
                if e.get("remarks"):
                    line += f" (remarks: {e['remarks']})"
                lines.append(line)
    return lines


def checked(engagement: Path, requirements: list[dict]) -> tuple[Record, list[str]]:
    record, found = problems(engagement.resolve(), requirements)
    return record, found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("engagement", help="the engagement repo a run left, such as a cold-run copy")
    parser.add_argument("--baseline", help="the engagement the run started from; print only what changed")
    args = parser.parse_args()
    requirements = load_requirements(default_requirements())

    record, found = checked(Path(args.engagement), requirements)
    if found:
        print(f"FAIL {args.engagement}: the record fails scribe's check")
        for line in found:
            print(f"       {line}")
        print("record: invalid; rubric check 4 scores 0 and the run fails")
        return 1

    lines = contents(record)
    if args.baseline:
        before, base_found = checked(Path(args.baseline), requirements)
        if base_found:
            print(f"FAIL {args.baseline}: the baseline fails scribe's check")
            print("record: valid, but the baseline could not be read, so nothing was compared")
            return 1
        before_lines = contents(before)
        old, new = set(before_lines), set(lines)
        removed = [ln for ln in before_lines if ln not in new]
        added = [ln for ln in lines if ln not in old]
        for ln in removed:
            print(f"- {ln}")
        for ln in added:
            print(f"+ {ln}")
        print(f"record: valid; {len(added)} lines added and {len(removed)} removed against {args.baseline}")
    else:
        for ln in lines:
            print(ln)
        print(f"record: valid; {len(lines)} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
