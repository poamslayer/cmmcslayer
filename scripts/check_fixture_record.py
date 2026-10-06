#!/usr/bin/env python3
"""Check the fixture engagement's record, the SSP under docs/fixture/engagement/ssp/.

The fixture's record was converted once from the previous consultant's
Markdown SSP and asset inventory into ssp.json (#100;
docs/cold-runs/2026-09-28-fixture-ssp-conversion.md), and from ssp.json into
the Markdown SSP of ADR-0012 (#128;
docs/cold-runs/2026-10-05-fixture-markdown-ssp-conversion.md). What the
previous consultant left is kept here, as the answer key's 6.14 states it,
and the record is held to it:

1. The record passes scribe's check, through scripts/check_record.py, the same
   command the grader rubric uses.
2. Its assets are the ones the previous consultant left, each with the
   category they gave it, mistakes included, and no other; out-of-scope assets
   carry a justification.
3. Its statements are on the 28 requirements the previous consultant wrote,
   and on no other.
4. The view is there, each page carrying the generated-file notice, and it is
   current: scribe's renderer, run on a copy, produces exactly the same pages.
5. The rubric bites: a copy of the fixture with one asset's category misspelled
   fails scripts/check_record.py, naming the category.
6. What is gone stays gone: no ssp.json or other OSCAL file anywhere in the
   fixture engagement, and no asset inventory or responsibility matrix under
   scope/ (#105).

    python3 scripts/check_fixture_record.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGAGEMENT = ROOT / "docs" / "fixture" / "engagement"
CHECK_RECORD = ROOT / "scripts" / "check_record.py"
RENDER = ROOT / "skills" / "flows" / "scribe" / "render_view.py"
NOTICE_START = "> **Generated file. Do not edit.**"

sys.path.insert(0, str(ROOT / "skills" / "flows" / "scribe"))
from ssp_record import default_requirements, is_unwritten, load, load_requirements  # noqa: E402

# The assets as the previous consultant left them (known-answers.md 6.14,
# "Assets, as left"): id, category, and the kind of a Specialized Asset.
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

# What must not come back: the OSCAL record, and the retired Markdown inventory and matrix.
GONE = ("**/*.json", "**/oscal", "scope/asset-inventory.md", "scope/esp-responsibility-matrix.md")


def record_check(engagement: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECK_RECORD), str(engagement)],
                          capture_output=True, text=True, check=False)


def check_assets(record, failures: list[str]) -> None:
    where = "docs/fixture/engagement/ssp/components/"
    assets = {a.get("id"): (a, c) for c in record.components.values() for a in c.assets}
    for name, wanted in AS_LEFT.items():
        if name not in assets:
            failures.append(f"{where}: {name} was left as {wanted[0]} and is missing from the record")
            continue
        asset, component = assets[name]
        have = (component.asset_category(asset), asset.get("kind"))
        if have != wanted:
            failures.append(f"{where}{component.slug}.md: {name} is {have} in the record; it was left as {wanted}")
    for name in sorted(set(assets) - set(AS_LEFT), key=str):
        failures.append(f"{where}{assets[name][1].slug}.md: {name} is an asset in the record and was not left in the inventory")


def check_statements(record, failures: list[str]) -> None:
    written = {
        rid
        for rid, data in record.statements.items()
        for entries in (data.get("objectives") or {}).values()
        for e in entries or []
        if isinstance(e, dict) and not is_unwritten(e)
    }
    for rid in sorted(WRITTEN - written):
        failures.append(f"docs/fixture/engagement/ssp/{rid}.md: written by the previous consultant and has no statement in the record")
    for rid in sorted(written - WRITTEN):
        failures.append(f"docs/fixture/engagement/ssp/{rid}.md: has a statement the previous consultant never wrote")


def check_gone(failures: list[str]) -> None:
    for pattern in GONE:
        for path in sorted(ENGAGEMENT.glob(pattern)):
            failures.append(f"{path.relative_to(ROOT)}: gone from the fixture; the SSP is the Markdown under ssp/ (ADR-0012) "
                            "and view/ is generated from it")


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
        proc = subprocess.run([sys.executable, str(RENDER), str(copy)], capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            failures.append(f"{RENDER.relative_to(ROOT)} on a copy of the fixture: {proc.stdout.strip()}{proc.stderr.strip()}")
            return
        rendered = view_pages(copy / "view")
    stale = sorted(name for name in set(pages) | set(rendered) if pages.get(name) != rendered.get(name))
    if stale:
        failures.append(f"{view}: not what scribe renders from ssp/; stale or missing: {', '.join(stale[:5])}"
                        " (re-render it in a cold-run copy with render_view.py and copy the view back)")


def check_rubric_bites(failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "engagement"
        shutil.copytree(ENGAGEMENT, copy)
        target = copy / "ssp" / "components" / "sag-nas.md"
        text = target.read_text(encoding="utf-8")
        if "category: cui-asset\n" not in text:
            failures.append("docs/fixture/engagement/ssp/components/sag-nas.md: no CUI Asset to misspell, "
                            "so the rubric's record check was not tested")
            return
        target.write_text(text.replace("category: cui-asset\n", "category: cui-asets\n", 1), encoding="utf-8")
        proc = record_check(copy)
        if proc.returncode == 0:
            failures.append(f"{CHECK_RECORD.relative_to(ROOT)}: passed a record with the category cui-asets")
        elif '"cui-asets"' not in proc.stdout:
            failures.append(f"{CHECK_RECORD.relative_to(ROOT)}: failed a misspelled category without naming it")


def main() -> int:
    failures: list[str] = []
    proc = record_check(ENGAGEMENT)
    if proc.returncode != 0:
        failures.append("\n".join(ln for ln in proc.stdout.splitlines() if not ln.startswith("record:")).removeprefix("FAIL "))
    else:
        record = load(ENGAGEMENT, load_requirements(default_requirements()))
        check_assets(record, failures)
        check_statements(record, failures)
        check_view(failures)
        check_rubric_bites(failures)
    check_gone(failures)
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"fixture record: scribe's check, assets, statements, view, the rubric's record check, and no OSCAL, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
