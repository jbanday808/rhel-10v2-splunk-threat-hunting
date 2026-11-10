**Step 37 — Require certificate verification in Splunk's LDAP client**

**Objective:** Configure Splunk Enterprise to trust **FreeIPA's certificate authority (CA)** and reject untrusted LDAP certificates before enabling directory sign-in.

**Run every command in this step on RHEL-SPLUNK01 (`splunk01.lab.test`, `172.25.250.10`).** The directory server is `idm01.lab.test` (`172.25.250.30`), using **LDAPS on TCP port 636**.

> **Important:** Splunk includes its own LDAP client configuration at `/opt/splunk/etc/openldap/ldap.conf`. Editing only RHEL's `/etc/openldap/ldap.conf` does not update this Splunk client configuration. The earlier setting `TLS_REQCERT never` disabled certificate verification and must be removed from the **active configuration**.

### 37.1 — Confirm the CA certificate is installed

On **RHEL-SPLUNK01**:

```bash
hostname -f
sudo -u splunk test -r /opt/splunk/etc/auth/ldap/idm-ca.pem && echo "FreeIPA CA certificate is readable by Splunk"
sudo ls -l /opt/splunk/etc/auth/ldap/idm-ca.pem
sudo openssl x509 -in /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -noout -fingerprint -sha256
```

**Expected:** The certificate exists and is readable by the `splunk` service account. The SHA-256 CA fingerprint previously verified directly on IdM was:

```text
A6:95:5A:83:36:8B:01:E4:42:1F:51:0E:72:84:39:8A:8E:E1:6D:A6:11:CD:BB:A9:13:84:DF:53:B8:B2:48:DE
```

Do not proceed if the certificate is missing or its fingerprint differs. Complete Steps 35–36 first.

### 37.2 — Back up the current Splunk LDAP configuration

Create a **timestamped backup before editing**, so the previous configuration can be restored:

```bash
sudo cp -a /opt/splunk/etc/openldap/ldap.conf \
  "/opt/splunk/etc/openldap/ldap.conf.before-ldap-$(date -u +%Y%m%dT%H%M%SZ)"
```

A separate, simple backup may also be used:

```bash
sudo cp -a /opt/splunk/etc/openldap/ldap.conf \
  /opt/splunk/etc/openldap/ldap.conf.bak
```

**Observed in this lab:** Both backup commands completed without errors. Use the timestamped backup for version-specific recovery; avoid overwriting the `.bak` copy after a known-good baseline is established.

**Command overview:** `sudo` permits an administrator to read the Splunk-owned configuration; `cp -a` preserves file metadata; `date -u` adds a UTC timestamp so backups are easier to distinguish.

### 37.3 — Edit `/opt/splunk/etc/openldap/ldap.conf`

Open the file **on RHEL-SPLUNK01**:

```bash
sudoedit /opt/splunk/etc/openldap/ldap.conf
```

Find the original insecure entries:

```text
ssl start_tls
TLS_REQCERT never
```

For this lab's **direct LDAPS connection on port 636**, comment out the existing `ssl start_tls` directive and replace `TLS_REQCERT never` with `TLS_REQCERT demand`. Add `TLS_CACERT` pointing to the **public IdM CA certificate already copied to Splunk**.

**Complete updated configuration** — use this as the full contents of `/opt/splunk/etc/openldap/ldap.conf` for this lab, preserving the existing TLS 1.2 cipher list:

```ini
#
# LDAP Defaults
# Splunk Enterprise - FreeIPA LDAPS Configuration
#
# Splunk server: splunk01.lab.test (172.25.250.10)
# FreeIPA server: idm01.lab.test (172.25.250.30)
# LDAPS port: 636
# Kerberos realm: LAB.TEST
#
# See ldap.conf(5) for details.
# This file should be world readable but not world writable.
#

# --------------------------------------------------
# 1. LDAP CONNECTION SECURITY
# --------------------------------------------------

# This lab connects using LDAPS on TCP 636, not STARTTLS.
# ssl start_tls

# Require valid and trusted LDAP server certificates.
# Never use TLS_REQCERT never for this lab.
TLS_REQCERT demand

# Trusted public FreeIPA certificate authority.
TLS_CACERT /opt/splunk/etc/auth/ldap/idm-ca.pem

# --------------------------------------------------
# 2. TLS PROTOCOL
# --------------------------------------------------

# Minimum TLS version: TLS 1.2.
# 3.1 = TLS 1.0; 3.2 = TLS 1.1; 3.3 = TLS 1.2
TLS_PROTOCOL_MIN 3.3

# --------------------------------------------------
# 3. TLS 1.2 CIPHER SUITES
# --------------------------------------------------

# Preserve the existing cipher list from the original file.
# TLS 1.3 cipher negotiation is separate.
TLS_CIPHER_SUITE ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256

# --------------------------------------------------
# 4. OPTIONAL CA CERTIFICATE DIRECTORY
# --------------------------------------------------

# Not needed because TLS_CACERT specifies the trusted CA file.
# TLS_CACERTDIR /opt/splunk/etc/openldap/certs

# --------------------------------------------------
# END OF CONFIGURATION
# --------------------------------------------------
```

**Save and exit:** In Vim, press `Esc`, enter `:wq`, and press Enter. With other editors, use their normal Save/Exit controls. Leave **one active occurrence** of each `TLS_REQCERT`, `TLS_CACERT`, and `TLS_PROTOCOL_MIN` setting.

**Why these settings matter:**

