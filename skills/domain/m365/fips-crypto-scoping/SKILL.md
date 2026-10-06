---
name: fips-crypto-scoping
description: Decide whether a specific device or software layer needs FIPS-validated cryptography, and whether the module it uses actually qualifies. Maps the CUI data flow to the real encryption and decryption endpoints, sorts each network device into CUI Asset, Security Protection Asset, or out of scope with a three-question tree, stops that logic at cloud storage, produces a per-device verdict, and records each network device the tree clears as an Out-of-Scope Asset, with its reason, in the SSP through scribe. Use whenever a client, vendor, or MSP claims a device "needs FIPS" or "is FIPS compliant," or before buying anything sold as a FIPS solution.
vault_sources:
  - "3.13.11"
  - "3.13.8"
  - "3.13.16"
  - "3.1.13"
  - "3.1.17"
  - "3.8.6"
  - "3.5.10"
  - "Normative vs Informative Sections of the CMMC Assessment Guide"
  - "POA&M Eligibility"
  - "Printer Scoping"
  - "Rev 2 vs Rev 3 Double Baseline"
public_sources:
  - "NIST SP 800-171 Rev 2, 3.13.11: https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final"
  - "32 CFR 170.19, CMMC Scoping: https://www.ecfr.gov/current/title-32/section-170.19"
  - "DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/section-252.204-7012"
  - "CMMC FAQs, B-Q8, E-Q2, F-Q3, F-Q4: https://dodcio.defense.gov/CMMC/FAQ/"
  - "DEFCERT, Not Every Device Needs to Be FIPS Validated (commercial): https://www.defcert.com/blog/not-every-device-neds-to-be-fips-validated"
  - "CMMC Level 2 Assessment Guide, DoD CIO, 3.13.11: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.24, CMMC Scoring Methodology: https://www.ecfr.gov/current/title-32/section-170.24"
  - "reference/32-cfr-170-24-scoring.md"
  - "reference/poam-eligible-46.md"
---

# FIPS crypto scoping

This skill answers one question at a time: does this device, application, or link need FIPS-validated cryptography, and does what it currently uses actually qualify. It does not map the CUI data flow itself (call the Skill tool with `cui-data-flow-mapping` for that) and it does not design the enclave or the network diagram (call `exchange-dlp-enclave-pattern` or `cmmc-scope-boundary` for that); it takes a data flow that already exists and tests each point in it against 3.13.11. When the device tree clears a network device as out of scope, it records that verdict and its reason in the engagement's SSP by calling the Skill tool with `scribe`; every other category belongs to `cmmc-scope-boundary`. It refuses to answer in the abstract: every verdict traces to a named encryption or decryption point in a mapped CUI flow, never to a device category on its own.

## Inputs

- `scope/data-flow.md`, or an equivalent CUI data flow map, showing where CUI enters, is generated, and exits. If this does not exist yet, tell the operator and call the Skill tool with `cui-data-flow-mapping` first; a device-by-device FIPS review without a flow map produces guesses, not verdicts. If the operator directs you to go on without one, work from the sources they name, write those sources in place of the data flow reference in the verdict table, and say in your summary that every verdict rests on them.
- The engagement's record, the components and their assets in `ssp/components/*.md`, so each device or service in the flow has a name, a category, and an owner. Read the files directly; they are the current state. Never read `view/asset-inventory.md`; it is generated for people.
- Vendor documentation or a CMVP search result for every cryptographic component under review, not a marketing page.
- Any existing SSP language for 3.13.11, 3.13.8, or 3.13.16, to check for drift between what was written and what is deployed.

## Method

1. **Map the flow before asking about FIPS.** 3.13.11 is a conditional requirement, triggered only "when used to protect the confidentiality of CUI," so nothing in this method can start from a device category. Start from the actual CUI data flow (call the Skill tool with `cui-data-flow-mapping` if it is not already mapped) and mark every point where data is encrypted or decrypted within it: disk encryption, TLS termination, VPN tunnel endpoints, application-layer encryption, backup encryption. A device that only carries already-encrypted bytes past itself is not one of these points. Do this mapping exercise once per environment and keep it current; it is the only thing that makes the rest of this method answerable instead of argued.

