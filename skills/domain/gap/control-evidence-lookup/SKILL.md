---
name: control-evidence-lookup
description: Answer "what satisfies 3.x.y" or "will this evidence pass" for any NIST SP 800-171 Rev 2 requirement. Returns what assessors have accepted, what they have rejected, what is over-engineering, the open edge cases, and evidence examples, with assessor disagreement preserved and thin requirements marked low confidence. Use whenever a requirement id is named and the question is about the bar.
vault_sources:
  - "3.1.1 through 3.14.7 (all 110 per-requirement pages)"
  - "raw/{AC,AT,AU,CA,CM,IA,IR,MA,MP,PE,PS,RA,SC,SI}.L2-3.y.z.md"
public_sources:
  - "CMMC Level 2 Assessment Guide, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "NIST SP 800-171A: https://csrc.nist.gov/pubs/sp/800/171/a/final"
  - "32 CFR 170.24: https://www.ecfr.gov/current/title-32/section-170.24"
---

# Control evidence lookup

The flagship of the domain layer. For any of the 110 requirements it answers one question: **where is the bar?** What has been accepted at assessment, what has been rejected, what is spending past the bar, what is still contested, and what artifact to hand over. It does not decide scope, it does not write SSP statements, and it does not compute a score; it feeds the skills that do.

## Inputs

- A requirement id (`3.1.1`) or a family (`AC`) or a question that names one ("will an Entra user export pass 3.1.1?").
- Optionally, the engagement's current state, so the answer can be applied rather than generic: the folder `evidence/3.x.y/`, and the record, for the requirement's statements in the frontmatter of `ssp/<requirement>.md` and the components and assets they describe in `ssp/components/*.md`. Read the files directly. Never read `view/` instead; it is generated for people and can be stale.

## Method

1. Open `controls/<id>.md`. Read the frontmatter first: `points`, `poam_eligible`, and `confidence`. If `confidence: low`, say so before anything else; the answer is the Assessment Guide plus little more, and the operator should not build on it without a second source.
2. Answer in the four buckets, in this order, quoting the file's bullets and keeping the objective letters: **Accepted** (Sufficient), **Rejected** (Insufficient), **Over-engineering**, **Open edge cases**. Then **Evidence examples**.
3. Preserve disagreement. Where a bullet ends "the outcome depends on the assessor", say that in the answer and name both positions. Do not pick one.
4. If the operator supplied a proposed implementation or artifact, place it: which bucket it falls in, which objectives it covers, which it leaves open, and the cheapest accepted alternative if it is over-engineering. Call the Skill tool with `over-engineering-guard` when the proposal is past the bar and money is involved.
5. If the operator supplied the engagement state, map each objective letter to the evidence present, and name the objective letters with nothing behind them. That output is the shape `audit` uses.
6. End with the related requirements from the file, so the operator sees the stack (for example 3.1.12 through 3.1.15 as one remote-access process).

## Output

```markdown
## 3.x.y <title> (points: n, POA&M eligible: yes/no, confidence: high/medium/low)

### Accepted
- ...

### Rejected
- ...

### Over-engineering
- ...

### Open edge cases
- ...

### Evidence examples
- ...

### Applied to this engagement (only when state was supplied)
| Objective | Evidence present | Gap |
|---|---|---|

### Related
- ...
```

Write nothing to the engagement repo; this skill answers. `audit` and `to-ssp` write.

## Where practitioners disagree

Disagreement lives inside each control file's Edge cases. The recurring ones: whether a VPN counts as remote access under 3.1.12; whether a TPM-backed PIN counts as two factors under 3.5.3; how 3.13.4 and 3.13.5 read at different assessors; the printer category. Each file states both positions; the outcome depends on the assessor.

## Seat notes

**OSC seat**: read the Accepted bucket first and stop there unless something in Rejected describes what you already do. **Consultant seat**: read Edge cases first for anything you will have to argue, and put contested positions on the pre-engagement question list for the C3PAO (`c3pao-selection-vetting`).

## Sources

The control files: [CONTROL-FILE-FORMAT.md](CONTROL-FILE-FORMAT.md) and `controls/`. Each file carries its own `public_sources` and `vault_sources`. Practitioner consensus, unattributed, backs the Accepted and Rejected buckets wherever a bullet carries no public citation.
