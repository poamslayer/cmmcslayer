---
name: ssp-statement-writer
description: Write the conformity statement for each assessment objective in the form an assessor can score without hunting, show it to the operator, and record it where the engagement keeps its SSP, the `ssp/` files through scribe or a GRC platform such as IntelliGRC. Use when drafting or repairing SSP text, and whenever a fix has to be written down.
vault_sources:
  - "3.12.4"
  - "Requirement Applicability"
  - "Practitioner insights B"
  - "3.13.12"
public_sources:
  - "NIST SP 800-171A: https://csrc.nist.gov/pubs/sp/800/171/a/final"
  - "CMMC Level 2 Assessment Guide, DoD CIO, CA.L2-3.12.4: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.24: https://www.ecfr.gov/current/title-32/section-170.24"
---

# SSP statement writer

One conformity statement per assessment objective, written so the assessor can score that objective without reading anything else, shown to the operator, and recorded where the engagement keeps its SSP.

## Before you write: destination and mode

1. **Choose the destination.** Read `CONTEXT.md`, `AGENTS.md`, and `docs/adr/` for where the engagement keeps its conformity statements, and use what they record. When nothing records it, ask the operator: the `ssp/` files through scribe, a GRC platform, or another format they name. When nobody can be asked and the repo has an `ssp/` folder, use scribe. Then read the destination's file, which says how to read the current text and how to record:
   - `ssp/` files through scribe: [`destinations/scribe.md`](destinations/scribe.md).
   - IntelliGRC: [`destinations/intelligrc.md`](destinations/intelligrc.md).
   - Another format: write the statements at the path and in the shape the operator names, one per objective, and follow the rest of this skill unchanged.

2. **Choose the drafting mode** (ADR-0013). Ask the operator unless they have said. When nobody can be asked, use the default.
   - **As is**, the default: the statement says only what is true today, and the status follows it (ADR-0010).
   - **As if met**: the statement is written as if the control is in place, and the objective's status is left exactly as it is. The status keeps telling the truth; the text is ready for the day the evidence exists.

## Why the objective is the unit

The assessor works down the 800-171A objectives and scores each one. A narrative covering a whole requirement makes them hunt for the sentence that answers objective [c], and a hunt is where a finding comes from. One statement per objective is the single highest-leverage habit in SSP writing (ADR-0008).

## Inputs

The objectives in `3.5.3[a]` form, with their own words from `reference/nist-800-171r2-requirements.json`; the current statement and status of each, read from the destination; a **precedent**, an SSP that has passed an assessment, when the operator or the engagement has one; the engagement's own facts: its environment pages, the relevant decisions in `docs/adr/`, the baselines, the policies the organization has actually committed to, the evidence under `evidence/`, and the open items list, `scope/open-items.md`; and the glossary in `CONTEXT.md`.

## Method

1. **Read the objective's own words** and answer exactly what it asks. An objective that asks whether something is *defined* wants the definition. One that asks whether it is *enforced* wants the mechanism. Answering the enforcement question at the definition objective leaves the definition objective unscored. The reverse holds too: a definition objective asks only whether the decision is written down. Which systems and accounts carry it out, and whether they do, is the enforcement objective's question, so a written rule that does not list the systems it covers is still defined, and the coverage goes to the enforcement objective.

2. **Apply the definition and enforcement pattern.** State the organization-wide decision once, at the definition objective. At the enforcement objective, name the mechanism that carries the decision out on each platform or component. Do not restate the decision per platform; point at it. This is what keeps an SSP from tripling in length and contradicting itself in the process.

3. **Point a definition objective at its document.** When a document defines the thing, the definition objective's statement is one or two sentences naming that document by title: "Essential ports are defined in the baseline documentation (Baseline: Windows 11 Workstation, Baseline: Sophos XGS Firewall)." Leave the document's content in the document. A nonessential or negative definition is the inverse in one sentence: "Nonessential ports are defined as any port not listed in the baseline for the system type." When the destination attaches the statement to the defining document itself, as scribe does with a policy or procedure component, a pointer would point at itself: state the definition's substance instead, with its values, in one or two sentences ("A user session ends after 30 minutes of inactivity.").

4. **Match the precedent.** When a precedent exists, read its statements for the same objectives first and follow their shape: their length, what they name, and how they cite. Change the facts, never copy them: every mechanism, document, and role must be true of this engagement.

