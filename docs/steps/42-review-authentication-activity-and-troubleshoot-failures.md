**Step 42 — Review authentication activity and troubleshoot failures**

Use the local Splunk administrator account for the searches in this step. The `lab_hunter` role from Step 39 does not have access to the `_audit` or `_internal` indexes.

### 1. Review login attempts in Splunk Web

Open **Search & Reporting** on **RHEL-SPLUNK01**, select **Last 7 days**, and run:

```spl
index=_audit action="login attempt"
| table _time user action info host
| sort - _time
```

`_audit` stores Splunk audit events. `action="login attempt"` selects login attempts; `table` shows the relevant fields, and `sort - _time` puts the newest event first. Review `info` and the underlying event before deciding whether a login succeeded or failed.

### 2. If Splunk says “No results found”

1. Confirm you are signed in as a **Splunk administrator**, not `hunter01`. Select **Last 7 days** in the time picker and run the query above again. Remove any older `earliest=-30m` text from the search: an inline time limit can narrow the search even when the picker shows a longer period. If there is no recent sign-in, make one attempt in a separate private browser window, then retry from the administrator session.
2. Check whether the administrator can see any audit events during the selected period:

   ```spl
   index=_audit
   | stats count AS audit_events
   ```

3. If `audit_events` is greater than zero, inspect the action values actually present:

   ```spl
   index=_audit
   | stats count by action
   | sort - count
   ```

   If login events use a different format or the displayed fields are empty, inspect a few original events before changing the search:

   ```spl
   index=_audit
   | table _time action user info host _raw
   | sort - _time
   | head 20
   ```

   To look for the raw phrase without relying on the extracted `action` field, you can also run:

   ```spl
   index=_audit "login attempt"
   ```

4. If `audit_events` is zero as an administrator, try **All time** briefly and check that the Splunk server clock and search time zone are correct. Then investigate audit indexing locally. On **RHEL-SPLUNK01**, `/opt/splunk/var/log/splunk/audit.log` can help confirm whether audit events are being written. Treat raw logs as private; do not upload them to GitHub. Do not treat a zero count from a restricted account as proof that audit logging is broken.

The earlier `action=login earliest=-30m` search can miss these events because the action value is `login attempt` in the documented audit search and the 30-minute limit narrows the window. The revised query is a starting point; verify it against events in your own Splunk build.

### 3. Check LDAP messages separately

As the Splunk administrator, keep **Last 7 days** selected and run:

```spl
index=_internal source=*splunkd.log* (LDAP OR ScopedLDAPConnection OR AuthenticationManager)
| table _time log_level component _raw
| sort - _time
```

If there are no matching messages, first check whether the administrator can search `splunkd.log` at all:

```spl
index=_internal source=*splunkd.log*
| stats count AS splunkd_events
```

No recent LDAP errors can be normal after a successful configuration. If `splunkd_events` is zero, check the selected time range and `_internal` access before diagnosing LDAP. A `TcpInputProc` “wrong version number” message from the Windows forwarder on port `9997` concerns the forwarding TLS path; it is not an LDAP bind error on port `636`. A successful LDAP login alone does not prove TLS certificate verification: retain the separate certificate and client-policy checks from Step 38.

### 4. Run directory checks on the correct VM

The following commands belong on **RHEL-IDM01**, the directory server. If your prompt says `labadmin@splunk01`, you are still on the Splunk client. Open the **RHEL-IDM01 VM console** and sign in as root or a sudo-enabled account. Alternatively, connect from **RHEL-SPLUNK01**:

```bash
ssh labadmin@idm01.lab.test
```

Use the Linux password configured for `labadmin` on RHEL-IDM01; it is separate from the Splunk Web and IdM `admin` credentials. `sudo` may prompt for that same Linux password. If DNS resolution fails, use `ssh labadmin@172.25.250.30` or the VM console.

On the machine where you intend to run service commands, verify the host:

```bash
hostnamectl --static
hostname -f
```

