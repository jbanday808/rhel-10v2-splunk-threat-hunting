#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo inside RHEL-SPLUNK01.' >&2; exit 1; }
LOG_FILE=/var/log/siem-lab/identity.log
[[ -f "$LOG_FILE" && ! -L "$LOG_FILE" ]] || {
    echo 'Run install-redaction-lab.sh first.' >&2; exit 1;
}
systemctl is-active --quiet Splunkd
STAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TEST_ID="SIEM-LAB-REDACTION-$(date -u +%Y%m%dT%H%M%SZ)-$$"
printf '%s action=redaction_check result=success account=labadmin password=LAB-DUMMY-ONE password=LAB-DUMMY-TWO test_id=%s\n' \
    "$STAMP" "$TEST_ID" >> "$LOG_FILE"
printf 'Search for this fresh test ID: %s\n' "$TEST_ID"
