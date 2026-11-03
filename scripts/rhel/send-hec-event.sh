#!/usr/bin/env bash
set -euo pipefail
# Run as labadmin on RHEL-SPLUNK01 after following the HEC appendix.
# Do not run with bash -x: tokens must not be traced.
HEC_URL=${HEC_URL:-https://172.25.250.10:8088/services/collector}
CA_FILE=${CA_FILE:-/home/labadmin/siem-public/ca.pem}
[[ "$HEC_URL" == https://* ]] || { echo 'HEC_URL must use HTTPS.' >&2; exit 1; }
[[ -r "$CA_FILE" ]] || { echo 'Verified public CA file is missing or unreadable.' >&2; exit 1; }
command -v curl >/dev/null
command -v python3 >/dev/null
umask 077
WORK_DIR=$(mktemp -d)
trap 'unset HEC_TOKEN; rm -rf -- "$WORK_DIR"' EXIT
read -r -s -p 'Paste the dedicated HEC token: ' HEC_TOKEN
printf '\n'
[[ "$HEC_TOKEN" =~ ^[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$ ]] || {
    echo 'Expected the GUID token value displayed by Splunk.' >&2; exit 1;
}
printf 'Authorization: Splunk %s\nContent-Type: application/json\n' "$HEC_TOKEN" > "$WORK_DIR/headers"
unset HEC_TOKEN
TEST_ID="SIEM-LAB-HEC-$(date -u +%Y%m%dT%H%M%SZ)-$$"
python3 - "$TEST_ID" > "$WORK_DIR/event.json" <<'PY'
import json
import sys
print(json.dumps({
    'index': 'lab', 'sourcetype': 'siem:hec', 'source': 'hec:siem-lab', 'host': 'splunk01',
    'event': 'action=hec_check result=success account=labadmin test_id=' + sys.argv[1]
}))
PY
printf 'Sending one dummy event with test ID: %s\n' "$TEST_ID"
curl --fail-with-body --silent --show-error \
    --connect-timeout 10 --max-time 30 \
    --cacert "$CA_FILE" \
    --header "@$WORK_DIR/headers" \
    --data-binary "@$WORK_DIR/event.json" \
    "$HEC_URL" > "$WORK_DIR/response.json"
python3 - "$WORK_DIR/response.json" <<'PY'
import json
import sys
from pathlib import Path
reply = json.loads(Path(sys.argv[1]).read_text())
if reply.get('code') != 0:
    raise SystemExit('HEC did not report success. Check the local response and server configuration.')
print('HEC returned code 0. Verify the exact test ID in Splunk Search to confirm indexing.')
PY
