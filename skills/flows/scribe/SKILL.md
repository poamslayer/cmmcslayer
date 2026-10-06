---
name: scribe
description: Record a decision in the engagement's SSP, `ssp.json`, the OSCAL document that is the record, or show what the record holds. The only skill that ever changes that file. Other skills call it with what was decided, in domain terms; scribe makes the change, validates it with oscal-cli, keeps it only if it passes, and re-renders the read-only view. Skills that read the SSP call it to show the record, so they never read the view.
---

# Scribe

The engagement's System Security Plan is one OSCAL document, `ssp/ssp.json`, and it is the record (ADR-0007). Scribe is the only thing that changes it. A skill that decides something (a component exists, an asset is a CUI Asset, an objective is met by a component) calls the Skill tool with `scribe` and says what was decided in the words of the engagement. The caller never needs to know OSCAL's shape; scribe does.

Never edit `ssp.json` by hand, and never edit anything under `view/`. The view is generated from the record and overwritten on every change.

A skill that needs to know what the SSP says (the components, the assets and their categories, the providers, the statements and their statuses) also calls scribe, and asks it to show the record. Scribe reads `ssp.json` at that moment, so the answer is never stale the way the view can be.

## The edit command

Every change goes through one command, `ssp_edit.py` in this skill's folder, run from the engagement repo:

```sh
python3 <path to this skill>/ssp_edit.py --engagement . <operation> [options]
```

Each run applies one operation. It reads the current `ssp.json`, applies the change, keeps every existing UUID, mints a new one only for a new object, writes the result to a temporary file, runs oscal-cli with the constraints file in `reference/oscal/`, and replaces `ssp.json` only if oscal-cli passes. Then it re-renders the view. On any failure it exits non-zero, prints `scribe: <operation> refused: <reason>`, and leaves `ssp.json` and the view exactly as they were.

It needs Java 11 or later and oscal-cli 3.2.0 on PATH. If either is missing the command stops; it never writes an unvalidated change. Tell the operator to run `bash scripts/install_oscal_cli.sh` in the skills repo.

### Operations

**Create the SSP.** Once per engagement, before any other operation.

```sh
python3 ssp_edit.py --engagement . create --system-name "<client or system name>"
```

Writes `ssp/ssp.json` with our profile of all 110 requirements imported, one implemented requirement per requirement, and one statement per assessment objective, every one `planned`. A placeholder component, "This System", carries those planned statements so the document is valid before scoping names anything. It copies the pinned profile and catalog into `ssp/oscal/`, so the record resolves on any machine. It refuses if `ssp.json` already exists.

**Add a component.** A named part of the system that conformity statements will describe once: "Entra ID", "Windows 11 laptops (engineering)", "Access Control Policy".

```sh
python3 ssp_edit.py --engagement . add-component \
  --title "Entra ID" --type service \
  --description "Identity provider for every user account." \
  [--category security-protection-asset]
```

- `--type` is the OSCAL component type. Use `service` for a cloud service or tenant, `software` for installed software, `hardware` for a class of devices, `policy` for a policy, `plan` for a plan, `process-procedure` for a procedure or practice, `physical` for a facility.
- `--category` is one of `cui-asset`, `security-protection-asset`, `contractor-risk-managed-asset`, `specialized-asset`, `out-of-scope-asset`. Give it only when every asset behind the component shares that category. Otherwise leave it off: the category belongs on the asset, and a component whose assets span categories is split.
- A component is identified by its title. Adding one that is already recorded with the same fields changes nothing. Adding one with the same title and different fields is refused.

**Change, rename, split, or remove a component.**

```sh
python3 ssp_edit.py --engagement . change-component --title "Entra ID" [--type ...] [--description ...] [--category ... | --clear-category]
python3 ssp_edit.py --engagement . rename-component --title "Windows 11 laptops" --new-title "Company laptops"
python3 ssp_edit.py --engagement . split-component --title "Company laptops" \
  --into "Company laptops (engineering)" --assets "ENG-LT-01,ENG-LT-02" [--category cui-asset]
python3 ssp_edit.py --engagement . remove-component --title "Old firewall" [--move-assets-to "New firewall"]
```

- A rename keeps the component's UUID, so its assets and statements stay attached. Renaming a provider renames its leveraged authorization too.
- Split when the assets behind one component fall in different categories, or will need different conformity statements. The named assets move to the new component; the rest stay.
- Remove is refused while assets point at the component, unless `--move-assets-to` names where they go, and while any conformity statement still describes it: clear those first. "This System" cannot be changed, renamed, or removed.

**Add, change, or remove an asset.** An asset is one row of the inventory: a real laptop, server, tenant, or device, and an instance of one component. The category belongs here.

