# Cold run: control-evidence-lookup

Date: 2026-09-14. Skill under test: `skills/domain/gap/control-evidence-lookup`. Tester: a fresh agent given only the SKILL.md and two control files. No other file, no writes.

## Prompts

1. "What satisfies 3.1.1?"
2. "We use a site-to-site VPN between two of our offices. Does that count as remote access under 3.1.12?"

## Result

| Check | Score | Evidence |
|---|---|---|
| Shape match | 2 | The answer followed the Output template: the header line with point value, POA&M eligibility, and confidence, then Accepted, Rejected, Over-engineering, Open edge cases, Evidence examples, Related. |
| Known-answer match | 2 | All four buckets returned with their objective letters intact. Named concrete artifacts, not categories: an access authorization roster carrying name, business justification, and validation date, and a firewall configuration export showing an allowlist. Correctly reported the directory user list as rejected. |
| Scrub check | 2 | No blocked term, no uncited name, no verbatim text. |

Total 6 of 6. Pass.

## Findings

**Disagreement survived the lookup.** The VPN question is the test that matters, because it is the one where a skill is tempted to give a single clean answer. The tester returned both positions, said the outcome depends on the assessor, and told the operator what to do about it: document a stance, name the tunnel in the remote access methods list, and keep evidence of the log review. That is the behaviour the skill exists for.

**The confidence marker is load bearing.** 3.1.1 is a high-confidence file and read as one. The one low-confidence file in the family, 3.1.8, was left thin rather than padded, so an operator who asks about it is told the source is thin before anything else.
