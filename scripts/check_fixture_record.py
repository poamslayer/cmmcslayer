#!/usr/bin/env python3
"""Check the fixture engagement's record, docs/fixture/engagement/ssp/ssp.json.

The fixture's ssp.json was converted once from the previous consultant's
Markdown SSP and asset inventory (#100; docs/cold-runs/2026-09-28-fixture-ssp-conversion.md).
That Markdown was retired in #105 (docs/cold-runs/2026-09-29-fixture-markdown-ssp-retired.md),
so what it held is kept here, as the answer key's 6.14 states it, and the
record is held to it:

1. The record passes oscal-cli with our constraints file, through
   scripts/check_record.py, the same command the grader rubric uses.
2. Its assets are the ones the previous consultant left, each with the
   category they gave it, mistakes included, and no other; out-of-scope assets
   carry a justification.
3. Its statements are on the 28 requirements the previous consultant wrote,
   and on no other.
4. The view is there, each page carrying the generated-file notice, and it is
   current: scribe's render, run on a copy, produces exactly the same pages.
5. The rubric bites: a copy of the fixture with one asset's category misspelled
   fails scripts/check_record.py on the constraint that forbids it.
6. The Markdown SSP stays retired: no Markdown file under ssp/, and no asset
   inventory or responsibility matrix under scope/.

    python3 scripts/check_fixture_record.py

Needs Java and oscal-cli; about fifteen seconds.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ENGAGEMENT = Path("docs/fixture/engagement")
SSP = ENGAGEMENT / "ssp" / "ssp.json"
CHECK_RECORD = Path("scripts/check_record.py")
EDIT = Path("skills/flows/scribe/ssp_edit.py")
NS = "https://poamslayer.github.io/ns/cmmc"
NOTICE_START = "> **Generated file. Do not edit.**"
UNWRITTEN = "Not yet written."

# The assets as the previous consultant left them (known-answers.md 6.14,
# "Assets, as left"): name, category, and the kind of a Specialized Asset.
# Every other row of their inventory was "not listed" and is not an asset.
OFFICE_ENDPOINTS = ("OFFICE-DANA", "OFFICE-LUIS", "ENG-PRIYA", "PROG-TOM", "QC-MARIA",
                    "SHIP-JORDAN", "PURCH-ELLEN", "ACCT-ROB", "NADIA-LT")
AS_LEFT = {
    **{name: ("cui-asset", None) for name in OFFICE_ENDPOINTS},
    "SHOP-PC-01": ("specialized-asset", "ot"),
    "Haas VF-2 (NextGen control)": ("cui-asset", None),
    "CMM-PC": ("contractor-risk-managed-asset", None),
    "SAG-NAS": ("cui-asset", None),
    "MFP-FRONT": ("out-of-scope-asset", None),
    "Personal phones (all staff)": ("out-of-scope-asset", None),
}

# The 28 requirements the previous consultant's SSP covered (6.14, "Statements").
WRITTEN = {
    *(f"3.1.{n}" for n in range(1, 23)),
    "3.3.1", "3.5.3", "3.6.3", "3.8.4", "3.12.4", "3.13.11",
}

# What the retired Markdown SSP left, which must not come back.
RETIRED = ("ssp/*.md", "scope/asset-inventory.md", "scope/esp-responsibility-matrix.md")


def prop(obj: dict, name: str, ns: str | None = NS) -> str | None:
    for p in obj.get("props", []):
        if p.get("name") == name and p.get("ns") == ns:
            return p.get("value")
    return None


def record_check(engagement: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECK_RECORD), str(engagement)],
        capture_output=True,
        text=True,
        check=False,
    )


def check_assets(doc: dict, failures: list[str]) -> None:
    items = {
        prop(i, "asset-id", ns=None): i
        for i in doc["system-security-plan"]["system-implementation"].get("inventory-items", [])
    }
    for name, wanted in AS_LEFT.items():
        item = items.get(name)
        if item is None:
            failures.append(f"{SSP}: {name} was left as {wanted[0]} and is missing from the record")
            continue
        have = (prop(item, "asset-category"), prop(item, "specialized-asset-type"))
        if have != wanted:
            failures.append(f"{SSP}: {name} is {have} in the record; it was left as {wanted}")
        if have[0] == "out-of-scope-asset" and not (item.get("remarks") or "").strip():
            failures.append(f"{SSP}: {name} is out of scope with no justification")
    for name in sorted(set(items) - set(AS_LEFT), key=str):
        failures.append(f"{SSP}: {name} is an asset in the record and was not left in the inventory")


def check_statements(doc: dict, failures: list[str]) -> None:
    written = set()
    for req in doc["system-security-plan"]["control-implementation"]["implemented-requirements"]:
        family, number, sub = (int(x) for x in req["control-id"].lstrip("_").split("."))
        label = f"{family}.{number}.{sub}"
        if any(
            bc.get("description") != UNWRITTEN
            for s in req.get("statements", [])
            for bc in s.get("by-components", [])
        ):
            written.add(label)
    for label in sorted(WRITTEN - written):
        failures.append(f"{SSP}: {label} was written by the previous consultant and has no statement in the record")
    for label in sorted(written - WRITTEN):
        failures.append(f"{SSP}: {label} has a statement in the record the previous consultant never wrote")


def check_retired(failures: list[str]) -> None:
    for pattern in RETIRED:
        for path in sorted(ENGAGEMENT.glob(pattern)):
            failures.append(f"{path}: the Markdown SSP is retired; ssp.json is the record and view/ is generated from it")


def view_pages(view: Path) -> dict[str, bytes]:
    return {str(page.relative_to(view)): page.read_bytes() for page in sorted(view.rglob("*.md"))}


def check_view(failures: list[str]) -> None:
    view = ENGAGEMENT / "view"
    pages = view_pages(view)
    expected = {"asset-inventory.md", "esp-responsibility-matrix.md"}
    if not expected <= set(pages) or len([p for p in pages if p.startswith("requirements/")]) != 110:
        failures.append(f"{view}: {len(pages)} pages, expected the asset inventory, the responsibility matrix, "
                        "and 110 requirement pages")
    for name, text in pages.items():
        if not text.decode("utf-8").startswith(NOTICE_START):
            failures.append(f"{view / name}: does not open with the generated-file notice")
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "engagement"
        shutil.copytree(ENGAGEMENT, copy)
        proc = subprocess.run([sys.executable, str(EDIT), "--engagement", str(copy), "render"],
                              capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            failures.append(f"{EDIT} render on a copy of the fixture: {proc.stderr.strip()}")
            return
        rendered = view_pages(copy / "view")
    stale = sorted(name for name in set(pages) | set(rendered) if pages.get(name) != rendered.get(name))
    if stale:
        failures.append(f"{view}: not what scribe renders from ssp.json; stale or missing: {', '.join(stale[:5])}"
                        " (re-render it in a cold-run copy with ssp_edit.py render and copy the view back)")


def check_rubric_bites(failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "engagement"
        shutil.copytree(ENGAGEMENT, copy)
        ssp = copy / "ssp" / "ssp.json"
        doc = json.loads(ssp.read_text(encoding="utf-8"))
        broken = False
        for item in doc["system-security-plan"]["system-implementation"].get("inventory-items", []):
            for p in item.get("props", []):
                if p.get("name") == "asset-category" and p.get("ns") == NS and p.get("value") == "cui-asset":
                    p["value"] = "cui-asets"
                    broken = True
                    break
            if broken:
                break
        if not broken:
            failures.append(f"{SSP}: no CUI Asset to misspell, so the rubric's record check was not tested")
            return
        ssp.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        proc = record_check(copy)
        if proc.returncode == 0:
            failures.append(f"{CHECK_RECORD}: passed a record with the category cui-asets")
        elif "cmmc-asset-category-values" not in proc.stdout:
            failures.append(f"{CHECK_RECORD}: failed a misspelled category without naming cmmc-asset-category-values")


def main() -> int:
    failures: list[str] = []
    proc = record_check(ENGAGEMENT)
    if proc.returncode != 0:
        # Relay check_record.py's own FAIL line and its indented detail as one failure.
        block = [ln for ln in proc.stdout.splitlines() if not ln.startswith("record:")]
        failures.append("\n".join(block).removeprefix("FAIL "))
    else:
        doc = json.loads(SSP.read_text(encoding="utf-8"))
        check_assets(doc, failures)
        check_statements(doc, failures)
        check_view(failures)
        check_rubric_bites(failures)
    check_retired(failures)
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"fixture record: oscal-cli, assets, statements, view, the rubric's record check, and the retired Markdown, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
