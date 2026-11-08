# Troubleshoot Splunk forwarding TLS and KV service warnings

This guide explains how to investigate the supplied RHEL Splunk receiver errors and Windows Universal Forwarder configuration. It covers the TLS handshake error on TCP 9997 and the separate KV service startup messages. Follow the steps in order on the identified lab VMs; the repository does not connect to or change them.

**Case status: investigation in progress.** The attached logs and later configuration output do not establish a final cause, prove that the current process loaded the configuration, or prove event delivery. Do not copy raw logs, credentials, private keys, completed backups, or unredacted system details into this public repository.

## 1. What the supplied evidence shows

| Supplied observation | What it shows | What still needs checking |
| --- | --- | --- |
| RHEL reports a listener on TCP 9997 and an enabled `[splunktcp-ssl:9997]` input. | Splunk was listening locally and its input was configured for TLS. | The listener alone does not prove a successful TLS handshake or indexed events. |
| Two `TcpInputProc` messages report `SSL routines::wrong version number` from the Windows lab address. | Those connections did not produce an acceptable TLS handshake at that time. | The sending process, bytes sent, and current condition are not established. Plaintext sent to a TLS port is one possible cause, not a confirmed diagnosis. |
| The Windows forwarder reports version **10.4.0**. Its displayed `lab_tls` settings include `useSSL = true`, `sslVerifyServerCert = true`, `sslVerifyServerName = true`, and the intended host and port. | The later `btool` output shows the effective settings read from configuration files. | The output does not prove when those settings were loaded by the running process or whether certificate validation and forwarding currently succeed. |
| Windows `server.conf` points to the lab CA and uses Splunk's trust store. | The forwarder has a configured CA path. | The file's existence, contents, permissions, certificate chain, and current handshake were not shown. |
| The server logged local KV service connection refusals, then a transition from `UNKNOWN` to `READY`. | The service reported readiness after the earlier messages. | Its current health, any migration state, and whether errors continue must be checked. |
| Warnings mention a duplicate credential, a sidecar capability, optional app imports, disabled collections, and introspection. | These are separate messages with different contexts. | A warning alone does not prove a persistent failure or justify changing permissions, credentials, apps, or database settings. |

The client `outputs.conf` in the repository already has `useSSL = true`; do not add a second copy blindly. The later supplied Windows output shows the active group settings coming from `etc\system\local\outputs.conf`, which can take precedence over the app copy. Check the current `btool` output again before making changes.

Splunk's compatibility matrix lists 10.4.x forwarders as compatible with 10.6.x indexers for event forwarding. Confirm the installed server version and support status separately; compatibility does not prove the connection is healthy.

## 2. Prepare and establish the current state

### Step 01 — Identify the two machines

- **RHEL-SPLUNK01:** the Splunk Enterprise receiver. The lab expects `splunk01.lab.test` and TCP `9997`.
- **WINHUNT01:** the Windows guest running Splunk Universal Forwarder. Run the PowerShell commands in the guest, not on the VMware host.
- The `172.25.250.x` addresses and names in the project are lab examples. Use the actual authorized addresses if yours differ.

Keep a private record of the current time and recent error times. Determine whether the errors are new or are old entries from before a configuration change or restart.

### Step 02 — Check versions and running services

On **RHEL-SPLUNK01**:

```bash
sudo -u splunk /opt/splunk/bin/splunk version
sudo systemctl status Splunkd --no-pager -l
```

**Command overview:** `splunk version` displays the installed server build. `systemctl status` displays the service state and recent systemd messages. **Expected result:** Record the actual server build and confirm the service is running; investigate a failed service before proceeding. These commands do not restart it.

On **WINHUNT01**, open PowerShell as administrator:

```powershell
$UfHome = 'C:\Program Files\SplunkUniversalForwarder'
$SplunkExe = Join-Path $UfHome 'bin\splunk.exe'
& $SplunkExe version
Get-CimInstance Win32_Service -Filter "Name='SplunkForwarder'" |
    Select-Object Name, State, StartName, PathName
```

