**Step 38 — Create the LDAP strategy in Splunk Web**

Steps 36 and 37 verify the IdM connection, the lookup account, and Splunk's certificate settings. In this step, you enter those same details in Splunk Web. Keep a local Splunk `admin` session open until directory sign-in has been tested in the later steps.

### 1. Restart Splunk

On **RHEL-SPLUNK01**, run each command separately:

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

**Expected:** The second command returns `active`. If it does not, stop and check `sudo journalctl -u Splunkd -n 50 --no-pager` before changing authentication settings.

**Command overview:** `restart` loads the LDAP client certificate policy from Step 37; `is-active` confirms Splunk is running; `journalctl` shows recent service errors if the restart fails.

### 2. Open the LDAP form

1. Sign in to `https://splunk01.lab.test:8000` with the **local** Splunk `admin` account.
2. Open **Settings → Users and authentication → Authentication Methods**.
3. Select **LDAP**, choose **Configure Splunk to use LDAP**, then click **New**. Labels may differ slightly by Splunk version.

### 3. Enter the server and lookup account

| Field in Splunk Web | Enter or select |
| --- | --- |
| Strategy name | `LAB_IDM_LDAPS` |
| Host | `idm01.lab.test` |
| Port | `636` |
| SSL enabled | Select it for LDAPS. |
| Verify LDAP server TLS certificate | Select it to check the CA chain and the `idm01.lab.test` hostname. |
| Trusted CA certificate path | `/opt/splunk/etc/auth/ldap/idm-ca.pem` |
| Bind DN | `uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test` |
| Bind DN password | Enter the protected `splunk-bind` password and confirm it if prompted. |

The bind account lets Splunk look up users and groups. Use its password, not the IdM `admin` password. Port `636` alone does not enable TLS: check both boxes. The CA path is a file **on RHEL-SPLUNK01**, already checked for readability in Step 37. If the CA field is left blank, this Splunk build can use the CA configured in Splunk's OpenLDAP client file; specifying the path makes this strategy's trust source clear.

### 4. Tell Splunk where to find users

| Field in Splunk Web | Enter or select |
| --- | --- |
| User base DN | `cn=users,cn=accounts,dc=lab,dc=test` |
| User base filter | `(objectClass=person)` |
| User name attribute | `uid` |
| Real name attribute | `cn` |
| Email attribute | Leave blank for these test accounts. |
| Group mapping attribute | `dn` |

### 5. Tell Splunk where to find groups

| Field in Splunk Web | Enter or select |
| --- | --- |
| Group base DN | `cn=groups,cn=accounts,dc=lab,dc=test` |
| Static group search filter | `(|(cn=splunk-hunters)(cn=splunk-admins))` |
| Group name attribute | `cn` |
| Static member attribute | `member` |
| Nested groups | Leave unselected; this lab uses direct group membership. |
| Dynamic group search filter | Leave blank. |
| Dynamic member attribute | Leave blank. |

Enter the full static group filter exactly as shown, without quotation marks or Markdown backticks. It selects the two lab access groups. Step 39 maps each group to a Splunk role.

### 6. Set advanced options and save

Expand **Advanced settings**:

| Field in Splunk Web | Enter or select |
| --- | --- |
| Enable referrals with anonymous bind only | Turn off for this lab. |
| Search request time limit | `15` seconds |
| Network socket timeout | `20` seconds |

Before saving, confirm that **SSL enabled** and **Verify LDAP server TLS certificate** are both checked, the CA path is correct, and the group filter is complete. Re-enter the `splunk-bind` password in **Bind DN Password** and **Confirm password**, then click **Save**. A masked password field does not show whether the value is correct. If your Splunk version presents a separate action to enable the strategy, complete it after saving. Confirm that `LAB_IDM_LDAPS` appears in the strategy list with host `idm01.lab.test`, port `636`, and status **Enabled**.

Splunk checks the connection when it creates a strategy. If Save fails, follow the checks below before changing IdM or disabling certificate verification.

### 7. If Splunk Web will not save the strategy

The banner **“Please check your LDAP configuration or consult splunkd.log for LDAP errors”** is general. The message `Error binding to LDAP. reason="Can't contact LDAP server"` does not, by itself, prove that IdM is down or that the password must be reset. Check each part of the connection before changing it.

