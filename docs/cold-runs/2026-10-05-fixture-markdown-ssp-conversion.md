# Conversion: the fixture's record becomes the Markdown SSP

Date: 2026-10-05. Issue #128. Not a graded skill run: the one-time move of the fixture engagement's record from the OSCAL `ssp/ssp.json` to the Markdown SSP of ADR-0012, made the way AGENTS.md requires, in a cold-run copy, reviewed, then copied back.

## Commands

```sh
python3 scripts/cold_run.py --skill fixture-markdown-ssp
python3 docs/cold-runs/2026-10-05-fixture-markdown-ssp-conversion.py . /tmp/poamslayer-cold-runs/2026-10-05-fixture-markdown-ssp
cp skills/setup/setup-poamslayer-skills/domain.md /tmp/poamslayer-cold-runs/2026-10-05-fixture-markdown-ssp/docs/agents/domain.md
                     # the layout tree now matches the setup seed: system.md, components/, the requirement files
python3 skills/flows/scribe/check_ssp.py /tmp/poamslayer-cold-runs/2026-10-05-fixture-markdown-ssp
                     # check_ssp: ok, 15 components, 15 assets, 53 written statements
python3 skills/flows/scribe/render_view.py /tmp/poamslayer-cold-runs/2026-10-05-fixture-markdown-ssp
```

The converter is the Python file beside this note. It reads `ssp/ssp.json` and writes `ssp/system.md`, one `ssp/components/<slug>.md` per component, and the 110 `ssp/<requirement>.md` files with scribe's own writer, then removes `ssp/ssp.json` and `ssp/oscal/`. After review, the copy's `ssp/`, `view/`, and `docs/agents/domain.md` were copied into `docs/fixture/engagement/`, and `diff -r` against the copy came back empty.

## The review

The record was compared line by line in the answer key's terms. The grader's `check_record.py` as it was before this change printed 83 lines from `ssp.json`; the rewritten one prints 83 lines from the Markdown SSP. Every component, provider, asset, category, kind, and written statement is the same, word for word. The two lines that differ are the two Out-of-Scope Assets, whose reason was in `remarks` and is now in the asset's own `justification` field, with the same text.

The view was compared page by page with the one `ssp_edit.py` had rendered. Apart from the generated-file notice, which now names the `ssp/` folder, three things changed, each explained below: the placeholder rows on three objectives, and the requirement statements of 3.3.2 and 3.5.4.

## The rules the conversion followed

- **Nothing the record held is lost or changed in meaning.** The previous consultant's mistakes are the plants the answer key grades against, so they are carried over exactly: the asset categories as left, the statements as made, the not applicable claims on 3.1.20[a] and [b] with their empty reason.
- **A component is its title's slug.** "Microsoft 365 commercial tenant" is `microsoft-365-commercial-tenant`, "SAG-NAS" is `sag-nas`. Titles are kept, so the view and the answer key's names do not change. The placeholder, "This System", is `this-system` and has no file. UUIDs are dropped.
- **An asset moves under the component it was an instance of,** with its category, kind, and description. No component carried a category, so every asset keeps its own.
- **The placeholder rule of ADR-0011 now holds everywhere.** The record was converted in #100, before ADR-0011 made scribe keep "This System" planned beside an objective whose only statements are not applicable. Three objectives had only not applicable statements and no placeholder: 3.1.20[a], 3.1.20[b], and 3.1.22[a]. The check refuses that, so the converter put the placeholder back on each, first, as scribe's own operation would have. The not applicable claims themselves are unchanged; known-answers 6.14 already said an objective like this stays planned on "This System".
- **Requirement and objective text comes from `reference/nist-800-171r2-requirements.json`,** cleaned in #125, instead of the vendored catalog. The objective text is identical. Two requirement statements differ by spelling, because the catalog followed NIST's CPRT export and the reference follows NIST's CSV: 3.3.2 loses a comma before "so they can", and 3.5.4 reads "non-privileged". No statement in the record speaks to either.

## Answer key and rubric

`known-answers.md` 6.14 names the Markdown SSP and the placeholder on the three objectives. `grader-rubric.md` check 4 now runs scribe's check instead of oscal-cli, and a run that changed the SSP without scribe still scores 0. `scripts/check_record.py` prints the record in the same terms as before and keeps `--baseline`, and `scripts/check_fixture_record.py` holds the fixture to the same assets and the same 28 requirements, proves the rubric still fails a misspelled category, and fails if `ssp.json` or any OSCAL file comes back.
