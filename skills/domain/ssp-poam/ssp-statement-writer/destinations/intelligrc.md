# Destination: IntelliGRC

The engagement keeps its conformity statements in IntelliGRC, as the implementation detail of each assessment objective in an evaluation. The repo's `ssp/` files, when they exist, hold only the scope; do not record statements there too.

## How IntelliGRC holds a statement

- **One text per objective.** IntelliGRC has no component. When several platforms carry an enforcement objective, write one statement that names the mechanism for each, one sentence per platform, rather than one paragraph per component.
- **Objective names** read `CM.L2-3.4.1[a]`: the CMMC practice id, then the objective letter.
- **Status** is a separate field. Its values come from `intelligrc lookup assessment-objective statuses`.
- **The text is HTML.** Wrap each statement in `<p>` and escape `&`, `<`, and `>`.
- **Some inventories are only in the web app.** The API does not read the Assets inventories (devices, network, software). When a statement names an inventory's columns, ask the operator for them.

## Reading the current text

Find the evaluation with `intelligrc evaluation list --profile <profile>` (usually the current one), then read the family:

```sh
intelligrc assessment-objective list --profile <profile> --evaluation-id <evaluation>
```

Each record carries `id`, `name`, `description` (the objective's words), `status`, `implementationDetail`, `findingDetail`, `recommendationDetail`, and `validationMethods`.

## Reading a precedent in another tenant

A precedent SSP may sit in another IntelliGRC tenant, such as the MSP's own, under its own profile. Its objectives may be named by another framework's ids (SCF ids such as `CFG-03_A01`, not `CM.L2-3.4.6[a]`). Match them by the `description`, the objective's words, not by the name. Read only: never write to the precedent's tenant.

## Recording

Once the operator says to record:

1. **Back up first.** Before the first write to a family, save every field of every objective in it to a JSON file in the engagement's scratch folder. Keep it until the operator is satisfied.
2. **Send every field the record should keep.** The update operation's handling of an omitted field is undocumented, so each write resends the current status and finding with the new text:

   ```sh
   intelligrc assessment-objective update <id> --profile <profile> --evaluation-id <evaluation> \
     --status-id <current status id> --implementation-detail '<p>...</p>' \
     --finding-detail '<current finding, when there is one>'
   ```

   In the as-if-met mode the status id is always the objective's current one. In the as-is mode it is the status the operator approved.
3. **Write one objective first** on a new family, and confirm the returned record before writing the rest.
4. **Verify every write.** The command prints the record IntelliGRC stored. Check that the text is exactly what was approved and that the status and finding did not move. Report any that differ.
5. **Save the approved text** for the requirement to a JSON file beside the backup, so the next pass starts from what the operator approved.
