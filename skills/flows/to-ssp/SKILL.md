---
name: to-ssp
description: Turn the grilling, the scoping record, and the recorded decisions into the SSP's conformity statements, one per assessment objective and component, recorded in `ssp/ssp.json` through scribe. No interview, just synthesis of what the engagement has already settled.
disable-model-invocation: true
---

# To SSP

Take what the engagement has already decided and write it into the SSP. The SSP is one OSCAL document, `ssp/ssp.json`, and it is the record (ADR-0007). Every statement goes into it by calling the Skill tool with `scribe`; never write `ssp.json` yourself and never edit anything under `view/`. Do not interview the operator; synthesize what is in the conversation, the record, the scope notes, and the ADRs. Where something is genuinely unknown, it goes to the open items list, never into a statement.

The engagement repo should already be scaffolded. If there is no `ssp/ssp.json`, tell the operator to run `/setup-poamslayer-skills`.

## The unit is the objective and the component

One conformity statement per assessment objective per component, not one narrative per requirement (ADR-0008). The assessor scores each objective separately, so a narrative that covers four objectives in one paragraph makes them hunt for the sentence that answers objective [c], and a hunt is where a finding comes from. Scribe attaches each statement to the objective it answers, written `3.5.3[a]`, and to the component it describes, so one objective can be met one way by Entra ID and another way by the laptops.

Call the Skill tool with `ssp-statement-writer` for the statement rules. This flow sequences the work; that skill decides what a good statement says.

## Inputs

- **The record, `ssp/ssp.json`**: the components, assets and their categories, providers, and every statement already recorded. Read it by calling the Skill tool with `scribe` and asking it to show the record for the requirements in hand; that is the current state. Never read `view/`: it is generated for people and can be stale.
- `CONTEXT.md` for the glossary and the seat, and `docs/adr/` for the decisions and their reasoning. Use the glossary's terms; do not drift to synonyms it avoids.
- `scope/data-flow.md`, `scope/network-diagram.md`, `scope/network-diagram.drawio`, `scope/cui-determinations.md`, and `scope/applicability-matrix.md` where they exist.
- `scope/open-items.md`, the open items list (ADR-0010).
- `policies/` for what the organization has actually committed to, and `evidence/` for what backs a claim.
- An SSP the client hands over from before the engagement, such as a consultant's Word document, is a source like any other document: test each claim in it against the engagement.

## Method

1. **Read the engagement first**, in the order above. List the components the record holds. A statement can name only a recorded component, never the "This System" placeholder.

2. **Work by requirement, in family order.** Within a requirement, work the objectives in letter order. Stop after each family and let the operator read it, because a wrong pattern repeated across 110 requirements is expensive to unpick.

3. **Apply the definition and enforcement pattern.** Most requirements have an objective asking whether something is *defined*, *identified*, or *specified* and a later one asking whether it is *enforced* or *implemented*. Treat the first kind as definition objectives. State the organization-wide decision once, at the definition objective, on the component that carries it: the policy or procedure that makes the decision, such as "Access control procedure". At the enforcement objective, write one statement per component that carries the decision out, each naming its own mechanism. Do not restate the decision per component; point at it.

4. **Match statements to components, not to individual machines.** The laptop fleet is one component. A statement on a component covers every asset behind it; listing controls per device produces redundancy without assurance.

5. **Place each statement on the right component.**
   - A company-wide decision or practice goes on the policy, plan, or procedure component that carries it. When the record has none, call the Skill tool with `scribe` to add one. Its type is `policy` for a written policy or plan, and `process-procedure` for a practice or procedure. That is the only kind of component this flow adds. When no written document makes the decision at all, do not file it under an unrelated procedure: put it on the component for the company's unwritten practices, adding one if the record has none, and say that nothing defines it.
   - A statement about a system goes on that system's component. When the component it needs is not in the record, do not add it: the inventory belongs to scoping. Put the gap on the open items list for `cmmc-scope-boundary` and go on.
   - Where several workloads federate to one identity provider, one log platform, or one endpoint manager, write the enforcement statement on the plane's component and name the workloads that inherit it.
   - Where an outside provider implements part of the objective, write two statements: the provider's part on the provider's component, and the company's part on its own component. When the provider's tool, such as its RMM, is not recorded as an asset, write on the provider's component and put the missing tool on the open items list for `esp-and-msp-scoping`. The responsibility matrix is generated from them as `view/esp-responsibility-matrix.md`; do not cite a matrix file as if it held the claim.

6. **Give each statement its status.**

   | Status | When |
   |---|---|
   | implemented | The component does what the objective asks today, and the engagement shows it. |
   | partial | It does part of it. The statement says which part, and what is missing. A known gap, never an unconfirmed one. |
   | planned | It does not do it yet, or anything the objective turns on waits on an open item (ADR-0010). |
   | alternative | The objective is met another way. The remarks give the reason. |
   | not applicable | The objective does not apply to this component. The remarks give the reason. |

   A component the objective could bear on but that you cannot place, such as a device with no logon at an authentication objective, is left off the objective and put on the open items list for `requirement-applicability-matrix`; never record it not applicable yourself.

   A claim the engagement contradicts is not implemented, whoever wrote it: an audit report in `.scratch/audit/`, the evidence, or a policy that says otherwise wins over the claim. Applicability is decided by `requirement-applicability-matrix`, not here. Record a not applicable or alternative status only where the matrix or an ADR already gives the reason, and never use one for the other. When one already in the record rests on a reason the engagement's facts contradict, record what is true instead and put the question on the open items list for `requirement-applicability-matrix`.

