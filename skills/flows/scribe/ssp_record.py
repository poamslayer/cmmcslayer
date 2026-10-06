"""Read and write the engagement's SSP: the ssp/ folder of Markdown files (ADR-0012).

check_ssp.py and render_view.py in this folder import it; setup's scaffold
uses its writer. It holds the record's shape and a reader for the YAML that
frontmatter is written in.

The reader takes a strict subset of YAML, so the SSP needs nothing beyond
Python's standard library. Every value it reads is text, a list, or a mapping;
it never turns a value into a number, a date, or a boolean. Anything outside
the subset is refused with its line number rather than guessed at, so a value
it accepts means the same as it would to any YAML reader. The subset:

- block mappings, `key: value`, with keys made of letters, digits, `.`, `_`, `-`;
- block sequences, `- item`, including `- key: value` items;
- plain values on one line, or continued on more-indented lines;
- quoted values on one line, in single or double quotes;
- block values introduced by `|` or `>`, optionally with `-` or `+`;
- `[]` and `{}` for an empty list or mapping; `~`, `null`, or nothing for no value;
- comments on their own line, or after a plain value.

The record's layout:

    ssp/system.md               the system: frontmatter, then the boundary as prose
    ssp/components/<slug>.md    one per component: frontmatter, then its description
    ssp/<requirement>.md        one per requirement: statements by objective in frontmatter
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

PLACEHOLDER = "this-system"
PLACEHOLDER_TITLE = "This System"
UNWRITTEN = "Not yet written."

STATUSES = {
    "implemented": "Implemented",
    "partial": "Partial",
    "planned": "Planned",
    "alternative": "Alternative",
    "not-applicable": "Not applicable",
}
NEEDS_REASON = ("alternative", "not-applicable")

# The five CMMC asset categories, in the order the view lists them (CONTEXT.md).
CATEGORIES = {
    "cui-asset": "CUI Asset",
    "security-protection-asset": "Security Protection Asset",
    "contractor-risk-managed-asset": "Contractor Risk Managed Asset",
    "specialized-asset": "Specialized Asset",
    "out-of-scope-asset": "Out-of-Scope Asset",
}
SPECIALIZED_KINDS = {
    "iot": "IoT",
    "iiot": "IIoT",
    "ot": "OT",
    "gfe": "Government furnished equipment",
    "restricted-information-system": "Restricted information system",
    "test-equipment": "Test equipment",
}
PROVIDER_ROLES = {
    "csp": "CSP",
    "msp": "MSP",
    "mssp": "MSSP",
    "soc": "SOC provider",
    "rmm": "RMM provider",
    "other-esp": "Other ESP",
}
FEDRAMP_STATUSES = {
    "fedramp-moderate-authorized": "FedRAMP Moderate authorized",
    "fedramp-moderate-equivalent": "FedRAMP Moderate equivalent",
    "none": "Neither",
}
COMPONENT_TYPES = (
    "service", "software", "hardware", "policy", "plan", "process-procedure",
    "physical", "standard", "guidance", "interconnection", "validation",
)
SYSTEM_STATUSES = ("under-development", "operational", "under-major-modification", "disposition", "other")
IMPACTS = ("low", "moderate", "high")

SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
REQUIREMENT_ID = re.compile(r"3\.\d{1,2}\.\d{1,2}")


def default_requirements() -> Path:
    """The requirements reference in the skills repo this skill was installed from."""
    return Path(__file__).resolve().parents[3] / "reference" / "nist-800-171r2-requirements.json"


def load_requirements(path: Path) -> list[dict]:
    """The 110 requirements, each with its id, family, title, statement, and objectives."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(
            f"cannot read the requirements reference at {path}: {error}; pass --requirements with the "
            "skills repo's reference/nist-800-171r2-requirements.json"
        ) from error
    if not isinstance(data, list) or len(data) != 110:
        raise ValueError(f"{path} must list the 110 requirements")
    return data


def slugify(title: str) -> str:
    """A component slug from its title: lowercase words joined by hyphens."""
    return "-".join(re.findall(r"[a-z0-9]+", title.lower()))


# ---------------------------------------------------------------- the reader


