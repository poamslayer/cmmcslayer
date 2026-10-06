---
name: find-cui
description: Find out whether an organization has CUI and where it goes. Take the intake facts from the contracts first, train, interview by role with IT last, determine each item against the ownership-first ruleset, and map the result into a data flow the scope can be drawn from.
disable-model-invocation: true
---

# Find CUI

The first on-ramp. Nothing else in an engagement is safe to start until this is done, because every later decision, the scope, the architecture, the budget, rests on knowing what the CUI actually is and where it goes.

The question arrives as "do we even have CUI?" and it is almost always asked of the IT lead, who cannot answer it. The answer is held by contracts, engineering, programming, the floor, inspection, shipping, purchasing, accounting, and the owner. This flow goes and gets it from them, in the right order.

**Order matters and is not negotiable: intake, train, interview, determine, map.** Each step's output is the next step's input, and running them out of order produces a confident wrong answer. The most common failure is starting from the asset list, which tells you what the company owns rather than what the data does.

## Step 0: Intake, in one sitting

Before the briefing, settle the facts that frame everything after it. One sitting with contracts and IT together should answer Level 1 versus Level 2, whether GCC High is worth discussing, and which deadline is real. Write the answers to `scope/intake.md`.

- **Read every active contract's clause list yourself.** Do not trust a prime's summary. Look for FAR 52.204-21, DFARS 252.204-7012, -7019, -7020, and -7021. Call the Skill tool with `flowdown-level-determination` when the clause list and what the company actually receives do not agree.
- **Ask the ITAR and EAR question directly**, including what the company expects to win next. This answer settles GCC High ahead of everything else; call the Skill tool with `export-control-overlay` when the answer is yes or unsure.
- **Ask about foreign ownership, control, or influence**, including a foreign parent that administers the tenant.
- **Get the current SPRS score**, who entered it, and what evidence backed it. A score with nothing behind it is a finding waiting to happen; call the Skill tool with `sprs-score-and-poam-eligibility` later to recompute it.
- **Gather what already exists**: a draft security plan, a milestone list from a past gap, a network drawing, an asset list, a self-attestation, an insurance form, a prior consultant's leftover policy set. Nothing on this list is trusted until checked, but all of it saves an interview.
- **Learn how the incumbent MSP connects**: standing admin accounts or only a shadowed session. That fact decides its category later in `esp-and-msp-scoping`, and the MSP needs an equal voice in scoping from here on.
- **Name who signs off on scope and spend, and whose deadline is real**: the contract's CMMC date, not a hoped-for one. The person who will sign the affirmation should know this is happening now.

## Step 1: Train first, and count it twice

Deliver the FCI and CUI briefing **before any interview**. Untrained staff over-claim CUI heavily, because "it came from a defense customer and it looked sensitive" feels like the safe answer. An interview run before the briefing produces a list of everything the company touches, and un-picking that costs more than the briefing did.

The briefing covers what FCI is, what CUI is, that a marking is not the same as a determination, that the company's own information is not CUI to the company, that "not CUI" does not mean "not sensitive" (the company's own designs, its customers' proprietary data, export-controlled data, and staff records all still need protecting), and that "I do not know" is a useful answer.

**Record attendance.** A dated attendance record with names and the material covered is evidence for 3.2.1. Put it in `evidence/3.2.1/`. The briefing you had to run anyway pays for itself twice.

## Step 2: Interview by role, IT last

Interview by **role**, not by department, and write one file per role into `scope/interviews/`. Tell the operator to run `/to-questionnaire` once per role; it is user-invoked, so it has to come from them rather than from this flow. The recipient is the person doing the work, so the questionnaire is aimed at their day, not at the standard.

The usual roles, in order:

1. Contracts and quoting
2. Engineering and design
3. Programming
4. Production and machining
5. Inspection and quality
6. Shipping and receiving
7. Purchasing
8. Accounting
9. Human resources
10. The owner or general manager
11. **IT, last**

Skip a role the company does not have. Add one it does.

**IT is interviewed last, and this is the rule people break.** Ask IT first and the technical picture frames everything after it: the answer becomes the systems IT knows about, and the paper on the clipboard, the thumb drive in the drawer, and the scan someone emails home do not come up. Interview the business first and you learn what the data does; then IT tells you which systems that lands in.

Every role questionnaire is built on the same seven questions plus destruction:

1. What do you receive from customers, and from whom?
2. How does it reach you?
3. What form does it arrive in?
4. Where do you keep it?
5. Who else has access to it?
6. Who do you send it to, and how?
7. How is it backed up?
8. How is it destroyed when you are finished with it?

Then the three probe questions, which are where the undocumented workflow comes out:

- What do you do when that breaks?
- How does a drawing actually get to the machine?
- Ask the newest employee how they were told to do it.

## Step 3: Determine

