#!/usr/bin/env bash
# Read the data integrity appendix first. This command does not repair buckets.
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo on RHEL-SPLUNK01.' >&2; exit 1; }
INTEGRITY_INDEX=${1:-lab}
[[ "$INTEGRITY_INDEX" == lab ]] || { echo 'This lab helper only checks the lab index.' >&2; exit 1; }
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug
echo 'Hashes must have existed when the selected data was indexed.'
read -r -p 'Type CHECK-LAB to stop Splunk briefly and check its local lab index: ' INTEGRITY_CONFIRM
[[ "$INTEGRITY_CONFIRM" == CHECK-LAB ]] || exit 1
systemctl is-active --quiet Splunkd
systemctl stop Splunkd
trap 'systemctl start Splunkd' EXIT
sudo -u splunk /opt/splunk/bin/splunk check-integrity -index lab -verbose
