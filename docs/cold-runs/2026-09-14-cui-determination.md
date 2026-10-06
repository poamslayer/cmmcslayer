# Cold run: cui-determination-workflow and derivative-cui-triage

Date: 2026-09-14. Skills under test: `skills/domain/cui/cui-determination-workflow` and `skills/domain/cui/derivative-cui-triage`. Tester: a fresh agent given only the two SKILL.md files and the fixture company documents. The answer key was withheld.

## Prompt

Determine the status of the fixture's ten documents, giving the status, the reason, and the step that produced it. Then produce the skills' output artifacts.

## First run: FAIL

| Check | Score | Evidence |
|---|---|---|
| Shape match | 2 | Both output artifacts produced in the right shape, with an open items list. |
| Known-answer match | 0 | Seven of ten matched. Two differed and one was incomplete, and the rubric scores two or more differences as zero. |
| Scrub check | 2 | Clean. |

Total 4 of 6 with a zero. Fail.

### What differed, and why each was a real defect

**The g-code, the important one.** The answer key says derivative CUI, because the toolpaths reproduce the customer's geometry and the shop does not own the design. The tester returned "potentially CUI, pending export classification" and stopped, because the skill's g-code chain ran export classification first and the fixture supplies no explicit classification. The tester was following the skill correctly. The skill was wrong.

Ownership and export are two different questions. Ownership decides whether something is CUI. Export decides whether it is also export controlled. Putting export first meant an operator who could not answer it never reached the ownership test that settles the CUI question on its own, which contradicts the ownership-first principle the rest of the skill is built on. The chain now runs ownership first and treats export as the overlay it is. It also says what counts as an answer to the classification question: an explicit classification is the strong form, a customer's own export warning plus a Controlled Technical Information designation block is a usable working answer that must be recorded as resting on the customer's marking, and an unresolved export question never blocks a determination ownership already made.

**The purchase order to the finisher.** The answer key says the purchase order is not itself CUI, but it transmits CUI, because the drawing was attached. The tester marked the whole thing CUI. It also reported, correctly, that the skill's intake procedure covers only incoming packages and gives no rule for what the shop sends outward. Added as its own step: triage the document and what travels with it separately, because "this purchase order is CUI" tells nobody what to fix, while "not CUI, but it transmitted the drawing to a supplier with no release path" names the actual problem and routes it.

**Federal Contract Information was missing entirely.** The answer key labels the quote and the clause page as FCI. Neither skill mentioned FCI, so the tester could only say "not CUI", which loses the fact that those documents still carry the fifteen basic safeguarding requirements and drive Level 1. Both skills now name FCI as the residual category, and the determination output allows it.

## Second run: PASS

Same prompt, same withheld answer key, fresh tester, against the corrected skills.

| Check | Score | Evidence |
|---|---|---|
| Shape match | 2 | Ten determinations in the table shape, each naming the numbered step that produced it. |
| Known-answer match | 2 | Ten of ten. The g-code resolved as derivative CUI on the ownership branch without touching the export chain. The finisher purchase order returned the two-part answer: the document is not CUI, and the drawing attached to it is a CUI flow needing a release path. The quote and the clause page came back labelled FCI. |
| Scrub check | 2 | Clean. |

Total 6 of 6. Pass.

### One more gap, also fixed

The tester reported that it had to keep the finisher purchase order's two answers apart, as the skill now demands, while the output table had only one status cell per row. Correct, and the format was fighting the rule. The table gained a **Carries CUI with it** column, so the document's own status and what travels attached to it are separate answers, and the row list gained the document types the fixture exposed: an outbound package, a quote, and a customer clause page.

## Finding

The tester's reasoning was sound in all three cases. It followed the skills as written and reported the two places they gave it nowhere to go. A cold run that fails this way is worth more than one that passes: each of the three gaps would have reached a real engagement, and the g-code one would have stalled the most contested determination a machine shop has to make.
