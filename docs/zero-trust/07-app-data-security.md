# 07 — Application, Workload and Data Protection

## Splunk Enterprise: resource-based controls

1. List all resources: Splunk Web (`8000`), receiver (`9997`), internal management listener (`8089`, not opened remotely), saved searches, dashboards, indexes and credentials.
2. Verify Splunk service runs as its designated, non-root identity.
3. Keep SSL/TLS certificates in private directories; verify hostnames and CAs. Do not copy private keys into GitHub.
4. Inspect the effective Splunk app and role configuration before applying changes; directory groups must not silently escalate privileges.
5. Limit each analyst to only the indexes/search capabilities necessary. Rely on actual `authorize.conf` and role tests, not source examples alone.
6. Define retention and deletion for `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, `lab`; avoid keeping raw secrets.
7. Restrict configuration editing and production log exports to designated administrators.
8. Document dependencies and risk of Splunk/IdM vendor upgrades before changing settings.

## Read-only verification (RHEL-SPLUNK01)

```bash
sudo systemctl status Splunkd.service --no-pager -l
sudo systemctl show Splunkd.service -p User -p Group
sudo ss -lntp
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool authorize list role_lab_hunter --debug
sudo -u splunk /opt/splunk/bin/splunk btool indexes list --debug
```

**Command overview:** Confirms Splunk process status/identity, listeners, configuration validity, analyst permissions, and index settings. Verify no overly permissive inherited capability or wildcard `srchIndexesAllowed`.

## Sensitive event handling

Some Windows and PowerShell events contain usernames, commands and environment variables, including potential secrets. **Do not** send raw log files to public GitHub or unapproved cloud/AI tools. Use the project's [redaction appendix](../appendices/06-password-redaction-before-indexing.md) as a documented demonstration, not a blanket guarantee that every sensitive field is removed.

## Beyond static RBAC: target design only

A more complete Zero Trust deployment would enforce **per-session** authenticated identity, device health, purpose/time constraints, re-evaluation and restricted resource access through a supported policy enforcement point and centrally managed decision logic. No such dynamic PEP/PDP is deployed by these files.

**Evidence:** signed source/CA verification, least-privilege role denial, retention documentation, version inventory and approved change record.
