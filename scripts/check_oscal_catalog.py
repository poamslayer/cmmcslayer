#!/usr/bin/env python3
"""Check the vendored OSCAL catalog and our profile against the requirements reference.

ADR-0009 adopts a pinned, patched, unofficial catalog. The pin and this check
are the guard on it: every requirement statement and every objective in
reference/oscal/nist-800-171r2-catalog.json must say what
reference/nist-800-171r2-requirements.json says, apart from the differences
listed in KNOWN_DIFFERENCES, each of which is recorded in
docs/research/oscal-rev2-catalog-candidates.md. A bad pin, a bad patch, or a
hand edit to either file fails here.

It also checks that our profile imports the vendored catalog and selects every
one of its 110 requirements, and nothing else.

    python3 scripts/check_oscal_catalog.py

Needs no Java; scripts/check_oscal_cli.py runs oscal-cli on the same files.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CATALOG = Path("reference/oscal/nist-800-171r2-catalog.json")
PROFILE = Path("reference/oscal/nist-800-171r2-profile.json")
REQUIREMENTS = Path("reference/nist-800-171r2-requirements.json")

# Where the catalog and the reference file disagree and neither is the
# catalog's defect. Keyed by (requirement, objective letter or "statement"),
# with the exact catalog text and the exact reference text, so a change on
# either side is caught. Source: docs/research/oscal-rev2-catalog-candidates.md,
# "Full sweep".
KNOWN_DIFFERENCES = {
    # NIST's CPRT export and NIST's CSV spell these two statements differently.
    ("3.3.2", "statement"): (
        "Ensure that the actions of individual system users can be uniquely traced to those users, "
        "so they can be held accountable for their actions.",
        "Ensure that the actions of individual system users can be uniquely traced to those users "
        "so they can be held accountable for their actions.",
    ),
    ("3.5.4", "statement"): (
        "Employ replay-resistant authentication mechanisms for network access to privileged and "
        "nonprivileged accounts.",
        "Employ replay-resistant authentication mechanisms for network access to privileged and "
        "non-privileged accounts.",
    ),
    # List artifacts in our own reference file; the catalog text is correct.
    ("3.5.8", "a"): (
        "the number of generations during which a password cannot be reused is specified.",
        "the number of generations during which a password cannot be reused is specified and",
    ),
    ("3.11.1", "b"): (
        "risk to organizational operations, organizational assets, and individuals resulting from "
        "the operation of an organizational system that processes, stores, or transmits CUI is "
        "assessed with the defined frequency.",
        "risk to organizational operations, organizational assets, and individuals resulting from "
        ":the operation of an organizational system that processes, stores, or transmits CUI is "
        "assessed with the defined frequency.",
    ),
}

# The reference file ends list items with "; :", "; and :", "; and", or ";".
LIST_TAIL = re.compile(r"\s*;(\s*and)?(\s*:)?$")


def normalize(text: str) -> str:
    """Compare text, not whitespace, list punctuation, or a final period."""
    text = re.sub(r"\s+", " ", text).strip()
    text = LIST_TAIL.sub("", text)
    return text.rstrip(".").strip()


def label(control: dict) -> str | None:
    for prop in control.get("props", []):
        if prop.get("name") == "label":
            return prop.get("value")
    return None


def check_catalog(failures: list[str]) -> list[str]:
    """Compare the catalog with the reference file. Returns the control ids."""
    try:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"{CATALOG}: cannot read it as JSON ({exc})")
        return []
    try:
        reference = {r["id"]: r for r in json.loads(REQUIREMENTS.read_text(encoding="utf-8"))}
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        failures.append(f"{REQUIREMENTS}: cannot read it as the requirements index ({exc})")
        return []

    control_ids: list[str] = []
    seen: set[str] = set()
    objective_count = 0
    used_differences: set[tuple[str, str]] = set()

    def compare(req: str, key: str, catalog_text: str, reference_text: str) -> None:
        if normalize(catalog_text) == normalize(reference_text):
            return
        known = KNOWN_DIFFERENCES.get((req, key))
        where = f"{req} {key}" if key == "statement" else f"{req}[{key}]"
        if known == (catalog_text, reference_text):
            used_differences.add((req, key))
            return
        failures.append(
            f"{CATALOG}: {where} text does not match {REQUIREMENTS}\n"
            f"       catalog:   {catalog_text!r}\n"
            f"       reference: {reference_text!r}"
        )

    for group in catalog.get("catalog", {}).get("groups", []):
        for control in group.get("controls", []):
            control_ids.append(control.get("id", ""))
            req = label(control)
            if req not in reference:
                failures.append(f"{CATALOG}: control {control.get('id')} has label {req!r}, not a requirement")
                continue
            seen.add(req)
            ref = reference[req]
            parts = control.get("parts", [])
            statements = [p for p in parts if p.get("name") == "statement"]
            if len(statements) != 1:
                failures.append(f"{CATALOG}: {req} has {len(statements)} statement parts, expected 1")
            else:
                compare(req, "statement", statements[0].get("prose", ""), ref["statement"])

            expected_id = "_" + ".".join(f"{int(n):02d}" for n in req.split("."))
            if control.get("id") != expected_id:
                failures.append(f"{CATALOG}: {req} has id {control.get('id')!r}, expected {expected_id!r}")

            objectives = {}
            for part in parts:
                if part.get("name") != "objective":
                    continue
                prefix = f"{expected_id}_obj."
                pid = part.get("id", "")
                if not pid.startswith(prefix):
                    failures.append(f"{CATALOG}: {req} objective id {pid!r} does not start with {prefix!r}")
                    continue
                objectives[pid[len(prefix):]] = part.get("prose", "")
            ref_objectives = {o["letter"]: o["text"] for o in ref["objectives"]}
            if set(objectives) != set(ref_objectives):
                failures.append(
                    f"{CATALOG}: {req} objectives are {sorted(objectives)}, the reference has {sorted(ref_objectives)}"
                )
            for letter in sorted(set(objectives) & set(ref_objectives)):
                compare(req, letter, objectives[letter], ref_objectives[letter])
            objective_count += len(objectives)

    missing = sorted(set(reference) - seen, key=lambda r: [int(n) for n in r.split(".")])
    if missing:
        failures.append(f"{CATALOG}: requirements missing from the catalog: {', '.join(missing)}")
    if len(control_ids) != 110 or objective_count != 320:
        failures.append(f"{CATALOG}: {len(control_ids)} requirements and {objective_count} objectives, expected 110 and 320")
    for req, key in sorted(set(KNOWN_DIFFERENCES) - used_differences):
        failures.append(
            f"{Path(__file__).name}: the known difference for {req} {key} no longer occurs; "
            "remove it from KNOWN_DIFFERENCES"
        )
    return control_ids


def check_profile(control_ids: list[str], failures: list[str]) -> None:
    """Our profile imports the vendored catalog and selects exactly its controls."""
    try:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))["profile"]
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        failures.append(f"{PROFILE}: cannot read it as an OSCAL profile ({exc})")
        return
    imports = profile.get("imports", [])
    if len(imports) != 1 or imports[0].get("href") != CATALOG.name:
        failures.append(f"{PROFILE}: must have one import, of {CATALOG.name}")
        return
    selected = [
        cid
        for block in imports[0].get("include-controls", [])
        for cid in block.get("with-ids", [])
    ]
    if imports[0].get("include-all") is not None:
        failures.append(f"{PROFILE}: selects with include-all; list the 110 ids in include-controls")
    duplicates = sorted({c for c in selected if selected.count(c) > 1})
    if duplicates:
        failures.append(f"{PROFILE}: selects these more than once: {', '.join(duplicates)}")
    absent = sorted(set(control_ids) - set(selected))
    extra = sorted(set(selected) - set(control_ids))
    if absent:
        failures.append(f"{PROFILE}: does not select {', '.join(absent)}")
    if extra:
        failures.append(f"{PROFILE}: selects ids not in the catalog: {', '.join(extra)}")


def main() -> int:
    failures: list[str] = []
    control_ids = check_catalog(failures)
    if control_ids:
        check_profile(control_ids, failures)
    for failure in failures:
        print(f"FAIL {failure}")
    print(
        f"oscal catalog: {len(control_ids)} requirements compared with the reference, "
        f"{len(KNOWN_DIFFERENCES)} known differences allowed, {len(failures)} failures"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
