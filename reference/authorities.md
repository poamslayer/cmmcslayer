> **Provenance.** This repo's own work, MIT. It lists public sources and quotes short passages from United States Government works, which are public domain. The rules for this file are in `docs/adr/0004-authority-tiers.md`.

# Authorities register

Every URL cited anywhere in `skills/` is listed here, once. `python3 scripts/check_authorities.py` (run by `verify.sh`) fails when a skill cites a URL that is not here, and when a mirror path below does not exist. `python3 scripts/check_links.py` checks that every URL here and in `skills/` still resolves.

## How to use it

- **Before citing a source in a skill**, find it here. If it is not here, add it first, in the right tier, then cite it.
- **Before stating a CUI status rule** (whether something is CUI, which category, whether a marking or a flowdown makes it CUI), cite a Tier 1 or Tier 2 entry. A Tier 3 entry can support how practitioners handle the question, never the answer. See ADR-0004 point 3.
- **To see which skills cite a source**, run `grep -rl '<url>' skills`. The register does not keep that list, because a hand-kept list goes stale.
- **When a host blocks scripted fetches**, read the mirror. When the source is reissued, refresh the mirror and its hash.

The **Checked** column gives the date a URL was last confirmed and how: `script` (it answered `check_links.py`), `browser` (the host refuses scripts, so it was opened in a browser), or `mirror` (it was fetched into `reference/` on that date).

Where two URLs reach the same source, both are listed, because the check matches the text of the URL.

## Tier 1: regulation and statute

Can establish a rule or a status.

