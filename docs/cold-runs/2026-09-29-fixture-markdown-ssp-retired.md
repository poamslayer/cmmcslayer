# Fixture change: the Markdown SSP is retired

Date: 2026-09-29. Not a graded run: a deliberate change to the fixture's starting state (#105), made the way AGENTS.md requires, in a cold-run copy, reviewed, then copied back.

## Why

Every skill that writes the SSP records through scribe, and every skill that reads it reads `ssp.json` through scribe's `show` (#101 to #104). The previous consultant's Markdown SSP, their asset inventory, and their responsibility matrix stub had been carried into the record when the fixture was converted (#100; `2026-09-28-fixture-ssp-conversion.md`), and nothing read them any more. Keeping them left the fixture with two SSPs that could disagree, and the 3.6.3 remediate run already showed one: `ssp/3.6.3.md` still said the plan was never exercised after the record said it had been (`2026-09-29-remediate.md`).

## Commands

```sh
python3 scripts/cold_run.py --skill fixture-markdown-ssp-retired
cd /tmp/poamslayer-cold-runs/2026-09-29-fixture-markdown-ssp-retired
git rm -q ssp/3.*.md scope/asset-inventory.md scope/esp-responsibility-matrix.md
cp <skills repo>/skills/setup/setup-poamslayer-skills/domain.md docs/agents/domain.md
                     # the layout tree now matches the setup seed: ssp.json and view/, no per-requirement files
python3 <skills repo>/skills/flows/scribe/ssp_edit.py --engagement . render
git status --short   # 30 deletions and docs/agents/domain.md; ssp.json and view/ unchanged
python3 <skills repo>/scripts/check_record.py . --baseline <skills repo>/docs/fixture/engagement
                     # record: valid; 0 lines added and 0 removed
```

Then the same deletions and the edited `docs/agents/domain.md` were made in `docs/fixture/engagement/`, and `diff -r` against the copy came back empty.

## What was removed, and where it lives now

| Removed | Now |
|---|---|
| `ssp/3.1.1.md` to `ssp/3.13.11.md`, 28 files | The statements in `ssp/ssp.json`, one per objective and component, placed by the conversion; people read them in `view/requirements/` |
| `scope/asset-inventory.md` | The assets and their categories in `ssp.json`, as left, mistakes included; people read `view/asset-inventory.md` |
| `scope/esp-responsibility-matrix.md`, an empty stub | The two providers in `ssp.json`; people read `view/esp-responsibility-matrix.md` |

The plants the answer key describes survive in the record: the 3.1.8 lockout contradiction and the "[TO BE CONFIRMED" text are in the 3.1.8[a] statement on the Microsoft 365 tenant, and the house-style gap is the objectives no sentence reached (known-answers 6.10 and 6.14). `scripts/check_fixture_record.py` used to hold the record to the Markdown it came from; it now holds it to the assets and the 28 requirements 6.14 lists, and fails if a Markdown SSP file, an asset inventory, or a responsibility matrix reappears.
