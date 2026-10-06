---
name: ssp-statement-writer
description: Write the conformity statement for one assessment objective and one component, in the form an assessor can score without hunting, and record it in `ssp/ssp.json` through scribe. Use when drafting or repairing SSP text, and whenever a fix has to be written down.
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

One conformity statement per assessment objective and component, written so the assessor can score that objective without reading anything else, and recorded in the engagement's SSP, `ssp/ssp.json`, by calling the Skill tool with `scribe` (ADR-0007). Never write `ssp.json` yourself, and never edit anything under `view/`.

## Why the objective is the unit

The assessor works down the 800-171A objectives and scores each one. A narrative covering a whole requirement makes them hunt for the sentence that answers objective [c], and a hunt is where a finding comes from. One statement per objective is the single highest-leverage habit in SSP writing, and it is how the record is built: scribe attaches each statement to its objective, written `3.5.3[a]`, and to the component it describes (ADR-0008).

## Inputs

The objective in `3.5.3[a]` form; the record, `ssp/ssp.json`, for the recorded components, the providers, and the statements already on the objective (call the Skill tool with `scribe` and ask it to show the record for the requirement; never read `view/`); the relevant decisions from `docs/adr/`; the policies the organization has actually committed to; the evidence under `evidence/`; the open items list, `scope/open-items.md`; and the glossary in `CONTEXT.md`.

## Method

1. **Read the objective's own words** and answer exactly what it asks. An objective that asks whether something is *defined* wants the definition. One that asks whether it is *enforced* wants the mechanism. Answering the enforcement question at the definition objective leaves the definition objective unscored. The reverse holds too: a definition objective asks only whether the decision is written down. Which systems and accounts carry it out, and whether they do, is the enforcement objective's question, so a written rule that does not list the systems it covers is still defined, and the coverage goes to the enforcement objective.

2. **Apply the definition and enforcement pattern.** State the organization-wide decision once, at the definition objective. At the enforcement objective, write one statement on each component that carries the decision out, naming its mechanism. Do not restate the decision per component; point at it. This is what keeps an SSP from tripling in length and contradicting itself in the process.

3. **Use the power of definition deliberately.** Many requirements let the organization define the term: what a privileged account is, what a security function is, what counts as an essential capability, what the session termination conditions are, how often logs are reviewed. **Define it as something you can actually do and actually evidence.** A definition written to sound rigorous becomes a finding the moment the evidence does not match it. Never define a separation of duties you cannot staff.

4. **Set periodicity with headroom.** "At least annually" is the floor. Write the policy period longer than what you actually do, so a cycle that slips by a month is not a finding. Do not write specific event identifiers or tool-specific settings into a statement; those belong in a baseline document the statement points at.

5. **Write at the component level**, using the component titles the record holds. The laptop fleet is one component. Per-machine statements add redundancy, not assurance. A statement names a recorded component, never the "This System" placeholder. An organization-wide decision goes on the policy, plan, or procedure component that carries it; when the record has none, call the Skill tool with `scribe` to add one. Its type is `policy` for a written policy or plan, or `process-procedure` for a practice. Any other missing component is a scoping gap: put it on the open items list for `cmmc-scope-boundary` rather than adding it.

6. **Collapse inherited components onto their control plane.** Where several workloads federate to one identity provider, one log platform, or one endpoint manager, write the enforcement statement on the plane's component and name what inherits it. Where an external provider implements part of the objective, write the provider's part on the provider's component and the company's part on the company's, rather than claiming the provider's work. Scribe generates the responsibility matrix from the two.

7. **Name the artifact.** A statement that points at the evidence lets the assessor score the objective and move on.

8. **Choose the status the engagement supports.** Implemented when the component does what the objective asks today; partial when it does part, the statement saying which part is in place and which is missing; planned when it does not yet, or when whether it does at all waits on an open item. Partial is for a known gap, never an unconfirmed one: when anything the objective turns on waits on an open item, the status is planned, and the statement says what is confirmed (ADR-0010). Alternative when the objective is met another way, and not applicable when it does not apply to this component, each with the reason in the remarks; do not use one for the other. Only those two carry remarks; for partial, what is missing goes in the statement. Applicability is `requirement-applicability-matrix`'s decision: record either status only where it or an ADR gives the reason.

