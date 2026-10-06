---
name: setup-poamslayer-skills
description: "Scaffold a CMMC Level 2 engagement repo: ask about the operator's role and record the seat, lay out CONTEXT.md, scope, the OSCAL SSP and its view, evidence, policies, configure the tracker and triage labels, and check the regulatory status brief is current. Run once in an empty client repo before any other skill."
disable-model-invocation: true
---

# Setup poamslayer Skills

## Purpose

This skill turns an empty client repo into an engagement repo in the layout every other skill in this repo expects. It writes the client glossary (`CONTEXT.md`), the decision record folder (`docs/adr/`), the scope folder, the engagement's SSP as one OSCAL document (`ssp/ssp.json`, created by the `scribe` skill's create operation, with its read-only `view/`), one evidence folder per requirement 3.1.1 through 3.14.7, the policies folder, and `.scratch/` for working notes. It also configures the issue tracker and the triage labels the flows read, so `to-poam`, `triage`, `wayfinder`, and `remediate` work without anyone editing files by hand. At the end it checks that the `cmmc-regulatory-status-brief` skill is current, because advice built on a stale brief is worse than no advice.

The first thing it asks is plain: "Tell me about your role." It does not explain seats to the operator; it reads the answer and records the seat itself. The **consultant seat** runs the engagement for a client and hears the engagement vocabulary as is. The **OSC seat** is the organization seeking certification, usually its IT lead. That seat gets plain-language framing and hears who in the company each step needs. The seat is a tone switch, not a gate: both seats travel the same main flow and can reach every skill, and no skill is consultant-only. Every flow that adapts its wording reads the seat from `CONTEXT.md`, so getting it recorded once here is what makes the rest of the skills speak to the right person.

This is a prompt-driven skill with one script underneath it. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; do not assume:

- `git remote -v`: is there a remote, and is it on GitHub? Which repo?
- `CONTEXT.md`, `AGENTS.md`, and `CLAUDE.md` at the repo root: does any of them exist? Is there already an `## Agent skills` block, or a `## Seat` heading in `CONTEXT.md`?
- `ssp/` (and `ssp/ssp.json` in particular), `scope/`, `evidence/`, `policies/`, `docs/adr/`: do any of these already exist with files in them? If so, this repo has been scaffolded before or holds someone else's work. Refuse to scaffold over it unless the user says so in this conversation, and then only with `--force` (see Re-running).
- `docs/agents/`: does this skill's prior output already exist?
- `.scratch/`: a sign the local markdown tracker is already in use.
- Is the `triage` skill installed? A `triage` folder under `skills/flows/` alongside this repo's skills, or `triage` in your available skills. This decides whether the labels question is worth asking.
- The client name: take it from the repo folder name or the remote. You will show it in step 3 for correction; do not spend a question on it.

### 2. Present findings and ask

Summarise what is present and what is missing. Then ask exactly three questions, one at a time. Section A is open-ended; lead Sections B and C with the recommended answer so the user can accept it in a word.

**Section A: Role.** Ask exactly this, with no preamble and no list of seats:

> Tell me about your role.

Do not explain the two seats, name them, or offer a recommended answer. The operator describes their job in their own words; you decide the seat from what they say:

- `consultant`: they run the engagement for someone else. An outside consultant, an MSP or RPO delivering CMMC work, a vCISO serving the client.
- `osc`: they work for the organization seeking certification. The IT lead, the owner, a contracts or quality manager, an internal compliance person.

If the answer does not settle it (an employee who is also a hired consultant, an MSP running its own certification), ask one follow-up in plain words, such as "Are you doing this for your own company, or for a client?" Do not ask more than one. Record the seat; it becomes the `## Seat` line in `CONTEXT.md`, and step 3 shows it so the operator can correct it.

**Section B: Issue tracker.**

> Where should engagement tickets live? (recommended: **GitHub** if the remote is on GitHub, otherwise **local markdown**)

Explainer, one line each:

- `to-poam` creates one ticket per NOT MET requirement, labeled `poam` or `opa` plus `req:<id>`, with the objective letters, the evidence gap, and for POA&M the 180-day closeout date in the body.
- `triage` moves findings the operator did not write through the five triage labels into agent-ready tickets.
- `wayfinder` charts the engagement's contested calls as a map ticket with one child ticket per decision, and resolves them one at a time.

