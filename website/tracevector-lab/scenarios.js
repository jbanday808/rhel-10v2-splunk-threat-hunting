/* Synthetic training records; no connection to a live Splunk instance. */
window.TV_SCENARIOS = [
  {
    id: 'ssh',
    title: 'A noisy SSH neighbor',
    summary: 'Investigate repeated authentication failures, group the evidence in SPL, and distinguish a hunting lead from a confirmed intrusion.',
    difficulty: 'Foundation', minutes: 15,
    technique: 'T1110.001', tactic: 'Credential Access',
    logSource: 'Normalized SSH authentication events · synthetic training data',
    spl: 'index=tracevector_lab sourcetype="tracevector:training" process="sshd" action="failure"\n| stats count AS failures values(user) AS users BY src_ip host\n| where failures >= 5',
    events: [
      {time:'2026-11-11 14:00:02',host:'rhel10-lab',src_ip:'192.0.2.44',user:'root',process:'sshd',action:'failure'},
      {time:'2026-11-11 14:00:12',host:'rhel10-lab',src_ip:'192.0.2.44',user:'root',process:'sshd',action:'failure'},
      {time:'2026-11-11 14:00:23',host:'rhel10-lab',src_ip:'192.0.2.44',user:'admin',process:'sshd',action:'failure'},
      {time:'2026-11-11 14:00:31',host:'rhel10-lab',src_ip:'192.0.2.44',user:'admin',process:'sshd',action:'failure'},
      {time:'2026-11-11 14:00:43',host:'rhel10-lab',src_ip:'192.0.2.44',user:'root',process:'sshd',action:'failure'},
      {time:'2026-11-11 14:01:02',host:'rhel10-lab',src_ip:'192.0.2.8',user:'analyst',process:'sshd',action:'success'}
    ],
    steps: [
      {title:'Read the authentication trail',body:'All six records are a fixed synthetic fixture. Inspect source, account, outcome, and time before drawing a conclusion.',question:'Which source accounts for all five failed logins?',options:['192.0.2.44','192.0.2.8','The host field does not identify a source IP'],answer:0,explanation:'192.0.2.44 has five failures across root and admin. The successful analyst login comes from a different source.'},
      {title:'Build the hunt',body:'The provided SPL filters failures, groups by source and host, and applies a training threshold of five. It assumes these normalized fields exist in a dedicated training index.',question:'What does the stats command produce here?',options:['One row for each failed password','An aggregate row for each source IP and host','A list of successful logins'],answer:1,explanation:'BY src_ip host groups the matching events. count becomes failures; values(user) preserves the distinct targeted accounts.'},
      {title:'Map and validate',body:'Repeated password failures can support a password-guessing hypothesis. Compare an approved scanner schedule, successful logins, and other host activity before escalating.',question:'What is the best next conclusion?',options:['The host is definitely compromised','T1110.001 is a useful hypothesis requiring corroboration','Every authentication failure proves persistence'],answer:1,explanation:'The ATT&CK mapping describes the suspected behavior, not a verdict. Record the time window and raw evidence, then validate the source and account activity.'}
    ],
    sources:[
      {label:'MITRE · Password Guessing',url:'https://attack.mitre.org/techniques/T1110/001/'},
      {label:'Splunk · stats reference',url:'https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.3/search-commands/stats'},
      {label:'RHEL 10 · Auditing the system',url:'https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/risk_reduction_and_recovery_operations/index'}
    ]
  },
  {
    id:'sudo',title:'Privilege in the wrong hands',
    summary:'Review a sudo activity trail, compare it with expected administrator behavior, and prepare a least-privilege remediation proposal.',
    difficulty:'Intermediate',minutes:20,
    technique:'T1548.003',tactic:'Privilege Escalation',
    logSource:'Normalized sudo / process records · synthetic training data',
    spl:'index=tracevector_lab sourcetype="tracevector:training" process="sudo" action="allowed"\n| stats count AS executions values(command) AS commands BY host user run_as',
    events:[
      {time:'2026-11-11 15:10:00',host:'rhel10-lab',user:'analyst',process:'sudo',action:'allowed',run_as:'root',command:'/usr/bin/systemctl status sshd'},
      {time:'2026-11-11 15:11:00',host:'rhel10-lab',user:'labuser',process:'sudo',action:'allowed',run_as:'root',command:'/usr/bin/bash'},
      {time:'2026-11-11 15:11:12',host:'rhel10-lab',user:'labuser',process:'sudo',action:'allowed',run_as:'root',command:'/usr/bin/id'},
      {time:'2026-11-11 15:12:00',host:'rhel10-lab',user:'guest',process:'sudo',action:'denied',run_as:'root',command:'/usr/bin/systemctl status sshd'}
    ],
    steps:[
      {title:'Establish expected behavior',body:'The exercise baseline permits analyst to inspect service status. labuser has no approved administrative role. Compare that baseline with the allowed events.',question:'Which activity most deserves investigation?',options:['analyst checking sshd status','labuser starting an allowed shell as root','A denied guest request proves root access'],answer:1,explanation:'The allowed root shell conflicts with the exercise baseline. Preserve the original sudo and process records, and confirm who authorized the session.'},
      {title:'Keep the actor visible',body:'The SPL groups activity by the original user, host, and target identity. On a real host, validate parser mappings and correlate process/audit evidence.',question:'Why retain both user and run_as?',options:['They always identify the same person','They distinguish the requesting account from the target privilege','run_as is the source IP address'],answer:1,explanation:'A target identity of root alone hides which account requested the action. Actor and target fields support attribution and privilege analysis.'},
      {title:'Propose a controlled fix',body:'Prepare a reviewable least-privilege proposal. Red Hat documents scoped sudo policies and syntax-aware editing with visudo. This Site does not apply host or repository changes.',question:'Which remediation plan is appropriate?',options:['Give every lab account unrestricted sudo','Review scoped sudoers.d permissions, validate syntax, and retest authorized tasks','Delete logs to reduce alert volume'],answer:1,explanation:'Document the proposed scope, validation, and rollback before applying an approved change. T1548.003 is a hypothesis about abuse of sudo privileges; legitimate sudo use alone is not malicious.'}
    ],
    sources:[
      {label:'MITRE · Sudo and Sudo Caching',url:'https://attack.mitre.org/techniques/T1548/003/'},
      {label:'RHEL 10 · Managing sudo access',url:'https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/security_hardening/managing-sudo-access'},
      {label:'Splunk · stats reference',url:'https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.3/search-commands/stats'}
    ]
  },
  {
    id:'cron',title:'The job that came back',
    summary:'Follow a scheduled-task change and recurring execution, then decide what evidence is needed to validate a persistence hypothesis.',
    difficulty:'Intermediate',minutes:20,
    technique:'T1053.003',tactic:'Persistence',
    logSource:'Normalized file-change and cron records · synthetic training data',
    spl:'index=tracevector_lab sourcetype="tracevector:training" resource="/etc/cron.d/telemetry-test"\n| stats count AS events values(action) AS actions values(user) AS users BY host resource',
    events:[
      {time:'2026-11-11 16:00:00',host:'rhel10-lab',user:'labuser',process:'file_monitor',action:'created',resource:'/etc/cron.d/telemetry-test'},
      {time:'2026-11-11 16:05:00',host:'rhel10-lab',user:'root',process:'crond',action:'executed',resource:'/etc/cron.d/telemetry-test'},
      {time:'2026-11-11 16:10:00',host:'rhel10-lab',user:'root',process:'crond',action:'executed',resource:'/etc/cron.d/telemetry-test'},
      {time:'2026-11-11 16:15:00',host:'rhel10-lab',user:'root',process:'crond',action:'executed',resource:'/etc/cron.d/telemetry-test'}
    ],
    steps:[
      {title:'Connect change to execution',body:'A file-change sensor observed a new task, followed by three execution records. The resource association is supplied by the training fixture; ordinary cron logs may require additional correlation.',question:'What is the recurring interval in the execution records?',options:['Five minutes','One hour','There is only one execution'],answer:0,explanation:'Execution appears at 16:05, 16:10, and 16:15. A repeating schedule is a useful lead, but legitimate automation also repeats.'},
      {title:'Map the behavior',body:'Cron can schedule legitimate work and can also support adversary persistence. Review the creator, target account, task content, and approved change history.',question:'Which ATT&CK sub-technique matches a suspicious cron task?',options:['T1110.001 · Password Guessing','T1053.003 · Cron','T1548.003 · Sudo and Sudo Caching'],answer:1,explanation:'T1053.003 covers cron abuse. Persistence is the exercise focus; ATT&CK also associates cron with execution and privilege escalation.'},
      {title:'Preserve, review, and retest',body:'Capture task metadata, content, hashes, owner, and correlated process records. Determine whether the task is authorized before proposing removal or containment.',question:'Which evidence best distinguishes approved automation from suspicious persistence?',options:['The filename alone','Task content, ownership, change approval, and execution lineage','A screenshot without a host or timestamp'],answer:1,explanation:'Combine provenance with behavior. Record a remediation proposal and retest plan; preserve the evidence and obtain review before modifying the repository.'}
    ],
    sources:[
      {label:'MITRE · Cron',url:'https://attack.mitre.org/techniques/T1053/003/'},
      {label:'RHEL 10 · Auditing the system',url:'https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/risk_reduction_and_recovery_operations/index'},
      {label:'Splunk · stats reference',url:'https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.3/search-commands/stats'}
    ]
  },
  {
    "id": "powershell",
    "title": "A script behind the switch",
    "summary": "Inspect an encoded PowerShell command, preserve its process context, and distinguish a suspicious-looking argument from proof of malicious execution.",
    "difficulty": "Intermediate",
    "minutes": 20,
    "platform": "Windows 11",
    "coverage": "Candidate",
    "technique": "T1059.001",
    "tactic": "Execution",
    "logSource": "Normalized Sysmon process records · fixed synthetic training data · UTC",
    "spl": "index=tracevector_lab sourcetype=\"tracevector:training\"\n| where event_code=1 AND match(image,\"(?i)powershell[.]exe$\") AND match(command_line,\"(?i)-encodedcommand[[:space:]]\")\n| table time host user parent_image command_line process_guid\n| sort 0 time",
    "events": [
      {
        "time": "2026-11-11 18:00:00",
        "host": "winhunt-training",
        "event_code": 1,
        "user": "lab-analyst",
        "image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "parent_image": "explorer.exe",
        "command_line": "powershell.exe Get-Date",
        "process_guid": "TRAIN-PS-001"
      },
      {
        "time": "2026-11-11 18:01:00",
        "host": "winhunt-training",
        "event_code": 1,
        "user": "lab-trainee",
        "image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "parent_image": "cmd.exe",
        "command_line": "powershell.exe -EncodedCommand UwBZAE4AVABIAEUAVABJAEMAXwBNAEEAUgBLAEUAUgA=",
        "process_guid": "TRAIN-PS-002"
      },
      {
        "time": "2026-11-11 18:01:02",
        "host": "winhunt-training",
        "event_code": 3,
        "user": "lab-trainee",
        "image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "parent_image": "cmd.exe",
        "command_line": "powershell.exe -EncodedCommand UwBZAE4AVABIAEUAVABJAEMAXwBNAEEAUgBLAEUAUgA=",
        "process_guid": "TRAIN-PS-002"
      },
      {
        "time": "2026-11-11 18:02:00",
        "host": "winhunt-training",
        "event_code": 1,
        "user": "lab-analyst",
        "image": "C:\\Windows\\System32\\cmd.exe",
        "parent_image": "explorer.exe",
        "command_line": "cmd.exe /c echo TRAINING",
        "process_guid": "TRAIN-CMD-003"
      }
    ],
    "steps": [
      {
        "title": "Inspect the command in context",
        "body": "These four rows are synthetic. The encoded value represents a training marker and is never executed by this Site. Inspect the event type, parent process, account, and ProcessGuid together.",
        "question": "Which process-start record matches the encoded PowerShell hunt?",
        "options": [
          "TRAIN-PS-001 running Get-Date",
          "The event-code 3 row, because every connection is a process start",
          "TRAIN-PS-002 with event_code 1 and -EncodedCommand"
        ],
        "answer": 2,
        "explanation": "TRAIN-PS-002 has a Sysmon-style process-start record with the matching argument. The event-code 3 row describes a different event type for the same synthetic process; Get-Date does not match the argument filter."
      },
      {
        "title": "Keep one row per observed start",
        "body": "The reference SPL selects event_code 1, PowerShell image paths, and the encoded-command argument. It returns the command with its actor, parent, host, time, and ProcessGuid. It does not decode or execute the argument.",
        "question": "Why does the reference result contain one row rather than two rows for TRAIN-PS-002?",
        "options": [
          "The search filters process starts and excludes the event-code 3 connection",
          "Splunk automatically deletes duplicate evidence",
          "Every ProcessGuid represents a confirmed incident"
        ],
        "answer": 0,
        "explanation": "The event_code=1 condition selects the single observed process start. Correlation with network or script-block data is a separate investigation step; filtering a row does not delete source evidence."
      },
      {
        "title": "Test the benign alternative",
        "body": "An encoded argument can appear in legitimate administration. Compare authorized change records, the parent and user context, and approved script-block evidence. The project ships candidate hunts, not a validated PowerShell detection.",
        "question": "Which finding is justified by these records?",
        "options": [
          "The encoded value proves a malware infection",
          "An encoded PowerShell start is a lead that needs authorization and behavior checks",
          "The account should be disabled automatically by this Site"
        ],
        "answer": 1,
        "explanation": "T1059.001 is a behavior hypothesis. Encoding alone does not establish malicious intent, script execution success, or compromise. Preserve the original records and investigate both benign and suspicious explanations."
      }
    ],
    "fixtureResult": [
      {
        "time": "2026-11-11 18:01:00",
        "host": "winhunt-training",
        "user": "lab-trainee",
        "parent_image": "cmd.exe",
        "command_line": "powershell.exe -EncodedCommand UwBZAE4AVABIAEUAVABJAEMAXwBNAEEAUgBLAEUAUgA=",
        "process_guid": "TRAIN-PS-002"
      }
    ],
    "sources": [
      {
        "label": "Project · Encoded PowerShell hunt",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/hunts/01-encoded-powershell.spl"
      },
      {
        "label": "Project · ATT&CK coverage and telemetry boundaries",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/docs/mitre-attack/coverage.md"
      },
      {
        "label": "MITRE · PowerShell",
        "url": "https://attack.mitre.org/techniques/T1059/001/"
      }
    ]
  },
  {
    "id": "account",
    "title": "An account fast-tracked to admin",
    "summary": "Correlate a new local account with a later group addition, then verify which group received it and whether the change was authorized.",
    "difficulty": "Intermediate",
    "minutes": 25,
    "platform": "Windows 11",
    "coverage": "Candidate",
    "technique": "T1136.001 / T1098.007",
    "tactic": "Persistence / Privilege Escalation",
    "logSource": "Normalized Windows Security 4720 / 4732 records · fixed synthetic training data · UTC",
    "spl": "index=tracevector_lab sourcetype=\"tracevector:training\" (event_code=4720 OR event_code=4732)\n| eval _time=strptime(time,\"%Y-%m-%d %H:%M:%S\"), account_sid=if(event_code=4720,target_sid,member_sid)\n| eval created_time=if(event_code=4720,_time,null()), created_name=if(event_code=4720,target_user,null())\n| sort 0 _time\n| streamstats last(created_time) AS created_at last(created_name) AS account BY host account_sid\n| where event_code=4732 AND isnotnull(created_at) AND _time>=created_at AND _time-created_at<=3600\n| eval added_at=time, created_at=strftime(created_at,\"%Y-%m-%d %H:%M:%S\")\n| table host account account_sid target_user subject_user group_sid created_at added_at",
    "events": [
      {
        "time": "2026-11-11 18:10:00",
        "host": "winhunt-training",
        "event_code": 4720,
        "target_sid": "S-1-5-21-100-200-300-1105",
        "member_sid": "-",
        "target_user": "lab-newuser",
        "subject_user": "lab-operator",
        "group_sid": "-"
      },
      {
        "time": "2026-11-11 18:18:00",
        "host": "winhunt-training",
        "event_code": 4732,
        "target_sid": "S-1-5-32-544",
        "member_sid": "S-1-5-21-100-200-300-1105",
        "target_user": "Administrators",
        "subject_user": "lab-operator",
        "group_sid": "S-1-5-32-544"
      },
      {
        "time": "2026-11-11 18:20:00",
        "host": "winhunt-training",
        "event_code": 4732,
        "target_sid": "S-1-5-32-545",
        "member_sid": "S-1-5-21-100-200-300-1199",
        "target_user": "Users",
        "subject_user": "lab-operator",
        "group_sid": "S-1-5-32-545"
      },
      {
        "time": "2026-11-11 19:40:00",
        "host": "winhunt-training",
        "event_code": 4732,
        "target_sid": "S-1-5-32-555",
        "member_sid": "S-1-5-21-100-200-300-1105",
        "target_user": "Remote Desktop Users",
        "subject_user": "lab-operator",
        "group_sid": "S-1-5-32-555"
      }
    ],
    "steps": [
      {
        "title": "Follow the account, not the group SID",
        "body": "Event 4720 identifies the created account in target_sid. In event 4732, member_sid identifies the added member while target_sid identifies the destination group. Every account and SID in this fixture is synthetic.",
        "question": "Which fields connect lab-newuser to its group-addition record?",
        "options": [
          "target_sid from event 4720 and target_sid from event 4732",
          "target_sid from event 4720 and member_sid from event 4732, on the same host",
          "The shared subject_user alone"
        ],
        "answer": 1,
        "explanation": "The account SID ends in 1105 and appears as the created target and later added member. Joining target_sid to the group's target_sid would correlate different objects; the actor alone could perform many unrelated changes."
      },
      {
        "title": "Apply the correlation window",
        "body": "The reference SPL parses the fixture time, orders events, carries the account's creation time forward, and keeps each group addition within one hour. The unknown member has no matching creation row, and the 19:40 addition is outside the window.",
        "question": "Which group addition remains in the fixed reference result?",
        "options": [
          "The 18:18 addition of lab-newuser to Administrators",
          "Every action performed by lab-operator",
          "Only the 19:40 Remote Desktop Users addition"
        ],
        "answer": 0,
        "explanation": "The 18:18 addition occurs eight minutes after the 18:10 creation and has the matching member SID. The 19:40 record is 90 minutes after creation and is excluded by this illustrative one-hour rule."
      },
      {
        "title": "Verify privilege and approval",
        "body": "The synthetic destination Administrators has group SID S-1-5-32-544. Check the actual group identity, actor, change approval, and effective account privileges before deciding whether the addition was unauthorized.",
        "question": "What does the account-to-group correlation establish?",
        "options": [
          "Every group membership change is privilege escalation",
          "The account has already stolen credentials",
          "A new account was added to a privileged group within the window; authorization still needs review"
        ],
        "answer": 2,
        "explanation": "This fixture supports a candidate T1136.001 / T1098.007 investigation. It does not establish adversarial intent, stolen credentials, or a completed real deployment. Preserve both event records and the reviewed change context."
      }
    ],
    "fixtureResult": [
      {
        "host": "winhunt-training",
        "account": "lab-newuser",
        "account_sid": "S-1-5-21-100-200-300-1105",
        "target_user": "Administrators",
        "subject_user": "lab-operator",
        "group_sid": "S-1-5-32-544",
        "created_at": "2026-11-11 18:10:00",
        "added_at": "2026-11-11 18:18:00"
      }
    ],
    "sources": [
      {
        "label": "Project · Account-to-group correlation",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/hunts/mitre-attack/03-account-to-group.spl"
      },
      {
        "label": "Project · ATT&CK coverage mapping",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/docs/mitre-attack/coverage.md"
      },
      {
        "label": "MITRE · Local Account",
        "url": "https://attack.mitre.org/techniques/T1136/001/"
      },
      {
        "label": "MITRE · Additional Local or Domain Groups",
        "url": "https://attack.mitre.org/techniques/T1098/007/"
      }
    ]
  },
  {
    "id": "runkey",
    "title": "The startup entry that changed",
    "summary": "Review a monitored Run-key change, pivot to the modifying process, and identify the evidence needed to test a persistence hypothesis.",
    "difficulty": "Intermediate",
    "minutes": 20,
    "platform": "Windows 11",
    "coverage": "Candidate",
    "technique": "T1547.001",
    "tactic": "Persistence / Privilege Escalation",
    "logSource": "Normalized Sysmon registry records · fixed synthetic training data · UTC",
    "spl": "index=tracevector_lab sourcetype=\"tracevector:training\" (event_code=12 OR event_code=13 OR event_code=14)\n| where like(lower(target_object),\"%currentversion%run%siemlab%\")\n| table time host event_code user image target_object details process_guid\n| sort 0 time",
    "events": [
      {
        "time": "2026-11-11 18:30:00",
        "host": "winhunt-training",
        "event_code": 12,
        "user": "lab-trainee",
        "image": "powershell.exe",
        "target_object": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\SIEMLab",
        "details": "Synthetic monitored object created",
        "process_guid": "TRAIN-REG-001"
      },
      {
        "time": "2026-11-11 18:31:00",
        "host": "winhunt-training",
        "event_code": 13,
        "user": "lab-trainee",
        "image": "powershell.exe",
        "target_object": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\SIEMLab",
        "details": "C:\\TraceVector\\lab-marker.cmd",
        "process_guid": "TRAIN-REG-001"
      },
      {
        "time": "2026-11-11 18:32:00",
        "host": "winhunt-training",
        "event_code": 13,
        "user": "lab-analyst",
        "image": "approved-updater.exe",
        "target_object": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\Updater",
        "details": "C:\\TraceVector\\approved-updater.exe",
        "process_guid": "TRAIN-REG-002"
      },
      {
        "time": "2026-11-11 18:33:00",
        "host": "winhunt-training",
        "event_code": 12,
        "user": "lab-analyst",
        "image": "regedit.exe",
        "target_object": "HKCU\\Software\\TraceVector\\Preferences",
        "details": "Synthetic preference key created",
        "process_guid": "TRAIN-REG-003"
      }
    ],
    "steps": [
      {
        "title": "Identify the monitored value",
        "body": "The fixture includes two records for the SIEMLab Run path and two unrelated registry changes. The filename in details is a synthetic marker reference; this Site does not create the value or run the file.",
        "question": "Which record shows the monitored SIEMLab value being set?",
        "options": [
          "The Updater record at 18:32",
          "The TraceVector Preferences record at 18:33",
          "The event-code 13 record at 18:31 with TRAIN-REG-001"
        ],
        "answer": 2,
        "explanation": "The 18:31 event names the SIEMLab Run path and the synthetic marker command. The preceding event-code 12 record is part of the same process context, while the other target objects are outside this query's scope."
      },
      {
        "title": "Understand the collection boundary",
        "body": "The SPL mirrors the repository's focused SIEMLab Run-key hunt. A training filter can narrow visible rows, but it cannot supply events the actual sensor never collected. The shipped Sysmon rule does not cover every Run value or Startup folder.",
        "question": "What can you infer if this focused query returns no records in the real lab?",
        "options": [
          "The monitored SIEMLab path has no matching collected records; broader persistence remains unassessed",
          "No startup persistence exists anywhere on the host",
          "Every other registry value is known to be safe"
        ],
        "answer": 0,
        "explanation": "An empty result can reflect scope, missing collection, field mapping, time selection, or no matching activity. Verify source health and the actual filter before making a coverage statement."
      },
      {
        "title": "Separate a change from execution",
        "body": "Pivot on the host and ProcessGuid, preserve the registry details, and review the writer's identity and change approval. To establish later execution, obtain suitable logon and process records rather than relying on the value alone.",
        "question": "Which conclusion best fits these synthetic records?",
        "options": [
          "The marker definitely executed at every sign-in",
          "A monitored startup value changed; its authorization and execution need corroboration",
          "T1547.001 is a verified detection because a key name matched"
        ],
        "answer": 1,
        "explanation": "A Run-key change supports a persistence hypothesis. It does not prove that the target ran, that it was malicious, or that the repository's broader persistence coverage is validated."
      }
    ],
    "fixtureResult": [
      {
        "time": "2026-11-11 18:30:00",
        "host": "winhunt-training",
        "event_code": 12,
        "user": "lab-trainee",
        "image": "powershell.exe",
        "target_object": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\SIEMLab",
        "details": "Synthetic monitored object created",
        "process_guid": "TRAIN-REG-001"
      },
      {
        "time": "2026-11-11 18:31:00",
        "host": "winhunt-training",
        "event_code": 13,
        "user": "lab-trainee",
        "image": "powershell.exe",
        "target_object": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\SIEMLab",
        "details": "C:\\TraceVector\\lab-marker.cmd",
        "process_guid": "TRAIN-REG-001"
      }
    ],
    "sources": [
      {
        "label": "Project · Focused SIEMLab Run-key hunt",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/hunts/mitre-attack/05-lab-run-key.spl"
      },
      {
        "label": "Project · Sysmon and telemetry boundaries",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/docs/mitre-attack/coverage.md#existing-source-boundaries"
      },
      {
        "label": "MITRE · Registry Run Keys / Startup Folder",
        "url": "https://attack.mitre.org/techniques/T1547/001/"
      }
    ]
  },
  {
    "id": "logclear",
    "title": "When the log goes quiet",
    "summary": "Separate Windows log-clear candidates from a same-number provider distractor, then preserve independent evidence before interpreting missing logs.",
    "difficulty": "Intermediate",
    "minutes": 20,
    "platform": "Windows 11",
    "coverage": "Candidate",
    "technique": "T1685.005",
    "tactic": "Defense Impairment",
    "logSource": "Normalized Windows Security / System records · fixed synthetic training data · UTC",
    "spl": "index=tracevector_lab sourcetype=\"tracevector:training\" (event_code=1102 OR event_code=104)\n| where (training_source=\"win_security\" AND event_code=1102) OR (training_source=\"win_system\" AND event_code=104 AND provider=\"Microsoft-Windows-Eventlog\")\n| table time host training_source event_code provider actor source\n| sort 0 time",
    "events": [
      {
        "time": "2026-11-11 19:00:00",
        "host": "winhunt-training",
        "training_source": "win_security",
        "event_code": 1102,
        "provider": "Microsoft-Windows-Eventlog",
        "actor": "lab-operator",
        "source": "Security"
      },
      {
        "time": "2026-11-11 19:01:00",
        "host": "winhunt-training",
        "training_source": "win_system",
        "event_code": 104,
        "provider": "Microsoft-Windows-Eventlog",
        "actor": "lab-operator",
        "source": "System"
      },
      {
        "time": "2026-11-11 19:02:00",
        "host": "winhunt-training",
        "training_source": "win_system",
        "event_code": 104,
        "provider": "TraceVector-TrainingService",
        "actor": "lab-service",
        "source": "System"
      },
      {
        "time": "2026-11-11 19:03:00",
        "host": "winhunt-training",
        "training_source": "win_system",
        "event_code": 6005,
        "provider": "EventLog",
        "actor": "SYSTEM",
        "source": "System"
      }
    ],
    "steps": [
      {
        "title": "Read the provider with the event code",
        "body": "Event numbers are not globally unique across providers. The fixture includes a System 104 row from Microsoft-Windows-Eventlog and a distractor with the same number from a synthetic training service.",
        "question": "Which System 104 row is relevant to the log-clear candidate?",
        "options": [
          "The 19:01 Microsoft-Windows-Eventlog row",
          "Any event numbered 104, regardless of provider",
          "The 19:03 event-code 6005 row"
        ],
        "answer": 0,
        "explanation": "Provider verification keeps the 19:01 row in scope. The synthetic training-service row shares the number but is not evidence of a Windows Event Log clear operation."
      },
      {
        "title": "Review the filtered candidates",
        "body": "The reference query selects Security 1102 and provider-verified System 104 records. training_source is a normalized fixture field that represents the original project index; all exercise rows still belong to tracevector_lab.",
        "question": "What does the fixed reference result contain?",
        "options": [
          "Four confirmed intrusions",
          "The two candidate rows at 19:00 and 19:01",
          "Only the unrelated training-service event"
        ],
        "answer": 1,
        "explanation": "The query returns Security 1102 and the verified-provider System 104 row. Both remain investigation candidates; the table does not establish why the operation occurred."
      },
      {
        "title": "Preserve an independent trail",
        "body": "Review authorized maintenance and actor context, and preserve already-forwarded copies and independent collection records. The repository's reviewed ATT&CK v20.1 mapping uses T1685.005 for Clear Windows Event Logs.",
        "question": "Which next step preserves the evidence boundary?",
        "options": [
          "Clear the remaining logs to recreate the event",
          "Treat a missing record as proof that clearing never occurred",
          "Compare collector records, source health, time alignment, and the approved maintenance history"
        ],
        "answer": 2,
        "explanation": "Independent collection and authorization context help distinguish maintenance, collection gaps, and suspicious clearing. Missing events do not rule out clearing, and this synthetic exercise does not alter real logs or validate live coverage."
      }
    ],
    "fixtureResult": [
      {
        "time": "2026-11-11 19:00:00",
        "host": "winhunt-training",
        "training_source": "win_security",
        "event_code": 1102,
        "provider": "Microsoft-Windows-Eventlog",
        "actor": "lab-operator",
        "source": "Security"
      },
      {
        "time": "2026-11-11 19:01:00",
        "host": "winhunt-training",
        "training_source": "win_system",
        "event_code": 104,
        "provider": "Microsoft-Windows-Eventlog",
        "actor": "lab-operator",
        "source": "System"
      }
    ],
    "sources": [
      {
        "label": "Project · Windows log-clear candidates",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/hunts/mitre-attack/06-event-log-clear-candidates.spl"
      },
      {
        "label": "Project · Reviewed ATT&CK v20.1 mapping",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/docs/mitre-attack/coverage.md"
      },
      {
        "label": "MITRE · Clear Windows Event Logs",
        "url": "https://attack.mitre.org/techniques/T1685/005/"
      }
    ]
  },
  {
    "id": "dns",
    "title": "A name worth a second look",
    "summary": "Review PowerShell-related DNS records, compare repeated names, and identify the evidence needed before claiming command and control.",
    "difficulty": "Intermediate",
    "minutes": 20,
    "technique": "T1071.004",
    "tactic": "Command and Control",
    "platform": "Windows 11",
    "coverage": "Context only",
    "logSource": "Normalized Sysmon DNS records · fixed synthetic training data",
    "spl": "index=tracevector_lab sourcetype=\"tracevector:training\" event_code=22 image=\"powershell.exe\"\n| stats count AS queries values(process_guid) AS processes values(query_result) AS answers BY host query_name\n| sort 0 query_name",
    "events": [
      {
        "time": "2026-11-11 17:00:00",
        "host": "WINHUNT01",
        "event_code": 22,
        "process_guid": "training-ps-01",
        "image": "powershell.exe",
        "query_name": "status-sync.example.test",
        "query_result": "203.0.113.25"
      },
      {
        "time": "2026-11-11 17:01:00",
        "host": "WINHUNT01",
        "event_code": 22,
        "process_guid": "training-ps-01",
        "image": "powershell.exe",
        "query_name": "status-sync.example.test",
        "query_result": "203.0.113.25"
      },
      {
        "time": "2026-11-11 17:02:00",
        "host": "WINHUNT01",
        "event_code": 22,
        "process_guid": "training-ps-01",
        "image": "powershell.exe",
        "query_name": "status-sync.example.test",
        "query_result": "203.0.113.25"
      },
      {
        "time": "2026-11-11 17:03:00",
        "host": "WINHUNT01",
        "event_code": 22,
        "process_guid": "training-ps-02",
        "image": "powershell.exe",
        "query_name": "assets.example.test",
        "query_result": "198.51.100.20"
      },
      {
        "time": "2026-11-11 17:04:00",
        "host": "WINHUNT01",
        "event_code": 22,
        "process_guid": "training-browser-01",
        "image": "chrome.exe",
        "query_name": "status-sync.example.test",
        "query_result": "203.0.113.25"
      }
    ],
    "steps": [
      {
        "title": "Read the process context",
        "body": "All domains and addresses are reserved training examples. Count the records for the selected process before treating repetition as unusual. Browser activity is a distractor in this fixture.",
        "question": "How many PowerShell DNS records reference status-sync.example.test?",
        "options": [
          "Four, because the browser record is also PowerShell",
          "Three, all from training-ps-01",
          "One, because repeated names collapse into one event"
        ],
        "answer": 1,
        "explanation": "Three records have image=powershell.exe and that query_name. The fourth record for the name belongs to chrome.exe and is excluded by the reference query."
      },
      {
        "title": "Group the observed names",
        "body": "The SPL filters normalized Sysmon 22 records and groups them by host and query name. The fixture contains four matching PowerShell records across two names.",
        "question": "What should the reference query return?",
        "options": [
          "Two rows: assets.example.test with 1 query, and status-sync.example.test with 3",
          "Five rows, one for every fixture record",
          "A list of confirmed DNS tunnels"
        ],
        "answer": 0,
        "explanation": "stats aggregates the filtered records into two name/host groups and retains their process identifiers and answers. It does not classify DNS payloads or confirm tunneling."
      },
      {
        "title": "Keep the hypothesis bounded",
        "body": "The repository collects selected PowerShell DNS context, not complete enterprise DNS visibility. Repeated queries can also come from approved health checks or scripts.",
        "question": "What is the strongest next step?",
        "options": [
          "Declare T1071.004 proven because a name repeats",
          "Block all DNS without reviewing dependencies",
          "Review the script, process lineage, approved task, DNS details, and related connections"
        ],
        "answer": 2,
        "explanation": "T1071.004 is context only here. Query records alone establish neither command and control nor tunneling. Confirm collection scope and benign alternatives before escalation."
      }
    ],
    "sources": [
      {
        "label": "MITRE · DNS",
        "url": "https://attack.mitre.org/techniques/T1071/004/"
      },
      {
        "label": "Project · PowerShell DNS context",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/hunts/mitre-attack/08-powershell-dns-context.spl"
      },
      {
        "label": "Project · Coverage and telemetry limits",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/docs/mitre-attack/coverage.md"
      }
    ],
    "fixtureResult": [
      {
        "host": "WINHUNT01",
        "query_name": "assets.example.test",
        "queries": 1,
        "processes": [
          "training-ps-02"
        ],
        "answers": [
          "198.51.100.20"
        ]
      },
      {
        "host": "WINHUNT01",
        "query_name": "status-sync.example.test",
        "queries": 3,
        "processes": [
          "training-ps-01"
        ],
        "answers": [
          "203.0.113.25"
        ]
      }
    ]
  },
  {
    "id": "web",
    "title": "A process with a new destination",
    "summary": "Correlate process starts and network events by process identity, then separate a connection from evidence of a web protocol or adversarial intent.",
    "difficulty": "Intermediate",
    "minutes": 25,
    "technique": "T1071.001",
    "tactic": "Command and Control",
    "platform": "Windows 11",
    "coverage": "Context only",
    "logSource": "Normalized Sysmon process-start and network records · fixed synthetic training data",
    "spl": "index=tracevector_lab sourcetype=\"tracevector:training\" (event_code=1 OR event_code=3) (image=\"powershell.exe\" OR image=\"curl.exe\")\n| stats count(eval(event_code=1)) AS process_events count(eval(event_code=3)) AS network_events values(image) AS images values(parent_image) AS parents values(destination_ip) AS destinations values(destination_port) AS ports BY host process_guid\n| where process_events>0 AND network_events>0\n| sort 0 process_guid",
    "events": [
      {
        "time": "2026-11-11 17:20:00",
        "host": "WINHUNT01",
        "event_code": 1,
        "process_guid": "training-ps-01",
        "image": "powershell.exe",
        "parent_image": "explorer.exe",
        "destination_ip": null,
        "destination_port": null,
        "user": "LAB\\analyst"
      },
      {
        "time": "2026-11-11 17:20:02",
        "host": "WINHUNT01",
        "event_code": 3,
        "process_guid": "training-ps-01",
        "image": "powershell.exe",
        "parent_image": null,
        "destination_ip": "203.0.113.25",
        "destination_port": 443,
        "user": "LAB\\analyst"
      },
      {
        "time": "2026-11-11 17:21:00",
        "host": "WINHUNT01",
        "event_code": 1,
        "process_guid": "training-ps-02",
        "image": "powershell.exe",
        "parent_image": "taskeng.exe",
        "destination_ip": null,
        "destination_port": null,
        "user": "LAB\\service"
      },
      {
        "time": "2026-11-11 17:21:03",
        "host": "WINHUNT01",
        "event_code": 3,
        "process_guid": "training-ps-03",
        "image": "powershell.exe",
        "parent_image": null,
        "destination_ip": "192.0.2.99",
        "destination_port": 443,
        "user": "LAB\\service"
      },
      {
        "time": "2026-11-11 17:22:00",
        "host": "WINHUNT01",
        "event_code": 1,
        "process_guid": "training-curl-01",
        "image": "curl.exe",
        "parent_image": "powershell.exe",
        "destination_ip": null,
        "destination_port": null,
        "user": "LAB\\analyst"
      },
      {
        "time": "2026-11-11 17:22:01",
        "host": "WINHUNT01",
        "event_code": 3,
        "process_guid": "training-curl-01",
        "image": "curl.exe",
        "parent_image": null,
        "destination_ip": "198.51.100.20",
        "destination_port": 80,
        "user": "LAB\\analyst"
      }
    ],
    "steps": [
      {
        "title": "Follow one process identity",
        "body": "A process image can appear in several independent executions. Here event_code=1 records a process start and event_code=3 records a connection. Null fields are not supplied by that record type.",
        "question": "Which PowerShell connection has a matching process-start record?",
        "options": [
          "training-ps-03, because its image is also powershell.exe",
          "Both PowerShell connections, regardless of process_guid",
          "training-ps-01 on WINHUNT01"
        ],
        "answer": 2,
        "explanation": "training-ps-01 has both event types on the same host. training-ps-02 has only a start; training-ps-03 has only a connection. Matching the image name would incorrectly join different executions."
      },
      {
        "title": "Test the correlation key",
        "body": "The SPL groups by host and process_guid and retains only groups with both event types. Process identity is more specific than image name or a short time gap.",
        "question": "Which groups survive the filter?",
        "options": [
          "training-ps-01 and training-curl-01",
          "training-ps-02 and training-ps-03",
          "Every event using destination port 443"
        ],
        "answer": 0,
        "explanation": "Each surviving group has one process-start event and one network event. The orphan start and orphan connection remain separate and fail the two-count condition."
      },
      {
        "title": "Ask what the connection cannot prove",
        "body": "The fixture supplies destination IPs and ports. It contains no packet content, HTTP request, TLS handshake, or verified command-and-control exchange. Approved downloads and administration are benign alternatives.",
        "question": "What does a destination port of 443 establish here?",
        "options": [
          "The process definitely used HTTPS for C2",
          "Only the recorded destination port; protocol and intent need corroboration",
          "The remote endpoint is a confirmed threat actor"
        ],
        "answer": 1,
        "explanation": "TCP 443 alone proves neither HTTPS nor command and control. T1071.001 remains context only. Review process lineage, destination ownership, authorized tasks, and approved protocol evidence before escalating."
      }
    ],
    "sources": [
      {
        "label": "MITRE · Web Protocols",
        "url": "https://attack.mitre.org/techniques/T1071/001/"
      },
      {
        "label": "Project · Process/network correlation",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/hunts/mitre-attack/01-process-network.spl"
      },
      {
        "label": "Project · Context-only coverage",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/docs/mitre-attack/coverage.md"
      }
    ],
    "fixtureResult": [
      {
        "host": "WINHUNT01",
        "process_guid": "training-curl-01",
        "process_events": 1,
        "network_events": 1,
        "images": [
          "curl.exe"
        ],
        "parents": [
          "powershell.exe"
        ],
        "destinations": [
          "198.51.100.20"
        ],
        "ports": [
          80
        ]
      },
      {
        "host": "WINHUNT01",
        "process_guid": "training-ps-01",
        "process_events": 1,
        "network_events": 1,
        "images": [
          "powershell.exe"
        ],
        "parents": [
          "explorer.exe"
        ],
        "destinations": [
          "203.0.113.25"
        ],
        "ports": [
          443
        ]
      }
    ]
  },
  {
    "id": "spray",
    "title": "One source, several accounts",
    "summary": "Compare failures across domain/account pairs in a fixed time window and test a password-spraying hypothesis without assuming that passwords are visible.",
    "difficulty": "Intermediate",
    "minutes": 20,
    "technique": "T1110.003",
    "tactic": "Credential Access",
    "platform": "Windows 11",
    "coverage": "Candidate",
    "logSource": "Normalized Windows Security 4625 records · fixed synthetic training data",
    "spl": "index=tracevector_lab sourcetype=\"tracevector:training\" event_code=4625\n| eval _time=strptime(time,\"%Y-%m-%d %H:%M:%S\"), source_ip=lower(trim(source_ip)), account=lower(trim(account)), account_domain=lower(trim(account_domain))\n| where account!=\"\" AND account!=\"-\" AND source_ip!=\"\" AND source_ip!=\"-\" AND source_ip!=\"127.0.0.1\" AND source_ip!=\"::1\" AND source_ip!=\"0.0.0.0\"\n| eval target_account=account_domain.\":\".account\n| bin _time span=15m\n| stats count AS failures dc(target_account) AS distinct_accounts values(target_account) AS accounts BY source_ip _time\n| where distinct_accounts>=3\n| eval window_start=strftime(_time,\"%Y-%m-%d %H:%M:%S\")\n| table window_start source_ip failures distinct_accounts accounts",
    "events": [
      {
        "time": "2026-11-11 18:01:00",
        "host": "WINHUNT01",
        "event_code": 4625,
        "source_ip": "192.0.2.44",
        "account_domain": "LAB",
        "account": "alice"
      },
      {
        "time": "2026-11-11 18:02:00",
        "host": "WINHUNT01",
        "event_code": 4625,
        "source_ip": "192.0.2.44",
        "account_domain": "LAB",
        "account": "bob"
      },
      {
        "time": "2026-11-11 18:03:00",
        "host": "WINHUNT01",
        "event_code": 4625,
        "source_ip": "192.0.2.44",
        "account_domain": "DEV",
        "account": "alice"
      },
      {
        "time": "2026-11-11 18:04:00",
        "host": "WINHUNT01",
        "event_code": 4625,
        "source_ip": "192.0.2.44",
        "account_domain": "LAB",
        "account": "alice"
      },
      {
        "time": "2026-11-11 18:05:00",
        "host": "WINHUNT01",
        "event_code": 4625,
        "source_ip": "127.0.0.1",
        "account_domain": "LAB",
        "account": "charlie"
      },
      {
        "time": "2026-11-11 18:16:00",
        "host": "WINHUNT01",
        "event_code": 4625,
        "source_ip": "192.0.2.44",
        "account_domain": "LAB",
        "account": "diana"
      }
    ],
    "steps": [
      {
        "title": "Count identities, not just names",
        "body": "The same username can refer to different identities in different domains. The first four records are in the 18:00–18:14:59 training bucket. The later failure belongs to the next bucket. Domain labels are synthetic identity namespaces, not a claim that the lab is domain-joined.",
        "question": "How many distinct domain/account pairs did 192.0.2.44 target in the first bucket?",
        "options": [
          "Two, because alice always identifies one account",
          "Three: lab:alice, lab:bob, and dev:alice",
          "Four, because the repeated alice record creates another identity"
        ],
        "answer": 1,
        "explanation": "The repeated lab:alice event increases the failure count but not the distinct-identity count. dev:alice is a separate domain/account pair."
      },
      {
        "title": "Scope the window and threshold",
        "body": "The reference query derives event time from the fixture field, excludes empty and local source values, and uses fixed 15-minute buckets. A threshold of three is for this small exercise; the linked repository example uses five and needs local tuning.",
        "question": "What is the matching result for the 18:00 bucket?",
        "options": [
          "Six failures against six accounts",
          "Five failures against four accounts, including loopback",
          "Four failures against three accounts from 192.0.2.44"
        ],
        "answer": 2,
        "explanation": "The loopback record is excluded. The 18:16 record is in the next bucket and has only one distinct account. Only the first four remote failures meet the training threshold."
      },
      {
        "title": "Investigate the hypothesis",
        "body": "Repeated failures across accounts may also come from stale service credentials, mistakes, or approved testing. Security 4625 records do not show which password was attempted.",
        "question": "Which conclusion is supported?",
        "options": [
          "A candidate T1110.003 lead requiring source, service, timing, and authorization checks",
          "Proof that the same password was reused and every account was compromised",
          "Evidence that the local loopback failure originated from 192.0.2.44"
        ],
        "answer": 0,
        "explanation": "The pattern supports an investigation, not proof of password spraying or compromise. Correlate any subsequent logons carefully and retain benign explanations and source-health limitations."
      }
    ],
    "sources": [
      {
        "label": "MITRE · Password Spraying",
        "url": "https://attack.mitre.org/techniques/T1110/003/"
      },
      {
        "label": "Project · Multiple-account failure hunt",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/hunts/mitre-attack/07-multiple-account-failures.spl"
      },
      {
        "label": "Project · Hypothesis-driven hunt playbook",
        "url": "https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/393ed725efadca0c863c409ae0324ed51f1b94b8/docs/mitre-attack/hunt-playbook.md"
      }
    ],
    "fixtureResult": [
      {
        "window_start": "2026-11-11 18:00:00",
        "source_ip": "192.0.2.44",
        "failures": 4,
        "distinct_accounts": 3,
        "accounts": [
          "dev:alice",
          "lab:alice",
          "lab:bob"
        ]
      }
    ]
  }
];