9. **Send anything unverified to the open items list.** Not into the statement with a caveat. Add a line to `scope/open-items.md` naming the fact, the objective, and who can confirm it, creating the file with a `# Open items` heading if the engagement has none, and record the objective planned for that component, its statement saying only what is true today (ADR-0010).

10. **Put a misplaced statement on the right component.** A statement already recorded on the wrong component, such as an enforcement sentence on a definition objective's tenant, is not fixed by editing it there. Record the right statement on the right component, then ask scribe to take the old component off the objective with `remove-statement` (not `remove-component`, which deletes the component), so it is not left behind as planned. Clear a statement instead only when that component still owes the objective and its statement is not written yet.

11. **Look at the paired objective.** Fixing a definition objective changes what its enforcement objective has to show, and the other way round. Say to the caller what the paired objective now needs; write it too when the caller asked for the requirement, and otherwise put it on the open items list.

## Form

- **Plain prose about the component it is attached to.** "Accounts are authorized in writing by the owner before IT creates them." Scribe records which component the statement describes, so do not prefix the text with the component's name.
- **Present tense, and only what is true today.** An SSP describes the system as it is. Work not yet done is recorded planned, with a statement saying what is in place now; the plan itself is a ticket, never a future-tense statement.
- **No "to be confirmed", no "TBD", no "as applicable", no "where appropriate".** Each one is an admission, and `ssp-lint` rejects them.

## Two failure shapes to avoid

- **The pure-reference SSP**, which answers every objective by pointing at another document. The assessor has to assemble your answer for you, and what they assemble is what gets scored.
- **The kitchen-sink SSP**, padded with material no objective asked for. It buries the sentences that matter and gives an assessor more surface to find contradictions on.

Format is otherwise free. Completeness is not.

## Output

The statement recorded through scribe (call the Skill tool with `scribe`) on its objective and component, with a second call to take a misplaced statement off the wrong component (step 10), with its status, and remarks where the status needs a reason; plus any line the work generated for `scope/open-items.md`. When the caller has several statements, give scribe them as one set so they are validated once. Say it to scribe in these terms:

```markdown
| Objective | Component | Status | Statement | Remarks |
|---|---|---|---|---|
| 3.1.10[b] | Windows 11 office endpoints | implemented | The screen locks after 15 minutes of inactivity, enforced by the endpoint management policy exported in evidence/3.1.10/. | |
```

An open items line reads: `- 3.1.8[b]: whether the lockout applies to local accounts on SAG-NAS. Confirm with <who>.`

Setting a statement again on the same objective and component replaces it and keeps its identity. If scribe refuses, the refusal is the answer: fix the statement and ask again, never work around it. Scribe re-renders `view/requirements/<id>.md`, where people read the result.

## Before you hand it over

Check the statement against the supporting document that backs it. A statement claiming a lockout threshold the procedure contradicts is the most common contradiction found in gap analyses, and it is expensive at assessment because many assessors permit only a handful of document corrections. Do not spend one on something a read-through would have caught. `ssp-lint` automates this check across the whole SSP.

## Where practitioners disagree

How much detail an assessor wants inside a statement varies. Some want the mechanism named precisely; others read that as brittleness, because a statement naming a product version becomes wrong when the product updates. The defensible middle is to name the control and the component in the statement, and leave versions and settings in the baseline document the statement points at. The outcome depends on the assessor.

## Sources

- NIST SP 800-171A, the objectives that are the unit of scoring: https://csrc.nist.gov/pubs/sp/800/171/a/final
- CMMC Level 2 Assessment Guide, DoD CIO, CA.L2-3.12.4, what the SSP has to cover: https://dodcio.defense.gov/CMMC/Resources-Documentation/
- 32 CFR 170.24(c)(2)(i)(5), the effect of an absent or incomplete SSP: `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24)

There is no SSP template in the source material, so this skill describes the shape of a statement rather than supplying a document to fill in. Practitioner consensus, unattributed, backs the one-statement-per-objective rule, the definition and enforcement pattern, and the two failure shapes.
