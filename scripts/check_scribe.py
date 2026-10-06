#!/usr/bin/env python3
"""Test scribe's edit command, skills/flows/scribe/ssp_edit.py, end to end.

Every case runs the command in a scratch engagement under a temporary folder,
never in the repository, and checks only what an operator or assessor would
see: the resulting ssp.json, oscal-cli's verdict on it, and the view. Nothing
here imports the command's internals.

1. create writes a skeleton that passes oscal-cli: 110 requirements, every
   objective planned, and a view with the generated-file notice.
2. create refuses to overwrite an existing ssp.json.
3. add-component passes oscal-cli and re-renders the view with the component.
4. The same add twice mints no second UUID and leaves the file unchanged.
5. A change oscal-cli rejects exits non-zero with a message naming the
   operation and the reason, and leaves ssp.json and the view byte for byte
   unchanged.
6. Without oscal-cli on PATH, the command stops and changes nothing.

Assets, categories, and providers (#97):

7. Assets in each of the five categories, a Specialized Asset with its kind,
   and providers with their role and FedRAMP status pass oscal-cli; a
   FedRAMP-authorized provider is a leveraged authorization; the view lists
   them, out-of-scope assets with their justification.
8. An asset takes its component's category when it gives none.
9. Renaming a component keeps its UUID, and its assets still point at it;
   renaming it to its own title changes nothing.
10. Splitting "Windows 11 laptops" into engineering and front-office components
    moves the named assets; all valid. A component split out of a provider
    stays a provider.
11. Removing a component still in use is refused and changes nothing; with a
    component to move the assets to, it succeeds.
12. The refusals: a category outside the five (by oscal-cli, through our
    constraints file), an asset or component category that contradicts the
    other, an out-of-scope asset with no justification, a CSP with no
    FedRAMP status, an asset on a component that does not exist. Each leaves
    ssp.json and the view byte for byte unchanged.
13. Renaming a provider keeps its leveraged authorization and party in step;
    removing an authorized CSP says it removed the leveraged authorization; a
    status that is no longer FedRAMP authorized drops it.

Conformity statements and the requirement view pages (#98):

14. Statements on 3.5.3[a] for Entra ID (implemented) and for the mobile
    devices (not applicable, with a reason) pass oscal-cli, land on the
    objective part, and replace the "This System" placeholder there. Setting
    the same statement again changes nothing.
15. The 3.5.3 view page shows objectives [a] to [d] with their statements and
    statuses, the generated-file notice, and no OSCAL ids.
16. The refusals: not applicable or alternative without a reason, an
    objective that is not in the catalog (3.5.3[e]), an objective not written
    in the 3.5.3[a] form, a statement that says nothing, a component that does
    not exist. Each leaves
    ssp.json and the view byte for byte unchanged.
17. Clearing a statement returns the objective to planned for that
    component; a component whose statements are all cleared can be removed,
    and an objective left with no component falls back to "This System".

The responsibility matrix view and re-rendering (#102):

18. Providers record their remarks (the access model and the data they hold)
    on add-provider and change-provider, and pass oscal-cli. The generated
    view/esp-responsibility-matrix.md opens with the generated-file notice and
    lists each provider with its role, CSP or ESP, FedRAMP status, what it
    does, and its remarks; the provider's assets with their categories; and,
    before any statement names a provider, says so. A component that is not a
    provider is not listed as one.
19. A conformity statement on a provider shows in the matrix under its
    objective, in 3.5.3[a] form, beside the company components' statements on
    the same objective, with no OSCAL ids.
20. render re-renders a view that was deleted or is stale, and leaves ssp.json
    byte for byte unchanged.

Many statements at once, for the SSP writers (#103):

21. set-statements records every statement in a file with one validation:
    the result passes oscal-cli, each lands on its objective and component
    with its status and reason, and the requirement pages show them. The same
    file again changes nothing.
22. A file with one bad entry records none of it: the refusal names the entry
    and its objective, and ssp.json and the view are byte for byte unchanged.
    A file that is not a list of statements, or an entry missing a field, is
    refused the same way.
23. remove-statement takes a component off an objective it should never have
    described: its entry is gone, not left planned, the requirement page no
    longer lists it, and an objective left with no component is planned on
    "This System" again. Removing a component that does not describe the
    objective is refused and changes nothing.
24. A not applicable statement does not answer the objective for the system:
    while every statement on an objective is not applicable, it stays planned
    on "This System" too, so the record never reads as if the requirement
    applies nowhere. The placeholder goes when a component records any other
    status, and comes back if that statement is removed.

Reading the record, for every skill that reads the SSP (#104):

25. show prints the record in domain terms: the components, providers, and
    assets with their categories, and, for the requirements asked, each
    objective in 3.5.3[a] form with every component's status and statement. A
    family such as 3.5 shows each of its requirements. It prints no OSCAL ids
    and no generated-file notice, and leaves ssp.json and the view byte for
    byte unchanged.
26. On a record someone edited by hand, show names the problems in operator
    words: a statement on a component the record does not have, an asset on
    a component the record does not have, an asset whose category
    contradicts its component's, an asset with no category or a category
    outside the five, an Out-of-Scope Asset with no justification, and a not
    applicable statement with no reason. A clean record says it has none.
27. show refuses a requirement the catalog does not have, and an engagement
    with no ssp.json.

    python3 scripts/check_scribe.py

Needs Java and oscal-cli, like check_oscal_cli.py. Takes about two minutes:
every case starts oscal-cli, which starts a JVM.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EDIT = Path("skills/flows/scribe/ssp_edit.py").resolve()
CONSTRAINTS = Path("reference/oscal/cmmc-constraints.xml").resolve()
NOTICE_START = "> **Generated file. Do not edit.**"


def edit(engagement: Path, *args: str, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(EDIT), "--engagement", str(engagement), *args],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def oscal_cli_passes(path: Path) -> bool:
    proc = subprocess.run(
        ["oscal-cli", "validate", "--no-color", str(path), "-c", str(CONSTRAINTS)],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def components(ssp: Path) -> list[dict]:
    doc = json.loads(ssp.read_text(encoding="utf-8"))
    return doc["system-security-plan"]["system-implementation"]["components"]


def add_entra(engagement: Path, *extra: str) -> subprocess.CompletedProcess:
    return edit(
        engagement,
        "add-component",
        "--title",
        "Entra ID",
        "--type",
        "service",
        "--description",
        "Identity provider for every user account.",
        *extra,
    )


def check(failures: list[str], base: Path) -> None:
    fresh = base / "fresh"
    ssp = fresh / "ssp" / "ssp.json"
    view = fresh / "view" / "asset-inventory.md"

    # 1. create
    proc = edit(fresh, "create", "--system-name", "Scratch Machining")
    if proc.returncode != 0:
        failures.append(f"{EDIT} create: exited {proc.returncode}: {proc.stderr.strip()}")
        return
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: the skeleton from create does not pass oscal-cli")
    plan = json.loads(ssp.read_text(encoding="utf-8"))["system-security-plan"]
    requirements = plan["control-implementation"]["implemented-requirements"]
    statements = [s for r in requirements for s in r.get("statements", [])]
    states = {b["implementation-status"]["state"] for s in statements for b in s["by-components"]}
    if len(requirements) != 110 or len(statements) != 320 or states != {"planned"}:
        failures.append(
            f"{ssp}: skeleton has {len(requirements)} requirements, {len(statements)} objectives, "
            f"states {sorted(states)}; expected 110, 320, planned"
        )
    if not view.is_file() or not view.read_text(encoding="utf-8").startswith(NOTICE_START):
        failures.append(f"{view}: create did not render the view with the generated-file notice")

    # 2. create never overwrites
    before = ssp.read_bytes()
    proc = edit(fresh, "create", "--system-name", "Other")
    if proc.returncode == 0 or ssp.read_bytes() != before:
        failures.append(f"{EDIT} create: overwrote an existing ssp.json")

    # 3. add a component
    added = base / "added"
    shutil.copytree(fresh, added)
    ssp = added / "ssp" / "ssp.json"
    view = added / "view" / "asset-inventory.md"
    proc = add_entra(added)
    if proc.returncode != 0:
        failures.append(f"{EDIT} add-component: exited {proc.returncode}: {proc.stderr.strip()}")
        return
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after add-component")
    text = view.read_text(encoding="utf-8")
    if not text.startswith(NOTICE_START) or "| Entra ID | service |" not in text:
        failures.append(f"{view}: not re-rendered with the notice and Entra ID after add-component")

    # 4. the same add twice mints no second UUID
    before = ssp.read_bytes()
    first = [c["uuid"] for c in components(ssp) if c["title"] == "Entra ID"]
    proc = add_entra(added)
    after = [c["uuid"] for c in components(ssp) if c["title"] == "Entra ID"]
    if proc.returncode != 0 or after != first or len(after) != 1 or ssp.read_bytes() != before:
        failures.append(f"{EDIT} add-component twice: expected one Entra ID with UUID {first}, found {after}")

    # 5. a change oscal-cli rejects leaves everything as it was
    before, view_before = ssp.read_bytes(), view.read_bytes()
    proc = edit(
        added,
        "add-component",
        "--title",
        "Engineering laptops",
        "--type",
        "hardware",
        "--description",
        "Windows 11 laptops in engineering.",
        "--category",
        "cui-asets",
    )
    message = proc.stderr
    if proc.returncode == 0:
        failures.append(f"{EDIT} add-component: accepted the invalid category cui-asets")
    if 'add-component "Engineering laptops"' not in message or "cmmc-asset-category-values" not in message:
        failures.append(f"{EDIT} add-component: the refusal does not name the operation and the rule: {message.strip()}")
    if ssp.read_bytes() != before or view.read_bytes() != view_before:
        failures.append(f"{ssp}: changed after a refused add-component")
    if list((added / "ssp").glob(".ssp-*")):
        failures.append(f"{added / 'ssp'}: a refused change left its temporary file behind")

    # 6. no oscal-cli is a hard stop, not a skip
    python_only = base / "bin"
    python_only.mkdir()
    (python_only / "python3").symlink_to(sys.executable)
    env = {**os.environ, "PATH": str(python_only)}
    proc = edit(
        added, "add-component", "--title", "SIEM", "--type", "service", "--description", "Log collection.", env=env
    )
    if proc.returncode == 0 or "not found" not in proc.stderr or ssp.read_bytes() != before:
        failures.append(f"{EDIT} add-component: did not stop cleanly without oscal-cli: {proc.stderr.strip()}")


def edit_ok(failures: list[str], engagement: Path, *args: str) -> bool:
    proc = edit(engagement, *args)
    if proc.returncode != 0:
        failures.append(f"{EDIT} {' '.join(args[:3])}: exited {proc.returncode}: {proc.stderr.strip()}")
        return False
    return True


def refused_unchanged(failures: list[str], engagement: Path, expect: str, *args: str) -> None:
    """The operation must be refused, say why, and leave the record and the view as they were."""
    ssp = engagement / "ssp" / "ssp.json"
    view = engagement / "view" / "asset-inventory.md"
    before, view_before = ssp.read_bytes(), view.read_bytes()
    proc = edit(engagement, *args)
    label = " ".join(args[:3])
    if proc.returncode == 0:
        failures.append(f"{EDIT} {label}: accepted; expected a refusal mentioning {expect!r}")
    elif expect not in proc.stderr:
        failures.append(f"{EDIT} {label}: refusal does not mention {expect!r}: {proc.stderr.strip()}")
    if ssp.read_bytes() != before or view.read_bytes() != view_before:
        failures.append(f"{ssp}: changed after a refused {label}")


def plan_of(engagement: Path) -> dict:
    return json.loads((engagement / "ssp" / "ssp.json").read_text(encoding="utf-8"))["system-security-plan"]


def cmmc(obj: dict, name: str) -> str | None:
    for prop in obj.get("props", []):
        if prop.get("ns") == "https://poamslayer.github.io/ns/cmmc" and prop.get("name") == name:
            return prop.get("value")
    return None


def by_title(plan: dict, title: str) -> dict | None:
    return next((c for c in plan["system-implementation"].get("components", []) if c.get("title") == title), None)


def asset_named(plan: dict, name: str) -> dict | None:
    for item in plan["system-implementation"].get("inventory-items", []):
        if any(p.get("name") == "asset-id" and p.get("value") == name for p in item.get("props", [])):
            return item
    return None


def points_at(item: dict | None) -> list[str]:
    return [ic["component-uuid"] for ic in (item or {}).get("implemented-components", [])]


def check_assets(failures: list[str], base: Path, fresh: Path) -> None:
    eng = base / "assets"
    shutil.copytree(fresh, eng)
    ssp = eng / "ssp" / "ssp.json"
    view = eng / "view" / "asset-inventory.md"

    # 7. one asset in each category, a specialized asset, providers
    steps = [
        ["add-component", "--title", "Windows 11 laptops", "--type", "hardware", "--description", "Company laptops."],
        ["add-component", "--title", "Entra ID", "--type", "service", "--description", "Identity provider.",
         "--category", "security-protection-asset"],
        ["add-component", "--title", "Haas mills", "--type", "hardware", "--description", "CNC mills on the floor."],
        ["add-component", "--title", "Guest Wi-Fi", "--type", "hardware", "--description", "Visitor network."],
        ["add-asset", "--name", "ENG-LT-01", "--component", "Windows 11 laptops", "--category", "cui-asset"],
        ["add-asset", "--name", "ENG-LT-02", "--component", "Windows 11 laptops", "--category", "cui-asset"],
        ["add-asset", "--name", "FO-LT-01", "--component", "Windows 11 laptops", "--category", "contractor-risk-managed-asset"],
        ["add-asset", "--name", "Entra tenant", "--component", "Entra ID"],
        ["add-asset", "--name", "VF-2 mill", "--component", "Haas mills", "--category", "specialized-asset",
         "--specialized-type", "ot"],
        ["add-asset", "--name", "Guest AP", "--component", "Guest Wi-Fi", "--category", "out-of-scope-asset",
         "--remarks", "Physically separate network; cannot reach CUI assets."],
        ["add-provider", "--title", "Microsoft 365 GCC High", "--role", "csp", "--description", "Email and files.",
         "--fedramp-status", "fedramp-moderate-authorized", "--date-authorized", "2020-01-15"],
        ["add-provider", "--title", "Acme MSP", "--role", "msp", "--description", "Manages endpoints and patching."],
    ]
    for step in steps:
        if not edit_ok(failures, eng, *step):
            return
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after assets and providers")
    plan = plan_of(eng)
    categories = {cmmc(i, "asset-category") for i in plan["system-implementation"].get("inventory-items", [])}
    if categories != {"cui-asset", "security-protection-asset", "contractor-risk-managed-asset",
                      "specialized-asset", "out-of-scope-asset"}:
        failures.append(f"{ssp}: asset categories recorded are {sorted(c or '' for c in categories)}")
    # 8. the asset took its component's category
    if cmmc(asset_named(plan, "Entra tenant") or {}, "asset-category") != "security-protection-asset":
        failures.append(f"{ssp}: Entra tenant did not take its component's category")
    if cmmc(asset_named(plan, "VF-2 mill") or {}, "specialized-asset-type") != "ot":
        failures.append(f"{ssp}: VF-2 mill does not record its specialized-asset-type")
    gcch = by_title(plan, "Microsoft 365 GCC High") or {}
    if (cmmc(gcch, "provider-role"), cmmc(gcch, "fedramp-status")) != ("csp", "fedramp-moderate-authorized"):
        failures.append(f"{ssp}: GCC High does not record role csp and FedRAMP Moderate authorized")
    if not any(la.get("title") == "Microsoft 365 GCC High" for la in plan["system-implementation"].get("leveraged-authorizations", [])):
        failures.append(f"{ssp}: GCC High is not recorded as a leveraged authorization")
    if cmmc(by_title(plan, "Acme MSP") or {}, "provider-role") != "msp":
        failures.append(f"{ssp}: Acme MSP does not record its role")
    text = view.read_text(encoding="utf-8")
    for needle in ("### Out-of-Scope Asset", "Physically separate network; cannot reach CUI assets.",
                   "### Specialized Asset", "Microsoft 365 GCC High", "FedRAMP Moderate authorized", "Acme MSP"):
        if needle not in text:
            failures.append(f"{view}: does not show {needle!r}")

    # 9. rename keeps the UUID and the assets; renaming to the same title changes nothing
    entra = (by_title(plan, "Entra ID") or {}).get("uuid")
    if not edit_ok(failures, eng, "rename-component", "--title", "Entra ID", "--new-title", "Microsoft Entra ID"):
        return
    plan = plan_of(eng)
    renamed = by_title(plan, "Microsoft Entra ID") or {}
    if renamed.get("uuid") != entra or points_at(asset_named(plan, "Entra tenant")) != [entra]:
        failures.append(f"{ssp}: rename changed the UUID or detached the assets")
    before = ssp.read_bytes()
    if edit_ok(failures, eng, "rename-component", "--title", "Microsoft Entra ID", "--new-title", "Microsoft Entra ID"):
        if ssp.read_bytes() != before:
            failures.append(f"{ssp}: renaming a component to its own title changed the record")
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after rename-component")

    # 10. split Windows 11 laptops into engineering and front-office components
    laptops = (by_title(plan, "Windows 11 laptops") or {}).get("uuid")
    if not edit_ok(failures, eng, "split-component", "--title", "Windows 11 laptops",
                   "--into", "Windows 11 laptops (engineering)", "--assets", "ENG-LT-01,ENG-LT-02",
                   "--category", "cui-asset"):
        return
    if not edit_ok(failures, eng, "split-component", "--title", "Windows 11 laptops",
                   "--into", "Windows 11 laptops (front office)", "--assets", "FO-LT-01",
                   "--category", "contractor-risk-managed-asset"):
        return
    plan = plan_of(eng)
    engineering = (by_title(plan, "Windows 11 laptops (engineering)") or {}).get("uuid")
    front = (by_title(plan, "Windows 11 laptops (front office)") or {}).get("uuid")
    if (not engineering or points_at(asset_named(plan, "ENG-LT-01")) != [engineering]
            or points_at(asset_named(plan, "ENG-LT-02")) != [engineering]):
        failures.append(f"{ssp}: split did not move ENG-LT-01 and ENG-LT-02 to the engineering component")
    if not front or points_at(asset_named(plan, "FO-LT-01")) != [front]:
        failures.append(f"{ssp}: split did not move FO-LT-01 to the front-office component")
    if by_title(plan, "Windows 11 laptops") is None or not laptops:
        failures.append(f"{ssp}: split removed the original component")
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after split-component")
    # a split provider stays a provider
    if edit_ok(failures, eng, "add-asset", "--name", "Acme RMM agent", "--component", "Acme MSP",
               "--category", "security-protection-asset"):
        if edit_ok(failures, eng, "split-component", "--title", "Acme MSP", "--into", "Acme MSP (RMM)",
                   "--assets", "Acme RMM agent"):
            if cmmc(by_title(plan_of(eng), "Acme MSP (RMM)") or {}, "provider-role") != "msp":
                failures.append(f"{ssp}: a component split out of a provider lost its provider-role")

    # 11. remove a component in use: refused, then allowed with somewhere to move the assets
    refused_unchanged(failures, eng, "still", "remove-component", "--title", "Windows 11 laptops (front office)")
    if not edit_ok(failures, eng, "add-component", "--title", "Kiosks", "--type", "hardware",
                   "--description", "Front desk kiosks."):
        return
    if not edit_ok(failures, eng, "remove-component", "--title", "Windows 11 laptops (front office)",
                   "--move-assets-to", "Kiosks"):
        return
    plan = plan_of(eng)
    kiosks = (by_title(plan, "Kiosks") or {}).get("uuid")
    if by_title(plan, "Windows 11 laptops (front office)") is not None or points_at(asset_named(plan, "FO-LT-01")) != [kiosks]:
        failures.append(f"{ssp}: remove-component with --move-assets-to did not move FO-LT-01 and remove the component")
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after remove-component")

    # 12. refusals, each leaving everything unchanged
    refused_unchanged(failures, eng, "cmmc-asset-category-values",
                      "add-asset", "--name", "ENG-LT-03", "--component", "Windows 11 laptops (engineering)",
                      "--category", "cui-asets")
    refused_unchanged(failures, eng, "contradicts",
                      "add-asset", "--name", "ENG-LT-04", "--component", "Windows 11 laptops (engineering)",
                      "--category", "contractor-risk-managed-asset")
    refused_unchanged(failures, eng, "contradicts",
                      "change-component", "--title", "Kiosks", "--category", "cui-asset")
    refused_unchanged(failures, eng, "justification",
                      "add-asset", "--name", "Lobby TV", "--component", "Guest Wi-Fi", "--category", "out-of-scope-asset")
    refused_unchanged(failures, eng, "fedramp",
                      "add-provider", "--title", "Box", "--role", "csp", "--description", "File sharing.")
    refused_unchanged(failures, eng, 'no component titled "No such thing"',
                      "add-asset", "--name", "X-1", "--component", "No such thing", "--category", "cui-asset")
    refused_unchanged(failures, eng, 'no asset named "No such asset"',
                      "remove-asset", "--name", "No such asset")

    # and change-asset, remove-asset work
    if edit_ok(failures, eng, "change-asset", "--name", "FO-LT-01", "--category", "out-of-scope-asset",
               "--remarks", "Kiosk image with no network access to CUI assets."):
        if cmmc(asset_named(plan_of(eng), "FO-LT-01") or {}, "asset-category") != "out-of-scope-asset":
            failures.append(f"{ssp}: change-asset did not change FO-LT-01's category")
    if edit_ok(failures, eng, "remove-asset", "--name", "Guest AP"):
        if asset_named(plan_of(eng), "Guest AP") is not None:
            failures.append(f"{ssp}: remove-asset left Guest AP in place")
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after change-asset and remove-asset")

    # 13. a provider keeps its leveraged authorization in step
    if edit_ok(failures, eng, "rename-component", "--title", "Microsoft 365 GCC High", "--new-title", "M365 GCC High"):
        plan = plan_of(eng)
        titles = [a.get("title") for a in plan["system-implementation"].get("leveraged-authorizations", [])]
        parties = [p.get("name") for p in plan["metadata"].get("parties", [])]
        if titles != ["M365 GCC High"] or parties != ["M365 GCC High"]:
            failures.append(f"{ssp}: renaming a provider left its leveraged authorization {titles} or party {parties}")
    proc = edit(eng, "remove-component", "--title", "M365 GCC High")
    if proc.returncode != 0 or "leveraged authorization" not in proc.stdout:
        failures.append(f"{EDIT} remove-component on an authorized CSP did not say it removed the leveraged authorization: {proc.stdout.strip()} {proc.stderr.strip()}")
    elif plan_of(eng)["system-implementation"].get("leveraged-authorizations"):
        failures.append(f"{ssp}: removing an authorized CSP left its leveraged authorization")
    if not edit_ok(failures, eng, "add-provider", "--title", "M365 GCC High", "--role", "csp", "--description",
                   "Email and files.", "--fedramp-status", "fedramp-moderate-authorized", "--date-authorized", "2020-01-15"):
        return
    if edit_ok(failures, eng, "change-provider", "--title", "M365 GCC High", "--fedramp-status", "none"):
        plan = plan_of(eng)
        if plan["system-implementation"].get("leveraged-authorizations") or plan["metadata"].get("parties"):
            failures.append(f"{ssp}: a provider no longer FedRAMP authorized still has a leveraged authorization")
    if "| VF-2 mill | Haas mills | OT |" not in view.read_text(encoding="utf-8"):
        failures.append(f"{view}: does not show the specialized asset's kind as OT")
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after the provider changes")


def objective_entries(plan: dict, objective_id: str) -> list[dict]:
    """The by-component entries recorded on one objective part of the catalog."""
    for req in plan["control-implementation"]["implemented-requirements"]:
        for statement in req.get("statements", []):
            if statement.get("statement-id") == objective_id:
                return statement.get("by-components", [])
    return []


def entry_for(plan: dict, objective_id: str, title: str) -> dict | None:
    component = by_title(plan, title) or {}
    return next((b for b in objective_entries(plan, objective_id) if b.get("component-uuid") == component.get("uuid")), None)


def state_of(entry: dict | None) -> str | None:
    return (entry or {}).get("implementation-status", {}).get("state")


def check_statements(failures: list[str], base: Path, fresh: Path) -> None:
    eng = base / "statements"
    shutil.copytree(fresh, eng)
    ssp = eng / "ssp" / "ssp.json"
    page = eng / "view" / "requirements" / "3.5.3.md"
    obj_a = "_03.05.03_obj.a"

    # 14. statements on 3.5.3[a] for two components
    steps = [
        ["add-component", "--title", "Entra ID", "--type", "service", "--description", "Identity provider."],
        ["add-component", "--title", "Mobile devices", "--type", "hardware", "--description", "Company phones."],
        ["set-statement", "--objective", "3.5.3[a]", "--component", "Entra ID", "--status", "implemented",
         "--statement", "Privileged accounts are the members of the Entra ID admin roles, reviewed monthly."],
        ["set-statement", "--objective", "3.5.3[a]", "--component", "Mobile devices", "--status", "not-applicable",
         "--statement", "No privileged account exists on the phones.",
         "--remarks", "Phones are enrolled as user devices; no local administrator account is available."],
    ]
    for step in steps:
        if not edit_ok(failures, eng, *step):
            return
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after set-statement")
    plan = plan_of(eng)
    entra = entry_for(plan, obj_a, "Entra ID")
    mobile = entry_for(plan, obj_a, "Mobile devices")
    if state_of(entra) != "implemented" or "admin roles" not in (entra or {}).get("description", ""):
        failures.append(f"{ssp}: 3.5.3[a] does not record Entra ID's statement as implemented: {entra}")
    if state_of(mobile) != "not-applicable" or "no local administrator" not in (mobile or {}).get(
            "implementation-status", {}).get("remarks", ""):
        failures.append(f"{ssp}: 3.5.3[a] does not record the mobile devices as not applicable with the reason: {mobile}")
    if entry_for(plan, obj_a, "This System") is not None:
        failures.append(f"{ssp}: 3.5.3[a] still carries the This System placeholder after statements were set")
    if state_of(entry_for(plan, "_03.05.03_obj.b", "This System")) != "planned":
        failures.append(f"{ssp}: 3.5.3[b] lost its planned placeholder when 3.5.3[a] was written")
    before = ssp.read_bytes()
    if edit_ok(failures, eng, *steps[2]) and ssp.read_bytes() != before:
        failures.append(f"{ssp}: setting the same statement again changed the record")

    # 15. the 3.5.3 view page
    text = page.read_text(encoding="utf-8") if page.is_file() else ""
    if not text.startswith(NOTICE_START):
        failures.append(f"{page}: missing, or does not open with the generated-file notice")
    for needle in ("# 3.5.3", "## 3.5.3[a]", "## 3.5.3[b]", "## 3.5.3[c]", "## 3.5.3[d]",
                   "privileged accounts are identified.", "| Entra ID | Implemented |", "admin roles",
                   "| Mobile devices | Not applicable |", "no local administrator account", "| This System | Planned |"):
        if needle not in text:
            failures.append(f"{page}: does not show {needle!r}")
    if "## 3.5.3[e]" in text or "_03." in text or "_obj" in text or "_smt" in text:
        failures.append(f"{page}: shows an OSCAL id or an objective that is not in the catalog")
    if not (eng / "view" / "requirements" / "3.1.1.md").is_file() or len(list((eng / "view" / "requirements").glob("*.md"))) != 110:
        failures.append(f"{page.parent}: expected one page per requirement, 110 in all")

    # 16. refusals, each leaving everything unchanged
    for status in ("not-applicable", "alternative"):
        refused_unchanged(failures, eng, "reason",
                          "set-statement", "--objective", "3.5.3[b]", "--component", "Mobile devices",
                          "--status", status, "--statement", "Handled elsewhere.")
    refused_unchanged(failures, eng, "not in the catalog",
                      "set-statement", "--objective", "3.5.3[e]", "--component", "Entra ID",
                      "--status", "implemented", "--statement", "Something.")
    refused_unchanged(failures, eng, "3.5.3[a]",
                      "set-statement", "--objective", "_03.05.03_obj.a", "--component", "Entra ID",
                      "--status", "implemented", "--statement", "Something.")
    refused_unchanged(failures, eng, "3.5.3[a]",
                      "set-statement", "--objective", "3.05.3[a]", "--component", "Entra ID",
                      "--status", "implemented", "--statement", "Something.")
    refused_unchanged(failures, eng, "says nothing",
                      "set-statement", "--objective", "3.5.3[b]", "--component", "Entra ID",
                      "--status", "planned", "--statement", "Not yet written.")
    refused_unchanged(failures, eng, 'no component titled "Okta"',
                      "set-statement", "--objective", "3.5.3[b]", "--component", "Okta",
                      "--status", "implemented", "--statement", "Something.")
    refused_unchanged(failures, eng, "still describe",
                      "remove-component", "--title", "Mobile devices")

    # 17. clearing returns the objective to planned for that component
    if edit_ok(failures, eng, "clear-statement", "--objective", "3.5.3[a]", "--component", "Entra ID"):
        entra = entry_for(plan_of(eng), obj_a, "Entra ID")
        if state_of(entra) != "planned":
            failures.append(f"{ssp}: clearing Entra ID's statement on 3.5.3[a] left it {state_of(entra)}")
        if "| Entra ID | Planned |" not in page.read_text(encoding="utf-8"):
            failures.append(f"{page}: does not show Entra ID as planned after clear-statement")
    if (edit_ok(failures, eng, "clear-statement", "--objective", "3.5.3[a]", "--component", "Mobile devices")
            and edit_ok(failures, eng, "remove-component", "--title", "Mobile devices")):
        plan = plan_of(eng)
        if [state_of(b) for b in objective_entries(plan, obj_a)] != ["planned"] or state_of(entry_for(plan, obj_a, "Entra ID")) != "planned":
            failures.append(f"{ssp}: 3.5.3[a] after removing the mobile devices is {objective_entries(plan, obj_a)}")
    if (edit_ok(failures, eng, "remove-component", "--title", "Entra ID")
            and state_of(entry_for(plan_of(eng), obj_a, "This System")) != "planned"):
        failures.append(f"{ssp}: 3.5.3[a] with no component left did not fall back to This System, planned")
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after clear-statement and remove-component")


def check_providers(failures: list[str], base: Path, fresh: Path) -> None:
    eng = base / "providers"
    shutil.copytree(fresh, eng)
    ssp = eng / "ssp" / "ssp.json"
    matrix = eng / "view" / "esp-responsibility-matrix.md"

    # 18. providers with remarks, and the matrix page
    steps = [
        ["add-provider", "--title", "Acme MSP", "--role", "msp", "--description", "Manages endpoints and patching.",
         "--remarks", "Account test: standing Global Administrator accounts. Holds: CUI reach."],
        ["add-provider", "--title", "Watchtower SOC", "--role", "soc", "--description", "Watches EDR alerts.",
         "--remarks", "Account test: no access. Holds: Security Protection Data only."],
        ["add-provider", "--title", "Microsoft 365 GCC High", "--role", "csp", "--description", "Email and files.",
         "--fedramp-status", "fedramp-moderate-authorized", "--date-authorized", "2020-01-15"],
        ["add-component", "--title", "Office desktops", "--type", "hardware", "--description", "Company desktops."],
        ["add-asset", "--name", "Acme RMM", "--component", "Acme MSP", "--category", "security-protection-asset",
         "--remarks", "Unattended remote control into every desktop."],
        ["add-asset", "--name", "DESK-01", "--component", "Office desktops", "--category", "cui-asset"],
    ]
    for step in steps:
        if not edit_ok(failures, eng, *step):
            return
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after providers with remarks")
    if "standing Global Administrator" not in (by_title(plan_of(eng), "Acme MSP") or {}).get("remarks", ""):
        failures.append(f"{ssp}: add-provider did not record Acme MSP's remarks")
    before = ssp.read_bytes()
    if edit_ok(failures, eng, *steps[0]) and ssp.read_bytes() != before:
        failures.append(f"{ssp}: adding the same provider with the same remarks again changed the record")
    refused_unchanged(failures, eng, "change-provider",
                      "add-provider", "--title", "Acme MSP", "--role", "msp",
                      "--description", "Manages endpoints and patching.", "--remarks", "Different.")
    if edit_ok(failures, eng, "change-provider", "--title", "Watchtower SOC",
               "--remarks", "Account test: no access. Holds: alerts and EDR telemetry only."):
        if "EDR telemetry" not in (by_title(plan_of(eng), "Watchtower SOC") or {}).get("remarks", ""):
            failures.append(f"{ssp}: change-provider did not replace Watchtower SOC's remarks")
    text = matrix.read_text(encoding="utf-8") if matrix.is_file() else ""
    if not text.startswith(NOTICE_START):
        failures.append(f"{matrix}: missing, or does not open with the generated-file notice")
    for needle in ("# ESP responsibility matrix", "## Providers",
                   "| Acme MSP | MSP | ESP | Not applicable |  | Manages endpoints and patching. | Account test: standing Global Administrator accounts. Holds: CUI reach. |",
                   "| Watchtower SOC | SOC provider | ESP |", "alerts and EDR telemetry only",
                   "| Microsoft 365 GCC High | CSP | CSP | FedRAMP Moderate authorized | 2020-01-15 |",
                   "## Provider assets",
                   "| Acme RMM | Acme MSP | Security Protection Asset | Unattended remote control into every desktop. |",
                   "## Per-requirement responsibility", "No conformity statement names a provider yet."):
        if needle not in text:
            failures.append(f"{matrix}: does not show {needle!r}")
    if "Office desktops" in text or "DESK-01" in text:
        failures.append(f"{matrix}: lists a component or asset that is not a provider's")

    # 19. a statement on a provider shows under its objective, beside the company's
    steps = [
        ["set-statement", "--objective", "3.7.5[a]", "--component", "Acme MSP", "--status", "implemented",
         "--statement", "Acme technicians sign in to the RMM with MFA before any remote session."],
        ["set-statement", "--objective", "3.7.5[a]", "--component", "Office desktops", "--status", "implemented",
         "--statement", "Desktops accept remote sessions only from the RMM agent."],
    ]
    for step in steps:
        if not edit_ok(failures, eng, *step):
            return
    text = matrix.read_text(encoding="utf-8")
    for needle in ("### 3.7.5[a]", "| Acme MSP | Provider's | Implemented | Acme technicians sign in to the RMM with MFA",
                   "| Office desktops | Company's | Implemented | Desktops accept remote sessions only"):
        if needle not in text:
            failures.append(f"{matrix}: does not show {needle!r}")
    if "No conformity statement names a provider yet." in text or "_03." in text or "_obj" in text:
        failures.append(f"{matrix}: still says no provider statement, or shows an OSCAL id")
    if "### 3.5.3[a]" in text:
        failures.append(f"{matrix}: shows an objective no provider has a statement on")

    # 20. render re-renders the view and leaves the record alone
    before = ssp.read_bytes()
    shutil.rmtree(eng / "view")
    if edit_ok(failures, eng, "render"):
        if ssp.read_bytes() != before:
            failures.append(f"{ssp}: render changed the record")
        rendered = [eng / "view" / "asset-inventory.md", matrix, eng / "view" / "requirements" / "3.7.5.md"]
        if not all(page.is_file() for page in rendered) or matrix.read_text(encoding="utf-8") != text:
            failures.append(f"{eng / 'view'}: render did not rebuild the view as it was")


def check_batch(failures: list[str], base: Path, fresh: Path) -> None:
    eng = base / "batch"
    shutil.copytree(fresh, eng)
    ssp = eng / "ssp" / "ssp.json"
    for step in (
        ["add-component", "--title", "Entra ID", "--type", "service", "--description", "Identity provider."],
        ["add-component", "--title", "Mobile devices", "--type", "hardware", "--description", "Company phones."],
    ):
        if not edit_ok(failures, eng, *step):
            return

    # 21. several statements, one validation
    good = [
        {"objective": "3.1.1[a]", "component": "Entra ID", "status": "implemented",
         "statement": "Authorized users are the members of the Saguaro Users group, approved in writing by the owner."},
        {"objective": "3.1.1[b]", "component": "Entra ID", "status": "partial",
         "statement": "Service accounts are listed in the account register; two have no recorded owner."},
        {"objective": "3.2.1[a]", "component": "Mobile devices", "status": "not-applicable",
         "statement": "Awareness training is for people, not phones.",
         "remarks": "A phone is a device; 3.2.1 is written for people."},
    ]
    batch = base / "batch-good.json"
    batch.write_text(json.dumps(good), encoding="utf-8")
    if not edit_ok(failures, eng, "set-statements", "--file", str(batch)):
        return
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after set-statements")
    plan = plan_of(eng)
    expected = [("_03.01.01_obj.a", "Entra ID", "implemented"), ("_03.01.01_obj.b", "Entra ID", "partial"),
                ("_03.02.01_obj.a", "Mobile devices", "not-applicable")]
    for objective, title, state in expected:
        if state_of(entry_for(plan, objective, title)) != state:
            failures.append(f"{ssp}: set-statements did not record {title} on {objective} as {state}")
    na = entry_for(plan, "_03.02.01_obj.a", "Mobile devices") or {}
    if not na.get("implementation-status", {}).get("remarks"):
        failures.append(f"{ssp}: set-statements dropped the not-applicable reason on 3.2.1[a]")
    page = eng / "view" / "requirements" / "3.1.1.md"
    if "Saguaro Users group" not in page.read_text(encoding="utf-8"):
        failures.append(f"{page}: does not show the statement set-statements recorded")
    before = ssp.read_bytes()
    if edit_ok(failures, eng, "set-statements", "--file", str(batch)) and ssp.read_bytes() != before:
        failures.append(f"{ssp}: the same set-statements file again changed the record")

    # 22. one bad entry records none of it
    bad = [
        {"objective": "3.1.2[a]", "component": "Entra ID", "status": "implemented", "statement": "Roles limit transactions."},
        {"objective": "3.5.3[e]", "component": "Entra ID", "status": "implemented", "statement": "Something."},
    ]
    bad_file = base / "batch-bad.json"
    bad_file.write_text(json.dumps(bad), encoding="utf-8")
    refused_unchanged(failures, eng, "entry 2 (3.5.3[e]", "set-statements", "--file", str(bad_file))
    not_list = base / "batch-not-list.json"
    not_list.write_text(json.dumps({"objective": "3.1.2[a]"}), encoding="utf-8")
    refused_unchanged(failures, eng, "list", "set-statements", "--file", str(not_list))
    missing = base / "batch-missing.json"
    missing.write_text(json.dumps([{"objective": "3.1.2[a]", "component": "Entra ID", "status": "implemented"}]),
                       encoding="utf-8")
    refused_unchanged(failures, eng, "statement", "set-statements", "--file", str(missing))

    # 23. remove-statement takes a component off an objective
    page = eng / "view" / "requirements" / "3.2.1.md"
    if edit_ok(failures, eng, "remove-statement", "--objective", "3.1.1[b]", "--component", "Entra ID"):
        if entry_for(plan_of(eng), "_03.01.01_obj.b", "Entra ID") is not None:
            failures.append(f"{ssp}: remove-statement left Entra ID on 3.1.1[b]")
        if state_of(entry_for(plan_of(eng), "_03.01.01_obj.b", "This System")) != "planned":
            failures.append(f"{ssp}: 3.1.1[b] with no component left did not fall back to This System, planned")
    if edit_ok(failures, eng, "remove-statement", "--objective", "3.2.1[a]", "--component", "Mobile devices"):
        if "Mobile devices" in page.read_text(encoding="utf-8"):
            failures.append(f"{page}: still lists Mobile devices after remove-statement")
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli after remove-statement")
    refused_unchanged(failures, eng, "no statement by component", "remove-statement",
                      "--objective", "3.1.1[a]", "--component", "Mobile devices")

    # 24. not applicable alone keeps the objective planned on This System
    obj = "_03.02.02_obj.a"
    if edit_ok(failures, eng, "set-statement", "--objective", "3.2.2[a]", "--component", "Mobile devices",
               "--status", "not-applicable", "--statement", "Phones take no training.",
               "--remarks", "3.2.2 is written for people."):
        if state_of(entry_for(plan_of(eng), obj, "This System")) != "planned":
            failures.append(f"{ssp}: 3.2.2[a] with only a not applicable statement lost its This System placeholder")
    if edit_ok(failures, eng, "set-statement", "--objective", "3.2.2[a]", "--component", "Entra ID",
               "--status", "planned", "--statement", "No role-based training is given."):
        if entry_for(plan_of(eng), obj, "This System") is not None:
            failures.append(f"{ssp}: 3.2.2[a] kept the This System placeholder after a planned statement")
    if edit_ok(failures, eng, "remove-statement", "--objective", "3.2.2[a]", "--component", "Entra ID"):
        if state_of(entry_for(plan_of(eng), obj, "This System")) != "planned":
            failures.append(f"{ssp}: 3.2.2[a] left with only not applicable did not get its placeholder back")
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli with not applicable beside the placeholder")


def show(failures: list[str], engagement: Path, *args: str) -> str:
    proc = edit(engagement, "show", *args)
    if proc.returncode != 0:
        failures.append(f"{EDIT} show {' '.join(args)}: exited {proc.returncode}: {proc.stderr.strip()}")
    return proc.stdout


def check_show(failures: list[str], base: Path, fresh: Path) -> None:
    eng = base / "show"
    shutil.copytree(fresh, eng)
    ssp = eng / "ssp" / "ssp.json"
    for step in (
        ["add-component", "--title", "Entra ID", "--type", "service", "--description", "Identity provider."],
        ["add-component", "--title", "Company laptops", "--type", "hardware", "--description", "Laptops.",
         "--category", "cui-asset"],
        ["add-asset", "--name", "ENG-LT-01", "--component", "Company laptops"],
        ["add-provider", "--title", "Acme MSP", "--role", "msp", "--description", "Manages endpoints.",
         "--remarks", "Standing admin accounts."],
        ["set-statement", "--objective", "3.5.3[a]", "--component", "Entra ID", "--status", "implemented",
         "--statement", "Privileged accounts are the members of the Entra ID admin roles."],
        ["set-statement", "--objective", "3.5.3[a]", "--component", "Company laptops", "--status", "not-applicable",
         "--statement", "No privileged account is used on a laptop.", "--remarks", "Local admin is disabled."],
    ):
        if not edit_ok(failures, eng, *step):
            return

    # 25. the record in domain terms, read only
    before = ssp.read_bytes()
    views = {p: p.read_bytes() for p in (eng / "view").rglob("*.md")}
    text = show(failures, eng, "--requirement", "3.5.3")
    for needle in ("| Entra ID | service |", "| Acme MSP | MSP |", "Standing admin accounts.",
                   "### CUI Asset", "| ENG-LT-01 | Company laptops |",
                   "## 3.5.3[a]", "## 3.5.3[d]", "| Entra ID | Implemented |", "admin roles",
                   "| Company laptops | Not applicable |", "Local admin is disabled.", "| This System | Planned |",
                   "No problems found in the record."):
        if needle not in text:
            failures.append(f"{EDIT} show --requirement 3.5.3: does not print {needle!r}")
    if "_03." in text or "_obj" in text or NOTICE_START in text or "## 3.1.1[a]" in text:
        failures.append(f"{EDIT} show --requirement 3.5.3: prints an OSCAL id, the view notice, or another requirement")
    family = show(failures, eng, "--requirement", "3.5")
    if not all(f"## 3.5.{n}[a]" in family for n in range(1, 12)) or "## 3.6.1[a]" in family:
        failures.append(f"{EDIT} show --requirement 3.5: does not print exactly the eleven 3.5 requirements")
    everything = show(failures, eng)
    if "## 3.1.1[a]" not in everything or "## 3.14.7[b]" not in everything:
        failures.append(f"{EDIT} show: with no requirement named, does not print every requirement")
    if ssp.read_bytes() != before or any(p.read_bytes() != b for p, b in views.items()):
        failures.append(f"{ssp}: show changed the record or the view")

    # 26. a hand-edited record: show names each problem
    broken = base / "show-broken"
    shutil.copytree(eng, broken)
    doc = json.loads((broken / "ssp" / "ssp.json").read_text(encoding="utf-8"))
    plan = doc["system-security-plan"]
    entra = by_title(plan, "Entra ID")
    laptops = by_title(plan, "Company laptops")
    for bc in objective_entries(plan, "_03.05.03_obj.a"):
        if bc["component-uuid"] == entra["uuid"]:
            bc["component-uuid"] = "00000000-0000-4000-8000-000000000000"
        if bc["component-uuid"] == laptops["uuid"]:
            bc["implementation-status"].pop("remarks", None)
    entra.setdefault("props", []).append(
        {"name": "asset-category", "ns": "https://poamslayer.github.io/ns/cmmc", "value": "spa"})
    item = asset_named(plan, "ENG-LT-01")
    for prop in item["props"]:
        if prop.get("name") == "asset-category":
            prop["value"] = "out-of-scope-asset"
    items = plan["system-implementation"]["inventory-items"]
    items.append({"uuid": "11111111-1111-4111-8111-111111111111", "description": "Stray tablet.",
                  "props": [{"name": "asset-id", "value": "TAB-01"},
                            {"name": "asset-category", "ns": "https://poamslayer.github.io/ns/cmmc", "value": "cui-asets"}],
                  "implemented-components": [{"component-uuid": "22222222-2222-4222-8222-222222222222"}]})
    (broken / "ssp" / "ssp.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")
    text = show(failures, broken, "--requirement", "3.5.3")
    for needle in ("3.5.3[a]: a statement is on a component the record does not have",
                   'asset "TAB-01" is an instance of a component the record does not have',
                   'asset "ENG-LT-01" is recorded as Out-of-Scope Asset, which contradicts component "Company laptops"',
                   'asset "ENG-LT-01" is an Out-of-Scope Asset with no justification',
                   'asset "TAB-01" has the category "cui-asets", which is not one of the five',
                   'component "Entra ID" has the category "spa", which is not one of the five',
                   '3.5.3[a]: the statement on "Company laptops" is not applicable with no reason'):
        if needle not in text:
            failures.append(f"{EDIT} show on a hand-edited record: does not report {needle!r}")
    if "No problems found" in text:
        failures.append(f"{EDIT} show on a hand-edited record: says it found no problems")

    # 27. refusals
    proc = edit(eng, "show", "--requirement", "3.99.1")
    if proc.returncode == 0 or "3.99.1" not in proc.stderr:
        failures.append(f"{EDIT} show --requirement 3.99.1: not refused with the requirement named: {proc.stderr.strip()}")
    proc = edit(base / "show-nothing", "show")
    if proc.returncode == 0 or "does not exist" not in proc.stderr:
        failures.append(f"{EDIT} show with no ssp.json: not refused: {proc.stderr.strip()}")


def main() -> int:
    failures: list[str] = []
    if shutil.which("oscal-cli") is None:
        failures.append("oscal-cli not found on PATH; install it with: bash scripts/install_oscal_cli.sh")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            check(failures, Path(tmp))
            if (Path(tmp) / "fresh" / "ssp" / "ssp.json").is_file():
                check_assets(failures, Path(tmp), Path(tmp) / "fresh")
                check_statements(failures, Path(tmp), Path(tmp) / "fresh")
                check_providers(failures, Path(tmp), Path(tmp) / "fresh")
                check_batch(failures, Path(tmp), Path(tmp) / "fresh")
                check_show(failures, Path(tmp), Path(tmp) / "fresh")
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"scribe: edit command checked in a scratch engagement, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