**Command overview:** The variables locate the installed forwarder. `splunk.exe version` displays its build. `Get-CimInstance` displays the service state, account, and executable path. **Expected result:** The service exists and is running; the supplied example reported UF 10.4.0. If your installation path differs, use the verified path.

### Step 03 — Check when the forwarder started

On **WINHUNT01**:

```powershell
Get-Item -LiteralPath "$UfHome\etc\system\local\outputs.conf", "$UfHome\etc\system\local\server.conf" |
    Select-Object FullName, LastWriteTime
Get-Process -Name splunkd -ErrorAction SilentlyContinue |
    Select-Object Id, StartTime, Path
```

**Command overview:** `Get-Item` shows when the two displayed local configuration files were last saved. `Get-Process` shows the start times of visible `splunkd` processes. **Expected result:** Compare the relevant file times with the service process start. A process started before a recent file edit may need a controlled forwarder restart; timestamps alone do not prove what settings the process loaded. If multiple Splunk instances exist, identify the process using its executable path. Investigate missing files or inaccessible process information.

### Step 04 — Check basic connectivity

On **WINHUNT01**:

```powershell
Resolve-DnsName splunk01.lab.test
Test-NetConnection -ComputerName splunk01.lab.test -Port 9997
```

**Command overview:** `Resolve-DnsName` displays the resolved address. `Test-NetConnection` attempts the TCP connection. **Expected result:** The name resolves to the intended receiver, and `TcpTestSucceeded` is `True`. A TCP test does not validate TLS, a certificate, the Splunk forwarding protocol, or ingestion. Name resolution failure or a closed port should be resolved before certificate troubleshooting.

On **RHEL-SPLUNK01**:

```bash
sudo ss -lntp 'sport = :9997'
```

**Command overview:** `ss -lntp` lists listening TCP sockets and their owning process; the filter selects port 9997. **Expected result:** A Splunk process is listening on the intended interface and port. The earlier supplied output showed a listener, but the current state may differ.

### Step 05 — Check the receiver's effective configuration

