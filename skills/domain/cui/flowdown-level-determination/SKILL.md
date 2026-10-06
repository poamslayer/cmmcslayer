---
name: flowdown-level-determination
description: Work out what CMMC level a subcontractor actually needs, split clause substance from the certification requirement, apply the paper-only rule, and push back on an overmarked package before it flows downstream. Use when a prime is flowing CMMC requirements down a supply chain, or when a subcontractor is asking what level applies to it.
vault_sources:
  - "CMMC for Subcontractors"
  - "CMMC Flow-Down for Hard-Copy CUI"
  - "Paper-Only CUI Environment"
  - "CUI and Supply Chain Position"
  - "CMMC Level 1"
  - "Supplier CUI Release Procedure"
  - "AEC Industry and CMMC"
  - "raw/CMMC-FAQs-v2.3-May-2026.md"
  - "Public panel on prime contractors and CMMC waivers, hosted by Summit 7: https://www.youtube.com/watch?v=haVzS8j7Qz4"
  - "Public panel where primes describe what they look for in their supplier base, hosted by Summit 7: https://www.youtube.com/watch?v=KWUuHElnPhc"
public_sources:
  - "CMMC FAQ B-Q6, C-Q2, C-Q11: https://dodcio.defense.gov/CMMC/FAQ/"
  - "81 FR 72986, the DFARS 252.204-7012 final rule, preamble at 72989 and 72997: https://www.federalregister.gov/documents/2016/10/21/2016-25315/defense-federal-acquisition-regulation-supplement-network-penetration-reporting-and-contracting-for-cloud-services-dfars"
  - "FAR 16.202-1 (firm-fixed-price contracts): https://www.ecfr.gov/current/title-48/section-16.202-1"
  - "89 FR 83092, the CMMC Program final rule, preamble at 83197: https://www.federalregister.gov/documents/2024/10/15/2024-22905/cybersecurity-maturity-model-certification-cmmc-program"
  - "32 CFR 170.5 (waivers): https://www.ecfr.gov/current/title-32/section-170.5"
  - "32 CFR 170.23 (CMMC level determination and flow-down): https://www.ecfr.gov/current/title-32/section-170.23"
  - "DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012"
  - "DFARS 252.204-7021: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7021"
  - "FAR 52.204-21: https://www.acquisition.gov/far/52.204-21"
  - "Public panel on prime contractors and CMMC waivers, hosted by Summit 7: https://www.youtube.com/watch?v=haVzS8j7Qz4"
  - "Public panel where primes describe what they look for in their supplier base, hosted by Summit 7: https://www.youtube.com/watch?v=KWUuHElnPhc"
---

# Flowdown level determination

This skill answers: what CMMC level does this specific subcontractor actually need, based on the data that actually flows to it, not on what the prime's attestation form asks it to sign? It splits the clause language a subcontract always carries from the certification obligation that only sometimes bites, applies the paper-only carve-out where it fits, and gives the subcontractor language to push back on an overmarked package. It does not make the CUI determination itself; call the Skill tool with `cui-marking-check` for marking questions and `export-control-overlay` when the data crosses into ITAR or EAR territory.

## Inputs

- The prime contract or subcontract clause list, read directly, not summarized secondhand by the prime.
- What the subcontractor actually receives: digital CUI, paper-only CUI, FCI only, or no controlled information at all.
- The subcontractor's position in the supply chain: design authority, prime, build-to-print manufacturer, commercial-off-the-shelf supplier, paper-only or read-only handler, or external service provider.
- Any attestation form, questionnaire, or "sign here" document the prime has sent.
- The subcontractor's record, the `ssp/` folder in its engagement repo, if one is already underway. Read the files directly: `ssp/components/*.md` for its components, assets, and providers, and the frontmatter of `ssp/<requirement>.md` for its statements. Never read `view/` instead; it is generated for people and can be stale.

## Method

