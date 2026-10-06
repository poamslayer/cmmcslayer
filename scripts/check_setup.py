#!/usr/bin/env python3
"""Test the setup skill's scaffold, skills/setup/setup-poamslayer-skills/scaffold.py.

Every case runs the script in a scratch folder under a temporary directory,
never in the repository, and checks only what an operator would see: the files
it leaves, the verdict of scribe's check on the SSP, and its exit status.
Nothing here imports the script's internals.

1. Setup in an empty folder creates the layout (110 evidence folders,
   CONTEXT.md with the seat, docs/agents/) and the Markdown SSP (ADR-0012):
   ssp/system.md with the client's name, and one ssp/<requirement>.md for each
   of the 110 requirements, every one of the 320 objectives planned on
   this-system. The SSP passes scribe's check and the view is rendered. No
   ssp.json or OSCAL file is written, and no asset inventory or responsibility
   matrix under scope/.
2. Re-running setup with --force leaves the SSP byte for byte unchanged.
3. Re-running setup without --force refuses and leaves the SSP unchanged.
4. With no Java on PATH, only Python, setup runs to completion and the SSP
   passes the check: nothing it needs is missing.
5. A folder that already holds CONTEXT.md or policies/ is refused without
   --force, and no existing file, a README.md included, is overwritten.

    python3 scripts/check_setup.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCAFFOLD = Path("skills/setup/setup-poamslayer-skills/scaffold.py").resolve()
CHECK = Path("skills/flows/scribe/check_ssp.py").resolve()
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


def check_passes(target: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECK), str(target)], capture_output=True, text=True, check=False)


def ssp_files(target: Path) -> dict[str, bytes]:
    return {str(p.relative_to(target)): p.read_bytes() for p in sorted((target / "ssp").rglob("*")) if p.is_file()}


def check_layout(failures: list[str], target: Path) -> None:
    for found in sorted(target.rglob("*.json")) + sorted(target.rglob("oscal")):
        failures.append(f"{found}: setup wrote an OSCAL file; the SSP is Markdown (ADR-0012)")
    for name in ("asset-inventory.md", "esp-responsibility-matrix.md"):
        if (target / "scope" / name).exists():
            failures.append(f"{target}: scope/{name} was written; it is a view page generated from the SSP")
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
    ssp = target / "ssp"
    system = ssp / "system.md"
    if not system.is_file():
        failures.append(f"{system}: setup did not create it")
        return
    if "system-name: Scratch Machining\n" not in system.read_text(encoding="utf-8"):
        failures.append(f"{system}: the system name is not the client name")
    files = sorted(ssp.glob("3.*.md"))
    text = "".join(f.read_text(encoding="utf-8") for f in files)
    placeholders = text.count("    - component: this-system\n      status: planned\n      statement: Not yet written.\n")
    if len(files) != 110 or placeholders != 320 or text.count("- component:") != 320:
        failures.append(f"{ssp}: {len(files)} requirement files and {placeholders} placeholders; "
                        "expected 110 files and all 320 objectives planned on this-system")
    proc = check_passes(target)
    if proc.returncode != 0:
        failures.append(f"{ssp}: fails scribe's check:\n{proc.stdout}")
    for page in ("view/asset-inventory.md", "view/esp-responsibility-matrix.md", "view/requirements/3.5.3.md"):
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
    before = ssp_files(fresh)

    # 2. --force never touches an existing SSP
    proc = run_scaffold(fresh, "--force")
    if proc.returncode != 0:
        failures.append(f"{SCAFFOLD} --force: exited {proc.returncode}: {proc.stderr.strip()}")
    if ssp_files(fresh) != before:
        failures.append(f"{fresh / 'ssp'}: changed by a re-run with --force")

    # 3. without --force a scaffolded repo is refused
    proc = run_scaffold(fresh)
    if proc.returncode == 0 or ssp_files(fresh) != before:
        failures.append(f"{SCAFFOLD}: re-ran over a scaffolded repo without --force")

    # 4. Python alone, no Java: setup still does everything
    bare = base / "bare"
    bare.mkdir()
    python_only = base / "bin"
    python_only.mkdir()
    (python_only / "python3").symlink_to(sys.executable)
    env = {**os.environ, "PATH": str(python_only)}
    env.pop("JAVA_HOME", None)
    proc = run_scaffold(bare, env=env)
    if proc.returncode != 0:
        failures.append(f"{SCAFFOLD}: failed with no Java on PATH: {proc.stderr.strip()}")
    check_layout(failures, bare)
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
    with tempfile.TemporaryDirectory() as tmp:
        check(failures, Path(tmp))
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"setup: scaffold checked in a scratch folder, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