class YamlError(ValueError):
    """Frontmatter the reader cannot take; line is 1-based within the file."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(f"line {line}: {message}")
        self.line = line


KEY = re.compile(r"([A-Za-z0-9_.][A-Za-z0-9_.-]*):(?:[ ]+|$)(.*)$")
RESERVED_START = tuple("[]{}&*!%@`|>'\"#,?")
BLOCK_HEADER = re.compile(r"([|>])([+-]?)\s*(?:#.*)?$")


@dataclass
class _Line:
    number: int
    indent: int
    text: str  # without the indent


class _Reader:
    def __init__(self, text: str, first_line: int) -> None:
        self.lines: list[_Line] = []
        self.raw: list[tuple[int, str]] = []
        for offset, raw in enumerate(text.split("\n")):
            number = first_line + offset
            self.raw.append((number, raw))
            stripped = raw.lstrip(" ")
            if raw.strip() and "\t" in raw[: len(raw) - len(raw.lstrip(" \t"))]:
                raise YamlError(number, "indent with spaces, not tabs")
            if not stripped.strip() or stripped.startswith("#"):
                continue
            self.lines.append(_Line(number, len(raw) - len(stripped), stripped.rstrip()))
        self.pos = 0

    def peek(self) -> _Line | None:
        return self.lines[self.pos] if self.pos < len(self.lines) else None

    def parse(self):
        if self.peek() is None:
            return {}
        value = self.block(self.peek().indent)
        extra = self.peek()
        if extra is not None:
            raise YamlError(extra.number, "this line is indented less than the value it belongs to")
        return value

    def block(self, indent: int):
        line = self.peek()
        if line.indent != indent:
            raise YamlError(line.number, "unexpected indent")
        if line.text == "-" or line.text.startswith("- "):
            return self.sequence(indent)
        return self.mapping(indent)

    def mapping(self, indent: int, first: tuple[_Line, str] | None = None) -> dict:
        result: dict = {}
        while True:
            if first is not None:
                line, text = first
                first = None
            else:
                line = self.peek()
                if line is None or line.indent < indent:
                    return result
                if line.indent > indent:
                    raise YamlError(line.number, "unexpected indent")
                if line.text == "-" or line.text.startswith("- "):
                    raise YamlError(line.number, "a list item where a key was expected")
                self.pos += 1
                text = line.text
            match = KEY.match(text)
            if not match:
                raise YamlError(line.number, f'expected "key: value", found "{text}"')
            key, rest = match.group(1), match.group(2)
            if key in result:
                raise YamlError(line.number, f'the key "{key}" appears twice')
            result[key] = self.value_after_key(line, indent, rest)

    def value_after_key(self, line: _Line, indent: int, rest: str):
        rest_clean = _strip_comment(rest, line.number) if rest and rest[0] not in "'\"" else rest
        if rest_clean == "":
            nxt = self.peek()
            if nxt is not None and nxt.indent > indent:
                return self.block(nxt.indent)
            if nxt is not None and nxt.indent == indent and (nxt.text == "-" or nxt.text.startswith("- ")):
                return self.sequence(indent)
            return None
        header = BLOCK_HEADER.match(rest_clean)
        if header:
            return self.block_scalar(line, indent, header.group(1), header.group(2))
        return self.scalar(line, rest, indent)

    def sequence(self, indent: int) -> list:
        result = []
        while True:
            line = self.peek()
            if line is None or line.indent < indent:
                return result
            if line.indent > indent:
                raise YamlError(line.number, "unexpected indent")
            if not (line.text == "-" or line.text.startswith("- ")):
                return result
            self.pos += 1
            rest = line.text[1:].lstrip(" ")
            content_indent = indent + (len(line.text) - len(rest))
            if rest == "" or rest.startswith("#"):
                nxt = self.peek()
                if nxt is not None and nxt.indent > indent:
                    result.append(self.block(nxt.indent))
                else:
                    result.append(None)
                continue
            if rest == "-" or rest.startswith("- "):
                raise YamlError(line.number, "write a nested list on its own indented lines")
            if KEY.match(rest) and rest[0] not in "'\"":
                result.append(self.mapping(content_indent, first=(line, rest)))
                continue
            header = BLOCK_HEADER.match(rest)
            if header:
                result.append(self.block_scalar(line, indent, header.group(1), header.group(2)))
                continue
            result.append(self.scalar(line, rest, indent))

    def scalar(self, line: _Line, text: str, parent_indent: int):
        if text[0] == '"':
            value, end = _double_quoted(text, line.number)
            _no_trailing(text[end:], line.number)
            self._no_continuation(parent_indent, "a quoted value")
            return value
        if text[0] == "'":
            value, end = _single_quoted(text, line.number)
            _no_trailing(text[end:], line.number)
            self._no_continuation(parent_indent, "a quoted value")
            return value
        text = _strip_comment(text, line.number)
        if text in ("[]", "{}"):
            self._no_continuation(parent_indent, "an empty list or mapping")
            return [] if text == "[]" else {}
        _check_plain(text, line.number)
        parts = [text]
        while True:
            nxt = self.peek()
            if nxt is None or nxt.indent <= parent_indent:
                break
            self.pos += 1
            more = _strip_comment(nxt.text, nxt.number)
            _check_plain(more, nxt.number, continuation=True)
            parts.append(more)
        value = " ".join(parts)
        if len(parts) == 1 and value in ("~", "null", "Null", "NULL"):
            return None
        return value

    def _no_continuation(self, parent_indent: int, what: str) -> None:
        nxt = self.peek()
        if nxt is not None and nxt.indent > parent_indent:
            raise YamlError(nxt.number, f"{what} must stay on one line; use | or > for a value that runs over several")

    def block_scalar(self, line: _Line, parent_indent: int, style: str, chomp: str) -> str:
        # Read raw lines after the header, so blank lines inside the value are kept.
        start = next(i for i, (number, _) in enumerate(self.raw) if number == line.number) + 1
        body: list[str] = []
        content_indent = None
        last_number = line.number
        for number, raw in self.raw[start:]:
            if not raw.strip():
                body.append("")
                continue
            current = len(raw) - len(raw.lstrip(" "))
            if content_indent is None:
                if current <= parent_indent:
                    break
                content_indent = current
            if current < content_indent:
                if current > parent_indent:
                    raise YamlError(number, "a line in this block value is indented less than its first line")
                break
            if style == ">" and current > content_indent:
                raise YamlError(number, "a > value cannot have lines indented more than its first line; use |")
            body.append(raw[content_indent:])
            last_number = number
        while self.pos < len(self.lines) and self.lines[self.pos].number <= last_number:
            self.pos += 1
        # Trailing blank lines belong to the value only for chomping to decide.
        trailing = 0
        while body and body[-1] == "":
            body.pop()
            trailing += 1
        if style == "|":
            text = "\n".join(body)
        else:
            text = ""
            for i, piece in enumerate(body):
                if i == 0:
                    text = piece
                elif piece == "":
                    text += "\n"
                elif body[i - 1] == "":
                    text += piece
                else:
                    text += " " + piece
        if not body:
            return "" if chomp != "+" else "\n" * trailing
        if chomp == "-":
            return text
        if chomp == "+":
            return text + "\n" + "\n" * trailing
        return text + "\n"


def _strip_comment(text: str, number: int) -> str:
    """A plain value without a trailing comment: YAML starts one at a space and #."""
    if text.startswith("#"):
        return ""
    cut = text.find(" #")
    return (text[:cut] if cut >= 0 else text).rstrip()


