**Step 32 — Create and prepare the RHEL directory VM**

In VMware Workstation Pro, create a **new** VM named `RHEL-IDM01` with RHEL 10.2 x64, 4 virtual CPUs, 8 GB RAM, a 60 GB disk, UEFI, and **Custom → VMnet8**. Install RHEL Minimal, create the local administrator `labadmin`, and keep SELinux enabled. Use a fresh installation rather than cloning the configured Splunk server.

On the **new VM console**, identify the active Ethernet profile:

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

If registration is needed, run `sudo subscription-manager register`. Follow the release-selection checks in Step 7 on this VM, then install its updates and tools:

```bash
sudo dnf upgrade --refresh -y
sudo dnf install -y ipa-server ipa-server-dns openldap-clients \
  bind-utils chrony firewalld openssl openssh-server open-vm-tools

sudo systemctl enable --now chronyd firewalld sshd vmtoolsd
sudo timedatectl set-timezone UTC
getent hosts idm01.lab.test
dig @172.25.250.2 docs.redhat.com +short
chronyc tracking
getenforce
sudo reboot
```

Continue only when the hostname resolves to `.30`, the upstream DNS query works, time is synchronized, and SELinux reports `Enforcing`. Leave IPv6 enabled for IdM, even though this lab uses IPv4 addresses.

**Command overview:** `nmcli` applies the static network settings; `hostnamectl` sets the directory hostname; `sudoedit` edits the hosts file; `dnf` installs IdM and its tools; `chronyc` checks time; `dig` tests DNS; `getenforce` checks SELinux.

**Summary:** The directory VM has its own fixed address and the packages needed for IdM.

References:

- [Red Hat IdM Preparation Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/installing_identity_management/preparing-the-system-for-idm-server-installation): This guide describes IdM prerequisites, required packages, networking, and installation permissions.

---
