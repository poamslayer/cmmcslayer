#!/usr/bin/env python3
"""Test scribe's check and renderer on scratch engagements (ADR-0012).

Scribe records a change by editing the SSP files, then runs
skills/flows/scribe/check_ssp.py, then render_view.py. This script is the test
of those two commands. It builds engagements under a temporary folder, never in
the repository, writes the files the way scribe or an operator would, runs the
commands, and looks only at the exit status, what they print, and the files
they leave. It imports neither command.

1. A blank SSP, every objective planned on this-system, passes.
2. A full one passes: components, assets in all five categories, a Specialized
   Asset's kind, an Out-of-Scope Asset's justification, an authorized CSP and an
   MSP, statements of every status, and the placeholder kept beside a not
   applicable statement and gone beside an implemented one.
3. The renderer writes every view page with the generated-file notice, and the
   pages show what the files hold.
4. Each rule the check enforces fails once, with a line naming the file and,
   for a statement, the objective.
5. The renderer refuses a record the check fails and leaves the view as it was.

    python3 scripts/check_scribe.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIBE = ROOT / "skills" / "flows" / "scribe"
CHECK = SCRIBE / "check_ssp.py"
RENDER = SCRIBE / "render_view.py"
REQUIREMENTS = json.loads((ROOT / "reference" / "nist-800-171r2-requirements.json").read_text(encoding="utf-8"))
NOTICE_START = "> **Generated file. Do not edit.**"

SYSTEM = """---
system-name: Acme Machining
status: under-development
information-types:
  - title: Controlled Unclassified Information
    description: CUI the organization receives or creates under its DoD contracts.
    confidentiality: moderate
    integrity: moderate
    availability: moderate
users:
  - title: System user
---

# Authorization boundary

The office network and the Microsoft 365 GCC High tenant.
"""

COMPONENTS = {
    "windows-laptops": """---
title: Windows 11 laptops
type: hardware
category: cui-asset
assets:
  - id: ENG-LT-01
    description: Engineering laptop
  - id: ENG-LT-02
---

Entra-joined Windows 11 laptops, one per office user.
""",
    "shop-floor": """---
title: Shop floor
type: hardware
assets:
  - id: VF-2 mill
    category: specialized-asset
    kind: ot
  - id: CMM-PC
    category: contractor-risk-managed-asset
    remarks: "Kept off the CUI share: no mapped drive."
  - id: Guest AP
    category: out-of-scope-asset
    justification: Separate ISP line; no route to any CUI asset.
  - id: EDR console
    category: security-protection-asset
---

The machines and the network on the shop floor.
""",
    "gcc-high": """---
title: Microsoft 365 GCC High
type: service
category: cui-asset
provider:
  role: csp
  fedramp-status: fedramp-moderate-authorized
  date-authorized: "2020-01-15"
assets:
  - id: acme.onmicrosoft.us
---

Email, files, and Teams.
""",
    "acme-msp": """---
title: Acme MSP
type: service
provider:
  role: msp
remarks: "Account test: standing Global Administrator accounts."
---

Manages endpoints and patching.
""",
}

PLACEHOLDER = "    - component: this-system\n      status: planned\n      statement: Not yet written.\n"


def requirement_file(req: dict, objectives: dict[str, str] | None = None) -> str:
    """A requirement file; objectives maps a letter to its statements' YAML, else the placeholder."""
    objectives = objectives or {}
    lines = ["---", f"requirement: {req['id']}", f"family: {req['family']}", "objectives:"]
    for objective in req["objectives"]:
        lines.append(f"  {objective['letter']}:")
        lines.append(objectives.get(objective["letter"], PLACEHOLDER).rstrip("\n"))
    lines += ["---", "", f"# {req['id']} {req['title']}", "", req["statement"], ""]
    return "\n".join(lines)


