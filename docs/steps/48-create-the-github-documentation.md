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
