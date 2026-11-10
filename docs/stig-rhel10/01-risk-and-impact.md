# 01 — RHEL 10 STIG Change-Risk and Dependency Assessment

**Targets:** RHEL-SPLUNK01 and RHEL-IDM01. **Source:** Uploaded V1R1 SCAP benchmark; specific rule numbers below were extracted from that exact XML, not guessed. All remediation and operational statuses are **Pending**.

## Special-risk rule families observed in the uploaded XML

| RHEL V1R1 STIG rule | Vulnerability ID | CAT | Review before changing |
| --- | --- | --- | --- |
| `RHEL-10-000500` | `V-281009` | I | **FIPS mode:** system crypto, SSH, Java/Splunk, TLS chains, IdM CA, Kerberos, reboot and deployment model |
| `RHEL-10-300040` | `V-281011` | I | **SSH server encryption:** supported algorithms and admin console recovery |
| `RHEL-10-200030` | `V-280945` | II | **gssproxy removal:** could break IdM/Kerberos service dependencies; investigate before uninstall |
| `RHEL-10-200642` | `V-280985` | II | **rsyslog TCP forwarding:** destinations, approved routing, authenticated transport and log leakage |
| `RHEL-10-200644` | `V-280987` | II | **rsyslog remote authentication:** trusted collector certificate, CA and logging continuity |
| `RHEL-10-700400` | `V-281249` | II | **SELinux targeted policy:** Splunk custom paths and service labels; preserve Enforcing |
| `RHEL-10-200530` | `V-280955` | II | **firewalld package:** review existing active network zones |
| `RHEL-10-200531` | `V-280956` | II | **firewalld service:** explicit 22, 8000, 9997, LDAPS/DNS/IdM dependencies |
| `RHEL-10-000560` | `V-280940` | II | **Separate /var/log mount:** existing disks, audit path, logrotate and boot dependencies |
| `RHEL-10-200541` | `V-280959` | II | **chronyd:** time source, Kerberos and certificate validity |
| `RHEL-10-200640` | `V-280983` | II | **rsyslog package:** local Splunk Linux logging |
| `RHEL-10-200641` | `V-280984` | II | **rsyslog service:** local and remote logs, Splunk inputs |
| `RHEL-10-600220` | `V-281181` | II | **Password minimum length:** IdM users vs local PAM, service/automation accounts |
| `RHEL-10-700970` | `V-280094` | II | **debug-shell service:** usually straightforward after service-state check |
| `RHEL-10-200020` | `V-280944` | I | **telnet-server prohibited:** check package and any dependencies |

**CAT indicates benchmark severity (high/medium/low)**, not a determination of actual risk in your environment. All 396 rules need host-specific review; this list highlights only selected higher-impact examples.

## Splunk-specific risk inventory

- **Index data:** `/splunkdata` must stay mounted with correct ownership and capacity; don't reformat disks or move indexes to satisfy mount rules casually.
- **Splunk Enterprise:** Installed as `splunk` user with systemd service; protect its files and custom configuration merge behavior.
- **Network:** TCP `8000` (Splunk Web), `9997` (TLS UF input), `8089` (local management; not exposed publicly) and outbound LDAPS `636` + DNS.
- **PKI:** Existing Splunk CA/private keys; new system crypto policies and FIPS rules may invalidate algorithms, signed chains or Java endpoints.
- **SELinux:** Keep Enforcing and investigate AVC denials rather than turning SELinux off. Paths under `/opt/splunk` and `/splunkdata` may have custom contexts.
- **Logs:** Audit, journald, rsyslog, systemd and existing forwarder pipelines can interact; verify ingestion after each change.
- **Disk partitions:** Benchmark rules for `/var`, `/var/log`, `/var/tmp`, `/tmp`, `/home` and `/var/log/audit` can require storage redesign; defer structural changes to planned maintenance/rebuild.

## IdM-specific risk inventory

- **Auth:** FreeIPA/IdM, LDAP/LDAPS, Kerberos, SSSD, directory groups, service credentials, internal CA and DNS. Never remove `gssproxy` blindly.
- **Network:** IdM service ports may include DNS, HTTP/HTTPS, LDAP/LDAPS, Kerberos, certificate authority/administration and NTP. Source restrictions require actual service inventory.
- **Time:** Kerberos authentication and TLS certificate validity depend on accurate chrony sync.
- **Crypto:** FIPS and host crypto policy changes can disrupt KDC algorithms or existing certs.
- **Database backups:** IdM stateful backup, CA data, restore rehearsal and intended VM snapshot semantics matter.
- **System user policy:** Differentiation between local PAM and centralized IdM account policies is required.

## Suggested risk gate before any remediation

| Field | Example |
| --- | --- |
| Host | RHEL-SPLUNK01 or RHEL-IDM01 |
| STIG rule and observed result | Exact `RHEL-10-...` and `fail` from private scan |
| Technical dependency | Named service, path, port, auth or application owner |
| Severity and impact | CAT plus observed actual service exposure |
| Approved remediation | Specific reviewed change command and expected state |
| Backout | Exact pre-change state, snapshot and restoration steps |
| Test | SCAP rule + DNS/TLS/Splunk/IdM functional regression |
| Reviewer | Actual human name/role stored privately |
| Status | Proposed → Approved → Implemented → Verified; never auto-advance |

**Stop conditions:** unexpected SSH or Splunk Web lockout; broken IdM sign-in; lost logs; SELinux denial impacting service; disk mount regression; unverified TLS; mass FIPS/crypto changes. Restore from the VM console using the documented recovery procedure.