2. **Apply the conditional, not a blanket rule.** 3.13.11's trigger word is "when": FIPS-validated cryptography is only required at the point where a cryptographic mechanism is doing the work of keeping CUI confidential. A cryptographic operation that exists for some other purpose, indexing, integrity hashing, session-key negotiation that does not itself carry CUI, does not trigger the requirement. The Assessment Guide's Further Discussion is explicit that encryption applied inside the already-protected environment of the system, for a purpose other than shielding CUI as it leaves that environment, carries no validation obligation. Treat that distinction as the test: identify what the encryption is actually shielding before deciding it must be validated.

3. **Run every network device in the flow through the device tree, in order.** A switch, router, firewall, access point, or VPN appliance gets its 3.13.11 verdict from what it does to the CUI, not from what it is. The same firewall model can land in any of the three categories depending on where it sits and how it is configured. Ask three questions and stop at the first one that decides:

   | # | Question | Yes | No |
   |---|---|---|---|
   | Q1 | Does the device encrypt or decrypt CUI, or can it reach plaintext CUI (holds the keys, terminates the session, is configured to inspect)? | **CUI Asset.** 3.13.11 applies to its module. Document it in the SSP. Examples: a VPN concentrator that terminates the tunnel and re-encrypts, a next-generation firewall doing TLS inspection, a TLS-terminating server or reverse proxy | Go to Q2 |
   | Q2 | Is the device cited in the SSP for a security function the assessment boundary relies on (default-deny perimeter, enclave segmentation, VLAN enforcement, boundary access control)? | **Security Protection Asset.** Assessed for the security functions the SSP says it performs, such as 3.13.1 boundary protection, and not for 3.13.11. It does not need to run in FIPS mode. Document it in the SSP | Go to Q3 |
   | Q3 | Does it meet all four out-of-scope conditions below? | **Out of scope.** 3.13.11 does not apply. An organization's own device is recorded as an Out-of-Scope Asset with the four conditions as its justification (see Output); it gets no conformity statements. Examples: an enterprise router outside the enclave, the ISP, the public internet | **Resolve the gap** before the verdict stands: fix the failing condition, or reclassify the device as a CUI Asset and meet 3.13.11 on it |

   The four conditions, all of which must hold:
   1. **Encrypted before it arrives** (3.13.8, 3.13.11). The CUI reaching the device is already encrypted by a FIPS-validated module on a CUI Asset upstream. The device is not the thing doing that encryption.
   2. **No decryption** (3.13.10). The device does not decrypt, has no access to the keys, and has no inspection policy that would decrypt.
   3. **No packet capture** (3.13.2, 3.4.6). The device does not capture and store packets in a way that leaves the ciphertext available for later decryption. A span port feeding a full-packet-capture appliance fails this condition.
   4. **No security function for the boundary** (3.1.5, 32 CFR 170.19). The device provides nothing the SSP relies on. Q2 already sorted out the devices that fail this one, and failing it makes the device an SPA, not a problem.

   Two limits on the out-of-scope verdict. First, it rests on FAQ F-Q4, which covers enterprise networking components outside an enclave that is logically separated from the enterprise network. FAQ F-Q3 says encryption alone is not logical separation, so confirm the separation holds (call the Skill tool with `logical-separation-test`) before relying on it. Second, it does not reach inward. A switch inside the assessed boundary is categorized under the usual rules even when everything it carries is encrypted. It still does not need a FIPS module of its own if it never encrypts CUI, but it does not drop out of scope for that reason. The same logic clears the ISP: FAQ B-Q8 accepts that ciphertext crosses common carrier networks, and a device meeting all four conditions is doing what a common carrier does. It also clears an internal printer inside a physical boundary that already protects CUI by other means, and internal hashing that is not protecting CUI in transit or at rest. A FIPS-rated firewall or switch that never terminates an encrypted session is money spent on the wrong control.

