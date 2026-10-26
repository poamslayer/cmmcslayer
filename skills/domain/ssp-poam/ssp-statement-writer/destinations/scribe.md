# Destination: the `ssp/` files, through scribe

The engagement's SSP is the `ssp/` folder (ADR-0012). Record every statement by calling the Skill tool with `scribe`. Never write the `ssp/` files yourself, and never edit anything under `view/`.

## Reading the current text

The recorded components and providers are in `ssp/components/*.md`. The statements already on an objective are in the frontmatter of `ssp/<requirement>.md`. Read the files directly; never read `view/`.

## One statement per objective and component

Scribe attaches each statement to its objective, written `3.5.3[a]`, and to the component it describes (ADR-0008). That adds four rules to the method in `SKILL.md`:

1. **Write at the component level**, using the components the record holds, named by their slug, the file name under `ssp/components/`. The laptop fleet is one component. Per-machine statements add redundancy, not assurance. A statement names a recorded component, never `this-system`, the placeholder. An objective whose only entry is `this-system`, planned and "Not yet written.", has no statement yet; a component's entry that is planned and "Not yet written." is a cleared statement that component still owes. An organization-wide decision goes on the policy, plan, or procedure component that carries it; when the record has none, ask scribe to add one. Its type is `policy` for a written policy or plan, or `process-procedure` for a practice. Any other missing component is a scoping gap: put it on the open items list for `cmmc-scope-boundary` rather than adding it.

2. **Collapse inherited components onto their control plane.** Where several workloads federate to one identity provider, one log platform, or one endpoint manager, write the enforcement statement on the plane's component and name what inherits it. Where an external provider implements part of the objective, write the provider's part on the provider's component and the company's part on the company's, rather than claiming the provider's work. Scribe generates the responsibility matrix from the two.

3. **Put a misplaced statement on the right component.** A statement already recorded on the wrong component, such as an enforcement sentence on a definition objective's tenant, is not fixed by editing it there. Record the right statement on the right component, then ask scribe to remove the old component's statement from the objective (remove the statement, not the component, which would delete the component), so it is not left behind as planned. Clear a statement instead only when that component still owes the objective and its statement is not written yet.

4. **Do not name the component in the text.** "Accounts are authorized in writing by the owner before IT creates them." Scribe records which component the statement describes. On a policy or procedure component this means the definition objective states the rule itself, with its values, rather than pointing at the document it is attached to (`SKILL.md`, method step 3).

Alternative and not applicable carry their reason in the remarks; no other status does. For partial, what is missing goes in the statement.

## Recording

Once the operator says to record, give scribe every statement for the requirement together, so they are recorded and checked as one change, with a second call to take a misplaced statement off the wrong component. In the as-if-met mode, give each statement the status the objective already has. Say it to scribe in these terms:

```markdown
| Objective | Component | Status | Statement | Remarks |
|---|---|---|---|---|
| 3.1.10[b] | `windows-11-office-endpoints` | implemented | The screen locks after 15 minutes of inactivity, enforced by the endpoint management policy exported in evidence/3.1.10/. | |
```

An open items line reads: `- 3.1.8[b]: whether the lockout applies to local accounts on SAG-NAS. Confirm with <who>.`

Setting a statement again on the same objective and component replaces the old one. If scribe refuses, the refusal is the answer: fix the statement and ask again, never work around it. Scribe re-renders `view/requirements/<id>.md`, where people read the result.
