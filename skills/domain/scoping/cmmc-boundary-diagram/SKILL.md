---
name: cmmc-boundary-diagram
description: Draw the network diagram of the CMMC Level 2 Assessment Scope in draw.io, color-coded by asset category, from the assets and categories already recorded in the SSP and from the environment or firewall config the operator describes. Use whenever an operator asks for the network diagram, the boundary diagram, or the scoping diagram, or after cmmc-scope-boundary has placed the assets.
vault_sources:
  - "CMMC Scoping"
  - "Network Segmentation for Scope Reduction"
  - "VPN Gateway"
  - "3.13.1"
  - "3.13.5"
  - "3.13.14"
  - "raw/CMMC Scoping Guide Level 2 v2.13.md"
public_sources:
  - "CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.19 (CMMC Assessment Scope and asset categories): https://www.ecfr.gov/current/title-32/section-170.19"
---

# CMMC boundary diagram

This skill draws one artifact: the network diagram of the CMMC Assessment Scope that the CMMC Level 2 Scoping Guide requires every organization to provide for pre-assessment scoping discussions. It is a zone-based (trust-boundary) architecture diagram, suitable for the SSP or a C3PAO: nested labeled boundaries, every asset colored by its category, every boundary crossing labeled with what it carries and how it is protected.

It draws decisions; it does not make them. The category of each asset comes from the record. Call the Skill tool with `cmmc-scope-boundary` to place an asset, with `esp-and-msp-scoping` to place a provider, and with `logical-separation-test` to decide whether a segment is really separated. This skill is for the network and boundary picture only. The CUI data flow diagrams, high level and low level, belong to `cui-data-flow-mapping`.

## Inputs

- The engagement's record, `ssp/components/*.md`: the components, the assets, their categories, and the providers with their FedRAMP status. Read the files directly. Never read `view/asset-inventory.md`.
- `scope/network-diagram.md`: the notes file, holding whatever diagram the client handed over and the separation verdicts `logical-separation-test` left there.
- `scope/data-flow.md`, for which boundary crossings carry CUI.
- `scope/network-diagram.drawio`, if a previous run left one. Update it rather than starting over, so the layout the operator already reviewed survives.
- A described environment or a firewall config, when the operator supplies one.
- `CONTEXT.md` for the client's component vocabulary.

When the record holds no assets yet, stop and recommend running `cmmc-scope-boundary` first. A diagram drawn before the assets are placed is a guess with colors on it.

## Method

### 1. Before building

1. Restate the goal in three to five sentences and confirm it with the operator when the environment is non-trivial: what is in scope, which cloud, which ESPs, what the diagram must prove.
2. Ask only what changes the drawing, at most two or three questions. For example:
   - Which segments or VLANs touch CUI, or whether the config's zone names say so.
   - Cloud or on-prem for a tool such as Tenable (a cloud platform plus on-prem scanners or agents?).
   - Whether endpoints are Entra-joined, hybrid-joined, or AD-joined.
3. If the operator provides a firewall config, remind them first to scrub secrets: PSKs, password hashes, SNMP communities, API tokens, FortiToken seeds. If unmasked secrets show up anyway, flag them in the reply as exposed and recommend rotating them. Never copy a secret into the diagram or any file.

### 2. Color every asset by its recorded category

| Category | Fill | Stroke | Style |
|---|---|---|---|
| CUI Asset (processes, stores, or transmits CUI) | #e1d5e7 | #9673a6 | solid, strokeWidth=2 |
| Contractor Risk Managed Asset | #d5e8d4 | #82b366 | solid |
| Security Protection Asset | #dae8fc | #6c8ebf | solid |
| Specialized Asset (OT, IoT, IIoT, GFE, restricted information system, test equipment) | #ffe6cc | #d79b00 | solid |
| Out-of-Scope Asset | #f5f5f5 | #666666 | dashed, fontColor #333333 |

If the operator supplies a different color scheme, use theirs, and keep purple meaning only CUI.

The category on the box is the category in the record, never one inferred while drawing. The checks below catch a record that looks wrong. When one fails, draw the asset as recorded, mark the box with "⚠", and send the asset back to `cmmc-scope-boundary` (or `esp-and-msp-scoping` for a provider) through `scope/open-items.md`. Do not recolor it here.

- Endpoints, file, ERP, and CAM servers, printers and MFPs, and backup repositories holding CUI are usually CUI Assets.
- The firewall, AD domain controllers, DNS, and certificate authority, identity, MDM, EDR, SIEM, RMM, vulnerability scanners, and admin or jump workstations are usually Security Protection Assets.
- CNC and shop-floor PCs that are part of the machine, cameras, and door access are usually Specialized Assets.
- A segment can be drawn as Out-of-Scope only when it has no allowed flow to a CUI Asset (a guest network, an isolated VoIP or IoT segment). A segment with allowed flows into the CUI zone cannot be Out-of-Scope. Write the reason on the box.
- An ESP is drawn with the category and FedRAMP status the record gives it. When the record says it does not store or process CUI, the box says "No CUI stored or processed". A cloud that stores CUI and is not shown as FedRAMP Moderate or equivalent is a finding.

