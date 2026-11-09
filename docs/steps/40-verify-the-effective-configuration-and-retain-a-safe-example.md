**Step 40 — Verify the effective configuration and retain a safe example**

On **RHEL-SPLUNK01**:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
sudo journalctl -u Splunkd -n 30 --no-pager
```

Inspect authentication details locally if needed. Avoid exporting unredacted `btool authentication list --debug` output because it can include the lookup credential.

For documentation, create a **sanitized example**, rather than copying live authentication settings into the project:

```bash
cd "$HOME/rhel-splunk-threat-hunting"
cat > docs/reference/ldap-authentication.conf.example <<'EOF'
# Documentation only. Enter the real bind password through Splunk Web.
[authentication]
authType = LDAP
authSettings = LAB_IDM_LDAPS

[LAB_IDM_LDAPS]
host = idm01.lab.test
port = 636
SSLEnabled = 1
sslVerifyServerCert = true
sslRootCAPath = /opt/splunk/etc/auth/ldap/idm-ca.pem
bindDN = uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test
bindDNpassword = REPLACE_THROUGH_SPLUNK_WEB
userBaseDN = cn=users,cn=accounts,dc=lab,dc=test
userBaseFilter = (objectClass=person)
userNameAttribute = uid
realNameAttribute = cn
groupBaseDN = cn=groups,cn=accounts,dc=lab,dc=test
groupBaseFilter = (|(cn=splunk-hunters)(cn=splunk-admins))
groupNameAttribute = cn
groupMemberAttribute = member
groupMappingAttribute = dn
nestedGroups = 0
anonymous_referrals = 0
timelimit = 15
network_timeout = 20

[roleMap_LAB_IDM_LDAPS]
lab_hunter = splunk-hunters
admin = splunk-admins
EOF

cat > docs/reference/ldap-client.conf.example <<'EOF'
# Documentation only: /opt/splunk/etc/openldap/ldap.conf
TLS_REQCERT demand
TLS_CACERT /opt/splunk/etc/auth/ldap/idm-ca.pem
EOF
```

These examples do not enable sign-in on their own. Do not deploy the placeholder password. The Step 38 Splunk Web form in this lab exposes the LDAP certificate verification and CA path fields shown above; confirm the saved values locally on the installed build without publishing live authentication output.

**Command overview:** `btool check` checks Splunk configuration; `journalctl` shows startup messages; `cat > ... <<'EOF'` creates examples while preserving their text.

**Summary:** Splunk starts with the new settings, and the project contains examples without live credentials.

---
