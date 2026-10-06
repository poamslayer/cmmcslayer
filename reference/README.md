# reference

Public-domain and openly licensed artifacts that skills cite by relative path instead of restating. Every file starts with a provenance header naming the public source, the retrieval date, and the licence. Nothing here derives from a private source.

| File | Source | Licence |
|---|---|---|
| nist-800-171r2-requirements.json | NIST SP 800-171 Rev 2 and 800-171A, via the CMMC Level 2 Assessment Guide | US Government work, public domain |
| nist-800-171r2-to-800-53r4-crosswalk.md | NIST SP 800-171 Rev 2, Appendix D | US Government work, public domain |
| 32-cfr-170-24-scoring.md | eCFR, 32 CFR 170.24 | Public domain |
| 32-cfr-170-21-poam-gates.md | eCFR, 32 CFR 170.21 | Public domain |
| poam-eligible-46.md | Derived from 170.21 and 170.24 | This repo, MIT |
| usg-zones-to-cmmc-categories.md | ComplianceForge Unified Scoping Guide, https://complianceforge.com/ | CC BY 4.0, attribution in file |
| cui-marking-spec.md | DoD CUI marking training aid, 2024 | US Government work, public domain |
| continuous-monitoring-cadence.md | Totem continuous monitoring plan template, https://www.totem.tech/ | MIT, notice in file |
| cui-registry/ | dodcui.mil registry mirror | US Government work, public domain |
| oscal/ | The pinned Rev 2 OSCAL catalog from https://github.com/khanssen/oscal-nist-800-171r2 with our documented patch, our profile of all 110 requirements, and the constraints file for our namespace. Provenance and patch in `oscal/README.md` | Catalog CC BY 4.0, Archstone Security LLC, attribution in `oscal/README.md`; NIST text public domain; profile and constraints this repo, MIT |
| authorities.md | The register of every cited source, with its tier (ADR-0004) | This repo, MIT |
| dod-issuances/ | Text of DoDI 5230.24, DoDD 5230.25, and DoDI 5200.48 from esd.whs.mil, which refuses scripted requests | US Government work, public domain |
| dodi-5230-24-defense-categories.md | Derived from DoDI 5230.24 para 4.3 (2023), the 2012 edition's reason tables, and the DoD CUI Registry: each defense category, its authority, and a test | This repo, MIT |
| isoo/ | Text of the ISOO CUI Stakeholders Update slides, Q2 FY2020, from a WordPress staging host | US Government work, public domain |

Files here reproduce their sources, so they keep the source's own punctuation and wording, including em dashes that the rest of the repo's prose avoids. `nist-800-171r2-requirements.json` is the machine-readable index the setup scaffold and the scoring skills read: one object per requirement with its id, family, title, point value, POA&M eligibility, the requirement statement, and every 800-171A objective with its letter. It holds all 110 requirements and 320 objectives. For the 12 requirements that are also Level 1 practices (3.1.1, 3.1.2, 3.1.20, 3.1.22, 3.5.1, 3.5.2, 3.8.3, 3.10.1, 3.13.1, 3.14.1, 3.14.2, 3.14.5), the index first carried the Level 1 practice wording, which says "information system" and, in 3.1.22 and 3.8.3, FCI where NIST says CUI. On 2026-09-26 those statements and the five FCI objectives were corrected to the text of NIST SP 800-171 Rev 2 and SP 800-171A, and every other entry was compared against 800-171A and matched.
