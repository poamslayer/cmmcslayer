---
name: logical-separation-test
description: Test whether a claimed network segment, print path, or asset separation actually removes an asset from CUI reach, or whether it only reduces the odds of use. Returns a verdict of not separated, isolation, or controlled access, with every allow-list entry judged on what it could carry. Use whenever an OSC claims a VLAN, ACL, firewall rule, or DLP policy takes an asset out of scope.
vault_sources:
  - "Logical Separation"
  - "DLP for CUI Scope Control"
  - "Network Segmentation for Scope Reduction"
  - "3.1.20"
  - "Printer Scoping"
  - "raw/practitioner-community-export-2026-08-08.md"
  - "raw/unified-scoping-guide.pdf"
public_sources:
  - "CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.19 (Out-of-Scope Asset definition): https://www.ecfr.gov/current/title-32/section-170.19"
  - "CMMC FAQs, F-Q3 (encryption alone is not logical separation): https://dodcio.defense.gov/CMMC/FAQ/"
  - "CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.20: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "Unified Scoping Guide, ComplianceForge, CC BY 4.0: https://complianceforge.com/"
---

# Logical separation test

This skill tests one claim at a time: "this asset is out of scope because of a VLAN, an ACL, a firewall rule, or a DLP policy." It returns a verdict, not a design. It does not draw the network diagram and it does not decide the asset's final category on its own (feed the verdict into `cmmc-scope-boundary`), and it does not evaluate a specific requirement's evidence (`control-evidence-lookup` does that).

## Inputs

- The claimed separation: what device or rule sits between the CUI Asset and the asset under test, and what it is configured to do.
- The full list of what is permitted to cross the boundary in either direction, at the protocol or service level, not just the vendor name of the device enforcing it.
- Whether any compensating control (DLP, monitoring, policy) is being offered in place of, or alongside, a technical block.
- The engagement repo's `scope/network-diagram.drawio`, `scope/network-diagram.md`, and `scope/data-flow.md`, so the claim can be checked against what is actually drawn.

## Method

1. **Run the three-tier test.** Sort the configuration into exactly one tier:

   | Configuration | Verdict |
   |---|---|
   | VLANs exist and traffic routes between them with no access control list | Not separated |
   | An access control list blocks all communication between the segments | Isolation |
   | A firewall enforces an allow-list with everything else denied by default | Isolation |

   A VLAN on its own only defines which devices share a broadcast domain; nothing about that stops packets from passing between segments. If two VLANs can route to each other with no filtering rule in the way, nothing has actually been separated, no matter what label the diagram gives the segments.

2. **Translate the verdict into the Unified Scoping Guide's two precise terms.** Isolation means no logical access is permitted at all between the asset and the CUI environment; the traffic simply cannot get there. Controlled access means logical access is permitted but restricted to a defined set of ports, protocols, services, and directions. Isolation is what a true Out-of-Scope claim needs; controlled access is what keeps an asset a Contractor Risk Managed Asset (CRMA) rather than removing it from scope. Total blockage is not required for isolation to hold, but whatever is allowed through must be tightly and verifiably limited to flows that structurally cannot carry CUI.

3. **Judge each permitted entry by what it could carry, not by why it was added.** The right question is never "why was this rule written" but "is this traffic type physically able to carry a document." DNS on UDP/53 to a gateway and NTP to a time server cannot carry a file payload and pass. Print jobs, file shares, backup streams, and license check-ins that exchange more than a status ping cannot be waved through on intent alone; if the protocol is structurally capable of carrying a document, treat the far side as reachable, and the far side becomes a CRMA rather than an isolated or out-of-scope asset.

4. **Rule that DLP is a control, not separation.** Data loss prevention that blocks CUI from reaching a print server, a file share, or any other structurally reachable asset does not remove the reachability; it only expresses an intent not to use it, backed by a filter that can misfire on untagged content. An asset that is reachable and protected only by DLP is a CRMA: capable of reaching CUI, not intended to, and documented accordingly. Some practitioners argue a strong DLP implementation, layered with VLAN rules and written procedure, should be able to satisfy the "cannot" bar for Out-of-Scope. The stronger and more common practitioner position is that DLP alone never converts a reachable path into a technical inability, because DLP failure modes (untagged content, misconfigured rules) leave the path open. Record which position the client's assessor holds; the outcome depends on the assessor.