On **RHEL-SPLUNK01**:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool inputs list splunktcp --debug
sudo -u splunk /opt/splunk/bin/splunk btool inputs list SSL --debug
```

**Command overview:** `btool` combines configuration files and shows where displayed settings come from; `--debug` includes the source path. **Expected result:** Find `[splunktcp-ssl:9997]` with `disabled = 0` and review `[SSL]` for the server certificate, `requireClientCert`, and allowed TLS versions. The supplied output showed `requireClientCert = false` and TLS 1.2/1.3. Treat all command output as private.

`requireClientCert = false` means this receiver does not require a client certificate. It does **not** turn off TLS or server certificate verification by the forwarder. Do not enable a plaintext receiver or disable verification to bypass this investigation.

## 3. Check the forwarder's configuration and trust

### Step 06 — Inspect all effective output stanzas

On **WINHUNT01**:

```powershell
& $SplunkExe btool outputs list --debug
```

**Command overview:** `btool outputs list --debug` displays the merged forwarding configuration and the source file for each displayed value. **Expected result:** Identify `[tcpout]`, its `defaultGroup`, the matching target-group stanza, each target `server`, and any `[tcpout-server://...]` override. Keep the output private because configuration files can include sensitive values.

For the later supplied output, the relevant settings were:

```ini
[tcpout]
defaultGroup = lab_tls

[tcpout:lab_tls]
server = splunk01.lab.test:9997
useSSL = true
sslVerifyServerCert = true
sslVerifyServerName = true
sslAltNameToCheck = splunk01.lab.test
sslVersions = tls1.2,tls1.3
```

This is an explanatory excerpt, not an instruction to overwrite a file. Compare it with the full current output and the actual receiver name. Settings at a more-specific server stanza can override group settings. A `defaultGroup` can also contain multiple groups; examine each group and any input-specific routing before deciding which connection generated an error. The source file shown by `btool` identifies where to inspect a value; it does not establish the process's loaded state.

### Step 07 — Check the CA configuration

On **WINHUNT01**:

```powershell
& $SplunkExe btool server list sslConfig --debug |
    Select-String -Pattern 'sslRootCAPath','caTrustStore'
$CaPath = Join-Path $UfHome 'etc\auth\lab\ca.pem'
Test-Path -LiteralPath $CaPath -PathType Leaf
```

**Command overview:** The first command shows the effective CA and trust-store settings with their source paths. `Test-Path` checks the example CA file. **Expected result:** The configured path corresponds to an existing, approved PEM CA file. The supplied output pointed to this lab path; if current output points elsewhere, check that actual path instead.

The forwarder's `[sslConfig]` trust settings can affect more than one connection. Do not replace a shared CA bundle or change `caTrustStore` without reviewing its other users. The `sslRootCAPath` setting in `outputs.conf` is deprecated in the documented Splunk versions; prefer the effective `server.conf` setting where applicable.

### Step 08 — Verify the public CA file

If your approved source is the lab's public PEM copy, compare its file hash on RHEL and Windows. Use the actual approved paths in your environment.

On **RHEL-SPLUNK01**:

```bash
sha256sum /home/labadmin/siem-public/ca.pem
```

On **WINHUNT01**:

```powershell
Get-FileHash -LiteralPath $CaPath -Algorithm SHA256 | Select-Object Algorithm, Hash
```

**Command overview:** Both commands calculate a SHA-256 hash of the public CA file. **Expected result:** Identical PEM file bytes produce the same hash. A mismatch requires investigation; different encodings or line endings can also change a file hash. Compare with the trusted source through your approved process. A matching hash alone does not authenticate the original source.

If the CA is missing or wrong, follow [Step 22](../steps/22-transfer-the-windows-configuration.md) to obtain the **public CA certificate** through the approved lab process, confirm its identity, and install it only after reviewing existing trust settings. Never transfer the CA private key or the receiver's certificate bundle containing its private key to the forwarder.

### Step 09 — Review service access to the CA

On **WINHUNT01**:

```powershell
Get-CimInstance Win32_Service -Filter "Name='SplunkForwarder'" |
    Select-Object Name, StartName
(Get-Acl -LiteralPath $CaPath).Access |
    Format-Table IdentityReference, FileSystemRights, AccessControlType, IsInherited -AutoSize
```

**Command overview:** The first command identifies the actual service account. `Get-Acl` displays the CA file's access rules. **Expected result:** Review the service identity, inherited group memberships, and access rules to determine whether the service can read the public CA file. An ACL listing alone does not prove effective access. Follow the approved permissions procedure in [Step 26](../steps/26-deploy-the-forwarder-configuration.md) if a verified permission issue exists; do not grant broad write access.

### Step 10 — Inspect the server certificate

On **RHEL-SPLUNK01**, use the actual `serverCert` path reported by Step 05. For the lab example:

```bash
sudo -u splunk openssl x509 \
  -in /opt/splunk/etc/auth/lab/splunk01.pem \
  -noout -subject -issuer -dates -ext subjectAltName
```

**Command overview:** `openssl x509` reads the certificate in the PEM bundle and displays the subject, issuer, validity dates, and subject alternative names. `-noout` avoids displaying the PEM contents. **Expected result:** The certificate is within its validity period, chains to the intended CA, and includes the hostname used by the forwarder. This command displays certificate metadata; it does not prove the full trust chain or live connection. Never print or share the private key in the bundle.

### Step 11 — Test the TLS handshake from Windows

On **WINHUNT01**, first verify the public CA path and Splunk's bundled OpenSSL command. Then run one authorized test:

```powershell
& $SplunkExe cmd openssl version
'' | & $SplunkExe cmd openssl s_client -connect 'splunk01.lab.test:9997' `
    -servername 'splunk01.lab.test' -CAfile $CaPath `
    -verify_hostname 'splunk01.lab.test' -verify_return_error
```

**Command overview:** `splunk cmd openssl` runs Splunk's OpenSSL utility. `s_client` initiates a TLS handshake to the named receiver; `-CAfile` supplies the public trust anchor, `-servername` sends the intended name, and `-verify_hostname` and `-verify_return_error` request name and certificate validation. The empty pipeline closes standard input after the test.

**Expected result:** Check for a negotiated TLS version and `Verify return code: 0 (ok)`. Certificate, trust, hostname, or protocol errors need separate investigation. This tests a TLS connection from Windows using the selected CA file; it is not the forwarder's own connection and does not prove Splunk-to-Splunk event delivery or every Splunk-specific name check. Closing this diagnostic connection may itself create a receiver log entry. If the bundled command or option is unavailable, use an approved equivalent and document its version.

### Step 12 — Interpret the result

| Result | Next action |
| --- | --- |
| Current btool settings are correct, the CA file is present, and TLS verification succeeds | Avoid editing the existing output solely because of old errors. Check current process state and fresh logs in Steps 15–18. |
| `useSSL` is false or absent for the actual active destination | Review the responsible file and any more-specific override; use the controlled change process in Steps 13–15. In the documented Splunk 10.4 setting, legacy mode uses a client certificate to decide whether to send TLS. |
| CA, chain, hostname, or expiry check fails | Correct the verified trust or certificate issue with the owner and retest. Do not disable verification. |
| TCP connection fails or resolves to the wrong address | Check DNS, network route, receiver service, and the applicable firewall before changing TLS. |
| TLS test succeeds, but new `wrong version number` messages continue | Correlate fresh receiver and forwarder logs and identify other authorized processes or tests connecting to the listener. The source IP alone does not prove which process sent the connection. |

## 4. Make a targeted correction only if a check identifies one

### Step 13 — Back up the file that owns the setting

If a correction is needed, use the source path from the **current** `btool` output. The supplied configuration identified `etc\system\local\outputs.conf`; your environment may differ. Set `$PrivateBackupDir` to an **existing, access-controlled private folder outside the Git checkout and Splunk's configuration tree**.

```powershell
$ConfigPath = Join-Path $UfHome 'etc\system\local\outputs.conf'
$PrivateBackupDir = 'C:\REPLACE_WITH_APPROVED_PRIVATE_FOLDER'
if (!(Test-Path -LiteralPath $ConfigPath -PathType Leaf)) { throw 'Select the existing file identified by btool.' }
if (!(Test-Path -LiteralPath $PrivateBackupDir -PathType Container)) { throw 'Select an existing protected backup folder.' }
$BackupFile = Join-Path $PrivateBackupDir ('outputs-before-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.conf')
if (Test-Path -LiteralPath $BackupFile) { throw 'Choose a new backup filename.' }
Copy-Item -LiteralPath $ConfigPath -Destination $BackupFile -ErrorAction Stop
```

**Command overview:** `Test-Path` checks the source, protected destination, and unused backup name. `Get-Date` creates a timestamped name; `Copy-Item` makes a private backup. **Expected result:** The backup exists before any edit. If another file also needs an approved change, protect that file separately. Review inherited permissions and protect the backup because configuration can contain secrets.

### Step 14 — Edit only the confirmed mismatch

Open the existing local file identified by `btool`:

```powershell
notepad.exe $ConfigPath
```

**Command overview:** `notepad.exe` opens the selected existing file for review. **Expected result:** Only the approved, identified setting is changed and saved; no unrelated output group is removed. Do not edit `default` files, replace the whole file, create duplicate stanzas or keys, or change `defaultGroup` without understanding all destinations.

For this lab's server-authenticated TLS design, the active group should point to the correct receiver and use `useSSL = true`, `sslVerifyServerCert = true`, and `sslVerifyServerName = true`. Its configured name check must match the receiver certificate. Preserve other needed settings such as `useACK` and routes. If the effective settings already match, make **no configuration edit**. If a server-specific stanza overrides the group, resolve the actual override with the configuration owner rather than adding a competing copy.

### Step 15 — Check the edited configuration and restart when needed

On **WINHUNT01**:

```powershell
& $SplunkExe btool check
& $SplunkExe btool outputs list --debug
```

**Command overview:** `btool check` reports configuration problems; `btool outputs list --debug` shows the values and their origins. **Expected result:** No relevant configuration errors, and the intended settings appear for the active target. Resolve any reported problem before restarting. `btool` checks files on disk and does not by itself prove a running process has loaded them.

If an output or trust setting was changed, or the service has not been restarted since a required output change, restart **only the Windows forwarder** during an approved lab window:

```powershell
Restart-Service -Name SplunkForwarder
Get-Service -Name SplunkForwarder | Select-Object Name, Status
```

**Command overview:** `Restart-Service` reloads the forwarder; `Get-Service` checks its state. **Expected result:** `Running`. A brief collection interruption can occur. If it fails to start, inspect the private forwarder log and restore the reviewed backup if necessary. No RHEL Splunk restart is required merely to apply a Windows forwarder change.

### Step 16 — Review fresh logs from both ends

On **WINHUNT01**:

```powershell
Get-Content -LiteralPath "$UfHome\var\log\splunk\splunkd.log" -Tail 200 |
    Select-String -Pattern 'TcpOutputProc|AutoLoadBalanced|SSL|TLS|certificate|ERROR|WARN'
```

On **RHEL-SPLUNK01**:

```bash
sudo tail -n 200 /opt/splunk/var/log/splunk/splunkd.log |
  grep -Ei 'TcpInputProc|wrong version number|SSL|TLS|certificate|ERROR|WARN'
```

**Command overview:** `Get-Content -Tail` and `tail` read recent log lines; `Select-String` and `grep` filter for connection and certificate messages. **Expected result:** Compare timestamps with the restart and test. An older warning does not prove a new failure, and no matching line does not prove successful event delivery. A filter can return no matches. Keep raw output private.

### Step 17 — Check the forwarder's connection status

On **WINHUNT01**:

```powershell
& $SplunkExe list forward-server
```

**Command overview:** `list forward-server` displays configured receiving targets and their connection status. **Expected result:** The intended receiver appears as an active forward if the connection is established. The CLI may require an authorized Splunk login; use an interactive prompt, not a password in a command or shell history. An active connection is useful evidence but does not by itself prove the selected events were indexed.

### Step 18 — Verify actual Windows events in Splunk

On **WINHUNT01**, inspect recent local System events:

```powershell
$Since = (Get-Date).AddMinutes(-15)
Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=$Since} -MaxEvents 5 |
    Select-Object TimeCreated, Id, RecordId, ProviderName
```

**Command overview:** `Get-WinEvent` displays up to five System events from the past 15 minutes. **Expected result:** Record the time and event details privately. If there are no recent events, wait for or create an approved benign lab event before comparing results.

In **Splunk Search & Reporting**, run:

```spl
index=win_system host=WINHUNT01 earliest=-30m
| eval indexed_at=strftime(_indextime,"%Y-%m-%d %H:%M:%S")
| table _time indexed_at host source sourcetype _raw
| head 20
```

**Search overview:** `index` and `host` select the intended Windows System data. `earliest` limits event time. `indexed_at` displays indexing time; `table` and `head` limit the display. **Expected result:** Compare an actual recent Windows event, its time, and record details with a corresponding indexed event after the connection is restored. Account for timezone and search permissions. If a recent event is outside the first 20 results, narrow the search using the locally observed event's details. Do not paste raw events into the public repository.

Repeat for the expected Security, PowerShell, and Sysmon indexes using [Step 27](../steps/27-verify-event-collection.md). A successful TLS test without matching events calls for input, channel permissions, indexing, or search-permission investigation.

### Step 19 — Roll back a bad change

If a change causes a new failure, restore the exact protected backup to its original location using the approved process, restart the **Windows forwarder** if its configuration was restored, and repeat Steps 15–18. Preserve the failed-state evidence privately. Do not delete queues, checkpoints, indexes, certificates, or data as a routine troubleshooting step.

## 5. Investigate the separate KV service and startup warnings

### Step 20 — Check current KV service status

On **RHEL-SPLUNK01**:

```bash
sudo -u splunk /opt/splunk/bin/splunk show kvstore-status
```

**Command overview:** `splunk show kvstore-status` requests the current KV store status. **Expected result:** Review the relevant member and, where shown for the installed version, cohosted KV status and migration status. A `ready` state is useful evidence; compare it with current logs and the feature being used. An authorized Splunk login may be required. Do not put a password in the command.

For Splunk Enterprise 10.6 and later, Splunk documents a cohosted KV store using a storage sidecar. If a migration is in progress or the status is not ready, follow the version-specific vendor guidance and involve the owner before restarting or attempting recovery. The earlier `UNKNOWN` to `READY` message does not prove the current migration or health state.

### Step 21 — Check current errors and storage

On **RHEL-SPLUNK01**:

```bash
sudo tail -n 300 /opt/splunk/var/log/splunk/splunkd.log |
  grep -Ei 'KVService|KVStore|sidecar|postgres|connection refused|ERROR|WARN'
df -h /opt/splunk /splunkdata
df -i /opt/splunk /splunkdata
```

**Command overview:** The first command filters recent Splunk messages; `df -h` checks space and `df -i` checks inode availability. **Expected result:** Determine whether KV-related failures continue after startup and whether the relevant mounted filesystems have capacity. A filter may show unrelated messages or no matches. Verify the actual KV storage location before drawing conclusions. Keep output private.

If KV remains unready, errors repeat, or an upgrade is stuck, follow Splunk's current troubleshooting and migration guidance for the installed version or contact support. Do not delete or clean KV data, grant sidecar privileges, change database settings, or restart an in-progress migration as a first response.

### Step 22 — Classify the other supplied warnings

| Message family | Review | Controlled response |
| --- | --- | --- |
| Credential already exists | Check whether it recurs and whether the associated supported feature fails. | Do not delete or overwrite stored credentials based only on the warning. |
| Sidecar reports missing capability | Check current service health, timestamps, and the vendor-supported feature requirements. | Do not grant `restart_splunkd` or `edit_messages` merely to silence a warning. |
| Enterprise Security app cannot be imported | Check whether that app is installed and actually required for this lab. | Investigate with the app owner or Splunk support if a required app is missing; do not install it solely because of this log line. |
| Collection disabled; creation skipped | Identify the owning app and whether its feature is required. | Do not enable, delete, or recreate collections without an approved reason. |
| `orphaned_collections_cleanup` message | Determine whether cleanup is required and consult the installed version's documentation. | Do not enable cleanup just to remove a warning. |
| Distributed-index introspection not enabled | Check whether the lab uses the feature and whether an actual function is failing. | Do not enable optional features solely to silence the message. |

Record whether each warning is historical, recurring, associated with a reproducible failure, or still unverified. The KV and sidecar messages do not establish the cause of the separate TCP 9997 handshake errors.

### Step 23 — Document the result safely

Record the actual server and forwarder versions, verification time, status, affected group, tests performed, observed outcome, and next action in an approved private record. Publish only sanitized conclusions after review. Never mark the error resolved until a current handshake and matching indexed event have been observed.

## References

- [Splunk 10.4 outputs.conf reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.0-configuration-file-reference/outputs.conf): Explains TLS, verification, and output-stanza precedence for the reported forwarder version.
- [Splunk forwarding configuration guide](https://help.splunk.com/en/splunk-cloud-platform/forward-and-process-data/universal-forwarder-manual/10.4/forward-data/configure-forwarding-with-outputs.conf): Explains configuration files, precedence, and restarting the forwarder after an output change.
- [Splunk TLS testing and troubleshooting](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/secure-splunk-platform-communications-with-transport-layer-security-certificates/test-and-troubleshoot-tls-connections): Describes OpenSSL and forwarder/receiver log checks.
- [Splunk forwarder and indexer compatibility](https://help.splunk.com/en/splunk-enterprise/release-notes-and-updates/compatibility-matrix/splunk-products-version-compatibility/compatibility-between-forwarders-and-splunk-enterprise-indexers): Lists version compatibility; support status is a separate question.
- [Splunk KV store troubleshooting](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/administer-the-app-key-value-store/kv-store-troubleshooting-tools): Explains status checks and troubleshooting.
- [Splunk cohosted KV store upgrade](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/administer-the-app-key-value-store/upgrade-to-a-cohosted-kv-store): Explains the 10.6 cohosted KV service, migration, and version-specific recovery.
