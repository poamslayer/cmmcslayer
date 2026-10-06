---
name: wayfinder
description: Chart an engagement's contested decisions as a map of decision tickets on the engagement tracker, and resolve them one at a time until the way to a defensible scope and SSP is clear.
disable-model-invocation: true
---

# Wayfinder

An engagement has arrived with more open calls than one session can hold. Enclave or enterprise. GCC High or not. What the printer is. Whether the owner's home PC is remote access. What the managed service provider is. Whether the travellers stay in the production system. Each one moves the cost of every later stage, each one depends on answers that are not in yet, and answering them in the wrong order means redoing the work.

Wayfinding is finding the way, not charging at the destination. This skill charts the way as a **map** on the engagement tracker, then works its **decision tickets** one at a time until the route is clear.

The destination varies. Usually it is a scope you can defend and an SSP you can write. Sometimes it is one architecture decision that has to be locked before anyone can budget. Naming it is the first act of charting, because the destination fixes the scope of the map.

## Decisions, not deliverables

Wayfinder plans. Each ticket resolves a decision and records it as an ADR in the engagement repo. The map is done when nothing is left to decide before someone can go and build.

The pull to start implementing is the signal you have reached the edge of the map. When the map clears, **hand off to `/to-ssp`**, which turns the recorded decisions into conformity statements. Looping the map straight into remediation throws away the reasoning the ADRs hold, and the reasoning is what an assessor asks for.

## Refer by name

Every map and ticket is an issue with a title. In everything a person reads, use the title, never the bare number. "Printer category" reads; "#42" does not. The number rides inside the link.

## The map

One issue on the engagement tracker, labelled `wayfinder:map`. Its tickets are child issues. Where the map, its children, blocking, and the frontier query physically live is tracker specific: read the "Wayfinding operations" section of `docs/agents/issue-tracker.md` in the engagement repo. If no tracker is configured, tell the operator to run `/setup-poamslayer-skills`.

The map is an **index**, not a store. A decision lives in exactly one place, its ticket. The map gists it and links.

```markdown
## Destination

<what reaching the end of this map looks like: the scope, the architecture, the SSP this engagement is finding its way to. One or two lines.>

## Notes

<the client in one paragraph: what they make, who they sell to, what the CUI is. The seat. Standing constraints: a contract date, a budget ceiling, an export control finding, a prime's deadline. The skills every session should consult.>

## Decisions so far

<!-- one line per closed ticket, with the ADR it produced -->

- [<ticket title>](link): <one-line gist of the decision> (ADR-<n>)

## Not yet specified

<!-- in-scope fog: questions you can see coming but cannot phrase sharply yet -->

## Out of scope

<!-- ruled beyond this map's destination; closed, never graduates -->
```

## Decision tickets

Each is a child issue of the map, sized to one session. The body:

```markdown
## Question

<the decision this ticket resolves>

## Resolved by

<the domain skill that answers it: cmmc-scope-boundary, esp-and-msp-scoping, gcc-high-decision, and so on>

## Depends on

<what has to be known first, as blocking edges on the tracker>
```

**Every decision ticket names the skill that resolves it.** That is the difference between this map and a list of worries. A ticket nobody can name a skill for is usually not a decision, it is a fact to go and find, which is a research ticket, or a question that is still fog.

A session **claims** a ticket by assigning it before doing any work, so concurrent sessions skip it. Blocking uses the tracker's native dependency relationship, so the frontier is visible in the tracker's own interface. A ticket is **unblocked** when every ticket blocking it is closed. The **frontier** is the open, unblocked, unclaimed children.

## Ticket types

Every ticket is either worked with the operator present, or driven alone.

- **Decision** (with the operator). The default. A contested call that a domain skill resolves and an ADR records. Call the Skill tool for the named skill, and for `grilling` and `domain-modeling` when the terms are still soft.
- **Research** (alone). A fact a decision waits on, outside the operator's head: whether a product holds a FedRAMP Moderate authorization, what a clause list actually says, whether a device has a validated cryptographic module. Call the Skill tool with `research`. Fire these in parallel; they are the only type you may resolve more than one of per session.
- **Interview** (with other people). The answer is in someone else's head: the contracts manager, the shop lead, the provider, the prime's buyer. Tell the operator to run `/to-questionnaire`, which interviews them about the send and aims the questions at the gap. The ticket resolves when the answers come back, so expect it to sit open across sessions.
- **Task** (either). Work that must happen before a decision can be made: getting a tenant's licensing detail, getting the provider to say what accounts they hold, walking the floor. It does rather than decides, and it earns its place by unblocking a decision.

## The usual first map

