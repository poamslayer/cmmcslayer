#!/usr/bin/env python3
"""One-off: convert an engagement's OSCAL ssp/ssp.json to the Markdown SSP (ADR-0012, #128).

Kept as the record of how the fixture's Markdown SSP was made; the reasoning is
in 2026-10-05-fixture-markdown-ssp-conversion.md beside it. It was run against
a cold-run copy, never against docs/fixture/engagement/ (AGENTS.md), and it is
not kept in scripts/: nothing else will ever need it.

    python3 docs/cold-runs/2026-10-05-fixture-markdown-ssp-conversion.py <skills repo> <engagement>

Reads ssp/ssp.json and writes ssp/system.md, ssp/components/<slug>.md, and the
110 ssp/<requirement>.md files with scribe's own writer, then removes
ssp/ssp.json and ssp/oscal/. It carries over, unchanged in meaning: the system
facts, every component (title, type, category, description, provider role and
FedRAMP status, leveraged authorization date, remarks), every asset (id,
category, kind, description; remarks, or the justification of an Out-of-Scope
Asset), and every statement by objective (component, status, text, remarks), in
the record's own order. UUIDs are dropped; a component is its title's slug.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

repo, engagement = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "skills" / "flows" / "scribe"))
import ssp_record as r  # noqa: E402

NS = "https://poamslayer.github.io/ns/cmmc"
IMPACT = {"fips-199-low": "low", "fips-199-moderate": "moderate", "fips-199-high": "high"}


def prop(obj: dict, name: str, ns: str | None = NS) -> str | None:
    return next((p["value"] for p in obj.get("props", []) if p["name"] == name and p.get("ns") == ns), None)


ssp_dir = engagement / "ssp"
plan = json.loads((ssp_dir / "ssp.json").read_text(encoding="utf-8"))["system-security-plan"]
chars, impl = plan["system-characteristics"], plan["system-implementation"]
requirements = r.load_requirements(repo / "reference" / "nist-800-171r2-requirements.json")

# The system.
system = {
    "system-name": chars["system-name"],
    "status": chars["status"]["state"],
    "information-types": [
        {
            "title": t["title"],
            "description": t["description"],
            "confidentiality": IMPACT[t["confidentiality-impact"]["base"]],
            "integrity": IMPACT[t["integrity-impact"]["base"]],
            "availability": IMPACT[t["availability-impact"]["base"]],
        }
        for t in chars["system-information"]["information-types"]
    ],
    "users": [{"title": u["title"]} for u in impl.get("users", [])],
}
boundary = chars["authorization-boundary"]["description"]
(ssp_dir / "system.md").write_text(r.record_text(system, f"# Authorization boundary\n\n{boundary}"), encoding="utf-8")

# Components, with their assets and provider fields.
authorizations = {a["uuid"]: a for a in impl.get("leveraged-authorizations", [])}
slugs: dict[str, str] = {}
(ssp_dir / "components").mkdir(exist_ok=True)
for c in impl["components"]:
    if c["type"] == "this-system":
        slugs[c["uuid"]] = r.PLACEHOLDER
        continue
    slug = r.slugify(c["title"])
    assert slug not in slugs.values(), f"two components share the slug {slug}"
    slugs[c["uuid"]] = slug
for c in impl["components"]:
    if c["type"] == "this-system":
        continue
    front: dict = {"title": c["title"], "type": c["type"]}
    if prop(c, "asset-category"):
        front["category"] = prop(c, "asset-category")
    if prop(c, "provider-role"):
        provider = {"role": prop(c, "provider-role")}
        if prop(c, "fedramp-status"):
            provider["fedramp-status"] = prop(c, "fedramp-status")
        authorization = authorizations.get(prop(c, "leveraged-authorization-uuid", ns=None) or "")
        if authorization:
            provider["date-authorized"] = authorization["date-authorized"]
        front["provider"] = provider
    if c.get("remarks"):
        front["remarks"] = c["remarks"]
    assets = []
    for item in impl.get("inventory-items", []):
        if [ic["component-uuid"] for ic in item["implemented-components"]] != [c["uuid"]]:
            continue
        asset = {"id": prop(item, "asset-id", ns=None), "category": prop(item, "asset-category")}
        if prop(item, "specialized-asset-type"):
            asset["kind"] = prop(item, "specialized-asset-type")
        if item.get("description") and item["description"] != asset["id"]:
            asset["description"] = item["description"]
        if item.get("remarks"):
            asset["justification" if asset["category"] == "out-of-scope-asset" else "remarks"] = item["remarks"]
        assets.append(asset)
    if assets:
        front["assets"] = assets
    (ssp_dir / "components" / f"{slugs[c['uuid']]}.md").write_text(r.record_text(front, c["description"]), encoding="utf-8")
placed = sum(len(i["implemented-components"]) == 1 for i in impl.get("inventory-items", []))
assert placed == len(impl.get("inventory-items", [])), "an asset is on more than one component"

# Statements by objective.
settled: list[str] = []
by_control = {req["control-id"]: req for req in plan["control-implementation"]["implemented-requirements"]}
for requirement in requirements:
    family, number, sub = (int(x) for x in requirement["id"].split("."))
    req = by_control[f"_{family:02d}.{number:02d}.{sub:02d}"]
    statements = {s["statement-id"].rsplit(".", 1)[1]: s for s in req.get("statements", [])}
    objectives = {}
    for objective in requirement["objectives"]:
        entries = []
        for bc in statements[objective["letter"]]["by-components"]:
            status = bc["implementation-status"]
            entry = {"component": slugs[bc["component-uuid"]], "status": status["state"], "statement": bc["description"]}
            if status.get("remarks"):
                entry["remarks"] = status["remarks"]
            entries.append(entry)
        # ADR-0011, which came after this record was converted (#100): an objective
        # whose statements are all not applicable stays planned on the placeholder.
        if all(e["status"] == "not-applicable" for e in entries if e["component"] != r.PLACEHOLDER) and not any(
            e["component"] == r.PLACEHOLDER for e in entries
        ):
            entries.insert(0, r.placeholder_statement())
            settled.append(f"{requirement['id']}[{objective['letter']}]")
        objectives[objective["letter"]] = entries
    front = {"requirement": requirement["id"], "family": requirement["family"], "objectives": objectives}
    (ssp_dir / f"{requirement['id']}.md").write_text(r.record_text(front, r.requirement_body(requirement)), encoding="utf-8")

(ssp_dir / "ssp.json").unlink()
shutil.rmtree(ssp_dir / "oscal", ignore_errors=True)
print(f"placeholder restored beside not applicable statements on: {', '.join(settled) or 'none'}")
print(f"converted {engagement}: {len(slugs) - 1} components, {len(impl.get('inventory-items', []))} assets, 110 requirement files")
