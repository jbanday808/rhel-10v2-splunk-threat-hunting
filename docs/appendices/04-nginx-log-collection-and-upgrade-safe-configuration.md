## Appendix NGINX log collection and upgrade safe configuration

**The correct answer in the supplied example is Option A:** `$SPLUNK_HOME/etc/apps/Splunk_TA_nginx/local/inputs.conf`. For this lab, the full path is `/opt/splunk/etc/apps/Splunk_TA_nginx/local/inputs.conf`.

Place your input changes in the add-on's `local` folder. Splunk combines them with the vendor defaults, and standard upgrades preserve local customizations. Keep a backup and validate the effective settings after an upgrade. Editing an app's `default/inputs.conf` risks losing the change when its vendor files are replaced.

This exercise runs NGINX on RHEL-SPLUNK01 and collects its access and error logs locally. The test web server listens only on `127.0.0.1:80`, so the curl test runs inside RHEL. The existing `lab` index and `lab_hunter` permissions are reused.

### NGINX step 1 Install the required software and add on

Complete the original RHEL Splunk setup first. Then, on RHEL:

```bash
sudo dnf install -y nginx acl curl

rpm -q nginx
sudo systemctl status Splunkd --no-pager
```

**Command overview:** `dnf install` installs NGINX, access-control tools, and curl; `rpm -q` shows the installed NGINX version; `systemctl status` checks Splunk.

Download a compatible **Splunk Add-on for NGINX** from its official Splunk page. In Splunk Web, use **Apps → Manage Apps → Install app from file**, install the vendor package, and restart if requested. Record the exact version in `docs/versions.md`.

Confirm the installed app folder:

```bash
sudo ls -d /opt/splunk/etc/apps/Splunk_TA_nginx
```

The ZIP contains the custom `local/inputs.conf` overlay. Install the official add-on before deploying this overlay; its vendor parsing and search settings are supplied by that separate package.

### NGINX step 2 Create the local test web server configuration

The following configuration is for this dedicated learning VM. If NGINX already hosts another application, merge an appropriate test server into its existing configuration instead of replacing that application's settings.

```bash
cd "$HOME/rhel-splunk-threat-hunting"
mkdir -p configs/nginx apps/Splunk_TA_nginx/local

cat > configs/nginx/nginx.conf <<'EOF'
user nginx;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log warn;

events {
    worker_connections 256;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log /var/log/nginx/access.log combined;
    sendfile on;

    server {
        listen 127.0.0.1:80;
        server_name localhost;
        root /usr/share/nginx/html;

        location = /siem-lab {
            default_type text/plain;
            return 200 "SIEM-LAB-NGINX-TEST\n";
        }
    }
}
EOF
```

**Configuration overview:** `listen` limits the server to loopback; `access_log ... combined` uses the standard combined access-log format; `error_log` records errors; the `/siem-lab` location returns a harmless test marker.

For the dedicated lab server, preserve its current file, test the new configuration, and install it:

```bash
NGINX_BACKUP="/etc/nginx/nginx.conf.before-siem-$(date -u +%Y%m%dT%H%M%SZ)"
sudo cp -a /etc/nginx/nginx.conf "$NGINX_BACKUP"

sudo nginx -t -c "$PWD/configs/nginx/nginx.conf"

sudo install -o root -g root -m 644 \
  configs/nginx/nginx.conf /etc/nginx/nginx.conf

sudo restorecon -RF /etc/nginx /var/log/nginx
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx
```

**Command overview:** `cp -a` backs up the current settings; `nginx -t` checks configuration; `-c` selects the proposed file; `install` deploys it with defined ownership and permissions; `restorecon` restores SELinux labels; `enable` enables automatic startup; `restart` starts NGINX with the installed configuration.

### NGINX step 3 Generate an access event with curl

Run inside RHEL-SPLUNK01:

```bash
curl --fail --silent --show-error \
  --user-agent 'SIEM-LAB-NGINX-TEST' \
  http://127.0.0.1/siem-lab

sudo tail -n 5 /var/log/nginx/access.log
```

**Command overview:** `curl` makes the request; `--fail` reports HTTP error responses as failures; `--silent` hides the progress meter; `--show-error` displays errors; `--user-agent` puts a recognizable marker in the access log; the URL selects the loopback test endpoint; `tail -n 5` shows recent log entries.

