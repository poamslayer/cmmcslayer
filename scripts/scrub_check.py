#!/usr/bin/env python3
"""Check repository files for restricted terms and private verbatim text."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path


DEFAULT_PATHS = (
    "skills",
    "reference",
    "docs/fixture",
    "README.md",
    "CONTEXT.md",
    "AGENTS.md",
)
CHECKED_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".sh", ".py"}
SKIPPED_DIRECTORIES = {".git", "node_modules", ".scratch"}
PUBLIC_RAW_PATTERNS = (
    "*.L2-3.*.md",
    "32-CFR-*.md",
    "CMMC*.md",
    "dodcui--*.md",
    "dod-cleared-*.md",
    "48-cfr-*.md",
    "eo-*.md",
    "unified-scoping-guide*",
)
PRIVATE_RAW_PATTERN = "-".join(("dis" + "cord", "coo" + "ey", "coe", "*.md"))
VERBATIM_LINE_PREFIXES = ("vault_sources", "sources:", "- wiki/", "- raw/")
URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)


@dataclass(frozen=True)
class TermPattern:
    """A configured term and its case-insensitive boundary-aware pattern."""

    term: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class CheckedFile:
    """A readable file selected for checking."""

    path: Path
    display_path: str
    lines: tuple[str, ...]


@dataclass(frozen=True)
class TermHit:
    """A blocklist or warnlist match."""

    path: str
    line: int
    term: str


@dataclass(frozen=True)
class VerbatimHit:
    """A line containing an N-gram unique to the private corpus."""

    path: str
    line: int
    window: str


def positive_integer(value: str) -> int:
    """Parse an argparse value that must be greater than zero."""
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check files for restricted terms and private verbatim text."
    )
    parser.add_argument("paths", metavar="PATH", nargs="*")
    parser.add_argument("--vault", default="~/cmmc-vault", metavar="DIR")
    parser.add_argument("--ngram", default=8, type=positive_integer, metavar="N")
    parser.add_argument("--no-verbatim", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args(argv)


def display_path(path: Path, repository: Path) -> str:
    """Return a stable repository-relative path when possible."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(repository).as_posix()
    except ValueError:
        return str(resolved)


def is_excluded(path: Path, repository: Path) -> bool:
    """Return whether a path is inside an excluded directory."""
    resolved = path.resolve()
    if any(part in SKIPPED_DIRECTORIES for part in resolved.parts):
        return True
    scrub_directory = (repository / "scripts" / "scrub").resolve()
    return resolved == scrub_directory or scrub_directory in resolved.parents


def collect_paths(
    requested_paths: Sequence[str], repository: Path, using_defaults: bool
) -> list[Path]:
    """Expand input paths into a deduplicated list of eligible files."""
    selected: dict[Path, None] = {}
    for raw_path in requested_paths:
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            path = repository / path
        if not path.exists():
            if not using_defaults:
                print(f"skip {raw_path}: not found", file=sys.stderr)
            continue
        if path.is_file():
            if (
                path.suffix.lower() in CHECKED_SUFFIXES
                and not is_excluded(path, repository)
            ):
                selected[path.resolve()] = None
            continue
        if not path.is_dir():
            print(
                f"skip {display_path(path, repository)}: not a regular file or directory",
                file=sys.stderr,
            )
            continue
        for root, directories, filenames in os.walk(path):
            root_path = Path(root)
            directories[:] = sorted(
                directory
                for directory in directories
                if directory not in SKIPPED_DIRECTORIES
                and not is_excluded(root_path / directory, repository)
            )
            for filename in sorted(filenames):
                candidate = root_path / filename
                if (
                    candidate.suffix.lower() in CHECKED_SUFFIXES
                    and not is_excluded(candidate, repository)
                ):
                    selected[candidate.resolve()] = None
    return sorted(selected, key=lambda item: display_path(item, repository))


