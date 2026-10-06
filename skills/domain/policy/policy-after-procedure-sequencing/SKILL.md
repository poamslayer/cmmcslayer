---
name: policy-after-procedure-sequencing
description: Decide what order to write CUI policy and procedure documentation in, and what each document has to contain. Enforces flow-first sequencing, a document discovery pass before any drafting, the policy/standard/procedure hierarchy, the power of definition, and the annual periodicity floor. Use when an engagement opens with "we need policies," or when a client hands over a purchased policy template before any process work has happened.
vault_sources:
  - "Practitioner insights B"
  - "Client Onboarding Discovery Checklist"
  - "Must-Have vs Nice-to-Have Security Controls"
  - "Unified Scoping Guide"
  - "3.1.4"
  - "3.1.6"
  - "3.1.7"
  - "3.1.11"
  - "3.3.1"
  - "3.4.7"
  - "3.11.2"
  - "3.12.1"
  - "raw/Summit 7 - Fun with NIST Policy Controls (TXsKdH3hC6E) - Transcript.md (Summit 7, https://www.youtube.com/watch?v=TXsKdH3hC6E)"
public_sources:
  - "Fun with NIST Policy Controls, Summit 7: https://www.youtube.com/watch?v=TXsKdH3hC6E"
  - "Unified Scoping Guide, ComplianceForge: https://complianceforge.com/"
---

# Policy after procedure sequencing

This skill answers one question: in what order do you build a client's CUI documentation set, and what belongs in which layer of it. It does not draft policy text itself and it does not decide what CUI is or where it flows (call `cui-data-flow-mapping` for that, first). It refuses to let an engagement start by installing a policy template before the underlying process exists, because a document that describes a company that does not yet operate that way cannot be evidenced at assessment.

## Inputs

- `scope/data-flow.md`, produced by `cui-data-flow-mapping`. Policy sequencing cannot start before the data flow is mapped; if this file does not exist, call that skill first.
- Any existing process documentation the client already has: quality manual, work instructions, onboarding and offboarding checklists, IT runbooks, change tickets. Collected during the document discovery pass in Method step 1.
- `CONTEXT.md` for the client's vocabulary, so definitions written in step 3 use the client's own terms for roles and systems.
- Any purchased or templated policy set the client already owns, read only to check it against what the client actually does, never treated as a starting point.

## Method

1. **Run document discovery before drafting anything.** Inventory what the client already has: a Quality Management System, AS9100 or ISO 9001 work instructions, bill-of-materials and traveler tracking records, onboarding and offboarding procedures, and existing IT runbooks. Manufacturing clients in particular usually already operate more of the required process than they think; this pass finds it before anyone writes a policy sentence that duplicates or contradicts it. Record every document found, its owner, and whether it still matches current practice. A document that no longer describes how the client actually works is a liability, not an asset, once it is cited as evidence.

2. **Enforce the sequence: flow, then process, then tweak, then policy.** First confirm the CUI flow is mapped (input above). Second, document the business processes that actually move and protect that CUI today, in the client's own words, not the language of a control. Third, adjust those processes until they are good enough to defend, closing the gaps that document discovery and the flow map exposed. Only after that does anyone write a policy, and the policy is written to match the now-compliant procedure, not the other way around. A policy drafted first describes a company that does not exist yet, and an assessor who compares that policy to what actually happens on the floor will find the gap immediately. This ordering is the spine of the whole skill; every other step in this Method assumes it has already run.

3. **Sort every document you write into its place in the hierarchy, and do not let layers collapse into each other.** Use this table:

   | Layer | What it holds | Who reads it |
   |---|---|---|
   | Policy | The management decision: what the company has decided to do and why, at what scope | Everyone the decision applies to, and the assessor checking for a documented decision |
   | Control objective | The outcome the policy is trying to produce | Whoever designs the standard below it |
   | Standard | The specific, technical requirement that satisfies the objective | IT and security staff implementing it |
   | Control | The mechanism selected to meet the standard | Whoever configures or operates it |
   | Procedure | The step-by-step instructions a person follows | The person doing the work |
   | Guideline | Optional, non-binding advice on how to do the procedure well | Anyone who wants the extra context |

   A policy that lists specific technical settings has collapsed the standard layer into itself, and now has to be rewritten every time that setting changes. A procedure with no matching policy has no management decision behind it for an assessor to verify. Keep each layer in its own document, or at minimum its own clearly labeled section, so a technical change does not force a policy rewrite and sign-off.

