---
name: export-control-overlay
description: Work out how ITAR and EAR sit on top of a CUI determination, catch the reflex that export-controlled data is automatically CUI, apply the deemed-export rule to foreign nationals and foreign-staffed service providers, and decide where classification authority actually sits. Use whenever technical data, a foreign national, an MSSP or EDR vendor, or a cloud region enters the conversation.
vault_sources:
  - "Export Controls and CUI"
  - "Practitioner insights A"
  - "Practitioner insights B"
  - "Controlled Technical Information"
  - "Marking CTI"
  - "Public panel analyzing a 2019 DDTC consent agreement involving an infrared-sensor manufacturer (FLIR), hosted by Summit 7: https://www.youtube.com/watch?v=qS44dOwoWUs"
  - "Public panel on practical ITAR compliance steps, hosted by Summit 7: https://www.youtube.com/watch?v=xhFX1eCHHSI"
  - "raw/dodcui--Export-Control--Export-Controlled.md"
public_sources:
  - "DoDI 5230.24, Distribution Statements on DoD Technical Information, January 10, 2023: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf"
  - "22 CFR 120.50 (export, including the deemed export at (a)(2)): https://www.ecfr.gov/current/title-22/section-120.50"
  - "22 CFR 120.56 (release definition): https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120/section-120.56"
  - "22 CFR Part 120 (ITAR definitions): https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120"
  - "22 CFR 120.11 (ITAR order of review): https://www.ecfr.gov/current/title-22/section-120.11"
  - "22 CFR 120.33 (ITAR technical data): https://www.ecfr.gov/current/title-22/section-120.33"
  - "15 CFR 772.1 (EAR definition of technology): https://www.ecfr.gov/current/title-15/section-772.1"
  - "DFARS 252.225-7048 (export-controlled items clause): https://www.ecfr.gov/current/title-48/section-252.225-7048"
  - "15 CFR 734.3 (items subject and not subject to the EAR, EAR99): https://www.ecfr.gov/current/title-15/section-734.3"
  - "15 CFR Part 774, Supplement No. 4 (Commerce Control List order of review): https://www.ecfr.gov/current/title-15/part-774/appendix-Supplement%20No.%204%20to%20Part%20774"
  - "DoD CUI Export Controlled category page: https://www.dodcui.mil/Export-Control/Export-Controlled/"
  - "Public panel analyzing a 2019 DDTC consent agreement involving an infrared-sensor manufacturer (FLIR): https://www.youtube.com/watch?v=qS44dOwoWUs"
  - "Public panel on practical ITAR compliance steps for small and mid-size businesses: https://www.youtube.com/watch?v=xhFX1eCHHSI"
  - "32 CFR Part 2002 (CUI program): https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2002"
  - "22 CFR 120.54 (activities that are not exports; the encrypted-storage rule at (a)(5)): https://www.ecfr.gov/current/title-22/section-120.54"
  - "22 CFR 122.1 (registration, including manufacturers that do not export): https://www.ecfr.gov/current/title-22/section-122.1"
  - "22 CFR 122.5 (records of registrants): https://www.ecfr.gov/current/title-22/section-122.5"
  - "22 CFR 125.4 (exemptions; (b)(9) technical data taken abroad by travelling employees): https://www.ecfr.gov/current/title-22/section-125.4"
  - "22 CFR 126.1 (proscribed countries): https://www.ecfr.gov/current/title-22/section-126.1"
  - "22 CFR 127.12 (voluntary disclosures): https://www.ecfr.gov/current/title-22/section-127.12"
  - "15 CFR 734.18 (activities that are not exports under the EAR; encrypted data at (a)(5)): https://www.ecfr.gov/current/title-15/section-734.18"
  - "15 CFR 740.9 (License Exception TMP; tools of trade and technology taken abroad): https://www.ecfr.gov/current/title-15/section-740.9"
  - "15 CFR 762.6 (EAR record retention): https://www.ecfr.gov/current/title-15/section-762.6"
  - "15 CFR 764.5 (voluntary self-disclosures to BIS): https://www.ecfr.gov/current/title-15/section-764.5"
  - "BIS, Export Compliance Guidelines: The Elements of an Effective Export Compliance Program: https://www.bis.gov/media/documents/export-compliance-guidelines"
---

# Export control overlay