4. **Require FIPS validated, never accept FIPS compliant.** Treat "FIPS compliant" as a marketing phrase with no assessment value. The only acceptable claim is that the specific cryptographic module in use has a CMVP (Cryptographic Module Validation Program) certificate number, checked against the current validated modules list, not the vendor's datasheet. Watch for browsers that ship their own cryptographic libraries instead of calling the operating system's validated module; putting the OS into FIPS mode does not automatically cover a browser that does its own crypto. Confirm the module for each encryption point identified in step 1 individually.

5. **Allow layered encryption to satisfy the requirement once, not at every layer.** If a CUI flow crosses a validated layer end to end, for example a TLS session using an OS crypto module already in FIPS mode, an outer tunnel or VPN carrying that already-encrypted session does not also need its own FIPS-validated module. Confirm the inner layer genuinely covers the full path before relying on this; a validated layer that terminates before the data reaches its destination does not clear the outer layer.

6. **Stop the tree at the cloud: storage is not transit.** The device tree clears equipment that forwards ciphertext. It does not clear a provider that stores or processes CUI, encrypted or not.
   - **A cloud service that stores encrypted CUI is still storing CUI** (FAQ B-Q8). It is a CUI Asset, and DFARS 252.204-7012(b)(2)(ii)(D) requires FedRAMP Moderate authorization or equivalency under the DoD CIO memo. FAQ E-Q2 says encryption does not substitute for that. A commercial cloud holding client-side encrypted CUI, with the keys kept on premises, still fails the cloud requirement. For the full CSP and ESP fork, call the Skill tool with `esp-and-msp-scoping`.
   - **The export control carve-out is a different rule.** 22 CFR 120.54(a)(5) and 15 CFR 734.18(a)(5) say that end-to-end encrypted technical data sent or stored abroad is not an export. That answers an ITAR or EAR question. It does not satisfy DFARS 7012 or 3.13.11.
   - **Both ends of the session need a validated module.** A FedRAMP authorized tenant such as GCC High provides the FIPS-validated cryptography on the provider's side, for the offering and features the authorization covers. The contractor's workstation or server that opens the session must run its own validated module, and the browser caveat in step 4 applies there. Record which end each module belongs to in the verdict table.
   - **A cloud security service that decrypts is not a pass-through.** A cloud web gateway, secure access service edge proxy, or email security gateway that inspects TLS traffic carrying CUI answers yes to Q1. It is a CUI Asset and a CSP handling CUI, so both 3.13.11 and the FedRAMP bar apply. Ask every such vendor whether inspection is on for the CUI path; if it can be bypassed for the enclave's traffic, the bypass is the cheaper answer.

7. **Check whether the alternative physical safeguards path is available, and flag that it is closing.** Under NIST SP 800-171 Rev 2, 3.13.8 and 3.13.16 both allow unencrypted CUI in transit or at rest to be protected instead by physical safeguards, a locked facility, badge access, a controlled physical boundary. Rev 3 removes this option entirely for both storage and transmission. Any decision today that relies on the physical-safeguards path, particularly for printers, wireless traffic, and on-site machine-to-machine flows, is a near-term spending decision, not a permanent architecture; note the Rev 3 exposure explicitly wherever this path is used.

8. **Work through the known pain points with the pattern that has actually worked, not a rebuild.**
   - **Wireless.** Consumer and most commercial wireless access points are not FIPS-validated. Either encrypt the CUI at a higher layer before it reaches the radio, so the wireless link only carries already-protected traffic, or require a wired connection for any device handling CUI.
   - **Printing.** General-purpose networked multifunction devices are the hardest case; validated encryption modules for print traffic are rare and getting a print job end to end FIPS-protected is close to impractical on ordinary hardware. Use a print station connected directly to the device with no network hop for CUI print jobs, or a multifunction device with a validated module, and treat the alternative-physical-safeguards path as a bridge that Rev 3 removes, not a permanent answer.
   - **Linux endpoints.** FIPS-mode kernels on common distributions frequently break wireless drivers and other hardware support. Where this is a blocker, isolate the Linux workload behind a validated layer instead, or run it inside a Windows host already in FIPS mode.
   - **Running a newer OS build than its validated version.** This is common, since patched builds routinely move past their CMVP-listed version. Do not treat it as a failure to fix immediately; document it and route it through step 9.

