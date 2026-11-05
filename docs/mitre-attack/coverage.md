# ATT&CK technique and telemetry mapping

**Reference:** MITRE ATT&CK Enterprise STIX **v20.1**, reviewed 2026-11-05.
The official [version history](https://attack.mitre.org/resources/updates/)
and [versioned STIX bundle](https://github.com/mitre-attack/attack-stix-data/blob/master/enterprise-attack/enterprise-attack-20.1.json)
are the authoritative sources. The reviewed bundle's SHA-256 is
`539a843a7b53ed9749740b2123dddae3726b1a4831841c32aca740b011b910b5`.
Tactic names follow that release, including **Stealth** and **Defense Impairment**.

**Interpretation**

- **Candidate**: repository source and a hunt are available or planned for a
  relevant observable. Field extraction, ingestion, and behavior have not been
  proven in a live system; a match may be benign.
- **Context only**: some related events can support a pivot, but they do not
  establish the technique or its adversarial purpose.
- **Gap**: the source, breadth, correlation, or suitable hunt needed to
  investigate the technique is not provided by the repository.

These labels describe the shipped source, not a live deployment or detection
effectiveness. An unlisted technique is **unassessed**, not covered. The
[Navigator layer](navigator-layer.json) uses the same labels and is not a score.

## Endpoint, identity, and network techniques

| Technique and tactic(s) | Hunt hypothesis and telemetry / query | Status |
| --- | --- | --- |
| [T1059.001 PowerShell](https://attack.mitre.org/techniques/T1059/001/) — Execution | Unusual PowerShell execution or script blocks; Sysmon 1 and PowerShell Operational, using [encoded PowerShell](../../hunts/01-encoded-powershell.spl), [script blocks](../../hunts/06-powershell-scriptblock.spl), and [process/network correlation](../../hunts/mitre-attack/01-process-network.spl). Encoded text alone is not malicious. | Candidate |
| [T1136.001 Local Account](https://attack.mitre.org/techniques/T1136/001/) — Persistence | Unexpected local account creation; Security 4720, with [account-to-group correlation](../../hunts/mitre-attack/03-account-to-group.spl). Confirm the account is local and creation was unauthorized. | Candidate |
| [T1098.007 Additional Local or Domain Groups](https://attack.mitre.org/techniques/T1098/007/) — Persistence, Privilege Escalation | A new or existing account is added to a security-enabled local group; Security 4732 and [account-to-group correlation](../../hunts/mitre-attack/03-account-to-group.spl). Confirm the group's SID, privilege, actor, and approval. | Candidate |
| [T1053.005 Scheduled Task](https://attack.mitre.org/techniques/T1053/005/) — Execution, Persistence, Privilege Escalation | A task is created or modified outside expected administration; Security 4698/4702 and [task changes](../../hunts/mitre-attack/04-scheduled-task-changes.spl). A registration is not proof of execution. | Candidate |
| [T1547.001 Registry Run Keys / Startup Folder](https://attack.mitre.org/techniques/T1547/001/) — Persistence, Privilege Escalation | A monitored Run key changes; Sysmon 12/13/14 and [lab Run key](../../hunts/mitre-attack/05-lab-run-key.spl). The shipped rule includes only the `SIEMLab` key, not all Run keys or Startup folders. | Candidate |
| [T1685.005 Clear Windows Event Logs](https://attack.mitre.org/techniques/T1685/005/) — Defense Impairment | Potential Security 1102 or System 104 log-clear records; [log-clear candidates](../../hunts/mitre-attack/06-event-log-clear-candidates.spl). Check the System event provider and independent collection before concluding. | Candidate |
| [T1110.001 Password Guessing](https://attack.mitre.org/techniques/T1110/001/) — Credential Access | Repeated 4625 failures before 4624 success for the same source, account, domain, and host; [failure/success hunt](../../hunts/mitre-attack/02-failures-before-success.spl). This pattern is not proof of password guessing or compromise. | Candidate |
| [T1110.003 Password Spraying](https://attack.mitre.org/techniques/T1110/003/) — Credential Access | One source fails against several accounts in a window; [multi-account failures](../../hunts/mitre-attack/07-multiple-account-failures.spl). Event logs do not reveal whether the same password was used. | Candidate |
| [T1078 Valid Accounts](https://attack.mitre.org/techniques/T1078/) — Initial Access, Persistence, Privilege Escalation, Stealth | Authentication context from [failure/success](../../hunts/mitre-attack/02-failures-before-success.spl) may support a pivot. A successful login does not establish stolen or adversarially used credentials. | Context only |
| [T1071.001 Web Protocols](https://attack.mitre.org/techniques/T1071/001/) — Command and Control | [Process/network](../../hunts/mitre-attack/01-process-network.spl) provides selected destination IPs and ports, not protocol content or C2 attribution. The optional NGINX access log is a local inbound test, not an outbound proxy. | Context only |
| [T1071.004 DNS](https://attack.mitre.org/techniques/T1071/004/) — Command and Control | [DNS context](../../hunts/mitre-attack/08-powershell-dns-context.spl) uses Sysmon 22, filtered to PowerShell. A query does not prove tunneling or C2. | Context only |
| [T1021.004 SSH](https://attack.mitre.org/techniques/T1021/004/) — Lateral Movement | [Local SSH context](../../hunts/mitre-attack/09-linux-ssh-context.spl) can show authentication on the Splunk VM. A login alone does not establish adversarial movement, and IdM logs are not forwarded. | Context only |

In ATT&CK v20, the older log-clear identifiers `T1070.001` and `T1070.002`
are revoked; use [T1685.005](https://attack.mitre.org/techniques/T1685/005/)
and [T1685.006](https://attack.mitre.org/techniques/T1685/006/) respectively.

## Prioritized gaps from the threat-hunter role

The examples below are hypotheses to scope later, not instructions to enable
additional collection or evidence that activity occurred.

| Technique and tactic(s) | Missing or insufficient visibility / next investigation requirement | Status |
| --- | --- | --- |
| [T1566.001 Spearphishing Attachment](https://attack.mitre.org/techniques/T1566/001/) — Initial Access | No mail, attachment, or identity-provider telemetry; obtain approved mail/security-gateway and endpoint delivery records. | Gap |
| [T1136.003 Cloud Account](https://attack.mitre.org/techniques/T1136/003/) — Persistence | No cloud identity audit stream; separately collect cloud account lifecycle and actor context. | Gap |
| [T1098.003 Additional Cloud Roles](https://attack.mitre.org/techniques/T1098/003/) — Persistence, Privilege Escalation | No cloud role-assignment audit data. Azure OIDC workflow output is not continuous cloud identity telemetry. | Gap |
| [T1003.001 LSASS Memory](https://attack.mitre.org/techniques/T1003/001/) — Credential Access | No configured EDR memory-access or Sysmon process-access coverage. Process names alone do not prove credential dumping. | Gap |
| [T1047 Windows Management Instrumentation](https://attack.mitre.org/techniques/T1047/) — Execution | Process starts alone do not cover remote WMI activity; add appropriate WMI and EDR telemetry only after review. | Gap |
| [T1021.002 SMB/Windows Admin Shares](https://attack.mitre.org/techniques/T1021/002/) — Lateral Movement | No domain-joined second Windows endpoint or configured share-audit dataset; correlate source and destination authentication, share, and process records. | Gap |
| [T1685.006 Clear Linux or Mac System Logs](https://attack.mitre.org/techniques/T1685/006/) — Defense Impairment | Auth syslog does not establish process/file activity or reliable log-tampering detection; consider approved audit/process and file-integrity sources. | Gap |
| [T1005 Data from Local System](https://attack.mitre.org/techniques/T1005/) — Collection | Sysmon FileCreate is restricted to a lab folder and does not provide general file-read evidence; investigate approved EDR/file-access sources. | Gap |
| [T1041 Exfiltration Over C2 Channel](https://attack.mitre.org/techniques/T1041/) — Exfiltration | No complete egress/proxy volume or payload context, nor established C2 channel; add authorized network and data-transfer telemetry. | Gap |
| [T1486 Data Encrypted for Impact](https://attack.mitre.org/techniques/T1486/) — Impact | No broad file-change, ransomware behavior, or backup-impact telemetry; use approved EDR, filesystem, and recovery evidence. | Gap |

Reconnaissance, Resource Development, and Discovery are not assessed by these
selected mappings. Absence of an annotated technique does not establish absence
of visibility or activity. Expand the matrix only after identifying a concrete
data source, hypothesis, owner, and test.

## Existing source boundaries

- The Windows forwarder selects Security, System, Application, PowerShell
  Operational, and Sysmon Operational channels. Actual audit policy and delivery
  must be verified; configured inputs alone do not prove event collection.
- Sysmon records process starts, but network connections are limited to
  `powershell.exe` and `curl.exe`, DNS to `powershell.exe`, file creation to the
  lab test folder, and registry events to the lab Run-key pattern.
- RHEL collects the Splunk host's local authentication and lab files. The
  directory server is separate and its logs are not automatically ingested.
- Splunk's `lab_hunter` role is limited to the six lab indexes; do not expand
  permissions just to query `_audit` or `_internal`. Request an authorized
  administrator's assistance when those sources are needed.
- The lab is not domain-joined and does not include EDR, cloud audit, mail,
  enterprise DNS, full proxy, or full packet collection by default.
