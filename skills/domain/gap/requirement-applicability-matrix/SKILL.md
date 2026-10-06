---
name: requirement-applicability-matrix
description: Decide which of the 110 NIST SP 800-171 Rev 2 requirements bear on each in-scope component, separate "address" from "implement", record each not applicable and alternative status with its reason in the SSP through scribe, and keep a requirements traceability matrix per component. Use after scope is set and before SSP writing, whenever someone assumes "in scope" means "implement all 110 on every asset".
vault_sources:
  - "Requirement Applicability"
  - "Scoping vs Applicability"
  - "Must-Have vs Nice-to-Have Security Controls"
  - "CMMC Scoping"
  - "3.1.11"
  - "3.13.11"
  - "raw/unified-scoping-guide.pdf"
public_sources:
  - "CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.19 (CMMC scoping): https://www.ecfr.gov/current/title-32/section-170.19"
  - "CMMC Level 2 Assessment Guide, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "NIST SP 800-171A: https://csrc.nist.gov/pubs/sp/800/171/a/final"
  - "Unified Scoping Guide, ComplianceForge, CC BY 4.0: https://complianceforge.com/"
---

# Requirement applicability matrix

Scope answers one question: do I assess this asset at all? Applicability answers the next one: which requirements bear on this in-scope asset? This skill answers the second question, one component at a time. It records every "does not apply" and every "met another way" in the engagement's SSP, `ssp/ssp.json`, by calling the Skill tool with `scribe`, and keeps the whole answer as a requirements traceability matrix. It refuses to draw the scope line (call the Skill tool with `cmmc-scope-boundary` for that), it refuses to judge whether an implementation is good enough (that is `control-evidence-lookup`), and it refuses to run on an asset that has no category yet.

## Inputs

- The record, `ssp/ssp.json`: the components, every asset with its category (CUI Asset, Specialized Asset, Security Protection Asset, Contractor Risk Managed Asset, or Out-of-Scope Asset), the providers, and the statements already recorded. Read it by calling the Skill tool with `scribe` and asking it to show the record; that is the current state. Never read `view/`, which is generated for people.
- `scope/open-items.md`, for assets scoping has not placed yet.
- `scope/network-diagram.drawio`, `scope/network-diagram.md`, or the data flow notes, so the function test can see where CUI is actually encrypted, authenticated, and logged.
- The engagement `CONTEXT.md` for the client's component vocabulary.
- Optionally, an existing `scope/applicability-matrix.md` to update.

## Method

1. **Confirm scope is closed for the components you are working.** Every asset in the record carries exactly one category; scribe will not record one without it. If the open items list still names assets scoping has not placed, stop and send them back to scoping, unless the operator names components whose categories are settled: then work those, and list the rest on the open items list. A row may be inherited from a control plane that is recorded as a component but has no asset or category yet, such as the firewall; say so on the open items list, because the inherited row is only as good as that component's placement. Do not let applicability become a way of arguing an asset out of scope. Out-of-Scope Assets get no matrix.

2. **Work per component, not per device.** A component in the record is a set of assets that share an operating system, a role, and a management plane: "Windows 11 endpoints under Intune", "Entra ID", "SharePoint Online", "shop-floor CNC controllers", "the edge firewall". Writing the SSP per individual device produces redundancy an assessor has to wade through; writing it per component is what assessors have accepted. When the assets behind one component need different answers, the component needs splitting: that is scoping's call, so put it on the open items list for `cmmc-scope-boundary` and work the component as recorded. Until it is split, a requirement that applies to any asset behind the component applies to the component: never record it not applicable because most of the assets are desktops when one is a laptop. People, processes, and facilities are components too, because some requirements apply only to them. When the record has none for one the matrix needs, ask scribe to add it: a written policy or plan as type `policy`, a program or practice that governs people, such as "Security awareness training", as `process-procedure`, and a facility as `physical`. Those are the only components this skill adds.

3. **Apply the address-versus-implement rule.** Every in-scope component has to address all 110 requirements. Implementing all 110 is a separate question, and the answer is usually no. Addressing a requirement means you evaluated it against the component and recorded the outcome. Deciding that a requirement does not apply to a firewall is still addressing it, provided the reason is written down. This vocabulary is not in the Scoping Guide or 32 CFR Part 170; it is practitioner consensus that fills a gap the DoD documents leave open.

4. **Run the asset-type test.** Requirements are written for kinds of assets. Ask: is this requirement about a device, a person, a process, or a facility? Then ask whether this component is that kind of thing. The Unified Scoping Guide gives the canonical examples: a firewall takes MFA, access control, a baseline, and patching, but cannot take awareness training, sign a non-disclosure agreement, or run an incident response exercise; a person can be trained and can sign, but cannot be baselined, scanned, or patched; an incident response plan is a document and cannot sign, authenticate, or be patched. If the component is not the kind of thing the requirement is written for, ask one more question before calling it N/A: is the requirement carried out *for* this component by something else? Physical protection (3.10) protects the server by locking the room; incident response (3.6), risk assessment (3.11), security assessment (3.12), and screening (3.9.1) cover the server because the organization runs them over every system. Those rows are **inherited from <the facility, process, or plan component>**, not N/A: "3.10.1 does not apply to the NAS" reads to an assessor as a claim that nobody limits physical access to it. Mark a row **N/A by asset type** only when the requirement cannot bear on this component at all: the firewall does not take training, and a device with no camera has no collaborative device to control. Record the one-line reason. Never record not applicable on a fact nobody has confirmed, such as whether a device has a local console: put the fact on the open items list and leave the row open.