With GitHub, all of that is `gh issue` commands against this repo. With local markdown, it is files under `.scratch/`. Record the choice; it is passed to the script as `--tracker github` or `--tracker local`.

**Section C: Triage labels.** Ask exactly one question:

> Keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, they are written as-is. Only if the user says no, usually because the tracker already uses other names, collect the overrides so `triage` applies existing labels instead of creating duplicates, and edit `docs/agents/triage-labels.md` after the script runs.

### 3. Confirm and edit

Show the user:

- The layout tree that will be created (see "What the engagement repo looks like"), with the client name filled in.
- The seat you recorded from Section A, in one line that says what it changes (for example: "I've set you up as the organization seeking certification, so the skills will speak in plain language and tell you who in the company each step needs."). This is where a wrong call gets corrected.
- The `CONTEXT.md` draft: a one-line heading naming the client, the `## Seat` line, and the empty `## Language`, `## CUI decisions`, and `## Scope decisions` sections, which say that no terms, CUI, or scope decisions have been recorded yet.
- The `## Agent skills` block that will be added to `CLAUDE.md` or `AGENTS.md` (see step 4).

Let them correct the client name and the seat, and edit the drafts, before anything is written.

### 4. Write

Run the scaffold script from this skill's folder:

```bash
python3 <path to this skill>/scaffold.py --target . --seat <consultant|osc> --client "<client name>" --tracker <github|local>
```

