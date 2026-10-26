---
name: ask-poamslayer
description: Ask which skill or flow fits your situation in a NIST SP 800-171 or CMMC Level 2 engagement. A router over the skills in this repo.
disable-model-invocation: true
---

# Ask poamslayer

You do not remember every skill, so ask. Say where you are and what just arrived, and this router names the next skill.

Before you say what a skill does, or recommend skipping a step, read that skill's SKILL.md. The summaries here are for orientation only.

A **flow** is a path through the skills. Most engagements travel one **main flow**, and two **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

## Read the seat first

The engagement repo's `CONTEXT.md` records the **seat** under a `## Seat` heading: `consultant` or `osc`. When no seat is recorded, use the OSC wording: plain words, and who in the company each step needs.

**The seat is a tone switch, not a gate.** Both seats travel the same main flow and can reach every skill; the seat changes how an answer is worded and which Seat notes a skill leans on, never which skills are offered. Do not hide a skill from either seat.

- **Consultant seat**: use the engagement vocabulary as is.
- **OSC seat**: the operator is usually an IT lead who has never heard the word CUI said out loud. Say what each skill will ask them to do in plain words, and say who in the company each step needs (contracts, engineering, the shop floor, the owner). Mention `/wayfinder` only when the open decisions are too many for one sitting.

## No engagement repo yet

Routing never waits for setup. Answer every question with its route, whether or not an engagement repo exists.

Setup is needed only before a skill that writes to the engagement repo: the main-flow stages, `scribe`, and the flows that leave files behind. When the route lands on one of those and there is no repo, name the route first, then say that `/setup-poamslayer-skills` comes before it, and why: the skill needs somewhere to keep what it learns.

A quick question with no repo behind it is not a request to start an engagement. For "do we need Level 2 if nothing is marked CUI?", "is this document CUI?", "what satisfies 3.x.y?" or "do we have to do this?", route to the skill that answers it and let that skill answer from the facts in the message. `/grill-me` and `/research` never need a repo.

## Outside what these skills cover

Say so plainly instead of stretching a nearby route. These skills do not cover:

- **Level 1**: its requirements and the Level 1 self-assessment. Never send a Level 1 company down the Level 2 path. If it is not sure it has no CUI, the question is "do we have CUI?", which routes to `/find-cui`.
- **Level 3** and NIST SP 800-172.
- **SPRS mechanics**: logins, CAGE and NCAGE codes, entering a score. Computing the score is covered by `sprs-score-and-poam-eligibility`.
- **Contract vehicles**: which agreement to sign before sending CUI to a vendor. What the vendor needs once it holds CUI is covered by `flowdown-level-determination`.
- **Comparing products or vendors**: GRC tools, MSPs, consultants. A product that will hold CUI still goes through gate 1 of `significant-change-determination`.
- **Prices**: what an assessment, a consultant or a tool costs.
- **Careers and exams**: CCP, CCA, the Cyber AB.

When a question is outside, `/research` can still find the primary source and leave a cited file.

## The first question

**"Do we even have CUI, and where is it?"** always routes to **`/find-cui`**, before scoping, before a gap assessment, before buying anything. Nobody draws a boundary around data they have not found. If the operator asks about scope, enclaves, GCC High, or an SPRS score and there is no `scope/data-flow.md` in the engagement repo, send them to `/find-cui` first and say why.

## The main flow: find CUI to continuous monitoring

The route most engagements travel, in order. Each stage names the flow that drives it and the domain skills it calls. Where you are is the first stage whose artifacts are missing from the engagement repo.

