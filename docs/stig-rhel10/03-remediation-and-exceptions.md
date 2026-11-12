# 03 — Controlled STIG Remediation, Verification and Exceptions

**Source:** DISA RHEL 10 STIG SCAP V1R1 provided by the user. **Policy:** One approved rule or minimal related change set at a time; no automatic mass remediation.

## Mandatory change prerequisites

- The host was scanned with the right benchmark and a complete profile.
- Actual `fail` (or documented manual deficiency) has a rule ID and named owner.
- Read the benchmark's full **check, discussion and fix text** for that exact rule, not just the title.
- Backup and tested VMware console recovery are available.
- Confirm effect on Splunk/IdM and **credential/TLS/SSH/service accounts**.
- Approve commands, working window, expected behavior, negative tests and rollback.
- Run after-change tests in the same window, then rescan.

## Example 1 — Debug shell service (RHEL-10-700970, V-280094)

Review whether `debug-shell.service` is present, active or enabled.

**Read-only inspection:**

```bash
systemctl is-enabled debug-shell.service || true
systemctl is-active debug-shell.service || true
```

**If the rule failed, service is unnecessary and owner approves**, apply on the VM console:

```bash
sudo systemctl mask --now debug-shell.service
systemctl is-enabled debug-shell.service
```

**Command overview:** `mask --now` blocks debug-shell from being started and stops it if currently active. Verify actual state; “not-found” is not necessarily a scanner error. This **one example is not proof of STIG compliance**.

**Recovery:** Restore its approved pre-change state only if needed, from the console and change record.

## Example 2 — Firewall enabled but existing flows must be preserved

Relevant rules include `RHEL-10-200530` / `V-280955` (package) and `RHEL-10-200531` / `V-280956` (active service).

```bash
rpm -q firewalld
sudo systemctl is-enabled firewalld
sudo systemctl is-active firewalld
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --zone=siem-lab --list-all
```

**Command overview:** Reads package/service/firewall status and the Splunk VM's `siem-lab` zone. Do **not** blindly apply or reset firewall rules. If a failure is observed, use the [zero-trust firewall safety runbook](../zero-trust/06-network-microsegmentation.md) and verify both allowed and blocked source traffic.

## Example 3 — FIPS mode requires a separate architecture plan

`RHEL-10-000500` / `V-281009` is **CAT I** in the uploaded benchmark.

**Read-only inspection (on each RHEL VM: RHEL-SPLUNK01 and RHEL-IDM01):**

```bash
cat /proc/sys/crypto/fips_enabled
update-crypto-policies --show
openssl version -a
```

**Command overview:** Run each command separately and retain its output and exit status. `cat` reads the running kernel's FIPS flag: `1` means enabled; `0` means disabled. The other commands report the selected system cryptographic policy and OpenSSL build/version information. These inspections do not change configuration and require no rollback. Do not suppress errors with `|| true`; a missing/unreadable flag or unexpected output makes the inspection inconclusive, not enabled or compliant.

**Validation boundary:** A flag value of `1`, a `FIPS` policy name, or OpenSSL version information does **not** independently establish FIPS 140 validation or STIG compliance. Review the relevant validated modules and their operating requirements, the exact benchmark check, and host-specific assessment evidence. Live scans, functional tests and compliance review remain **Pending** until performed and recorded; this documentation is not host validation or certification.

**RHEL 10 planning constraint:** [Red Hat's RHEL 10 FIPS guidance](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/security_hardening/switching-rhel-to-fips-mode) documents that `fips-mode-setup` was removed and enabling FIPS after installation is unsupported. If FIPS is required, plan a separately approved replacement VM installation with FIPS enabled during installation. Do **not** attempt an in-place conversion or change system cryptographic policy on an existing Splunk/IdM VM as a shortcut. Before any replacement or cutover, verify compatibility with the installed Splunk and IdM versions, relevant validated modules, TLS/SSH, credentials, keys, certificates and service accounts; require owner approval, private backups, tested console recovery, rollback and functional regression tests.

## Example 4 — Do not remove IdM packages based on one generic package rule

`RHEL-10-200030` / `V-280945` refers to `gssproxy` removal. On the **IdM VM**, inspect usage rather than immediately uninstalling:

```bash
rpm -q gssproxy
systemctl is-active gssproxy || true
rpm -q --whatrequires gssproxy || true
sudo ipactl status
```

**Command overview:** Checks package/service state, direct RPM requirements and IdM health. Requires dependency owner review; no package removal command is provided.

## Example 5 — rsyslog and audit protection

Relevant source rules include `RHEL-10-200640/641/642/644`. Existing syslog/remote forwarding choices can conflict with Splunk inputs. Investigate first:

```bash
rpm -q rsyslog audit
sudo systemctl is-active rsyslog auditd
sudo rsyslogd -N1
findmnt --mountpoint /var/log || true
findmnt --mountpoint /var/log/audit || true
```

**Command overview:** Checks installed packages, audit and logging services, validates rsyslog syntax, and inspects log mounts. Configure an authenticated approved collector and transport **only after** identifying real requirements; do not blindly send sensitive logs to arbitrary addresses.

## Example 6 — Filesystem separations and SELinux contexts

Requirements like `RHEL-10-000560` / `V-280940` may call for a separate `/var/log` filesystem. Inspect layout and determine whether a **future rebuild or planned storage migration** is required. Do **not** format a disk, move `/splunkdata`, or alter `/etc/fstab` blindly.

```bash
findmnt -R /var
findmnt --mountpoint /splunkdata || true
getenforce
sudo ausearch -m AVC -ts recent || true
```

**Command overview:** Reports mount hierarchy, Splunk data mount where applicable, SELinux status and recent access denials. Apply least-privilege SELinux policy corrections after interpreting actual AVCs, not by disabling enforcement.

## POA&M and exceptions

For any unresolved item, record `V-ID`, `SV-ID`, `RHEL-10-ID`, affected host, severity, observed test result, impact, change owner, compensating control, due date, status and approval decision. A risk decision must come from the **actual authorized decision maker**; a lab's student-facing POA&M does not grant an ATO or waive official requirements.

**Never run an arbitrary SCAP auto-fix, system-wide chmod/chown, disk formatter or SSH policy overwrite against the existing VMs without an approved, tested rollback. Do not attempt an in-place FIPS conversion on RHEL 10.**
