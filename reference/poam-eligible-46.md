> **Provenance.** Derived in this repository from 32 CFR 170.21(a)(2) (POA&M conditions) and 32 CFR 170.24(c)(2) (Level 2 scoring), both public domain; see `reference/32-cfr-170-21-poam-gates.md` and `reference/32-cfr-170-24-scoring.md`. The derivation is arithmetic over the regulation's own lists and is reproduced by `reference/nist-800-171r2-requirements.json`. Licence: MIT (this repository).

# POA&M-eligible Level 2 requirements

A requirement may sit on a Plan of Action and Milestones for a Conditional Level 2 status only when all three conditions in 32 CFR 170.21(a)(2) hold: the score is at least 0.8 of the maximum (88 of 110), the requirement is worth 1 point (with the single exception below), and the requirement is not one of the six named in 170.21(a)(2)(iii).

## The arithmetic

| Bucket | Count | Basis |
|---|---|---|
| 5-point requirements | 42 | 170.24(c)(2)(i)(B)(1) |
| 3-point requirements | 14 | 170.24(c)(2)(i)(B)(2) |
| Adjustable requirements (3.5.3, 3.13.11) | 2 | 170.24(c)(2)(i)(B)(4) |
| 1-point requirements | 52 | 170.24(c)(2)(i)(B)(3), all remaining |
| Total | 110 | |
| 1-point requirements never eligible | 6 | 170.21(a)(2)(iii) |
| **1-point requirements eligible** | **46** | 52 minus 6 |

Plus one requirement above 1 point: 3.13.11, only when encryption is employed but not FIPS-validated (3 points). When encryption is not employed at all (5 points) it is not eligible. 3.5.3 is scored 3 or 5 and is never eligible.

## The 46 eligible 1-point requirements, by family

| Family | Requirements |
|---|---|
| AC | 3.1.3, 3.1.4, 3.1.6, 3.1.7, 3.1.8, 3.1.9, 3.1.10, 3.1.11, 3.1.14, 3.1.15, 3.1.21 |
| AT | 3.2.3 |
| AU | 3.3.3, 3.3.4, 3.3.6, 3.3.7, 3.3.8, 3.3.9 |
| CM | 3.4.3, 3.4.4, 3.4.9 |
| IA | 3.5.4, 3.5.5, 3.5.6, 3.5.7, 3.5.8, 3.5.9, 3.5.11 |
| IR | 3.6.3 |
| MA | 3.7.3, 3.7.6 |
| MP | 3.8.4, 3.8.5, 3.8.6, 3.8.9 |
| PE | 3.10.6 |
| RA | 3.11.3 |
| SC | 3.13.3, 3.13.4, 3.13.7, 3.13.9, 3.13.10, 3.13.12, 3.13.13, 3.13.14, 3.13.16 |

## The six 1-point requirements that are never eligible

| Family | Requirements |
|---|---|
| AC | 3.1.20, 3.1.22 |
| CA | 3.12.4 |
| PE | 3.10.3, 3.10.4, 3.10.5 |

## 5-point requirements (never eligible)

| Family | Requirements |
|---|---|
| AC | 3.1.1, 3.1.2, 3.1.12, 3.1.13, 3.1.16, 3.1.17, 3.1.18 |
| AT | 3.2.1, 3.2.2 |
| AU | 3.3.1, 3.3.5 |
| CA | 3.12.1, 3.12.3 |
| CM | 3.4.1, 3.4.2, 3.4.5, 3.4.6, 3.4.7, 3.4.8 |
| IA | 3.5.1, 3.5.2, 3.5.10 |
| IR | 3.6.1, 3.6.2 |
| MA | 3.7.2, 3.7.5 |
| MP | 3.8.3, 3.8.7 |
| PE | 3.10.1, 3.10.2 |
| PS | 3.9.2 |
| RA | 3.11.2 |
| SC | 3.13.1, 3.13.2, 3.13.5, 3.13.6, 3.13.15 |
| SI | 3.14.1, 3.14.2, 3.14.3, 3.14.4, 3.14.6 |

## 3-point requirements (never eligible)

| Family | Requirements |
|---|---|
| AC | 3.1.5, 3.1.19 |
| AU | 3.3.2 |
| CA | 3.12.2 |
| MA | 3.7.1, 3.7.4 |
| MP | 3.8.1, 3.8.2, 3.8.8 |
| PS | 3.9.1 |
| RA | 3.11.1 |
| SC | 3.13.8 |
| SI | 3.14.5, 3.14.7 |

## Closeout

A POA&M must be closed out by a POA&M closeout assessment within 180 days of the Conditional CMMC Status Date (32 CFR 170.21(b)). The closeout covers only the requirements that were on the POA&M. A POA&M does not make a requirement MET; every requirement on it is scored NOT MET until closed (32 CFR 170.24(c)(2)(i)(6)).
