---
name: scribe
description: Record a decision in the engagement's SSP, the Markdown files under `ssp/`. The only skill that ever changes them. Other skills call it with what was decided, in domain terms; scribe edits the files, runs the check, keeps the change only if it passes, commits it, and re-renders the read-only view.
---

# Scribe

The engagement's System Security Plan is the `ssp/` folder of the engagement repo, written in Markdown with YAML frontmatter, and it is the record (ADR-0012). Scribe is the only thing that changes it. A skill that decides something (a component exists, an asset is a CUI Asset, an objective is met by a component) calls the Skill tool with `scribe` and says what was decided in the words of the engagement. The caller never needs to know the file layout; scribe does.

Any skill may read the SSP files; only scribe writes them. Nobody edits anything under `view/`: it is generated from the record and overwritten on every change.

## The record

```
ssp/system.md                 the system
ssp/components/<slug>.md      one per component, with its assets and, for a provider, its provider fields
ssp/3.1.1.md ... ssp/3.14.7.md   one per requirement, 110 in all, statements by objective
```

Each file opens with YAML frontmatter between `---` lines. The frontmatter is the record; the body below it is prose for people.

**`ssp/system.md`**

```yaml
---
system-name: Acme Machining
status: under-development        # or operational, under-major-modification, disposition, other
information-types:
  - title: Controlled Unclassified Information
    description: CUI the organization receives or creates under its DoD contracts.
    confidentiality: moderate    # low, moderate, or high
    integrity: moderate
    availability: moderate
users:
  - title: System user
---

# Authorization boundary

What the system's boundary takes in, as prose. Scoping records it.
```

**`ssp/components/<slug>.md`.** A component is a named part of the system that conformity statements describe once: "Entra ID", "Windows 11 laptops (engineering)", "Access Control Policy". Its slug is its file name, lowercase words joined by hyphens, made from its title: `windows-11-laptops-engineering`. Every statement names it by that slug.

```yaml
---
title: Windows 11 laptops
type: hardware
category: cui-asset              # only when every asset behind it shares one category
assets:
  - id: ENG-LT-01
    description: Engineering laptop, Dell 7440
  - id: ENG-LT-02
    remarks: Loaner kept in the office safe.
---

Entra-joined Windows 11 laptops, one per office user.
```

- `title` is how people name it. Titles are unique.
- `type`: `service` for a cloud service or tenant, `software` for installed software, `hardware` for a class of devices, `policy`, `plan`, `process-procedure` for a procedure or practice, `physical` for a facility. Also allowed: `standard`, `guidance`, `interconnection`, `validation`.
- `category` is one of `cui-asset`, `security-protection-asset`, `contractor-risk-managed-asset`, `specialized-asset`, `out-of-scope-asset`. Give it only when every asset behind the component shares it; an asset that gives none takes it. Otherwise leave it off: the category belongs on each asset, and a component whose assets span categories is split.
- The body is the description: what the component is. It is required.
- `remarks` is for a provider: how it was placed.

**Assets.** An asset is one row of the inventory: a real laptop, server, tenant, or device, and an instance of one component. It is listed under that component's `assets`.

- `id` is the client's own name for it: its hostname, asset tag, or tenant name. Asset ids are unique across the whole SSP.
- `category` is required unless the component gives one, and must not contradict the component's.
- A Specialized Asset gives `kind`: `iot`, `iiot`, `ot`, `gfe`, `restricted-information-system`, or `test-equipment`. No other asset has one.
- An Out-of-Scope Asset gives `justification`: why it cannot process, store, or transmit CUI. No other asset has one.
- `description` and `remarks` are optional. With no description the view shows the id.

**Providers.** An outside provider (an ESP, or a CSP, which is the cloud kind of ESP) is a `service` component with a `provider` block:

```yaml
---
title: Microsoft 365 GCC High
type: service
category: cui-asset
provider:
  role: csp
  fedramp-status: fedramp-moderate-authorized
  date-authorized: "2020-01-15"
assets:
  - id: acme.onmicrosoft.us
---

Email, files, and Teams.
```