This skill answers: does ITAR or EAR change the answer for this piece of technical data, this foreign national, this service provider, or this cloud region, and if so, what does the contractor actually have to do about it? It does not make a CUI determination on its own; call the Skill tool with `cui-marking-check` once the category and marking are settled, and route the underlying scoping question to `esp-and-msp-scoping` when a provider's placement in the architecture is the open question. It refuses to let IT or a program manager freelance a classification call that belongs to an attorney or an engineering review.

## Inputs

- A description of the technical data, item, or service in question, and whether it has a government contract attached.
- Who will touch it: US persons only, or one or more foreign nationals, and their role (SOC analyst, IT admin, visitor, MSP staff).
- The vendor or service provider's operating model: where its support and security staff sit, and whether it has remote-shell or admin-level access.
- The cloud region and hosting model in play, if any.
- If this overlay is being run against an existing scope: the assets and providers in the record, `ssp/ssp.json`, shown by calling the Skill tool with `scribe`, and `scope/external-systems.md`. Never read `view/` instead; it is generated for people and can be stale.

## Method

1. **Name the four regimes up front, out loud, before doing anything else.** CMMC is run by the CMMC PMO inside DoD. CUI is run by the Information Security Oversight Office inside the National Archives. ITAR is run by the Directorate of Defense Trade Controls inside the State Department. EAR is run by the Bureau of Industry and Security inside the Commerce Department. None of these four agencies merges its rules with another's, and none of them will reconcile a conflict for the contractor. The obligation to satisfy all four at once sits entirely with the contractor.

2. **Break the "export-controlled equals CUI" reflex.** An item can be regulated by ITAR or EAR and still not be CUI, and the reverse also happens. The proprietary carve-out that keeps a company's own IP from becoming CUI to that company does nothing for ITAR or EAR: a design a contractor owns outright can be ITAR-controlled technology and simultaneously not CUI, because ownership is a CUI test, not an export-control test. The moment a copy of that same design is delivered to the government, the delivered copy becomes CUI on possession, while the contractor's retained copy remains its own IP and stays export-controlled on its own terms. Do not let a "we own it, so it's not CUI" answer end the export-control question; ask it separately. Record both answers in the item's data categories in `scope/cui-determinations.md`: the owned design is Proprietary (own) and Export-controlled (ITAR or EAR), with no CUI label, and that pairing is the common case in the defense industrial base, not an exception.

   The reverse mistake is just as common: an export warning does not make data CTI. The two tests differ at every point:

   | | CTI (a DoD CUI category) | ITAR |
   |---|---|---|
   | Question | Does DoD control this technical information, through a controlling DoD office or the contract? | Is this technical data required for a USML defense article? |
   | Run by | DoD, through the contract (DFARS 252.204-7012, CMMC) | The State Department (22 CFR Parts 120 to 130) |
   | What it controls | Safeguarding: NIST SP 800-171, incident reporting, CMMC | Release to foreign persons: exports and deemed exports |
   | Does ownership matter | Yes. The company's own IP is not CUI to the company | No |

   CTI needs a DoD nexus: a controlling DoD office on the distribution statement (DoDI 5230.24), or data provided by or for DoD under a contract carrying DFARS 252.204-7012. A privately funded drawing from a commercial customer, marked only with an export warning, can be ITAR-controlled and not CUI at all. One clue about where a warning came from: the DoD warning text ends "Disseminate in accordance with provisions of DoD Directive 5230.25" (DoDI 5230.24, Figure 3), while a company's own notice usually cites the ITAR directly. That points toward DoD-sourced data; it does not prove it. Settle CUI status through `cui-determination-workflow`.

   The order of review in step 3 answers the export question only. It says nothing about whether the item is CUI; that determination runs on 32 CFR Part 2002 and the CUI Registry, through `cui-determination-workflow`.

