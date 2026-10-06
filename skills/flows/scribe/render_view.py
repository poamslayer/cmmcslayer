#!/usr/bin/env python3
"""Render the engagement's view/ from its SSP, the ssp/ folder (ADR-0012).

Scribe runs this after every change the check passes. It refuses a record
the check fails, so the view is never rendered from a bad record.

    python3 render_view.py                 # the engagement in the current directory
    python3 render_view.py path/to/engagement [--requirements FILE]

It writes, each page opening with the generated-file notice:

    view/asset-inventory.md            components, providers, and assets by category
    view/esp-responsibility-matrix.md  providers, their assets, and who implements what
    view/requirements/3.5.3.md         one page per requirement, statements by objective

Pages for requirements that are no longer in the record are removed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_ssp import problems  # noqa: E402
from ssp_record import (  # noqa: E402
    CATEGORIES,
    FEDRAMP_STATUSES,
    PLACEHOLDER,
    PROVIDER_ROLES,
    SPECIALIZED_KINDS,
    STATUSES,
    Component,
    Record,
    default_requirements,
    is_unwritten,
    load_requirements,
)

NOTICE = (
    "> **Generated file. Do not edit.** Rendered by scribe from the `ssp/` folder, "
    "which is the record. The next change to the SSP overwrites this file; "
    "to change what it says, record the change through scribe."
)


def cell(value) -> str:
    return re.sub(r"\s*\n\s*", " ", str(value or "")).replace("|", "\\|")


def provider_fields(component: Component) -> tuple[str, str, str]:
    """A provider's role, FedRAMP status, and date authorized, in the words the view uses."""
    provider = component.provider or {}
    role = provider.get("role") or ""
    status = FEDRAMP_STATUSES.get(provider.get("fedramp-status") or "", "Not applicable")
    return PROVIDER_ROLES.get(role, role), status, provider.get("date-authorized") or ""


def by_title(components) -> list[Component]:
    return sorted(components, key=lambda c: c.title.lower())


