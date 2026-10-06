#!/usr/bin/env python3
"""Vendor the pinned Rev 2 OSCAL catalog into reference/oscal/, with our patch.

ADR-0009 adopts khanssen/oscal-nist-800-171r2 at tag v2.0-combined.1 and
patches our copy. This script is the patch, so the vendored file can always be
rebuilt from the pin and checked for drift:

    python3 scripts/vendor_oscal_catalog.py                  # fetch the pin and write
    python3 scripts/vendor_oscal_catalog.py --from FILE      # patch a local copy of the pin
    python3 scripts/vendor_oscal_catalog.py --check          # fail if the vendored file differs

The patch does three things and nothing else:

1. Strips the 800-171A PDF page footer from the nine objectives that carry it
   (FOOTER_OBJECTIVES). It refuses to run if any of the nine lacks the footer,
   or if any other objective has it, because either means the pin moved and the
   patch needs a person to look at it again.
2. Gives the patched document its own uuid and last-modified, because OSCAL
   expects a document's uuid to change when its content does.
3. Writes the provenance header into metadata remarks: the pin, the upstream
   hash, the CC BY 4.0 attribution, and what was patched.

Moving the pin is a deliberate change: update PIN_TAG, PIN_COMMIT, and
UPSTREAM_SHA256 together, re-run, and read the diff.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

PIN_REPO = "https://github.com/khanssen/oscal-nist-800-171r2"
PIN_TAG = "v2.0-combined.1"
PIN_COMMIT = "291261e23b0544a7abf010aa8929ccdce1342561"
UPSTREAM_PATH = "catalog/nist-sp-800-171r2-combined-catalog.json"
UPSTREAM_URL = (
    f"https://raw.githubusercontent.com/khanssen/oscal-nist-800-171r2/{PIN_COMMIT}/{UPSTREAM_PATH}"
)
UPSTREAM_SHA256 = "13cf12214e57929f2423b77cff8967f2747b4a606a2838ca48c9df7462dc33c1"

OUT = Path("reference/oscal/nist-800-171r2-catalog.json")

FOOTER = " This publication is available free of charge from: https://doi.org/10.6028/NIST.SP.800-171A"
FOOTER_OBJECTIVES = (
    "_03.01.09_obj.a",
    "_03.01.16_obj.b",
    "_03.03.07_obj.a",
    "_03.03.09_obj.b",
    "_03.05.05_obj.a",
    "_03.08.03_obj.b",
    "_03.13.02_obj.e",
    "_03.13.16_obj.a",
    "_03.14.06_obj.c",
)

# Fixed, so re-running the patch on the same pin gives the same bytes.
PATCHED_UUID = "f0842075-9bbe-425f-b538-2f897384f888"
PATCHED_LAST_MODIFIED = "2026-09-28T00:00:00Z"

PROVENANCE = f"""Vendored by poamslayer/nist-800-171-skills. Provenance header (ADR-0009).

Source: NIST SP 800-171 Rev 2 Combined OSCAL Catalog, Archstone Security LLC, {PIN_REPO} . Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The requirement, discussion, objective, and assessment text is NIST's (SP 800-171 Rev 2 and SP 800-171A), a US Government work in the public domain.

Pin: tag `{PIN_TAG}`, commit `{PIN_COMMIT}`, file `{UPSTREAM_PATH}`, SHA-256 `{UPSTREAM_SHA256}`.

Changes made to the upstream file, by `scripts/vendor_oscal_catalog.py`: the 800-171A PDF page footer ("This publication is available free of charge from: https://doi.org/10.6028/NIST.SP.800-171A") is removed from the prose of nine objectives, {", ".join(FOOTER_OBJECTIVES)}; the document uuid and last-modified are replaced, because the content changed; and this remark is added. The same footer in assessment parts is left as upstream wrote it. Nothing else differs from the pinned file."""


def objectives(doc: dict) -> dict[str, dict]:
    """Every objective part in the catalog, by id."""
    found: dict[str, dict] = {}
    for group in doc["catalog"]["groups"]:
        for control in group["controls"]:
            for part in control.get("parts", []):
                if part.get("name") == "objective":
                    found[part["id"]] = part
    return found


def patch(raw: bytes) -> str:
    """Apply the documented patch to the pinned upstream bytes."""
    actual = hashlib.sha256(raw).hexdigest()
    if actual != UPSTREAM_SHA256:
        raise SystemExit(
            f"FAIL upstream {UPSTREAM_PATH}: SHA-256 is {actual}, the pin says {UPSTREAM_SHA256}. "
            "If the pin moved on purpose, update PIN_TAG, PIN_COMMIT, and UPSTREAM_SHA256 together."
        )
    doc = json.loads(raw)
    patched = copy.deepcopy(doc)
    objs = objectives(patched)

    problems = []
    for oid in FOOTER_OBJECTIVES:
        prose = objs.get(oid, {}).get("prose", "")
        if not prose.endswith(FOOTER):
            problems.append(f"{oid} does not end with the footer the patch removes")
    for oid, part in objs.items():
        if oid not in FOOTER_OBJECTIVES and FOOTER.strip() in part.get("prose", ""):
            problems.append(f"{oid} carries the footer but is not in the patch list")
    if problems:
        for p in problems:
            print(f"FAIL {UPSTREAM_PATH}: {p}")
        raise SystemExit("the patch no longer fits the pinned file; review it by hand")

    for oid in FOOTER_OBJECTIVES:
        objs[oid]["prose"] = objs[oid]["prose"][: -len(FOOTER)]

    catalog = patched["catalog"]
    catalog["uuid"] = PATCHED_UUID
    metadata = catalog["metadata"]
    metadata["last-modified"] = PATCHED_LAST_MODIFIED
    metadata["remarks"] = PROVENANCE
    return json.dumps(patched, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="source", type=Path, help="a local copy of the pinned upstream file")
    parser.add_argument("--check", action="store_true", help="fail if the vendored file is not what the patch produces")
    args = parser.parse_args()

    if args.source:
        raw = args.source.read_bytes()
    else:
        with urllib.request.urlopen(UPSTREAM_URL, timeout=60) as response:
            raw = response.read()

    result = patch(raw)
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != result:
            print(f"FAIL {OUT}: differs from the pinned upstream file with the documented patch applied")
            return 1
        print(f"{OUT}: matches the pin with the documented patch")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(result, encoding="utf-8")
    print(f"wrote {OUT} from {PIN_TAG} ({PIN_COMMIT[:8]}), {len(FOOTER_OBJECTIVES)} objectives patched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
