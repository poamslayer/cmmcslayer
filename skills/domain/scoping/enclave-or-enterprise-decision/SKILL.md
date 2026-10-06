---
name: enclave-or-enterprise-decision
description: Choose the CMMC architecture before money is spent. Refuses the headcount rule of thumb, decides on the business case, lays out the five architectures with their tradeoffs, draws an enclave around controlled customer technical data, handles an enclave that holds no CUI, warns about the nonclave, and designs for three years of contracts. Use when an organization asks "enclave or whole company?", has Level 2 flowed down without clear CUI, or is about to buy a tenant, VDI, or segmentation project.
vault_sources:
  - "CMMC Scoping"
  - "Client Onboarding Checklist"
  - "Exchange Online CUI Enclave Pattern"
  - "VDI Scoping"
  - "Practitioner insights A"
  - "Practitioner insights B"
  - "AEC Industry and CMMC"
public_sources:
  - "CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.19 (CMMC Assessment Scope): https://www.ecfr.gov/current/title-32/section-170.19"
  - "CMMC FAQ C-Q2, C-Q12, and F-Q1 through F-Q5: https://dodcio.defense.gov/CMMC/FAQ/"
  - "Public post on matching scope to data: https://reddit.com/r/CMMC/comments/1t5b9t1/_/ok8mwq0/"
  - "Public post on answering twice with a cloud tenant: https://reddit.com/r/NISTControls/comments/kf02ft/_/gg5n41f/"
  - "Public interview on construction and CMMC (three-year design horizon): https://www.youtube.com/watch?v=F5ufR0HtaA4"
  - "IntelliGRC Ep. 11, CUI, Supply Chain Flow-Downs and the Real CMMC Challenges (2026-05-06): https://www.youtube.com/watch?v=PG7aZWUvVvs"
  - "89 FR 83092, the CMMC Program final rule, preamble at 83136 and 83170: https://www.federalregister.gov/documents/2024/10/15/2024-22905/cybersecurity-maturity-model-certification-cmmc-program"
  - "DFARS 252.227-7013 (technical data definition): https://www.ecfr.gov/current/title-48/section-252.227-7013"
---

# Enclave or enterprise decision

This skill answers: which architecture should carry the CMMC Level 2 scope, and why? It produces a decision the organization can defend for three years, recorded as an ADR. It refuses to answer from headcount, it does not price anything, it does not compare vendors, and it does not categorize individual assets (call the Skill tool with `cmmc-scope-boundary` for that after the architecture is chosen). It assumes the data flow map exists; if it does not, call the Skill tool with `cui-data-flow-mapping` first, because the architecture falls out of the map and not the other way round.

## Inputs

- `scope/data-flow.md`: entry points, generated-CUI paths, exits, paper, and backups, each labeled with its data categories (CUI, FCI, Export-controlled, Proprietary own or third-party, PII, Security Protection Data, Public; see `CONTEXT.md`). Only the CUI and FCI flows set the assessment scope. The enclave boundary itself is drawn around controlled customer technical data (step 5), so the Export-controlled flows decide where it goes as much as the CUI flows do.
- The interview notes per role from onboarding, especially who touches CUI and who does not.
- The contract list with clauses, and the pipeline: what contracts the organization expects to bid in the next three years, and what data they will bring.
- The export-control answer (ITAR or EAR now or expected), because it decides the tenant question and shapes physical controls.
- The current environment as the record, the engagement's `ssp/` folder, holds it, if scoping has started: identity backbone, tenant type, VDI, network layout, shop floor systems, SaaS list, as components, assets, and providers in `ssp/components/*.md`. Read the files directly. Never read `view/` instead; it is generated for people and can be stale.
- The seat, from `CONTEXT.md`.

## Method

1. **Refuse the headcount heuristic.** If the question arrives as "we have 40 people and 10 touch CUI, so enclave, right?", say no and explain why. A percentage of staff is not a rule; practitioner consensus rejects the common "under a third of staff means enclave" shortcut. Some organizations are so small, or so integrated in how work moves, that nearly everyone needs CUI at some point, and for them an enterprise-wide scope is correct. Others have hundreds of staff and a dozen who ever see a drawing. Headcount is an input to cost, not to the decision.

