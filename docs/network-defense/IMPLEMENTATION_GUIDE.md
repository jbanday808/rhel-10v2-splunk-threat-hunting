# Complete 30-Step Guide — Passive Network Defense Lab on RHEL 10.2 with Splunk

**Scope:** Build a project-focused, *non-intrusive* workflow for Zeek, Wireshark/TShark, tcpdump, Suricata IDS, YARA, Sigma and CMMC Level 2/NIST SP 800-171 evidence mapping. Your existing VMware Splunk/IdM/Windows services are preserved. No live sensor, detection, capture or CMMC assessment is claimed by publishing this guide.

**Host plan:** RHEL-SPLUNK01 `172.25.250.10`; WINHUNT01 `172.25.250.20`; RHEL-IDM01 `172.25.250.30`; optional **NEW** RHEL-SENSOR01 `172.25.250.40` (verify no collision); Windows 11 host and WSL at VMnet8 `172.25.250.1`. Follow [architecture](ARCHITECTURE.md) and [CONOPS](CONOPS.md).

**Terms:** *PCAP* is a packet capture, *IDS* observes/alerts without blocking, *TAP/SPAN* delivers authorized traffic copies, *EVE* is Suricata JSON event output, *SPL* is Splunk Search Processing Language. Only use packets from owned or explicitly authorized sources.

For a first run on an existing analysis workstation, use the [worked HTTP investigation](OFFLINE_HTTP_WALKTHROUGH.md). It includes known-good and candidate traffic, an alert tuning comparison and a one-time Splunk upload. The following deployment path covers the optional dedicated sensor.

## Phase 1 — Scope, inventory and preparation

### Step 01 — Synchronize the existing GitHub repository (Ubuntu WSL)

~~~bash
cd ~/projects/rhel-10v2-splunk-threat-hunting
git status
git switch main
git pull --ff-only origin main
code .
~~~

**Command overview:** `cd` enters the existing repo, `git status` displays uncommitted edits, `switch` selects the main branch, `pull --ff-only` downloads the newest documents, and `code .` opens VS Code.

**Validate:** Original 52 deployment steps and existing six indexes are intact.

### Step 02 — Adopt a written CONOPS (WSL and security owner)

Review [CONOPS](CONOPS.md), [architecture](ARCHITECTURE.md), [CMMC mapping](CMMC_LEVEL2.md). Record capture owner, approved sample PCAPs, intended devices/protocols, retention, security contacts, escalation thresholds, change approvals, and **prohibited active scanning**.

**Validate:** No CUI or classified information in public GitHub. All live results remain Pending.

### Step 03 — Create a baseline and recovery plan (VMware)

From VMware Workstation Pro, document the current Splunk, Windows, and IdM VM status. Take consistent snapshots/backups under your approved procedure, and verify the management console is accessible. For IdM, use a supported stateful backup/restore method; do not rely on an untested running snapshot. Record network/firewall/TLS baselines privately.

**Validate:** Splunk Web 8000, Windows UF 9997, IdM LDAPS/DNS and `/splunkdata` remain functional before the sensor addition.

### Step 04 — Choose offline-first sensing (host design)

Use **a new optional sensor VM**, rather than installing Suricata/Zeek on the Splunk indexer or IdM directory server. Allocate resources as your workstation permits (illustrative: 2–4 vCPU, 4–8 GiB RAM, 40+ GiB separate storage), with RHEL 10.2 and **no** active routing/bridging to production. Any second sniffing NIC is **future work**, not needed for offline PCAPs.

Follow the existing [download and verification steps](../steps/04-download-and-verify-the-software.md) and [VMware RHEL installation](../steps/05-create-and-install-the-rhel-vm.md) with a separate VM name and disk. Use the sensor's management address from the architecture table when adapting the [networking steps](../steps/06-configure-rhel-networking.md). Stop before any Splunk-server-specific steps.

**Validate:** Proposed sensor address `172.25.250.40` is free and no existing firewall/network rule is altered.

### Step 05 — Verify RHEL 10.2 sensor and networking (RHEL-SENSOR01 console)

~~~bash
cat /etc/redhat-release
hostnamectl
ip -brief address
nmcli -f NAME,DEVICE,TYPE connection show --active
getenforce
sudo firewall-cmd --get-active-zones
df -hT
~~~

