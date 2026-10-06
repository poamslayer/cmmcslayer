#!/usr/bin/env python3
"""Validate every skill's frontmatter and its Codex metadata.

Two harnesses read these files and neither tolerates a mismatch. A skill whose
`name` does not match its folder will not resolve when another skill calls it by
name. A skill that is user-invoked in one harness and model-invoked in the other
is reachable by the model in exactly one of them, which is the kind of bug that
shows up as a skill firing when nobody asked for it.

    python3 scripts/check_skills.py

Exit status is 1 when any skill fails.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SKILLS_ROOT = Path("skills")
DOMAIN_ROOT = SKILLS_ROOT / "domain"


def frontmatter(text: str) -> str | None:
    """Return the leading YAML block, or None when there is not one."""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    return parts[1] if len(parts) == 3 else None


def skill_calls(text: str) -> set[str]:
    """Return every skill name this skill instructs the agent to call.

    Dependencies are written as an instruction to call the Skill tool with a
    named skill, so the names are recoverable from the prose.
    """
    names: set[str] = set()
    for clause in re.findall(r"[Ss]kill tool (?:twice, )?(?:with|for) ([^\n.]*)", text):
        names.update(re.findall(r"[`\"]([a-z][a-z0-9-]+)[`\"]", clause))
    return names


def check_skill(skill_file: Path) -> list[str]:
    """Return the problems with one skill, empty when it passes."""
    problems: list[str] = []
    folder = skill_file.parent
    text = skill_file.read_text(encoding="utf-8")

    front = frontmatter(text)
    if front is None:
        return ["no YAML frontmatter"]

    name = re.search(r"^name:\s*(\S+)", front, re.M)
    if not name:
        problems.append("no name in frontmatter")
    elif name.group(1).strip("\"'") != folder.name:
        problems.append(f"name {name.group(1)} does not match folder {folder.name}")

    if not re.search(r"^description:", front, re.M):
        problems.append("no description in frontmatter")

    # Domain skills record where their judgment came from, so a change to a
    # source page tells the maintainer which skills to re-check.
    if DOMAIN_ROOT in folder.parents and not re.search(r"^vault_sources:", front, re.M):
        problems.append("domain skill has no vault_sources")

    # Every domain skill answers the same four questions in the same order, so
    # an operator can find the method without reading the whole file and a
    # later skill knows where the output lands. A reference-shaped skill that
    # skips them reads fine and cannot be followed.
    if DOMAIN_ROOT in folder.parents:
        headings = set(re.findall(r"^## (.+?)\s*$", text, re.M))
        for wanted in ("Inputs", "Method", "Output", "Sources"):
            if wanted not in headings:
                problems.append(f"domain skill has no ## {wanted} section")

    yaml_path = folder / "agents" / "openai.yaml"
    if not yaml_path.is_file():
        problems.append("no agents/openai.yaml")
        return problems

    yaml_text = yaml_path.read_text(encoding="utf-8")
    if "display_name" not in yaml_text:
        problems.append("openai.yaml has no interface.display_name")
    if "short_description" not in yaml_text:
        problems.append("openai.yaml has no interface.short_description")

    user_invoked = "disable-model-invocation: true" in front
    policy_set = "allow_implicit_invocation: false" in yaml_text
    if user_invoked != policy_set:
        problems.append(
            "invocation mismatch: frontmatter says user-invoked="
            f"{user_invoked}, openai.yaml policy says {policy_set}"
        )

    return problems


def main() -> int:
    """Check every skill and report the failures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="skill folders to check")
    parser.add_argument("--skills-root", default=str(SKILLS_ROOT))
    args = parser.parse_args()

    if args.paths:
        files = []
        for path in args.paths:
            candidate = Path(path)
            files.extend(
                [candidate / "SKILL.md"]
                if (candidate / "SKILL.md").is_file()
                else sorted(candidate.rglob("SKILL.md"))
            )
    else:
        files = sorted(Path(args.skills_root).rglob("SKILL.md"))

    failures = 0
    for skill_file in files:
        problems = check_skill(skill_file)
        if problems:
            failures += 1
            for problem in problems:
                print(f"FAIL {skill_file.parent}: {problem}")

    # Inter-skill calls are checked across the whole set, because a call is only
    # legal if the target exists and is model-invoked. A user-invoked skill is
    # reachable by the human alone, so no skill can call it: that instruction
    # fails at runtime, and the convention is to tell the operator to run it.
    every = sorted(Path(args.skills_root).rglob("SKILL.md"))
    present = {path.parent.name for path in every}
    user_invoked = set()
    for path in every:
        front = frontmatter(path.read_text(encoding="utf-8")) or ""
        if "disable-model-invocation: true" in front:
            user_invoked.add(path.parent.name)

    for skill_file in files:
        caller = skill_file.parent.name
        for target in sorted(skill_calls(skill_file.read_text(encoding="utf-8"))):
            if target not in present:
                failures += 1
                print(f"FAIL {skill_file.parent}: calls {target}, which does not exist")
            elif target in user_invoked:
                failures += 1
                print(
                    f"FAIL {skill_file.parent}: calls {target}, which is user-invoked "
                    "and cannot be reached by a skill; tell the operator to run it"
                )

    print(f"skills: {len(files)} checked, {failures} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
