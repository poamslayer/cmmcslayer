# Cold run: cmmc-scope-boundary

Date: 2026-09-28. Skill under test: `skills/domain/scoping/cmmc-scope-boundary`, after it began recording through scribe (#101). Three runs, each on a fresh copy made by `python3 scripts/cold_run.py`. Each tester got the SKILL.md, scribe's folder (the skill cannot write the record without it), the scratch engagement, and the fixture company files. The testers were also allowed the `reference/` files the skill cites, which rubric step b does not list; run 1 opened none, and no run's placement rests on one. The answer key and the rubric were withheld, and every other skill was unavailable, so each tester made the delegated calls (printers, endpoints, providers) with this skill's own method. A second agent graded each run without seeing the SKILL.md.

## Prompt

"Place every asset at Saguaro in scope or out and record it. The previous consultant's inventory is in the repo and I don't trust it. There's no data flow map yet and no one to interview today, so treat the company files (the IT environment write-up, the network diagram, the documents) as what you found on the walk. Split anything that needs splitting. We have no Level 3 plans." Runs 2 and 3 added "don't stop to ask me, just record and show me the table at the end", because no operator was live to confirm the table.

## Result

| Check | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Shape match | 2 | 2 | 2 |
| Known-answer match | 1 | 1 | 2 |
| Scrub check | 2 | 2 | 2 |
| Record validity | 2 | 2 | 2 |
| Record match | 1 | 1 | 2 |
| Total | 8 | 8 | 10 |

All three pass. Run 3 was made on the skill as committed, except for one later sentence on the order and naming scribe needs, which came from run 3's own refusals.

Every run changed the record only through scribe: each grader re-rendered `view/` from the run's `ssp.json` with scribe's renderer and found it identical, and `scripts/check_record.py` passed the record. No run wrote or edited a Markdown inventory; the previous consultant's `scope/asset-inventory.md` was left in place, re-tested row by row.

Run 3's record, against the fixture: SHOP-PC-01 to CUI Asset; Haas VF-2 to Specialized Asset (OT); CMM-PC to Specialized Asset (test equipment), on a component renamed to hold it with the new CMM measuring head, both test equipment; MFP-FRONT to CUI Asset, its remarks naming the three printer positions with the choice left open; the personal phones to CUI Asset. Added as CUI Assets: SAG-SRV1, the Hyper-V host, PRN-SHOP, Dana's home PC, Maria's home laptop, the USB backup drives, the switch, and the Wi-Fi access point. Added as Security Protection Assets: the EdgeRouter and Northstar RMM. The Microsoft 365 tenant split into two components, mail and files (CUI Asset) and identity and security (Security Protection Asset). No CRMA and nothing out of scope. The open items list names the conformity statements the corrections left stale, for `to-ssp`.

## What the runs found, and what changed

**Run 1 recorded CMM-PC as a Specialized Asset, and the key said that fails.** The run's grader read the reasoning first and found the key weaker. 32 CFR 170.4 defines test equipment as "hardware and/or associated IT components used in the testing of products, system components, and contract deliverables", and CMM-PC is dedicated to the CMM's measurement software. The key's only reason, "it is not OT", answered a claim the run never made. The key now takes CUI Asset or Specialized Asset (test equipment), fails CRMA or OT, and says the Windows 7 platform decides neither: it is a 3.14.1 finding. Between runs 1 and 2 the skill briefly said a PC is never Specialized for what it drives. That contradicted the same definition and was rewritten while run 2 was under way, so run 2 placed CMM-PC as a CUI Asset on the earlier text. Both answers pass.

**Run 1 put the tenant's two categories on one component.** The spec (#94, user story 11) splits a component whose assets span categories, so that each conformity statement describes one kind of thing. The skill now says the tenant's component is split, and runs 2 and 3 did.

**Both of the first two runs placed MFP-FRONT right but never named the three printer positions.** The skill now names them where it settles placements, and says to leave the choice on the open items list when nobody can be asked. Run 3 did both.

**Every run through run 2 called the g-code CUI** because it was made from the drawing, against 6.1. Both scoping skills now take CUI status from `scope/cui-determinations.md` and put an undetermined item on the open items list. Run 3 rested no placement on it.

**Run 1 also found:** no rule for CRMA versus CUI Asset when nobody knows what a user handles, now settled by the regulation's condition for a CRMA (32 CFR 170.19(c): policy, procedures, and practices keep CUI off it); nothing on firewalls that carry CUI, removable media, grouped devices, or the SSID versus the access point; nothing on statements a correction leaves stale; and a hard stop on a missing data flow map that the operator had overruled. Each is now in the skill.

**The key had four smaller defects**, each corrected: CMM-PC saves its reports to the NAS rather than storing them; nothing in the company files says travelers print on PRN-SHOP, so SHOP-PC-01's reason now rests on the flat LAN and the attached printer; the Hyper-V host holding SAG-SRV1's disk was missing from 6.2; and the key allowed the unmanaged switch as a CUI Asset but forbade the access point, the same kind of device. The row now also says the provider and external-system rows of 6.2 belong to `esp-and-msp-scoping`.

## Left as found

- **Scribe's `split-component --assets` is comma-separated**, so an asset whose name holds a comma can be recorded but never split out. Runs 2 and 3 were refused on it, renamed, and retried; the record was never at risk. The skill now says to avoid commas in asset names. The fix belongs in scribe.
- **Splitting a provider's component copies the provider's role and FedRAMP status to both halves.** The skill now says that is expected. Whether a split tenant should show as one provider or two in the view is for `esp-and-msp-scoping` (#102).
- **Where the tenant's existing statements land after a split** is not in the key. Run 3 kept them on the identity half and listed them for `to-ssp`, which is the statement writers' work (#103).