**Command overview:** Shows OS, hostname, interfaces, active profiles, SELinux/firewall and free storage. Configure hostname `sensor01.lab.test` and the chosen IP only through a separate approved NetworkManager change with VM console recovery. **Do not** copy the Splunk server's network zone blindly.

### Step 06 — Protect private working data (RHEL-SENSOR01)

~~~bash
mkdir -p "$HOME/network-lab/private-pcaps" \
         "$HOME/network-lab/zeek-out" \
         "$HOME/network-lab/suricata-out" \
         "$HOME/network-lab/yara-test"
chmod 700 "$HOME/network-lab" "$HOME/network-lab/"*
~~~

**Command overview:** Creates private PCAP, log and synthetic-file working directories with user-only access. Never place raw captures in a public Git directory or a Splunk monitored log path.

### Step 07 — Install first-party utilities (RHEL-SENSOR01)

~~~bash
sudo dnf install -y python3 git tcpdump wireshark-cli podman
rpm -q python3 tcpdump wireshark-cli podman
tshark --version
podman --version
~~~

**Command overview:** Installs RHEL-supported base tools and reads package versions. If RHEL registration/repositories do not provide a package, check entitlements instead of enabling random repos. `wireshark-cli` provides TShark; full Wireshark GUI is optional on Windows, not necessary on a headless sensor.

## Phase 2 — Build a safe reproducible packet dataset

### Step 08 — Generate a harmless synthetic DNS PCAP (WSL or RHEL-SENSOR01)

From the repository checkout (or reviewed script copied to sensor):

~~~bash
python3 scripts/network-defense/generate_synthetic_pcap.py \
  --output "$HOME/network-lab/private-pcaps/lab-dns.pcap"
sha256sum "$HOME/network-lab/private-pcaps/lab-dns.pcap"
~~~

**Command overview:** Creates a **synthetic DNS request** using reserved documentation IP addresses and `lab-marker.example.test`. Store the file privately and retain its SHA-256. The default timestamp is fixed for reproducibility. If replaying into a short-retention Splunk index, pass `--timestamp "$(date -u +%s)"` to the generator and regenerate the sensor logs before indexing.

### Step 09 — Decode the DNS PCAP with TShark (sensor)

~~~bash
tshark -r "$HOME/network-lab/private-pcaps/lab-dns.pcap" \
  -Y "dns" -T fields \
  -e frame.number -e ip.src -e ip.dst -e dns.qry.name
~~~

**Command overview:** Reads an **existing** capture (`-r`), filters DNS (`-Y`) and displays selected fields (`-T fields -e`). It does not collect live traffic.

### Step 10 — Investigate packets using Wireshark GUI (optional Windows host)

Transfer the **synthetic** PCAP only, via a reviewed private path. Open it in Wireshark (File → Open) and apply `dns`, `tcp`, `tls` or `http` display filters as data permits. Use `Statistics → Protocol Hierarchy` and `Conversations` to establish what the capture actually contains. No real credentials or private CUI may be exported in screenshots.

### Step 11 — Learn read-only capture commands without touching other VM traffic

For a **future explicitly approved** capture interface, inspect:

~~~bash
sudo tcpdump -D
ip -br link
~~~

**Command overview:** These commands list interfaces. After the owner approves the exact interface, endpoint pair, protocol, and retention, run a bounded sample. Replace both documentation IPs with the specific endpoints in the approved scope. Check whether a 128-byte snapshot is sufficient for the stated purpose.

~~~bash
umask 077
CAPTURE_RUN=$(mktemp -d "$HOME/network-lab/private-pcaps/authorized-XXXXXXXX")
read -r -p 'Approved capture interface: ' CAPTURE_IFACE
sudo timeout --signal=INT 20 tcpdump -nn -i "$CAPTURE_IFACE" -s 128 -c 50 -w - \
  'host 192.0.2.20 and host 192.0.2.10 and tcp port 80' > "$CAPTURE_RUN/bounded.pcap"
~~~

**Summary:** `timeout` caps the capture at 20 seconds and `-c` stops at 50 matching packets. `-nn` suppresses name lookups, `-s` caps stored bytes per packet, `-w -` streams the capture to the private file, and the quoted filter limits it to the approved flow. Record tcpdump's captured and dropped packet counters and keep separate notes about potential mirror loss and missing directions.

## Phase 3 — Zeek protocol intelligence

### Step 12 — Select a supported Zeek installation method

