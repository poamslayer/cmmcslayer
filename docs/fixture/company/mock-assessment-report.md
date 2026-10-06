# Mock Assessment Report

Prepared by an RPO, March 2026. Fictional. Prose-style, loose paragraphs, no objective letters, and a mix of observations and opinions, reproduced here as received.

## Finding 1

The Entra ID user list was reviewed and is being offered as the authorized user list for the environment. It shows twelve Saguaro accounts plus the two Northstar administrator accounts.

## Finding 2

SHOP-PC-01, at the Haas machine, has a single local account named "shop" that both Kevin Marsh and Ana Delgado use across their shifts. There is no way to tell from the machine's logs which of them did what.

## Finding 3

The SAG-NAS device has no logging enabled anywhere in its admin console. If something happened on that box last month there would be no record of it.

## Finding 4

Drawings are printed and left on a clipboard at the machine for the length of the job, and old travelers, which carry the drawing thumbnail, go into the shop's ordinary recycling dumpster once the job ships.

## Finding 5

The finisher, Sonoran Anodize and Plating, receives the drawing as a PDF attached to the purchase order email. Sonoran has no IT staff and no plans for CMMC.

## Finding 6

We recommend Saguaro buy a SIEM and stand up a 24/7 SOC to get ahead of this before the assessment.

## Additional note

Microsoft 365 multifactor authentication was checked and found to be missing, so this is recorded here as a gap needing remediation.

(Fixture note: this last item is a plant. Conditional Access already requires MFA for all users. The consultant in this fixture did not check the Conditional Access policy before writing the finding.)
