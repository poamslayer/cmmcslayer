# cmmcslayer

A skills repo for taking a defense contractor through NIST SP 800-171 Rev 2 and a CMMC Level 2 assessment. Two layers: a **flow layer** ported from mattpocock/skills (MIT) and rewritten to operate on a CMMC engagement, and a **domain layer** of skills derived from a private practitioner wiki under the source policy in ADR-0001.

This file is the repo's own glossary. Skills use these terms exactly. The engagement repo that `setup-poamslayer-skills` scaffolds gets its own `CONTEXT.md` for the client's vocabulary; that one is separate from this one.

## Language

**Requirement**:
One of the 110 NIST SP 800-171 Rev 2 security requirements, written `3.x.y` (for example `3.1.1`). The unit an SPRS score is computed over. A control file describes one requirement.
_Avoid_: control (the 800-53 word; use it only when quoting 800-53 or a crosswalk), practice (the CMMC 1.0 word).

**Objective**:
One of the 320 NIST SP 800-171A assessment objectives, written with the requirement and a bracketed letter, `3.1.1[a]`. The unit an assessor scores and the unit an SSP conformity statement covers. A requirement is MET only when every applicable objective is MET.
_Avoid_: sub-control, criterion.

**Family**:
One of the 14 groups of requirements (AC, AT, AU, CA, CM, IA, IR, MA, MP, PE, PS, RA, SC, SI).

**MET / NOT MET / N/A**:
The three assessment findings from 32 CFR 170.24(b). MET means every applicable objective is satisfied by evidence in final form. NOT MET means at least one objective is not. N/A means the requirement or objective does not apply, with a justification a human wrote.

**CUI**:
Controlled Unclassified Information, defined in 32 CFR Part 2002. Information the Government owns, or that a contractor makes for the Government under a contract, where a law, regulation, or Government-wide policy calls for safeguarding. Ownership comes first: information the company owns is not CUI to the company.

**FCI**:
Federal Contract Information as defined in FAR 52.204-21. Not CUI. Drives Level 1 only.

**CTI**:
Controlled Technical Information, the CUI category most build-to-print work involves. DoDI 5230.24 defines it as "technical information with military or space application that is subject to controls on access, use, reproduction, modification, performance, display, release, disclosure, or distribution." It is a DoD category, so it also needs a DoD nexus: a controlling DoD office, or data provided by or for DoD under the contract. Correctly marked CTI carries a Distribution Statement B through F, never A, but a statement on a document does not make it CTI. CTI status and ITAR or EAR status are separate determinations: an export warning alone does not make data CTI, and CTI is not always export controlled.

**Re-used CUI**:
CUI content that the company incorporates, restates, or paraphrases into a document it creates, as 32 CFR 2002.4(pp) defines re-use (a traveler that copies the customer's dimensions, an inspection report that quotes the drawing's requirements). Re-use is a form of handling. The CUI content stays CUI, and the source agency is still the one that designated it. The new document is CUI because of the content it carries, never because of the document it came from: whatever the company adds of its own (its methods, its toolpaths, its routing) is not CUI to the company.
_Avoid_: derivative CUI, contaminated, "inherits the source's status". CUI is not a classification system, and its status does not spread by contact.

**Data category**:
A label that says why a piece of information needs protecting and under which obligation. An item carries every category that applies, so one drawing can be CUI, export-controlled, and third-party proprietary at once. The categories:
- **CUI**, named with its Registry category, for example CUI (CTI).
- **FCI**, as defined above.
- **Export-controlled**, naming ITAR or EAR, from `export-control-overlay`.
- **Proprietary (own)**: the company's own IP, processes, and pricing. Protected by trade secret law and by the company's own choices.
- **Proprietary (third-party)**: a customer's or supplier's information held under an NDA, a license, or a proprietary legend. Protected by that agreement.
- **PII**: personal information about people, such as employee and HR records. Protected by privacy law and contract.
- **Security Protection Data**: logs, alerts, configurations, and vulnerability data about the security of the scope, as 32 CFR 170.4 defines it.
- **Public**: published or released without restriction, including Distribution Statement A. It cannot be combined with CUI or either Proprietary label.

