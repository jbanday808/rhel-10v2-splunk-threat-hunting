# RHEL 10.2 Splunk Threat Hunting Lab with LDAP Integration

This complete guide uses VMware Workstation Pro, a RHEL Splunk server, a Windows 11 hunting VM, and a separate RHEL Identity Management directory server. It preserves the `172.25.250.0/24` network and adds verified LDAPS sign-in with group-based Splunk access.

The guide now has **52 steps**. **Steps 31–44** cover the directory integration. If the original lab is already complete through its dashboard and analyst role, begin at Step 31; otherwise follow the steps in order. The remaining original sections have been renumbered to Steps 45–52.

The LDAP provider selected for this addition is **Red Hat IdM**. Windows 11 remains the hunting endpoint. VS Code with WSL remains the final documentation and GitHub workspace. LDAP authentication does not enroll the VMs into a domain or forward directory-server logs automatically.

The procedures and example commands require execution and validation on your VMs. Record observed results in the included checklists; no live connection tests are claimed here.

---

**Step 1 — Confirm the IP address plan**

Your screenshot confirms VMnet8 uses subnet `172.25.250.0` with mask `255.255.255.0`. Configure or confirm the remaining values:

| Component                      | Address or setting |
| ------------------------------ | ------------------ |
| VMware network                 | `VMnet8 — NAT`     |
| Network                        | `172.25.250.0/24`  |
| Subnet mask                    | `255.255.255.0`    |
| Physical host’s VMnet8 adapter | `172.25.250.1`     |
| NAT gateway                    | `172.25.250.2`     |
| RHEL Splunk server             | `172.25.250.10`    |
| Windows hunting VM             | `172.25.250.20`    |
| Gateway for all three VMs | `172.25.250.2` |
| Initial DNS for the original VMs | `172.25.250.2` |
| RHEL IdM directory server | `172.25.250.30` |
| Final DNS for Splunk after Step 35 | `172.25.250.30` |
| Final DNS for IdM after Step 33 | `172.25.250.30` |
| Windows hunting VM DNS | `172.25.250.2` |
| DHCP starting address          | `172.25.250.100`   |
| DHCP ending address            | `172.25.250.200`   |

The gateway and DHCP values are settings to configure or confirm because those details were not displayed in your screenshot.

In VMware Workstation Pro:

1. Open **Edit → Virtual Network Editor**.
2. Click **Change Settings**.
3. Select **VMnet8**.
4. Keep **NAT** selected.
5. Keep subnet `172.25.250.0` and mask `255.255.255.0`.
6. Open **NAT Settings** and confirm gateway `172.25.250.2`.
7. Open **DHCP Settings** and configure `.100–.200`.
8. Keep the host virtual adapter connected.
9. Click **Apply → OK**.

For the physical host’s **VMnet8 adapter**, use `.1` and the subnet mask. Leave its gateway and DNS fields blank.

Confirm `.10`, `.20`, and `.30` are available before assigning them. The IdM VM initially uses `.2` for DNS while packages are installed; it hosts DNS at `.30` after Step 33. Splunk switches to that DNS server in Step 35. All three VMs keep the NAT gateway at `.2`.

VMware NAT supplies a private network shared by the host and VMs, with outbound access through the host. This lab does not require inbound NAT port forwarding. [knowledge.broadcom.com](https://knowledge.broadcom.com/external/article/339371/using-the-virtual-network-editor-in-vmwa.html?utm_source=chatgpt.com)

---

**Step 2 — Understand the Splunk components**

| Component                                        | Simple explanation                                               | Placement                                          |
| ------------------------------------------------ | ---------------------------------------------------------------- | -------------------------------------------------- |
| **Indexer**                                      | Receives and stores records so you can search them later.        | RHEL                                               |
| **Universal Forwarder**                          | Collects records from a computer and sends them to Splunk.       | Windows VM                                         |
| **Heavy Forwarder**                              | Can organize or filter records before sending them onward.       | Optional future RHEL VM                            |
| **Search Head**                                  | Provides searches, dashboards, reports, and alerts.              | Same RHEL server                                   |
| **Search Peer**                                  | Searches its stored records when another Search Head asks it to. | Used when you separate the Search Head and indexer |
| **Deployment Server**                            | Distributes settings and apps to forwarders.                     | Optional future expansion                          |
| **License Manager**, formerly **License Master** | Coordinates Splunk license use across servers.                   | This standalone server uses its local license      |

A Universal Forwarder does not provide full indexing and searching. A Deployment Server distributes configuration; it does not carry the endpoint’s event traffic. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/forward-and-process-data/forwarding-and-receiving-data/10.4/introduction-to-forwarding/types-of-forwarders?utm_source=chatgpt.com)

This updated guide builds **three VMs**: a RHEL Splunk server, a Windows hunting endpoint, and a separate RHEL IdM directory server. LDAP sign-in is configured on the Splunk search interface; additional Splunk Enterprise roles would also run on RHEL if you expand the lab.

---

**Step 3 — Plan the VM resources**

| Setting | RHEL Splunk server | Windows hunting VM | RHEL directory server |
| --- | --- | --- | --- |
| Name | `RHEL-SPLUNK01` | `WINHUNT01` | `RHEL-IDM01` |
| Operating system | RHEL 10.2 x64 | Windows 11 x64 | RHEL 10.2 x64 |
| Virtual CPUs | 8 total | 4 total | 4 total |
| Memory | 16 GB | 8 GB | 8 GB |
| OS disk | 100 GB | 100 GB | 60 GB |
| Additional data disk | 250 GB | Not required | Not required |
| Firmware | UEFI | UEFI | UEFI |
| Secure Boot | Enabled | Enabled | Enabled |
| Virtual TPM | Not required | TPM 2.0 | Not required |
| Network | Custom: VMnet8 | Custom: VMnet8 | Custom: VMnet8 |

These are small learning-lab sizes. The three VMs allocate 32 GB RAM in total, so leave additional memory for the physical Windows host. A **64 GB host** is a practical target for running all three together. Create the separate directory VM in Step 32.

---

**Step 4 — Download and verify the software**

Download:

1. RHEL 10.2 x86_64 ISO.
2. Windows 11 x64 ISO.
3. Splunk Enterprise Linux x64 `.tgz`.
4. Compatible Windows x64 Universal Forwarder `.msi`.
5. Splunk Add-on for Microsoft Windows.
6. Splunk Add-on for Sysmon.

Official pages:

