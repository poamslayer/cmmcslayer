---
name: endpoint-and-vdi-scoping
description: Decide whether a laptop, thin client, home network connection, or personal device is in the CMMC Assessment Scope, and which test decided it. Covers the VDI keyboard/video/mouse carve-out, the hops test for remote access, VPN documentation under 3.1.12, cloud-native inheritance of the physical protection family, personal-device RDP, and the unresolved wireless positions. Records each endpoint and its category in the SSP through scribe. Use whenever an operator asks whether a specific endpoint, remote connection, or device needs to be assessed.
vault_sources:
  - "VDI Scoping"
  - "Remote Access"
  - "Wireless Network Scoping"
  - "3.1.12"
  - "3.1.13"
  - "3.1.14"
  - "3.1.15"
  - "3.10.6"
  - "3.13.7"
  - "raw/CMMC-FAQs-v2.3-May-2026.md"
  - "raw/AC.L2-3.1.12.md"
  - "raw/unified-scoping-guide.pdf"
public_sources:
  - "CMMC FAQs, F-Q1 and F-Q2 (VDI endpoint scoping): https://dodcio.defense.gov/CMMC/FAQ/"
  - "32 CFR 170.19 (Out-of-Scope Asset definition and the VDI carve-out): https://www.ecfr.gov/current/title-32/section-170.19"
  - "CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.12: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "NIST glossary, remote access: https://csrc.nist.gov/glossary/term/remote_access"
  - "Unified Scoping Guide, ComplianceForge, CC BY 4.0, Appendix B: https://complianceforge.com/"
---

# Endpoint and VDI scoping

This skill places a single endpoint or remote connection in or out of the CMMC Assessment Scope and names the test that decided it. It covers thin clients accessing Virtual Desktop Infrastructure (VDI), laptops connecting by VPN, cloud-native access with no on-premises network at all, and personal devices reaching a CUI endpoint by Remote Desktop Protocol (RDP). It does not draw the network diagram and it does not judge whether a specific remote-access control implementation clears the bar for its requirement (call `control-evidence-lookup` for that); it decides placement, names what evidence 3.1.12 through 3.1.15 will need, and records each endpoint and its category in the engagement's SSP by calling the Skill tool with `scribe`.

## Inputs

- The endpoint or connection under review: managed or unmanaged, what it connects to, and what protocol carries the session.
- The VDI or RDP server-side configuration, if one is in use: whether clipboard, file transfer, drive redirection, printer redirection, and local caching are disabled, and where that is enforced.
- Whether the organization has any on-premises network at all, or is fully cloud-native.
- Where the user is physically located when connecting (office, home, a client site, a public space).
- `scope/cui-determinations.md`, for which documents and data are CUI. A placement that rests on whether something is CUI takes that status from the determinations; never infer it yourself from what a file was made from. When an item has no determination, do not decide it here. Place the asset on facts that do not depend on it, and put the question on `scope/open-items.md` for `cui-determination-workflow`.
- The engagement's record, `ssp/ssp.json`, for the endpoints, components, and categories already recorded, and `CONTEXT.md`. Read it by calling the Skill tool with `scribe` and asking it to show the record; that is the current state. Never read `view/asset-inventory.md`; it is generated for people. The walk, the company's own documents, and the record are the sources.

## Method

0. **Place an ordinary in-office endpoint by the Process/Store/Transmit test.** A desktop or laptop used only inside the office, with no VDI and no remote session, needs none of the tests below: it is a CUI Asset when it processes, stores, or transmits CUI, as `cmmc-scope-boundary` defines them. One that can reach CUI, with no technical separation from it, is a Contractor Risk Managed Asset (CRMA) only when a written policy and procedure keep CUI off it; with none, it is a CUI Asset. Say which in the remarks, and put the role question on the open items list when nobody has confirmed what the user of that endpoint handles. Then run the steps below on whatever remote connection the same endpoint also has.

