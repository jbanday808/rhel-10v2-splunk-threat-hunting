**Step 29 — Create the hunting search files**

On **RHEL**:

```
cd "$HOME/rhel-splunk-threat-hunting"
```

Create the health search:

```
cat > hunts/00-data-health.spl <<'EOF'
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h
| eval ingest_delay_seconds=_indextime-_time
| stats count latest(_time) as last_event max(_indextime) as last_received perc95(ingest_delay_seconds) as p95_delay_seconds by index host sourcetype
| eval seconds_since_receipt=now()-last_received
| convert ctime(last_event) ctime(last_received)
EOF
```

Create the encoded-PowerShell search:

```
cat > hunts/01-encoded-powershell.spl <<'EOF'
index=sysmon EventCode=1 earliest=-30m
| eval command=coalesce(CommandLine,process_command_line), image=coalesce(Image,process_path), account=coalesce(User,user)
| where match(image,"(?i)powershell[.]exe$") AND match(command,"(?i)-encodedcommand\s+")
| table _time host account image ParentImage command ProcessGuid
EOF
```

Create the account-change search:

```
cat > hunts/02-account-changes.spl <<'EOF'
index=win_security (EventCode=4720 OR EventCode=4732 OR EventCode=4733 OR EventCode=4726) earliest=-30m
| table _time host EventCode SubjectUserName TargetUserName MemberName TargetSid
| sort 0 _time
EOF
```

Create the failed-login search:

```
cat > hunts/03-failed-logons.spl <<'EOF'
index=win_security EventCode=4625 earliest=-30m
| eval account=coalesce(TargetUserName,Target_User_Name,user,"unknown"), source_ip=coalesce(IpAddress,Source_Network_Address,src_ip,"local-or-not-recorded")
| stats count values(LogonType) as logon_types values(Status) as status by host account source_ip
| sort - count
EOF
```

Create the scheduled-task search:

```
cat > hunts/04-scheduled-task.spl <<'EOF'
index=win_security EventCode=4698 earliest=-30m "SIEMLab-HuntTest"
| table _time host SubjectUserName TaskName TaskContent
EOF
```

Create the process/network search:

```
cat > hunts/05-process-network.spl <<'EOF'
index=sysmon (EventCode=1 OR EventCode=3) earliest=-30m
| eval image=coalesce(Image,process_path)
| search image="*curl.exe"
| stats earliest(_time) as first_seen values(EventCode) as event_ids values(image) as image values(CommandLine) as command values(DestinationIp) as destination_ip values(DestinationPort) as destination_port by host ProcessGuid
| convert ctime(first_seen)
EOF
```

Create the script-logging search:

```
cat > hunts/06-powershell-scriptblock.spl <<'EOF'
index=powershell earliest=-30m "SIEM-LAB-ENCODED-TEST"
| table _time host EventCode ScriptBlockText _raw
EOF
```

Create the Linux search:

```
cat > hunts/07-linux-pipeline.spl <<'EOF'
index=linux earliest=-30m "SIEM-LAB-LINUX-PIPELINE-TEST"
| table _time host source sourcetype _raw
EOF
```

Create the custom-field search:

```
cat > hunts/08-custom-fields.spl <<'EOF'
index=lab sourcetype=siem:lab earliest=-30m
| table _time host action result account _raw
EOF
```

Run each search in Splunk.

**Search-command overview:**

| Command         | Explanation                               |
| --------------- | ----------------------------------------- |
| `eval`          | Creates useful result values.             |
| `coalesce`      | Uses whichever listed field is available. |
| `where`         | Keeps matching records.                   |
| `match`         | Checks a text pattern.                    |
| `stats`         | Counts or combines records.               |
| `sort`          | Orders results.                           |
| `convert ctime` | Displays readable timestamps.             |

A match identifies activity to investigate; it does not prove an attack.

**Optional Splunk exercise:** [Cobalt Strike–associated named-pipe hunt and Atomic Red Team validation](../../hunts/cobalt-strike/COBALT_STRIKE_ATOMIC_VALIDATION.md) adds separate SPL files, a reviewed Sysmon pipe-event fragment, positive/negative controls and process-context review for WINHUNT01. Run it separately after event collection is verified; it is not part of the initial searches above.

---