| Directive | Purpose |
| --- | --- |
| `# ssl start_tls` | Disables the file's STARTTLS setting for this lab's direct LDAPS connection on port `636`. |
| `TLS_REQCERT demand` | Requires the LDAP server's certificate to be valid and trusted. |
| `TLS_CACERT /opt/splunk/etc/auth/ldap/idm-ca.pem` | Specifies the FreeIPA CA certificate installed in Step 35. |
| `TLS_PROTOCOL_MIN 3.3` | Requires TLS 1.2 or newer. |
| `TLS_CIPHER_SUITE` | Retains the original TLS 1.2 cipher list. |

This file configures **LDAP client certificate verification**. It does not replace Splunk's HTTPS/forwarder settings in `server.conf` or configure users and groups for Splunk sign-in.

### 37.4 — Verify the active LDAP settings

Check the active (noncommented) directives:

```bash
sudo grep -nE '^[[:space:]]*(ssl|TLS_REQCERT|TLS_CACERT|TLS_PROTOCOL_MIN|TLS_CIPHER_SUITE)' \
  /opt/splunk/etc/openldap/ldap.conf
```

**Verified output from this lab** (relevant lines):

```text
24:TLS_REQCERT demand
27:TLS_CACERT /opt/splunk/etc/auth/ldap/idm-ca.pem
39:TLS_PROTOCOL_MIN 3.3
```

Line numbers depend on the file contents, so they may differ on other systems. There should be **no active** `TLS_REQCERT never` or `ssl start_tls` entry for this direct-LDAPS lab setup. The active `TLS_CIPHER_SUITE` line should still be present.

**Command overview:** `grep -nE` shows matching settings and their line numbers; the leading pattern `^[[:space:]]*` matches active directives instead of commented lines.

### 37.5 — Test the LDAP configuration as the Splunk service account

From **RHEL-SPLUNK01**, bind to IdM over TLS using the updated configuration:

```bash
sudo -u splunk env \
  LDAPCONF=/opt/splunk/etc/openldap/ldap.conf \
  ldapwhoami -x \
  -H ldaps://idm01.lab.test:636 \
  -D 'uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test' \
  -W
```

At `Enter LDAP Password:`, enter the **`splunk-bind` system-account password**, not the IdM `admin` or Linux login password. **Do not place live passwords in commands or GitHub.**

**Verified result from 8 November 2026:**

```text
Enter LDAP Password:
dn: uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test
```

This verifies that `splunk` can load the selected LDAP client configuration and authenticate to the IdM server. Step 36 separately verified the LDAPS certificate chain and hostname with `openssl s_client`, plus user/group searches. This successful command-line test does **not** mean Splunk Web LDAP sign-in has been enabled yet.

**Command overview:** `sudo -u splunk` runs as the Splunk service user; `LDAPCONF` points the LDAP tool to this specific client file; `ldapwhoami` tests the LDAP bind; `-x` uses password-based LDAP authentication; `-H` chooses `ldaps://idm01.lab.test:636`; `-D` provides the lookup account DN; `-W` securely requests its password.

### 37.6 — Troubleshoot and recover

| Symptom | Explanation and correction |
| --- | --- |
| `TLS_REQCERT never` is still active | Replace it with `TLS_REQCERT demand`. Do not retain both directives. |
| `ssl start_tls` remains active | Comment it out for this guide's direct-LDAPS/636 setup. |
| `ldap_bind: Invalid credentials (49)` | The bind password or account state is incorrect. Re-check the **`splunk-bind`** password; Step 36 documents the validated bind and password troubleshooting. |
| Certificate trust error | Verify `TLS_CACERT` is correct, that the `splunk` user can read the certificate, and that the certificate and server hostname match. Do not disable verification to make a failed test pass. |
| `Can't contact LDAP server` | Check DNS resolution for `idm01.lab.test`, network connectivity to TCP `636`, and IdM LDAP services. |
| `grep` prints the old policy | Edit the **Splunk-specific** file, not `/etc/openldap/ldap.conf`, save it, and rerun the check. |

**Restore the original configuration only if you need to roll back:** Identify the correct timestamped backup from `37.2`, then restore that backup after reviewing its contents and permissions. Do **not** re-enable `TLS_REQCERT never` as a troubleshooting shortcut.

### 37.7 — Prepare for Step 38

Step 38 restarts Splunk to load its LDAP client policy and creates the `LAB_IDM_LDAPS` authentication strategy in Splunk Web.

If your installed `/opt/splunk/etc/system/README/authentication.conf.spec` explicitly documents the LDAP-strategy settings `sslVerifyServerCert` and `sslRootCAPath` under the relevant LDAP stanza, configure them there as well (`true` and `/opt/splunk/etc/auth/ldap/idm-ca.pem` respectively). Do not copy settings from unrelated SAML sections or assume all Splunk releases support the same parameters.

**Completion checklist:**

- [x] Splunk's `ldap.conf` backed up and edited.
- [x] `TLS_REQCERT demand` configured.
- [x] FreeIPA CA file configured via `TLS_CACERT`.
- [x] Existing TLS protocol and cipher settings retained.
- [x] Active settings verified with `grep`.
- [x] `splunk-bind` authenticated successfully using `LDAPCONF`.

**Summary:** Step 37 is **verified complete** for the supplied terminal session. Splunk's LDAP client requires certificate verification, trusts the FreeIPA CA, and successfully authenticates the `splunk-bind` lookup account. Proceed to **Step 38 — Create the LDAP strategy in Splunk Web**.

**References:**

- [Splunk LDAP Configuration Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.0/perform-advanced-configuration-of-ldap-authentication-in-splunk-enterprise/configure-ldap-using-configuration-files): Explains the Splunk LDAP client file location and certificate-verification directives.
- [Splunk Authentication Configuration Reference](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/configuration-file-reference/10.6.1-configuration-file-reference/authentication.conf): Lists supported authentication settings; check the reference for your installed Splunk version.

---
