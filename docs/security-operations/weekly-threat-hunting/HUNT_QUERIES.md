# Weekly APT Hunt Queries and Validation

These are read-only candidate searches for the [weekly guide](README.md) and [response playbook](../APT_INCIDENT_RESPONSE_PLAYBOOK.md). They do not deploy detections or establish that any lab system is compromised. No search in this document has been executed against the live lab as part of publication.

## Scope and telemetry checks

Use only the six existing indexes: `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, `lab`. The core systems are RHEL-SPLUNK01, WINHUNT01 and RHEL-IDM01. Confirm the actual indexed host aliases before adding host filters; the packaged Linux input uses `host = splunk01`.

| Source | What must be verified before using a result |
| --- | --- |
| Windows Security | Forwarded records, event ID extraction, audit settings and retention; task events 4698/4702 require the relevant audit policy |
| Sysmon | Event 1 process creation and extracted Image, CommandLine, ParentImage, ProcessGuid and User; forwarding configuration alone does not verify source generation |
| PowerShell | Script-block/module logging policy, generated events and extraction; forwarding the Operational channel alone does not enable full script logging |
| Linux | The baseline input reads `/var/log/siem-lab/linux.log`; full auditd EXECVE/SYSCALL, journal, application and authentication coverage must be designed and verified separately |
| Windows network/file/registry | The shipped Sysmon configuration selectively collects network events for PowerShell/curl, file creation in the lab test folder, a specific Run key and PowerShell DNS; it is not complete endpoint coverage |
| Appliance, DNS/proxy, EDR and cloud | Optional external sources. Confirm entitlement, collection, schema, routing, access and retention before using them. Cloud service-principal activity is not present merely because the lab has IdM |

Set the Splunk user display timezone deliberately. Record UTC bounds and original event timezone, then save the job ID, query version, warnings and coverage privately. The searches use a bounded seven-day window; use explicit older incident bounds when a campaign or plausible dwell time predates it. Work in smaller intervals if volume is high and retain search warnings.

### Q0 Check available data

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h latest=now
| stats count min(_time) as first_event max(_time) as last_event max(_indextime) as last_ingested by index sourcetype host
| eval first_event_display=strftime(first_event,"%Y-%m-%dT%H:%M:%S%z"), last_event_display=strftime(last_event,"%Y-%m-%dT%H:%M:%S%z")
| sort index host sourcetype
```

**Expected:** inventory of observed streams and event/ingestion ranges. The displayed offset is the search user's timezone; use UTC in preferences if labeling exports UTC. An absent stream may be missing collection, permission, retention or activity. Compare to the approved asset/source inventory; Q0 cannot prove completeness.

Before Windows searches, inspect a small authorized sample with `| table _time host source sourcetype EventCode EventID Image CommandLine ParentImage ProcessGuid User`. If fields are null, inspect the raw XML privately and correct the extraction with the detection engineer. Do not treat null fields as a negative hunt.

## Q1 Linux remote-access tool name candidates

**Hypothesis:** unapproved remote-access tooling appears in the available Linux telemetry. Name matching is a narrow lead; renamed tools and missing process logging evade it.

```spl
index=linux earliest=-7d latest=now
| regex _raw="(?i)(gs-netcat|gsnetcat|gsocket)"
| table _time host source sourcetype _raw
| sort 0 _time
```

Inspect whether a hit represents execution, a package record, an approved administrator or text mentioning a tool. Verify executable path/hash, process lineage, effective identity, startup entries and outbound activity using independent approved evidence. A legitimate dual-use tool name does not identify an APT.

**Synthetic filter controls, without endpoint execution or ingestion:**

```spl
| makeresults count=4
| streamstats count as sample_id
| eval sample=case(sample_id=1,"SYNTHETIC process=gs-netcat",sample_id=2,"SYNTHETIC process=gsocket",sample_id=3,"SYNTHETIC process=backup-agent",sample_id=4,"SYNTHETIC process=systemd-journald")
| eval expected=if(sample_id<=2,1,0), observed=if(match(sample,"(?i)(gs-netcat|gsnetcat|gsocket)"),1,0)
| eval result=if(expected=observed,"PASS","FAIL")
| table sample_id sample expected observed result
```