def render_asset_inventory(record: Record) -> str:
    components = by_title(record.components.values())
    lines = ["# Asset inventory", "", "## Components", ""]
    if components:
        lines += ["| Component | Type | Category | Description |", "|---|---|---|---|"]
        for c in components:
            category = CATEGORIES.get(c.data.get("category") or "", "")
            lines.append(f"| {cell(c.title)} | {cell(c.data.get('type'))} | {cell(category)} | {cell(c.description)} |")
    else:
        lines.append("No components recorded yet.")

    providers = [c for c in components if c.provider]
    lines += ["", "## Providers", ""]
    if providers:
        lines += ["| Provider | Role | FedRAMP status | Date authorized |", "|---|---|---|---|"]
        for c in providers:
            role, status, date = provider_fields(c)
            lines.append(f"| {cell(c.title)} | {cell(role)} | {cell(status)} | {cell(date)} |")
    else:
        lines.append("No providers recorded yet.")

    assets = [(asset, c) for c in record.components.values() for asset in c.assets]
    lines += ["", "## Assets by category", ""]
    if not assets:
        lines.append("No assets recorded yet.")
    for value, label in CATEGORIES.items():
        group = [(a, c) for a, c in assets if c.asset_category(a) == value]
        if not group:
            continue
        kind_column = value == "specialized-asset"
        out_of_scope = value == "out-of-scope-asset"
        columns = ["Asset", "Component"] + (["Kind"] if kind_column else []) + [
            "Description", "Justification" if out_of_scope else "Remarks"]
        lines += [f"### {label}", "", "| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
        for asset, c in sorted(group, key=lambda pair: str(pair[0].get("id") or "").lower()):
            row = [asset.get("id"), c.title]
            if kind_column:
                kind = asset.get("kind") or ""
                row.append(SPECIALIZED_KINDS.get(kind, kind))
            row += [asset.get("description") or asset.get("id"),
                    asset.get("justification") if out_of_scope else asset.get("remarks")]
            lines.append("| " + " | ".join(cell(v) for v in row) + " |")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def render_responsibility_matrix(record: Record) -> str:
    """Providers, their assets, and, per objective a provider speaks to, who implements what."""
    providers = by_title(c for c in record.components.values() if c.provider)
    provider_slugs = {c.slug for c in providers}

    lines = ["# ESP responsibility matrix", "", "## Providers", ""]
    if providers:
        lines += ["| Provider | Role | CSP or ESP | FedRAMP status | Date authorized | What it does | Remarks |",
                  "|---|---|---|---|---|---|---|"]
        for c in providers:
            role, status, date = provider_fields(c)
            kind = "CSP" if (c.provider or {}).get("role") == "csp" else "ESP"
            row = [c.title, role, kind, status, date, c.description, c.data.get("remarks")]
            lines.append("| " + " | ".join(cell(v) for v in row) + " |")
    else:
        lines.append("No providers recorded yet.")

    lines += ["", "## Provider assets", ""]
    items = [(asset, c) for c in providers for asset in c.assets]
    if items:
        lines += ["| Asset | Provider | Category | Remarks |", "|---|---|---|---|"]
        for asset, c in sorted(items, key=lambda pair: (pair[1].title.lower(), str(pair[0].get("id") or "").lower())):
            category = CATEGORIES.get(c.asset_category(asset) or "", "")
            lines.append("| " + " | ".join(cell(v) for v in (asset.get("id"), c.title, category, asset.get("remarks"))) + " |")
    else:
        lines.append("No provider assets recorded yet.")

    lines += ["", "## Per-requirement responsibility", "",
              "A statement on a provider's component says how that service meets the objective, including settings "
              "the company configures in it; the statement says who performs each part.", ""]
    shown = False
    for requirement in record.requirements:
        for objective in requirement["objectives"]:
            entries = [e for e in record.objective_entries(requirement["id"], objective["letter"]) if not is_unwritten(e)]
            if not any(e.get("component") in provider_slugs for e in entries):
                continue
            shown = True
            lines += [f"### {requirement['id']}[{objective['letter']}]", "",
                      "| Component | Whose component | Status | Statement |", "|---|---|---|---|"]
            for e in entries:
                status = e.get("status", "")
                side = "Provider's" if e.get("component") in provider_slugs else "Company's"
                lines.append("| " + " | ".join(cell(v) for v in (
                    record.title_of(e.get("component", "")), side, STATUSES.get(status, status), e.get("statement"))) + " |")
            lines.append("")
    if not shown:
        lines.append("No conformity statement names a provider yet.")
    return "\n".join(lines).rstrip("\n") + "\n"


def render_requirement(record: Record, requirement: dict) -> str:
    """One requirement's page: each objective in 3.5.3[a] form with its statements."""
    rid = requirement["id"]
    lines = [f"# {rid}", "", requirement["statement"], ""]
    for objective in requirement["objectives"]:
        lines += [f"## {rid}[{objective['letter']}]", "", objective["text"], ""]
        entries = record.objective_entries(rid, objective["letter"])
        if not entries:
            lines += ["No statement recorded.", ""]
            continue
        lines += ["| Component | Status | Statement | Remarks |", "|---|---|---|---|"]
        for e in entries:
            status = e.get("status", "")
            lines.append(
                f"| {cell(record.title_of(e.get('component', PLACEHOLDER)))} | {cell(STATUSES.get(status, status))} "
                f"| {cell(e.get('statement'))} | {cell(e.get('remarks'))} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def generated(page: str) -> str:
    return f"{NOTICE}\n\n{page}"


def render(record: Record) -> None:
    view = record.engagement / "view"
    pages = view / "requirements"
    pages.mkdir(parents=True, exist_ok=True)
    (view / "asset-inventory.md").write_text(generated(render_asset_inventory(record)), encoding="utf-8")
    (view / "esp-responsibility-matrix.md").write_text(generated(render_responsibility_matrix(record)), encoding="utf-8")
    wanted = set()
    for requirement in record.requirements:
        name = f"{requirement['id']}.md"
        wanted.add(name)
        (pages / name).write_text(generated(render_requirement(record, requirement)), encoding="utf-8")
    for page in pages.glob("*.md"):
        if page.name not in wanted:
            page.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render view/ from an engagement's SSP.")
    parser.add_argument("engagement", nargs="?", default=".", help="The engagement repo. Defaults to the current directory.")
    parser.add_argument("--requirements", type=Path, help="Alternate path to the requirements reference.")
    args = parser.parse_args(argv)
    try:
        requirements = load_requirements(args.requirements or default_requirements())
    except ValueError as error:
        print(f"render_view: {error}", file=sys.stderr)
        return 2
    engagement = Path(args.engagement).resolve()
    record, found = problems(engagement, requirements)
    if found:
        for line in found:
            print(line)
        print(f"render_view: refused; the SSP fails the check with {len(found)} problems, so the view was not rendered")
        return 1
    render(record)
    print(f"render_view: rendered {engagement / 'view'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
