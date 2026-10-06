#!/usr/bin/env python3
"""Create a deterministic CMMC Level 2 engagement repository scaffold."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any, Sequence


REQUIREMENT_ID_PATTERN = re.compile(r"^3\.\d{1,2}\.\d{1,2}$")
LABELS = (
    "needs-triage",
    "needs-info",
    "ready-for-agent",
    "ready-for-human",
    "wontfix",
    "poam",
    "opa",
    "wayfinder:map",
    "wayfinder:research",
    "wayfinder:prototype",
    "wayfinder:grilling",
    "wayfinder:task",
)
SEED_FILES = {
    "triage-labels.md": ("docs/agents/triage-labels.md", "# Triage labels\n"),
    "domain.md": ("docs/agents/domain.md", "# Domain\n"),
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a CMMC Level 2 engagement repository scaffold."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Engagement repository to scaffold. Defaults to the current directory.",
    )
    parser.add_argument(
        "--seat",
        choices=("consultant", "osc"),
        required=True,
        help="Operator seat to record in CONTEXT.md.",
    )
    parser.add_argument("--client", required=True, help="Client name.")
    parser.add_argument(
        "--tracker",
        choices=("github", "local"),
        help="Issue tracker. Defaults to GitHub for a GitHub clone, otherwise local.",
    )
    parser.add_argument(
        "--requirements",
        type=Path,
        help="Alternate path to the NIST SP 800-171 Rev 2 requirements JSON file.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Add missing scaffold files without overwriting existing files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print GitHub label commands without running them.",
    )
    return parser.parse_args(argv)


def requirements_path(override: Path | None) -> Path:
    """Return the requested requirements path or the repository-relative default."""
    if override is not None:
        return override.expanduser().resolve()
    return (
        Path(__file__).resolve().parents[3]
        / "reference"
        / "nist-800-171r2-requirements.json"
    )


def load_requirements(path: Path) -> list[dict[str, Any]]:
    """Load the 110 requirements and check the ids the evidence folders are named by."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"could not read requirements from {path}: {error}") from error

    if not isinstance(data, list) or len(data) != 110:
        raise ValueError("requirements data must be a list containing exactly 110 items")

    seen_ids: set[str] = set()
    for index, requirement in enumerate(data):
        if not isinstance(requirement, dict):
            raise ValueError(f"requirement at index {index} must be an object")
        requirement_id = requirement.get("id")
        if not isinstance(requirement_id, str) or not REQUIREMENT_ID_PATTERN.fullmatch(
            requirement_id
        ):
            raise ValueError(f"invalid requirement id at index {index}: {requirement_id!r}")
        if requirement_id in seen_ids:
            raise ValueError(f"duplicate requirement id: {requirement_id}")
        seen_ids.add(requirement_id)
    return data


