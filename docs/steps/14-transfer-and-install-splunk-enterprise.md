**Step 14 — Transfer and install Splunk Enterprise**

On the **RHEL console**, display the SSH fingerprint:

```
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
```

On the **physical Windows host**:

```
Get-Command ssh.exe,scp.exe
```

If missing, use administrator PowerShell:

```
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

Copy the package:

```
$SplunkPackage = Read-Host 'Full path to the Linux Splunk .tgz'

scp.exe $SplunkPackage labadmin@172.25.250.10:/home/labadmin/siem-downloads/
```

Compare the SSH fingerprint before accepting the first connection.

Back on **RHEL**:

```
read -r -p 'Full path to the staged Splunk .tgz: ' SPLUNK_PACKAGE

read -r -p 'Official SHA-256 checksum from Splunk: ' SPLUNK_SHA256

printf '%s  %s\n' "$SPLUNK_SHA256" "$SPLUNK_PACKAGE" \
  | sha256sum --check -
```

Continue when it reports `OK`:

```
sudo tar -xzf "$SPLUNK_PACKAGE" -C /opt

sudo chown -R splunk:splunk /opt/splunk

sudo -u splunk /opt/splunk/bin/splunk start --accept-license
```

Create the Splunk web administrator named `admin`.

Then:

```
sudo -u splunk /opt/splunk/bin/splunk stop
```

**Command overview:**

- `ssh-keygen -lf` displays the SSH identity.
- `scp` copies the package securely.
- `sha256sum --check` verifies it.
- `tar -xzf` extracts it.
- `-C /opt` selects the destination.
- `chown -R` assigns ownership.
- `sudo -u splunk` runs Splunk under its service account.
- `start --accept-license` initializes the software.
- `stop` stops the initial instance.

If `/opt/splunk` already contains an installation, inspect it before extracting another package over it.

---
