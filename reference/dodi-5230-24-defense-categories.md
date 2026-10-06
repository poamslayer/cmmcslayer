> **Provenance.** This repo's own work, MIT. It maps the defense categories in DoDI 5230.24 (January 10, 2023), para 4.3, to the law or rule behind each, using the text mirrored at `reference/dod-issuances/dodi-5230-24.md` and the DoD CUI Registry pages mirrored at `reference/cui-registry/`. The history column comes from DoDI 5230.24, August 23, 2012, Incorporating Change 3, October 15, 2018, Enclosure 4, Tables 1 to 4, read from the Wayback Machine copy listed in `reference/authorities.md`. Short passages are quoted from these United States Government works, which are public domain. Regulation text was checked against the eCFR on 2026-09-26. Every source is in `reference/authorities.md` with its tier.

# DoDI 5230.24 defense categories and the authority behind each

A Distribution Statement B to E has to name a defense category (DoDI 5230.24 para 4.1.c(2)). Of the fourteen categories, only one is itself a CUI category: "CTI is a category of CUI" (para 4.3.a). For the other thirteen, the category tells you why the controlling DoD office limited distribution. It does not tell you the content is CUI. To decide that, find the authority behind the category and check whether it reaches the content you are holding. This file is that lookup. `cui-determination-workflow` step 7 sends you here.

## Three rules that apply to every row

1. **The category is a reason for limiting distribution, not a CUI designation.** "The application of a distribution statement does not automatically mean the document is CUI" (DoD CUI Program FAQ, Use of Distribution Statements). The distribution statement still binds you: handle the document within its authorized audience whether or not it is CUI.
2. **A CUI status rests on a Registry category and its Tier 1 authority.** CUI categories are the exclusive designations (32 CFR 2002.12(a)). If no Registry category's authority reaches the content, the defense category does not make it CUI. Other categories can still reach it, so run the rest of `cui-determination-workflow` before you conclude it is not CUI.
3. **Information a company creates and owns on its own is not CUI in its own hands.** 32 CFR 2002.4(h) excludes information "a non-executive branch entity possesses and maintains in its own systems that did not come from, or was not created or possessed by or for, an executive branch agency". This matters most for rows b, j, k, l and m, because those categories protect a company's own information once the Government holds it.

## Outcomes

- **CUI.** The statement itself says the content is CUI. This outcome applies only to row a.
- **CUI if the test passes.** A Registry category exists. The content is CUI only when the category's authority reaches it. Apply the test in the row.
- **No CUI basis from this category.** No Registry category matches. The category controls release under the contract or a licence. Treat the content as CUI only if some other category reaches it.

## Lookup

Registry categories link to the local mirror. "Tier" follows ADR-0004: 1 is regulation or statute, 2 is official guidance.

### a. Controlled Technical Information (CTI)

- **Statements:** B, C, D, E, F, REL TO.
- **Registry:** [Defense: Controlled Technical Information](cui-registry/Defense--Controlled-Technical-Information.md).
- **Authority:** 10 U.S.C. 130; DFARS 252.204-7012 (Tier 1). The Registry page also lists the ITAR and the EAR.
- **Outcome:** CUI. The controlling DoD office has already decided.
- **Test:** None needed for status. If the CUI banner is missing, handle the content as CUI and ask the controlling DoD office to fix the marking.
- **2012 edition:** Not a reason in the 2012 tables. It was added in the 2023 edition.

### b. Contractor Performance Evaluation

- **Statements:** B, E, F.
- **Registry:** [Procurement and Acquisition: Source Selection](cui-registry/Procurement-and-Acquisition--Source-Selection.md); [General Procurement and Acquisition](cui-registry/Procurement-and-Acquisition--General-Procurement-and-Acquisition.md).
- **Authority:** 48 CFR 3.104-4 (Tier 1), which bars disclosing source selection information to anyone the agency has not authorized. FAR 42.1503(d) (Tier 1) says a completed past-performance evaluation "shall not be released to other than Government personnel and the contractor whose performance is being evaluated during the period the information may be used to provide source selection information", and that such evaluations "should therefore be marked" with the legend "Source Selection Information". 5230.24 also names DoDI 5000.79 (Tier 2).
- **Outcome:** CUI if the test passes.
- **Test:** Is it a Government evaluation of a contractor, such as a CPARS record, or other information prepared for a source selection? If yes, the content falls under Source Selection. A company's own internal ratings of its suppliers do not qualify, because no FAR provision reaches them and 32 CFR 2002.4(h) excludes them.
- **2012 edition:** Statements B and E, "Assigned pursuant to subparts 203.104-4" of the DFARS.

