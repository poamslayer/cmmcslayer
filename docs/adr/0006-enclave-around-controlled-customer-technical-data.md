# ADR-0006: Build the enclave around controlled customer technical data, and apply 800-171 without calling it CUI

Date: 2026-09-26. Status: accepted. Issue #67, map #74. Builds on ADR-0005.

## Context

A subcontractor usually cannot see the prime contract above it, so it cannot run the ownership and contract-origin tests in `cui-determination-workflow` on its own. Primes often flow CMMC Level 2 down anyway, sometimes when nothing they send is marked CUI. That leaves the sub with two problems. It has to decide what the drawings it received are. And if it builds a Level 2 environment, it needs something real to build it around.

Before this decision the skills drew the enclave around CUI flows only. A shop that had received export-controlled drawings but no marked CUI had two options, and both were bad. It could build an empty enclave, or it could call the drawings CUI so the enclave had something in it. The second option is the "everything is CUI" default that ADR-0005 removed.

## Decision

1. **A Level 2 flowdown is a clue, not a label.** The sub lists what it received, decides a status for each item on the evidence, and notifies the prime in writing (the reverse guidance in `cui-determination-workflow`). It notifies rather than asks: an open question to a prime usually gets no answer or "treat it all as CUI", and 32 CFR 2002.50(a)'s own verb is notify. Under DFARS 252.204-7012(m)(1), deciding whether information sent to a sub is covered defense information is the prime's job, and the notice is how the prime gets the chance to correct the sub's call. An item with a real reason for doubt is recorded as "potentially CUI, notice sent" and protected meanwhile, as ADR-0005 (amended) sets out. Nothing is CUI by default.
2. **The enclave is built around controlled customer technical data.** This applies to any company that receives customer technical data carrying a CUI marking, an export-control warning, or a DoD Distribution Statement B to F. The recommended design puts all of it in one enclave. The boundary statement is "we apply NIST SP 800-171 to controlled customer technical data".
3. **Applying 800-171 is not a CUI determination.** Each item keeps its own data categories (ADR-0005, #59). The SSP and `scope/data-flow.md` list CUI, Export-controlled, and Proprietary items separately. "Treat as CUI" is retired as a phrase, because it gets read as "it is CUI".
4. **The boundary is a kind of data, not a legal label.** Business records stay outside the enclave, because DFARS 252.227-7013 excludes "financial, administrative, cost or pricing, or management information" from technical data. The enclave is built to the union of the regimes that reach its data, so ITAR data usually means GCC High. Shop-floor machines are Specialized Assets.
5. **When no CUI flows, the rules point to Level 1, and a voluntary Level 2 is still possible.** First, confirm "no CUI" through `cui-determination-workflow`. An unmarked export-controlled drawing received under a 7012 subcontract can still be CUI. If there really is none, the sub raises DFARS 252.204-7021(f) with the prime once, in writing. That paragraph asks for a level "appropriate for the information that is being flowed down", and DoD's FAQ C-A2 says a company without CUI needs no independent assessment. If the sub certifies anyway, the assessment runs against the scope it declares (32 CFR 170.19(a)(1)). The CMMC rule's preamble expects voluntary assessments, including by an ESP that holds no CUI (89 FR 83136, 83170).

## Considered options

- **Level 2 means treat everything received as CUI.** Rejected. It hands the determination to the prime's template and restores what ADR-0005 removed.
- **Enclave around marked CUI only.** Rejected. A shop without marked CUI gets an empty enclave, and its export-controlled drawings still need protecting somewhere else.
- **The new pattern only for subs that have no CUI.** Rejected. A single rule means nobody has to sort CUI from ITAR at the inbox, and CUI that arrives later is already where it belongs.
- **Include customer proprietary technical data by default.** Rejected. The Proprietary data categories add no assets to scope (#59). A client can choose to include it.
- **Put False Claims Act exposure and pricing market claims in the skills.** Both were researched and both rejected. FCA content reads as legal advice. The pricing claims ("subs are price-takers", "absorb it in overhead") have no Tier 1 or Tier 2 source. DoD has declined to address CMMC cost recovery (89 FR 83197). Only the sourced point is kept: compliance cost belongs in proposal pricing (81 FR 72989, 72997), and a firm-fixed-price contract is not repriced for cost experience (FAR 16.202-1).

## Consequences

- An enclave can hold no CUI and still be real. The environment it describes is honest, and the SSP records its data by category.
- Export-controlled data often drives the design to GCC High sooner than CUI alone would. That cost is deliberate: the data needs it whatever its CUI status.
- No Tier 1 or Tier 2 source says how a C3PAO scores objectives that need CUI to be present, when an enclave holds none. The skill says this is unsettled and tells the operator to agree the scope in writing with the assessor. Practitioner experience is that assessors assess the declared boundary, and organizations holding no CUI have been certified.
- Whether Level 2 is currently required depends on the program's status, including the July 2026 Phase II suspension. The skills point to `cmmc-regulatory-status-brief` rather than restating a date that will go stale.
