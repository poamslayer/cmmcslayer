#!/usr/bin/env python3
"""Grade an engagement's record, ssp/ssp.json, for a cold run.

The grader rubric's two record checks (docs/fixture/grader-rubric.md) start
here:

1. The record passes oscal-cli with our constraints file. This is the whole of
   rubric check 4, and a failure scores it 0, which fails the run.
2. What the record holds, printed in the answer key's terms (components,
   assets and their categories, providers with role and FedRAMP status, and
   every written statement by objective), so a grader can compare it with
   known-answers.md 6.14 for rubric check 5. With --baseline, only what the
   run changed against the starting record is printed.

    python3 scripts/check_record.py /tmp/poamslayer-cold-runs/<run>
    python3 scripts/check_record.py /tmp/poamslayer-cold-runs/<run> --baseline docs/fixture/engagement

Exit status is 1 when the record is missing, is not JSON, or fails oscal-cli.
Needs Java and oscal-cli, like scripts/check_oscal_cli.py.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

CONSTRAINTS = Path(__file__).resolve().parents[1] / "reference" / "oscal" / "cmmc-constraints.xml"
NS = "https://poamslayer.github.io/ns/cmmc"
INSTALL_HINT = "install it with: bash scripts/install_oscal_cli.sh"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
SCHEMA_NOISE = re.compile(r"\[#\] #:|subschema|schema violations found")
OBJECTIVE_ID = re.compile(r"_(\d+)\.(\d+)\.(\d+)_obj\.([a-z])")
# scribe's placeholder for an objective nobody has written yet.
UNWRITTEN = "Not yet written."


def oscal_cli_problems(ssp: Path) -> str | None:
    """None when oscal-cli passes the record, otherwise why it did not."""
    if shutil.which("java") is None:
        return "java not found; oscal-cli needs Java 11 or later"
    if shutil.which("oscal-cli") is None:
        return f"oscal-cli not found on PATH; {INSTALL_HINT}"
    proc = subprocess.run(
        ["oscal-cli", "validate", "--no-color", str(ssp), "-c", str(CONSTRAINTS)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return None
    output = ANSI.sub("", proc.stdout + proc.stderr)
    lines = [ln for ln in output.splitlines() if not ln.startswith("Picked up JAVA_TOOL_OPTIONS")]
    kept = [ln for ln in lines if ("ERROR" in ln or "CRITICAL" in ln) and not SCHEMA_NOISE.search(ln)]
    return "oscal-cli rejected it\n" + "\n".join(f"       {ln.strip()}" for ln in (kept or lines[-5:]))


def load(engagement: Path) -> tuple[Path, dict | None, str | None]:
    ssp = engagement / "ssp" / "ssp.json"
    if not ssp.is_file():
        return ssp, None, "no record; the run must leave ssp/ssp.json"
    try:
        return ssp, json.loads(ssp.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as error:
        return ssp, None, f"not valid JSON: {error}"


def prop(obj: dict, name: str, ns: str | None = NS) -> str | None:
    for p in obj.get("props", []):
        if p.get("name") == name and p.get("ns") == ns:
            return p.get("value")
    return None


def objective_label(statement_id: str) -> str:
    match = OBJECTIVE_ID.fullmatch(statement_id)
    if not match:
        return statement_id
    family, number, sub, letter = match.groups()
    return f"{int(family)}.{int(number)}.{int(sub)}[{letter}]"


def contents(doc: dict) -> list[str]:
    """The record as lines a grader compares with the answer key. No OSCAL ids."""
    plan = doc["system-security-plan"]
    system = plan.get("system-implementation", {})
    components = system.get("components", [])
    titles = {c["uuid"]: c.get("title", "") for c in components}
    placeholder = next((c["uuid"] for c in components if c.get("type") == "this-system"), None)
    lines = []
    for c in components:
        if c.get("type") == "this-system":
            continue
        category = prop(c, "asset-category")
        line = f"component: {c.get('title')} ({c.get('type')})"
        if category:
            line += f", category {category}"
        role = prop(c, "provider-role")
        if role:
            line += f", provider role {role}"
            status = prop(c, "fedramp-status")
            if status:
                line += f", FedRAMP {status}"
        lines.append(line)
    for item in system.get("inventory-items", []):
        name = prop(item, "asset-id", ns=None) or item.get("description", "")
        category = prop(item, "asset-category") or "no category"
        kind = prop(item, "specialized-asset-type")
        owners = ", ".join(titles.get(ic.get("component-uuid"), "?") for ic in item.get("implemented-components", []))
        line = f"asset: {name}: {category}{f' ({kind})' if kind else ''}, component {owners}"
        if item.get("remarks"):
            line += f"; remarks: {item['remarks']}"
        lines.append(line)
    for req in plan.get("control-implementation", {}).get("implemented-requirements", []):
        for statement in req.get("statements", []):
            for bc in statement.get("by-components", []):
                if bc.get("description") == UNWRITTEN:
                    # The placeholder on This System is the default and says nothing. A
                    # cleared statement left on a named component is a claim that the
                    # component still owes the objective, so a grader must see it.
                    if bc.get("component-uuid") != placeholder:
                        lines.append(
                            f"statement: {objective_label(statement.get('statement-id', ''))} by "
                            f"{titles.get(bc.get('component-uuid'), '?')}: planned, not yet written"
                        )
                    continue
                status = bc.get("implementation-status", {})
                line = (
                    f"statement: {objective_label(statement.get('statement-id', ''))} by "
                    f"{titles.get(bc.get('component-uuid'), '?')}: {status.get('state')}: {bc.get('description')}"
                )
                if status.get("remarks"):
                    line += f" (remarks: {status['remarks']})"
                lines.append(line)
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("engagement", help="the engagement repo a run left, such as a cold-run copy")
    parser.add_argument("--baseline", help="the engagement the run started from; print only what changed")
    args = parser.parse_args()

    ssp, doc, problem = load(Path(args.engagement))
    if problem is None:
        problem = oscal_cli_problems(ssp)
    if problem is not None:
        print(f"FAIL {ssp}: {problem}")
        print("record: invalid; rubric check 4 scores 0 and the run fails")
        return 1

    lines = contents(doc)
    if args.baseline:
        _, before, base_problem = load(Path(args.baseline))
        if base_problem is not None:
            print(f"FAIL {args.baseline}: {base_problem}")
            print("record: valid, but the baseline could not be read, so nothing was compared")
            return 1
        before_lines = contents(before)
        old = set(before_lines)
        new = set(lines)
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