9. **Recognize the CMVP version-drift case, and route it instead of scoring it here.** A validated module that has aged out of its CMVP listing because the OS patched past it is still encryption in place, just not the currently validated module; log it as a Temporary Deficiency. This is the one case in this skill's scope that can carry a POA&M-eligible finding above 1 point, because encryption employed but not FIPS-validated is a different, lighter finding than no encryption at all. See the `POA&M Eligibility` page's rules on this carve-out, and call the Skill tool with `sprs-score-and-poam-eligibility` for the actual point value, the gates, and whether the item can currently sit on a POA&M or should instead run as an operational plan of action; do not recompute that scoring here.

## Output

Two outputs: the out-of-scope verdicts, recorded in the SSP through scribe, and the verdict table, a Markdown working note.

**The out-of-scope verdicts.** For each network device the tree clears at Q3, call the Skill tool with `scribe` and record it as an Out-of-Scope Asset. Never write the `ssp/` files yourself and never edit anything under `view/`. Tell scribe:

1. **The component**: its slug when it is already recorded, or, if it is not, the class of device ("Enterprise network switches"), with one line describing it.
2. **The asset**: its asset id (hostname or asset tag), its component, the category Out-of-Scope Asset, a short description, and its justification: that it met all four conditions, what upstream CUI Asset's FIPS-validated module encrypts the traffic before it arrives, that it holds no keys and decrypts nothing, that it captures no packets, that the SSP relies on it for no security function, and the logical separation it rests on, with the `logical-separation-test` verdict (FAQ F-Q3, F-Q4). When the verdict depends on the broad reading of F-Q4, say so in the justification.
3. **A correction**, when the record already holds the device in another category: its asset id, the new category, the justification above, and remarks saying why the old one was wrong. Correct it in place; do not remove and re-add it.

When the tree clears no device, record nothing and say so to the operator; on a flat network that is the expected result. Record only the organization's own devices. The ISP and the public internet are not assets and get no row; the verdict table and the network diagram carry them. Record nothing for a device the tree does not clear. A device on a flat network, or inside the assessed boundary, never clears Q3 (step 3), and a device whose Q3 answer is no is resolved first, never recorded as out of scope while a condition fails. A device that exits at Q1 or Q2 is a CUI Asset or a Security Protection Asset; when the record holds it in a category the tree contradicts, or does not hold it at all, tell the operator and hand it to `cmmc-scope-boundary` rather than recording it here. A device the record holds as out of scope that the tree does not clear goes to `cmmc-scope-boundary` the same way, and so does any other asset, such as a printer or a phone, that the flow shows handling CUI while the record holds it out of scope.

Before calling scribe, show the operator the devices you will record as out of scope. Record them once the operator confirms, or straight away if the operator asked you to record without stopping. If scribe refuses a change, the refusal is the answer: quote scribe's check line, fix the decision, and ask again. Never work around it. An asset id is unique across the whole SSP.

**The verdict table.** Write it to `scope/fips-verdicts.md` in the engagement repo: a data flow with a named verdict at every encryption and decryption point. It stays Markdown; it is a working note, not the record.

```markdown
# FIPS crypto scoping verdict: <client>

Data flow reference: scope/data-flow.md, dated <date>

| Device or component | Role in the flow | Tree exit | Asset category | Encryption point? | Module claimed | CMVP certificate | Verdict |
|---|---|---|---|---|---|---|---|
| | (pass-through / endpoint / storage / print / cloud) | Q1 / Q2 / Q3 yes / Q3 no / cloud (step 6) | CUI Asset / SPA / out of scope | Y/N | | | FIPS validated / not required / gap: POA&M or OPA / resolve condition <n> |

## Out-of-scope network devices
- <each device cleared at Q3, the four conditions checked, and the logical separation it relies on (FAQ F-Q3, F-Q4). Each of the organization's own is recorded in the SSP as an Out-of-Scope Asset with this as its justification; the network diagram shows it carrying ciphertext only>

## Cloud services in the flow
- <each CSP that stores or processes CUI, its FedRAMP Moderate authorization or equivalency evidence, and which end of each session's cryptography it provides>

## Physical safeguards relied on
- <where the alternative-physical-safeguards path under Rev 2 is in use, and the Rev 3 exposure>

## Open gaps
- <any device without a confirmed CMVP certificate, routed to a POA&M or OPA per step 9>
```

