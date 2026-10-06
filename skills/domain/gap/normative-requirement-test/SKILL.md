---
name: normative-requirement-test
description: Decide whether a cited passage of the CMMC Level 2 Assessment Guide can actually fail an assessment, by sorting it into the two normative sections or the three informative ones. Use whenever a vendor, consultant, assessor, or forum thread treats Discussion text, an Example, or a Potential Assessment Consideration as if it were a requirement.
vault_sources:
  - "Normative vs Informative Sections of the CMMC Assessment Guide"
  - "3.5.3"
  - "3.13.11"
  - "3.5.10"
  - "3.3.9"
  - "3.3.7"
  - "3.6.1"
  - "raw/IA.L2-3.5.3.md"
  - "raw/SC.L2-3.13.11.md"
public_sources:
  - "NIST SP 800-171 Rev 2: https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final"
  - "NIST SP 800-171A: https://csrc.nist.gov/pubs/sp/800/171/a/final"
  - "CMMC Level 2 Assessment Guide, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "Summit 7, \"75% of the CMMC Assessment Guide Isn't Requirements\": https://www.youtube.com/watch?v=CgojtXRh9rM"
---

# Normative requirement test

This skill answers one question: can the passage someone just cited actually be the basis of a finding? It sorts any quoted line from the CMMC Level 2 Assessment Guide into normative or informative, and it gives you the question to ask back when the answer is informative. It refuses to tell you whether a specific implementation is sufficient (call the Skill tool with `control-evidence-lookup` for that) and it refuses to override an assessment objective that genuinely does require the thing being argued about.

## Inputs

- The exact passage being cited: a Practice Statement, an Assessment Objective, a line from Potential Assessment Methods and Objects, Discussion, Further Discussion, an Example, or a Potential Assessment Consideration (PAC).
- The requirement id the passage sits under (`3.x.y`).
- Optionally, the requirement's conformity statements in the record, `ssp/ssp.json`, if you are checking whether one over-claims by citing Discussion text instead of an objective. Call the Skill tool with `scribe` and ask it to show the record for the requirement. Never read `view/` instead; it is generated for people and can be stale.

## Method

1. **Classify the section the passage came from.** Every practice in the Assessment Guide has the same five sections, and only two of them can fail you.

   | Section | Authored by | Binding on a finding? |
   |---|---|---|
   | Practice Statement | NIST SP 800-171 Rev 2 | Yes, this is the requirement |
   | Assessment Objectives | NIST SP 800-171A | Yes, this is what gets verified |
   | Potential Assessment Methods and Objects | DoD CIO | No |
   | Discussion | NIST SP 800-171 Rev 2 | No |
   | Further Discussion, Example, Potential Assessment Considerations | DoD CIO | No |

   NIST's own introductory language to SP 800-171 Rev 2 says plainly that its Discussion paragraphs explain a requirement rather than govern it, and warns readers against reading them as broadening what a requirement covers or as prescribing a particular product or design. Only the 110 Practice Statements and the 320 lettered Assessment Objectives make up the set an assessor may cite in a finding. The remaining prose, which is most of the document by volume, exists to help a reader understand the requirement, not to add to it.

2. **Ask the test question.** For any cited passage, ask yourself plainly: does an assessor have to check this, or is somebody just explaining the requirement to you? Anything outside the Practice Statement and its lettered objectives cannot carry a finding by itself, however useful it is for understanding the requirement.

3. **Flag the DoD-added sections separately.** The Potential Assessment Methods and Objects, the Example, and the Potential Assessment Considerations were written by the DoD CIO, not NIST. Some assessors treat them as authoritative because they sit inside the official Guide; others treat them as unreliable precisely because NIST did not write them. A documented case: one requirement's Example uses "the same authoritative time server" (singular) while its Potential Assessment Considerations say "NTP Servers" (plural), an inconsistency inside the Guide itself that a normative document would not contain. Do not resolve this disagreement; write it down and move to the next step.

4. **Deploy the standing counter-question.** Whenever someone argues that a Discussion paragraph, a Further Discussion note, an Example, or a PAC line is mandatory, put the burden back on them: which lettered objective in 800-171A actually calls for this? If all they can produce is more Discussion text, a blanket claim that a Security Protection Asset must satisfy everything, or a neighboring requirement's own Discussion, the test has not been met.

