# Cold run: endpoint-and-vdi-scoping

Date: 2026-09-28. Skill under test: `skills/domain/scoping/endpoint-and-vdi-scoping`, after it began recording through scribe (#101). Three runs, each on a fresh copy made by `python3 scripts/cold_run.py`. Each tester got the SKILL.md, scribe's folder (the skill cannot write the record without it), the scratch engagement, and the fixture company files. The answer key and the rubric were withheld, and every other skill was unavailable. A second agent graded each run without seeing the SKILL.md.

## Prompt

"Go through every endpoint and remote connection at Saguaro: the office PCs, the shop PC, anybody working from home, phones. Tell me which are in scope and record them. The old inventory in the repo was the previous consultant's and may be wrong or missing things. Use the company files as what we know." Runs 2 and 3 added "don't stop to ask me, just record and show me the table at the end" and "We haven't picked a Wi-Fi posture", because no operator was live to confirm the table.

## Result

| Check | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Shape match | 2 | 2 | 2 |
| Known-answer match | 2 | 1 | 2 |
| Scrub check | 2 | 2 | 2 |
| Record validity | 2 | 2 | 2 |
| Record match | 2 | 2 | 2 |
| Total | 10 | 9 | 10 |

All three pass. Run 3 was made on the skill as committed.

Every run changed the record only through scribe: each grader re-rendered `view/` from the run's `ssp.json` with scribe's renderer and found it identical, and `scripts/check_record.py` passed the record. No run wrote or edited a Markdown inventory. Scribe refused nothing.

Run 3's record changes against the fixture, from `check_record.py --baseline`: SHOP-PC-01 from Specialized Asset (OT) to CUI Asset; the personal phones from Out-of-Scope Asset to CUI Asset; a new component, Personal home computers, holding Dana's home PC and Maria's home laptop as CUI Assets, the first with the VPN plus RDP path named as remote access under 3.1.12[b], the second with the personal Gmail flow named as unauthorized and to be stopped; remarks on each of the nine office endpoints. Nothing else changed. The Wi-Fi posture went to `scope/open-items.md` as undecided, with the options.

## What the runs found, and what changed

**Run 1 found eleven gaps in the skill.** Each is now in it: a rule for an ordinary in-office endpoint (step 0, the P/S/T test); more than one test per row; remote access types for vendor remote support and for an unauthorized flow; unverified facts go to the open items list, not the remarks; no row for guest devices; the old Markdown inventory is a list of candidates; the table is shown to the operator before scribe records it; and assets outside the skill's lane are handed on, not recategorized. Run 1 had corrected MFP-FRONT, a printer, on the way.

**The key's "CRMA at minimum" for personal phones was weaker than the fixture.** The run and its grader both placed the phones as CUI Assets: the company diagram shows MFP scans emailed to them, drawings go out by email that staff read there, and no policy keeps CUI off them, which is the condition a CRMA needs (32 CFR 170.19(c)). 6.2 and 6.14 now say either passes and CUI Asset is better supported. 6.2's "8 office endpoints" label, which names nine, was corrected, and 6.14 now says a change outside a skill's row passes when it agrees with 6.2.

**Run 2 lost a point for calling the g-code CUI.** It said the g-code carries the drawing's geometry, against 6.1, which reasons that it re-uses no drawing content. The categories stood on other facts. Every scoping run so far had made the same move, so both scoping skills now take CUI status from `scope/cui-determinations.md` and put an undetermined item on the open items list rather than decide it. Run 3 did exactly that and recorded its categories on facts that hold either way. Run 2 also asked what category a device on an unauthorized flow takes and whether the shop-floor PC is this skill's; both are now answered.

**The CRMA rule was aligned with the regulation.** The first text said an endpoint that can reach CUI is at least a CRMA. A CRMA is an asset that can reach CUI but is not intended to, because of policy, procedures, and practices in place (32 CFR 170.19(c)); with none in place it is a CUI Asset. Both scoping skills now say so.

## Left as found

- The company files disagree on how often Maria used her personal Gmail: the IT write-up describes a habit, the FAI report one occasion. It does not change a category.
- Scribe has no field for the test that decided a placement, the remote access type, or a provisional category; all three live in remarks. The list of permitted remote access types for 3.1.12[b] is a conformity statement for `to-ssp` (#103).
- The hops table makes every in-office endpoint that reaches Microsoft 365 a remote access endpoint. Run 3 applied it literally. That reading is the skill's existing position and not something this change altered.