1. **Find CUI**: **`/find-cui`**. Take the intake facts first (every contract's clause list read firsthand, the ITAR and EAR answer, foreign ownership, the SPRS score and its evidence, how the MSP connects), train and record attendance as 3.2.1 evidence, interview by role with `to-questionnaire` (IT last), determine with `cui-determination-workflow`, and with `cui-re-use-triage` for the documents the company creates from CUI it received, map with `cui-data-flow-mapping`. Leaves `scope/intake.md`, `scope/data-flow.md`, one interview file per role, and CUI terms in `CONTEXT.md`. Overlays for a marked document, an export question, or a sub asking what level it needs: `cui-marking-check`, `export-control-overlay`, `flowdown-level-determination`.
2. **Scope**: walk the site in nine areas and place every asset with `cmmc-scope-boundary`; test a claimed separation with `logical-separation-test`; laptops, thin clients, home networks, and VPNs with `endpoint-and-vdi-scoping`; printers and shop-floor machines with `printer-and-ot-asset-scoping`; MSPs, RMMs, and SaaS with `esp-and-msp-scoping`; once the assets are recorded, draw the network diagram of the scope with `cmmc-boundary-diagram`. Two decisions are large enough to be their own ADRs: `enclave-or-enterprise-decision` and `gcc-high-decision`. Every scoping skill records its components, assets, categories, and providers in `ssp/components/` through `scribe`, and `fips-crypto-scoping` records the network devices its device tree clears as out of scope; people read the inventory in the generated `view/asset-inventory.md` and the responsibility matrix in `view/esp-responsibility-matrix.md`. Leaves `scope/network-diagram.drawio` beside the `scope/network-diagram.md` notes, `scope/open-items.md`, `scope/fips-verdicts.md` when FIPS was scoped, and ADRs. When the contested decisions are too many for one session, chart them with **`/wayfinder`** (see On-ramps).
3. **Gap**: decide which requirements apply per component with `requirement-applicability-matrix`, which records each not applicable and alternative status, with its reason, in the requirement files under `ssp/` through `scribe`; separate what can fail you from what cannot with `normative-requirement-test`; ask "what satisfies 3.x.y" with `control-evidence-lookup`; stop spending on controls nobody asked for with `over-engineering-guard`; compute the score and the POA&M split with `sprs-score-and-poam-eligibility`. Then run **`/audit`** per requirement: a subagent reads the engagement repo and the control file and reports each objective MET or NOT MET with the letter and the evidence gap. Audit writes to `.scratch/audit/`.
4. **Remediate**: **`/to-poam`** turns every NOT MET into a ticket routed POA&M or OPA by `poam-or-opa-router`, gated by `sprs-score-and-poam-eligibility`. **`/remediate`** takes one ticket, drives the fix, records the statements for the objectives it closed through `scribe`, runs `/audit` again, and closes the ticket only when every objective is MET. `/audit` calls `over-engineering-guard` when a fix goes past the bar. Between tickets, `/clear` context; each ticket stands alone.
5. **Document**: **`/to-ssp`** turns the grilling, the scoping record, and the wayfinder decisions into conformity statements, one per objective and component, through `ssp-statement-writer`, and records them in the requirement files under `ssp/` through `scribe`; people read them in `view/requirements/`. Unconfirmed facts go on `scope/open-items.md`, and their objectives are recorded planned (ADR-0010). Policies come after procedures: `policy-after-procedure-sequencing`. A machine shop sending a package to a finisher gets `supplier-cui-release-procedure`. Then **`/ssp-lint`** reviews the SSP on two axes, house style and evidence, and rejects any "to be confirmed" text inside a statement.
6. **Evidence**: `evidence-package-builder` assembles evidence per objective in final form and builds `evidence/continuous-monitoring-calendar.md` from the recurring activities. `fips-crypto-scoping` finds the actual encryption points before anyone buys FIPS switches. `exchange-dlp-enclave-pattern` when email is the enclave boundary.
7. **Mock**: `mock-assessment-runbook` runs against the 320 objectives, gated on prerequisites (an SSP, a drawn scope, a segmented network). `top-failed-requirements-drill` puts the prep time where assessors fail people, and carries the 3.6.3 tabletop scaffold.
8. **Assessment**: `c3pao-selection-vetting` before the contract is signed. `cmmc-regulatory-status-brief` for what is in force today, with its as-of date; setup warns when it is older than 60 days.
9. **Closeout**: POA&M items close through **`/remediate`** and **`/audit`** inside the 180-day clock. `poam-or-opa-router` keeps a temporary deficiency found after certification off the POA&M and on an OPA.
10. **Continuous monitoring**: the calendar from stage 6, worked on cadence. A proposed change to the certified environment goes through `significant-change-determination` first (see On-ramps).

### Context hygiene

Keep the grilling, the scoping decisions, and `/to-ssp` in one unbroken context window where you can, so the statements carry the reasoning. Each `/remediate` starts fresh from its ticket. The limit is the smart zone (roughly 150k tokens); if a session approaches it before `/to-ssp`, `/compact` at the nearest phase boundary rather than pushing on degraded. See Phase boundaries.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Findings you did not create**: a mock assessment report, a C3PAO's readiness review, a prime's questionnaire, an auditor's list. Route to **`/triage`**. It moves each finding through the five labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`) into agent-ready tickets that **`/remediate`** later picks up. Triage is only for findings someone else wrote; tickets `/to-poam` produced are already agent-ready, so do not triage them. A finding that recommends a control no objective requires is a `wontfix` with an `over-engineering-guard` note.

- **A proposed change to a certified or assessed environment**: a new SaaS tool, a swapped MSP, a new site, a migration. Route to **`significant-change-determination`** before anything is bought or deployed.

  **Check first whether anything has been assessed yet.** If the engagement has no SSP and no completed assessment, there is no certified state to change, so this is not a significant change question. It is still gated: run gate 1 of `significant-change-determination` on its own, because a cloud service that will hold CUI needs FedRAMP Moderate authorization or equivalency whatever stage the engagement is at, and a tool that fails that gate cannot be used in scope at any stage. Then hand the rest to stage 2 as ordinary scoping work, `esp-and-msp-scoping` for a provider or `cmmc-scope-boundary` for an asset. It runs four gates (can the service be used in scope at all; was the capability in the assessed environment; which scope artifacts shift; how many families gain new evidence) and says plainly that the Affirming Official decides. A change that passes lands as an ADR and a change-management package; a significant one merges back at stage 2.

- **An engagement too big for one session**: too many contested calls to settle in one sitting (enclave or enterprise, GCC High, the printer category, VPN as remote access, the MSP category, and whatever the grilling surfaces). Route to **`/wayfinder`**. It charts a map of decision tickets on the engagement tracker, each naming the domain skill that resolves it, and resolves them one at a time, producing decisions and ADRs, not deliverables. When the map clears it hands off to **`/to-ssp`**; it does not build.

## Vocabulary underneath

Two model-invoked references run beneath the other skills.

- **`/domain-modeling`** keeps the engagement `CONTEXT.md` a clean glossary: challenge a fuzzy term ("in scope" doing three jobs), record a hard-to-reverse call as an ADR. `/grill-with-docs` drives it; `/find-cui` writes the CUI decisions through it.
- **`control-evidence-lookup`** is the single source for what satisfies a requirement: accepted, rejected, over-engineering, edge cases, and evidence examples, per requirement, with assessor disagreement preserved and thin requirements marked low confidence. `/audit`, `over-engineering-guard`, and `evidence-package-builder` all read it.

## The record

The engagement's SSP is the `ssp/` folder of Markdown files with YAML frontmatter, and it is the record (ADR-0012): `ssp/system.md` for the system, one file per component in `ssp/components/`, named by its slug, and one file per requirement, such as `ssp/3.5.3.md`, holding its statements by objective. **`scribe`** is the only skill that changes it: any skill that decides something calls the Skill tool with `scribe` to record the decision, and scribe checks every change with `check_ssp.py` and refuses one that fails. A skill that needs to know what the SSP says reads the files directly. The Markdown under `view/` is generated from the record for people to read; no skill reads it and nobody edits it. Scribe records components, assets with their categories, providers with their FedRAMP status, and one conformity statement per objective and component with its implementation status.

## Phase boundaries

A **phase** is a chunk of work inside a session: the interviews, the scoping, the SSP writing, the audit. At the boundary between two you have five options, and choosing is the fuzziest decision on this map:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window, when nothing here matters to what is next.
- **`/handoff`** writes a portable Markdown file. Narrow: for a new harness, a new directory (the engagement repo from the skills repo, or one client from another), a colleague, or a side task found mid-phase.
- **Subagent**: send a tightly scoped task to its own window. `/audit` is the standard case.
- **`/compact`** compresses this context and seeds a fresh session with it. The default, at the bottom of the tree, not the first reach.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered tree and the reasoning. Decide at a boundary; mid-phase, continue or split the rest into subagents.

## Standalone

Off the main flow entirely.

- **`/grill-me`**: the relentless interview, stateless. For sharpening a plan, a client proposal, a position you will argue with an assessor, with no repo under it. Inside an engagement repo use `/grill-with-docs` instead, which runs the same interview and leaves `CONTEXT.md` and ADRs behind.
- **`/grilling`** is the interview primitive: rounds, the frontier, facts are the agent's job and decisions are yours. `/find-cui`, `/triage`, and `/wayfinder` run it internally.
- **`/research`** delegates reading to a background agent that works from primary sources (the eCFR, the DoD CIO guides, the CUI Registry, vendor FedRAMP listings) and leaves a cited Markdown file in the repo. Take the file into `/grill-with-docs`.
- **`/to-questionnaire`** writes the questions for someone whose head holds the answer: the contracts manager, the shop lead, the MSP, the prime's buyer. `/find-cui` runs it once per role; reach for it directly whenever a fact lives with someone else.
- **`/wizard`** generates an interactive script for steps only a human can take: enabling a tenant setting in a vendor portal, turning on FIPS mode, configuring a Conditional Access policy, provisioning an account. Model-invoked, so the agent reaches for it when it hits a wall only you can pass.
- **`/wait-what`** re-pitches a message that did not land, in plain English, with the engagement `CONTEXT.md` vocabulary. Use it mid-conversation inside any skill.
- **`/writing-for-agents`** is the reference for writing documents agents consume: skills, `AGENTS.md`, pointed-at docs. For maintaining this repo, not for engagements.
- **`cmmc-regulatory-status-brief`**: what is in force today, with an as-of date. Read it before advising anyone to wait.

## Precondition

**`/setup-poamslayer-skills`**: run once in an empty client repo before anything else. It asks about your role and records the seat, scaffolds the engagement layout (`CONTEXT.md`, `docs/adr/`, `scope/`, `ssp/` with the system file and the 110 requirement files in scribe's shape, which are the whole SSP, the generated `view/`, `evidence/` with one folder per requirement, `policies/`, `.scratch/`), configures the issue tracker and the five triage labels, and warns when the regulatory status brief is stale.

## Quick routes

| The operator says | Route |
|---|---|
| "Do we even have CUI?" or "where is the CUI?" | `/find-cui` |
| "Is this document CUI?" | `cui-determination-workflow` |
| "Is our own paperwork CUI because we made it from the customer's drawing?" | `cui-re-use-triage`, which sends each document to `cui-determination-workflow` |
| "Our prime wants Level 2 but we never get anything marked CUI" | `cui-determination-workflow` (step 10, for a sub that cannot see above its prime), then `flowdown-level-determination`, then `enclave-or-enterprise-decision` |
| "Is this asset in scope?" | `cmmc-scope-boundary` |
| "Draw the network diagram" or "we need a boundary diagram" | `cmmc-boundary-diagram`, after `cmmc-scope-boundary` has recorded the assets |
| "Does our VLAN take the shop floor out of scope?" | `logical-separation-test` |
| "Are laptops or home PCs in scope?" | `endpoint-and-vdi-scoping` |
| "What about the printer or the CNC?" | `printer-and-ot-asset-scoping` |
| "Where does our MSP land?" | `esp-and-msp-scoping` |
| "Enclave or the whole company?" | `enclave-or-enterprise-decision` |
| "Do we need GCC High?" | `gcc-high-decision` |
| "We want to add a SaaS tool" or "swap the MSP", after assessment | `significant-change-determination` |
| "We want to add a SaaS tool", before any assessment | Gate 1 of `significant-change-determination`, then `esp-and-msp-scoping` |
| "What satisfies 3.x.y?" | `control-evidence-lookup` |
| "Do we have to do this?" (vendor quotes the guide) | `normative-requirement-test`, then `over-engineering-guard` |
| "What is our score?" or "can we POA&M this?" | `sprs-score-and-poam-eligibility` |
| "Assess 3.x.y" | `/audit` |
| "Turn the NOT METs into tickets" | `/to-poam` |
| "Work this ticket" | `/remediate` |
| "Write the SSP" | `/to-ssp` |
| "Review the SSP" | `/ssp-lint` |
| "Record this in the SSP" | `scribe` |
| "We got a mock report" or "the prime sent findings" | `/triage` |
| "What evidence do we show for 3.x.y?" | `evidence-package-builder` |
| "Do we need FIPS switches?" | `fips-crypto-scoping` |
| "Can email stay in one tenant?" | `exchange-dlp-enclave-pattern` |
| "We need policies" | `policy-after-procedure-sequencing` |
| "Sending a package to the finisher" | `supplier-cui-release-procedure` |
| "Are we ready?" | `mock-assessment-runbook`, then `top-failed-requirements-drill` |
| "Which C3PAO?" | `c3pao-selection-vetting` |
| "Is CMMC still happening?" | `cmmc-regulatory-status-brief` |
| "New client" or "what do I ask in the first meeting?" | `/setup-poamslayer-skills` if there is no engagement repo, then `/find-cui`, starting at its intake step |
| "What do we inventory?" | `cmmc-scope-boundary`, starting at its discovery walk |
| "Too many open decisions" | `/wayfinder` |
| "Am I overlooking something?" about a position they hold | `/grill-me` |
| "We only need Level 1" or "do I need an SSP for Level 1?" | Outside: Level 1 is not covered; `/research`. If they are unsure there is no CUI, `/find-cui` |
| "We need to send CUI to a vendor or an outside drafter" | `flowdown-level-determination`, then `supplier-cui-release-procedure` |
| "Which GRC tool, MSP or consultant?" | Outside for the comparison; gate 1 of `significant-change-determination` for any product that will hold CUI |
| "How do I enter our score in SPRS?" | Outside: SPRS mechanics are not covered; `/research` |
| "Where do I start?" | The first stage of the main flow whose artifacts are missing |