2. **Decide on the business case.** Answer three questions from the data flow map and the interviews, and write the answers down:

   | Question | What to look at | Pushes toward |
   |---|---|---|
   | What kind and volume of CUI? | Categories (CTI, export controlled, PII), how many documents a month, paper versus digital | Small and digital: enclave. Large, mixed, or paper-heavy: segmentation or enterprise |
   | How integrated are the workflows? | Does the drawing go from quoting to engineering to the floor to inspection to shipping through one shared system? | Highly integrated: enterprise or segmentation. A few isolated roles: enclave |
   | Can shadow IT be held by training alone? | Interview evidence of thumb drives, personal email, phone photos, notes fields, workarounds when the VPN breaks | Training holds: enclave with policy boundaries. Training will not hold: technical controls, which means segmentation or enterprise |

   The third question is the one people skip. An enclave only works if CUI actually stays inside it; that is a behavior claim, and the interviews tell you whether the organization can keep it.

3. **Lay out the five architectures with their tradeoffs.** Present all five, even when one is obvious, so the ADR records what was rejected.

   | Architecture | What it is | Scope size | Evidence burden | Main risk |
   |---|---|---|---|---|
   | Full enterprise | The whole organizational network is the scope | Largest | Every asset, every requirement, one story | Cost scales with every device; anything bought later is in scope |
   | Enclave | A separated environment used only for work on controlled customer technical data (a dedicated tenant, VDI, dedicated devices, or a dedicated VLAN) | Smallest | Concentrated, but the boundary must be technical and provable | Users route around it; mixed-use endpoints collapse the out-of-scope claim |
   | Segmentation | The production network, with controlled boundaries drawn between the zones holding controlled customer technical data and everything else | Middle | The boundary itself (firewall, ACL, deny by default) becomes the critical artifact | Weak separation is argued at assessment; VLANs alone do not separate |
   | Hybrid | Enclave for digital controlled customer technical data, physical and paper handling treated as its own controlled area | Middle | Two stories: the digital boundary and the physical one | Paper leaks scope into the office; the physical requirements cannot go on a POA&M |
   | Paper only | No digital CUI at all; physical receipt, storage, use, and destruction | Small | Physical protection, media, and personnel requirements carry the weight | One scanned page makes it digital; FAQ C-Q11 still requires an assessment |