5. **Run the function test.** A requirement lands on the component that performs the function the requirement protects, not on every component the protected data passes through. The test case is FIPS-validated cryptography (3.13.11): it applies to the module doing the encrypting, not to a switch or router carrying ciphertext it cannot read. The same logic puts session termination (3.1.11) at Microsoft Entra ID for every Microsoft 365 workload, because Entra ID owns the token and the session, rather than at SharePoint, Exchange Online, and Teams separately. Ask: which component actually does this? Mark the others **inherited from <component>**. A requirement whose subject does not exist at the organization, such as secure software development at a company that writes no software, is N/A with that reason, recorded on the component that would carry it rather than on every device.

6. **Triage each remaining requirement three ways.** For every requirement the two tests leave standing against a component, pick one outcome:

   | The component | Outcome | What to write |
   |---|---|---|
   | Cannot technically implement the requirement | Addressed, not implemented | Why it is technically impossible, and what compensates |
   | Can implement it, but there is a strong business reason not to | Addressed, not implemented | The business justification, and what compensates |
   | Can implement it, with no defensible reason to decline | Implement | How it is implemented, per objective |

   "Strong business reason" means a reason you would say to an assessor's face and that a competitor in the same business would recognize. Cost alone is not one. Anything in the first two rows without a written justification is a silent N/A, and a silent N/A is a NOT MET waiting to happen. An "addressed, not implemented" row with nothing that compensates is not an alternative at all: the objective is simply not met, and it is a gap for `/audit` and a ticket, not a status this skill records. Write it in the matrix with the outcome "gap, nothing compensates".

7. **Collapse inherited components onto their control plane.** Where several components federate to one identity provider, one log platform, or one endpoint manager, write the organization-wide decision once at the objective that asks whether something is defined, then at the enforcement objective write one statement on each component that carries it out, naming the control plane that enforces it (the definition and enforcement pattern in the glossary). In the matrix, the definition row is inherited from the policy or process component that makes the decision, and the enforcement row is implemented on each component. It doubles as the working argument for federating whatever you can onto one identity provider: it lands the Access Control and Identification and Authentication families on a single enforceable plane, and fewer objects have to be assessed.

8. **Correct the category confusion.** The five asset categories in the Scoping Guide and 32 CFR 170.19(c) tell the assessor how much assurance work each asset gets. They do not tell you which requirements apply. For the organization, the burden is the same for a CUI Asset, an SPA, and a CRMA: address all 110. The one category that changes the burden is Specialized Assets, which are documented and managed under a risk-based policy and not assessed against the requirements at Level 2. The requirements that most often fall away for an SPA or CRMA are those that name CUI in the objective, such as FIPS-validated cryptography for CUI confidentiality and the FedRAMP bar for a cloud service holding CUI. The Scoping Guide also says an SPA is assessed against the requirements relevant to the capability it provides; record that capability in the matrix so the assessor sees the same list you do.

9. **Mark the compliance floor versus discretionary rows.** Every row that implements a requirement is a minimum compliance requirement: driven from outside by the contract. Anything you add beyond the objectives is a discretionary security requirement: driven by your own risk appetite. Tag discretionary rows so `over-engineering-guard` can see which spend is optional. Being compliant is not the same as being secure; the matrix records what the objectives require, and the discretionary tag records what you chose on top.

10. **Record the not applicable and alternative rows through scribe.** Each outcome maps to one implementation status, recorded on every objective of the requirement for that component. A not applicable row does not answer the objective for the system: scribe keeps it planned on "This System" until a component records how it is met, so recording the not applicable rows first leaves no requirement reading as if it applied nowhere.

    | Matrix outcome | Status in the record | Statement | Remarks |
    |---|---|---|---|
    | N/A by asset type | not applicable | One sentence: the requirement does not apply to this component, and why. | The one-line reason, such as "3.2.1 is written for people, and the firewall is a device." |
    | Addressed, not implemented, with a compensating measure | alternative | What the component does instead, naming the compensating measure. | Why the requirement itself is not implemented: the technical impossibility or the business justification. |
    | Inherited from another component | nothing on this component | | |
    | Implement | nothing here: `to-ssp` writes it | | |

    Not applicable means the requirement does not apply to this component; alternative means it applies and is met another way. Never use one for the other. A Specialized Asset's component gets no not applicable rows: it is not assessed against the requirements at Level 2, which is different from their not applying, so its matrix records the risk-based policy instead. When an objective of the requirement does apply to the component while the others do not, record the status only on the objectives it covers.

    Show the operator each component's rows as a table, then call the Skill tool with `scribe` and give it the component's rows as one set, so they are validated once. Record straight away if the operator asked you not to stop, and show the tables afterwards. If scribe refuses, the refusal names the row: fix it and give scribe the set again. When the record already holds a statement on that objective and component that your row contradicts, say so to the operator and record yours only if they confirm; it replaces the old one. A statement on another component that the matrix shows is wrong, such as a not applicable claim the facts contradict, is not yours to change: put it on the open items list for `to-ssp`. Never write `ssp.json` yourself, and never edit anything under `view/`.