1. **Read the clause list yourself.** Do not accept a prime's verbal or emailed summary of what applies, and do not sign an attestation that asks for blanket agreement to "everything on this list" without reading the underlying contract. The clauses that matter are FAR 52.204-21, DFARS 252.204-7012, and DFARS 252.204-7021, plus whatever the prime's own solicitation carries forward. A subcontractor that signs an attestation sight unseen has agreed to obligations it has not verified apply to its own scope.

2. **Split clause substance from the certification obligation.** These are two different questions with two different answers:

   | Question | Answer |
   |---|---|
   | Does 252.204-7012 paragraph (m) require flowing the clause's substance to every sub handling covered defense information? | Yes, always, paper or digital |
   | Does 252.204-7021 paragraph (c)(1) require flowing the clause's substance to all subcontracts? | Yes, always |
   | Does the 252.204-7021(c)(2) certification requirement bite for this specific subcontractor? | Only when CUI or FCI actually lands on that subcontractor's information system |

   A subcontractor can be correctly bound by clause substance and still owe no third-party certification, if no CUI or FCI ever reaches an information system it operates. Do not conflate "the clause is in the contract" with "I need a C3PAO assessment."

3. **Position the subcontractor by supply-chain tier**, because ownership math and obligations differ by tier:

   | Tier | Typical CUI posture |
   |---|---|
   | OEM or design authority | Owns its IP outright; asserts data rights; can afford to chase a commodity jurisdiction or classification request to pin its own status |
   | Prime | Its own generated content is not CUI to itself; the PROPIN marking belongs on what it sends up to its government customer, and applying it to work handed down to subs is a mismark |
   | Build-to-print manufacturer | Does not own the customer's design, but owns how it makes the part; the exposure is the drawing content its own paperwork re-uses (see `cui-re-use-triage`), not its tooling, programs, or process knowledge |
   | COTS supplier | Often the lightest obligation; a purchase order for catalog parts or raw material is usually not CUI unless it carries sensitive end-use context |
   | Paper-only or read-only subcontractor | Still performs on a subcontract that involves CUI and still needs Level 2 certification, but potentially a narrow scope hitting mostly a handful of families rather than all 110 requirements |
   | External service provider | Assessed for what it provides, not for whether it itself handles CUI directly; a provider can be in scope with no IT systems of its own touching CUI, because it supplies people and inherited controls |

4. **Apply the paper-only rule, and enumerate what breaks it.** Per CMMC FAQ C-Q11, an organization that only ever handles hard-copy CUI is not required to complete a CMMC third-party assessment, though it may elect to self-assess or seek third-party assessment anyway for a higher degree of assurance. The clause substance in step 2 still applies regardless. The posture collapses the moment CUI is placed on any information system, and the FAQ names the specific triggers:

   | Trigger | Effect |
   |---|---|
   | A jobsite photo of a drawing on a phone | The phone and its data path become part of the assessed system |
   | Scanning a hardcopy for a request for information | The scanning device and its destination system enter scope |
   | Uploading to a project portal | The portal and the account used to reach it enter scope |
   | Emailing a snippet to a colleague | The mailbox and its transport enter scope |
   | Printing from a source that was itself digitally scanned | The printer becomes a CUI asset, even though the output is paper |

   Once any of these happens, the receiving device or account has to meet the applicable CMMC assessment bar first, before the CUI lands on it, not as a cleanup step afterward. An organization that handles both paper and digital CUI gets assessed on the whole picture, not just the digital piece.

