# Kali network analysis workstation — Wireshark, Zeek, Suricata, Arkime, YARA and Sigma

**Status:** Optional deployment procedure; no Kali installation, capture, rule hit or Arkime import has been verified by this repository. Run the checkpoints below and record actual results privately. The original three-VM Splunk lab remains unchanged.

This guide uses Kali on VMware Workstation as an **analysis workstation**. Wireshark inspects packets; Zeek records protocol activity; Suricata tests IDS rules; Arkime stores searchable sessions and packets; YARA classifies approved files; Sigma converts detection rules to queries. YARA and Sigma do **not** capture packets. All commands below run in a **Kali Bash terminal**, not Windows PowerShell.

## 1. Choose the capture path

| Lab system | Existing/example address | Role |
| --- | --- | --- |
| RHEL-SPLUNK01 | `172.25.250.10` | Splunk Enterprise; no change in this guide |
| WINHUNT01 | `172.25.250.20` | Windows/Sysmon/forwarder; no change |
| RHEL-IDM01 | `172.25.250.30` | IdM, DNS and LDAPS; no change |
| Kali VM | Verify an unused address on `172.25.250.0/24` | New optional analysis workstation |
| RHEL-SENSOR01 | `172.25.250.40`, proposed in the existing guides | **Alternative** optional RHEL sensor; do not assign its proposed address to Kali without checking |

Attach Kali's management NIC to the existing **VMnet8** only after checking VMware settings and address availability. Give the VM a separate capture NIC only when an authorized mirror/TAP feeds it. VMnet8 NAT is a switched network: promiscuous mode alone does not prove Kali can see WINHUNT01 ↔ Splunk or Splunk ↔ IdM unicast. Start with locally generated PCAPs; for real traffic, use a verified mirror/TAP or transfer an approved capture from the traffic owner. Do not bridge Kali inline, enable IPS/drop mode, or collect unrelated traffic. Read the [architecture](ARCHITECTURE.md) and [CONOPS](CONOPS.md).

**Suggested starting capacity:** 4 vCPU, 8 GB RAM and 80 GB free disk for the all-in-one synthetic exercise; 12–16 GB RAM and separate packet/database storage are more comfortable. These are planning estimates, not measured requirements. Arkime's database competes with the other tools for memory and disk. Snapshot Kali before installing.

## 2. Prepare Kali and the private workspace

### Step 1 — Confirm the VM and network

~~~bash
cat /etc/os-release
uname -m
free -h
df -h /
ip -br address
ip route get 172.25.250.10
getent ahostsv4 splunk01.lab.test
timedatectl
~~~

**Command Overview:** These read the OS, architecture, capacity, NIC, route, resolver and clock. **Summary:** Proceed only if Kali can use the intended lab route and has enough resources. Do not copy a proposed IP onto an existing VM. Time and name resolution matter when comparing packet and Splunk records.

### Step 2 — Install workstation tools from Kali repositories

First check `systemctl is-active suricata.service`. If an existing sensor is running, review its owner and configuration before following this new-workstation procedure.

~~~bash
sudo apt update
sudo apt install -y wireshark tshark tcpdump jq git openssl libcap2-bin \
  python3 python3-venv \
  suricata suricata-update yara docker.io docker-compose
sudo systemctl disable --now suricata.service
sudo systemctl enable --now docker
~~~