5. **Note that encryption is not a substitute for either test.** A claim that traffic is encrypted end to end, with no ACL or firewall behind it, does not establish logical separation. Encryption protects confidentiality in transit; it does nothing to prevent the transfer itself, which is what the separation tests above are checking for.

6. **Read 3.1.20 as the one place with more latitude than the Scoping Guide.** The Out-of-Scope Asset definition in the Scoping Guide turns on the word "cannot," a technical-impossibility bar. The 3.1.20 objectives ask instead whether external system connections are identified, whether their approved use is documented, and whether they are verified, controlled, and limited: a documentable posture, not an absolute. For a connection the organization controls end to end but cannot prove is technically incapable of carrying CUI, documenting it fully under 3.1.20 (with its category, its FedRAMP status where relevant, and firewall rules enforcing the limitation) is a more defensible move than forcing a Scoping Guide "cannot" argument the connection cannot actually win.

7. **Scale the documentation to the amount of scope reduction claimed.** The more an organization leans on segmentation to shrink the assessment scope, the more detailed the network diagram, the data flow diagram, and the port/protocol/service documentation need to be. Expect the assessor to verify the segmentation directly rather than accept the diagram at face value.

## Output

One verdict block per claimed separation, added to `scope/network-diagram.md` or a dedicated `scope/separation-log.md`:

```markdown
## Separation claim: <asset or segment name>

- **Configuration:** <VLAN only / ACL / firewall allow-list / DLP / encryption-only, described precisely>
- **Verdict:** not separated / isolation / controlled access
- **Resulting category (feed to cmmc-scope-boundary):** CUI Asset / CRMA / Out-of-Scope

### Allow-list entries judged by payload capacity

| Traffic permitted | Direction | Could it carry a document? | Verdict |
|---|---|---|---|
| DNS UDP/53 | outbound | no | passes |
| NTP | outbound | no | passes |
| <print jobs, file shares, backups, license checks> | <direction> | yes | does not pass; far side is reachable |
```

Feed the resulting category to `cmmc-scope-boundary`, which records it in the SSP through `scribe`.

## Where practitioners disagree

- **Whether DLP plus VLAN rules plus written procedure can meet the "cannot" bar.** One position treats this stack as sufficient because it demonstrably keeps CUI off the asset in practice. The stronger position, and the one this skill defaults to, is that any structurally open path fails "cannot" regardless of the control stack in front of it, because the control can fail without the path itself changing. The outcome depends on the assessor.
- **Whether 3.1.20's lack of the word "cannot" is a real escape hatch or just a different, narrower requirement.** Treat it as a documentation strategy for organization-controlled connections, not as a way to relabel a CRMA as Out-of-Scope.

## Seat notes

**Consultant seat**: run this test on every segmentation claim you inherit from a prior IT team or MSP before it goes into the network diagram; inherited diagrams routinely label VLAN-only configurations as separated. **OSC seat**: if your team's answer to "why is this segment out of scope" is a product name rather than a rule set, treat that as a signal to run this test before the assessor does.

## Sources

- CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the Out-of-Scope "cannot" bar).
- 32 CFR 170.19: https://www.ecfr.gov/current/title-32/section-170.19 (the Out-of-Scope Asset definition).
- CMMC FAQs, F-Q3: https://dodcio.defense.gov/CMMC/FAQ/ (encryption alone does not create logical separation).
- CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.20: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (external connection identification, verification, and control).
- Unified Scoping Guide, ComplianceForge, CC BY 4.0: https://complianceforge.com/ (the Isolation versus Controlled Access vocabulary).
- Practitioner consensus, unattributed, backs the three-tier test in step 1, the payload-capacity rule in step 3, the DLP-as-CRMA position in step 4, and the 3.1.20 latitude reading in step 6.
