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
  }
];
