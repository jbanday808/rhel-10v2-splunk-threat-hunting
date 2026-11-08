# Validation and test commands

## On the RHEL Splunk VM (read-only checks)

```bash
cat /etc/redhat-release
getenforce
findmnt --mountpoint /splunkdata
df -h /splunkdata
sudo systemctl status Splunkd.service --no-pager -l
sudo -u splunk /opt/splunk/bin/splunk btool check
```

## On Windows endpoint (read-only checks)

```powershell
Get-Service SplunkForwarder
Test-NetConnection splunk01.lab.test -Port 9997
Get-WinEvent -ListLog 'Microsoft-Windows-Sysmon/Operational'
```

## In Splunk Search

Execute the `.spl` files in `hunts/` and record: index, source, UTC time, event count, latest event, expected marker and exact sanitized evidence. No events or empty dashboards are **not** success.

## On the developer workstation

```bash
python3 tools/validate_repository.py
```

Static validation checks file structure and XML syntax; it does **not** prove a running Splunk instance, LDAP auth, TLS verification or data ingestion.
