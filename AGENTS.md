# cmmcslayer

Two layers of agent skills for taking a defense contractor through NIST SP 800-171 Rev 2 and CMMC Level 2. Read `CONTEXT.md` first; it is the glossary every skill uses. Read `docs/adr/0001-source-policy.md` and `docs/adr/0004-authority-tiers.md` before writing or editing any domain skill.

## Layout

- `skills/flows/`: process skills. Ported from mattpocock/skills under MIT (`grilling`, `grill-me`, `grill-with-docs`, `handoff`, `wait-what`, `research`, `wizard`, `writing-for-agents`, `domain-modeling`, `to-questionnaire`) or rewritten for a CMMC engagement (`ask-poamslayer`, `find-cui`, `wayfinder`, `to-ssp`, `to-poam`, `remediate`, `audit`, `ssp-lint`, `triage`, `scribe`).
- `skills/setup/setup-poamslayer-skills/`: the one skill to run first. Asks about the operator's role and records the seat, scaffolds the engagement repo, configures the tracker and labels.
- `skills/domain/<phase>/<skill>/`: the judgment layer, one folder per skill, grouped by engagement phase: `cui`, `scoping`, `gap`, `ssp-poam`, `evidence`, `assessment`, `m365`, `policy`, `engagement`. `skills/domain/gap/control-evidence-lookup/controls/` holds one control file per requirement.
- `reference/`: public-domain and openly licensed artifacts skills cite by relative path instead of restating. Each file has a provenance header. `reference/nist-800-171r2-requirements.json` is the only source of requirement and objective text, for the skills and for the SSP (ADR-0012).
- `docs/adr/`: decisions about this repo. `docs/specs/` (private repository only): the spec and the vault inventory. `docs/fixture/`: the fictional machine shop, its known answers, and the grader rubric. `docs/cold-runs/`: graded cold-run results. `docs/agents/`: tracker, labels, and domain-doc conventions for working on this repo. `docs/diagrams/`: the target layout diagram and the CUI determination tree.
- `scripts/`: `scrub_check.py` and helpers.

Every skill is one folder with a `SKILL.md` in the shape mattpocock/skills uses, so the repo installs with `npx skills add` now and as a Claude Code plugin later.

## Rules for editing

- No em dashes anywhere in prose. Rewrite the sentence. Two exceptions: `reference/`, which reproduces outside material verbatim and keeps the source's own punctuation, and `docs/specs/` (private repository only), which holds the spec and the vault inventory as they were written, because editing them would falsify the record of what this build was specified from.
- Domain skills carry `vault_sources` in frontmatter. Control files carry `requirement`, `family`, `confidence`, `as_of`, `vault_sources`.
- Every cited URL is in `reference/authorities.md` first, with its tier. Read `docs/adr/0004-authority-tiers.md` before citing anything: the tier limits what a source may support, and a CUI status rule needs Tier 1 or Tier 2. `verify.sh` fails on a citation missing from the register.
- Run `python3 scripts/check_links.py` when you add or change citations. It needs network access, so it is not in `verify.sh`. A citation that does not resolve is worse than a missing one: it looks like evidence and is not.
- Run `bash scripts/verify.sh` before committing. `verify.sh` needs only Python 3. The scrub check reads private term lists from `~/.config/cmmcslayer/scrub/` (or `CMMCSLAYER_SCRUB_DIR`) and skips the name check when they are missing. The public repository is a snapshot of `main` without `docs/specs/`, made with `bash scripts/publish_snapshot.sh`; run `bash scripts/verify.sh --publish` in the snapshot before pushing it. `verify.sh` runs the skill validator, the control file schema check, the router link check, the authorities register check, the scribe check and render test, the setup scaffold test, the fixture record check, the scrub check, and the em dash check. `--strict` additionally requires every skill the router names to exist, and is the release gate.
- Dependencies between skills are written as "call the Skill tool with `name`", never as a bare slash mention. User-invoked skills set `disable-model-invocation: true` and cannot be reached by other skills.
- When a skill is added, renamed, or removed, update `ask-poamslayer` so the router never lies.
- Never edit `docs/fixture/engagement/` in place; `python3 scripts/cold_run.py --skill <name>` makes the copy. A deliberate change to the fixture's starting state, such as converting its SSP, is made in a cold-run copy through the skills that own it (scribe, for the record), reviewed, and only then copied back, with its command list and reasoning recorded in `docs/cold-runs/`.
- When a cold run disagrees with the fixture's answer key, read the reasoning before deciding which is wrong. The key has been wrong before.

## Agent skills

### Issue tracker

Issues are tracked as GitHub Issues on `poamslayer/cmmcslayer` via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage labels are used as-is: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
