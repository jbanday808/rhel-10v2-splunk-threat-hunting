**Step 33 — Install IdM with DNS and its certificate authority**

Configure **RHEL-IDM01** as the FreeIPA / Red Hat Identity Management (IdM) server for the isolated RHEL 10.2 Splunk threat-hunting lab. This step covers integrated DNS, Kerberos, LDAP, a built-in certificate authority (CA), firewall access, and verification.

| Component | Lab value |
| --- | --- |
| IdM server | `idm01.lab.test` |
| Server address / interface | `172.25.250.30/24` on `ens160` |
| DNS domain | `lab.test` |
| Kerberos realm | `LAB.TEST` |
| NetBIOS name | `LAB` |
| VMware gateway and external DNS forwarder | `172.25.250.2` |
| Reverse DNS zone | `250.25.172.in-addr.arpa.` |
| Splunk server | `splunk01.lab.test` → `172.25.250.10` |
| Windows 11 endpoint | `winhunt01.lab.test` → `172.25.250.20` |

### 33.1 — Verify hostname, IPv4 resolution, packages, and time

Run these commands on **RHEL-IDM01**:

```bash
hostnamectl --static
ip -4 address show dev ens160
getent ahostsv4 idm01.lab.test
cat /etc/hosts
rpm -q ipa-server ipa-server-dns
dig @172.25.250.2 redhat.com A +short
chronyc tracking
chronyc sources -v
```

**Expected:** The server hostname is `idm01.lab.test`; interface `ens160` has `172.25.250.30/24`; IPv4 hostname lookup returns `172.25.250.30`; the IdM packages are installed; the forwarder resolves external names; and Chrony has a working time source.

If needed, correct the hostname:

```bash
sudo hostnamectl set-hostname idm01.lab.test
sudo vi /etc/hosts
```

Keep the existing loopback entries and ensure this mapping appears once without a conflicting hostname entry:

```text
172.25.250.30 idm01.lab.test idm01
```

**Observed in this lab (8 November 2026):**

- `ipa-server-4.13.4-1.el10_2` and `ipa-server-dns-4.13.4-1.el10_2` were already installed.
- `dig @172.25.250.2 redhat.com A +short` returned IPv4 addresses; the VMware DNS forwarder worked.
- `getent hosts idm01.lab.test` returned a link-local IPv6 address (`fe80::...`), but `getent ahostsv4 idm01.lab.test` correctly returned `172.25.250.30`. IPv6 does not need to be disabled just because the first lookup returns IPv6.
- `/etc/hosts` contained the correct `172.25.250.30 idm01.lab.test idm01` entry.
- Time synchronization still needs to be checked with `chronyc tracking` and `chronyc sources -v`. Kerberos depends on accurate clocks.

If the packages are missing, install them:

```bash
sudo dnf install -y ipa-server ipa-server-dns
```

### 33.2 — Open IdM services in the existing firewall zone

First inspect the zones instead of assuming a new zone must be created:

```bash
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --permanent --get-zones
sudo firewall-cmd --zone=idm-lab --list-all
```

**Observed in this lab:** `idm-lab` already exists and matches source `172.25.250.0/24`; `public` is the default interface zone for `ens160`. Do **not** run `--new-zone=idm-lab` again. The previous command targeting `--zone=siem-lab` returned `INVALID_ZONE` because `siem-lab` is not present on this IdM server.

On this VM, configure the **existing** `idm-lab` zone:

```bash
sudo firewall-cmd --permanent --zone=idm-lab --add-service=freeipa-4
sudo firewall-cmd --permanent --zone=idm-lab --add-service=dns
sudo firewall-cmd --permanent --zone=idm-lab --add-service=ssh
sudo firewall-cmd --reload
sudo firewall-cmd --zone=idm-lab --list-all
sudo firewall-cmd --get-active-zones
```

If building a **fresh** VM where `idm-lab` does not exist, create it and assign the private subnet **before** running the service commands:

```bash
sudo firewall-cmd --permanent --new-zone=idm-lab
sudo firewall-cmd --permanent --zone=idm-lab --add-source=172.25.250.0/24
sudo firewall-cmd --reload
```

**Command overview:** `firewall-cmd` manages firewall rules; `--zone=idm-lab` selects the actual lab zone; `freeipa-4` permits IdM services; `dns` permits DNS queries; `ssh` permits remote administration; `--reload` applies changes.

### 33.3 — Install IdM with integrated DNS and CA

Start a root session **as a separate command**:

```bash
sudo -i
```

Once the prompt changes to `root@idm01`, execute this block **inside that shell**:

```bash
umask 0022
ipa-server-install \
  --hostname=idm01.lab.test \
  --domain=lab.test \
  --realm=LAB.TEST \
  --ip-address=172.25.250.30 \
  --setup-dns \
  --forwarder=172.25.250.2 \
  --auto-reverse
```

Enter separate strong passwords for the **Directory Manager** and **IdM `admin`** accounts when prompted; do not put passwords in the command or commit them to GitHub. Retain the integrated, self-signed root CA. These credentials are separate from Splunk's local administrator password.