5. **Use the power of definition deliberately.** Many requirements let the organization define the term: what a privileged account is, what a security function is, what counts as an essential capability, what the session termination conditions are, how often logs are reviewed. **Define it as something you can actually do and actually evidence.** A definition written to sound rigorous becomes a finding the moment the evidence does not match it. Never define a separation of duties you cannot staff.

6. **Set periodicity with headroom.** "At least annually" is the floor. Write the policy period longer than what you actually do, so a cycle that slips by a month is not a finding. Do not write specific event identifiers or tool-specific settings into a statement; those belong in a baseline document the statement points at.

7. **Name the artifact.** A statement that points at the evidence, the inventory, or the document lets the assessor score the objective and move on. Use the name the engagement uses for it, and its location when it lives in a system rather than a file.

8. **Set the status by the mode.**
   - **As is:** implemented when the system does what the objective asks today; partial when it does part, the statement saying which part is in place and which is missing; planned when it does not yet, or when whether it does at all waits on an open item. Partial is for a known gap, never an unconfirmed one (ADR-0010). Alternative when the objective is met another way, and not applicable when it does not apply, each with its reason; do not use one for the other. Applicability is `requirement-applicability-matrix`'s decision: record either status only where it or an ADR gives the reason. Send anything unverified to `scope/open-items.md`, a line naming the fact, the objective, and who can confirm it, creating the file with a `# Open items` heading if the engagement has none. Never put it in the statement with a caveat.
   - **As if met:** write each statement as if the control is in place, and leave every status as it is. Assume the pieces the plan calls for exist: the procedure, the list, the policy section. Raise only a statement that contradicts a documented fact or decision, such as a tool the engagement does not use or a setting a baseline sets the other way.

9. **Look at the paired objective.** Fixing a definition objective changes what its enforcement objective has to show, and the other way round. Say to the operator what the paired objective now needs; write it too when they asked for the requirement.

## Form

- **Present tense.** An SSP describes the system as it is. In the as-is mode, work not yet done is recorded planned, with a statement saying what is in place now; the plan itself is a ticket, never a future-tense statement.
- **Short.** One to three sentences per objective is the norm. A longer statement is earned by an enforcement objective with several platforms, one sentence each.
- **No "to be confirmed", no "TBD", no "as applicable", no "where appropriate".** Each one is an admission, and `ssp-lint` rejects them.

## Output

Show, then record. Work one requirement at a time. Show the operator every objective's full statement in the conversation, under the objective's own words. After the statements, list only the decisions that are the operator's to make: a name, a role, a period, a document's title, or a statement that contradicts a documented fact. Do not list back what the mode told you to assume.

Record nothing until the operator says to. Their edits replace yours, and a decision they make holds for every later requirement. Then record through the destination's file and report what the destination returned.

## Two failure shapes to avoid

- **The pure-reference SSP**, which answers every objective by pointing at another document. The assessor has to assemble your answer for you, and what they assemble is what gets scored. A pointer answers a definition objective (step 3); an enforcement objective names its mechanism.
- **The kitchen-sink SSP**, padded with material no objective asked for. It buries the sentences that matter and gives an assessor more surface to find contradictions on.

Format is otherwise free. Completeness is not.

## Before you hand it over

Check the statement against the supporting document that backs it. A statement claiming a lockout threshold the procedure contradicts is the most common contradiction found in gap analyses, and it is expensive at assessment because many assessors permit only a handful of document corrections. Do not spend one on something a read-through would have caught. `ssp-lint` automates this check across an `ssp/` record.

## Where practitioners disagree

How much detail an assessor wants inside a statement varies. Some want the mechanism named precisely; others read that as brittleness, because a statement naming a product version becomes wrong when the product updates. The defensible middle is to name the control and the mechanism in the statement, and leave versions and settings in the baseline document the statement points at. The outcome depends on the assessor.

## Sources

- NIST SP 800-171A, the objectives that are the unit of scoring: https://csrc.nist.gov/pubs/sp/800/171/a/final
- CMMC Level 2 Assessment Guide, DoD CIO, CA.L2-3.12.4, what the SSP has to cover: https://dodcio.defense.gov/CMMC/Resources-Documentation/
- 32 CFR 170.24(c)(2)(i)(5), the effect of an absent or incomplete SSP: `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24)

There is no SSP template in the source material, so this skill describes the shape of a statement rather than supplying a document to fill in. Practitioner consensus, unattributed, backs the one-statement-per-objective rule, the definition and enforcement pattern, and the two failure shapes. The pointer statements, the precedent rule, and the as-if-met mode come from a live engagement whose MSP's own SSP passed assessment in that shape (ADR-0013).
