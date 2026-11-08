# Splunk — Cobalt Strike–Associated Pipe Hunt and Atomic Red Team Validation

Add this optional exercise after [Step 27: verify event collection](../steps/27-verify-event-collection.md) and [Step 29: hunting searches](../steps/29-create-the-hunting-search-files.md). It uses the existing `sysmon` index and owned **WINHUNT01** endpoint.

**Objective:** hunt for a small set of default-style named-pipe patterns associated with Cobalt Strike and review their process context against an authorized penetration-test scope. Validate the search with a harmless upstream Atomic Red Team test that creates a local named pipe. No PenTest team events or indicators were supplied; actual team attribution must be confirmed with the exercise owner.

**Status:** source content and planned lab validation. These instructions have not been executed on WINHUNT01 or in the user's Splunk instance. A pipe-name match is a candidate for review, not proof of Cobalt Strike, compromise or authorization.

## What is included

| Component | Location |
| --- | --- |
| Four paste-ready SPL searches | [Hunt files](../../hunts/cobalt-strike/README.md) |
| Sysmon collection fragment | [PipeEvent XML example](../../configs/sysmon/pipe-events.xml.example) |
| Validation record | [Sanitized template](../../evidence/sanitized/cobalt-strike-atomic-validation.md) |

This exercise tests **named-pipe creation**, mapped to ATT&CK **T1559, Inter-Process Communication**, following Atomic Red Team's technique organization. It does not emulate Beacon communications, remote access, injection, persistence or lateral movement. Keep endpoint protection enabled; this test needs no security exclusions or payload downloads.

## Step 1 — Record the exercise boundary

Use only the owned isolated lab. Record WINHUNT01, the approved operator, the run identifier, the UTC test window and the expected two pipe names. Preserve a VMware snapshot and a usable copy of the currently applied Sysmon XML before modifying telemetry. Do not point an emulator at another host or run an entire technique collection.

For a real PenTest review, obtain the authorized hosts, operator contact, dates/times and expected indicators through the exercise owner. A name that resembles Cobalt Strike is not enough to call an event either malicious or authorized.

## Step 2 — Open the correct shell and create a private workspace

On **WINHUNT01**, use a new 64-bit Windows PowerShell window. Administrator rights are required for the later Sysmon configuration change; the selected Atomic named-pipe test itself does not require elevation.

```powershell
$PSVersionTable.PSVersion
[Environment]::Is64BitProcess
$env:COMPUTERNAME
Get-Service -Name Sysmon64,Sysmon -ErrorAction SilentlyContinue
```

**Command overview:** Check the shell version, process architecture, computer and existing Sysmon service. Expect the intended Windows host, a 64-bit shell and an installed running Sysmon service. Use [Step 27](../steps/27-verify-event-collection.md) to resolve missing Sysmon or forwarding first. These are PowerShell commands, not Command Prompt commands.

Create a new private run directory outside the Git checkout:

```powershell
$PrivateRoot = Join-Path 'C:\SIEMLab' ('AtomicValidation-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
if (Test-Path -LiteralPath $PrivateRoot) { throw 'Run directory already exists; choose a new one.' }
New-Item -ItemType Directory -Path $PrivateRoot -ErrorAction Stop | Out-Null
$AtomicRoot = Join-Path $PrivateRoot 'atomics'
New-Item -ItemType Directory -Path $AtomicRoot -ErrorAction Stop | Out-Null
New-Item -ItemType Directory -Path (Join-Path $AtomicRoot 'T1559') -ErrorAction Stop | Out-Null
```

**Summary:** Keep this PowerShell window open so later steps can reuse its variables. The directory will hold downloaded YAML, private configuration backups and execution records. Do not commit it or its results to GitHub.

## Step 3 — Install the execution framework from an approved source

