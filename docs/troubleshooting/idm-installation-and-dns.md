# IdM setup errors: missing commands and DNS connection refused

Use this guide on **RHEL-IDM01** if the earlier Step 32–33 errors recur on a new installation. Step 33 separately records the successful IdM installation observed in the lab. Run commands individually, check each result, and keep passwords and installation logs out of this public repository.

| Reported symptom | What to check first |
| --- | --- |
| `unknown connection 'IDM_PROFILE'` | The profile name was entered literally instead of the active Ethernet profile (`ens160` in this lab). |
| `m,cli: command not found` or `nmcli con ens160 up` rejects an argument | Correct the typo and use `nmcli con up ens160`. |
| `subscription-manager`: `Name or service not known` | Check the gateway and upstream DNS at `172.25.250.2` before registration. |
| `sudo: ipactl: command not found`, `kinit: command not found`, or `ipa: command not found` | Confirm that the **server** packages from Step 32 were installed. These commands must be used after the appropriate setup stage. |
| Suggested `ipa-client` installation ends in `Failed to obtain authentication` | The unprivileged automatic package prompt failed; install the intended server packages with `sudo dnf`. |
| `dig @172.25.250.30 ...`: `connection refused` | IdM DNS is unavailable at `.30`; first confirm that Step 33 finished successfully, then check the listener and firewall. |

## 1. Check the VM network and registration

Work from the VM console when changing network settings, because bringing the connection up can interrupt a remote session. Check the actual profile, address, route, DNS server, and Red Hat hostname resolution:

```bash
nmcli -f NAME,DEVICE,TYPE connection show --active
ip -4 address show dev ens160
ip -4 route show default
nmcli -f IP4.DNS device show ens160
getent ahostsv4 subscription.rhsm.redhat.com
```

For this three-VM lab, expect `ens160` at `172.25.250.30/24`, default gateway `172.25.250.2`, and upstream DNS `172.25.250.2` **before** IdM installation. If the profile or address differs, return to [Step 32](../steps/32-create-and-prepare-the-rhel-directory-vm.md). At its `read` prompt, enter `ens160`, not the variable name `IDM_PROFILE`. Check that `.30` is available before assigning it. Use `nmcli con up ens160` to activate a saved profile; `nmcli con ens160 up` reverses the arguments.

If the Red Hat subscription hostname does not resolve, verify VMware VMnet8 NAT and its DNS settings. Once resolution succeeds, check registration and the enabled repositories:

```bash
sudo subscription-manager identity
sudo dnf repolist
```

An unregistered VM may report no identity. After DNS works, use the interactive `sudo subscription-manager register` command if required and follow [Step 7](../steps/07-register-update-and-prepare-rhel.md) for release and repository checks. Keep account credentials out of command arguments and published output. The RHEL 10 `BaseOS` and `AppStream` repositories must be available for the IdM server packages.

**Command overview:** `nmcli` identifies the active profile and DNS; `ip` shows the address and route; `getent` tests name resolution; `subscription-manager` and `dnf repolist` check whether packages can be obtained.

## 2. Confirm and install the server packages

Check packages before using `ipactl`, `kinit`, or `ipa`:

```bash
rpm -q ipa-server ipa-server-dns krb5-workstation bind-utils
```

`package ... is not installed` means Step 32 has not completed. From the `labadmin` account, after registration and repository checks succeed, run:

```bash
sudo dnf install -y ipa-server ipa-server-dns krb5-workstation \
  openldap-clients bind-utils chrony firewalld openssl \
  openssh-server open-vm-tools
rpm -q ipa-server ipa-server-dns krb5-workstation bind-utils
```

Stop if `dnf` fails or any required package is still missing. The shell's suggestion to install **`ipa-client`** does not replace the `ipa-server` and `ipa-server-dns` packages for this VM. The `Failed to obtain authentication` message came from the automatic installation prompt, not from the IdM `admin` account. Use `sudo dnf` from `labadmin` rather than accepting that prompt again.

**Command overview:** `rpm -q` checks installed packages; `sudo dnf install` installs the IdM server, integrated DNS, Kerberos tools, and the Step 32 utilities using OS administrator privileges.

