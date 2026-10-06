---
name: ssp-lint
description: "Review the SSP on two axes: house style (does every objective carry a statement in the required form?) and evidence (does every claim match the supporting document and the evidence folder?). Runs both as parallel subagents and reports them side by side."
---

Two-axis review of the engagement's SSP, or of the part of it the operator names.

- **House style**: does every assessment objective carry a statement, in the form this repo requires?
- **Evidence**: does every claim match the document that backs it and the artifacts in the evidence folder?

Both axes run as **parallel subagents** so neither pollutes the other's context, then this skill reports them side by side.

## Why two axes

An SSP can pass one and fail the other.

- Every objective has a well-formed statement, and one of them claims a lockout threshold the procedure contradicts. House style passes, evidence fails.
- Every claim is true and backed, and three objectives have no statement at all because one narrative covers the whole requirement. Evidence passes, house style fails.

Reporting them separately stops one from masking the other. Do not merge or rerank the findings.

## Spend the corrections where they count

Many assessors allow only a handful of document corrections during an assessment. A contradiction between the SSP and a supporting document is the cheapest kind to find now and the most expensive to find then, because it costs a correction and it invites the assessor to look harder at everything else. That is what this skill is for.

## Process

### 1. Pin the scope

Whatever the operator named: one requirement, one family, or the whole SSP. Default to the whole SSP. The SSP is the record, the `ssp/` folder (ADR-0012). Read it directly for that scope: one requirement is `ssp/3.5.3.md`, a family is `ssp/3.5.*.md`, and everything is all 110 requirement files. Each requirement file's frontmatter holds its statements under `objectives`, by letter, each with its component's slug, status, statement, and remarks. The components, the providers, and the assets with their categories are in `ssp/components/`, whatever the scope. Never read `view/` instead; the view is generated for people and can be stale.

Then run scribe's check over the whole record, which only reads it: `python3 <path to the scribe skill>/check_ssp.py .` from the engagement repo. It prints `check_ssp: ok` and a count, or one line per problem, naming the file and, for a statement, the objective.

If every objective in scope is still planned on `this-system` with "Not yet written.", nothing has been written yet. That is a job for `/to-ssp`, not a lint finding.

### 2. Gather the sources both axes need

- The record for the scope: the requirement files, and every file in `ssp/components/`.
- The check's output, as it came back.
- `evidence/` for the artifacts.
- `policies/` for the procedures and policies the statements name.
- `scope/open-items.md` for the facts still waiting on someone.
- `CONTEXT.md` for the glossary and the seat.

### 3. Spawn both subagents in parallel

**House style subagent.** Give it the record for the scope, the check's output, and this brief:

> Report, per requirement: (a) every assessment objective with no statement, meaning its only entry is `this-system` planned with "Not yet written.", or a component's entry is planned with "Not yet written.", a cleared statement that component still owes, naming the letter; (b) every statement containing "to be confirmed", "TBD", "as applicable", "where appropriate", or a future tense promise, quoting it; (c) every statement whose text is about a different component than the one it is recorded on, quoting it and naming both; (d) every statement whose status contradicts its own text, such as implemented where the text says something is missing, or not applicable or alternative where the remarks do not give the reason; (e) every requirement where one narrative is copied across several objectives, or one statement answers objectives it is not recorded on, rather than one statement per objective; (f) every place the definition and enforcement pattern is not applied, meaning the organization-wide decision is restated per component instead of stated once at the objective that asks whether it is defined. Quote the statement for each finding, with its objective in `3.5.3[a]` form and its component. Under 500 words.
>
> Then report every problem line in the check's output, once each, whatever the scope: the check covers the whole record, and each line is a hand edit to put right. Quote the line, then say in the operator's words what it means for the SSP an assessor reads, not the rule it breaks. A statement on a component the record does not have describes nothing in the system, so the objective reads as answered by a thing nobody can point to. An asset whose category contradicts its component's leaves the inventory and the statements disagreeing about how that asset is assessed. A category outside the five is not a category an assessor recognizes. An Out-of-Scope Asset with no justification is the first thing an assessor asks about. An alternative or not applicable statement with no reason is a claim with nothing behind it. Say that someone edited the record by hand, since scribe refuses every one of these, and that the fix is to record it again through scribe.

**Evidence subagent.** Give it the record for the scope, the policies, the evidence folder listing, and this brief:

> Report, per requirement: (a) every statement that contradicts a policy or procedure in `policies/`, another statement in the record, or the category or justification the record gives an asset, quoting both sides, for example an SSP saying accounts lock after five attempts where the procedure says three, and every justification or statement that cites a policy `policies/` does not hold; (b) every statement naming an artifact that is not in `evidence/<id>/`; (c) every statement on a company component claiming work that the record puts on a provider's component, and every company statement that relies on a provider when the provider's component carries no statement on that objective; (d) every statement that is a claim with no artifact behind it where the objective asks for a practice rather than a document; (e) every artifact that appears to be a draft or a working paper rather than final. Quote the statement, with its objective and component, and the source line for each finding. Under 500 words.

### 4. Report

Present the two reports under `## House style` and `## Evidence`, verbatim or lightly cleaned. End with one line: the count per axis and the worst finding within each axis. Do not pick a single winner across axes.

**Count findings, not requirements and not statements.** One finding is one thing to fix. A single rule broken the same way across every requirement is one systemic finding, reported once with the count of requirements it touches, not one finding per requirement: "no requirement has one statement per objective, 26 of 28 affected" beats twenty-six identical entries, which bury the specific problems underneath them. A contradiction between one statement and one document is its own finding, every time.

### 5. List the unverified text

For every "to be confirmed" the house style axis found, do the thing the rule exists for (ADR-0010): add the fact to `scope/open-items.md` as one line naming the fact, the objective in `3.5.3[a]` form, and who can confirm it, creating the file if it does not exist, and show the operator the line. The statement itself still carries the admission until it is written again, and this skill does not write statements: name each one, with its objective and component, as the first thing for `ssp-statement-writer`. Name it and the finding only; which objective and component the rewritten statement belongs on, and its status, is that skill's call, not the lint's. An SSP that ships with an admission inside a statement has told the assessor where to look.

## What this skill does not do

It does not decide whether an objective is MET. That is `/audit`, which reads the evidence against what assessors have accepted. The lint checks the document against itself and against the repo, which is a cheaper and narrower question.

It does not write statements, and it never changes the record: it only reads the files and runs the check, which reads them too. It reports what is wrong with the statements, and `/to-ssp` or `ssp-statement-writer` fixes them.

## Sources

- The statement rules: call the Skill tool with `ssp-statement-writer`.
- 32 CFR 170.24(c)(2)(i)(5), the consequence of an absent or incomplete SSP: `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24)
- NIST SP 800-171A, the objective letters: https://csrc.nist.gov/pubs/sp/800/171/a/final

Rewritten from `code-review` in mattpocock/skills (MIT, see `skills/flows/LICENSE-mattpocock`). The two-axis structure, the parallel subagents, and the refusal to rerank across axes are kept. Standards becomes house style, and spec becomes evidence.
