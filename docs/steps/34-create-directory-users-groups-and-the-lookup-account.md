**Step 34 — Create directory users, groups, and the lookup account**

On **RHEL-IDM01**, create dedicated application groups and three test users:

```bash
kinit admin
ipa group-add splunk-hunters --nonposix --desc='Splunk lab threat hunters'
ipa group-add splunk-admins --nonposix --desc='Splunk lab administrators'

ipa user-add hunter01 --first=Lab --last=Hunter --password
ipa user-add splunkadmin01 --first=Splunk --last=Administrator --password
ipa user-add unmapped01 --first=Unmapped --last=Test --password

ipa group-add-member splunk-hunters --users=hunter01
ipa group-add-member splunk-admins --users=splunkadmin01
```

Enter temporary passwords at the prompts. Complete the required first-password change for **each** user before testing Splunk:

```bash
kdestroy
kinit hunter01
kdestroy
kinit splunkadmin01
kdestroy
kinit unmapped01
kdestroy
kinit admin
```

Each `kinit` prompts for that user's temporary password and then a new password. Splunk's LDAP login page is not the place to complete this first-password change. Use the final passwords for later login tests.

RHEL 10.2 introduces the IdM system-account commands. Create the dedicated directory lookup account:

```bash
ipa sysaccount-add splunk-bind --password
ipa sysaccount-show splunk-bind --all --raw
```

Store the password securely. Confirm its directory name is:

```text
uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test
```

If `sysaccount-add` is unavailable, confirm the installed RHEL release and IdM packages before continuing. This procedure requires the RHEL 10.2 system-account feature.

Grant this account only the additional directory-read permissions needed for user and group lookups:

```bash
ipa permission-add 'Splunk Read Users' --type=user \
  --right=read --right=search --right=compare \
  --attrs=uid --attrs=cn --attrs=objectclass

ipa permission-add 'Splunk Read Groups' --type=group \
  --right=read --right=search --right=compare \
  --attrs=cn --attrs=member --attrs=objectclass

ipa privilege-add 'Splunk Directory Lookup'
ipa privilege-add-permission 'Splunk Directory Lookup' \
  --permissions='Splunk Read Users' --permissions='Splunk Read Groups'

ipa role-add 'Splunk Directory Reader'
ipa role-add-privilege 'Splunk Directory Reader' \
  --privileges='Splunk Directory Lookup'
ipa role-add-member 'Splunk Directory Reader' --sysaccounts=splunk-bind

ipa group-show splunk-hunters --all --raw
ipa group-show splunk-admins --all --raw
ipa role-show 'Splunk Directory Reader'
kdestroy
```

Do not add `splunk-bind` to the IdM `admins` group, a password-reset role, or either Splunk access group. The directory lookup role controls directory reads; the two application groups control access to Splunk. Existing IdM default read permissions may also apply.

**Command overview:** `ipa user-add` creates a directory user; `--password` prompts for a password; `ipa group-add` creates an application group; `--nonposix` avoids creating a Linux group ID; `group-add-member` assigns membership; `sysaccount-add` creates the lookup account; `permission-add`, `privilege-add`, and `role-add` grant selected read access; `kdestroy` clears the current authentication ticket.

**Summary:** Hunters and administrators have separate groups, and Splunk has a dedicated account for reading directory entries.

References:

- [Red Hat IdM Groups Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_idm_users_groups_hosts_and_access_control_rules/managing-user-groups-in-idm-cli): This guide explains group creation and membership management.
- [Red Hat IdM System Accounts Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_idm_users_groups_hosts_and_access_control_rules/configuring-a-system-account-in-idm-to-change-user-passwords-without-requiring-a-reset): This guide documents the RHEL 10.2 system-account creation commands; this lab grants directory reads only.
- [FreeIPA System Accounts Design](https://freeipa.readthedocs.io/en/latest/designs/sysaccounts.html): This reference explains system-account directory names and LDAP binding.
- [Red Hat IdM Permissions Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_idm_users_groups_hosts_and_access_control_rules/managing-role-based-access-controls-in-idm-using-the-cli): This guide explains permissions, privileges, and roles.

---
