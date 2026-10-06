---
name: over-engineering-guard
description: Test whether a proposed control is required by an assessment objective, optional and worth the spend anyway, or over-engineering that a cheaper alternative already satisfies. Use whenever a consultant, vendor, or an OSC's own team proposes a purchase or a build that costs money and nobody has pointed to the objective that requires it.
vault_sources:
  - "3.1.1"
  - "3.1.11"
  - "3.1.13"
  - "3.1.16"
  - "3.1.22"
  - "3.5.4"
  - "3.5.11"
  - "3.4.2"
  - "3.7.4"
  - "3.6.1"
  - "3.10.2"
  - "3.13.11"
  - "3.8.4"
  - "3.1.9"
  - "3.13.7"
  - "3.13.6"
  - "Practitioner insights A"
  - "Practitioner insights B"
  - "Normative vs Informative Sections of the CMMC Assessment Guide"
  - "Must-Have vs Nice-to-Have Security Controls"
public_sources:
  - "CMMC Level 2 Assessment Guide, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "NIST SP 800-171A: https://csrc.nist.gov/pubs/sp/800/171/a/final"
  - "32 CFR 170.19 (CMMC scoping, Specialized Assets): https://www.ecfr.gov/current/title-32/section-170.19"
  - "Unified Scoping Guide, ComplianceForge, CC BY 4.0: https://complianceforge.com/"
---

# Over-engineering guard

This skill answers one question about a proposed control: is it required, is it optional but worth doing anyway, or is it spending money to solve a problem the requirement does not have? It gives you the two questions to ask before signing off on a purchase or a build, a table of named cases where the answer turned out to be over-engineering, and the cases where the vault says spend anyway. It refuses to bless a control as sufficient (that is `control-evidence-lookup`) and it refuses to declare something over-engineering without pointing at the objective, or the absence of one, that makes the case.

## Inputs

- The proposed control: what it is, what it costs, and which requirement it is being sold against.
- The requirement id it targets (`3.x.y`) and, if available, the applicability matrix row from `scope/applicability-matrix.md` showing whether the component is even in scope for that requirement.
- Optionally, the requirement's conformity statements in the record, `ssp/ssp.json`, if the proposal is already written into one. Call the Skill tool with `scribe` and ask it to show the record for the requirement. Never read `view/` instead; it is generated for people and can be stale.

**When a proposal cites no requirement at all, that is the finding.** It arrives often: a provider proposes a tool because it is good practice, or because they deploy it everywhere, and nobody has said which objective it answers. Do not guess the requirement on the vendor's behalf and then grade the guess. Return **no requirement cited**, say that the proposal cannot be judged against a bar nobody has named, and put one question back to whoever proposed it: which assessment objective does this satisfy? A proposal that cannot answer that is discretionary by definition, whatever its other merits, and it gets budgeted as discretionary rather than as compliance work.

**Judging whether a tool may be used at all is a different question and not this skill's.** Over-engineering asks whether a control goes past what an objective requires. Whether a cloud service can hold CUI at all, whether a provider's access model puts it in scope, whether a change needs a reassessment: those are gates, not excess. Route them. Call the Skill tool with `significant-change-determination` for a change to an assessed environment, and with `esp-and-msp-scoping` for a provider. A tool that fails those gates is not over-engineering; it is unusable, and saying "that is more than you need" about it gives the operator exactly the wrong instruction.

## Method

1. **Ask the two diagnostic questions before anything else.**

   - *Am I looking at a requirement here, or just a risk worth managing?* A risk is a reason to weigh spending money; a requirement is a reason you have no choice. Confusing the two is how a security team ends up defending a purchase to an assessor with nothing in 800-171A to point to.
   - *Which assessment objective requires this?* If nobody in the room can answer with a lettered objective, treat the proposal as discretionary until someone can. Call the Skill tool with `normative-requirement-test` to run this question properly against a specific cited passage.

2. **Separate the compliance floor from the discretionary layer.** A control that meets an objective is a minimum compliance requirement, driven from outside by the contract. A control that goes beyond every applicable objective is a discretionary security requirement, driven by the organization's own risk appetite. Both can coexist in a mature program. The failure mode this skill exists to catch is treating a discretionary choice as if the contract demanded it, which inflates cost without anyone having decided to spend the money on purpose.

