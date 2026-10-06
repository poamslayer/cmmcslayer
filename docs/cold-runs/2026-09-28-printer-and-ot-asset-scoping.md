# Cold run: printer-and-ot-asset-scoping

Date: 2026-09-28. Skill under test: `skills/domain/scoping/printer-and-ot-asset-scoping`, after it began recording through scribe (#102). One run on a fresh copy made by `python3 scripts/cold_run.py`. The tester got the SKILL.md, scribe's folder (the skill cannot write the record without it), the scratch engagement, and the fixture company files. The answer key and the rubric were withheld, and every other skill was unavailable. A second agent graded the run without seeing the SKILL.md.

## Prompt

"Go through the printers, the copier, and everything on the shop floor at Saguaro: the Haas, the CMM, anything attached to them. Categorize them and record them. The previous consultant's inventory is in the repo and may be wrong or missing things. Use the company files as what we know; nobody at Saguaro can be asked today, and they haven't picked a printer position. Don't stop to ask me, just record and show me the table at the end."

## Result

| Check | Score |
|---|---|
| Shape match | 2 |
| Known-answer match | 2 |
| Scrub check | 2 |
| Record validity | 2 |
| Record match | 2 |
| Total | 10 |

Pass. The record changed only through scribe: nine commands, no refusals. The grader re-rendered `view/` from the run's `ssp.json` and found it identical, and replayed the commands on a fresh copy to confirm the record's shape came from scribe.

The run's record changes against the fixture: MFP-FRONT from Out-of-Scope Asset to CUI Asset, its remarks naming the three printer positions, with the choice on `scope/open-items.md` because nobody could be asked; PRN-SHOP added as a CUI Asset on a new component; Haas VF-2 from CUI Asset to Specialized Asset (OT); CMM-PC from CRMA to CUI Asset; the CMM measuring head added as a Specialized Asset (test equipment) on a new component. SHOP-PC-01 and the personal phones, both wrongly recorded, were left alone and handed on, as the skill says. No ADR, correctly, since no position was chosen.

## What the run found, and what changed

**Before the run**, the skill's first printer position was "CRMA, because the path is open", which contradicts the CRMA condition #101 settled (a written policy and procedure keep CUI off the asset, 32 CFR 170.19(c)). The three positions now match `cmmc-scope-boundary` and the key: in scope as a CUI Asset, in scope as a Specialized Asset when the device cannot be secured, or taken off the CUI path. The CMM-PC rule from `cmmc-scope-boundary` was added too.

**From the run's notes**: step 1 said to write an ADR while Output said to write one only once the client chooses; it now says no ADR until then. The ADR template's "(cannot proven)" was fixed. Scribe's SKILL.md now lists `change-asset --description` and `--specialized-type`, which the tester found only in the command's help.

**The key was corrected on two points.** 6.2 said PRN-SHOP "prints travelers that originate on SHOP-PC-01", which the company files do not say (the key's own SHOP-PC-01 row admits it); it now gives the facts the files support. The 6.14 row now allows MFP-FRONT's choice to be left on the open items list, as 6.2 and the `cmmc-scope-boundary` row already did, and says PRN-SHOP's remarks may carry the three positions.

## Left as found

- The run placed CMM-PC as a CUI Asset on an open path with no policy, deferring whether the FAI reports are CUI; the key's reason is that the reports carry CUI. Both reach the same category.
- The tester opened `view/asset-inventory.md` once while looking around, against the skill's rule; no decision rests on it.
- The shop-floor separation pattern in step 6 assumes a CUI workstation beside a separate machine PC, which is not Saguaro's layout. The run recorded its absence in the Haas remarks and the open items.
