---
name: cui-determination-workflow
description: Determine whether a piece of information is Controlled Unclassified Information (CUI), using an ownership-first ruleset. Checks ownership, then contract origin, then controlling authority, in that order, and tests a document the company created from CUI on its content, never its ancestry. Applies the Copy A / Copy B mechanic, reads the contract's clause family, treats the CUI Registry as an eligibility list rather than an automatic-status list, and pushes unclear markings upstream in writing. Use whenever the operator or another skill asks "is this CUI?" about a document, a data field, or a whole data type.
vault_sources:
  - "How to Identify CUI"
  - "Practitioner insights A"
  - "Practitioner insights B"
  - "Controlled Unclassified Information"
  - "How CUI Flows Through a Contractor"
  - "CUI and Supply Chain Position"
  - "Data Rights Assertions"
  - "Reverse SCG Technique"
  - "Controlled Technical Information"
public_sources:
  - "DoD CUI Program FAQ, Use of Distribution Statements: https://www.dodcui.mil/Frequently-Asked-Questions/Use-of-Distribution-Statements/"
  - "DoDI 5230.24, Distribution Statements on DoD Technical Information, January 10, 2023: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf"
  - "32 CFR 2002.14 (safeguarding; (h)(2) NIST SP 800-171 for non-Federal systems): https://www.ecfr.gov/current/title-32/section-2002.14"
  - "32 CFR 2002.20 (marking): https://www.ecfr.gov/current/title-32/section-2002.20"
  - "32 CFR 170.4 (Security Protection Data definition): https://www.ecfr.gov/current/title-32/section-170.4"
  - "CUI Registry, National Archives, mirrored at dodcui.mil: https://www.dodcui.mil/CUI-Categories-and-Abbreviations/"
  - "32 CFR Part 2002 (CUI program): https://www.ecfr.gov/current/title-32/part-2002"
  - "32 CFR 2002.4 (definitions: (h) CUI, (ee) misuse, (pp) re-use): https://www.ecfr.gov/current/title-32/section-2002.4"
  - "32 CFR 2002.50 (challenges to a designation): https://www.ecfr.gov/current/title-32/section-2002.50"
  - "81 FR 63324, CUI final rule, preamble at 63334: https://www.federalregister.gov/documents/2016/09/14/2016-21665/controlled-unclassified-information"
  - "DoDI 5200.48, para 3.6.a: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/520048p.PDF"
  - "DoD Cybersecurity FAQs on DFARS Subpart 204.73, A32: https://dodprocurementtoolbox.com/uploads/Cybersecurity_FAQ_update_12_19_22_ba047be683.pdf"
  - "DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012"
  - "DFARS 252.227-7013, Rights in Technical Data: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.227-7013"
  - "CUI Basic vs CUI Specified, Summit 7: https://www.youtube.com/watch?v=5_AaOcYD-9w"
  - "How To Know If You Have CUI, a talk by Ryan Bonner at CS2, hosted by Summit 7: https://www.youtube.com/watch?v=IEy-TkmKMt8"
---

# CUI determination workflow

This skill answers one question: is this specific piece of information CUI, right now, for this company? It is the only skill in this repo that answers it; every other CUI skill sends its items here for the status. It runs a fixed order of tests so the operator never starts by staring at the content and guessing. It does not decide markings on a document you already know is CUI (call `cui-marking-check`), it does not resolve export-control status on its own (call `export-control-overlay` when ITAR or EAR is in play), and it does not walk the set of documents a company creates from CUI it received (call `cui-re-use-triage`, which gathers the facts for each document and sends it back here).

## The tree

Who owns the data comes first. This is the order the method below runs in, drawn as a tree; the picture is `docs/diagrams/cui-determination.drawio.png`. Each branch points to the step that holds the rule.

