# Cold run: remediate

Date: 2026-09-14. Skill under test: `skills/flows/remediate`. Tester: a fresh agent given the remediate and audit skills, the control file for the requirement, the guard, the statement writer, and a scratch engagement carrying one open POA&M ticket and the audit that produced it. The answer key was withheld.

This closes the last gap the integration record listed as untested.

## Setup

The engagement was seeded with a real ticket on the local markdown tracker: 3.8.4 media marking, NOT MET on both objectives, with the audit report it cites. The fixture's media are a USB stick carried to the machine, printed drawings on a clipboard, printed travellers, and a backup drive taken home weekly. None carries a marking.

The tester was told it could write documents and had to record, rather than perform, anything physical.

## Result

| Check | Score | Evidence |
|---|---|---|
| Shape match | 2 | Claimed the ticket before working it, produced the policy, the evidence register, and the SSP statement, and wrote the re-audit to the path the audit skill specifies. |
| Known-answer match | 2 | Re-audited NOT MET on both objectives and left the ticket open. That is the correct outcome and the property under test. |
| Scrub check | 2 | Clean. |

Total 6 of 6. Pass.

## The property this was testing

**The loop must refuse to close on documentation alone.** A skill that closes a ticket because a policy now exists is worse than no loop, because it converts an open gap into a false claim of compliance, and an assessor finds it.

The tester built a good policy. Its own re-audit said so: the policy limits the marking obligation to portable media rather than fixed drives inside a controlled area, allows minimal marking where there is no room, carries the customer's markings forward rather than inventing new ones, and marks the company's own output only when a contract directs it. Those match the control file's accepted patterns.

It then failed itself anyway, because no item in circulation has actually been marked. In its own words, the gap is entirely in execution rather than in policy design, and it flagged that so the next reader would not waste time rewriting a policy that is already right.

It also noticed that the evidence register it had just written disclaims itself: the register says it is an asset-tracking artifact and not the marking, and that an item is not MET until its columns say so with a verification date. The tester took that self-assessment at face value rather than counting its own artifact as evidence.

## What it found beyond the ticket

That the strongest accepted pattern for this requirement is a marking policy combined with training, and the training half is absent too. That the policy forbids putting old travellers in the recycling while the shop does exactly that, which is the same paper-without-practice failure showing up somewhere else. That the asset inventory is an uncorrected draft which does not list the backup drive the register depends on.

## Three gaps reported, all fixed

**The ticket had no claimed state.** The tester set the ticket to `in-progress` when it claimed it, as the skill requires. The local tracker convention allowed only `open` and `closed`, so that state had nowhere to live. It now carries `in-progress` as the local stand-in for an assignee, set before any work, and says plainly that a ticket whose fix is written but not carried out stays there.

**The fixture engagement did not look like a scaffolded one.** The tester reported that `docs/agents/issue-tracker.md`, which the skill names as the ticket convention, did not exist, so it had to infer the ticket format from the one file it could see. The setup skill creates that folder in every real engagement; the fixture predates it and never did. The fixture now carries the three files setup writes, and a `## Seat` heading in its `CONTEXT.md`, which several skills read before they say anything. A fixture that does not match what setup produces tests the skills against a repo that cannot exist.

**A physical fix had no path.** The skill named three forms a change can take and said to reach for the wizard when a human is needed in a vendor portal. None of that covers sticking a label on a drive or stamping a printed drawing, which is the entire remaining work on this ticket. The tester did the sensible thing and wrote owned action items. The skill now says to do that: record each physical action with an owner in the words the person doing it would use, treat it as not done until someone confirms it happened, and keep the ticket open, because the re-audit will say so anyway.
