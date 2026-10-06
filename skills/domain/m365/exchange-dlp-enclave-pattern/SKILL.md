---
name: exchange-dlp-enclave-pattern
description: Decide the scoping outcome for an organization that sends CUI by email inside a GCC High (or equivalent) Microsoft 365 tenant and wants to keep most mailbox users out of assessment scope. Compares the three Exchange Online architectures, grounds the Out-of-Scope claim in the Scoping Guide's logical separation test, lists exactly what stays in scope, and lists the evidence an assessor will ask for. Use when a client licenses Exchange Online in a CUI-capable tenant and asks whether every licensed user becomes in scope.
vault_sources:
  - "Exchange Online CUI Enclave Pattern"
  - "CMMC Scoping"
  - "DLP for CUI Scope Control"
  - "VDI Scoping"
  - "How to Identify CUI"
  - "3.13.8"
  - "raw/CMMC Scoping Guide Level 2 v2.13.md"
  - "raw/Summit 7 - Identify Assets for CMMC (kvw5uhLK2U8) - Transcript.md (Summit 7, https://www.youtube.com/watch?v=kvw5uhLK2U8)"
public_sources:
  - "CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.19 (CMMC Assessment Scope, asset categories): https://www.ecfr.gov/current/title-32/section-170.19"
  - "Identify Assets for CMMC, Summit 7: https://www.youtube.com/watch?v=kvw5uhLK2U8"
---

# Exchange DLP enclave pattern

This skill answers one scoping question: an organization licenses Exchange Online in a GCC High tenant to send CUI by email, and wants the rest of its licensed users left out of the CMMC Level 2 assessment. It decides which of three Exchange Online architectures the organization actually runs, and what each produces for scoping. It does not configure the Purview rule, draw the network diagram, or decide whether a given message is CUI (call the Skill tool with `cui-determination-workflow` for that; an unmarked message defeats every architecture below equally). It also does not run the general logical-separation test for a non-email asset (call the Skill tool with `logical-separation-test` for a VLAN, ACL, or non-mail DLP claim).

## Inputs

- Confirmation of the tenant type (GCC High), from `gcc-high-decision` if not already recorded in `CONTEXT.md`.
- The current Exchange Online configuration: whether a mail-flow (transport) rule exists, what it matches on, and its action.
- The shared mailbox permission list, if one exists, pulled from the Exchange admin center rather than taken on the client's word.
- `scope/data-flow.md` from `cui-data-flow-mapping`, confirming email as an actual CUI entry or exit point, not an assumed one.
- Whether marking practice is reliable enough for a mail-flow rule to match on it (see `How to Identify CUI`); a rule matching on markings nobody applies cannot do this pattern's job.

## Method

1. **Sort the tenant into exactly one of three architectures, and read off the scoping result.** Do not let the client self-report which one they are running; check the mail-flow rule list and the mailbox permissions directly.

   | Architecture | What is actually configured | Scoping result for the regular user population |
   |---|---|---|
   | Default Exchange Online, no DLP controls | Every licensed mailbox can receive CUI; nothing stops it | **Contractor Risk Managed Asset (CRMA)**. Every mailbox is capable of receiving CUI even though it is not intended to. Documented in the asset inventory, the SSP, and the network diagram; the assessor may run a limited check if the documentation is weak. |
   | Automatic re-routing DLP rule, a single shared mailbox, no mailbox access for regular users | A Purview mail-flow rule intercepts and redirects CUI-marked mail to one shared mailbox before it reaches any other inbox; regular users have no permission on that shared mailbox | **Out-of-Scope** for the regular user population. Their mailboxes cannot receive CUI, and they have no path to the mailbox that does. |
   | No Exchange Online license at all in the CUI-handling tenant | The user has no account in the tenant that holds CUI | **Out-of-Scope**, trivially. There is no reachability question to argue; the user cannot reach the tenant. |

   The middle row is the pattern this skill exists to evaluate. The first row is the default outcome most organizations get by doing nothing. The third row needs no further analysis; skip to a different licensing question if that is the client's actual setup.

