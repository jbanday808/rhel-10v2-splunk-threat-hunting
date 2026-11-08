**Step 35 — Configure Splunk DNS and trust the directory certificate**

**Run this step on RHEL-SPLUNK01 (172.25.250.10), not RHEL-IDM01 (172.25.250.30).** Step 33 configured the IdM server; Step 35 configures the separate Splunk server to resolve and trust IdM. Use the **Splunk VM console** when applying network changes, since activating a connection may temporarily interrupt SSH.

### 35.1 — Confirm you are on the Splunk VM

```bash
hostnamectl --static
ip -4 address show dev ens160
nmcli -f NAME,DEVICE,TYPE connection show --active
```

**Expected:** The VM being configured is `splunk01.lab.test` with IPv4 `172.25.250.10/24` (the hostname may vary if your VM naming is different). Do not continue with the DNS changes if the address is `172.25.250.30`; that is **idm01**, the directory server.

Install the client tools **on Splunk**:

```bash
sudo dnf install -y openldap-clients bind-utils
```

### 35.2 — Get the active Ethernet profile without a blank prompt

The original interactive step asked for the Splunk VM Ethernet profile name. Pressing **Enter** without a value left `SPLUNK_PROFILE` empty and caused:

```text
Enter the Splunk VM Ethernet profile name:
Error: unknown connection ''.
Error: unknown connection ''.
```

In the captured session, `nmcli` displayed `ens160` as the connection name on **idm01**, but that is **not evidence the commands were run on Splunk**. The empty name meant the attempted changes were rejected.

**On RHEL-SPLUNK01**, retrieve the active profile on interface `ens160` automatically:

```bash
SPLUNK_PROFILE="$(nmcli -g GENERAL.CONNECTION device show ens160)"
printf 'Active Ethernet profile: %s\n' "$SPLUNK_PROFILE"
```

If this shows an empty value or `--`, stop and inspect `nmcli connection show --active` before attempting a change. On this lab the active profile is often named `ens160`, but always use the name actually returned **on Splunk**.

Apply the DNS setting **only after confirming the Splunk VM's IP is `172.25.250.10`**:

```bash
if ! ip -4 -o address show dev ens160 | grep -q 'inet 172\.25\.250\.10/'; then
  echo 'STOP: This is not the expected Splunk VM (172.25.250.10).'
elif [ -z "$SPLUNK_PROFILE" ] || [ "$SPLUNK_PROFILE" = '--' ]; then
  echo 'STOP: No active Ethernet connection profile was found.'
else
  sudo nmcli connection modify "$SPLUNK_PROFILE" \
    ipv4.dns 172.25.250.30 \
    ipv4.ignore-auto-dns yes
  sudo nmcli connection up "$SPLUNK_PROFILE"
fi
```

This changes **only Splunk's DNS resolver**, not its static address or gateway. Keep Splunk at `172.25.250.10` with gateway `172.25.250.2`. The Windows VM and physical host can retain their existing DNS and Splunk hosts-file entries.

**Command overview:** `nmcli -g GENERAL.CONNECTION` identifies the Ethernet profile; `SPLUNK_PROFILE` stores the name for later commands; `ipv4.dns` points Splunk at IdM; `ipv4.ignore-auto-dns yes` prevents DHCP DNS values from overriding it; `connection up` activates the setting.

### 35.3 — Verify DNS on RHEL-SPLUNK01

```bash
nmcli -f IP4.DNS device show ens160
ip -4 address show dev ens160
ip -4 route show default
getent ahostsv4 idm01.lab.test
dig idm01.lab.test +short
dig docs.redhat.com +short
```

**Expected:**

- Active DNS server: `172.25.250.30`.
- Splunk server address: `172.25.250.10`; gateway: `172.25.250.2`.
- IdM hostname resolution: `172.25.250.30`.
- External domain resolution: one or more valid answers, confirming IdM's forwarding works.

**IPv6 lookup note:** In the captured failure session, `getent hosts idm01.lab.test` printed a link-local IPv6 address (`fe80::...`), while `dig idm01.lab.test +short` correctly returned `172.25.250.30`. Use `getent ahostsv4` to explicitly test IPv4; the IPv6 result alone is not an error.