**First, check the form:** Keep port `636`; confirm both SSL and certificate verification are selected; enter the CA path and the complete static group filter from the tables above. Then type the **same `splunk-bind` password that works in the terminal** into both password fields. The terminal's password prompt and Splunk Web's password fields are separate entries.

**If Save still fails, run these checks separately on RHEL-SPLUNK01:**

```bash
sudo -u splunk test -r /opt/splunk/etc/auth/ldap/idm-ca.pem && echo 'CA file readable'
```

Expected: `CA file readable`. This confirms that the Splunk service account can read the public IdM CA certificate.

```bash
sudo -u splunk timeout 10 openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test \
  -verify_return_error -brief </dev/null
```

Expected: `Connecting to 172.25.250.30`, `CONNECTION ESTABLISHED`, `Verification: OK`, and `Verified peername: idm01.lab.test`. This checks the connection and certificate, **not** the bind password.

```bash
sudo -u splunk env LDAPCONF=/opt/splunk/etc/openldap/ldap.conf \
  ldapwhoami -x -H ldaps://idm01.lab.test:636 \
  -D 'uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test' -W
```

At the prompt, enter the `splunk-bind` password. Expected:

```text
dn: uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test
```

**Command overview:** `sudo -u splunk` runs the tests as Splunk; `test -r` checks CA file access; `openssl s_client` checks LDAPS and the server certificate; `LDAPCONF` points the LDAP tool to Splunk's client policy; `ldapwhoami` checks the bind account; `-W` prompts for the password without placing it in the command; `timeout 10` stops a stalled TLS test after ten seconds.

| Result | Next action |
| --- | --- |
| CA file is unreadable | Check that the path exists on RHEL-SPLUNK01 and that `splunk` can read the public CA file. |
| TLS test cannot connect or verify the server | Check IdM DNS, TCP `636`, the CA file, and the server certificate name. Keep certificate verification enabled. |
| TLS passes but `ldapwhoami` fails | Check the exact `splunk-bind` password and account state. Do not assume a working TLS handshake also validates the password. |
| All three tests pass but Save fails | Re-enter that tested password in **both** Splunk Web fields and review the checkboxes, CA path, and group filter. Do not reset a password that already works in `ldapwhoami`. |

**Observed resolution in this lab:** All three command-line checks passed, including the bind DN response. Splunk Web still failed to save because a different password had been entered in its form. Entering the correct `splunk-bind` password there saved the strategy. The resulting LDAP strategies page showed `LAB_IDM_LDAPS`, `idm01.lab.test`, port `636`, connection order `1`, and **Enabled**. This confirms that the strategy was created; Step 39 still needs role mapping, and a directory user sign-in remains a separate check.

For a new failed Save, inspect recent **LDAP-specific** messages rather than unrelated forwarder errors:

```bash
sudo tail -n 250 /opt/splunk/var/log/splunk/splunkd.log |
  grep -E 'ScopedLDAPConnection|AdminHandler:AuthenticationHandler' |
  tail -n 20
```

**Command overview:** `tail` reads recent Splunk log lines; `grep` keeps the LDAP connection and authentication messages. The `TcpInputProc ... SSL routines::wrong version number` messages from the Windows forwarder are a separate forwarding issue, not evidence of an LDAP failure. Share only redacted error lines; do not publish raw logs or credentials.

**Keep credentials private:** Enter the lookup password only at the Splunk Web or `ldapwhoami -W` prompt. Do not put it in a command, commit the live `authentication.conf`, encrypted password values, `splunk.secret`, or screenshots showing password fields.

**Summary:** `LAB_IDM_LDAPS` is saved and enabled based on the supplied Splunk Web result. Continue to Step 39 to map the groups to roles; creating the strategy alone does not prove that a directory user can sign in.

References:

- [Splunk Web LDAP Setup Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/use-ldap-as-an-authentication-scheme/configure-ldap-with-splunk-web): This guide explains the form fields, LDAP strategy validation, and group settings.
- [Splunk 10.6.1 authentication.conf reference](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/configuration-file-reference/10.6.1-configuration-file-reference/authentication.conf): This reference explains LDAP certificate verification and the trusted CA path.

---