```sh
python3 ssp_edit.py --engagement . add-asset --name "ENG-LT-01" --component "Windows 11 laptops" \
  --category cui-asset [--description "Engineering laptop, Dell 7440"] [--remarks "..."]
python3 ssp_edit.py --engagement . add-asset --name "VF-2 mill" --component "Haas mills" \
  --category specialized-asset --specialized-type ot
python3 ssp_edit.py --engagement . add-asset --name "Guest AP" --component "Guest Wi-Fi" \
  --category out-of-scope-asset --remarks "Separate ISP line; no route to any CUI asset."
python3 ssp_edit.py --engagement . change-asset --name "FO-LT-01" [--category ...] [--specialized-type ...] [--component ...] [--new-name ...] [--description ...] [--remarks ...]
python3 ssp_edit.py --engagement . remove-asset --name "FO-LT-01"
```

- `--name` identifies the asset: its hostname, asset tag, or tenant name.
- `--category` is required unless the component carries a category, in which case the asset takes it.
- A Specialized Asset must give `--specialized-type`: `iot`, `iiot`, `ot`, `gfe`, `restricted-information-system`, or `test-equipment`.
- An Out-of-Scope Asset must give `--remarks` with its justification: why it cannot process, store, or transmit CUI.
- An asset whose category differs from its component's category is refused. Split the component, or clear its category with `change-component --clear-category`.

**Add or change a provider.** An outside provider (an ESP, or a CSP, which is the cloud kind of ESP) is a service component with its role and, for a CSP, its FedRAMP status.

```sh
python3 ssp_edit.py --engagement . add-provider --title "Microsoft 365 GCC High" --role csp \
  --description "Email, files, and Teams." \
  --fedramp-status fedramp-moderate-authorized --date-authorized 2020-01-15
python3 ssp_edit.py --engagement . add-provider --title "Acme MSP" --role msp \
  --description "Manages endpoints and patching." \
  --remarks "Account test: standing Global Administrator accounts, unattended RMM remote control. Holds: CUI reach."
python3 ssp_edit.py --engagement . change-provider --title "Acme MSP" [--role ...] [--fedramp-status ...] [--date-authorized ...] [--description ...] [--remarks ...]
```

- `--role` is one of `csp`, `msp`, `mssp`, `soc`, `rmm`, `other-esp`. A provider has exactly one role. A company doing two jobs, such as an MSP that also runs the SOC, is recorded as two providers, one per role, so each role carries its own statements.
- `--description` says what the provider does for the organization. `--remarks` carries how it was placed: the access model, the data it holds or reaches, and who sits behind it. `--remarks ""` on change-provider clears them.
- A `csp` must give `--fedramp-status`: `fedramp-moderate-authorized`, `fedramp-moderate-equivalent`, or `none`. Any other role must not; the FedRAMP bar is for cloud providers that hold CUI.
- A FedRAMP Moderate authorized CSP is also recorded as a leveraged authorization, and needs `--date-authorized` from its FedRAMP Marketplace listing. Changing its status away from authorized drops the leveraged authorization.
- Assets of a provider, such as the organization's tenant or the provider's RMM tool, are added with `add-asset` like any other.
- The responsibility matrix is generated from this, never written by hand: `view/esp-responsibility-matrix.md` lists each provider, its assets, and, per objective, the conformity statements on the provider's component beside the company's.

**Set or clear a conformity statement.** One statement says how one component meets one assessment objective (ADR-0008). Write the objective as people do, `3.5.3[a]`; scribe translates it to the catalog's objective and refuses one the catalog does not have, such as 3.5.3[e].

```sh
python3 ssp_edit.py --engagement . set-statement --objective "3.5.3[a]" --component "Entra ID" \
  --status implemented \
  --statement "Privileged accounts are the members of the Entra ID admin roles, reviewed monthly."
python3 ssp_edit.py --engagement . set-statement --objective "3.5.3[a]" --component "Mobile devices" \
  --status not-applicable --statement "No privileged account exists on the phones." \
  --remarks "Phones are enrolled as user devices; no local administrator account is available."
python3 ssp_edit.py --engagement . clear-statement --objective "3.5.3[a]" --component "Entra ID"
```

- `--status` is one of `implemented`, `partial`, `planned`, `alternative`, `not-applicable`.
- `alternative` and `not-applicable` must give `--remarks` with the reason. An alternative is met another way; not applicable does not apply to this component. Do not use one for the other.
- `--component` names a recorded component, never "This System". Setting a statement again for the same objective and component replaces it and keeps its UUID.
- Until a component answers an objective, the objective is planned on "This System". The first statement with any status other than not applicable replaces that placeholder. A not applicable statement says the objective does not bear on that one component, not that it is answered, so an objective whose statements are all not applicable stays planned on "This System" beside them, and the record never reads as if a requirement applies nowhere.
- Clearing a statement returns the objective to planned for that component: the component still owes the objective, and its statement is not written yet. A component whose statements are all cleared can be removed; an objective left with no component is planned on "This System" again.
- When a component should never have described the objective, such as an enforcement sentence written on a definition objective's wrong component, remove it instead of clearing it. It is taken off the objective and not left planned there:

  ```sh
  python3 ssp_edit.py --engagement . remove-statement --objective "3.1.8[a]" --component "Microsoft 365 commercial tenant"
  ```

  Record the statement on the right component first, so the objective is never left with nothing but the placeholder.