STATEMENTS = {
    "3.1.1": {
        "a": "    - component: gcc-high\n      status: implemented\n"
             "      statement: \"Authorized users are the accounts in Entra ID: the user list is the record.\"\n",
        "b": "    - component: this-system\n      status: planned\n      statement: Not yet written.\n"
             "    - component: shop-floor\n      status: not-applicable\n      statement: No process acts for a user here.\n"
             "      remarks: The shop floor runs no service accounts.\n",
        "c": "    - component: windows-laptops\n      status: partial\n      statement: >-\n"
             "        Laptops are joined to Entra ID;\n        the CMM PC is not.\n",
        "d": "    - component: acme-msp\n      status: alternative\n      statement: The MSP reviews sign-ins weekly.\n"
             "      remarks: A compensating review stands in for automated blocking.\n"
             "    - component: gcc-high\n      status: implemented\n      statement: Conditional Access blocks unknown users.\n",
        "e": "    - component: windows-laptops\n      status: planned\n      statement: Not yet written.\n",
    },
}


def write_engagement(root: Path, full: bool) -> Path:
    eng = root
    (eng / "ssp" / "components").mkdir(parents=True)
    (eng / "ssp" / "system.md").write_text(SYSTEM, encoding="utf-8")
    if full:
        for slug, text in COMPONENTS.items():
            (eng / "ssp" / "components" / f"{slug}.md").write_text(text, encoding="utf-8")
    for req in REQUIREMENTS:
        objectives = STATEMENTS.get(req["id"]) if full else None
        (eng / "ssp" / f"{req['id']}.md").write_text(requirement_file(req, objectives), encoding="utf-8")
    return eng


def run(command: Path, eng: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(command), str(eng)], capture_output=True, text=True, check=False)


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"test setup: {old!r} not in {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def snapshot(folder: Path) -> dict[str, bytes]:
    return {str(p.relative_to(folder)): p.read_bytes() for p in sorted(folder.rglob("*")) if p.is_file()}


