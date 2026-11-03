**Step 47 — Create the backup script**

On **RHEL**:

```
cat > scripts/rhel/backup-config.sh <<'EOF'
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
EOF

chmod +x scripts/rhel/backup-config.sh

bash -n scripts/rhel/backup-config.sh

sudo bash scripts/rhel/backup-config.sh
```

**Command overview:**

| Command                         | Explanation                                            |
| ------------------------------- | ------------------------------------------------------ |
| `set -euo pipefail`             | Stops on important failures.                           |
| `umask 077`                     | Makes backup files private.                            |
| `trap ... EXIT`                 | Starts Splunk again when the script finishes or fails. |
| `tar --acls --xattrs --selinux` | Preserves important file information.                  |
| `chmod 600`                     | Restricts backup access.                               |
| `bash -n`                       | Checks syntax.                                         |

This backup contains sensitive configuration. Keep it outside GitHub and copy it to separate protected storage.

It excludes indexed records, the CA private key, and complete OS settings.

For a recovery exercise, use an isolated clone with the same Splunk version:

```
read -r -p 'Full path to the known-good backup: ' BACKUP_FILE

sudo tar -tzf "$BACKUP_FILE"

sudo systemctl stop Splunkd

sudo mv /opt/splunk/etc \
  "/opt/splunk/etc.before-restore-$(date -u +%Y%m%dT%H%M%SZ)"

sudo tar --acls --xattrs --selinux \
  -xzf "$BACKUP_FILE" \
  -C /opt/splunk

sudo chown -R splunk:splunk /opt/splunk/etc

sudo restorecon -RF /opt/splunk/etc

sudo systemctl start Splunkd
```

**Command overview:** These commands inspect the backup, preserve current settings, restore the saved configuration, fix permissions, and restart Splunk.

If extraction fails, keep Splunk stopped and restore the preserved directory.

---
