**Step 37 — Require certificate verification in Splunk's LDAP client**

Splunk uses its own LDAP client settings at **`/opt/splunk/etc/openldap/ldap.conf`**. Changing only RHEL's `/etc/openldap/ldap.conf` does not configure Splunk's client.

On **RHEL-SPLUNK01**:

```bash
sudo cp -a /opt/splunk/etc/openldap/ldap.conf \
  "/opt/splunk/etc/openldap/ldap.conf.before-ldap-$(date -u +%Y%m%dT%H%M%SZ)"
sudoedit /opt/splunk/etc/openldap/ldap.conf
```

Preserve unrelated settings. Replace any existing active `TLS_REQCERT` and `TLS_CACERT` directives so there is only one of each:

```text
TLS_REQCERT demand
TLS_CACERT /opt/splunk/etc/auth/ldap/idm-ca.pem
```

These settings require certificate validation and supply the trusted IdM CA. Avoid `TLS_REQCERT never`. Splunk's `server.conf` settings for browser or forwarding connections do not replace these LDAP settings.

Some updated Splunk builds also document **LDAP-strategy** settings named `sslVerifyServerCert` and `sslRootCAPath`. If your installed `$SPLUNK_HOME/etc/system/README/authentication.conf.spec` lists them under **LDAP settings**, set `sslVerifyServerCert = true` and `sslRootCAPath = /opt/splunk/etc/auth/ldap/idm-ca.pem` in `[LAB_IDM_LDAPS]` as well. Do not assume those settings apply to LDAP merely because they appear under SAML or another authentication section. The `ldap.conf` policy above remains required by this guide.

**Command overview:** `cp -a` preserves the previous client settings; `sudoedit` updates the file; `TLS_REQCERT demand` requires a trusted directory certificate; `TLS_CACERT` identifies its signing certificate.

**Summary:** Splunk must validate the directory server instead of merely encrypting an unverified connection.

References:

- [Splunk LDAP Configuration Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.0/perform-advanced-configuration-of-ldap-authentication-in-splunk-enterprise/configure-ldap-using-configuration-files): This guide explains Splunk's LDAP client file location and certificate-verification directives.
- [Splunk Authentication Configuration Reference](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/configuration-file-reference/10.6.1-configuration-file-reference/authentication.conf): This reference describes the authentication settings supported by that Splunk release; use the reference matching your installed build.

---
