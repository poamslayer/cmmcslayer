#!/usr/bin/env python3
"""Write the control corpus into the public dictionary repository.

The site at dictionary.poamslayer.com is a separate public repository whose
content directory is generated, never authored. This script is what generates
it. See docs/adr/0003-dictionary-site-is-a-separate-public-repo.md.

Three properties of this script are the reason it exists at all, and each one
is easy to lose by accident:

  - It gates on `scripts/verify.sh --strict`. The verbatim half of the scrub
    check builds its n-gram set from the private wiki and skips itself when the
    wiki is absent. A gate that ran on a build server would pass while its
    strongest check silently did not run, so the gate stays on the machine that
    has the wiki.

  - It regenerates rather than merges. Every file in the target directory is
    deleted and rewritten. A hand edit made in the public repository is lost on
    the next run, which is the intended behaviour and not a limitation to work
    around. Content is fixed here and only here.

  - It strips `vault_sources` and does nothing else to the file. The field
    names private wiki pages, and it tells a reader nothing. Beyond removing it
    this script does not parse the Markdown body, because all parsing happens
    once in the Astro content collection schema. Two parsers would be two
    things to keep correct.

The check runs against the public working tree before the push, never after. A
check that ran after the push would report a leak that had already happened.

    python3 scripts/sync_dictionary.py                 # write and check, no git
    python3 scripts/sync_dictionary.py --push          # also commit and push

Exit status is 1 when anything fails.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

CONTROLS_DIR = Path("skills/domain/gap/control-evidence-lookup/controls")
CONTENT_SUBDIR = Path("src/content/requirements")
GLOSSARY_FILE = Path("src/content/glossary.json")
CONTEXT_FILE = Path("CONTEXT.md")
EXPECTED = 110
STRIPPED_KEY = "vault_sources"

# The glossary is a subset of this repository's own CONTEXT.md, chosen by name
# rather than by a rule.
#
# CONTEXT.md holds two kinds of term. The CMMC vocabulary a reader needs, and
# the machinery this project is built from: the fixture, the cold run, the
# seat, the control file, the scrub check. The second kind is meaningless to
# someone looking up what a POA&M is, and publishing it would describe how this
# repository works to an audience that has no reason to care.
#
# An allowlist rather than a denylist, because the failure modes are not
# symmetric. A new CMMC term that nobody adds here is merely missing from the
# site. A new machinery term that a denylist has not learned about yet would be
# published.
# Phrases that describe how this project is built rather than what a CMMC term
# means. A published definition carrying one is trimmed of that sentence.
#
# Withholding a machinery term by name is not enough on its own. Four of the
# published definitions explained themselves partly in machinery: the SSP
# definition described a folder layout, and the POA&M and OPA definitions
# described GitHub issue labels. None of that means anything to a reader
# looking up what a POA&M is, and all of it describes a private repository.
MACHINERY_PHRASES = (
    "control file",
    "engagement repo",
    "in this repo",
    "fixture",
    "cold run",
    "scrub check",
    "domain skill",
    "open items list",
    "vault",
)

PUBLIC_TERMS = [
    "Requirement",
    "Objective",
    "Family",
    "MET / NOT MET / N/A",
    "CUI",
    "FCI",
    "CTI",
    "Re-used CUI",
    "CUI Asset",
    "Security Protection Asset (SPA)",
    "Contractor Risk Managed Asset (CRMA)",
    "Specialized Asset",
    "Out-of-Scope Asset",
    "Scope",
    "Applicability",
    "ESP",
    "CSP",
    "Responsibility matrix",
    "SSP",
    "Conformity statement",
    "POA&M",
    "OPA",
    "Enduring exception",
    "SPRS score",
    "Significant change",
    "Affirming Official",
    "C3PAO",
]


def sort_key(requirement_id: str) -> tuple[int, ...]:
    """Order requirements numerically, so 3.1.2 comes before 3.1.13."""
    return tuple(int(part) for part in requirement_id.split("."))


def strip_vault_sources(text: str) -> tuple[str, bool]:
    """Remove the vault_sources key and its list items from the frontmatter.

    Returns the rewritten file and whether the key was found. The edit is line
    based on purpose. Re-serializing the frontmatter through a YAML library
    would reformat every other field, and the public file should differ from
    the private one in exactly one way.
    """
    if not text.startswith("---"):
        return text, False

    lines = text.split("\n")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return text, False

    out: list[str] = []
    dropping = False
    found = False
    for index, line in enumerate(lines):
        if index >= end:
            dropping = False
            out.append(line)
            continue
        if re.match(rf"^{STRIPPED_KEY}\s*:", line):
            dropping = True
            found = True
            continue
        if dropping:
            # A list item or a continuation line belongs to the key being
            # dropped. Anything at column zero starts the next key.
            if line.startswith((" ", "\t", "-")) or not line.strip():
                continue
            dropping = False
        out.append(line)

    return "\n".join(out), found


def slugify(term: str) -> str:
    """A stable id for a term, used as its anchor on the glossary page."""
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def publishable(definition: str) -> str:
    """Drop the sentences that describe this project rather than the term.

    Sentence granularity is the right unit here: every machinery reference in
    CONTEXT.md sits in a sentence of its own or can be made to, and dropping a
    whole sentence never leaves a half-finished one behind. What survives is
    checked again on the public side, so a future edit that reintroduces one of
    these phrases fails the check rather than shipping.
    """
    kept = [
        sentence
        for sentence in re.split(r"(?<=\.)\s+", definition)
        if not any(phrase in sentence.lower() for phrase in MACHINERY_PHRASES)
    ]
    return " ".join(kept).strip()


def parse_glossary(text: str) -> dict[str, dict[str, str]]:
    """Read the term blocks out of the Language section of CONTEXT.md.

    Each block is a bold term, a definition, and sometimes a line beginning
    `_Avoid_:` naming the words not to use. That last line is the part of this
    glossary nobody else publishes, so it is lifted into its own field rather
    than left buried in the definition.
    """
    section = text.split("## Language", 1)
    if len(section) < 2:
        return {}
    body = section[1].split("\n## ", 1)[0]

    entries: dict[str, dict[str, str]] = {}
    for match in re.finditer(r"^\*\*(.+?)\*\*:\n(.*?)(?=\n\*\*|\Z)", body, re.S | re.M):
        term = match.group(1).strip()
        lines = [line for line in match.group(2).strip().split("\n") if line.strip()]
        avoid = ""
        definition: list[str] = []
        for line in lines:
            if line.startswith("_Avoid_:"):
                avoid = line[len("_Avoid_:"):].strip()
            else:
                definition.append(line.strip())
        entries[term] = {"definition": " ".join(definition), "avoid": avoid}
    return entries


def write_glossary(root: Path, public: Path) -> int:
    """Write the published terms, and report how many failures it found."""
    entries = parse_glossary((root / CONTEXT_FILE).read_text(encoding="utf-8"))
    if not entries:
        print(f"FAIL {CONTEXT_FILE}: no Language section to read terms from")
        return 1

    failures = 0
    trimmed = 0
    published = []
    for term in PUBLIC_TERMS:
        entry = entries.get(term)
        if entry is None:
            print(f"FAIL {CONTEXT_FILE}: no definition for the published term {term!r}")
            failures += 1
            continue
        definition = publishable(entry["definition"])
        if not definition:
            print(f"FAIL {CONTEXT_FILE}: {term!r} has nothing left to publish once trimmed")
            failures += 1
            continue
        if definition != entry["definition"]:
            trimmed += 1
        published.append(
            {
                "id": slugify(term),
                "term": term,
                "definition": definition,
                "avoid": publishable(entry["avoid"]),
            }
        )

    target = public / GLOSSARY_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(published, indent=2) + "\n", encoding="utf-8")
    withheld = len(entries) - len(PUBLIC_TERMS)
    print(
        f"glossary: {len(published)} terms published, {withheld} withheld, "
        f"{trimmed} trimmed of machinery, {failures} failing"
    )
    return failures


def run(command: list[str], cwd: Path | None = None) -> int:
    """Run a command with its output going straight to this script's output.

    Flushing first matters: without it this script's own headings sit in a
    buffer while the child writes straight to the terminal, and the log comes
    out in an order that did not happen.
    """
    sys.stdout.flush()
    return subprocess.run(command, cwd=cwd).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--public-repo",
        default="~/cmmc-dictionary",
        help="local clone of the public dictionary repository",
    )
    parser.add_argument(
        "--controls-dir",
        default=str(CONTROLS_DIR),
        help="where the control files are read from",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="bypass the publication gate; for development only",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="commit and push the public repository after a clean run",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent

    # 1. The publication gate.
    if args.skip_verify:
        print(
            "WARNING: the publication gate was bypassed. Nothing here has been "
            "checked against the scrub. Do not push this.",
            file=sys.stderr,
        )
    else:
        print("== publication gate: verify.sh --strict")
        if run(["bash", "scripts/verify.sh", "--strict"], cwd=root) != 0:
            print("FAIL verify.sh: the publication gate did not pass, so nothing was written")
            return 1
        print()

    # 2. The public clone.
    public = Path(args.public_repo).expanduser().resolve()
    if not public.is_dir():
        print(f"FAIL {public}: the public repository is not cloned here")
        return 1
    if not (public / ".git").exists():
        print(f"FAIL {public}: this is not a git working tree")
        return 1

    controls = root / args.controls_dir
    sources = sorted(controls.glob("*.md"), key=lambda p: sort_key(p.stem))
    if len(sources) != EXPECTED:
        print(f"FAIL {controls}: found {len(sources)} control files, expected {EXPECTED}")
        return 1

    # 3. Regenerate. The whole directory goes, so a file deleted upstream does
    #    not linger here and a hand edit does not survive.
    target = public / CONTENT_SUBDIR
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    print(f"== regenerating {target}")

    failures = 0
    written = 0
    for source in sources:
        text = source.read_text(encoding="utf-8")
        stripped, found = strip_vault_sources(text)
        if not found:
            print(f"FAIL {source}: no {STRIPPED_KEY} in the frontmatter")
            failures += 1
            continue
        (target / source.name).write_text(stripped, encoding="utf-8")
        written += 1

    # 4. Check this script's own output before it is anyone else's problem.
    for path in sorted(target.glob("*.md")):
        if STRIPPED_KEY in path.read_text(encoding="utf-8"):
            print(f"FAIL {path}: {STRIPPED_KEY} survived the strip")
            failures += 1

    if written != EXPECTED:
        print(f"FAIL {target}: wrote {written} files, expected {EXPECTED}")
        failures += 1

    print(f"sync: {written} of {EXPECTED} written, {failures} failing")
    failures += write_glossary(root, public)
    if failures:
        return 1
    print()

    # 5. The public repository's own check, against the working tree.
    check = public / "scripts" / "check.mjs"
    if check.exists():
        print("== public repository check")
        if run(["node", "scripts/check.mjs"], cwd=public) != 0:
            print("FAIL scripts/check.mjs: the public repository check did not pass")
            return 1
        print()
    else:
        print("note: scripts/check.mjs does not exist yet, so nothing gated this tree")
        print()

    # 6. Commit and push, only on a clean run and only when asked.
    if not args.push:
        print("sync: wrote and checked the tree. Re-run with --push to publish it.")
        return 0

    status = subprocess.run(
        ["git", "status", "--porcelain", str(CONTENT_SUBDIR), str(GLOSSARY_FILE)],
        cwd=public,
        capture_output=True,
        text=True,
    )
    if not status.stdout.strip():
        print("sync: the public tree already matches this corpus, nothing to commit")
        return 0

    message = (
        "Sync the requirement corpus\n\n"
        f"{written} requirements, generated on {date.today().isoformat()}.\n"
        "Generated output. Edit the corpus upstream, never here."
    )
    if run(["git", "add", str(CONTENT_SUBDIR), str(GLOSSARY_FILE)], cwd=public) != 0:
        return 1
    if run(["git", "commit", "-m", message], cwd=public) != 0:
        return 1
    if run(["git", "push"], cwd=public) != 0:
        return 1
    print(f"sync: published {written} requirements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