```
Who owns the data?                                        (step 1)
├─ We do: we created it and kept it
│    → Our own. Not CUI to us. Proprietary (own).
│      Any part that copies CUI we received goes down the government
│      branch as received content; the rest stays ours.  (step 1, re-use)
├─ A third party: commercial, not for the government
│    → Not CUI. Proprietary (third-party).
└─ The government: from DoD or an agency, directly or via a prime,
   or a deliverable we owe them                           (steps 2 to 4)
     Does a CUI Registry authority apply to it?           (steps 5 and 6)
     ├─ No  → Not CUI. FCI.                               (step 11)
     └─ Yes → Is it marked or identified with its CUI category?  (step 7)
              ├─ Yes → CUI, with its Registry category.
              └─ No, or unclear → Potentially CUI, notice sent.  (steps 8 and 10)

Every branch: export control is its own label (export-control-overlay),
and every item gets its data categories (step 12).
```

## Inputs

- The information in question: a document, a data field, a spreadsheet column, or a whole category the operator wants to know about.
- Who created it and who has kept it: the company, the government, or both.
- The contract or agreement it relates to, if any, and its clause list.
- Any markings already on it: banners, distribution statements, proprietary legends.
- The engagement repo files: `CONTEXT.md` for prior CUI determinations already recorded as terms, and `scope/cui-determinations.md` if it exists.

## Method

Run the three tests in this order. Do not start with the fourth test (what the data says) until the first three are settled, because content-first reasoning is exactly the reflex this workflow exists to stop.

1. **Test ownership first.** Ask: did the company create this, and does the company still hold it in its own systems? If yes, it is not CUI to the company, even if a law or regulation (ITAR or EAR, for example) still reaches it for other reasons. If the company does not own it, or no longer holds the only copy, move to the next test. Ownership is the gate every other test sits behind: evaluating a document's subject matter before checking who owns it puts the operator too far down the sequence to reach a defensible answer.

   **A document the company created while using CUI it received gets the re-use test here.** Re-use is "incorporating, restating, or paraphrasing information from its originally designated form into a newly created document" (32 CFR 2002.4(pp)), and it is a form of handling (2002.4(aa)). The test is on content, never ancestry: a derived document is CUI "because it contains controlled information, not simply because it is derived from a document that contains CUI", and one built only from a source's non-CUI portions is not CUI on that account (81 FR 63324, 63334). So split the document. The CUI content it re-uses (a copied dimension, a restated requirement, a paraphrased passage) stays CUI, the source agency is still its designator, and the document carrying it is CUI. What the company adds of its own (its method, its toolpaths, its routing) passes test 1 and is not CUI to the company. "It came from a CUI drawing" is never a reason on its own. `cui-re-use-triage` gathers the facts for this test document by document.

2. **Apply the Copy A / Copy B mechanic.** The same information can sit in two places with two different statuses. Copy A is the version the company keeps in its own systems: not CUI, even where a controlling authority applies to it, because the company both made it and possesses it. Copy B is the version delivered to the government: once the government possesses it, its status converts, typically to Controlled Technical Information (CTI), export-controlled material, or proprietary information belonging to the company (marked PROPIN) on the government's side. A bid package is the clean example: the pricing data stays the company's working copy while the delivered copy becomes CUI in the government's hands. This mechanic is why "is this CUI" needs a "to whom, and which copy" qualifier before it can be answered.

3. **Check whether it was created inside a contract, specifically for the government.** Work that is directly described in the contract's statement of work, performance work statement, or equivalent is in scope for this test. Work that is merely incidental to performing the contract, the kind of activity a company would document or track anyway, is not "specifically for" the government even if the government benefits from it. The distinction matters because only work created specifically for the government, under an agreement that assigns ownership to the government, becomes CUI-eligible on delivery.

4. **Read the contract's clause family to settle ownership.** Two clause families produce opposite outcomes:

   | Clause family | What it does | Effect |
   |---|---|---|
   | Data-rights clauses (DFARS 252.227-7013, 252.227-7014) | Grants the government a license (unlimited, government purpose, or limited rights) to use delivered data | Company keeps ownership; its retained copy stays proprietary, not CUI to the company |
   | Special-works / become-property clauses (DFARS 252.227-7020, DFARS 252.227-7023, FAR 52.227-17) | Transfers ownership of a deliverable first created and required to be delivered under the contract | Government owns the work; the delivered item is CUI-eligible |

   Read the actual clause numbers in the contract. Do not accept a prime's or a customer's verbal assurance about which family applies; ask for the clause citation. Recent contract-dispute rulings back the default assumption that a contractor keeps ownership of its technical data unless a clause says otherwise, which means the government asking for data rights is itself evidence that the contractor started out owning the data.

