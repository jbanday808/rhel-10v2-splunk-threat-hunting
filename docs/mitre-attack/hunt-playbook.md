# Hypothesis-driven threat-hunting playbook

Use this playbook for the isolated lab or another environment where the hunt is
explicitly authorized. It is an investigation workflow, not an automated
response. All example thresholds are starting points, not established detections.

## 1. Scope and formulate the hypothesis

1. Record the objective, authorized hosts and accounts, time range, analyst,
   owner, expected maintenance, and escalation contact. Use UTC for evidence.
2. Select a behavior from the [ATT&CK mapping](coverage.md), a public intelligence
   report, a previous incident, or a visibility gap. Record the exact source and
   publication date; do not turn uncorroborated IOCs into a claim of compromise.
3. Write a falsifiable hypothesis with a benign alternative. Example: “An
   unexpected PowerShell process may contact a network destination after being
   launched by an unusual parent.” A legitimate administration script or software
   update is an alternative explanation.
4. Define the expected source events and pivots **before** running the search:
   host, account/SID, process GUID, event time, parent, destination and source.
   Record what data could disprove the hypothesis and what is missing.

## 2. Establish telemetry and a baseline

Run [data health](../../hunts/00-data-health.spl) in the lab app. Confirm that
the intended index, host, sourcetype, and time window contain recent events.
The six indexes are `win_security`, `win_system`, `powershell`, `sysmon`,
`linux`, and `lab`. A source not appearing in the result is a gap to investigate,
not proof that no activity occurred.