**Expected:** four PASS rows, matching cases 1 and 2. This tests the filter only. It does not generate audit events, validate transport or test an alert. A real process-execution validation needs a separately approved benign simulation and source-to-index evidence.

## Q2 Linux persistence and writable-path review

**Hypothesis:** unexpected service/cron/startup or writable-path activity deserves context review. This deliberately broad query requires event-level interpretation.

```spl
index=linux earliest=-7d latest=now
("/dev/shm/" OR "/etc/cron" OR "/var/spool/cron" OR "/etc/systemd/system/" OR "/etc/profile.d/" OR "authorized_keys")
| table _time host source sourcetype _raw
| sort 0 _time
```

**Triage:** distinguish an audit record of execution/write from a path mentioned in text. Compare to change records and known-good configuration; correlate to identity, parent process and outbound activity. Software installation, backup and administration can explain hits. These paths are analyst-selected review surfaces, not campaign-specific indicators.

**Controls:** in a private synthetic dataset, a clearly labeled event mentioning `/etc/systemd/system/synthetic-review.service` should match; an equally labeled ordinary authentication event without any listed term should not. Confirm both were ingested before judging the filter. Do not create a real persistence mechanism to test this text query.

## Q3 Windows scheduled-task command candidates

**Hypothesis:** a process created or changed a scheduled task. This also finds routine maintenance and software deployment; it does not establish persistence or attribution.

```spl
index=sysmon earliest=-7d latest=now (EventCode=1 OR EventID=1)
| eval image=lower(coalesce(Image,process_path,"")), cmd=coalesce(CommandLine,process_command_line,"")
| where like(image,"%schtasks.exe") AND (match(lower(cmd),"/create") OR match(lower(cmd),"/change"))
| table _time host User ProcessGuid ParentImage image cmd
| sort 0 _time
```

**Triage:** inspect complete task action, author/principal, run level, trigger, referenced files, signer and creator lineage. Correlate with Q4 and the underlying task definition. A command invocation may fail and is not proof a task was registered. PowerShell/COM/RPC-created tasks can bypass this narrow process search.

**Safe synthetic controls:**

```spl
| makeresults count=2
| streamstats count as sample_id
| eval image="c:/windows/system32/schtasks.exe", cmd=if(sample_id=1,"SYNTHETIC /create inert-placeholder","SYNTHETIC /query"), expected=if(sample_id=1,1,0)
| eval observed=if(like(image,"%schtasks.exe") AND (match(lower(cmd),"/create") OR match(lower(cmd),"/change")),1,0)
| eval result=if(expected=observed,"PASS","FAIL")
| table sample_id cmd expected observed result
```

**Expected:** two PASS rows. These strings are never executed; this validates predicate behavior only.

## Q4 Windows task registration and modification

```spl
index=win_security earliest=-7d latest=now (EventCode=4698 OR EventID=4698 OR EventCode=4702 OR EventID=4702)
| eval event_id=tonumber(coalesce(EventCode,EventID)), task_name=coalesce(TaskName,Task_Name), actor=coalesce(SubjectUserName,Subject_User_Name)
| table _time host event_id actor task_name TaskContent
| sort 0 _time
```

**Expected:** audited task registrations/updates within the visible scope. Check source XML if TaskContent is not extracted; task actions may be XML-escaped. Correlate with the actual task, file and execution records. Absence of these events with audit policy disabled is a visibility gap.

**Controls:** in private synthetic fixtures use EventCode 4698 (included) and 4699 (excluded), with equivalent collection and known timestamps. Neither record proves a live task existed. See the existing [scheduled-task hunt](../../../hunts/mitre-attack/04-scheduled-task-changes.spl).

## Q5 Windows installer and script context

```spl
index=sysmon earliest=-7d latest=now (EventCode=1 OR EventID=1)
| eval image=lower(coalesce(Image,process_path,"")), parent=lower(coalesce(ParentImage,parent_process_path,"")), cmd=coalesce(CommandLine,process_command_line,"")
| where like(image,"%ftp.exe") OR like(image,"%msiexec.exe") OR like(image,"%control.exe") OR like(image,"%rundll32.exe") OR like(image,"%powershell.exe") OR like(image,"%pwsh.exe")
| table _time host User ProcessGuid ParentProcessGuid parent image cmd Hashes
| sort 0 _time
```