5. **Confirm a law, regulation, or government-wide policy actually controls it, independently of the first three tests.** Ownership and contract origin decide whether the information is CUI-eligible. A controlling authority, a specific entry in the CUI Registry with a named legal basis, decides whether it actually is CUI. Run this test on its own; do not let a "yes" on ownership or contract origin substitute for finding the authority, and do not let a scary-sounding category substitute for it either. If no authority actually reaches the data, it is not CUI, full stop, regardless of how the first three tests came out.

6. **Read the CUI Registry as an eligibility list, not an automatic-status list.** The Registry enumerates categories of information that are eligible to become CUI when the other tests are met; it is not a checklist where matching a category description makes something CUI automatically. Read the authorities cited at the bottom of a Registry category page, the actual law, regulation, or policy named there, rather than stopping at the plain-language description at the top. A keyword match to a category title (a report that mentions "vulnerability," for example) does not by itself put the data under that category's authority.

7. **Reject two common but wrong shortcuts.**
   - *A distribution statement is a clue, never the determination.* DoD says so directly: "The application of a distribution statement does not automatically mean the document is CUI" (DoD CUI Program FAQ, Use of Distribution Statements), and DoDI 5230.24 puts statements on classified, CUI, and uncontrolled technical documents alike. Read the markings in this order:
     1. A CUI designation indicator naming the category is the strongest evidence.
     2. Next, the defense category written into the statement. DoDI 5230.24 requires a statement B to E to name one (para 4.1.c(2)), and it says "CTI is a category of CUI" (para 4.3.a). A statement whose category reads "Controlled Technical Information" is the controlling DoD office saying the information is CTI, even if the banner is missing; handle it as CUI and ask for the marking to be fixed.
     3. Any other category (for example, critical technology or proprietary business information) is not a CUI determination. Look it up in `reference/dodi-5230-24-defense-categories.md`, which gives each category's Registry category, its authority, and the test for whether that authority reaches the content. Apply the test, then confirm with the source.
     4. No statement and no banner, from an originator who marks correctly, means not CTI and not Export Controlled, because both categories require Distribution Statement B through F. That rests on an assumption, and "the lack of a CUI marking on information that qualifies as CUI does not exempt the authorized holder from abiding by applicable handling requirements" (32 CFR 2002.20(a)(7)). Turn the assumption into evidence: check that the contract carries no DFARS 252.204-7012 or 252.204-7021, and get the source's "not CUI" in writing.
   - *DFARS 252.204-7012 reaches more than CTI, and only DoD.* Covered defense information is "unclassified controlled technical information or other information, as described in the ... CUI Registry", provided by or for DoD or developed in support of the contract, so Export Controlled CUI under a DoD contract is covered too. The second prong, "developed ... in support of the performance of the contract", is a link to the contract, not a net: the information must still be CTI or a Registry category, and DoD's FAQ says the phrase "does NOT mean that all information used by the contractor to support contract performance ... is considered to be covered defense information" (DoD Cybersecurity FAQs, A32). The clause is DoD's alone. Data under a NASA or other civilian agency contract is not CTI and brings no CMMC requirement; it can still be that agency's CUI, protected under NIST SP 800-171 through the agency's contract terms (32 CFR 2002.14(h)(2)). Which contract the work is performed under decides it, not which agency the data came from.
   - *Aggregation does not concentrate sensitivity.* A long list of otherwise-uncontrolled items, such as thousands of ordinary part numbers, stays uncontrolled when assembled into one list. Volume is not a CUI trigger by itself; each item still needs its own controlling authority.

