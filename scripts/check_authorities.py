#!/usr/bin/env python3
"""Check that every URL the skills cite is in the authorities register.

ADR-0004 makes reference/authorities.md the one list of cited sources, each
with a tier that limits what it can support. A citation that skips the register
has no tier, so nobody decided what it is allowed to prove. This finds those,
and it finds register entries that name a local mirror that is not there.

    python3 scripts/check_authorities.py

Needs no network, so it runs in scripts/verify.sh. Whether the URLs still
resolve is scripts/check_links.py's job.
"""

from __future__ import annotations

import re
from pathlib import Path

from check_links import REGISTER, SKILLS_ROOT, cited_urls, urls_in

MIRROR_PATTERN = re.compile(r"`(reference/[^`]+)`")


def main() -> int:
    """Report unregistered citations and missing mirrors."""
    if not REGISTER.exists():
        print(f"FAIL {REGISTER} is missing; see docs/adr/0004-authority-tiers.md")
        return 1

    registered = urls_in(REGISTER)
    cited = cited_urls(SKILLS_ROOT)
    missing = {url: files for url, files in cited.items() if url not in registered}

    for url, files in sorted(missing.items()):
        print(f"FAIL not in the register: {url}")
        for path in sorted(files):
            print(f"       cited by {path}")

    text = REGISTER.read_text(encoding="utf-8")
    absent = sorted({m for m in MIRROR_PATTERN.findall(text) if not Path(m).exists()})
    for path in absent:
        print(f"FAIL the register names a mirror that does not exist: {path}")

    print(
        f"authorities: {len(cited)} cited URLs, {len(missing)} not in the register, "
        f"{len(absent)} missing mirrors"
    )
    return 1 if missing or absent else 0


if __name__ == "__main__":
    raise SystemExit(main())