3. **Determine whether the item is ITAR or EAR, never both, by working the order of review in the regulations' own sequence.** An item that is subject to the ITAR is not subject to the EAR (15 CFR 734.3(b)(1)(i)), so the ITAR question always comes first. Take the steps in this order and stop at the first one that places the item:
   1. **The US Munitions List, under 22 CFR 120.11.** Start from the item's general characteristics to find the USML category, then match it to a specific entry. An item is on the USML because it is enumerated in a category, or because it falls in a catch-all paragraph that uses "specially designed" as a control parameter. "Specially designed" is a defined term with release exclusions (22 CFR 120.11(b)(1) points to them), not a loose "built for defense." When an item fits more than one entry, the enumerated entry wins over the catch-all (22 CFR 120.11(b)(2)). A USML item stays ITAR-controlled after it is built into something that is not on the USML (22 CFR 120.11(c)). If the item is on the USML, it is ITAR and there is no need to review the Commerce Control List.
   2. **Whether the item is subject to the EAR at all, under 15 CFR 734.3.** Some information is outside the EAR entirely: published information, results of fundamental research, catalog course instruction, patent information, and non-proprietary system descriptions (15 CFR 734.3(b)(3)). Information that is not "technology" as 15 CFR 772.1 defines it is not subject to the EAR either (the note to 15 CFR 734.3(b)(3)); a purchase order that states stock size and quantity is the usual example. That result is "not subject to the EAR," which is a different answer from EAR99. Record which one applies.
   3. **The Commerce Control List, in the order Supplement No. 4 to 15 CFR Part 774 sets.** Find the CCL category (0 through 9) and the product group (A through E). Then check the "600 series" and 9x515 entries first, because they describe military items that were once on the USML and trump every other ECCN; check their "specially designed" catch-all paragraphs next; and only then work through the rest of the product group. A match gives the item an ECCN.
   4. **EAR99, under 15 CFR 734.3(c) and step 6 of Supplement No. 4.** An item that is subject to the EAR and matches no ECCN is designated EAR99. EAR99 is not "uncontrolled" or "commercial, no further action." The supplement says EAR99 items may still need a license when they go to a prohibited or restricted end user, end use, or destination, so the end-user and destination screening still has to run.

   **Technical data takes its status from the article.** The order of review is written for articles. A drawing is ITAR technical data because it is required to produce a defense article (22 CFR 120.33(a)(1)), and software directly related to a defense article is technical data too (22 CFR 120.33(a)(4)), which covers an NC program. Information in the public domain is excluded (22 CFR 120.33(b)). So classify the part first, then give the drawing, and every sketch, traveler, inspection report, and NC program that reproduces its geometry, the part's answer. A document that carries none of that geometry does not inherit it just because it belongs to the same job.

   **A build-to-print supplier gets the answer from the design authority.** A shop that makes a part to a customer's drawing usually cannot see the end item, and "specially designed" turns on it. Do not guess the end item. Ask the design authority in writing for the jurisdiction (USML category, or ECCN) of the part and its technical data, using the jurisdiction request under Output, and file the answer with the memo. The standard DoD export warning on a drawing names both the Arms Export Control Act and the Export Administration Act, and a DFARS 252.225-7048 clause covers both regimes, so neither one settles which regime applies. Until the answer arrives, handle the data as ITAR: ITAR handling meets anything a "600 series" answer would need, and the reverse is not true. Record the result as pending, not as ITAR.

   Once the data is ITAR, or handled as ITAR, where it will finally live is a separate question: call the Skill tool with `gcc-high-decision`. A provider whose support staff can reach the data is a release question under step 4, whatever its CMMC status. The ITAR gives no grace period while that decision is made, so "handle as ITAR" means these steps, starting now:
   1. **Stop new data.** Put no new data handled as ITAR into a tenant or service whose provider has not committed in writing to US-person-only access for its support and operations staff, unless the data is encrypted under step 4's encrypted-storage rule with keys the provider cannot use.
   2. **Find the data that is already there.** List every place it sits: tenant sites and libraries, mailboxes, OneDrive folders, endpoints, file servers and NAS shares, backups and backup media, removable media, and paper. Record each place in the memo.
   3. **Deal with data already stored with a provider that has no US-person commitment.** This does not wait for `gcc-high-decision`. The capability test in step 4 applies to data that is already stored, not only to new data. Move the data now to a location where only US persons can reach it, e.g., an on-premises share or a device outside the provider's reach, or protect it where it is with encryption that meets step 4's encrypted-storage rule, with keys the provider cannot use. `gcc-high-decision` then decides where the data ends up for good. It does not decide whether the data moves now.
   4. **Send the past exposure to the export attorney.** Whether the storage before the move was already a release is a question for step 12, not for this memo. Record the dates the data sat there.

   When another skill has already ruled a provider out for CUI (for example, a cloud service with no FedRAMP authorization), say in the export memo that it cannot be used in scope; do not write "hold pending answers."

   The hinge between steps 1 and 3 is usually whether the item was specifically designed to meet military-application performance thresholds enumerated on the Munitions List; something designed independently of a defense end item usually lands under EAR instead. The order of review gives the classification memo its structure and gives the consultant the questions to ask. It does not move the call itself out of step 9's hands. Only a small slice of a larger EAR dataset may cross into ITAR territory when it is adapted to hit ITAR-level specs, and that slice, not the whole dataset, is what needs ITAR handling. When the classification is unclear or the stakes are high, a commodity jurisdiction request to the State Department or a classification request to Commerce can settle it, though a request like that is realistically only worth the cost to an OEM or design authority, not a deep-tier supplier.