8. **When a marking is unclear, decide on the evidence, then notify the source in writing.** The holder's duty is to check, not to designate. DoDI 5200.48 para 3.6.a makes the authorized holder responsible for determining, at the time of creation, whether information in a new document falls into a CUI category, so a company that re-uses CUI content and leaves the result unmarked has failed that duty. The same rule runs the other way: the company is not the designating agency, and marking its own work as CUI because of where it came from is a determination it has no basis for. 32 CFR 2002.4(ee) counts "designating or marking information as CUI when it does not qualify as CUI" as misuse, and overmarking pulls every asset that stores the document into scope. Only the designating agency designates. That does not mean the holder waits for it. When a document arrives marked ambiguously, or unmarked but suspiciously formatted, make the call from the evidence (its markings, the contract clauses, the tests above), write the reasoning down, and send the source a notice: the status the company will apply to each item, the proposed CUI category where a marking is incomplete, and the reasoning. The regulation's verb is notify, not ask: a holder who believes a designation is improper, or that it has received unmarked CUI, "should notify the disseminating agency", and keeps safeguarding the item meanwhile (32 CFR 2002.50(a), (d)). Send a notice, not an open question. Practitioner consensus is that an open question invites the lazy answer, "treat it all as CUI", with no category or authority behind it, and the holder then has to live with it. Where a clean file with the markings removed would settle the doubt, request one.

   The notice proposes a definite status for every item, including the doubtful ones. While it is open, record a doubtful item as "potentially CUI, notice sent" and safeguard it as CUI. Silence after a reasonable window accepts the notice, and the proposed status becomes the record; a reply that corrects it with a category and authority replaces it. Keep the notice, the reasoning, and any reply, or the silence, as the record of a good-faith determination.

9. **Escalate the determination out of IT.** This is a cross-functional call that belongs to sales, contracts, program management, engineering, and trade compliance, in roughly that order as a deal moves from quote to award to delivery, and it reaches IT last, only after the company knows what data exists and who is allowed to touch it. Do not let an IT department decide CUI status on its own, and do not accept a Certified Third-Party Assessment Organization's opinion on CUI status either; determining CUI status is outside an assessor's role.

