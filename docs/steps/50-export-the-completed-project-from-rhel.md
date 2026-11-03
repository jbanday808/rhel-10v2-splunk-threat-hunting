**Step 50 — Export the completed project from RHEL**

```
tar -czf "$HOME/rhel-splunk-source.tgz" \
  --exclude='rhel-splunk-threat-hunting/evidence/raw' \
  --exclude='rhel-splunk-threat-hunting/downloads' \
  --exclude='rhel-splunk-threat-hunting/private' \
  --exclude='rhel-splunk-threat-hunting/backups' \
  --exclude='rhel-splunk-threat-hunting/.git' \
  -C "$HOME" \
  rhel-splunk-threat-hunting

sha256sum "$HOME/rhel-splunk-source.tgz"
```

**Command overview:**

- `tar -czf` packages the source project.
- `--exclude` omits private or unnecessary material.
- `sha256sum` creates a transfer-check fingerprint.

On the **physical Windows host**:

```
New-Item -ItemType Directory -Path C:\SIEMLab\Export -Force

scp.exe labadmin@172.25.250.10:/home/labadmin/rhel-splunk-source.tgz C:\SIEMLab\Export\

Get-FileHash C:\SIEMLab\Export\rhel-splunk-source.tgz -Algorithm SHA256
```

Compare the hash with RHEL.

---