| Source | Relied on for | URL | Mirror | Checked |
|---|---|---|---|---|
| 32 CFR Part 170 | CMMC Program: definitions, levels, scoping, POA&M, scoring | https://www.ecfr.gov/current/title-32/part-170 and https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-D/part-170 | | 2026-09-26 script |
| 32 CFR 170.4 | Definitions: ESP, CSP, Security Protection Data, Operational Plan of Action, Test Equipment | https://www.ecfr.gov/current/title-32/section-170.4 | | 2026-09-26 script |
| 32 CFR 170.5 | Waivers | https://www.ecfr.gov/current/title-32/section-170.5 | | 2026-09-26 script |
| 32 CFR 170.19 | CMMC assessment scope and asset categories, including the Out-of-Scope Asset and VDI provisions | https://www.ecfr.gov/current/title-32/section-170.19 | | 2026-09-26 script |
| 32 CFR 170.21 | POA&M requirements and gates | https://www.ecfr.gov/current/title-32/section-170.21 | `reference/32-cfr-170-21-poam-gates.md` | 2026-09-26 script |
| 32 CFR 170.23 | CMMC level determination and flowdown | https://www.ecfr.gov/current/title-32/section-170.23 | | 2026-09-26 script |
| 32 CFR 170.24 | Scoring methodology, MET and NOT MET, OPA treatment | https://www.ecfr.gov/current/title-32/section-170.24 | `reference/32-cfr-170-24-scoring.md` | 2026-09-26 script |
| 32 CFR Part 2002 | The CUI Program | https://www.ecfr.gov/current/title-32/part-2002 and https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2002 | | 2026-09-26 script |
| 32 CFR 2002.4(h) | CUI definition, and the exclusion for a non-executive branch entity's own information. Quoted below | https://www.ecfr.gov/current/title-32/section-2002.4 | | 2026-09-26 script |
| 32 CFR 2002.4(aa), (pp) | "Handling" includes re-using; "re-use" defined | https://www.ecfr.gov/current/title-32/section-2002.4 | | 2026-09-26 script |
| 32 CFR 2002.4(ee) | Misuse includes marking information as CUI when it does not qualify | https://www.ecfr.gov/current/title-32/section-2002.4 | | 2026-09-26 script |
| 32 CFR 2002.4(nn) | "Required or permitted" basis; general agency discretion excluded | https://www.ecfr.gov/current/title-32/section-2002.4 | | 2026-09-26 script |
| 32 CFR 2002.12(a) | CUI categories are the exclusive designations | https://www.ecfr.gov/current/title-32/section-2002.12 | | 2026-09-26 script |
| 32 CFR 2002.14(h)(2) | Agencies must use NIST SP 800-171 for CUI on non-Federal information systems; how a civilian agency's CUI reaches a contractor without DFARS | https://www.ecfr.gov/current/title-32/section-2002.14 | | 2026-09-26 script |
| 32 CFR 2002.18(f) | Indicate decontrol when re-using | https://www.ecfr.gov/current/title-32/section-2002.18 | | 2026-09-26 script |
| 32 CFR 2002.20 | Marking. (a)(1), (a)(2), (a)(4), (a)(7), (d), (f): only Registry markings designate; legacy markings are void; the designating agency determines; lack of a marking does not exempt; designation indicator; portion marking | https://www.ecfr.gov/current/title-32/section-2002.20 | | 2026-09-26 script |
| 32 CFR 2002.50 | Challenges to a CUI designation | https://www.ecfr.gov/current/title-32/section-2002.50 | | 2026-09-26 script |
| 81 FR 63324 (2016-09-14), the CUI final rule and its preamble | The preamble at 81 FR 63334: a document derived from CUI is CUI "because it contains controlled information, not simply because it is derived from a document that contains CUI". Published by NARA with the rule it explains. Quoted below | https://www.federalregister.gov/documents/2016/09/14/2016-21665/controlled-unclassified-information and https://www.govinfo.gov/content/pkg/FR-2016-09-14/html/2016-21665.htm | | 2026-09-26 script |
| 81 FR 72986 (2016-10-21), the DFARS 252.204-7012 final rule and its preamble | 72989 and 72997: the cost of complying with 7012 is allowable and "should be considered during proposal preparation"; DoD does not develop "cost recovery models" | https://www.federalregister.gov/documents/2016/10/21/2016-25315/defense-federal-acquisition-regulation-supplement-network-penetration-reporting-and-contracting-for-cloud-services-dfars and https://www.govinfo.gov/content/pkg/FR-2016-10-21/html/2016-25315.htm | | 2026-09-26 script |
| 89 FR 83092 (2024-10-15), the CMMC Program final rule and its preamble | 83136: nothing precludes an ESP that holds no CUI from voluntarily requesting a C3PAO assessment; 83170: entities may voluntarily seek certification; 83197: the rule makes no change to cost allowability under FAR 31.201-2 | https://www.federalregister.gov/documents/2024/10/15/2024-22905/cybersecurity-maturity-model-certification-cmmc-program and https://www.govinfo.gov/content/pkg/FR-2024-10-15/html/2024-22905.htm | | 2026-09-26 script |
| FAR 16.202-1 | A firm-fixed-price contract is "not subject to any adjustment on the basis of the contractor's cost experience" | https://www.ecfr.gov/current/title-48/section-16.202-1 | | 2026-09-26 script |
| DFARS 252.204-7012 | Covered defense information (both prongs), CTI, technical information, safeguarding, incident reporting | https://www.ecfr.gov/current/title-48/section-252.204-7012 and https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012 | | 2026-09-26 script |
| DFARS 252.204-7021 | CMMC requirements; flowdown at (f), "appropriate for the information that is being flowed down" | https://www.ecfr.gov/current/title-48/section-252.204-7021 and https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7021 | `reference/dfars-252-204-7021.md` | 2026-09-26 script; mirror 2026-09-26 |
| DFARS 252.227-7013 | Rights in technical data: technical data definition, data rights, private expense | https://www.ecfr.gov/current/title-48/section-252.227-7013 and https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.227-7013 | | 2026-09-26 script |
| DFARS 252.225-7048 | Export-controlled items clause; (a) defines the term to cover both EAR and ITAR items, so the clause alone does not say which regime applies | https://www.ecfr.gov/current/title-48/section-252.225-7048 | | 2026-09-26 script |
| FAR 52.204-21 | FCI and basic safeguarding | https://www.ecfr.gov/current/title-48/section-52.204-21 and https://www.acquisition.gov/far/52.204-21 | | 2026-09-26 script |
| 22 CFR Part 120 | ITAR definitions | https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120 | | 2026-09-26 script |
| 22 CFR 120.31 | Defense article, including unfinished products that have reached a stage in manufacturing where they are identifiable as defense articles | https://www.ecfr.gov/current/title-22/section-120.31 and https://www.ecfr.gov/current/title-22/part-120/section-120.31 | | 2026-09-26 script |
| 22 CFR 120.33 | ITAR technical data ("required for") | https://www.ecfr.gov/current/title-22/section-120.33 | | 2026-09-26 script |
| 22 CFR 120.50 | Export; (a)(2) defines the deemed export: releasing technical data to a foreign person in the United States | https://www.ecfr.gov/current/title-22/section-120.50 | | 2026-09-26 script |
| 22 CFR 120.56 | Release, including release to a foreign person (deemed export) | https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120/section-120.56 | | 2026-09-26 script |
| 22 CFR 120.41 | "Specially designed"; (b)(2) releases fasteners, washers, spacers, and similar hardware "regardless of form or fit"; the release does not reach an item a USML entry names directly | https://www.ecfr.gov/current/title-22/section-120.41 | | 2026-09-26 script |
| 22 CFR 120.11 | ITAR order of review: USML first, enumerated entry over "specially designed" catch-all, integration rule, pointer to the CCL order of review | https://www.ecfr.gov/current/title-22/section-120.11 | | 2026-09-26 script |
| 15 CFR 734.3 | Items subject to the EAR; ITAR items excluded at (b)(1)(i); published, fundamental research and other information excluded at (b)(3); EAR99 designation at (c) | https://www.ecfr.gov/current/title-15/section-734.3 | | 2026-09-26 script |
| 15 CFR 772.1 | EAR definitions: "technology", "required", "specially designed" (fasteners released at (b)(2), "regardless of form or fit") | https://www.ecfr.gov/current/title-15/section-772.1 | | 2026-09-26 script |
| 15 CFR Part 774, Supplement No. 4 | Commerce Control List order of review: no CCL review for a USML item, "600 series" and 9x515 first, EAR99 may still need a license by end user, end use, or destination | https://www.ecfr.gov/current/title-15/part-774/appendix-Supplement%20No.%204%20to%20Part%20774 | | 2026-09-26 script |
| 22 CFR 120.54 | Activities that are not exports; (a)(5) sending, taking, or storing technical data that is unclassified, end-to-end encrypted with FIPS 140-2 or successor modules (or at least AES-128 strength), and not sent to or stored in a 126.1 country; (b) end-to-end encryption means the means of decryption are not provided to any third party; (c) access to data encrypted that way is not a release | https://www.ecfr.gov/current/title-22/section-120.54 | | 2026-09-26 script |
| 22 CFR 122.1 | Registration; (a) a manufacturer of defense articles must register even if it does not export | https://www.ecfr.gov/current/title-22/section-122.1 | | 2026-09-26 script |
| 22 CFR 122.5 | Records a registrant keeps, how they are kept, and the five-year retention period | https://www.ecfr.gov/current/title-22/section-122.5 | | 2026-09-26 script |
| 22 CFR 125.4 | Exemptions of general applicability; (a) none apply to 126.1 destinations; (b)(9) technical data taken abroad by a U.S. person, or a foreign person employee of a U.S. person, travelling or on temporary assignment, with its conditions | https://www.ecfr.gov/current/title-22/section-125.4 | | 2026-09-26 script |
| 22 CFR 126.1 | Prohibited exports and proscribed countries | https://www.ecfr.gov/current/title-22/section-126.1 | | 2026-09-26 script |
| 22 CFR 127.12 | Voluntary disclosures to DDTC; (b)(2) timing, before the government learns of it from another source; (b)(3)(v) senior management knowledge and authorization | https://www.ecfr.gov/current/title-22/section-127.12 | | 2026-09-26 script |
| 15 CFR 734.18 | Activities that are not exports under the EAR; (a)(5) the encrypted sending, taking, or storing rule, with Country Group D:5; (c) access to data encrypted that way is not a release | https://www.ecfr.gov/current/title-15/section-734.18 | | 2026-09-26 script |
| 15 CFR 740.9 | License Exception TMP; (a)(1) tools of trade; (a)(3) "technology" taken abroad by a U.S. person or a foreign person employee travelling, with its conditions | https://www.ecfr.gov/current/title-15/section-740.9 | | 2026-09-26 script |
| 15 CFR 762.6 | EAR records are kept five years | https://www.ecfr.gov/current/title-15/section-762.6 | | 2026-09-26 script |
| 15 CFR 764.5 | Voluntary self-disclosures to BIS | https://www.ecfr.gov/current/title-15/section-764.5 | | 2026-09-26 script |
| 10 U.S.C. 130 | DoD authority to withhold technical data; "can be used, or be adapted for use" | https://www.law.cornell.edu/uscode/text/10/130 | | 2026-09-26 script |
| 31 U.S.C. 3729(b)(1) | False Claims Act, the meaning of "knowingly". Read the current text before quoting it | https://www.law.cornell.edu/uscode/text/31/3729 | | 2026-09-26 script |
| 48 CFR 3.104-4 | Disclosure, protection, and marking of source selection information; the authority behind the Source Selection and General Procurement Registry categories | https://www.ecfr.gov/current/title-48/section-3.104-4 | | 2026-09-26 script |
| FAR 42.1503 | (d) a completed past-performance evaluation is released only to the Government and the evaluated contractor while it may be used as source selection information, and is marked "Source Selection Information" | https://www.ecfr.gov/current/title-48/section-42.1503 | | 2026-09-26 script |
| FAR 27.302 | Policy on inventions made under Government contracts; an authority of the Registry's Inventions category | https://www.ecfr.gov/current/title-48/section-27.302 | | 2026-09-26 script |
| DFARS Subpart 227.72 | Rights in computer software and software documentation; a licence, not a safeguarding authority | https://www.ecfr.gov/current/title-48/part-227/subpart-227.72 | | 2026-09-26 script |
| DFARS 252.227-7014 | Rights in other than commercial computer software and software documentation | https://www.ecfr.gov/current/title-48/section-252.227-7014 | | 2026-09-26 script |
| DFARS 252.227-7018 | SBIR and STTR data rights; limits the Government's licence, is not a safeguarding authority | https://www.ecfr.gov/current/title-48/section-252.227-7018 | | 2026-09-26 script |
| 32 CFR Part 250 | Withholding of unclassified technical data from public disclosure; implements 10 U.S.C. 130 | https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-M/part-250 | | 2026-09-26 script |
| 32 CFR 311.8 (removed) | Cited by the 2012 edition of DoDI 5230.24 for the Test and Evaluation reason. An OSD Privacy Act exemption procedure, removed on 2019-08-07; the link is its eCFR version history | https://www.ecfr.gov/api/versioner/v1/versions/title-32.json?section=311.8 | | 2026-09-26 script |
| 37 CFR 401.13 | Confidentiality of invention disclosures and patent applications under funding agreements | https://www.ecfr.gov/current/title-37/section-401.13 | | 2026-09-26 script |
| 10 U.S.C. 130c | Withholding sensitive information of foreign governments and international organizations; (b) the determinations required | https://www.law.cornell.edu/uscode/text/10/130c | | 2026-09-26 script |
| 10 U.S.C. 130e | DoD critical infrastructure security information | https://www.law.cornell.edu/uscode/text/10/130e | | 2026-09-26 script |
| 15 U.S.C. 638 | SBIR and STTR; (k) the SBA award databases, which is what the Registry's Small Business Research and Technology category rests on | https://www.law.cornell.edu/uscode/text/15/638 | | 2026-09-26 script |
| 18 U.S.C. 1905 | Trade Secrets Act; binds federal employees; an authority of the Registry's General Proprietary Business Information category | https://www.law.cornell.edu/uscode/text/18/1905 | | 2026-09-26 script |
| 35 U.S.C. 122 | Confidential status of patent applications | https://www.law.cornell.edu/uscode/text/35/122 | | 2026-09-26 script |
| 35 U.S.C. 181 | Secrecy orders on inventions | https://www.law.cornell.edu/uscode/text/35/181 | | 2026-09-26 script |
| 35 U.S.C. 205 | Confidentiality of information disclosing federally funded inventions | https://www.law.cornell.edu/uscode/text/35/205 | | 2026-09-26 script |
| 44 U.S.C. 3554 and 3555 | Federal agency information security responsibilities; the authority of the Registry's Information Systems Vulnerability Information category | https://www.law.cornell.edu/uscode/text/44/3554 and https://www.law.cornell.edu/uscode/text/44/3555 | | 2026-09-26 script |
| NIST SP 800-171 Rev 2 | The 110 security requirements. Incorporated by reference in 32 CFR 170.2 and required by DFARS 252.204-7012 | https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final | `reference/nist-800-171r2-requirements.json` | 2026-09-26 script |
| NIST SP 800-171A (June 2018) | The 320 assessment objectives. Incorporated by reference in 32 CFR 170.2 | https://csrc.nist.gov/pubs/sp/800/171/a/final | `reference/nist-800-171r2-requirements.json` | 2026-09-26 script |

