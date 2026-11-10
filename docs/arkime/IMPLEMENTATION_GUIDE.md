# Arkime on RHEL 10.2 — Installation, Configuration and Deployment

This optional, step-by-step lab adds Arkime to the Splunk threat-hunting project. You will install Arkime and a single-node OpenSearch database on a **new sensor VM**, import two locally generated packet files, and investigate a known synthetic anomaly. The [companion case](INVESTIGATION.md) gives the analyst workflow and expected observations.

For an **offline Kali workstation** instead of this RHEL sensor, use the [Kali cross-tool guide](../network-defense/KALI_DEPLOYMENT.md). Its container-based OpenSearch configuration is isolated for synthetic evaluation and is not a substitute for this guide's hardened sensor path.

**Status:** planned documentation. These commands have not been run on WINHUNT01, RHEL-SPLUNK01, RHEL-IDM01 or a live sensor. Record your own results; a successful connection or a published guide is not evidence that packet collection works.

## Follow the complete workflow

| Stage | Procedure | Expected checkpoint |
| --- | --- | --- |
| Prepare the sensor | [Steps 1–8](#phase-1--plan-and-prepare) | Verified VM, architecture, clock and two different data filesystems |
| Download and install | [Steps 9–21](#phase-2--download-verify-and-install-opensearch) | Verified vendor packages and local authenticated search service |
| Configure Arkime | [Steps 22–26](#step-22--create-a-private-arkime-configuration) | Restricted configuration, initialized lab database and Viewer over SSH |
| Analyze saved packets | [Steps 27–31](#phase-4--generate-and-import-safe-test-traffic) and [worked case](INVESTIGATION.md) | Synthetic routine and candidate traffic can be inspected |
| Test a live interface locally | [Optional loopback test](CONTROLLED_LIVE_TEST.md) | Known local HTTP requests become retrievable sessions and packets |
| Hunt for anomalies | [Analyst playbook](HUNTING_PLAYBOOK.md) | Baselines, protocol queries, graphs and bounded packet-content Hunt |
| Deploy to an approved segment | [Steps 32–38](#phase-5--authorized-live-deployment-and-operations) | Security prerequisites, capture source, collection quality and operations reviewed |

> **Scope and security:** The detailed path below is a disposable, single-user lab with synthetic data. OpenSearch's installer creates a **demo security configuration**, including publicly known demo users and transport certificates. Binding its services to loopback and replacing its HTTP certificate limits exposure but does not make the demo configuration suitable for real or controlled traffic. Before using any real traffic, replace the demo security configuration and credentials, implement approved least-privilege service accounts and TLS, apply your organization's retention and access controls, and obtain capture authorization. This guide does not certify compliance with a STIG, CMMC or an operational CONOPS.

## Architecture and prerequisites

| Component | Example | Purpose |
| --- | --- | --- |
| Existing Splunk | `RHEL-SPLUNK01`, `172.25.250.10` | Existing event searches; unchanged |
| Existing endpoint | `WINHUNT01`, `172.25.250.20` | Windows and Sysmon events; unchanged |
| Existing identity server | `RHEL-IDM01`, `172.25.250.30` | Existing identity services; unchanged |
| Optional sensor | `RHEL-SENSOR01`, example `172.25.250.40` | Arkime, local OpenSearch, synthetic analysis |
| Search data | `/srv/arkime-opensearch` | Dedicated filesystem on a new disk |
| Packet data | `/srv/arkime-pcap` | Different dedicated filesystem on a second new disk |

The addresses are examples; confirm VMware networking, name resolution and available addresses before assigning them. The first three VMs and the six existing Splunk indexes (`win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`) do not need changes. Arkime session metadata resides in OpenSearch, while packet files remain on the sensor. They are not automatically events in Splunk.

For this example use an x86-64 RHEL 10.2 VM with an active subscription or approved package repositories, sudo access, internet access to approved vendor sources, **at least 8 GB RAM, 4 vCPUs**, an OS disk, and two additional empty virtual disks. These are lab starting points, not production sizing. For a small exercise, 40 GB for each new data disk is a starting point; packet retention depends on volume. A larger deployment needs separate search nodes, resilient storage and capacity planning. Arkime recommends keeping packet and database storage on separate filesystems.

The examples below use Bash on **RHEL-SENSOR01** unless a step explicitly says Windows PowerShell or Splunk Web. Do not run a Bash command in Windows Command Prompt. Run each command or block in order; stop and investigate unexpected errors. If a command uses an example device, host, or username, replace it with your verified value first.

## Phase 1 — Plan and prepare

### Step 1 — Approve the lab boundary

Use synthetic packet files initially. Confirm the VM's owner, approved network, local storage, access permissions, clock, snapshots, and how to restore the VM. A sensor may see credentials and sensitive content in packets, so collect only traffic you are authorized to retain. A VMware NAT network by itself does not guarantee visibility into traffic between other VMs. Obtain a real mirror/TAP or a deliberately configured test source before enabling live capture.

### Step 2 — Create the optional sensor VM

In VMware Workstation, create a new RHEL 10.2 VM named `RHEL-SENSOR01`. Provision the OS disk plus **two distinct new, empty** data disks, then install and update RHEL using approved media and repositories. Connect one management NIC to the approved lab network; a separate capture NIC is used only if a mirror is available. Do not assume an assigned IP address or configure another VM's disk.

Sign in as a named administrator, open a Bash terminal and check the system:

```bash
hostnamectl
cat /etc/redhat-release
uname -m
free -h
ip -brief address
```

**Command overview:** These commands show the host, operating system, CPU architecture, memory and addresses. The pinned package commands below require `x86_64` and RHEL 10. Use the vendor's matching package for another architecture instead of forcing this one.

### Step 3 — Check time and name resolution

```bash
timedatectl
getent hosts splunk01.lab.test
```

**Command overview:** `timedatectl` shows time synchronization. `getent` asks the system resolver for the existing Splunk host. If names or times are wrong, correct them through your lab's approved configuration before using cross-tool timestamps. For the synthetic exercise, Splunk connectivity is optional.

### Step 4 — Inspect the new disks

```bash
lsblk -p -o NAME,SIZE,TYPE,FSTYPE,UUID,MOUNTPOINTS,MODEL,SERIAL
findmnt /
sudo wipefs -n /dev/REPLACE_WITH_VERIFIED_EMPTY_OPENSEARCH_DISK
sudo wipefs -n /dev/REPLACE_WITH_VERIFIED_EMPTY_PCAP_DISK
```

**Command overview:** `lsblk` and `findmnt` identify current storage; `wipefs -n` only lists detected signatures. Replace each intentionally invalid placeholder with the correct **whole new disk** only after comparing size, serial, VMware settings and mount information. Both must be distinct, unmounted, have no mounted children, contain no partitions or signatures, and not be the OS disk or existing Splunk storage. Stop if anything is unclear. Lack of a signature alone does not prove a disk is safe to erase.

### Step 5 — Create the two lab filesystems

**Destructive operation:** `mkfs.xfs` erases the selected device. The next commands are only for the two disks verified in Step 4 on the new sensor. Double-check each device independently. Never use them on `/`, `/splunkdata`, an existing VM disk, or a device containing data you need.

```bash
sudo dnf install -y xfsprogs util-linux
sudo mkfs.xfs /dev/REPLACE_WITH_VERIFIED_EMPTY_OPENSEARCH_DISK
sudo mkfs.xfs /dev/REPLACE_WITH_VERIFIED_EMPTY_PCAP_DISK
sudo mkdir -p /srv/arkime-opensearch /srv/arkime-pcap
sudo blkid /dev/REPLACE_WITH_VERIFIED_EMPTY_OPENSEARCH_DISK
sudo blkid /dev/REPLACE_WITH_VERIFIED_EMPTY_PCAP_DISK
```

**Command overview:** `mkfs.xfs` creates the filesystems, `mkdir` creates mount points and `blkid` reports their UUIDs. Record the two different UUIDs privately. Do not continue if either disk was not the intended empty disk.

### Step 6 — Mount by UUID

Create a private backup before editing, then edit the file:

```bash
sudo install -o root -g root -m 0600 /etc/fstab \
  "/root/fstab.before-arkime-$(date +%Y%m%d%H%M%S)"
sudoedit /etc/fstab
```

Add these two lines with the **actual**, different UUID values reported by `blkid`:

```text
UUID=REPLACE_WITH_OPENSEARCH_UUID /srv/arkime-opensearch xfs defaults 0 0
UUID=REPLACE_WITH_PCAP_UUID /srv/arkime-pcap xfs defaults 0 0
```

Save, compare the complete edited file with the backup, and review all merged entries before validating and mounting only the new entries:

```bash
sudo findmnt --verify
sudo mount /srv/arkime-opensearch
sudo mount /srv/arkime-pcap
findmnt -no SOURCE,UUID,FSTYPE,TARGET /srv/arkime-opensearch
findmnt -no SOURCE,UUID,FSTYPE,TARGET /srv/arkime-pcap
```

**Expected:** Both are mounted XFS filesystems with different sources and UUIDs. Stop on a verification error or if either resolves to the OS disk or the same filesystem. A missing mount must not silently fill the OS disk; systemd checks are added later.

### Step 7 — Install basic tools and check capacity

```bash
sudo dnf install -y curl gnupg2 openssl git python3 python3-pip ca-certificates policycoreutils coreutils procps-ng iproute
rpm -q curl openssl python3
df -hT / /srv/arkime-opensearch /srv/arkime-pcap
```

**Command overview:** `dnf` installs prerequisites, `rpm -q` reports installed package versions, and `df` displays space on each filesystem. Use approved RHEL repositories and retain sufficient free capacity. If a package is unavailable, fix the subscription/repository configuration rather than downloading an untrusted replacement.

### Step 8 — Prepare a private download directory

```bash
umask 077
mkdir -p "$HOME/arkime-lab/downloads"
cd "$HOME/arkime-lab/downloads"
```

**Command overview:** `umask 077` restricts new files, and `mkdir` creates a download directory outside the Git repository. Reuse this same terminal for the package steps.

## Phase 2 — Download, verify and install OpenSearch

### Step 9 — Download the pinned OpenSearch package

Package examples reviewed on **November 7, 2026 (Hawaii)** use **OpenSearch 3.9.0** and **Arkime 6.9.1**. The Arkime compatibility matrix lists OpenSearch 3.x for Arkime 6. Before installation, review the vendor security advisories, compatibility matrix and current approved versions. Change package URLs and verification values together when you deliberately update versions.

```bash
curl -fSLO https://artifacts.opensearch.org/releases/bundle/opensearch/3.9.0/opensearch-3.9.0-linux-x64.rpm
curl -fSLO https://artifacts.opensearch.org/releases/bundle/opensearch/3.9.0/opensearch-3.9.0-linux-x64.rpm.sig
curl -fSLO https://artifacts.opensearch.org/publickeys/opensearch-release.pgp
```

**Command overview:** `curl -fSLO` downloads the RPM, its detached signature and the vendor's public signing key. A network or HTTP error is a stop condition. The official [OpenSearch artifacts list](https://opensearch.org/artifacts/by-version/) provides the package and signature links.

### Step 10 — Verify the OpenSearch signature

```bash
gpg --show-keys --with-fingerprint opensearch-release.pgp
```

Compare the displayed full fingerprint with a trusted, independently verified OpenSearch signing-key fingerprint through your organization's approved process. A key downloaded beside a package is not an independent identity check. Only after the fingerprint matches:

```bash
gpg --import opensearch-release.pgp
gpg --verify opensearch-3.9.0-linux-x64.rpm.sig opensearch-3.9.0-linux-x64.rpm
```

**Expected:** a good signature from the verified signing key. GPG can say the key is not certified by your personal web of trust; the independent fingerprint comparison is still necessary. Stop on a bad signature, wrong key, missing signature or unknown fingerprint.

### Step 11 — Install OpenSearch with a new demo administrator password

Choose a long unique password meeting OpenSearch's current complexity rules. To keep it out of shell history and command arguments, this command asks for it silently inside a privileged shell. Use a private screen. For the later Arkime INI example, avoid whitespace, colons and INI comment delimiters in this particular lab password.

```bash
sudo bash -c 'read -r -s -p "New OpenSearch demo admin password: " OPENSEARCH_INITIAL_ADMIN_PASSWORD; echo; export OPENSEARCH_INITIAL_ADMIN_PASSWORD; dnf install -y ./opensearch-3.9.0-linux-x64.rpm; result=$?; unset OPENSEARCH_INITIAL_ADMIN_PASSWORD; exit "$result"'
```

**Command overview:** `read -s` hides entry, `export` supplies the password to the RPM installer, and `unset` removes it from that shell afterwards. Privileged processes may inspect a running process environment. Store the password in an approved password manager, not the repository. If the installer reports a weak password or fails, stop and inspect its messages before retrying; a partially installed RPM may need repair.

```bash
rpm -q opensearch
systemctl is-active opensearch
```

**Expected:** the package is installed; the service should be inactive until configured below. `is-active` returns a nonzero status for an inactive service. If it is already active, stop and check whether this is an existing installation; do not overwrite an existing cluster.

### Step 12 — Set a loopback-only database name

Open the hosts file:

```bash
sudoedit /etc/hosts
```

Add a separate line if no conflicting entry exists:

```text
127.0.0.1 arkime-db.lab.test
```

```bash
getent ahostsv4 arkime-db.lab.test
```

**Expected:** `127.0.0.1`. This name is only for the local sensor. The exact DNS name matters: Arkime 6's capture and database utilities can automatically skip certificate verification for URLs literally using `localhost` or `127.0.0.1`. We use a loopback-resolving name that matches the certificate instead. Do not change it to an external IP or use `--insecure`.

### Step 13 — Create a private lab HTTP certificate

This creates a lab CA and an HTTP server certificate for `arkime-db.lab.test`. The CA private key stays in `/root/arkime-lab-ca` and is never copied to the repository or the Arkime process. This replaces **only OpenSearch HTTP TLS**, not the installer's demo transport credentials or users.

```bash
sudo install -d -o root -g root -m 0700 /root/arkime-lab-ca
sudo openssl req -x509 -newkey rsa:3072 -sha256 -days 365 -nodes \
  -keyout /root/arkime-lab-ca/ca-key.pem -out /root/arkime-lab-ca/ca.pem \
  -subj '/CN=Arkime Lab HTTP CA'
sudo openssl req -new -newkey rsa:3072 -nodes \
  -keyout /root/arkime-lab-ca/http-key.pem -out /root/arkime-lab-ca/http.csr \
  -subj '/CN=arkime-db.lab.test'
```

Create the certificate extension file:

```bash
sudoedit /root/arkime-lab-ca/http.ext
```

Insert:

```text
basicConstraints=CA:FALSE
keyUsage=digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:arkime-db.lab.test
```

Sign and install only the leaf key, leaf certificate and public CA where OpenSearch can read them:

```bash
sudo openssl x509 -req -sha256 -days 365 -in /root/arkime-lab-ca/http.csr \
  -CA /root/arkime-lab-ca/ca.pem -CAkey /root/arkime-lab-ca/ca-key.pem \
  -CAcreateserial -out /root/arkime-lab-ca/http.pem -extfile /root/arkime-lab-ca/http.ext
sudo install -o root -g opensearch -m 0640 /root/arkime-lab-ca/http-key.pem /etc/opensearch/arkime-http-key.pem
sudo install -o root -g opensearch -m 0640 /root/arkime-lab-ca/http.pem /etc/opensearch/arkime-http.pem
sudo install -o root -g opensearch -m 0644 /root/arkime-lab-ca/ca.pem /etc/opensearch/arkime-http-ca.pem
```

**Command overview:** `openssl` generates a CA and a signed certificate; `install` sets ownership and permissions. The private HTTP key must be readable by the `opensearch` service but not world-readable. Plan certificate expiry and replacement; deleting the CA key prevents future certificates from being signed by that CA.

### Step 14 — Trust only the public lab CA on this sensor

```bash
sudo install -o root -g root -m 0644 /etc/opensearch/arkime-http-ca.pem \
  /etc/pki/ca-trust/source/anchors/arkime-lab-http-ca.pem
sudo update-ca-trust
```

**Command overview:** This adds the public CA to the sensor's system trust store for local tools, including the Arkime database utility. It affects TLS trust for other software on **this VM**, so use it only on the dedicated lab sensor. Never place the CA private key in the trust directory. The rollback section removes the trust anchor.

### Step 15 — Configure the single-node OpenSearch service

Back up the installer-created file privately and edit it:

```bash
sudo cp -p /etc/opensearch/opensearch.yml /etc/opensearch/opensearch.yml.before-arkime-lab
sudoedit /etc/opensearch/opensearch.yml
```

Find and **replace** existing settings with the lines below; add only keys that do not already exist. Do not leave duplicate YAML keys. Retain the demo security settings and transport entries, and do not set `plugins.security.disabled` to true.

```yaml
cluster.name: arkime-lab
node.name: arkime-lab-node
network.host: 127.0.0.1
http.port: 9200
discovery.type: single-node
path.data: /srv/arkime-opensearch
plugins.security.ssl.http.enabled: true
plugins.security.ssl.http.pemcert_filepath: arkime-http.pem
plugins.security.ssl.http.pemkey_filepath: arkime-http-key.pem
plugins.security.ssl.http.pemtrustedcas_filepath: arkime-http-ca.pem
```

**Overview:** REST and node traffic stay on the sensor's loopback interface; HTTPS presents the private lab certificate. `path.data` uses the dedicated database filesystem. A one-node cluster offers no redundancy. The demo internal users and transport certificates remain a lab-only limitation.

### Step 16 — Give OpenSearch access to its filesystem

```bash
if mountpoint -q /srv/arkime-opensearch; then
  sudo chown opensearch:opensearch /srv/arkime-opensearch
  sudo chmod 0750 /srv/arkime-opensearch
  echo 'Database filesystem mounted and permissions set'
else
  echo 'STOP: Database filesystem is not mounted' >&2
fi
```

**Command overview:** The first command checks that the database disk is actually mounted; proceed only when it prints the expected line. `chown` and `chmod` grant the service access to that filesystem. Never run the ownership commands when the mount is absent.

### Step 17 — Configure memory mapping and heap

```bash
cat /proc/sys/vm/max_map_count
```

OpenSearch recommends at least `262144`. If the current value is smaller, create a sensor-specific file and apply only that file:

```bash
printf '%s\n' 'vm.max_map_count=262144' | sudo tee /etc/sysctl.d/99-arkime-opensearch.conf
sudo sysctl -p /etc/sysctl.d/99-arkime-opensearch.conf
```

For an 8 GB sensor running both applications, start with a 2 GB heap and adjust after measuring. Edit `/etc/opensearch/jvm.options`, setting the existing `-Xms` and `-Xmx` lines to the same value, such as `-Xms2g` and `-Xmx2g`; do not add duplicate heap flags. Leave memory for RHEL, Arkime and file cache. Back up the file before changing it.

### Step 18 — Prevent database startup on a missing mount

```bash
sudo systemctl edit opensearch
```

Insert and save this override:

```ini
[Unit]
RequiresMountsFor=/srv/arkime-opensearch

[Service]
ExecStartPre=/usr/bin/mountpoint -q /srv/arkime-opensearch
```

**Overview:** systemd orders the required mount and refuses to start if the directory is not a mount point. If your system does not have `/usr/bin/mountpoint`, check `command -v mountpoint` and use its verified absolute path.

### Step 19 — Start and verify the database

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now opensearch
systemctl status opensearch --no-pager
ss -lnt | grep -E ':(9200|9300)\b'
```

**Expected:** the service is active and its listening addresses are loopback. If it fails, inspect `sudo journalctl -u opensearch -n 80 --no-pager`, the private OpenSearch logs and filesystem permissions; do not disable SELinux or the security plugin to bypass an error.

```bash
curl --noproxy '*' --fail --show-error --user admin \
  https://arkime-db.lab.test:9200/
curl --noproxy '*' --fail --show-error --user admin \
  'https://arkime-db.lab.test:9200/_cluster/health?pretty'
```

Enter the OpenSearch administrator password when prompted. **Expected:** JSON reporting the local cluster and its health; no certificate warning or `-k` is needed. A one-node cluster may be yellow because replica shards cannot be assigned. Investigate red health or an authentication, DNS or certificate error before proceeding. An HTTP `401` is not a successful authentication.

Check that this is a dedicated empty lab instance before initialization:

```bash
curl --noproxy '*' --fail --show-error --user admin \
  'https://arkime-db.lab.test:9200/_cat/indices?v'
```

Do not proceed if it contains existing application or Arkime data that must be preserved. OpenSearch security system indexes may be present. The next database initialization creates Arkime indexes and **deletes previous Arkime data** on the target.

## Phase 3 — Install and configure Arkime

### Step 20 — Download and check the Arkime EL10 RPM

```bash
cd "$HOME/arkime-lab/downloads"
curl -fSLO https://github.com/arkime/arkime/releases/download/v6.9.1/arkime-6.9.1-1.el10.x86_64.rpm
sha256sum arkime-6.9.1-1.el10.x86_64.rpm
```

The expected SHA-256 from the [v6.9.1 release asset](https://github.com/arkime/arkime/releases/tag/v6.9.1) is:

```text
b960db9a975ff1e6538ec895868c1367f737384234ea961140b993697bd03f62
```

**Command overview:** `sha256sum` calculates the file's fingerprint. Compare every character with the vendor release before installing. A matching hash confirms the downloaded bytes match the cited release value; checking a digest from the same channel alone does not independently prove publisher identity. Stop on a mismatch. Obtain the matching EL10 aarch64 package and its own vendor digest for ARM; do not use this x86-64 hash for it.

### Step 21 — Install Arkime and create its service account

```bash
sudo dnf install -y ./arkime-6.9.1-1.el10.x86_64.rpm
rpm -q arkime
/opt/arkime/bin/capture --version
```

**Expected:** the installed version and capture version are shown. Resolve library or repository errors using the matching vendor build; do not force-install the wrong RPM. The package supplies `arkimecapture` and `arkimeviewer` systemd units. It does not need a second Elasticsearch installation.

```bash
getent group arkime || sudo groupadd --system arkime
getent passwd arkime || sudo useradd --system --no-create-home --gid arkime --shell /sbin/nologin arkime
id arkime
sudo install -d -o arkime -g arkime -m 0750 /opt/arkime/logs
if mountpoint -q /srv/arkime-pcap; then
  sudo install -d -o arkime -g arkime -m 0750 /srv/arkime-pcap/output /srv/arkime-pcap/import
  echo 'Packet filesystem mounted and directories created'
else
  echo 'STOP: Packet filesystem is not mounted' >&2
fi
```

**Overview:** The restricted `arkime` account owns lab packet and log directories. Run `mountpoint` first and **stop** unless it prints the expected message; do not create directories on the underlying OS filesystem. If the account or group already exists, review its identity, group membership and permissions rather than assuming it is dedicated to this service.

### Step 22 — Create a private Arkime configuration

This procedure edits the vendor sample directly; it does not run the interactive `Configure` script, which can echo the database password and offer to install a separate demo database. Only create the file if it does not already exist. If it exists, back it up privately and review it instead of overwriting it.

```bash
if sudo test -e /opt/arkime/etc/config.ini; then
  echo 'STOP: Existing Arkime configuration; back it up and review it.'
else
  sudo install -o root -g arkime -m 0640 /opt/arkime/etc/config.ini.sample /opt/arkime/etc/config.ini
fi
```

Proceed only if the file did not already exist and the `install` command succeeded. The following command edits that new file; it is not for an existing installation:

```bash
sudo sed -i \
  -e 's|ARKIME_INSTALL_DIR|/opt/arkime|g' \
  -e 's|ARKIME_ELASTICSEARCH|https://arkime-db.lab.test:9200|g' \
  -e 's|ARKIME_INTERFACE|lo|g' /opt/arkime/etc/config.ini
sudoedit /opt/arkime/etc/config.ini
```

Place a public CA copy in Arkime's readable directory before starting the Viewer. The OpenSearch configuration directory itself may not be traversable by the `arkime` account:

```bash
sudo install -o root -g root -m 0644 /etc/pki/ca-trust/source/anchors/arkime-lab-http-ca.pem \
  /opt/arkime/etc/arkime-lab-http-ca.pem
sudo -u arkime test -r /opt/arkime/etc/arkime-lab-http-ca.pem && echo 'Public CA readable'
```

In the `[default]` section, find and replace the existing keys; uncomment applicable entries and do not leave duplicates. Supply your real values **only in the private file**:

```ini
elasticsearch=https://arkime-db.lab.test:9200
elasticsearchBasicAuth=admin:REPLACE_PRIVATELY_WITH_YOUR_OPENSEARCH_PASSWORD
caTrustFile=/opt/arkime/etc/arkime-lab-http-ca.pem
passwordSecret=REPLACE_PRIVATELY_WITH_A_LONG_RANDOM_INDEPENDENT_SECRET
interface=lo
pcapDir=/srv/arkime-pcap/output
maxFileSizeG=1
freeSpaceG=20%
dropUser=arkime
dropGroup=arkime
viewHost=127.0.0.1
viewPort=8005
authMode=digest
```

In the `[default]` section, comment out any active `rirFile` and `ouiFile` entries inherited from the vendor sample. The synthetic exercise does not provision those lookup files; leaving either setting active can prevent capture imports from starting.

Use a unique, random `passwordSecret`, independent of the database password, and keep it stable: changing it can invalidate existing Arkime user passwords. The sample `elasticsearchBasicAuth` stores a plaintext service credential, so protect the file and never paste it into GitHub, chat or screenshots. The lab uses the demo database administrator for simplicity; use a reviewed, least-privilege service identity in any operational design. `interface=lo` is a placeholder for offline setup: **do not start the capture service yet**. The example rotates packet files at 1 GB and starts expiring packet files when free space is below 20%; it is not a guaranteed retention period. The Viewer must be running for packet-file expiration. Packet and session retention are different.

```bash
sudo chown root:arkime /opt/arkime/etc/config.ini
sudo chmod 0640 /opt/arkime/etc/config.ini
sudo stat -c '%U %G %a %n' /opt/arkime/etc/config.ini
```

**Expected:** `root arkime 640`. Do not print the configuration file, because it contains credentials. Optional GeoIP data needs its own approved source and account; its absence does not establish a failure to capture sessions.

### Step 23 — Initialize the dedicated Arkime database exactly once

**Destructive warning:** Arkime `init` removes prior Arkime indexes on the target. Run it only on the new, dedicated and checked `arkime-lab` cluster. Do not run it on an existing production or shared cluster, and never rerun it to troubleshoot a populated lab. For an existing Arkime database use the vendor's documented upgrade and backup procedure instead.

```bash
sudo env no_proxy=arkime-db.lab.test,localhost,127.0.0.1 \
  NO_PROXY=arkime-db.lab.test,localhost,127.0.0.1 \
  /opt/arkime/db/db.pl --esuser admin https://arkime-db.lab.test:9200 init --ism
```

Enter the OpenSearch administrator password when prompted and respond to the tool's confirmation only after reviewing its target. Then set the example force-merge age to one day and session-index deletion age to seven days. This does not set index rollover or guarantee that all Arkime metadata is retained for seven days:

```bash
sudo env no_proxy=arkime-db.lab.test,localhost,127.0.0.1 \
  NO_PROXY=arkime-db.lab.test,localhost,127.0.0.1 \
  /opt/arkime/db/db.pl --esuser admin https://arkime-db.lab.test:9200 ism 1d 7d
```

**Command overview:** `db.pl init --ism` creates Arkime's database structures using OpenSearch Index State Management. In `ism 1d 7d`, the first age is when an index transitions to force merge, and the second is the session-index deletion age. Arkime's `rotateIndex` setting controls index rotation; history indexes have a separate policy. Confirm the resulting ISM policy, rotation setting and index state in OpenSearch; a policy is not proof that timed deletion has occurred. Change these examples only with an approved retention plan. The CA was installed in Step 14 so `db.pl` can verify the named endpoint without bypass flags.

### Step 24 — Create a local Arkime administrator

```bash
sudo env no_proxy=arkime-db.lab.test,localhost,127.0.0.1 \
  NO_PROXY=arkime-db.lab.test,localhost,127.0.0.1 \
  /opt/arkime/bin/arkime_add_user.sh arkimeadmin 'Lab Administrator' - --admin
```

**Command overview:** `-` requests the new Arkime user's password interactively instead of putting it in the command line, and `--admin` grants administrative privileges. Use a different strong password from the database and keep it private. This is an Arkime account, not a Linux or Splunk account. Create a separate lower-privilege analyst account through the Viewer for routine use.

### Step 25 — Restrict and start the Viewer

```bash
sudo systemctl edit arkimeviewer
```

Add:

```ini
[Unit]
RequiresMountsFor=/srv/arkime-pcap
After=opensearch.service

[Service]
User=arkime
Group=arkime
ExecStartPre=/usr/bin/mountpoint -q /srv/arkime-pcap
```

Now start only the Viewer:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now arkimeviewer
systemctl status arkimeviewer --no-pager
ss -lnt | grep ':8005'
systemctl is-active arkimecapture
```

**Expected:** Viewer is active and listens on `127.0.0.1:8005`; capture is inactive. An inactive `is-active` result is expected and returns nonzero. The packaged Viewer service writes to `/opt/arkime/logs/viewer.log`; check that file privately if startup fails. If SELinux denies access, examine the denial and apply an approved labeling/policy fix rather than turning SELinux off.

### Step 26 — Open the Viewer through an SSH tunnel

From **Windows PowerShell**, substitute the sensor's actual authorized administrator and address:

```powershell
ssh.exe -N -L 127.0.0.1:8005:127.0.0.1:8005 YOUR_SENSOR_ADMIN@172.25.250.40
```

Verify the SSH host fingerprint through a trusted channel on first use, authenticate and leave this window open. On the same Windows PC, browse to `http://127.0.0.1:8005` and sign in with `arkimeadmin` and its Arkime password.

**Command overview:** `ssh -L` forwards a local Windows port to the sensor's loopback Viewer through an encrypted SSH connection. Viewer HTTP digest authentication is used inside this local tunnel. Do not expose port 8005 or OpenSearch 9200 on the network. For shared or remote operational access, use approved HTTPS, individual accounts and a hardened authentication architecture. If Windows port 8005 is already taken, use `127.0.0.1:18005:127.0.0.1:8005` and browse to port `18005`.

## Phase 4 — Generate and import safe test traffic

### Step 27 — Obtain the project on the sensor

If you already have a trusted checkout on the sensor, `cd` to it and confirm the expected branch. Otherwise, as the normal sensor administrator:

```bash
cd "$HOME"
git clone https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting.git
cd "$HOME/rhel-10v2-splunk-threat-hunting"
git status --short
```

**Overview:** `git clone` obtains the published guide and synthetic generator. Do not run `git clone` into an existing checkout or overwrite local work. Never put generated packet files or private configurations in the repository.

### Step 28 — Create synthetic packet files

Run these commands in the repository root in the **same Bash session**:

```bash
umask 077
ARKIME_LAB_REPO="$PWD"
mkdir -p "$HOME/arkime-lab/runs"
ARKIME_LAB_RUN=$(mktemp -d "$HOME/arkime-lab/runs/fixture-XXXXXXXX")
python3 -m venv "$ARKIME_LAB_RUN/venv"
"$ARKIME_LAB_RUN/venv/bin/python" -m pip install 'dpkt==1.9.8'
"$ARKIME_LAB_RUN/venv/bin/python" \
  "$ARKIME_LAB_REPO/scripts/network-defense/generate_http_fixtures.py" \
  "$ARKIME_LAB_RUN/captures"
sha256sum "$ARKIME_LAB_RUN/captures/"*.pcap
```

**Command overview:** `venv` isolates the generator dependency, and the Python script **writes files without transmitting packets**. It creates a routine baseline and a candidate investigation file with recent timestamps and documentation IP addresses. Use an approved Python package source. The generator creates `captures` itself; the parent must exist. Record the actual file hashes and run time privately.

### Step 29 — Prepare import files

```bash
ARKIME_IMPORT_DIR="/srv/arkime-pcap/import/${ARKIME_LAB_RUN##*/}"
if mountpoint -q /srv/arkime-pcap && ! sudo test -e "$ARKIME_IMPORT_DIR"; then
  sudo install -d -o arkime -g arkime -m 0750 "$ARKIME_IMPORT_DIR"
  sudo install -o arkime -g arkime -m 0640 \
    "$ARKIME_LAB_RUN/captures/baseline.pcap" "$ARKIME_IMPORT_DIR/baseline.pcap"
  sudo install -o arkime -g arkime -m 0640 \
    "$ARKIME_LAB_RUN/captures/investigation.pcap" "$ARKIME_IMPORT_DIR/investigation.pcap"
else
  echo 'STOP: Packet disk is not mounted or import directory already exists' >&2
fi
sudo -u arkime test -r "$ARKIME_IMPORT_DIR/baseline.pcap" && echo 'Baseline readable'
sudo -u arkime test -r "$ARKIME_IMPORT_DIR/investigation.pcap" && echo 'Investigation readable'
```

**Expected:** both `readable` messages. The directory name includes the unique run ID so a new run does not overwrite an earlier import. Stop if a check fails; record which files belong to each run.

### Step 30 — Import both files without live capture

```bash
sudo env no_proxy=arkime-db.lab.test,localhost,127.0.0.1 \
  NO_PROXY=arkime-db.lab.test,localhost,127.0.0.1 \
  /opt/arkime/bin/capture -c /opt/arkime/etc/config.ini \
  -r "$ARKIME_IMPORT_DIR/baseline.pcap" --copy
sudo env no_proxy=arkime-db.lab.test,localhost,127.0.0.1 \
  NO_PROXY=arkime-db.lab.test,localhost,127.0.0.1 \
  /opt/arkime/bin/capture -c /opt/arkime/etc/config.ini \
  -r "$ARKIME_IMPORT_DIR/investigation.pcap" --copy
```

**Command overview:** `capture -r` reads each saved file; `--copy` writes Arkime-managed packet files under the configured packet directory. It does not start the live service. Allow the command to finish and check for errors. Re-importing a fixture can duplicate sessions; use a new run ID/time window and document repeats. Packet files and session metadata have separate lifecycles.

### Step 31 — Find the sessions in Arkime

In the Viewer, open **Sessions**, set the time picker to include the fixture timestamps, and search:

```text
ip.src == 192.0.2.20 && ip.dst == 192.0.2.10
```

If necessary, try the address filter in either direction using the Viewer's field autocomplete. A fixture has three baseline HTTP sessions and two investigation HTTP sessions, plus DNS sessions to `192.0.2.30`. Exact Viewer totals depend on the time window and any repeated imports. Open the candidate session, verify the destination port and HTTP host/path, and inspect the reconstructed data. See the [worked investigation](INVESTIGATION.md) for the evidence and expected result. A successful import is not live visibility.

### Step 31.1 — Optionally test a periodic detection

This optional test tags the known synthetic candidate; it does not send a message or create a Splunk alert. In `/opt/arkime/etc/config.ini`, uncomment or set `cronQueries=true` once in the `[default]` section, save privately, and restart the Viewer:

```bash
sudo systemctl restart arkimeviewer
systemctl status arkimeviewer --no-pager
```

In a multi-Viewer design, enable periodic-query processing on only one designated node. For this one-Viewer lab, reconnect through the SSH tunnel and:

1. Open **Settings → Periodic Queries → New Periodic Query**.
2. Set a short query name such as `lab-http-review`, the expression `http.host == review.example.test`, action **Tag**, and a tag such as `lab_http_review`.
3. Select a start time covering your synthetic run, such as **1 hour ago** if the fixture is within that period. Do not use **all** on a populated database.
4. Leave notifiers unselected and create/enable the query. Review its last run, match count and errors. Arkime processes completed sessions with a delay; wait for a scheduled run and refresh the page.
5. Open the matching session and verify the tag. Record the result and then disable or delete the periodic query when the test ends. Its tag can remain on previously matched sessions unless removed separately.

The configured rule identifies the known exercise host; it is not a general anomaly detector. Arkime can use an approved notifier for matching sessions, but notification delivery, recipients, secrets and frequency need a separately approved configuration and a successful end-to-end test. A match counter alone is not evidence that an alert was delivered. See the [Arkime periodic-query API reference](https://arkime.com/apiv3#cron-api) and the Viewer's built-in Help.

### Step 31.2 — Optionally verify live capture using generated local traffic

Follow the [controlled local live test](CONTROLLED_LIVE_TEST.md) to capture three harmless HTTP requests on the sensor's loopback interface. The test uses a narrow BPF filter, a two-minute timeout and a separate tag, then checks the resulting sessions and reconstructed packets. It requires no mirror and does not prove visibility into another VM. Stop the foreground test before starting any capture service.

Use the [anomaly analysis playbook](HUNTING_PLAYBOOK.md) to continue with representative baselines, DNS/HTTP/TLS and service-port queries, SPIGraph/Connections review, a saved-packet Hunt and reporting. The provided synthetic dataset contains HTTP and DNS only; other protocol hunts need their own approved test data.

## Phase 5 — Authorized live deployment and operations

### Step 32 — Review the live capture gate

Only after the offline exercise works, a designated owner approves scope and the demo security configuration is replaced, identify a **dedicated capture NIC** connected to an approved TAP, SPAN/mirror or a purposely generated test stream. Document direction, VLANs, clock, filters, sensitive-data handling, packet volume, retention, access, disk alarms and response channels. Confirm whether traffic is dropped or asymmetric. Virtual networking and a management NIC do not provide a universal mirror. Do not enable capture on `lo` or the management adapter by accident.

### Step 33 — Inspect the capture interface

```bash
ip -brief link
ip -s link
```

**Overview:** List interface names, state and counters. Identify the approved receive-only mirror interface by VMware adapter mapping and the network owner's documentation; do not infer its role from names like `ens192`. Arkime's packaged startup script may change interface settings. Review `/opt/arkime/bin/arkime_config_interfaces.sh` and the unit before enabling it. Measure observed traffic and capture loss with approved tooling.

### Step 34 — Configure the interface and mount protection

Edit `/opt/arkime/etc/config.ini` privately and replace only `interface=lo` with the verified capture interface, for example `interface=ens224` **only if that is actually the designated interface**. Review capture-specific settings and output storage. Add a service override:

```bash
sudo systemctl edit arkimecapture
```

```ini
[Unit]
RequiresMountsFor=/srv/arkime-pcap
After=opensearch.service

[Service]
ExecStartPre=/usr/bin/mountpoint -q /srv/arkime-pcap
```

**Overview:** The packaged capture service starts with privileges needed to set up capture, then drops to the `arkime` user configured above. Confirm the mount, ownership, SELinux and approved NIC configuration before enabling it.

### Step 35 — Start capture only after approval

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now arkimecapture
systemctl status arkimecapture --no-pager
sudo tail -n 60 /opt/arkime/logs/capture.log
```

**Expected:** active service and no recurring capture, filesystem, authentication or database errors. Check Arkime **Stats** for the correct node, received packets and drops, then use a known authorized test flow to confirm visibility. Do not publish log lines or packet contents without sanitization. If counters stay at zero, troubleshoot the mirror, interface, packet permissions and filters; a running service is not proof of traffic visibility.

### Step 36 — Review baseline and investigate

Use the [worked case](INVESTIGATION.md) for the repeatable HTTP baseline and the [17-step anomaly playbook](HUNTING_PLAYBOOK.md) for protocol queries, graphs, packet-content searching and analyst reporting. For real traffic, establish a representative baseline by segment, role, time of day and business activity; investigate new destinations, unexpected protocols, repeated connections and unusual data movement against authorized context. Record collection coverage, packet loss and what encryption prevents you from seeing. An outlier is a lead, not proof of an attack.

### Step 37 — Operate, protect and retain data

Check service status, disk capacity, packet loss, time synchronization, certificate expiry and database health. Use individual analyst accounts and review permissions. Protect both packet files and metadata; Viewer admins can access sensitive content. Confirm packet deletion thresholds **and** ISM retention separately, taking account of legal holds and approved evidence preservation. Back up configuration and database through an approved process without copying private data to GitHub. Update Arkime/OpenSearch only after checking compatibility, snapshots, change control and the vendor's upgrade steps.

### Step 38 — Record results and recover safely

Use the [sanitized evidence template](../../evidence/sanitized/arkime-validation.md) to record only reviewed results. Keep actual logs, PCAPs, IP inventories, certificates, passwords and screenshots in approved private storage. Document who validated the test, the actual versions and whether capture remains disabled.

To stop live collection without deleting data:

```bash
sudo systemctl disable --now arkimecapture
systemctl is-active arkimecapture
```

To stop the lab Viewer and database after collection has stopped:

```bash
sudo systemctl disable --now arkimeviewer
sudo systemctl disable --now opensearch
```

Remove the sensor's added CA trust only if no approved application still depends on it:

```bash
sudo rm -i /etc/pki/ca-trust/source/anchors/arkime-lab-http-ca.pem
sudo update-ca-trust
```

**Overview:** Stopping services does not erase packet or database files. Removing the trust anchor affects all sensor software that relies on that CA. Restore reviewed configuration backups and remove added systemd overrides or the sensor-specific sysctl only through an approved change; check their contents first. If a full lab teardown is authorized, preserve required evidence and securely dispose of the VM/disks under your retention policy. Do not rerun `db.pl init` as a cleanup shortcut.

## Troubleshooting

| Symptom | Checks and action |
| --- | --- |
| OpenSearch will not start | `sudo journalctl -u opensearch -n 80 --no-pager`; check both data mount and ownership, duplicate YAML keys, heap, available RAM, certificate paths and `vm.max_map_count`. Review SELinux audit denials; do not disable SELinux. |
| TLS name or CA error | `getent hosts arkime-db.lab.test`; verify the named endpoint's SAN and the public CA. Use `sudo openssl x509 -in /etc/opensearch/arkime-http.pem -noout -subject -ext subjectAltName`. Keep `caTrustFile` and system CA trust consistent; do not use `-k` or `--insecure`. |
| `401 Unauthorized` | Confirm the prompted OpenSearch password and private `elasticsearchBasicAuth`. Do not publish the config or paste passwords into commands. Arkime Viewer and OpenSearch accounts are separate. |
| Viewer fails or cannot reach database | Inspect `/opt/arkime/logs/viewer.log` privately, loopback listener, certificate trust, file permissions, systemd override, service account and proxy exclusions. Check logs for accidentally enabled insecure mode. |
| No sessions after offline import | Confirm the import command finished without errors, the fixture times and Viewer time range, copied file readability, database health, capture logs and session filter. Search a wider window first. Re-import only when the duplication is understood. |
| Sessions appear but packets cannot be opened | Verify the original managed files still exist in `pcapDir`, Viewer can read them, the correct node is reachable and the capture was copied; packet expiration can remove PCAPs while session records remain. |
| No live traffic or excessive drops | Check authorized mirror configuration, selected NIC, VLANs, receive counters, capture and Arkime statistics, capacity and any filters. NAT reachability or a green service is not proof of mirror visibility. |
| Disk usage grows | Check both `df -hT` filesystems and Viewer health; packet free-space cleanup and ISM session retention are separate. Protect evidence under hold before changing deletion settings. |
| Splunk has no Arkime events | This design does not configure Arkime-to-Splunk ingestion. Use the existing separately validated synthetic Zeek/Suricata case; do not assume matching session IDs or invent a new index. |

## References

- [Arkime installation guide](https://arkime.com/install): Vendor package, database initialization and service instructions.
- [Arkime release v6.9.1](https://github.com/arkime/arkime/releases/tag/v6.9.1): EL10 packages, release notes and asset digests.
- [Arkime FAQ](https://arkime.com/faq): Compatibility, TLS and operational troubleshooting.
- [Arkime settings](https://arkime.com/settings): Capture, authentication, storage and retention settings.
- [OpenSearch RPM installation](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/rpm/): Package installation, security and service setup.
- [OpenSearch artifacts by version](https://opensearch.org/artifacts/by-version/): Versioned RPMs and signatures.
- [OpenSearch demo security configuration](https://docs.opensearch.org/latest/security/configuration/demo-configuration/): Demo setup and its limitations.
- [OpenSearch ISM documentation](https://docs.opensearch.org/latest/im-plugin/ism/index/): Index lifecycle and policy operation.
