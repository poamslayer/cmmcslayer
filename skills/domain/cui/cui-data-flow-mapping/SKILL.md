---
name: cui-data-flow-mapping
description: Map how CUI actually moves through the company before any asset gets categorized. Runs the train-then-interview-then-map-then-assets sequence, asks the seven non-technical interview questions plus destruction, interviews by business role with IT last, draws all four flow classes including paper and sneakernet, and produces the data flow diagram at the organization, business-process, and system levels. Use at the start of a scoping engagement, or whenever the asset inventory and the SSP disagree about where CUI lives.
vault_sources:
  - "Data Flow Diagram"
  - "Client Onboarding: Data Flow Mapping First"
  - "Practitioner insights B"
  - "How CUI Flows Through a Contractor"
  - "Client Onboarding Discovery Checklist"
public_sources:
  - "reference/usg-zones-to-cmmc-categories.md"
---

# CUI data flow mapping

This skill maps where CUI enters, where it is generated, where it exits, and where it moves on paper or by hand, before a single asset gets a category. It enforces a strict ordering: train the people who handle data, interview them, map the flows their answers describe, and only then identify assets. It does not categorize assets itself (call `cmmc-scope-boundary` once the map exists), and it does not test whether a specific document is CUI (call `cui-determination-workflow` for that, or `cui-re-use-triage` for the documents the company creates from CUI it received). This skill is normally called by the engagement's `find-cui` flow, after training and role interviews, and before scoping begins.

## Inputs

- Every interview file under `scope/interviews/`, one per business role, written by the `to-questionnaire` skill during the engagement's interview step. Read all of them before drawing anything; a map built from a partial set of interviews will miss a flow.
- A record that FCI/CUI training happened before the interviews were conducted, since interviews run before training produce inflated, unreliable answers.
- `CONTEXT.md` for the client's vocabulary and any CUI determinations already on record.
- Any assets already in the record, `ssp/ssp.json`, read only to check for disagreement with the flows this skill maps, never as the starting point. Call the Skill tool with `scribe` and ask it to show the record. Never read `view/` instead; it is generated for people and can be stale.

## Method

1. **Confirm the ordering has actually been followed: train, then interview, then map, then identify assets.** Never start from an asset inventory and try to work out which assets touch CUI; that produces the opposite failure mode, where the assets define the story instead of the data. If interviews were conducted before training, treat their answers as unreliable and re-run them: untrained staff over-claim CUI at a high rate, commonly cited around 80 percent, because without training people call anything that feels sensitive "CUI." An inventory inflated that way ends up needing correction after the fact, at a cost well above just doing the sequence right from the start.

2. **Confirm the interviews asked the seven questions, verbatim, for every role.** These questions are deliberately non-technical: a shipping clerk or a contracts admin can answer every one of them without any networking background, and the answers map directly onto the elements a data flow diagram needs:
   - What kind of data do you receive?
   - How do you receive it?
   - What format is it in?
   - Where is it stored?
   - Who has access to it?
   - Who do you share it with?
   - How is it backed up?
   - Add an eighth question for anyone who handles paper or physical media: how is it destroyed?
   If an interview file is missing an answer to one of these eight, that is a gap in the map, not something to infer; go back to the role and ask.

3. **Interview by business role, not by department, and put IT last.** Cover, in whatever order fits the shop: quoting and contracts, engineering and CAD, programming, machining, inspection, shipping and receiving, purchasing, accounting, human resources, and the owner, all before IT. Each role sees a different slice of the same data as it moves through the company: sales and contracts see it first, at the quote and award stage; engineering and program management see it as deliverables and marking instructions get assigned; production and quality see it as it becomes travelers, work instructions, and inspection records; shipping sees it as it leaves. IT is interviewed last because it can only usefully describe how the systems carry the data once the other roles have already established what the data is, who needs access, and where that data is required to sit. Interviewing IT first produces a systems-first map that misses the business processes generating the data in the first place.

4. **Draw all four flow classes as first-class flows, none of them as an afterthought.**
   - **Entry points**: every place CUI-relevant information first reaches the company, a prime's portal, an email attachment, a request for quote package, a government furnished document.
   - **Generated-CUI paths**: everything the company itself creates that reproduces or depends on the entering data, drawings-derived sketches, travelers, programs, inspection reports, engineering analyses.
   - **Exits**: every place CUI-relevant information leaves the company, a subcontractor, a finisher or coater, the prime, or the government directly.
   - **Paper and sneakernet**: printed drawings, binders, a USB drive carried to a CNC controller, a fax line. This flow class is dropped from most first-pass maps because it feels informal, but it is a full flow, not an exception, and it is frequently where the real scope boundary sits on a shop floor.