Most engagements surface the same contested calls. Chart the ones that apply, and do not chart the ones that do not:

| Decision | Resolved by | Usually blocked by |
|---|---|---|
| Is there CUI, and where | `find-cui` | nothing; it comes first |
| What each asset is | `cmmc-scope-boundary` | the data flow |
| Whether a claimed separation holds | `logical-separation-test` | the asset list |
| Where laptops, home networks, and remote access land | `endpoint-and-vdi-scoping` | the data flow |
| What the printers and shop-floor machines are | `printer-and-ot-asset-scoping` | the data flow |
| What the managed service provider is | `esp-and-msp-scoping` | knowing which accounts they hold |
| Enclave or enterprise | `enclave-or-enterprise-decision` | the data flow, the asset list |
| GCC High or not | `gcc-high-decision` | the export control finding |
| Whether export control changes the answer | `export-control-overlay` | the CUI determination |
| What the finisher or sub needs | `flowdown-level-determination` | the CUI determination |
| Whether the production system stays in scope | `cui-re-use-triage` | the CUI determination |

The shape repeats: the CUI determination and the data flow block nearly everything, which is why `find-cui` is the first on-ramp and why a map charted before it is mostly fog.

## Fog of war

The map is deliberately incomplete. Beyond the live tickets is the **fog**: decisions you can tell are coming but cannot yet phrase, because they hang on answers not in yet. Resolving a ticket clears the fog ahead of it and graduates whatever is now sharp into fresh tickets.

**Fog or ticket?** The test is whether you can state the question precisely now, not whether you can answer it now.

- **Ticket** when the question is sharp, even if it is blocked.
- **Not yet specified** when you cannot phrase it that sharply. Do not pre-slice fog into ticket-sized pieces; one patch may graduate into several tickets, or none.

## Out of scope

Fog gathers only toward the destination. Work beyond it is out of scope: not fog, and not in **Not yet specified**. When a ticket turns out to sit past the destination, close it and leave one line in **Out of scope** with the reason. It stays out of **Decisions so far**, which records the route actually walked.

Level 3 questions, a second site not yet under contract, and a certification the client has not decided to pursue are the usual candidates.

## Invocation

Two modes. Either way, **never resolve more than one decision ticket per session**, research tickets excepted.

### Chart the map

The operator arrives with an engagement.

1. **Name the destination.** Call the Skill tool twice, for `grilling` and `domain-modeling`, to pin down what this map is finding its way to and to get the client's terms into the engagement `CONTEXT.md`.
2. **Map the frontier.** Grill again, breadth first this time, across the whole engagement rather than deep on one thread. The table above is the checklist, not the answer; ask which of those calls are actually live here, and what else this client has that is not on it. **If this surfaces no fog**, there is no map to draw: the engagement is small enough to run straight down the main flow. Say so and stop.
3. **Create the map** with the destination and notes filled in, decisions empty, the fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** as child issues, then wire the blocking edges in a second pass, because issues need ids before they can reference each other.
5. **Fire the research tickets** in parallel as subagents calling the Skill tool with `research`.
6. **Stop.** Charting is one session's work. It resolves nothing by hand.

### Work through the map

The operator arrives with a map, and optionally a ticket. Without one, you pick.

1. Load the map, the low resolution view, not every ticket body.
2. Choose the ticket: the one the operator named, else the first frontier ticket in map order. **Claim it** before any work.
3. Resolve it. Call the Skill tool for the skill the ticket names. Zoom into any related or closed ticket on demand. If the ticket names no skill and is not research, that is a charting error: either it is fog, or you have not found the skill that answers it.
4. Record the resolution three ways: a resolution comment on the ticket, **an ADR in the engagement's `docs/adr/`** holding the decision and its reasoning, and a one-line gist appended to the map's **Decisions so far** naming the ADR. The ADR is the artifact that survives; the ticket is where the working went.
5. Update the map: create newly surfaced tickets and wire them, graduate fog that is now sharp and clear it from **Not yet specified**, rule anything past the destination out of scope, and delete or rewrite tickets the decision invalidated.

The operator may run unblocked tickets in parallel, so expect other sessions to be editing the tracker at the same time.

## When the map clears

Hand off to `/to-ssp`. The decisions are in ADRs and the scope files; `to-ssp` turns them into one conformity statement per objective. Say this out loud rather than starting to write the SSP inside wayfinder, because the handoff is where the map's job ends.

## Sources

Rewritten from `wayfinder` in mattpocock/skills (MIT, see `skills/flows/LICENSE-mattpocock`). The map, the fog of war, the frontier, the claim, and the one-ticket-per-session rule are kept as they are. The ticket types, the decision table, and the ADR requirement are this repo's.
