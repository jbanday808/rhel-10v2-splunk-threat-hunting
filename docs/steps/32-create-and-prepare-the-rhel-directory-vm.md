**Step 32 — Create and prepare the RHEL directory VM**

In VMware Workstation Pro, create a **new** VM named `RHEL-IDM01` with RHEL 10.2 x64, 4 virtual CPUs, 8 GB RAM, a 60 GB disk, UEFI, and **Custom → VMnet8**. Install RHEL Minimal, create the local administrator `labadmin`, and keep SELinux enabled. Use a fresh installation rather than cloning the configured Splunk server.

On the **new VM console**, identify the active Ethernet profile:

At the prompt, enter the profile shown in the `NAME` column (for this VM, `ens160`). Do not type `IDM_PROFILE`, which is only the shell variable name. Changing the connection can briefly interrupt remote access.

```bash
cat /etc/redhat-release
nmcli -f NAME,DEVICE,TYPE connection show --active
read -r -p 'Enter the directory VM Ethernet profile name: ' IDM_PROFILE

sudo nmcli connection modify "$IDM_PROFILE" \
  ipv4.method manual \
  ipv4.addresses 172.25.250.30/24 \
  ipv4.gateway 172.25.250.2 \
  ipv4.dns 172.25.250.2 \
  ipv4.ignore-auto-dns yes

sudo nmcli connection up "$IDM_PROFILE"
sudo hostnamectl set-hostname idm01.lab.test
sudo cp -a /etc/hosts /etc/hosts.before-idm
sudoedit /etc/hosts
```

Preserve the localhost lines. Add the following entry once, and remove any conflicting entry that maps `idm01.lab.test` to another address:

```text
172.25.250.30 idm01.lab.test idm01
```

Before registering, confirm the VM has `.30`, a route through `.2`, and can resolve the Red Hat subscription host. If registration reports `Name or service not known`, fix upstream DNS before retrying:

```bash
ip -4 address show dev ens160
ip -4 route show default
nmcli -f IP4.DNS device show ens160
getent ahostsv4 subscription.rhsm.redhat.com
```

If registration is needed, run `sudo subscription-manager register`. Follow the release-selection checks in [Step 7](07-register-update-and-prepare-rhel.md) on this VM. Confirm `BaseOS` and `AppStream` are available, then run the following commands **one at a time**; stop if an update or installation fails:

```bash
sudo dnf upgrade --refresh -y
sudo dnf install -y ipa-server ipa-server-dns krb5-workstation openldap-clients \
  bind-utils chrony firewalld openssl openssh-server open-vm-tools

rpm -q ipa-server ipa-server-dns krb5-workstation bind-utils
sudo systemctl enable --now chronyd firewalld sshd vmtoolsd
sudo timedatectl set-timezone UTC
getent hosts idm01.lab.test
dig @172.25.250.2 docs.redhat.com +short
chronyc tracking
getenforce
sudo reboot
```

Continue only when all required packages report installed, the hostname resolves to `.30`, upstream DNS works, time is synchronized, and SELinux reports `Enforcing`. DNS at `.30` is expected **after** Step 33 installs IdM; use `.2` until then. Leave IPv6 enabled for IdM, even though this lab uses IPv4 addresses. For the reported profile, registration, package, and DNS errors, see [IdM setup troubleshooting](../troubleshooting/idm-installation-and-dns.md).

**Command overview:** `nmcli` applies the static network settings; `hostnamectl` sets the directory hostname; `sudoedit` edits the hosts file; `dnf` installs IdM and its tools; `chronyc` checks time; `dig` tests DNS; `getenforce` checks SELinux.

**Summary:** The directory VM has its own fixed address and the packages needed for IdM.

References:

- [Red Hat IdM Preparation Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/installing_identity_management/preparing-the-system-for-idm-server-installation): This guide describes IdM prerequisites, required packages, networking, and installation permissions.

---
