#!/usr/bin/env python3
"""Check that every URL the skills cite actually resolves.

The source policy requires a public citation for every claim, so a citation
that does not resolve is worse here than a missing one: it looks like evidence
and is not. This finds links that were mistyped, that rotted, or that were
never real.

    python3 scripts/check_links.py              # every cited URL
    python3 scripts/check_links.py --timeout 10 # shorter per-request budget

It checks the URLs in the skills and in reference/authorities.md, the register
ADR-0004 keeps of every cited source, so a source the register holds for later
use is checked before anything cites it.

Needs network access, so it is not part of scripts/verify.sh. Run it before
publishing and whenever a batch of citations is added.

A 403 is reported but does not fail the run. Several federal sites refuse
scripted requests while serving the page to a browser, so a 403 means the host
declined to answer, not that the page is gone. A 404 fails.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SKILLS_ROOT = Path("skills")
REGISTER = Path("reference/authorities.md")
URL_PATTERN = re.compile(r'https?://[^\s")`<>\]]+')


def cited_urls(root: Path) -> dict[str, set[str]]:
    """Return every cited URL mapped to the files citing it."""
    found: dict[str, set[str]] = {}
    for path in sorted(root.rglob("*.md")):
        for url in urls_in(path):
            found.setdefault(url, set()).add(str(path))
    return found


def urls_in(path: Path) -> set[str]:
    """Return the URLs in one Markdown file."""
    # A trailing period is sentence punctuation far more often than it is part
    # of a path, and a citation that only resolves with the full stop attached
    # is a citation waiting to break.
    text = path.read_text(encoding="utf-8")
    return {raw.rstrip(".,;:") for raw in URL_PATTERN.findall(text)}


def status_of(url: str, timeout: int) -> str:
    """Return the HTTP status curl reports, or 000 when the request failed."""
    try:
        result = subprocess.run(
            [
                "curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}",
                "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "--max-time", str(timeout), url,
            ],
            capture_output=True,
            text=True,
            timeout=timeout + 10,
        )
        return result.stdout.strip() or "000"
    except (subprocess.SubprocessError, OSError):
        return "000"


def main() -> int:
    """Check every cited URL and report the ones that do not resolve."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", default=str(SKILLS_ROOT))
    parser.add_argument("--timeout", type=int, default=25)
    args = parser.parse_args()

    urls = cited_urls(Path(args.skills_root))
    if REGISTER.exists():
        for url in urls_in(REGISTER):
            urls.setdefault(url, set()).add(str(REGISTER))
    broken: list[tuple[str, str, set[str]]] = []
    declined = 0

    for url, files in sorted(urls.items()):
        code = status_of(url, args.timeout)
        if code.startswith("2"):
            continue
        if code == "403":
            declined += 1
            continue
        broken.append((code, url, files))

    for code, url, files in broken:
        print(f"FAIL {code} {url}")
        for path in sorted(files):
            print(f"       cited by {path}")

    print(
        f"links: {len(urls)} cited, {len(broken)} not resolving, "
        f"{declined} declined a scripted request"
    )
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