Only CUI and FCI set the CMMC assessment scope, and Security Protection Data decides how SPAs and ESPs are treated. The other categories do not add assets to scope. They are recorded so that "not CUI" never reads as "not sensitive."
_Avoid_: "sensitive" as a label, and "not CUI" as the whole record.

**Controlled customer technical data**:
The customer's technical data that arrives already regulated: anything carrying a CUI marking, an export-control warning (ITAR, or EAR other than EAR99), or a DoD Distribution Statement B to F. It is the boundary an enclave is built around: the company chooses to apply NIST SP 800-171 to all of it, so nobody has to decide CUI or not at the inbox. Choosing to apply 800-171 is not a CUI determination. Each item keeps its own data categories, and only `cui-determination-workflow` says which items are CUI. Business records (quotes, purchase orders, invoices, schedules) are not technical data and stay outside (DFARS 252.227-7013).
_Avoid_: "treat it as CUI", "CUI enclave" for an enclave that holds no CUI. Say "we apply 800-171 to it".

**CUI Asset**:
An asset that processes, stores, or transmits CUI. Assessed against every Level 2 requirement. One of the five asset categories in the CMMC Level 2 Scoping Guide and 32 CFR 170.19(c).

**Security Protection Asset (SPA)**:
An asset whose job is protecting the scope: a firewall, an identity provider, endpoint detection, an RMM with admin reach, a log platform. Assessed only against the requirements its capability touches.

**Contractor Risk Managed Asset (CRMA)**:
An asset that could touch CUI but is not meant to, and sits unseparated from CUI Assets. Documented in the SSP, whose assets are the inventory, and in the network diagram; reviewed through the SSP, with limited checks if the documentation is weak.

**Specialized Asset**:
IoT, IIoT, operational technology, government furnished equipment, restricted information systems, and test equipment that can handle CUI but cannot be fully secured. Documented in the SSP, whose assets are the inventory, and in the network diagram; managed under a risk-based policy; not assessed against the Level 2 requirements at Level 2.

**Out-of-Scope Asset**:
An asset that cannot process, store, or transmit CUI, provides no security protection, and is physically or logically separated. The bar is "cannot", a technical inability, never a policy. Not assessed; the justification must be ready.

**Asset**:
One inventory item in the SSP, listed in the file of the component it is an instance of: a real laptop, server, service tenant, or device. The asset carries the CMMC category (one of the five above), and, for a Specialized Asset, its kind. People read the assets in the generated view page `view/asset-inventory.md`.
_Avoid_: "system" for a single asset.

**Component**:
A named part of the system that conformity statements describe once: "Entra ID", "Windows 11 laptops (engineering)", "Access Control Policy". Several assets can be instances of one component. A component carries a category only as a shorthand when every asset behind it shares that category; when they do not, the component is split. A component is known by its slug, the name of its file in the SSP, and a conformity statement names the component by that slug.
_Avoid_: using "asset" and "component" interchangeably.

