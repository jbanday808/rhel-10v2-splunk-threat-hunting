# Synthetic Tabletop — Hunt, Incident, Vulnerability and AI Review

**Status:** exercise instructions only. All injects below are fictional training inputs. They are not reports from WINHUNT01, a Trellix installation, a customer, or a PenTest team. No real incident, product action or model call occurs by reading this document or running the helper.

## Step 1 — Prepare the exercise

Assign functional analyst, coordinator, system owner, forensic reviewer and vulnerability owner roles, even if one learner covers several. Select a facilitator, time window, learning goals and private worksheet location. Copy the [plan](templates/threat-hunt-plan.md), [incident](templates/incident-record.md), [vulnerability](templates/vulnerability-record.md), [briefing](templates/hunt-briefing.md) and [report](templates/threat-hunt-report.md) templates into that private location.

Expected output: a bounded exercise with named role responsibilities, evidence conventions and completion criteria. Do not add actual customer identifiers to the public copies.

## Step 2 — Intake inject

Fictional input: an analyst sees a pipe name resembling `postex_a1b2c3d4` in a constructed event summary. No original event or supporting process history is supplied.

Open a case, record the source and uncertainty, and decide what telemetry must be checked before declaring an incident. Explain why the name alone does not identify a Cobalt Strike Beacon or prove compromise. Use the [named-pipe guide](../../hunts/cobalt-strike/COBALT_STRIKE_ATOMIC_VALIDATION.md) to identify required events, fields and controls; run that separate lab only if it is approved and ready.

Expected output: a hypothesis, evidence gap, initial disposition, owner and next action. Priority must follow the chosen exercise policy and business impact, not a product label.

## Step 3 — Context and decision inject

Fictional input: an exercise owner states that a server-only Atomic test was planned. The facilitator has not supplied native event logs, actual execution records or proof of authorization for a real host.

Separate the plan from observed execution. Identify the operator/scope confirmation, collected nonmatching control, indexed events and process history needed for a benign-exercise conclusion. Record a bounded next investigation; do not automatically suppress all events from that host or account.

Expected output: a reviewed disposition of inconclusive or a conditional exercise explanation, with the missing evidence named.

## Step 4 — Vulnerability inject

Fictional input: a separate synthetic HTTP case shows a cleartext download using a hostname outside the exercise baseline. It is not evidence that the named-pipe activity caused the connection.

Use the [worked HTTP case](../network-defense/OFFLINE_HTTP_WALKTHROUGH.md) to explain the observed tuple, HTTP host and limitations. Open a linked vulnerability/misconfiguration record for owner validation of service/alias/encryption policy, without inventing a CVE or claiming exploitation. Assign a risk review and retest plan under the chosen policy.

Expected output: a distinct finding with applicability still to validate, owner, approved next check and no unsupported causal link.

## Step 5 — AI review inject

Run the synthetic packet preparation and illustrative-response validation from [AI-assisted forensics](AI_ASSISTED_FORENSICS.md). Inspect the source summaries and human-review requirement. The example response is analyst-authored, not evidence of an AI execution.

As a negative validation test, copy the illustrative response into the private run directory, replace one evidence ID with `E999`, and run the validator on that copy. Expect rejection. Preserve the original example.

Fictional input: a model produces “Cobalt Strike is confirmed” while citing valid E001/E002 IDs. Discuss why citation existence alone cannot validate the conclusion. A schema checker may pass it; the human reviewer must reject the unsupported attribution.

Expected output: one structural failure correctly detected, one unsupported conclusion rejected through human review, and an explicit statement that no external AI service was used unless separately approved and actually tested.

## Step 6 — Brief the owner

Use the six-part [briefing outline](templates/hunt-briefing.md). State observed synthetic facts, uncertainty, mission-risk assumptions, current actions, the decision needed, accountable owners and the next update. Record handoff acknowledgment.

Expected output: a decision-focused briefing with no claim of confirmed compromise, actual Trellix deployment or completed remediation.

## Step 7 — Report and hand over

Complete the [detailed report](templates/threat-hunt-report.md) and [engagement closeout](templates/engagement-closeout.md) for the exercise. Mark unperformed collections, changes, training or live tests as pending/unperformed. Keep operational findings and commercial records out of the public repository.

Expected output: linked case/hunt/finding IDs, evidence gaps, conclusions, owners, dates/review points, control improvements and retention decisions.

## Step 8 — Assess the exercise

Record actual learner outcomes in the [sanitized validation template](../../evidence/sanitized/security-operations-validation.md). Review whether the learner separated source facts from inferences, preserved evidence boundaries, identified authorities, used controls, rejected unsupported AI claims and transferred open actions clearly.

Do not report faster response or improved accuracy without measured baseline and test results. Use lessons to revise the process and repeat the exercise before treating it as an operational capability.