Reference the verdict table from the SSP conformity statements for 3.13.8, 3.13.11, and 3.13.16; `to-ssp` writes those statements, not this skill.

## Where practitioners disagree

- Whether a networked multifunction printer sitting inside a physical boundary can be scoped as out of scope, as a specialized asset comparable to shop-floor equipment, or must be treated as in-scope because a technical path to CUI-handling endpoints exists regardless of VLAN segmentation. The outcome depends on the assessor.
- Whether an SSP that claims the alternative-physical-safeguards path for print or on-site flows will still be accepted once Rev 3 formally removes that path, or whether it will draw an immediate finding. The outcome depends on the assessor.

- Whether FAQ F-Q4 reaches every pass-through device that meets the four conditions, or only the topology it describes: an enclave routing through enterprise networking components to reach the internet. The broad reading treats F-Q4 as one example of a general principle. The narrow reading confines it to its facts. When the verdict for a device outside the enclave depends on the broad reading, say so in the verdict row. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: bring the client the per-device verdict table before they buy anything marketed as "FIPS ready." A FIPS-rated switch or firewall that never terminates an encrypted session is a wasted purchase; a validated print station is often cheaper than a fleet of validated multifunction devices. **OSC seat**: run the CMVP lookup yourself for anything IT already owns before assuming a gap exists; a surprising number of existing Windows and network deployments already clear the bar once the OS crypto module is confirmed in FIPS mode.

## Sources

- CMMC Level 2 Assessment Guide, DoD CIO, 3.13.11: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the conditional trigger, and the Further Discussion language on encryption used within the protected environment).
- 32 CFR 170.24, CMMC Scoring Methodology: https://www.ecfr.gov/current/title-32/section-170.24 (the 3-point versus 5-point split for 3.13.11, and that only 3.5.3 and 3.13.11 score adjustably).
- `reference/32-cfr-170-24-scoring.md`, `reference/poam-eligible-46.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24, https://www.ecfr.gov/current/title-32/section-170.21).
- NIST SP 800-171 Rev 2, 3.13.11: https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final (the text "when used to protect the confidentiality of CUI" that makes the requirement follow function).
- 32 CFR 170.19, CMMC Scoping: https://www.ecfr.gov/current/title-32/section-170.19 (the CUI Asset, Security Protection Asset, and Out-of-Scope Asset categories the device tree sorts into).
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/section-252.204-7012 (paragraph (b)(2)(ii)(D), the FedRAMP Moderate or equivalent bar for a cloud service storing CUI).
- CMMC FAQs, DoD CIO: https://dodcio.defense.gov/CMMC/FAQ/ (B-Q8: encrypted CUI is still CUI, and the common carrier risk accepted for ciphertext; E-Q2: encryption does not substitute for FedRAMP; F-Q3: encryption alone is not logical separation; F-Q4: enterprise networking components outside a logically separated enclave do not extend the assessment scope when CUI is properly encrypted).
- 22 CFR 120.54 and 15 CFR 734.18: https://www.ecfr.gov/current/title-22/section-120.54 and https://www.ecfr.gov/current/title-15/section-734.18 (the end-to-end encryption carve-out is an export rule, not a DFARS one).
- DEFCERT, "Not Every Device Needs to Be FIPS Validated" (2026-06-18), commercial, Tier 3: https://www.defcert.com/blog/not-every-device-neds-to-be-fips-validated (the order of the three device questions, the four out-of-scope conditions and their mapping to requirements, and the transit versus storage caveat for cloud providers; method only, with the rules cited above).
- Practitioner consensus, unattributed, backs ruling out internal hashing, the FIPS-validated-versus-compliant distinction with the CMVP certificate requirement, the browser-crypto-library caveat, the layered-encryption rule, the wireless and printing mitigation patterns, the Linux FIPS-mode driver problem, and the framing of the Rev 3 removal of alternative physical safeguards as a near-term spending decision.