4. **Apply the deemed-export rule to any foreign person with access.** Releasing technical data to a foreign person in the United States is a deemed export (22 CFR 120.50(a)(2)), and 22 CFR 120.56 says what counts as a release. The regulation lists, as a release, "the use of access information to cause or enable a foreign person, including yourself, to access, view, or possess unencrypted technical data" (22 CFR 120.56(a)(3)), and it requires authorization "to provide access information to that foreign person, if that access information can cause or enable access, viewing, or possession of the unencrypted technical data" (22 CFR 120.56(b)). Passwords and decryption keys are the everyday examples. In the memo, quote the regulation for this rule rather than restating it. Handing a foreign national the credentials that reach a system holding ITAR technical data is a release, whether or not that person ever opens the file. This is a capability-based standard, not an alerts-based one: if access was conceptually possible, the exposure already happened.

   **Encryption decides whether stored data can be released at all.** The release rule above covers unencrypted technical data. 22 CFR 120.54(a)(5) says that sending, taking, or storing technical data is not an export when all of these hold:
   - The data is unclassified.
   - It is secured with end-to-end encryption.
   - The encryption uses cryptographic modules compliant with FIPS 140-2 or its successors, with key management that follows current NIST guidance, or gives at least the security strength of AES-128.
   - It is not sent to a person in, or stored in, a country listed in 22 CFR 126.1, and not sent from one.

   22 CFR 120.54(c) adds that the ability to reach data encrypted this way is not a release. The test turns on who holds the keys. End-to-end encryption, as 22 CFR 120.54(b) defines it, requires that "the means of decryption are not provided to any third party." If the provider holds the keys, or can use them, the data fails this test, so the provider's staff are back under the release rule. Encryption that the provider manages for the customer is the common example. The EAR has the same rule at 15 CFR 734.18(a)(5), with Country Group D:5 in place of the 126.1 list.

   Apply this to what the engagement actually finds, and record each one in the memo:
   - **Storage with no encryption at rest.** Examples are a laptop without BitLocker, and a NAS that encrypts SMB traffic but not the disks. The encrypted-storage rule does not cover it, so everyone who holds access information for it, or who can pick up the device, is a release question.
   - **Encryption from a module that is not FIPS-validated.** For the export test this is not the end of the question, because the ITAR text also accepts other means at least as strong as AES-128, and the EAR text accepts "other equally or more effective cryptographic means." Record the algorithm, the key length, and who holds the keys, and let the export attorney decide whether it qualifies. Validation does decide 3.13.11 for CUI; call the Skill tool with `fips-crypto-scoping` for that.
   - **Recovery keys and backup keys.** Whoever holds the BitLocker recovery keys, the backup encryption keys, or the NAS admin credentials holds "access information" under 22 CFR 120.56(b). If an MSP holds them, that MSP's staffing is a release question under this step and step 6. Record where each set of keys is kept and who can reach it.
   - **Lost or stolen devices.** A lost laptop whose data meets the encrypted-storage rule, with keys the finder cannot get, is not a release. A lost laptop without that encryption goes to step 12.

   This is the export test only. Whether the same encryption satisfies 3.13.11 for CUI is a separate question for the CUI side of the engagement.

5. **Cite the FLIR case for why "we didn't see anything in the logs" is not a defense.** In a public panel discussion analyzing a 2019 DDTC consent agreement involving an infrared-sensor manufacturer (FLIR), https://www.youtube.com/watch?v=qS44dOwoWUs, the underlying problem was not that a foreign national was confirmed to have opened ITAR-controlled files. It was that the company could not produce IT records proving that no unauthorized access had happened. Logging supports proving an individual violation after the fact; it does not substitute for a design that prevents the access from being possible in the first place.

6. **Kill the follow-the-sun managed detection and response pattern.** A security operations center staffed with foreign nationals who hold remote-shell access into hosts running an EDR agent is a live deemed-export violation the moment ITAR data sits in that environment, regardless of whether anyone on that team ever actually pulls a file. Two clean options close this gap:
   - Use a security operations center staffed only by US persons.
   - Use an endpoint detection tool with no remote-shell capability at all, so there is nothing for a foreign-staffed team to reach into even if a request comes through.