4. **Use the power of definition, and use it on terms you can actually execute.** Across the objectives that ask "is X defined," the operating text is the same: the organization gets to define the term, and an assessor tests the definition against what actually happens, not against some external standard of what the term should mean. Apply this deliberately to every term a policy or procedure needs and an objective asks you to define:
   - Duties that require separation, and who holds which one (feeds 3.1.4).
   - What counts as a non-privileged account or role for a given system (feeds 3.1.6).
   - What counts as a privileged function, defined by category rather than an exhaustive list of every action (feeds 3.1.7).
   - The conditions that terminate a user session, written as something you can actually configure or enforce, such as "logoff" or "account disabled" rather than an idle timeout nobody will tolerate (feeds 3.1.11).
   - What audit events need to be captured, and why, since the organization sets this list itself against its own risk judgment (feeds 3.3.1).
   - Which ports, protocols, services, functions, and programs are essential, restricted, or prohibited (feeds 3.4.7).
   - How often logs actually get reviewed, and by whom, stated as a cadence the reviewer will really keep (feeds the review half of 3.3.1 and 3.1.4's log-review separation evidence).
   The rule that runs through every one of these: never define a separation, a category, or a condition you cannot actually implement and evidence. The definition itself is what an assessor holds you to, so a definition that outruns what the company can do becomes a self-inflicted finding.

5. **Set periodicity at "at least annually" as the floor, and write the stated period longer than the actual cadence.** Every objective that asks for a review, scan, or assessment frequency treats "periodic" as meaning at minimum once a year; several teams choose to run some activities more often depending on how risky they judge them, while annual stays the floor nobody can fall under. Write the policy's stated frequency at or above what the team actually intends to do in practice, for example stating "quarterly" in policy while scanning weekly, or stating "annually" while reviewing more often for high-risk items. This gives room to miss a single cycle without that miss becoming, by itself, a finding against the written policy. It does not excuse missing the stated floor; it only protects against a stricter internal habit turning into a paper trap.

6. **Attach a review trigger to every policy, not just a frequency.** A policy that names only a calendar interval will be checked against operations that changed since the last review. Add a second trigger: review and update after any significant change to what the policy covers, not only on the calendar date. This mirrors how the underlying NIST control families handle their own policy-and-procedure entries: a defined review frequency, plus a defined triggering event, both pointed at whoever is designated to own the document.

7. **Keep brittle technical specifics out of policy text; put them in the standard or baseline layer instead.** The clearest example is audit logging: policy should say that privileged function execution and defined audit events must be logged, not list the specific Windows Event IDs or the specific log source names to capture, because that list changes independently of the management decision to log at all and belongs in a baseline document. Apply the same rule anywhere a policy sentence would otherwise need to be rewritten every time a product version or a specific technical setting changes.

## Output

Write `policies/document-discovery.md` and `policies/writing-order.md` in the engagement repo.

```markdown
# Document discovery inventory: <client>

Built from document discovery on <date>, before any policy drafting began.

| Document | Owner | Covers | Current or stale | Reused as | Notes |
|---|---|---|---|---|---|
| | | | | Policy / standard / procedure / not usable | |

## Gaps found
- <process areas with no existing documentation at all>
```

```markdown
# Policy writing order: <client>

Sequence confirmed: flow mapped (scope/data-flow.md, dated <date>) -> processes documented -> processes tweaked to close gaps -> policy drafted to match.

## Writing order, per process area

For each process area (access control, audit and accountability, configuration management, and so on), draft the five layers in this order, bottom of the hierarchy first:

1. **Standard / control** - the technical bar and the mechanism that meets it, written from what the now-tweaked process actually does.
2. **Procedure** - the step-by-step instructions, written from the same tweaked process, checked against the person who actually does the work.
3. **Control objective** - the outcome stated in one sentence, checked against steps 1 and 2 to confirm they actually produce it.
4. **Policy** - the management decision, written last, to match steps 1 through 3, not the other way around.
5. **Guideline** (optional) - non-binding advice for doing the procedure well, added only if it helps the person doing the work.

| Process area | Standard/control drafted | Procedure drafted | Control objective confirmed | Policy drafted | Guideline (optional) |
|---|---|---|---|---|---|
| | | | | | |

## Definitions to carry into every relevant policy
| Term | Definition used | Requirement(s) it feeds |
|---|---|---|
| | | |

## Periodicity table
| Activity | Stated policy frequency | Actual intended cadence | Review trigger |
|---|---|---|---|
| | | | at least annually and after significant change |
```

Both files are inputs to whichever policy-drafting work follows; they are not the policies themselves. Hand off with a note: no policy for a process area gets drafted until that area has a procedure entry with a status of current.

## Where practitioners disagree

- Whether a client's documentation set should be one combined governance document covering every control family, or a separate policy per family (access control, audit, configuration management, and so on). Smaller organizations tend toward one combined document with the family-level content organized as sections; larger ones split it out. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run document discovery as its own scheduled meeting, separate from the data flow interviews, and bring a checklist of common manufacturing documentation (QMS, AS9100 work instructions, traveler tracking) so the client recognizes what they already have instead of describing it as "nothing." **OSC seat**: if you are writing your own policies without outside help, resist the pull to start from a purchased template; run the sequence in Method step 2 first even informally, then use a template only to check that your own draft covers the same ground a control's policy-and-procedure requirement expects.

## Sources

- Fun with NIST Policy Controls, Summit 7: https://www.youtube.com/watch?v=TXsKdH3hC6E (the policy, control objective, standard, procedure layering; review frequency plus triggering-event pattern; keeping brittle technical detail out of policy text).
- Unified Scoping Guide, ComplianceForge: https://complianceforge.com/ (the policy to control objective to standard to control to procedure to guideline documentation hierarchy).
- CMMC Level 2 Assessment Guide, DoD CIO, 3.11.2 and 3.12.1: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (periodic defined as at least annually).
- Practitioner consensus, unattributed, backs the flow-then-process-then-tweak-then-policy sequence, the document discovery pass as a first step, the power-of-definition technique applied across 3.1.4, 3.1.6, 3.1.7, 3.1.11, 3.3.1, and 3.4.7, and the practice of stating a policy period longer than the actual operating cadence.