**Expected result:** The response contains `SIEM-LAB-NGINX-TEST`, and the access log contains a request for `/siem-lab` with the marker as its user agent. HTTP is used only for this loopback test endpoint; Splunk Web and Windows forwarding retain their existing TLS settings.

### NGINX step 4 Allow the Splunk account to read the logs

```bash
sudo setfacl -m u:splunk:rx /var/log/nginx
sudo setfacl -d -m u:splunk:rx /var/log/nginx
sudo setfacl -m u:splunk:r \
  /var/log/nginx/access.log /var/log/nginx/error.log

getfacl /var/log/nginx
sudo -u splunk head -n 1 /var/log/nginx/access.log
```

**Command overview:** `setfacl -m` grants the service account access; `-d` supplies an inherited default for new log files; directory `rx` permits traversal and listing; file `r` permits reading; `getfacl` displays the access rules; `head` confirms that the account can read an entry.

Retest reading after log rotation. If collection still fails under SELinux, inspect `sudo ausearch -m AVC -ts recent` and Splunk's log; keep SELinux enforcing while investigating the actual denial.

### NGINX step 5 Configure the add on local input

Create the source overlay:

```bash
cat > apps/Splunk_TA_nginx/local/inputs.conf <<'EOF'
[monitor:///var/log/nginx/access.log]
disabled = 0
index = lab
sourcetype = nginx:plus:access
host = splunk01

[monitor:///var/log/nginx/error.log]
disabled = 0
index = lab
sourcetype = nginx:plus:error
host = splunk01
EOF
```

**Configuration overview:** Each `monitor` section selects one log; `disabled = 0` enables collection; `index = lab` chooses storage; `sourcetype` selects the vendor's rules; `host` labels the source computer. The `nginx:plus:access` source type supports this combined-format access log and does not require an NGINX Plus subscription for this file-monitoring example.

If the installed `local/inputs.conf` already exists, review it and merge these two sections without discarding unrelated inputs. For a fresh add-on installation:

```bash
sudo install -d -o splunk -g splunk -m 750 \
  /opt/splunk/etc/apps/Splunk_TA_nginx/local

sudo install -o splunk -g splunk -m 640 \
  apps/Splunk_TA_nginx/local/inputs.conf \
  /opt/splunk/etc/apps/Splunk_TA_nginx/local/inputs.conf

sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool inputs list \
  'monitor:///var/log/nginx/access.log' --debug

sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

**Command overview:** `install -d` creates the local override directory; `install -m 640` deploys the input file; `btool check` validates settings; `btool inputs list ... --debug` identifies the effective input and its source file; `systemctl` restarts and checks Splunk.

### NGINX step 6 Confirm collection and upgrade behavior

Repeat the curl command after restarting Splunk. In the Threat Hunting Lab app:

```spl
index=lab sourcetype=nginx:plus:access "SIEM-LAB-NGINX-TEST"
earliest=-15m latest=now
| table _time host source sourcetype _raw
```

**Command overview:** The index and source type select access records; the quoted marker finds the curl request; the time terms select recent events; `table` shows the record and its source details.

Save a reusable search in the project:

```bash
cat > hunts/09-nginx-access.spl <<'EOF'
index=lab sourcetype=nginx:plus:access earliest=-24h
| stats count by host status
| sort - count
EOF
```

If the raw event is present but expected fields are missing, verify the installed add-on's version, log format, source type, and app permissions. If the event is absent, inspect the file path, service-account access, input enablement, index, and time range first.

Before an add-on upgrade, back up the installed `local` folder to protected storage. After upgrading, rerun `btool` and the curl/search test. Do not replace the vendor `default` folder with files from this ZIP. Record actual results in `evidence/sanitized/nginx-validation.md`.

**Summary:** Install the vendor add-on, generate a known request, grant log access, configure `Splunk_TA_nginx/local/inputs.conf`, and verify the resulting event in Splunk.

References:

- [Splunk NGINX Input Guide](https://splunk.github.io/splunk-add-on-for-nginx/Configureinputsv2monitor/): This guide explains the local input file and the source types for NGINX logs.
- [Splunk Configuration Directories Guide](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/administer-splunk-enterprise-with-configuration-files/configuration-file-directories): This guide explains default files, local overrides, and upgrades.
- [Red Hat NGINX Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/deploying_web_servers_and_reverse_proxies/setting-up-and-configuring-nginx): This guide explains installing and configuring NGINX on RHEL.
- [curl Manual](https://curl.se/docs/manpage.html): This manual explains the request and error-handling options used in the test.

---