Use the official PowerShell Gallery packages named by [Atomic's installation documentation](https://www.atomicredteam.io/docs/invoke-atomicredteam/getting-started). Inspect the selected versions and publisher information before installing. If your environment restricts module installation or script execution, use its approved distribution/signing process rather than bypassing policy.

```powershell
$ModuleChoices = foreach ($ModuleName in 'Invoke-AtomicRedTeam','powershell-yaml') {
    Find-Module -Name $ModuleName -Repository PSGallery -ErrorAction Stop
}
$ModuleChoices | Select-Object Name,Version,Author,Repository
```

After reviewing the returned versions and their approved source, install those exact selections:

```powershell
foreach ($Choice in $ModuleChoices) {
    Install-Module -Name $Choice.Name -RequiredVersion $Choice.Version -Repository PSGallery -Scope CurrentUser -ErrorAction Stop
}
Import-Module powershell-yaml -ErrorAction Stop
Import-Module Invoke-AtomicRedTeam -ErrorAction Stop
Get-Module Invoke-AtomicRedTeam,powershell-yaml | Select-Object Name,Version,Path
Get-Command Invoke-AtomicTest -Syntax
```

**Command overview:** `Find-Module` retrieves package metadata; `RequiredVersion` installs the reviewed selection; `CurrentUser` scopes the installation; `Import-Module` loads the framework. Record the actual module versions and review any repository/NuGet prompts. No `Invoke-Expression` bootstrap or automatic download of the full Atomic payload collection is needed.

## Step 4 — Download the pinned technique YAML only

This guide was reviewed on **November 7, 2026 (Hawaii)**. It selects upstream **Create Named Pipe**, GUID `17521690-2183-460f-a182-5dfd6f9f0a7f`, from the pinned source below. Other tests in the same technique can perform different operations; select only this GUID.

```powershell
$AtomicCommit = 'a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6'
$AtomicYaml = Join-Path $AtomicRoot 'T1559\T1559.yaml'
$AtomicUrl = "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/$AtomicCommit/atomics/T1559/T1559.yaml"
Invoke-WebRequest -UseBasicParsing -Uri $AtomicUrl -OutFile $AtomicYaml -ErrorAction Stop
$ExpectedHash = '56535667b9ddc6c2e6f359a098ce747b1d86ef4627b5f5172305d9ee2a7b667b'
if ((Get-FileHash -LiteralPath $AtomicYaml -Algorithm SHA256).Hash -ne $ExpectedHash) {
    throw 'Atomic YAML hash mismatch; do not run it.'
}
```

**Command overview:** Download only one text definition, pinned by commit, and compare its SHA-256. The recorded digest checks consistency with the reviewed source; it is not an independent identity guarantee if the source channel itself is compromised. Review the [pinned file](https://github.com/redcanaryco/atomic-red-team/blob/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/atomics/T1559/T1559.yaml). Do not switch the URL to a moving branch without a new review and hash.

## Step 5 — Review the exact test and resolved command

```powershell
$TestGuid = '17521690-2183-460f-a182-5dfd6f9f0a7f'
$Definition = ConvertFrom-Yaml -Yaml (Get-Content -LiteralPath $AtomicYaml -Raw -Encoding UTF8)
$SelectedTest = @($Definition.atomic_tests | Where-Object { $_.auto_generated_guid -eq $TestGuid })
if ($SelectedTest.Count -ne 1 -or $SelectedTest[0].name -ne 'Create Named Pipe') {
    throw 'Expected named-pipe test was not uniquely found.'
}
$SelectedTest[0].executor.command
```

**Expected:** a command creating `System.IO.Pipes.NamedPipeServerStream`, sleeping for 30 seconds, and disposing the pipe. It has a `pipe_name` argument, runs in PowerShell, needs no elevation and has no payload dependency. Stop if the selected definition differs from that reviewed scope.

Prepare the exact test parameters and inspect them:

```powershell
$AtomicParams = @{
    PathToAtomicsFolder = $AtomicRoot
    TestGuids = @($TestGuid)
    ExecutionLogPath = (Join-Path $PrivateRoot 'atomic-execution.csv')
}
Invoke-AtomicTest T1559 @AtomicParams -InputArgs @{ pipe_name = 'postex_a1b2c3d4' } -ShowDetails
Invoke-AtomicTest T1559 @AtomicParams -InputArgs @{ pipe_name = 'postex_a1b2c3d4' } -CheckPrereqs
```

**Summary:** `ShowDetails` is review, `CheckPrereqs` is a prerequisite check, and neither is proof of test execution or event collection. Do not use `All`, omit the GUID selector, or invoke `GetPrereqs` for the whole technique. The selected test creates a pipe server only: **Event 17 is expected; Event 18 is not required**, because no client connects.

## Step 6 — Preserve the current Sysmon configuration

Locate the actual Sysmon binary and the XML source that was last applied. The following paths are examples from this lab; verify them and the file's authenticity before using them:

```powershell
$SysmonExe = 'C:\SIEMLab\Source\sysmon\Sysmon64.exe'
$CurrentConfig = 'C:\SIEMLab\Source\sysmon\sysmon.xml'
if (-not (Test-Path -LiteralPath $SysmonExe)) { throw 'Set the verified Sysmon executable path.' }
if (-not (Test-Path -LiteralPath $CurrentConfig)) { throw 'Locate the currently applied Sysmon XML before continuing.' }
Get-AuthenticodeSignature -FilePath $SysmonExe | Select-Object Status,SignerCertificate
$BackupConfig = Join-Path $PrivateRoot 'sysmon-before.xml'
$CandidateConfig = Join-Path $PrivateRoot 'sysmon-pipe-validation.xml'
Copy-Item -LiteralPath $CurrentConfig -Destination $BackupConfig -ErrorAction Stop
Copy-Item -LiteralPath $CurrentConfig -Destination $CandidateConfig -ErrorAction Stop
```

**Expected:** a valid Microsoft signature and the correct current XML copied to both new files. If the source file is stale or unknown, stop and obtain the actual applied configuration. A console display of settings is not necessarily a restorable copy of the full configuration.

## Step 7 — Merge the optional PipeEvent fragment

The repository's baseline `sysmon/sysmon.xml` does not define `PipeEvent` collection. Review the [fragment](../../configs/sysmon/pipe-events.xml.example), then merge its `RuleGroup` under the candidate file's existing `<EventFiltering>` element. Retain the existing schema and all other rules. Do not replace the whole configuration with this fragment or overwrite the baseline file.

```powershell
notepad.exe $CandidateConfig
```

The fragment includes the selected `postex_`, `msagent_` and `MSSE-` prefixes plus the `SIEMLabControl_` prefix. The last one is necessary: the negative control must be **collected** even though the hunt should not match it. Existing exclusions take precedence; review any existing pipe exclusions, duplicate groups and organization policy before applying. This narrow fragment does not collect all named pipes.

## Step 8 — Apply the reviewed configuration

Run in Administrator PowerShell only after reviewing the merged file and preserving the rollback copy:

```powershell
[xml]$CandidateXml = Get-Content -LiteralPath $CandidateConfig -Raw
& $SysmonExe -s
& $SysmonExe -c $CandidateConfig
if ($LASTEXITCODE -ne 0) { throw 'Sysmon rejected the configuration; review the error before testing.' }
Get-Service -Name Sysmon64,Sysmon -ErrorAction SilentlyContinue
```

**Command overview:** The XML cast checks well-formedness, `-s` shows Sysmon's supported schema, and `-c` applies the candidate. XML parsing alone does not validate the Sysmon schema. Check the update result, running service and local configuration-change Event 16 before running controls. Preserve the prior approved configuration for rollback.

## Step 9 — Check the searchable telemetry

In **Splunk Web → Search & Reporting**, run [00-pipe-telemetry-health.spl](../../hunts/cobalt-strike/00-pipe-telemetry-health.spl). Confirm the current host and the availability of extracted `EventCode`/`EventID`, `PipeName`/`pipe_name`, `Image` and `ProcessGuid` fields. A zero pipe count before the controls is possible; a positive total Sysmon count alone does not establish pipe-event coverage.

The existing forwarder input already reads the Sysmon Operational channel into `sysmon`. No new Splunk index is required. If the local events are absent in Splunk, use [Step 27](../steps/27-verify-event-collection.md) and the [forwarder troubleshooting guide](../troubleshooting/splunk-forwarder-tls-and-kv-service.md). Keep the actual logs private.

## Step 10 — Test the pattern in Splunk without endpoint activity

Run [03-synthetic-pattern-self-test.spl](../../hunts/cobalt-strike/03-synthetic-pattern-self-test.spl). It creates twelve search-time rows covering expected names, path prefixes, case differences and near-misses.

**Expected:** all twelve rows show `PASS`. No test data is indexed. This checks expression behavior in the local Splunk engine; it does not validate Sysmon or forwarding. Stop and resolve any failing case before interpreting endpoint results. Python unit tests in this repository check the same pattern boundaries separately, not the Splunk engine.

## Step 11 — Execute the negative control

Back in the same WINHUNT01 PowerShell window:

```powershell
$ValidationStart = Get-Date
$ValidationStart.ToUniversalTime().ToString('o')
Invoke-AtomicTest T1559 @AtomicParams -InputArgs @{ pipe_name = 'SIEMLabControl_20261107' }
```

**Command overview:** The GUID selects only the reviewed upstream test. The input overrides the pipe name. Wait for the approximately 30-second test to finish. **Expected:** local Sysmon Event 17 for `\SIEMLabControl_20261107`, then an indexed copy; the candidate hunt must not return it. No Event 18 is required. Test execution without an observable event is not a successful negative control.

## Step 12 — Execute the positive control

```powershell
Invoke-AtomicTest T1559 @AtomicParams -InputArgs @{ pipe_name = 'postex_a1b2c3d4' }
$ValidationEnd = Get-Date
$ValidationEnd.ToUniversalTime().ToString('o')
```

**Expected:** local Sysmon Event 17 for `\postex_a1b2c3d4`, an indexed copy and a candidate-search match. The expected process is the PowerShell test executor, not a Cobalt Strike Beacon. The selected test disposes its pipe after roughly 30 seconds. Treat an error, timeout or blocked script as an incomplete test and inspect the cause without disabling protection.

## Step 13 — Confirm both source events locally and in Splunk

Read the private local test window:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-Sysmon/Operational'
    Id = 17,18
    StartTime = $ValidationStart
    EndTime = $ValidationEnd
} -ErrorAction Stop | Select-Object TimeCreated,Id,Message
```

**Expected:** verify the two exact pipe names, host, process path and ProcessGuid in the returned event details. Other events may exist in the same window; compare the actual names. These messages contain endpoint details and belong in private evidence storage.

In Splunk Web, use the same UTC window and verify that both names were indexed. For example, select the appropriate range and run:

```spl
index=sysmon host=WINHUNT01 (EventCode=17 OR EventID=17)
| eval pipe_name=coalesce(PipeName,pipe_name)
| eval pipe_leaf=lower(mvindex(split(pipe_name,urldecode("%5C")),-1))
| where pipe_leaf="postex_a1b2c3d4" OR pipe_leaf="siemlabcontrol_20261107"
| table _time host EventCode EventID pipe_name Image ProcessGuid
```

**Query overview:** Selects pipe-created events and the two normalized exercise names, displaying source context. This search uses the time picker because it has no inline modifiers. Verify the original field values and UTC window as well as the normalized name.

## Step 14 — Run the Cobalt Strike–associated candidate hunt

Paste [01-default-pipe-candidates.spl](../../hunts/cobalt-strike/01-default-pipe-candidates.spl), or this identical query:

```spl
index=sysmon host=WINHUNT01 earliest=-24h latest=now (EventCode=17 OR EventCode=18 OR EventID=17 OR EventID=18)
| eval event_code=tonumber(coalesce(EventCode,EventID)), pipe_name=coalesce(PipeName,pipe_name), process_guid=coalesce(ProcessGuid,ProcessGUID,process_guid), process_path=coalesce(Image,process_path), account=coalesce(User,user)
| eval pipe_leaf=lower(mvindex(split(pipe_name,urldecode("%5C")),-1))
| where match(pipe_leaf,"^(msagent_[0-9a-f]+|postex_[0-9a-f]+|postex_ssh_[0-9a-f]+|msse-[0-9]+-server)$")
| eval assessment="Named-pipe candidate; verify process context and authorized test scope"
| sort 0 _time
| table _time host event_code pipe_name pipe_leaf process_path process_guid account assessment
```

| Query part | Explanation |
| --- | --- |
| `index=sysmon host=WINHUNT01` | Limits the example to the existing endpoint/index. Adapt only to approved scope. |
| `earliest=-24h latest=now` | Searches the last day; these inline bounds override the corresponding time-picker bounds. |
| Event IDs 17 and 18 | Selects pipe creation and connection records. |
| `coalesce` | Uses whichever of the documented field aliases is available. It does not create missing telemetry. |
| `split`, `mvindex`, `lower` | Extracts and normalizes the final pipe-name component. `%5C` represents a backslash. |
| `match` with `^...$` | Checks the complete name against this limited pattern set. |
| `table` | Presents the event and process details for review. |

**Expected control result:** positive name returned; negative name absent **after confirming both were collected**. Repeated runs may create extra hits. Adjust the inline window for older tests, and verify field extraction if expected values are blank. These limited default-style patterns miss custom names; a hit is not product attribution.

## Step 15 — Pivot to process context

Run [02-process-context.spl](../../hunts/cobalt-strike/02-process-context.spl). It selects matching pipes and correlates available process events using **host plus ProcessGuid**. Review the image, parent, command line and account, then compare the actual start and pipe times.

A missing process-creation record can mean the process started before the search window or was not collected. Missing GUIDs exclude rows from this correlation but not the base hunt. If one process used several pipes, its context can include other pipe names as well; only the base hunt classifies matching names. `eventstats` resource limits may also affect large searches; use a narrow approved scope and review job messages. Do not substitute a PID-only join, which can combine unrelated processes.

## Step 16 — Validate PenTest attribution and tune carefully

For a real exercise, compare hits with the team's approved host, UTC window, actual tool/profile indicators and process history. Ask the team to confirm the specific activity. Record one of: confirmed simulation, confirmed authorized PenTest activity, unexplained candidate, or insufficient evidence.

Do not create a broad exception for an entire operator, host or testing period. If a known benign application matches, document its observed context and test any narrower filter against both controls. Coordinate profile-specific coverage with the exercise owner; this small default-name set is not full Cobalt Strike detection. The locally selected Atomic test validates only creation of a matching name, not actual C2 behavior.

## Step 17 — Save the hunt and retain evidence

Save the reviewed query as a search/report if useful, with an owner, question, telemetry requirements and false-positive notes. Start with manual execution. Alerting or a scheduled search requires an approved schedule, ingestion-delay allowance, deduplication strategy and an observed delivery test; this repository does not configure those automatically.

Complete the [validation record](../../evidence/sanitized/cobalt-strike-atomic-validation.md). Record the pinned source, installed module versions, actual UTC window, local events, indexed events, positive/negative outcomes, process pivot and limitations. Keep raw XML, execution CSVs, host/user details and actual PenTest indicators in approved private storage.

## Step 18 — Clean up and restore telemetry if appropriate

The selected test disposes its named pipe when it returns; it defines no separate cleanup command. If execution was interrupted, inspect only the known test process and its state before stopping anything. Do not kill all PowerShell processes or remove unrelated pipes. Execution logs and downloaded YAML remain in the private run directory until disposed of under the lab's retention policy.

If the telemetry change was temporary, restore the reviewed pre-test XML in Administrator PowerShell:

```powershell
& $SysmonExe -c $BackupConfig
if ($LASTEXITCODE -ne 0) { throw 'Rollback failed; review the error and current service configuration.' }
Get-Service -Name Sysmon64,Sysmon -ErrorAction SilentlyContinue
```

**Expected:** successful update and running Sysmon; verify configuration-change events and normal event forwarding. Restore only if no later approved change would be overwritten. If the new collection is retained, record its owner, capacity review and change approval instead. Restoring telemetry does not delete previously recorded events.

## Troubleshooting

| Symptom | Next check |
| --- | --- |
| No local pipe event | Applied Sysmon rules, exclusions, service state, selected GUID, test exit and the local time window. |
| Local events exist, Splunk events do not | Forwarder Sysmon input, destination TLS/connection, receiving/indexing, role permissions and time range. |
| Pipe events exist but fields are blank | Inspect the actual event and add-on/extraction. The query requires an extracted name and event ID; it does not parse arbitrary raw XML automatically. |
| Positive control is indexed but not returned | Inspect exact PipeName, field aliases, host filter, inline time bounds and the synthetic self-test results. |
| Negative control not returned anywhere | Collection is not validated. A missing negative event is not proof of a correct exclusion by the hunt. |
| Event 18 absent | Expected for this server-only test. It does not open a client connection. |
| An unexpected hit appears | Preserve process/event context and validate with the owner. Do not assume it belongs to the test team. |

## References

- [Atomic T1559 at the pinned commit](https://github.com/redcanaryco/atomic-red-team/blob/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/atomics/T1559/T1559.yaml): Definition and GUID of the selected server-only test.
- [Invoke-AtomicRedTeam installation](https://www.atomicredteam.io/docs/invoke-atomicredteam/getting-started): Official execution-framework packages and setup.
- [Local Atomic execution](https://www.atomicredteam.io/docs/invoke-atomicredteam/execute-tests-locally): Selecting tests and providing a custom atomics path.
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon): Pipe-created/connected events and configuration commands.
- [Sysmon configuration files](https://learn.microsoft.com/en-us/windows/security/operating-system-security/sysmon/sysmon-configuration-files): Filter logic and exclusion precedence.
- [Splunk Windows Suspicious C2 Named Pipe](https://research.splunk.com/endpoint/90599d85-dc2a-4d4c-8c59-9485c3665828/): Current broader named-pipe analytic for comparison. This repository's lab query is independent and uses no ES macros.
- [Retired Cobalt Strike Named Pipes analytic](https://research.splunk.com/removed/5876d429-0240-4709-8b93-ea8330b411b5/): Historical context; Splunk replaced this standalone analytic with the broader detection.
- [Splunk evaluation functions](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/10.6/evaluation-functions/evaluation-functions): Function behavior used by the lab searches.