5. **Run the worked example: does an MFA authenticator need FIPS validation?**

   - **Practice statement, requirement 3.5.3**, multifactor authentication: it calls for a second factor on local and network access to privileged accounts, and on network access to everyone else. Nothing in that sentence mentions cryptographic module validation.
   - **Its four lettered objectives**: they walk through identifying privileged accounts and then requiring the second factor across the three access paths (local privileged, network privileged, network everyone else). Again, no module-validation language anywhere.
   - **Its Discussion paragraph**: it points a reader toward NIST SP 800-63-3 for background on digital identity. Pointing toward guidance is not the same as binding a reader to a specific sub-document like 800-63B, and the paragraph sits in the informative half of the practice regardless.
   - **What follows**: the 110 requirements and 320 objectives contain exactly one place that ever demands a validated cryptographic module, and it belongs to a different requirement, 3.13.11, gated by its own condition: only when the module is doing the work of keeping CUI's contents secret. Signing a login challenge is not that job. Whatever secures the session that login unlocks, commonly a TLS channel riding on a validated operating-system module, is where that gate applies instead.

6. **Rebut the three standard counter-arguments**, all of which fail the normative test:

   | Counter-argument | Why it fails |
   |---|---|
   | "NIST SP 800-63B requires FIPS-validated authenticators" | 800-63B is reachable only through 3.5.3's Discussion section, which cites the parent document 800-63-3 as "guidance." Discussion cannot extend a requirement. |
   | "The token is a Security Protection Asset, and SPAs must meet every requirement" | True that SPAs are assessed against everything relevant to their capability. False that this erases 3.13.11's own qualifying clause, which only reaches a module doing CUI-confidentiality work. Signing a login challenge authenticates a person; it never carries CUI content. |
   | "3.1.13 requires cryptographic mechanisms for remote access, and that includes the authenticator" | 3.1.13's objectives target the confidentiality of the remote access session itself, which is the job of the VPN or TLS transport. An authenticator gates entry to the session; it does not establish, encrypt, or carry it. The FIPS obligation lands on the transport. |

7. **Generalize past this one example.** The same five-section sort applies to any requirement. Two more documented cases: a requirement whose Discussion allows a mathematically minimal "subset" of privileged users to manage audit logging, where the objective only requires the subset to be defined, not sized a particular way; and a requirement where an assessor confirmed that continuous, 24-hour monitoring is not required by the objectives even though Further Discussion language about "timely" response invites that reading. In both cases the objective text, not the surrounding prose, is what a finding can rest on.

8. **Write the evidence mapping to objectives, not to Discussion bullets.** When building or reviewing an SSP conformity statement, map each sentence to the lettered objective it satisfies. A statement that only echoes an Example or a PAC, with no objective it maps to, is padding: it will not help you pass and it may have cost money to implement.

## Output

Produce a short worksheet, either inline in your response or added to the engagement repo's open items list, `scope/open-items.md`, as a line naming the objective in `3.5.3[a]` form, if the passage came from a live SSP dispute.

```markdown
# Normative test: <requirement id>, <one-line description of the cited passage>

Passage cited: "<the quoted text>"
Section: Practice Statement / Assessment Objective / Potential Assessment Methods and Objects / Discussion / Further Discussion / Example / Potential Assessment Consideration
Authored by: NIST SP 800-171 Rev 2 / NIST SP 800-171A / DoD CIO
Status: Normative / Informative

Verdict: <can fail you / cannot on its own fail you>
Counter-question asked, if informative: which lettered 800-171A objective actually requires this?
Objective actually cited in response, if any: <letter and text, or "none produced">
```

## Where practitioners disagree

- **Whether the DoD-added Examples and Potential Assessment Considerations carry weight.** Some assessors read them as authoritative because they are printed inside the official Assessment Guide. Others read them as unreliable precisely because NIST, the author of the normative sections, did not write them, and the Guide's own introduction disclaims extending scope. The outcome depends on the assessor.
- **Whether a Security Protection Asset's general obligation to meet every relevant requirement overrides a requirement's own conditional language**, as in the 3.13.11 "when used to protect the confidentiality of CUI" clause applied to an MFA token. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run this test out loud the first time a client's IT vendor or a well-meaning forum post pushes an unnecessary purchase, and log the worksheet in the open items list so the decision survives staff turnover. **OSC seat**: when a vendor tells you their product is "required for CMMC," ask them directly which assessment objective in 800-171A requires it. If they cite a Discussion section, a PAC, or "best practice," you are not obligated to buy it to pass.

## Sources

- NIST SP 800-171 Rev 2, Introduction and requirement 3.5.3: https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final
- NIST SP 800-171A, objectives for 3.5.3 and 3.13.11: https://csrc.nist.gov/pubs/sp/800/171/a/final
- CMMC Level 2 Assessment Guide, DoD CIO, IA.L2-3.5.3 and SC.L2-3.13.11: https://dodcio.defense.gov/CMMC/Resources-Documentation/
- Summit 7, public talk on how little of the Assessment Guide is enforceable: https://www.youtube.com/watch?v=CgojtXRh9rM
- Practitioner consensus, unattributed, backs the DoD-added-sections disagreement in step 3 and the "SPA must meet everything" rebuttal in step 6.