## 3. Install IdM before testing its DNS

Before installation, verify the prerequisites from [Step 32](../steps/32-create-and-prepare-the-rhel-directory-vm.md):

```bash
hostname -f
getent hosts idm01.lab.test
dig @172.25.250.2 docs.redhat.com +short
chronyc tracking
getenforce
```

The hostname must resolve to `172.25.250.30`, upstream DNS must return an answer, time must be synchronized, and SELinux must report `Enforcing`. Then follow [Step 33](../steps/33-install-idm-with-dns-and-its-certificate-authority.md) to review the lab firewall rules and run the **interactive** `ipa-server-install --setup-dns` procedure. Enter Directory Manager and IdM `admin` passwords only at its prompts. Wait for the installer to report success before proceeding.

An unanswered `dig @172.25.250.30` test **before** successful installation does not prove a bad DNS record: no integrated DNS server has been configured yet. Keep the VM's upstream resolver at `.2` until installation succeeds; then verify that its resolver uses the integrated DNS at `.30`. If an installer run failed partway through, inspect its local `/var/log/ipaserver-install.log` and resolve the specific failure before attempting further installation or DNS changes; do not publish that log.

**Command overview:** `hostname` and `getent` check the IdM name; `dig @172.25.250.2` checks the upstream DNS server; `chronyc` checks time; `getenforce` checks SELinux.

## 4. Verify services, then create the remaining records

Only after the installer reports success, run these checks individually:

```bash
sudo ipactl status
dig @172.25.250.30 idm01.lab.test +short
dig @172.25.250.30 -x 172.25.250.30 +short
dig @172.25.250.30 _ldap._tcp.lab.test SRV +short
kinit admin
klist
```

Expect running IdM services, including `named` for integrated DNS; the forward query should return `.30`, the reverse query should return `idm01.lab.test.`, the LDAP SRV query should return an IdM host, and `klist` should show an `admin@LAB.TEST` ticket. Before `kinit`, verify that the VM's resolver now uses `.30` with `nmcli -f IP4.DNS device show ens160`. If it still uses `.2`, follow Step 33 to change only the active profile's DNS after the `.30` queries work. Then proceed with Step 33's `ipa dnsrecord-add` commands for the Splunk and Windows VM names. Inspect existing records first if they may already have been added.

If the installer reported success but port 53 still refuses connections, inspect the service and listener locally:

```bash
sudo ipactl status
sudo systemctl status ipa --no-pager
sudo ss -lntup | grep ':53'
sudo firewall-cmd --zone=idm-lab --list-all
sudo journalctl -u ipa -b -n 80 --no-pager
```

No listener points to a service or configuration problem; a listener with failed remote queries calls for a firewall and interface check. Stop and review the local installer log and service journal before making additional changes. The `.30` DNS tests cannot pass just by installing `ipa-client`.

**Command overview:** `ipactl` checks the installed services; `dig` tests IdM DNS; `kinit` signs in as the IdM administrator; `klist` shows the resulting ticket; `ss` and `firewall-cmd` help locate a DNS listener or access problem.

**Summary:** Install the server packages in Step 32, finish the interactive server installation in Step 33, and only then run `ipactl`, `kinit`, `ipa`, and DNS queries against `.30`. Confirm each gate on the actual VM; sanitize any evidence before publication.

References:

- [Red Hat RHEL 10 IdM preparation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/installing_identity_management/preparing-the-system-for-idm-server-installation): Explains registration, `BaseOS` and `AppStream`, server packages, and the required installation umask.
- [Red Hat RHEL 10 IdM installation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/installing_identity_management/index): Covers the interactive DNS and certificate authority setup and the private installer log.
- [Red Hat RHEL 10 IdM service access](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/accessing_identity_management_services/index): Describes `kinit` and `ipactl status` after installation.
- [Red Hat RHEL 10 Ethernet configuration](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/configuring_and_managing_networking/configuring-an-ethernet-connection): Shows the `nmcli connection modify` and `nmcli connection up` sequence.
