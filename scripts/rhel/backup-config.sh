#!/usr/bin/env bash
set -euo pipefail

[[ $EUID -eq 0 ]] || {
  echo 'Run with sudo.' >&2
  exit 1
}

umask 077

install -d -m 700 /var/backups/siem-lab

BACKUP_FILE="/var/backups/siem-lab/splunk-etc-$(date -u +%Y%m%dT%H%M%SZ).tar.gz"

systemctl is-active --quiet Splunkd
systemctl stop Splunkd

trap 'systemctl start Splunkd' EXIT

tar --acls --xattrs --selinux \
  -czf "$BACKUP_FILE" \
  -C /opt/splunk etc

chmod 600 "$BACKUP_FILE"

sha256sum "$BACKUP_FILE"

printf 'Configuration backup: %s\n' "$BACKUP_FILE"
