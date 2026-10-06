#!/usr/bin/env python3
"""Check an engagement's SSP, the ssp/ folder (ADR-0012), and say pass or fail.

Scribe runs this after every edit. If it fails, scribe restores the files with
git; if it passes, scribe renders the view. It prints one line per violation,
naming the file and, for a statement, the objective, and exits 1; or prints a
one-line summary and exits 0.

    python3 check_ssp.py                 # the engagement in the current directory
    python3 check_ssp.py path/to/engagement [--requirements FILE]

What it enforces:

- ssp/system.md is present, with the system's name, status, information types, and users;
- all 110 requirement files are present, each with every objective in the requirements reference and no other;
- every file's frontmatter parses, and holds only the keys the record defines;
- every status is one of the five; every category, kind, provider role, and FedRAMP status is one the glossary names;
- every statement names a component that has a file, or the placeholder, this-system;
- asset ids are unique across the SSP, and component titles are unique;
- an alternative or not applicable statement gives its reason in remarks;
- an Out-of-Scope Asset gives its justification, and a Specialized Asset its kind;
- an asset's category agrees with its component's, when the component gives one;
- a CSP records its FedRAMP status, and an authorized one its date authorized; no other provider does;
- the placeholder rule (ADR-0011): an objective is planned on this-system exactly while no component
  answers it with a status other than not applicable;
- no ssp.json or other OSCAL file is present.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ssp_record import (  # noqa: E402
    CATEGORIES,
    COMPONENT_TYPES,
    FEDRAMP_STATUSES,
    IMPACTS,
    NEEDS_REASON,
    PLACEHOLDER,
    PROVIDER_ROLES,
    REQUIREMENT_ID,
    SLUG,
    SPECIALIZED_KINDS,
    STATUSES,
    SYSTEM_STATUSES,
    UNWRITTEN,
    Record,
    default_requirements,
    is_unwritten,
    load,
    load_requirements,
)

SYSTEM_KEYS = {"system-name", "status", "information-types", "users"}
INFORMATION_TYPE_KEYS = {"title", "description", "confidentiality", "integrity", "availability"}
COMPONENT_KEYS = {"title", "type", "category", "provider", "remarks", "assets"}
PROVIDER_KEYS = {"role", "fedramp-status", "date-authorized"}
ASSET_KEYS = {"id", "category", "kind", "description", "justification", "remarks"}
REQUIREMENT_KEYS = {"requirement", "family", "objectives"}
STATEMENT_KEYS = {"component", "status", "statement", "remarks"}
DATE = re.compile(r"\d{4}-\d\d-\d\d")


def text(value) -> bool:
    """A non-empty piece of text."""
    return isinstance(value, str) and bool(value.strip())


def unknown_keys(data: dict, allowed: set[str]) -> list[str]:
    return [key for key in data if key not in allowed]


def check_system(record: Record, out: list[str]) -> None:
    where = "ssp/system.md"
    if not (record.engagement / where).is_file():
        out.append(f"{where}: missing; the SSP needs its system file")
        return
    system = record.system
    if system is None:
        return  # it did not parse, and load() said so
    for key in unknown_keys(system, SYSTEM_KEYS):
        out.append(f'{where}: "{key}" is not a field of the system file')
    if not text(system.get("system-name")):
        out.append(f"{where}: no system-name")
    if system.get("status") not in SYSTEM_STATUSES:
        out.append(f"{where}: status must be one of {', '.join(SYSTEM_STATUSES)}")
    types = system.get("information-types")
    if not isinstance(types, list) or not types:
        out.append(f"{where}: information-types must list at least one information type")
    else:
        for number, info in enumerate(types, start=1):
            if not isinstance(info, dict):
                out.append(f"{where}: information type {number} is not a mapping")
                continue
            for key in unknown_keys(info, INFORMATION_TYPE_KEYS):
                out.append(f'{where}: information type {number}: "{key}" is not a field of an information type')
            if not text(info.get("title")):
                out.append(f"{where}: information type {number} has no title")
            for impact in ("confidentiality", "integrity", "availability"):
                if info.get(impact) not in IMPACTS:
                    out.append(f"{where}: information type {number}: {impact} must be one of {', '.join(IMPACTS)}")
    users = system.get("users")
    if not isinstance(users, list) or not users or not all(isinstance(u, dict) and text(u.get("title")) for u in users):
        out.append(f"{where}: users must list at least one user, each with a title")


def check_provider(where: str, provider, out: list[str]) -> None:
    if not isinstance(provider, dict):
        out.append(f"{where}: provider must be a mapping with role, and for a CSP its fedramp-status")
        return
    for key in unknown_keys(provider, PROVIDER_KEYS):
        out.append(f'{where}: "{key}" is not a field of a provider')
    role = provider.get("role")
    status = provider.get("fedramp-status")
    date = provider.get("date-authorized")
    if role not in PROVIDER_ROLES:
        out.append(f'{where}: provider role "{role}" is not one of {", ".join(PROVIDER_ROLES)}')
    if role == "csp" and status is None:
        out.append(f"{where}: a CSP must record its fedramp-status")
    if role != "csp" and status is not None:
        out.append(f"{where}: only a CSP records a fedramp-status; FedRAMP does not apply to an ESP that is not a cloud provider")
    if status is not None and status not in FEDRAMP_STATUSES:
        out.append(f'{where}: fedramp-status "{status}" is not one of {", ".join(FEDRAMP_STATUSES)}')
    if status == "fedramp-moderate-authorized":
        if not (isinstance(date, str) and DATE.fullmatch(date)):
            out.append(f"{where}: a FedRAMP Moderate authorized CSP needs date-authorized (YYYY-MM-DD) from its FedRAMP Marketplace listing")
    elif date is not None:
        out.append(f"{where}: date-authorized is recorded only for a FedRAMP Moderate authorized CSP")


def check_components(record: Record, out: list[str]) -> None:
    titles: dict[str, str] = {}
    asset_ids: dict[str, str] = {}
    for slug, component in record.components.items():
        where = f"ssp/components/{slug}.md"
        data = component.data
        if slug == PLACEHOLDER:
            out.append(f"{where}: {PLACEHOLDER} is the placeholder and has no file")
        elif not SLUG.fullmatch(slug):
            out.append(f"{where}: a component's file name is its slug: lowercase letters, digits, and single hyphens")
        for key in unknown_keys(data, COMPONENT_KEYS):
            out.append(f'{where}: "{key}" is not a field of a component')
        title = data.get("title")
        if not text(title):
            out.append(f"{where}: no title")
        elif title in titles:
            out.append(f'{where}: the title "{title}" is also the title of ssp/components/{titles[title]}.md')
        else:
            titles[title] = slug
        if data.get("type") not in COMPONENT_TYPES:
            out.append(f'{where}: type "{data.get("type")}" is not one of {", ".join(COMPONENT_TYPES)}')
        if not component.description:
            out.append(f"{where}: no description; the body says what the component is")
        category = data.get("category")
        if category is not None and category not in CATEGORIES:
            out.append(f'{where}: category "{category}" is not one of the five CMMC asset categories')
        if "provider" in data:
            check_provider(where, data["provider"], out)
        if "remarks" in data and not isinstance(data["remarks"], str):
            out.append(f"{where}: remarks must be text")
        assets = data.get("assets", [])
        if assets is None:
            assets = []
        if not isinstance(assets, list):
            out.append(f"{where}: assets must be a list")
            continue
        for number, asset in enumerate(assets, start=1):
            check_asset(where, number, component, asset, asset_ids, out)


def check_asset(where: str, number: int, component, asset, asset_ids: dict[str, str], out: list[str]) -> None:
    if not isinstance(asset, dict):
        out.append(f"{where}: asset {number} is not a mapping")
        return
    name = asset.get("id")
    label = f'asset "{name}"' if text(name) else f"asset {number}"
    for key in unknown_keys(asset, ASSET_KEYS):
        out.append(f'{where}: {label}: "{key}" is not a field of an asset')
    if not text(name):
        out.append(f"{where}: asset {number} has no id")
    elif name in asset_ids:
        out.append(f'{where}: asset id "{name}" is also used in ssp/components/{asset_ids[name]}.md; asset ids are unique across the SSP')
    else:
        asset_ids[name] = component.slug
    own = asset.get("category")
    category = component.asset_category(asset)
    if category is None:
        out.append(f"{where}: {label} has no category, and its component gives none to take")
        return
    if category not in CATEGORIES:
        out.append(f'{where}: {label} has the category "{category}", which is not one of the five CMMC asset categories')
        return
    shared = component.data.get("category")
    if own is not None and shared is not None and own != shared:
        out.append(f"{where}: {label} is recorded as {CATEGORIES[own]}, which contradicts its component, "
                   f"recorded as {CATEGORIES.get(shared, shared)}; split the component or change one of them")
    kind = asset.get("kind")
    if category == "specialized-asset":
        if kind not in SPECIALIZED_KINDS:
            out.append(f"{where}: {label} is a Specialized Asset and must record its kind, one of {', '.join(SPECIALIZED_KINDS)}")
    elif kind is not None:
        out.append(f"{where}: {label} records a kind, which only a Specialized Asset has")
    if category == "out-of-scope-asset":
        if not text(asset.get("justification")):
            out.append(f"{where}: {label} is an Out-of-Scope Asset with no justification; say why it cannot process, store, or transmit CUI")
    elif "justification" in asset:
        out.append(f"{where}: {label} has a justification, which only an Out-of-Scope Asset gives; use remarks")


def check_requirements(record: Record, out: list[str]) -> None:
    for requirement in record.requirements:
        rid = requirement["id"]
        where = f"ssp/{rid}.md"
        path = record.engagement / where
        if not path.is_file():
            out.append(f"{where}: missing; the SSP holds one file for each of the 110 requirements")
            continue
        data = record.statements.get(rid)
        if data is None:
            continue  # it did not parse, and load() said so
        for key in unknown_keys(data, REQUIREMENT_KEYS):
            out.append(f'{where}: "{key}" is not a field of a requirement file')
        if data.get("requirement") != rid:
            out.append(f"{where}: requirement must be {rid}")
        if data.get("family") != requirement["family"]:
            out.append(f"{where}: family must be {requirement['family']}")
        objectives = data.get("objectives")
        if not isinstance(objectives, dict):
            out.append(f"{where}: objectives must map each objective letter to its statements")
            continue
        letters = [o["letter"] for o in requirement["objectives"]]
        for letter in objectives:
            if letter not in letters:
                out.append(f"{where}: {rid}[{letter}] is not an objective; {rid} has [{letters[0]}] to [{letters[-1]}]")
        for letter in letters:
            label = f"{rid}[{letter}]"
            if letter not in objectives:
                out.append(f"{where}: {label} is missing")
                continue
            check_objective(record, where, label, objectives[letter], out)


def check_objective(record: Record, where: str, label: str, entries, out: list[str]) -> None:
    if not isinstance(entries, list) or not entries:
        out.append(f"{where}: {label} has no statements; an objective no component answers is planned on {PLACEHOLDER}")
        return
    seen: set[str] = set()
    placeholder = False
    answered = False
    for entry in entries:
        if not isinstance(entry, dict):
            out.append(f"{where}: {label}: each statement is a mapping of component, status, statement, and remarks")
            continue
        component = entry.get("component")
        status = entry.get("status")
        statement = entry.get("statement")
        remarks = entry.get("remarks")
        for key in unknown_keys(entry, STATEMENT_KEYS):
            out.append(f'{where}: {label}: "{key}" is not a field of a statement')
        if not text(component):
            out.append(f"{where}: {label}: a statement names no component")
            continue
        if component in seen:
            out.append(f'{where}: {label}: component "{component}" has two statements; give it one')
        seen.add(component)
        if status not in STATUSES:
            out.append(f'{where}: {label}: the statement on "{component}" has the status "{status}", which is not one of {", ".join(STATUSES)}')
        if not text(statement):
            out.append(f'{where}: {label}: the statement on "{component}" says nothing')
        if remarks is not None and not isinstance(remarks, str):
            out.append(f'{where}: {label}: the remarks on "{component}" must be text')
        if component == PLACEHOLDER:
            placeholder = True
            if not is_unwritten(entry) or remarks:
                out.append(f'{where}: {label}: {PLACEHOLDER} is the placeholder; it is only ever planned, '
                           f'"{UNWRITTEN}", and a statement names the component that meets the objective')
            continue
        if component not in record.components:
            out.append(f'{where}: {label}: the statement names component "{component}", which has no file in ssp/components/')
        if statement == UNWRITTEN and status != "planned":
            out.append(f'{where}: {label}: the statement on "{component}" is {status} but says "{UNWRITTEN}"')
        if status in NEEDS_REASON and not text(remarks):
            out.append(f'{where}: {label}: the statement on "{component}" is {STATUSES[status].lower()} with no reason in remarks')
        if status in STATUSES and status != "not-applicable":
            answered = True
    if answered and placeholder:
        out.append(f"{where}: {label}: {PLACEHOLDER} is still planned beside a statement that answers the objective; remove it")
    if not answered and not placeholder:
        out.append(f"{where}: {label}: no component answers the objective, so it must stay planned on {PLACEHOLDER}")


def check_layout(record: Record, out: list[str]) -> None:
    ssp = record.engagement / "ssp"
    if not ssp.is_dir():
        return
    expected = {"system.md", *(f"{r['id']}.md" for r in record.requirements)}
    for path in sorted(ssp.rglob("*")):
        rel = path.relative_to(record.engagement)
        if path.suffix == ".json" or "oscal" in path.name.lower():
            out.append(f"{rel}: OSCAL is gone from the SSP (ADR-0012); remove it")
        elif path.is_file() and path.parent == ssp and path.name not in expected and not path.name.startswith("."):
            hint = "a requirement file is named by its id, such as 3.5.3.md" if REQUIREMENT_ID.fullmatch(path.stem) or path.stem.startswith("3.") else "the SSP holds system.md, components/, and the requirement files"
            out.append(f"{rel}: not part of the SSP; {hint}")
        elif path.is_file() and path.parent == ssp / "components" and path.suffix != ".md":
            out.append(f"{rel}: not part of the SSP; a component is a Markdown file")


def problems(engagement: Path, requirements: list[dict]) -> tuple[Record, list[str]]:
    """The record, and every violation in it, each in one line."""
    record = load(engagement, requirements)
    out = list(record.problems)
    if not (engagement / "ssp").is_dir():
        return record, [f"ssp/: missing; {engagement} holds no SSP"]
    check_system(record, out)
    check_components(record, out)
    check_requirements(record, out)
    check_layout(record, out)
    return record, out


def summary(record: Record) -> str:
    assets = sum(len(c.assets) for c in record.components.values())
    written = sum(
        1
        for data in record.statements.values()
        for entries in (data.get("objectives") or {}).values()
        for entry in (entries or [])
        if isinstance(entry, dict) and not is_unwritten(entry)
    )
    return f"{len(record.components)} components, {assets} assets, {written} written statements"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check an engagement's SSP, the ssp/ folder.")
    parser.add_argument("engagement", nargs="?", default=".", help="The engagement repo. Defaults to the current directory.")
    parser.add_argument("--requirements", type=Path, help="Alternate path to the requirements reference.")
    args = parser.parse_args(argv)
    try:
        requirements = load_requirements(args.requirements or default_requirements())
    except ValueError as error:
        print(f"check_ssp: {error}", file=sys.stderr)
        return 2
    engagement = Path(args.engagement).resolve()
    record, found = problems(engagement, requirements)
    if found:
        for line in found:
            print(line)
        print(f"check_ssp: FAIL, {len(found)} problems")
        return 1
    print(f"check_ssp: ok, {summary(record)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
