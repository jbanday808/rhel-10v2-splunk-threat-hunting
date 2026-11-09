# Complete Step-by-Step Zeek Installation, Configuration, and Deployment Guide

**Platform:** RHEL 10.2, VMware Workstation, and the existing Splunk threat-hunting lab.

**Status:** Optional deployment instructions and reviewable examples only. This guide does not establish that RHEL-SENSOR01 exists, that Zeek is installed, that mirrored traffic is visible, or that Splunk has received data. Record actual results in the [network-defense evidence worksheet](../../evidence/sanitized/network-defense-validation.md).

## What this guide deploys

Use the **official Zeek container with Podman**, rather than assuming that a native RHEL 10 RPM exists. First analyze an inert synthetic PCAP without network access or capture capabilities. After separate authorization, deploy a single standalone Zeek process through a rootful Podman Quadlet service on a dedicated sensor.

This is a low-volume lab starting point, not a production sizing or high-availability design. It does not configure ZeekControl, a worker cluster, an IPS, a traffic mirror, automatic file extraction, or automatic forwarding of live metadata. Do not mix the standalone service with a second ZeekControl-managed capture process.

| Phase | Steps | Outcome |
| --- | --- | --- |
| [Prepare](#phase-1-prepare-the-sensor) | 1-4 | Authorized scope, prerequisites, and private workspace |
| [Install and test offline](#phase-2-install-and-validate-zeek-offline) | 5-9 | Pinned image, reviewed policy, synthetic DNS JSON |
| [Deploy live capture](#phase-3-optional-authorized-live-deployment) | 10-17 | Proven packet visibility and a persistent sensor service |
| [Integrate Splunk](#phase-4-optional-splunk-integration) | 18-23 | Reviewed parsing, synthetic upload, optional TLS forwarding |
| [Operate and recover](#phase-5-operations-troubleshooting-and-rollback) | 24-28 | Health checks, upgrades, rollback, and acceptance evidence |

**Execution rule:** Run sensor commands in Bash as an administrative user on **RHEL-SENSOR01**, using `sudo` only where shown. WSL is an editing workstation, not a substitute for the sensor's approved capture interface. Steps explicitly marked **RHEL-SPLUNK01** or **WINHUNT01** run on those systems instead.

**Change rule:** Installation commands assume a first deployment. If a target file, app, directory policy, or NetworkManager profile already exists, stop, make a private backup, and merge the change. Never overwrite an existing configuration with an example. Read-only inventory commands require no rollback.

## Phase 1: Prepare the sensor

### Step 1: Confirm the architecture and authorization

Preserve the existing three VMs and the six core indexes.

| System | Example lab address | Responsibility |
| --- | --- | --- |
| RHEL-SPLUNK01 | `172.25.250.10` | Existing Splunk Enterprise, search, and TLS receiver |
| WINHUNT01 | `172.25.250.20` | Existing Windows events, Sysmon, and Universal Forwarder |
| RHEL-IDM01 | `172.25.250.30` | Existing IdM, DNS, and LDAPS |
| RHEL-SENSOR01, optional | `172.25.250.40` | New Zeek sensor; verify the address is unused |

The original indexes remain `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`. A later `net_zeek` index is an optional addition, not a replacement.

Before installing anything, record privately:

1. Owner approval, the authorized network and endpoints, and the change window.
2. Whether the scope is offline analysis only or includes a specific mirrored interface.
3. Approved metadata fields, access controls, disk budget, retention, and legal-hold handling.
4. The current Splunk/Windows/IdM health baseline and a tested recovery method.
5. Who can stop capture and review unexpected traffic, packet loss, or sensitive data.

Use the existing [architecture](ARCHITECTURE.md), [CONOPS](CONOPS.md), and [publication safety checklist](../reference/security-and-sanitization.md). Do not put raw captures, logs, certificate material, credentials, or deployment inventories in Git.

**Gate:** Offline processing uses only the supplied synthetic fixture. Live capture remains prohibited until Steps 10-12 pass. No GitHub workflow connects to the private lab.

### Step 2: Inventory the proposed sensor

**Run on RHEL-SENSOR01:**

~~~bash
cat /etc/redhat-release
hostnamectl
uname -m
ip -brief address
ip route
nmcli -f NAME,DEVICE,TYPE connection show --active
getenforce
sudo firewall-cmd --get-active-zones
timedatectl
df -hT
free -h
sudo sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding
sudo subscription-manager identity
sudo dnf repolist --enabled
~~~

**Command overview:** Reads OS, CPU architecture, interfaces, routes, SELinux, firewall, time, storage, forwarding state, and RHEL repository access.

**Expected:** An owner-approved RHEL 10.2 sensor with SELinux **Enforcing**, working time synchronization, adequate private storage, and no unintended routing or bridging. A planning allocation of 2-4 vCPU and 4-8 GiB RAM is not a throughput guarantee. Do not install packet-processing services on the Splunk or IdM VM to avoid creating a separate sensor.

**Stop if:** The proposed sensor address conflicts, the management path is uncertain, RHEL repositories are unavailable, or forwarding is enabled without an approved design. Resolve these through the existing lab procedures; do not disable SELinux or reconfigure the other VMs.

### Step 3: Install RHEL prerequisites

Review the packages available from the enabled, entitled RHEL repositories:

~~~bash
sudo dnf info podman tcpdump wireshark-cli python3 jq git ethtool openssl
~~~

After approval:

~~~bash
sudo dnf install -y podman tcpdump wireshark-cli python3 jq git ethtool openssl
rpm -q podman tcpdump wireshark-cli python3 jq git ethtool openssl
podman --version
podman info --format '{{.Host.CgroupsVersion}}'
tshark --version
~~~

**Command overview:** Installs the container runtime, packet readers, JSON tooling, and source-control tools, then records installed versions. `wireshark-cli` supplies TShark. Quadlet requires cgroup v2; expect `v2`.

**Check:** Resolve package or rootless Podman errors before continuing. For rootless user-namespace issues, have the RHEL administrator review the account's subordinate UID/GID allocation; do not replace the offline test with `sudo` or `--privileged` as a workaround.

**Undo:** Record newly installed packages. Remove only packages introduced by this change after checking dependencies; do not remove a runtime used by other services. No Docker daemon or third-party RPM repository is required.

### Step 4: Obtain the repository and create private working directories

If this user does not already have a checkout:

~~~bash
mkdir -p "$HOME/projects"
git clone https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting.git \
  "$HOME/projects/rhel-10v2-splunk-threat-hunting"
~~~

For an existing checkout, inspect `git status` and update with `git pull --ff-only` only from a clean, appropriate branch. Do not reset or discard local work.

Set these variables in the same sensor Bash session used for the following steps:

~~~bash
umask 077
LAB_REPO="$HOME/projects/rhel-10v2-splunk-threat-hunting"
ZEEK_WORK="$HOME/network-lab/zeek"
PCAP_DIR="$HOME/network-lab/private-pcaps"
install -d -m 0700 "$ZEEK_WORK" "$PCAP_DIR" \
  "$ZEEK_WORK/policy" "$ZEEK_WORK/runs" "$ZEEK_WORK/inventory" \
  "$ZEEK_WORK/approved"
cd "$LAB_REPO"
git status --short
git rev-parse HEAD
~~~

**Command overview:** Separates public source from private PCAPs, policies, output, and deployment records. Record the repository revision privately.

**Check:** None of the private directories is inside the Git checkout or a Splunk-monitored directory. If you open a new sensor terminal, restore `LAB_REPO`, `ZEEK_WORK`, and `PCAP_DIR` before running later commands.

**Undo:** Keep generated data private until retention review. Deleting a checkout is not a sensor rollback and must not remove evidence.

## Phase 2: Install and validate Zeek offline

### Step 5: Select an official release and pin its digest

The reference release for this guide is **Zeek 9.0.1**, published October 26, 2026. Re-check the [official releases](https://github.com/zeek/zeek/releases) and [OS support guidance](https://github.com/zeek/zeek/wiki/Zeek-Operating-System-Support-Matrix) at installation time. Choose a maintained release approved for your environment; a release tag is not an immutable deployment reference.

~~~bash
ZEEK_TAG=9.0.1
podman pull "docker.io/zeek/zeek:$ZEEK_TAG"
podman image inspect "docker.io/zeek/zeek:$ZEEK_TAG" \
  --format '{{range .RepoDigests}}{{println .}}{{end}}'
~~~

Copy the approved complete `docker.io/zeek/zeek@sha256:...` reference from that output:

~~~bash
read -r -p 'Approved full Zeek image digest reference: ' ZEEK_IMAGE
if [[ ! "$ZEEK_IMAGE" =~ ^docker\.io/zeek/zeek@sha256:[0-9a-f]{64}$ ]]; then
  printf 'Invalid Zeek digest reference; stop and review the image.\n' >&2
  exit 1
fi
podman image exists "$ZEEK_IMAGE" &&
  podman image inspect "$ZEEK_IMAGE" > "$ZEEK_WORK/inventory/image-inspect.json" &&
  printf '%s\n' "$ZEEK_IMAGE" > "$ZEEK_WORK/inventory/image-reference.txt"
~~~

**Command overview:** Downloads the official versioned image, displays its registry digest, checks the selected reference is local, and records the exact artifact. Review image architecture and release metadata in the inventory.

**Check:** The digest must correspond to the reviewed release and sensor architecture. A digest pins content; it is not, by itself, proof of publisher identity or a signature-verification result. Keep registry TLS verification enabled. Do not use `latest`, `lts`, a development image, or automatic image updates for the deployed service.

**Undo/negative check:** An invalid digest must fail validation or image lookup. Do not substitute an arbitrary local image after a failed pull. Retain the approved old digest when upgrading.

### Step 6: Install the site policy and check the image

The repository supplies an optional [site policy](../../configs/network-defense/zeek/local.zeek.example):

~~~bash
install -m 0600 \
  "$LAB_REPO/configs/network-defense/zeek/local.zeek.example" \
  "$ZEEK_WORK/policy/local.zeek"

podman run --rm --pull=never --network=none --cap-drop=ALL \
  --security-opt=no-new-privileges --read-only \
  "$ZEEK_IMAGE" zeek --version

podman run --rm --pull=never --network=none --cap-drop=ALL \
  --userns=keep-id --user "$(id -u):$(id -g)" \
  --security-opt=no-new-privileges --read-only \
  --tmpfs /tmp:rw,nosuid,nodev,size=64m \
  -v "$ZEEK_WORK/policy:/policy:ro,Z" -w /tmp \
  "$ZEEK_IMAGE" zeek --parse-only /policy/local.zeek
~~~

**Command overview:** Copies the reviewed example, prints the actual Zeek version, and parses the policy without starting packet capture. The official reference image installs Zeek under `/usr/local/zeek`, not the `/opt/zeek` path used by some native packages.

Review these policy choices before use:

| Setting | Meaning |
| --- | --- |
| `@load tuning/json-logs` | One JSON object per log line rather than tab-separated output |
| `JSON::TS_EPOCH` | Numeric epoch-seconds `ts`, suitable for verified Splunk event-time parsing |
| `Log::default_rotation_interval = 1hr` | Rotate logs hourly; does **not** delete old logs |
| `Site::local_nets` | Classify the lab subnet as local; does **not** filter captured packets |
| `misc/stats`, `misc/capture-loss` | Produce health observations when enough time/traffic exists |

This policy does not load the image's sample `local.zeek`, third-party packages, email notification policies, or file-extraction policies. Do not enable plugins, external enrichment, or payload extraction without separate review.

**Check:** Both containers exit successfully and leave no running service. `:Z` relabels only the dedicated bind-mounted directory for a private container; never apply it to `/home`, `/etc`, or `/var/log` as a whole. Do not run overlapping containers against the same `:Z` directory.

**Undo/negative check:** A syntax error must stop deployment. Restore the last reviewed private policy and repeat `--parse-only`; do not suppress the error.

### Step 7: Generate the harmless DNS fixture

~~~bash
python3 "$LAB_REPO/scripts/network-defense/generate_synthetic_pcap.py" \
  --timestamp "$(date -u +%s)" \
  --output "$PCAP_DIR/zeek-dns-fixture.pcap"
sha256sum "$PCAP_DIR/zeek-dns-fixture.pcap"
tshark -n -r "$PCAP_DIR/zeek-dns-fixture.pcap" \
  -Y dns -T fields -e ip.src -e ip.dst -e dns.qry.name
~~~

**Command overview:** Writes one synthetic DNS request using documentation addresses and `lab-marker.example.test`; it does not transmit a packet. Using the current timestamp avoids accidentally testing old data against a short Splunk search or retention window.

**Expected:** One DNS question with the fixture marker. Record the PCAP hash and timestamp privately. Preserve a fixed copy for reproducibility; do not overwrite a capture already used as evidence.

### Step 8: Run Zeek without network access

~~~bash
RUN_DIR=$(mktemp -d "$ZEEK_WORK/runs/dns-XXXXXXXX")
podman run --rm --pull=never --network=none --cap-drop=ALL \
  --userns=keep-id --user "$(id -u):$(id -g)" \
  --security-opt=no-new-privileges --read-only --umask=0077 \
  --tmpfs /tmp:rw,nosuid,nodev,size=64m \
  -v "$PCAP_DIR:/pcaps:ro,Z" \
  -v "$ZEEK_WORK/policy:/policy:ro,Z" \
  -v "$RUN_DIR:/out:Z" -w /out \
  "$ZEEK_IMAGE" zeek -r /pcaps/zeek-dns-fixture.pcap /policy/local.zeek
printf 'Private output: %s\n' "$RUN_DIR"
~~~

**Command overview:** Reads the PCAP through a read-only mount and writes results to a fresh user-owned run directory. `--network=none` and `--cap-drop=ALL` prevent this offline invocation from accessing a live host interface. `--userns=keep-id` avoids root-owned output and unsafe permission workarounds.

**Check:** The command exits zero. Do not reuse the output directory: a new Zeek process can replace active log filenames. No `-C` checksum bypass is needed for the supplied fixture.

**Undo:** No host capture service or network setting changed. Keep or dispose of this private synthetic run under the approved retention policy.

### Step 9: Validate JSON, protocol coverage, and failure handling

~~~bash
find "$RUN_DIR" -maxdepth 1 -type f -name '*.log' -print
jq -e -s 'length > 0 and all(.[]; (.ts | type) == "number")' \
  "$RUN_DIR/conn.log"
jq -e -s 'length == 1 and .[0].query == "lab-marker.example.test"' \
  "$RUN_DIR/dns.log"
python3 "$LAB_REPO/scripts/network-defense/summarize_network_logs.py" \
  "$RUN_DIR/dns.log" --type zeek
~~~

**Command overview:** Lists generated files, checks JSON and numeric event time, checks the single expected DNS marker, and summarizes rows without publishing raw data.

**Expected:** Nonempty connection metadata, one DNS fixture row, and no invalid JSON. A DNS-only PCAP does not prove HTTP, TLS, SMB, or RDP visibility. An absent `http.log` or `ssl.log` is expected here, not a broken installation.

Test a missing input separately:

~~~bash
if podman run --rm --pull=never --network=none --cap-drop=ALL \
  --security-opt=no-new-privileges --read-only \
  "$ZEEK_IMAGE" zeek -r /does-not-exist.pcap; then
  printf 'FAIL: a nonexistent PCAP was accepted.\n' >&2
  exit 1
fi
~~~

**Negative result:** Zeek must report the missing capture and return nonzero. A failed parse, empty result, or missing expected DNS row is a blocker, not a passing test.

For a richer synthetic HTTP replay, use the existing [worked investigation](OFFLINE_HTTP_WALKTHROUGH.md). Do not manufacture TLS results from a fixture without TLS packets.

## Phase 3: Optional authorized live deployment

### Step 10: Approve the actual traffic feed

**Stop here for an offline-only deployment.**

Have the network owner deliver an authorized TAP/SPAN or virtual-switch mirror to a **dedicated capture NIC** on RHEL-SENSOR01. Record the source ports/VMs, VLANs, packet directions, filter, and expected throughput. Keep management on its existing separate NIC.

VMnet8 NAT, attaching another VM to VMnet8, and enabling promiscuous mode do **not** prove visibility into other VMs' unicast traffic. If Workstation cannot supply the required mirror, continue offline or choose an approved capture architecture. Do not create an inline bridge, enable routing, or capture a shared physical network to compensate.

**Gate:** The network owner approves the exact interface and packet scope. No packet feed, no live deployment.

### Step 11: Prepare only the dedicated capture interface

**Run on RHEL-SENSOR01 with VM console recovery available:**

~~~bash
ip -brief link
ip route show default
nmcli -f NAME,DEVICE,TYPE connection show --active
read -r -p 'Approved dedicated capture interface: ' CAPTURE_IFACE
ip -brief address show dev "$CAPTURE_IFACE"
~~~

**Command overview:** Identifies the interface before any change. Never select the NIC carrying the management address, default route, or remote shell.

For a **new, unused, owner-approved capture NIC only**, create a layer-2-only profile:

~~~bash
sudo nmcli connection add type ethernet ifname "$CAPTURE_IFACE" \
  con-name zeek-capture ipv4.method disabled ipv6.method disabled \
  connection.autoconnect yes
sudo nmcli connection up zeek-capture
ip -brief address show dev "$CAPTURE_IFACE"
ip route show default
~~~

**Expected:** The capture link is up without an IPv4/IPv6 address or a new default route; the original management path is unchanged. If a profile already owns this NIC, stop and have the administrator review that profile rather than creating a conflicting one.

**Undo:** After stopping all capture processes, bring down and delete only the `zeek-capture` profile created by this change. Do not remove the management profile. Adding a local profile does not configure the upstream mirror.

### Step 12: Prove bidirectional visibility with a bounded observation

**Run on RHEL-SENSOR01, only after capture approval:**

~~~bash
sudo timeout --signal=INT 30 tcpdump -nn -i "$CAPTURE_IFACE" \
  -s 256 -c 100 \
  'net 172.25.250.0/24 and (port 53 or tcp port 9997)'
~~~

During that window, an authorized operator on **WINHUNT01** can perform a normal lookup against the lab's existing IdM DNS service:

~~~powershell
Resolve-DnsName splunk01.lab.test -Server 172.25.250.30 -Type A -DnsOnly
~~~

**Command overview:** Observes a maximum of 30 seconds or 100 matching packets, without writing a PCAP. The Windows command is a normal lookup, not a network scan. Also observe existing Windows-to-Splunk forwarding if it is in scope; do not generate credentials or probes to fill an empty capture.

**Expected:** The owner can match the DNS request and response to the two endpoints and the approved capture point. Record tcpdump's captured/dropped counters and the mirror's counters. A timeout can return status `124`; it means the bounded window elapsed, not that visibility passed.

**Negative check:** No packets, one direction only, wrong VLANs, or unrelated traffic means stop. Promiscuous mode is not evidence that a mirror works. The 256-byte diagnostic snap length can truncate content; it is not a recommendation to truncate the subsequent Zeek packet feed.

### Step 13: Prepare the rootful service without starting capture

Rootless image storage and rootful image storage are separate. Pull the **same reviewed digest** for the system service:

~~~bash
ZEEK_IMAGE=$(cat "$ZEEK_WORK/inventory/image-reference.txt")
sudo podman pull "$ZEEK_IMAGE"
sudo podman image inspect "$ZEEK_IMAGE" --format '{{.Id}}'
sudo install -d -m 0700 /etc/zeek-lab /var/lib/zeek-lab/logs
sudo install -m 0600 "$ZEEK_WORK/policy/local.zeek" \
  /etc/zeek-lab/local.zeek
sudo install -m 0600 \
  "$LAB_REPO/configs/network-defense/zeek/run-live.sh.example" \
  /etc/zeek-lab/run-live.sh

sudo podman run --rm --pull=never --network=none --cap-drop=ALL \
  --security-opt=no-new-privileges --read-only \
  -v /etc/zeek-lab:/policy:ro,Z -w /tmp \
  "$ZEEK_IMAGE" zeek --parse-only /policy/local.zeek
~~~

**Command overview:** Preloads the exact image and copies policy and the reviewed startup wrapper into private root-owned directories. The check remains network-disabled. These commands do not start a live sensor.

**Check:** The rootful policy parse succeeds under SELinux Enforcing. Review the [wrapper](../../configs/network-defense/zeek/run-live.sh.example): each start creates a unique `/logs/run-*` directory before `exec` starts Zeek. This prevents an automatic restart from truncating the preceding run's active logs.

**Undo:** Leave the service uninstalled if these checks fail. Preserve existing configuration in a private backup before merging or replacing it.

### Step 14: Review and install the Quadlet definition

~~~bash
install -m 0600 \
  "$LAB_REPO/configs/network-defense/zeek/zeek-live.container.example" \
  "$ZEEK_WORK/zeek-live.container"
~~~

Open the staged file in a local editor. Replace:

1. `REPLACE_WITH_APPROVED_DIGEST` with the reviewed 64-character digest, keeping the complete official image reference.
2. `REPLACE_WITH_CAPTURE_INTERFACE` with the dedicated interface proven in Step 12.

Review the quoted `net 172.25.250.0/24` BPF filter against the written authorization. It admits packets with a source or destination in that subnet; it is not an access-control boundary. For VLAN-tagged mirrors, have the capture owner validate an appropriate BPF expression against the actual feed.

~~~bash
if grep -n 'REPLACE_' "$ZEEK_WORK/zeek-live.container"; then
  printf 'Unresolved service placeholders; do not install.\n' >&2
  exit 1
fi
sudo install -d -m 0755 /etc/containers/systemd
sudo install -m 0644 "$ZEEK_WORK/zeek-live.container" \
  /etc/containers/systemd/zeek-live.container
~~~

**Command overview:** Stages a reviewable unit and installs it only after placeholders are removed.

The [Quadlet example](../../configs/network-defense/zeek/zeek-live.container.example) uses:

| Control | Purpose and limit |
| --- | --- |
| Digest plus `Pull=never` | No unexpected image pull at service start |
| `Network=host` | Access the approved host capture NIC; removes container network isolation |
| Rootful `User=0`, only `CAP_NET_RAW` | Open packet sockets in the host network namespace; this is a privileged capture boundary, not a sandbox for untrusted code |
| `DropCapability=all`, `NoNewPrivileges=true` | Avoid unrelated capabilities and privilege escalation |
| Read-only root/policy mounts | Limit writable state to private logs and temporary runtime storage |
| Private SELinux `:Z` mounts, restrictive umask | Protect raw metadata; do not share the raw mount with the UF |
| Restart rate limit and new run directory | Recover from transient failure without overwriting earlier logs or endlessly restarting a broken configuration |
| No `[Install]` section | No automatic boot capture until Step 17 explicitly approves it |

Do not add `--privileged`, disable SELinux labels, grant `CAP_SYS_ADMIN`, publish ports, or mount the host filesystem to solve an error. If the installed libpcap/SELinux policy requires another permission, stop for a narrowly scoped review.

### Step 15: Generate and inspect the service before starting it

~~~bash
sudo systemctl daemon-reload
sudo systemctl cat zeek-live.service
sudo systemd-analyze verify zeek-live.service
sudo systemctl is-active zeek-live.service
~~~

**Command overview:** Quadlet generates `zeek-live.service` from `zeek-live.container`; inspect the generated arguments and validate the service syntax.

**Expected:** A generated service using the approved digest, interface, filter, and mount paths. `is-active` should report `inactive` before the first start; that nonzero status is expected at this stage. A generated service is not proof of capture.

**Stop if:** The unit is missing, a Quadlet key is unsupported, the image is not in rootful storage, the filter is wrong, or another service already owns `zeek-lab`. Consult the installed `man podman-systemd.unit` and journal; do not replace a conflicting service.

### Step 16: Perform a bounded live-service smoke test

**This step starts capture.** Coordinate the same harmless authorized DNS lookup from Step 12 in a second terminal. Run the complete subshell so its exit handler stops the service after the observation or an interruption:

~~~bash
(
  set -e
  trap 'sudo systemctl stop zeek-live.service' EXIT
  trap 'exit 129' HUP
  trap 'exit 130' INT
  trap 'exit 143' TERM
  sudo systemctl start zeek-live.service
  sleep 60
)
sudo journalctl -u zeek-live.service --since '-5 minutes' --no-pager
sudo podman ps --filter name=zeek-lab
sudo find /var/lib/zeek-lab/logs -mindepth 1 -maxdepth 2 \
  -type f -name '*.log' -print
~~~

**Command overview:** Runs a 60-second observation, stops Zeek, and inspects private service records and output filenames. Stop it immediately if the scope or management baseline changes; keep console recovery available.

Select the exact run directory printed in the journal:

~~~bash
read -r -p 'Exact /var/lib/zeek-lab/logs/run-* directory for this test: ' LIVE_RUN
sudo jq -e -s 'length > 0 and all(.[]; (.ts | type) == "number")' \
  "$LIVE_RUN/conn.log"
~~~

**Expected:** The container is no longer running, the service shut down cleanly, and the selected run contains the approved flow with valid JSON/event times. Review both endpoints and directionality privately. A live DNS query is not the synthetic fixture and must not be copied by the fixture-export procedure below.

**Negative check:** An active unit with no expected flow is a failed visibility test. A short run may not produce meaningful `stats.log` or `capture_loss.log`; missing metrics are not zero loss. Do not index unrelated live metadata to demonstrate success.

### Step 17: Approve ongoing capture and startup at boot

Only continue after the smoke test, private storage/retention plan, packet-loss review, and owner sign-off. The template intentionally does not auto-start on reboot.

Create `/etc/containers/systemd/zeek-live.container.d/10-autostart.conf` with `sudoedit`, first creating its parent directory if it does not exist:

~~~bash
sudo install -d -m 0755 /etc/containers/systemd/zeek-live.container.d
sudoedit /etc/containers/systemd/zeek-live.container.d/10-autostart.conf
~~~

Enter this reviewed content:

~~~ini
[Install]
WantedBy=multi-user.target
~~~

Then:

~~~bash
sudo systemctl daemon-reload
sudo systemctl start zeek-live.service
sudo systemctl is-active zeek-live.service
sudo systemctl cat zeek-live.service
~~~

**Command overview:** Adds Quadlet's boot dependency and starts the approved ongoing capture. Do **not** run `systemctl enable zeek-live.service`: Quadlet generates the service and applies its `[Install]` dependencies itself.

**Check:** During an approved later sensor reboot, verify the expected capture NIC, service, fresh run directory, output, and core-lab health. Merely seeing `active` is insufficient.

**Undo:** Follow Step 27 to stop capture and remove the Quadlet from the generator's search. No existing VM service needs to be changed.

## Phase 4: Optional Splunk integration

### Step 18: Review Splunk version, parsing, and index placement

**Run on RHEL-SPLUNK01 as the actual Splunk service identity:**

~~~bash
sudo -u splunk /opt/splunk/bin/splunk version
sudo -u splunk /opt/splunk/bin/splunk btool props list zeek:json --debug
sudo -u splunk /opt/splunk/bin/splunk btool indexes list --debug
~~~

**Command overview:** Records the installed version and effective source/index definitions before proposing changes. Adapt the path/identity if this lab differs.

Have the owner review the version and existing stanzas before making installation-specific changes. If a supported Zeek add-on is already installed, use its documented sourcetypes and parsing strategy rather than layering this custom source type over it.

For the custom `zeek:json` path, review [props.conf.example](../../configs/network-defense/zeek/props.conf.example):

- Place line-breaking and timestamp settings on the **first full parsing tier**, normally RHEL-SPLUNK01 in this all-in-one lab, not blindly on a Universal Forwarder.
- Place `KV_MODE=json` on the **search tier**. This is the same server in the all-in-one lab but not necessarily in a distributed deployment.
- The reference format `%s.%6N` parses Zeek's fractional epoch `ts`. Inspect the actual JSON and preview on the installed Splunk build; if the selected producer emits integer-only timestamps, review `%s` instead. Do not substitute receipt time.
- Keep each JSON object as one event. Validate maximum event length; do not blindly disable truncation limits.
- This example uses search-time JSON extraction. Do not combine it with `INDEXED_EXTRACTIONS=json` without a reviewed plan to avoid duplicate field extraction.

For the one-time fixture upload, use existing index **`lab`**. For persistent sensor ingestion, create optional **`net_zeek`** only after reviewing storage, retention, and role access under [Splunk integration](SPLUNK_INTEGRATION.md). Merge only the needed index stanza from the [proposed indexes](../../configs/network-defense/splunk/indexes.conf.example); do not install all optional indexes just for Zeek.

**Check/undo:** Back up and merge, never overwrite existing `props.conf` or `indexes.conf`. Use `btool` and the installed version's restart/reload procedure. Keep all six core indexes and existing app settings unchanged. Restore only this change's stanzas if the parser test or core-lab regression fails.

### Step 19: Export and upload only the approved synthetic DNS row

**Run on RHEL-SENSOR01**, using the successful offline `RUN_DIR` from Step 8:

~~~bash
STAGED_JSON=$(mktemp --suffix=.log \
  "$ZEEK_WORK/approved/zeek-dns-fixture-XXXXXXXX")
jq -c '
  if .query == "lab-marker.example.test" then
    {ts, uid,
     "id.orig_h": .["id.orig_h"], "id.orig_p": .["id.orig_p"],
     "id.resp_h": .["id.resp_h"], "id.resp_p": .["id.resp_p"],
     query, qtype_name}
  else error("Not the authorized synthetic DNS fixture")
  end
' "$RUN_DIR/dns.log" > "$STAGED_JSON" &&
  jq -e -s 'length == 1 and (.[0].ts | type) == "number"' "$STAGED_JSON"
printf 'Review this private synthetic upload: %s\n' "$STAGED_JSON"
~~~

**Command overview:** Creates a uniquely named private staging file with an explicit field allowlist and rejects a different DNS question. This is a synthetic-fixture export, **not a live-data sanitizer**. Do not stage a partial file after an error.

On the private **Splunk Web** console:

1. Open **Add Data > Upload** and select only this approved synthetic JSON file.
2. Use the reviewed `zeek:json` source type. Confirm one JSON object becomes one event and the preview time matches numeric `ts`, accounting for the UI time zone.
3. Select index **`lab`** and host **`zeek-fixture`**.
4. Review the destination and submit once. Repeat uploads duplicate data; generate a new fixture/run for a deliberate retest.

Search:

~~~spl
index=lab host=zeek-fixture sourcetype=zeek:json earliest=-30m query="lab-marker.example.test"
| eval drift_s=abs(_time-ts)
| stats count count(ts) as timestamped max(drift_s) as max_time_error_s
~~~

**Expected:** One row, `timestamped=1`, and event-time error no greater than `0.001` seconds. If the fixture is older, use its absolute time range and check retention rather than changing the event time to ingestion time.

**Negative check:** An unrelated JSON file, missing marker, split JSON event, incorrect timestamp, or duplicate upload must not pass acceptance. Stop before enabling a persistent input. A successful upload does not prove UF TLS forwarding.

### Step 20: Install a separate Linux Universal Forwarder, if approved

Skip Steps 20-22 for a one-time upload. Zeek does not require the UF to run.

**Run on RHEL-SENSOR01.** Verify that the exact UF release supports the installed RHEL 10 version and CPU architecture in the official Splunk requirements. Obtain the Linux RPM and published verification material from Splunk through the approved software process, outside Git.

~~~bash
read -r -p 'Full path to the approved Linux UF RPM: ' UF_RPM
sha256sum "$UF_RPM"
rpm -K "$UF_RPM"
rpm -qp --qf '%{NAME} %{VERSION}-%{RELEASE} %{ARCH}\n' "$UF_RPM"
~~~

**Command overview:** Checks the artifact's hash, RPM signature, name, version, and architecture. Compare against the vendor's trusted verification material. `NOKEY`, a mismatch, or an unsupported platform is a blocker; do not use `--nosignature`, an unverified signing key, or a Windows MSI.

For a first installation only, after those checks pass:

~~~bash
sudo rpm -i "$UF_RPM"
stat -c '%U:%G %n' /opt/splunkforwarder
read -r -p 'Verified UF service account for this release: ' UF_USER
id "$UF_USER"
sudo -u "$UF_USER" /opt/splunkforwarder/bin/splunk start --accept-license
~~~

**Command overview:** Installs the reviewed RPM and starts the UF under its verified non-root service account. Follow the selected release's Linux first-start procedure; enter any bootstrap credentials interactively in the private terminal, never in a command, repository file, or screenshot. Do not assume the account name from a different release.

If approved for boot, use the installed release's native systemd procedure. For releases supporting this form:

~~~bash
sudo -u "$UF_USER" /opt/splunkforwarder/bin/splunk stop
sudo /opt/splunkforwarder/bin/splunk enable boot-start \
  -user "$UF_USER" -systemd-managed 1
~~~

Review the resulting unit name, ownership, and startup behavior, then start the verified unit:

~~~bash
read -r -p 'Verified generated UF unit name, including .service: ' UF_UNIT
sudo systemctl cat "$UF_UNIT"
sudo systemctl start "$UF_UNIT"
sudo systemctl status "$UF_UNIT" --no-pager
~~~

**Command overview:** Stops the CLI-started process before handing lifecycle management to systemd. Boot registration can enable startup, so run it only after that approval. Do not simultaneously manage the same UF process through both CLI and systemd.

**Check/undo:** Confirm the UF runs as the selected service account and has no enabled Zeek input yet. If a UF is already installed, do not reinstall or change its identity: review and merge. On failure, stop only this new sensor UF; do not change the existing Windows forwarder.

### Step 21: Verify the sensor-to-Splunk TLS path

**On RHEL-SPLUNK01:** Review the existing `9997/tcp` receiver and firewall zone. The Windows `.20` allowance does not automatically authorize sensor `.40`. If needed, approve an additional source-limited rule for `172.25.250.40/32` to `9997/tcp`; do not open the receiver to all sources or replace existing rules.

**On RHEL-SENSOR01:** Use a privately provisioned trusted CA chain and the exact hostname in the receiver certificate:

~~~bash
getent hosts splunk01.lab.test
read -r -p 'Absolute path to the approved receiver CA chain: ' CA_FILE
openssl s_client -connect splunk01.lab.test:9997 \
  -servername splunk01.lab.test \
  -CAfile "$CA_FILE" -verify_hostname splunk01.lab.test \
  -verify_return_error </dev/null
~~~

**Command overview:** Tests DNS, TCP reachability, certificate-chain trust, and server-name verification. A successful TCP connection alone is not a verified TLS result. If the existing receiver requires mutual TLS, use its approved client-certificate procedure; never publish or generate a replacement private key in this repository.

Configure the UF output only after reviewing its current `btool outputs` and `btool server` results. The actual merged configuration must preserve these requirements:

| Requirement | Expected setting or review |
| --- | --- |
| Destination | `splunk01.lab.test:9997` |
| TLS enabled | `useSSL=true` |
| Trusted server certificate | `sslVerifyServerCert=true` and the approved CA chain |
| Name verification | `sslVerifyServerName=true` and the installed release's supported SAN-name checks for `splunk01.lab.test` |
| CA placement | Installed version's `server.conf`/`outputs.conf` specification; do not invent a setting in the wrong stanza |
| Delivery assurance | Review indexer acknowledgment, queue/backpressure, and receiver behavior |

The repository deliberately ships no sensor `outputs.conf` or secrets. Use [the existing forwarding troubleshooting guide](../troubleshooting/splunk-forwarder-tls-and-kv-service.md) and [Splunk integration](SPLUNK_INTEGRATION.md) with the verified Linux release.

**Negative check:** A hostname mismatch, untrusted CA, unauthorized source, or required-but-missing client certificate must fail. Do not set verification to false to make forwarding work. Revert only firewall/TLS changes introduced for this sensor if acceptance fails.

### Step 22: Stage approved metadata and enable only the Zeek input

The [sensor input app](../../apps/SENSOR_UF/local/inputs.conf) ships **disabled**. Keep it disabled until the optional index, parsing, TLS, RBAC, and privacy gates pass.

**Run on RHEL-SENSOR01** with the verified `UF_USER` and successful synthetic `STAGED_JSON`:

~~~bash
UF_GROUP=$(id -gn "$UF_USER")
sudo install -d -o root -g "$UF_GROUP" -m 0750 \
  /var/log/siem-sensor /var/log/siem-sensor/zeek
sudo install -o root -g "$UF_GROUP" -m 0640 "$STAGED_JSON" \
  "/var/log/siem-sensor/zeek/$(basename "$STAGED_JSON")"
sudo -u "$UF_USER" test -r \
  "/var/log/siem-sensor/zeek/$(basename "$STAGED_JSON")"
~~~

**Command overview:** Copies only the approved synthetic row into a separate UF-readable staging directory. The UF does not receive access to `/var/lib/zeek-lab/logs`, PCAPs, or the container's private SELinux mount.

After backing up and merging the sensor app, enable **only** this reviewed Zeek stanza in the actual on-host UF configuration:

~~~ini
[monitor:///var/log/siem-sensor/zeek/*.log]
disabled = 0
index = net_zeek
sourcetype = zeek:json
~~~

Leave Suricata and YARA inputs disabled. This guide does not change the repository's disabled defaults. Verify the effective configuration:

~~~bash
sudo -u "$UF_USER" /opt/splunkforwarder/bin/splunk btool inputs list --debug
sudo -u "$UF_USER" /opt/splunkforwarder/bin/splunk btool outputs list --debug
sudo -u "$UF_USER" /opt/splunkforwarder/bin/splunk btool server list --debug
~~~

Apply the installed release's approved reload/restart procedure, then inspect the local UF logs privately for forwarding and indexing errors.

**Check:** The monitor selects the staging directory, `net_zeek` exists, only the approved input is enabled, and the UF can read but does not own the staged files. If permission or SELinux checks fail, investigate the exact denial rather than granting world access.

**Live-forwarding boundary:** Do not copy all live logs into staging or point the monitor at the raw run directory. Continuous live export needs a separately reviewed field/privacy policy and a durable staging process: closed rotated files, unique names, atomic publication, retry/offset tracking, backpressure, and retention. The fixture export is not that process.

**Undo:** Disable only this Zeek stanza and use the approved UF reload/restart procedure. Retain staged data until the owner decides retention; do not reset the fishbucket or re-copy files under new names to force delivery.

### Step 23: Prove ingestion, event time, RBAC, and regression

**Run in Splunk Search on RHEL-SPLUNK01:**

~~~spl
index=net_zeek sourcetype=zeek:json earliest=-30m
| stats count max(_time) as last_event by host source
| convert ctime(last_event)
~~~

~~~spl
index=net_zeek sourcetype=zeek:json earliest=-30m query="lab-marker.example.test"
| eval drift_s=abs(_time-ts)
| stats count count(ts) as timestamped max(drift_s) as max_time_error_s
~~~

~~~spl
index=net_zeek sourcetype=zeek:json earliest=-30m
| table _time host source uid id.orig_h id.orig_p id.resp_h id.resp_p query
~~~

**Command overview:** Checks received sources, event-time accuracy, and the actual Zeek fields. The dotted names are literal JSON field names. In `eval` expressions, reference dotted fields with single quotes, for example `src='id.orig_h'`; do not assume Windows/Sysmon field names.

**Expected:** The forwarded fixture appears once in `net_zeek`, with numeric `ts` and no more than `0.001` seconds of timestamp drift. The separate one-time upload remains in `lab`; it is not proof of this forwarding path. Empty results, null fields, ingestion warnings, or duplicates require investigation.

Test the authorized analyst's index access and, using a separately approved restricted account, confirm a role without `net_zeek` permission cannot retrieve its data. Do not grant all-index access to fix a failed search.

Finally repeat the existing Windows/Sysmon ingestion, Splunk Web, IdM DNS/LDAPS, and six-index health checks. Record actual results; a new Zeek search must not hide a regression in the core lab.

## Phase 5: Operations, troubleshooting, and rollback

### Step 24: Monitor health, loss, rotation, and storage

**Run on RHEL-SENSOR01:**

~~~bash
sudo systemctl status zeek-live.service --no-pager
sudo journalctl -u zeek-live.service --since '-30 minutes' --no-pager
sudo podman stats --no-stream zeek-lab
sudo du -sh /var/lib/zeek-lab/logs
df -h /var/lib/zeek-lab
~~~

**Command overview:** Shows process health, failures/restarts, CPU/memory, log growth, and free space. A healthy process is only one part of sensor health.

Inspect the current private run's `stats.log` and, when available, `capture_loss.log`. Review `pkts_proc`, optional `pkts_dropped`/`pkts_link`, and capture-loss `gaps`, `acks`, and `percent_lost`. Missing optional counters are **unknown**, not zero. Capture-loss analysis depends on suitable TCP traffic and observation intervals; it does not measure every loss upstream of a mirror or validate UDP visibility.

The policy rotates logs hourly using Zeek's rotation framework. This standalone deployment does not use a ZeekControl `logs/current` tree. It also does **not** automatically expire old runs.

Before unattended operation, approve and implement monitored retention with a disk budget, alerts, forwarding backlog allowance, and legal-hold exclusions. Inventory candidate files without deleting them:

~~~bash
sudo find /var/lib/zeek-lab/logs -type f -name '*.log' -mtime +7 -print
~~~

**Check:** This is a review list, not a seven-day deletion policy. Do not delete active files or unforwarded evidence, use `copytruncate`, blindly compress a watched staging file, or add an unreviewed cleanup cron job. A full disk or growing loss rate is an incident to investigate, not an acceptable baseline.

Scale only after measurement. A multi-worker/AF_PACKET or ZeekControl design needs its own packet-distribution, affinity, state, logging, and privilege review; starting duplicate independent captures is not a scaling plan.

### Step 25: Back up and upgrade with a reversible change

Keep private backups of `/etc/zeek-lab`, the Quadlet, its optional drop-in directory, the approved image reference, and the exact on-host Splunk/UF stanzas before changing them. Do not put backups inside a mounted log directory, monitored staging directory, or Git.

For every upgrade:

1. Select the maintained official release and record the new digest and architecture.
2. Repeat the rootless version, policy-parse, synthetic PCAP, and JSON checks in fresh directories.
3. Compare field names, timestamps, notices, row counts, and installed-version parser behavior.
4. Pre-pull the reviewed new digest into rootful storage while keeping the old image.
5. During the approved window, stop `zeek-live.service`, merge the reviewed policy/unit changes, reload systemd, and start it again.
6. Prove the approved live flow, fresh run directory, loss/storage behavior, TLS ingestion if enabled, and core-lab regression.
7. Roll back to the exact previous digest and configuration if acceptance fails.

**Command overview:** An upgrade is a tested configuration-and-image change, not a tag refresh. Do not use unattended container auto-update or prune the rollback image before acceptance. A restarted process uses a new run directory; preserve the earlier evidence and forwarding backlog.

### Step 26: Troubleshoot the failing layer

| Symptom | Check and corrective action |
| --- | --- |
| No RHEL 10 Zeek package | Do not assume `dnf install zeek` works or install another distribution's RPM. Use the approved official container path or a separately tested source build. |
| Image pull fails | Check the official tag, architecture, approved registry/proxy access, and TLS trust. Do not use an insecure registry or an unrelated mirror. |
| Offline output is permission denied | Check dedicated directory ownership, `--userns=keep-id`, mount paths, and SELinux labels. Do not use `chmod 777` or `--privileged`. |
| Policy parse fails | Read the exact Zeek error, verify the release and script paths, restore the reviewed policy, and rerun `--parse-only`. |
| Quadlet service is missing | Inspect the installed `man podman-systemd.unit`, the `.container` filename/search path, cgroup v2, supported keys, and generator errors. Do not manually edit a generated service. |
| Repeated failure reaches the start limit | Stop, fix the actual cause, then use `sudo systemctl reset-failed zeek-live.service` before a deliberate retry. Do not remove the rate limit. |
| Live capture says operation not permitted | Check rootful execution, host networking, `CAP_NET_RAW`, and the exact AVC denial. Review `sudo ausearch -m AVC,USER_AVC -ts recent` if audit tooling is installed. Do not disable SELinux or add broad capabilities. |
| Service runs but sees no expected flow | Repeat the bounded mirror/interface/VLAN/direction test. Check the BPF filter against the actual feed. Service status does not establish packet coverage. |
| tcpdump sees traffic but Zeek lacks connections | Check checksum errors and `ethtool -k "$CAPTURE_IFACE"`. Local/virtual offload artifacts can require a reviewed `-C` decision or capture-path correction. Never add `-C` blindly; it disables checksum validation. |
| No HTTP/TLS log | Confirm the capture contains that protocol and both directions. Encryption and unsupported/encrypted handshakes limit visibility. DNS-only fixtures cannot prove TLS analysis. |
| New process seems to lose old logs | Inspect each `run-*` directory. The wrapper must create a fresh one; do not bypass it or reuse the same offline output directory. |
| No Splunk result | Check raw producer output, approved staging, UF read access, effective input/index, output/receiver errors, time window, retention, and RBAC in that order. Do not reset ingestion state to mask the issue. |
| Splunk fields duplicate or time is wrong | Review the effective source type on parsing/search tiers, `ts` representation, line breaking, and indexed versus search-time JSON extraction. Test a new fixture before changing live parsing. |
| UF TLS fails | Check trusted CA, certificate SAN/name, receiver requirements, sensor source allowance, and system time. Never disable verification. |
| Disk or packet loss grows | Stop unapproved collection, protect evidence, reduce only owner-approved scope, and investigate mirror capacity, CPU, queues, and storage. Do not label absent metrics as zero loss. |

**Summary:** Fix the first failing layer and repeat its positive and negative checks. Do not treat a later-stage search as a substitute for packet visibility, valid JSON, or TLS verification.

### Step 27: Stop and roll back only this extension

**Run on RHEL-SENSOR01:**

~~~bash
sudo systemctl stop zeek-live.service
sudo mv /etc/containers/systemd/zeek-live.container \
  /etc/containers/systemd/zeek-live.container.disabled
sudo systemctl daemon-reload
sudo podman ps --filter name=zeek-lab
~~~

**Command overview:** Stops capture and removes the Quadlet from active generation without deleting configuration, images, or evidence. Check first that the `.disabled` destination does not already exist. The associated auto-start drop-in no longer activates a missing `.container` source.

Then, only where this change introduced them:

1. Disable the Zeek UF monitor and follow the approved UF restart/reload procedure; keep unrelated inputs and Windows forwarding intact.
2. Restore the previous optional parsing/output settings from private backups if reverting those changes is required. Keep parsers needed to search already indexed evidence.
3. Remove only the sensor-specific firewall allowance added by this change, after confirming no other approved service depends on it.
4. After capture has stopped, remove only the newly created capture-NIC profile if returning that NIC to its previous design.
5. Keep raw logs, staged files, optional index data, and the old image until retention/hold review. Do not delete an index or raw evidence as a rollback shortcut.
6. Recheck Splunk Web, Windows UF, IdM DNS/LDAPS, the management route, and the six core indexes.

For an upgrade rollback, restore the previous policy and `.container` source from the private backup, reload systemd, and start it only if the previous capture authorization still applies.

### Step 28: Record acceptance evidence

Use the [existing evidence worksheet](../../evidence/sanitized/network-defense-validation.md). Keep live records private and publish only reviewed sanitized summaries.

| Acceptance item | Required observation | Milestone |
| --- | --- | --- |
| Scope and host | Owner approval, approved subnet/interface, actual RHEL/Podman/Zeek versions, repository revision, and image digest | NET-01, NET-02 |
| Offline input | Synthetic PCAP SHA-256, timestamp, and decoded DNS marker | NET-03, NET-04 |
| Offline Zeek | Successful parse, valid connection JSON, exactly one DNS fixture row, and failed missing-file test | NET-05 |
| Live capture, if approved | Proven bidirectional feed, actual filter, clean stop/start, fresh run directories, and measured loss/visibility limits | NET-11 |
| Persistent service, if approved | Generated arguments reviewed and approved reboot/startup verified | NET-11 |
| Splunk upload | One synthetic event with extracted fields and no more than `0.001` seconds of event-time error | NET-10 |
| UF, if approved | Correct service identity, approved staging, verified TLS/name checks, input/index routing, and separate forwarded fixture | NET-09, NET-10 |
| Access and failure checks | Unauthorized role cannot retrieve `net_zeek`; invalid policy/input/TLS is rejected | NET-09, NET-10 |
| Operations and rollback | Defined retention/disk alerts, private backups, stop procedure, and recoverable previous image/configuration | NET-11 |
| Existing lab | Splunk, Windows ingestion, IdM DNS/LDAPS, and original six indexes still work | NET-14 |

Leave any unperformed item **Pending** or **Not in scope** with its reason. Documentation, source checks, example output, and screenshots of commands do not establish a deployed sensor or operational detection.

## Official references

- [Zeek 9.0.1 release](https://github.com/zeek/zeek/releases/tag/v9.0.1), [installation](https://docs.zeek.org/en/current/install.html), and [OS support](https://github.com/zeek/zeek/wiki/Zeek-Operating-System-Support-Matrix).
- [Official image documentation and source](https://github.com/zeek/zeek/tree/v9.0.1/docker), including the runtime image's `/usr/local/zeek` installation.
- [Zeek quick start](https://docs.zeek.org/en/current/quickstart.html), [logging framework](https://docs.zeek.org/en/current/frameworks/logging.html), and [JSON writer options](https://docs.zeek.org/en/current/scripts/base/frameworks/logging/writers/ascii.zeek.html).
- [Podman Quadlet reference](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html). Check the installed manual for the sensor's version; the example uses options documented in [Podman 5.4](https://github.com/containers/podman/blob/v5.4.0/docs/source/markdown/podman-systemd.unit.5.md).
- [RHEL 10 documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10) for subscription access, containers, NetworkManager, SELinux, time, and firewall administration.
- [Splunk Enterprise documentation](https://help.splunk.com/en/splunk-enterprise): select the installed Enterprise/UF versions for Linux support, installation, TLS, configuration specifications, file monitoring, and source-type preview.
- Repository companions: [network deployment guide](IMPLEMENTATION_GUIDE.md), [packet analysis](ZEEK_AND_WIRESHARK.md), [Splunk integration](SPLUNK_INTEGRATION.md), and [official reference index](REFERENCES.md).