11. **Write the matrix and hand it forward.** One table per component, one row per requirement, kept as the working note `scope/applicability-matrix.md`. The not applicable and alternative rows are also in the record; `to-ssp` writes the implement rows from the matrix, not the other way around.

## Output

- The not applicable and alternative statuses, with their reasons, recorded in `ssp/ssp.json` by scribe on every objective they cover (step 10). Scribe re-renders `view/requirements/<id>.md`.
- `scope/applicability-matrix.md`, the working note. It stays Markdown and holds every row, including the inherited and implement rows the record does not.
- A one-line entry in the engagement `CONTEXT.md` glossary for each component name the matrix introduces.
- Any component that needs splitting, or asset scoping has not placed, on `scope/open-items.md`.

```markdown
# Requirements traceability matrix

Scope closed on: YYYY-MM-DD (ssp/ssp.json at commit <sha>)

## Components

| Component | Category | Kind (device / person / process / facility) | Control plane it inherits from |
|---|---|---|---|

## <Component title, as recorded> (category: CUI Asset / SPA / CRMA / Specialized)

Capability provided (SPA only): ...

| Req | Test result | Outcome | Justification or mechanism | Objectives covered | Floor or discretionary | Recorded as |
|---|---|---|---|---|---|---|
| 3.1.1 | applies | implement | Entra ID groups, LAPS; statements by to-ssp | a-f | floor | (to-ssp) |
| 3.2.1 | N/A by asset type | not applicable | A firewall does not take training | a-d | n/a | not applicable |
| 3.5.3 | applies | gap, nothing compensates | The admin console takes a password only | c | floor | (none: a gap for /audit) |
| 3.13.11 | inherited from Windows 11 endpoints | inherited | Switch carries ciphertext only; encryption at endpoint TLS | a | floor | (none) |
| 3.10.1 | inherited from Office building | inherited | The closet door lock and the visitor log limit physical access to the switch | a-f | floor | (none) |
| 3.7.5 | applies | addressed, not implemented | Cannot: controller firmware has no MFA; compensating: physical access log | a-d | floor | alternative |

Rows with outcome "addressed, not implemented" and an empty justification are lint failures.
```

Counts to check before closing: every one of the 110 requirements on each component, one row per outcome (a requirement whose objectives split between outcomes takes one row per outcome, each naming its objectives), no empty justification, no row marked both "implement" and "N/A", and every not applicable or alternative row present in the record on the objectives it covers.

## Where practitioners disagree

- **Whether assessors accept the address-versus-implement vocabulary.** It is not in the Scoping Guide, the Assessment Guide, or 32 CFR Part 170. Most assessors have accepted a matrix that records a justified "does not apply" per component. Some assessors read "in scope" as "show me the requirement on this asset" and press for implementation or a formal N/A finding. The outcome depends on the assessor.
- **Whether an SPA or CRMA sheds the CUI-specific requirements.** One position: an objective that names CUI cannot apply to an asset that never holds CUI, so FIPS and FedRAMP fall away. The other: the SPA protects the scope and is assessed against everything relevant to its capability, and some assessors count encryption of security protection data as relevant. The outcome depends on the assessor.
- **Whether category changes the organization's burden.** Practitioner consensus says only Specialized Assets change it. Some assessors give CRMAs a lighter review as the Scoping Guide allows, and some run the limited checks the guide permits when the SSP narrative is weak. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: build the matrix before the first SSP statement and walk the client through the three-way triage on two components they care about (the endpoints and the shop floor) so they see that "addressed, not implemented" is a real outcome. **OSC seat**: you do not need to implement 110 requirements on your firewall. You need to be able to say, for each one, "here is how" or "here is why not". Fill the justification column yourself; it is the part an assessor will ask you, not your consultant.

## Sources

- CMMC Level 2 Scoping Guide v2.13, DoD CIO, and 32 CFR 170.19(c): https://www.ecfr.gov/current/title-32/section-170.19 (the five asset categories and what each is assessed against).
- Unified Scoping Guide, ComplianceForge, CC BY 4.0, "Scoping ≠ Applicability" and Appendix C: https://complianceforge.com/ (the firewall, person, and incident response plan examples; the matrix remedy; minimum compliance versus discretionary requirements). See also reference/usg-zones-to-cmmc-categories.md.
- CMMC Level 2 Assessment Guide, DoD CIO, 3.1.11 and 3.13.11: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the objectives the function test is run against).
- NIST SP 800-171A: https://csrc.nist.gov/pubs/sp/800/171/a/final.
- Practitioner consensus, unattributed, backs the address-versus-implement rule, the three-way triage, the asset-type and function tests as applied to 800-171, the control-plane collapse, and the statement that only Specialized Assets change the organization's burden.
