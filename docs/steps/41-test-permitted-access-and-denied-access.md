**Step 41 — Test permitted access and denied access**

Use a private browser window for each account and sign out between tests. Use the short directory usernames, such as `hunter01`, because this configuration uses the `uid` attribute.

| Test | Expected result |
| --- | --- |
| Sign in as `hunter01` with its final IdM password | Sign-in succeeds and the account has `lab_hunter` |
| Open the lab dashboard and search a populated lab index | The hunter can view the dashboard and retrieve lab events |
| Search `index=_internal` as `hunter01` | No protected records are returned |
| Attempt to change users or authentication as `hunter01` | Administrative actions are denied |
| Sign in as `splunkadmin01` | Sign-in succeeds with the Splunk `admin` role |
| Sign in as `unmapped01` | Splunk access is denied because no group grants a role |
| Enter one incorrect password for `hunter01` | Sign-in is denied |
| Sign in with the original local Splunk `admin` | Local recovery access still works |

For the hunter's positive search test, select **Last 24 hours** and run:

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab)
| stats count by index
```

Confirm an administrator can see recent `_internal` records before interpreting the hunter's empty `_internal` search as a valid restriction test.

Test removal of access on **RHEL-IDM01**:

```bash
kinit admin
ipa group-remove-member splunk-hunters --users=hunter01
ipa group-show splunk-hunters --all --raw
kdestroy
```

As the local Splunk administrator, use **Reload authentication configuration** if your release offers it, or restart `Splunkd` on `.10` to clear cached authentication data. Close the hunter's existing browser session and test a **new** login; it should be denied. Membership changes should not be treated as proof that every existing session was immediately revoked.

Restore membership on **RHEL-IDM01**, refresh authentication again, and repeat the hunter's login:

```bash
kinit admin
ipa group-add-member splunk-hunters --users=hunter01
kdestroy
```

After all checks, disable the unmapped test account on **RHEL-IDM01**:

```bash
kinit admin
ipa user-disable unmapped01
kdestroy
```

**Command overview:** `group-remove-member` removes group-based access; `group-add-member` restores it; `user-disable` disables the unused test identity. The search counts events in the indexes the hunter is permitted to search.

**Summary:** Authorized users can sign in, restricted accounts cannot administer Splunk, and group removal blocks a new login after authentication data is refreshed.

---