7. **Flip the map on access control.** Do not stop at checking whether a foreign national's assigned role looks low-risk. Check whether that person, in any role, can grant themselves broader access: a foreign national holding schema-admin or identity-provider-admin rights is already a problem, independent of what their day-to-day job title says they do.

8. **Cover visual, casual, and photographic access alongside data access.** A deemed export can happen through inspection, not just through a file transfer: letting a foreign visitor examine, handle, or study a controlled item is a different and higher-risk act than briskly walking that same visitor past it without stopping. A locked-down virtual desktop hosted in a US datacenter, with no local file transfer, no printing, and controls against someone photographing the screen, is a workable carve-out precisely because the data never crosses a border, even though the visitor is physically present. Marketing photography deserves the same scrutiny as a data export: a photo detailed enough that someone could reproduce the item's unique characteristics from it is itself technical data, and a marketing program needs a review step for exactly that reason.

9. **Route classification to an export attorney or a program-level engineering review, never to IT.** Nobody in the IT department is positioned to read a Munitions List entry or an Export Control Classification Number and make the call; that skill set belongs to trade compliance, contracts, or outside counsel. Once classification is settled, run the minimum program. For a contractor that does not itself export and did not design the controlled item, the minimum program has four parts.

   1. **DDTC registration, if it applies.** Under 22 CFR 122.1(a), anyone in the United States in the business of manufacturing defense articles must register with DDTC, and "a manufacturer who does not engage in exporting must nevertheless register." One occasion of manufacturing is enough. A shop that makes a part on the USML is therefore likely to need registration even though it ships only to a US prime. Ask the export attorney whether it applies, and record the answer. Do not let the client assume that "we don't export" ends the question.
   2. **The export compliance program (ECP).** This is the written program. It is also called an Export Control Plan, and the two names mean the same document. The Bureau of Industry and Security lists eight elements in its Export Compliance Guidelines. Written for a shop that does not export, they come to this:
      - Management commitment. A statement signed by the owner or president that the company follows the ITAR and the EAR, and that names the person responsible for export compliance.
      - Risk assessment. Where controlled data comes in, who touches it, which providers can reach it, and whether anyone travels with it.
      - Export authorization. The classification record for each item, the rule that no controlled data goes to a foreign person without a license or exemption, and who approves any exception.
      - Recordkeeping. The records listed in part 4 below.
      - Training. Who is trained, on what, and how often.
      - Audits. A periodic check that the program is followed.
      - Handling violations. The procedure in step 12.
      - Building and maintaining the program. Who owns it and when it is reviewed.
   3. **The Technology Control Plan (TCP).** This is the plan that keeps controlled technical data away from people who may not receive it. The ITAR mentions a TCP only in passing (22 CFR 126.13(c)). The BIS guidelines say what it contains, and they say a company that employs foreign nationals or meets them often should have one. Its parts are:
      - A physical security plan, including locked storage and how paper is destroyed.
      - An information security plan, including who can reach which folders and where the keys are held (step 4).
      - Personnel screening, meaning how the company confirms and records each person's US-person status before access.
      - Corporate commitment.
      - Training and awareness.
      - Self-evaluation.
   4. **Records.** Keep these:
      - The classification memo for each item, with the design authority's written answer attached.
      - The US-person status of each person with access, and the document that shows it.
      - A log of foreign-national visitors. The BIS guidelines list six fields: the visitor's name and nationality, the organization they represent, the date, the people visited, the purpose and the products discussed, and a summary of the visit.
      - Each provider's written US-person commitment.
      - Travel records under step 11.
      - Loss-of-control records and disclosure decisions under step 12.
      - Training records.

      A registrant must keep its ITAR records for five years, in a form where every change shows who made it and when (22 CFR 122.5). EAR records are also kept for five years (15 CFR 762.6). Use five years for everything above unless the attorney says otherwise.

10. **Classify and isolate at the program level, not the file level.** A license, when one is needed, is granted against a program, not against an individual document, so mixing data from two different programs in the same file share or SharePoint site defeats the whole point of classifying carefully. Give each program its own isolated data location and make the classification decision once, at the program level, rather than re-litigating it document by document.

