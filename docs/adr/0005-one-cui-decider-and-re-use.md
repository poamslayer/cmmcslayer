# ADR-0005: One skill decides CUI status, and re-used CUI replaces derivative CUI

Date: 2026-09-26. Status: accepted. Issue #58, map #74.

## Context

Two skills answered "is this document CUI?" and they disagreed. `cui-determination-workflow` tested ownership first. `derivative-cui-triage` skipped that test and gave a table that already said "contaminated, treat as CUI" for the sketch, the traveler, and the inspection report. When `/find-cui` called both, the concrete table won. A test run on a build-to-print shop put nine of the shop's own document types into CUI, and the right answer was two. Calling the NC programs CUI pulled the machine tools, the USB sticks, and every machine control into scope on its own.

The word "derivative" was the other half of the problem. It comes from derivative classification in the classified world, where status follows the content into every new document. CUI is not a classification system. The regulation's word is re-use (32 CFR 2002.4(pp)), and the preamble to the 2016 final rule says a derived document is CUI "because it contains controlled information, not simply because it is derived from a document that contains CUI" (81 FR 63324, 63334).

## Decision

1. **Only `cui-determination-workflow` decides whether information is CUI.** It holds the ownership gate, the re-use test (is this document CUI because of the content it carries, never because of the document it came from), the holder's duty to check a new document at creation (DoDI 5200.48 para 3.6.a), and the warning that marking something CUI when it does not qualify is misuse (32 CFR 2002.4(ee)).
2. **`derivative-cui-triage` becomes `cui-re-use-triage`, and it decides nothing.** It covers any industry. It walks the documents a company creates from CUI it received, asks the questions that separate re-used CUI from the company's own work, and sends each document to the workflow for its status. The build-to-print machine shop is its first worked example.
3. **"Derivative CUI" is retired as a term,** along with "contaminated" and "inherits the source's status." The glossary term is **Re-used CUI**.
4. **An unclear item is recorded as "potentially CUI, notice sent".** The operator decides a status on the evidence, writes down the reasoning, notifies the customer in writing (32 CFR 2002.50(a): a holder "should notify the disseminating agency"), and protects the item as CUI while the notice is open. Silence after a reasonable window accepts the notice. No separate "contested" status.

   *Amended 2026-09-26 (#67, PR #84):* this decision originally said to ask the customer and record "pending customer response". Practitioner evidence showed an open question to a prime usually gets no answer or "treat it all as CUI", and the regulation's verb is notify, so the operator now decides and notifies.

## Considered options

- **Fix `derivative-cui-triage` in place and keep both deciders.** Rejected. Two sources of truth for one rule is the root cause, and they would drift again.
- **A new general skill for documents a company creates, alongside the workflow.** Rejected. That makes three CUI skills that can each give a verdict.
- **"Only the government decides what is CUI", the common practitioner framing.** Rejected as the skill's rule. DoDI 5200.48 para 3.6.a makes the authorized holder responsible for determining, at creation, whether a document contains information in a CUI category. The rule the skills carry is that the holder checks the content, and must not mark by ancestry.

## Consequences

The fixture's answer key is re-graded under the re-use test. The g-code whose toolpaths trace the drawing is where practitioners genuinely split, so its row prefers "not CUI, export-controlled, proprietary (own)" and grades the reasoning. A reasoned "potentially CUI" passes, and "CUI because it came from the drawing" fails.
