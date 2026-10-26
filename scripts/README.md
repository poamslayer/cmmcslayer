# scripts

Every check this repository enforces, plus the harness for testing a skill against the fixture. Run them from the repository root.

## Start here

```sh
bash scripts/verify.sh            # everything, allowing skills the router names but nobody has written
bash scripts/verify.sh --strict   # every named skill must exist; the release gate
bash scripts/verify.sh --publish  # --strict, plus the two gates that decide whether this repo is safe to make public
```

`verify.sh` runs the checks in the order that fails cheapest first and exits 1 if any fail. It needs only Python 3. Two checks are deliberately outside it: `check_links.py` needs network access, and the publish gates only matter at publication.

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

**`check_scribe.py`** tests scribe's check and renderer, `skills/flows/scribe/check_ssp.py` and `render_view.py`, on scratch engagements under a temporary folder. A blank SSP and a full one pass: components, assets in all five categories, a Specialized Asset's kind, an Out-of-Scope Asset's justification, an authorized CSP and an MSP, statements of every status, and the placeholder kept beside a not applicable statement and gone beside an implemented one. The renderer writes every view page with its generated-file notice, and the pages show what the files hold. Then each rule the check enforces is broken once, in a copy, and the check must fail with a line naming the file and, for a statement, the objective, while the renderer refuses and leaves the view as it was. It looks only at exit status, output, and files, never at either command's internals. A few seconds.

**`check_setup.py`** runs the setup skill's scaffold, `skills/setup/setup-poamslayer-skills/scaffold.py`, in a scratch folder under a temporary directory. In an empty folder it must lay out the engagement and write the Markdown SSP: `ssp/system.md` with the client's name and the 110 requirement files with all 320 objectives planned on `this-system`, passing scribe's check, with the view rendered and no `ssp.json` or other OSCAL file anywhere. A re-run with `--force` must leave the SSP byte for byte unchanged, and one without `--force` must refuse. With only Python on the PATH, no Java, setup must still do all of it. A folder that already holds `CONTEXT.md` or `policies/` is refused without `--force`, and no existing file, a `README.md` included, is ever overwritten. A few seconds.

**`check_fixture_record.py`** checks the fixture engagement's record, the SSP under `docs/fixture/engagement/ssp/`. It must pass scribe's check, through `check_record.py`; its assets must be the ones the previous consultant left, each with the category they gave it, and no other; the 28 requirements they wrote must have a written statement in the record, and no other requirement may; and the view must be there with its generated-file notice and be exactly what scribe's renderer produces. The expected assets and requirements are written into the script, as `known-answers.md` 6.14 states them. Then it proves the rubric's record check bites: a copy of the fixture with one category misspelled must fail `check_record.py`, naming the category. It fails if `ssp.json` or any other OSCAL file, or the retired asset inventory or responsibility matrix, comes back. A few seconds.

**`check_record.py`** is the grader's tool for the rubric's two record checks, not part of `verify.sh` on its own. Given the engagement a cold run left, it runs scribe's check on the SSP under `ssp/`, which is the whole of rubric check 4, and prints what the record holds in the answer key's terms: components, assets and categories, providers with role and FedRAMP status, and every written statement by objective. With `--baseline docs/fixture/engagement` it prints only what the run changed, for comparison with `known-answers.md` 6.14.

```sh
python3 scripts/check_record.py /tmp/poamslayer-cold-runs/<run> --baseline docs/fixture/engagement
```

**`check_links.py`** checks that every URL the skills cite, and every URL in `reference/authorities.md`, resolves. A 404 fails. A 403 is reported and does not, because several federal hosts refuse scripted requests while serving the page to a browser. Needs network access, so it is not in `verify.sh`; run it when citations change. A citation that does not resolve is worse than a missing one in a repo whose policy requires a public citation for every claim: it looks like evidence and is not.

**`check_publish_safety.py`** checks every blob reachable from any commit, not just the working tree. Deleting a file does not remove it from a git repository, so a repo published after a tidy-up commit still hands over everything it ever held. This currently fails on purpose. See `docs/adr/0001-source-policy.md`.

## Publishing the dictionary site

**`sync_dictionary.py`** writes the 110 control files into a local clone of the public dictionary repository, `cmmc-dictionary`. See `docs/adr/0003-dictionary-site-is-a-separate-public-repo.md`.

```sh
python3 scripts/sync_dictionary.py           # write and check, touching no git
python3 scripts/sync_dictionary.py --push    # also commit and push the public repo
```

Three of its properties are the reason it exists, and each is easy to lose by accident. It gates on `verify.sh --strict`, because the verbatim half of the scrub builds its n-gram set from the private wiki and skips itself when the wiki is absent: a gate that ran on a build server would pass while its strongest check silently did not run. It regenerates rather than merges, so a hand edit in the public repository is lost on the next run, which is intended rather than a limitation. And it strips `vault_sources` and otherwise leaves the file alone, because all parsing happens once in the public repository's content collection schema, and two parsers would be two things to keep correct.

The public repository's own check runs against its working tree before the push, never after. A check that ran after the push would be reporting a leak that had already happened.

`--public-repo PATH` points at a clone somewhere other than `~/cmmc-dictionary`. `--skip-verify` bypasses the publication gate for development and says so loudly on stderr.

## The test harness

**`cold_run.py`** makes the throwaway copy of the fixture engagement that every cold run needs, and prints what the tester may read.

```sh
python3 scripts/cold_run.py --skill audit
```

The fixture is never edited in place: its mistakes are deliberate and the answer key describes them. `docs/cold-runs/README.md` explains what a tester is given, what it is denied, and what this method cannot test.

## The term lists

The term lists are private and are not in this repository, because the blocklist itself names the people and communities it protects. `scrub_check.py` reads them from `~/.config/cmmcslayer/scrub/`, or from the folder in `CMMCSLAYER_SCRUB_DIR`, and skips the name check with a notice when they are missing. `blocklist.txt` holds what may never appear: handles, private individuals, the community the material came from, venture names. `warnlist.txt` holds names that may appear only on a line that also carries a public citation. Both take one term per line, ignore `#` comments, and match case-insensitively on whole words.