## Tier 2: official federal guidance

Can state how the government reads a rule. Cite it next to the Tier 1 rule it explains, not in place of it.

| Source | Relied on for | URL | Mirror | Checked |
|---|---|---|---|---|
| DoD CIO, CMMC Resources and Documentation | The CMMC Level 1 and Level 2 Scoping Guides and Assessment Guides. Per ADR-0001 point 5, the only allowed source for Assessment Guide text | https://dodcio.defense.gov/CMMC/Resources-Documentation/ | `reference/nist-800-171r2-requirements.json` (objective text) | 2026-09-26 browser |
| DoD CIO, CMMC FAQs | Answers by FAQ number, for example C-Q9, C-Q12, E-A1, F-Q1 to F-Q5 | https://dodcio.defense.gov/CMMC/FAQ/ | | 2026-09-26 browser |
| DoD CIO, FedRAMP Moderate Equivalency memo (December 2023) | What a cloud service offering needs to be equivalent to FedRAMP Moderate | https://dodcio.defense.gov/Portals/0/Documents/Library/FEDRAMP-EquivalencyCloudServiceProviders.pdf | | 2026-09-26 browser |
| Department of War, suspension of CMMC Phase II requirements (2026-07-13) | The suspension and the 60-day review | https://business.defense.gov/Engage/News/Article/4542563/forging-the-arsenal-of-freedom-department-of-war-suspends-cmmc-phase-ii-require/ | | 2026-09-26 browser |
| DoD Cyber Crime Center, DIBNET | Where DFARS 252.204-7012 incident reports are filed. As of 2026-09-26 it redirects to the DC3 DIB Cybersecurity page | https://dibnet.dod.mil | | 2026-09-26 browser |
| DoD CUI Program, home | Entry point; the DoD CUI marking training aid (December 2024, DOPSR 25-P-0275) | https://www.dodcui.mil/ | `reference/cui-marking-spec.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, category list and abbreviations | Categories as the DoD lists them | https://www.dodcui.mil/CUI-Categories-and-Abbreviations/ | `reference/cui-registry/CUI-Categories-and-Abbreviations.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Controlled Technical Information | CTI definition and authorities | https://www.dodcui.mil/Defense/Controlled-Technical-Information/ | `reference/cui-registry/Defense--Controlled-Technical-Information.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Export Controlled | Export Controlled category | https://www.dodcui.mil/Export-Control/Export-Controlled/ | `reference/cui-registry/Export-Control--Export-Controlled.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Source Selection | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Procurement-and-Acquisition/Source-Selection/ | `reference/cui-registry/Procurement-and-Acquisition--Source-Selection.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, General Procurement and Acquisition | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Procurement-and-Acquisition/General-Procurement-and-Acquisition/ | `reference/cui-registry/Procurement-and-Acquisition--General-Procurement-and-Acquisition.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Small Business Research and Technology | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Procurement-and-Acquisition/Small-Business-Research-and-Technology/ | `reference/cui-registry/Procurement-and-Acquisition--Small-Business-Research-and-Technology.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, General Proprietary Business Information | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Proprietary-Business-Information/General-Proprietary-Business-Information/ | `reference/cui-registry/Proprietary-Business-Information--General-Proprietary-Business-Information.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, International Agreement Information | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/International-Agreements/International-Agreement-Information/ | `reference/cui-registry/International-Agreements--International-Agreement-Information.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Operations Security | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Intelligence/Operations-Security/ | `reference/cui-registry/Intelligence--Operations-Security.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Inventions | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Patent/Inventions/ | `reference/cui-registry/Patent--Inventions.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Patent Applications | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Patent/Patent-Applications/ | `reference/cui-registry/Patent--Patent-Applications.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Secrecy Orders | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Patent/Secrecy-Orders/ | `reference/cui-registry/Patent--Secrecy-Orders.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, Information Systems Vulnerability Information | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Critical-Infrastructure/Information-Systems-Vulnerability-Information/ | `reference/cui-registry/Critical-Infrastructure--Information-Systems-Vulnerability-Information.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Registry, DoD Critical Infrastructure Security Information | Category description and authorities, for `reference/dodi-5230-24-defense-categories.md` | https://www.dodcui.mil/Defense/DoD-Critical-Infrastructure-Security-Information/ | `reference/cui-registry/Defense--DoD-Critical-Infrastructure-Security-Information.md` | 2026-09-26 browser; mirror 2026-05-13 |
| BIS, Export Compliance Guidelines: The Elements of an Effective Export Compliance Program | The eight elements of an export compliance program; what a Technology Control Plan should contain; the six fields of a foreign-national visitor record. PDF sha256 1f757636ba40f5860da631e1f7cbed4422305a98b771dfe681f70e598ce03bea | https://www.bis.gov/media/documents/export-compliance-guidelines | | 2026-09-26 script |
| DoD CUI Program, Distribution Statements | Distribution statements A to F | https://www.dodcui.mil/Distribution-Statements/ | `reference/cui-registry/Distribution-Statements.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Program, Limited Dissemination Controls | LDCs | https://www.dodcui.mil/Limited-Dissemination-Controls/ | `reference/cui-registry/Limited-Dissemination-Controls.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoD CUI Program FAQ, Use of Distribution Statements | "A distribution statement does not automatically mean the document is CUI." Quoted below | https://www.dodcui.mil/Frequently-Asked-Questions/Use-of-Distribution-Statements/ | `reference/cui-registry/Frequently-Asked-Questions--Use-of-Distribution-Statements.md` | 2026-09-26 browser; mirror 2026-05-13 |
| DoDI 5230.24, "Distribution Statements on DoD Technical Information," January 10, 2023 | Distribution statements B to F, the controlling DoD office, reason codes. The 2012 version was titled "on Technical Documents" | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf | `reference/dod-issuances/dodi-5230-24.md` | 2026-09-26 mirror |
| DoDI 5230.24, "Distribution Statements on Technical Documents," August 23, 2012, Incorporating Change 3, October 15, 2018. **Superseded** | History only: the 2012 reasons and the authority each cited (Enclosure 4, Tables 1 to 4). PDF sha256 2635ef02e96c10e7a96f0a9588cf9980ee2ed91b309bb895097ef0d554daa3a8 | https://web.archive.org/web/20201017000814/https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf |  | 2026-09-26 script |
| DoDI 5000.79, "Defense-wide Sharing and Use of Supplier and Product Performance Information (PI)" | Named by DoDI 5230.24 para 4.3.b for the Contractor Performance Evaluation category | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/500079p.pdf |  | 2026-09-26 browser |
| DoDI 2040.02, "International Transfers of Technology, Articles, and Services" | Named by DoDI 5230.24 para 4.3.e for the Export Controlled category | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/204002p.pdf |  | 2026-09-26 browser |
| DoDD 5205.02E, "DoD Operations Security (OPSEC) Program" | The DoD OPSEC program behind the Registry's Operations Security category | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/520502e.pdf |  | 2026-09-26 browser |
| DoDD 3020.40, "Mission Assurance (MA)" | DoD policy under the Registry's DoD Critical Infrastructure Security Information category | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/302040p.pdf |  | 2026-09-26 browser |
| DoD Cybersecurity FAQs on DFARS Subpart 204.73 and 239.76, July 30, 2020 rev 3 (updated 2021-12-19), Defense Pricing and Contracting | A32: "in support of the performance of the contract" does not make all information a contractor uses to perform the contract covered defense information. Quoted below. Dated: read the current DoD CIO and DPC guidance before relying on it | https://dodprocurementtoolbox.com/uploads/Cybersecurity_FAQ_update_12_19_22_ba047be683.pdf | `reference/dod-issuances/dod-cybersecurity-faq-covered-defense-information.md` | 2026-09-26 mirror |
| DoDD 5230.25, "Withholding of Unclassified Technical Data From Public Disclosure," Change 2, October 15, 2018 | The source of the DoD export-control warning wording | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/523025p.pdf | `reference/dod-issuances/dodd-5230-25.md` | 2026-09-26 mirror |
| DoDI 5200.48, "Controlled Unclassified Information (CUI)," March 6, 2020 | How the DoD implements the CUI Program; para 3.6.a, the authorized holder determines at creation whether information in a new document falls into a CUI category. Quoted below | https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/520048p.PDF | `reference/dod-issuances/dodi-5200-48.md` | 2026-09-26 mirror |
| ISOO, CUI Stakeholders Update, Q2 FY2020 (2020-02-12), slide 8 | Proprietary information a contractor creates internally and owns is not CUI. Quoted below, with a warning about the second bullet | https://isoo.blogs.archives.gov/2020/02/13/cui-q2-stakeholders-update-slides/ and https://archivescarterchronicle.wpcomstaging.com/wp-content/uploads/2020/02/CUI-Stakeholders-Q2-2020.pdf | `reference/isoo/cui-stakeholders-update-q2-fy2020.md` | 2026-09-26 mirror |
| NARA CUI Registry, category list | The authoritative list of CUI categories | https://www.archives.gov/cui/registry/category-list | | 2026-09-26 script |
| NARA CUI Marking Handbook v1.1 (2016-12-06) | Marking conventions | https://www.archives.gov/files/cui/20161206-cui-marking-handbook-v1-1.pdf | | 2026-09-26 script |
| NIST SP 800-30 Rev 1 | Risk assessment method | https://csrc.nist.gov/pubs/sp/800/30/r1/final | | 2026-09-26 script |
| NIST SP 800-40 Rev 4 | Patch management planning | https://csrc.nist.gov/pubs/sp/800/40/r4/final | | 2026-09-26 script |
| NIST SP 800-41 Rev 1 | Firewall guidance | https://csrc.nist.gov/pubs/sp/800/41/r1/final | | 2026-09-26 script |
| NIST SP 800-63B | Digital identity: authenticators and passwords | https://csrc.nist.gov/pubs/sp/800/63/b/upd2/final and https://pages.nist.gov/800-63-3/sp800-63b.html | | 2026-09-26 script |
| NIST SP 800-84 | Test, training, and exercise programs | https://csrc.nist.gov/pubs/sp/800/84/final | | 2026-09-26 script |
| NIST SP 800-88 Rev 1 | Media sanitization | https://csrc.nist.gov/pubs/sp/800/88/r1/final | | 2026-09-26 script |
| NIST SP 800-160 Vol 1 Rev 1 | Systems security engineering | https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final | | 2026-09-26 script |
| NIST CSRC glossary, "media" | Definition of media | https://csrc.nist.gov/glossary/term/media | | 2026-09-26 script |
| NIST CSRC glossary, "remote access" | Definition of remote access | https://csrc.nist.gov/glossary/term/remote_access | | 2026-09-26 script |
| FedRAMP Marketplace, Salesforce listing | The authorization status of that offering | https://www.fedramp.gov/marketplace/products/FR2003061248/ | | 2026-09-26 script |
| CISA Tabletop Exercise Packages | Tabletop exercise method | https://www.cisa.gov/resources-tools/services/cisa-tabletop-exercise-packages and https://www.cisa.gov/cisa-tabletop-exercise-packages | | 2026-09-26 script |