### c. Critical Technology

- **Statements:** B, C, D, E, F, REL TO.
- **Registry:** [Export Control: Export Controlled](cui-registry/Export-Control--Export-Controlled.md).
- **Authority:** The ITAR (22 CFR 120 to 130) and the EAR (15 CFR 730 to 774) (Tier 1). 5230.24 says this category's information "is export controlled", and DoDD 5230.25 (Tier 2) governs how it is withheld.
- **Outcome:** CUI if the test passes.
- **Test:** Is the content ITAR technical data (22 CFR 120.33) or EAR "technology" (15 CFR 772.1) that is controlled for export? Use the `export-control-overlay` skill to decide jurisdiction and classification. If the content is controlled, it is Export Controlled CUI, and it is often CTI as well. If it is EAR99 or not subject to the EAR (15 CFR 734.3(b)(3)), this category gives it no CUI basis.
- **2012 edition:** Statements B, C, D and E, "Assigned pursuant to subpart 800.209 of title 31, CFR ... ITAR; and EAR." At the time, 31 CFR 800.209 was the definition of "critical technologies" in the CFIUS foreign investment rule. It was renumbered on 2020-02-13 (eCFR version history). A definition tells you what the category is aimed at. It is not a safeguarding authority.

### d. Direct Military Support

- **Statements:** E, F, REL TO.
- **Registry:** [Export Control: Export Controlled](cui-registry/Export-Control--Export-Controlled.md).
- **Authority:** 10 U.S.C. 130 and 32 CFR Part 250 (Tier 1), which is the rule that implements it. 5230.24 says "A competent authority will designate such data in accordance with DoDD 5230.25" (Tier 2) and the export-control warning in Figure 3.
- **Outcome:** CUI if the test passes. The test almost always passes, because this category only applies to "export-controlled technical information".
- **Test:** Same as row c. The Figure 3 warning on the cover is strong evidence that the controlling DoD office found the content export controlled. Confirm with the controlling DoD office if the cover lacks the warning.
- **2012 edition:** Statement E only, "Assigned pursuant to section 2751 of title 22, U.S.C." (the Arms Export Control Act).

### e. Export Controlled

- **Statements:** B, C, D, E, F, REL TO.
- **Registry:** [Export Control: Export Controlled](cui-registry/Export-Control--Export-Controlled.md).
- **Authority:** The ITAR and the EAR, 10 U.S.C. 130, and 32 CFR Part 250 (Tier 1); DoDD 5230.25 and DoDI 2040.02 (Tier 2). This is the list para 4.3.e gives.
- **Outcome:** CUI if the test passes.
- **Test:** Same as row c. Statements C and D also require a current DD Form 2345 before release to a contractor (para 4.3.e(1)).
- **2012 edition:** Statements B, C, D and E, protecting information "subject to the provisions of" DoDD 5230.25. The old Distribution "X" was folded into this reason.

### f. Foreign Government Information

- **Statements:** B, C, D, E, F, REL TO.
- **Registry:** No category with this name. The closest is [International Agreements: International Agreement Information](cui-registry/International-Agreements--International-Agreement-Information.md), which covers information "provided by, otherwise made available by, or produced in cooperation with, a foreign government or international organization" that requires protection under 10 U.S.C. 130c(b), "when not subject to classification under Executive Order 13526".
- **Authority:** 10 U.S.C. 130c (Tier 1). Under 130c(b), withholding requires the national security official concerned to make the determinations listed there, including that the foreign government or organization is itself withholding the information.
- **Outcome:** CUI if the test passes. Classified foreign government information is outside this repo.
- **Test:** Did a foreign government or international organization provide the information, or was it produced with one, under a written condition that it not be released? Did the controlling DoD office rely on that condition? If yes, it is International Agreement Information. If the only foreign connection is a foreign customer's commercial data under a direct commercial sale, 130c does not reach it. Test that content under rows c, e and j.
- **2012 edition:** Statements B, C, D and E, "Assigned pursuant to chapter 15 of title 50, U.S.C. ... and Executive Order 13526". Those authorities are for classified national security information, and the Registry now points unclassified foreign government information to 130c.

