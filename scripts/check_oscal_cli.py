#!/usr/bin/env python3
"""Run oscal-cli on the vendored catalog, our profile, and our constraints file.

ADR-0007 makes metaschema-framework oscal-cli the only OSCAL validator. This
check proves the files every engagement's ssp.json stands on are sound:

1. Java and the pinned oscal-cli are on PATH. Either missing is a failure,
   never a skip: an unvalidated OSCAL file must not look like a validated one.
2. The catalog and the profile pass `oscal-cli validate`.
3. The profile resolves against the catalog to exactly 110 requirements.
4. The constraints file loads and bites. A small SSP is written to a temporary
   folder, never to the repository: with valid values it must pass, and with
   one violation of every rule it must fail on each rule's id. oscal-cli calls
   its constraint validation experimental, so this is how we know it still
   enforces ours.

    python3 scripts/check_oscal_cli.py

Install oscal-cli with `bash scripts/install_oscal_cli.sh`.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

OSCAL_DIR = Path("reference/oscal")
CATALOG = OSCAL_DIR / "nist-800-171r2-catalog.json"
PROFILE = OSCAL_DIR / "nist-800-171r2-profile.json"
CONSTRAINTS = OSCAL_DIR / "cmmc-constraints.xml"

PINNED_VERSION = "3.2.0"
NS = "https://poamslayer.github.io/ns/cmmc"
INSTALL_HINT = "install it with: bash scripts/install_oscal_cli.sh"

# One entry per rule in the constraints file. The bad SSP breaks every one of
# them, and each id must appear in oscal-cli's output.
EXPECTED_RULES = (
    "cmmc-field-names",
    "cmmc-asset-category-placement",
    "cmmc-specialized-asset-type-placement",
    "cmmc-provider-role-placement",
    "cmmc-fedramp-status-placement",
    "cmmc-asset-category-values",
    "cmmc-asset-category-at-most-one",
    "cmmc-specialized-asset-type-values",
    "cmmc-specialized-asset-type-at-most-one",
    "cmmc-specialized-asset-type-needs-category",
    "cmmc-asset-category-required",
    "cmmc-specialized-asset-needs-type",
    "cmmc-provider-role-values",
    "cmmc-provider-role-at-most-one",
    "cmmc-fedramp-status-values",
    "cmmc-fedramp-status-at-most-one",
    "cmmc-fedramp-status-needs-csp",
    "cmmc-csp-needs-fedramp-status",
)

ANSI = re.compile(r"\x1b\[[0-9;]*m")


def oscal_cli(*args: str) -> tuple[int, str]:
    """Run oscal-cli and return its exit status and its output without color."""
    proc = subprocess.run(
        ["oscal-cli", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    output = ANSI.sub("", proc.stdout + proc.stderr)
    lines = [line for line in output.splitlines() if not line.startswith("Picked up JAVA_TOOL_OPTIONS")]
    return proc.returncode, "\n".join(lines)


SCHEMA_NOISE = re.compile(r"\[#\] #:|subschema|schema violations found")


def problems_in(output: str) -> str:
    """The ERROR and CRITICAL lines of an oscal-cli run, indented for a FAIL message.

    A schema failure also prints one line per OSCAL model the file is not
    (catalog, profile, SSP, ...), all at the document root; those are dropped
    so the line naming the actual path and problem is what the reader sees.
    """
    kept = [
        line
        for line in output.splitlines()
        if ("ERROR" in line or "CRITICAL" in line) and not SCHEMA_NOISE.search(line)
    ]
    return "\n".join(f"       {line}" for line in (kept or output.splitlines()[-5:]))


def check_tools(failures: list[str]) -> bool:
    """Java and the pinned oscal-cli are present. Returns False if not."""
    if shutil.which("java") is None:
        failures.append(f"java not found; oscal-cli {PINNED_VERSION} needs Java 11 or later")
        return False
    if shutil.which("oscal-cli") is None:
        failures.append(f"oscal-cli not found on PATH; {INSTALL_HINT}")
        return False
    status, output = oscal_cli("--version")
    match = re.search(r"oscal-cli\s+(\S+)", output)
    if status != 0 or not match:
        failures.append(f"oscal-cli --version failed:\n{problems_in(output)}")
        return False
    if match.group(1) != PINNED_VERSION:
        failures.append(f"oscal-cli is {match.group(1)}, the pin is {PINNED_VERSION}; {INSTALL_HINT}")
        return False
    return True


def check_validate(path: Path, failures: list[str]) -> None:
    status, output = oscal_cli("validate", "--no-color", str(path))
    if status != 0:
        failures.append(f"{path}: oscal-cli validate failed\n{problems_in(output)}")


def check_resolution(failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        resolved = Path(tmp) / "resolved.json"
        status, output = oscal_cli("resolve-profile", "--no-color", "--to=JSON", str(PROFILE), str(resolved))
        if status != 0 or not resolved.exists():
            failures.append(f"{PROFILE}: oscal-cli resolve-profile failed\n{problems_in(output)}")
            return
        catalog = json.loads(resolved.read_text(encoding="utf-8"))["catalog"]
        count = sum(len(g.get("controls", [])) for g in catalog.get("groups", []))
        count += len(catalog.get("controls", []))
        if count != 110:
            failures.append(f"{PROFILE}: resolves to {count} requirements, expected 110")


def prop(name: str, value: str) -> dict:
    return {"name": name, "ns": NS, "value": value}


def ssp(characteristics_props: list[dict], components: list[dict], items: list[dict]) -> dict:
    """A minimal SSP that passes the OSCAL schema, holding the given props."""
    this_system = str(uuid.uuid4())
    characteristics = {
        "system-ids": [{"id": "constraints-self-test"}],
        "system-name": "Constraints self-test",
        "description": "Written by scripts/check_oscal_cli.py into a temporary folder.",
        "system-information": {
            "information-types": [
                {
                    "uuid": str(uuid.uuid4()),
                    "title": "CUI",
                    "description": "Controlled Unclassified Information.",
                    "confidentiality-impact": {"base": "fips-199-moderate"},
                    "integrity-impact": {"base": "fips-199-moderate"},
                    "availability-impact": {"base": "fips-199-moderate"},
                }
            ]
        },
        "status": {"state": "operational"},
        "authorization-boundary": {"description": "The self-test system."},
    }
    if characteristics_props:
        characteristics["props"] = characteristics_props
    all_components = [
        {
            "uuid": this_system,
            "type": "this-system",
            "title": "This System",
            "description": "The system as a whole.",
            "status": {"state": "operational"},
        }
    ]
    for i, props in enumerate(components):
        component = {
            "uuid": str(uuid.uuid4()),
            "type": "service",
            "title": f"Component {i}",
            "description": "A component.",
            "status": {"state": "operational"},
        }
        if props:
            component["props"] = props
        all_components.append(component)
    inventory = []
    for props in items:
        item = {
            "uuid": str(uuid.uuid4()),
            "description": "An asset.",
            "implemented-components": [{"component-uuid": this_system}],
        }
        if props:
            item["props"] = props
        inventory.append(item)
    return {
        "system-security-plan": {
            "uuid": str(uuid.uuid4()),
            "metadata": {
                "title": "Constraints self-test",
                "last-modified": "2026-09-28T00:00:00Z",
                "version": "1",
                "oscal-version": "1.1.2",
            },
            "import-profile": {"href": PROFILE.resolve().as_uri()},
            "system-characteristics": characteristics,
            "system-implementation": {
                "users": [{"uuid": str(uuid.uuid4()), "title": "User"}],
                "components": all_components,
                "inventory-items": inventory,
            },
            "control-implementation": {
                "description": "Self-test.",
                "implemented-requirements": [
                    {
                        "uuid": str(uuid.uuid4()),
                        "control-id": "_03.05.03",
                        "statements": [
                            {
                                "uuid": str(uuid.uuid4()),
                                "statement-id": "_03.05.03_obj.a",
                                "by-components": [
                                    {
                                        "uuid": str(uuid.uuid4()),
                                        "component-uuid": this_system,
                                        "description": "Planned.",
                                        "implementation-status": {"state": "planned"},
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
        }
    }


GOOD = ssp(
    [],
    [
        [prop("asset-category", "security-protection-asset")],
        [prop("provider-role", "csp"), prop("fedramp-status", "fedramp-moderate-authorized")],
        [prop("provider-role", "msp")],
        [prop("asset-category", "specialized-asset"), prop("specialized-asset-type", "ot")],
    ],
    [
        [prop("asset-category", "cui-asset")],
        [prop("asset-category", "contractor-risk-managed-asset")],
        [prop("asset-category", "out-of-scope-asset")],
        [prop("asset-category", "specialized-asset"), prop("specialized-asset-type", "test-equipment")],
    ],
)

BAD = ssp(
    # Placement: all four fields where none may appear.
    [
        prop("asset-category", "cui-asset"),
        prop("specialized-asset-type", "ot"),
        prop("provider-role", "msp"),
        prop("fedramp-status", "none"),
    ],
    [
        [prop("asset-cateogry", "cui-asset")],  # cmmc-field-names
        [prop("provider-role", "cloud")],  # cmmc-provider-role-values
        [prop("provider-role", "msp"), prop("provider-role", "soc")],  # cmmc-provider-role-at-most-one
        [prop("provider-role", "csp"), prop("fedramp-status", "high")],  # cmmc-fedramp-status-values
        [  # cmmc-fedramp-status-at-most-one
            prop("provider-role", "csp"),
            prop("fedramp-status", "none"),
            prop("fedramp-status", "fedramp-moderate-authorized"),
        ],
        [prop("provider-role", "msp"), prop("fedramp-status", "none")],  # cmmc-fedramp-status-needs-csp
        [prop("provider-role", "csp")],  # cmmc-csp-needs-fedramp-status
    ],
    [
        [prop("asset-category", "cui-asets")],  # cmmc-asset-category-values
        [prop("asset-category", "cui-asset"), prop("asset-category", "out-of-scope-asset")],  # at-most-one
        [prop("asset-category", "specialized-asset"), prop("specialized-asset-type", "drone")],  # values
        [  # cmmc-specialized-asset-type-at-most-one
            prop("asset-category", "specialized-asset"),
            prop("specialized-asset-type", "ot"),
            prop("specialized-asset-type", "iot"),
        ],
        [prop("asset-category", "cui-asset"), prop("specialized-asset-type", "ot")],  # needs-category
        [],  # cmmc-asset-category-required
        [prop("asset-category", "specialized-asset")],  # cmmc-specialized-asset-needs-type
    ],
)


def check_constraints(failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        good = Path(tmp) / "good-ssp.json"
        bad = Path(tmp) / "bad-ssp.json"
        good.write_text(json.dumps(GOOD, indent=1), encoding="utf-8")
        bad.write_text(json.dumps(BAD, indent=1), encoding="utf-8")

        status, output = oscal_cli("validate", "--no-color", str(good), "-c", str(CONSTRAINTS))
        if status != 0:
            failures.append(
                f"{CONSTRAINTS}: an SSP using only allowed values failed validation\n{problems_in(output)}"
            )
            return

        status, output = oscal_cli("validate", "--no-color", str(bad), "-c", str(CONSTRAINTS))
        if status == 0:
            failures.append(f"{CONSTRAINTS}: an SSP breaking every rule passed validation")
            return
        schema_errors = [line for line in output.splitlines() if "CRITICAL" in line]
        if schema_errors:
            failures.append(
                f"{Path(__file__).name}: the self-test SSP is not schema-valid, so it tests nothing\n"
                + "\n".join(f"       {line}" for line in schema_errors[:5])
            )
            return
        for rule in EXPECTED_RULES:
            if not re.search(rf"\b{re.escape(rule)}:", output):
                failures.append(f"{CONSTRAINTS}: rule {rule} did not fire on an SSP that breaks it")


def main() -> int:
    failures: list[str] = []
    if check_tools(failures):
        check_validate(CATALOG, failures)
        check_validate(PROFILE, failures)
        check_resolution(failures)
        check_constraints(failures)
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"oscal-cli: catalog, profile, and {len(EXPECTED_RULES)} constraint rules checked, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