**Why run `sudo -i` separately?** In an earlier attempt, the installer command was pasted immediately after `sudo -i` and no installation wizard appeared. Confirm the root prompt before entering `ipa-server-install`. Do not interpret the lack of output as a completed installation.

**Observed installer prompts and selections:**

| Installer prompt / setting | Selection or observed result |
| --- | --- |
| NetBIOS domain name `[LAB]` | `LAB` (press Enter) |
| Configure Chrony with a specified NTP server or pool? `[no]` | `No` (retain existing sources **if synchronized**) |
| Domain / realm | `lab.test` / `LAB.TEST` |
| Hostname / IPv4 | `idm01.lab.test` / `172.25.250.30` |
| DNS forwarder / policy | `172.25.250.2` / `only` |
| Reverse DNS | Installer reported it will create `250.25.172.in-addr.arpa.` |
| CA | `CN=Certificate Authority,O=LAB.TEST`; self-signed root |
| Continue to configure the system with these values? `[no]` | Type `yes` to begin installation |

**Verified installation update (8 November 2026):** The installer later reported `Setup complete` and `The ipa-server-install command was successful`. All nine listed IdM services were reported running. Integrated DNS returned `172.25.250.30` for `idm01.lab.test`, the LDAP SRV record advertised port `389`, and the administrator's Kerberos authentication was eventually restored as documented in §33.8.

If the installer fails, inspect the installation log instead of repeatedly rerunning it:

```bash
sudo tail -n 100 /var/log/ipaserver-install.log
```

Once installation finishes, leave the root session:

```bash
exit
```

### 33.4 — Verify services, Kerberos, and DNS zones

Only **after the installer reports successful completion**, run as the regular lab administrator:

```bash
sudo ipactl status
kinit admin
klist
ipa ping
ipa dnszone-find
ipa dnszone-show 250.25.172.in-addr.arpa.
```

**Expected:** IdM services are running, `kinit admin` obtains a Kerberos ticket for `LAB.TEST`, the IPA command works, and the reverse zone exists. If the reverse zone was not created, inspect DNS configuration first; create it only when genuinely missing:

```bash
ipa dnszone-add 250.25.172.in-addr.arpa.
```

### 33.5 — Add Splunk and Windows DNS records

Check for existing entries before adding records (these commands may return “not found” when a record has not yet been created):

```bash
ipa dnsrecord-show lab.test splunk01
ipa dnsrecord-show lab.test winhunt01
ipa dnsrecord-show 250.25.172.in-addr.arpa. 10
ipa dnsrecord-show 250.25.172.in-addr.arpa. 20
```

For **missing records only**, add the following:

```bash
ipa dnsrecord-add lab.test splunk01 --a-rec=172.25.250.10
ipa dnsrecord-add lab.test winhunt01 --a-rec=172.25.250.20
ipa dnsrecord-add 250.25.172.in-addr.arpa. 10 --ptr-rec=splunk01.lab.test.
ipa dnsrecord-add 250.25.172.in-addr.arpa. 20 --ptr-rec=winhunt01.lab.test.
```

**Command overview:** `ipa dnsrecord-add` creates DNS entries; `--a-rec` maps hostnames to IPv4 addresses; `--ptr-rec` maps IPv4 addresses back to hostnames.

### 33.6 — Validate forward DNS, reverse DNS, and LDAP discovery

```bash
dig @172.25.250.30 idm01.lab.test +short
dig @172.25.250.30 splunk01.lab.test +short
dig @172.25.250.30 winhunt01.lab.test +short
dig @172.25.250.30 -x 172.25.250.30 +short
dig @172.25.250.30 -x 172.25.250.10 +short
dig @172.25.250.30 -x 172.25.250.20 +short
dig @172.25.250.30 _ldap._tcp.lab.test SRV +short
```

**Expected:**

- Forward lookups: `172.25.250.30`, `172.25.250.10`, and `172.25.250.20` respectively.
- Reverse lookups: `idm01.lab.test.`, `splunk01.lab.test.`, and `winhunt01.lab.test.`.
- LDAP SRV record: includes `idm01.lab.test.` and usually advertises port `389`. Splunk will use encrypted LDAP on port `636` when configured to do so.

Check the local resolver after installation:

```bash
nmcli -f IP4.DNS device show ens160
cat /etc/resolv.conf
chronyc tracking
chronyc sources -v
```

The IdM server should use its own integrated DNS service at `172.25.250.30` after installation. If it does not, inspect the active NetworkManager connection and correct its DNS setting deliberately. Keep the default gateway at `172.25.250.2` and the IdM **external DNS forwarder** at `172.25.250.2`; these serve different roles.

### 33.7 — Troubleshooting observed during initial setup

