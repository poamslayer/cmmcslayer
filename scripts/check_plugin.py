#!/usr/bin/env python3
"""Check that the Claude Code plugin manifest lists every skill.

`.claude-plugin/plugin.json` is how a stranger installs the repo. A skill folder
the manifest leaves out is a skill the plugin never loads, and nothing else
would notice. This compares the manifest's `skills` list with the skill folders
on disk, both ways, and checks the marketplace file names the same plugin.

    python3 scripts/check_plugin.py

Exit status is 1 on a failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PLUGIN = Path(".claude-plugin/plugin.json")
MARKETPLACE = Path(".claude-plugin/marketplace.json")


def main() -> int:
    plugin = json.loads(PLUGIN.read_text())
    market = json.loads(MARKETPLACE.read_text())
    listed = {s.removeprefix("./") for s in plugin["skills"]}
    on_disk = {str(p.parent) for p in Path("skills").rglob("SKILL.md")}
    failures = [f"missing from plugin.json: {s}" for s in sorted(on_disk - listed)]
    failures += [f"in plugin.json but not on disk: {s}" for s in sorted(listed - on_disk)]
    names = [p["name"] for p in market["plugins"]]
    if plugin["name"] not in names:
        failures.append(f"marketplace.json does not list plugin {plugin['name']}")
    for failure in failures:
        print(failure)
    print(f"plugin: {len(listed)} skills listed, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