- `role` is one of `csp`, `msp`, `mssp`, `soc`, `rmm`, `other-esp`. A provider has exactly one role. A company doing two jobs, such as an MSP that also runs the SOC, is two components, one per role, so each role carries its own statements.
- A `csp` gives `fedramp-status`: `fedramp-moderate-authorized`, `fedramp-moderate-equivalent`, or `none`. Any other role must not; the FedRAMP bar is for cloud providers that hold CUI.
- A FedRAMP Moderate authorized CSP gives `date-authorized`, in quotes, from its FedRAMP Marketplace listing. No other provider does.
- The body says what the provider does for the organization; `remarks` carries how it was placed: the access model, the data it holds or reaches, and who sits behind it.
- The responsibility matrix, `view/esp-responsibility-matrix.md`, is generated from this and from the statements on providers' components. It is never written by hand.

**`ssp/<requirement>.md`.** One statement says how one component meets one assessment objective (ADR-0008). People write an objective as `3.5.3[a]`; in the file it is the letter under `objectives`.

```yaml
---
requirement: 3.5.3
family: IA
objectives:
  a:
    - component: entra-id
      status: implemented
      statement: Privileged accounts are the members of the Entra ID admin roles, reviewed monthly.
  b:
    - component: this-system
      status: planned
      statement: Not yet written.
    - component: mobile-devices
      status: not-applicable
      statement: No privileged account exists on the phones.
      remarks: Phones are enrolled as user devices; no local administrator account is available.
---
```

- `component` is a component's slug, or `this-system`, the placeholder, which has no file.
- `status` is one of `implemented`, `partial`, `planned`, `alternative`, `not-applicable`.
- `statement` says how the component meets the objective. It never names its own component: it is attached to it.
- `alternative` and `not-applicable` give the reason in `remarks`. An alternative is met another way; not applicable does not apply to this component. Do not use one for the other.
- Every objective of the requirement is present, and no other. The body below the frontmatter carries the requirement and objective text for people; leave it as setup wrote it.

**The placeholder rule (ADR-0011).** `this-system` with `status: planned` and `statement: Not yet written.` stands on an objective exactly while no component answers it. A not applicable statement says the objective does not bear on that one component; it does not answer it. So:

- when any component has a statement with a status other than `not-applicable`, the objective has no `this-system` entry;
- when every statement is `not-applicable`, or there is none, the `this-system` entry is there, first;
- `this-system` is never given any other status or text.

**Writing the YAML.** The check reads a strict subset of YAML and refuses anything else with the line number, so write it the way the examples are written:

- indent with two spaces, never tabs;
- write a value on one line. Quote it in double quotes when it contains `: ` or ` #`, ends with `:`, starts with a character other than a letter, a digit, or `(`, or looks like a number, a date, `yes`, `no`, `true`, `false`, or `null`. Inside double quotes, write `\"` for a quote and `\\` for a backslash;
- for a long statement, a line of any length is fine, or use `>-` and indent the lines below it.

## Recording a change

Run every step from the engagement repo.

1. **Restate the decision** you were asked to record, in domain terms: which component, asset, or provider; what kind; which category; for a statement, which objective, which status, and the reason; and why. If the caller left out something the edit needs, ask the caller, or the operator, rather than guess.
2. **Start from a clean record.** Run `git status --porcelain -- ssp/`. If it lists anything, stop: the SSP has changes nobody recorded through scribe. Tell the operator, and do not edit until they commit or discard them. If the engagement is not a git repo, stop and ask the operator to run `git init` and commit; scribe restores the record with git.
3. **Edit the files** for the operation, below. Several decisions from one caller, such as a pass over a family or a component's not applicable rows, are one change: make every edit, then check once.
4. **Run the check:**

   ```sh
   python3 <path to this skill>/check_ssp.py .
   ```

   It prints one line per problem, naming the file and, for a statement, the objective, and exits 1; or it prints `check_ssp: ok` and a count. If it cannot find the requirements reference, give it `--requirements <skills repo>/reference/nist-800-171r2-requirements.json`.
5. **If the check fails, restore the record** and report the refusal:

   ```sh
   git restore --source=HEAD --staged --worktree -- ssp/
   git clean -fdq -- ssp/
   ```

   A refusal is an answer, not an error to work around. Quote the check's lines to the caller in their terms, for example "`ssp/components/shop-floor.md: asset "CMM-PC" has the category "cui-asets"`: that is not one of the five CMMC asset categories". Fix the edit only when the mistake was yours, such as an unquoted colon; never change a decision the caller made to get past the check.
