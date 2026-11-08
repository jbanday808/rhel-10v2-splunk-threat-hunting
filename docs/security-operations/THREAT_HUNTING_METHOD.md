# Detailed Threat-Hunting Method, Plans, Briefings and Reports

**Status:** proposed method and lab examples. A hunt is an evidence-driven investigation with a question and a bounded scope. The artifacts below make it reviewable and repeatable; they do not claim validated detection coverage.

## Step 1 — Define the mission question

Start a [detailed hunt plan](templates/threat-hunt-plan.md). Identify the service/asset owner, business concern, trigger and scope. Examples: “Did the test endpoint create a pipe matching a selected default-style pattern?” or “Did the client use a hostname outside the approved HTTP baseline?” Avoid starting with a tool name and assuming compromise.

## Step 2 — Write a falsifiable hypothesis

Describe the expected behavior, affected population, evidence that would support it, evidence that would weaken it and likely benign alternatives. Record ATT&CK technique/version and mapping rationale where useful. A technique mapping is context, not evidence that the adversary used it.

## Step 3 — Agree on scope and authority

Record approved hosts, accounts, network segments, data classes, UTC period, analysis environment and permitted methods. Identify excluded assets, mission constraints, data movement restrictions, owner, reviewers and stop/escalation conditions. Keep active tests and response actions separate from read-only hunting authority.

## Step 4 — Verify telemetry and visibility

List each required source, actual schema/field names, event time versus ingestion time, retention, latency, permissions, coverage and known exclusions. Confirm source events and indexed copies before tuning a query. For packets, establish the authorized capture point, directions, loss and encryption limits. No data is not the same as no activity.

## Step 5 — Establish a representative baseline

Compare similar-duration windows and asset roles; annotate maintenance, software changes and approved tests. Describe the population, expected services/peers and collection changes. Thresholds must come from measured context and an agreed purpose, not an arbitrary claim that every rare event is malicious.

## Step 6 — Choose queries and pivot keys

Record query file, repository commit, parameters, exact time bounds and field assumptions. Prefer host plus process GUID for process correlation; use time and the observed network tuple for flow comparisons. Explain shared identifiers such as Community ID only when enabled and verified. Do not join all activity by PID or IP alone.

## Step 7 — Define controls and success criteria

For a simulation, identify matching and nonmatching controls, expected source events, indexed events, search results and cleanup. Verify that the negative control was collected before calling its absence from a hunt a success. Keep schema tests, endpoint execution, forwarding, search execution, analyst conclusion and alert delivery as separate outcomes.

## Step 8 — Execute and log the investigation

Run approved searches one at a time, save versions/time windows privately and record job warnings. Inspect underlying events instead of treating a chart as the source of truth. Link every material observation to an evidence ID, source and time. Record contradictory observations and failed collection attempts.

## Step 9 — Examine artifacts and build a timeline

Use approved acquisition and forensic methods for relevant process, file, persistence, identity and packet artifacts. Maintain original evidence and working copies. Normalize display times to UTC while retaining original timezone/clock uncertainty. Do not invent a causal link because events happened close together.

## Step 10 — Test alternatives and expand deliberately

Ask the owner about authorized activity. Compare other available sources and document confidence. Expand hosts or time only within authority; record the change and its impact on baselines. Move to the [incident workflow](INCIDENT_MANAGEMENT.md) when adverse activity warrants response, and link exposures through the [vulnerability workflow](VULNERABILITY_MANAGEMENT.md).

## Step 11 — Brief decisions, not just data

Use the [six-slide briefing](templates/hunt-briefing.md). State the question, observed scope, strongest evidence, uncertainty, mission impact, recommendation and decision needed. Tailor the leadership view to risk and decisions, and the analyst view to methods, pivot keys and next actions. Record the decision owner and next update time.

## Step 12 — Write the detailed report

Use the [hunt report](templates/threat-hunt-report.md). Separate facts, hypotheses, limitations and recommendations. Include negative results, telemetry coverage, tested controls, alternative explanations, residual risks, linked case IDs, owners and retest dates. Identify content drafted with AI and how a human verified it.

## Step 13 — Handover, improve and retest

Transfer unresolved findings with acknowledged ownership. Propose a detection or telemetry improvement with a test plan, false-positive review, change owner and rollback. Verify any later scheduled search/alert separately. Preserve approved evidence and remove test artifacts under the retention plan.

## Outcome vocabulary

| Outcome | Required basis |
| --- | --- |
| Supported | Reviewed evidence supports the scoped hypothesis, with remaining uncertainty stated |
| Not supported within observed scope | The reviewed data and coverage do not support it; state what was tested and limits |
| Benign / authorized exercise | Owner confirmation and evidence explain the specific activity |
| Inconclusive | Missing data, uncertain scope, extraction gaps or insufficient corroboration prevent a conclusion |
| Escalated | Incident/vulnerability owner accepted the linked case and next action |

An empty result set generally needs coverage review before it supports any negative conclusion. Avoid claims of “100% detection” from a tiny fixture or a single Atomic test.

## Two worked plans using existing lab content

| Plan element | Named-pipe review | Passive HTTP review |
| --- | --- | --- |
| Question | Are selected default-style pipe names observable and reviewable? | Did the client request an unexpected HTTP host? |
| Source | Sysmon process/pipe events in the existing `sysmon` index | Same synthetic PCAP through Zeek/Suricata and optional Arkime; approved synthetic Splunk upload |
| Procedure | [Atomic and SPL guide](../splunk/COBALT_STRIKE_ATOMIC_VALIDATION.md) | [Worked HTTP investigation](../network-defense/OFFLINE_HTTP_WALKTHROUGH.md) |
| Controls | Matching `postex_` name; collected nonmatching lab name | Routine hostname; candidate hostname and inert body marker |
| Critical gap | Baseline Sysmon lacks PipeEvent until a reviewed merge; custom names can evade the narrow hunt | Small generated dataset, no real mirror/traffic coverage, encrypted content not visible by default |
| Supported conclusion | Pattern behavior and collection only if actually observed; not product attribution | A scoped synthetic outlier, not evidence of compromise or root cause |
| Escalation | Validate actual PenTest scope or unexplained activity with owner | Validate alias/service/encryption policy with owner |

Record actual execution and findings only after testing. For broader network questions use the [Arkime playbook](../arkime/HUNTING_PLAYBOOK.md) and [network CONOPS](../network-defense/CONOPS.md). The existing [short hunt report](../hunt-report-template.md) remains useful for a compact record.
