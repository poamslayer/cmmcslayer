# ADR-0001: Source policy for public-safe skills

Date: 2026-09-13. Status: accepted.

## Context

Every domain skill in this repo derives from `~/cmmc-vault`, a private wiki of 186 pages. Its most valuable pages, the 110 per-requirement overlays and the practitioner syntheses, are built from verbatim quotes from a private practitioner community and from named individuals' public and semi-public posts, attributed by handle, real name, and credential. That attribution is what makes the material trustworthy and also what makes it unpublishable as it stands. The inventory that backs this decision is `docs/specs/2026-09-09-vault-inventory.md`; its section 5 lists the pages and raw files that are out of scope by name, and its section 4 lists the thin pages.

The repo will be public under the `poamslayer` personal brand once the build is done. Publishing must be a decision, not a rewrite, so every file is written public-safe from the first commit.

## Decision

1. **Keep rules, tests, and decision tables.** A rule, a test, a checklist, or a decision table is not anyone's copyrightable expression. Skills carry the judgment, not the conversation that produced it.
2. **Drop verbatim quotes, handles, and private real names.** No sentence from the private community is reproduced. No handle appears. No private individual is named.
3. **Cite the public primary source for every claim.** The CMMC Level 2 Scoping Guide, the CMMC Level 2 Assessment Guide from the DoD CIO, 32 CFR Part 170, the CMMC FAQs, NIST SP 800-171 Rev 2 and 800-171A, 32 CFR Part 2002, the DFARS clauses, the DoD CUI Registry, the 2024 DoD CUI marking training aid, and public talks and posts. Where a practitioner said the same thing publicly, cite that public source with a link.
4. **Where a conclusion rests only on private practitioner consensus, say so in those words and name nobody.** The phrase is "practitioner consensus" or "assessors have accepted this in practice", with no attribution.
5. **Assessment Guide text comes from the DoD CIO source.** The vault's raw copies of the Assessment Guide entries carry a third-party reproduction footer. Skills cite the DoD CIO document (`https://dodcio.defense.gov/CMMC/Resources-Documentation/`) and never the reproduction. The footer, the support address, and any line naming the reproduction are stripped before any of that text is used as an input.
6. **Excluded vault pages, by name.** The following wiki pages are never used as a source and never shipped: Landing Page Copywriting; Identity-Based Marketing; Plain Language Writing; Buyer vs Champion; Cold Call Fear (the mindset corpus); CUI Enclave Market Pricing; cmmc-search-demand-landscape; DoD Components Driving CMMC Demand (its positioning section; the demand data may be cited to its public sources only); the AEC notes page written about a named practitioner; and the private pricing page. The Trusting RPs and RPOs page is used only for its buyer-protection substance, never its competitive framing.
7. **Excluded raw material, wholesale.** Every swipe file, tweet corpus, LinkedIn corpus, personal sales-call note, content-idea file, and readiness-bottleneck marketing note in `raw/`. The one technical finding in the content-ideas file (consultants writing CNC machines into the SSP as CUI Assets) is carried into `over-engineering-guard` as a rule, without the file.
8. **Every domain skill lists its vault sources in frontmatter** under `vault_sources`, as wiki page titles and raw file names. A vault update then tells the maintainer which skills to re-check. The control files also carry `as_of` so drift is visible.
9. **The scrub check runs at write time, not before publishing.** `scripts/scrub_check.py` fails any file that contains a blocklisted handle or name, a warn-listed name without a public citation on the same line, or a run of eight or more words that appears verbatim in the private wiki and not in a public source. Every ticket's acceptance includes a clean scrub.
10. **No venture names.** The repo is a personal brand. No consulting company name, no competitor positioning, no pricing.

11. **Publishing is a fresh repository, not a deletion.** The planning documents are in the root commit, so every version of them stays reachable from history no matter what the working tree looks like later. Deleting them and committing the deletion makes the repository look clean and changes nothing about what a reader can recover. The safe route is to publish an orphan commit of the current tree as a new public repository, and keep this one private as the working history. Rewriting history and force-pushing is the alternative, and it is worse: every existing clone and fork keeps the old objects, and the failure mode is silent. `python3 scripts/check_publish_safety.py` checks every blob reachable from any commit, and `bash scripts/verify.sh --publish` runs it.

12. **`docs/specs/` is internal and must not be published.** The spec and the vault inventory were written to plan this build, not to ship. They name the private community, its members' handles, and real people, because that is what the planning needed. They are deliberately outside the scrub check's default paths, so ordinary work is not drowned in hits about them, and that exclusion is precisely why publication has to check them deliberately. `bash scripts/verify.sh --publish` runs that gate and fails while they are still there. Before the repository is made public, `docs/specs/` is removed or scrubbed. The decision of which is Arnold's; the gate only refuses to let it happen by accident.

## Consequences

- Control files lose the named attribution that made the vault pages persuasive. They keep the rule and gain a public citation. Where only private consensus backs a rule, the file says so.
- Thin source pages produce thin control files marked `confidence: low`. They are not padded.
- The maintainer re-checks a skill when a page it names in `vault_sources` changes.
- A contributor without the vault can still run the term check; the verbatim check skips itself when the vault is absent.