2. **Test the middle row against the Scoping Guide's own definition of logical separation, not against a looser standard.** The Scoping Guide sets the bar for an Out-of-Scope Asset at "cannot process, store, or transmit CUI," and it defines logical separation as data transfer being prevented "by non-physical means such as software or network assets," for example a firewall, a router, or a VLAN. A mail-flow rule that redirects the message before it is delivered, so the message is never placed in the regular user's mailbox even momentarily, is exactly that kind of non-physical, software-enforced block. It is a technical boundary the same way a firewall rule is, not a written policy asking users not to open something they could otherwise reach.

3. **Confirm the redirect happens before delivery; that is what separates this pattern from a DLP policy the Scoping Guide will not credit.** A rule that delivers the message and then moves it out again does not qualify: for that interval the mailbox stored CUI, making it a CUI Asset regardless of what happens next. Message trace logs must show the redirect firing ahead of delivery, not a deliver-then-move sequence.

4. **Apply the Virtual Desktop Infrastructure carve-out as the closest existing precedent.** The Scoping Guide already accepts one case where a device that can technically reach CUI is still Out-of-Scope: an endpoint running a VDI client configured to pass nothing beyond keyboard, video, and mouse signal to the CUI session. The mail-flow rule does the same job for a mailbox, keeping CUI from ever landing where the regular user can reach it. The VDI carve-out's known failure mode applies here too: a regular user later granted any access to the shared mailbox pulls their own mailbox and device straight back into scope.