- [Red Hat Enterprise Linux](https://developers.redhat.com/products/rhel/download)
- [Windows 11](https://www.microsoft.com/software-download/windows11)
- [Splunk Enterprise](https://www.splunk.com/en_us/download/splunk-enterprise.html)
- [Universal Forwarder](https://www.splunk.com/en_us/download/universal-forwarder.html)
- [Microsoft Windows add-on](https://splunkbase.splunk.com/app/742?utm_source=chatgpt.com)
- [Sysmon add-on](https://splunkbase.splunk.com/app/5709?utm_source=chatgpt.com)

Choose add-on releases that explicitly support your selected Splunk version. [splunkbase.splunk.com](https://splunkbase.splunk.com/app/742?utm_source=chatgpt.com)

On your **physical Windows computer**, check downloaded files with PowerShell:

```
$Download = Read-Host 'Enter the full path to the downloaded file'

Get-FileHash -LiteralPath $Download -Algorithm SHA256
```

**Command overview:**

- `Read-Host` asks for the file location.
- `Get-FileHash` calculates its fingerprint.
- `SHA256` selects the fingerprint method.

Compare the complete result with the vendor’s published checksum.

---

**Step 5 — Create and install the RHEL VM**

In VMware Workstation Pro:

1. Select **File → New Virtual Machine**.
2. Choose **Custom** to review the hardware.
3. Select a supported virtual hardware version.
4. Select your RHEL ISO.
5. Select the appropriate RHEL x64 guest option.
6. Name the VM `RHEL-SPLUNK01`.
7. Assign 16 GB RAM and 8 total virtual CPUs.
8. Select UEFI and Secure Boot.
9. Create a 100 GB OS disk.
10. Add a **separate new 250 GB disk**.
11. Select **Custom → VMnet8**.
12. Enable **Connected** and **Connect at power on**.

Confirm that your Workstation release supports the selected RHEL guest and kernel. Broadcom’s support table distinguishes support by Workstation release. [knowledge.broadcom.com](https://knowledge.broadcom.com/external/article/315653?utm_source=chatgpt.com)

During RHEL installation:

1. Select your language and keyboard.
2. Choose **Minimal Install**.
3. Enable networking.
4. Select **only the 100 GB disk** for the OS.
5. Leave the 250 GB disk untouched.
6. Give `/` approximately 70 GB or more.
7. Create `labadmin` with administrator privileges.
8. Keep SELinux enabled.
9. Complete installation and reboot.
10. Disconnect the ISO.

If RHEL is already installed, begin with the verification commands below.

---

**Step 6 — Configure RHEL networking**

Run from the **RHEL VM console**:

```
cat /etc/redhat-release

uname -m

id

nmcli -f NAME,DEVICE,TYPE connection show --active

ip -brief address
```

**Command overview:**

| Command                   | Explanation                       |
| ------------------------- | --------------------------------- |
| `cat /etc/redhat-release` | Shows the RHEL version.           |
| `uname -m`                | Shows the processor architecture. |
| `id`                      | Shows your account and groups.    |
| `nmcli`                   | Lists network profiles.           |
| `ip -brief address`       | Shows network addresses.          |

Set the fixed address:

```
read -r -p 'Enter the active Ethernet profile name: ' NET_PROFILE

sudo nmcli connection modify "$NET_PROFILE" \
  ipv4.method manual \
  ipv4.addresses 172.25.250.10/24 \
  ipv4.gateway 172.25.250.2 \
  ipv4.dns 172.25.250.2

sudo nmcli connection up "$NET_PROFILE"

sudo hostnamectl set-hostname splunk01.lab.test
```

Update the lab-name records:

```
sudo cp -a /etc/hosts /etc/hosts.before-siem

sudo sed -i \
  -e '/splunk01\.lab\.test/d' \
  -e '/winhunt01\.lab\.test/d' \
  /etc/hosts

printf '\n172.25.250.10 splunk01.lab.test splunk01\n172.25.250.20 winhunt01.lab.test winhunt01\n' \
  | sudo tee -a /etc/hosts

ip route

getent hosts splunk01.lab.test
```

**Command overview:**

- `sudo` runs a command with administrator permission.
- `read` stores the profile name.
- `nmcli connection modify` changes network settings.
- `nmcli connection up` applies them.
- `hostnamectl` sets the server name.
- `cp -a` preserves a backup.
- `sed` removes previous lab-name entries.
- `printf` produces the new entries.
- `tee -a` adds them to the file.
- `getent hosts` checks name resolution.

---

**Step 7 — Register, update, and prepare RHEL**

If not already registered:

```
sudo subscription-manager register
```

Then:

```
sudo subscription-manager identity

sudo subscription-manager repos --list-enabled

sudo subscription-manager release --list
```

If `10.2` appears in the release list:

```
sudo subscription-manager release --set=10.2
```

Resolve any registration or release-selection problem before continuing.

Install updates and tools:

```
sudo dnf upgrade --refresh -y

sudo dnf install -y \
  chrony firewalld openssl tar gzip curl \
  openssh-server openssh-clients \
  rsyslog logrotate audit acl parted xfsprogs \
  util-linux policycoreutils policycoreutils-python-utils \
  procps-ng python3 open-vm-tools
```

Enable services:

```
sudo systemctl enable --now \
  chronyd firewalld rsyslog sshd vmtoolsd

sudo timedatectl set-timezone UTC

chronyc tracking

chronyc sources -v

sudo reboot
```

**Command overview:**

| Command                  | Explanation                                    |
| ------------------------ | ---------------------------------------------- |
| `subscription-manager`   | Manages registration and software access.      |
| `dnf upgrade`            | Installs updates.                              |
| `dnf install`            | Installs the named tools.                      |
| `systemctl enable --now` | Starts services and enables automatic startup. |
| `timedatectl`            | Sets the time zone.                            |
| `chronyc`                | Checks clock synchronization.                  |
| `reboot`                 | Restarts RHEL.                                 |

After restarting:

```
cat /etc/redhat-release

getenforce

df -h /
```

Confirm RHEL 10.2, SELinux `Enforcing`, and sufficient free space.

---

**Step 8 — Create the project folders on RHEL**

```
mkdir -p "$HOME/rhel-splunk-threat-hunting"

cd "$HOME/rhel-splunk-threat-hunting"

mkdir -p \
  apps/LAB_SIEM/local \
  apps/LAB_SIEM/metadata \
  apps/LAB_SIEM/default/data/ui/views \
  apps/LAB_UF_WINDOWS/local \
  configs/rsyslog \
  configs/logrotate \
  scripts/rhel \
  scripts/windows \
  sysmon \
  hunts \
  docs/reference \
  docs/images \
  evidence/sanitized \
  evidence/raw

mkdir -p "$HOME/siem-downloads"

touch README.md docs/reference/versions.md
```

**Command overview:**

- `mkdir -p` creates folders and missing parents.
- `cd` selects the working folder.
- `touch` creates empty files.

Create `.gitignore`:

```
cat > .gitignore <<'EOF'
downloads/
private/
backups/
evidence/raw/
.env
*.key
*.pem
*.pfx
*.p12
*.csr
*.srl
*.iso
*.vmdk
*.vmem
*.vmss
*.nvram
*.msi
*.exe
*.evtx
*.log
*.tgz
*.tar.gz
*.zip
__pycache__/
Thumbs.db
.DS_Store
EOF
```

Create `.gitattributes`:

```
cat > .gitattributes <<'EOF'
* text=auto
*.sh text eol=lf
*.conf text eol=lf
*.meta text eol=lf
*.xml text eol=lf
*.spl text eol=lf
*.md text eol=lf
*.ps1 text eol=crlf
EOF
```

**Command overview:**

- `cat > filename` creates or replaces a file.
- `<<'EOF'` preserves the enclosed text exactly.
- `.gitignore` excludes private and unnecessary files.
- `.gitattributes` keeps line endings consistent.

At the start of another RHEL terminal session, return to the project:

```
cd "$HOME/rhel-splunk-threat-hunting"
```

---

**Step 9 — Understand the configuration files**

Use Splunk’s exact filenames: **`outputs.conf`** and **`transforms.conf`**.

| File              | Simple explanation                                    |
| ----------------- | ----------------------------------------------------- |
| `inputs.conf`     | Chooses records to collect or receive.                |
| `outputs.conf`    | Tells the collector where to send records.            |
| `props.conf`      | Tells Splunk how to read each entry.                  |
| `transforms.conf` | Defines rules for extracting useful details.          |
| `indexes.conf`    | Creates separate storage areas and sets their limits. |
| `authentication.conf` | Connects Splunk sign-in to the directory and maps groups to roles. |
| `authorize.conf` | Defines the actions and indexes each Splunk role can use. |
| `etc/openldap/ldap.conf` | Requires certificate checks for Splunk LDAP connections. |

These files manage different stages of collecting, reading, forwarding, and storing records. [help.splunk.com](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/administer-splunk-enterprise-with-configuration-files/list-of-configuration-files?utm_source=chatgpt.com)

---

**Step 10 — Create the RHEL Splunk configuration**

Create the app information:

```
cat > apps/LAB_SIEM/local/app.conf <<'EOF'
[install]
is_configured = 1

[ui]
is_visible = true
label = Threat Hunting Lab

[launcher]
author = James Banday
version = 1.0.0
description = RHEL and Windows threat hunting with Splunk Enterprise
EOF
```

Create `server.conf`:

```
cat > apps/LAB_SIEM/local/server.conf <<'EOF'
[general]
serverName = splunk01
EOF
```

Create `indexes.conf`:

```
cat > apps/LAB_SIEM/local/indexes.conf <<'EOF'
[win_security]
homePath = /splunkdata/win_security/db
coldPath = /splunkdata/win_security/colddb
thawedPath = /splunkdata/win_security/thaweddb
maxTotalDataSizeMB = 20480
frozenTimePeriodInSecs = 2592000

[win_system]
homePath = /splunkdata/win_system/db
coldPath = /splunkdata/win_system/colddb
thawedPath = /splunkdata/win_system/thaweddb
maxTotalDataSizeMB = 10240
frozenTimePeriodInSecs = 2592000

[powershell]
homePath = /splunkdata/powershell/db
coldPath = /splunkdata/powershell/colddb
thawedPath = /splunkdata/powershell/thaweddb
maxTotalDataSizeMB = 10240
frozenTimePeriodInSecs = 1209600

[sysmon]
homePath = /splunkdata/sysmon/db
coldPath = /splunkdata/sysmon/colddb
thawedPath = /splunkdata/sysmon/thaweddb
maxTotalDataSizeMB = 30720
frozenTimePeriodInSecs = 1209600

[linux]
homePath = /splunkdata/linux/db
coldPath = /splunkdata/linux/colddb
thawedPath = /splunkdata/linux/thaweddb
maxTotalDataSizeMB = 10240
frozenTimePeriodInSecs = 2592000

[lab]
homePath = /splunkdata/lab/db
coldPath = /splunkdata/lab/colddb
thawedPath = /splunkdata/lab/thaweddb
maxTotalDataSizeMB = 5120
frozenTimePeriodInSecs = 604800
EOF
```

**File overview:** These indexes separate Windows security, Windows system/application, PowerShell, Sysmon, Linux, and custom test records.

| Setting                  | Explanation                                     |
| ------------------------ | ----------------------------------------------- |
| `homePath`               | Stores actively used data.                      |
| `coldPath`               | Stores older searchable data.                   |
| `thawedPath`             | Provides a location for restored archived data. |
| `maxTotalDataSizeMB`     | Sets the size limit.                            |
| `frozenTimePeriodInSecs` | Sets the age-based retirement target.           |

A size limit can retire data before the age target. Without archiving, retired buckets are deleted. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.1-configuration-file-reference/indexes.conf?utm_source=chatgpt.com)

Create the server’s `inputs.conf`:

```
cat > apps/LAB_SIEM/local/inputs.conf <<'EOF'
[splunktcp-ssl:9997]
disabled = 0

[SSL]
serverCert = /opt/splunk/etc/auth/lab/splunk01.pem
requireClientCert = false
sslVersions = tls1.2,tls1.3

[monitor:///var/log/siem-lab/linux.log]
disabled = 0
index = linux
sourcetype = syslog
host = splunk01

[monitor:///var/log/siem-lab/events.log]
disabled = 0
index = lab
sourcetype = siem:lab
host = splunk01

[WinEventLog://Security]
disabled = 1

[WinEventLog://System]
disabled = 1

[WinEventLog://Application]
disabled = 1

[WinEventLog://Microsoft-Windows-PowerShell/Operational]
disabled = 1

[WinEventLog://Microsoft-Windows-Sysmon/Operational]
disabled = 1
EOF
```

**File overview:** This receives encrypted records on port `9997` and collects two Linux files. Windows collection takes place on the Windows VM.

Create `props.conf`:

```
cat > apps/LAB_SIEM/local/props.conf <<'EOF'
[siem:lab]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = ^
TIME_FORMAT = %Y-%m-%dT%H:%M:%SZ
MAX_TIMESTAMP_LOOKAHEAD = 20
TZ = UTC
KV_MODE = none
REPORT-lab-fields = lab_fields
EOF
```

**File overview:** This describes the date and layout of custom test entries.

Create `transforms.conf`:

```
cat > apps/LAB_SIEM/local/transforms.conf <<'EOF'
[lab_fields]
REGEX = action=(\S+)\s+result=(\S+)\s+account=(\S+)
FORMAT = action::$1 result::$2 account::$3
EOF
```

**File overview:** This extracts the action, result, and account from the custom entry.

The custom rules apply only to `siem:lab`. The official add-ons interpret Windows and Sysmon records.

Create `web.conf`:

```
cat > apps/LAB_SIEM/local/web.conf <<'EOF'
[settings]
httpport = 8000
enableSplunkWebSSL = true
privKeyPath = /opt/splunk/etc/auth/lab/splunk01.key
serverCert = /opt/splunk/etc/auth/lab/fullchain.pem
sslVersions = tls1.2,tls1.3
EOF
```

**File overview:** This protects browser access with HTTPS.

---

**Step 11 — Create the Windows forwarder configuration**

Still on **RHEL**:

```
cat > apps/LAB_UF_WINDOWS/local/app.conf <<'EOF'
[install]
is_configured = 1

[ui]
is_visible = false

[launcher]
version = 1.0.0
description = Windows event collection and protected forwarding
EOF
```

Create Windows `inputs.conf`:

```
cat > apps/LAB_UF_WINDOWS/local/inputs.conf <<'EOF'
[default]
host = WINHUNT01

[WinEventLog://Security]
disabled = 0
index = win_security
renderXml = true
start_from = oldest
current_only = 0

[WinEventLog://System]
disabled = 0
index = win_system
renderXml = true
start_from = oldest
current_only = 0

[WinEventLog://Application]
disabled = 0
index = win_system
renderXml = true
start_from = oldest
current_only = 0

[WinEventLog://Microsoft-Windows-PowerShell/Operational]
disabled = 0
index = powershell
renderXml = true
start_from = oldest
current_only = 0

[WinEventLog://Microsoft-Windows-Sysmon/Operational]
disabled = 0
index = sysmon
sourcetype = XmlWinEventLog:Microsoft-Windows-Sysmon/Operational
renderXml = true
start_from = oldest
current_only = 0
EOF
```

**File overview:** This chooses the Windows channels to collect.

The `oldest` and `current_only = 0` settings read retained existing records and continue with new records. Monitor the initial backlog against your licensed allowance. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/inputs.conf?utm_source=chatgpt.com)

Create `outputs.conf`:

```
cat > apps/LAB_UF_WINDOWS/local/outputs.conf <<'EOF'
[tcpout]
defaultGroup = lab_tls

[tcpout:lab_tls]
server = splunk01.lab.test:9997
useACK = true
useSSL = true
sslVerifyServerCert = true
sslVerifyServerName = true
sslAltNameToCheck = splunk01.lab.test
sslVersions = tls1.2,tls1.3
EOF
```

**File overview:** This sends records to RHEL and verifies the receiving server’s identity.

Create Windows `server.conf`:

```
cat > apps/LAB_UF_WINDOWS/local/server.conf <<'EOF'
[sslConfig]
sslRootCAPath = C:\Program Files\SplunkUniversalForwarder\etc\auth\lab\ca.pem
caTrustStore = splunk
EOF
```

**File overview:** This identifies the public CA certificate trusted by the forwarder.

This setup verifies the receiving server without requiring a client certificate. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/outputs.conf?utm_source=chatgpt.com)

---

**Step 12 — Create the Sysmon rules**

On **RHEL**:

```
cat > sysmon/sysmon.xml <<'EOF'
<Sysmon schemaversion="4.82">
  <HashAlgorithms>SHA256</HashAlgorithms>
  <EventFiltering>
    <ProcessCreate onmatch="exclude" />

    <NetworkConnect onmatch="include">
      <Image condition="end with">powershell.exe</Image>
      <Image condition="end with">curl.exe</Image>
    </NetworkConnect>

    <FileCreate onmatch="include">
      <TargetFilename condition="begin with">C:\SIEMLab\TestFiles\</TargetFilename>
    </FileCreate>

    <RegistryEvent onmatch="include">
      <TargetObject condition="contains">\CurrentVersion\Run\SIEMLab</TargetObject>
    </RegistryEvent>

    <DnsQuery onmatch="include">
      <Image condition="end with">powershell.exe</Image>
    </DnsQuery>
  </EventFiltering>
</Sysmon>
EOF
```

**File overview:** This records process starts and selected network, file, registry, and DNS activity.

The empty process exclusion records all process starts. The other rules limit selected event types for the lab. [learn.microsoft.com](https://learn.microsoft.com/sysinternals/downloads/sysmon?utm_source=chatgpt.com)

---

**Step 13 — Create the service account and prepare storage**

On **RHEL**:

```
getent group splunk >/dev/null || sudo groupadd --system splunk

id splunk >/dev/null 2>&1 || sudo useradd --system \
  --gid splunk \
  --home-dir /opt/splunk \
  --no-create-home \
  --shell /sbin/nologin \
  splunk
```

**Command overview:**

- `getent` checks for the group.
- `id` checks for the account.
- `groupadd` creates the service group.
- `useradd` creates the service account.
- `/sbin/nologin` prevents normal interactive login.

Identify the new disk:

```
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
```

Create the storage script:

```
cat > scripts/rhel/prepare-storage.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

[[ $EUID -eq 0 ]] || {
  echo 'Run with sudo.' >&2
  exit 1
}

DISK=$(readlink -f "${1:?Provide the new blank data disk}")

[[ -b "$DISK" ]] || {
  echo 'Not a block device.' >&2
  exit 1
}

[[ $(lsblk -dn -o TYPE "$DISK") == disk ]] || {
  echo 'Select a whole disk.' >&2
  exit 1
}

[[ $(lsblk -nr -o NAME "$DISK" | wc -l) -eq 1 ]] || {
  echo 'Disk has child devices; stopping.' >&2
  exit 1
}

[[ -z $(lsblk -n -o MOUNTPOINTS "$DISK") ]] || {
  echo 'Disk is mounted; stopping.' >&2
  exit 1
}

SIGNATURES=$(wipefs -n --noheadings "$DISK")

[[ -z "$SIGNATURES" ]] || {
  echo 'Disk has existing signatures; stopping.' >&2
  exit 1
}

if findmnt --mountpoint /splunkdata >/dev/null ||
   grep -Eq '[[:space:]]/splunkdata[[:space:]]' /etc/fstab; then
  echo '/splunkdata is already configured; stopping.' >&2
  exit 1
fi

lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS "$DISK"

read -r -p "Type the full disk path ($DISK) to initialize it: " ANSWER
[[ "$ANSWER" == "$DISK" ]] || exit 1

parted --script "$DISK" mklabel gpt
parted --script "$DISK" mkpart primary xfs 1MiB 100%
partprobe "$DISK"
udevadm settle

PARTITION=$(lsblk -lnpo NAME,TYPE "$DISK" |
  awk '$2 == "part" {print $1; exit}')

[[ -b "$PARTITION" ]] || exit 1

mkfs.xfs -L SIEMDATA "$PARTITION"

mkdir -p /splunkdata

DATA_UUID=$(blkid -s UUID -o value "$PARTITION")

cp -a /etc/fstab "/etc/fstab.before-siem-$(date +%Y%m%dT%H%M%S)"

printf 'UUID=%s /splunkdata xfs defaults 0 0\n' "$DATA_UUID" >> /etc/fstab

systemctl daemon-reload
mount /splunkdata

chown splunk:splunk /splunkdata
chmod 750 /splunkdata

findmnt --mountpoint /splunkdata
df -h /splunkdata
EOF
```

Check and run it:

```
bash -n scripts/rhel/prepare-storage.sh

sudo bash scripts/rhel/prepare-storage.sh /dev/sdb
```

Use `/dev/sdb` only if it is the **new, empty 250 GB disk**. VMware may use another name, such as `/dev/nvme0n2`.

**Command overview:**

| Command             | Explanation                      |
| ------------------- | -------------------------------- |
| `bash -n`           | Checks script syntax.            |
| `wipefs -n`         | Inspects disk signatures.        |
| `parted`            | Creates the partition.           |
| `partprobe`         | Refreshes partition information. |
| `mkfs.xfs`          | Formats the selected partition.  |
| `blkid`             | Reads its stable identifier.     |
| `mount`             | Attaches the filesystem.         |
| `chown` and `chmod` | Set ownership and permissions.   |
| `findmnt` and `df`  | Verify the mounted disk.         |

Formatting erases the selected disk. The script refuses disks with detected partitions, mounts, or signatures.

---

**Step 14 — Transfer and install Splunk Enterprise**

On the **RHEL console**, display the SSH fingerprint:

```
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
```

On the **physical Windows host**:

```
Get-Command ssh.exe,scp.exe
```

If missing, use administrator PowerShell:

```
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

Copy the package:

```
$SplunkPackage = Read-Host 'Full path to the Linux Splunk .tgz'

scp.exe $SplunkPackage labadmin@172.25.250.10:/home/labadmin/siem-downloads/
```

Compare the SSH fingerprint before accepting the first connection.

Back on **RHEL**:

```
read -r -p 'Full path to the staged Splunk .tgz: ' SPLUNK_PACKAGE

read -r -p 'Official SHA-256 checksum from Splunk: ' SPLUNK_SHA256

printf '%s  %s\n' "$SPLUNK_SHA256" "$SPLUNK_PACKAGE" \
  | sha256sum --check -
```

Continue when it reports `OK`:

```
sudo tar -xzf "$SPLUNK_PACKAGE" -C /opt

sudo chown -R splunk:splunk /opt/splunk

sudo -u splunk /opt/splunk/bin/splunk start --accept-license
```

Create the Splunk web administrator named `admin`.

Then:

```
sudo -u splunk /opt/splunk/bin/splunk stop
```

**Command overview:**

- `ssh-keygen -lf` displays the SSH identity.
- `scp` copies the package securely.
- `sha256sum --check` verifies it.
- `tar -xzf` extracts it.
- `-C /opt` selects the destination.
- `chown -R` assigns ownership.
- `sudo -u splunk` runs Splunk under its service account.
- `start --accept-license` initializes the software.
- `stop` stops the initial instance.

If `/opt/splunk` already contains an installation, inspect it before extracting another package over it.

---

**Step 15 — Create the lab certificates**

On **RHEL**:

```
sudo -i
```

Create a protected working folder:

```
umask 077

mkdir -p /root/siem-lab-pki

cd /root/siem-lab-pki
```

If this folder contains a working CA, preserve it and use it to issue the updated server certificate.

For a new CA:

```
openssl req -x509 -newkey rsa:3072 -sha256 -days 1825 \
  -keyout ca.key \
  -out ca.pem \
  -subj '/CN=SIEM Lab Root CA' \
  -addext 'basicConstraints=critical,CA:TRUE' \
  -addext 'keyUsage=critical,keyCertSign,cRLSign'
```

Enter a strong passphrase.

Create the server request:

```
openssl req -new -newkey rsa:3072 -noenc \
  -keyout splunk01.key \
  -out splunk01.csr \
  -subj '/CN=splunk01.lab.test'
```

Create the certificate settings:

```
cat > splunk01.ext <<'EOF'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:splunk01.lab.test,DNS:splunk01,IP:172.25.250.10
EOF
```

Sign the server certificate:

```
openssl x509 -req \
  -in splunk01.csr \
  -CA ca.pem \
  -CAkey ca.key \
  -CAcreateserial \
  -out splunk01.crt \
  -days 365 \
  -sha256 \
  -extfile splunk01.ext
```

Create and verify the files:

```
cat splunk01.crt splunk01.key ca.pem > splunk01.pem

cat splunk01.crt ca.pem > fullchain.pem

openssl x509 -in ca.pem -outform DER -out ca.cer

openssl verify -CAfile ca.pem splunk01.crt

openssl x509 -in splunk01.crt -noout -dates -ext subjectAltName
```

Install them:

```
install -d -o splunk -g splunk -m 700 /opt/splunk/etc/auth/lab

install -o splunk -g splunk -m 600 \
  splunk01.pem splunk01.key fullchain.pem ca.pem \
  /opt/splunk/etc/auth/lab/
```

Prepare only the public CA files for transfer:

```
install -d -m 755 /home/labadmin/siem-public

install -m 644 ca.pem ca.cer /home/labadmin/siem-public/

sha256sum \
  /home/labadmin/siem-public/ca.pem \
  /home/labadmin/siem-public/ca.cer

exit
```

**Command overview:**

| Command or option   | Explanation                               |
| ------------------- | ----------------------------------------- |
| `sudo -i`           | Opens an administrator shell.             |
| `umask 077`         | Makes new files private.                  |
| `openssl req -x509` | Creates the CA certificate.               |
| `-newkey rsa:3072`  | Creates an RSA key.                       |
| `-days`             | Sets certificate lifetime.                |
| `openssl req -new`  | Creates the server’s signing request.     |
| `-noenc`            | Allows unattended service startup.        |
| `subjectAltName`    | Lists valid names and the server address. |
| `openssl verify`    | Checks the certificate chain.             |
| `install -m 600`    | Restricts private-file access.            |
| `exit`              | Returns to `labadmin`.                    |

Keep private keys outside the project. Renew the server certificate before its one-year expiry.

Splunk supports custom certificates for forwarding and browser connections. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/secure-splunk-platform-communications-with-transport-layer-security-certificates/configure-splunk-indexing-and-forwarding-to-use-tls-certificates?utm_source=chatgpt.com)

---

**Step 16 — Configure Linux logging**

On **RHEL**:

```
cd "$HOME/rhel-splunk-threat-hunting"
```

Create the logging settings:

```
cat > configs/rsyslog/30-siem-lab.conf <<'EOF'
if ($syslogfacility-text == "auth" or $syslogfacility-text == "authpriv" or $programname == "siem-lab") then {
    action(type="omfile"
        file="/var/log/siem-lab/linux.log"
        fileOwner="root"
        fileGroup="splunk"
        fileCreateMode="0640"
        template="RSYSLOG_TraditionalFileFormat")
}
EOF
```

Create rotation settings:

```
cat > configs/logrotate/siem-lab <<'EOF'
/var/log/siem-lab/*.log {
    daily
    rotate 7
    missingok
    notifempty
    compress
    delaycompress
    create 0640 root splunk
    sharedscripts
    postrotate
        /usr/bin/systemctl kill -s HUP rsyslog.service >/dev/null 2>&1 || true
    endscript
}
EOF
```

Create the actual files:

```
sudo install -d -o root -g splunk -m 750 /var/log/siem-lab

sudo touch \
  /var/log/siem-lab/linux.log \
  /var/log/siem-lab/events.log

sudo chown root:splunk /var/log/siem-lab/*.log

sudo chmod 640 /var/log/siem-lab/*.log
```

Deploy and verify:

```
sudo install -m 644 \
  configs/rsyslog/30-siem-lab.conf \
  /etc/rsyslog.d/30-siem-lab.conf

sudo install -m 644 \
  configs/logrotate/siem-lab \
  /etc/logrotate.d/siem-lab

sudo restorecon -RF /var/log/siem-lab

sudo rsyslogd -N1

sudo systemctl restart rsyslog

sudo logrotate --debug /etc/logrotate.d/siem-lab
```

Generate test records:

```
logger -p authpriv.notice -t siem-lab \
  'SIEM-LAB-LINUX-PIPELINE-TEST'

printf '%s action=pipeline_check result=success account=labadmin\n' \
  "$(date -u +%FT%TZ)" \
  | sudo tee -a /var/log/siem-lab/events.log
```

**Command overview:**

- `install -d` creates a folder with defined permissions.
- `touch` creates files.
- `install` deploys configuration.
- `restorecon` restores SELinux labels.
- `rsyslogd -N1` checks logging settings.
- `logrotate --debug` checks rotation rules.
- `logger` writes a test entry.
- `date -u` produces a UTC timestamp.

---

**Step 17 — Deploy the Splunk app and automatic startup**

```
sudo cp -a apps/LAB_SIEM /opt/splunk/etc/apps/

sudo chown -R splunk:splunk /opt/splunk/etc/apps/LAB_SIEM

sudo find /opt/splunk/etc/apps/LAB_SIEM \
  -type d -exec chmod 750 {} +

sudo find /opt/splunk/etc/apps/LAB_SIEM \
  -type f -exec chmod 640 {} +
```

Enable automatic startup:

```
sudo /opt/splunk/bin/splunk enable boot-start \
  -systemd-managed 1 \
  -user splunk \
  -group splunk
```

Create the service override:

```
sudo mkdir -p /etc/systemd/system/Splunkd.service.d

sudo tee /etc/systemd/system/Splunkd.service.d/lab.conf > /dev/null <<'EOF'
[Unit]
RequiresMountsFor=/splunkdata

[Service]
LimitNOFILE=65536
LimitNPROC=16000
TasksMax=16000
EOF
```

Check and start:

```
sudo -u splunk /opt/splunk/bin/splunk btool check

sudo systemctl daemon-reload

sudo systemctl enable --now Splunkd

sudo systemctl status Splunkd --no-pager
```

**Command overview:**

- `cp -a` copies the app.
- `find ... -exec chmod` applies permissions.
- `enable boot-start` creates automatic startup.
- `RequiresMountsFor` requires the data disk before startup.
- `btool check` checks configuration.
- `systemctl` loads and starts the service.

Splunk documents this systemd startup method. [help.splunk.com](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/start-splunk-enterprise-and-perform-initial-tasks/run-splunk-enterprise-as-a-systemd-service?utm_source=chatgpt.com)

---

**Step 18 — Configure the RHEL firewall**

Use the **RHEL VM console**:

```
nmcli -f NAME,DEVICE,TYPE connection show --active

read -r -p 'Enter the Ethernet profile name: ' NET_PROFILE

sudo firewall-cmd --permanent --new-zone=siem-lab
```

If the zone already exists, inspect it and skip recreating it.

Allow host and Windows VM administration:

```
for SOURCE_IP in 172.25.250.1 172.25.250.20; do
  for PORT in 22 8000; do
    sudo firewall-cmd --permanent --zone=siem-lab \
      --add-rich-rule="rule family=ipv4 source address=$SOURCE_IP/32 port port=$PORT protocol=tcp accept"
  done
done
```

Allow event forwarding:

```
sudo firewall-cmd --permanent --zone=siem-lab \
  --add-rich-rule='rule family=ipv4 source address=172.25.250.20/32 port port=9997 protocol=tcp accept'
```

Apply:

```
sudo firewall-cmd --reload

sudo nmcli connection modify "$NET_PROFILE" connection.zone siem-lab

sudo nmcli connection up "$NET_PROFILE"

sudo firewall-cmd --get-active-zones

sudo firewall-cmd --zone=siem-lab --list-all
```

**Command overview:**

- `--permanent` saves the rules.
- `--new-zone` creates a dedicated rule set.
- `--add-rich-rule` permits a specific source and port.
- `--reload` applies saved settings.
- `connection.zone` assigns the adapter.

| Port     | Purpose               | Allowed source      |
| -------- | --------------------- | ------------------- |
| TCP 22   | SSH and file transfer | Host and Windows VM |
| TCP 8000 | Splunk HTTPS          | Host and Windows VM |
| TCP 9997 | Encrypted forwarding  | Windows VM          |
| TCP 8089 | Splunk management     | Not opened remotely |

---

**Step 19 — Verify the server**

```
sudo systemctl show Splunkd -p User -p Group -p LimitNOFILE

findmnt --mountpoint /splunkdata

sudo ss -lntp

getenforce

sudo -u splunk /opt/splunk/bin/splunk btool inputs list --debug

sudo -u splunk /opt/splunk/bin/splunk btool indexes list --debug

sudo -u splunk /opt/splunk/bin/splunk btool props list siem:lab --debug

sudo -u splunk /opt/splunk/bin/splunk btool transforms list lab_fields --debug
```

Check HTTPS:

```
curl --cacert /home/labadmin/siem-public/ca.pem \
  https://splunk01.lab.test:8000/en-US/account/login \
  -o /dev/null \
  -w '%{http_code}\n'
```

**Command overview:**

- `systemctl show` checks service ownership.
- `ss -lntp` shows listening services.
- `btool --debug` shows effective settings and source files.
- `curl --cacert` verifies HTTPS using the lab CA.

Confirm:

- Splunk runs as `splunk`.
- `/splunkdata` is mounted.
- SELinux is `Enforcing`.
- Ports `8000` and `9997` are listening.
- HTTPS validates.

---

**Step 20 — Open Splunk and install the add-ons**

On the **physical Windows host**, use administrator PowerShell:

```
New-Item -ItemType Directory -Path C:\SIEMLab\Public -Force

scp.exe labadmin@172.25.250.10:/home/labadmin/siem-public/ca.cer C:\SIEMLab\Public\

Get-FileHash C:\SIEMLab\Public\ca.cer -Algorithm SHA256
```

Compare the hash with RHEL.

Import the public CA:

```
Import-Certificate `
  -FilePath C:\SIEMLab\Public\ca.cer `
  -CertStoreLocation Cert:\CurrentUser\Root
```

Update the server name:

```
$HostsFile = "$env:SystemRoot\System32\drivers\etc\hosts"

$HostsLines = Get-Content $HostsFile |
    Where-Object { $_ -notmatch 'splunk01\.lab\.test' }

$HostsLines = @($HostsLines) +
    '172.25.250.10 splunk01.lab.test splunk01'

Set-Content -Path $HostsFile -Value $HostsLines -Encoding Ascii

Start-Process 'https://splunk01.lab.test:8000'
```

**Command overview:**

- `Import-Certificate` trusts the verified public CA.
- `Get-Content` reads the hosts file.
- `Where-Object` removes the previous lab-name entry.
- `Set-Content` writes the updated entry.
- `Start-Process` opens Splunk.

In Splunk:

1. Sign in as `admin`.
2. Open **Apps → Manage Apps → Install app from file**.
3. Install the Microsoft Windows add-on.
4. Install the Sysmon add-on.
5. Restart when requested.
6. Open **Settings → Licensing**.
7. Record the allowance and expiry.

Splunk Enterprise Security is a separate product. This core lab uses Enterprise searches, dashboards, and alerts.

---

**Step 21 — Create and install the Windows VM**

In VMware Workstation Pro:

1. Create `WINHUNT01`.
2. Assign 8 GB RAM and 4 total virtual CPUs.
3. Create a 100 GB disk.
4. Select UEFI and Secure Boot.
5. Enable the encryption required for the virtual TPM.
6. Add TPM 2.0.
7. Attach the adapter to VMnet8.
8. Install Windows 11.
9. Create your administrator account.
10. Install Windows updates.
11. Install VMware Tools.
12. Restart.

Keep the VM encryption password securely.

VMware documents Secure Boot, encryption, and virtual TPM setup for Windows 11 guests. [knowledge.broadcom.com](https://knowledge.broadcom.com/external/article/315650?utm_source=chatgpt.com)

Inside the **Windows VM**, open administrator Windows PowerShell:

```
Rename-Computer -NewName WINHUNT01 -Restart
```

After restarting:

```
Get-NetAdapter | Format-Table Name,InterfaceIndex,Status,MacAddress
```

For a fresh VM with one adapter named `Ethernet`:

```
$Adapter = Get-NetAdapter -Name Ethernet

Set-NetIPInterface `
  -InterfaceIndex $Adapter.ifIndex `
  -AddressFamily IPv4 `
  -Dhcp Disabled

New-NetIPAddress `
  -InterfaceIndex $Adapter.ifIndex `
  -IPAddress 172.25.250.20 `
  -PrefixLength 24 `
  -DefaultGateway 172.25.250.2

Set-DnsClientServerAddress `
  -InterfaceIndex $Adapter.ifIndex `
  -ServerAddresses 172.25.250.2

Get-NetIPConfiguration

w32tm.exe /query /status
```

Substitute the actual adapter name if different.

**Command overview:**

- `Rename-Computer` sets the guest name.
- `Get-NetAdapter` identifies its adapter.
- `Set-NetIPInterface` disables DHCP.
- `New-NetIPAddress` sets the fixed address.
- `Set-DnsClientServerAddress` sets DNS.
- `w32tm` checks the clock.

---

**Step 22 — Transfer the Windows configuration**

On **RHEL**:

```
cd "$HOME/rhel-splunk-threat-hunting"

tar -czf "$HOME/endpoint-config.tgz" \
  apps/LAB_UF_WINDOWS \
  sysmon
```

**Command overview:** `tar -czf` packages the forwarding settings and Sysmon rules.

Inside the **Windows VM**:

```
New-Item -ItemType Directory -Force -Path `
  C:\SIEMLab\Downloads, `
  C:\SIEMLab\Source, `
  C:\SIEMLab\Tools, `
  C:\SIEMLab\Public, `
  C:\SIEMLab\Evidence, `
  C:\SIEMLab\TestFiles
```

Check the SSH client:

```
Get-Command scp.exe
```

If missing:

```
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

Transfer and extract:

```
scp.exe labadmin@172.25.250.10:/home/labadmin/endpoint-config.tgz C:\SIEMLab\Downloads\

tar.exe -xzf C:\SIEMLab\Downloads\endpoint-config.tgz -C C:\SIEMLab\Source

scp.exe labadmin@172.25.250.10:/home/labadmin/siem-public/ca.pem C:\SIEMLab\Public\

scp.exe labadmin@172.25.250.10:/home/labadmin/siem-public/ca.cer C:\SIEMLab\Public\

Get-FileHash C:\SIEMLab\Public\ca.pem,C:\SIEMLab\Public\ca.cer -Algorithm SHA256
```

Compare certificate hashes with RHEL.

Update the server name:

```
$HostsFile = "$env:SystemRoot\System32\drivers\etc\hosts"

$HostsLines = Get-Content $HostsFile |
    Where-Object { $_ -notmatch 'splunk01\.lab\.test' }

$HostsLines = @($HostsLines) +
    '172.25.250.10 splunk01.lab.test splunk01'

Set-Content -Path $HostsFile -Value $HostsLines -Encoding Ascii
```

**Command overview:**

- `New-Item` creates folders.
- `scp` copies files securely.
- `tar.exe -xzf` extracts them.
- `Get-FileHash` checks transferred certificates.
- The hosts-file commands update local name resolution.

---

**Step 23 — Enable Windows auditing and PowerShell logging**

Inside the **Windows VM**, use administrator PowerShell:

```
auditpol.exe /backup /file:C:\SIEMLab\Evidence\audit-policy-before.csv
```

Enable audit categories:

```
$AuditCategories = @(
    '{0CCE9215-69AE-11D9-BED3-505054503030}',
    '{0CCE922B-69AE-11D9-BED3-505054503030}',
    '{0CCE9235-69AE-11D9-BED3-505054503030}',
    '{0CCE9237-69AE-11D9-BED3-505054503030}',
    '{0CCE9227-69AE-11D9-BED3-505054503030}'
)

foreach ($Category in $AuditCategories) {
    auditpol.exe /set "/subcategory:$Category" /success:enable /failure:enable
}
```

These cover sign-ins, process creation, account changes, group changes, and other object access such as scheduled-task auditing.

Enable command-line information:

```
$AuditPath = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System\Audit'

New-Item -Path $AuditPath -Force | Out-Null

New-ItemProperty `
  -Path $AuditPath `
  -Name ProcessCreationIncludeCmdLine_Enabled `
  -PropertyType DWord `
  -Value 1 `
  -Force | Out-Null
```

Enable advanced audit-policy precedence:

```
New-ItemProperty `
  -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' `
  -Name SCENoApplyLegacyAuditPolicy `
  -PropertyType DWord `
  -Value 1 `
  -Force | Out-Null
```

Enable PowerShell script logging:

```
$PowerShellPath = 'HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'

New-Item -Path $PowerShellPath -Force | Out-Null

New-ItemProperty `
  -Path $PowerShellPath `
  -Name EnableScriptBlockLogging `
  -PropertyType DWord `
  -Value 1 `
  -Force | Out-Null
```

Enable and resize event logs:

```
wevtutil.exe sl Microsoft-Windows-PowerShell/Operational /e:true /ms:134217728

wevtutil.exe sl Security /ms:536870912

wevtutil.exe sl System /ms:134217728

wevtutil.exe sl Application /ms:134217728
```

**Command overview:**

| Command            | Explanation                        |
| ------------------ | ---------------------------------- |
| `auditpol /backup` | Saves original audit settings.     |
| `auditpol /set`    | Enables selected activity records. |
| `New-Item`         | Creates a settings location.       |
| `New-ItemProperty` | Sets the logging option.           |
| `wevtutil sl`      | Enables or resizes event logs.     |

Windows requires the command-line policy to include command details in Event 4688. [learn.microsoft.com](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/auditpol?utm_source=chatgpt.com)

Open a new PowerShell window before later tests.

---

**Step 24 — Install Sysmon**

Check for an existing installation:

```
Get-Service -Name Sysmon,Sysmon64 -ErrorAction SilentlyContinue

Get-WindowsOptionalFeature `
  -Online `
  -FeatureName Sysmon `
  -ErrorAction SilentlyContinue
```

If built-in Sysmon is active:

```
sysmon.exe -c C:\SIEMLab\Source\sysmon\sysmon.xml
```

If its feature is enabled but its service is not installed, use its existing executable with `-i` and the XML.

For a fresh VM without an active built-in or standalone instance:

```
Invoke-WebRequest `
  -Uri 'https://download.sysinternals.com/files/Sysmon.zip' `
  -OutFile C:\SIEMLab\Downloads\Sysmon.zip

Expand-Archive `
  -Path C:\SIEMLab\Downloads\Sysmon.zip `
  -DestinationPath C:\SIEMLab\Tools\Sysmon `
  -Force
```

Verify the executable:

```
$SysmonExe = 'C:\SIEMLab\Tools\Sysmon\Sysmon64.exe'

$Signature = Get-AuthenticodeSignature -FilePath $SysmonExe

$Signature | Format-List Status,SignerCertificate

if ($Signature.Status -ne 'Valid' -or
    $Signature.SignerCertificate.Subject -notmatch 'Microsoft') {
    throw 'Stop: the Sysmon signature did not validate.'
}
```

Install and verify:

```
& $SysmonExe -accepteula -i C:\SIEMLab\Source\sysmon\sysmon.xml

wevtutil.exe sl Microsoft-Windows-Sysmon/Operational /ms:268435456

Get-Service Sysmon64

Get-WinEvent `
  -LogName Microsoft-Windows-Sysmon/Operational `
  -MaxEvents 5 |
  Select-Object TimeCreated,Id
```

**Command overview:**

- `Invoke-WebRequest` downloads the package.
- `Expand-Archive` extracts it.
- `Get-AuthenticodeSignature` verifies the executable.
- `-i` installs Sysmon with the XML.
- `-c` updates an existing installation.
- `Get-WinEvent` checks generated records.

Use one Sysmon implementation. Microsoft documents both built-in and standalone options. [learn.microsoft.com](https://learn.microsoft.com/windows/security/operating-system-security/sysmon/how-to-enable-sysmon?utm_source=chatgpt.com)

---

**Step 25 — Install the Universal Forwarder**

Inside the **Windows VM**, download the compatible MSI:

```
$UfMsi = Read-Host 'Full path to the Universal Forwarder MSI'

Get-FileHash -LiteralPath $UfMsi -Algorithm SHA256
```

After checksum verification:

```
Start-Process msiexec.exe `
  -ArgumentList "/i `"$UfMsi`"" `
  -Wait
```

In the wizard:

1. Select **Splunk Enterprise**.
2. Keep `C:\Program Files\SplunkUniversalForwarder`.
3. Use `NT SERVICE\SplunkForwarder`.
4. Create the forwarder administrator credentials.
5. Leave deployment-server and receiving-indexer fields blank.
6. Leave event collection unchecked because your app defines it.
7. Complete installation.

Splunk documents the virtual account as its least-privileged Windows forwarder account. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/forward-and-process-data/universal-forwarder-manual/10.6/install-the-universal-forwarder/install-a-windows-universal-forwarder?utm_source=chatgpt.com)

---

**Step 26 — Deploy the forwarder configuration**

Inside the **Windows VM**:

```
$UfHome = 'C:\Program Files\SplunkUniversalForwarder'

Stop-Service SplunkForwarder

New-Item `
  -ItemType Directory `
  -Path "$UfHome\etc\auth\lab" `
  -Force | Out-Null

Copy-Item `
  -LiteralPath C:\SIEMLab\Public\ca.pem `
  -Destination "$UfHome\etc\auth\lab\ca.pem" `
  -Force

Copy-Item `
  -Path C:\SIEMLab\Source\apps\LAB_UF_WINDOWS `
  -Destination "$UfHome\etc\apps" `
  -Recurse `
  -Force
```

Set public-CA permissions:

```
icacls.exe "$UfHome\etc\auth\lab" /inheritance:r /grant:r `
  '*S-1-5-18:(OI)(CI)F' `
  '*S-1-5-32-544:(OI)(CI)F' `
  'NT SERVICE\SplunkForwarder:(OI)(CI)R'
```

Confirm the service account:

```
Get-CimInstance Win32_Service `
  -Filter "Name='SplunkForwarder'" |
  Select-Object Name,StartName
```

Add Event Log Readers membership if needed:

```
$Readers = Get-LocalGroup -SID 'S-1-5-32-573'

$ServiceSid = (
    [System.Security.Principal.NTAccount]'NT SERVICE\SplunkForwarder'
).Translate([System.Security.Principal.SecurityIdentifier])

$AlreadyMember = Get-LocalGroupMember -Group $Readers |
    Where-Object { $_.SID -eq $ServiceSid }

if (!$AlreadyMember) {
    Add-LocalGroupMember `
      -Group $Readers `
      -Member 'NT SERVICE\SplunkForwarder'
}
```

Check and start:

```
& "$UfHome\bin\splunk.exe" btool check

& "$UfHome\bin\splunk.exe" btool inputs list --debug

& "$UfHome\bin\splunk.exe" btool outputs list --debug

Start-Service SplunkForwarder

Test-NetConnection splunk01.lab.test -Port 9997

Get-Content "$UfHome\var\log\splunk\splunkd.log" -Tail 50
```

**Command overview:**

| Command                | Explanation                             |
| ---------------------- | --------------------------------------- |
| `Stop-Service`         | Pauses collection during configuration. |
| `Copy-Item`            | Copies the app and public CA.           |
| `icacls`               | Sets file permissions.                  |
| `Get-CimInstance`      | Checks the service account.             |
| `Add-LocalGroupMember` | Adds event-log reader membership.       |
| `btool`                | Checks configuration.                   |
| `Start-Service`        | Starts collection.                      |
| `Test-NetConnection`   | Checks the receiver’s port.             |
| `Get-Content -Tail`    | Displays recent messages.               |

A successful port check does not prove certificate validation. Confirm actual event delivery next.

---

**Step 27 — Verify event collection**

Open **Splunk Web → Search & Reporting** and run each search separately. These searches only return events that have been collected, indexed, and made available to your Splunk role. Keep raw event details in an approved private location.

## Step 27.1 — Review the lab indexes

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h
| stats count by index host sourcetype
```

**Query overview:** `index` selects the six existing lab indexes. `earliest=-24h` searches the previous 24 hours, and `stats count` groups the matching events by index, host, and sourcetype.

**Expected result:** A count appears for each combination with searchable events in the time range. An index with no matching events does not appear; its absence does not prove it is missing or that collection is configured correctly.

## Step 27.2 — Check the custom lab event

Paste this search into Splunk Web and click the green **Search** button:

```spl
index=lab sourcetype="siem:lab" earliest=-24h latest=now
| table _time host action result account _raw
```

**Query overview:**

- `index=lab`: Searches the lab index.
- `sourcetype="siem:lab"`: Selects custom lab messages.
- `earliest=-24h latest=now`: Searches the previous 24 hours through the current time.
- `table`: Displays the requested fields and the original message.

**Expected result:** The previously observed lab event appears if it is still within the last 24 hours, is searchable by your role, and has the specified index and sourcetype. The sample `pipeline_check` event may show `action=pipeline_check`, `result=success`, and `account=labadmin`; actual events can contain different values.

The time range in this search is written directly in SPL and overrides the corresponding range selected in Splunk Web. If the event is older than 24 hours, use the alternative below.

### Alternative: search using the time-range picker

Select **Last 7 days** in Splunk Web, paste this search, and click **Search**:

```spl
index=lab sourcetype="siem:lab"
| table _time host action result account _raw
```

**Expected result:** The search uses the selected seven-day range because it has no inline time modifiers. Check that the event timestamp falls within that range.

### If lab fields are blank

If `_raw` contains the expected values but `action`, `result`, or `account` is blank, review the event's actual sourcetype, the `LAB_SIEM` app context and permissions, and its search-time field extraction. The packaged `lab_fields` transform expects `action`, `result`, and `account` in that order with whitespace between them. Compare the actual message format with the transform before changing configuration. Do not publish raw event data.

If no event appears, review the time range, index and sourcetype, role permissions, and whether the event was indexed. Absence from this search alone does not identify the cause.

## Step 27.3 — Check Sysmon process-creation events

Select **Last 7 days** in Splunk Web, paste this search, and click **Search**:

```spl
index=sysmon EventCode=1
| table _time host User Image ParentImage CommandLine ProcessGuid
| head 20
```

**Query overview:**

- `index=sysmon`: Searches the Sysmon index.
- `EventCode=1`: Selects events where the extracted event code is 1, typically Sysmon process creation.
- `table`: Displays the requested process details.
- `head 20`: Shows up to 20 matching results.

**Expected result:** Up to 20 matching events appear if Event ID 1 is present and `EventCode` is extracted as expected. This search has no inline time modifiers, so it uses the **Last 7 days** selection. Field names and values depend on the event format, add-ons, and search-time extraction.

## Step 27.4 — If the Sysmon search returns no results

Keep **Last 7 days** selected and first check for any searchable Sysmon events:

```spl
index=sysmon
| stats count AS sysmon_events
```

**Query overview:** `index=sysmon` selects the Sysmon index. `stats count AS sysmon_events` reports the number of matching events as `sysmon_events`.

- **Count is zero:** No events were searchable in `sysmon` within the selected range for your current role. Check the time range and permissions, the Sysmon Operational channel, the forwarder's input and destination, and the receiving/indexing path. This result alone does not establish where the problem occurred.
- **Count is greater than zero:** Events are present. Check whether process-creation events exist and whether their event ID is extracted as `EventCode`.

To inspect a few events and their available fields, run:

```spl
index=sysmon
| table _time host source sourcetype EventCode EventID _raw
| head 20
```

**Query overview:** `table` displays the event metadata, possible event-ID fields, and original message; `head 20` limits the output. **Expected result:** Inspect `_raw` for an event ID of 1 and compare it with the extracted fields. A blank `EventCode` may require an appropriate add-on or field extraction; a nonzero count alone does not prove Event ID 1 exists. The first 20 results may not include every event type. Keep raw events private.

For missing Windows events or TLS handshake errors, follow the [forwarder TLS and KV service troubleshooting guide](../troubleshooting/splunk-forwarder-tls-and-kv-service.md) and compare a recent local event with its indexed copy.

## Reference

- [Splunk time modifiers](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/10.6/time-format-variables-and-modifiers/time-modifiers): Explains how inline `earliest` and `latest` settings interact with the time-range picker.

---

**Step 28 — Generate harmless hunting activity**

Run these commands only inside **WINHUNT01**, individually in the **same administrator Windows PowerShell window**. Its prompt begins with `PS`. The `$TestPassword` and `$LabCredential` variables are available only in that PowerShell session. Do not enter or share passwords in GitHub, screenshots, or chat. If a password prompt is cancelled or a command fails, stop; do not continue with values left from an earlier attempt.

This exercise has two account paths:

- **New account:** Complete Steps 28.2–28.3, skip Steps 28.4–28.5, then continue at Step 28.6 using the password entered in Step 28.2.
- **Existing disposable account:** Verify it in Step 28.1, skip Steps 28.2–28.3, and follow Steps 28.4–28.7 to reset and test its password. Use this path only after confirming that the existing account is the authorized disposable local lab account.

The optional `05-Generate-HuntActivity.ps1` helper still stops if `SIEMLabUser` exists; it does not perform the manual password reset. For shell or credential errors, see [PowerShell, Command Prompt, and lab credentials troubleshooting](../troubleshooting/windows-powershell-cmd-credentials.md).

## Step 28.1 — Confirm the guest and account

```powershell
$env:COMPUTERNAME
Get-LocalUser -Name 'SIEMLabUser' | Select-Object Name, Enabled, PrincipalSource, Description
```

**Command overview:** `$env:COMPUTERNAME` displays the computer name. `Get-LocalUser` checks the local test account and `Select-Object` shows its status and source. **Expected result:** The computer is `WINHUNT01`. If the account exists, confirm it is the enabled, disposable **local** lab account you intend to use. If Windows reports that the user was not found, use the new-account path. Investigate other errors before continuing. The LocalAccounts module requires 64-bit PowerShell on 64-bit Windows.

## Step 28.2 — Create a new disposable account, if absent

Skip this step when the account already exists. First run:

```powershell
if (Get-LocalUser -Name 'SIEMLabUser' -ErrorAction SilentlyContinue) {
    throw 'SIEMLabUser already exists. Review it before running this exercise.'
}
```

**Command overview:** `Get-LocalUser` checks for the account; `throw` stops this new-account check when it exists. **Expected result:** No message if the account is absent. If it exists, do not run the rest of Step 28.2; use the verified existing-account path.

Enter a temporary password:

```powershell
$TestPassword = Read-Host -Prompt 'Choose a temporary password for SIEMLabUser' -AsSecureString
```

**Command overview:** `Read-Host -AsSecureString` prompts without displaying the password and stores it in `$TestPassword`. **Expected result:** The prompt returns without displaying the password. Choose a nonempty password that meets local policy.

Create the account:

```powershell
New-LocalUser -Name 'SIEMLabUser' -Password $TestPassword -Description 'Disposable threat-hunting lab account' -ErrorAction Stop
```

**Command overview:** `New-LocalUser` creates the disposable local account using the entered password. **Expected result:** Windows reports the new account. If an error occurs, stop and resolve it before continuing; entering a password does not itself create or change an account.

## Step 28.3 — Generate a group-membership change, if using a new account

This optional lab action adds the newly created test account to the local Administrators group to generate a membership-change event. It grants administrator-group membership; use it only for the authorized disposable lab account and review the cleanup in Step 46. Skip this step for an existing account until its membership and the intended change have been reviewed.

```powershell
$Administrators = Get-LocalGroup -SID 'S-1-5-32-544'
Add-LocalGroupMember -Group $Administrators -Member 'SIEMLabUser' -ErrorAction Stop
```

**Command overview:** `Get-LocalGroup` finds the local Administrators group by SID. `Add-LocalGroupMember` adds the test account. **Expected result:** The command completes without an error. Windows may generate a group-membership event if the applicable audit policy is enabled. Stop on an error; do not assume membership changed.

## Step 28.4 — Enter a new password for an existing test account

For an **existing account only**, first confirm in Step 28.1 that `SIEMLabUser` is the authorized disposable local lab account. This step prepares a new password; it does not change Windows yet. Users who created the account in Step 28.2 should skip Steps 28.4–28.5.

```powershell
$TestPassword = Read-Host -Prompt 'Choose a new temporary password for SIEMLabUser' -AsSecureString
```

**Command overview:** `Read-Host -AsSecureString` prompts for a password without displaying it and stores it in `$TestPassword`. **Expected result:** A password prompt appears and returns to PowerShell. Choose a nonempty password that satisfies the local password policy.

## Step 28.5 — Apply the new password to the existing account

```powershell
Set-LocalUser -Name 'SIEMLabUser' -Password $TestPassword -ErrorAction Stop
```

**Command overview:** `Set-LocalUser` applies the entered password to the specified existing local account. `-ErrorAction Stop` reports a failure. **Expected result:** The command returns to the PowerShell prompt without an error. If it fails, stop and review the error before continuing. A successful password change does not itself prove that sign-in works.

This changes the account's password and can affect any other use of that account. Do not use it on an unverified account or an account connected to a Microsoft account.

## Step 28.6 — Build credentials from the same password

After a successful account creation in Step 28.2 **or** a successful password change in Step 28.5, run:

```powershell
$LabCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList "$env:COMPUTERNAME\SIEMLabUser", $TestPassword
```

**Command overview:** `New-Object` creates a credential object from the local computer and account name plus the same secure password value. **Expected result:** PowerShell returns without displaying the password. If the command fails, stop and do not reuse an older credential object. This does not authenticate the account; the next step tests it. If you changed PowerShell windows or either earlier account operation failed, return to the appropriate path rather than using an old variable.

## Step 28.7 — Test the correct password

```powershell
Start-Process -FilePath "$env:SystemRoot\System32\cmd.exe" -ArgumentList '/k whoami' -WorkingDirectory "$env:SystemRoot\System32" -Credential $LabCredential -ErrorAction Stop
```

**Command overview:** `Start-Process` opens Command Prompt using the test credentials. `/k whoami` displays the account name and keeps the new window open. **Expected result:** A new window displays the local computer name and test account, for example `winhunt01\siemlabuser`. Capitalization may differ. Confirm the actual output before continuing.

If Windows reports an incorrect user name or password, a disabled/locked account, or a logon-right problem, stop and investigate with the [credential troubleshooting guide](../troubleshooting/windows-powershell-cmd-credentials.md). Do not repeatedly guess passwords or weaken policy. The successful creation of `$LabCredential` alone does not prove authentication succeeded.

## Step 28.8 — Close the test window

In the **new Command Prompt window**, run:

```cmd
exit
```

**Command overview:** `exit` closes the test Command Prompt. **Expected result:** Only that window closes; return to the original administrator PowerShell window for the remaining steps.

## Step 28.9 — Run a harmless encoded command

```powershell
$Payload = "Write-Output 'SIEM-LAB-ENCODED-TEST'"
$Encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($Payload))
powershell.exe -NoProfile -EncodedCommand $Encoded
```

**Command overview:** The first two commands encode a harmless marker; `powershell.exe -EncodedCommand` runs it. **Expected result:** `SIEM-LAB-ENCODED-TEST` is displayed. Relevant PowerShell and process events depend on local logging and audit settings.

## Step 28.10 — Generate a known network connection

```powershell
curl.exe --fail --silent --show-error 'https://example.com/' --output C:\SIEMLab\TestFiles\example.html
```

**Command overview:** `curl.exe` requests the public example page and writes it to the lab test folder. **Expected result:** The file is created if the folder, DNS, and approved outbound connectivity are available. If this fails, investigate the displayed network or file error separately.

## Step 28.11 — Register a harmless task

```powershell
$Action = New-ScheduledTaskAction -Execute "$env:SystemRoot\System32\cmd.exe" -Argument '/c echo SIEM-LAB-TASK-TEST'
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddHours(1)
Register-ScheduledTask -TaskName SIEMLab-HuntTest -Action $Action -Trigger $Trigger -Description 'Harmless SIEM hunting test'
```

**Command overview:** The first two commands define the marker action and trigger. `Register-ScheduledTask` registers the task. **Expected result:** Windows reports the new task. If the named task already exists, review it before making changes; do not overwrite an unrelated task.

## Step 28.12 — Start the task

```powershell
Start-ScheduledTask -TaskName SIEMLab-HuntTest
```

**Command overview:** `Start-ScheduledTask` starts the previously registered task. **Expected result:** The command returns without an error; inspect Task Scheduler history if the task's actual execution needs verification.

## Step 28.13 — Create an Application marker

```powershell
eventcreate.exe /T INFORMATION /ID 100 /L APPLICATION /SO SIEMLab /D 'SIEM-LAB-APPLICATION-TEST'
```

**Command overview:** `eventcreate.exe` writes an informational marker to the Application log. **Expected result:** The command reports success. Check Event Viewer if it reports an error.

## Step 28.14 — Prepare for one intentional failed login

Only proceed after the **correct-password test succeeded** in Step 28.7 and the failed-login exercise is authorized for the disposable account. Review the local account lockout policy first:

```powershell
net accounts
```

**Command overview:** `net accounts` displays local account policy, including the lockout threshold. **Expected result:** Review the actual policy and recent failed attempts. Even one more failed attempt can lock the account if previous failures are near the threshold. Do not change the policy to force the exercise; skip the failed-login test if the risk is unacceptable.

## Step 28.15 — Generate one intentional failed login

```powershell
runas.exe /user:.\SIEMLabUser cmd.exe
```

**Command overview:** `runas.exe` prompts for the local test account's password and attempts to start Command Prompt. **Expected result:** For this **intentional failed-login exercise**, enter an incorrect password **once**; an authentication error is expected. This is separate from the correct-password test in Step 28.7. Do not keep retrying, and do not share the password entered.

If logon auditing is enabled and the event is collected, Windows can generate Security event `4625`. Account creation (`4720`), group change (`4732`), process activity (`4688`), and scheduled task creation (`4698`) likewise depend on the actions performed and the relevant audit settings. An existing-account path does not create a new `4720` event merely by resetting its password.

Review the actual events in Splunk after forwarding is validated. [Step 46](../steps/46-remove-the-test-objects.md) and its cleanup helper remove the named account and other test objects; review what they will delete before running them, especially if reusing an existing disposable account. They do not restore a previous password.

## References

- [Microsoft Set-LocalUser](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/set-localuser?view=powershell-5.1): Explains how to change a local account password with a secure string.
- [Microsoft PSCredential constructor](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.pscredential.-ctor): Explains creating a credential from a user name and secure password.
- [Microsoft Start-Process](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process?view=powershell-5.1): Explains starting a process using alternate credentials.
- [Microsoft account lockout threshold](https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/account-lockout-threshold): Explains the effect of failed sign-in attempts.

---

**Step 29 — Create the hunting search files**

On **RHEL**:

```
cd "$HOME/rhel-splunk-threat-hunting"
```

Create the health search:

```
cat > hunts/00-data-health.spl <<'EOF'
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h
| eval ingest_delay_seconds=_indextime-_time
| stats count latest(_time) as last_event max(_indextime) as last_received perc95(ingest_delay_seconds) as p95_delay_seconds by index host sourcetype
| eval seconds_since_receipt=now()-last_received
| convert ctime(last_event) ctime(last_received)
EOF
```

Create the encoded-PowerShell search:

```
cat > hunts/01-encoded-powershell.spl <<'EOF'
index=sysmon EventCode=1 earliest=-30m
| eval command=coalesce(CommandLine,process_command_line), image=coalesce(Image,process_path), account=coalesce(User,user)
| where match(image,"(?i)powershell[.]exe$") AND match(command,"(?i)-encodedcommand\s+")
| table _time host account image ParentImage command ProcessGuid
EOF
```

Create the account-change search:

```
cat > hunts/02-account-changes.spl <<'EOF'
index=win_security (EventCode=4720 OR EventCode=4732 OR EventCode=4733 OR EventCode=4726) earliest=-30m
| table _time host EventCode SubjectUserName TargetUserName MemberName TargetSid
| sort 0 _time
EOF
```

Create the failed-login search:

```
cat > hunts/03-failed-logons.spl <<'EOF'
index=win_security EventCode=4625 earliest=-30m
| eval account=coalesce(TargetUserName,Target_User_Name,user,"unknown"), source_ip=coalesce(IpAddress,Source_Network_Address,src_ip,"local-or-not-recorded")
| stats count values(LogonType) as logon_types values(Status) as status by host account source_ip
| sort - count
EOF
```

Create the scheduled-task search:

```
cat > hunts/04-scheduled-task.spl <<'EOF'
index=win_security EventCode=4698 earliest=-30m "SIEMLab-HuntTest"
| table _time host SubjectUserName TaskName TaskContent
EOF
```

Create the process/network search:

```
cat > hunts/05-process-network.spl <<'EOF'
index=sysmon (EventCode=1 OR EventCode=3) earliest=-30m
| eval image=coalesce(Image,process_path)
| search image="*curl.exe"
| stats earliest(_time) as first_seen values(EventCode) as event_ids values(image) as image values(CommandLine) as command values(DestinationIp) as destination_ip values(DestinationPort) as destination_port by host ProcessGuid
| convert ctime(first_seen)
EOF
```

Create the script-logging search:

```
cat > hunts/06-powershell-scriptblock.spl <<'EOF'
index=powershell earliest=-30m "SIEM-LAB-ENCODED-TEST"
| table _time host EventCode ScriptBlockText _raw
EOF
```

Create the Linux search:

```
cat > hunts/07-linux-pipeline.spl <<'EOF'
index=linux earliest=-30m "SIEM-LAB-LINUX-PIPELINE-TEST"
| table _time host source sourcetype _raw
EOF
```

Create the custom-field search:

```
cat > hunts/08-custom-fields.spl <<'EOF'
index=lab sourcetype=siem:lab earliest=-30m
| table _time host action result account _raw
EOF
```

Run each search in Splunk.

**Search-command overview:**

| Command         | Explanation                               |
| --------------- | ----------------------------------------- |
| `eval`          | Creates useful result values.             |
| `coalesce`      | Uses whichever listed field is available. |
| `where`         | Keeps matching records.                   |
| `match`         | Checks a text pattern.                    |
| `stats`         | Counts or combines records.               |
| `sort`          | Orders results.                           |
| `convert ctime` | Displays readable timestamps.             |

A match identifies activity to investigate; it does not prove an attack.

---

**Step 30 — Create the dashboard and analyst role**

On **RHEL**, create the dashboard:

```
cat > apps/LAB_SIEM/default/data/ui/views/overview.xml <<'EOF'
<dashboard version="1.1">
  <label>Threat Hunting Lab Overview</label>
  <description>Lab activity during the last 24 hours.</description>

  <row>
    <panel>
      <title>Events by index</title>
      <chart>
        <search>
          <query>(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) | stats count by index</query>
          <earliest>-24h</earliest>
          <latest>now</latest>
        </search>
        <option name="charting.chart">column</option>
      </chart>
    </panel>
  </row>

  <row>
    <panel>
      <title>Recent process starts</title>
      <table>
        <search>
          <query>index=sysmon EventCode=1 | table _time host User Image ParentImage CommandLine | head 50</query>
          <earliest>-24h</earliest>
          <latest>now</latest>
        </search>
      </table>
    </panel>
  </row>
</dashboard>
EOF
```

Create the role:

```
cat > apps/LAB_SIEM/local/authorize.conf <<'EOF'
[role_lab_hunter]
search = enabled
get_metadata = enabled
get_typeahead = enabled
change_own_password = enabled
srchIndexesAllowed = win_security;win_system;powershell;sysmon;linux;lab
srchIndexesDefault = win_security;win_system;powershell;sysmon;linux;lab
srchJobsQuota = 3
EOF
```

Create permissions:

```
cat > apps/LAB_SIEM/metadata/default.meta <<'EOF'
[]
access = read : [ admin, lab_hunter ], write : [ admin ]
export = system
EOF
```

Deploy the updated app:

```
sudo cp -a apps/LAB_SIEM/. /opt/splunk/etc/apps/LAB_SIEM/

sudo chown -R splunk:splunk /opt/splunk/etc/apps/LAB_SIEM

sudo find /opt/splunk/etc/apps/LAB_SIEM \
  -type d -exec chmod 750 {} +

sudo find /opt/splunk/etc/apps/LAB_SIEM \
  -type f -exec chmod 640 {} +

sudo -u splunk /opt/splunk/bin/splunk btool check

sudo systemctl restart Splunkd
```

In Splunk:

1. Open the **Threat Hunting Lab** app.
2. Open its Overview dashboard.
3. Create a separate analyst account.
4. Assign only `lab_hunter` for the access test.
5. Confirm it can search the six lab indexes.
6. Confirm it cannot retrieve protected `_internal` records.

**File overview:** The role permits lab searches and allows users to change their own passwords. Administrators retain configuration access.

---

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

If registration is needed, run `sudo subscription-manager register`. Follow the release-selection checks in [Step 7](../steps/07-register-update-and-prepare-rhel.md) on this VM. Confirm `BaseOS` and `AppStream` are available, then run the following commands **one at a time**; stop if an update or installation fails:

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

For the earlier missing `ipactl`/`kinit`/`ipa` commands, failed automatic package authorization, and pre-installation DNS refusal, see [IdM setup troubleshooting](../troubleshooting/idm-installation-and-dns.md). Those checks distinguish missing packages from an installed but unconfigured server.

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

**Step 34 — Create directory users, groups, and the lookup account**

On **RHEL-IDM01**, create dedicated application groups and three test users:

```bash
kinit admin
ipa group-add splunk-hunters --nonposix --desc='Splunk lab threat hunters'
ipa group-add splunk-admins --nonposix --desc='Splunk lab administrators'

ipa user-add hunter01 --first=Lab --last=Hunter --password
ipa user-add splunkadmin01 --first=Splunk --last=Administrator --password
ipa user-add unmapped01 --first=Unmapped --last=Test --password

ipa group-add-member splunk-hunters --users=hunter01
ipa group-add-member splunk-admins --users=splunkadmin01
```

Enter temporary passwords at the prompts. Complete the required first-password change for **each** user before testing Splunk:

```bash
kdestroy
kinit hunter01
kdestroy
kinit splunkadmin01
kdestroy
kinit unmapped01
kdestroy
kinit admin
```

Each `kinit` prompts for that user's temporary password and then a new password. Splunk's LDAP login page is not the place to complete this first-password change. Use the final passwords for later login tests.

RHEL 10.2 introduces the IdM system-account commands. Create the dedicated directory lookup account:

```bash
ipa sysaccount-add splunk-bind --password
ipa sysaccount-show splunk-bind --all --raw
```

Store the password securely. Confirm its directory name is:

```text
uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test
```

If `sysaccount-add` is unavailable, confirm the installed RHEL release and IdM packages before continuing. This procedure requires the RHEL 10.2 system-account feature.

Grant this account only the additional directory-read permissions needed for user and group lookups:

```bash
ipa permission-add 'Splunk Read Users' --type=user \
  --right=read --right=search --right=compare \
  --attrs=uid --attrs=cn --attrs=objectclass

ipa permission-add 'Splunk Read Groups' --type=group \
  --right=read --right=search --right=compare \
  --attrs=cn --attrs=member --attrs=objectclass

ipa privilege-add 'Splunk Directory Lookup'
ipa privilege-add-permission 'Splunk Directory Lookup' \
  --permissions='Splunk Read Users' --permissions='Splunk Read Groups'

ipa role-add 'Splunk Directory Reader'
ipa role-add-privilege 'Splunk Directory Reader' \
  --privileges='Splunk Directory Lookup'
ipa role-add-member 'Splunk Directory Reader' --sysaccounts=splunk-bind

ipa group-show splunk-hunters --all --raw
ipa group-show splunk-admins --all --raw
ipa role-show 'Splunk Directory Reader'
kdestroy
```

Do not add `splunk-bind` to the IdM `admins` group, a password-reset role, or either Splunk access group. The directory lookup role controls directory reads; the two application groups control access to Splunk. Existing IdM default read permissions may also apply.

**Command overview:** `ipa user-add` creates a directory user; `--password` prompts for a password; `ipa group-add` creates an application group; `--nonposix` avoids creating a Linux group ID; `group-add-member` assigns membership; `sysaccount-add` creates the lookup account; `permission-add`, `privilege-add`, and `role-add` grant selected read access; `kdestroy` clears the current authentication ticket.

**Summary:** Hunters and administrators have separate groups, and Splunk has a dedicated account for reading directory entries.

References:

- [Red Hat IdM Groups Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_idm_users_groups_hosts_and_access_control_rules/managing-user-groups-in-idm-cli): This guide explains group creation and membership management.
- [Red Hat IdM System Accounts Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_idm_users_groups_hosts_and_access_control_rules/configuring-a-system-account-in-idm-to-change-user-passwords-without-requiring-a-reset): This guide documents the RHEL 10.2 system-account creation commands; this lab grants directory reads only.
- [FreeIPA System Accounts Design](https://freeipa.readthedocs.io/en/latest/designs/sysaccounts.html): This reference explains system-account directory names and LDAP binding.
- [Red Hat IdM Permissions Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_idm_users_groups_hosts_and_access_control_rules/managing-role-based-access-controls-in-idm-using-the-cli): This guide explains permissions, privileges, and roles.

---

**Step 35 — Configure Splunk DNS and trust the directory certificate**

On **RHEL-SPLUNK01**, run from the VM console:

```bash
sudo dnf install -y openldap-clients bind-utils
nmcli -f NAME,DEVICE,TYPE connection show --active
read -r -p 'Enter the Splunk VM Ethernet profile name: ' SPLUNK_PROFILE

sudo nmcli connection modify "$SPLUNK_PROFILE" \
  ipv4.dns 172.25.250.30 \
  ipv4.ignore-auto-dns yes
sudo nmcli connection up "$SPLUNK_PROFILE"

getent hosts idm01.lab.test
dig idm01.lab.test +short
dig docs.redhat.com +short
```

The first two checks must resolve IdM to `172.25.250.30`. The last confirms that IdM forwards external DNS requests. Splunk's address and gateway stay `.10` and `.2`. The Windows VM and physical host can keep their existing DNS and Splunk hosts-file entries.

Obtain the **public IdM CA certificate** over SSH. First display the IdM SSH fingerprint at its VM console:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
openssl x509 -in /etc/ipa/ca.crt -noout -fingerprint -sha256
```

Then, on **RHEL-SPLUNK01**:

```bash
mkdir -p "$HOME/siem-public"
scp labadmin@172.25.250.30:/etc/ipa/ca.crt "$HOME/siem-public/idm-ca.pem"
openssl x509 -in "$HOME/siem-public/idm-ca.pem" -noout -fingerprint -sha256

sudo install -d -o splunk -g splunk -m 700 /opt/splunk/etc/auth/ldap
sudo install -o splunk -g splunk -m 600 \
  "$HOME/siem-public/idm-ca.pem" /opt/splunk/etc/auth/ldap/idm-ca.pem
```

Compare the SSH fingerprint before accepting the connection, then compare the CA fingerprints. Copy the public CA certificate only. Keep the existing `/opt/splunk/etc/auth/lab/` certificates for Splunk Web and forwarder traffic.

**Command overview:** `nmcli` changes only the Splunk VM's DNS resolver; `scp` copies the public certificate securely; `openssl x509` displays its fingerprint; `install` saves the certificate with access limited to the Splunk service account.

**Summary:** Splunk can find the directory server and has a trusted copy of its signing certificate.

---

**Step 36 — Verify LDAPS before enabling directory sign-in**

On **RHEL-SPLUNK01**, verify the directory's certificate chain and hostname as the Splunk service account:

```bash
sudo -u splunk openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test \
  -verify_return_error </dev/null
```

Continue only when the output shows a successful certificate verification, normally `Verify return code: 0 (ok)`.

Test the directory lookup account and inspect the exact attributes Splunk will use:

```bash
sudo -u splunk env \
  LDAPTLS_CACERT=/opt/splunk/etc/auth/ldap/idm-ca.pem \
  LDAPTLS_REQCERT=demand \
  ldapsearch -LLL -x -H ldaps://idm01.lab.test:636 \
  -D 'uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test' -W \
  -b 'cn=users,cn=accounts,dc=lab,dc=test' \
  '(uid=hunter01)' uid cn

sudo -u splunk env \
  LDAPTLS_CACERT=/opt/splunk/etc/auth/ldap/idm-ca.pem \
  LDAPTLS_REQCERT=demand \
  ldapsearch -LLL -x -H ldaps://idm01.lab.test:636 \
  -D 'uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test' -W \
  -b 'cn=groups,cn=accounts,dc=lab,dc=test' \
  '(|(cn=splunk-hunters)(cn=splunk-admins))' cn member
```

Enter the `splunk-bind` password at each prompt. Confirm both groups are returned and that each `member` value contains the expected user's full directory name. A successful command with no returned entries is not a successful lookup test.

Also verify the hunter's final password:

```bash
sudo -u splunk env \
  LDAPTLS_CACERT=/opt/splunk/etc/auth/ldap/idm-ca.pem \
  LDAPTLS_REQCERT=demand \
  ldapwhoami -x -H ldaps://idm01.lab.test:636 \
  -D 'uid=hunter01,cn=users,cn=accounts,dc=lab,dc=test' -W
```

**Command overview:** `openssl s_client` tests the encrypted connection; `-CAfile` selects the trusted CA; `-verify_hostname` checks the server name; `ldapsearch` checks user and group visibility; `-x` uses a password bind; `-H` selects the encrypted directory endpoint; `-D` supplies the account's full directory name; `-W` prompts without putting the password in the command; `-b` chooses the search location; `ldapwhoami` tests a user's password bind.

**Summary:** Certificate checks, lookup permissions, group membership, and the hunter's password work before Splunk authentication is changed.

---

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

**Step 38 — Create the LDAP strategy in Splunk Web**

Steps 36 and 37 verify the IdM connection, the lookup account, and Splunk's certificate settings. In this step, you enter those same details in Splunk Web. Keep a local Splunk `admin` session open until directory sign-in has been tested in the later steps.

### 1. Restart Splunk

On **RHEL-SPLUNK01**, run each command separately:

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

**Expected:** The second command returns `active`. If it does not, stop and check `sudo journalctl -u Splunkd -n 50 --no-pager` before changing authentication settings.

**Command overview:** `restart` loads the LDAP client certificate policy from Step 37; `is-active` confirms Splunk is running; `journalctl` shows recent service errors if the restart fails.

### 2. Open the LDAP form

1. Sign in to `https://splunk01.lab.test:8000` with the **local** Splunk `admin` account.
2. Open **Settings → Users and authentication → Authentication Methods**.
3. Select **LDAP**, choose **Configure Splunk to use LDAP**, then click **New**. Labels may differ slightly by Splunk version.

### 3. Enter the server and lookup account

| Field in Splunk Web | Enter or select |
| --- | --- |
| Strategy name | `LAB_IDM_LDAPS` |
| Host | `idm01.lab.test` |
| Port | `636` |
| SSL enabled | Select it for LDAPS. |
| Verify LDAP server TLS certificate | Select it to check the CA chain and the `idm01.lab.test` hostname. |
| Trusted CA certificate path | `/opt/splunk/etc/auth/ldap/idm-ca.pem` |
| Bind DN | `uid=splunk-bind,cn=sysaccounts,cn=etc,dc=lab,dc=test` |
| Bind DN password | Enter the protected `splunk-bind` password and confirm it if prompted. |

The bind account lets Splunk look up users and groups. Use its password, not the IdM `admin` password. Port `636` alone does not enable TLS: check both boxes. The CA path is a file **on RHEL-SPLUNK01**, already checked for readability in Step 37. If the CA field is left blank, this Splunk build can use the CA configured in Splunk's OpenLDAP client file; specifying the path makes this strategy's trust source clear.

### 4. Tell Splunk where to find users

| Field in Splunk Web | Enter or select |
| --- | --- |
| User base DN | `cn=users,cn=accounts,dc=lab,dc=test` |
| User base filter | `(objectClass=person)` |
| User name attribute | `uid` |
| Real name attribute | `cn` |
| Email attribute | Leave blank for these test accounts. |
| Group mapping attribute | `dn` |

### 5. Tell Splunk where to find groups

| Field in Splunk Web | Enter or select |
| --- | --- |
| Group base DN | `cn=groups,cn=accounts,dc=lab,dc=test` |
| Static group search filter | `(|(cn=splunk-hunters)(cn=splunk-admins))` |
| Group name attribute | `cn` |
| Static member attribute | `member` |
| Nested groups | Leave unselected; this lab uses direct group membership. |
| Dynamic group search filter | Leave blank. |
| Dynamic member attribute | Leave blank. |

Enter the full static group filter exactly as shown, without quotation marks or Markdown backticks. It selects the two lab access groups. Step 39 maps each group to a Splunk role.

### 6. Set advanced options and save

Expand **Advanced settings**:

| Field in Splunk Web | Enter or select |
| --- | --- |
| Enable referrals with anonymous bind only | Turn off for this lab. |
| Search request time limit | `15` seconds |
| Network socket timeout | `20` seconds |

Before saving, confirm that **SSL enabled** and **Verify LDAP server TLS certificate** are both checked, the CA path is correct, and the group filter is complete. Click **Save**. If your Splunk version presents a separate action to enable the LDAP strategy, complete it after saving. Confirm that `LAB_IDM_LDAPS` appears in the strategy list. Splunk checks the connection when you create a strategy; if saving fails, review the IdM host and port, CA trust, bind DN and password, and search fields before trying again. Do not turn off certificate verification to make a failed connection pass.

**Keep credentials private:** Enter the lookup password only in Splunk Web. Do not commit the live `authentication.conf`, encrypted password values, `splunk.secret`, or screenshots showing password fields.

**Summary:** The expected result is a saved `LAB_IDM_LDAPS` strategy. Continue to Step 39 to map groups to roles; creating the strategy alone does not confirm that a directory user can sign in.

References:

- [Splunk Web LDAP Setup Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/use-ldap-as-an-authentication-scheme/configure-ldap-with-splunk-web): This guide explains the form fields, LDAP strategy validation, and group settings.
- [Splunk 10.6.1 authentication.conf reference](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/configuration-file-reference/10.6.1-configuration-file-reference/authentication.conf): This reference explains LDAP certificate verification and the trusted CA path.

---

**Step 39 — Map the directory groups to Splunk roles**

On the LDAP strategies page, choose **Map groups** beside `LAB_IDM_LDAPS`. Apply these mappings and save each one:

| Directory group | Splunk role | Intended access |
| --- | --- | --- |
| `splunk-hunters` | `lab_hunter` only | Search the six lab indexes and view the lab dashboard |
| `splunk-admins` | `admin` only | Administer this lab's Splunk instance |

Do not map the broad IdM `ipausers` group to a Splunk role. Keep `unmapped01` outside both mapped groups. Keep `hunter01` outside `splunk-admins`.

Confirm **Settings → Roles → lab_hunter** contains only the six lab indexes from Step 30 and has no inherited role granting wider access. Confirm the Threat Hunting Lab app and dashboard permit `lab_hunter` to read them. A user in both mapped groups receives the combined permissions, including administrator access.

**Summary:** Directory membership determines who can hunt and who can administer Splunk.

References:

- [Splunk LDAP Group Mapping Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/use-ldap-as-an-authentication-scheme/map-ldap-groups-to-splunk-roles-in-splunk-web): This guide explains assigning Splunk roles to directory groups.

---

**Step 40 — Verify Splunk and review the safe LDAP examples**

Run these checks on **RHEL-SPLUNK01**. Step 38 created the `LAB_IDM_LDAPS` strategy in Splunk Web. The example files below document its intended settings; they do not change the live strategy.

### 40.1 — Check Splunk's configuration and service

Run each command separately:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool check && echo 'btool check completed'
sudo systemctl is-active Splunkd
sudo journalctl -u Splunkd -n 30 --no-pager
```

**Expected:** Review any `btool` warnings; the completion message appears only if the command exits successfully. `systemctl is-active` returns `active`. The journal should show Splunk starting without a service failure. If you changed a **live** Splunk configuration file since its last restart, restart once and check again:

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

**Observed in the supplied lab output:** `btool check` showed no problem text, `systemctl is-active` returned `active`, and the journal showed Splunk stopping and starting successfully. Those lines do not indicate a Splunk startup error. The later `No such file or directory` messages came from trying to write documentation files into a missing local folder.

**Command overview:** `btool check` checks Splunk configuration syntax; `systemctl is-active` checks the service; `journalctl` shows recent service messages. Restart Splunk only after a relevant live configuration change.

### 40.2 — Check the local repository before editing documentation

The **current GitHub repository already contains** both sanitized examples under `docs/reference/`. The earlier `cat > docs/reference/...` commands failed because that folder was absent from the local checkout. A shell redirection cannot create a missing parent folder. Do not rerun those commands or overwrite the tracked examples.

In the local project directory, run each command separately:

```bash
cd "$HOME/rhel-splunk-threat-hunting"
git rev-parse --show-toplevel
git remote get-url origin
git branch --show-current
git status --short
test -d docs/reference && echo 'docs/reference exists' || echo 'docs/reference is missing'
```

**Expected:** The directory is the intended project checkout, `origin` is `jbanday808/rhel-10v2-splunk-threat-hunting`, the branch is `main`, and `git status --short` prints nothing before an update. A different remote, branch, or local changes require review before syncing; do not discard work.

If those conditions hold and `docs/reference` is missing, bring this **clean `main` checkout** up to date:

```bash
git pull --ff-only origin main
ls -l docs/reference/ldap-authentication.conf.example \
  docs/reference/ldap-client.conf.example
```

**Expected:** Both files are listed. If the fast-forward pull fails or the files remain missing, stop and check the remote and checkout rather than creating a second copy or overwriting local work.

**Command overview:** `git rev-parse` identifies the checkout; `git remote get-url` identifies its source; `git status` exposes local changes; `test -d` checks the folder; `git pull --ff-only` updates a clean `main` without creating a merge commit; `ls` confirms the two tracked examples are present.

### 40.3 — Review the existing sanitized examples

- [LDAP authentication example](../reference/ldap-authentication.conf.example): Shows `LAB_IDM_LDAPS`, LDAPS on port `636`, certificate verification and CA path, search bases, group filter, and role mappings. The bind password is a **placeholder**.
- [Splunk LDAP client example](../reference/ldap-client.conf.example): Shows `TLS_REQCERT demand` and the public IdM CA path.

These are **documentation examples**, not instructions to replace live `/opt/splunk/etc/system/local/authentication.conf` or `/opt/splunk/etc/openldap/ldap.conf`. Step 38 entered the real bind password through Splunk Web. Keep live credentials, encrypted password values, `splunk.secret`, and unredacted `btool authentication list --debug` output outside GitHub.

Confirm in Splunk Web that `LAB_IDM_LDAPS` is **Enabled**. Step 39 separately maps `splunk-hunters` to `lab_hunter` and `splunk-admins` to `admin`; a successful strategy save or service restart does not prove that an LDAP user can sign in with the intended role.

**Summary:** The supplied output confirms Splunk is running. Update the correct local checkout to obtain the already tracked examples; the missing `docs/reference` folder is a local repository layout issue, not a Splunk service failure.

---

**Step 41 — Test permitted access and denied access**

Use a private browser window for each account and sign out between tests. Use the short directory usernames, such as `hunter01`, because this configuration uses the `uid` attribute.

| Test | Expected result |
| --- | --- |
| Sign in as `hunter01` with its final IdM password | Sign-in succeeds and the account has `lab_hunter` |
| Open the lab dashboard and search a populated lab index | The hunter can view the dashboard and retrieve lab events |
| Search `index=_internal` as `hunter01` | No protected records are returned |
| Attempt to change users or authentication as `hunter01` | Administrative actions are denied |
| Sign in as `splunkadmin01` | Sign-in succeeds with the Splunk `admin` role |
| Sign in as `unmapped01` | Splunk access is denied because no group grants a role |
| Enter one incorrect password for `hunter01` | Sign-in is denied |
| Sign in with the original local Splunk `admin` | Local recovery access still works |

For the hunter's positive search test, select **Last 24 hours** and run:

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab)
| stats count by index
```

Confirm an administrator can see recent `_internal` records before interpreting the hunter's empty `_internal` search as a valid restriction test.

Test removal of access on **RHEL-IDM01**:

```bash
kinit admin
ipa group-remove-member splunk-hunters --users=hunter01
ipa group-show splunk-hunters --all --raw
kdestroy
```

As the local Splunk administrator, use **Reload authentication configuration** if your release offers it, or restart `Splunkd` on `.10` to clear cached authentication data. Close the hunter's existing browser session and test a **new** login; it should be denied. Membership changes should not be treated as proof that every existing session was immediately revoked.

Restore membership on **RHEL-IDM01**, refresh authentication again, and repeat the hunter's login:

```bash
kinit admin
ipa group-add-member splunk-hunters --users=hunter01
kdestroy
```

After all checks, disable the unmapped test account on **RHEL-IDM01**:

```bash
kinit admin
ipa user-disable unmapped01
kdestroy
```

**Command overview:** `group-remove-member` removes group-based access; `group-add-member` restores it; `user-disable` disables the unused test identity. The search counts events in the indexes the hunter is permitted to search.

**Summary:** Authorized users can sign in, restricted accounts cannot administer Splunk, and group removal blocks a new login after authentication data is refreshed.

---

**Step 42 — Review authentication activity and troubleshoot failures**

Use the local Splunk administrator account for the searches in this step. The `lab_hunter` role from Step 39 does not have access to the `_audit` or `_internal` indexes.

### 1. Review login attempts in Splunk Web

Open **Search & Reporting** on **RHEL-SPLUNK01**, select **Last 7 days**, and run:

```spl
index=_audit action="login attempt"
| table _time user action info host
| sort - _time
```

`_audit` stores Splunk audit events. `action="login attempt"` selects login attempts; `table` shows the relevant fields, and `sort - _time` puts the newest event first. Review `info` and the underlying event before deciding whether a login succeeded or failed.

### 2. If Splunk says “No results found”

1. Confirm you are signed in as a **Splunk administrator**, not `hunter01`. Select **Last 7 days** in the time picker and run the query above again. Remove any older `earliest=-30m` text from the search: an inline time limit can narrow the search even when the picker shows a longer period.
2. Check whether the administrator can see any audit events during the selected period:

   ```spl
   index=_audit
   | stats count AS audit_events
   ```

3. If `audit_events` is greater than zero, inspect the action values actually present:

   ```spl
   index=_audit
   | stats count by action
   | sort - count
   ```

   If login events use a different format or the displayed fields are empty, inspect a few original events before changing the search:

   ```spl
   index=_audit
   | table _time action user info host _raw
   | sort - _time
   | head 20
   ```

4. If `audit_events` is zero as an administrator, try **All time** briefly and check that the Splunk server clock and search time zone are correct. Then investigate audit indexing locally. Do not treat a zero count from a restricted account as proof that audit logging is broken.

The earlier `action=login earliest=-30m` search can miss these events because the action value is `login attempt` in the documented audit search and the 30-minute limit narrows the window. The revised query is a starting point; verify it against events in your own Splunk build.

### 3. Check LDAP messages separately

As the Splunk administrator, keep **Last 7 days** selected and run:

```spl
index=_internal source=*splunkd.log* (LDAP OR ScopedLDAPConnection OR AuthenticationManager)
| table _time log_level component _raw
| sort - _time
```

If there are no matching messages, first check whether the administrator can search `splunkd.log` at all:

```spl
index=_internal source=*splunkd.log*
| stats count AS splunkd_events
```

No recent LDAP errors can be normal after a successful configuration. If `splunkd_events` is zero, check the selected time range and `_internal` access before diagnosing LDAP. A `TcpInputProc` “wrong version number” message from the Windows forwarder on port `9997` concerns the forwarding TLS path; it is not an LDAP bind error on port `636`. A successful LDAP login alone does not prove TLS certificate verification: retain the separate certificate and client-policy checks from Step 38.

### 4. Run directory checks on the correct VM

The following commands belong on **RHEL-IDM01**, the directory server. If your prompt says `labadmin@splunk01`, you are still on the Splunk client. Open the **RHEL-IDM01 VM console** and sign in as root or a sudo-enabled account. Verify the host before running service commands:

```bash
hostname -f
```

Expected host: `idm01.lab.test`. Then check IdM and its LDAPS listener:

```bash
sudo ipactl status
sudo ss -lntp 'sport = :636'
sudo systemctl list-units --all 'dirsrv@*.service'
```

Find the exact Directory Server unit name in the last command's output. For a `LAB.TEST` realm it is typically `dirsrv@LAB-TEST.service`; if your output differs, use the name shown there:

```bash
sudo journalctl --since '30 minutes ago' --no-pager -u dirsrv@LAB-TEST.service
```

If the correct unit has no entries in that 30-minute window, use `sudo journalctl -u dirsrv@LAB-TEST.service -n 50 --no-pager` to inspect its last 50 entries. No recent messages alone does not mean the directory service has failed.

On **RHEL-SPLUNK01**, check the client connection instead of expecting a local LDAP service:

```bash
hostname -f
getent ahostsv4 idm01.lab.test
sudo -u splunk timeout 10 openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test \
  -verify_return_error -brief </dev/null
```

The connection test should report **Verification: OK** and **Verified peername: idm01.lab.test**. Do not enter or publish the bind password in this test.

| What you see | Meaning and next check |
| --- | --- |
| `sudo: ipactl: command not found` on `splunk01` | You ran a directory-server command on the Splunk client. Switch to the `idm01` console; do not install IdM on the Splunk VM. |
| No listener appears for TCP `636` on `splunk01` | Expected: the Splunk VM connects to LDAPS; `idm01` listens for it. Run the listener check on `idm01`. |
| `Failed to add filter for units: No data available` on `splunk01` | There is no Directory Server unit on that host. List the units on `idm01` and use its exact `dirsrv@...service` name. |
| Cannot resolve `idm01.lab.test` | Check IdM DNS, the Splunk VM's resolver, and the directory VM's `.30` address. |
| Connection to TCP `636` times out | Check the VM network, IdM firewall, and listener on `idm01`. |
| Certificate verification fails | Check the CA file, certificate validity, host name, and clocks without disabling verification. |
| Bind fails despite a verified TLS connection | Check the exact `uid=splunk-bind,...` DN and current password using the private Step 38 bind test. |
| Lookup returns no users or groups | Check base DNs, filters, attributes, and bind-account permissions. |
| Password works elsewhere but Splunk denies access | Check required password changes, mapped group membership, role mapping, and duplicate local usernames. |
| Hunter receives too much access | Check `splunk-admins` membership, multiple mapped roles, and role inheritance. |
| Group change appears delayed | Refresh cached directory data and test in a new browser session. |

**Command overview:** `hostname -f` identifies the VM; `ipactl status` checks IdM services; `ss` checks the LDAPS listener; `systemctl list-units` finds the installed service name; `journalctl` reads that service's recent messages. On the Splunk VM, `getent` checks name resolution and `openssl s_client` tests the remote server's TLS certificate and host name.

**Summary:** Search audit events as an administrator, expand the time range when results are empty, and run server-side IdM commands on `idm01` while testing the remote LDAPS connection from `splunk01`.

References:

- [Splunk Search the Audit Log](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/audit-activity-in-splunk-enterprise/search-the-audit-log): This guide shows how to find login attempts in `_audit`.
- [Splunk Time Modifiers](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/10.6/time-format-variables-and-modifiers/time-modifiers): This guide explains how search time limits interact with the time picker.
- [Red Hat Identity Management service status](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/accessing_identity_management_services/viewing-starting-and-stopping-the-identity-management-services): This guide identifies the IdM server services and the `ipactl status` check.

---

**Step 43 — Back up the directory and document recovery**

The Splunk configuration backup in Step 47 includes live LDAP settings and Splunk's trusted directory certificate. Keep it private because it also includes secrets needed by the installation. It does **not** back up the separate IdM directory.

On **RHEL-IDM01**, create an IdM backup during a planned lab interruption:

```bash
sudo ipa-backup
sudo ipactl status
sudo ls -ld /var/lib/ipa/backup/ipa-full-*
```

A full IdM backup temporarily takes IdM services offline. Protect the backup and copy it to separate secure storage. Validate recovery in an isolated VM using the matching RHEL and IdM versions; follow Red Hat's recovery procedure rather than starting a restored copy beside the original directory server.

If LDAP configuration prevents a successful lab test:

1. Sign in with the original **local Splunk `admin`**, open Authentication Methods, and select native Splunk authentication.
2. If Web access is unavailable, open the **RHEL-SPLUNK01 console** and run `sudoedit /opt/splunk/etc/system/local/authentication.conf`.
3. In the existing `[authentication]` section, set `authType = Splunk`. Preserve the remaining sections for investigation; do not create a second `[authentication]` section.
4. Run the commands below and retest the local account.

```bash
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

For a complete configuration restore, use the protected pre-LDAP backup and the isolated recovery procedure in Step 47. LDAP rollback does not require changing the Windows forwarder or its TCP `9997` receiver.

Record the lookup account's owner, password-rotation date, and certificate-renewal checks in private operational notes. When its password changes, update the bind password through Splunk Web and repeat the lookup and login tests. Check IdM service-certificate renewal health as well as the expiry of the copied CA certificate.

**Command overview:** `ipa-backup` creates a directory backup; `ipactl status` confirms services returned; `sudoedit` changes authentication locally; `btool check` validates configuration before restart.

**Summary:** Splunk and IdM have separate backups, and local Splunk authentication remains a recovery option.

References:

- [Red Hat IdM Backup and Restore Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/preparing_for_disaster_recovery_with_identity_management/backing-up-and-restoring-idm): This guide explains full directory backups and supported recovery procedures.

---

**Step 44 — Record LDAP validation and screenshots**

On **RHEL-SPLUNK01**, add a separate validation record to the project:

```bash
cd "$HOME/rhel-splunk-threat-hunting"
cat > evidence/sanitized/ldap-validation.md <<'EOF'
# LDAP integration validation

Record observations and UTC timestamps. Replace Pending only after testing.

| Check | Actual result | Observed at (UTC) |
| --- | --- | --- |
| Exact RHEL and IdM builds recorded | Pending | Pending |
| Authentication-capable Splunk license confirmed | Pending | Pending |
| Directory DNS resolves to 172.25.250.30 | Pending | Pending |
| Directory CA fingerprint verified | Pending | Pending |
| LDAPS chain and hostname verification succeed | Pending | Pending |
| Lookup account reads intended users and both groups | Pending | Pending |
| Splunk LDAP client requires certificate verification | Pending | Pending |
| Hunter signs in with lab_hunter only | Pending | Pending |
| Hunter can search populated lab indexes | Pending | Pending |
| Hunter cannot retrieve protected _internal records | Pending | Pending |
| Hunter cannot change authentication or users | Pending | Pending |
| Directory Splunk administrator signs in | Pending | Pending |
| Unmapped user and incorrect password are denied | Pending | Pending |
| Removing hunter membership blocks a new login after refresh | Pending | Pending |
| Hunter membership restored and retested | Pending | Pending |
| Unmapped test account disabled | Pending | Pending |
| Local Splunk admin remains usable | Pending | Pending |
| Login audit activity reviewed | Pending | Pending |
| Splunk configuration and separate IdM backup completed | Pending | Pending |
| Recovery validated in an isolated copy | Pending | Pending |
EOF

cat >> .gitignore <<'EOF'

# LDAP secrets and live runtime settings
authentication.conf
splunk.secret
*.keytab
ldap-private/
EOF
```

If a sensitive file was already tracked, `.gitignore` alone does not remove it from Git history. Review staged content before committing; keep only the `.example` files and sanitized evidence.

Suggested screenshot filenames:

| Screenshot | Filename |
| --- | --- |
| Directory VM network | `LDAP_01_IdM_Network.png` |
| Directory application groups | `LDAP_02_Splunk_Groups.png` |
| Verified LDAPS connection | `LDAP_03_TLS_Validation.png` |
| Splunk LDAP strategy without password fields | `LDAP_04_Splunk_Strategy.png` |
| Directory groups mapped to Splunk roles | `LDAP_05_Role_Mapping.png` |
| Hunter's permitted searches | `LDAP_06_Hunter_Search.png` |
| Recent authentication activity | `LDAP_07_Login_Audit.png` |

**Command overview:** `cat >` creates the validation record; `cat >>` adds ignore rules; quoted `EOF` markers preserve the file text.

**Summary:** The project includes reusable examples and a validation checklist without claiming unperformed tests have passed.

---

**Step 45 — Create and test an alert**

In the **Threat Hunting Lab** app:

1. Run the encoded-PowerShell search.
2. Replace `earliest=-30m` with `earliest=-10m` in the search text.
3. Select **Save As → Alert**.
4. Name it `LAB - Encoded PowerShell`.
5. Schedule every five minutes.
6. If cron is requested, enter:
   ```
   */5 * * * *
   ```
7. Trigger when results are greater than zero.
8. Select **Add to Triggered Alerts**.
9. Use per-result suppression for 15 minutes on `host` and `ProcessGuid`.
10. Save under the administrator account.

Inside Windows, generate another marker:

```
$Payload = "Write-Output 'SIEM-LAB-ENCODED-TEST'"

$Encoded = [Convert]::ToBase64String(
    [Text.Encoding]::Unicode.GetBytes($Payload)
)

powershell.exe -NoProfile -EncodedCommand $Encoded
```

Check **Triggered Alerts** after the next scheduled run.

On RHEL, review the generated alert settings:

```
sudo cat /opt/splunk/etc/apps/LAB_SIEM/local/savedsearches.conf
```

If the file contains the lab alert, copy it to the source project:

```
sudo install -o labadmin -g labadmin -m 640 \
  /opt/splunk/etc/apps/LAB_SIEM/local/savedsearches.conf \
  "$HOME/rhel-splunk-threat-hunting/apps/LAB_SIEM/local/savedsearches.conf"
```

Also review and preserve `metadata/local.meta` if it contains the alert ownership and access settings.

**Command overview:** `cat` displays the settings; `install` copies the reviewed configuration to the project.

Scheduling and role behavior require an appropriate active license.

---

**Step 46 — Remove the test objects**

Inside **WINHUNT01**:

```
Stop-ScheduledTask `
  -TaskName SIEMLab-HuntTest `
  -ErrorAction SilentlyContinue

Unregister-ScheduledTask `
  -TaskName SIEMLab-HuntTest `
  -Confirm:$false

$Administrators = Get-LocalGroup -SID 'S-1-5-32-544'

Remove-LocalGroupMember `
  -Group $Administrators `
  -Member SIEMLabUser

Remove-LocalUser -Name SIEMLabUser

Remove-Item `
  -LiteralPath C:\SIEMLab\TestFiles\example.html `
  -Force `
  -ErrorAction SilentlyContinue
```

**Command overview:**

- `Stop-ScheduledTask` stops the task.
- `Unregister-ScheduledTask` removes it.
- `Remove-LocalGroupMember` removes temporary administrator membership.
- `Remove-LocalUser` deletes the disposable account.
- `Remove-Item` deletes the test download.

Keep the event records for investigation notes.

---

**Step 47 — Create the backup script**

On **RHEL**:

```
cat > scripts/rhel/backup-config.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

[[ $EUID -eq 0 ]] || {
  echo 'Run with sudo.' >&2
  exit 1
}

umask 077

install -d -m 700 /var/backups/siem-lab

BACKUP_FILE="/var/backups/siem-lab/splunk-etc-$(date -u +%Y%m%dT%H%M%SZ).tar.gz"

systemctl is-active --quiet Splunkd
systemctl stop Splunkd

trap 'systemctl start Splunkd' EXIT

tar --acls --xattrs --selinux \
  -czf "$BACKUP_FILE" \
  -C /opt/splunk etc

chmod 600 "$BACKUP_FILE"

sha256sum "$BACKUP_FILE"

printf 'Configuration backup: %s\n' "$BACKUP_FILE"
EOF

chmod +x scripts/rhel/backup-config.sh

bash -n scripts/rhel/backup-config.sh

sudo bash scripts/rhel/backup-config.sh
```

**Command overview:**

| Command                         | Explanation                                            |
| ------------------------------- | ------------------------------------------------------ |
| `set -euo pipefail`             | Stops on important failures.                           |
| `umask 077`                     | Makes backup files private.                            |
| `trap ... EXIT`                 | Starts Splunk again when the script finishes or fails. |
| `tar --acls --xattrs --selinux` | Preserves important file information.                  |
| `chmod 600`                     | Restricts backup access.                               |
| `bash -n`                       | Checks syntax.                                         |

This backup contains sensitive configuration. Keep it outside GitHub and copy it to separate protected storage.

It excludes indexed records, the CA private key, and complete OS settings.

For a recovery exercise, use an isolated clone with the same Splunk version:

```
read -r -p 'Full path to the known-good backup: ' BACKUP_FILE

sudo tar -tzf "$BACKUP_FILE"

sudo systemctl stop Splunkd

sudo mv /opt/splunk/etc \
  "/opt/splunk/etc.before-restore-$(date -u +%Y%m%dT%H%M%SZ)"

sudo tar --acls --xattrs --selinux \
  -xzf "$BACKUP_FILE" \
  -C /opt/splunk

sudo chown -R splunk:splunk /opt/splunk/etc

sudo restorecon -RF /opt/splunk/etc

sudo systemctl start Splunkd
```

**Command overview:** These commands inspect the backup, preserve current settings, restore the saved configuration, fix permissions, and restart Splunk.

If extraction fails, keep Splunk stopped and restore the preserved directory.

---

**Step 48 — Create the GitHub documentation**

On **RHEL**:

```
cat > README.md <<'EOF'
# RHEL 10.2 Splunk Threat Hunting Lab

This project uses VMware Workstation Pro, a RHEL 10.2 Splunk Enterprise
server, a separate Windows 11 endpoint, and a RHEL 10.2 IdM directory
server for verified LDAPS sign-in and group-based access.

## Architecture

- RHEL-SPLUNK01: indexing, searches, dashboards, and Linux logging.
- WINHUNT01: Windows logs, Sysmon, and Universal Forwarder.
- RHEL-IDM01: IdM directory accounts, groups, DNS, and directory certificates.
- Splunk signs users in over verified LDAPS on TCP 636.
- VS Code with WSL: final review and GitHub upload.

## Network

- VMnet8 NAT: 172.25.250.0/24
- RHEL: 172.25.250.10
- Windows endpoint: 172.25.250.20
- IdM directory and final Splunk DNS: 172.25.250.30
- Gateway and external DNS forwarder: 172.25.250.2

## Configuration files

- inputs.conf selects records to collect or receive.
- outputs.conf sends Windows records securely to RHEL.
- props.conf describes how custom records are read.
- transforms.conf extracts action, result, and account.
- indexes.conf defines storage areas and limits.
- authentication.conf configures directory sign-in and role mapping.
- authorize.conf defines role permissions and searchable indexes.
- etc/openldap/ldap.conf requires verified directory certificates.
- Only sanitized authentication examples belong in this repository.

## Contents

- apps/: Splunk server and forwarder configuration.
- configs/: Linux logging and rotation settings.
- scripts/: storage and backup scripts.
- sysmon/: Windows activity logging rules.
- hunts/: threat-hunting searches.
- docs/reference/: architecture and installed versions.
- evidence/sanitized/: reviewed validation results.

## Validation

See evidence/sanitized/validation.md and
evidence/sanitized/ldap-validation.md for actual results.
See docs/reference/ldap-authentication.conf.example and docs/reference/ldap-client.conf.example
for sanitized directory configuration examples. Pending entries are not passes.

## Scope

This is a learning environment. Search matches require investigation
before activity is classified as malicious.
EOF
```

Create the architecture record:

```
cat > docs/reference/architecture.md <<'EOF'
# Architecture

| System | Address | Purpose |
| --- | --- | --- |
| VMware host adapter | 172.25.250.1 | Host access |
| RHEL-SPLUNK01 | 172.25.250.10 | Splunk Enterprise |
| WINHUNT01 | 172.25.250.20 | Windows monitoring and tests |
| RHEL-IDM01 | 172.25.250.30 | IdM directory and lab DNS |
| NAT gateway | 172.25.250.2 | Outbound access |

RHEL combines indexing and the search interface.
Windows sends records over verified TLS on TCP 9997.
Splunk Web uses HTTPS on TCP 8000.
Splunk queries IdM over verified LDAPS on TCP 636.
Splunk uses IdM DNS at 172.25.250.30; IdM forwards external queries to .2.
The splunk-hunters group maps only to lab_hunter.
The splunk-admins group maps to admin.
The native Splunk admin remains available for recovery.
WSL and VS Code are used only for the final GitHub upload.
EOF
```

Create the version record:

```
cat > docs/reference/versions.md <<'EOF'
# Installed versions

Record the exact builds used on both RHEL servers; include the IdM
package versions from rpm -q ipa-server ipa-server-dns.

| Component | Installed version |
| --- | --- |
| VMware Workstation Pro | Pending |
| RHEL | Pending |
| RHEL kernel | Pending |
| IdM server RHEL | Pending |
| IdM / FreeIPA packages | Pending |
| Splunk Enterprise | Pending |
| Windows 11 | Pending |
| Universal Forwarder | Pending |
| Sysmon | Pending |
| Windows add-on | Pending |
| Sysmon add-on | Pending |
EOF
```

Create the validation record:

```
cat > evidence/sanitized/validation.md <<'EOF'
# Validation results

Replace Pending only after observing the result.

| Check | Actual result |
| --- | --- |
| RHEL 10.2 confirmed | Pending |
| Data disk mounted after reboot | Pending |
| Splunk runs as splunk | Pending |
| HTTPS validates successfully | Pending |
| Windows forwarding works | Pending |
| Windows Security records are searchable | Pending |
| Sysmon process records are searchable | Pending |
| PowerShell marker is searchable | Pending |
| Linux marker is searchable | Pending |
| Custom fields are extracted | Pending |
| Dashboard displays data | Pending |
| Scheduled alert triggers | Pending |
| Analyst restrictions work | Pending |
| Verified LDAPS sign-in works | Pending |
| Directory group mappings and removal tests pass | Pending |
| Local Splunk administrator remains usable | Pending |
| Separate IdM backup created | Pending |
| Test account and task removed | Pending |
| Backup and recovery tested | Pending |
EOF
```

Create a hunt-report template:

```
cat > docs/reference/hunt-report-template.md <<'EOF'
# Hunt report

Date and time zone:

Question being investigated:

Data source and time range:

Search file:

Observed results:

Evidence reference:

Expected explanation:

Other possible explanations:

Follow-up investigation:

Detection improvement:

Cleanup:

Limitations:
EOF
```

**Command overview:** These blocks create the project description, architecture, installed-version record, validation checklist, and investigation template.

Save reviewed screenshots under `docs/images`. Keep original event exports and transcripts in excluded raw-evidence storage.

---

**Step 49 — Perform the final checks**

On **RHEL**:

```
sudo systemctl is-active Splunkd

findmnt --mountpoint /splunkdata

df -h / /splunkdata

chronyc tracking

sudo -u splunk /opt/splunk/bin/splunk btool check

sudo journalctl -u Splunkd -n 50 --no-pager

sudo tail -n 50 /opt/splunk/var/log/splunk/splunkd.log

sudo openssl x509 \
  -in /opt/splunk/etc/auth/lab/splunk01.pem \
  -noout \
  -enddate
```

**Command overview:**

- `is-active` checks service state.
- `df -h` checks storage.
- `journalctl` shows service messages.
- `tail` shows recent Splunk messages.
- `openssl ... -enddate` checks certificate expiry.

| Problem                   | Check first                                                          |
| ------------------------- | -------------------------------------------------------------------- |
| Cannot connect            | VMware network, guest IP, gateway, and firewall zone.                |
| Updates fail              | DNS, NAT, and Red Hat repositories.                                  |
| Splunk will not start     | Data mount, storage, ownership, certificates, and logs.              |
| Windows data missing      | Event Viewer, forwarder service, permissions, TLS, and target index. |
| Fields are blank          | Add-ons and actual event sourcetype.                                 |
| Custom fields are missing | `siem:lab`, the `REPORT` reference, and expected format.             |
| Directory sign-in fails | IdM DNS, TCP 636, CA trust, final user password, and role mapping. |
| Data disappears early     | Index limits and Windows event-log rollover.                         |

For SELinux denials:

```
sudo ausearch -m AVC -ts recent
```

**Command overview:** `ausearch` finds specific denied operations for investigation.

### Reset the fishbucket for one source file

Use this optional troubleshooting procedure when you intend to read an already monitored file again. The fishbucket stores file-reading checkpoints.

**Single-source reset command — Option C in the reference question:**

```bash
splunk cmd btprobe \
  -d "$SPLUNK_HOME/var/lib/splunk/fishbucket/splunk_private_db" \
  --file "<source-file>" \
  --reset
```

Replace `<source-file>` with the actual file path. The example assumes the default fishbucket location; use the actual location if it was changed. Run the command on the Splunk instance that monitors the file.

For this lab, run the following on **RHEL-SPLUNK01** to reset the monitored file `/var/log/siem-lab/events.log`:

```bash
sudo systemctl stop Splunkd

sudo -u splunk /opt/splunk/bin/splunk cmd btprobe \
  -d /opt/splunk/var/lib/splunk/fishbucket/splunk_private_db \
  --file /var/log/siem-lab/events.log \
  --reset

sudo systemctl start Splunkd

sudo systemctl is-active Splunkd
```

Confirm the intended path if prompted. Stop Splunk before running `btprobe`; the change takes effect after startup.

**Command overview:**

| Command or option | Explanation |
| --- | --- |
| `sudo -u splunk` | Runs the utility as the Splunk service account. |
| `splunk cmd btprobe` | Opens Splunk's file-checkpoint utility. |
| `-d` | Specifies the fishbucket database folder. |
| `--file` | Selects one source file. |
| `--reset` | Resets that file's checkpoint. |
| `systemctl stop/start` | Stops and starts the Splunk service. |

**Summary:** This resets one file's reading checkpoint so an active file monitor can read it again. Existing indexed events remain; rereading can create duplicate events and increase ingestion-license use.

**Reference:** [Splunk Command Line Tools Guide](https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/10.6/contact-splunk-support/command-line-tools-for-use-with-support): This guide explains `btprobe` options and resetting a specific file's fishbucket checkpoint.

---

**Step 50 — Export the completed project from RHEL**

```
tar -czf "$HOME/rhel-splunk-source.tgz" \
  --exclude='rhel-splunk-threat-hunting/evidence/raw' \
  --exclude='rhel-splunk-threat-hunting/downloads' \
  --exclude='rhel-splunk-threat-hunting/private' \
  --exclude='rhel-splunk-threat-hunting/backups' \
  --exclude='rhel-splunk-threat-hunting/.git' \
  -C "$HOME" \
  rhel-splunk-threat-hunting

sha256sum "$HOME/rhel-splunk-source.tgz"
```

**Command overview:**

- `tar -czf` packages the source project.
- `--exclude` omits private or unnecessary material.
- `sha256sum` creates a transfer-check fingerprint.

On the **physical Windows host**:

```
New-Item -ItemType Directory -Path C:\SIEMLab\Export -Force

scp.exe labadmin@172.25.250.10:/home/labadmin/rhel-splunk-source.tgz C:\SIEMLab\Export\

Get-FileHash C:\SIEMLab\Export\rhel-splunk-source.tgz -Algorithm SHA256
```

Compare the hash with RHEL.

---

**Step 51 — Open the completed project in WSL and VS Code**

This is the stage where you use **WSL**.

For an Ubuntu/Debian-based WSL distribution:

```
sudo apt update

sudo apt install -y git gh python3

mkdir -p "$HOME/projects"

tar -xzf /mnt/c/SIEMLab/Export/rhel-splunk-source.tgz \
  -C "$HOME/projects"

cd "$HOME/projects/rhel-splunk-threat-hunting"

code .
```

**Command overview:**

| Command       | Explanation                          |
| ------------- | ------------------------------------ |
| `apt update`  | Refreshes package information.       |
| `apt install` | Installs Git and GitHub tools.       |
| `tar -xzf`    | Extracts the completed RHEL project. |
| `code .`      | Opens it in VS Code.                 |

Use the VS Code WSL extension and confirm that the window shows a WSL connection. Microsoft documents opening WSL folders with `code .`. [code.visualstudio.com](https://code.visualstudio.com/docs/remote/wsl?utm_source=chatgpt.com)

Review:

- Configuration files.
- Exact installed versions.
- Actual validation results.
- Screenshot contents.
- The absence of passwords, keys, backups, and raw records.

---

**Step 52 — Upload to GitHub**

In the VS Code **WSL terminal**:

```
git init -b main

git config user.name 'James Banday'

read -r -p 'Your verified GitHub email or GitHub noreply email: ' COMMIT_EMAIL

git config user.email "$COMMIT_EMAIL"

git add .

git diff --cached --check

git diff --cached --stat

git diff --cached
```

**Command overview:**

- `git init` starts project history.
- `git config` sets author information.
- `git add` stages files.
- `git diff --cached` shows exactly what will be uploaded.
- `--check` checks formatting problems.

After reviewing:

```
git commit -m 'Add RHEL Splunk threat hunting lab with verified LDAPS access'

gh auth login \
  --hostname github.com \
  --git-protocol https \
  --web

gh auth setup-git

gh repo create rhel-splunk-threat-hunting \
  --private \
  --source=. \
  --remote=origin \
  --push

gh repo view --web
```

**Command overview:**

| Command               | Explanation                           |
| --------------------- | ------------------------------------- |
| `git commit`          | Records the reviewed files.           |
| `gh auth login --web` | Signs in through the browser.         |
| `gh auth setup-git`   | Enables authenticated Git access.     |
| `gh repo create`      | Creates the repository.               |
| `--private`           | Keeps it private during final review. |
| `--source=.`          | Uses the current folder.              |
| `--push`              | Uploads the commit.                   |
| `gh repo view --web`  | Opens the repository.                 |

GitHub documents creating a repository from a local folder using `--source` and uploading commits with `--push`. [cli.github.com](https://cli.github.com//manual/gh_repo_create?utm_source=chatgpt.com)

If the repository already exists, connect to its actual URL and push to it instead of creating a duplicate.

For later changes:

```
git add .gitignore README.md apps configs scripts sysmon hunts docs evidence/sanitized

git diff --cached

git commit -m 'Update validated lab results and hunting searches'

git push
```

Keep passwords, private keys, installers, VM disks, raw event records, and configuration backups outside the repository.

---

**References**

- [VMware Virtual Network Editor](https://knowledge.broadcom.com/external/article/339371/using-the-virtual-network-editor-in-vmwa.html?utm_source=chatgpt.com): Explains NAT, host adapters, and DHCP settings.
- [Windows 11 on VMware](https://knowledge.broadcom.com/external/article/315650?utm_source=chatgpt.com): Explains Secure Boot, encryption, and virtual TPM setup.
- [RHEL 10.2 Release Notes](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/10.2_release_notes/index): Describes RHEL 10.2 and its hardware requirements.
- [Splunk System Requirements](https://help.splunk.com/en/splunk-enterprise/administer/install-and-upgrade/10.6/plan-your-splunk-enterprise-installation/system-requirements-for-use-of-splunk-enterprise-on-premises?utm_source=chatgpt.com): Lists supported server and forwarder platforms.
- [Splunk TLS Forwarding](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/secure-splunk-platform-communications-with-transport-layer-security-certificates/configure-splunk-indexing-and-forwarding-to-use-tls-certificates?utm_source=chatgpt.com): Explains protected event forwarding.
- [Microsoft Sysmon](https://learn.microsoft.com/sysinternals/downloads/sysmon?utm_source=chatgpt.com): Explains installation, event types, and filtering rules.
- [VS Code with WSL](https://code.visualstudio.com/docs/remote/wsl?utm_source=chatgpt.com): Explains opening the completed project in WSL.
- [GitHub CLI Repository Creation](https://cli.github.com/manual/gh_repo_create?utm_source=chatgpt.com): Explains creating a repository and uploading local commits.

---

## Appendix Splunk input parsing indexing and search phases

Splunk processes data in this order: **Input → Parsing → Indexing → Search**. The first three phases collect, prepare, and store records. The search phase lets you investigate the stored events and use them in dashboards and alerts.

Read this section alongside **Step 9**. The examples use the existing `siem:lab` configuration from Step 10. Run the RHEL checks after Steps 16–20 are complete; check Windows collection after Step 27 and directory-user access after Step 41.

### Where each phase runs in this lab

| Phase | Main purpose | Location in this lab |
| --- | --- | --- |
| Input | Collect records and identify their source. | Windows Universal Forwarder for Windows channels; RHEL Splunk for local files. |
| Parsing | Separate text into events and recognize event times. | RHEL Splunk processes the custom text input. Official add-ons support Windows event formats. |
| Indexing | Store events and the files used to find them. | RHEL Splunk indexer using `/splunkdata`. |
| Search | Retrieve events, extract fields, and display results. | RHEL Splunk provides both the search interface and local search execution. |

The Windows Universal Forwarder collects and sends records; it cannot index or search them. It has limited parsing capabilities for certain structured inputs. This guide places the full custom text parsing rules on RHEL. If you later add a heavy forwarder, review where parsing occurs before moving those rules.

### Input phase

The input phase reads data and assigns source information such as `host`, `source`, `sourcetype`, and the destination `index`.

For the custom RHEL input, `inputs.conf` monitors `/var/log/siem-lab/events.log`, assigns `host = splunk01` and `sourcetype = siem:lab`, and selects `index = lab`.

For Windows, `inputs.conf` on WINHUNT01 selects the event channels. Its `outputs.conf` sends the collected records to `splunk01.lab.test:9997` over TLS. The RHEL receiver accepts that connection. Steps 11 and 26 contain the forwarder settings and checks.

The fishbucket tracks reading progress for monitored files. The single-file reset in Step 49 is an optional replay procedure. Windows Event Log inputs use their own checkpoints, so that fishbucket command does not reset Windows event-channel collection.

**Summary:** Input chooses what Splunk collects and labels where it came from.

### Parsing phase

Parsing turns incoming text into individual events and determines each event's timestamp. It can also apply configured rules that change, filter, or route events before storage.

The existing `[siem:lab]` section in `props.conf` uses these settings:

- `LINE_BREAKER` separates records at line endings.
- `SHOULD_LINEMERGE = false` keeps the test records separate.
- `TIME_PREFIX = ^` starts timestamp detection at the beginning of the record.
- `TIME_FORMAT = %Y-%m-%dT%H:%M:%SZ` recognizes the lab's UTC date format.
- `MAX_TIMESTAMP_LOOKAHEAD = 20` limits the timestamp area to 20 characters.
- `TZ = UTC` sets the time zone for this source type.

Apply these rules to `siem:lab` on RHEL. Keep the Windows and Sysmon add-on rules for their own source types. Changing parsing settings affects newly processed records; it does not automatically correct events already stored.

**Summary:** Parsing defines each event and its time before Splunk stores it.

### Indexing phase

The indexer stores the parsed events as compressed event data with associated search index files. Splunk groups these files into storage units called buckets.

In this guide, the `[lab]` section of `indexes.conf` places active data under `/splunkdata/lab/db` and older searchable data under `/splunkdata/lab/colddb`. Its size and age limits determine when data is retired. Step 10 defines these settings, and Step 13 prepares the mounted data disk.

The `_time` field represents the event's time; `_indextime` records when Splunk indexed it. They can differ when older records arrive later.

**Summary:** Indexing saves the events and prepares them for efficient retrieval.

### Search phase

The search phase retrieves stored events and applies search commands, field extractions, and other search settings. Reports, dashboards, and alerts use searches.

In this lab, `REPORT-lab-fields = lab_fields` in `props.conf` references `[lab_fields]` in `transforms.conf`. This rule extracts `action`, `result`, and `account` when a search runs. `KV_MODE = none` disables automatic key-value extraction for `siem:lab`, so the named extraction is especially useful.

The same `props.conf` therefore contains settings used in different phases. `LINE_BREAKER` and `TIME_FORMAT` control parsing; `REPORT-lab-fields` and `KV_MODE` control search-time extraction. A `REPORT` reference applies at search time, while a `TRANSFORMS` reference can apply transformations during parsing.

LDAPS verifies a directory user's identity. The mapped Splunk role controls access to indexes and search features. After Step 41, `hunter01` should use the `lab_hunter` role to search the six permitted lab indexes, including `lab`.

**Summary:** Search turns stored events into useful results within the user's permissions.

### Verify the four phases step by step

Use the installed settings under `/opt/splunk`, rather than only reviewing the project copies. The following checks inspect configuration; the test in Check 5 deliberately adds one harmless record.

**Check 1 — Review the input**

On **RHEL-SPLUNK01**:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool inputs list \
  'monitor:///var/log/siem-lab/events.log' --debug
```

**Command overview:** `sudo -u splunk` runs as the Splunk service account; `btool inputs list` displays the merged input settings; the quoted name selects this file monitor; `--debug` shows the source configuration files.

Confirm `disabled = 0`, `index = lab`, `sourcetype = siem:lab`, and `host = splunk01`.

**Check 2 — Review parsing**

```bash
sudo -u splunk /opt/splunk/bin/splunk btool props list siem:lab --debug
```

**Command overview:** `btool props list siem:lab` shows the effective settings for the custom source type; `--debug` identifies where each setting comes from.

Confirm the line-breaking and UTC timestamp settings listed above. This command shows configuration on disk; the new-event test below checks the running behavior.

**Check 3 — Review indexing and storage**

```bash
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug

findmnt --mountpoint /splunkdata

df -h /splunkdata
```

**Command overview:** `btool indexes list lab` displays the lab index settings; `findmnt --mountpoint` confirms the data disk is mounted at the exact path; `df -h` displays storage use in readable units.

Confirm the configured paths point to `/splunkdata/lab`, the mount exists, and the disk has free space.

**Check 4 — Review search field extraction**

```bash
sudo -u splunk /opt/splunk/bin/splunk btool transforms list lab_fields --debug
```

**Command overview:** `btool transforms list lab_fields` displays the extraction rule referenced by `REPORT-lab-fields`; `--debug` shows its configuration file.

Confirm the rule extracts `action`, `result`, and `account`. Run the search in the Threat Hunting Lab app so the app's search settings are available.

**Check 5 — Add a new test record**

```bash
printf '%s action=phase_check result=success account=labadmin\n' \
  "$(date -u +%FT%TZ)" \
  | sudo tee -a /var/log/siem-lab/events.log
```

**Command overview:** `date -u +%FT%TZ` creates the expected UTC timestamp; `printf` formats one record; `|` passes it to the next command; `sudo tee -a` appends it to the monitored file with administrator permission.

**Summary:** This creates a new entry that can pass through input, parsing, and indexing without resetting an existing checkpoint.

**Check 6 — Search for the new event**

In Splunk Web, sign in as the local `admin` account, open the **Threat Hunting Lab** app, and run this search:

```spl
index=lab sourcetype=siem:lab source="/var/log/siem-lab/events.log"
"action=phase_check" earliest=-15m latest=now
| table _time host source sourcetype action result account _raw
```

**Command overview:** `index`, `sourcetype`, and `source` select this input's stored events; the quoted text finds the test record even if field extraction fails; `earliest=-15m latest=now` limits the time range; `| table` displays the named fields; `_raw` shows the original event text.

Allow a few seconds for collection. Confirm that the new event appears, `_time` represents the same moment as its UTC timestamp, allowing for your displayed time zone, `host` is `splunk01`, and the extracted fields show `action = phase_check`, `result = success`, and `account = labadmin`.

After Step 41, repeat the search as `hunter01`. Confirm the mapped `lab_hunter` role permits the `lab` index. The same record may appear several times if you deliberately repeat Check 5.

### Find the phase to investigate

| Observation | Phase or setting to check first |
| --- | --- |
| The test record is absent from the source file. | Event generation and the file path, before Splunk input. |
| The file contains the record, but Splunk never reads it. | Input enablement, file permissions, and the monitored path. |
| Records merge together or have the wrong time. | Parsing rules for `siem:lab`; use All time temporarily if the event time is wrong. |
| Splunk reports a missing index or cannot write data. | Index definition, the `/splunkdata` mount, free space, and ownership. |
| The raw event appears, but custom fields are empty. | Search-time `REPORT-lab-fields`, `[lab_fields]`, and app permissions. |
| Admin finds the event, but the directory hunter cannot. | LDAP group mapping, `lab_hunter` index permissions, and the search time range. |

Record the observed event, timestamp, extracted fields, and directory-user result in your lab evidence. Configuration output alone does not prove that all four phases succeeded.

References:

- [Splunk Data Pipeline Guide](https://help.splunk.com/en/splunk-enterprise/administer/distributed-deployment-manual/10.6/overview-of-splunk-enterprise-distributed-deployments/how-data-moves-through-splunk-deployments-the-data-pipeline): This guide explains the input, parsing, indexing, and search phases.
- [Splunk Configuration and Data Phases Guide](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/administer-splunk-enterprise-with-configuration-files/configuration-parameters-and-the-data-pipeline): This guide explains which settings apply during each phase and where to configure them.
- [Splunk Indexing Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-indexers-and-indexer-clusters/10.6/indexing-overview/how-indexing-works): This guide explains how Splunk processes events and stores searchable data.
- [Splunk Universal Forwarder Guide](https://help.splunk.com/en/splunk-cloud-platform/forward-and-process-data/ingest-actions/process-data-with-forwarders/the-universal-forwarder): This guide explains what the Universal Forwarder collects and forwards and its processing limits.

---

## Appendix Splunk local data integrity checks

Use `check-integrity` to compare stored local event data with the hashes recorded by Splunk. Run this procedure on **RHEL-SPLUNK01** after the Splunk app and local `lab` index are working. The procedure includes a short maintenance stop of this standalone lab server.

### Choose the correct command scope

The two supported forms select different amounts of data:

```bash
./splunk check-integrity -index lab -verbose
```

```bash
./splunk check-integrity -bucketPath "/full/path/to/one/bucket" -verbose
```

| Option | Meaning |
| --- | --- |
| `./splunk` | Runs the program from the current directory, normally `/opt/splunk/bin`. The lab commands below use its full path. |
| `check-integrity` | Checks recorded data hashes against the selected local data. |
| `-index lab` | Selects the local index named `lab`, covering its buckets. |
| `-bucketPath` | Selects one actual bucket directory, rather than the index's parent directory. |
| `-verbose` | Displays additional details. |

The supplied question displays `-index` but its explanation switches to `-bucketPath`. Use the first form for an index and the second for one bucket. Do not type the square brackets used to illustrate optional arguments in documentation.

This feature supports local Splunk Enterprise indexes, including this lab's `/splunkdata` storage. It does not support SmartStore indexes or Splunk Cloud Platform. Integrity hashes must have been generated when the data was indexed; enabling the feature now does not create a historical baseline for previously unhashed data.

### Integrity check 1 Review the existing index

On RHEL:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug

findmnt --mountpoint /splunkdata
```

**Command overview:** `sudo -u splunk` runs as the Splunk service account; `btool indexes list lab` shows the merged settings for the lab index; `--debug` identifies their configuration files; `findmnt --mountpoint` checks the exact data mount.

Confirm `homePath = /splunkdata/lab/db` and `coldPath = /splunkdata/lab/colddb`. Check `enableDataIntegrityControl`; its default is `false`.

### Integrity check 2 Enable hashing and preserve the project copy

Back up the current index settings before editing them:

```bash
install -d -m 700 "$HOME/siem-private"

sudo cp -a /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf \
  "$HOME/siem-private/indexes.conf.before-integrity"

sudoedit /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf
```

**Command overview:** `install -d -m 700` creates a private backup folder; `cp -a` preserves a copy and its attributes; `sudoedit` opens the configuration with administrator permission.

Add the following setting inside the **existing** `[lab]` section. Keep its storage paths, limits, and all other index sections:

```ini
[lab]
enableDataIntegrityControl = true
```

This snippet shows only the setting to add. It is not a replacement for the complete file from Step 10.

Check the file and apply the change:

```bash
sudo chown splunk:splunk /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf
sudo chmod 640 /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf

sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug
```

**Command overview:** `chown` assigns ownership; `chmod 640` sets file access; `btool check` validates configuration; the final command confirms which file supplies `enableDataIntegrityControl = true`.

Resolve configuration errors before restarting. Then:

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd

cd "$HOME/rhel-splunk-threat-hunting"
sudo cat /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf \
  > apps/LAB_SIEM/local/indexes.conf
```

**Command overview:** `systemctl restart` reloads Splunk with the new settings; `is-active` checks its state; `cd` selects the project; `sudo cat ... > ...` copies the installed index settings back into the user's project file.

### Integrity check 3 Create and confirm new covered data

Hashing uses SHA-256. Splunk records hashes of new data slices in `rawdata/l1Hashes`; when a bucket becomes warm, it creates `rawdata/l2Hash` from those recorded hashes.

Append one new test record after hashing has been enabled:

```bash
printf '%s action=integrity_check result=success account=labadmin\n' \
  "$(date -u +%FT%TZ)" \
  | sudo tee -a /var/log/siem-lab/events.log
```

**Command overview:** `date -u` supplies the UTC time; `printf` formats one record; `|` passes it onward; `sudo tee -a` appends it to the monitored file.

In the Threat Hunting Lab app, confirm collection:

```spl
index=lab sourcetype=siem:lab "action=integrity_check"
earliest=-15m latest=now
| table _time host action result account _raw
```

**Command overview:** `index` and `sourcetype` choose the lab data; the quoted text finds the test record; `earliest` and `latest` set the time range; `table` displays the selected fields.

### Integrity check 4 Locate a completed bucket

For this small lab, use a planned clean restart after the test record is searchable, then inspect the resulting warm buckets. A normal hot-to-warm roll also creates the bucket-level hash. Do not repeatedly force small bucket rolls as a routine check.

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd

sudo -u splunk find /splunkdata/lab/db /splunkdata/lab/colddb \
  -type f -name l2Hash -print
```

**Command overview:** `systemctl` restarts and checks the service; `find` searches local lab storage; `-type f` selects files; `-name l2Hash` finds completed bucket hashes; `-print` displays their paths.

If no matching file exists, do not record a successful integrity check. Confirm hashing is active, new data arrived, and a covered bucket has completed its roll. Repeat the inspection after a normal roll if needed.

Select an actual bucket from the displayed paths. For a path ending in `/rawdata/l2Hash`, the bucket path is the part before `/rawdata/l2Hash`:

```bash
read -r -p 'Full path to the selected warm or cold lab bucket: ' INTEGRITY_BUCKET

sudo -u splunk ls -l -- \
  "$INTEGRITY_BUCKET/rawdata/l1Hashes" \
  "$INTEGRITY_BUCKET/rawdata/l2Hash"
```

**Command overview:** `read -r` stores the selected directory; `ls -l` displays both hash files; `--` ends the command's options. Use the bucket directory itself, not `/splunkdata/lab/db` or the `rawdata` directory.

### Integrity check 5 Run the index and bucket checks

The following lab procedure pauses ingestion and searches while the standalone service is stopped. It gives you a stable inspection window:

```bash
sudo systemctl stop Splunkd

sudo -u splunk /opt/splunk/bin/splunk check-integrity \
  -index lab -verbose

sudo -u splunk /opt/splunk/bin/splunk check-integrity \
  -bucketPath "$INTEGRITY_BUCKET" -verbose

sudo systemctl start Splunkd
sudo systemctl is-active Splunkd
```

**Command overview:** `stop` pauses Splunk; `-index lab` checks the named local index; `-bucketPath` narrows the check to the selected bucket; `-verbose` provides details; `start` resumes the service; `is-active` confirms it returned.

Record both outputs and any warnings before classifying the result. A bucket selected for checking must have an applicable hash baseline. Older buckets in the index may lack one even when the newly covered bucket verifies successfully.

### Integrity check 6 Interpret and record the result

| Result observed | Meaning and next action |
| --- | --- |
| The selected covered data passes its reported checks. | Record the index or bucket scope, command, time, Splunk version, and actual output. |
| Hash files or a historical baseline are missing. | Record that data as not verified. Confirm when hashing was enabled and whether the bucket rolled. |
| A hash mismatch is reported. | Preserve the output and affected data. Investigate with a known backup or Splunk Support before changing files. |
| The path or permissions are wrong. | Confirm the real bucket path and that the `splunk` account can read it. |
| The index uses SmartStore. | This local data integrity feature does not apply. |

Do not delete, edit, or regenerate hash files to make a mismatch disappear. The check validates data against its recorded hashes; it does not repair corruption. Confirm the service is active when you finish, and retain the project configuration update for future deployments.

**Summary:** Enable hashes before collecting the data, select a local index or an individual covered bucket, run the appropriate `check-integrity` command, and record the observed result.

References:

- [Splunk Data Integrity Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/audit-activity-in-splunk-enterprise/manage-data-integrity): This guide explains local data integrity, hash files, and the index and bucket command forms.
- [Splunk Index Configuration Reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/indexes.conf): This reference explains `enableDataIntegrityControl` and index settings.
- [Splunk Indexed Data Backup Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-indexers-and-indexer-clusters/10.6/back-up-and-archive-your-indexes/back-up-indexed-data): This guide explains bucket states, clean restarts, and considerations for manual bucket rolls.

---

## Appendix GitHub Actions OpenID Connect with Azure

OpenID Connect, or **OIDC**, lets a GitHub Actions job obtain a short-lived Azure login without storing an Azure client password. This addition uses Microsoft Entra ID and Azure for the GitHub project created in Step 52. LDAPS continues to handle human sign-in to Splunk.

The working example authenticates a manually started GitHub job and reads one DEV resource group. It uses a GitHub-hosted runner and grants **Reader** access only at that group's scope. A GitHub-hosted runner has no direct route into the lab's private VMnet8 network; this workflow does not deploy to `172.25.250.10`.

### OIDC step 1 Confirm prerequisites and execution locations

You need an Azure subscription, permission to create an Entra application and service principal, and permission to create a resource group and assign its Azure roles. Role assignment requires an appropriate Azure role such as Role Based Access Control Administrator, User Access Administrator, or Owner at the relevant scope. Entra application permissions and Azure resource permissions are separate.

| Task | Where to perform it |
| --- | --- |
| Create workflows and run GitHub CLI commands | The existing WSL project in VS Code, after Step 52. |
| Create the Azure identity, trust, and role assignment | Azure Cloud Shell using Bash. |
| Execute the workflows | GitHub Actions on `ubuntu-24.04`. |
| View lab events or change Splunk settings | RHEL-SPLUNK01 or Splunk Web, as in the earlier steps. |

The example repository is `jbanday808/rhel-10v2-splunk-threat-hunting` and the trusted branch is `main`. If your Step 52 repository has a different owner or name, replace that exact value in both workflow guards below before committing them. Confirm Actions is enabled in the repository's **Settings → Actions → General**.

In the WSL terminal:

```bash
cd "$HOME/projects/rhel-splunk-threat-hunting"
gh auth status
gh repo view --json nameWithOwner,defaultBranchRef
git branch --show-current
git status --short
mkdir -p .github/workflows
```

**Command overview:** `cd` selects the exported project; `gh auth status` checks GitHub access; `gh repo view` identifies the repository and default branch; `git branch` shows your branch; `git status` shows pending changes; `mkdir -p` creates the workflow folder.

Confirm the repository and `main` branch before continuing. Review any existing changes instead of overwriting them.

### OIDC step 2 Capture the actual GitHub subject

Azure must trust the exact OIDC `sub` value GitHub issues. Newer repositories can include immutable owner and repository IDs, while older repositories can use the earlier name-based format. Capturing the actual value also detects a custom subject template.

Create `.github/workflows/oidc-claims.yml` in VS Code with this complete content:

```yaml
name: Inspect OIDC trust claims

on:
  workflow_dispatch:

permissions: {}

jobs:
  claims:
    if: >-
      github.ref == 'refs/heads/main' &&
      github.repository == 'jbanday808/rhel-10v2-splunk-threat-hunting'
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    permissions:
      id-token: write
    steps:
      - name: Display selected trust claims
        shell: bash
        run: |
          python3 - <<'PY'
          import base64
          import json
          import os
          import urllib.parse
          import urllib.request

          url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"]
          separator = "&" if "?" in url else "?"
          url += separator + urllib.parse.urlencode({
              "audience": "api://AzureADTokenExchange"
          })
          request = urllib.request.Request(url, headers={
              "Authorization": "bearer " + os.environ[
                  "ACTIONS_ID_TOKEN_REQUEST_TOKEN"
              ]
          })
          with urllib.request.urlopen(request, timeout=30) as response:
              encoded = json.load(response)["value"].split(".")[1]
          encoded += "=" * (-len(encoded) % 4)
          claims = json.loads(base64.urlsafe_b64decode(encoded))
          keys = ("iss", "aud", "sub", "repository", "ref",
                  "repository_id", "repository_owner_id", "event_name")
          print(json.dumps({key: claims.get(key) for key in keys},
                           indent=2))
          PY
```

**Workflow overview:** `workflow_dispatch` provides a manual start; the job guard permits only this repository's `main` branch; `id-token: write` allows token requests. The Python code requests a token for Azure's audience and displays only the selected identity claims. It does not print the token or its bearer credential. Decoding these claims is for setup inspection; Azure performs signature validation during the actual exchange.

Commit only the intended file after reviewing its contents:

```bash
git add .github/workflows/oidc-claims.yml
git diff --cached --check
git diff --cached
git commit -m 'Add OIDC subject inspection workflow'
git push origin main

gh workflow run oidc-claims.yml --ref main
gh run list --workflow oidc-claims.yml --limit 5
```

**Command overview:** `git add` stages the workflow; `git diff` checks and displays staged changes; `git commit` records them; `git push` sends them to GitHub; `gh workflow run` starts the manual job; `gh run list` lists its runs.

After the run completes:

```bash
read -r -p 'OIDC claims workflow run ID: ' CLAIMS_RUN_ID
gh run view "$CLAIMS_RUN_ID" --log
```

**Command overview:** `read -r` stores the run ID; `gh run view --log` displays its job log.

Confirm `iss` is `https://token.actions.githubusercontent.com`, `aud` is `api://AzureADTokenExchange`, and `ref` is `refs/heads/main`. Copy the complete `sub` string, preserving case and any IDs. A current immutable subject can have the following shape; the angle-bracket values here are placeholders:

```text
repo:jbanday808@<owner-id>/rhel-splunk-threat-hunting@<repo-id>:ref:refs/heads/main
```

An older repository may instead show `repo:jbanday808/rhel-10v2-splunk-threat-hunting:ref:refs/heads/main`. Use the observed value rather than constructing one from this example. Both workflows in this guide deliberately omit a GitHub `environment`; adding one can change the subject and requires matching Azure trust.

### OIDC step 3 Open Azure Cloud Shell and select the subscription

In the Azure portal, open **Cloud Shell**, select **Bash**, and use your intended DEV subscription. An ephemeral session can use **No storage account required**. If Cloud Shell has not been enabled for the subscription, register the `Microsoft.CloudShell` resource provider under **Subscriptions → your subscription → Resource providers** first. Keep the session open through the Azure setup steps; its local files and shell variables are temporary.

```bash
az account list --output table
read -r -p 'DEV Azure subscription ID: ' AZURE_SUBSCRIPTION_ID
az account set --subscription "$AZURE_SUBSCRIPTION_ID"

AZURE_TENANT_ID=$(az account show --query tenantId --output tsv)
az account show --query '{subscription:id,tenant:tenantId,name:name}' --output table

OIDC_RG=rg-siem-oidc-dev
OIDC_LOCATION=westus3
OIDC_APP_NAME=app-siem-github-oidc-dev

az group create --name "$OIDC_RG" --location "$OIDC_LOCATION" --output table
OIDC_RG_SCOPE=$(az group show --name "$OIDC_RG" --query id --output tsv)
```

**Command overview:** `az account list` shows available subscriptions; `read` collects the chosen ID; `az account set` selects it; `az account show` confirms subscription and tenant; `az group create` creates the DEV group; `az group show` retrieves its full scope. `--query` selects fields and `--output tsv` stores a plain value.

Use an approved region if `westus3` is unsuitable. If the resource group already exists, inspect it before reusing it. This example creates no Azure VM or Splunk cloud server.

### OIDC step 4 Create an identity without a client password

Run these creation commands once. If you resume an earlier setup, reuse its recorded application ID instead of creating duplicate applications.

```bash
AZURE_CLIENT_ID=$(az ad app create \
  --display-name "$OIDC_APP_NAME" \
  --sign-in-audience AzureADMyOrg \
  --query appId --output tsv)

OIDC_APP_OBJECT_ID=$(az ad app show \
  --id "$AZURE_CLIENT_ID" --query id --output tsv)

OIDC_SP_OBJECT_ID=$(az ad sp create \
  --id "$AZURE_CLIENT_ID" --query id --output tsv)

printf 'Client ID: %s\nTenant ID: %s\nSubscription ID: %s\nResource group: %s\n' \
  "$AZURE_CLIENT_ID" "$AZURE_TENANT_ID" "$AZURE_SUBSCRIPTION_ID" "$OIDC_RG"
```

**Command overview:** `az ad app create` registers a single-tenant application; `az ad app show` retrieves its directory object ID; `az ad sp create` creates the service principal used for Azure access; `printf` displays the values needed later. These commands do not create a client password.

Keep the application object ID and service principal object ID distinct. The client ID is used by `azure/login`; the service principal object ID receives the resource role.

### OIDC step 5 Create an exact federated trust

Paste the `sub` copied from the successful claims workflow:

```bash
read -r -p 'Exact main-branch OIDC sub from the GitHub log: ' OIDC_SUBJECT
export OIDC_SUBJECT

python3 - <<'PY'
import json
import os
from pathlib import Path

subject = os.environ["OIDC_SUBJECT"]
if not subject.endswith(":ref:refs/heads/main"):
    raise SystemExit("Expected the inspected main-branch subject.")
credential = {
    "name": "github-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": subject,
    "audiences": ["api://AzureADTokenExchange"],
    "description": "Main branch of the RHEL Splunk lab repository"
}
Path("github-main-federation.json").write_text(
    json.dumps(credential, indent=2) + "\n"
)
PY

cat github-main-federation.json

az ad app federated-credential create \
  --id "$OIDC_APP_OBJECT_ID" \
  --parameters github-main-federation.json

az ad app federated-credential list \
  --id "$OIDC_APP_OBJECT_ID" --output json
```

**Command overview:** `read` captures the exact subject; `export` makes it available to Python; the Python code creates the trust JSON; `cat` lets you inspect it; `az ad app federated-credential create` adds the trust; `list` confirms the stored issuer, subject, and audience.

Before creating the credential, confirm the JSON's subject identifies your actual repository and `main` branch. A branch-based trust can authorize eligible jobs on that branch, not just one workflow filename. Review workflow changes on `main` and enable available branch protections or rulesets. Do not broaden the subject to fix a mismatch.

### OIDC step 6 Grant Reader access to the DEV group

```bash
OIDC_ROLE_ASSIGNMENT_ID=$(az role assignment create \
  --assignee-object-id "$OIDC_SP_OBJECT_ID" \
  --assignee-principal-type ServicePrincipal \
  --role Reader \
  --scope "$OIDC_RG_SCOPE" \
  --query id --output tsv)

az role assignment list \
  --assignee "$OIDC_SP_OBJECT_ID" \
  --scope "$OIDC_RG_SCOPE" \
  --include-inherited --output table
```

**Command overview:** `az role assignment create` assigns the Reader role; `--assignee-object-id` identifies the service principal; `--scope` limits access to one resource group; `list` displays applicable assignments.

Confirm the dedicated identity has only the intended access. Reader is sufficient for this validation workflow; a later deployment task requires its own reviewed permissions. Allow time for identity and role changes to become available before testing.

### OIDC step 7 Add GitHub settings

Return to the **WSL project terminal**. Enter the values displayed in Cloud Shell:

```bash
read -r -p 'Azure client ID: ' AZURE_CLIENT_ID
read -r -p 'Azure tenant ID: ' AZURE_TENANT_ID
read -r -p 'Azure subscription ID: ' AZURE_SUBSCRIPTION_ID

gh secret set AZURE_CLIENT_ID --body "$AZURE_CLIENT_ID"
gh secret set AZURE_TENANT_ID --body "$AZURE_TENANT_ID"
gh secret set AZURE_SUBSCRIPTION_ID --body "$AZURE_SUBSCRIPTION_ID"
gh variable set AZURE_DEV_RESOURCE_GROUP --body rg-siem-oidc-dev

gh secret list
gh variable list
```

**Command overview:** `read` collects the identity IDs; `gh secret set` stores the three login settings; `gh variable set` stores the resource group name; the list commands confirm setting names without revealing secret values.

The IDs are configuration values, not client passwords. This workflow uses GitHub secrets for them, following Microsoft's setup pattern. No `AZURE_CLIENT_SECRET` or password-bearing `AZURE_CREDENTIALS` setting is needed.

### OIDC step 8 Create the Azure login workflow

Create `.github/workflows/azure-oidc.yml` with this complete content:

```yaml
name: Validate Azure OIDC access

on:
  workflow_dispatch:

permissions: {}

jobs:
  verify:
    if: >-
      github.ref == 'refs/heads/main' &&
      github.repository == 'jbanday808/rhel-10v2-splunk-threat-hunting'
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    permissions:
      id-token: write
    env:
      AZURE_CORE_OUTPUT: none
      AZURE_DEV_RESOURCE_GROUP: ${{ vars.AZURE_DEV_RESOURCE_GROUP }}
      EXPECTED_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      EXPECTED_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
    steps:
      - name: Sign in to Azure with OIDC
        uses: azure/login@a641126d1b8aa4d1fa005f4f92df94a3a4c4c906 # v3.1.0
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          audience: api://AzureADTokenExchange
      - name: Verify the subscription and DEV resource group
        shell: bash
        run: |
          set -euo pipefail
          test -n "$AZURE_DEV_RESOURCE_GROUP"
          actual_subscription=$(az account show --query id --output tsv)
          actual_tenant=$(az account show --query tenantId --output tsv)
          test "$actual_subscription" = "$EXPECTED_SUBSCRIPTION_ID"
          test "$actual_tenant" = "$EXPECTED_TENANT_ID"
          az group show --name "$AZURE_DEV_RESOURCE_GROUP" \
            --query '{name:name,location:location}' --output table
```

**Workflow overview:** The manual trigger and job guard select this repository's `main` branch. `id-token: write` allows an OIDC token request; it does not grant Azure write access. `azure/login` exchanges that token for Azure access. The script verifies the subscription and tenant, then reads the DEV group. No checkout step is needed because this example runs no repository code.

The action is pinned to the verified v3.1.0 release commit. Review Azure Login releases and update the pinned commit when adopting fixes; a commit pin does not update itself.

### OIDC step 9 Commit and validate the workflow

In WSL:

```bash
git add .github/workflows/azure-oidc.yml
git diff --cached --check
git diff --cached
git commit -m 'Add Azure OIDC login validation'
git push origin main

gh workflow run azure-oidc.yml --ref main
gh run list --workflow azure-oidc.yml --limit 5
```

**Command overview:** The Git commands review, commit, and push the workflow; `gh workflow run` starts it; `gh run list` shows its status and run ID.

Select the new run:

```bash
read -r -p 'Azure OIDC workflow run ID: ' AZURE_OIDC_RUN_ID
gh run watch "$AZURE_OIDC_RUN_ID" --exit-status
gh run view "$AZURE_OIDC_RUN_ID" --log
```

**Command overview:** `gh run watch --exit-status` waits for the result and returns failure if the run fails; `gh run view --log` displays the observed output.

Confirm the Azure login succeeds, subscription and tenant checks pass, and the expected DEV group appears. A manual run on another existing branch must skip the guarded job. That confirms the workflow guard; the exact federated subject remains the separate Azure trust restriction.

If a Git push is rejected because your GitHub CLI authentication lacks workflow permission, use `gh auth refresh --scopes workflow`, complete its sign-in, and retry the push. Check the repository or organization Actions policy if the pinned Azure action is blocked.

### OIDC step 10 Troubleshoot the actual result

| Observation | Check first |
| --- | --- |
| Token request variables are unavailable. | The job must run in GitHub Actions and have `id-token: write`. |
| Azure reports no matching federated identity. | Compare exact issuer, audience, and observed subject; check case, immutable IDs, branch, environment, and any custom subject template. |
| Azure cannot find the application or tenant. | Confirm the three GitHub secret values and the application's tenant. |
| Login succeeds but reading the group is denied. | Check the principal's Reader assignment, group scope, group name, and propagation delay. |
| A job is skipped. | Confirm the selected branch and exact repository name match its guard. |
| The workflow cannot connect to the private Splunk VM. | GitHub-hosted networking does not reach VMnet8 directly. Plan a separate private connectivity and runner design before adding VM deployment. |

Record the GitHub run URL, commit, observed subject, Azure client ID, role scope, and actual result in `docs/reference/versions.md` or sanitized evidence. Do not record OIDC tokens, Azure access tokens, or session credentials.

### OIDC step 11 Disable access when the lab no longer needs it

To pause this integration, disable **Validate Azure OIDC access** from the workflow's Actions menu. To revoke its Azure exchange capability, return to Cloud Shell, confirm the dedicated application's recorded object ID, and remove its `github-main` federated credential:

```bash
read -r -p 'Dedicated OIDC application object ID: ' OIDC_APP_OBJECT_ID

az ad app federated-credential list \
  --id "$OIDC_APP_OBJECT_ID" --output table

read -r -p 'ID of its github-main federated credential: ' OIDC_FEDERATED_ID

az ad app federated-credential delete \
  --id "$OIDC_APP_OBJECT_ID" \
  --federated-credential-id "$OIDC_FEDERATED_ID"
```

**Command overview:** `read` selects the recorded application and credential IDs; `list` lets you verify the target; `delete` removes that specific trust. It does not delete the DEV resource group or the Splunk lab. Removing the trust prevents new token exchanges; already issued Azure access tokens remain valid until they expire.

**Summary:** GitHub issues a short-lived identity token, Entra verifies its exact trust claims, and Azure grants only the dedicated identity's resource permissions. The example verifies access to one DEV resource group while the original RHEL and LDAPS procedures remain available in the same guide.

References:

- [GitHub Azure OIDC Guide](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure): This guide explains GitHub token permissions and Azure trust for workflow authentication.
- [GitHub OIDC Reference](https://docs.github.com/en/actions/reference/security/oidc): This reference explains issuer, audience, subject formats, immutable IDs, and token request variables.
- [Microsoft Azure Login with OIDC Guide](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect): This guide explains Entra identities and GitHub settings for Azure Login.
- [Microsoft Federated Identity Setup Guide](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust): This guide explains creating an application's federated credential.
- [Azure Role Assignment Guide](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-cli): This guide explains assigning a role to a service principal at a specific scope.
- [Azure Cloud Shell Ephemeral Session Guide](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/ephemeral): This guide explains starting Bash without a persistent storage account.
- [Azure Login Action](https://github.com/Azure/login): This repository documents supported versions, inputs, and commit pinning.
- [Azure Login v3.1.0 Commit](https://github.com/Azure/login/commit/a641126d1b8aa4d1fa005f4f92df94a3a4c4c906): This release commit is the action version pinned in the example workflow.

---

## Appendix NGINX log collection and upgrade safe configuration

**The correct answer in the supplied example is Option A:** `$SPLUNK_HOME/etc/apps/Splunk_TA_nginx/local/inputs.conf`. For this lab, the full path is `/opt/splunk/etc/apps/Splunk_TA_nginx/local/inputs.conf`.

Place your input changes in the add-on's `local` folder. Splunk combines them with the vendor defaults, and standard upgrades preserve local customizations. Keep a backup and validate the effective settings after an upgrade. Editing an app's `default/inputs.conf` risks losing the change when its vendor files are replaced.

This exercise runs NGINX on RHEL-SPLUNK01 and collects its access and error logs locally. The test web server listens only on `127.0.0.1:80`, so the curl test runs inside RHEL. The existing `lab` index and `lab_hunter` permissions are reused.

### NGINX step 1 Install the required software and add on

Complete the original RHEL Splunk setup first. Then, on RHEL:

```bash
sudo dnf install -y nginx acl curl

rpm -q nginx
sudo systemctl status Splunkd --no-pager
```

**Command overview:** `dnf install` installs NGINX, access-control tools, and curl; `rpm -q` shows the installed NGINX version; `systemctl status` checks Splunk.

Download a compatible **Splunk Add-on for NGINX** from its official Splunk page. In Splunk Web, use **Apps → Manage Apps → Install app from file**, install the vendor package, and restart if requested. Record the exact version in `docs/reference/versions.md`.

Confirm the installed app folder:

```bash
sudo ls -d /opt/splunk/etc/apps/Splunk_TA_nginx
```

The ZIP contains the custom `local/inputs.conf` overlay. Install the official add-on before deploying this overlay; its vendor parsing and search settings are supplied by that separate package.

### NGINX step 2 Create the local test web server configuration

The following configuration is for this dedicated learning VM. If NGINX already hosts another application, merge an appropriate test server into its existing configuration instead of replacing that application's settings.

```bash
cd "$HOME/rhel-splunk-threat-hunting"
mkdir -p configs/nginx apps/Splunk_TA_nginx/local

cat > configs/nginx/nginx.conf <<'EOF'
user nginx;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log warn;

events {
    worker_connections 256;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log /var/log/nginx/access.log combined;
    sendfile on;

    server {
        listen 127.0.0.1:80;
        server_name localhost;
        root /usr/share/nginx/html;

        location = /siem-lab {
            default_type text/plain;
            return 200 "SIEM-LAB-NGINX-TEST\n";
        }
    }
}
EOF
```

**Configuration overview:** `listen` limits the server to loopback; `access_log ... combined` uses the standard combined access-log format; `error_log` records errors; the `/siem-lab` location returns a harmless test marker.

For the dedicated lab server, preserve its current file, test the new configuration, and install it:

```bash
NGINX_BACKUP="/etc/nginx/nginx.conf.before-siem-$(date -u +%Y%m%dT%H%M%SZ)"
sudo cp -a /etc/nginx/nginx.conf "$NGINX_BACKUP"

sudo nginx -t -c "$PWD/configs/nginx/nginx.conf"

sudo install -o root -g root -m 644 \
  configs/nginx/nginx.conf /etc/nginx/nginx.conf

sudo restorecon -RF /etc/nginx /var/log/nginx
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx
```

**Command overview:** `cp -a` backs up the current settings; `nginx -t` checks configuration; `-c` selects the proposed file; `install` deploys it with defined ownership and permissions; `restorecon` restores SELinux labels; `enable` enables automatic startup; `restart` starts NGINX with the installed configuration.

### NGINX step 3 Generate an access event with curl

Run inside RHEL-SPLUNK01:

```bash
curl --fail --silent --show-error \
  --user-agent 'SIEM-LAB-NGINX-TEST' \
  http://127.0.0.1/siem-lab

sudo tail -n 5 /var/log/nginx/access.log
```

**Command overview:** `curl` makes the request; `--fail` reports HTTP error responses as failures; `--silent` hides the progress meter; `--show-error` displays errors; `--user-agent` puts a recognizable marker in the access log; the URL selects the loopback test endpoint; `tail -n 5` shows recent log entries.

**Expected result:** The response contains `SIEM-LAB-NGINX-TEST`, and the access log contains a request for `/siem-lab` with the marker as its user agent. HTTP is used only for this loopback test endpoint; Splunk Web and Windows forwarding retain their existing TLS settings.

### NGINX step 4 Allow the Splunk account to read the logs

```bash
sudo setfacl -m u:splunk:rx /var/log/nginx
sudo setfacl -d -m u:splunk:rx /var/log/nginx
sudo setfacl -m u:splunk:r \
  /var/log/nginx/access.log /var/log/nginx/error.log

getfacl /var/log/nginx
sudo -u splunk head -n 1 /var/log/nginx/access.log
```

**Command overview:** `setfacl -m` grants the service account access; `-d` supplies an inherited default for new log files; directory `rx` permits traversal and listing; file `r` permits reading; `getfacl` displays the access rules; `head` confirms that the account can read an entry.

Retest reading after log rotation. If collection still fails under SELinux, inspect `sudo ausearch -m AVC -ts recent` and Splunk's log; keep SELinux enforcing while investigating the actual denial.

### NGINX step 5 Configure the add on local input

Create the source overlay:

```bash
cat > apps/Splunk_TA_nginx/local/inputs.conf <<'EOF'
[monitor:///var/log/nginx/access.log]
disabled = 0
index = lab
sourcetype = nginx:plus:access
host = splunk01

[monitor:///var/log/nginx/error.log]
disabled = 0
index = lab
sourcetype = nginx:plus:error
host = splunk01
EOF
```

**Configuration overview:** Each `monitor` section selects one log; `disabled = 0` enables collection; `index = lab` chooses storage; `sourcetype` selects the vendor's rules; `host` labels the source computer. The `nginx:plus:access` source type supports this combined-format access log and does not require an NGINX Plus subscription for this file-monitoring example.

If the installed `local/inputs.conf` already exists, review it and merge these two sections without discarding unrelated inputs. For a fresh add-on installation:

```bash
sudo install -d -o splunk -g splunk -m 750 \
  /opt/splunk/etc/apps/Splunk_TA_nginx/local

sudo install -o splunk -g splunk -m 640 \
  apps/Splunk_TA_nginx/local/inputs.conf \
  /opt/splunk/etc/apps/Splunk_TA_nginx/local/inputs.conf

sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool inputs list \
  'monitor:///var/log/nginx/access.log' --debug

sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

**Command overview:** `install -d` creates the local override directory; `install -m 640` deploys the input file; `btool check` validates settings; `btool inputs list ... --debug` identifies the effective input and its source file; `systemctl` restarts and checks Splunk.

### NGINX step 6 Confirm collection and upgrade behavior

Repeat the curl command after restarting Splunk. In the Threat Hunting Lab app:

```spl
index=lab sourcetype=nginx:plus:access "SIEM-LAB-NGINX-TEST"
earliest=-15m latest=now
| table _time host source sourcetype _raw
```

**Command overview:** The index and source type select access records; the quoted marker finds the curl request; the time terms select recent events; `table` shows the record and its source details.

Save a reusable search in the project:

```bash
cat > hunts/09-nginx-access.spl <<'EOF'
index=lab sourcetype=nginx:plus:access earliest=-24h
| stats count by host status
| sort - count
EOF
```

If the raw event is present but expected fields are missing, verify the installed add-on's version, log format, source type, and app permissions. If the event is absent, inspect the file path, service-account access, input enablement, index, and time range first.

Before an add-on upgrade, back up the installed `local` folder to protected storage. After upgrading, rerun `btool` and the curl/search test. Do not replace the vendor `default` folder with files from this ZIP. Record actual results in `evidence/sanitized/nginx-validation.md`.

**Summary:** Install the vendor add-on, generate a known request, grant log access, configure `Splunk_TA_nginx/local/inputs.conf`, and verify the resulting event in Splunk.

References:

- [Splunk NGINX Input Guide](https://splunk.github.io/splunk-add-on-for-nginx/Configureinputsv2monitor/): This guide explains the local input file and the source types for NGINX logs.
- [Splunk Configuration Directories Guide](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/administer-splunk-enterprise-with-configuration-files/configuration-file-directories): This guide explains default files, local overrides, and upgrades.
- [Red Hat NGINX Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/deploying_web_servers_and_reverse_proxies/setting-up-and-configuring-nginx): This guide explains installing and configuring NGINX on RHEL.
- [curl Manual](https://curl.se/docs/manpage.html): This manual explains the request and error-handling options used in the test.

---

## Appendix Use the complete ZIP on Windows and upload to GitHub

The downloadable `rhel-splunk-threat-hunting-complete.zip` contains an assembled source project named `rhel-splunk-threat-hunting`. It includes the complete Word and Markdown guides, all 52 step files, configuration files, scripts, hunting searches, LDAP examples, NGINX overrides, and GitHub Actions workflows.

Vendor operating-system images, Splunk installers, vendor add-on packages, certificates, and live credentials are obtained or generated on your machines using the guide. Their download and setup instructions are included in the project.

### Package step 1 Download and extract on Windows 11

Save the ZIP in your Windows Downloads folder. Use **Extract All** in File Explorer, or open Windows PowerShell and run:

```powershell
$ZipFile = Join-Path $env:USERPROFILE 'Downloads\rhel-splunk-threat-hunting-complete.zip'
$ExtractRoot = Join-Path $env:USERPROFILE 'Documents\SIEMLab-Complete'

if (Test-Path -LiteralPath $ExtractRoot) {
    throw 'Choose a new extraction folder to preserve existing work.'
}

Expand-Archive -LiteralPath $ZipFile -DestinationPath $ExtractRoot
$Project = Join-Path $ExtractRoot 'rhel-splunk-threat-hunting'
Set-Location -LiteralPath $Project
Get-ChildItem -Force
```

**Command overview:** `Join-Path` builds paths for your Windows account; `Test-Path` checks for an existing folder; `Expand-Archive` extracts the ZIP; `Set-Location` opens the project; `Get-ChildItem -Force` shows all entries, including `.github`.

Open **start-here/START_HERE_WINDOWS.md** first in the current GitHub layout. The `.zip` itself is a download package; GitHub receives the extracted project contents.

### Package step 2 Review the included folders

| Folder or file | Contents |
| --- | --- |
| `README.md` | Project purpose, deployment order, and links. |
| `start-here/START_HERE_WINDOWS.md` | Windows extraction, checks, and GitHub upload instructions. |
| `apps/LAB_SIEM` | Splunk server settings, role, permissions, and dashboard. |
| `apps/LAB_UF_WINDOWS` | Windows event inputs and verified TLS forwarding settings. |
| `apps/Splunk_TA_nginx/local` | Custom NGINX inputs to apply after installing the vendor add-on. |
| `configs` | rsyslog, log rotation, NGINX, and systemd examples. |
| `scripts/rhel` | Storage preparation, backups, deployment checks, and NGINX helpers. |
| `scripts/windows` | Audit setup, Sysmon, forwarder deployment, lab activity, and package checks. |
| `scripts/azure` | OIDC identity-setup and trust instructions. |
| `sysmon` | The lab's Sysmon XML configuration. |
| `hunts` | Original hunting searches plus NGINX and integrity searches. |
| `docs/steps` and `docs/appendices` | The full procedures split into numbered files. |
| `docs` | The full Word and text guides, architecture, version records, and LDAP examples. |
| `evidence/sanitized` | Validation and investigation templates with results marked Pending. |
| `.github/workflows` | Linux and Windows project checks, OIDC inspection, and Azure OIDC validation. |
| `FILE_MANIFEST.json` | Initial file list and SHA-256 values for package verification. |

The package has the final assembled custom files. When using those files, follow the guide's installation, review, and deployment instructions; you can skip recreating a file with a `cat >` block when the included file already supplies it. Retain later additions if you choose to recreate earlier configuration files. The packaged `[lab]` index includes the integrity setting described in its appendix.

### Package step 3 Verify the extracted files

Read `scripts/windows/Test-Project.ps1`, then run it from the extracted project in Windows PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\windows\Test-Project.ps1 -VerifyManifest
```

**Command overview:** `-NoProfile` opens a clean PowerShell process; `-ExecutionPolicy Bypass` permits this reviewed local check in that process; `-File` selects the validator; `-VerifyManifest` checks initial file hashes. It does not change the machine's persistent execution policy.

The validator checks required files, parses the PowerShell scripts and XML, and optionally verifies the initial manifest. On RHEL or WSL, run `python3 scripts/validate_project.py --verify-manifest` for Python, shell, XML, JSON, and project configuration checks. A source check does not replace the live Splunk, NGINX, Windows, or Azure validation steps.

The manifest describes the downloaded release. Editing a file changes its hash; use normal validation without `-VerifyManifest` after making your own changes.

### Package step 4 Install Git and GitHub CLI

On the physical Windows host, install Git for Windows and GitHub CLI from their official installers, or use WinGet:

```powershell
winget install --id Git.Git --exact --source winget
winget install --id GitHub.cli --exact --source winget
```

Close and reopen PowerShell so it picks up the installed command paths. Return to the extracted project, then check and authenticate:

```powershell
git --version
gh --version
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
gh api user --jq .login
```

**Command overview:** `winget install` installs the named tools; the version commands confirm them; `gh auth login` opens GitHub sign-in; `gh auth setup-git` connects Git to that authentication; `gh api user` displays the signed-in account.

Confirm the correct account before uploading. If the owner or repository name differs from the OIDC example, update both OIDC workflow guards and capture the actual subject before configuring Azure trust.

### Package step 5 Initialize and review a new local repository

From the extracted project root, use these commands only when it has no existing `.git` directory:

```powershell
git init -b main
git config user.name 'James Banday'
$CommitEmail = Read-Host 'Your verified GitHub email or GitHub noreply email'
git config user.email $CommitEmail

git add .
git diff --cached --check
git diff --cached --stat
git status --short
```

**Command overview:** `git init` creates the local repository and its main branch; `git config` sets this project's author details; `git add` stages included files; `git diff` checks and summarizes them; `git status` shows what will be committed.

Inspect the staged list. The included `.gitignore` excludes generated keys, certificates, installers, live authentication settings, backups, and raw evidence. Keep credentials out of source files. The `.gitattributes` file keeps shell files in Linux format and PowerShell files in Windows format.

### Package step 6 Commit and upload the extracted project

For a new GitHub repository:

```powershell
git commit -m 'Add complete RHEL Splunk lab with LDAP NGINX and Azure OIDC'

gh repo create rhel-splunk-threat-hunting `
  --private --source . --remote origin --push

gh repo view --web
```

**Command overview:** `git commit` records the reviewed project; `gh repo create` creates a private GitHub repository; `--source .` uses the extracted project; `--remote origin` connects it; `--push` uploads the commit; `gh repo view --web` opens the repository.

If that repository already exists, preserve it by cloning it into a separate folder first with `gh repo clone OWNER/REPOSITORY`. Copy and merge the extracted source files into that checkout, review `git status` and `git diff`, and commit and push there. Do not replace its `.git` directory or force-push over its history. For authentication that needs workflow-file permission, use `gh auth refresh --scopes workflow` and complete its sign-in.

Use the command-line upload so `.github`, nested configuration folders, and all source files are included together. Git tracks files rather than empty folders; `.gitkeep` files preserve the intended non-private empty folders in this package.

### Package step 7 Confirm GitHub and follow the deployment order

Open the repository's **Actions** tab and inspect **Validate project**. It checks source files on GitHub-hosted Linux and Windows machines. Its result does not claim the lab VMs are already deployed. Run the two OIDC workflows manually only after following the OIDC appendix in order.

Then follow these stages:

1. Complete VMware, networking, RHEL, storage, certificates, and the Splunk server through Step 20.
2. Configure the Windows endpoint, forwarder, Sysmon, hunting activity, and dashboard through Step 30.
3. Configure and validate IdM and LDAPS through Step 44.
4. Complete alerts, cleanup, backup, final checks, and documentation through Step 52.
5. Follow the data-phase, integrity, NGINX, and OIDC appendices as needed, recording actual results in the included evidence templates.

The RHEL helpers live under `scripts/rhel`, and Windows helpers live under `scripts/windows`. Their README files identify where each runs and its prerequisites. Storage formatting and credential-dependent operations remain explicit steps in the guide.

**Summary:** Extract the ZIP, review and validate the files, authenticate GitHub, commit the project, upload it, and then document the results of each live lab procedure.

References:

- [GitHub Local Project Upload Guide](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github): This guide explains importing a local project through Git and GitHub CLI.
- [GitHub Repository Creation Manual](https://cli.github.com/manual/gh_repo_create): This manual explains `--source`, `--remote`, and `--push`.
- [Git for Windows](https://git-scm.com/install/windows): This page provides the official Windows Git installer.
- [GitHub CLI Installation](https://cli.github.com/): This page provides GitHub CLI installation options.

---

## Appendix Password redaction before indexing

**Question 151 answer: B.** Put `SEDCMD-redact_pw` in `props.conf` under the source type that receives the events. The following lab procedure uses `[identity]`. It changes the incoming raw event during parsing before storage. `REGEX-redact_pw` is not a valid substitute for this setting, and `SEDCMD` does not belong in `transforms.conf`.

Run this exercise after `LAB_SIEM` and the `lab` index work. Configure RHEL-SPLUNK01, which parses this local text file. In a distributed deployment, configure and test the first full parsing tier before sending sensitive events. This exercise does not use structured indexed extractions.

This example masks lowercase, unquoted `password=value` tokens whose values end at whitespace, a comma, or the end of the event. It supports slashes within the value. Quoted values containing spaces, JSON properties, and other field spellings need separate rules and tests. Use only the fake `LAB-DUMMY` values below until the live result is verified.

### Redaction step 1 Open the project on the RHEL server

Copy the extracted source project to RHEL-SPLUNK01 using the guide's existing transfer process, then open a terminal there. Use your actual project location if it differs:

```bash
cd ~/rhel-splunk-threat-hunting
test -d apps/LAB_SIEM/local
sudo systemctl is-active Splunkd
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug
```

**Command overview:** `cd` opens the source project; `test` checks its app folder; `systemctl` checks the service; `btool` shows the effective lab index and the files supplying its settings. Confirm the index and service before continuing.

Keep the existing `siem:lab` source type and other inputs. The ZIP already includes the additions in `apps/LAB_SIEM/local`; the next snippets also support updating an older installed app.

### Redaction step 2 Define the dedicated file input

The ZIP includes this snippet. To recreate it from the project root:

```bash
mkdir -p configs/redaction
cat > configs/redaction/inputs.conf.example <<'EOF'
[monitor:///var/log/siem-lab/identity.log]
disabled = 0
index = lab
sourcetype = identity
host = splunk01
EOF
```

**Command overview:** `mkdir -p` creates the snippet folder; the quoted heredoc writes the stanza literally. The monitor reads one dedicated file, assigns source type `identity`, and stores events in `lab`. The input is enabled with `disabled = 0`.

### Redaction step 3 Define the parsing rule in props conf

Create or review the matching snippet:

```bash
cat > configs/redaction/props.conf.example <<'EOF'
[identity]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = ^
TIME_FORMAT = %Y-%m-%dT%H:%M:%SZ
MAX_TIMESTAMP_LOOKAHEAD = 20
TZ = UTC
KV_MODE = none
REPORT-lab-fields = lab_fields
SEDCMD-redact_pw = s/\b(password=)[^,\s]+/\1REDACTED/g
EOF
```

**Command overview:** `[identity]` matches the input source type. The timestamp settings match the generator's UTC timestamp, and line breaking keeps each log line separate. `REPORT-lab-fields` reuses the existing search time extraction for action, result, and account. The `SEDCMD` setting performs the masking before indexing.

Read the substitution as follows:

| Part | Purpose |
| --- | --- |
| `s/…/…/g` | Replace every matching occurrence in the event. |
| `\b(password=)` | Match the lowercase key at a word boundary and capture it. |
| `[^,\s]+` | Match one or more value characters through the next comma or whitespace. |
| `\1REDACTED` | Keep the captured key and replace the value with `REDACTED`. |

For example, `password=LAB-DUMMY-ONE` becomes `password=REDACTED`. The replacement preserves the key and uses the correctly spelled marker. Preserve the backslashes and straight quotes when copying commands.

### Redaction step 4 Merge the additions and restart Splunk

Review the supplied helper files before running them. Preview the changes first:

```bash
sudo python3 scripts/merge_redaction_config.py \
  --target-dir /opt/splunk/etc/apps/LAB_SIEM/local
```

**Command overview:** The merger checks both installed configuration files before proposing changes. Preview mode writes nothing. It appends an absent stanza, accepts a matching stanza, and stops if the named stanza exists with incomplete or conflicting settings.

Then use the RHEL installer:

```bash
sudo bash scripts/rhel/install-redaction-lab.sh
```

**Command overview:** The installer applies the preflighted merge, backs up changed files under `/var/backups/siem-lab/redaction-*`, prepares the dedicated log with `root:splunk` ownership and mode `0640`, restores SELinux labels, checks the configuration, and restarts `Splunkd`. It does not truncate an existing log.

For a manual update, back up the installed app outside the repository. Merge the snippets into its `local/inputs.conf` and `local/props.conf`, adding each stanza once. Retain existing stanzas and `transforms.conf`; never overwrite a complete configuration with a snippet.

Resolve conflicting stanzas manually, then rerun preview. If installation stops after a change, inspect its backup and configuration errors before retrying. Use dummy credentials throughout.

### Redaction step 5 Verify the effective configuration

Run these commands even when the installer has printed them:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool props list identity --debug
sudo -u splunk /opt/splunk/bin/splunk btool inputs list \
  'monitor:///var/log/siem-lab/identity.log' --debug
sudo -u splunk test -r /var/log/siem-lab/identity.log
sudo systemctl is-active Splunkd
```

**Command overview:** `btool` checks configuration and shows effective settings and their files; `test -r` checks source access; `systemctl` checks service status.

Confirm that effective `[identity]` includes the intended `SEDCMD-redact_pw`, that the monitor uses `sourcetype = identity`, `index = lab`, and `disabled = 0`, and that the values come from the intended local configuration. Resolve conflicting overrides before continuing. A successful configuration listing does not prove that an event has been masked.

### Redaction step 6 Generate a fresh dummy event

After the restart and checks succeed, run the supplied generator:

```bash
sudo bash scripts/rhel/generate-redaction-marker.sh
```

**Command overview:** The generator appends one UTC record containing two fake password tokens and prints a unique `SIEM-LAB-REDACTION-…` test ID. Copy that exact ID. The second token tests the global replacement flag.

The source record has this layout, with generated timestamp and ID values:

```text
2026-11-01T12:00:00Z action=redaction_check result=success account=labadmin password=LAB-DUMMY-ONE password=LAB-DUMMY-TWO test_id=SIEM-LAB-REDACTION-EXAMPLE
```

This is an example, not an observed event. The actual source file still contains its fake plaintext values. `SEDCMD` changes the ingested event, not the original file. Protect source logs and configure the producing application to avoid logging real passwords.

### Redaction step 7 Inspect the stored raw event

In Splunk Search, use an account allowed to search `lab`. Replace the example marker with the exact newly printed ID:

```spl
index=lab sourcetype=identity source="/var/log/siem-lab/identity.log"
"SIEM-LAB-REDACTION-REPLACE-WITH-EXACT-ID" earliest=-15m latest=now
| table _time host source sourcetype _raw
```

**Command overview:** The base search selects the dedicated source and test ID; `table` displays the stored `_raw` value. Allow ingestion time, then rerun the same search. Both `password=` occurrences should read `password=REDACTED`. This search applies no display masking.

Use the same exact ID in the count check:

```spl
index=lab sourcetype=identity source="/var/log/siem-lab/identity.log"
"SIEM-LAB-REDACTION-REPLACE-WITH-EXACT-ID" earliest=-15m latest=now
| eval unmasked=if(match(_raw,"password=LAB-DUMMY-"),1,0)
| eval masked=if(match(_raw,"password=REDACTED"),1,0)
| stats count AS events sum(masked) AS masked_events sum(unmasked) AS unmasked_events
```

**Command overview:** `match` checks the stored event text; `eval` labels each event; `stats` counts the retrieved, masked, and unmasked events. A pass requires `events > 0`, `masked_events = events`, `unmasked_events = 0`, and visual confirmation that both values are replaced. Zero matching events is an incomplete test.

The ZIP includes a reusable recent-event overview search:

```bash
cat > hunts/11-password-redaction-check.spl <<'EOF'
index=lab sourcetype=identity source="/var/log/siem-lab/identity.log"
"SIEM-LAB-REDACTION-" earliest=-15m latest=now
| eval unmasked=if(match(_raw,"password=LAB-DUMMY-"),1,0)
| eval masked=if(match(_raw,"password=REDACTED"),1,0)
| stats count AS events sum(masked) AS masked_events sum(unmasked) AS unmasked_events
EOF
```

**Command overview:** The heredoc saves the search for later use. Its broad marker covers recent redaction exercises; use an exact ID when validating a specific change. Record the live observations in `evidence/sanitized/redaction-validation.md`.

### Redaction step 8 Test changes and troubleshoot

From the extracted project root on RHEL or WSL, run the source checks and offline tests:

```bash
python3 scripts/validate_project.py
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

**Command overview:** The validator checks source files and lab settings. Tests cover dummy values, delimiters, repeated keys, and safe merging; `-B` prevents bytecode files. Python checks shared regex features, so live Splunk verification remains required. GitHub's Linux workflow runs these tests.

If events are missing, check the exact ID, time range, index permission, monitor path, source readability, service status, and Splunk internal logs. If plaintext dummy values remain, confirm the event source type and effective parsing rule, check for overrides, restart the parsing instance, and generate a fresh marker. Search time `replace` or `rex mode=sed` can change displayed output, so do not use them to prove stored-data redaction.

The rule applies only to events ingested after activation. It does not rewrite existing indexed events. The fishbucket reset in the earlier guide can cause replay; it is not a repair for previously stored secrets. Use a new dummy event for each test. For real historical exposure, follow your organization's incident and data-remediation process, including credential rotation where applicable.

Retest the original `siem:lab` marker. Record the new test ID, count, configuration path, commit, and time. Review the diff before publishing; keep backups and raw evidence outside GitHub.

**Summary:** Match the input's source type to `[identity]`, place `SEDCMD-redact_pw` in the parsing tier's `props.conf`, restart, generate a fresh dummy record, and verify its stored `_raw` before relying on the rule.

References:

- [Splunk Props Configuration Reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/props.conf): Defines `SEDCMD`, substitution syntax, captured replacements, and index time use.
- [Splunk Data Anonymization Guide](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.6/configure-event-processing/anonymize-data): Explains source type matching and deployment on the parsing Splunk Enterprise instance.

---

## Appendix HTTP Event Collector endpoint and curl test

**Question 154 answer: A.** Use `/services/collector`, or `https://172.25.250.10:8088/services/collector` in this lab. HEC defaults to HTTPS on port 8088; use your configured port if different.

This adds an application-event input alongside the port 9997 receiver. Send only the harmless payload below: the local `identity` redaction rule does not cover source type `siem:hec`.

### HEC step 1 Identify the endpoint

| Path | Use |
| --- | --- |
| `/services/collector` | Receive JSON event envelopes. Correct choice for Question 154. |
| `/services/collector/event` | Explicit JSON event endpoint. |
| `/services/collector/raw` | Receive raw text; requires a request channel. |
| `/services/collector/health` | Check whether HEC can accept data. |

Splunk Web on port 8000 is the administration interface. The management API usually uses port 8089. Send this exercise's data to the HEC listener on port 8088.

### HEC step 2 Enable the collector in Splunk Web

Sign in as a Splunk administrator at `https://172.25.250.10:8000`. Open **Settings > Data Inputs > HTTP Event Collector > Global Settings**. Enable **All Tokens**, select **Enable SSL**, use port **8088**, and save. Keep deployment-server distribution off for this standalone lab.

Confirm `lab` exists and the Step 15 certificate is current, includes IP `172.25.250.10`, and is readable by Splunk. The client uses its verified public CA.

### HEC step 3 Configure the lab TLS certificate

The ZIP supplies this global-settings example:

```bash
mkdir -p configs/hec
cat > configs/hec/inputs.conf.example <<'EOF'
[http]
disabled = 0
port = 8088
enableSSL = 1
serverCert = /opt/splunk/etc/auth/lab/splunk01.pem
EOF
```

**Command overview:** The example defines global HEC and certificate settings. It contains no token and is not automatically installed.

On RHEL-SPLUNK01, back up the existing HEC local configuration before editing:

```bash
sudo install -d -m 0700 /var/backups/siem-lab
sudo install -d -o splunk -g splunk -m 0700 \
  /opt/splunk/etc/apps/splunk_httpinput/local
sudo bash -c 'if test -f /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf; then
  cp -a /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf \
    /var/backups/siem-lab/hec-inputs-$(date -u +%Y%m%dT%H%M%SZ).conf
fi'
sudoedit /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf
```

**Command overview:** `install -d` prepares protected folders; `cp -a` preserves the existing file in a timestamped backup; `sudoedit` opens the live file.

Merge these settings into the single `[http]` stanza, adding it once if absent. Preserve other settings and `[http://…]` token stanzas; never overwrite the complete file with this example.

Apply ownership, check the settings, and restart:

```bash
sudo chown splunk:splunk /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf
sudo chmod 0600 /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf
sudo restorecon -v /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
sudo ss -lntp 'sport = :8088'
```

**Command overview:** Ownership and mode protect the file; `restorecon` restores SELinux labeling; `btool` checks configuration; `systemctl` restarts Splunk; `ss` checks the listener. Resolve errors before testing. Verify HEC's `[http]` certificate separately from the browser connection.

### HEC step 4 Create a dedicated lab token

In **Settings > Data Inputs > HTTP Event Collector**, choose **New Token**. Name it `siem-lab-curl`. Set default source type to `siem:hec`, default index to `lab`, and allowed indexes to only `lab`. Review and submit. Ensure this individual token is enabled. Leave indexer acknowledgment off for this simple exercise; an acknowledgment-enabled client needs a channel and acknowledgment polling.

Keep the token in your password manager and use the hidden prompt. Keep live HEC configurations, backups, and full `btool inputs list` output outside GitHub; they can contain tokens.

### HEC step 5 Review the payload and send it with curl

Run as `labadmin` in the RHEL project root. Review `examples/hec/event.json` and `scripts/rhel/send-hec-event.sh`, then execute:

```bash
bash scripts/rhel/send-hec-event.sh
```

**Command overview:** The sender hides token entry, prepares private temporary files, sends one JSON event with a unique `SIEM-LAB-HEC-…` ID, checks the response, and removes temporary files. Keep shell tracing off.

Its curl request is:

```bash
curl --fail-with-body --silent --show-error \
  --connect-timeout 10 --max-time 30 \
  --cacert "$CA_FILE" \
  --header "@$WORK_DIR/headers" \
  --data-binary "@$WORK_DIR/event.json" \
  "$HEC_URL" > "$WORK_DIR/response.json"
```

**Command overview:** The sender sets `HEC_URL` to this lab's collector, `CA_FILE` to `/home/labadmin/siem-public/ca.pem`, and `WORK_DIR` to its private temporary folder. `--cacert` verifies trust and the address; `--header @file` reads the protected `Authorization: Splunk <token>` header; `--data-binary @file` sends JSON. Timeouts bound the request. HTTP errors and nonzero HEC response codes fail the test.

The JSON envelope contains `index`, `sourcetype`, `source`, `host`, and `event`; its harmless event begins with `action=hec_check`. The helper prints the unique ID and avoids automatic retries, which could duplicate accepted events.

### HEC step 6 Confirm the event is indexed

Copy the newly printed test ID into this Splunk search:

```spl
index=lab sourcetype=siem:hec source="hec:siem-lab"
"SIEM-LAB-HEC-REPLACE-WITH-EXACT-ID" earliest=-15m latest=now
| table _time host source sourcetype _raw
```

**Command overview:** The search displays the stored event. Confirm at least one result with the expected metadata and exact ID. HTTP acceptance alone does not prove indexing.

The ZIP also includes this reusable search:

```bash
cat > hunts/12-hec-ingestion-check.spl <<'EOF'
index=lab sourcetype=siem:hec source="hec:siem-lab"
"SIEM-LAB-HEC-" earliest=-24h latest=now
| table _time host source sourcetype _raw
EOF
```

**Command overview:** The heredoc saves the recent-event search. Use an exact test ID for a specific validation run and record observations in `evidence/sanitized/hec-validation.md`.

### HEC step 7 Troubleshoot and control client access

For connection failures, check the service, listener, and URL. For TLS failures, check the CA, expiry, and certificate names. For authorization failures, check global and token enablement and the `Splunk` header prefix. Check that `lab` exists and is allowed. For missing search results, check permissions, metadata, time range, and indexing health.

This exercise sends from RHEL-SPLUNK01 to its own lab address, so it needs no remote-client firewall opening. To use WINHUNT01 as a client later, permit only its address in the existing `siem-lab` firewall zone:

```bash
sudo firewall-cmd --permanent --zone=siem-lab \
  --add-rich-rule='rule family=ipv4 source address=172.25.250.20/32 port port=8088 protocol=tcp accept'
sudo firewall-cmd --reload
sudo firewall-cmd --zone=siem-lab --list-rich-rules
```

**Command overview:** The optional rule allows TCP 8088 from the Windows lab endpoint; reload applies it, and the list command verifies it. A remote client also needs the verified public CA and a dedicated token. Disable unused test tokens in Splunk Web after the exercise, and remove this optional firewall rule if remote collection is no longer needed.

**Summary:** Use `/services/collector` for HEC JSON events, enable TLS and a dedicated token, send a unique curl marker, and verify the indexed event in Splunk.

References:

- [Splunk Input Endpoint Reference](https://help.splunk.com/en/splunk-enterprise/rest-api-reference/10.6/input-endpoints/input-endpoint-descriptions): Defines HEC paths and the standard event endpoint.
- [Splunk Web HEC Setup](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.6/get-data-with-http-event-collector/set-up-and-use-http-event-collector-in-splunk-web): Explains global enablement, token creation, and allowed indexes.
- [Splunk Inputs Configuration Reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/inputs.conf): Defines the HEC listener's `[http]` TLS and port settings.
- [curl Manual](https://curl.se/docs/manpage.html): Defines the certificate, header-file, payload, and failure options used by the sender.
