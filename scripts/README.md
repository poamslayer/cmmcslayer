# scripts

Every check this repository enforces, plus the harness for testing a skill against the fixture. Run them from the repository root.

## Start here

```sh
bash scripts/verify.sh            # everything, allowing skills the router names but nobody has written
bash scripts/verify.sh --strict   # every named skill must exist; the release gate
bash scripts/verify.sh --publish  # --strict, plus the two gates that decide whether this repo is safe to make public
```

`verify.sh` runs the checks in the order that fails cheapest first and exits 1 if any fail. It needs Java 11 or later and oscal-cli 3.2.0 on PATH: run `bash scripts/install_oscal_cli.sh` once. Two checks are deliberately outside it: `check_links.py` needs network access, and the publish gates only matter at publication.

## The checks

**`scrub_check.py`** is the one the source policy rests on. It fails any file containing a blocked term, a warn-listed name on a line with no public citation, or a run of eight or more words that appears in the private wiki and not in a public source. URLs, public document citations, and NIST SP 800-171 requirement identifiers (3.1.18, AC.L2-3.1.18) are stripped before comparison, because two texts citing the same regulation or listing the same requirements are not copying each other, and the private corpus's own frontmatter is excluded, because file paths and document titles are metadata rather than expression.

```sh
python3 scripts/scrub_check.py                    # the default paths
python3 scripts/scrub_check.py skills/domain/cui  # or anything you name
```

`--vault DIR` points at a different private source, `--ngram N` changes the match size, `--no-verbatim` runs only the term checks, and `--json` gives machine-readable output. A warn-listed name is allowed when its line carries an `http://` or `https://` citation.

**`check_skills.py`** validates every skill: the name matches its folder, a description exists, domain skills carry `vault_sources`, the Codex metadata exists, and the user-invoked flag agrees between the two harnesses. It also checks every inter-skill call across the whole set, since a call is legal only if the target exists and is model-invoked. A user-invoked skill is reachable by the human alone, so an instruction for a skill to call one fails at runtime.

**`check_control_files.py`** validates the requirements index before anything else: 110 requirements, 320 assessment objectives, consecutive letters. Then each control file against it: frontmatter keys, point value, POA&M eligibility, the eight sections in order, the objective letters listed and the letters used in the body, and that Related requirements points only at requirements that exist.

**`check_router_links.py`** compares every skill the router names against the skill folders on disk. `--strict` turns any outstanding skill into a failure.

**`check_oscal_catalog.py`** compares every requirement statement and objective in the vendored OSCAL catalog, `reference/oscal/nist-800-171r2-catalog.json`, with `reference/nist-800-171r2-requirements.json`. Only the four differences recorded in `docs/research/oscal-rev2-catalog-candidates.md` are allowed, each pinned to its exact text on both sides, so a bad pin, a bad patch, or a hand edit fails. It also checks that our profile imports that catalog and selects exactly its 110 requirements. See `reference/oscal/README.md`.

**`check_oscal_cli.py`** runs oscal-cli 3.2.0 on the catalog and the profile, resolves the profile to 110 requirements, and proves `reference/oscal/cmmc-constraints.xml` still enforces every rule: it writes a small SSP to a temporary folder, which must pass with valid values and fail on each rule's id when every rule is broken. It takes about twenty seconds. Missing Java or oscal-cli is a failure, never a skip (ADR-0007).

**`check_scribe.py`** tests scribe's edit command, `skills/flows/scribe/ssp_edit.py`, end to end in a scratch engagement under a temporary folder: the skeleton from `create` passes oscal-cli, adding a component passes and re-renders the view with its generated-file notice, a change oscal-cli rejects leaves `ssp.json` and the view byte for byte unchanged and exits non-zero naming the operation and the reason, the same add twice mints no second UUID, `create` never overwrites, and a missing oscal-cli stops the command. It also covers assets in all five categories, a Specialized Asset's kind, providers with their FedRAMP status and leveraged authorization, rename keeping UUIDs, split moving the named assets, remove refused while in use, and every refusal (a category outside the five, a component category contradicting an asset, an out-of-scope asset with no justification, a CSP with no FedRAMP status) leaving the record and the view unchanged. It checks only the resulting files and oscal-cli's verdict, never the command's internals. Needs oscal-cli; about two minutes, because each case starts oscal-cli's JVM.

**`check_setup.py`** runs the setup skill's scaffold, `skills/setup/setup-poamslayer-skills/scaffold.py`, in a scratch folder under a temporary directory. In an empty folder it must lay out the engagement, with no Markdown SSP file under `ssp/` and no asset inventory or responsibility matrix under `scope/`, and have scribe create `ssp/ssp.json`, which must pass oscal-cli with our profile imported and all 110 requirements planned. A re-run with `--force` must leave that `ssp.json` byte for byte unchanged, and one without `--force` must refuse. Without oscal-cli the layout still lands, no `ssp.json` is written, the script exits non-zero and says why, and a later `--force` adds the missing file. A folder that already holds `CONTEXT.md` or `policies/` is refused without `--force`, and no existing file, a `README.md` included, is ever overwritten. Needs oscal-cli; about twenty seconds.