def _check_plain(text: str, number: int, continuation: bool = False) -> None:
    if not continuation and text.startswith(RESERVED_START):
        raise YamlError(number, f'a value starting with "{text[0]}" must be quoted')
    if not continuation and (text == "-" or text.startswith("- ")):
        raise YamlError(number, "a list item where a value was expected")
    if ": " in text or text.endswith(":"):
        raise YamlError(number, 'a value containing ": " or ending in ":" must be quoted')
    if text.startswith("#"):
        raise YamlError(number, "a value starting with # must be quoted")


def _no_trailing(rest: str, number: int) -> None:
    rest = rest.strip()
    if rest and not rest.startswith("#"):
        raise YamlError(number, f'unexpected text after the closing quote: "{rest}"')


ESCAPES = {'"': '"', "\\": "\\", "/": "/", "n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "0": "\0", " ": " "}


def _double_quoted(text: str, number: int) -> tuple[str, int]:
    out = []
    i = 1
    while i < len(text):
        ch = text[i]
        if ch == '"':
            return "".join(out), i + 1
        if ch == "\\":
            i += 1
            if i >= len(text):
                break
            esc = text[i]
            if esc in ESCAPES:
                out.append(ESCAPES[esc])
            elif esc in "xuU":
                width = {"x": 2, "u": 4, "U": 8}[esc]
                digits = text[i + 1 : i + 1 + width]
                if len(digits) != width or not all(c in "0123456789abcdefABCDEF" for c in digits):
                    raise YamlError(number, f"a \\{esc} escape needs {width} hex digits")
                out.append(chr(int(digits, 16)))
                i += width
            else:
                raise YamlError(number, f"\\{esc} is not an escape YAML knows")
        else:
            out.append(ch)
        i += 1
    raise YamlError(number, "a double-quoted value is not closed on its line")


def _single_quoted(text: str, number: int) -> tuple[str, int]:
    out = []
    i = 1
    while i < len(text):
        if text[i] == "'":
            if text[i + 1 : i + 2] == "'":
                out.append("'")
                i += 2
                continue
            return "".join(out), i + 1
        out.append(text[i])
        i += 1
    raise YamlError(number, "a single-quoted value is not closed on its line")


def parse_yaml(text: str, first_line: int = 1):
    """Read frontmatter text; first_line numbers its first line in errors."""
    return _Reader(text, first_line).parse()


def split_frontmatter(text: str) -> tuple[str, str, int]:
    """(frontmatter, body, line number of the frontmatter's first line). Raises YamlError."""
    if not (text.startswith("---\n") or text.startswith("---\r\n")):
        raise YamlError(1, "the file must open with a --- line and YAML frontmatter")
    lines = text.splitlines(keepends=True)
    for index in range(1, len(lines)):
        if lines[index].rstrip("\r\n") == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :]), 2
    raise YamlError(1, "the frontmatter has no closing --- line")