11. **Treat travel abroad with controlled data as an export.** Taking technical data out of the United States is an export (22 CFR 120.50(a)(1)), and so is a laptop, phone, or USB drive that holds it. Three cases cover almost every trip:
    - **The device holds no controlled data.** Nothing is exported. This is the default to recommend: a clean travel device, with controlled data left at home.
    - **The data is carried but never opened abroad.** If the data meets the encrypted-storage rule in step 4, taking it is not an export (22 CFR 120.54(a)(5)), provided the trip is not to a country listed in 22 CFR 126.1. It stops being covered the moment it is decrypted abroad, because causing technical data outside the United States to be in unencrypted form is a release (22 CFR 120.56(a)(4)) and an export (22 CFR 120.50(a)(6)). Opening a file through a remote session from a hotel counts, because the data is on a screen abroad.
    - **The data is opened or used abroad.** This needs an authorization. The usual one is the exemption at 22 CFR 125.4(b)(9). It covers a US person, or a foreign-person employee of a US person, travelling or on temporary assignment, but only if all of these hold. The person is directly employed by the US company, not by a foreign subsidiary. Only US persons or authorized foreign persons possess or use the data. The traveller takes security precautions, e.g., encryption and a VPN. The data is not used for foreign production or defense services. The exemption never applies to a 126.1 country (22 CFR 125.4(a)). Otherwise a license is needed, which is a question for the export attorney.

    For EAR technology the rules match: 15 CFR 734.18(a)(5) for encrypted data carried, License Exception TMP at 15 CFR 740.9(a)(3) for technology used abroad, and 15 CFR 740.9(a)(1) for the device itself as a tool of trade.

    Two more rules for the travel procedure. First, a foreign border officer who demands a password or a device unlock is asking for access information under 22 CFR 120.56(b), which is one more reason to carry a clean device. Second, keep a record for each trip with controlled data: the traveller, the dates, the countries, the device, the data, and the rule or exemption relied on. Add the procedure to the TCP.

12. **Treat a loss of control as a possible release until the export attorney says otherwise.** Some events are not a known release but still put controlled data where anyone could take it. Examples are travelers thrown in an ordinary recycling dumpster, an unencrypted laptop left in a taxi, and a drawing emailed to the wrong address. The capability standard in step 4 means the company cannot show that no foreign person saw the data, so the consultant does not decide that it "was not a release." Do these things instead:
    1. **Contain it.** Recover what can be recovered, and stop the cause, e.g., put a locked shred bin next to the recycling bin.
    2. **Record it** in the memo's loss-of-control section: what was lost, the classification of the item it describes, when and where, how long it was exposed, and who could have reached it. A public dumpster means anyone could.
    3. **Take it to the export attorney and senior management at once.** They decide whether a violation may have happened and whether to make a voluntary disclosure, to DDTC under 22 CFR 127.12 for ITAR data or to BIS under 15 CFR 764.5 for EAR data. Delay costs the company here. A disclosure counts as voluntary only if DDTC receives it before the government learns of the matter from another source and starts an inquiry (22 CFR 127.12(b)(2)), and only if senior management knows of it and authorizes it (22 CFR 127.12(b)(3)(v)).
    4. **Fix the cause in the TCP** and train the people involved.

    If the data is also CUI, the loss is a failure of 3.8.1, which covers paper media, and of 3.8.3, which requires media to be sanitized or destroyed before disposal. It is not a DFARS 252.204-7012 report by default. That clause defines a cyber incident as "actions taken through the use of computer networks," which paper in a dumpster is not. Whether the contract requires some other report is a question for whoever holds the contracts.

## Output

A determination memo for the item, person, or service under review, written to `docs/adr/NNNN-export-control-<short-name>.md` or appended to `scope/external-systems.md` when the subject is a service provider:

