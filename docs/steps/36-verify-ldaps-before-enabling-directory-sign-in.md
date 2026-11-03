**Step 36 — Verify LDAPS before enabling directory sign-in**

On **RHEL-SPLUNK01**, verify the directory's certificate chain and hostname as the Splunk service account:

```bash
sudo -u splunk openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test \
  -verify_return_error </dev/null
```

Continue only when the output shows a successful certificate verification, normally `Verify return code: 0 (ok)`.

Test the directory lookup account and inspect the exact attributes Splunk will use:

```bash
sudo -u splunk env \
  LDAPTLS_CACERT=/opt/splunk/etc/auth/ldap/idm-ca.pem \
  LDAPTLS_REQCERT=demand \
  ldapsearch -LLL -x -H ldaps://idm01.lab.test:636 \
  -D 'uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test' -W \
  -b 'cn=users,cn=accounts,dc=lab,dc=test' \
  '(uid=hunter01)' uid cn

sudo -u splunk env \
  LDAPTLS_CACERT=/opt/splunk/etc/auth/ldap/idm-ca.pem \
  LDAPTLS_REQCERT=demand \
  ldapsearch -LLL -x -H ldaps://idm01.lab.test:636 \
  -D 'uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test' -W \
  -b 'cn=groups,cn=accounts,dc=lab,dc=test' \
  '(|(cn=splunk-hunters)(cn=splunk-admins))' cn member
```

Enter the `splunk-bind` password at each prompt. Confirm both groups are returned and that each `member` value contains the expected user's full directory name. A successful command with no returned entries is not a successful lookup test.

Also verify the hunter's final password:

```bash
sudo -u splunk env \
  LDAPTLS_CACERT=/opt/splunk/etc/auth/ldap/idm-ca.pem \
  LDAPTLS_REQCERT=demand \
  ldapwhoami -x -H ldaps://idm01.lab.test:636 \
  -D 'uid=hunter01,cn=users,cn=accounts,dc=lab,dc=test' -W
```

**Command overview:** `openssl s_client` tests the encrypted connection; `-CAfile` selects the trusted CA; `-verify_hostname` checks the server name; `ldapsearch` checks user and group visibility; `-x` uses a password bind; `-H` selects the encrypted directory endpoint; `-D` supplies the account's full directory name; `-W` prompts without putting the password in the command; `-b` chooses the search location; `ldapwhoami` tests a user's password bind.

**Summary:** Certificate checks, lookup permissions, group membership, and the hunter's password work before Splunk authentication is changed.

---