5. **Read the actual clause list per contract before accepting the prime's summary or the "just sign the attestation" instruction.** A prime's convenience in getting every sub to attest to everything does not change what the contract actually requires of a given subcontractor. Where a subcontractor genuinely receives no CUI and no FCI, there is no certification requirement to sign onto, and the correct response is to say so in writing, not to attest defensively.

   **When the prime demands Level 2 and no CUI will flow.** Settle "no CUI" first: call the Skill tool with `cui-determination-workflow`, whose step 10 is where a sub that cannot see the prime contract works from the evidence it has. If there really is no CUI, the level is out of step with the clause. DFARS 252.204-7021(f) requires the prime to ensure the sub holds a CMMC status "at the CMMC level that is appropriate for the information that is being flowed down to the subcontractor based on the requirements at 32 CFR 170.23", and DoD's FAQ C-Q2 says a company that does not process, store, or transmit CUI "does not need an independent assessment". Put that to the prime once, in writing, with the clause text, and keep the answer. After that letter, certifying anyway is the sub's business decision, not a compliance one. If the sub does certify, call the Skill tool with `enclave-or-enterprise-decision`: the enclave built around its controlled customer technical data is the cheapest honest scope. Whether Level 2 can be required under current DoD contracts at all depends on the program's status; call the Skill tool with `cmmc-regulatory-status-brief` rather than assuming.

6. **Push back on overmarking before accepting a flow-down package.** Primes routinely apply broad markings by default, because a standard template or an abundance of caution is cheaper for the prime than a careful review. A documented case: a prime received a roughly 1,100-page solicitation marked as containing CUI throughout; after push-back, the agency remarked it, and the corrected result was that only about one-tenth of the document was actually CUI. The technique: return the package and ask the originator to identify what is actually CUI, rather than accepting the burden of sorting it out downstream. A subcontractor that accepts an overmarked package at face value ends up scoping and certifying against data it may never actually touch.

7. **Ask the prime to sanitize or descope before flow-down, as a first move, not a last resort.** Where a work package mixes CUI content with content that does not need protection, ask the prime to split them so the subcontractor scope only covers what is genuinely controlled. A construction-sector example: a prime separated CUI building plans from non-controlled commercial products in the same package, so the subs handling only the non-controlled portion needed nothing beyond basic hygiene.

8. **State the hard rules on waivers, because they are not negotiable.** Neither a contracting officer nor a prime contractor may waive or deviate from CMMC's cybersecurity requirements (32 CFR 170.5). Where a waiver exists at all, it applies to an entire contract, decided before the solicitation is issued, through an approval chain running from the program office through component leadership to the DoD CIO; it is never granted to an individual subcontractor after the fact. Once CMMC language is already in a solicitation, that door is closed. Even where a waiver removes the certification requirement, the underlying obligation to implement NIST SP 800-171 under the clauses in step 1 still stands; a waiver only removes the outside verification, not the requirement itself.

9. **Price it in at proposal time, and fund it through rates, never as a line item.** DoD's position for 7012 is that "the cost related to compliance should be considered during proposal preparation" and that "the cost of compliance is allowable and should be accounted for in proposal pricing" (81 FR 72989, 72997). Pricing it in later is harder: a firm-fixed-price contract "is not subject to any adjustment on the basis of the contractor's cost experience" (FAR 16.202-1), so a sub that bids first and builds the enclave afterwards carries the cost on that contract. The cost passes through hourly rates, material markup, or overhead allocation. There is no separate CMMC compliance billing category, and a subcontractor should not expect to invoice a prime directly for it. DoD has not said how CMMC assessment costs are treated beyond the general FAR 31.201-2 allowability tests (89 FR 83197), so do not promise a client that they are recovered.

## Output

A determination for one supplier, written to `docs/adr/NNNN-flowdown-<supplier-short-name>.md`:

```markdown
# Flowdown level determination: <supplier name>

Date: YYYY-MM-DD. Prime contract or subcontract reviewed: ...

## Tier and posture
Supply-chain tier: OEM/design authority | prime | build-to-print | COTS | paper-only/read-only | ESP.
What actually flows to this supplier: CUI (digital) | CUI (paper-only) | FCI only | nothing controlled.

## Clause basis
FAR 52.204-21 applies: yes/no. DFARS 252.204-7012(m) substance flows: yes/no.
DFARS 252.204-7021(c)(1) substance flows: yes/no. 7021(c)(2) certification bites: yes/no, basis: ...

## Paper-only check (if applicable)
Digitization triggers reviewed: jobsite photo / scan / portal upload / email / print-from-scan.
Written no-digitization commitment in place: yes/no.

## Overmarking check
Package reviewed for overmarking: yes/no. Push-back sent: yes/no. Result: ...

## Level required
Level: 1 | 2, narrow scope | 2, full scope | none.

## Recommended path
digital CUI path | paper-only path | no-CUI package (descoped) | not yet determined, pending prime response.

## Waiver status
Waiver claimed: yes/no. If yes, verified against 32 CFR 170.5 chain of approval: yes/no.
```