5. **Enumerate what stays in scope under the middle-row architecture. Nothing on this list is optional or judgment-dependent; each item is a CUI Asset or a Security Protection Asset by the ordinary application of the category test.**

   | Item | Category | Why |
   |---|---|---|
   | The shared mailbox itself | CUI Asset | Stores and processes CUI by design |
   | Every user actually authorized to access the shared mailbox | CUI Asset (the user's account and access) | The point of the mailbox is that these users process the CUI in it |
   | Laptops and phones that authorized staff use to read the shared mailbox | CUI Asset | Opening the mailbox on the device means the device is processing CUI at that moment |
   | The Purview DLP rule, Microsoft Information Protection labeling, and conditional access policies that enforce the boundary | Security Protection Asset | These are the services that make the separation real; they are assessed against the Level 2 requirements their capability touches, not against all 110 |

   Regular users, their mailboxes, and their devices are Out-of-Scope, with the one obligation the Scoping Guide places on any Out-of-Scope designation: be ready to justify the inability to process, store, or transmit CUI if an assessor asks.

6. **Note the separate transmission-encryption question; do not conflate it with scoping.** Whichever architecture is chosen, mail carrying CUI must still meet 3.13.8's requirement to protect confidentiality in transit. GCC High enforces TLS 1.2 with FIPS-validated cryptography by default, normally sufficient on its own; call the Skill tool with `fips-crypto-scoping` if the tenant mixes in a non-GCC High partner domain or an unmanaged connector. This controls the CUI Assets from step 5; it does not substitute for the logical-separation argument in steps 2 through 4.

7. **Build the checklist of what the organization must be able to defend, and confirm each item exists before the client relies on this pattern.** An assessor can ask to see any of these; a gap in one weakens the Out-of-Scope claim for the whole regular user population.

   - The mail-flow rule's conditions and action, kept under version control so a change is tracked and reviewable rather than silently made.
   - Periodic test sends of marked CUI, with the test reports retained, proving the rule still fires correctly on a current basis rather than only at initial configuration.
   - Message trace logs that show the redirect happening before delivery, not a deliver-then-move pattern, for a representative sample of matched messages.
   - A current, verifiable listing of who holds permissions on the shared mailbox, pulled from the Exchange admin center rather than from memory.
   - The SSP's written justification for why the regular user population's mailboxes cannot process, store, or transmit CUI.
   - A network or data-flow diagram that draws the mail-flow rule itself as the scope boundary, not merely as a note in the SSP text.

8. **Name the failure modes and check each one against the client's actual operating discipline, not against the design on paper.**

   - **False negatives in the DLP rule.** CUI that was never marked, or marked in a format the rule does not recognize, is not caught and lands in a regular mailbox, making that mailbox a CUI Asset for real. This traces back to marking discipline (`How to Identify CUI`'s domain, not this skill's); unmarked CUI from a staffer or an external partner defeats the boundary no matter how well the rule is built.
   - **Assessor skepticism toward a same-tenant claim.** The shared mailbox and the unauthorized users sit in the same tenant, and some assessors weigh that heavily even where the technical block is sound; expect this pattern to draw interview time a fully separate tenant would not.
   - **Operational drift.** A new mail-flow rule added for an unrelated reason, a permission grant made to solve a short-term problem, or a rule disabled temporarily for troubleshooting and never re-enabled can each silently break the boundary between verification cycles.
   - **The Level 3 implication.** This pattern is evaluated here at Level 2; at Level 3 the separation standard tightens and the same architecture may not carry over. An organization on a Level 3 path should not treat this as a permanent design.

## Output

Write the architecture decision, the in-scope list, and the evidence list to `scope/exchange-dlp-enclave.md`:

```markdown
# Exchange DLP enclave decision: <client>

## Architecture chosen

<one of: default Exchange Online with no DLP (CRMA); auto-rerouting DLP + shared mailbox + no regular-user access (Out-of-Scope); no license in the CUI tenant (Out-of-Scope, trivial)>

Confirmed against: <mail-flow rule name(s), shared mailbox name, permission list pulled on <date>>

## In-scope items

| Item | Category | Notes |
|---|---|---|
| | | |

## Out-of-scope justification

<the SSP-facing sentence stating why the regular user population's mailboxes cannot process, store, or transmit CUI>

## Evidence on file

- [ ] Mail-flow rule conditions and action, under version control
- [ ] Test send reports, dated <date of most recent test>
- [ ] Message trace logs showing redirect-before-delivery
- [ ] Shared mailbox permission listing, pulled <date>
- [ ] SSP justification language, drafted
- [ ] Network/data-flow diagram showing the DLP rule as the scope boundary

## Failure modes reviewed

- [ ] DLP false negatives on unmarked CUI
- [ ] Marking discipline checked against `How to Identify CUI`
- [ ] Assessor same-tenant skepticism, noted as an interview risk
- [ ] Operational drift, re-verification cadence set
- [ ] Level 3 implication, flagged if the client has a Level 3 path
```

This feeds the asset inventory; hand the in-scope table to `cmmc-scope-boundary`, which records the categories in the SSP through `scribe`, rather than re-deriving them there.

## Where practitioners disagree

- Whether a strong DLP rule alone, without the redirect-before-delivery and no-access conditions in the middle-row architecture, can ever meet the "cannot" bar on its own. One reading treats DLP as always just a policy control that produces a CRMA at best. Another reading holds that a DLP rule combined with other technical controls can meet "cannot" if it is strong enough. The outcome depends on the assessor.
- Whether same-tenant separation is inherently weaker than a fully separate tenant in an assessor's eyes, even when the technical boundary is identical on paper. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: build the evidence list in step 7 into the engagement's recurring verification cadence, not a one-time setup task; operational drift is the failure mode most likely to surface between the SSP being written and the assessment happening. **OSC seat**: if a Level 3 path is even plausible in the next few years, ask whether this pattern is worth building at all, since Level 3's tighter separation standard may force a redesign anyway.

## Sources

- CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (asset category definitions, logical separation, the VDI carve-out).
- 32 CFR 170.19, CMMC Assessment Scope: https://www.ecfr.gov/current/title-32/section-170.19
- Identify Assets for CMMC, Summit 7: https://www.youtube.com/watch?v=kvw5uhLK2U8 (the Security Protection Asset framing applied to the Purview/MIP/conditional-access services in step 5).
- Practitioner consensus, unattributed, backs treating a Purview mail-flow rule that redirects before delivery as a technical boundary rather than a policy control, the specific evidence items in step 7, the false-negative and operational-drift failure modes in step 8, and the Level 3 caution.