3. **Apply the cost argument.** The organizations with the least developed understanding of CMMC are the ones that pull everything into the assessment scope and end up carrying the largest possible expense and administrative load. Narrowing scope and applicability correctly, before buying anything, costs less over the life of the program than buying broadly and unwinding it later. Over-engineering and over-scoping come from the same root cause: nobody separated "the contract requires this" from "this seemed like the safe thing to do."

4. **Check the proposal against the named findings.** These are documented cases where a proposed control, once tested against its requirement's actual objectives, turned out to be unnecessary. The pattern repeats across many requirements, so use the table to spot a proposal that rhymes with one of these even if the specific technology differs.

   **The requirement column says where the finding was recorded, not where it applies.** Match on the shape of the argument, not the id. The same control offered against a different requirement is the same finding, and the whole value of the table is that a vendor proposing it rarely cites the requirement it was first written against. Confirm the transfer against the target requirement's own control file before you rely on it; the table narrows where to look, it does not decide.

   | Requirement | Proposed control | Why the objective does not require it | Sufficient alternative |
   |---|---|---|---|
   | 3.1.1 | Disabling Bluetooth device-wide | Access-control objectives, not wireless; nonessential-functions language only asks the org to weigh restricting radios, not remove them | Block Bluetooth file-transfer profiles via endpoint management; leave the radio on |
   | 3.1.11 | A 2-hour idle logoff on ordinary, non-VDI workstations | Session-termination sets no specific duration, only that one is defined | A shorter, documented timeout; reserve short ones for shared or VDI sessions |
   | 3.1.13 | A dedicated FIPS VPN on top of a connection that already terminates inside GCC High | Remote-access confidentiality is already met by GCC High's own FIPS-validated encryption | Document the GCC High termination and rely on its session encryption |
   | 3.1.16 | 802.1X to satisfy wireless access authorization | Wireless-access is met by limiting the network to authorized users and devices; 802.1X answers a different identification objective | A managed WPA2 or WPA3 pre-shared key with issuance and rotation documented |
   | 3.1.22 | Monitoring employees' personal social media | Public-information review covers content on systems the org controls, not personal accounts | Cover it in awareness training and rules of behavior |
   | 3.5.4 | Packet captures to prove replay resistance | Configuration evidence and vendor documentation satisfy the objective | Export the protocol settings and cite vendor documentation |
   | 3.5.11 | Disabling the password-reveal control everywhere | Authenticator feedback does not require removing a user-triggered reveal control | Leave it available except on shared or public terminals |
   | 3.4.2 | A separate baseline for every OS-bundled applet | An applet that inherits the OS's own settings is already covered by that baseline | One baseline per OS or suite, with an appendix only for outliers |
   | 3.7.4 | A dedicated air-gapped scanning machine | Endpoint protection with real-time, on-insertion scanning already checks removable media | Turn on the existing platform's scan-on-insertion feature |
   | 3.6.1 | 24/7 security operations center monitoring | The incident-handling objectives set no staffing model or coverage window | A documented capability, business-hours staffed with on-call escalation |
   | 3.10.2 | A camera on CUI already in a locked cabinet in a locked room | Two independent locked barriers already satisfy physical-access monitoring | A logged entry process for the room and the cabinet |
   | 3.10.2 | Redundant power supplies and fail-closed doors | The objective is access monitoring, not uptime; 800-171 dropped 800-53's availability-focused physical controls | Standard locking hardware and logged entry; spend on backup instead |
   | 3.13.11 | FIPS-validated firewalls and switches carrying only ciphertext | The FIPS objective reaches the module that encrypts or decrypts CUI, not pass-through gear | Validate the module that actually does the encrypting |
   | 3.8.4 and 3.1.9 | CUI stickers on laptops and a verbatim government-system banner | Marking and notification objectives do not require an exterior label; a label invites theft; the banner is written for government-operated systems | A marking procedure with no exterior labels, and a banner written for a private system |
   | 3.13.7 | A hosted VPN concentrator with geofencing for a cloud-only org | The objective stops a device bridging an external and internal network at once; a cloud-only org has no on-premises segment to bridge | Disable split tunneling on whatever remote clients exist |
   | 3.13.6 | Per-executable firewall rules or IP allow-listing | Default-deny with the necessary exceptions satisfies boundary protection | A default-deny outbound rule set scoped to the required ports |