def read_file(path: Path) -> tuple[dict, str]:
    """A record file's frontmatter, which must be a mapping, and its body."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise YamlError(1, f"not UTF-8 text: {error}") from error
    front, body, first = split_frontmatter(text)
    data = parse_yaml(front, first)
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise YamlError(first, "the frontmatter must be a mapping of keys to values")
    return data, body


# ---------------------------------------------------------------- the writer

PLAIN_SAFE = re.compile(r"[A-Za-z0-9(][^\n\r\t]*")
LOOKS_TYPED = re.compile(
    r"(?i:~|null|true|false|yes|no|on|off|y|n)$|[-+]?(\d[\d_]*)?\.?\d+([eE][-+]?\d+)?$|\d{4}-\d\d-\d\d|0[xob]"
)


def _plain_ok(text: str) -> bool:
    return bool(
        PLAIN_SAFE.fullmatch(text)
        and text == text.strip()
        and ": " not in text
        and " #" not in text
        and not text.endswith(":")
        and not LOOKS_TYPED.match(text)
    )


def dump_scalar(value) -> str:
    if value is None:
        return "~"
    text = str(value)
    return text if _plain_ok(text) else json.dumps(text, ensure_ascii=False)


def dump_yaml(data, indent: int = 0) -> str:
    """Block-style YAML the reader above takes back exactly, keys in the order given."""
    pad = " " * indent
    lines: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) and value:
                lines.append(f"{pad}{key}:")
                lines.append(dump_yaml(value, indent + 2).rstrip("\n"))
            elif isinstance(value, list) and value:
                lines.append(f"{pad}{key}:")
                lines.append(dump_yaml(value, indent + 2).rstrip("\n"))
            elif isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}: {'{}' if isinstance(value, dict) else '[]'}")
            else:
                lines.append(f"{pad}{key}: {dump_scalar(value)}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item:
                inner = dump_yaml(item, indent + 2).rstrip("\n").split("\n")
                lines.append(f"{pad}- {inner[0][indent + 2:]}")
                lines.extend(inner[1:])
            elif isinstance(item, (dict, list)) and item:
                raise ValueError("the writer does not nest a list directly in a list")
            elif isinstance(item, (dict, list)):
                lines.append(f"{pad}- {'{}' if isinstance(item, dict) else '[]'}")
            else:
                lines.append(f"{pad}- {dump_scalar(item)}")
    else:
        raise ValueError("dump_yaml takes a mapping or a list")
    return "\n".join(lines) + "\n"


def record_text(frontmatter: dict, body: str) -> str:
    """A record file: frontmatter between --- lines, then the body."""
    body = body.strip("\n")
    return f"---\n{dump_yaml(frontmatter)}---\n" + (f"\n{body}\n" if body else "")


def requirement_body(requirement: dict) -> str:
    """The text a requirement file carries for people. It is never parsed."""
    lines = [f"# {requirement['id']} {requirement['title']}", "", requirement["statement"], "", "## Objectives", ""]
    lines += [f"- {requirement['id']}[{o['letter']}] {o['text']}" for o in requirement["objectives"]]
    return "\n".join(lines)


def placeholder_statement() -> dict:
    return {"component": PLACEHOLDER, "status": "planned", "statement": UNWRITTEN}


def blank_requirement(requirement: dict) -> str:
    """A requirement file with every objective planned on the placeholder."""
    front = {
        "requirement": requirement["id"],
        "family": requirement["family"],
        "objectives": {o["letter"]: [placeholder_statement()] for o in requirement["objectives"]},
    }
    return record_text(front, requirement_body(requirement))


def blank_system(system_name: str) -> str:
    front = {
        "system-name": system_name,
        "status": "under-development",
        "information-types": [
            {
                "title": "Controlled Unclassified Information",
                "description": "CUI the organization receives or creates under its DoD contracts.",
                "confidentiality": "moderate",
                "integrity": "moderate",
                "availability": "moderate",
            }
        ],
        "users": [{"title": "System user"}],
    }
    body = "# Authorization boundary\n\nNot yet drawn; scoping records it."
    return record_text(front, body)


# ---------------------------------------------------------------- the record


@dataclass
class Component:
    slug: str
    path: Path
    data: dict
    description: str

    @property
    def title(self) -> str:
        return str(self.data.get("title") or self.slug)

    @property
    def provider(self) -> dict | None:
        provider = self.data.get("provider")
        return provider if isinstance(provider, dict) else None

    @property
    def assets(self) -> list[dict]:
        assets = self.data.get("assets")
        return [a for a in assets if isinstance(a, dict)] if isinstance(assets, list) else []

    def asset_category(self, asset: dict) -> str | None:
        """The asset's category, or its component's when it gives none."""
        return asset.get("category") or self.data.get("category")


@dataclass
class Record:
    engagement: Path
    requirements: list[dict]
    system: dict | None = None
    system_body: str = ""
    components: dict[str, Component] = field(default_factory=dict)
    statements: dict[str, dict] = field(default_factory=dict)  # requirement id -> frontmatter
    problems: list[str] = field(default_factory=list)  # files that could not be read

    def title_of(self, slug: str) -> str:
        if slug == PLACEHOLDER:
            return PLACEHOLDER_TITLE
        component = self.components.get(slug)
        return component.title if component else f"{slug} (a component the record does not have)"

    def objective_entries(self, requirement_id: str, letter: str) -> list[dict]:
        objectives = (self.statements.get(requirement_id) or {}).get("objectives")
        entries = objectives.get(letter) if isinstance(objectives, dict) else None
        return [e for e in entries if isinstance(e, dict)] if isinstance(entries, list) else []


def is_unwritten(entry: dict) -> bool:
    return entry.get("status") == "planned" and entry.get("statement") == UNWRITTEN


def relative(engagement: Path, path: Path) -> str:
    try:
        return str(path.relative_to(engagement))
    except ValueError:
        return str(path)


def load(engagement: Path, requirements: list[dict]) -> Record:
    """Read every file of the SSP. Files that do not parse are named in record.problems."""
    record = Record(engagement, requirements)
    ssp = engagement / "ssp"
    system = ssp / "system.md"
    if system.is_file():
        try:
            record.system, record.system_body = read_file(system)
        except YamlError as error:
            record.problems.append(f"{relative(engagement, system)}: {error}")
    for path in sorted((ssp / "components").glob("*.md")):
        try:
            data, body = read_file(path)
        except YamlError as error:
            record.problems.append(f"{relative(engagement, path)}: {error}")
            continue
        record.components[path.stem] = Component(path.stem, path, data, body.strip())
    for requirement in requirements:
        path = ssp / f"{requirement['id']}.md"
        if not path.is_file():
            continue
        try:
            record.statements[requirement["id"]], _ = read_file(path)
        except YamlError as error:
            record.problems.append(f"{relative(engagement, path)}: {error}")
    return record