**Command Overview:** `apt` installs packaged tools; `systemctl` keeps Suricata's default live service stopped and starts Docker for the official Zeek and Arkime images. **Summary:** If `suricata-update` or `docker-compose` has a different package name on your Kali release, inspect `apt-cache policy PACKAGE` and install the available official Kali package. Do not mix Debian/Ubuntu repositories into Kali to fix a dependency. Kali's [Docker instructions](https://www.kali.org/docs/containers/installing-docker-on-kali/) identify `docker.io` as the container engine package.

~~~bash
wireshark --version | head -n 1
tshark --version | head -n 1
suricata -V
suricata-update --version
yara --version
sudo docker --version
sudo docker compose version
~~~

**Expected:** Each tool prints a version. If Compose is installed as a standalone command on your release, use `sudo docker-compose` wherever this guide says `sudo docker compose`. Do **not** add your everyday account to the `docker` group just to omit `sudo`; that group grants broad host privileges.

### Step 3 — Obtain the public examples and create private output folders

~~~bash
cd "$HOME"
REPO="$HOME/rhel-10v2-splunk-threat-hunting"
if [ -e "$REPO" ]; then
  echo 'Existing checkout: review its branch and changes before updating it.'
else
  git clone https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting.git "$REPO"
fi
LAB="$HOME/network-lab/kali"
umask 077
mkdir -p "$LAB"/{pcaps,zeek,suricata,yara,sigma,arkime}
git -C "$REPO" status --short
~~~

**Command Overview:** `git clone` gets the published examples; `umask 077` and `mkdir` create private folders. **Summary:** If the checkout already exists, inspect its local changes and use that path for `REPO`; do not clone over it. The `network-lab` directory is outside Git. Keep this same shell open so `REPO` and `LAB` remain set.

### Step 4 — Generate two harmless in-scope DNS packets

~~~bash
python3 "$REPO/scripts/network-defense/generate_synthetic_pcap.py" \
  --lab-addresses --timestamp "$(date -u +%s)" --output "$LAB/pcaps/short-dns.pcap"
python3 "$REPO/scripts/network-defense/generate_synthetic_pcap.py" \
  --lab-addresses --long-label --timestamp "$(date -u +%s)" \
  --output "$LAB/pcaps/long-dns.pcap"
sha256sum "$LAB/pcaps/"*.pcap
capinfos -c -a -e "$LAB/pcaps/"*.pcap
~~~

**Command Overview:** The script writes packet files only; `--lab-addresses` uses synthetic `172.25.250.20 → 172.25.250.30` DNS requests, and `--long-label` changes the first DNS label to 50 characters. `capinfos` checks packet counts and times. **Summary:** Each file should contain one packet. These addresses in a file do **not** mean the VMs sent the traffic.

## 3. Wireshark and TShark

### Step 5 — Inspect the offline packets

~~~bash
wireshark "$LAB/pcaps/long-dns.pcap"
tshark -n -r "$LAB/pcaps/short-dns.pcap" -Y dns \
  -T fields -e frame.number -e ip.src -e ip.dst -e dns.qry.name
tshark -n -r "$LAB/pcaps/long-dns.pcap" -Y dns \
  -T fields -e frame.number -e ip.src -e ip.dst -e dns.qry.name
~~~

**Command Overview:** `-r` reads a file, `-Y` filters decoded packets and `-e` selects output fields. **Summary:** In Wireshark use `dns` as the display filter. Confirm the same source, destination and different query lengths in both tools. An offline file needs no live capture permissions. [Wireshark/TShark documentation](https://www.wireshark.org/docs/man-pages/tshark.html).

### Step 6 — Prepare optional live capture permissions

~~~bash
sudo dpkg-reconfigure wireshark-common
sudo usermod -aG wireshark "$USER"
getcap "$(command -v dumpcap)"
~~~

Choose **Yes** when asked whether non-superusers may capture. Log out and back in, then check `id -nG` and `dumpcap -D`. **Summary:** These permissions allow a local user to capture on available interfaces; they do not create a mirror. If you only analyze files, skip this step. Capture only authorized traffic and store it outside the repository.

## 4. Zeek

### Step 7 — Install the official Zeek container

~~~bash
sudo docker pull zeek/zeek:lts
sudo docker run --rm zeek/zeek:lts zeek --version
sudo docker image inspect zeek/zeek:lts --format '{{index .RepoDigests 0}}'
~~~

**Command Overview:** `pull` downloads the official Debian-based Zeek image and `inspect` records its immutable digest for later repeatability. **Summary:** Zeek's Kali package has had dependency problems; use this supported container first. If `apt-cache policy zeek` and `sudo apt -s install zeek` succeed on your Kali version, a native `zeek` install is an optional alternative. Do not add an Ubuntu Zeek repository to Kali. [Zeek installation](https://docs.zeek.org/en/current/install.html).

### Step 8 — Analyze the same packets separately

~~~bash
mkdir -p "$LAB/zeek/short" "$LAB/zeek/long"
for sample in short long; do
  sudo docker run --rm --network none --cap-drop ALL \
    --mount "type=bind,src=$LAB/pcaps,dst=/input,readonly" \
    --mount "type=bind,src=$LAB/zeek/$sample,dst=/out" \
    -w /out zeek/zeek:lts \
    zeek -r "/input/$sample-dns.pcap" LogAscii::use_json=T
done
sudo chown -R "$USER:$USER" "$LAB/zeek"
jq -c '{query, id_orig_h: ."id.orig_h", id_resp_h: ."id.resp_h"}' \
  "$LAB/zeek/short/dns.log"
~~~

**Command Overview:** `-r` reads a PCAP without sending traffic; each run writes JSON logs to a separate folder. **Summary:** Look for a DNS query and source/destination in `dns.log`; also inspect `conn.log` if present. A single request has no DNS response, so response fields may be empty. If no DNS log exists, check container errors and the one-packet capture before drawing conclusions. [Zeek offline invocation](https://docs.zeek.org/en/current/tutorial/invoking-zeek.html).

## 5. Suricata custom-rule validation

### Step 9 — Inspect the rules and confirm the Kali configuration

~~~bash
grep '^alert ' "$REPO/configs/network-defense/suricata/passive-review.rules.example"
grep -nE 'eve-log:|filename: eve.json' /etc/suricata/suricata.yaml
mkdir -p "$LAB/suricata"/{check,short,long,marker}
suricata -T -c /etc/suricata/suricata.yaml \
  -S "$REPO/configs/network-defense/suricata/passive-review.rules.example" \
  -l "$LAB/suricata/check"
~~~

**Command Overview:** `-T` checks that Kali's Suricata can load the eight opt-in rules; `-S` selects that test file, and `-l` places output in the private folder. **Summary:** Stop if rule loading fails. All eight example headers use `172.25.250.0/24`. Check that the package's EVE JSON output is enabled before interpreting an empty log. Do not copy the example into a live rules directory merely to test it.

### Step 10 — Compare a matching and nonmatching DNS file

~~~bash
for sample in short long; do
  suricata -r "$LAB/pcaps/$sample-dns.pcap" \
    -c /etc/suricata/suricata.yaml \
    -S "$REPO/configs/network-defense/suricata/passive-review.rules.example" \
    -l "$LAB/suricata/$sample" || break
  test -s "$LAB/suricata/$sample/eve.json" || break
  printf '%s: ' "$sample"
  jq -r 'select(.event_type=="alert") | .alert.signature_id' \
    "$LAB/suricata/$sample/eve.json"
done
~~~

**Command Overview:** `-r` analyzes saved packets; `jq` prints alert SIDs. **Expected, subject to your actual run:** No `1002001` from the short first label and one `1002001` from the 50-character first label. Confirm Suricata decoded DNS events as well; absence of an alert without packet processing is not a valid negative control. Other SIDs require their own positive/negative HTTP, TLS, SMB or RDP PCAPs. See [all eight rule meanings and controls](../../configs/network-defense/suricata/README.md).

### Step 11 — Check the separate benign marker rule

~~~bash
suricata -T -c /etc/suricata/suricata.yaml \
  -S "$REPO/configs/network-defense/suricata/local.rules" \
  -l "$LAB/suricata/marker"
suricata -r "$LAB/pcaps/short-dns.pcap" \
  -c /etc/suricata/suricata.yaml \
  -S "$REPO/configs/network-defense/suricata/local.rules" \
  -l "$LAB/suricata/marker"
jq -r 'select(.event_type=="alert") | .alert.signature_id' \
  "$LAB/suricata/marker/eve.json"
~~~

**Expected:** SID `1000001` for the harmless `lab-marker.example.test` query. Use a fresh output folder for each repeat. For an operational ruleset, `sudo suricata-update` obtains and maintains ET Open rules; first review feeds and run `suricata -T`, then separately authorize the interface and service. This lab test needs no rule download. [Suricata rule management](https://docs.suricata.io/en/latest/rule-management/suricata-update.html).

## 6. Arkime with OpenSearch on Kali — synthetic offline evaluation

Arkime does not publish a Kali-native package in its [supported distribution instructions](https://arkime.com/install); its [official container image](https://arkime.com/docker) is the practical Kali route. The repository's [RHEL Arkime guide](../arkime/IMPLEMENTATION_GUIDE.md) remains the separate, hardened sensor path. The Compose example below uses **OpenSearch with its security plugin disabled** on a Docker-only network and binds Viewer to Kali loopback. It is for **synthetic, single-user data only**. Do not import real captures or expose it to a shared network; move to authenticated TLS, restricted accounts, storage/retention controls and an approved capture architecture first.

### Step 12 — Prepare Docker resources and the example

~~~bash
cat /proc/sys/vm/max_map_count
if [ "$(cat /proc/sys/vm/max_map_count)" -lt 262144 ]; then
  if [ -e /etc/sysctl.d/99-kali-arkime-lab.conf ]; then
    echo 'Review the existing sysctl file before continuing.'
  else
    printf '%s\n' 'vm.max_map_count=262144' |
      sudo tee /etc/sysctl.d/99-kali-arkime-lab.conf
    sudo sysctl -p /etc/sysctl.d/99-kali-arkime-lab.conf
  fi
fi
if [ -e "$LAB/arkime/docker-compose.yaml" ]; then
  echo 'Review the existing Compose file before continuing.'
else
  cp "$REPO/configs/network-defense/arkime/kali-offline-compose.yaml.example" \
    "$LAB/arkime/docker-compose.yaml"
fi
~~~

**Command Overview:** `vm.max_map_count` permits OpenSearch's memory maps; `cp` copies the **example** outside Git. **Summary:** Stop and review an existing sysctl or Compose file instead of overwriting it. Confirm the resulting value is at least `262144` before starting OpenSearch. [OpenSearch Docker settings](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/).

### Step 13 — Create a local Arkime configuration and distinct secret

~~~bash
if [ -e "$LAB/arkime/config.ini" ]; then
  echo 'Review the existing private Arkime config before continuing.'
else
  ARKIME_SECRET="$(openssl rand -hex 32)"
  umask 077
  cat > "$LAB/arkime/config.ini" <<EOF
[default]
elasticsearch=http://opensearch:9200
passwordSecret=$ARKIME_SECRET
authMode=digest
interface=lo
pcapDir=/opt/arkime/raw
viewHost=0.0.0.0
viewPort=8005
EOF
  unset ARKIME_SECRET
  chmod 0600 "$LAB/arkime/config.ini"
fi
cd "$LAB/arkime"
sudo docker compose config --quiet
~~~

**Command Overview:** `openssl rand` makes a unique user-password encryption secret; the private INI config is mounted into the container. `viewHost=0.0.0.0` is **inside** Docker; Compose publishes only `127.0.0.1:8005` on Kali. **Summary:** Never commit `config.ini` or change its secret after creating Arkime accounts. For a later reuse, review the existing file instead of replacing it. The Compose config command checks syntax, not database health.

### Step 14 — Start and verify only OpenSearch

~~~bash
sudo docker compose pull
sudo docker compose up -d opensearch
sudo docker compose ps
sudo docker compose exec opensearch curl -fsS http://localhost:9200/
~~~

**Command Overview:** `pull` gets the two pinned images; `up` starts only the database; `curl` checks the local container endpoint. **Summary:** Do not continue if the database is unhealthy. It has **no host port 9200 mapping**. If startup fails, use `sudo docker compose logs opensearch` and check memory, disk and `vm.max_map_count`. [Arkime 6/OpenSearch 3 compatibility](https://github.com/arkime/arkime/blob/main/CHANGELOG).

### Step 15 — Initialize this new, disposable Arkime database once

~~~bash
sudo docker compose run --rm --no-deps viewer \
  /opt/arkime/db/db.pl http://opensearch:9200 init --ism
~~~

**Command Overview:** `db.pl init` creates Arkime's indexes in this newly created OpenSearch volume. **Summary:** This operation can erase existing Arkime indexes. Do it **only once** on the confirmed new disposable lab volume; never use it to repair an existing database. Follow vendor upgrade/backup instructions for any existing data. If the command asks for confirmation, read the target before answering.

### Step 16 — Create an Arkime administrator without a password argument

~~~bash
sudo docker compose run --rm --no-deps viewer \
  /opt/arkime/bin/arkime_add_user.sh arkimeadmin 'Lab Administrator' - --admin
~~~

**Command Overview:** The `-` asks for the password interactively; `--admin` is for the one setup account. **Summary:** Use a unique password and store it privately. This is a separate Arkime account, not a Splunk or Kali user. If your Compose version does not allocate a terminal, add `--interactive --tty` to `run`.

### Step 17 — Start Viewer, inspect its bind and sign in

~~~bash
sudo docker compose up -d viewer
sudo docker compose ps
sudo docker compose logs --tail=80 viewer
ss -lnt | grep ':8005'
~~~

**Expected:** Viewer runs and host port 8005 listens only on `127.0.0.1`. Open `http://127.0.0.1:8005` **inside Kali**, sign in as `arkimeadmin` and inspect the empty Sessions view. Digest authentication is over HTTP on local loopback only; do not expose this port on VMnet8. The DB and packet store are Docker volumes and persist across `docker compose down`.

### Step 18 — Import the two saved PCAPs, without live capture

~~~bash
sudo docker compose run --rm --no-deps viewer \
  /opt/arkime/bin/capture -c /opt/arkime/etc/config.ini \
  -n kaliarkime --copy -r /input/short-dns.pcap
sudo docker compose run --rm --no-deps viewer \
  /opt/arkime/bin/capture -c /opt/arkime/etc/config.ini \
  -n kaliarkime --copy -r /input/long-dns.pcap
sudo docker compose logs --tail=80 viewer
~~~

**Command Overview:** `-r` imports a PCAP; `--copy` keeps Arkime-managed packet data in its volume, and `-n` matches the Viewer's `kaliarkime` node name. The original files are read-only in the container. **Summary:** Set the Viewer time range to the generated UTC timestamps; look for the two DNS requests and verify packet retrieval. If a one-packet flow is not useful, generate and import the repository's complete [HTTP baseline/investigation PCAPs](../arkime/IMPLEMENTATION_GUIDE.md#phase-4--generate-and-import-safe-test-traffic). A successful offline import never proves that Kali sees peer-to-peer live traffic. [Arkime PCAP import](https://arkime.com/faq#how-do-i-import-existing-pcaps).

### Step 19 — Stop the lab without deleting data

~~~bash
sudo docker compose down
~~~

**Command Overview:** Stops the containers. **Summary:** Do **not** use `down -v` unless you deliberately want to erase the OpenSearch and Arkime PCAP volumes after a verified export/retention decision. Database metadata and packets have separate lifecycles; disk capacity and retention need review before any ongoing use.

## 7. YARA — match approved local files

### Step 20 — Test a benign marker and negative control

~~~bash
printf 'LAB_NETWORK_DEFENSE_FIXTURE\n' > "$LAB/yara/marker.txt"
printf 'Ordinary benign note\n' > "$LAB/yara/control.txt"
yarac "$REPO/rules/yara/lab_marker.yar" "$LAB/yara/lab_marker.yarac"
yara "$REPO/rules/yara/lab_marker.yar" "$LAB/yara/marker.txt"
yara "$REPO/rules/yara/lab_marker.yar" "$LAB/yara/control.txt"
~~~

**Command Overview:** `yarac` compiles the example rule; `yara` checks each file's bytes. **Expected:** `LAB_Network_Defense_Fixture` matches only `marker.txt`. The rule is a test marker, not malware attribution. For a packet-derived file, export an authorized HTTP object to private storage in Wireshark/TShark, hash it and scan that **file**. YARA does not inspect a network interface by itself. [YARA CLI](https://yara.readthedocs.io/en/stable/commandline.html).

## 8. Sigma — convert a detection rule for Splunk

### Step 21 — Install Sigma and its Splunk backend in an isolated environment

~~~bash
python3 -m venv "$LAB/sigma/venv"
"$LAB/sigma/venv/bin/python" -m pip install --upgrade pip
"$LAB/sigma/venv/bin/python" -m pip install sigma-cli pysigma-backend-splunk
"$LAB/sigma/venv/bin/sigma" version
"$LAB/sigma/venv/bin/sigma" list targets
~~~

**Command Overview:** `venv` keeps Python packages out of Kali's system interpreter; `pip` installs Sigma and the Splunk converter together. **Summary:** Record exact versions and package source before long-term reuse; Sigma plugins and field mappings change. [Sigma installation and plugins](https://sigmahq.io/docs/guide/getting-started).

### Step 22 — Convert and review the benign DNS rule

~~~bash
"$LAB/sigma/venv/bin/sigma" convert -t splunk --without-pipeline \
  "$REPO/rules/sigma/lab_network_dns_marker.yml" \
  > "$LAB/sigma/lab-network-dns.spl"
cat "$LAB/sigma/lab-network-dns.spl"
~~~

**Command Overview:** The YAML describes a Zeek DNS `query` value; the backend writes a candidate SPL expression. **Summary:** Confirm the output uses `query="lab-marker.example.test"` and inspect its syntax before adding a **verified** `index=...`, `sourcetype=...` and time range. The existing six indexes have **no automatically deployed Zeek feed**; optional `net_zeek`/`net_suricata` indexes in other guides are only proposals. Sigma conversion is not a working Splunk alert. A Sysmon Sigma rule requires the separate Windows mapping and actual Windows ingestion.

## 9. Optional live passive collection — only after visibility is verified

### Step 23 — Prove the capture point

Document the interface, packet source, expected client/server addresses, timestamp, permitted duration and storage owner. Confirm a mirror/TAP supplies **both directions** of a known test flow from two other lab systems. Without it, a Kali VM can still analyze its **own** traffic and imported files; absence of peer traffic is a capture limitation, not evidence of no activity. Keep full PCAPs and any credential-bearing HTTP payload private.

### Step 24 — Record a short approved sample

After confirming `id -nG` includes `wireshark`, inspect `dumpcap -D` and substitute the **actual** mirrored interface:

~~~bash
SENSOR_IF='REPLACE_WITH_VERIFIED_MIRROR_INTERFACE'
dumpcap -i "$SENSOR_IF" -f 'net 172.25.250.0/24' \
  -a duration:60 -w "$LAB/pcaps/approved-live.pcapng"
capinfos -c -a -e "$LAB/pcaps/approved-live.pcapng"
tshark -n -r "$LAB/pcaps/approved-live.pcapng" \
  -Y 'ip.addr == 172.25.250.20 && ip.addr == 172.25.250.10' \
  -T fields -e ip.src -e ip.dst -e tcp.port
~~~

**Command Overview:** `-f` filters during collection; `-a duration:60` bounds it; `-Y` checks the saved file. **Summary:** Verify known traffic and its reverse direction, packet counts and drops. An empty result means stop and investigate the mirror, filter and traffic generation. For Arkime, convert a permitted `pcapng` to `pcap` using `tshark -r INPUT.pcapng -F pcap -w OUTPUT.pcap` and import it only after replacing the disposable database setup with an approved authenticated deployment. Do not import real traffic into the Step 12–19 evaluation stack.

### Step 25 — Deploy a live IDS/metadata sensor only after review

For an approved **manual** live test on the verified mirror, run Zeek in one terminal:

~~~bash
mkdir -p "$LAB/zeek/live"
sudo docker run --rm --network host --cap-add NET_RAW --cap-add NET_ADMIN \
  --mount "type=bind,src=$LAB/zeek/live,dst=/out" -w /out \
  zeek/zeek:lts zeek -C -i "$SENSOR_IF" LogAscii::use_json=T
~~~

Stop with Ctrl+C at the approved end time; check `conn.log` and any protocol logs against the bounded Wireshark PCAP. The container's output may need `sudo chown -R "$USER:$USER" "$LAB/zeek/live"` before analyst review.

In a **separate** terminal, check the Suricata configuration and run the reviewed rules in passive IDS mode:

~~~bash
mkdir -p "$LAB/suricata/live"
sudo suricata -T -c /etc/suricata/suricata.yaml \
  -S "$REPO/configs/network-defense/suricata/passive-review.rules.example" \
  -l "$LAB/suricata/live"
sudo suricata -i "$SENSOR_IF" -c /etc/suricata/suricata.yaml \
  -S "$REPO/configs/network-defense/suricata/passive-review.rules.example" \
  -l "$LAB/suricata/live"
~~~

Stop with Ctrl+C at the approved end time, then inspect `eve.json` for flows, protocol records and alerts. **Command Overview:** Zeek and Suricata read the same mirrored interface independently; `-i` selects it, while `-S` loads only the reviewed optional rules. **Summary:** A loaded rule does not imply a match; verify capture and protocol decoding first. Keep Suricata alert-only; do not configure NFQUEUE/IPS or drops.

For an approved **persistent** feed, define interface/direction, start/stop procedure, time sync, rule sources, baseline, storage budget and alert owner first. Follow the [Zeek deployment](ZEEK_DEPLOYMENT.md), [Suricata validation](SURICATA.md) and [hardened Arkime sensor](../arkime/IMPLEMENTATION_GUIDE.md) for durable services and retention. Any future Splunk forwarding needs its own TLS, parser, index and timestamp checks; no feed is created by this guide.

## 10. Acceptance record and troubleshooting

| Checkpoint | Accept only after observing |
| --- | --- |
| Wireshark | Both known DNS PCAPs decode; source/destination and timestamp match |
| Zeek | DNS JSON for the same PCAP, with the expected query and addresses |
| Suricata | `-T` passes; decoded DNS exists; long-label SID `1002001`, short-label negative control, marker SID `1000001` |
| Arkime | Isolated database starts; Viewer bound to Kali loopback; two imported sessions are searchable and packets retrievable |
| YARA | Marker matches; clean control does not |
| Sigma | Splunk converter emits the expected `query` condition; any deployed SPL is separately checked against the real sourcetype |
| Live visibility | Known third-party test flows and reverse direction are actually present; drops/time drift are recorded |

If no Suricata alert: check the PCAP's addresses/first label with TShark, `suricata -T`, EVE configuration, actual `dns` events and the rule SID. If Zeek has no DNS log: inspect image exit status, mount paths, packet decoding and checksum/offload behavior. If Arkime has no session: inspect `docker compose logs`, the time picker, image/DB versions, PCAP format and matching node names. If Docker cannot start OpenSearch: inspect available RAM/disk, `vm.max_map_count` and container logs. If Sigma output differs: record versions, installed backend and actual Zeek/Splunk fields; do not copy a query directly into a scheduled alert.

**Rollback:** `sudo docker compose down` in the private Arkime folder stops those services; `sudo systemctl disable --now docker` stops Docker only if nothing else uses it. Keep or delete private PCAPs/logs according to your retention decision. Remove the Kali-only `/etc/sysctl.d/99-kali-arkime-lab.conf` only after comparing the current value and other software needs. Do not remove shared tools, destroy volumes or alter core Splunk/IdM/Windows settings as a routine rollback.

**References:** [Kali Wireshark packages](https://www.kali.org/tools/wireshark/) · [Kali Docker](https://www.kali.org/docs/containers/installing-docker-on-kali/) · [Zeek install](https://docs.zeek.org/en/current/install.html) · [Suricata rule management](https://docs.suricata.io/en/latest/rule-management/suricata-update.html) · [Arkime Docker](https://arkime.com/docker) · [Arkime import](https://arkime.com/faq#how-do-i-import-existing-pcaps) · [OpenSearch Docker](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/) · [YARA CLI](https://yara.readthedocs.io/en/stable/commandline.html) · [Sigma CLI](https://sigmahq.io/docs/guide/getting-started).