def github_remote(target: Path) -> bool:
    """Return whether the target repository has a github.com remote."""
    try:
        result = subprocess.run(
            ["git", "-C", str(target), "remote", "-v"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return False
    return result.returncode == 0 and "github.com" in result.stdout.lower()


def ensure_directory(path: Path) -> bool:
    """Create one directory and return whether it was newly created."""
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"expected a directory at {path}")
        return False
    path.mkdir()
    return True


def write_file(path: Path, content: bytes, target: Path) -> bool:
    """Write one file unless it exists, and return whether it was created."""
    relative_path = path.relative_to(target)
    if path.exists():
        print(f"skipped: {relative_path}")
        return False
    path.write_bytes(content)
    return True


def context_text(client: str, seat: str) -> str:
    """Render the engagement CONTEXT.md file."""
    return f"""# {client} engagement

Client glossary and the scope decisions in force. Every skill reads this file first.

## Seat

{seat}

## Language

(terms are added as decisions land)

## CUI decisions

(written by find-cui)

## Scope decisions

(written by the scoping skills; each links its ADR)
"""


def seed_content(script_dir: Path, seed_name: str, placeholder: str) -> bytes:
    """Read a seed verbatim, or return a one-line placeholder with a warning."""
    seed_path = script_dir / seed_name
    try:
        return seed_path.read_bytes()
    except FileNotFoundError:
        print(
            f"WARNING: seed file {seed_path.name} not found; wrote a placeholder.",
            file=sys.stderr,
        )
        return placeholder.encode("utf-8")


def write_seed(
    target: Path,
    script_dir: Path,
    seed_name: str,
    destination_name: str,
    placeholder: str,
) -> bool:
    """Copy a seed file verbatim or write its placeholder."""
    return write_file(
        target / destination_name,
        seed_content(script_dir, seed_name, placeholder),
        target,
    )


def configure_labels(target: Path, tracker: str, is_github_clone: bool, dry_run: bool) -> int:
    """Print requested label commands and run them when it is safe to do so."""
    if tracker != "github":
        return 0

    gh_path = shutil.which("gh")
    should_run = gh_path is not None and is_github_clone and not dry_run
    for label in LABELS:
        print(f"gh label create {label}")
        if not should_run:
            continue
        result = subprocess.run(
            [gh_path, "label", "create", label],
            cwd=target,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            continue
        output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
        if "already exists" not in output.lower():
            detail = output or f"gh exited with status {result.returncode}"
            print(f"WARNING: could not create label {label}: {detail}", file=sys.stderr)
    return len(LABELS)


def scribe_dir() -> Path:
    """Scribe's folder, which holds the record's writer, its check, and its renderer."""
    return Path(__file__).resolve().parents[3] / "skills" / "flows" / "scribe"


def run_scribe(command: str, target: Path, requirements_file: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(scribe_dir() / command), str(target), "--requirements", str(requirements_file)],
        check=False,
        capture_output=True,
        text=True,
    )


def create_ssp(target: Path, client: str, requirements: list[dict[str, Any]], requirements_file: Path) -> str:
    """Write the Markdown SSP unless one exists, then check it and render the view. Return what happened.

    The SSP is ssp/system.md and one ssp/<requirement>.md per requirement, every
    objective planned on the placeholder, this-system (ADR-0012). An existing
    SSP file is never touched; a missing one is added.
    """
    if not (scribe_dir() / "ssp_record.py").is_file():
        print(f"ERROR: scribe not found at {scribe_dir()}; the SSP was not created.", file=sys.stderr)
        return "not created"
    sys.path.insert(0, str(scribe_dir()))
    import ssp_record  # noqa: E402  (scribe's writer, so setup and scribe write the same shape)

    ssp = target / "ssp"
    (ssp / "components").mkdir(parents=True, exist_ok=True)
    pending = {ssp / "system.md": ssp_record.blank_system(client)}
    pending.update({ssp / f"{r['id']}.md": ssp_record.blank_requirement(r) for r in requirements})
    written = 0
    for path, text in pending.items():
        if path.exists():
            continue
        path.write_text(text, encoding="utf-8")
        written += 1
    outcome = "created" if written == len(pending) else "kept" if written == 0 else f"{written} missing files added"
    if written == 0:
        print("skipped: ssp/ (the SSP exists)")

    check = run_scribe("check_ssp.py", target, requirements_file)
    if check.returncode != 0:
        print(f"ERROR: the SSP fails scribe's check:\n{check.stdout.strip()}{check.stderr.strip()}", file=sys.stderr)
        return "fails the check"
    if written or not (target / "view").is_dir():
        render = run_scribe("render_view.py", target, requirements_file)
        if render.returncode != 0:
            print(f"WARNING: the view was not rendered:\n{render.stdout.strip()}{render.stderr.strip()}", file=sys.stderr)
    return outcome


def run_status_check(script_dir: Path) -> str:
    """Run the adjacent status checker and return its output."""
    result = subprocess.run(
        [sys.executable, str(script_dir / "status-check.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    output = "\n".join(part.rstrip() for part in (result.stdout, result.stderr) if part)
    return output or f"status check exited with status {result.returncode} without output"


def scaffold(args: argparse.Namespace) -> int:
    """Create all missing or requested engagement repository artifacts."""
    target = args.target.expanduser().resolve()
    if target.exists() and not target.is_dir():
        print(f"ERROR: target is not a directory: {target}", file=sys.stderr)
        return 1
    target.mkdir(parents=True, exist_ok=True)

    guarded_paths = [target / name for name in ("CONTEXT.md", "ssp", "scope", "evidence", "policies")]
    existing_guarded = [path for path in guarded_paths if path.exists()]
    if existing_guarded and not args.force:
        names = ", ".join(
            f"{path.name}/" if path.is_dir() else path.name for path in existing_guarded
        )
        print(
            f"ERROR: target already contains {names}; use --force to add missing files.",
            file=sys.stderr,
        )
        return 1

    requirements_file = requirements_path(args.requirements)
    try:
        requirements = load_requirements(requirements_file)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    is_github_clone = github_remote(target)
    tracker = args.tracker or ("github" if is_github_clone else "local")
    script_dir = Path(__file__).resolve().parent

    directory_names = [
        "docs",
        "docs/adr",
        "docs/agents",
        "scope",
        "scope/interviews",
        "ssp",
        "evidence",
        *(f"evidence/{requirement['id']}" for requirement in requirements),
        "policies",
        ".scratch",
    ]
    folders_created = 0
    try:
        for directory_name in directory_names:
            folders_created += ensure_directory(target / directory_name)
    except (OSError, ValueError) as error:
        print(f"ERROR: could not create scaffold directories: {error}", file=sys.stderr)
        return 1

    files_created = 0
    try:
        static_files = {
            "CONTEXT.md": context_text(args.client, args.seat),
            "README.md": (
                f"{args.client}\n"
                "CMMC Level 2 engagement repo scaffolded by "
                f"setup-poamslayer-skills on {date.today().isoformat()}\n"
                "Read CONTEXT.md first.\n"
            ),
            "docs/adr/.gitkeep": "",
            "scope/.gitkeep": "",
            "scope/interviews/.gitkeep": "",
            "evidence/continuous-monitoring-calendar.md": (
                "# Continuous monitoring calendar\n"
            ),
            "policies/.gitkeep": "",
            ".scratch/.gitkeep": "",
            ".gitignore": ".DS_Store\n",
        }
        for destination_name, content in static_files.items():
            files_created += write_file(
                target / destination_name,
                content.encode("utf-8"),
                target,
            )

        issue_seed = f"issue-tracker-{tracker}.md"
        files_created += write_seed(
            target,
            script_dir,
            issue_seed,
            "docs/agents/issue-tracker.md",
            "# Issue tracker\n",
        )
        for seed_name, (destination_name, placeholder) in SEED_FILES.items():
            files_created += write_seed(
                target,
                script_dir,
                seed_name,
                destination_name,
                placeholder,
            )

        for requirement in requirements:
            requirement_id = requirement["id"]
            files_created += write_file(
                target / "evidence" / requirement_id / ".gitkeep",
                b"",
                target,
            )
    except OSError as error:
        print(f"ERROR: could not write scaffold: {error}", file=sys.stderr)
        return 1

    ssp_outcome = create_ssp(target, args.client, requirements, requirements_file)
    labels_created_or_printed = configure_labels(
        target, tracker, is_github_clone, args.dry_run
    )
    status_output = run_status_check(script_dir)

    print("Summary:")
    print(f"files created: {files_created}")
    print(f"folders created: {folders_created}")
    print(f"labels created or printed: {labels_created_or_printed}")
    print(f"seat recorded: {args.seat}")
    print(f"ssp/: {ssp_outcome}")
    print(status_output)
    return 1 if ssp_outcome in ("not created", "fails the check") else 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the scaffold command."""
    return scaffold(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