Out-of-Scope Assets need no diagram entry under the Scoping Guide. Draw one when it explains a boundary, such as a guest VLAN beside a CUI VLAN, and leave it off otherwise. Printers, MFPs, and OT assets are the exception: draw every one, whatever its category, because the assessor will ask about each.

### 3. Layout conventions

- The title goes at the top. The **CMMC Level 2 Assessment Scope** is a large container: dashed black, `dashPattern=8 4`, strokeWidth 2, no fill.
- Inside the scope, from left to right:
  - Remote users (if a VPN exists) and a **Public Internet** cloud (`ellipse;shape=cloud`, grey) at the top.
  - An **On-prem site** container (fill #fafafa, stroke #333, width 2).
  - The firewall box at the top of the site (Security Protection Asset blue, strokeWidth 3), listing the model and OS, the NGFW features, the zone policy, admin MFA, and that all VLANs terminate there.
  - One dashed grey container per firewall zone, labeled `Firewall zone: <name>` in bold italic. Inside each zone, one box per VLAN colored by category: VLAN ID and name (bold), subnet, key hosts with IPs, and purpose. Mark warnings with "⚠".
  - Hosts of a different category inside a VLAN go in a nested child box (for example, domain controllers as a blue box inside the purple Servers VLAN).
  - An **External Service Providers** container (blue stroke, white fill), stacked with one box per ESP: name, commercial or FedRAMP, what it touches, and "No CUI" where the record says so.
  - The **cloud service provider block** on the right (see the standard below).
- Outside the scope, at the bottom: the legend, and a "Personal and unmanaged devices: out of scope" box with a red dashed ✕ "Blocked" edge (`endArrow=cross`) to the identity block. Draw that box only when the record or the operator confirms personal devices are blocked.
- A flat network has one zone. Draw it as one zone; do not invent segments to make the picture look tidier.

#### Standard Microsoft 365 GCC High block

Use it exactly when the record shows the tenant is GCC High. For any other tenant, keep the same structure and change the label and the authorization to what the record says.

- **Outer container** (490x545):
  - Label: "Microsoft 365 GCC High: FedRAMP High authorized (Cloud Service Provider)"
  - Style: white fill, stroke #1a1a1a, strokeWidth 4.
- **Inner purple container**, "CUI Storage and Processing: CUI Assets" (460x205, at 15,45):
  - Four white boxes, 100x55 at y=45 and x=15, 125, 235, 345: Exchange Online, SharePoint Online, OneDrive for Business, Microsoft Teams.
  - Note: "CUI labeled with Purview sensitivity labels. Encrypted at rest (service-side encryption) and in transit (TLS 1.2+). Data resides in US sovereign cloud; support staff are screened US persons." Drop any sentence the engagement has not confirmed, such as the labeling.
- **Inner blue container**, "Security Protection Assets" (460x255, at 15,270), with icons:
  - Entra ID: `https://app.diagrams.net/img/lib/azure2/identity/Azure_Active_Directory.svg`, label "MFA · Conditional Access"
  - Intune: `https://app.diagrams.net/img/lib/azure2/intune/Intune.svg`, label "Device compliance"
  - Defender for Endpoint: `https://app.diagrams.net/img/lib/azure2/security/Azure_Defender.svg`
  - Purview: `https://icons.diagrams.net/assets/microsoft-fabric/1/Microsoft_Purview.svg`, label "Audit · DLP · Labels"
  - A note box mapping them to the AC, IA, CM, SI, and AU families.

#### Edges: label every boundary crossing

- Orthogonal, rounded, bidirectional (`startArrow=block;endArrow=block`), strokeWidth 2, `labelBackgroundColor=#ffffff`, fontSize 10.
- Color each edge by what it carries:
  - Purple: CUI traffic, for example "HTTPS · TLS 1.2+ · CUI access". Take which crossings carry CUI from `scope/data-flow.md`.
  - Blue: authentication, management, or telemetry.
  - Blue dashed: ESP agent telemetry.
  - Dark grey: WAN or inter-VLAN.
  - Green dashed: allowed cross-zone flows between a Contractor Risk Managed Asset and a CUI Asset (list the services).
- VPN edge: state the protocol, the IdP and MFA, and the crypto suite (for example, IKEv2, Entra SAML plus MFA, AES-256 and SHA-256, DH group 20).

#### Legend (bottom)

Three columns: the five category swatches, the cloud service provider boundary swatch, the assessment boundary line, the firewall zone line, and the cross-zone flow arrow.

### 4. Parsing a firewall config (FortiGate example; adapt for others)

Extract:

- `system interface`: WANs (alias and ISP; mask public IPs unless the operator wants them shown), VLANs (vlanid, subnet, alias).
- `system zone`: zone membership. Zone names often declare CUI intent.
- `firewall address` and `addrgrp`: named hosts and their comments (servers, printers, scanners, NAS).
- `firewall policy`: cross-zone allows. Find specifically:
  - Any accept from a non-CUI zone into a CUI zone, or the reverse. Each one means the segment cannot be Out-of-Scope; send it to `logical-separation-test`.
  - Guest isolation.
  - Overly broad rules (service ALL, setup leftovers).
- `vpn ipsec phase1` and `phase2`, `user saml`, `user group`: VPN type, IdP (login.microsoftonline.us means GCC High), groups, crypto.
- `log syslogd` and `log fortiguard`: where logs go. Each destination is an ESP or Security Protection Asset; check it is in the record.
- `system dhcp server`: DNS servers that point to domain controllers mean on-prem AD exists.
- `system fips-cc`: empty or disabled means the firewall is not in FIPS mode. Do not call that a failure here. Put it on `scope/open-items.md` for `fips-crypto-scoping`, which decides whether this device needs validated cryptography for 3.13.11 at all.

Any host, segment, or provider the config reveals that the record does not hold goes on `scope/open-items.md` for `cmmc-scope-boundary` or `esp-and-msp-scoping`. Draw it with a "⚠ not in the record" note until it is placed.

### 5. Build

Use the draw.io connector's `create_diagram` with **XML** (not Mermaid) and `routing: "libavoid"`. Do not use `postLayout`; it moves the boxes and breaks the containers.

- Use `search_shapes` only for icons you have not verified.
- The XML must have no comments. Escape HTML in values (`&lt;b&gt;`, `&lt;br&gt;`), and avoid a raw `&` (write "and").
- Use `container=1;collapsible=0;` on every boundary, with children in relative coordinates. Edges can connect cells in different containers.
- Size boxes so the text fits (fontSize 10, spacing 8). A full environment is usually a page of about 1800x1260; a simple cloud-only one is about 1200x840.

The connector displays the diagram but saves nothing. Write the same XML, wrapped in `<mxfile><diagram name="CMMC Assessment Scope">...</diagram></mxfile>`, to `scope/network-diagram.drawio` in the engagement repo, so the diagram is versioned with the record it was drawn from. If the draw.io desktop CLI is installed, also export `scope/network-diagram.drawio.png` for people who do not have draw.io.

## Output

- `scope/network-diagram.drawio`, and its PNG when it could be exported.
- One line per assumption and per finding on `scope/open-items.md`, each with who will check it. An assumption made while drawing is an unverified fact, and unverified facts live there, never in the record.
- Nothing in the `ssp/` files. This skill records no decision; if drawing showed that one is wrong, the owning skill corrects it through `scribe`.

Then reply to the operator. Keep it short; the diagram is visible, so do not describe it again.

1. One sentence on what the diagram shows.
2. **Assumptions to confirm**: each guess made while drawing (segment purpose, join type, collector role, any box drawn ahead of the record).
3. **Findings that will matter in an assessment**: numbered, most important first. For example:
   - Exposed secrets.
   - A firewall not in FIPS mode, sent to `fips-crypto-scoping`.
   - Segments that cannot be out of scope.
   - Broad or leftover rules.
   - IoT devices in CUI VLANs.
   - Weak VPN or SNMP settings.
   - ESPs missing from the record.
   - Assets whose recorded category the checks in step 2 flagged.
4. Offer to update the diagram once the assumptions are confirmed.

## Seat notes

**Consultant seat**: an inherited diagram is a claim, not evidence. Draw from the record and the config, then compare with what the client handed over in `scope/network-diagram.md`; every difference is an open item. **OSC seat**: redraw whenever `significant-change-determination` finds the network diagram shifts. The diagram an assessor sees should match the network on assessment day.

## Sources

- CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the requirement to document each in-scope category in the network diagram of the CMMC Assessment Scope, and to provide that diagram for pre-assessment scoping discussions).
- 32 CFR 170.19: https://www.ecfr.gov/current/title-32/section-170.19 (the five asset categories the colors stand for).
- Practitioner consensus, unattributed, backs the layout, color, and edge conventions and the firewall parsing checklist. They are a house style, not a requirement; an assessor accepts any diagram that shows the boundary, the categories, and the connections.