def read_text(path: Path, shown_path: str) -> str | None:
    """Read UTF-8 text, reporting unreadable files to stderr."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"skip {shown_path}: {error}", file=sys.stderr)
        return None


def read_checked_files(paths: Iterable[Path], repository: Path) -> list[CheckedFile]:
    """Read selected files once for use by all checks."""
    checked: list[CheckedFile] = []
    for path in paths:
        shown_path = display_path(path, repository)
        text = read_text(path, shown_path)
        if text is None:
            continue
        checked.append(CheckedFile(path, shown_path, tuple(text.splitlines())))
    return checked


def scrub_lists_dir() -> Path:
    """Where the private term lists live. They are kept out of the repository on purpose,
    because the blocklist itself names the people and communities it protects."""
    return Path(os.environ.get("CMMCSLAYER_SCRUB_DIR", "~/.config/cmmcslayer/scrub")).expanduser()


def load_terms(path: Path) -> list[TermPattern]:
    """Load and compile unique configured terms from a list file."""
    text = read_text(path, str(path))
    if text is None:
        raise RuntimeError(f"cannot read required term list: {path}")
    terms: list[TermPattern] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        term = raw_line.strip()
        if not term or term.startswith("#") or term.casefold() in seen:
            continue
        seen.add(term.casefold())
        pattern = re.compile(
            rf"(?<![^\W_]){re.escape(term)}(?![^\W_])", re.IGNORECASE
        )
        terms.append(TermPattern(term, pattern))
    return terms


def find_term_hits(
    checked_files: Iterable[CheckedFile],
    block_terms: Iterable[TermPattern],
    warn_terms: Iterable[TermPattern],
) -> tuple[list[TermHit], list[TermHit]]:
    """Find all blocklist and uncited warnlist matches."""
    block_hits: list[TermHit] = []
    warn_hits: list[TermHit] = []
    block_patterns = tuple(block_terms)
    warn_patterns = tuple(warn_terms)
    for checked_file in checked_files:
        for line_number, line in enumerate(checked_file.lines, start=1):
            for configured in block_patterns:
                for _match in configured.pattern.finditer(line):
                    block_hits.append(
                        TermHit(checked_file.display_path, line_number, configured.term)
                    )
            if URL_PATTERN.search(line):
                continue
            for configured in warn_patterns:
                for _match in configured.pattern.finditer(line):
                    warn_hits.append(
                        TermHit(checked_file.display_path, line_number, configured.term)
                    )
    return block_hits, warn_hits


URL_PATTERN = re.compile(r"https?://\S+|\b[\w.-]+\.(?:gov|org|com|mil|edu|dev)\b/?\S*")

# Identifiers for public documents and their subsections. Two texts citing the
# same regulation are not copying each other, and a subsection chain such as
# (c)(2)(i)(5) tokenizes into a long run that collides by construction. The same
# goes for NIST SP 800-171 requirement identifiers, bare (3.1.18) or in the CMMC
# form (AC.L2-3.1.18): a list of them in a citation line is shared public
# numbering, and it tokenizes into a run of letters and digits that matches any
# other list of the same requirements.
CITATION_PATTERN = re.compile(
    r"\b(?:[a-z]{2}\.l[123]-)?3\.\d{1,2}\.\d{1,2}\b"
    r"|\b(?:\d{1,2}\s*cfr\s*(?:part\s*)?[\d.]+(?:\s*\([a-z0-9]+\))*"
    r"|dfars\s*[\d.\-]+"
    r"|far\s*(?:clause\s*)?[\d.\-]+"
    r"|nist\s*sp\s*[\w.\-]+"
    r"|fips\s*(?:pub\s*)?[\d\-]+)",
    re.IGNORECASE,
)


def normalize(text: str) -> list[str]:
    """Lowercase text and split it into letter-and-digit tokens.

    URLs and public document citations are removed before tokenizing. A source
    this repository and the private wiki both point at is a shared public
    reference, not copied expression, so leaving them in produces false
    verbatim matches.
    """
    stripped = URL_PATTERN.sub(" ", text.lower())
    stripped = CITATION_PATTERN.sub(" ", stripped)
    cleaned = "".join(
        character if character.isalnum() else " " for character in stripped
    )
    return cleaned.split()


def ngrams(tokens: Sequence[str], size: int) -> Iterable[tuple[str, ...]]:
    """Yield all consecutive N-grams in a token sequence."""
    for index in range(len(tokens) - size + 1):
        yield tuple(tokens[index : index + size])


def private_corpus_files(vault: Path) -> list[Path]:
    """Return all files that contribute to the private corpus."""
    files: set[Path] = set()
    wiki = vault / "wiki"
    if wiki.is_dir():
        files.update(path for path in wiki.rglob("*.md") if path.is_file())
    raw = vault / "raw"
    if raw.is_dir():
        files.update(path for path in raw.glob(PRIVATE_RAW_PATTERN) if path.is_file())
    return sorted(files)


def public_corpus_files(vault: Path, repository: Path) -> list[Path]:
    """Return all files that contribute to the public subtraction corpus."""
    files: set[Path] = set()
    raw = vault / "raw"
    if raw.is_dir():
        for path in raw.rglob("*"):
            if path.is_file() and any(
                fnmatch.fnmatchcase(path.name, pattern) for pattern in PUBLIC_RAW_PATTERNS
            ):
                files.add(path)
    reference = repository / "reference"
    if reference.is_dir():
        files.update(path for path in reference.rglob("*") if path.is_file())
    return sorted(files)


def strip_frontmatter(text: str) -> str:
    """Drop a leading YAML frontmatter block.

    A source page's frontmatter is metadata: file paths, page titles, dates,
    the names of public documents it cites. None of it is the expression the
    verbatim check exists to protect, and leaving it in makes any file that
    cites the same public talk or regulation look copied.
    """
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    return parts[2] if len(parts) == 3 else text


def build_ngram_set(
    paths: Iterable[Path], size: int, repository: Path
) -> set[tuple[str, ...]]:
    """Build an in-memory N-gram set from text files."""
    corpus: set[tuple[str, ...]] = set()
    for path in paths:
        text = read_text(path, display_path(path, repository))
        if text is None:
            continue
        corpus.update(ngrams(normalize(strip_frontmatter(text)), size))
    return corpus


def find_verbatim_hits(
    checked_files: Iterable[CheckedFile], private_ngrams: set[tuple[str, ...]], size: int
) -> list[VerbatimHit]:
    """Find checked lines containing an N-gram unique to the private corpus."""
    hits: list[VerbatimHit] = []
    for checked_file in checked_files:
        in_frontmatter = False
        frontmatter_finished = False
        for line_number, line in enumerate(checked_file.lines, start=1):
            stripped = line.strip()
            if not frontmatter_finished and stripped == "---":
                if in_frontmatter:
                    in_frontmatter = False
                    frontmatter_finished = True
                else:
                    in_frontmatter = True
                continue
            if in_frontmatter:
                continue
            if stripped.lower().startswith(VERBATIM_LINE_PREFIXES):
                continue
            tokens = normalize(line)
            if len(tokens) < size:
                continue
            for index, candidate in enumerate(ngrams(tokens, size)):
                if candidate in private_ngrams:
                    window = " ".join(tokens[index : index + 12])
                    hits.append(VerbatimHit(checked_file.display_path, line_number, window))
                    break
    return hits


def hit_to_dict(hit: TermHit | VerbatimHit) -> dict[str, str | int]:
    """Convert a hit dataclass to its JSON representation."""
    if isinstance(hit, TermHit):
        return {"path": hit.path, "line": hit.line, "term": hit.term}
    return {"path": hit.path, "line": hit.line, "window": hit.window}


def print_text_results(
    files_checked: int,
    block_hits: Iterable[TermHit],
    warn_hits: Iterable[TermHit],
    verbatim_hits: Iterable[VerbatimHit],
) -> None:
    """Print human-readable findings and the required summary."""
    blocks = list(block_hits)
    warnings = list(warn_hits)
    verbatim = list(verbatim_hits)
    for hit in blocks:
        print(f"BLOCK {hit.path}:{hit.line}: {hit.term}")
    for hit in warnings:
        print(f"WARN {hit.path}:{hit.line}: {hit.term}")
    for hit in verbatim:
        print(f'VERBATIM {hit.path}:{hit.line}: "{hit.window}"')
    print(
        f"scrub: {files_checked} files checked, {len(blocks)} block, "
        f"{len(warnings)} warn, {len(verbatim)} verbatim"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the scrub checks and return zero only when no findings exist."""
    args = parse_args(argv)
    repository = Path(__file__).resolve().parent.parent
    using_defaults = not args.paths
    requested_paths = list(args.paths) if args.paths else list(DEFAULT_PATHS)
    selected_paths = collect_paths(requested_paths, repository, using_defaults)
    checked_files = read_checked_files(selected_paths, repository)

    lists_dir = scrub_lists_dir()
    if not (lists_dir / "blocklist.txt").is_file():
        print(
            f"scrub: no private term lists at {lists_dir}; skipping the name check. "
            "Set CMMCSLAYER_SCRUB_DIR to a folder with blocklist.txt and warnlist.txt to run it.",
            file=sys.stderr,
        )
        block_terms, warn_terms = [], []
    else:
        try:
            block_terms = load_terms(lists_dir / "blocklist.txt")
            warn_terms = load_terms(lists_dir / "warnlist.txt")
        except RuntimeError as error:
            print(error, file=sys.stderr)
            return 2

    block_hits, warn_hits = find_term_hits(checked_files, block_terms, warn_terms)
    verbatim_hits: list[VerbatimHit] = []
    if not args.no_verbatim:
        vault = Path(args.vault).expanduser().resolve()
        if not vault.is_dir():
            message = f"verbatim check skipped: vault not found at {vault}"
            print(message, file=sys.stderr if args.json_output else sys.stdout)
        else:
            private = build_ngram_set(private_corpus_files(vault), args.ngram, repository)
            public = build_ngram_set(
                public_corpus_files(vault, repository), args.ngram, repository
            )
            private.difference_update(public)
            verbatim_hits = find_verbatim_hits(checked_files, private, args.ngram)

    if args.json_output:
        result = {
            "files": len(checked_files),
            "block": [hit_to_dict(hit) for hit in block_hits],
            "warn": [hit_to_dict(hit) for hit in warn_hits],
            "verbatim": [hit_to_dict(hit) for hit in verbatim_hits],
        }
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    else:
        print_text_results(
            len(checked_files), block_hits, warn_hits, verbatim_hits
        )

    return 1 if block_hits or warn_hits or verbatim_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