## Tier 3: public secondary sources

Can support a method or a practice. Never settles a status question on its own. Commercial sources are marked **commercial**.

| Source | Relied on for | URL | Mirror | Checked |
|---|---|---|---|---|
| ISOO blog, "FCI and CUI, what is the difference?" (2020-06-19) | "All CUI in possession of a Government contractor is FCI, but not all FCI is CUI." Official author, but the post says it "does not constitute CUI guidance", so it is Tier 3. Its definitions are quoted from 32 CFR 2002.4 and FAR 52.204-21; cite those instead | https://isoo.blogs.archives.gov/2020/06/19/%E2%80%8Bfci-and-cui-what-is-the-difference/ | | 2026-09-26 script |
| ComplianceForge, Unified Scoping Guide (CC BY 4.0) | Zone-based scoping method. **Commercial** | https://complianceforge.com/ | `reference/usg-zones-to-cmmc-categories.md` | 2026-09-26 script |
| `khanssen/oscal-nist-800-171r2`, "NIST SP 800-171 Rev 2 Combined OSCAL Catalog", Archstone Security LLC (CC BY 4.0), pinned to tag `v2.0-combined.1` | The OSCAL catalog every `ssp.json` references through our profile: its structure and its ids (`_03.05.03`, `_03.05.03_obj.a`). ADR-0009. An unofficial transform of NIST text, vendored with a documented patch; for what a requirement or objective says, cite NIST SP 800-171 Rev 2 and 800-171A. **Commercial** | https://github.com/khanssen/oscal-nist-800-171r2 | `reference/oscal/nist-800-171r2-catalog.json` | 2026-09-28 mirror |
| Totem Technologies, continuous monitoring plan template (MIT) | Monitoring cadence. **Commercial** | https://www.totem.tech/ | `reference/continuous-monitoring-cadence.md` | 2026-09-26 script |
| Salesforce Help, Einstein in Government Cloud | Which Salesforce features Government Cloud supports. **Commercial**; supports facts about the vendor's own product only | https://help.salesforce.com/apex/HTViewHelpDoc?id=sf.einstein_sales_considerations.htm | | 2026-09-26 script |
| DEFCERT, "Not Every Device Needs to Be FIPS Validated" (2026-06-18) | The network device decision tree for 3.13.11: decrypts, then cited in the SSP for a security function, then the four out-of-scope conditions. Also the transit versus storage caveat for cloud providers. Its FAQ citations (B-Q8, E-Q2, F-Q3, F-Q4) are cited from the FAQ itself. **Commercial** | https://www.defcert.com/blog/not-every-device-neds-to-be-fips-validated | | 2026-09-27 script |
| NDISAC DIB SCC, incident response exercises | Tabletop exercise material for the DIB. Industry association | https://ndisac.org/dibscc/implementation-and-assessment/incident-response-and-management/exercises/ | | 2026-09-26 script |
| Washington State, cybersecurity tabletop exercises | Tabletop exercise material. State government, not the regulator | https://cybersecurity.wa.gov/tabletop-exercises | | 2026-09-26 script |
| Holland and Knight alert on the CMMC Phase II suspension | Reporting on the suspension. Law firm | https://www.hklaw.com/en/insights/publications/2026/07/dow-suspends-cmmc-phase-ii-requirements | | 2026-09-26 script |
| Crowell and Moring client alert on the suspension and the 60-day review | Reporting on the suspension. Law firm | https://www.crowell.com/en/insights/client-alerts/department-of-war-immediately-suspends-cmmc-phase-ii-requirements-launches-60-day-reform-review | | 2026-09-26 script |
| Federal News Network on the suspension | Reporting on the suspension. Trade press | https://federalnewsnetwork.com/cybersecurity/2026/07/pentagon-suspends-cmmc-phase-two-requirements-launches-review-of-program/ | | 2026-09-26 script |
| ClearanceJobs on the task force tradeoffs (2026-08-17) | Reporting on the CMMC review. Trade press | https://news.clearancejobs.com/2026/08/17/will-cmmc-keep-third-party-audits-pentagon-task-force-weighs-the-tradeoffs/ | | 2026-09-26 script |
| IntelliGRC Ep. 11, "CUI, Supply Chain Flow-Downs & the Real CMMC Challenges" (2026-05-06) | "Apply 800-171 to" versus "treat as CUI"; intake-first enclave; allow-list. Timestamps in #67 | https://www.youtube.com/watch?v=PG7aZWUvVvs | | 2026-09-26 script |
| Summit 7, "Distribution Statement Deep Dive" (2024-09-12) | Good, better, best marking test; a document is a data set. Timestamps in #66 | https://www.youtube.com/watch?v=izKNPCqrhjE | | 2026-09-26 script |
| Summit 7, "How To Know If You Have CUI", CS2 talk | Method for finding CUI | https://www.youtube.com/watch?v=IEy-TkmKMt8 | | 2026-09-26 script |
| Summit 7, "CUI Basic vs CUI Specified" | Basic and Specified in practice | https://www.youtube.com/watch?v=5_AaOcYD-9w | | 2026-09-26 script |
| Summit 7, "CMMC Level 2 Assessment: What to Expect" | Assessment practice | https://www.youtube.com/watch?v=39YxwH0BZX4 | | 2026-09-26 script |
| Summit 7, "75% of the CMMC Assessment Guide Isn't Requirements" | Reading the Assessment Guide | https://www.youtube.com/watch?v=CgojtXRh9rM | | 2026-09-26 script |
| Summit 7, "C3PAO Panel: Assessor Perspectives from the Field" | Assessor practice | https://www.youtube.com/watch?v=Oxf-d6yoLsc | | 2026-09-26 script |
| Summit 7, "Fun with NIST Policy Controls" | Policy practice | https://www.youtube.com/watch?v=TXsKdH3hC6E | | 2026-09-26 script |
| Summit 7, "Identify Assets for CMMC" | Asset inventory practice | https://www.youtube.com/watch?v=kvw5uhLK2U8 | | 2026-09-26 script |
| Public panel on what primes look for in their supplier base, Summit 7 | Prime expectations | https://www.youtube.com/watch?v=KWUuHElnPhc | | 2026-09-26 script |
| Public panel on prime contractors and CMMC waivers, Summit 7 | Waivers in practice | https://www.youtube.com/watch?v=haVzS8j7Qz4 | | 2026-09-26 script |
| Public panel on a 2019 DDTC consent agreement (FLIR), Summit 7 | ITAR enforcement lessons | https://www.youtube.com/watch?v=qS44dOwoWUs | | 2026-09-26 script |
| Public panel on practical ITAR compliance steps, Summit 7 | ITAR practice for small and mid-size firms | https://www.youtube.com/watch?v=xhFX1eCHHSI | | 2026-09-26 script |
| Public interview on construction and CMMC | Three-year design horizon | https://www.youtube.com/watch?v=F5ufR0HtaA4 | | 2026-09-26 script |
| Public recap of a Cyber AB town hall | The Registered Practitioner program | https://www.youtube.com/watch?v=mIVnOkQnZg0 | | 2026-09-26 script |
| Reddit r/CMMC, public post on matching scope to data | Scoping practice. Forum | https://reddit.com/r/CMMC/comments/1t5b9t1/_/ok8mwq0/ | | 2026-09-26 script |
| Reddit r/CMMC, public post on ESP and MSP scoping | Scoping practice. Forum | https://reddit.com/r/CMMC/comments/pza6rh/_/hf0odxj/ | | 2026-09-26 script |
| Reddit r/NISTControls, public post on ESP and MSP scoping | Scoping practice. Forum | https://reddit.com/r/NISTControls/comments/pza6rh/_/hf0odxj/ | | 2026-09-26 script |
| Reddit r/NISTControls, public post on ESP scoping | Scoping practice. Forum | https://reddit.com/r/NISTControls/comments/19czouy/_/kj30ida/ | | 2026-09-26 script |
| Reddit r/NISTControls, public post on answering twice with a cloud tenant | Scoping practice. Forum | https://reddit.com/r/NISTControls/comments/kf02ft/_/gg5n41f/ | | 2026-09-26 script |

