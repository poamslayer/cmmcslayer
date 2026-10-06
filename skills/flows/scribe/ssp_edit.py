#!/usr/bin/env python3
"""The one command that changes an engagement's ssp.json (ADR-0007), and shows it.

The scribe skill calls this for every change. Each run applies one operation:

1. read the current ssp/ssp.json (or start from nothing, for create);
2. apply the change, keeping every existing UUID and minting a random v4 UUID
   only for an object that is new;
3. write the result to a temporary file beside ssp.json, so the relative
   profile href resolves the same way it will for the real file;
4. run oscal-cli on it with our constraints file;
5. replace ssp.json only if oscal-cli passes, then re-render the view.

On any failure it exits non-zero with a message naming the operation and the
reason, and leaves ssp.json and the view exactly as they were. Missing Java or
oscal-cli is a failure, never a skip: an unvalidated change must not land.

    python3 ssp_edit.py --engagement DIR create --system-name "Acme Machining"
    python3 ssp_edit.py --engagement DIR add-component --title "Entra ID" \\
        --type service --description "Identity provider for every user account."
    python3 ssp_edit.py --engagement DIR add-asset --name ENG-LT-01 \\
        --component "Windows 11 laptops" --category cui-asset
    python3 ssp_edit.py --engagement DIR set-statement --objective "3.5.3[a]" \\
        --component "Entra ID" --status implemented --statement "..."

Operations: create, add-component, change-component, rename-component,
split-component, remove-component, add-asset, change-asset, remove-asset,
add-provider, change-provider, set-statement, set-statements, clear-statement,
remove-statement, render, show. Run with --help for each one's options. set-statements applies a file
of statements as one change: validated once, and refused whole if any entry is.

show changes nothing: it prints the record in domain terms for the skills that
read the SSP, read from ssp.json at that moment, with any problem a hand edit
left in it named in the operator's words. It is how a skill reads the SSP
without reading OSCAL, and without reading the view, which can be stale.

The engagement layout it writes:

    ssp/ssp.json                          the record
    ssp/oscal/nist-800-171r2-profile.json the profile ssp.json imports, copied at create
    ssp/oscal/nist-800-171r2-catalog.json the catalog that profile imports
    view/asset-inventory.md               generated, read-only, for people
    view/esp-responsibility-matrix.md     generated: providers and what each implements
    view/requirements/3.5.3.md            one generated page per requirement
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

PINNED_OSCAL_CLI = "3.2.0"
OSCAL_VERSION = "1.1.2"
NS = "https://poamslayer.github.io/ns/cmmc"
PROFILE_NAME = "nist-800-171r2-profile.json"
CATALOG_NAME = "nist-800-171r2-catalog.json"
CONSTRAINTS_NAME = "cmmc-constraints.xml"
PROFILE_HREF = f"oscal/{PROFILE_NAME}"
INSTALL_HINT = "install it with: bash scripts/install_oscal_cli.sh in the skills repo"

NOTICE = (
    "> **Generated file. Do not edit.** Rendered by scribe from `ssp/ssp.json`, "
    "which is the record. The next change to the SSP overwrites this file; "
    "to change what it says, record the change through scribe."
)

# The five CMMC asset categories, in the order the view lists them (CONTEXT.md).
CATEGORY_LABELS = {
    "cui-asset": "CUI Asset",
    "security-protection-asset": "Security Protection Asset",
    "contractor-risk-managed-asset": "Contractor Risk Managed Asset",
    "specialized-asset": "Specialized Asset",
    "out-of-scope-asset": "Out-of-Scope Asset",
}

ANSI = re.compile(r"\x1b\[[0-9;]*m")
SCHEMA_NOISE = re.compile(r"\[#\] #:|subschema|schema violations found")


SPECIALIZED_KINDS = {
    "iot": "IoT",
    "iiot": "IIoT",
    "ot": "OT",
    "gfe": "Government furnished equipment",
    "restricted-information-system": "Restricted information system",
    "test-equipment": "Test equipment",
}

PROVIDER_ROLES = {
    "csp": "CSP",
    "msp": "MSP",
    "mssp": "MSSP",
    "soc": "SOC provider",
    "rmm": "RMM provider",
    "other-esp": "Other ESP",
}

# OSCAL's implementation-status states, in the words the view uses.
STATUS_LABELS = {
    "implemented": "Implemented",
    "partial": "Partial",
    "planned": "Planned",
    "alternative": "Alternative",
    "not-applicable": "Not applicable",
}
NEEDS_REASON = ("alternative", "not-applicable")

# A by-component entry the SSP carries only so an objective is never silent:
# planned, and nothing written yet. create puts one on "This System" for every
# objective; clear-statement leaves one on the component it clears.
UNWRITTEN = "Not yet written."

OBJECTIVE_FORM = re.compile(r"([1-9]\d*)\.([1-9]\d*)\.([1-9]\d*)\[([a-z])\]")

FEDRAMP_LABELS = {
    "fedramp-moderate-authorized": "FedRAMP Moderate authorized",
    "fedramp-moderate-equivalent": "FedRAMP Moderate equivalent",
    "none": "Neither",
}
# The fields of each entry in a set-statements file; remarks is optional.
STATEMENT_FIELDS = ("objective", "component", "status", "statement")


class Refused(Exception):
    """The operation cannot be applied; the message says why."""


def default_oscal_dir() -> Path:
    return Path(__file__).resolve().parents[3] / "reference" / "oscal"


def engagement_catalog(engagement: Path) -> Path:
    """The catalog copied into the engagement at create, which the record resolves against."""
    return engagement / "ssp" / "oscal" / CATALOG_NAME


def new_uuid() -> str:
    return str(uuid.uuid4())


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")



def objectives_by_requirement(catalog_path: Path) -> list[tuple[str, list[str]]]:
    """Every requirement id in the catalog with its objective ids, in catalog order."""
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))["catalog"]
    result = []
    for group in catalog.get("groups", []):
        for control in group.get("controls", []):
            objectives = [p["id"] for p in control.get("parts", []) if p.get("name") == "objective"]
            result.append((control["id"], objectives))
    return result


def placeholder_entry(component_uuid: str) -> dict:
    return {
        "uuid": new_uuid(),
        "component-uuid": component_uuid,
        "description": UNWRITTEN,
        "implementation-status": {"state": "planned"},
    }


def is_unwritten(entry: dict) -> bool:
    return entry.get("description") == UNWRITTEN and entry.get("implementation-status", {}).get("state") == "planned"


def skeleton(system_name: str, oscal_dir: Path) -> dict:
    """A valid SSP: the profile imported, every objective planned on This System."""
    this_system = new_uuid()
    requirements = []
    for control_id, objectives in objectives_by_requirement(oscal_dir / CATALOG_NAME):
        requirements.append(
            {
                "uuid": new_uuid(),
                "control-id": control_id,
                "statements": [
                    {
                        "uuid": new_uuid(),
                        "statement-id": objective,
                        "by-components": [
                            placeholder_entry(this_system)
                        ],
                    }
                    for objective in objectives
                ],
            }
        )
    return {
        "system-security-plan": {
            "uuid": new_uuid(),
            "metadata": {
                "title": f"{system_name} System Security Plan",
                "last-modified": now(),
                "version": "0.1.0",
                "oscal-version": OSCAL_VERSION,
            },
            "import-profile": {"href": PROFILE_HREF},
            "system-characteristics": {
                "system-ids": [{"id": new_uuid()}],
                "system-name": system_name,
                "description": f"The system that processes, stores, or transmits CUI for {system_name}.",
                "system-information": {
                    "information-types": [
                        {
                            "uuid": new_uuid(),
                            "title": "Controlled Unclassified Information",
                            "description": "CUI the organization receives or creates under its DoD contracts.",
                            "confidentiality-impact": {"base": "fips-199-moderate"},
                            "integrity-impact": {"base": "fips-199-moderate"},
                            "availability-impact": {"base": "fips-199-moderate"},
                        }
                    ]
                },
                "status": {"state": "under-development"},
                "authorization-boundary": {"description": "Not yet drawn; scoping records it."},
            },
            "system-implementation": {
                "users": [{"uuid": new_uuid(), "title": "System user"}],
                "components": [
                    {
                        "uuid": this_system,
                        "type": "this-system",
                        "title": "This System",
                        "description": "The system as a whole. A placeholder so the SSP is valid before scoping names any component.",
                        "status": {"state": "under-development"},
                    }
                ],
            },
            "control-implementation": {
                "description": "One implemented requirement per NIST SP 800-171 Rev 2 requirement, one statement per assessment objective (ADR-0008).",
                "implemented-requirements": requirements,
            },
        }
    }


def add_component(doc: dict, title: str, ctype: str, description: str, category: str | None) -> bool:
    """Add a component. Returns False when the same component is already there.

    A component is identified by its title. Asking again for one that exists
    with the same fields changes nothing and mints no UUID; asking with
    different fields is refused, because changing a component is its own
    operation.
    """
    components = doc["system-security-plan"]["system-implementation"].setdefault("components", [])
    wanted = {"type": ctype, "description": description, "category": category}
    for existing in components:
        if existing.get("title") != title:
            continue
        have = {
            "type": existing.get("type"),
            "description": existing.get("description"),
            "category": prop_value(existing, "asset-category"),
        }
        if have == wanted:
            return False
        differs = ", ".join(k for k in wanted if wanted[k] != have[k])
        raise Refused(f'a component titled "{title}" already exists with a different {differs}')
    component = {
        "uuid": new_uuid(),
        "type": ctype,
        "title": title,
        "description": description,
    }
    if category is not None:
        component["props"] = [{"name": "asset-category", "ns": NS, "value": category}]
    component["status"] = {"state": "operational"}
    components.append(component)
    return True


def prop_value(obj: dict, name: str, ns: str | None = NS) -> str | None:
    """One prop's value: ours by default, or OSCAL's own with ns=None."""
    for prop in obj.get("props", []):
        if prop.get("ns") == ns and prop.get("name") == name:
            return prop.get("value")
    return None


def set_prop(obj: dict, name: str, value: str | None, ns: str | None = NS) -> None:
    """Set one prop (ours by default, or OSCAL's own with ns=None), or remove it when value is None."""
    props = [p for p in obj.get("props", []) if not (p.get("name") == name and p.get("ns") == ns)]
    if value is not None:
        prop = {"name": name, "value": value}
        if ns is not None:
            prop["ns"] = ns
        props.append(prop)
    if props:
        obj["props"] = props
    else:
        obj.pop("props", None)


def system_implementation(doc: dict) -> dict:
    return doc["system-security-plan"]["system-implementation"]


def find_component(doc: dict, title: str) -> dict:
    for component in system_implementation(doc).get("components", []):
        if component.get("title") == title:
            return component
    raise Refused(f'no component titled "{title}" is recorded')


def asset_name(item: dict) -> str | None:
    return prop_value(item, "asset-id", ns=None)


def find_editable_component(doc: dict, title: str, verb: str) -> dict:
    component = find_component(doc, title)
    if component.get("type") == "this-system":
        raise Refused(f'"This System" is the placeholder the SSP needs; it cannot be {verb}')
    return component


def refuse_taken_title(doc: dict, title: str) -> None:
    if any(c.get("title") == title for c in system_implementation(doc).get("components", [])):
        raise Refused(f'a component titled "{title}" is already recorded')


def find_asset(doc: dict, name: str) -> dict:
    for item in system_implementation(doc).get("inventory-items", []):
        if asset_name(item) == name:
            return item
    raise Refused(f'no asset named "{name}" is recorded')


def assets_of(doc: dict, component_uuid: str) -> list[dict]:
    return [
        item
        for item in system_implementation(doc).get("inventory-items", [])
        if any(ic.get("component-uuid") == component_uuid for ic in item.get("implemented-components", []))
    ]


def implemented_requirements(doc: dict) -> list[dict]:
    return doc["system-security-plan"]["control-implementation"].get("implemented-requirements", [])


def statements_using(doc: dict, component_uuid: str) -> int:
    """How many written conformity statements describe the component. Unwritten placeholders do not count."""
    count = 0
    for req in implemented_requirements(doc):
        for bc in req.get("by-components", []):
            count += bc.get("component-uuid") == component_uuid and not is_unwritten(bc)
        for statement in req.get("statements", []):
            for bc in statement.get("by-components", []):
                count += bc.get("component-uuid") == component_uuid and not is_unwritten(bc)
    return count


def this_system(doc: dict) -> dict:
    return next(c for c in system_implementation(doc)["components"] if c.get("type") == "this-system")


def drop_unwritten(doc: dict, component_uuid: str) -> None:
    """Drop the component's placeholders. An objective no component answers falls back to This System, planned."""
    for req in implemented_requirements(doc):
        for statement in req.get("statements", []):
            entries = statement.get("by-components", [])
            kept = [bc for bc in entries if bc.get("component-uuid") != component_uuid]
            if len(kept) == len(entries):
                continue
            statement["by-components"] = kept
            settle_placeholder(doc, statement)


def category_conflicts(doc: dict) -> list[str]:
    """Each asset whose category contradicts its component's, in the words the operator uses.

    A component carries a category only as a shorthand for every asset behind
    it (CONTEXT.md, Component).
    """
    found = []
    for component in system_implementation(doc).get("components", []):
        category = prop_value(component, "asset-category")
        if category is None:
            continue
        for item in assets_of(doc, component["uuid"]):
            asset_category = prop_value(item, "asset-category")
            if asset_category not in CATEGORY_LABELS or category not in CATEGORY_LABELS:
                continue  # an unknown value is oscal-cli's to report, by name, through our constraints file
            if asset_category != category:
                found.append(
                    f'asset "{asset_name(item)}" is recorded as {CATEGORY_LABELS[asset_category]}, which contradicts '
                    f'component "{component.get("title")}", recorded as {CATEGORY_LABELS[category]}'
                )
    return found


def check_categories(doc: dict) -> None:
    """Refuse a record where a component's category contradicts one of its assets'. Called before every commit."""
    for conflict in category_conflicts(doc):
        raise Refused(f"{conflict}; split the component or change one of them")


def unjustified_assets(doc: dict) -> list[str]:
    """Each Out-of-Scope Asset with no justification, in the words the operator uses."""
    return [
        f'asset "{asset_name(item)}" is an Out-of-Scope Asset with no justification'
        for item in system_implementation(doc).get("inventory-items", [])
        if prop_value(item, "asset-category") == "out-of-scope-asset" and not (item.get("remarks") or "").strip()
    ]


def check_justifications(doc: dict) -> None:
    for missing in unjustified_assets(doc):
        raise Refused(f"{missing}; give --remarks saying why it cannot process, store, or transmit CUI")


def add_asset(doc: dict, args: argparse.Namespace) -> bool:
    name, component_title, category, kind, description, remarks = (
        args.name, args.component, args.category, args.specialized_type, args.description, args.remarks)
    component = find_component(doc, component_title)
    category = category or prop_value(component, "asset-category")
    if category is None:
        raise Refused(f'no category given, and component "{component_title}" has none to take; give --category')
    wanted = {"component": component["uuid"], "category": category, "kind": kind,
              "description": description or name, "remarks": remarks}
    for item in system_implementation(doc).get("inventory-items", []):
        if asset_name(item) != name:
            continue
        points = [ic["component-uuid"] for ic in item.get("implemented-components", [])]
        have = {"component": points[0] if points else None,
                "category": prop_value(item, "asset-category"), "kind": prop_value(item, "specialized-asset-type"),
                "description": item.get("description"), "remarks": item.get("remarks")}
        if have == wanted:
            return False
        raise Refused(f'an asset named "{name}" is already recorded differently; use change-asset')
    item = {"uuid": new_uuid(), "description": wanted["description"]}
    set_prop(item, "asset-id", name, ns=None)
    set_prop(item, "asset-category", category)
    set_prop(item, "specialized-asset-type", kind)
    item["implemented-components"] = [{"component-uuid": component["uuid"]}]
    if remarks:
        item["remarks"] = remarks
    system_implementation(doc).setdefault("inventory-items", []).append(item)
    return True


def change_asset(doc: dict, args: argparse.Namespace) -> None:
    item = find_asset(doc, args.name)
    if args.component:
        item["implemented-components"] = [{"component-uuid": find_component(doc, args.component)["uuid"]}]
    if args.category:
        set_prop(item, "asset-category", args.category)
        if args.category != "specialized-asset" and not args.specialized_type:
            set_prop(item, "specialized-asset-type", None)
    if args.specialized_type:
        set_prop(item, "specialized-asset-type", args.specialized_type)
    if args.description:
        item["description"] = args.description
    if args.remarks is not None:
        if args.remarks:
            item["remarks"] = args.remarks
        else:
            item.pop("remarks", None)
    if args.new_name and args.new_name != args.name:
        if any(asset_name(i) == args.new_name for i in system_implementation(doc).get("inventory-items", [])):
            raise Refused(f'an asset named "{args.new_name}" is already recorded')
        set_prop(item, "asset-id", args.new_name, ns=None)


def remove_asset(doc: dict, name: str) -> None:
    item = find_asset(doc, name)
    system_implementation(doc)["inventory-items"] = [i for i in system_implementation(doc)["inventory-items"] if i is not item]
    if not system_implementation(doc)["inventory-items"]:
        del system_implementation(doc)["inventory-items"]


def change_component(doc: dict, args: argparse.Namespace) -> None:
    component = find_editable_component(doc, args.title, "changed")
    if args.type:
        component["type"] = args.type
    if args.description:
        component["description"] = args.description
    if args.clear_category:
        set_prop(component, "asset-category", None)
    elif args.category:
        set_prop(component, "asset-category", args.category)


def rename_component(doc: dict, title: str, new_title: str) -> bool:
    component = find_editable_component(doc, title, "renamed")
    if new_title == title:
        return False
    refuse_taken_title(doc, new_title)
    component["title"] = new_title
    authorization = leveraged_authorization_of(doc, component)
    if authorization is not None:
        authorization["title"] = new_title
        for party in doc["system-security-plan"]["metadata"].get("parties", []):
            if party.get("uuid") == authorization.get("party-uuid"):
                party["name"] = new_title
    return True


def split_component(doc: dict, args: argparse.Namespace) -> None:
    source = find_component(doc, args.title)
    refuse_taken_title(doc, args.into)
    names = [n.strip() for n in args.assets.split(",") if n.strip()]
    if not names:
        raise Refused("name at least one asset to move with --assets")
    moving = []
    for name in names:
        item = find_asset(doc, name)
        if source["uuid"] not in [ic.get("component-uuid") for ic in item.get("implemented-components", [])]:
            raise Refused(f'asset "{name}" is not an instance of component "{args.title}"')
        moving.append(item)
    new = {
        "uuid": new_uuid(),
        "type": source["type"],
        "title": args.into,
        "description": args.description or source.get("description", args.into),
    }
    # The new component is the same kind of thing: a provider stays a provider,
    # sharing its leveraged authorization. Only the category is the caller's.
    kept = [dict(p) for p in source.get("props", []) if not (p.get("ns") == NS and p.get("name") == "asset-category")]
    if kept:
        new["props"] = kept
    set_prop(new, "asset-category", args.category)
    new["status"] = {"state": "operational"}
    components = system_implementation(doc)["components"]
    components.insert(components.index(source) + 1, new)
    for item in moving:
        item["implemented-components"] = [{"component-uuid": new["uuid"]}]


def remove_component(doc: dict, title: str, move_to: str | None) -> str:
    """Remove a component. Returns a note on anything else that went with it."""
    component = find_editable_component(doc, title, "removed")
    in_use = statements_using(doc, component["uuid"])
    if in_use:
        raise Refused(f'{in_use} conformity statements still describe component "{title}"; clear them first')
    items = assets_of(doc, component["uuid"])
    if items and not move_to:
        names = ", ".join(asset_name(i) or "" for i in items)
        raise Refused(f'assets still point at component "{title}" ({names}); give --move-assets-to')
    if items:
        target = find_component(doc, move_to)
        if target is component:
            raise Refused("--move-assets-to names the component being removed")
        for item in items:
            item["implemented-components"] = [
                {"component-uuid": target["uuid"]} if ic.get("component-uuid") == component["uuid"] else ic
                for ic in item["implemented-components"]
            ]
    authorization = leveraged_authorization_of(doc, component)
    drop_unwritten(doc, component["uuid"])
    system_implementation(doc)["components"] = [c for c in system_implementation(doc)["components"] if c is not component]
    if authorization is None:
        return ""
    if any(prop_value(c, "leveraged-authorization-uuid", ns=None) == authorization["uuid"]
           for c in system_implementation(doc)["components"]):
        return ""
    drop_leveraged_authorization(doc, authorization)
    return f'; its FedRAMP leveraged authorization "{authorization.get("title")}" was removed with it'


def leveraged_authorization_of(doc: dict, component: dict) -> dict | None:
    ref = prop_value(component, "leveraged-authorization-uuid", ns=None)
    for authorization in system_implementation(doc).get("leveraged-authorizations", []):
        if authorization.get("uuid") == ref:
            return authorization
    return None


def drop_leveraged_authorization(doc: dict, authorization: dict) -> None:
    system_implementation(doc)["leveraged-authorizations"] = [a for a in system_implementation(doc)["leveraged-authorizations"] if a is not authorization]
    if not system_implementation(doc)["leveraged-authorizations"]:
        del system_implementation(doc)["leveraged-authorizations"]
    metadata = doc["system-security-plan"]["metadata"]
    party = authorization.get("party-uuid")
    metadata["parties"] = [p for p in metadata.get("parties", []) if p.get("uuid") != party]
    if not metadata["parties"]:
        del metadata["parties"]


def apply_provider(doc: dict, component: dict, role: str, status: str | None, date_authorized: str | None) -> None:
    """Record role and FedRAMP status; an authorized CSP is a leveraged authorization."""
    if role == "csp" and status is None:
        raise Refused("a CSP must record its FedRAMP status; give --fedramp-status")
    if role != "csp" and status is not None:
        raise Refused("only a CSP records a FedRAMP status; FedRAMP does not apply to an ESP that is not a cloud provider")
    set_prop(component, "provider-role", role)
    set_prop(component, "fedramp-status", status)
    set_prop(component, "implementation-point", "external", ns=None)
    authorization = leveraged_authorization_of(doc, component)
    if status == "fedramp-moderate-authorized":
        if authorization is None:
            if not date_authorized:
                raise Refused("a FedRAMP Moderate authorized CSP needs --date-authorized (YYYY-MM-DD), from its FedRAMP Marketplace listing")
            party = {"uuid": new_uuid(), "type": "organization", "name": component["title"]}
            doc["system-security-plan"]["metadata"].setdefault("parties", []).append(party)
            authorization = {"uuid": new_uuid(), "title": component["title"], "party-uuid": party["uuid"],
                             "date-authorized": date_authorized}
            system_implementation(doc).setdefault("leveraged-authorizations", []).append(authorization)
        elif date_authorized:
            authorization["date-authorized"] = date_authorized
        set_prop(component, "leveraged-authorization-uuid", authorization["uuid"], ns=None)
    else:
        set_prop(component, "leveraged-authorization-uuid", None, ns=None)
        if authorization is not None and not any(
            prop_value(c, "leveraged-authorization-uuid", ns=None) == authorization["uuid"]
            for c in system_implementation(doc).get("components", [])
        ):
            drop_leveraged_authorization(doc, authorization)


def add_provider(doc: dict, args: argparse.Namespace) -> bool:
    for existing in system_implementation(doc).get("components", []):
        if existing.get("title") != args.title:
            continue
        auth = leveraged_authorization_of(doc, existing)
        have = (existing.get("type"), existing.get("description"), prop_value(existing, "provider-role"),
                prop_value(existing, "fedramp-status"), prop_value(existing, "asset-category"),
                auth.get("date-authorized") if auth else None, existing.get("remarks"))
        wanted = ("service", args.description, args.role, args.fedramp_status, args.category,
                  args.date_authorized if args.fedramp_status == "fedramp-moderate-authorized" else None,
                  args.remarks or None)
        if have == wanted:
            return False
        raise Refused(f'a component titled "{args.title}" is already recorded differently; use change-provider')
    component = {"uuid": new_uuid(), "type": "service", "title": args.title, "description": args.description}
    set_prop(component, "asset-category", args.category)
    component["status"] = {"state": "operational"}
    if args.remarks:
        component["remarks"] = args.remarks
    apply_provider(doc, component, args.role, args.fedramp_status, args.date_authorized)
    system_implementation(doc).setdefault("components", []).append(component)
    return True


def change_provider(doc: dict, args: argparse.Namespace) -> None:
    component = find_component(doc, args.title)
    role = args.role or prop_value(component, "provider-role")
    if role is None:
        raise Refused(f'component "{args.title}" is not recorded as a provider; give --role')
    status = args.fedramp_status or (prop_value(component, "fedramp-status") if role == "csp" else None)
    if args.description:
        component["description"] = args.description
    if args.remarks is not None:
        if args.remarks:
            component["remarks"] = args.remarks
        else:
            component.pop("remarks", None)
    apply_provider(doc, component, role, status, args.date_authorized)



def objective_id(objective: str, catalog: Path) -> str:
    """Translate 3.5.3[a] to the catalog's objective id, _03.05.03_obj.a, or refuse."""
    match = OBJECTIVE_FORM.fullmatch(objective)
    if not match:
        raise Refused(f'"{objective}" is not an objective; write it as the requirement and a bracketed letter, such as 3.5.3[a]')
    family, number, sub, letter = match.groups()
    requirement = f"_{int(family):02d}.{int(number):02d}.{int(sub):02d}"
    wanted = f"{requirement}_obj.{letter}"
    for control_id, objectives in objectives_by_requirement(catalog):
        if control_id != requirement:
            continue
        if wanted in objectives:
            return wanted
        letters = [o.rsplit(".", 1)[1] for o in objectives]
        raise Refused(f"objective {objective} is not in the catalog; {objective.split('[')[0]} has objectives [{letters[0]}] to [{letters[-1]}]")
    raise Refused(f"objective {objective} is not in the catalog; there is no requirement {objective.split('[')[0]}")


def objective_statement(doc: dict, objective_part: str) -> dict:
    """The statement for one objective part; create made one for every objective."""
    requirement = objective_part.split("_obj.")[0]
    for req in implemented_requirements(doc):
        if req.get("control-id") != requirement:
            continue
        for statement in req.get("statements", []):
            if statement.get("statement-id") == objective_part:
                return statement
        statement = {"uuid": new_uuid(), "statement-id": objective_part, "by-components": []}
        req.setdefault("statements", []).append(statement)
        return statement
    raise Refused(f"the SSP has no implemented requirement {requirement}; it was not created by scribe")


def find_describable_component(doc: dict, title: str) -> dict:
    component = find_component(doc, title)
    if component.get("type") == "this-system":
        raise Refused('"This System" is the placeholder the SSP needs; a statement names the component that meets the objective')
    return component


def set_statement(doc: dict, args: argparse.Namespace, catalog: Path) -> bool:
    if args.status not in STATUS_LABELS:
        raise Refused(f'"{args.status}" is not an implementation status; use one of {", ".join(STATUS_LABELS)}')
    remarks = (args.remarks or "").strip()
    if args.status in NEEDS_REASON and not remarks:
        raise Refused(needs_reason(args.status))
    text = args.statement.strip()
    if not text or text == UNWRITTEN:
        raise Refused("the statement says nothing; give --statement with how the component meets the objective")
    statement = objective_statement(doc, objective_id(args.objective, catalog))
    component = find_describable_component(doc, args.component)
    status = {"state": args.status}
    if remarks:
        status["remarks"] = remarks
    entries = statement.setdefault("by-components", [])
    existing = next((bc for bc in entries if bc.get("component-uuid") == component["uuid"]), None)
    if existing is None:
        existing = {"uuid": new_uuid(), "component-uuid": component["uuid"]}
        entries.append(existing)
    elif existing.get("description") == text and existing.get("implementation-status") == status:
        return False
    existing["description"] = text
    existing["implementation-status"] = status
    settle_placeholder(doc, statement)
    return True


def settle_placeholder(doc: dict, statement: dict) -> None:
    """Keep This System's planned placeholder exactly while no component answers the objective.

    A not applicable statement says the objective does not bear on that one
    component; it does not answer it for the system. So the placeholder stays
    while every statement is not applicable, and goes once any other status is
    recorded, so the record never reads as if a requirement applies nowhere.
    """
    placeholder = this_system(doc)["uuid"]
    others = [bc for bc in statement.get("by-components", []) if bc.get("component-uuid") != placeholder]
    answered = any(bc.get("implementation-status", {}).get("state") != "not-applicable" for bc in others)
    if answered:
        statement["by-components"] = others
    elif len(others) == len(statement.get("by-components", [])):
        statement["by-components"] = [placeholder_entry(placeholder), *others]


def read_statements(path: Path) -> list[argparse.Namespace]:
    """The statements in a set-statements file, each shaped like set-statement's arguments."""
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise Refused(f"cannot read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise Refused(f"{path} is not valid JSON: {error}") from error
    if not isinstance(entries, list) or not entries:
        raise Refused(f"{path} must hold a list of statements, each with {', '.join(STATEMENT_FIELDS)}, and remarks where the status needs a reason")
    statements = []
    for number, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise Refused(f"entry {number} is not a statement; each entry has {', '.join(STATEMENT_FIELDS)}")
        missing = [field for field in STATEMENT_FIELDS if not isinstance(entry.get(field), str)]
        if missing:
            raise Refused(f"entry {number} ({entry.get('objective', 'no objective')}) has no {', '.join(missing)}")
        remarks = entry.get("remarks")
        if remarks is not None and not isinstance(remarks, str):
            raise Refused(f"entry {number} ({entry['objective']}): remarks must be text")
        statements.append(argparse.Namespace(**{field: entry[field] for field in STATEMENT_FIELDS}, remarks=remarks))
    return statements


def set_statements(doc: dict, statements: list[argparse.Namespace], catalog: Path, changed: list[int]) -> bool:
    """Apply every statement to doc, noting in changed the entries that changed; refuse the whole file on the first one that fails."""
    for number, args in enumerate(statements, start=1):
        try:
            if set_statement(doc, args, catalog):
                changed.append(number)
        except Refused as error:
            raise Refused(f"entry {number} ({args.objective}, \"{args.component}\"): {error}; nothing in the file was recorded") from error
    return bool(changed)


def recorded_entry(doc: dict, args: argparse.Namespace, catalog: Path) -> tuple[dict, dict]:
    """The objective's statement and the named component's entry on it, or refuse."""
    statement = objective_statement(doc, objective_id(args.objective, catalog))
    component = find_describable_component(doc, args.component)
    for entry in statement.get("by-components", []):
        if entry.get("component-uuid") == component["uuid"]:
            return statement, entry
    raise Refused(f'no statement by component "{args.component}" is recorded on {args.objective}')


def clear_statement(doc: dict, args: argparse.Namespace, catalog: Path) -> bool:
    _, entry = recorded_entry(doc, args, catalog)
    if is_unwritten(entry):
        return False
    entry["description"] = UNWRITTEN
    entry["implementation-status"] = {"state": "planned"}
    return True


def remove_statement(doc: dict, args: argparse.Namespace, catalog: Path) -> None:
    """Take the component off the objective; an objective left with none is planned on This System."""
    statement, entry = recorded_entry(doc, args, catalog)
    statement["by-components"] = [bc for bc in statement["by-components"] if bc is not entry]
    settle_placeholder(doc, statement)


def needs_reason(state: str) -> str:
    return f"a statement that is {STATUS_LABELS[state].lower()} needs the reason; give --remarks"


def unreasoned_statements(doc: dict) -> list[tuple[dict, dict, dict]]:
    """Each (requirement, objective statement, entry) that is alternative or not applicable with no reason."""
    return [
        (req, statement, bc)
        for req in implemented_requirements(doc)
        for statement in req.get("statements", [])
        for bc in statement.get("by-components", [])
        if bc.get("implementation-status", {}).get("state") in NEEDS_REASON
        and not (bc["implementation-status"].get("remarks") or "").strip()
    ]


def check_reasons(doc: dict) -> None:
    for _, _, bc in unreasoned_statements(doc):
        raise Refused(needs_reason(bc["implementation-status"]["state"]))


def oscal_cli_problems(path: Path, constraints: Path) -> str | None:
    """None when oscal-cli passes the file, otherwise the reason it did not."""
    if shutil.which("java") is None:
        return f"java not found; oscal-cli {PINNED_OSCAL_CLI} needs Java 11 or later"
    if shutil.which("oscal-cli") is None:
        return f"oscal-cli not found on PATH; {INSTALL_HINT}"
    proc = subprocess.run(
        ["oscal-cli", "validate", "--no-color", str(path), "-c", str(constraints)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return None
    output = ANSI.sub("", proc.stdout + proc.stderr)
    lines = [ln for ln in output.splitlines() if not ln.startswith("Picked up JAVA_TOOL_OPTIONS")]
    kept = [ln for ln in lines if ("ERROR" in ln or "CRITICAL" in ln) and not SCHEMA_NOISE.search(ln)]
    detail = "\n".join(f"  {ln.strip()}" for ln in (kept or lines[-5:]))
    return f"oscal-cli rejected the result:\n{detail}"



def cell(text: str | None) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ")


MISSING_COMPONENT = "(a component the record does not have)"


def component_titles(doc: dict) -> dict[str, str]:
    return {c["uuid"]: c.get("title", "") for c in system_implementation(doc).get("components", [])}


def title_of(titles: dict[str, str], component_uuid: str | None) -> str:
    """A component's title, or a plain note that the record has no such component."""
    return titles.get(component_uuid, MISSING_COMPONENT)


def provider_fields(doc: dict, component: dict) -> tuple[str, str, str]:
    """A provider's role, FedRAMP status, and date authorized, in the words the view uses."""
    role = prop_value(component, "provider-role") or ""
    status = FEDRAMP_LABELS.get(prop_value(component, "fedramp-status") or "", "Not applicable")
    authorization = leveraged_authorization_of(doc, component)
    return PROVIDER_ROLES.get(role, role), status, (authorization or {}).get("date-authorized", "")


def render_asset_inventory(doc: dict) -> str:
    system = system_implementation(doc)
    components = [c for c in system.get("components", []) if c.get("type") != "this-system"]
    by_uuid = component_titles(doc)
    items = system.get("inventory-items", [])

    lines = ["# Asset inventory", "", "## Components", ""]
    if components:
        lines += ["| Component | Type | Category | Description |", "|---|---|---|---|"]
        for c in sorted(components, key=lambda c: c.get("title", "").lower()):
            category = CATEGORY_LABELS.get(prop_value(c, "asset-category") or "", "")
            lines.append(f"| {cell(c.get('title'))} | {cell(c.get('type'))} | {cell(category)} | {cell(c.get('description'))} |")
    else:
        lines.append("No components recorded yet.")

    providers = [c for c in components if prop_value(c, "provider-role")]
    lines += ["", "## Providers", ""]
    if providers:
        lines += ["| Provider | Role | FedRAMP status | Date authorized |", "|---|---|---|---|"]
        for c in sorted(providers, key=lambda c: c.get("title", "").lower()):
            role, status, date = provider_fields(doc, c)
            lines.append(f"| {cell(c.get('title'))} | {cell(role)} | {cell(status)} | {cell(date)} |")
    else:
        lines.append("No providers recorded yet.")

    lines += ["", "## Assets by category", ""]
    if not items:
        lines.append("No assets recorded yet.")
    for value, label in CATEGORY_LABELS.items():
        group = [i for i in items if prop_value(i, "asset-category") == value]
        if not group:
            continue
        kind_column = value == "specialized-asset"
        columns = ["Asset", "Component"] + (["Kind"] if kind_column else []) + [
            "Description",
            "Justification" if value == "out-of-scope-asset" else "Remarks",
        ]
        lines += [f"### {label}", "", "| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
        for item in sorted(group, key=lambda i: (asset_name(i) or "").lower()):
            names = ", ".join(title_of(by_uuid, ic.get("component-uuid")) for ic in item.get("implemented-components", []))
            row = [asset_name(item), names]
            if kind_column:
                kind = prop_value(item, "specialized-asset-type") or ""
                row.append(SPECIALIZED_KINDS.get(kind, kind))
            row += [item.get("description"), item.get("remarks")]
            lines.append("| " + " | ".join(cell(v) for v in row) + " |")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def objective_label(control: dict, part_id: str) -> str:
    """_03.07.05_obj.a in 3.7.5[a] form."""
    return f"{label_of(control)}[{part_id.rsplit('.', 1)[1]}]"


def render_responsibility_matrix(doc: dict, controls: dict[str, dict]) -> str:
    """Providers, their assets, and, per objective a provider speaks to, who implements what."""
    system = system_implementation(doc)
    providers = sorted((c for c in system.get("components", []) if prop_value(c, "provider-role")),
                       key=lambda c: c.get("title", "").lower())
    provider_uuids = {c["uuid"] for c in providers}
    titles = component_titles(doc)

    lines = ["# ESP responsibility matrix", "", "## Providers", ""]
    if providers:
        lines += ["| Provider | Role | CSP or ESP | FedRAMP status | Date authorized | What it does | Remarks |",
                  "|---|---|---|---|---|---|---|"]
        for c in providers:
            role, status, date = provider_fields(doc, c)
            kind = "CSP" if prop_value(c, "provider-role") == "csp" else "ESP"
            row = [c.get("title"), role, kind, status, date, c.get("description"), c.get("remarks")]
            lines.append("| " + " | ".join(cell(v) for v in row) + " |")
    else:
        lines.append("No providers recorded yet.")

    lines += ["", "## Provider assets", ""]
    items = [(i, ic.get("component-uuid")) for i in system.get("inventory-items", [])
             for ic in i.get("implemented-components", []) if ic.get("component-uuid") in provider_uuids]
    if items:
        lines += ["| Asset | Provider | Category | Remarks |", "|---|---|---|---|"]
        for item, owner in sorted(items, key=lambda pair: (titles.get(pair[1], "").lower(), (asset_name(pair[0]) or "").lower())):
            category = CATEGORY_LABELS.get(prop_value(item, "asset-category") or "", "")
            lines.append("| " + " | ".join(cell(v) for v in (asset_name(item), titles.get(owner), category, item.get("remarks"))) + " |")
    else:
        lines.append("No provider assets recorded yet.")

    lines += ["", "## Per-requirement responsibility", "",
              "A statement on a provider's component says how that service meets the objective, including settings "
              "the company configures in it; the statement says who performs each part.", ""]
    shown = False
    for req in implemented_requirements(doc):
        control = controls.get(req.get("control-id"))
        if control is None:
            continue
        for statement in req.get("statements", []):
            entries = [bc for bc in statement.get("by-components", []) if not is_unwritten(bc)]
            if not any(bc.get("component-uuid") in provider_uuids for bc in entries):
                continue
            shown = True
            lines += [f"### {objective_label(control, statement['statement-id'])}", "",
                      "| Component | Whose component | Status | Statement |", "|---|---|---|---|"]
            for bc in entries:
                state = bc.get("implementation-status", {}).get("state", "")
                side = "Provider's" if bc.get("component-uuid") in provider_uuids else "Company's"
                lines.append("| " + " | ".join(cell(v) for v in (
                    title_of(titles, bc.get("component-uuid")), side, STATUS_LABELS.get(state, state), bc.get("description"))) + " |")
            lines.append("")
    if not shown:
        lines.append("No conformity statement names a provider yet.")
    return "\n".join(lines).rstrip("\n") + "\n"


def catalog_controls(catalog: Path) -> dict[str, dict]:
    doc = json.loads(catalog.read_text(encoding="utf-8"))["catalog"]
    return {control["id"]: control for group in doc.get("groups", []) for control in group.get("controls", [])}


def label_of(control: dict) -> str:
    return prop_value(control, "label", ns=None) or control["id"]


def render_requirement(doc: dict, req: dict, control: dict) -> str:
    """One requirement's page: each objective in 3.5.3[a] form with its statements. No OSCAL ids."""
    titles = component_titles(doc)
    label = label_of(control)
    parts = control.get("parts", [])
    text = next((p.get("prose", "") for p in parts if p.get("name") == "statement"), control.get("title", ""))
    written = {s.get("statement-id"): s.get("by-components", []) for s in req.get("statements", [])}
    lines = [f"# {label}", "", text, ""]
    for part in parts:
        if part.get("name") != "objective":
            continue
        lines += [f"## {objective_label(control, part['id'])}", "", part.get("prose", ""), ""]
        entries = written.get(part["id"], [])
        if not entries:
            lines += ["No statement recorded.", ""]
            continue
        lines += ["| Component | Status | Statement | Remarks |", "|---|---|---|---|"]
        for bc in entries:
            status = bc.get("implementation-status", {})
            state = status.get("state", "")
            lines.append(
                f"| {cell(title_of(titles, bc.get('component-uuid')))} | {cell(STATUS_LABELS.get(state, state))} "
                f"| {cell(bc.get('description'))} | {cell(status.get('remarks'))} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def generated(page: str) -> str:
    """A view page opens with the notice that it is generated; show prints the same pages without it."""
    return f"{NOTICE}\n\n{page}"


def where_is(controls: dict[str, dict], req: dict, statement: dict) -> str:
    """An objective in 3.5.3[a] form, or its catalog id when the catalog does not have the requirement."""
    control = controls.get(req.get("control-id"))
    return objective_label(control, statement["statement-id"]) if control else statement.get("statement-id", "")


def record_problems(doc: dict, controls: dict[str, dict]) -> list[str]:
    """What scribe would refuse, or oscal-cli reject, in a record someone changed by hand, in operator words."""
    titles = component_titles(doc)
    problems = []
    for req in implemented_requirements(doc):
        for statement in req.get("statements", []):
            where = where_is(controls, req, statement)
            for bc in statement.get("by-components", []):
                if bc.get("component-uuid") not in titles:
                    text = (bc.get("description") or "").strip()
                    problems.append(f'{where}: a statement is on a component the record does not have; it reads "{text}"')
    for item in system_implementation(doc).get("inventory-items", []):
        name = asset_name(item)
        if any(ic.get("component-uuid") not in titles for ic in item.get("implemented-components", [])):
            problems.append(f'asset "{name}" is an instance of a component the record does not have')
        category = prop_value(item, "asset-category")
        if category is None:
            problems.append(f'asset "{name}" has no category')
        elif category not in CATEGORY_LABELS:
            problems.append(f'asset "{name}" has the category "{category}", which is not one of the five CMMC asset categories')
    for component in system_implementation(doc).get("components", []):
        category = prop_value(component, "asset-category")
        if category is not None and category not in CATEGORY_LABELS:
            problems.append(f'component "{component.get("title")}" has the category "{category}", '
                            "which is not one of the five CMMC asset categories")
    problems += category_conflicts(doc)
    problems += unjustified_assets(doc)
    for req, statement, bc in unreasoned_statements(doc):
        state = STATUS_LABELS[bc["implementation-status"]["state"]].lower()
        problems.append(f'{where_is(controls, req, statement)}: the statement on "{title_of(titles, bc.get("component-uuid"))}" '
                        f"is {state} with no reason")
    return problems


def render_view(engagement: Path, doc: dict) -> None:
    """Re-render the view. The record has already changed when this runs."""
    try:
        view = engagement / "view"
        view.mkdir(exist_ok=True)
        (view / "asset-inventory.md").write_text(generated(render_asset_inventory(doc)), encoding="utf-8")
        controls = catalog_controls(engagement_catalog(engagement))
        (view / "esp-responsibility-matrix.md").write_text(
            generated(render_responsibility_matrix(doc, controls)), encoding="utf-8")
        pages = view / "requirements"
        pages.mkdir(exist_ok=True)
        for req in implemented_requirements(doc):
            control = controls.get(req.get("control-id"))
            if control is not None:
                (pages / f"{label_of(control)}.md").write_text(
                    generated(render_requirement(doc, req, control)), encoding="utf-8")
    except (OSError, ValueError, KeyError) as error:
        raise Refused(f"the change was recorded in ssp.json, but the view could not be re-rendered: {error}") from error



def commit(engagement: Path, doc: dict, constraints: Path) -> None:
    """Validate doc beside ssp.json and replace ssp.json only if it passes."""
    ssp_dir = engagement / "ssp"
    fd, tmp_name = tempfile.mkstemp(prefix=".ssp-", suffix=".json", dir=ssp_dir)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(doc, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        problem = oscal_cli_problems(tmp, constraints)
        if problem:
            raise Refused(problem)
        os.replace(tmp, ssp_dir / "ssp.json")
    finally:
        tmp.unlink(missing_ok=True)


def load(ssp_path: Path) -> dict:
    if not ssp_path.is_file():
        raise Refused(f"{ssp_path} does not exist; run create first")
    try:
        return json.loads(ssp_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise Refused(f"{ssp_path} is not valid JSON: {error}") from error


def create(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    ssp_path = engagement / "ssp" / "ssp.json"
    if ssp_path.exists():
        raise Refused(f"{ssp_path} already exists; create never overwrites an SSP")
    profile_dir = engagement / "ssp" / "oscal"
    profile_dir.mkdir(parents=True, exist_ok=True)
    for name in (PROFILE_NAME, CATALOG_NAME):
        if not (profile_dir / name).exists():
            shutil.copyfile(oscal_dir / name, profile_dir / name)
    doc = skeleton(args.system_name, oscal_dir)
    commit(engagement, doc, constraints)
    render_view(engagement, doc)
    count = len(doc["system-security-plan"]["control-implementation"]["implemented-requirements"])
    return f"created {ssp_path} with {count} requirements"


def record_change(engagement: Path, constraints: Path, apply: Callable[[dict], bool | None]) -> bool:
    """Load the record, apply one change, check it, validate it, replace it, render the view.

    apply(doc) returns False when the change is already recorded, in which case
    nothing is written and no UUID is minted; any other return (True or None)
    means the document changed.
    """
    doc = load(engagement / "ssp" / "ssp.json")
    if apply(doc) is False:
        return False
    check_categories(doc)
    check_justifications(doc)
    check_reasons(doc)
    doc["system-security-plan"]["metadata"]["last-modified"] = now()
    commit(engagement, doc, constraints)
    render_view(engagement, doc)
    return True


def add_component_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    if not record_change(engagement, constraints, lambda d: add_component(d, args.title, args.type, args.description, args.category)):
        return f'component "{args.title}" is already recorded; nothing changed'
    return f'added component "{args.title}"'


def change_component_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    record_change(engagement, constraints, lambda d: change_component(d, args))
    return f'changed component "{args.title}"'


def rename_component_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    if not record_change(engagement, constraints, lambda d: rename_component(d, args.title, args.new_title)):
        return f'component "{args.title}" already has that title; nothing changed'
    return f'renamed component "{args.title}" to "{args.new_title}"; its UUID is unchanged'


def split_component_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    record_change(engagement, constraints, lambda d: split_component(d, args))
    return f'split "{args.into}" out of "{args.title}" with assets {args.assets}'


def remove_component_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    notes: list[str] = []
    record_change(engagement, constraints, lambda d: notes.append(remove_component(d, args.title, args.move_assets_to)))
    moved = f'; its assets moved to "{args.move_assets_to}"' if args.move_assets_to else ""
    moved += "".join(notes)
    return f'removed component "{args.title}"{moved}'


def add_asset_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    recorded = record_change(engagement, constraints, lambda d: add_asset(d, args))
    if not recorded:
        return f'asset "{args.name}" is already recorded; nothing changed'
    return f'added asset "{args.name}" to component "{args.component}"'


def change_asset_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    record_change(engagement, constraints, lambda d: change_asset(d, args))
    return f'changed asset "{args.name}"'


def remove_asset_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    record_change(engagement, constraints, lambda d: remove_asset(d, args.name))
    return f'removed asset "{args.name}"'


def add_provider_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    if not record_change(engagement, constraints, lambda d: add_provider(d, args)):
        return f'provider "{args.title}" is already recorded; nothing changed'
    return f'added provider "{args.title}"'


def change_provider_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    record_change(engagement, constraints, lambda d: change_provider(d, args))
    return f'changed provider "{args.title}"'


def set_statement_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    if not record_change(engagement, constraints, lambda d: set_statement(d, args, engagement_catalog(engagement))):
        return f'the statement by "{args.component}" on {args.objective} is already recorded; nothing changed'
    return f'recorded {args.objective} for component "{args.component}" as {STATUS_LABELS[args.status].lower()}'


def set_statements_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    statements = read_statements(Path(args.file))
    changed: list[int] = []
    if not record_change(engagement, constraints, lambda d: set_statements(d, statements, engagement_catalog(engagement), changed)):
        return f"all {len(statements)} statements in {args.file} are already recorded; nothing changed"
    unchanged = len(statements) - len(changed)
    already = f"; {unchanged} were already recorded" if unchanged else ""
    return f"recorded {len(changed)} statements from {args.file}{already}"


def clear_statement_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    if not record_change(engagement, constraints, lambda d: clear_statement(d, args, engagement_catalog(engagement))):
        return f'{args.objective} is already planned for component "{args.component}"; nothing changed'
    return f'cleared the statement by "{args.component}" on {args.objective}; it is planned again'


def remove_statement_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    record_change(engagement, constraints, lambda d: remove_statement(d, args, engagement_catalog(engagement)))
    return f'removed component "{args.component}" from {args.objective}; it no longer describes that objective'


def render_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    render_view(engagement, load(engagement / "ssp" / "ssp.json"))
    return f"re-rendered {engagement / 'view'} from ssp.json; the record is unchanged"


def selected_requirements(doc: dict, controls: dict[str, dict], asked: list[str] | None) -> list[tuple[dict, dict]]:
    """The requirements asked for, as 3.5.3 or a family such as 3.5; every requirement when none is named."""
    recorded = [(req, controls[req["control-id"]]) for req in implemented_requirements(doc) if req.get("control-id") in controls]
    if not asked:
        return recorded
    chosen = []
    for wanted in asked:
        matches = [pair for pair in recorded
                   if label_of(pair[1]) == wanted or label_of(pair[1]).startswith(f"{wanted}.")]
        if not matches:
            raise Refused(f"no requirement {wanted} is in the catalog; name one as 3.5.3 or a family as 3.5")
        chosen += [pair for pair in matches if pair not in chosen]
    return chosen


def show_op(args: argparse.Namespace, engagement: Path, oscal_dir: Path, constraints: Path) -> str:
    """Print the record in domain terms. Reads ssp.json now, so it is never stale; changes nothing."""
    doc = load(engagement / "ssp" / "ssp.json")
    controls = catalog_controls(engagement_catalog(engagement))
    chosen = selected_requirements(doc, controls, args.requirement)
    metadata = doc["system-security-plan"]["metadata"]
    problems = record_problems(doc, controls)
    lines = [f"# {metadata.get('title', 'System Security Plan')}", "",
             f"Read from `ssp/ssp.json`, last modified {metadata.get('last-modified', '')}. "
             "This is the record as it stands now.", "", "## Problems in the record", ""]
    lines += [f"- {problem}" for problem in problems] or ["No problems found in the record."]
    pages = [render_asset_inventory(doc), render_responsibility_matrix(doc, controls)]
    pages += [render_requirement(doc, req, control) for req, control in chosen]
    return "\n".join(lines) + "\n\n" + "\n".join(pages)


def run(args: argparse.Namespace) -> str:
    engagement = Path(args.engagement).resolve()
    oscal_dir = Path(args.oscal_dir).resolve() if args.oscal_dir else default_oscal_dir()
    constraints = oscal_dir / CONSTRAINTS_NAME
    if not constraints.is_file():
        raise Refused(f"constraints file not found at {constraints}; pass --oscal-dir with the skills repo's reference/oscal folder")
    return args.apply(args, engagement, oscal_dir, constraints)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply one change to an engagement's ssp.json, or show it.")
    parser.add_argument("--engagement", default=".", help="The engagement repo. Defaults to the current directory.")
    parser.add_argument("--oscal-dir", help="Alternate reference/oscal folder (profile, catalog, constraints).")
    ops = parser.add_subparsers(dest="operation", required=True)

    create_parser = ops.add_parser("create", help="Create the skeleton ssp.json. Never overwrites.")
    create_parser.add_argument("--system-name", required=True, help="The client or system name.")
    create_parser.set_defaults(apply=create, label=lambda a: "create")

    add = ops.add_parser("add-component", help="Add one component.")
    add.add_argument("--title", required=True, help='What people call it, such as "Entra ID".')
    add.add_argument("--type", required=True, help="OSCAL component type: service, software, hardware, policy, process-procedure, and so on.")
    add.add_argument("--description", required=True, help="One sentence on what it is and does.")
    add.add_argument("--category", help="CMMC asset category, only when every asset behind the component shares it.")
    add.set_defaults(apply=add_component_op, label=lambda a: f'add-component "{a.title}"')

    categories = list(CATEGORY_LABELS)
    kinds = list(SPECIALIZED_KINDS)

    cc = ops.add_parser("change-component", help="Change a component's type, description, or category.")
    cc.add_argument("--title", required=True)
    cc.add_argument("--type")
    cc.add_argument("--description")
    group = cc.add_mutually_exclusive_group()
    group.add_argument("--category", help="Set the category every asset behind the component shares.")
    group.add_argument("--clear-category", action="store_true", help="Drop the component's category shorthand.")
    cc.set_defaults(apply=change_component_op, label=lambda a: f'change-component "{a.title}"')

    rn = ops.add_parser("rename-component", help="Rename a component. Its UUID, assets, and statements stay attached.")
    rn.add_argument("--title", required=True)
    rn.add_argument("--new-title", required=True)
    rn.set_defaults(apply=rename_component_op, label=lambda a: f'rename-component "{a.title}"')

    sp = ops.add_parser("split-component", help="Split named assets out of a component into a new one.")
    sp.add_argument("--title", required=True, help="The component to split.")
    sp.add_argument("--into", required=True, help="Title of the new component.")
    sp.add_argument("--assets", required=True, help="Comma-separated asset names to move to the new component.")
    sp.add_argument("--description", help="Description of the new component. Defaults to the original's.")
    sp.add_argument("--category", help="Category for the new component, when every moved asset shares it.")
    sp.set_defaults(apply=split_component_op, label=lambda a: f'split-component "{a.title}"')

    rm = ops.add_parser("remove-component", help="Remove a component no statement describes.")
    rm.add_argument("--title", required=True)
    rm.add_argument("--move-assets-to", help="Component to move this component's assets to. Required if it has any.")
    rm.set_defaults(apply=remove_component_op, label=lambda a: f'remove-component "{a.title}"')

    aa = ops.add_parser("add-asset", help="Add one asset: an inventory row, an instance of one component.")
    aa.add_argument("--name", required=True, help='The asset\'s name or tag, such as "ENG-LT-01". Identifies it.')
    aa.add_argument("--component", required=True, help="Title of the component it is an instance of.")
    aa.add_argument("--category", help=f"One of {', '.join(categories)}. Defaults to the component's category.")
    aa.add_argument("--specialized-type", help=f"For a Specialized Asset: one of {', '.join(kinds)}.")
    aa.add_argument("--description", help="What it is. Defaults to the name.")
    aa.add_argument("--remarks", help="Required for an Out-of-Scope Asset: why it cannot process, store, or transmit CUI.")
    aa.set_defaults(apply=add_asset_op, label=lambda a: f'add-asset "{a.name}"')

    ca = ops.add_parser("change-asset", help="Change an asset's component, category, kind, description, or remarks.")
    ca.add_argument("--name", required=True)
    ca.add_argument("--new-name")
    ca.add_argument("--component")
    ca.add_argument("--category")
    ca.add_argument("--specialized-type")
    ca.add_argument("--description")
    ca.add_argument("--remarks", help='Replace the remarks; "" clears them.')
    ca.set_defaults(apply=change_asset_op, label=lambda a: f'change-asset "{a.name}"')

    ra = ops.add_parser("remove-asset", help="Remove one asset.")
    ra.add_argument("--name", required=True)
    ra.set_defaults(apply=remove_asset_op, label=lambda a: f'remove-asset "{a.name}"')

    roles = list(PROVIDER_ROLES)
    statuses = list(FEDRAMP_LABELS)
    ap = ops.add_parser("add-provider", help="Add an outside provider (ESP or CSP) as a service component.")
    ap.add_argument("--title", required=True, help='The provider and service, such as "Microsoft 365 GCC High".')
    ap.add_argument("--role", required=True, help=f"One of {', '.join(roles)}.")
    ap.add_argument("--description", required=True, help="What it does for the organization.")
    ap.add_argument("--fedramp-status", help=f"Required for a csp: one of {', '.join(statuses)}.")
    ap.add_argument("--date-authorized", help="YYYY-MM-DD. Required when --fedramp-status is fedramp-moderate-authorized.")
    ap.add_argument("--category", help="The provider's category when every asset behind it shares one.")
    ap.add_argument("--remarks", help="The access model and the data the provider holds or reaches.")
    ap.set_defaults(apply=add_provider_op, label=lambda a: f'add-provider "{a.title}"')

    cp = ops.add_parser("change-provider", help="Change a provider's role, FedRAMP status, date authorized, description, or remarks.")
    cp.add_argument("--title", required=True)
    cp.add_argument("--role")
    cp.add_argument("--fedramp-status")
    cp.add_argument("--date-authorized")
    cp.add_argument("--description")
    cp.add_argument("--remarks", help='Replace the remarks; "" clears them.')
    cp.set_defaults(apply=change_provider_op, label=lambda a: f'change-provider "{a.title}"')

    ss = ops.add_parser("set-statement", help="Set the conformity statement for one objective and one component.")
    ss.add_argument("--objective", required=True, help="The objective, written like 3.5.3[a].")
    ss.add_argument("--component", required=True, help="Title of the component the statement describes.")
    ss.add_argument("--status", required=True, help=f"One of {', '.join(STATUS_LABELS)}.")
    ss.add_argument("--statement", required=True, help="How the component meets the objective.")
    ss.add_argument("--remarks", help="The reason. Required for alternative and not-applicable.")
    ss.set_defaults(apply=set_statement_op, label=lambda a: f'set-statement {a.objective} "{a.component}"')

    sb = ops.add_parser(
        "set-statements",
        help="Set many conformity statements from a JSON file, validated once; one bad entry records none.",
    )
    sb.add_argument(
        "--file",
        required=True,
        help="A JSON list of statements, each with objective, component, status, statement, and remarks where needed.",
    )
    sb.set_defaults(apply=set_statements_op, label=lambda a: f"set-statements {a.file}")

    cs = ops.add_parser("clear-statement", help="Clear one component's statement on one objective; it becomes planned.")
    cs.add_argument("--objective", required=True, help="The objective, written like 3.5.3[a].")
    cs.add_argument("--component", required=True)
    cs.set_defaults(apply=clear_statement_op, label=lambda a: f'clear-statement {a.objective} "{a.component}"')

    rs = ops.add_parser(
        "remove-statement",
        help="Take a component off an objective it does not describe; unlike clear, it is not left planned.",
    )
    rs.add_argument("--objective", required=True, help="The objective, written like 3.5.3[a].")
    rs.add_argument("--component", required=True)
    rs.set_defaults(apply=remove_statement_op, label=lambda a: f'remove-statement {a.objective} "{a.component}"')

    rv = ops.add_parser("render", help="Re-render the view from ssp.json without changing the record.")
    rv.set_defaults(apply=render_op, label=lambda a: "render")

    sh = ops.add_parser("show", help="Print the record in domain terms, with any problems in it. Changes nothing.")
    sh.add_argument("--requirement", action="append",
                    help="A requirement, 3.5.3, or a family, 3.5. Repeat for more. Defaults to every requirement.")
    sh.set_defaults(apply=show_op, label=lambda a: "show", plain=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        message = run(args)
    except Refused as error:
        print(f"scribe: {args.label(args)} refused: {error}", file=sys.stderr)
        return 1
    print(message if getattr(args, "plain", False) else f"scribe: {message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
