#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo inside RHEL-SPLUNK01.' >&2; exit 1; }
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
APP_LOCAL=/opt/splunk/etc/apps/LAB_SIEM/local
[[ -x /opt/splunk/bin/splunk && -f "$APP_LOCAL/indexes.conf" ]] || {
    echo 'Deploy the LAB_SIEM app and lab index first.' >&2; exit 1;
}
id splunk >/dev/null
systemctl is-active --quiet Splunkd
python3 "$PROJECT_ROOT/scripts/merge_redaction_config.py" --target-dir "$APP_LOCAL"
python3 "$PROJECT_ROOT/scripts/merge_redaction_config.py" --target-dir "$APP_LOCAL" --apply
install -d -m 0750 -o root -g splunk /var/log/siem-lab
if [[ ! -e /var/log/siem-lab/identity.log ]]; then
    install -m 0640 -o root -g splunk /dev/null /var/log/siem-lab/identity.log
fi
[[ -f /var/log/siem-lab/identity.log && ! -L /var/log/siem-lab/identity.log ]] || {
    echo 'identity.log must be a regular file, not a symlink.' >&2; exit 1;
}
chown root:splunk /var/log/siem-lab/identity.log
chmod 0640 /var/log/siem-lab/identity.log
restorecon -v "$APP_LOCAL/inputs.conf" "$APP_LOCAL/props.conf" /var/log/siem-lab/identity.log
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool props list identity --debug
sudo -u splunk /opt/splunk/bin/splunk btool inputs list 'monitor:///var/log/siem-lab/identity.log' --debug
systemctl restart Splunkd
systemctl is-active --quiet Splunkd
echo 'Restart complete. Inspect btool output, then generate a new dummy marker and search its stored _raw.'
