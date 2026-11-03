**Step 38 — Create the LDAP strategy in Splunk Web**

On **RHEL-SPLUNK01**, restart Splunk to load the LDAP client policy:

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

Sign in to **`https://splunk01.lab.test:8000`** with the local Splunk `admin` account. Open **Settings → Users and authentication → Authentication Methods**, select **LDAP**, choose **Configure Splunk to use LDAP**, and click **New**. Menu wording can vary slightly by installed release.

Enter these settings:

| Splunk setting | Value |
| --- | --- |
| Strategy name | `LAB_IDM_LDAPS` |
| Host | `idm01.lab.test` |
| Port | `636` |
| SSL enabled | Selected |
| Bind DN | `uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test` |
| Bind password | The protected `splunk-bind` password |
| User base DN | `cn=users,cn=accounts,dc=lab,dc=test` |
| User base filter | `(objectClass=person)` |
| User name attribute | `uid` |
| Real name attribute | `cn` |
| Email attribute | Leave blank for these test accounts |
| Group mapping attribute | `dn` |
| Group base DN | `cn=groups,cn=accounts,dc=lab,dc=test` |
| Static group search filter | `(|(cn=splunk-hunters)(cn=splunk-admins))` |
| Group name attribute | `cn` |
| Static member attribute | `member` |
| Nested groups | Not selected; use direct membership |
| Dynamic group search filter | Blank |
| Dynamic member attribute | Blank |
| Anonymous referrals | Disabled |
| Search request time limit | `15` seconds |
| Network socket timeout | `20` seconds |

Save the strategy and complete any separate enable action shown by your release. If saving fails, correct the connection, password, certificate, or search settings before proceeding.

Enter the lookup password through Splunk Web. Keep live `authentication.conf` files, encrypted password strings, `splunk.secret`, and screenshots of password fields outside the project repository.

**Command overview:** `systemctl restart Splunkd` loads the LDAP client policy; `systemctl is-active` confirms Splunk restarted.

**Summary:** Splunk has a named, encrypted connection to the IdM directory.

References:

- [Splunk Web LDAP Setup Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/use-ldap-as-an-authentication-scheme/configure-ldap-with-splunk-web): This guide explains LDAP connection fields, directory attributes, and connection tests in Splunk Web.

---