4. **Match the scope to the data, not the data to the scope.** If CUI already lives on engineers' or developers' workstations and in their tools, a VDI enclave will be too locked down for the work and the organization will reject it in practice (public post: https://reddit.com/r/CMMC/comments/1t5b9t1/_/ok8mwq0/). The correct move is to draw the scope around where the data has to be, then reduce the data's footprint with need-to-know (3.1.5) and role carve-outs, and only then pick the architecture. Two specific tests before choosing an enclave:
   - **The mixed-use test.** An endpoint that opens the enclave and also does normal business is a CUI Asset, whatever the VDI marketing says. The endpoint is out of scope only when it does nothing beyond keyboard, video, and mouse to the VDI session and cannot process, store, or transmit CUI itself (Scoping Guide; FAQ F-Q1 and F-Q2). Plan for dedicated devices or accept the endpoints in scope.
   - **The remote-user test.** When the only CUI Assets are in a cloud data center reached over the internet, 3.10.1 through 3.10.5 are normally inherited, while 3.10.6 (alternate work sites) is not, and every user counts as a remote user. Budget the controlled home-office story.
   A cloud tenant does not remove the on-premises story either: the organization answers for its requirements once in the cloud and again for whatever remains on site (public post: https://reddit.com/r/NISTControls/comments/kf02ft/_/gg5n41f/).

5. **Draw the enclave around controlled customer technical data.** When the organization receives customer drawings, models, or specifications that carry a CUI marking, an export-control warning, or a DoD Distribution Statement B to F, the recommended enclave holds all of it, not only the items already found to be CUI (ADR-0006; see **Controlled customer technical data** in `CONTEXT.md`). Write the boundary as one sentence: "We apply NIST SP 800-171 to controlled customer technical data." That sentence is a choice about protection, not a CUI determination. Keep the two apart:
   - **Every item keeps its own labels.** The SSP and `scope/data-flow.md` list CUI, Export-controlled, and Proprietary items separately, and only `cui-determination-workflow` says which items are CUI. Writing "treat it as CUI" in the ADR or SSP invites the reading "it is CUI", which is the mistake the workflow exists to stop.
   - **Why it works.** Nobody has to decide CUI or not at the inbox, the enclave protects real data from day one, and CUI that arrives later from the same customers lands where it belongs. Practitioners recommend starting at the point where customer documents are first received, and applying 800-171 where data already regulated by a CUI Registry authority lives (IntelliGRC Ep. 11, from 46:53 and 1:01:19: https://www.youtube.com/watch?v=PG7aZWUvVvs).
   - **Build to the union of the regimes inside.** CMMC does not require US-persons-only access or US data residency; ITAR does. An enclave holding ITAR data usually means GCC High, which is why the tenant question in step 9 takes the export-control answer first.
   - **Business records stay outside.** Technical data excludes "financial, administrative, cost or pricing, or management information" (DFARS 252.227-7013). Quotes, purchase orders, invoices, and schedules stay in the everyday environment as FCI.
   - **Watch the shop floor.** Export-controlled geometry travels into CAM, machine controls, travelers, ERP, and inspection equipment, and "all of it in the enclave" can quietly pull in the plant. Machine controls and CMMs are Specialized Assets (call the Skill tool with `printer-and-ot-asset-scoping`), paper travelers are a physical and media question, and the drawing content copied onto shop paperwork is sorted by `cui-re-use-triage`, including the allow-list of public content that may be copied out.
   - **One intake path.** Customer technical data enters only through the enclave: a dedicated mailbox, a portal, or a file drop inside the boundary, never the general inbox. Name the path in the ADR and in the purchasing and quoting procedure. The intake path is what makes the boundary hold, and it pushes the customer to decide what it really needs to send.

6. **Handle an enclave that holds no CUI.** A sub can have Level 2 flowed down, build the enclave above, and still hold no CUI. In that case:
   1. **Confirm "no CUI" first.** Call the Skill tool with `cui-determination-workflow`; its step 10 is where a sub that cannot see above its prime works out what it received.
   2. **If there is truly no CUI,** call the Skill tool with `flowdown-level-determination` for the level the rules point to and the written point to put to the prime.
   3. **If the organization certifies anyway,** the CMMC Assessment Scope "must be specified prior to assessment" (32 CFR 170.19(a)(1)), and the rule's preamble expects voluntary assessments, including by a provider that is not itself handling CUI (89 FR 83136, 83170). Practitioner experience is that the organization declares the boundary, the assessor validates and assesses it, and nobody asks to inspect the CUI itself; organizations holding no CUI have been certified. How the objectives that need CUI to be present get scored is unsettled (see "Where practitioners disagree"), so agree the scope with the assessor in writing before the assessment starts.
   4. **When the first CUI arrives,** record it as a change and call the Skill tool with `significant-change-determination`.

7. **Warn about the nonclave.** A nonclave is an environment built only to produce an SPRS score or to satisfy a customer's blanket demand, while the real work keeps happening in the everyday environment. It stays non-compliant no matter how clean it looks, because CUI is being handled outside it. Practitioner consensus: if the organization truly never handles CUI, keep the compliant environment as small and simple as possible and say so; if it does handle CUI, an enclave that people do not use is a liability, not a scope reduction. Test for it by asking, per role, "when a drawing arrives, where do you open it?" If the answer is not "inside the enclave", you are looking at a nonclave. An enclave that holds the controlled customer technical data people actually work on is not a nonclave, even before any CUI arrives: the data in it is real, and so is the evidence.

8. **Design for the next three years of contracts.** Ask which contracts the organization expects to bid or win in the next three years, what CUI categories they carry, whether any bring export-controlled data, a new site, a new subsidiary, or a new operating system family. The architecture must hold that future scope, because a later boundary change, a new site holding CUI, a new CSP, or a new OS family is the kind of change that can require reassessment (FAQ C-Q12; public interview: https://www.youtube.com/watch?v=F5ufR0HtaA4). A scope sized for today's single contract and rebuilt in year two costs more than one sized for the pipeline. Call the Skill tool with `significant-change-determination` when a change to a certified scope is already on the table.

9. **Take the tenant question separately.** The enclave decision and the tenant decision are two decisions. The tenant is driven by the export-control answer and the CUI categories, not by the architecture. Call the Skill tool with `gcc-high-decision` after the architecture is chosen.

10. **Write the decision as an ADR** with the rejected options and the reason each was rejected. Record the open debates the organization took a position on (endpoint treatment, wireless, paper, MSP category) so the next person sees why.

## Output

An ADR at `docs/adr/NNNN-cmmc-architecture.md`:

```markdown
# ADR-NNNN: CMMC Level 2 architecture

Date: YYYY-MM-DD. Status: proposed | accepted.

## Context
- CUI kind and volume: ...
- Workflow integration: ...
- Shadow IT: can training hold it? ... Evidence: ...
- Export control: ...
- Three-year pipeline: contracts, data categories, sites, OS families, subsidiaries expected: ...
- Data flow map: scope/data-flow.md (version or date)

## Decision
Architecture: full enterprise | enclave | segmentation | hybrid | paper only
Boundary statement: "We apply NIST SP 800-171 to controlled customer technical data" (or the organization's own wording).
Boundary in one paragraph: what is inside, what technical bar keeps the rest out.
Data categories inside the boundary: CUI (<category>) / Export-controlled (ITAR or EAR) / Proprietary (third-party) ... each listed separately.
Intake path: <the one route customer technical data enters by>.
CUI held today: yes / none yet (determination: scope/cui-determinations.md).
Endpoint treatment: dedicated devices | in-scope mixed-use endpoints | KVM-only VDI clients
Tenant question: deferred to ADR-NNNN (gcc-high-decision)

## Options rejected
| Architecture | Why rejected |
|---|---|
| ... | ... |

## Nonclave check
Per role, where CUI is opened today and where it will be opened after the change: ...

## Positions taken on open debates
- ...

## Consequences
- What becomes in scope, what leaves, what the three-year pipeline adds.
- The change that would reopen this decision.
```

Also add one line to the engagement `CONTEXT.md` under the client's vocabulary: the name the organization uses for its scope ("the enclave", "the CUI network") and what it means.

## Where practitioners disagree

- **How small "so small that enterprise is right" is.** Some practitioners hold that under a certain size every organization should just put everything in scope; others push scope reduction even at ten people. The outcome depends on the assessor only indirectly, through how hard the boundary is tested; the cost outcome depends on the organization.
- **Enclave inside a shared tenant.** A shared mailbox with auto-rerouting data loss prevention and no access for regular users can make the other mailboxes out of scope on a technical-inability argument. Some assessors accept it; others treat everything in one tenant as too entangled and expect CRMA at minimum. The outcome depends on the assessor.
- **Segmentation as scope reduction.** Deny-by-default firewall rules with a justified allow-list are accepted as logical separation; VLANs without ACLs are not; ACLs that pass file shares or print jobs are argued. The outcome depends on the assessor.
- **Assessing an enclave that holds no CUI.** One position: the assessor validates the declared scope and assesses the controls as configured, so the certificate is honest. The other: the objectives that turn on CUI (marking media, controlling CUI flows) cannot be shown without CUI, so they are scored N/A or the scope is questioned. No Tier 1 or Tier 2 source settles it. The outcome depends on the assessor.
- **Reassessment scope after a boundary change.** Whether a new site or new CSP triggers a full reassessment or a delta limited to the change is contested. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: refuse to produce this ADR before the data flow map and the role interviews exist; a decision made from the org chart is the headcount heuristic wearing a suit. **OSC seat**: you can answer the three business-case questions from your own interviews; the one you cannot answer alone is the three-year pipeline, so take that question to the owner and the contracts lead before writing the ADR.

## Sources

- CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (asset categories, VDI carve-out, logical separation).
- 32 CFR 170.19: https://www.ecfr.gov/current/title-32/section-170.19.
- CMMC FAQ C-Q2, C-Q11, C-Q12, F-Q1 through F-Q5: https://dodcio.defense.gov/CMMC/FAQ/.
- Public post on matching scope to data: https://reddit.com/r/CMMC/comments/1t5b9t1/_/ok8mwq0/.
- Public post on answering twice with a cloud tenant: https://reddit.com/r/NISTControls/comments/kf02ft/_/gg5n41f/.
- Public interview on construction and CMMC, three-year design horizon and recertification exposure: https://www.youtube.com/watch?v=F5ufR0HtaA4.
- IntelliGRC Ep. 11, "CUI, Supply Chain Flow-Downs and the Real CMMC Challenges" (2026-05-06): https://www.youtube.com/watch?v=PG7aZWUvVvs (paraphrased, not quoted: start 800-171 at the point of receipt, from 46:53; apply it where Registry-regulated data already lives, from 1:01:19; "apply 800-171 to" rather than "treat as CUI", from 1:01:44; step 5).
- 89 FR 83092, the CMMC Program final rule, preamble at 83136 and 83170: https://www.federalregister.gov/documents/2024/10/15/2024-22905/cybersecurity-maturity-model-certification-cmmc-program (voluntary assessments, including by a provider holding no CUI, step 6).
- DFARS 252.227-7013: https://www.ecfr.gov/current/title-48/section-252.227-7013 (technical data excludes financial, administrative, cost or pricing, and management information, step 5).
- Practitioner consensus, unattributed, backs the rejection of the headcount heuristic in step 1, the three business-case questions in step 2, the shop-floor and intake-path guidance in step 5, the assessor practice in step 6.3, the nonclave warning in step 7, and the 3.10.6 limit in step 4. ADR-0006 records why the enclave is drawn around controlled customer technical data.