### g. International Agreements

- **Statements:** B, C, D, E, F, REL TO.
- **Registry:** [International Agreements: International Agreement Information](cui-registry/International-Agreements--International-Agreement-Information.md).
- **Authority:** 10 U.S.C. 130c (Tier 1). Para 4.3.g(2) cites the same section.
- **Outcome:** CUI if the test passes.
- **Test:** Same as row f. An agreement that has been published on the State Department treaty portal is public, so it is not CUI.
- **2012 edition:** Not a reason in the 2012 tables.

### h. Operations Security

- **Statements:** B, E, F.
- **Registry:** [Intelligence: Operations Security](cui-registry/Intelligence--Operations-Security.md).
- **Authority:** The Registry names NSPM-28, which is not public ("contact your OPSEC office for a copy"), and DoDD 5205.02E and DoDM 5205.02 (Tier 2). No public Tier 1 text is available to test against.
- **Outcome:** CUI if the test passes. The Registry says: "To use the OPSEC category, the information must be on the CIL", meaning the Critical Information List.
- **Test:** Is the information on the Government program's Critical Information List? A contractor cannot answer that question itself. Ask the controlling DoD office. Until it answers, handle the content as CUI and send the notice described in `cui-determination-workflow` step 8.
- **2012 edition:** Statements B and E, "Assigned in accordance with DoDD 5205.02E".

### i. Patents and Inventions

- **Statements:** B, E, F.
- **Registry:** [Patent: Inventions](cui-registry/Patent--Inventions.md); [Patent Applications](cui-registry/Patent--Patent-Applications.md); [Secrecy Orders](cui-registry/Patent--Secrecy-Orders.md).
- **Authority:** 35 U.S.C. 205, which keeps information about federally funded inventions confidential while a patent application may be filed; 37 CFR 401.13; FAR 27.302; 35 U.S.C. 122(a); 35 U.S.C. 181 for secrecy orders (all Tier 1).
- **Outcome:** CUI if the test passes.
- **Test:** Does the Government own or may it own a right, title or interest in the invention, for example a subject invention under a funding agreement, or is the invention under a secrecy order? If yes, the matching Patent category applies. Para 4.3.i excludes issued patents, which are public, and information that is protected only by copyright. A company's own invention that is not a subject invention and is not under a secrecy order falls under 32 CFR 2002.4(h), so it is not CUI in the company's hands.
- **2012 edition:** Called "Premature Dissemination". Statements B and E, "Assigned pursuant to section 205 of title 35, U.S.C."

### j. Proprietary Business Information

- **Statements:** B, E, F.
- **Registry:** [Proprietary Business Information: General Proprietary Business Information](cui-registry/Proprietary-Business-Information--General-Proprietary-Business-Information.md).
- **Authority:** 18 U.S.C. 1905, the Trade Secrets Act, which binds federal employees, and the other statutes the Registry page lists, including 10 U.S.C. 4021 and FAR 52.227-20(d) (all Tier 1).
- **Outcome:** CUI if the test passes, and only in the Government's hands or when it comes from the Government.
- **Test:** Whose information is it, and where did it come from? If it is another company's proprietary information that reached you from the Government, it is CUI when you receive it. Your own proprietary information, created and kept in your own systems, is not CUI (32 CFR 2002.4(h)). ISOO said the same thing for proprietary information "you create internally and maintain ownership of" (ISOO CUI Stakeholders Update Q2 FY2020, slide 8, quoted in `reference/authorities.md`). A Statement B on your own drawing, applied when the drawing was delivered to the Government, does not turn the original in your own systems into CUI.
- **2012 edition:** Called "Proprietary Information". Statements B and E, "Assigned pursuant to Public Law 104-294" (the Economic Espionage Act), 28 U.S.C. 1498(a), title 17, 18 U.S.C. 1905, and 15 U.S.C. 638.

### k. Small Business Innovation Research (SBIR)

