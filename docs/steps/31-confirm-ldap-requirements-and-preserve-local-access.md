**Step 31 — Confirm LDAP requirements and preserve local access**

This phase adds centralized Splunk sign-in through **Red Hat Identity Management (IdM)** on a separate RHEL VM. LDAP is the directory service; **LDAPS** protects the connection with encryption and a verified server certificate. The directory choice keeps both lab servers on RHEL.

| System | Address | Purpose |
| --- | --- | --- |
| `splunk01.lab.test` | `172.25.250.10` | Splunk Enterprise and its search interface |
| `winhunt01.lab.test` | `172.25.250.20` | Windows threat hunting and event forwarding |
| `idm01.lab.test` | `172.25.250.30` | Directory accounts, groups, DNS, and directory certificates |

Splunk connects **outbound** from `.10` to `.30` on TCP `636`. Do not add an inbound LDAP port to the Splunk server. Windows continues forwarding events on TCP `9997`.

Before continuing:

1. Confirm `.30` is available and outside the VMware DHCP pool.
2. In Splunk, open **Settings → Licensing** and confirm an active Enterprise trial or another license that supports authentication. **Splunk Free removes authentication and user management**, so it cannot validate this integration.
3. Sign in with the existing **local Splunk `admin`** account in a separate browser window and retain its password.
4. Confirm you can still open the RHEL VM console as `labadmin`.
5. Keep directory usernames different from local Splunk usernames. Native Splunk accounts take precedence over LDAP accounts with the same name.
6. Confirm Step 30 created the `lab_hunter` role and its six-index restriction.

On **RHEL-SPLUNK01**, create a protected configuration backup while no other configuration changes are being made:

```bash
sudo bash <<'ROOT'
set -euo pipefail
umask 077
install -d -m 700 /var/backups/siem-lab
tar -czf "/var/backups/siem-lab/splunk-before-ldap-$(date -u +%Y%m%dT%H%M%SZ).tar.gz" \
  -C /opt/splunk etc
ROOT
```

**Command overview:** `sudo bash` runs the enclosed commands as administrator; `set -euo pipefail` stops on errors; `umask 077` protects new files; `install -d -m 700` creates a private backup folder; `tar -czf` saves Splunk configuration.

**Summary:** You have a local recovery account and a private configuration backup before enabling directory sign-in.

References:

- [Splunk Free Guide](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configure-splunk-licenses/about-splunk-free): This guide explains which authentication features are unavailable under the Free license.
- [Splunk LDAP Authentication Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/use-ldap-as-an-authentication-scheme/set-up-user-authentication-with-ldap): This guide explains LDAP sign-in and local-account precedence.

---
