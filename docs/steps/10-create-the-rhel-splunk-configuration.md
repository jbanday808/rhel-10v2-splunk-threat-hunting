**Step 10 — Create the RHEL Splunk configuration**

Create the app information:

```
cat > apps/LAB_SIEM/local/app.conf <<'EOF'
[install]
is_configured = 1

[ui]
is_visible = true
label = Threat Hunting Lab

[launcher]
author = James Banday
version = 1.0.0
description = RHEL and Windows threat hunting with Splunk Enterprise
EOF
```

Create `server.conf`:

```
cat > apps/LAB_SIEM/local/server.conf <<'EOF'
[general]
serverName = splunk01
EOF
```

Create `indexes.conf`:

```
cat > apps/LAB_SIEM/local/indexes.conf <<'EOF'
[win_security]
homePath = /splunkdata/win_security/db
coldPath = /splunkdata/win_security/colddb
thawedPath = /splunkdata/win_security/thaweddb
maxTotalDataSizeMB = 20480
frozenTimePeriodInSecs = 2592000

[win_system]
homePath = /splunkdata/win_system/db
coldPath = /splunkdata/win_system/colddb
thawedPath = /splunkdata/win_system/thaweddb
maxTotalDataSizeMB = 10240
frozenTimePeriodInSecs = 2592000

[powershell]
homePath = /splunkdata/powershell/db
coldPath = /splunkdata/powershell/colddb
thawedPath = /splunkdata/powershell/thaweddb
maxTotalDataSizeMB = 10240
frozenTimePeriodInSecs = 1209600

[sysmon]
homePath = /splunkdata/sysmon/db
coldPath = /splunkdata/sysmon/colddb
thawedPath = /splunkdata/sysmon/thaweddb
maxTotalDataSizeMB = 30720
frozenTimePeriodInSecs = 1209600

[linux]
homePath = /splunkdata/linux/db
coldPath = /splunkdata/linux/colddb
thawedPath = /splunkdata/linux/thaweddb
maxTotalDataSizeMB = 10240
frozenTimePeriodInSecs = 2592000

[lab]
homePath = /splunkdata/lab/db
coldPath = /splunkdata/lab/colddb
thawedPath = /splunkdata/lab/thaweddb
maxTotalDataSizeMB = 5120
frozenTimePeriodInSecs = 604800
EOF
```

**File overview:** These indexes separate Windows security, Windows system/application, PowerShell, Sysmon, Linux, and custom test records.

| Setting                  | Explanation                                     |
| ------------------------ | ----------------------------------------------- |
| `homePath`               | Stores actively used data.                      |
| `coldPath`               | Stores older searchable data.                   |
| `thawedPath`             | Provides a location for restored archived data. |
| `maxTotalDataSizeMB`     | Sets the size limit.                            |
| `frozenTimePeriodInSecs` | Sets the age-based retirement target.           |

A size limit can retire data before the age target. Without archiving, retired buckets are deleted. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.1-configuration-file-reference/indexes.conf?utm_source=chatgpt.com)

Create the server’s `inputs.conf`:

```
cat > apps/LAB_SIEM/local/inputs.conf <<'EOF'
[splunktcp-ssl:9997]
disabled = 0

[SSL]
serverCert = /opt/splunk/etc/auth/lab/splunk01.pem
requireClientCert = false
sslVersions = tls1.2,tls1.3

[monitor:///var/log/siem-lab/linux.log]
disabled = 0
index = linux
sourcetype = syslog
host = splunk01

[monitor:///var/log/siem-lab/events.log]
disabled = 0
index = lab
sourcetype = siem:lab
host = splunk01

[WinEventLog://Security]
disabled = 1

[WinEventLog://System]
disabled = 1

[WinEventLog://Application]
disabled = 1

[WinEventLog://Microsoft-Windows-PowerShell/Operational]
disabled = 1

[WinEventLog://Microsoft-Windows-Sysmon/Operational]
disabled = 1
EOF
```

**File overview:** This receives encrypted records on port `9997` and collects two Linux files. Windows collection takes place on the Windows VM.

Create `props.conf`:

```
cat > apps/LAB_SIEM/local/props.conf <<'EOF'
[siem:lab]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = ^
TIME_FORMAT = %Y-%m-%dT%H:%M:%SZ
MAX_TIMESTAMP_LOOKAHEAD = 20
TZ = UTC
KV_MODE = none
REPORT-lab-fields = lab_fields
EOF
```

**File overview:** This describes the date and layout of custom test entries.

Create `transforms.conf`:

```
cat > apps/LAB_SIEM/local/transforms.conf <<'EOF'
[lab_fields]
REGEX = action=(\S+)\s+result=(\S+)\s+account=(\S+)
FORMAT = action::$1 result::$2 account::$3
EOF
```

**File overview:** This extracts the action, result, and account from the custom entry.

The custom rules apply only to `siem:lab`. The official add-ons interpret Windows and Sysmon records.

Create `web.conf`:

```
cat > apps/LAB_SIEM/local/web.conf <<'EOF'
[settings]
httpport = 8000
enableSplunkWebSSL = true
privKeyPath = /opt/splunk/etc/auth/lab/splunk01.key
serverCert = /opt/splunk/etc/auth/lab/fullchain.pem
sslVersions = tls1.2,tls1.3
EOF
```

**File overview:** This protects browser access with HTTPS.

---
