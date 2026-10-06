# Control file format

One file per NIST SP 800-171 Rev 2 requirement under `controls/`, named `3.x.y.md`. The audit flow, `over-engineering-guard`, and `evidence-package-builder` all read these files, so the shape is fixed.

## Frontmatter

```yaml
---
requirement: "3.1.1"
family: AC
title: "Authorized Access Control"
points: 5            # 1, 3, or 5 per 32 CFR 170.24(c)(2); "3 or 5" for 3.5.3 and 3.13.11
poam_eligible: false # true only for 1-point requirements outside the six prohibited, plus the 3.13.11 three-point case
confidence: high     # high, medium, or low; low means the source page was thin and the file is not padded
as_of: "2026-09-13"
vault_sources:
  - "3.1.1"
  - "raw/AC.L2-3.1.1.md"
public_sources:
  - "CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.1: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "NIST SP 800-171A, 3.1.1: https://csrc.nist.gov/pubs/sp/800/171/a/final"
---
```

## Body

Eight `##` sections in this order. Keep every section, even when it says "No documented position; see confidence".

1. **Requirement**: the security requirement statement, quoted from NIST SP 800-171 Rev 2.
2. **Objectives**: the 800-171A objectives as a list, each on one line, `[a] ...`, quoted. These letters are what the audit reports against.
3. **Sufficient**: what assessors have accepted. One bullet per accepted implementation or artifact, bold lead, then the reason, then which objective letters it satisfies in brackets. Concrete artifacts, not categories.
4. **Insufficient**: what assessors have rejected, same shape, with the reason it fails and the objective it fails.
5. **Over-engineering**: what costs money and satisfies no objective, with the objective-based reason and the cheaper thing that does satisfy it.
6. **Edge cases**: the unresolved or situation-dependent questions. Where assessors disagree, state both positions and end the bullet with "the outcome depends on the assessor".
7. **Evidence examples**: concrete artifacts an assessor has taken, one per bullet, with the objective letters each covers.
8. **Related requirements**: the requirements this one stacks with, and one line each on how.

## Rules

- Restate every rule in your own words. Never copy a sentence from the source page. No names, no handles, no community references. Where the only backing is private practitioner consensus, write "practitioner consensus" or "assessors have accepted this in practice" and nothing more.
- Cite the Assessment Guide's Discussion or Examples by requirement id when a rule comes from there; cite the eCFR by section for scoring and POA&M facts.
- Failure-rate facts (top-failed lists) may be stated only with a public citation.
- Rev 3 deltas may be mentioned in Edge cases when the source page names one; never restate Rev 3 control text.
- `confidence: low` files keep every section; thin sections say "No documented position beyond the Assessment Guide; see confidence." Do not pad.
- No em dashes.