**`check_fixture_record.py`** checks the fixture engagement's record, `docs/fixture/engagement/ssp/ssp.json`. It must pass oscal-cli with our constraints file; its assets must be the ones the previous consultant left, each with the category they gave it, and no other; the 28 requirements they wrote must have a written statement in the record, and no other requirement may; the view must be there with its generated-file notice and be exactly what scribe renders; and no Markdown SSP file, asset inventory, or responsibility matrix may come back, since the Markdown SSP was retired (#105). The expected assets and requirements are written into the script, as `known-answers.md` 6.14 states them. Then it proves the rubric's record check bites: a copy of the fixture with one category misspelled must fail `check_record.py` on the rule that forbids it. Needs oscal-cli; about fifteen seconds.

**`check_record.py`** is the grader's tool for the rubric's two record checks, not part of `verify.sh` on its own. Given the engagement a cold run left, it runs oscal-cli on `ssp/ssp.json` with our constraints file, which is the whole of rubric check 4, and prints what the record holds in the answer key's terms: components, assets and categories, providers with role and FedRAMP status, and every written statement by objective. With `--baseline docs/fixture/engagement` it prints only what the run changed, for comparison with `known-answers.md` 6.14.

```sh
python3 scripts/check_record.py /tmp/poamslayer-cold-runs/<run> --baseline docs/fixture/engagement
```

**`check_links.py`** checks that every URL the skills cite, and every URL in `reference/authorities.md`, resolves. A 404 fails. A 403 is reported and does not, because several federal hosts refuse scripted requests while serving the page to a browser. Needs network access, so it is not in `verify.sh`; run it when citations change. A citation that does not resolve is worse than a missing one in a repo whose policy requires a public citation for every claim: it looks like evidence and is not.

**`check_publish_safety.py`** checks every blob reachable from any commit, not just the working tree. Deleting a file does not remove it from a git repository, so a repo published after a tidy-up commit still hands over everything it ever held. This currently fails on purpose. See `docs/adr/0001-source-policy.md`.

## Publishing the dictionary site

**`sync_dictionary.py`** writes the 110 control files into a local clone of the public dictionary repository, which serves `dictionary.poamslayer.com`. See `docs/adr/0003-dictionary-site-is-a-separate-public-repo.md`.

```sh
python3 scripts/sync_dictionary.py           # write and check, touching no git
python3 scripts/sync_dictionary.py --push    # also commit and push the public repo
```

Three of its properties are the reason it exists, and each is easy to lose by accident. It gates on `verify.sh --strict`, because the verbatim half of the scrub builds its n-gram set from the private wiki and skips itself when the wiki is absent: a gate that ran on a build server would pass while its strongest check silently did not run. It regenerates rather than merges, so a hand edit in the public repository is lost on the next run, which is intended rather than a limitation. And it strips `vault_sources` and otherwise leaves the file alone, because all parsing happens once in the public repository's content collection schema, and two parsers would be two things to keep correct.

The public repository's own check runs against its working tree before the push, never after. A check that ran after the push would be reporting a leak that had already happened.

`--public-repo PATH` points at a clone somewhere other than `~/cmmc-dictionary`. `--skip-verify` bypasses the publication gate for development and says so loudly on stderr.

## OSCAL tooling

**`install_oscal_cli.sh`** installs the pinned oscal-cli (metaschema-framework, v3.2.0) from Maven Central, checks the archive's SHA-256, unpacks it into `~/.local/share/oscal-cli-3.2.0`, and links `~/.local/bin/oscal-cli`. It needs Java 11 or later and stops if Java is missing. This is the one step a local operator runs; the web-session start hook runs it automatically.

```sh
bash scripts/install_oscal_cli.sh
```

**`vendor_oscal_catalog.py`** rebuilds `reference/oscal/nist-800-171r2-catalog.json` from the pinned upstream file and applies the documented patch. `--check` fails if the vendored file is not exactly pin plus patch. It needs network access unless given `--from FILE`, so it is not in `verify.sh`; `check_oscal_catalog.py` is the offline guard.

## The test harness

**`cold_run.py`** makes the throwaway copy of the fixture engagement that every cold run needs, and prints what the tester may read.

```sh
python3 scripts/cold_run.py --skill audit
```

The fixture is never edited in place: its mistakes are deliberate and the answer key describes them. `docs/cold-runs/README.md` explains what a tester is given, what it is denied, and what this method cannot test.

## The term lists

The term lists are private and are not in this repository, because the blocklist itself names the people and communities it protects. `scrub_check.py` reads them from `~/.config/cmmcslayer/scrub/`, or from the folder in `CMMCSLAYER_SCRUB_DIR`, and skips the name check with a notice when they are missing. `blocklist.txt` holds what may never appear: handles, private individuals, the community the material came from, venture names. `warnlist.txt` holds names that may appear only on a line that also carries a public citation. Both take one term per line, ignore `#` comments, and match case-insensitively on whole words.