Expected static host: `idm01.lab.test`. If it differs, stop and connect to the directory VM. The `hostname -f` check also depends on name resolution and can fail if DNS is broken. Then check IdM and its LDAPS listener:

```bash
sudo ipactl status
sudo ss -lntp 'sport = :636'
sudo systemctl list-units --all 'dirsrv@*.service'
```

Expected: IdM services report `RUNNING`, and the local listener includes TCP port `636`. If `ipactl` is missing on the verified IdM VM, review the package and installation checks in Steps 32 and 33.

Find the exact Directory Server unit name in the last command's output. For a `LAB.TEST` realm it is typically `dirsrv@LAB-TEST.service`; if your output differs, use the name shown there:

```bash
sudo journalctl --since '30 minutes ago' --no-pager -u dirsrv@LAB-TEST.service
```

If the correct unit has no entries in that 30-minute window, use `sudo journalctl -u dirsrv@LAB-TEST.service -n 50 --no-pager` to inspect its last 50 entries. No recent messages alone does not mean the directory service has failed.

On **RHEL-SPLUNK01**, check the client connection instead of expecting a local LDAP service:

```bash
hostname -f
getent ahostsv4 idm01.lab.test
sudo -u splunk timeout 10 openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test \
  -verify_return_error -brief </dev/null
```

The connection test should report **Verification: OK** and **Verified peername: idm01.lab.test**. Do not enter or publish the bind password in this test.

| What you see | Meaning and next check |
| --- | --- |
| `sudo: ipactl: command not found` on `splunk01` | You ran a directory-server command on the Splunk client. Switch to the `idm01` console; do not install IdM on the Splunk VM. |
| No listener appears for TCP `636` on `splunk01` | Expected: the Splunk VM connects to LDAPS; `idm01` listens for it. Run the listener check on `idm01`. |
| `Failed to add filter for units: No data available` on `splunk01` | The filter found no matching local journal data; this does not establish the state of `idm01`. List the units on `idm01` and use its exact `dirsrv@...service` name. |
| Cannot resolve `idm01.lab.test` | Check IdM DNS, the Splunk VM's resolver, and the directory VM's `.30` address. |
| Connection to TCP `636` times out | Check the VM network, IdM firewall, and listener on `idm01`. |
| Certificate verification fails | Check the CA file, certificate validity, host name, and clocks without disabling verification. |
| Bind fails despite a verified TLS connection | Check the exact `uid=splunk-bind,...` DN and current password using the private Step 38 bind test. |
| Lookup returns no users or groups | Check base DNs, filters, attributes, and bind-account permissions. |
| Password works elsewhere but Splunk denies access | Check required password changes, mapped group membership, role mapping, and duplicate local usernames. |
| Hunter receives too much access | Check `splunk-admins` membership, multiple mapped roles, and role inheritance. |
| Group change appears delayed | Refresh cached directory data and test in a new browser session. |

**Command overview:** `ssh` connects to the directory VM; `hostnamectl --static` identifies the configured host; `hostname -f` checks its resolved name; `ipactl status` checks IdM services; `ss` checks the local LDAPS listener; `systemctl list-units` finds the installed service name; `journalctl` reads that service's recent messages. On the Splunk VM, `getent` checks name resolution and `openssl s_client` tests the remote server's TLS certificate and host name.

**Summary:** Search audit events as an administrator, expand the time range when results are empty, and run server-side IdM commands on `idm01` while testing the remote LDAPS connection from `splunk01`.

References:

- [Splunk Search the Audit Log](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/audit-activity-in-splunk-enterprise/search-the-audit-log): This guide shows how to find login attempts in `_audit`.
- [Splunk Time Modifiers](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/10.6/time-format-variables-and-modifiers/time-modifiers): This guide explains how search time limits interact with the time picker.
- [Red Hat Identity Management service status](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/accessing_identity_management_services/viewing-starting-and-stopping-the-identity-management-services): This guide identifies the IdM server services and the `ipactl status` check.

---
