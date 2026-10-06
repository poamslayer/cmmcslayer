---
name: c3pao-selection-vetting
description: Vet a C3PAO, Registered Practitioner Organization, or consultant before signing, on past performance and technical literacy rather than the marketplace badge alone, and build the pre-engagement question list from the requirements assessors read differently. Use before selecting a certification assessor or a consultant, or before deciding to switch one mid-engagement.
vault_sources:
  - "Trusting RPs and RPOs"
  - "3.1.12"
  - "3.1.18"
  - "3.1.19"
  - "3.3.6"
  - "3.3.7"
  - "3.13.8"
  - "Printer Scoping"
  - "CMMC Significant Change Determination"
  - "raw/public-talk-transcript-mIVnOkQnZg0.md"
  - "raw/public-talk-transcript-EY91HbErRIE.md"
public_sources:
  - "CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.12, AC.L2-3.1.18, AC.L2-3.1.19, AU.L2-3.3.6, AU.L2-3.3.7, SC.L2-3.13.8: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "CMMC Assessment Process FAQ, C-Q12: https://dodcio.defense.gov/CMMC/FAQ/"
  - "Public recap of a Cyber AB town hall discussing the Registered Practitioner program: https://www.youtube.com/watch?v=mIVnOkQnZg0"
---

# C3PAO selection vetting

This skill answers: is this assessor, or this consultant, actually qualified, and what should I ask them before signing? A marketplace listing tells you someone paid a fee and took a training course; on its own it says nothing about whether the firm has actually walked a client through certification, or reads a contested requirement the same way your eventual assessor will. This skill does not draw scope or write SSP language; it only produces the vetting judgment and the question list. It does not name any specific firm, because the point is a repeatable method, not a recommendation.

## Inputs

- The candidate firm's name, credential type (C3PAO, Registered Practitioner Organization, or unregistered consultant), and how the engagement found them.
- The scoping decisions in the record, the engagement's `ssp/` folder: the components, the assets with their categories, and the providers, so the pre-engagement questions can be asked about this environment specifically. Read them from `ssp/components/*.md`, one file per component with its assets and, for a provider, its role and FedRAMP status. Never read `view/` instead; it is generated for people and can be stale.
- Whether a provider swap is being considered alongside this selection; if an existing MSP or MSSP would be replaced, that swap has its own significant-change question, separate from this one.

## Method

1. **Treat the badge as hygiene, not qualification.** Being listed as a Registered Practitioner (RP) or a Registered Practitioner Organization (RPO) in the Cyber AB marketplace confirms only that a fee was paid and a short training course was completed. Neither status confirms the firm has walked a client through an actual Level 2 certification assessment, and neither confirms that the advice they give along the way is correct. The Cyber AB itself has publicly acknowledged the Registered Practitioner program needs an overhaul, citing the training's depth, its length, and unclear role definition between what a practitioner does and does not do. Code-of-conduct enforcement on registered firms is described as thin in practice, and an unregistered consultant is not bound by any code of conduct at all.

2. **Vet on past performance, not the pitch.** Ask directly: how many clients has this firm taken through an actual Level 2 C3PAO certification assessment, what were the outcomes, and can they give names and dates you can verify. A firm that has only done Level 1 self-assessments, or has only prepared clients without ever sitting through a certification assessment with them, is a materially different service than one that has been through the process and knows where it actually goes wrong. Do not accept "we do CMMC work" as an answer to this question.

3. **Check trained-and-tested against merely registered.** A Certified CMMC Professional (CCP) and a Certified CMMC Assessor (CCA) both require passing a proctored exam. An RP does not. A firm whose only credentialed staff hold the RP designation is a different proposition than one with a CCP or CCA on staff, and the difference is worth asking about directly rather than assuming from the marketplace badge.

4. **Ask about forward technical literacy.** A firm that cannot speak to the coming NIST SP 800-171 Rev 3 uplift, or to what Level 3 will require, is not tracking the standard closely enough to be a long-term partner. This matters because your certification is not a one-time event; you will need this relationship, or one like it, again.

5. **Treat certain answers as a walk-away signal.** A candidate who tells you "you did Level 1 in Microsoft commercial, so you're ready for Level 2" does not understand that Level 2 CUI storage requires FedRAMP Moderate authorization or an equivalent, a materially different bar than Level 1. That answer alone is disqualifying.

6. **Reject manufactured deadlines.** A candidate pushing a hard compliance deadline tied to a specific month is very likely misreading the CMMC rollout. The phased rollout determines when C3PAO certification assessments become the norm in DoD solicitations; it is not itself a fixed compliance date every contractor must hit. Pressure sold as an externally imposed deadline is a sales tactic, not a regulatory fact, and it is worth asking the candidate to point to the specific clause creating any deadline they cite.

7. **Build the pre-engagement question list from the requirements where assessors genuinely differ.** The value of asking these before signing is that the candidate's answer tells you how they will read your environment, and you can compare that against what you already believe about your own scope. Use the table in Output below and get the answers in writing.

8. **Weigh the switching cost before treating a change as easy.** Replacing an assessor mid-process has scheduling and cost consequences. Replacing an MSP or MSSP is a different and larger question: it is very likely itself a significant change to a certified environment, requiring the change-control and reassessment analysis that any other architectural change would trigger. Call the Skill tool with `significant-change-determination` before treating a provider swap as a simple vendor switch.

