# 04 — Identity, Authentication and Least-Privilege Access

## Objective

Protect Splunk Web and directory resources with explicit identities, verified encrypted directory connections, group-based least privilege, separate privileged accounts, and recorded allow/deny tests. Native LDAP mappings are a **starting point**, not continuous-authorization or phishing-resistant MFA.

## Step A — Verify directory state (RHEL-IDM01 console)

Prerequisite: original [Steps 31–34](../steps/README.md) completed and IdM DNS/certificates checked.

```bash
sudo ipactl status
kinit admin
ipa user-show hunter01
ipa group-show splunk-hunters
ipa group-show splunk-admins
kdestroy
```

**Command overview:** `ipactl status` checks IdM components; `kinit` prompts for a Kerberos password; `ipa` commands read directory entries; `kdestroy` clears cached credentials. If `admin` is not an approved lab administrator, use a permitted testing account.

**Verify:** Only authorized test users belong to the correct directory groups. In particular, `hunter01` must **not** inherit `splunk-admins` and `unmapped01` must not be mapped to any Splunk role.

## Step B — Validate the IdM TLS boundary (RHEL-SPLUNK01 console)

Prerequisite: retrieve and verify the **public** IdM CA exactly as in [Step 35](../steps/35-configure-splunk-dns-and-trust-the-directory-certificate.md).

```bash
getent hosts idm01.lab.test
sudo -u splunk openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test \
  -verify_return_error </dev/null
```

**Command overview:** DNS lookup confirms the directory name; `openssl s_client` checks certificate chain, hostname and verified TLS. Require the certificate validation success message; TLS encryption alone without identity verification is insufficient.

For a permitted lookup test, follow [Step 36](../steps/36-verify-ldaps-before-enabling-directory-sign-in.md) with `ldapsearch -W`; never store the bind password in code or logs. Splunk also requires its own LDAP client certificate policy; follow [Step 37](../steps/37-require-certificate-verification-in-splunk-s-ldap-client.md).

## Step C — Verify Splunk authorization

On RHEL-SPLUNK01:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool authorize list role_lab_hunter --debug
```

In **Splunk Web → Settings → Authentication methods / LDAP strategies → Map groups**, inspect mapping:

| Directory group | Splunk role | Intent |
| --- | --- | --- |
| `splunk-hunters` | `lab_hunter` | Searches six lab indexes only |
| `splunk-admins` | `admin` | Carefully limited lab administrators |
| `ipausers` | No automatic Splunk mapping | Avoid broad implicit privileges |
| `unmapped01` (test user) | None | Denial control |

Review `apps/LAB_SIEM/local/authorize.conf` and confirm active merged settings; avoid blanket `admin` for analyst users. Keep a local Splunk emergency admin identity under strict break-glass controls.

## Step D — Confirm both access and denial (Splunk Web)

1. Sign in as a known hunter test account; search an **allowed** index.
2. Attempt access to an index **not granted** to that role (use a dedicated harmless test index if appropriate); expect denial.
3. Attempt sign-in as `unmapped01`; expect no authorized Splunk app access.
4. Sign in using the lab administrator only through the separately approved admin route.
5. Remove a test user from `splunk-hunters` during a controlled exercise and check whether permissions change according to documented sessions/cache behavior.
6. Capture sanitized event IDs, expected/observed, date and tester; never include passwords.

**Stop:** privilege escalation, unexpected access, certificate failure, or emergency admin failure.

## Step E — MFA and adaptive policy as future work

For a **complete dynamic Zero Trust design**, place the resource behind a compatible identity provider / ZTNA policy enforcement boundary that evaluates MFA, device compliance and session risk. **IdM group membership and a simple LDAP bind do not themselves provide this adaptive policy**. Plan an approved IdP with SAML/OIDC or a vendor-supported Splunk auth method after verifying your installed Splunk version. Never improvise insecure authentication header forwarding or open management port 8089 publicly.

## Optional cross-vendor roadmap (not installed)

Microsoft Entra ID / Conditional Access, an approved ICAM/PAM solution, Palo Alto Prisma Access, Cisco Secure Access, Juniper networking, and VMware networking may support parts of an enterprise design. Name them in a requirements/decision matrix, **not in the installed-assets list**.

**Evidence:** [validation template](10-verification-and-evidence.md). **Status:** live IAM enforcement and MFA outcomes remain Pending.