**Scope**:
The CMMC Assessment Scope: the set of assets and the categories assigned to them, recorded in the SSP and drawn in the network diagram, `scope/network-diagram.drawio`.
_Avoid_: boundary as a synonym for the whole scope (the SSP's "system boundary" is one part of it).

**Applicability**:
The per-asset question of which requirements bear on it, decided after scope. Every in-scope asset must address all 110; it need not implement all 110.

**ESP**:
External Service Provider, as defined in 32 CFR 170.4: an outside organization that processes, stores, or transmits CUI, or provides security protection, within the scope. MSPs, MSSPs, and SOC providers are ESPs.

**CSP**:
Cloud Service Provider, a type of ESP that offers cloud services. When a CSP holds CUI it needs a FedRAMP Moderate authorization, or equivalency under the DoD CIO memo. An ESP that is not a CSP does not face that bar.

**Responsibility matrix**:
The document that states, per requirement, what the company implements and what each ESP implements. Also called the customer responsibility matrix (CRM) or shared responsibility matrix. In an engagement it is generated from the SSP, the providers and the conformity statements on their components, as the view page `view/esp-responsibility-matrix.md`; nobody writes it by hand.
_Avoid_: CRM on its own, because it collides with customer relationship management.

**SSP**:
System Security Plan, required by 3.12.4. In this repo the SSP is the `ssp/` folder of the engagement repo, in Markdown with YAML frontmatter: one file per requirement holding the conformity statements on its objectives, and one file per component holding its assets and, for an outside provider, its role and FedRAMP status. It is the record (ADR-0012, which replaced the OSCAL record of ADR-0007).

**SSP view**:
The read-only Markdown that scribe renders from the SSP into the engagement repo's `view/` folder, for people: a prose page per requirement, the asset inventory, and the responsibility matrix. No skill reads it and nobody edits it.
_Avoid_: calling the view the SSP.

**Scribe**:
The only skill that changes the SSP. Every other skill that decides something calls it to record the decision, and every skill that reads the SSP calls it to show the record, read from the SSP files at that moment. A change is refused, and the files restored, when the result breaks the SSP's rules.

**Conformity statement**:
The sentence or short paragraph in the SSP that says how one objective is satisfied by one component. It attaches to the objective, not only to the requirement (ADR-0008), and to the component it describes, so its text never needs to name the component. Each carries an implementation status: implemented, partial, planned, alternative (met another way, with the reason), or not applicable (does not apply to this component, with the reason).

**Definition and enforcement pattern**:
Say the organization-wide decision once, at the objective that asks whether something is defined. At the objective that asks whether it is enforced, write one statement on each component that carries out that decision, saying how.

**Open items list**:
Where an unverified fact goes: one Markdown list in the engagement repo, `scope/open-items.md`, outside the record. Each line names the fact, the objective it bears on when there is one, and who will confirm it. Never inside a conformity statement: an objective whose statement waits on an open item is recorded planned (ADR-0010). Text such as "to be confirmed" inside a statement is a lint failure.

**POA&M**:
Plan of Action and Milestones. A requirement assessed NOT MET during an assessment, with milestones the company controls and a hard 180-day closeout from the Conditional CMMC Status Date (32 CFR 170.21). Only 1-point requirements and the 3-point 3.13.11 case are eligible, and six requirements are never eligible. In an engagement repo a POA&M item is a ticket on the engagement's tracker, a GitHub issue or a local Markdown file, labeled `poam` and `req:<id>`.

**OPA**:
Operational Plan of Action. A temporary deficiency that arises after the system was compliant, assessed MET under 32 CFR 170.24(b)(1)(ii). No milestones the company controls, no 180-day clock. In an engagement repo an OPA item is a ticket on the engagement's tracker labeled `opa` and `req:<id>`.

**Enduring exception**:
A permanent deviation described in the SSP with its mitigations, assessed MET under 32 CFR 170.24(b)(1)(i). Its home is the SSP; it never goes on a POA&M or an OPA.

**SPRS score**:
The Level 2 score from 32 CFR 170.24(c)(2): 110 minus the point value of every NOT MET requirement, using the 5, 3, 1 table and the two adjustable requirements 3.5.3 and 3.13.11.

**Significant change**:
A change to a certified environment large enough to require a new assessment. The Affirming Official decides.

**Affirming Official**:
The senior company official who signs the CMMC affirmation and owns the significant change decision.

**C3PAO**:
CMMC Third-Party Assessment Organization. Conducts Level 2 certification assessments.

**Control file**:
One Markdown file per requirement under `skills/domain/gap/control-evidence-lookup/controls/`, with the requirement and its objectives, the five sections Sufficient, Insufficient, Over-engineering, Edge cases, Evidence examples, and related requirements. The audit flow reads it to know what fails.

**Low confidence**:
A control file whose source page was thin. Marked `confidence: low` in frontmatter and not padded.

**Vault**:
Two different things, and the collision is deliberate to note rather than rename. In `vault_sources` frontmatter it means the private practitioner wiki the domain layer derives from. In control file prose it means a password vault: a credential store that releases a shared or privileged password against a checkout record, which is what 3.5.1, 3.5.3 and 3.5.10 accept as evidence. The public surface only ever carries the second meaning, because `vault_sources` is stripped before anything is published.
_Avoid_: using the bare word in an instruction. Say "the private wiki" or "a password vault".

**Seat**:
Who the operator is. The **consultant seat** runs engagements for clients and hears the engagement vocabulary as is. The **OSC seat** is the organization seeking certification, usually its IT lead, and gets plain-language framing that names who in the company each step needs. The seat is a tone switch, not a gate: both seats travel the same main flow and can reach every skill. Recorded by setup in the engagement repo.

**Operator**:
The person driving the skills, in either seat.

**Engagement repo**:
The per-client git repo that `setup-poamslayer-skills` scaffolds: `CONTEXT.md`, `docs/adr/`, `scope/`, `ssp/` holding the SSP, the generated `view/`, `evidence/`, `policies/`, `.scratch/`, with POA&M and OPA items as tickets on its tracker. Nobody writes an asset inventory or a responsibility matrix: the SSP holds what they say and the view shows them.

**Fixture**:
The fictional machine shop under `docs/fixture/` with its known answers and grader rubric. Every skill is checked by a cold run against it.

**Cold run**:
A fresh subagent given only a skill, the fixture, and the prompt an operator would type. Graded by a second subagent against the known answers and the rubric.

**Scrub check**:
`scripts/scrub_check.py`. Fails on any private handle, unattributed real name, venture name, or verbatim run of text from the private wiki.

**Flow**:
A skill that sequences other skills along an engagement (find-cui, wayfinder, to-ssp, to-poam, remediate, audit, ssp-lint, triage), the record's one writer (scribe), or a ported process primitive (grilling, handoff, research, wizard, to-questionnaire, and the rest).

**Domain skill**:
A skill that holds CMMC judgment, derived from the vault under ADR-0001, with `vault_sources` in its frontmatter.

**Authority tier**:
How much a cited source can settle, from Tier 1 (regulation and statute, which can establish a rule or a status) through Tier 2 (official federal guidance), Tier 3 (public secondary sources, method only) and Tier 4 (unattributed practitioner consensus). Set by ADR-0004.
_Avoid_: "authoritative source" without a tier.

**Authorities register**:
`reference/authorities.md`, the one list of every source the skills cite, each with its tier.

## Relationships

- A **requirement** has several **objectives**; a requirement is MET only when all its objectives are.
- The **SSP** holds one **conformity statement** per objective and component; **scribe** writes it, and the **SSP view** is rendered from it.
- An **asset** is an instance of one **component**. The **category** belongs to the asset; a conformity statement is attached to the component, so its text does not name it.
- A **NOT MET** objective becomes a ticket routed to **POA&M** or **OPA** by `poam-or-opa-router`, after `sprs-score-and-poam-eligibility` checks the gates.
- A **control file** feeds **audit**, `control-evidence-lookup`, `over-engineering-guard`, and `evidence-package-builder`.
- The **seat** is recorded by `setup-poamslayer-skills` and read by every flow that adapts its wording.
- The **fixture** and the **cold run** are how any skill is tested; the **scrub check** runs on every output.
- A **data category** is recorded for every item `cui-determination-workflow` looks at, next to its CUI determination, not instead of it. The overlaps that come up most:
  - A design the company owns outright is **Proprietary (own)** and can also be **Export-controlled**, and it is still not CUI to the company. Ownership removes CUI status. It does nothing for ITAR or EAR.
  - A customer's drawing can be **CUI (CTI)**, **Export-controlled**, and **Proprietary (third-party)** when it carries the owner's legend.
  - **PII** the company holds about its own staff is not CUI. PII the Government provides can be CUI (Privacy), and then it is labeled CUI.

## Flagged ambiguities

- "control" is used loosely in the industry for a requirement, an objective, or an 800-53 control. Resolved: requirement and objective are the two units here; control is reserved for 800-53 and for the phrase "control file".
- "CRM" collides with customer relationship management. Resolved: responsibility matrix.
- "in scope" gets read as "implement all 110 on this asset". Resolved: scope and applicability are separate terms.
- "Proprietary" collides with PROPIN, the Government's CUI marking for a contractor's proprietary business information once the Government holds it (the delivered Copy B). Resolved: Proprietary (own) and Proprietary (third-party) are the company's labels for its own copies; PROPIN is only ever part of a CUI determination.
- "Derivative CUI" is borrowed from derivative classification in the classified world, where status follows the content into every new document. Resolved: the term is retired. **Re-used CUI** is the content a new document carries, and the rest of that document is judged on its own.
- "Treat as CUI" gets read as "it is CUI". Resolved: a company applies NIST SP 800-171 to **controlled customer technical data** by choice, and that choice is recorded apart from any CUI determination.
- "POA&M" gets used for any tracked deficiency. Resolved: POA&M, OPA, and enduring exception are three different things with three different scoring outcomes.