10. **When a prime or agency will not provide guidance, use the reverse-guidance technique.** Build an index of everything received and everything generated under the contract. Propose a status and, where applicable, a category and dissemination control for each item. Send the index to the customer as a value-added service. It is a notice of what the company holds and how it will handle each item, not a question; the customer can correct anything it disagrees with. A sub asking a prime's program office for guidance usually gets no answer, or a blanket one, which is why the index informs rather than asks (How To Know If You Have CUI, from 40:40: https://www.youtube.com/watch?v=IEy-TkmKMt8). Treat silence, after a reasonable window, as acceptance of the proposed markings, and keep the index and the transmittal as the paper trail for the determination.

   **A subcontractor that cannot see above its prime starts here.** A sub usually cannot read the prime contract, its funding, or its data-rights clauses, so steps 1 to 4 have gaps it cannot fill alone. The regulation expects that: DFARS 252.204-7012(m)(1) makes the prime "determine if the information required for subcontractor performance retains its identity as covered defense information". Work from what the prime actually sent and wrote:
   - **A CMMC Level 2 requirement in the purchase order is a clue, not a label.** It says the prime thinks CUI may flow. It designates nothing, and it does not make every document received CUI.
   - **Read the evidence you can see:** the markings on each document, the clauses in the purchase order (7012, 7021, 252.225-7048), and what the prime says in writing.
   - **Send the index above**, with a proposed status for each item received. Give every item a definite proposed status. While the notice is open, record an item with a real reason for doubt, such as an export warning or a DoD distribution statement, as "potentially CUI, notice sent", and protect it (step 8). Silence accepts the proposed statuses as written. Record the rest with the reason they are not CUI.
   - **Nothing is CUI by default,** on either side: not because the purchase order asks for Level 2, and not "not CUI" because nobody marked it.
   - **Ask for less where you can.** A cleaned drawing, a performance specification, or only the sheets the work needs (step 8's request for a clean file). What the sub never receives never has to be decided.

   Where the evidence does not settle it, `enclave-or-enterprise-decision` gives the design that removes the need to decide at the inbox: apply NIST SP 800-171 to all controlled customer technical data, and keep each item's own label.

11. **When the answer is "not CUI", say what it is instead.** A document that fails every test above, but exists because of a federal contract, is **Federal Contract Information**: information not intended for public release, provided by or generated for the Government under a contract to develop or deliver a product or service. Quotes, purchase orders, clause pages, schedules, and delivery paperwork are the usual examples. FCI is not a lesser kind of CUI, it is a different category with its own floor: the fifteen basic safeguarding requirements in FAR 52.204-21, which are what Level 1 assesses. Recording a document as FCI rather than leaving it unlabelled is what stops it being re-argued as a possible CUI item every quarter, and it is what tells the scoping work that the asset holding it is still in a boundary, just a different one.

12. **Label every item with its data categories, including the items that are not CUI.** The determination answers one question, whether the item is CUI. The data categories answer a wider one, what the item is and why it needs protecting. Record every category that applies, from the set in `CONTEXT.md`: CUI (with its Registry category), FCI, Export-controlled (ITAR or EAR), Proprietary (own), Proprietary (third-party), PII, Security Protection Data, and Public. They overlap, and the overlaps are the point:
    - **A design the company owns outright is Proprietary (own), and it can be Export-controlled at the same time.** Test 1 makes it not CUI to the company. It does nothing for ITAR or EAR, so run `export-control-overlay` on it anyway. In the defense industrial base this is common, not an edge case: the shop's own fixture design for an ITAR part, its process know-how on a controlled item, its own engineering on a defense article.
    - **A customer's drawing can be CUI, Export-controlled, and Proprietary (third-party) at once.** The proprietary legend says who owns the data. It does not decide CUI status, and it survives even if the CUI status is later withdrawn, because the NDA or license behind it is a separate obligation.
    - **A quote is FCI and Proprietary (own).** The pricing belongs to the company whatever the contract status.
    - **PII the company holds about its own staff is not CUI**, for the same ownership reason as test 1. PII the Government provides under the contract can be CUI (Privacy), and then it is labeled CUI.
    - **Security Protection Data** is logs, alerts, configurations, and vulnerability data about the scope's security (32 CFR 170.4). It decides how SPAs and ESPs are handled, so label it where it flows to a provider.
    - **Public** means released without restriction, such as a catalog sheet or a Distribution Statement A document. It cannot be combined with CUI or with either Proprietary label.

    Only CUI and FCI set the assessment scope. The other categories add no asset to scope, and this workflow must not let them creep in as a reason to over-scope. They are recorded because "not CUI" is not "not sensitive": they tell the company where its own IP, its customers' IP, and its people's data sit, and which obligation (trade secret, NDA, privacy law, export regulations) protects each one.

## Output

Write one entry per item determined, appended to `scope/cui-determinations.md`:

```markdown
## <item or document description>

- Date: <date>
- Contract or agreement: <id, or "none">
- Ownership test: <company-owned / government-owned / unclear>
- Copy: <Copy A, retained / Copy B, delivered / both>
- Clause family: <data-rights 252.227-7013/-7014 / special-works 252.227-7020/-7023 / FAR 52.227-17 / not present>
- "Specifically for the government" test: <yes / incidental / unclear>
- Controlling authority: <CUI Registry category and citation, or "none found">
- Determination: <CUI / FCI / not CUI and not FCI / potentially CUI, notice sent>
- Data categories: <every one that applies: CUI (<Registry category>) / FCI / Export-controlled (ITAR or EAR) / Proprietary (own) / Proprietary (third-party, owner) / PII / Security Protection Data / Public>
- Action taken: <notice sent (date, to whom, window), reverse-guidance index sent, clean file requested, marking accepted as-is>
- Open items: <anything unresolved>
```

Record any determination that changes a term's meaning, or sets a precedent the engagement will lean on again, as an entry in `CONTEXT.md` through the `domain-modeling` skill, so the glossary stays the single source of truth for what "CUI" means on this engagement. An unresolved determination goes on the open items list, never into a conformity statement as though it were settled.

## Where practitioners disagree

- Whether a company that receives CUI on paper only, with no contract clause spelling out CUI handling explicitly, has to treat a document as CUI before the customer confirms it. Some hold that a document should be handled according to whatever it was marked when it arrived, paired with a good-faith notice to the customer and a chance for them to correct it. Others hold that nothing is CUI until the customer expressly says so in writing, and treating an unconfirmed marking as CUI overstates scope. The outcome depends on the assessor.
- **Whether to ask the source or to notify it.** One position: always ask the customer what category and controls apply, because the customer is the one who should know. The other, which this workflow follows: decide on the evidence and notify, because an open question to a prime or a program office usually gets no answer or a blanket "treat it all as CUI", and a notice puts the company's reasoning on record either way. The outcome depends on the customer more than the assessor.
- Whether "sensitive end-use context" shared to support a quote, before any contract exists, is already inside the CUI determination process or is still a pre-contract sales conversation with no CUI implications yet. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run this workflow with the client's contracts and program staff in the room, not alone; the ownership and clause-family tests require someone who can read the actual contract, and IT staff usually cannot answer them. **OSC seat**: if nobody in the company has read the data-rights and special-works clauses in the contract before, start there before touching test 5; the clause family alone resolves most of the easy cases.

## Sources

- DoD CUI Program FAQ, Use of Distribution Statements: https://www.dodcui.mil/Frequently-Asked-Questions/Use-of-Distribution-Statements/ (mirrored at `reference/cui-registry/Frequently-Asked-Questions--Use-of-Distribution-Statements.md`).
- DoDI 5230.24, Distribution Statements on DoD Technical Information, January 10, 2023: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf (mirrored at `reference/dod-issuances/dodi-5230-24.md`).
- `reference/dodi-5230-24-defense-categories.md`: the fourteen defense categories in para 4.3, the authority behind each, and the test for each (step 7).
- 32 CFR 2002.14 (safeguarding; (h)(2) NIST SP 800-171 for non-Federal systems): https://www.ecfr.gov/current/title-32/section-2002.14.
- 32 CFR 2002.20 (marking): https://www.ecfr.gov/current/title-32/section-2002.20.
- 32 CFR 170.4 (Security Protection Data definition, used in step 12): https://www.ecfr.gov/current/title-32/section-170.4.
- CUI Registry, National Archives, mirrored at dodcui.mil: https://www.dodcui.mil/CUI-Categories-and-Abbreviations/ (eligibility categories and authorities).
- 32 CFR Part 2002: https://www.ecfr.gov/current/title-32/part-2002 (the CUI program's reach through contracts and agreements).
- 32 CFR 2002.4: https://www.ecfr.gov/current/title-32/section-2002.4 ((aa) and (pp) re-use as handling, for the re-use test in step 1; (ee) overmarking as misuse, step 8).
- 81 FR 63324, the CUI final rule, preamble at 63334: https://www.federalregister.gov/documents/2016/09/14/2016-21665/controlled-unclassified-information (content, not ancestry, for the re-use test in step 1; quoted in `reference/authorities.md`).
- DoDI 5200.48, para 3.6.a: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/520048p.PDF (mirrored at `reference/dod-issuances/dodi-5200-48.md`; the holder checks a new document at creation, step 8).
- DoD Cybersecurity FAQs on DFARS Subpart 204.73, A32: https://dodprocurementtoolbox.com/uploads/Cybersecurity_FAQ_update_12_19_22_ba047be683.pdf (mirrored at `reference/dod-issuances/dod-cybersecurity-faq-covered-defense-information.md`; DFARS 252.204-7012 prong (2) as a contract link, step 7).
- 32 CFR 2002.50: https://www.ecfr.gov/current/title-32/section-2002.50 (the written route for an unclear item, step 8).
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012 (the clause that pulls Controlled Technical Information into a defense contract).
- DFARS 252.227-7013, Rights in Technical Data: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.227-7013 (the data-rights clause family and its license categories).
- CUI Basic vs CUI Specified, Summit 7: https://www.youtube.com/watch?v=5_AaOcYD-9w (the baseline-versus-added-rules distinction referenced in test 5).
- How To Know If You Have CUI, a talk by Ryan Bonner at CS2, hosted by Summit 7: https://www.youtube.com/watch?v=IEy-TkmKMt8 (the five-step read-the-contract-first method behind this workflow, and the reverse-guidance technique in step 10, including its notify-not-ask framing).
- Practitioner consensus, unattributed, backs the ownership-first ordering in steps 1 through 3, the Copy A / Copy B mechanic in step 2, the eligibility-not-automatic reading of the Registry in step 6, both rejected shortcuts in step 7, and the escalate-out-of-IT rule in step 9.
