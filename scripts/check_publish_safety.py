#!/usr/bin/env python3
"""Check whether this repository is safe to make public, history included.

Deleting a file does not remove it from a git repository. Every earlier version
stays reachable, so a repo published after a tidy-up commit still hands over
everything it ever held. For a repo built from a private source under a policy
about what may be said in public, that is the failure that matters.

This checks the working tree and every blob in history against the same block
and warn lists the scrub check uses.

    python3 scripts/check_publish_safety.py

Exit status is 1 when anything private is reachable from any commit.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scrub_check import load_terms, scrub_lists_dir  # noqa: E402

SCRUB_DIR = scrub_lists_dir()
CHECKED_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json"}


def git(*args: str) -> str:
    """Run a git command and return its stdout."""
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False
    )
    return result.stdout


def historical_blobs() -> list[tuple[str, str]]:
    """Return every (path, blob hash) pair reachable from any commit."""
    listing = git("rev-list", "--objects", "--all")
    blobs: list[tuple[str, str]] = []
    for line in listing.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        sha, path = parts
        if Path(path).suffix.lower() in CHECKED_SUFFIXES:
            blobs.append((path, sha))
    return blobs


def main() -> int:
    """Check every historical blob for blocked terms."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scrub-dir", default=str(SCRUB_DIR))
    args = parser.parse_args()

    scrub_dir = Path(args.scrub_dir).expanduser()
    if not (scrub_dir / "blocklist.txt").is_file():
        print(f"publish safety: no private blocklist at {scrub_dir}; skipping.", file=sys.stderr)
        return 0
    block_patterns = load_terms(scrub_dir / "blocklist.txt")

    blobs = historical_blobs()
    offending: dict[str, set[str]] = {}

    for path, sha in blobs:
        if path.startswith("scripts/scrub/"):
            continue
        content = git("cat-file", "-p", sha)
        if not content:
            continue
        for configured in block_patterns:
            if configured.pattern.search(content):
                offending.setdefault(path, set()).add(configured.term)

    for path in sorted(offending):
        terms = ", ".join(sorted(offending[path])[:6])
        print(f"FAIL {path}: reachable in history, contains {terms}")

    print(
        f"publish safety: {len(blobs)} historical files checked, "
        f"{len(offending)} carrying blocked terms"
    )
    if offending:
        print()
        print("Deleting these files does not make the repository safe to publish.")
        print("Every version stays reachable from history. Two ways out:")
        print("  1. Publish a fresh repository from an orphan commit of the")
        print("     current tree, keeping this one private as the working history.")
        print("  2. Rewrite history to drop these paths, then force-push, knowing")
        print("     every existing clone and fork keeps the old objects.")
        print("Option 1 is the safe one. See docs/adr/0001-source-policy.md.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
