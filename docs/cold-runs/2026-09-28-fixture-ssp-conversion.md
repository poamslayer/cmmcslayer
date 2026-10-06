# Conversion: the fixture's ssp.json

Date: 2026-09-28. Issue #100. Not a graded skill run: this is the one-time conversion that gave the fixture engagement its record, `docs/fixture/engagement/ssp/ssp.json`, so every later cold run can be graded on it.

## How it was made

The fixture is never edited in place (AGENTS.md), so the conversion ran in a cold-run copy:

```sh
python3 scripts/cold_run.py --skill fixture-ssp-conversion
bash docs/cold-runs/2026-09-28-fixture-ssp-conversion.sh /tmp/poamslayer-cold-runs/2026-09-28-fixture-ssp-conversion
```

The script beside this file is the whole conversion: scribe's `create`, then one scribe operation per component, provider, asset, and statement. Every operation went through scribe's edit command, so oscal-cli with our constraints file passed the record after each one. The result was reviewed against the Markdown it came from, then `ssp/ssp.json`, `ssp/oscal/`, and `view/` were copied into the fixture. The Markdown SSP files, the inventory, and the responsibility matrix stay where they are until the skills that read them move to the record (#104) and the Markdown SSP is retired (#105).

`scripts/check_fixture_record.py`, run by `verify.sh`, now holds the two together: the record must pass oscal-cli, its assets must be the inventory's rows with the categories they were left with, and its statements must cover exactly the requirements the Markdown SSP covers.

## The rules the conversion followed

- **The record keeps the previous consultant's mistakes.** They are the plants the answer key grades against. A conversion that corrected them would leave every scoping and audit run with nothing to find.
- **An asset is an inventory row that has a category.** The rows the inventory left "not listed" are not assets in the record, because scribe cannot record an asset without a category and inventing one would erase the gap. Where the SSP describes one of them (the EdgeRouter, Northstar's RMM), it is a component with no asset behind it.
- **Out-of-scope assets carry the only justification the inventory gave.** MFP-FRONT's is "policy prohibits scanning CUI". The phones had none beyond the note "Outlook on personal devices", and the remarks say so.
- **Providers are the two the SSP names with a role.** Microsoft 365 is a CSP whose FedRAMP status nobody checked, recorded as neither authorized nor equivalent until someone does, and the description says that. Northstar is an MSP. The responsibility matrix was an empty stub, so it added nothing.
- **Statement text is the Markdown's own sentences,** placed on the objective each one speaks to and the component it describes. A sentence about two components was split between them, with the least rewording that allowed. A sentence about the company as a whole went on one process component, "Saguaro operating practices", because a statement must name a component and "This System" is only the placeholder. An objective no sentence reached stays planned on "This System".
- **Statuses are the Markdown's claims, not the truth.** Implemented where it says a thing is done, partial where done in part, planned where it says a thing is missing, not applicable where it says there is nothing to act on. Scribe needs a reason for not applicable. 3.1.22 gave one; 3.1.20 gave none, and its remarks say so rather than supply one.
- **A claim goes on the objectives its words speak to, not on the whole requirement.** "Saguaro does not connect to external systems" identifies connections and use, 3.1.20[a] and [b]; it says nothing about verifying or limiting them, so [c] to [f] stay planned. That also matches 6.3, which grades [a] and [b].
- **What the record does not hold stays Markdown.** Each SSP file's evidence list points at files under `evidence/`, which stays Markdown (#94), so the record carries no evidence links. The responsibility matrix's one cell, "Northstar to provide", records no decision. Northstar has no FedRAMP status because only a cloud provider records one; our constraints file refuses it on an MSP.

## Where the conversion disagreed with the answer key

**3.3.1's NOT MET objectives.** The key listed [d] and [e]. Placing the Markdown's sentences put "SAG-NAS, SHOP-PC-01, and CMM-PC keep no audit log at all" on [c], records are created, and the endpoints' 20 MB rollover with no central collection on [f], records are retained. Nothing in the engagement defines retention, which is [e]. [d] asks that records carry the content [b] defines, and nothing defines any, so nothing supports calling [d] the failure rather than [c] and [f]. The key's reasoning was read and it was the key that was wrong: it is corrected to [c], [e], [f], with a note in 6.3. The requirement is NOT MET either way, so the SPRS score does not move.

**The house-style gap in 6.10.** The key says every SSP file is one narrative per requirement. The record cannot hold that shape, since a statement belongs to one objective. The key is right about the Markdown, and 6.10 now also says how the plant appears in the record: as the objectives the narrative never reached.

Everything else agreed. The claims 6.3 marks wrong (3.1.1, 3.1.20, 3.5.3, 3.13.11) are recorded as the previous consultant made them, and 3.1.8[a] carries both 6.10 plants.

## Answer key and rubric

`known-answers.md` gains 6.14: what the starting record holds, and what each skill's run should leave in it. `grader-rubric.md` gains two checks, record validity and record match, and the pass mark moves from 5 of 6 to 8 of 10 with no check at 0, so an SSP that fails oscal-cli fails the run. `scripts/check_record.py` is the grader's command for both, and `check_fixture_record.py` proves it fails a copy of the fixture with one category misspelled.
