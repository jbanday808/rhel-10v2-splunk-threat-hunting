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

Before saving, confirm that **SSL enabled** and **Verify LDAP server TLS certificate** are both checked, the CA path is correct, and the group filter is complete. Click **Save**. If your Splunk version presents a separate action to enable the LDAP strategy, complete it after saving. Confirm that `LAB_IDM_LDAPS` appears in the strategy list. Splunk checks the connection when you create a strategy; if saving fails, review the IdM host and port, CA trust, bind DN and password, and search fields before trying again. Do not turn off certificate verification to make a failed connection pass.

**Keep credentials private:** Enter the lookup password only in Splunk Web. Do not commit the live `authentication.conf`, encrypted password values, `splunk.secret`, or screenshots showing password fields.

**Summary:** The expected result is a saved `LAB_IDM_LDAPS` strategy. Continue to Step 39 to map groups to roles; creating the strategy alone does not confirm that a directory user can sign in.

References:

- [Splunk Web LDAP Setup Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/use-ldap-as-an-authentication-scheme/configure-ldap-with-splunk-web): This guide explains the form fields, LDAP strategy validation, and group settings.
- [Splunk 10.6.1 authentication.conf reference](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/configuration-file-reference/10.6.1-configuration-file-reference/authentication.conf): This reference explains LDAP certificate verification and the trusted CA path.

---
