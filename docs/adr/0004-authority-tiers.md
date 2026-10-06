# ADR-0004: Authority tiers, and one register of every cited source

Date: 2026-09-26. Status: accepted. Builds on ADR-0001 points 3 and 4. Issue #70.

## Context

ADR-0001 point 3 says every claim cites a public primary source. It does not say which sources can settle which claims, and #58 showed that the gap matters. A public practitioner wiki was allowed to decide whether a shop's data was CUI. Only a regulation or the designating agency can decide that.

The citations were also scattered. The same sources (32 CFR 2002, DFARS 252.204-7012, the ISOO Q2 FY2020 slides, the DoD CUI FAQ) were found, quoted, and linked again in #58, #66, and #67. Some sit on hosts that refuse scripted requests (esd.whs.mil, dodcui.mil, dodcio.defense.gov), and one sits on a WordPress staging domain.

## Decision

1. **Every source a skill cites is listed once, in `reference/authorities.md`.** Each entry gives the exact citation, a tier, a stable URL, a local mirror under `reference/` when the host is fragile or blocks scripted fetches, the date it was last checked, and what the repo relies on it for. A source that carries a CUI status rule also quotes the text relied on.
2. **Every source has one of four tiers, and the tier limits what it can support.**
   - **Tier 1, regulation and statute.** The CFR (including 32 CFR 170, 32 CFR 2002, the FAR and DFARS clauses, the ITAR and the EAR), the U.S. Code, and a document that a regulation incorporates by reference, for the text so incorporated. NIST SP 800-171 Rev 2 and SP 800-171A are Tier 1, because 32 CFR 170.2 incorporates them by reference and DFARS 252.204-7012 requires 800-171. A Tier 1 source can establish a rule or a status.
   - **Tier 2, official federal guidance.** Material that a federal body publishes to explain or run a program: ISOO and the NARA CUI Registry, the DoD CUI Program and its registry, DoD issuances, the DoD CIO CMMC guides and FAQs, other NIST publications, FedRAMP, and CISA. A Tier 2 source can state how the government reads a rule. It is cited alongside the Tier 1 rule it explains, not instead of it.
   - **Tier 3, public secondary sources.** Named practitioner talks and posts, public wikis, vendor documentation, law firm alerts, trade press, forums, industry associations, state government material, and any official post that says it is not guidance. A Tier 3 source can support a method or a practice, and a vendor's documentation can support a fact about that vendor's own product. It never settles a status question on its own. Vendor sources are labeled as commercial in the register.
   - **Tier 4, practitioner consensus.** Unattributed, per ADR-0001 point 4. It has no entry in the register, because it has no URL. It supports method only, and the skill says so in the words ADR-0001 sets.
3. **A skill states a CUI status rule only on a Tier 1 or Tier 2 source.** This covers whether information is CUI, which category it falls in, whether a marking designates it, and whether a flowdown makes it CUI. A Tier 3 source can say how practitioners handle the question. It cannot answer it.
4. **Links that are not sources are listed too, in their own section.** A licence attribution or a link that defines a term is not a source. It still appears in the register, marked as not a source, so that the offline check below has no exceptions to remember.
5. **The register is enforced.** `scripts/check_authorities.py` runs in `verify.sh` and fails when a Markdown file under `skills/` cites a URL that is not in the register, or when the register names a mirror path that does not exist. It needs no network. `scripts/check_links.py` checks the register's URLs as well as the skills' URLs.

## Considered options

- **Put the links in each ADR that needs them.** Rejected. An ADR records one decision at one point in time. The same source would be copied into several ADRs and drift, a dead link would mean editing an accepted decision, and an author asking "what can I cite for this?" would have to read every ADR.
- **List the citing skills in each register entry.** Rejected. A hand-kept back-reference goes stale the first time a skill is edited, which is the same drift this ADR exists to stop. `grep -rl '<url>' skills` gives the answer from the files themselves.
- **Commit the mirrored PDFs.** Rejected for now. The mirrors are text extracted from the PDF, with the PDF's sha256 in the provenance header. The text is what an agent reads. The hash shows which file the text came from.
- **Make `verify.sh` warn instead of fail on an unregistered citation.** Rejected. A warning is read once and then ignored. A new citation costs one register line, so failing is cheap.

## Consequences

- Adding a citation to a skill means adding it to the register first. The tier has to be decided at that point, not later.
- A skill that settles a CUI status question on a Tier 3 source is a defect, whatever the source's reputation. The practitioner the repo trusts most on CUI is still Tier 3.
- A mirror goes stale when its source is reissued. The register's check date says when it was last checked.
