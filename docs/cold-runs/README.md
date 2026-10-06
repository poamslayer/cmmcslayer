# cold-runs

Graded results of running a skill cold against `docs/fixture/`. One file per run, named `<date>-<skill>.md`, holding the prompt used, the scores from `docs/fixture/grader-rubric.md`, and the evidence for each. Runs recorded before the fixture had an `ssp.json` were graded on the rubric's first three checks, out of 6; from #100 on, every run is also graded on its record, out of 10.

A deliberate change to the fixture's starting state is recorded here too, since it is made the same way, in a cold-run copy: `2026-09-28-fixture-ssp-conversion.md` explains how the fixture got its `ssp.json`, and the `.sh` beside it is the exact list of scribe commands that made it; `2026-10-05-fixture-markdown-ssp-conversion.md` explains how that record became the Markdown SSP of ADR-0012, and the `.py` beside it is the converter that did it. It has no scores, because it is not a graded run.

## How to run one

```bash
python3 scripts/cold_run.py --skill <name>
```

That makes a throwaway copy of the fixture engagement and prints what the tester is allowed to read. The fixture itself is never edited in place: its mistakes are deliberate and the answer key describes them.

The tester gets the skill under test, the files inside that skill's own folder, the scratch engagement, the fixture company, and the prompt an operator would type. It does not get the answer key, the rubric, or any other skill. A second agent grades the output against the answer key and the rubric, and does not see the skill's prose, so it grades what the operator sees rather than whether the skill was followed.

## What a failing run is worth

A run that fails is more informative than one that passes, and several here did. Each failure traced to a real gap: a decision chain in the wrong order, an output template that could not express the answer the skill demanded, a category the skills never named. Every one would have reached an engagement.

When a tester's answer disagrees with the answer key, the key is not automatically right. One run reported more failed objectives than the key listed, with better reasoning than the key carried. The key was corrected and the reasoning recorded.

## What cannot be tested this way

A flow whose steps are human interviews cannot be run cold end to end, because the answers do not exist until people give them. `find-cui` is the clear case: its training and interview steps produce the input that its determination and mapping steps consume. The testable half is covered by the `cui-determination-workflow` and `derivative-cui-triage` runs, which work the documents those interviews would surface. The fixture holds no interview files, so a run of the first half would be testing invented answers.

The same applies to `wayfinder`, `grilling`, and `to-questionnaire`, all of which resolve through a live exchange with a person who speaks for themselves. An agent that answers its own questions has not tested anything.
