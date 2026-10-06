# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this engagement repo's issue tracker.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Operator needs to evaluate this finding  |
| `needs-info`               | `needs-info`         | Waiting on the reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires a person to do the work         |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.

## Routing labels

These labels route a ticket to a requirement and a plan. `to-poam` applies them; `remediate` and `audit` read them. They are not triage states and do not replace the table above.

| Label      | Meaning                                                                                                   |
| ---------- | --------------------------------------------------------------------------------------------------------- |
| `poam`     | A POA&M item: a NOT MET requirement with milestones and a 180-day closeout from the Conditional CMMC Status Date |
| `opa`      | An OPA item: a temporary deficiency arising once the system was already compliant, scored MET, with no closeout clock        |
| `req:<id>` | The requirement the ticket covers, for example `req:3.1.1`. Created on first use                          |

A ticket carries exactly one of `poam` or `opa`, and exactly one `req:<id>`. With the local markdown tracker these become the `Type:` and `Requirement:` lines in the ticket file.
