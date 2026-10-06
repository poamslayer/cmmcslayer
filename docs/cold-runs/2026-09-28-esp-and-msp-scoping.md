# Cold run: esp-and-msp-scoping

Date: 2026-09-28. Skill under test: `skills/domain/scoping/esp-and-msp-scoping`, after it began recording providers through scribe (#102). Two runs, each on a fresh copy made by `python3 scripts/cold_run.py`. Each tester got the SKILL.md, scribe's folder, the scratch engagement, and the fixture company files. The answer key and the rubric were withheld, and every other skill was unavailable. A second agent graded each run without seeing the SKILL.md.

## Prompt

"Place every outside provider Saguaro uses: the MSP, anything behind it, the SOC, Microsoft 365, the copier vendor, anyone with remote access or holding our data, and record them. The previous consultant's inventory and responsibility matrix are in the repo and I don't trust them. Use the company files as what we know; there's nobody to call today. Don't stop to ask me, just record and show me the table at the end."

## Result

| Check | Run 1 | Run 2 |
|---|---|---|
| Shape match | 2 | 2 |
| Known-answer match | 2 | 1 |
| Scrub check | 2 | 2 |
| Record validity | 2 | 2 |
| Record match | 2 | 2 |
| Total | 10 | 9 |

Both pass. Run 2 was made on the skill as committed after run 1's fixes, before the last clarification below, which came from run 2's own gap.

Every run changed the record only through scribe, with no refusals: each grader re-rendered `view/` from the run's `ssp.json` and found it identical, and neither run wrote a Markdown inventory or responsibility matrix; the old ones under `scope/` were left in place, with the operator told the view pages replace them.

Run 2's record changes against the fixture: Sentry SOC LLC added as a provider with role SOC and no asset; the copier's service vendor added as an other ESP, its access model marked unconfirmed; Northstar RMM and Northstar's technician devices added as Security Protection Assets of Northstar Managed IT; new descriptions and remarks on Northstar (MSP) and Microsoft 365 (CSP, FedRAMP status neither, the Marketplace check on the open items list). CloudVault Backup, MeridianLink, Sonoran, and Maria's Gmail were not recorded and were named on the open items list for the skills they belong to. Run 1 differed in recording Northstar RMM and the technician devices as CUI Assets and Defender as a Security Protection Asset on the tenant.

## What the runs found, and what changed

**The key's Northstar RMM row was narrower than its own reasoning.** Run 1 recorded the RMM as a CUI Asset because its unattended remote control relays the screens and files of CUI Assets. The grader held that better supported for this configuration: 6.2 already makes Dana's home PC a CUI Asset for pixels in the process path. 6.2 and 6.14 now pass either category, with the reason. The same run's FIPS sibling raised the EdgeRouter the same way (`2026-09-28-fips-crypto-scoping.md`).

**Run 1 found gaps the skill now closes**: a third-party RMM whose relay carries CUI is recorded as a CSP, so its FedRAMP status has a home under the one-role rule; an unnamed second-tier provider and an unanswered account test go on the open items list rather than being invented or read as "none"; a SOC that reaches in with nothing gets no asset; the organization's tenant and the services inside it are `cmmc-scope-boundary`'s, which scribe's refusal of a category-less asset had made unworkable here anyway; a lower-tier supplier that receives CUI is a flowdown question, not an ESP; an unapproved use is written as the current use with the approval on the open items list; and recording before the MSP has reviewed the placement is said so in the remarks.

**Run 2 lost a point for leaving Northstar's CUI reach "pending a determination"**, against the key and the marked drawing on the Jobs share that Northstar's RMM and Global Administrator accounts reach. Its tester named the cause: the skill's rule to place on facts independent of a determination pulled against its rule that a tool which displays CUI is a CUI Asset. The skill now says reach into an asset the record holds as a CUI Asset is CUI reach, a fact, and places at the Security Protection Asset floor only when the record's own category is in doubt. It also now separates remarks that say a thing is unconfirmed (allowed, pointing at the open item) from remarks that state it as fact (not allowed), allows a plain descriptive title for a provider the facts do not name, and the consultant seat note no longer says "refuse" where Output says record and mark it unreviewed. The 6.14 row now requires Northstar's remarks to state CUI reach, and lets the RMM vendor wait on the open items list until named.

## Left as found

- The account test's outcomes fit a CSP awkwardly; both runs described Microsoft staff access as not described and Northstar's admin reach separately.
- Neither run could discover vendors the files never mention (the ERP, CNC, and CMM vendors); both listed them as questions.
- The shared local administrator password from Northstar's build image is a finding, not an asset; both runs noted it in Northstar's remarks and the open items.