**Set many statements at once.** A pass over a family, or a component's not applicable rows, is many statements. Each `set-statement` starts oscal-cli, which takes seconds, so give them to scribe as one file instead:

```sh
python3 ssp_edit.py --engagement . set-statements --file .scratch/statements-3.1.json
```

```json
[
  {"objective": "3.1.1[a]", "component": "Access control procedure", "status": "implemented",
   "statement": "Authorized users are the people the owner approves in writing on the access request form."},
  {"objective": "3.2.1[a]", "component": "EdgeRouter firewall and VPN", "status": "not-applicable",
   "statement": "Awareness training is given to people; a firewall takes none.",
   "remarks": "3.2.1 is written for people, and the firewall is a device."}
]
```

- Each entry is one `set-statement`, with the same fields and the same rules.
- The file is one change: every entry is applied, the result is validated once, and the view is rendered once. If any entry is refused, nothing in the file is recorded, and the refusal names the entry number, its objective, and its component. Fix that entry and run the file again.
- Entries already recorded as they are change nothing, so re-running a file after fixing one entry is safe.
- Write the file under `.scratch/`; it is a working file, not part of the record.

**Re-render the view.** Changes nothing in the record; rebuilds `view/` from `ssp.json`. Use it when the view is missing or was rendered by an older scribe.

```sh
python3 ssp_edit.py --engagement . render
```

**Show the record.** Changes nothing. Reads `ssp.json` now and prints it in domain terms, with no OSCAL ids: the problems in the record, if any; the components, the providers, and the assets by category, as the asset inventory; each provider with its role, FedRAMP status, what it does, and its remarks, and the statements on its component, as the responsibility matrix; and, for each requirement asked, each objective in `3.5.3[a]` form with every component's status, statement, and remarks.

```sh
python3 ssp_edit.py --engagement . show --requirement 3.5.3
python3 ssp_edit.py --engagement . show --requirement 3.1 --requirement 3.13.11
python3 ssp_edit.py --engagement . show
```

- `--requirement` takes a requirement, `3.5.3`, or a family, `3.5`, and repeats. With none, it shows every requirement, which is long; ask for what the caller needs.
- An objective no component answers yet shows as planned on "This System" with "Not yet written." Its statement has not been written.
- **Problems in the record** lists what scribe would refuse and oscal-cli would reject, found in a record someone changed by hand: a statement on a component the record does not have, an asset on a component the record does not have, an asset whose category contradicts its component's, an asset with no category, a category outside the five on an asset or a component, an Out-of-Scope Asset with no justification, and an alternative or not applicable statement with no reason. Each is named in the operator's words. A record scribe wrote has none; say so when it has any, and never fix one by hand.

## Process

To show the record, run `show` for what the caller asked about and hand back its output as it is. Otherwise:

1. **Restate the decision** you were asked to record, in domain terms: which component, asset, or provider; what kind; which category; for a statement, which objective, which status, and the reason; and why. If the caller left something out that the operation needs, ask the caller, or the operator, rather than guess.
2. **Run the one operation** that records it.
3. **Report the outcome** to the caller in one line: what was recorded, or the refusal and its reason, quoted from the command. A refusal is an answer, not an error to work around: never hand-edit the JSON to get past it. Translate the reason into the caller's terms when it names an OSCAL rule, for example "`cmmc-asset-category-values`: `cui-asets` is not one of the five CMMC asset categories".

## What the engagement holds after a change

- `ssp/ssp.json`: the record. Skills that need the SSP read it through `show`.
- `ssp/oscal/`: the profile and catalog the record imports, copied at create.
- `view/asset-inventory.md`: generated for people, opening with a notice that it is generated. It lists components, providers with their FedRAMP status, and assets grouped by category, out-of-scope ones with their justification. No skill reads it.
- `view/esp-responsibility-matrix.md`: generated for people, opening with the same notice. It lists each provider with its role, CSP or ESP, FedRAMP status, what it does, and its remarks; the provider's assets; and, per objective a provider has a statement on, every component's statement, each marked as the provider's or the company's; the statement text says who performs each part. It is the document a provider signs; the signed copy is evidence. No skill reads it.
- `view/requirements/3.5.3.md`, one per requirement: generated for people, opening with the same notice. Each objective is a heading in `3.5.3[a]` form, with the statement, status, and remarks of every component that describes it. No skill reads it; a skill that needs a statement asks scribe to show it from `ssp.json`.

## Sources

- ADR-0007, the record and its one writer: `docs/adr/0007-oscal-ssp-is-the-record-and-scribe-writes-it.md`
- ADR-0009, the catalog, the profile, and our namespace: `docs/adr/0009-adopt-a-pinned-unofficial-rev-2-catalog.md`
- Our fields and their allowed values: `reference/oscal/README.md` and `reference/oscal/cmmc-constraints.xml`