1. **Apply the VDI keyboard/video/mouse (KVM) carve-out precisely.** Per 32 CFR Part 170 and CMMC FAQ F-Q1/F-Q2, an endpoint hosting a VDI client is Out-of-Scope only when the client is configured to allow nothing beyond keyboard, video, and mouse data to the session, and that configuration is verified on the server side. Displaying CUI in an application or browser window counts as the endpoint processing and transmitting it, because the data exists in that device's CPU and RAM the moment it renders, even if nothing is saved locally. To hold the carve-out, the VDI server must block copy-paste, file transfer, screenshots, and printing to the endpoint, and access to the VDI server must require multifactor authentication that is separate from the endpoint itself. Any one of those controls missing collapses the endpoint back into scope as a CUI Asset.

2. **Watch for mixed use collapsing the carve-out.** An endpoint that reaches a CUI-holding VDI session and is also used for ordinary, non-CUI business on the same device no longer meets the KVM-only test, because the device is doing more than relaying a keyboard, a video feed, and a mouse. As soon as that same box doubles as a regular, everyday workstation, it counts as a CUI Asset no matter how carefully the VDI session itself is locked down. Where mixed use is unavoidable, treat the non-VDI side of the device as its own reachable path and run `logical-separation-test` on it, or split CUI work and non-CUI work onto separate physical or virtual devices.

3. **Apply the hops test to decide whether a connection is remote at all.** A connection is remote when any hop between the two endpoints leaves organizational control, most commonly the internet. If every hop stays inside the organization's own controlled network, the connection is not remote, even if it uses a network protocol. Worked placements:

   | Connection | Remote? | Why |
   |---|---|---|
   | In-office device to an on-prem server, no external hop | No | Every hop stays on the internal network |
   | User VPN from home or a client site | Yes | The connection crosses the internet before reaching the boundary |
   | Site-to-site or permanent point-to-point VPN between two offices | No | Treated as an extension of the organization's own network, not a hop to an outside party |
   | Direct access to cloud or SaaS resources over the internet | Yes | The connection crosses the internet, unless first routed through an organization-controlled VPN tunnel with restricted access on the far end |

4. **Document VPN as a type of permitted remote access even when it is operated as internal.** NIST SP 800-171's discussion under 3.1.12 allows an organization to treat a well-provisioned encrypted VPN connection as an internal network for operational purposes once the tunnel is established. That permission is about how the connection may be operated; it does not remove the connection from 3.1.12[b]'s identification requirement. List VPN, and any other method that crosses the internet before landing inside the boundary, as an identified type of permitted remote access, whatever operational latitude is claimed for it afterward. A fully cloud-native organization with no office at all still has types to name: TLS to hosted resources, a cloud access gateway, or whatever mechanism actually carries the connection.

5. **Split the physical protection family for cloud-native organizations.** When the organization's only CUI assets live inside a Cloud Service Provider's data center, such as behind a VDI solution, the requirements covering physical protection of that data center (3.10.1 through 3.10.5) are inherited from the provider. The one requirement that is never inherited is 3.10.6, safeguarding CUI at alternate work sites, because the provider has no visibility into an employee's home office or hotel room. A fully cloud-native organization is, for this purpose, an organization where every user connects from an alternate work site, since reaching the cloud-hosted system always crosses the internet unless the user is physically inside the provider's facility.

6. **Place personal-device RDP by the process-path test, not by storage.** A personal device that opens an RDP session into a CUI-holding machine is in the CUI process path even if nothing is ever saved to it, because the screen content and keystrokes it exchanges are the same category of processing the KVM carve-out is meant to prevent. Standard RDP does not limit the exchange to keyboard, video, and mouse by default; clipboard, drive, and printer redirection have to be explicitly disabled on the session host for the endpoint to have any chance of staying out of scope. Three ways to make the connection defensible: reconfigure it as a provable KVM-only VDI client that meets the step 1 bar; convert the personal device into a managed enclave device the organization actually controls; or build real logical separation between the personal device and the CUI machine with VLANs, ACLs, or a jump host, verified with `logical-separation-test`. Absent one of the three, treat the personal device as in scope.