Take what the interviews surfaced and decide each item's status. Call the Skill tool with `cui-determination-workflow`, which asks about ownership first, then whether the work was performed under a contract and for the Government's own purposes, and only then whether some authority in law or policy actually controls the information. Evaluating the content first means you are already too far down the ruleset.

Where the company creates its own documents from the CUI it received, call the Skill tool with `cui-re-use-triage` as well. For a build-to-print manufacturer that is the trail the part generates: customer drawing, shop sketch, traveller, work instruction, inspection report, machine code, purchase order. The triage separates the CUI content each document re-uses from the company's own work and sends each document back to `cui-determination-workflow` for its status, so there is one answer per document, not two. A document is CUI because of the content it carries, never because of the document it came from, and the company's own work is where the scope gets its money back.

Where markings are unclear, **decide on the evidence, then notify the source in writing**: the status the company will apply, the proposed category, and the reasoning. A notice, not an open question: asked, a prime usually answers "treat it all as CUI" or not at all. Only the Government designates; for a document the company creates, the check is whether it re-uses CUI content. Record the notice and what came back, including silence, which accepts it.

Determinations are written to `scope/cui-determinations.md`, one entry per item. Each entry carries the item's data categories as well as its CUI status: every label that applies, from CUI, FCI, Export-controlled, Proprietary (own), Proprietary (third-party), PII, Security Protection Data, and Public (see `CONTEXT.md`). An item cleared as not CUI keeps its other labels. The company's own ITAR design is Proprietary (own) and Export-controlled, and it stays on the list.

## Step 4: Map, then write the terms down

Call the Skill tool with `cui-data-flow-mapping` to turn the interviews and determinations into `scope/data-flow.md`. The map covers four classes of flow, and the fourth is the one that catches people:

- **Entry**: how CUI arrives.
- **Generated**: what the company makes, and which CUI content each document re-uses.
- **Exit**: where it goes, including to subcontractors and finishers.
- **Paper and sneakernet**: the printout on the clipboard, the thumb drive walked to the machine, the scan-to-email, the backup drive that goes home. These are flows, not exceptions. A scope drawn from "we only email it" is drawn around a fiction.

Then **write the decisions into the engagement `CONTEXT.md`**. Call the Skill tool with `domain-modeling`. Every later skill reads that glossary, so the terms settled here are what keeps the whole engagement using one vocabulary. Record what this client's CUI actually is, in their words, with the determination behind it.

## Done when

- `scope/intake.md` holds the clause list per contract, the export-control and foreign-ownership answers, the SPRS score and its evidence, what already existed, and how the MSP connects.
- `evidence/3.2.1/` holds a dated attendance record.
- `scope/interviews/` holds one file per role in scope, with IT's dated last.
- `scope/cui-determinations.md` gives every item a status, its data categories, and a reason.
- `scope/data-flow.md` covers entry, generated, exit, and paper and sneakernet.
- `CONTEXT.md` names this client's CUI in this client's words.

Then the engagement can be scoped. Hand off to `cmmc-scope-boundary`, which walks the site with the data flow in hand and needs it to place a single asset.

## Traps to say out loud in week one

1. Everything looks like CUI until staff are trained; treat any pre-training answer as unreliable.
2. A prime's flowdown clause alone does not prove the sub handles CUI; it obligates only if CUI is actually involved.
3. A thumb drive walked to a CNC controller is a data flow, not an exception; it goes on the map first.
4. The MSP's access model decides its category, not what it says it intends to do.
5. Nothing collected this week goes into an SSP statement until someone verifies it.

## Seat notes

**Consultant seat**: this is the first thing a new engagement runs. Hold the intake before any contract is signed if you can; a prospect who cannot answer the intake questions needs a paid discovery week, not a quote. Say the week-one traps out loud to the owner and contracts, not only to IT.

**OSC seat**: run the intake internally, contracts and IT together, before approaching a consultant or a C3PAO; a clear answer up front shortens every conversation that follows. After that, you are handing questionnaires to colleagues who have never heard the term. Do not send them the standard. Ask about their work in their words, and let this flow do the translation. Expect the contracts and engineering interviews to change what you thought you knew, and expect your own IT picture to be the least reliable part of the answer until the others are in.

## Sources

- 32 CFR Part 2002, what CUI is: https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2002
- The DoD CUI Registry, category eligibility and authorities: `reference/cui-registry/` (also public at https://www.dodcui.mil/)
- CMMC Level 2 Assessment Guide, DoD CIO, AT.L2-3.2.1: https://dodcio.defense.gov/CMMC/Resources-Documentation/
- FAR 52.204-21: https://www.acquisition.gov/far/52.204-21
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012
- DFARS 252.204-7021: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7021

Practitioner consensus, unattributed, backs the intake question list including reading contract clauses firsthand, the training-first ordering, the IT-last rule, the three probe questions, and the week-one traps.