**Important:** Zeek does not guarantee native RHEL 10 binary RPM support. Review [Zeek official install](https://docs.zeek.org/en/current/install.html), [OS support](https://github.com/zeek/zeek/wiki/Zeek-Operating-System-Support-Matrix), the installed RHEL kernel and container policy. Prefer an approved, **version-pinned official container** or a tested Zeek source build; never use random unofficial RPMs.

After confirming the exact image tag exists in the vendor registry and approving the digest, an example is:

~~~bash
podman pull docker.io/zeek/zeek:9.0.1
podman image inspect docker.io/zeek/zeek:9.0.1 \
  --format '{{range .RepoDigests}}{{println .}}{{end}}'
~~~

**Command overview:** Downloads the official versioned image and prints its repository digest. Verify the tag and approve the digest before proceeding. Use the complete `docker.io/zeek/zeek@sha256:...` reference from that check for the next step.

### Step 13 — Run Zeek offline against the synthetic PCAP

~~~bash
read -r -p 'Approved Zeek image reference including digest: ' ZEEK_IMAGE
podman run --rm --pull=never --network none --cap-drop=all \
  -v "$HOME/network-lab/private-pcaps:/pcaps:ro,Z" \
  -v "$HOME/network-lab/zeek-out:/out:Z" \
  -w /out \
  "$ZEEK_IMAGE" \
  zeek -r /pcaps/lab-dns.pcap LogAscii::use_json=T
~~~

**Command overview:** Uses a network-disabled container to read the private PCAP, writing Zeek JSON logs under `zeek-out`. If the image has a different entrypoint/command convention, review its documented usage instead of guessing. On SELinux-enforcing hosts, verify reviewed bind mount labels.

**Expected:** At least a `conn.log` or `dns.log` with synthetic traffic; a single UDP DNS query may not generate every possible protocol log.

### Step 14 — Verify Zeek output and metadata

~~~bash
find "$HOME/network-lab/zeek-out" -maxdepth 1 -name '*.log' -type f -print
python3 scripts/network-defense/summarize_network_logs.py \
  "$HOME/network-lab/zeek-out/dns.log" --type zeek
~~~

**Command overview:** Lists output logs and summarizes newline-delimited JSON records locally. Do not open raw customer DNS questions in public tools. If no logs exist, review container process status, input PCAP and command.

### Step 15 — Plan live Zeek monitoring only after packet mirroring is proven

A dedicated switch port mirror/TAP or approved VMware vSwitch mirror is required for network-wide capture. **VMnet8 NAT does not guarantee this**. Verify both directions with a benign known-flow test and record visibility/loss metrics. Do not set Zeek to actively transmit, capture unapproved networks or add an inline interface.

## Phase 4 — Suricata IDS and triage

### Step 16 — Review RHEL 10 Suricata packaging (RHEL-SENSOR01)

On the optional sensor, use the [RHEL package setup and offline service check](SURICATA.md#package-installation) after approving the EPEL and OISF sources. On an existing analysis workstation, use the [worked case's analysis setup](OFFLINE_HTTP_WALKTHROUGH.md#1-set-up-an-analysis-workspace).

### Step 17 — Validate the Suricata configuration and rules

~~~bash
suricata -T -c /etc/suricata/suricata.yaml \
  -S "$PWD/configs/network-defense/suricata/local.rules" \
  -l "$HOME/network-lab/suricata-out"
~~~

**Command overview:** `-T` tests the YAML and `-S` selects the repository's single fixture rule. Run from the repository root and verify that one rule loads. Use [Suricata rule updates](SURICATA.md#configuration-and-existing-rule-sources) separately for an approved operational ruleset.

### Step 18 — Analyze the same synthetic PCAP with passive Suricata

~~~bash
suricata -r "$HOME/network-lab/private-pcaps/lab-dns.pcap" \
  -c /etc/suricata/suricata.yaml \
  -S "$PWD/configs/network-defense/suricata/local.rules" \
  --set unix-command.enabled=no \
  -l "$HOME/network-lab/suricata-out"
~~~

**Command overview:** Runs Suricata in **offline read-only PCAP mode**. It produces IDS metadata/EVE logs but does not block traffic. If the package's runtime identity cannot write into the chosen private directory, use a reviewed owner/group change, not global `chmod 777`.

### Step 19 — Inspect and tune IDS alert content

~~~bash
python3 scripts/network-defense/summarize_network_logs.py \
  "$HOME/network-lab/suricata-out/eve.json" --type suricata
~~~

The offline replay should emit one alert with SID `1000001`. Check the actual EVE output for `event_type`, `alert.signature_id`, source and destination, protocol, and timestamps. Repeat in a fresh output directory to avoid mixing runs. Use the [worked case](OFFLINE_HTTP_WALKTHROUGH.md#5-test-and-tune-the-suricata-rule) for a positive and negative control and a comparison of broad and narrow rules.

### Step 20 — Compare Zeek metadata with Suricata observations

Correlate PCAP SHA-256, time, IPs, port/protocol, DNS query and any rule alerts. Explain missing differences: Zeek generates protocol logs while Suricata may emit flow/DNS and selected alerts depending on configuration/rules. Log that a real sensor may miss packets. No false positive or performance claim before actual tests.

## Phase 5 — YARA file classification and Sigma-to-Splunk rules

### Step 21 — Install a supported YARA engine for **file-only** testing

On RHEL, first check available approved packages:

~~~bash
sudo dnf info yara || true
command -v yara || true
~~~

If an approved package exists, install it with `sudo dnf install -y yara`. Otherwise use the YARA CLI package on **Ubuntu WSL** as shown in the [analysis setup](OFFLINE_HTTP_WALKTHROUGH.md#1-set-up-an-analysis-workspace). Record the engine version and package source.

### Step 22 — Test a harmless YARA marker rule

The repository includes [lab_marker.yar](../../rules/yara/lab_marker.yar) with an exact benign text marker. On a host with the approved `yara` CLI:

~~~bash
printf 'LAB_NETWORK_DEFENSE_FIXTURE\n' \
  > "$HOME/network-lab/yara-test/harmless.txt"
yara rules/yara/lab_marker.yar \
  "$HOME/network-lab/yara-test/harmless.txt"
~~~

**Command overview:** Writes a harmless local text sample and scans it against a project-owned marker rule. A positive match only proves the test rule matched known fixture bytes; it does **not** prove malware detection.

### Step 23 — Install Sigma CLI on WSL in an isolated environment

~~~bash
python3 -m venv "$HOME/.venvs/sigma-lab"
"$HOME/.venvs/sigma-lab/bin/python" -m pip install --upgrade pip
"$HOME/.venvs/sigma-lab/bin/python" -m pip install sigma-cli
"$HOME/.venvs/sigma-lab/bin/sigma" plugin list
"$HOME/.venvs/sigma-lab/bin/sigma" plugin install splunk
~~~

**Command overview:** Creates an isolated Python environment, installs Sigma CLI, lists plugins and installs its Splunk conversion backend. Pin versions and retain package hashes before operational use.

### Step 24 — Convert and review the sample Sigma rule

~~~bash
"$HOME/.venvs/sigma-lab/bin/sigma" convert \
  -t splunk --without-pipeline \
  rules/sigma/lab_network_dns_marker.yml
~~~

**Command overview:** Converts the fixture rule against Zeek's native JSON `query` field. In Splunk, scope the result to the expected Zeek source and capture window. See [Sigma mapping and validation](YARA_AND_SIGMA.md) and the [Windows process control](OFFLINE_HTTP_WALKTHROUGH.md#7-convert-a-separate-sysmon-sigma-control-to-spl) for distinct mappings.

## Phase 6 — Splunk ingestion, baseline and investigations

### Step 25 — Prepare optional Splunk indexes (RHEL-SPLUNK01, reviewer approval)

Proposed new indexes: `net_zeek`, `net_suricata`, `net_yara`. Review [index examples](../../configs/network-defense/splunk/indexes.conf.example), storage, retention, RBAC and your existing app configuration. Merge only reviewed stanzas into the appropriate local `indexes.conf`; do **not** overwrite original six indexes or delete data. Check `splunk btool indexes list --debug` and storage permissions after application.

### Step 26 — Set up verified TLS forwarding from the optional sensor

Install a version-compatible Splunk Universal Forwarder **from the vendor's verified installer** on RHEL-SENSOR01 according to [Splunk's forwarder documentation](https://help.splunk.com/en/splunk-enterprise/forward-and-process-data). Source files under [SENSOR_UF](../../apps/SENSOR_UF/local/inputs.conf) are **examples**, not installed configs. Review cert chain, `sslVerifyServerCert=true`, server name, outputs to `splunk01.lab.test:9997`, and firewall allowlist for `172.25.250.40/32`; the existing firewall may only allow WINHUNT01. Validate `/opt/splunkforwarder/bin/splunk btool outputs list --debug` and avoid embedding private keys or credentials in the repo.

### Step 27 — Safely ingest JSON telemetry and validate timestamps

Only approved **sanitized newline JSON** from designated paths may be indexed, not PCAP binaries or raw extracted files. Review [Splunk ingestion](SPLUNK_INTEGRATION.md). Test actual parsing and timestamp extraction (Zeek epoch fractions vs Suricata ISO 8601) with one test event. A default `_json` sourcetype and index-time ingestion timestamps may be inadequate for historical PCAP analysis—verify `_time` against `ts` / `timestamp`.

Test SPL after ingestion:

~~~spl
(index=net_zeek OR index=net_suricata OR index=net_yara) earliest=-24h
| stats count by index sourcetype host
~~~

**Command overview:** Counts actual indexed network-security events by source. An empty result is a debugging signal, not an installation success.

### Step 28 — Develop a normal-traffic baseline and passive findings

See [detection workflow](DETECTIONS_AND_TESTING.md) and [sample hunts](../../hunts/network-defense/README.md). Capture owner-approved daily protocol flow counts, unique DNS domains, destinations, ports, Suricata alert rates and data gaps. Review unexpected cleartext services, weak TLS, new connections and outlier flows. Validate potential vulnerabilities with authorized owners; passive metadata cannot confirm every CVE, patch level, exploit or asset criticality.

## Phase 7 — Governance, evidence and rollback

### Step 29 — Document incident workflow and CMMC Level 2 evidence

Read [CMMC Level 2 mapping](CMMC_LEVEL2.md) and [CONOPS](CONOPS.md). Map approved event collection, access logs, response process, risk assessments, incident documentation and monitoring to **select** NIST SP 800-171 Rev 2 requirements in the CMMC model. The map is illustrative: it does not demonstrate all 110 requirements. This synthetic lab has **no CUI** and no CMMC certification/assessment result.

Update [validation evidence](../../evidence/sanitized/network-defense-validation.md) with actual run ID, product versions, source hash, expected vs observed, reviewer, limitations, false positives and private evidence location. Keep unperformed items marked **Pending**.

### Step 30 — Run repository tests, verify functionality and plan ongoing review

From Ubuntu WSL in the repository:

~~~bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_project.py
python3 tools/publication_preflight.py
git diff --check
~~~

**Command overview:** Checks code/fixtures, source structure, public-release safety and whitespace. GitHub Actions runs source checks for Linux and Windows. These checks do **not** install sensors, prove IDS alert performance, or certify CMMC.

**Rollback:** Remove only the optional sensor log sources/index permissions/configuration added under approved change control. Preserve the three existing lab VMs, original six indexes, keys, Splunk services, IdM DNS and Windows forwarding. For failures, revert the precise change or restore the verified snapshot from VMware console; never disable Selinux/TLS protections or flush all firewall rules to “make it work.”

## Final acceptance checklist

| Milestone | Acceptance evidence | Initial status |
| --- | --- | --- |
| Sensor architecture/CONOPS | Owner-approved scope, VM snapshot and packet source | Pending |
| Wireshark/TShark | Synthetic DNS packet accurately decoded | Pending |
| Zeek | Expected local JSON event(s) from the synthetic PCAP | Pending |
| Suricata | Validated config and inspected EVE event(s) | Pending |
| YARA | Fixture-only match + no match on control sample | Pending |
| Sigma | Splunk backend conversion + mapping review | Pending |
| Splunk | Reviewed new indexes and verified certificate and timestamps | Pending |
| Baseline | Known-good period, outliers, measurement limits | Pending |
| Reporting | Incident notes, false-positive review, root cause/owner feedback | Pending |
| CMMC | Sample evidence mapping only, no certification claim | Documentation only |

## References

[Official guidance](REFERENCES.md) | [CONOPS](CONOPS.md) | [Architecture](ARCHITECTURE.md) | [Zeek/TShark](ZEEK_AND_WIRESHARK.md) | [Suricata](SURICATA.md) | [YARA/Sigma](YARA_AND_SIGMA.md) | [CMMC](CMMC_LEVEL2.md)