7. **Carry the unresolved wireless positions as open items, not settled answers.** A late-2025 revision to scoping guidance put network hardware that merely carries already-encrypted CUI traffic back on the table for review, unsettling a question many practitioners had considered closed. Guest wifi with no route into the CUI environment can reasonably be treated as Out-of-Scope. A wifi network that does reach the CUI environment should be tested the same way a wired VLAN is, under `logical-separation-test`, since wireless has its own attack surface and can be treated as an internal boundary. Home networks and public networks such as coffee shops have no settled position: some practitioners would pull them into scope under the same reasoning as corporate wifi, others hold that is too broad a reading. Ask the operator which posture the client has chosen. Record the chosen posture and the reasoning behind it as an open item, or, when none has been chosen, record the question as undecided with the options; do not present either side as decided. Guest devices on a network that reaches the CUI environment are not the organization's assets and get no row in the record; they belong in the same open item, as the reason the network fails separation.

8. **Check split tunneling on any remote endpoint.** A device that can hold a remote session to the organization's systems while simultaneously routing other traffic to the open internet may violate the requirement to prevent split tunneling (3.13.7). Endpoint-level controls (host firewall, endpoint detection, DNS filtering) that make the device its own enforcement boundary are an accepted substitute for a hardware VPN concentrator, particularly for cloud-only environments; a policy statement with no technical enforcement behind it is not.

## Output

Record every placement in the SSP by calling the Skill tool with `scribe`, one decision at a time. Never write `ssp/ssp.json` yourself, and never edit anything under `view/`: the record is the inventory, and scribe renders `view/asset-inventory.md` from it for people. Point the operator at that view when they want to read the placements.

A connection is not an asset; the devices at each end are. Record the endpoint, and carry what you decided about the connection in the endpoint's remarks. For each endpoint, tell scribe:

1. **The component**, if it is not already recorded: the class of device the endpoint belongs to, with one line describing it. A personal or home device never goes on the company's managed-endpoint component, because the conformity statements that describe a managed laptop are not true of it; give personal devices their own component. When endpoints of one component land in different categories, ask scribe to split the component so each category, and each set of statements, has its own.
2. **The asset**: its name (hostname, asset tag, or a plain name such as "Dana's home PC"), its component, its category, a short description, and remarks naming each test that decided it (Process/Store/Transmit, KVM carve-out, hops test, process-path test, inheritance split; an endpoint often needs two, one for its category and one for its connection), what the test found, and, for a remote connection, the type of remote access it uses under 3.1.12[b] (VPN, RDP over VPN, TLS to a cloud resource, a cloud gateway, vendor remote support through a remote monitoring and management (RMM) tool or a vendor portal). A flow that is not a permitted type at all, such as CUI sent to a personal email account, is named as unauthorized, and the remarks say it should be stopped rather than scoped in permanently. Until it is stopped and the copies are gone, the device that received the CUI is a CUI Asset; it cannot be Out-of-Scope, because nothing stops it holding CUI. Once the flow is stopped and the copies removed, ask scribe to remove the asset. The remarks hold what was decided and verified; a fact nobody has checked (whether redirection is disabled on the session host, whether split tunneling is blocked, whether a laptop leaves the building) goes on `scope/open-items.md` instead, with who will check it. An Out-of-Scope endpoint must carry its justification: the server-side configuration that holds the KVM carve-out, or the technical barrier that removes every path.
3. **A correction**, when the record already holds the endpoint in a category your method rejects: the new category, and remarks saying why the old one was wrong. Correct it in place; do not remove and re-add it.