7. **Correct what is already recorded.** Setting a statement again for the same objective and component replaces it and keeps its identity. When a statement sits on the wrong component, record the right one on the right component, then ask scribe to take the wrong component off the objective (`remove-statement`); clearing would leave it there as planned. Clear a statement only when the component still owes the objective and its statement is not yet written.

8. **Cover 3.12.4 deliberately** on any pass over the whole SSP; when the operator named particular requirements, say whether 3.12.4's statements still hold and leave them to the next whole pass. The SSP itself is a requirement, it is worth 1 point, it can never sit on a POA&M, and its absence stops an assessment outright (32 CFR 170.24(c)(2)(i)(5)). Its objectives ask for the system boundary, the environments of operation in terms of people, technology, and facilities, how the requirements are implemented, and the relationships and connections to other systems. Write those explicitly rather than assuming the rest of the document implies them.

9. **Send everything unverified to the open items list.** If a fact is not confirmed, it does not go in a statement with a caveat attached. It goes on `scope/open-items.md` (create it with a `# Open items` heading if the engagement has none), one line naming the fact, the objective in `3.5.3[a]` form, and who can confirm it (a person, or "for <skill>" when a skill owns the answer), and the objective is recorded planned for that component (ADR-0010). The planned statement says only what is true today, for example "Lockout for local accounts on SAG-NAS is not documented." Text such as "to be confirmed" inside a statement is a lint failure and, at assessment, an admission.

10. **Record the family through scribe.** Show the operator the family as a table first, then call the Skill tool with `scribe` and give it the family's statements as one set. Scribe records a set with one validation, which matters across 320 objectives. Record straight away if the operator asked you not to stop; that skips the pause for the operator between families, never the lint. If scribe refuses, the refusal names the entry: fix that statement and give scribe the set again. Never work around a refusal.

11. **Run the lint.** When a family is recorded, call the Skill tool with `ssp-lint` on it. Fix what it finds before moving on.

## House rules

- **The component is the statement's subject.** Scribe attaches each statement to its component, so write it about that component and do not prefix the text with the component's name. Use the component titles the record holds, never a bare category label.
- **No "to be confirmed", no "TBD", no "as applicable"** inside a statement.
- **Present tense, and only what is true today.** An SSP describes the system as it is. Work not yet done is recorded planned, with a statement saying what is in place now; the plan itself belongs on a POA&M ticket, never in a future-tense statement.
- **Name the artifact where one exists.** A statement that points at the evidence is what lets an assessor score the objective without asking a question.

## What this flow does not do

It does not decide anything. A contested call that arrives unresolved goes to `/wayfinder` or to the domain skill that owns it, and comes back as an ADR. Writing a statement is how a decision gets recorded, not how it gets made.

It does not assess. `/audit` decides whether an objective is MET; a statement is a claim until evidence backs it.

It does not scope. Components, assets, categories, and providers come from the scoping skills.

## Output

- The statements, recorded in `ssp/ssp.json` by scribe, each on its objective and component with its status, and remarks where the status needs a reason. Scribe re-renders `view/requirements/<id>.md` for each requirement; point the operator at those pages to read the result.
- New lines on `scope/open-items.md`, which stays Markdown:

  ```markdown
  - 3.1.8[b]: whether the lockout applies to local accounts on SAG-NAS. Confirm with <who>.
  ```

- Per family, the table shown to the operator before recording:

  ```markdown
  | Objective | Component | Status | Statement | Remarks (reason, for alternative or not applicable) |
  |---|---|---|---|---|
  | 3.1.1[a] | Access control procedure | implemented | Authorized users are ... | |
  ```

## Seat notes

**Consultant seat**: the open items list is the client's homework and belongs in the weekly note. **OSC seat**: write the statements in the words your own staff use, since they are the ones an assessor will interview, and an SSP whose vocabulary nobody recognizes is a finding waiting to happen.

## Sources

- ADR-0007, the record and its one writer: `docs/adr/0007-oscal-ssp-is-the-record-and-scribe-writes-it.md`
- ADR-0008, statements attach to objectives: `docs/adr/0008-conformity-statements-attach-to-objectives.md`
- ADR-0010, open items stay outside the record: `docs/adr/0010-open-items-stay-outside-the-record.md`
- 32 CFR 170.24(c)(2)(i)(5), the SSP requirement and the effect of its absence: `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24)
- NIST SP 800-171A, 3.12.4 objectives: https://csrc.nist.gov/pubs/sp/800/171/a/final
- CMMC Level 2 Assessment Guide, DoD CIO, CA.L2-3.12.4: https://dodcio.defense.gov/CMMC/Resources-Documentation/

Rewritten from `to-spec` in mattpocock/skills (MIT, see `skills/flows/LICENSE-mattpocock`). The no-interview rule and the synthesize-what-you-know shape are kept; the seams become assessment objectives and the spec template becomes the SSP record.