## Output

Write one record per candidate to `scope/vetting/<candidate-name>.md`. When a candidate is chosen, record the decision and the reasoning as an ADR in `docs/adr/`, because who assessed you and why is a question that gets asked again three years later.

```markdown
# C3PAO / consultant vetting record

## Past performance
- Level 2 certification assessments completed with clients: [names, dates, outcomes]
- Credentials on staff: [RP / CCP / CCA, per person]
- Forward literacy: [Rev 3 uplift and Level 3 readiness, in their own words]
- Cloud literacy check: [pass/fail on the FedRAMP Moderate distinction]
- Deadline claims made: [quote, and whether it traces to an actual clause]

## Pre-engagement question list

| Requirement | Contested question | Candidate's position |
|---|---|---|
| 3.1.12 | Does a VPN connection from a company device count as remote access once the tunnel is established, or only during the handshake? | |
| 3.5.3 | Does Windows Hello for Business with a TPM and PIN count as multifactor authentication for local sign-in? | |
| 3.1.18 | Is a laptop a mobile device under this candidate's reading, or a mobile computing platform with different requirements? | |
| 3.1.19 | Can email be descoped from the CUI environment, and what evidence would they require to accept that? | |
| 3.3.6 | Does a commercial, non-GCC SIEM qualify as a Security Protection Asset, and what CUI-exclusion evidence would they want? | |
| n/a | How do they categorize printers and multifunction devices: Contractor Risk Managed Asset, Specialized Asset, or out of scope? | |
| 3.13.8 | Do they accept common-carrier MPLS as meeting the transmission-protection requirement without added encryption? | |
| n/a | What evidence would satisfy them for a paper-only CUI handling claim? | |

## Decision
Selected: yes/no. Rationale: ...
```

File at `docs/adr/NNNN-c3pao-selection-<short-name>.md` if the decision is being formalized, or `scope/vetting/<candidate-name>.md` for a working record.

## Where practitioners disagree

- **Whether an established VPN session counts as remote access.** One position: the handshake into the tunnel is remote, but traffic inside an established tunnel is not, because it is now part of the internal system. Another, more recent position: the connection is still remote access under the plain reading of the objective, and belongs in the identification of permitted remote access types regardless of how the tunnel is treated operationally. No consensus exists; the outcome depends on the assessor.
- **Whether Windows Hello for Business with a TPM and PIN is defensible as multifactor authentication.** The technical argument for it rests on treating the TPM as a "something you have" factor recognized by federal authentication guidance. The argument against it is that many assessors will not visibly see two distinct factors during an interview and may reject it on that basis alone, regardless of the technical merit. The outcome depends on the assessor.
- **Whether a laptop is a mobile device.** Strong practitioner consensus holds it is not, under the federal definition distinguishing a mobile device from a mobile computing platform, but that consensus is not universal outside the practitioner community, and at least one documented mock assessment finding treated a laptop as a mobile device anyway. The outcome depends on the assessor.
- **Whether email can be descoped from the CUI environment.** One position: yes, with policy, training, and evidence that no CUI reaches the mail system another way. Another: any device that could see CUI, even accidentally, risks being pulled back into scope, which would functionally put the whole internet in scope if taken to its extreme. The outcome depends on the assessor.
- **Whether a commercial SIEM handling logs from CUI-adjacent systems counts as CUI in the log data.** One position: logs are metadata, not CUI content, so a properly configured commercial tool is fine as a Security Protection Asset. A stricter reading treats anything connected to a CUI asset as carrying CUI risk by association. The outcome depends on the assessor.
- **Printer and multifunction device category.** Three positions circulate: a Contractor Risk Managed Asset, because the data path to the device is open even across VLANs; a Specialized Asset treated like operational technology, because the device converts a digital file into a physical one; or out of scope, if firewall and access-control rules can prove the device truly cannot process, store, or transmit CUI. The outcome depends on the assessor.
- **Whether common-carrier MPLS satisfies the transmission-protection requirement without added encryption.** The Assessment Guide's own example allows unencrypted transmission over standard, carrier-provided MPLS, but practitioners report inconsistent acceptance of this exception in practice, and software-defined networking does not qualify as true MPLS under any reading. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run this vetting on your own subcontracted assessors and partners too, not only on the client's behalf; your reputation travels with whoever you refer. **OSC seat**: get every answer in the pre-engagement table in writing before signing an engagement letter, since these are exactly the positions that turn into a dispute mid-assessment if they surface for the first time during an interview.

## Sources

- CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.12, AC.L2-3.1.18, AC.L2-3.1.19, AU.L2-3.3.6, AU.L2-3.3.7, SC.L2-3.13.8: https://dodcio.defense.gov/CMMC/Resources-Documentation/.
- CMMC Assessment Process FAQ, C-Q12: https://dodcio.defense.gov/CMMC/FAQ/ (significant change determination and the Affirming Official's authority).
- Public recap of a Cyber AB town hall discussing the Registered Practitioner program overhaul: https://www.youtube.com/watch?v=mIVnOkQnZg0.
- Practitioner consensus, unattributed, backs the past-performance vetting steps, the trained-versus-registered distinction, the cloud-literacy walk-away signal, the fake-deadline rejection, and every position recorded in the disagreement section above.
