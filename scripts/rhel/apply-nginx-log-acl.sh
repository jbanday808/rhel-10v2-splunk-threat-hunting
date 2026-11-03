#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run this on RHEL-SPLUNK01 with sudo.' >&2; exit 1; }
id splunk >/dev/null
command -v setfacl >/dev/null
[[ -d /var/log/nginx ]] || { echo 'Install and start NGINX first.' >&2; exit 1; }
setfacl -m u:splunk:rx /var/log/nginx
setfacl -d -m u:splunk:rx /var/log/nginx
for log_file in /var/log/nginx/access.log /var/log/nginx/error.log; do
    [[ -f "$log_file" ]] && setfacl -m u:splunk:r "$log_file"
done
getfacl /var/log/nginx
echo 'Retest file reading as splunk and event arrival after log rotation.'