```markdown
# Export control determination: <item, person, or service>

Date: YYYY-MM-DD. Program: <program name, if applicable>.

## The four regimes, checked independently
CMMC applicability: yes/no. CUI status and category: ...

## Order of review (22 CFR 120.11, then Supplement No. 4 to 15 CFR Part 774)
1. USML: on the USML / not on the USML / undetermined (end item not known to this shop). Category and entry if on it: ... Enumerated or "specially designed" catch-all: ...
2. Subject to the EAR: yes / no, and the 15 CFR 734.3(b) basis if no: ...
3. CCL: ECCN: ... | not reached. ("600 series" and 9x515 checked first: yes/no)
4. EAR99: yes/no. End-user, end-use, and destination screening done: yes/no.
Result: ITAR | EAR, ECCN ... | EAR99 | not subject to the EAR | pending (handled as ITAR until answered).
Classified by: export attorney | program-level engineering review | design authority in writing (attach it) | pending, request drafted (attached) | pending, request sent to ... on YYYY-MM-DD.
For technical data: the article it describes, and 22 CFR 120.33 basis: ...

## Ownership vs export status
Contractor-owned IP: yes/no. CUI to the contractor: yes/no. Export-controlled regardless of CUI status: yes/no.

## Foreign-person exposure
Foreign nationals with any access path: ... Access information (passwords, decryption keys, remote-shell reach) exposed to them: yes/no.
Ownership and control of the company itself, and any foreign owner, investor, or controlling party: ... (ask; do not assume)
US-person status of each person, and the record that shows it: ... (never inferred from a name; "unknown" is an answer)
Deemed export under 22 CFR 120.50(a)(2), by a release under 22 CFR 120.56: yes / no / unknown, basis: ...

## Where the data sits now (handled as ITAR)
| Location | Provider | Written US-person commitment | Action: stays / moved on YYYY-MM-DD / encrypted in place | Dates held there before the action |
|---|---|---|---|---|

## Encryption and keys
| Location or device | Encrypted at rest | Algorithm and module, validated or not | Who holds the keys and recovery keys | Meets 22 CFR 120.54(a)(5): yes / no / attorney to decide |
|---|---|---|---|---|

## Service provider model (if applicable)
SOC or support staff location: ... Remote-shell or admin-level access: yes/no.
US-person staffing: confirmed in writing (attach) | denied | unknown, not confirmed in writing (treated as not US-person-only).
Clean option selected: US-persons-only SOC | no-remote-shell EDR | neither, gap open.

## Travel
Travel abroad with controlled data: none / clean device only / carried encrypted, not opened / opened abroad under 22 CFR 125.4(b)(9) or 15 CFR 740.9 / licensed. Trip records kept: yes/no.

## Loss of control
None known | event: what, item classification, when, where, exposure window, who could reach it. Referred to export attorney and senior management on YYYY-MM-DD. Disclosure decision: ... (theirs, not this memo's).

## Program-level classification
Classified by: export attorney | program-level engineering review. Program isolation in place: yes/no, location: ...
Minimum program: DDTC registration required: yes / no / attorney asked on YYYY-MM-DD; registered: yes/no. ECP in place: yes/no. TCP in place: yes/no. Records kept for five years: classification memos, US-person records, visitor log, provider commitments, travel, loss of control, training: ...

## Determination
Result: proceed as scoped | remediation required before proceeding.
Remediation items: ...
```

File the memo. When the subject is a service provider, write the finding under that provider's heading in `scope/external-systems.md`, and create the file if it does not exist. This skill does not record anything about the provider in the record, `ssp/ssp.json`, and never edits the responsibility matrix, which is generated from the record under `view/`: where a provider sits in the architecture belongs to `esp-and-msp-scoping`, which records it through scribe.
- Add one line to `scope/open-items.md`: "<provider>: US-person staffing <confirmed in writing | denied | unknown>, per the export memo of YYYY-MM-DD, for `esp-and-msp-scoping` to carry into the provider's remarks."
- Write the same in the memo's remediation items.
- If the staffing model is unknown, write "US-person staffing: unknown, not confirmed in writing." Treat the provider as not US-person-only under step 3 until the provider answers in writing.

When the jurisdiction comes from a design authority (step 3), send it this request and attach it to the memo, marked with the date sent:

```markdown
Subject: Export jurisdiction and classification request, <part number>, <drawing number> Rev <rev>

To: <design authority, and the buyer on the purchase order>
From: <company>, <name and title of the person responsible for export compliance>
Date: YYYY-MM-DD

We are manufacturing <part number> to your drawing <drawing number> Rev <rev> under purchase order <PO number>. We do not know the end item, so we cannot classify the part ourselves. Please tell us in writing:

1. The export jurisdiction and classification of the part: USML category and paragraph, or ECCN, or EAR99, or not subject to the EAR.
2. The export jurisdiction and classification of the technical data you sent us (the drawing, models, and specifications), if different from the part.
3. The basis: a commodity jurisdiction determination (give its number), or a self-classification, and who made it.
4. Any license or agreement under which we receive the data, or confirmation that none is needed because only US persons at our company will have access.
5. If the data came from DoD: the distribution statement and the controlling DoD office.

Until you answer, we will handle the part and all its technical data as ITAR-controlled.

Please sign and date your reply.
```

Item 5 does not settle CUI status. It gives `cui-determination-workflow` the facts it needs.

