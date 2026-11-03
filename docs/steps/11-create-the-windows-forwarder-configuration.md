**Step 11 — Create the Windows forwarder configuration**

Still on **RHEL**:

```
cat > apps/LAB_UF_WINDOWS/local/app.conf <<'EOF'
[install]
is_configured = 1

[ui]
is_visible = false

[launcher]
version = 1.0.0
description = Windows event collection and protected forwarding
EOF
```

Create Windows `inputs.conf`:

```
cat > apps/LAB_UF_WINDOWS/local/inputs.conf <<'EOF'
[default]
host = WINHUNT01

[WinEventLog://Security]
disabled = 0
index = win_security
renderXml = true
start_from = oldest
current_only = 0

[WinEventLog://System]
disabled = 0
index = win_system
renderXml = true
start_from = oldest
current_only = 0

[WinEventLog://Application]
disabled = 0
index = win_system
renderXml = true
start_from = oldest
current_only = 0

[WinEventLog://Microsoft-Windows-PowerShell/Operational]
disabled = 0
index = powershell
renderXml = true
start_from = oldest
current_only = 0

[WinEventLog://Microsoft-Windows-Sysmon/Operational]
disabled = 0
index = sysmon
sourcetype = XmlWinEventLog:Microsoft-Windows-Sysmon/Operational
renderXml = true
start_from = oldest
current_only = 0
EOF
```

**File overview:** This chooses the Windows channels to collect.

The `oldest` and `current_only = 0` settings read retained existing records and continue with new records. Monitor the initial backlog against your licensed allowance. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/inputs.conf?utm_source=chatgpt.com)

Create `outputs.conf`:

```
cat > apps/LAB_UF_WINDOWS/local/outputs.conf <<'EOF'
[tcpout]
defaultGroup = lab_tls

[tcpout:lab_tls]
server = splunk01.lab.test:9997
useACK = true
useSSL = true
sslVerifyServerCert = true
sslVerifyServerName = true
sslAltNameToCheck = splunk01.lab.test
sslVersions = tls1.2,tls1.3
EOF
```

**File overview:** This sends records to RHEL and verifies the receiving server’s identity.

Create Windows `server.conf`:

```
cat > apps/LAB_UF_WINDOWS/local/server.conf <<'EOF'
[sslConfig]
sslRootCAPath = C:\Program Files\SplunkUniversalForwarder\etc\auth\lab\ca.pem
caTrustStore = splunk
EOF
```

**File overview:** This identifies the public CA certificate trusted by the forwarder.

This setup verifies the receiving server without requiring a client certificate. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/outputs.conf?utm_source=chatgpt.com)

---