This is an inventory query with substantial benign volume. Prioritize unexpected user-writable/removable paths, unapproved installers, remote actions and unusual parent-child sequences; review signing, change records and source artifacts. Do not suppress every signed executable: legitimate tools can be abused. Apply equivalent review to developer/recruitment and software-delivery leads.

**Controls:** a synthetic EventCode 1 record with Image `c:/windows/system32/msiexec.exe` should appear; a synthetic EventCode 1 record with Image `c:/windows/system32/notepad.exe` should not. Test event ID and field extraction separately. Complete sample content remains private and explicitly synthetic.

## Q6 Correlate a scoped host timeline

After identifying the actual indexed hostname, replace `REPLACE_WITH_INDEXED_LAB_HOST` locally. Do not publish a real endpoint identifier. Narrow the interval to the case first, then deliberately expand if needed.

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h latest=now host="REPLACE_WITH_INDEXED_LAB_HOST"
| eval event_id=coalesce(EventCode,EventID), actor=coalesce(User,SubjectUserName,TargetUserName,user)
| table _time _indextime index sourcetype source host event_id actor ProcessGuid ParentProcessGuid Image CommandLine TaskName
| sort 0 _time
```

Correlate using stable identifiers and corroborating evidence. The host-only timeline supplies context; it does not show causation. Preserve raw records privately rather than relying only on the displayed fields. For a synthetic scope control, two same-time records with distinct synthetic host values should return only the selected host.

## Optional cloud and network investigations

The lab has no verified cloud service-principal, Microsoft Graph, appliance or full DNS/proxy feed. Do not add an invented index or interpret absent cloud data as a clean tenant. The authorized cloud administrator should use the current vendor investigation workflow, preserving application IDs, local service-principal object IDs, credential/role changes, successful and failed sign-ins and resource access in every affected tenant. The current edition links the relevant primary reporting and remediation guidance.

For network evidence, verify the sensor/capture point, both directions, timestamps, loss and visibility into encrypted sessions. A shared relay or CDN can serve legitimate users; do not treat a domain match as proof of attacker ownership or apply a broad block without checking impact.

## Authorized read-only host review

**Command overview:** the commands below inspect time, network connections and scheduling. Run them only under the approved forensic collection plan on the appropriate owned lab host; preserve outputs privately. Live commands alter system state and output from a compromised host may be untrustworthy. They are examples to review, not actions performed by publishing this file.

RHEL examples:

```bash
date -u
timedatectl status
ss -plant
systemctl list-timers --all
systemctl list-unit-files --type=service
```

Windows PowerShell examples:

```powershell
[DateTime]::UtcNow.ToString('o')
Get-NetTCPConnection
Get-ScheduledTask | Select-Object TaskPath, TaskName, State
```

**Expected:** inspectable time configuration, current visible connections and scheduling inventory. Access restrictions may hide details. The absence of an entry in a summary listing does not establish that all persistence is absent; acquire actual definitions and forensic artifacts as authorized.

**Command summary:** use these observations to choose evidence pivots, then compare task/service definitions, files, identities and network records against the approved baseline. They do not eradicate a compromise or verify a detection.

## Record results and escalation

For each search retain hypothesis, version, UTC window, source/field coverage, control outcomes, candidate evidence, benign alternatives, conclusion/confidence and next owner. Use **supported**, **not supported within observed scope**, **inconclusive**, **benign/authorized**, or **escalated**. Keep search execution, endpoint simulation, transport, alert delivery and analyst conclusions distinct.

Escalate credible privileged compromise, active exfiltration, destructive behavior, uncontrolled spread, missing critical telemetry during an incident or suspected novel exploitation using the [severity matrix](../APT_INCIDENT_RESPONSE_PLAYBOOK.md#severity-and-when-to-escalate). Never use a weekly publication schedule as an incident response timer.
