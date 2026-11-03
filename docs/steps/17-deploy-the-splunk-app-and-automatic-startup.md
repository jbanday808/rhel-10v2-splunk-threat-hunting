**Step 17 — Deploy the Splunk app and automatic startup**

```
sudo cp -a apps/LAB_SIEM /opt/splunk/etc/apps/

sudo chown -R splunk:splunk /opt/splunk/etc/apps/LAB_SIEM

sudo find /opt/splunk/etc/apps/LAB_SIEM \
  -type d -exec chmod 750 {} +

sudo find /opt/splunk/etc/apps/LAB_SIEM \
  -type f -exec chmod 640 {} +
```

Enable automatic startup:

```
sudo /opt/splunk/bin/splunk enable boot-start \
  -systemd-managed 1 \
  -user splunk \
  -group splunk
```

Create the service override:

```
sudo mkdir -p /etc/systemd/system/Splunkd.service.d

sudo tee /etc/systemd/system/Splunkd.service.d/lab.conf > /dev/null <<'EOF'
[Unit]
RequiresMountsFor=/splunkdata

[Service]
LimitNOFILE=65536
LimitNPROC=16000
TasksMax=16000
EOF
```

Check and start:

```
sudo -u splunk /opt/splunk/bin/splunk btool check

sudo systemctl daemon-reload

sudo systemctl enable --now Splunkd

sudo systemctl status Splunkd --no-pager
```

**Command overview:**

- `cp -a` copies the app.
- `find ... -exec chmod` applies permissions.
- `enable boot-start` creates automatic startup.
- `RequiresMountsFor` requires the data disk before startup.
- `btool check` checks configuration.
- `systemctl` loads and starts the service.

Splunk documents this systemd startup method. [help.splunk.com](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/start-splunk-enterprise-and-perform-initial-tasks/run-splunk-enterprise-as-a-systemd-service?utm_source=chatgpt.com)

---