# Each case breaks one rule in a copy of the full engagement. It names what it
# does, how, and the text the check's output must hold: the file, the objective
# where there is one, and the reason.
def break_cases():
    s = "ssp"
    c = "ssp/components"
    return [
        ("missing system file", lambda e: (e / s / "system.md").unlink(), ["ssp/system.md: missing"]),
        ("missing requirement file", lambda e: (e / s / "3.5.3.md").unlink(), ["ssp/3.5.3.md: missing"]),
        ("missing objective", lambda e: edit(e / s / "3.5.3.md", "  b:\n" + PLACEHOLDER, ""), ["ssp/3.5.3.md: 3.5.3[b] is missing"]),
        ("objective not in the reference", lambda e: edit(e / s / "3.5.3.md", "  d:\n", "  e:\n" + PLACEHOLDER + "  d:\n"),
         ["ssp/3.5.3.md: 3.5.3[e] is not an objective"]),
        ("frontmatter that does not parse", lambda e: edit(e / s / "3.1.1.md", "      status: partial\n", "      status: partial: maybe\n"),
         ["ssp/3.1.1.md: line", 'must be quoted']),
        ("no closing frontmatter line", lambda e: (e / s / "3.2.1.md").write_text("---\nrequirement: 3.2.1\n", encoding="utf-8"),
         ["ssp/3.2.1.md:", "no closing --- line"]),
        ("status outside the five", lambda e: edit(e / s / "3.1.1.md", "status: partial", "status: done"),
         ["ssp/3.1.1.md: 3.1.1[c]", '"done"', "not one of"]),
        ("component with no file", lambda e: edit(e / s / "3.1.1.md", "component: gcc-high\n      status: implemented\n      statement: \"Auth",
                                                 "component: gcc-hi\n      status: implemented\n      statement: \"Auth"),
         ["ssp/3.1.1.md: 3.1.1[a]", '"gcc-hi"', "has no file"]),
        ("duplicate asset id", lambda e: edit(e / c / "shop-floor.md", "id: CMM-PC", "id: ENG-LT-01"),
         ['asset id "ENG-LT-01" is also used in ssp/components/', "asset ids are unique across the SSP"]),
        ("alternative with no remarks", lambda e: edit(e / s / "3.1.1.md", "      remarks: A compensating review stands in for automated blocking.\n", ""),
         ["ssp/3.1.1.md: 3.1.1[d]", '"acme-msp" is alternative with no reason']),
        ("not applicable with no remarks", lambda e: edit(e / s / "3.1.1.md", "      remarks: The shop floor runs no service accounts.\n", ""),
         ["ssp/3.1.1.md: 3.1.1[b]", '"shop-floor" is not applicable with no reason']),
        ("placeholder missing beside only not applicable", lambda e: edit(e / s / "3.1.1.md", "  b:\n" + PLACEHOLDER, "  b:\n"),
         ["ssp/3.1.1.md: 3.1.1[b]", "must stay planned on this-system"]),
        ("placeholder left beside an implemented statement", lambda e: edit(e / s / "3.1.1.md", "  a:\n", "  a:\n" + PLACEHOLDER),
         ["ssp/3.1.1.md: 3.1.1[a]", "this-system is still planned beside a statement that answers"]),
        ("objective with no statements", lambda e: edit(e / s / "3.5.3.md", "  a:\n" + PLACEHOLDER, "  a: []\n"),
         ["ssp/3.5.3.md: 3.5.3[a] has no statements"]),
        ("placeholder with a written statement", lambda e: edit(e / s / "3.5.3.md", "  a:\n" + PLACEHOLDER,
                                                                "  a:\n    - component: this-system\n      status: implemented\n      statement: Done.\n"),
         ["ssp/3.5.3.md: 3.5.3[a]: this-system is the placeholder"]),
        ("category outside the five", lambda e: edit(e / c / "shop-floor.md", "category: contractor-risk-managed-asset", "category: cui-asets"),
         ['ssp/components/shop-floor.md: asset "CMM-PC" has the category "cui-asets"', "five CMMC asset categories"]),
        ("asset category contradicting its component", lambda e: edit(e / c / "windows-laptops.md", "  - id: ENG-LT-02\n",
                                                                      "  - id: ENG-LT-02\n    category: out-of-scope-asset\n    justification: Spare.\n"),
         ['ssp/components/windows-laptops.md: asset "ENG-LT-02" is recorded as Out-of-Scope Asset, which contradicts its component']),
        ("asset with no category to take", lambda e: edit(e / c / "shop-floor.md", "    category: security-protection-asset\n", ""),
         ['ssp/components/shop-floor.md: asset "EDR console" has no category']),
        ("out-of-scope asset with no justification", lambda e: edit(e / c / "shop-floor.md", "    justification: Separate ISP line; no route to any CUI asset.\n", ""),
         ['ssp/components/shop-floor.md: asset "Guest AP" is an Out-of-Scope Asset with no justification']),
        ("specialized asset with no kind", lambda e: edit(e / c / "shop-floor.md", "    kind: ot\n", ""),
         ['ssp/components/shop-floor.md: asset "VF-2 mill" is a Specialized Asset and must record its kind']),
        ("CSP with no FedRAMP status", lambda e: edit(e / c / "gcc-high.md", "  fedramp-status: fedramp-moderate-authorized\n  date-authorized: \"2020-01-15\"\n", ""),
         ["ssp/components/gcc-high.md: a CSP must record its fedramp-status"]),
        ("FedRAMP status on an MSP", lambda e: edit(e / c / "acme-msp.md", "  role: msp\n", "  role: msp\n  fedramp-status: none\n"),
         ["ssp/components/acme-msp.md: only a CSP records a fedramp-status"]),
        ("authorized CSP with no date", lambda e: edit(e / c / "gcc-high.md", "  date-authorized: \"2020-01-15\"\n", ""),
         ["ssp/components/gcc-high.md: a FedRAMP Moderate authorized CSP needs date-authorized"]),
        ("provider role outside the six", lambda e: edit(e / c / "acme-msp.md", "role: msp", "role: vendor"),
         ['ssp/components/acme-msp.md: provider role "vendor"']),
        ("field the record does not define", lambda e: edit(e / c / "acme-msp.md", "type: service\n", "type: service\nowner: Dana\n"),
         ['ssp/components/acme-msp.md: "owner" is not a field of a component']),
        ("two components with one title", lambda e: edit(e / c / "acme-msp.md", "title: Acme MSP", "title: Shop floor"),
         ['ssp/components/shop-floor.md: the title "Shop floor" is also the title of ssp/components/acme-msp.md']),
        ("a component file for the placeholder", lambda e: (e / c / "this-system.md").write_text(COMPONENTS["acme-msp"].replace("Acme MSP", "This System"), encoding="utf-8"),
         ["ssp/components/this-system.md: this-system is the placeholder and has no file"]),
        ("ssp.json back in the SSP", lambda e: (e / s / "ssp.json").write_text("{}", encoding="utf-8"),
         ["ssp/ssp.json: OSCAL is gone from the SSP"]),
    ]


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="scribe-check-") as tmp:
        tmp = Path(tmp)

        blank = write_engagement(tmp / "blank", full=False)
        proc = run(CHECK, blank)
        if proc.returncode != 0:
            failures.append(f"a blank SSP fails the check:\n{proc.stdout}")

        full = write_engagement(tmp / "full", full=True)
        proc = run(CHECK, full)
        if proc.returncode != 0:
            failures.append(f"a full, valid SSP fails the check:\n{proc.stdout}")
        elif "4 components, 7 assets, 5 written statements" not in proc.stdout:
            failures.append(f"the check's summary does not count what the files hold: {proc.stdout.strip()}")

        proc = run(RENDER, full)
        view = full / "view"
        if proc.returncode != 0:
            failures.append(f"the renderer fails on a valid SSP:\n{proc.stdout}{proc.stderr}")
        else:
            pages = snapshot(view)
            if len([p for p in pages if p.startswith("requirements/")]) != 110 or not {
                    "asset-inventory.md", "esp-responsibility-matrix.md"} <= set(pages):
                failures.append(f"the view has {len(pages)} pages; expected the inventory, the matrix, and 110 requirement pages")
            for name, data in pages.items():
                if not data.decode("utf-8").startswith(NOTICE_START):
                    failures.append(f"view/{name} does not open with the generated-file notice")
            inventory = (view / "asset-inventory.md").read_text(encoding="utf-8")
            for wanted in ("| ENG-LT-02 | Windows 11 laptops | ENG-LT-02 |", "| VF-2 mill | Shop floor | OT |",
                           "| Guest AP | Shop floor | Guest AP | Separate ISP line; no route to any CUI asset. |",
                           "| Microsoft 365 GCC High | CSP | FedRAMP Moderate authorized | 2020-01-15 |",
                           "### Security Protection Asset", "Kept off the CUI share: no mapped drive."):
                if wanted not in inventory:
                    failures.append(f"view/asset-inventory.md does not show {wanted!r}")
            page = (view / "requirements" / "3.1.1.md").read_text(encoding="utf-8")
            for wanted in ("| Microsoft 365 GCC High | Implemented | Authorized users are the accounts in Entra ID: the user list is the record. |  |",
                           "| This System | Planned | Not yet written. |  |\n| Shop floor | Not applicable |",
                           "| Windows 11 laptops | Partial | Laptops are joined to Entra ID; the CMM PC is not. |",
                           "| Acme MSP | Alternative | The MSP reviews sign-ins weekly. | A compensating review stands in for automated blocking. |"):
                if wanted not in page:
                    failures.append(f"view/requirements/3.1.1.md does not show {wanted!r}")
            matrix = (view / "esp-responsibility-matrix.md").read_text(encoding="utf-8")
            for wanted in ("| Acme MSP | MSP | ESP | Not applicable |  | Manages endpoints and patching. | Account test: standing Global Administrator accounts. |",
                           "### 3.1.1[d]", "| Acme MSP | Provider's | Alternative |", "| acme.onmicrosoft.us | Microsoft 365 GCC High | CUI Asset |"):
                if wanted not in matrix:
                    failures.append(f"view/esp-responsibility-matrix.md does not show {wanted!r}")
            if "### 3.1.1[c]" in matrix:
                failures.append("view/esp-responsibility-matrix.md lists 3.1.1[c], which no provider speaks to")

        for name, damage, wanted in break_cases():
            case = tmp / "case"
            shutil.rmtree(case, ignore_errors=True)
            shutil.copytree(full, case)
            damage(case)
            before = snapshot(case / "view")
            proc = run(CHECK, case)
            if proc.returncode != 1:
                failures.append(f"{name}: the check passed it")
                continue
            missing = [w for w in wanted if w not in proc.stdout]
            if missing:
                failures.append(f"{name}: the check's output does not say {missing}:\n{proc.stdout}")
            proc = run(RENDER, case)
            if proc.returncode == 0 or snapshot(case / "view") != before:
                failures.append(f"{name}: the renderer did not refuse it, or changed the view")

    for failure in failures:
        print(f"FAIL {failure}")
    print(f"scribe check and render: {len(break_cases())} rules broken one at a time, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