An item memo uses every section. A memo about a person or a service provider may replace the order-of-review and ownership sections with one line, "not applicable: subject is a person" or "a service", and uses the rest in full. Several provider memos can share `scope/external-systems.md`, one heading each. The memo is read by someone who has not seen this skill, so state each principle in plain words and do not refer to step numbers or to the cases this skill cites. Before finishing, read the remediation items across all the memos from the run and make sure no two of them contradict each other.

## Where practitioners disagree

- **Whether a locked-down VDI carve-out is sufficient on its own, or needs a temporary-work-assignment exemption layered on top.** One position: the technical controls (no file transfer, no printing, screen-only access, anti-shoulder-surfing measures) are enough by themselves because the data never leaves the US datacenter. The other: a fully locked VDI plus a formal exemption gives a defensible second layer if the technical controls are ever found lacking. The outcome depends on the assessor and, for this question specifically, the export attorney of record.
- **How much weight a consent-agreement precedent like the one cited in step 5 should carry for a company with no prior export history.** One position: the capability-based standard applies equally regardless of company size or history, so the lesson generalizes. The other: enforcement posture and penalty severity in practice track company size, contract value, and whether the government already has an open compliance relationship with the company. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: do not let a client's IT lead sign off on an export classification; document who made the call (attorney or engineering review) in the memo, because that attribution is itself evidence of a sound program. **OSC seat**: if your security tooling budget did not have room to ask what country your MSSP's SOC staff sit in, ask now; a vendor contract signed for its price, without a written answer to that question, is the fastest way to end up owning step 6's live violation without knowing it.

## Sources

- DoDI 5230.24, Distribution Statements on DoD Technical Information, January 10, 2023: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf (mirrored at `reference/dod-issuances/dodi-5230-24.md`).
- 22 CFR 120.50: https://www.ecfr.gov/current/title-22/section-120.50.
- 22 CFR 120.56: https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120/section-120.56.
- 22 CFR Part 120: https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120.
- 22 CFR 120.11: https://www.ecfr.gov/current/title-22/section-120.11.
- 22 CFR 120.33: https://www.ecfr.gov/current/title-22/section-120.33.
- 15 CFR 772.1: https://www.ecfr.gov/current/title-15/section-772.1.
- DFARS 252.225-7048: https://www.ecfr.gov/current/title-48/section-252.225-7048.
- 15 CFR 734.3: https://www.ecfr.gov/current/title-15/section-734.3.
- 15 CFR Part 774, Supplement No. 4: https://www.ecfr.gov/current/title-15/part-774/appendix-Supplement%20No.%204%20to%20Part%20774.
- DoD CUI Export Controlled category page: https://www.dodcui.mil/Export-Control/Export-Controlled/.
- Public panel analyzing a 2019 DDTC consent agreement involving an infrared-sensor manufacturer (FLIR): https://www.youtube.com/watch?v=qS44dOwoWUs.
- Public panel on practical ITAR compliance steps for small and mid-size businesses: https://www.youtube.com/watch?v=xhFX1eCHHSI.
- 32 CFR Part 2002: https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2002.
- 22 CFR 120.54: https://www.ecfr.gov/current/title-22/section-120.54.
- 22 CFR 122.1: https://www.ecfr.gov/current/title-22/section-122.1.
- 22 CFR 122.5: https://www.ecfr.gov/current/title-22/section-122.5.
- 22 CFR 125.4: https://www.ecfr.gov/current/title-22/section-125.4.
- 22 CFR 126.1: https://www.ecfr.gov/current/title-22/section-126.1.
- 22 CFR 127.12: https://www.ecfr.gov/current/title-22/section-127.12.
- 15 CFR 734.18: https://www.ecfr.gov/current/title-15/section-734.18.
- 15 CFR 740.9: https://www.ecfr.gov/current/title-15/section-740.9.
- 15 CFR 762.6: https://www.ecfr.gov/current/title-15/section-762.6.
- 15 CFR 764.5: https://www.ecfr.gov/current/title-15/section-764.5.
- BIS, Export Compliance Guidelines: The Elements of an Effective Export Compliance Program: https://www.bis.gov/media/documents/export-compliance-guidelines.
- Practitioner consensus, unattributed, backs the "handle as ITAR while the answer is pending" rule in step 3, the four-regime framing in step 1, the "flip the map" access-control test in step 7, the visual and casual access distinction in step 8, the program-level classification and isolation rule in step 10, and the clean travel device default in step 11.
