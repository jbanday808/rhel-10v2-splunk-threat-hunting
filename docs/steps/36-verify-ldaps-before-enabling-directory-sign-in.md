**Step 36 — Verify LDAPS before enabling directory sign-in**

Run these tests on **RHEL-SPLUNK01** (`172.25.250.10`), with FreeIPA at `idm01.lab.test` (`172.25.250.30`). Do not enable Splunk LDAP sign-in until the secure connection, service-account lookup, group membership, and test-user authentication all work.

### 36.1 — Verify the LDAPS certificate and hostname

Run the TLS check as the Splunk service user:

```bash
sudo -u splunk openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test \
  -verify_return_error </dev/null
```

**Verified in this lab:** `Connecting to 172.25.250.30`, `Verification: OK`, `Verified peername: idm01.lab.test`, `TLSv1.3`, and `Verify return code: 0 (ok)`. The certificate is signed by the FreeIPA CA (`O=LAB.TEST, CN=Certificate Authority`). If verification fails, correct DNS, certificates, or server identity before testing credentials; **do not disable certificate verification**.

### 36.2 — Verify the Splunk lookup account can bind

```bash
sudo -u splunk env \
  LDAPTLS_CACERT=/opt/splunk/etc/auth/ldap/idm-ca.pem \
  LDAPTLS_REQCERT=demand \
  ldapwhoami -x \
  -H ldaps://idm01.lab.test:636 \
  -D 'uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test' \
  -W
```

Enter the **`splunk-bind` system-account password** at the prompt. A successful bind returns:

```text
dn: uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test
```

**Verified in this lab:** The lookup account authenticated successfully. Earlier `ldap_bind: Invalid credentials (49)` responses for `splunk-bind` were resolved before this successful test. Use the correct service-account password; do not substitute the IdM `admin` or Directory Manager password.

### 36.3 — Verify user and group searches

With the `splunk-bind` password, verify the exact attributes Splunk will query:

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

**Verified output (abridged):**

```text
dn: uid=hunter01,cn=users,cn=accounts,dc=lab,dc=test
uid: hunter01
cn: Lab Hunter

dn: cn=splunk-hunters,cn=groups,cn=accounts,dc=lab,dc=test
cn: splunk-hunters
member: uid=hunter01,cn=users,cn=accounts,dc=lab,dc=test

dn: cn=splunk-admins,cn=groups,cn=accounts,dc=lab,dc=test
cn: splunk-admins
member: uid=splunkadmin01,cn=users,cn=accounts,dc=lab,dc=test
```

A command exiting successfully with **no matching entries** does **not** verify the requested users or groups. Check both entries and full member DNs.

### 36.4 — Verify the hunter user password over LDAPS

```bash
sudo -u splunk env \
  LDAPTLS_CACERT=/opt/splunk/etc/auth/ldap/idm-ca.pem \
  LDAPTLS_REQCERT=demand \
  ldapwhoami -x -H ldaps://idm01.lab.test:636 \
  -D 'uid=hunter01,cn=users,cn=accounts,dc=lab,dc=test' \
  -W
```

Enter **hunter01's final password**, not the `splunk-bind` password.

**Observed problem:** Repeated hunter authentication attempts returned:

```text
Enter LDAP Password:
ldap_bind: Invalid credentials (49)
```

**Important distinction:** The successful `splunk-bind` bind and directory searches prove the **service account** can look up user and group entries. They do **not** prove that `hunter01` can authenticate. Error `49` at this point relates to the **hunter user's bind credentials/account state**, not certificate trust or search permissions.

### 36.5 — Troubleshoot `Invalid credentials (49)` for hunter01

One common cause in this lab is that a newly created user is still using an administrator-assigned **temporary password** or has not completed the required first password change. A mistyped password or account lockout may also cause an authentication failure. The captured terminal output does **not** show the exact password-reset/change commands that eventually resolved the issue, so use the following recovery procedure **when needed**, rather than treating it as an observed command transcript.

**On RHEL-IDM01 (the FreeIPA server):**

Authenticate as the IdM administrator and reset the hunter's temporary password:

```bash
kinit admin@LAB.TEST
ipa passwd hunter01
```

Set a strong **temporary** password at the prompt. Then obtain a Kerberos ticket as the hunter, completing the required password-change prompts:

```bash
kdestroy
kinit hunter01@LAB.TEST
klist
```

If prompted that the password is expired, enter the temporary password and choose a **new final password**. Verify that `klist` shows `Default principal: hunter01@LAB.TEST`. Keep the final password private.

**Back on RHEL-SPLUNK01:** Rerun the `ldapwhoami` command in **36.4** and enter the **final hunter01 password**. Do not disable TLS verification to work around error `49`. If it persists, check `ipa user-status hunter01` on IdM for potential lockout and confirm the account/password state before retrying repeatedly.

**Final verified result from the shared Splunk session:**

```text
Enter LDAP Password:
dn: uid=hunter01,cn=users,cn=accounts,dc=lab,dc=test
```

This confirms that **hunter01's LDAPS password bind ultimately succeeded**. It does not, by itself, prove that the other test users (`splunkadmin01` and `unmapped01`) have completed their initial password changes; verify those separately when needed.

### 36.6 — Commands and readiness summary

| Test | Observed result |
| --- | --- |
| TLS certificate chain and hostname | **Passed:** `Verify return code: 0 (ok)` |
| LDAPS port | **Passed:** `636` on `idm01.lab.test` |
| Service-account password bind | **Passed:** `splunk-bind` returned its DN |
| User search | **Passed:** `hunter01` returned with `uid` and `cn` |
| Group search | **Passed:** both Splunk groups returned with their expected `member` DNs |
| Hunter's initial LDAPS bind | **Failed:** `ldap_bind: Invalid credentials (49)` |
| Hunter's final LDAPS bind | **Passed:** `uid=hunter01,cn=users,cn=accounts,dc=lab,dc=test` |

**Command overview:** `openssl s_client` verifies the encrypted connection; `-CAfile` selects the trusted CA; `-verify_hostname` checks server identity; `LDAPTLS_CACERT` and `LDAPTLS_REQCERT=demand` enforce certificate trust for LDAP tools; `ldapsearch` checks user/group visibility; `ldapwhoami` tests a password bind; `-x` selects simple authentication; `-H` selects the LDAPS endpoint; `-D` supplies the full LDAP bind DN; `-W` prompts securely for a password; `-b` sets the search base; `ipa passwd` resets a user password; `kinit` and `klist` validate Kerberos login.

**Summary:** LDAPS security, the `splunk-bind` lookup account, the two Splunk access groups, and the hunter's final password are now **verified**. These checks establish readiness to **configure** Splunk LDAP sign-in, but they do not yet prove that a login to Splunk Web succeeds.

---