The script creates the whole layout: `CONTEXT.md` with the seat, `docs/adr/`, `docs/agents/` (copied from the seed files in this folder, matching the tracker choice), `scope/`, `ssp/ssp.json`, `evidence/` with one subfolder per requirement in `reference/nist-800-171r2-requirements.json`, `policies/`, and `.scratch/`. `ssp.json` and `view/` are the SSP: there is no Markdown SSP file, asset inventory, or responsibility matrix to write. With `--tracker github` it also creates the labels with `gh label create`: the five triage labels, `poam`, `opa`, and the `wayfinder:*` labels (`wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, `wayfinder:task`). It never overwrites an existing file.

The script does not write `ssp/ssp.json` itself. It runs the scribe skill's edit command, `ssp_edit.py create`, with the client name as the system name. That writes an SSP with our profile imported, all 110 requirements present, and every assessment objective planned; copies the profile and catalog into `ssp/oscal/`; validates the result with oscal-cli; and renders `view/`. If `ssp/ssp.json` already exists, the script leaves it alone and prints `skipped: ssp/ssp.json`. Scribe needs Java 11 or later and oscal-cli 3.2.0. If either is missing, the script still writes the rest of the layout, prints `ERROR: ssp/ssp.json was not created.` with scribe's reason, and exits non-zero. Repeat the reason to the user, tell them to run `bash scripts/install_oscal_cli.sh` in the skills repo, and then re-run the script with `--force`, which adds only what is missing.

Then add the `## Agent skills` block. **Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create; do not pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists, or the other way round. If an `## Agent skills` block already exists in the chosen file, update it in place rather than appending a duplicate. Do not touch the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one line: GitHub Issues on this repo via `gh`, or local markdown under `.scratch/`]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one line: the five defaults, or the overrides collected in Section C]. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Seat

[consultant or osc]. Recorded under `## Seat` in `CONTEXT.md`; every flow reads it before it speaks.
```

If the user overrode any triage label in Section C, edit the right-hand column of `docs/agents/triage-labels.md` now.

### 5. Done

Run the status check:

```bash
python3 <path to this skill>/status-check.py
```

It reads the `as_of` date on the `cmmc-regulatory-status-brief` skill and compares it with today. If it prints a line starting with `WARNING`, repeat that line to the user verbatim and tell them to re-check the regulatory posture (the 32 CFR Part 170 phase-in, the DFARS clause status, and the current C3PAO guidance) before advising a client on it.

Then tell the user:

- Setup is complete, and which skills now read these files: `ask-poamslayer` and every flow read the seat; `to-poam`, `triage`, `wayfinder`, and `remediate` read the tracker file and the labels; `audit` and `ssp-lint` read the SSP from `ssp/ssp.json` and the folders under `evidence/`; `domain-modeling` and `grill-with-docs` read `CONTEXT.md` and `docs/adr/`.
- `ssp/ssp.json` is the SSP record, and `scribe` is the only skill that changes it: every skill that decides something calls scribe to record it. Nobody edits it by hand. The scoping skills (`cmmc-scope-boundary`, `endpoint-and-vdi-scoping`, `printer-and-ot-asset-scoping`, `esp-and-msp-scoping`, and `fips-crypto-scoping` for its out-of-scope verdicts) record assets, categories, and providers in it and read it. `to-ssp`, `ssp-statement-writer`, and `remediate` record conformity statements in it, and `requirement-applicability-matrix` records not applicable and alternative statuses with their reasons. Every skill that reads the SSP, `audit`, `ssp-lint`, and `to-poam` among them, reads `ssp.json` by asking scribe to show it.
- `view/` is generated from `ssp.json` for people to read, including the asset inventory and the responsibility matrix, and is overwritten on every change. No skill reads it and nobody edits it.
- They can edit `docs/agents/*.md` and `CONTEXT.md` directly later.
- The next step is to run `/ask-poamslayer` with "where do I start".

## What the engagement repo looks like

```
/
├── CONTEXT.md                      client glossary, scope decisions in force, and the ## Seat line
├── CLAUDE.md or AGENTS.md          carries the ## Agent skills block
├── docs/
│   ├── adr/                        determinations: enclave or enterprise, GCC High, printer category, significant change memos
│   └── agents/
│       ├── issue-tracker.md        GitHub or local markdown conventions, POA&M and OPA operations
│       ├── triage-labels.md        the five triage labels plus poam, opa, req:<id>
│       └── domain.md               how skills read CONTEXT.md and the ADRs
├── scope/                          data flow, network diagram, open items list, CUI determinations, applicability matrix, FIPS verdicts, one interview file per role
├── ssp/
│   ├── ssp.json                    the SSP record, one OSCAL document; only scribe writes it
│   └── oscal/                      the profile and catalog ssp.json imports, copied at create
├── view/                           generated from ssp.json for people; no skill reads it, nobody edits it
│   ├── asset-inventory.md
│   ├── esp-responsibility-matrix.md
│   └── requirements/3.1.1.md ...   one page per requirement
├── evidence/
│   ├── 3.1.1/                      one folder per requirement, 110 folders
│   ├── 3.1.2/
│   └── ... through 3.14.7/
├── policies/                       the policy and procedure set
└── .scratch/                       working notes, audit output, and the local tracker when one is used
```

POA&M and OPA items are not files in this tree. They are tickets on the tracker, labeled `poam` or `opa` plus `req:<id>`, with the objective letters and the evidence gap in the body.

## Seat

`CONTEXT.md` carries a heading exactly like this:

```markdown
## Seat

consultant
```

or `osc`. Every flow that adapts its wording reads this heading before it speaks. `ask-poamslayer` uses it to decide whether to use the engagement vocabulary as is or to describe each step in plain words and name who in the company it needs; it never uses the seat to hide a skill. `find-cui` uses it to choose between the consultant framing and the plain-language framing for people who have never heard the word CUI. If the heading is missing, those skills tell the operator to run this skill first, so do not remove it. To change seats, edit the one word under the heading; nothing else needs to move.

## Re-running

The script never overwrites a file. If the target already holds any of `CONTEXT.md`, `ssp/`, `scope/`, `evidence/`, or `policies/`, it stops and says so. Passing `--force` tells it to continue, and even then it only adds what is missing: `ssp/ssp.json` if there is none, an evidence folder that does not exist, a seed file under `docs/agents/` that was deleted. Existing files, including a `CONTEXT.md` with the client's terms in it and an `ssp/ssp.json` holding recorded decisions, are left exactly as they were.

Run this skill again only to switch trackers, change the seat, or fill in files that were removed. For a tracker switch, delete `docs/agents/issue-tracker.md` first so the script can write the new one. For a seat change, edit the word under `## Seat` in `CONTEXT.md` by hand; that is faster than re-running.

Rewritten from setup-matt-pocock-skills in mattpocock/skills (MIT, see skills/flows/LICENSE-mattpocock).