| Error or observation | Cause / corrective action |
| --- | --- |
| `IPA is not configured` from `ipactl status` | Packages are installed, but the IPA server installation has not completed. Run and finish `ipa-server-install`, then check `ipactl status`. |
| `Configuration file does not specify default realm` from `kinit admin` | Kerberos is not configured yet. Complete IdM server installation and retry `kinit admin`. |
| `IPA client is not configured on this system` | IPA command-line configuration is not ready until server setup succeeds. |
| `dig @172.25.250.30 ...` → `connection refused` | DNS was not yet accepting connections on the IdM IP. Install/start integrated DNS, then verify services and firewall. |
| `INVALID_ZONE: siem-lab` | Wrong zone for this VM. Use the existing `idm-lab` zone; check `firewall-cmd --get-active-zones` first. |
| `getent hosts` reports `fe80::...` | This alone does not prove IPv4 hostname failure. `getent ahostsv4 idm01.lab.test` correctly returned `172.25.250.30`. |
| No installer wizard after `sudo -i` | Ensure the command is run at the `root@idm01` prompt, not merely displayed or pasted as part of the shell transition. |
| NTP prompt answered `No` | Fine **only if** an existing Chrony source provides synchronized time. Verify with `chronyc tracking` and `chronyc sources -v`. |

### 33.8 — Reset the FreeIPA administrator password through LDAP (verified recovery)

**Purpose:** Recover the IdM `admin@LAB.TEST` account when Kerberos authentication fails. This changes the **IPA admin account password** using an authenticated LDAP connection; it does **not** reset the Directory Manager password.

**Observed failed Kerberos attempt:**

```bash
kinit admin@LAB.TEST
klist
ipa ping
ipa dnszone-find
```

```text
Password for admin@LAB.TEST:
kinit: Password read interrupted while getting initial credentials
klist: Credentials cache 'KCM:0' not found
ipa: ERROR: did not receive Kerberos credentials
ipa: ERROR: did not receive Kerberos credentials
```

The password prompt was interrupted, so no Kerberos ticket was obtained. If still at the password prompt, press **Ctrl+C** before running recovery commands. Earlier attempts also reported an incorrect IPA admin password.

**Reset the IPA admin password:** Run as `root` on `idm01.lab.test`. You must know the **Directory Manager** password established when IdM was installed:

```bash
export LDAPTLS_CACERT=/etc/ipa/ca.crt

ldappasswd -x \
  -H ldaps://idm01.lab.test \
  -D "cn=Directory Manager" \
  -W -S \
  "uid=admin,cn=users,cn=accounts,dc=lab,dc=test"
```

The command prompts interactively:

```text
New password:
Re-enter new password:
Enter LDAP Password:
```

- **New password / Re-enter new password:** Enter and confirm the new password for `admin@LAB.TEST`.
- **Enter LDAP Password:** Enter the **Directory Manager password** (not the new IPA admin password and not the Linux root password).
- The passwords are hidden while typing. **Never copy passwords into GitHub, documentation, shell arguments, or screenshots.**

**Observed error and resolution:** The first two attempts returned:

```text
ldap_bind: Invalid credentials (49)
```

This means the **Directory Manager LDAP bind** failed, usually because the password supplied to `-W` was wrong. Re-check the Directory Manager password and retry deliberately; do not change the LDAP bind DN or disable TLS to work around a credentials error. Later attempts returned to the shell prompt **without an error**, followed by successful Kerberos authentication. `ldappasswd` commonly produces no success message.

**Verify the restored admin account:**

```bash
kinit admin@LAB.TEST
klist
ipa ping
ipa dnszone-find
```

**Verified results from 8 November 2026:**

- `kinit admin@LAB.TEST` accepted the new password.
- `klist` showed `Default principal: admin@LAB.TEST` and a valid `krbtgt/LAB.TEST@LAB.TEST` ticket.
- `ipa ping` returned `IPA server version 4.13.4. API version 2.257`.
- `ipa dnszone-find` returned **two active DNS zones**: `lab.test.` and `250.25.172.in-addr.arpa.`, both naming `idm01.lab.test.` as the authoritative server.
- The FreeIPA services, integrated DNS, and Chrony synchronization were also verified earlier; `chronyc tracking` reported `Leap status: Normal`, and `timedatectl` reported `System clock synchronized: yes`.

**Command overview:** `kinit` obtains an admin Kerberos ticket; `klist` shows it; `LDAPTLS_CACERT` selects the trusted CA file; `ldappasswd` changes the IPA admin password over secure LDAP; `-x` uses simple LDAP authentication; `-H` selects the LDAPS server; `-D` names the Directory Manager bind account; `-W` prompts for its password; `-S` prompts for the user's new password; `ipa ping` and `ipa dnszone-find` verify that administrator access works.

**Summary:** IPA admin password recovery **succeeded**, and the `LAB.TEST` administrator can authenticate and access both DNS zones. Continue with Step 34 after confirming that any required Splunk and Windows A/PTR records from `33.5` exist; those records were not proven by this password-reset output.

**Summary:** FreeIPA installation, core services, integrated DNS, CA, synchronized time, and IPA administrator authentication have been verified on `idm01.lab.test`. Check the Splunk and Windows A/PTR records before continuing to Step 34.

References:

- [Red Hat IdM Installation Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/installing_identity_management/installing-an-idm-server-with-integrated-dns-with-an-integrated-ca-as-the-root-ca): This guide explains interactive installation with integrated DNS and a certificate authority.
- [Red Hat IdM DNS Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/working_with_dns_in_identity_management/index): This guide explains forward and reverse DNS records in IdM.

---
