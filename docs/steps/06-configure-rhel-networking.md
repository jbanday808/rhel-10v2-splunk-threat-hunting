**Step 6 — Configure RHEL networking**

Run from the **RHEL VM console**:

```
cat /etc/redhat-release

uname -m

id

nmcli -f NAME,DEVICE,TYPE connection show --active

ip -brief address
```

**Command overview:**

| Command                   | Explanation                       |
| ------------------------- | --------------------------------- |
| `cat /etc/redhat-release` | Shows the RHEL version.           |
| `uname -m`                | Shows the processor architecture. |
| `id`                      | Shows your account and groups.    |
| `nmcli`                   | Lists network profiles.           |
| `ip -brief address`       | Shows network addresses.          |

Set the fixed address:

```
read -r -p 'Enter the active Ethernet profile name: ' NET_PROFILE

sudo nmcli connection modify "$NET_PROFILE" \
  ipv4.method manual \
  ipv4.addresses 172.25.250.10/24 \
  ipv4.gateway 172.25.250.2 \
  ipv4.dns 172.25.250.2

sudo nmcli connection up "$NET_PROFILE"

sudo hostnamectl set-hostname splunk01.lab.test
```

Update the lab-name records:

```
sudo cp -a /etc/hosts /etc/hosts.before-siem

sudo sed -i \
  -e '/splunk01\.lab\.test/d' \
  -e '/winhunt01\.lab\.test/d' \
  /etc/hosts

printf '\n172.25.250.10 splunk01.lab.test splunk01\n172.25.250.20 winhunt01.lab.test winhunt01\n' \
  | sudo tee -a /etc/hosts

ip route

getent hosts splunk01.lab.test
```

**Command overview:**

- `sudo` runs a command with administrator permission.
- `read` stores the profile name.
- `nmcli connection modify` changes network settings.
- `nmcli connection up` applies them.
- `hostnamectl` sets the server name.
- `cp -a` preserves a backup.
- `sed` removes previous lab-name entries.
- `printf` produces the new entries.
- `tee -a` adds them to the file.
- `getent hosts` checks name resolution.

---