Attach this determination to `scope/external-systems.md` for the subcontractor's own engagement repo, or, if the subcontractor is being tracked as an ESP, as a line on `scope/open-items.md` for `esp-and-msp-scoping` to carry into that provider's remarks through scribe. Never edit the responsibility matrix under `view/`; it is generated from the record.

## Where practitioners disagree

- **Whether "paper-only" is a realistic operating posture or a scoping fiction that rarely survives contact with a real jobsite.** One position: it is a legitimate, deliberate strategy for keeping small finishing houses and single-purpose suppliers out of scope entirely, and the FAQ backs it. The other: an organization that cannot demonstrate, operationally, that digitization never happens, with policy, training, and enforcement, will not survive an assessor's scrutiny of the claim, no matter what the FAQ permits in principle. The outcome depends on the assessor.
- **Whether operating inside a prime's own enclave, using prime-owned equipment, substitutes for the subcontractor's own certification.** One position: it is a workable interim arrangement for a small specialist doing narrow, contained work. The other: the contractual and scope boundaries of this arrangement are unresolved even among primes who use it, and it is not treated as a long-term substitute for the sub's own compliance posture. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run steps 6 and 7 before you scope anything; a client that accepts an overmarked package without pushing back will pay for compliance work against data it may never actually handle. Draft the push-back and sanitize-or-descope requests as templates the client can send without waiting on you each time. **OSC seat**: before spending money, get two things from your prime in writing: the deadline they need your certification by, and the specific data that will actually flow to you. A prime that has gone quiet on CMMC entirely is a signal worth acting on, not a reason to assume you are exempt.

## Sources

- CMMC FAQ B-Q6, C-Q2, C-Q11: https://dodcio.defense.gov/CMMC/FAQ/.
- 81 FR 72986, the DFARS 252.204-7012 final rule, preamble at 72989 and 72997: https://www.federalregister.gov/documents/2016/10/21/2016-25315/defense-federal-acquisition-regulation-supplement-network-penetration-reporting-and-contracting-for-cloud-services-dfars (compliance cost belongs in proposal pricing, step 9).
- FAR 16.202-1: https://www.ecfr.gov/current/title-48/section-16.202-1 (a firm-fixed-price contract is not repriced for cost experience, step 9).
- 89 FR 83092, the CMMC Program final rule, preamble at 83197: https://www.federalregister.gov/documents/2024/10/15/2024-22905/cybersecurity-maturity-model-certification-cmmc-program (the rule makes no change to cost allowability, step 9).
- 32 CFR 170.5: https://www.ecfr.gov/current/title-32/section-170.5.
- 32 CFR 170.23: https://www.ecfr.gov/current/title-32/section-170.23.
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012.
- DFARS 252.204-7021: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7021.
- FAR 52.204-21: https://www.acquisition.gov/far/52.204-21.
- Public panel on prime contractors and CMMC waivers, hosted by Summit 7: https://www.youtube.com/watch?v=haVzS8j7Qz4.
- Public panel where primes describe what they look for in their supplier base, hosted by Summit 7: https://www.youtube.com/watch?v=KWUuHElnPhc.
- Practitioner consensus, unattributed, backs the tier-by-tier posture table in step 3, the push-back technique in step 6, the sanitize-or-descope recommendation in step 7, the rates-not-line-item funding rule in step 9, the advice to raise the 7021(f) mismatch once in writing in step 5, and both rows in the disagreement section.