## Not sources

Links that attribute a licence, define a working term, or point at an image a skill embeds. They support no claim and have no tier. They are listed so the register check has no exceptions.

| Link | Why it is cited | URL |
|---|---|---|
| mattpocock/skills | MIT attribution for the ported flows | https://github.com/mattpocock/skills |
| mattpocock/skills, domain-modeling | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md |
| mattpocock/skills, grill-with-docs | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md |
| mattpocock/skills, research | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md |
| mattpocock/skills, wizard | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/engineering/wizard/SKILL.md |
| mattpocock/skills, grill-me | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md |
| mattpocock/skills, grilling | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md |
| mattpocock/skills, handoff | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md |
| mattpocock/skills, to-questionnaire | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/productivity/to-questionnaire/SKILL.md |
| mattpocock/skills, wait-what | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/productivity/wait-what/SKILL.md |
| mattpocock/skills, writing-for-agents | Port attribution | https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md |
| draw.io Azure stencil, Entra ID icon | Image the boundary diagram embeds | https://app.diagrams.net/img/lib/azure2/identity/Azure_Active_Directory.svg |
| draw.io Azure stencil, Intune icon | Image the boundary diagram embeds | https://app.diagrams.net/img/lib/azure2/intune/Intune.svg |
| draw.io Azure stencil, Defender icon | Image the boundary diagram embeds | https://app.diagrams.net/img/lib/azure2/security/Azure_Defender.svg |
| draw.io Microsoft Fabric stencil, Purview icon | Image the boundary diagram embeds | https://icons.diagrams.net/assets/microsoft-fabric/1/Microsoft_Purview.svg |
| AI Hero dictionary, "smart zone" | Defines a term used in the phase boundary guidance | https://www.aihero.dev/ai-coding-dictionary/smart-zone |

