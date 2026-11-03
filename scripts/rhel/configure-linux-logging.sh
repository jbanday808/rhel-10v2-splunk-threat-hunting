#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$PROJECT_ROOT"

cd "$HOME/rhel-splunk-threat-hunting"


cat > configs/rsyslog/30-siem-lab.conf <<'EOF'
if ($syslogfacility-text == "auth" or $syslogfacility-text == "authpriv" or $programname == "siem-lab") then {
    action(type="omfile"
        file="/var/log/siem-lab/linux.log"
        fileOwner="root"
        fileGroup="splunk"
        fileCreateMode="0640"
        template="RSYSLOG_TraditionalFileFormat")
}
EOF


cat > configs/logrotate/siem-lab <<'EOF'
/var/log/siem-lab/*.log {
    daily
    rotate 7
    missingok
    notifempty
    compress
    delaycompress
    create 0640 root splunk
    sharedscripts
    postrotate
        /usr/bin/systemctl kill -s HUP rsyslog.service >/dev/null 2>&1 || true
    endscript
}
EOF


sudo install -d -o root -g splunk -m 750 /var/log/siem-lab

sudo touch \
  /var/log/siem-lab/linux.log \
  /var/log/siem-lab/events.log

sudo chown root:splunk /var/log/siem-lab/*.log

sudo chmod 640 /var/log/siem-lab/*.log


sudo install -m 644 \
  configs/rsyslog/30-siem-lab.conf \
  /etc/rsyslog.d/30-siem-lab.conf

sudo install -m 644 \
  configs/logrotate/siem-lab \
  /etc/logrotate.d/siem-lab

sudo restorecon -RF /var/log/siem-lab

sudo rsyslogd -N1

sudo systemctl restart rsyslog

sudo logrotate --debug /etc/logrotate.d/siem-lab


logger -p authpriv.notice -t siem-lab \
  'SIEM-LAB-LINUX-PIPELINE-TEST'

printf '%s action=pipeline_check result=success account=labadmin\n' \
  "$(date -u +%FT%TZ)" \
  | sudo tee -a /var/log/siem-lab/events.log