5. **Watch for the same mistake one level up: mis-scoping an asset, not just over-building a control.** A documented pattern in shop-floor environments is a consultant writing a CNC machine or similar production equipment into the SSP as a CUI Asset by default. That decision, made once at the scoping stage, drags every one of the 110 requirements onto a machine that usually cannot implement most of them, and the shop then either fails those rows or spends heavily trying to force compliance onto equipment that was never built for it. Test the asset category first: if the machine cannot store, process, or transmit CUI on its own and only handles data incidentally through operational technology, it is very likely a Specialized Asset, documented in the inventory and SSP and managed under a risk-based policy, not assessed against the Level 2 requirements. Getting the category right the first time prevents the over-engineering the wrong category would otherwise force.

6. **Balance the guard: name where spending anyway is worth it.** Refusing over-engineering is not the same as refusing all discretionary spend. Three places the vault consistently treats as worth paying for even though nothing forces the exact form:

   - **A real second authentication factor**, as opposed to a control that gets called MFA but is not: a domain-joined device alone, IP address allow-listing alone, or a MAC address are all documented as rejected substitutes, not accepted factors. Spending to deploy an actual second factor, rather than arguing a workaround counts, is money well spent.
   - **Segmentation an organization can actually defend**, as opposed to a paper claim of separation. Where a component is being carved out of scope as physically or logically separated, or documented as a Contractor Risk Managed Asset, the separation has to be real enough to explain to an assessor, and building it properly is worth the cost.
   - **A mock or practice assessment before the real one.** Running a dry run ahead of a certification or self-assessment catches the gap between what the SSP claims and what supporting documents actually show, which is cheaper to fix on your own schedule than during the 180-day POA&M clock. Call the Skill tool with `sprs-score-and-poam-eligibility` once a mock has surfaced NOT MET items, to check what can and cannot go on a POA&M.

## Output

Return a verdict for each proposed control, either inline or appended to the applicability matrix row it modifies.

**One verdict per control, never per proposal.** Vendors bundle. A single pitch often carries one control that closes a real gap and another that closes nothing, and a single verdict on the bundle either buys the second or refuses the first. Split the bundle, and say plainly that you have, so the operator can accept one line item and decline the other.

```markdown
# Over-engineering guard verdict: <requirement id>, <proposed control>

Diagnostic question 1: requirement, or risk? <answer>
Diagnostic question 2: assessment objective that requires it: <letter and text, or "none produced">

Verdict: required by objective <letter> / optional, discretionary spend / over-engineering
Sufficient alternative, if over-engineering: <what to do instead>
Spend anyway, if discretionary and chosen on purpose: <yes/no, and why>
```

## Where practitioners disagree

- **Whether a mock assessment is worth the cost for a small, simple environment.** Some practitioners treat it as close to mandatory before any certification attempt; others consider it overkill for a one- or two-person IT shop with a short, well-understood scope. The outcome depends on the assessor pool the organization expects to face and how much documentation risk it is willing to carry into the real assessment.
- **Whether a Specialized Asset determination for shop-floor equipment will hold up.** Practitioner consensus treats most CNC and similar production equipment as Specialized rather than a CUI Asset, but an assessor unfamiliar with the equipment may still push for full Level 2 treatment until the justification is well documented. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run the two diagnostic questions in front of the client the first time a vendor pitches a control, so the client learns to ask the question themselves before the next pitch arrives. Put every "over-engineering" verdict in writing, because the client will be asked to defend the decision not to spend, not just the decisions to spend. **OSC seat**: when your own IT staff or an outside vendor proposes something expensive, ask them directly which assessment objective it satisfies. If the honest answer is "none, but it's good practice," that is a discretionary decision you get to make on purpose, not a requirement you have to accept.

## Sources

- CMMC Level 2 Assessment Guide, DoD CIO, for the assessment objectives cited per requirement: https://dodcio.defense.gov/CMMC/Resources-Documentation/
- NIST SP 800-171A, assessment objectives: https://csrc.nist.gov/pubs/sp/800/171/a/final
- 32 CFR 170.19, Specialized Asset category and scoping treatment: https://www.ecfr.gov/current/title-32/section-170.19
- Unified Scoping Guide, ComplianceForge, on the distinction between minimum compliance requirements and discretionary security requirements: https://complianceforge.com/
- Practitioner consensus, unattributed, backs the named findings table in step 4, the CNC mis-scoping pattern in step 5, and the three spend-anyway items in step 6.
