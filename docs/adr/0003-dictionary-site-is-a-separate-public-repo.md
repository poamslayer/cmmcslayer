# ADR-0003: The dictionary site is a separate public repository fed by a one-way sync

Date: 2026-09-14. Status: accepted. Builds on ADR-0001 and ADR-0002.

## Context

ADR-0001 point 11 says publishing is a fresh repository from an orphan commit, never a
deletion, because the planning documents in `docs/specs/` sit in the root commit and stay
reachable from history whatever the working tree looks like later.
`python3 scripts/check_publish_safety.py` still refuses for exactly that reason, and the
decision it is waiting on has been open since 2026-09-13 with nothing forcing it.

A web site is a different publication surface from a repository. It serves rendered HTML.
Git history does not travel with a deploy. So the material can reach readers without
resolving point 11 at all, and the two problems only looked like one problem.

Four options were considered.

A `site/` directory in this private repo, deployed by a build server, keeps one copy of the
content but puts the deploy credentials and the build next to the history the gate exists to
contain, and leaves the site unable to accept outside contribution.

A git submodule from a public repo to this private one needs a token wherever the site is
built and points a public repository at a private one, which invites exactly the question
this repo is careful not to raise.

Waiting for the orphan-commit repository blocks the site behind a decision with no deadline.

A separate public repository fed by a one-way sync duplicates the content, which is the drift
the `vault_sources` machinery in ADR-0001 point 8 exists to detect. That is the real cost and
it is accepted below, because the duplicate is generated rather than authored.

## Decision

1. **The site lives in a new public repository, `cmmc-dictionary`.** This repository stays
   private and remains the only source of truth for the control files.
2. **Content reaches the public repository by a one-way sync run from this one.** The content
   directory there is generated. A hand edit in the public repository is lost at the next
   sync, and that is the intended behaviour, not a limitation to work around.
3. **The sync strips `vault_sources` from every file it writes.** ADR-0002 made those labels
   safe to publish by replacing person-titled and community-titled pages with neutral labels.
   Safe is not the same as useful: the field exists so the maintainer knows which skills to
   re-check when a wiki page changes, and it tells a reader nothing. The public surface does
   not carry it, and no published file refers to the private wiki in any form.
4. **The sync runs only after a clean `bash scripts/verify.sh --strict` on the maintainer's
   machine.** ADR-0001 point 9 builds the verbatim check's n-gram set from the private wiki,
   and that check skips itself when the wiki is absent. A hosted build server never has the
   wiki, so a gate that ran there would pass while its strongest check silently did not run.
   The gate stays where the wiki is.
5. **The synced tree is verified before it is pushed, not after.** Sync writes into a local
   clone, the public repository's own check runs against that working tree, and only a clean
   run is committed and pushed. Cloudflare Pages then builds from the public repository and
   serves `dictionary.poamslayer.com`.

## Consequences

- The site ships without resolving ADR-0001 point 11. Publishing *this repository* stays open,
  and this ADR must not be read as having settled it.
- Two repositories hold the control content. The sync regenerates rather than merges, so any
  divergence resolves to whatever this repository says, and the public copy is disposable.
- Outside contributors can raise issues against the public repository but cannot fix content
  there. Content fixes come here.
- A reader of the public repository finds no reference to the private wiki, by construction
  rather than by review.
- The public repository's history is generated output. If it ever needs rewriting, it can be
  recreated from scratch, which is exactly the property this repository does not have.