6. **If it passes, render the view and commit** the record and the view together:

   ```sh
   python3 <path to this skill>/render_view.py .
   git add ssp/ view/
   git commit -m "scribe: <the change in one line>"
   ```

7. **Report the outcome** to the caller in one line: what was recorded, or the refusal and its reason.

## Operations

Each is an edit to the files, then steps 4 to 7.

**Add a component.** Make its slug from its title and write `ssp/components/<slug>.md`. If a file with that slug exists and says the same, nothing changes; if it says something different, the component is already recorded: change it instead, or pick a title that tells the two apart.

**Change a component.** Edit its fields or its body. Changing `title` alone keeps the slug, so every statement stays attached.

**Rename a component's slug.** When the title change should show in the slug too, move the file with `git mv ssp/components/<old>.md ssp/components/<new>.md`, then change `component: <old>` to `component: <new>` in every requirement file; `grep -l "component: <old>$" ssp/*.md` lists them. The check fails if any reference is left.

**Split a component.** When the assets behind one component fall in different categories, or will need different conformity statements, write the new component's file, move the named asset entries to it, and set each component's `category` to what its assets share, or remove it. The new component is the same kind of thing as the old: copy its `type`, and for a provider its `provider` block and `remarks`, so both halves keep the role and FedRAMP status.

**Remove a component.** Refused while it has assets or written statements: move its assets to another component, and clear or remove its statements first. Its cleared statements, planned and "Not yet written.", go with it: delete those entries, and put `this-system` back on any objective the placeholder rule now needs it on. Then delete the file. `this-system` cannot be added, changed, or removed.

**Add, change, move, or remove an asset.** Add, edit, or delete the entry under the component's `assets`. To move an asset to another component, cut the entry from one and paste it under the other, checking that its category agrees with its new component's.

**Add or change a provider.** Write or edit the component's `provider` block, `remarks`, and body by the rules above. Changing a CSP away from FedRAMP Moderate authorized removes its `date-authorized`. A provider's assets, such as the organization's tenant or the provider's RMM tool, are listed under its `assets` like any other.

**Set a statement.** In `ssp/<requirement>.md`, under the objective's letter, replace the named component's entry, or add one. Then apply the placeholder rule to that objective. A statement names a recorded component, never `this-system`.

**Clear a statement.** Set the component's entry to `status: planned` and `statement: Not yet written.`, and delete its `remarks`. The component still owes the objective; its statement is not written yet. The placeholder stays away, since the component still answers the objective.

**Remove a statement.** When a component should never have described the objective, such as an enforcement sentence written on a definition objective's wrong component, delete its entry instead of clearing it. Then apply the placeholder rule: an objective left with only not applicable statements, or none, gets `this-system` back. Record the statement on the right component first, so the objective is never left with nothing but the placeholder.

## What the engagement holds after a change

- `ssp/`: the record, as above. Skills that need the SSP read these files; the statements are fields in each requirement file's frontmatter.
- `view/asset-inventory.md`: generated for people, opening with a notice that it is generated. It lists components, providers with their FedRAMP status, and assets grouped by category, out-of-scope ones with their justification. No skill reads it.
- `view/esp-responsibility-matrix.md`: generated for people, opening with the same notice. It lists each provider with its role, CSP or ESP, FedRAMP status, what it does, and its remarks; the provider's assets; and, per objective a provider has a statement on, every component's statement, each marked as the provider's or the company's; the statement text says who performs each part. It is the document a provider signs; the signed copy is evidence. No skill reads it.
- `view/requirements/3.5.3.md`, one per requirement: generated for people, opening with the same notice. Each objective is a heading in `3.5.3[a]` form, with the statement, status, and remarks of every component that describes it. No skill reads it.

## Sources

- ADR-0012, the record as Markdown and its one writer: `docs/adr/0012-markdown-ssp-replaces-oscal.md`
- ADR-0008, statements on objectives: `docs/adr/0008-conformity-statements-attach-to-objectives.md`
- ADR-0011, clear, remove, and the placeholder: `docs/adr/0011-statement-operations-and-the-placeholder.md`
- The fields and their values in one table: `reference/ssp-fields.md`
- The asset categories, provider roles, and statuses: `CONTEXT.md`