In the authorized lab, a starting check for expected event codes is:

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux) earliest=-24h
| eval event_code=coalesce(EventCode,EventID,"not_extracted")
| stats count latest(_time) as last_event by index host sourcetype event_code
| convert ctime(last_event)
```

Confirm audit policy, Sysmon filtering, forwarder delivery, actual field names,
clock synchronization, retention, and ingest delay. `ctime` uses the Splunk
user's display time zone; record the corresponding UTC time separately. Ask an
authorized administrator for `_audit` or `_internal` checks when necessary; do
not widen `lab_hunter` permissions.

Use [rare parent/child](../../hunts/mitre-attack/10-rare-parent-child.spl) as
an exploratory seven-day frequency view. Compare the selected period with a
representative, healthy historical baseline, approved changes, software
versions, and host roles. A one-host learning lab is not a representative
enterprise baseline; rare or new does not mean malicious. Note initial
backfill, short retention, and changes in collection before drawing conclusions.

## 3. Run focused hunts and pivot

| Hypothesis | Start here | Pivot and alternative explanation |
| --- | --- | --- |
| Unusual PowerShell execution and a connection | [Process/network](../../hunts/mitre-attack/01-process-network.spl); existing [encoded PowerShell](../../hunts/01-encoded-powershell.spl) and [script-block](../../hunts/06-powershell-scriptblock.spl) searches | Join Sysmon 1 and 3 by host and ProcessGuid; inspect parent, command, account, destination, process start time, and script-block context. Administrators and software use PowerShell and curl legitimately. |
| A local account gains group membership | [Account-to-group](../../hunts/mitre-attack/03-account-to-group.spl) | Join Security 4720 account `TargetSid` to 4732 `MemberSid` on the same host; verify the group SID, actor, change ticket, and order. Membership in an ordinary group is not administrator access. |
| An account is targeted by repeated authentication failures | [Failures before success](../../hunts/mitre-attack/02-failures-before-success.spl) and [multiple-account failures](../../hunts/mitre-attack/07-multiple-account-failures.spl) | Compare source, domain, account, host, event order, logon type, shared NAT, and approved activity. Lockouts, mistyped credentials, services, and scanners can be benign. |
| A task or Run key supports persistence | [Task changes](../../hunts/mitre-attack/04-scheduled-task-changes.spl) and [lab Run key](../../hunts/mitre-attack/05-lab-run-key.spl) | Review the owner, task action or registry value, signer, parent process, execution records, and change history. The supplied registry rule covers only one lab pattern. |
| A log may have been cleared | [Windows log-clear candidates](../../hunts/mitre-attack/06-event-log-clear-candidates.spl) | Validate Security 1102 or the `Microsoft-Windows-Eventlog` provider for System 104, actor, authorized maintenance, and independent retained events. Do not clear live logs merely to test. |
| A process, destination, or SSH session needs context | [DNS](../../hunts/mitre-attack/08-powershell-dns-context.spl), [SSH](../../hunts/mitre-attack/09-linux-ssh-context.spl), and [timeline](../../hunts/mitre-attack/11-investigation-timeline.spl) | A domain, connection, or successful login is not by itself C2 or lateral movement. Correlate separate endpoint and network records, and record gaps. |

Use the [search index](../../hunts/mitre-attack/README.md) for precise
thresholds and limitations. The timeline orders events by `_time`, but does not
prove causality. Compare `_indextime` with event time, validate source clocks
and time zones, and account for delayed or missing logs. A process ID can be
reused; prefer ProcessGuid or a device, process ID, and process-creation-time
combination. Do not join unrelated accounts simply because their display names
match.

For a separately authorized Defender XDR tenant, the optional
[KQL example](../../hunts/mitre-attack/optional-defender-powershell-network.kql)
shows the same process/network question in another platform. Its tables are not
included in this lab. Do not infer cloud, EDR, or multi-endpoint coverage from
the presence of that file.

## 4. Validate the query, not just its appearance

1. Inspect at least one actual event for each required field using approved
   private access. Adapt names only after checking the installed add-ons.
2. Compare an expected positive case with a benign control and a negative case.
   The existing [lab activity generator](../../scripts/windows/05-Generate-HuntActivity.ps1)
   creates a disposable account, group change, encoded PowerShell, task, and curl
   request **only on WINHUNT01**. Review it and the
   [cleanup script](../../scripts/windows/06-Cleanup-TestObjects.ps1) first.
   Obtain approval, preserve existing objects, and clean up afterward. Actual
   event delivery is still a separate test.
3. One deliberately failed login in that script does **not** meet the five-event
   failure threshold, and the script does not create five distinct test accounts.
   Do not report those threshold hunts as passed from that single event. Use
   synthetic in-memory fixtures below instead of conducting a password attack.
4. Verify expected counts, field extraction, event order, false positives,
   processing limits, and source coverage. An empty result can mean a missing
   field, missing input, disabled audit policy, or incorrect time range.
5. Before promoting a hunt to an alert, obtain approval; tune against relevant
   data, document ownership and suppression, test positive and negative cases,
   and route results to a human. No query here quarantines or blocks anything.

### In-memory threshold fixture: failures before success

Paste this into Splunk Search on an authorized lab instance. It uses
`makeresults`; it does not create accounts, send logins, or index records.

```spl
| makeresults count=6
| streamstats count as seq
| eval _time=now()-600+seq*60, host="fixture", account_domain="example", account="fixture-user", source_ip="192.0.2.10", event_code=if(seq<=5,4625,4624)
| eval failed=if(event_code=4625,1,0)
| sort 0 _time
| streamstats time_window=15m global=false sum(failed) as preceding_failures by host account_domain account source_ip
| where event_code=4624 AND preceding_failures>=5
| table event_code preceding_failures
```

Expected: exactly one row with `event_code=4624` and `preceding_failures=5`.
For a negative control, replace `seq<=5` with `seq<=4`: expect zero rows.
This tests the aggregation logic only, not Windows collection or the entire
production search. Equal timestamps and Splunk streaming limits need separate
review.

### In-memory identity-join fixture

Start with this fixture, then append every pipeline line **after the first line**
from [03-account-to-group.spl](../../hunts/mitre-attack/03-account-to-group.spl):

```spl
| makeresults count=3
| streamstats count as seq
| eval _time=now()-7200+case(seq=1,0,seq=2,1,true(),7140), host="fixture", EventCode=if(seq=1,4720,4732), TargetSid=if(seq=1,"S-1-5-21-1-2-3-1001",null()), MemberSid=if(seq>1,"S-1-5-21-1-2-3-1001",null()), TargetUserName=case(seq=1,"fixture-user",seq=2,"fixture-group",true(),"outside-window-group"), SubjectUserName="fixture-actor"
```

Expected: exactly one result, `target_group=fixture-group`, with a one-second
interval. `outside-window-group` must not appear. For negative controls, change
the fixture `MemberSid` ending from `1001` to `1002`, or change `seq=2,1` to
`seq=2,3601`: each change should produce zero results when applied separately.
This tests the correlation logic, not live Windows collection or authorization.

### Multi-account threshold fixture

```spl
| makeresults count=5
| streamstats count as seq
| eval _time=relative_time(now(),"@h")+60, host="fixture", source_ip="192.0.2.10", target_account="example:user".seq
| bin _time span=15m
| stats count as failures dc(target_account) as distinct_accounts dc(host) as distinct_hosts values(host) as hosts by source_ip _time
| where distinct_accounts>=5
```

Expected: one row with five failures and five distinct accounts. Change
`count=5` to `count=4`: expect zero rows. The fixed bucket can split activity
at a boundary; this fixture does not establish that the same password was used.

## 5. Document, escalate, and improve

1. Use the [hunt report](../reference/hunt-report-template.md) to record the hypothesis,
   ATT&CK version and rationale, scope, query revision, source health, UTC
   timeline, observations, alternatives, gaps, and confidence.
2. Preserve original evidence in approved private storage. Follow the
   organization's DFIR procedures for collection, integrity hashes, chain of
   custody, access restrictions, and legal requirements. Do not rewrite
   original events to make a timeline fit.
3. Escalate promptly to the designated incident response team when independent
   evidence supports active or historical compromise. Include the case context,
   business impact, evidence references, uncertainty, and requested next action.
   A search hit or an ATT&CK label alone is not an incident verdict.
4. After investigation, convert useful findings into reviewed detections or
   new hypotheses. Record alert ownership, false positives, visibility gaps,
   validation date, and retest triggers. Keep raw logs and real identifiers out
   of the public repository.