If DNS fails, compare:

```bash
dig @172.25.250.30 idm01.lab.test A +short
dig @172.25.250.30 docs.redhat.com A +short
cat /etc/resolv.conf
```

If the direct query to IdM works but the ordinary `dig` fails, inspect the **Splunk** resolver configuration; do not reinstall IdM.

### 35.4 — Obtain and trust the public IdM CA certificate

**On the RHEL-IDM01 VM console**, display the IdM server's SSH host-key fingerprint and CA certificate fingerprint:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
openssl x509 -in /etc/ipa/ca.crt -noout -fingerprint -sha256
```

**On RHEL-SPLUNK01**, copy only the **public** IdM CA certificate:

```bash
mkdir -p "$HOME/siem-public"
scp labadmin@172.25.250.30:/etc/ipa/ca.crt "$HOME/siem-public/idm-ca.pem"
openssl x509 -in "$HOME/siem-public/idm-ca.pem" -noout -fingerprint -sha256

sudo install -d -o splunk -g splunk -m 700 /opt/splunk/etc/auth/ldap
sudo install -o splunk -g splunk -m 600 \
  "$HOME/siem-public/idm-ca.pem" /opt/splunk/etc/auth/ldap/idm-ca.pem
```

Before accepting the SSH connection, compare its host-key fingerprint with the value displayed directly on IdM. Then compare both CA certificate fingerprints; they must match. If the certificate cannot be read with `scp`, check file access on IdM rather than transferring private CA files.

Keep the existing `/opt/splunk/etc/auth/lab/` certificates for Splunk Web and forwarder traffic. Do not copy `/root/cacert.p12`, the Directory Manager password, or private keys to Splunk.

**Command overview:** `scp` securely copies the public CA certificate; `openssl x509` displays its fingerprint; `install` creates a directory and stores the certificate with Splunk service ownership and restrictive permissions.

### 35.5 — Troubleshooting observed on 8 November 2026

| Output | Explanation / fix |
| --- | --- |
| `Must be root to run ipa-server-install`, followed by `The ipa-server-install command failed.` | This message indicates an `ipa-server-install` invocation without root privileges after leaving the root shell. It does **not** mean Step 35 requires the installer. FreeIPA was already installed and verified on `idm01`. Do not rerun the installer for DNS client configuration. |
| `nmcli ...` → `Error: unknown connection ''.` | `SPLUNK_PROFILE` was empty because the interactive prompt received no profile name. Obtain the actual active Ethernet profile automatically, verify it, and rerun on **Splunk**. |
| `labadmin@idm01:~$` when executing Step 35 | Wrong VM: this prompt belongs to `idm01`. Switch to the `splunk01` VM before changing DNS. |
| `getent hosts idm01.lab.test` returns `fe80::...` | The lookup returned IPv6. Test the IPv4 entry with `getent ahostsv4 idm01.lab.test` or `dig idm01.lab.test A +short`. |
| `dig docs.redhat.com +short` succeeds on `idm01` | IdM DNS forwarding is working, but this does **not** verify that the Splunk VM has been configured. Run the Step 35 DNS checks on Splunk. |

**Observed outcome:** The `dnf` command reported the tools already installed on `idm01`, and the `nmcli` modifications failed due to an empty connection name. The displayed DNS tests were also run on `idm01`. **Splunk VM DNS configuration and CA certificate trust remain unverified** until these steps are successfully executed on `172.25.250.10`.

**Summary:** Configure **only** the Splunk VM to use IdM DNS at `172.25.250.30`, confirm IPv4 and external name resolution from Splunk, and install a fingerprint-verified copy of the IdM public CA certificate.

References:

- [Red Hat Enterprise Linux 10 networking guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/configuring_and_managing_networking/): Explains how to inspect and modify NetworkManager connection profiles and configure DNS.
- [NetworkManager nmcli reference](https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nmcli.html): Documents commands to show active Ethernet profiles, modify settings, and activate connections.

---
