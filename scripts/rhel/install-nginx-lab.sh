#!/usr/bin/env bash
# Dedicated loopback test server only. See the NGINX appendix before running.
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo on RHEL-SPLUNK01.' >&2; exit 1; }
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
APP_HOME=/opt/splunk/etc/apps/Splunk_TA_nginx
[[ -d "$APP_HOME/default" ]] || {
    echo 'Install the official Splunk Add-on for NGINX first.' >&2; exit 1;
}
id splunk >/dev/null
INPUT_SOURCE="$PROJECT_ROOT/apps/Splunk_TA_nginx/local/inputs.conf"
if [[ -f "$APP_HOME/local/inputs.conf" ]] &&
   ! cmp -s "$INPUT_SOURCE" "$APP_HOME/local/inputs.conf"; then
    echo 'Existing NGINX local inputs differ. Merge them manually using the guide.' >&2
    exit 2
fi
echo 'This replaces the NGINX server configuration with the loopback lab configuration.'
read -r -p 'Type NGINX-LAB to continue: ' NGINX_CONFIRM
[[ "$NGINX_CONFIRM" == NGINX-LAB ]] || exit 1
dnf install -y nginx acl curl
NGINX_BACKUP="/etc/nginx/nginx.conf.before-siem-$(date -u +%Y%m%dT%H%M%SZ)"
cp -a /etc/nginx/nginx.conf "$NGINX_BACKUP"
nginx -t -c "$PROJECT_ROOT/configs/nginx/nginx.conf"
install -o root -g root -m 644 "$PROJECT_ROOT/configs/nginx/nginx.conf" /etc/nginx/nginx.conf
restorecon -RF /etc/nginx /var/log/nginx
nginx -t
systemctl enable nginx
systemctl restart nginx
curl --fail --silent --show-error --user-agent SIEM-LAB-NGINX-TEST http://127.0.0.1/siem-lab
bash "$PROJECT_ROOT/scripts/rhel/apply-nginx-log-acl.sh"
install -d -o splunk -g splunk -m 750 "$APP_HOME/local"
install -o splunk -g splunk -m 640 "$INPUT_SOURCE" "$APP_HOME/local/inputs.conf"
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool inputs list 'monitor:///var/log/nginx/access.log' --debug
systemctl restart Splunkd
systemctl is-active Splunkd
curl --fail --silent --show-error --user-agent SIEM-LAB-NGINX-TEST http://127.0.0.1/siem-lab
printf 'NGINX backup: %s\nSearch Splunk using hunts/09-nginx-access.spl.\n' "$NGINX_BACKUP"