5. **Map the flows to the three levels a data flow diagram covers, and produce both a high-level and a low-level diagram.**
   - **Organizations**: how information moves between the company and separate legal entities, the prime, the government, a subcontractor, an external service provider.
   - **Business processes**: how information is meant to move inside the company, quoting to engineering to production to shipping.
   - **Systems, applications, and services**: the actual system interconnections that make each business process work, the file share, the ERP, the CAD/PLM environment, the shop-floor terminal.
   Produce a high-level diagram that a non-technical reader can follow at a glance, and a detailed low-level diagram that names the ports, protocols, and services in play, matched against the access control lists already in place. The high-level view sells the story; the low-level view is what an assessor checks against the network diagram.

6. **Surface the undocumented workflow with three probe questions, since the interview's official answers rarely catch it.**
   - Ask what the person does the moment their normal process fails. The workaround someone reaches for under pressure, emailing a personal account when the VPN is down, photographing a drawing on a phone, carrying a USB stick over to a machine, is the undocumented flow the official process hides.
   - Ask, specifically, how a drawing physically reaches the machine that uses it. This single question frequently exposes half the shop floor's real data path in one answer.
   - Talk to whoever was hired most recently. A new hire still remembers what confused them on day one, and what the actual unwritten process turned out to be, before they learned to describe their job the way everyone else does.
   Treat every answer to these three prompts as a flow to add to the map, not as an anecdote to note and move past.

7. **Record the destruction question as part of every paper and physical-media flow, not as an afterthought.** How CUI in paper or physical form gets destroyed, cross-cut shredding, a contracted destruction service, an approved burn process, belongs in the same flow entry as how it was received and stored. A flow map that stops at storage and skips disposition is incomplete.

## Output

Write `scope/data-flow.md` with these sections, populated from the interview files and the probe-question findings:

```markdown
# Data flow map: <client>

Built from interviews in scope/interviews/, dated <date range>. Training confirmed on <date>.

## Entry

| Source | Channel | Format | Role that receives it | Data categories |
|---|---|---|---|---|
| | | | | |

## Generated

| Document or system | Derived from | Role that generates it | Data categories |
|---|---|---|---|
| | | | |

## Exit

| Destination | Channel | Role that sends it | Data categories |
|---|---|---|---|
| | | | |

## Paper and sneakernet

| Item | Carried by | From | To | How destroyed | Data categories |
|---|---|---|---|---|---|
| | | | | | |

## Diagram levels

### Organizations
<narrative or diagram reference: company, prime, government, ESPs>

### Business processes
<narrative or diagram reference: quoting to engineering to production to shipping>

### Systems, applications, and services
<narrative or diagram reference: named systems, ports, protocols, matched to the ACLs>

## Undocumented workflows found
- <what happens when the normal process fails, how a drawing physically reaches the machine, and what the newest hire says the unwritten process actually is>

## Open items
- <anything an interview left unanswered>
```

Fill the Data categories column from `scope/cui-determinations.md`, listing every category that applies (see `CONTEXT.md`). Keep flows that carry no CUI on the map, labeled: a customer's proprietary drawing with no CUI marking, the company's own ITAR design, HR files, and logs going to a SOC are all flows the company has to protect, even though only the CUI and FCI flows draw the assessment scope. A flow left off the map because it was "not CUI" is the one nobody protects.

This file is a required input to `cmmc-scope-boundary` and to the asset inventory that follows it. Hand off with a note: assets get identified from this map, never the reverse.

## Where practitioners disagree

- Whether the low-level, port-and-protocol diagram needs to exist before scoping starts, or can be built after the high-level map and the asset inventory are already underway. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run training as a standalone first engagement activity, and keep the attendance record; it doubles as evidence for the security awareness training requirement (3.2.1) later. Do not let a client shortcut straight to an asset inventory because they are in a hurry; the ordering is the point. **OSC seat**: if outside help is not available, run the seven questions yourself with each department head after a short internal training session, and be honest that the newest employee on staff is often the best source for the probe questions.

## Sources

- `reference/usg-zones-to-cmmc-categories.md` (the organization, business-process, and system levels a data flow diagram covers, and how they feed the scope boundary) (also public at https://complianceforge.com/).
- Practitioner consensus, unattributed, backs the train-then-interview-then-map-then-assets ordering, the seven interview questions plus the destruction question, interviewing by role with IT last, all four flow classes including paper and sneakernet as first-class flows, and the three undocumented-workflow probe questions.