Record only endpoints and the devices at the organization's end of a remote connection. A device at an outside provider's end (the MSP's technician laptops, a vendor's portal) is placed by `esp-and-msp-scoping`; name the connection in the remarks of the organization's endpoint and hand the provider to that skill. A general-purpose PC on the shop floor is an endpoint and is yours; the machine it sends programs to, and a PC dedicated to a machine as part of it, are not. A printer, shop-floor machine, server, or other asset you notice on the way is not yours to recategorize, even when its recorded category looks wrong: tell the operator which ones and hand them to `cmmc-scope-boundary`, or to `printer-and-ot-asset-scoping` for printers and shop-floor equipment.

The list of permitted remote access types for 3.1.12[b] is a conformity statement, and this skill does not write statements; `to-ssp` writes it later from the types these remarks name.

Before calling scribe, write the placements as a table and show it to the operator. Record them once the operator confirms, or straight away if the operator asked you to record without stopping. Scribe gets one row per call:

```markdown
| Endpoint | Component | Test applied | Category | Remote access type (3.1.12[b]) | Reason (the remarks) |
|---|---|---|---|---|---|
| <thin client, laptop, personal device> | <component title> | P/S/T / KVM carve-out / hops test / process-path test / inheritance split, one or more | CUI Asset / Contractor Risk Managed Asset / Out-of-Scope Asset | <VPN, RDP over VPN, TLS to cloud resource, cloud gateway, vendor remote support, unauthorized, none> | <what the tests found> |
```

If scribe refuses a change, the refusal is the answer: read its reason, fix the decision, and ask again. Never work around it. Give an asset a name without commas, because a split names the assets it moves as a comma-separated list, and change the assets' categories before giving their component one.

Log any wireless posture decided under step 7, and the reasoning for it, on the engagement's open items list, `scope/open-items.md`, which stays Markdown. It does not go in an asset's remarks or an SSP statement until it is confirmed.

## Where practitioners disagree

- **Whether an established VPN tunnel is "not remote" once connected.** An earlier reading held that only the initial handshake is remote and that traffic inside an established tunnel is not. The harder-line and more recently dominant reading, carried in step 4, is that the connection still belongs on the organization's list of permitted remote access methods for 3.1.12[b], no matter how the tunnel is treated operationally afterward. Document your interpretation and rationale clearly regardless of which position you take; the outcome depends on the assessor.
- **Whether accessing an organization's own cloud-hosted SaaS environment over the internet counts as remote access at all under 3.1.14.** One position argues the managed access control point requirement was written for legacy on-premises infrastructure and does not cleanly apply to SaaS; the safer practice is to demonstrate a managed access control point (such as cloud identity conditional access) regardless of which reading is correct, since the requirement is trivially satisfiable either way.
- **Home networks and public wifi**, per step 7: no consensus exists on whether they belong in scope after the late-2025 shift. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run the hops test and the VDI carve-out test on every remote-access pattern during discovery, and put the wireless open items on the pre-assessment question list for the client's chosen C3PAO before design work locks in. **OSC seat**: if IT cannot answer "does our VDI block clipboard and printing" with a configuration screenshot, treat the endpoint as in scope until it can.

## Sources

- CMMC FAQs, F-Q1 and F-Q2: https://dodcio.defense.gov/CMMC/FAQ/ (the VDI endpoint scoping test and its required configuration).
- 32 CFR 170.19: https://www.ecfr.gov/current/title-32/section-170.19 (the Out-of-Scope Asset definition the VDI carve-out relies on).
- CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.12: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the remote access definition and the hops reasoning).
- NIST glossary, remote access: https://csrc.nist.gov/glossary/term/remote_access.
- Unified Scoping Guide, ComplianceForge, CC BY 4.0, Appendix B: https://complianceforge.com/ (the VDI scoping edge case and its compensating controls).
- Practitioner consensus, unattributed, backs the mixed-use collapse rule in step 2, the VPN-as-permitted-remote-access reading in step 4, the cloud-native inheritance split in step 5, the personal-device RDP placement in step 6, and the wireless open items in step 7.