- **Statements:** B, E, F.
- **Registry:** No direct match. [Procurement and Acquisition: Small Business Research and Technology](cui-registry/Procurement-and-Acquisition--Small-Business-Research-and-Technology.md) rests on 15 U.S.C. 638(k)(4). Section 638(k) covers the Small Business Administration's SBIR and STTR award databases, not the technical data an SBIR awardee delivers.
- **Authority:** The DFARS SBIR data-rights clause, 252.227-7018 (Tier 1). It limits the Government's licence to use and disclose the data. It is not a safeguarding authority.
- **Outcome:** No CUI basis from this category.
- **Test:** Test the technical data on its own content. If it has military or space application, test it as CTI (row a). If it is export controlled, apply row e. If it is the awardee's own proprietary information that reached you from the Government, apply row j. The SBIR legend alone does not make the data CUI.
- **2012 edition:** Not a separate reason. The "Proprietary Information" reason cited 15 U.S.C. 638.

### l. Software Documentation

- **Statements:** B, C, D, E, F.
- **Registry:** No match.
- **Authority:** DFARS Subpart 227.72 and the licence negotiated under it, for example DFARS 252.227-7014 (Tier 1). These govern licence rights, not safeguarding.
- **Outcome:** No CUI basis from this category.
- **Test:** Handle the documentation under the licence terms. Treat it as CUI only if another category reaches it. The common cases are CTI (row a), for documentation of software with military application, and Export Controlled (row e), for documentation of software controlled under the ITAR or EAR.
- **2012 edition:** Statements B, C, D and E, citing "the software license in subpart 227.72" of the DFARS.

### m. Test and Evaluation

- **Statements:** B, E, F, REL TO.
- **Registry:** No match.
- **Authority:** The 2023 edition names no authority for this category. The 2012 edition cited 32 CFR 311.8, which was an OSD Privacy Act exemption procedure and was removed from the CFR on 2019-08-07 (eCFR version history). No current safeguarding authority is named.
- **Outcome:** No CUI basis from this category.
- **Test:** Test results for a manufacturer's product are usually proprietary business information (row j) when the Government holds them. Results for military hardware are often CTI (row a). Test the content against those rows. If neither applies, the category controls distribution only.
- **2012 edition:** Statements B and E, "Assigned pursuant to part 311.8 of title 32, CFR".

### n. Vulnerability Information

- **Statements:** B, C, D, E, F.
- **Registry:** [Critical Infrastructure: Information Systems Vulnerability Information](cui-registry/Critical-Infrastructure--Information-Systems-Vulnerability-Information.md), which rests on 44 U.S.C. 3554 and 3555; [Defense: DoD Critical Infrastructure Security Information](cui-registry/Defense--DoD-Critical-Infrastructure-Security-Information.md), which rests on 10 U.S.C. 130e.
- **Authority:** 44 U.S.C. 3554 and 3555; 10 U.S.C. 130e (Tier 1). DoDD 3020.40 (Tier 2) sits under the second.
- **Outcome:** CUI if the test passes.
- **Test:** Does the content reveal vulnerabilities of a Government information system, or of DoD critical infrastructure such as installations and mission-critical assets? If yes, the matching category applies. A contractor's scan results or assessment of its own network fall under 32 CFR 2002.4(h), so they are not CUI in its own hands, even though they deserve protection. The Registry's examples, such as "Existence/details of intrusions into WARCOM networks", describe Government systems.
- **2012 edition:** Statements B, C, D and E, "Assigned pursuant to Public Law 107-296" (the Homeland Security Act of 2002).

## Reasons from the 2012 edition with no 2023 category

The 2023 edition's categories "override authorized reasons enacted in previous issuances but do not affect distribution statements assigned to legacy information" (para 4.3). Older documents can still carry these reasons:

- **Administrative or Operational Use** (Statements B, C, D, E). The 2012 edition cited no statute for it. Treat it like row l: it controls distribution, and it gives no CUI basis on its own. Test the content under rows a and e.
- **Specific Authority** (B, C, D, E). The reason itself names the authority, for example "Specific Authority (identification of valid documented authority)". Find that authority's Registry category and test the content against it.
- **Premature Dissemination** and **Proprietary Information** are rows i and j under their old names.
