# Cold run: fips-crypto-scoping

Date: 2026-09-28. Skill under test: `skills/domain/m365/fips-crypto-scoping`, after it began recording its out-of-scope verdicts through scribe (#102). One run on a fresh copy made by `python3 scripts/cold_run.py`. The tester got the SKILL.md, scribe's folder, the scratch engagement, and the fixture company files. The answer key and the rubric were withheld, and every other skill was unavailable. A second agent graded the run without seeing the SKILL.md.

## Prompt

"Northstar wants to sell Saguaro FIPS switches and a FIPS firewall. Go through every network device and encryption point and tell me what actually needs FIPS, and record whatever is out of scope. There's no data flow file in the repo yet; treat the company's network diagram and IT write-up as the mapped flow. Nobody at Saguaro can be asked today. Don't stop to ask me, just record and show me the verdicts at the end."

## Result

| Check | Score |
|---|---|
| Shape match | 2 |
| Known-answer match | 2 |
| Scrub check | 2 |
| Record validity | 2 |
| Record match | 2 |
| Total | 10 |

Pass. The run recorded nothing, which is what 6.14 asks: the LAN is flat with no enclave, so no device clears the out-of-scope question. `check_record.py --baseline` shows no change; `ssp/` and `view/` are identical to the fixture. The only output is the working note `scope/fips-verdicts.md`: switches need no FIPS module, the firewall needs one only while it terminates a CUI-carrying VPN with no validated inner layer, and the money belongs on the endpoints (BitLocker without the FIPS Algorithm Policy), the NAS's non-validated SMB module, printing, and the cloud tenant, matching 6.3's 3.13.11 finding.

## What the run found, and what changed

**The key and the skill disagreed on the EdgeRouter.** The skill's device tree places a VPN device that terminates the tunnel at Q1, a CUI Asset; 6.2 said Security Protection Asset. The grader held both defensible: the router terminates Dana's VPN, holds its keys, and forwards the RDP session that carries CUI, and 32 CFR 170.19(c) makes an asset an SPA whether or not it transmits CUI. 6.2 and 6.14 now pass either, with the reason. Nothing was recorded either way, so the record was unaffected.

**Gaps in the skill, now closed**: it had no fallback when the operator names a substitute for the missing flow map (it now works from the named sources and says so, as `cmmc-scope-boundary` does); it never said that recording nothing is the expected result on a flat network; its handoff rule covered only network devices, so MFP-FRONT and the phones, recorded out of scope while handling CUI, had nowhere to go (they now go to `cmmc-scope-boundary`); and "Open gaps" pointed at step 8 instead of step 9.

## Left as found

The tester raised points about the device tree itself, which this change did not alter: a switch that carries plaintext CUI without holding keys falls to Q3, whose "meet 3.13.11 on it" remedy does not fit hardware that cannot host cryptography; the tree does not point back to step 5 (layered encryption) for a device that terminates an outer tunnel; "both ends need a validated module" is stated only for cloud sessions; FIPS mode off on a possibly validated module has no stated finding; and the verdict table has no "unknown" state. Each is a method question for a later change to the skill.
