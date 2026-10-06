# Fixture change: the responsibility matrix view page

Date: 2026-09-28. Not a graded run: a deliberate change to the fixture's starting state (#102), made the way AGENTS.md requires, in a cold-run copy through scribe, then copied back.

## Why

Scribe began rendering `view/esp-responsibility-matrix.md` from the record, and gained `render`, which rebuilds `view/` without changing `ssp.json`. The fixture's view was rendered before that page existed, so `scripts/check_fixture_record.py`, which now requires the fixture's view to be exactly what scribe renders from its `ssp.json`, failed on the missing page.

## Commands

```sh
python3 scripts/cold_run.py --skill fixture-view-render
cd /tmp/poamslayer-cold-runs/2026-09-28-fixture-view-render
python3 <skills repo>/skills/flows/scribe/ssp_edit.py --engagement . render
git status --short   # ?? view/esp-responsibility-matrix.md, nothing else
cp view/esp-responsibility-matrix.md <skills repo>/docs/fixture/engagement/view/
```

`ssp.json` and every existing view page came out byte for byte the same; the new page was the only difference. It shows the two providers the conversion recorded, no provider assets, and the statements the conversion put on the Microsoft 365 tenant and on Northstar beside the company components' statements on the same objectives.

## Second render, after the spec review

The spec review found the matrix labelled every statement on a provider's component "Provider", so customer-configured tenant settings (lockout, Conditional Access MFA) read as Microsoft's work in the document a provider signs. The column became "Whose component", with "Provider's" and "Company's", and a line under the heading says the statement text says who performs each part. The page was re-rendered the same way, in a fresh cold-run copy with `ssp_edit.py render`; only `view/esp-responsibility-matrix.md` changed, and it was copied back.
