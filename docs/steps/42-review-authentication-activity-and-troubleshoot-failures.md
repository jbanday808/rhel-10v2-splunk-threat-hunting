**Step 42 — Review authentication activity and troubleshoot failures**

As a **Splunk administrator**, search recent authentication audit activity:

```spl
index=_audit action="login attempt"
| table _time user action info host
| sort - _time
```

Review LDAP connection messages separately:

```spl
index=_internal source=*splunkd.log* earliest=-30m
(LDAP OR ScopedLDAPConnection OR AuthenticationManager)
| table _time log_level component _raw
| sort - _time
```

These are starting searches. Confirm the actual fields and messages in your installed build before creating a scheduled detection. An LDAP message alone does not prove the connection was encrypted; retain the successful certificate test and verified client policy as separate evidence.

| Problem | Check first |
| --- | --- |
| Cannot find `idm01.lab.test` | IdM DNS service, the Splunk VM resolver, and its `.30` address |
| LDAPS connection times out | VMnet8 connection, directory firewall zone, and TCP `636` listener |
| Certificate verification fails | IdM CA fingerprint, trusted certificate path, certificate dates, hostname, and system time |
| Lookup account cannot bind | Exact `uid=splunk-bind,...` name and its current password |
| Lookup returns no users or groups | Base names, filters, selected attributes, and lookup-account permissions |
| User's password works elsewhere but Splunk denies access | Required password change, group membership, role mapping, and duplicate local username |
| Hunter receives too much access | Membership in `splunk-admins`, multiple mapped roles, and role inheritance |
| Group change appears delayed | Cached directory data and an existing browser session |

On **RHEL-IDM01**, inspect service health and the directory listener:

```bash
sudo ipactl status
sudo ss -lntp 'sport = :636'
sudo journalctl --since '30 minutes ago' --no-pager -u 'dirsrv@*'
```

**Command overview:** `ipactl status` checks IdM services; `ss` confirms a service is listening on TCP `636`; `journalctl` shows recent Directory Server messages. The Splunk searches show login outcomes and directory connection errors.

**Summary:** You can investigate failed logins without weakening certificate checks or granting extra administrator access.

---
