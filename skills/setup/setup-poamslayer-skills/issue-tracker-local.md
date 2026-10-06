# Issue tracker: Local Markdown

Issues and tickets for this engagement repo live as markdown files in `.scratch/`.

## Conventions

- One effort per directory: `.scratch/<effort-slug>/`
- The spec, when there is one, is `.scratch/<effort-slug>/spec.md`
- Tickets are one file each at `.scratch/<effort-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each ticket file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<effort-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the ticket number directly.

## POA&M and OPA operations

Used by `to-poam`, `remediate`, and `audit`. One file per NOT MET requirement under `.scratch/poam/`.

- **File**: `.scratch/poam/<id>-<slug>.md`, for example `.scratch/poam/3.1.1-shop-floor-user-list.md`. The first line is a heading in the form `<id> <objective letters> <short gap>`.
- **Header lines**, near the top: `Type: poam` or `Type: opa`; `Requirement: <id>`; `Status: open`, `Status: in-progress`, or `Status: closed`. These stand in for the `poam`, `opa`, and `req:<id>` labels on GitHub. `in-progress` is the local stand-in for the assignee on a real tracker: `remediate` sets it when it claims the ticket, before doing any work, so a second session skips it.
- **Body**: the objective letters that are NOT MET, one line each with the evidence gap `audit` reported. For a `poam` file, add one line `Closeout date: <Conditional CMMC Status Date plus 180 days>`. An `opa` file carries no closeout date and no milestones; it records the temporary deficiency, when it started, and the mitigation in place.
- **Routing**: `poam-or-opa-router` decides the type and `sprs-score-and-poam-eligibility` checks the gates before the file is created. A requirement that is not POA&M eligible cannot take `Type: poam`.
- **Close**: only when `audit` reports every objective MET. Append the audit result under `## Comments`, then set `Status: closed`. Never close on a promise or a partial fix. A ticket whose fix is written but not yet carried out stays `in-progress`: a documented procedure is not the practice the objective asks for, and the re-audit will say so.

## Wayfinding operations

Used by `wayfinder`. The **map** is a file with one **child** file per ticket. The child tickets are the engagement's contested calls: enclave or enterprise, GCC High, the printer category, VPN as remote access, the MSP category, and whatever the grilling surfaces. Each child names the domain skill that resolves it.

- **Map**: `.scratch/<effort>/map.md` (the Notes / Decisions-so-far / Fog body).
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (the ADR path, or a gist and link) to the map's Decisions-so-far in `map.md`.
