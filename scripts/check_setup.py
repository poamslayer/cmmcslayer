#!/usr/bin/env python3
"""Test the setup skill's scaffold, skills/setup/setup-poamslayer-skills/scaffold.py.

Every case runs the script in a scratch folder under a temporary directory,
never in the repository, and checks only what an operator would see: the files
it leaves, the SSP's verdict from oscal-cli, and its exit status. Nothing here
imports the script's internals.

1. Setup in an empty folder creates the layout (110 evidence folders,
   CONTEXT.md with the seat, docs/agents/) and ssp/ssp.json, made by scribe's
   create: it passes oscal-cli, imports our profile, holds all 110
   requirements with every objective planned, and the view exists. ssp.json
   and view/ are the SSP: no Markdown SSP file is written under ssp/, and no
   asset inventory or responsibility matrix under scope/ (#105).
2. Re-running setup with --force leaves ssp.json byte for byte unchanged.
3. Re-running setup without --force refuses and leaves ssp.json unchanged.
4. Without oscal-cli on PATH, setup still lays out the folders, writes
   no ssp.json, exits non-zero, and says why. Re-running with --force once
   oscal-cli is back adds the ssp.json that was missing.
5. A folder that already holds CONTEXT.md or policies/ is refused without
   --force, and no existing file, a README.md included, is overwritten.

    python3 scripts/check_setup.py

Needs Java and oscal-cli, like check_scribe.py.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCAFFOLD = Path("skills/setup/setup-poamslayer-skills/scaffold.py").resolve()
CONSTRAINTS = Path("reference/oscal/cmmc-constraints.xml").resolve()
PROFILE_HREF = "oscal/nist-800-171r2-profile.json"
CLIENT_WORDS = "the client's own words\n"


def run_scaffold(target: Path, *extra: str, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(SCAFFOLD),
            "--target",
            str(target),
            "--seat",
            "consultant",
            "--client",
            "Scratch Machining",
            "--tracker",
            "local",
            *extra,
        ],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def oscal_cli_passes(path: Path) -> bool:
    proc = subprocess.run(
        ["oscal-cli", "validate", "--no-color", str(path), "-c", str(CONSTRAINTS)],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def check_layout(failures: list[str], target: Path) -> None:
    markdown = sorted(p.name for p in (target / "ssp").glob("*.md"))
    if markdown:
        failures.append(f"{target}: Markdown SSP files under ssp/ ({', '.join(markdown[:3])}); ssp.json is the SSP")
    for name in ("asset-inventory.md", "esp-responsibility-matrix.md"):
        if (target / "scope" / name).exists():
            failures.append(f"{target}: scope/{name} was written; it is a view page generated from ssp.json")
    evidence = [p for p in (target / "evidence").glob("3.*") if p.is_dir()]
    if len(evidence) != 110:
        failures.append(f"{target}: {len(evidence)} evidence folders; expected 110")
    context = target / "CONTEXT.md"
    if not context.is_file() or "## Seat\n\nconsultant" not in context.read_text(encoding="utf-8"):
        failures.append(f"{context}: missing, or has no ## Seat heading with the seat")
    for name in ("issue-tracker.md", "triage-labels.md", "domain.md"):
        if not (target / "docs" / "agents" / name).is_file():
            failures.append(f"{target}: docs/agents/{name} was not written")


def check_ssp(failures: list[str], target: Path) -> None:
    ssp = target / "ssp" / "ssp.json"
    if not ssp.is_file():
        failures.append(f"{ssp}: setup did not create it")
        return
    if not oscal_cli_passes(ssp):
        failures.append(f"{ssp}: does not pass oscal-cli")
    plan = json.loads(ssp.read_text(encoding="utf-8"))["system-security-plan"]
    if plan.get("import-profile", {}).get("href") != PROFILE_HREF:
        failures.append(f"{ssp}: imports {plan.get('import-profile')}; expected {PROFILE_HREF}")
    if plan["system-characteristics"]["system-name"] != "Scratch Machining":
        failures.append(f"{ssp}: system name is not the client name")
    requirements = plan["control-implementation"]["implemented-requirements"]
    statements = [s for r in requirements for s in r.get("statements", [])]
    states = {b["implementation-status"]["state"] for s in statements for b in s["by-components"]}
    if len(requirements) != 110 or len(statements) != 320 or states != {"planned"}:
        failures.append(
            f"{ssp}: {len(requirements)} requirements, {len(statements)} objectives, "
            f"states {sorted(states)}; expected 110, 320, planned"
        )
    for name in ("nist-800-171r2-profile.json", "nist-800-171r2-catalog.json"):
        if not (target / "ssp" / "oscal" / name).is_file():
            failures.append(f"{target}: ssp/oscal/{name} was not copied")
    for page in ("view/asset-inventory.md", "view/requirements/3.5.3.md"):
        if not (target / page).is_file():
            failures.append(f"{target}: {page} was not rendered")


def check(failures: list[str], base: Path) -> None:
    # 1. an empty folder
    fresh = base / "fresh"
    fresh.mkdir()
    proc = run_scaffold(fresh)
    if proc.returncode != 0:
        failures.append(f"{SCAFFOLD}: exited {proc.returncode}: {proc.stderr.strip()}")
        return
    check_layout(failures, fresh)
    check_ssp(failures, fresh)
    ssp = fresh / "ssp" / "ssp.json"
    if not ssp.is_file():
        return
    before = ssp.read_bytes()

    # 2. --force never touches an existing ssp.json
    proc = run_scaffold(fresh, "--force")
    if proc.returncode != 0:
        failures.append(f"{SCAFFOLD} --force: exited {proc.returncode}: {proc.stderr.strip()}")
    if ssp.read_bytes() != before:
        failures.append(f"{ssp}: changed by a re-run with --force")

    # 3. without --force a scaffolded repo is refused
    proc = run_scaffold(fresh)
    if proc.returncode == 0 or ssp.read_bytes() != before:
        failures.append(f"{SCAFFOLD}: re-ran over a scaffolded repo without --force")

    # 4. no oscal-cli: the layout lands, the SSP does not, and --force adds it later
    bare = base / "bare"
    bare.mkdir()
    python_only = base / "bin"
    python_only.mkdir()
    (python_only / "python3").symlink_to(sys.executable)
    env = {**os.environ, "PATH": str(python_only)}
    proc = run_scaffold(bare, env=env)
    if proc.returncode == 0 or "oscal-cli" not in proc.stderr:
        failures.append(f"{SCAFFOLD}: did not report the missing oscal-cli: {proc.stderr.strip()}")
    if (bare / "ssp" / "ssp.json").exists():
        failures.append(f"{bare}: wrote ssp.json without oscal-cli")
    check_layout(failures, bare)
    proc = run_scaffold(bare, "--force")
    if proc.returncode != 0:
        failures.append(f"{SCAFFOLD} --force: did not add the missing ssp.json: {proc.stderr.strip()}")
    check_ssp(failures, bare)

    # 5. a repo that already holds the client's work is refused, and nothing is overwritten
    for held_path in ("CONTEXT.md", "policies/access-control.md"):
        held = base / f"held-{held_path.split('/')[0]}"
        existing = held / held_path
        existing.parent.mkdir(parents=True)
        existing.write_text(CLIENT_WORDS, encoding="utf-8")
        if run_scaffold(held).returncode == 0:
            failures.append(f"{SCAFFOLD}: ran over an existing {held_path} without --force")
        if existing.read_text(encoding="utf-8") != CLIENT_WORDS:
            failures.append(f"{existing}: overwritten by setup")
    readme = base / "kept" / "README.md"
    readme.parent.mkdir()
    readme.write_text(CLIENT_WORDS, encoding="utf-8")
    run_scaffold(readme.parent)
    if readme.read_text(encoding="utf-8") != CLIENT_WORDS:
        failures.append(f"{readme}: overwritten by setup")


def main() -> int:
    failures: list[str] = []
    if shutil.which("oscal-cli") is None:
        failures.append("oscal-cli not found on PATH; install it with: bash scripts/install_oscal_cli.sh")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            check(failures, Path(tmp))
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"setup: scaffold checked in a scratch folder, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
