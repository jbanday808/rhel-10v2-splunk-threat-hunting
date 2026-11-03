#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$PROJECT_ROOT"

sudo systemctl show Splunkd -p User -p Group -p LimitNOFILE

findmnt --mountpoint /splunkdata

sudo ss -lntp

getenforce

sudo -u splunk /opt/splunk/bin/splunk btool inputs list --debug

sudo -u splunk /opt/splunk/bin/splunk btool indexes list --debug

sudo -u splunk /opt/splunk/bin/splunk btool props list siem:lab --debug

sudo -u splunk /opt/splunk/bin/splunk btool transforms list lab_fields --debug


curl --cacert /home/labadmin/siem-public/ca.pem \
  https://splunk01.lab.test:8000/en-US/account/login \
  -o /dev/null \
  -w '%{http_code}\n'