## Quoted text for CUI status rules

These are the passages the repo relies on to state a CUI status rule, quoted exactly.

**32 CFR 2002.4(h).** "Controlled Unclassified Information (CUI) is information the Government creates or possesses, or that an entity creates or possesses for or on behalf of the Government, that a law, regulation, or Government-wide policy requires or permits an agency to handle using safeguarding or dissemination controls. However, CUI does not include classified information (see paragraph (e) of this section) or information a non-executive branch entity possesses and maintains in its own systems that did not come from, or was not created or possessed by or for, an executive branch agency or an entity acting for an agency."

**ISOO, CUI Stakeholders Update Q2 FY2020, slide 8.** Under "Is my Proprietary Information CUI?": "The government will protect it as CUI (and may even send it back to you as CUI) but the proprietary information you create internally and maintain ownership of is not CUI (though it may require protections pursuant to other laws or regs)."

The same slide says "Information should always be protected in accordance with the requirements in the contract under which it was produced or received." That sentence answers a different question on the slide, about legacy markings such as FOUO and SBU. Do not cite it as ISOO's answer on proprietary information.

**DoD CUI Program FAQ, Use of Distribution Statements.** "The application of a distribution statement does not automatically mean the document is CUI. Do not confuse the two issues."

**81 FR 63324, 63334 (preamble to the CUI final rule).** "A document containing CUI that is derived from another document that contains CUI would also be CUI--because it contains controlled information, not simply because it is derived from a document that contains CUI. It is possible the original document contains both CUI and non-CUI and the derived document could therefore contain only information derived from the non-CUI portions of the original document. In such a case, the derived document would not become CUI simply because the information was derived from a CUI document."

**32 CFR 2002.4(pp).** "Re-use means incorporating, restating, or paraphrasing information from its originally designated form into a newly created document."

**32 CFR 2002.4(ee).** Misuse of CUI "may also include designating or marking information as CUI when it does not qualify as CUI."

**DoDI 5200.48, para 3.6.a.** "The authorized holder of a document or material is responsible for determining, at the time of creation, whether information in a document or material falls into a CUI category. If so, the authorized holder is responsible for applying CUI markings and dissemination instructions accordingly."

**DoD Cybersecurity FAQs, A32.** "It is meant to include any covered defense information used in performance of the contract and exclude other information that may be developed by the contractor but not associated with contract performance. It does NOT mean that all information used by the contractor to support contract performance, e.g., information in the contractor's human resources or financial/accounting systems, is considered to be covered defense information."
