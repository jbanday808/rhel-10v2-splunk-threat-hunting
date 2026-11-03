**Step 19 — Verify the server**

```
sudo systemctl show Splunkd -p User -p Group -p LimitNOFILE

findmnt --mountpoint /splunkdata

sudo ss -lntp

getenforce

sudo -u splunk /opt/splunk/bin/splunk btool inputs list --debug

sudo -u splunk /opt/splunk/bin/splunk btool indexes list --debug

sudo -u splunk /opt/splunk/bin/splunk btool props list siem:lab --debug

sudo -u splunk /opt/splunk/bin/splunk btool transforms list lab_fields --debug
```

Check HTTPS:

```
curl --cacert /home/labadmin/siem-public/ca.pem \
  https://splunk01.lab.test:8000/en-US/account/login \
  -o /dev/null \
  -w '%{http_code}\n'
```

**Command overview:**

- `systemctl show` checks service ownership.
- `ss -lntp` shows listening services.
- `btool --debug` shows effective settings and source files.
- `curl --cacert` verifies HTTPS using the lab CA.

Confirm:

- Splunk runs as `splunk`.
- `/splunkdata` is mounted.
- SELinux is `Enforcing`.
- Ports `8000` and `9997` are listening.
- HTTPS validates.

---
