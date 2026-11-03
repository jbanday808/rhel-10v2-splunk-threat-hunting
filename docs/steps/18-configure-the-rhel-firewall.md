**Step 18 — Configure the RHEL firewall**

Use the **RHEL VM console**:

```
nmcli -f NAME,DEVICE,TYPE connection show --active

read -r -p 'Enter the Ethernet profile name: ' NET_PROFILE

sudo firewall-cmd --permanent --new-zone=siem-lab
```

If the zone already exists, inspect it and skip recreating it.

Allow host and Windows VM administration:

```
for SOURCE_IP in 172.25.250.1 172.25.250.20; do
  for PORT in 22 8000; do
    sudo firewall-cmd --permanent --zone=siem-lab \
      --add-rich-rule="rule family=ipv4 source address=$SOURCE_IP/32 port port=$PORT protocol=tcp accept"
  done
done
```

Allow event forwarding:

```
sudo firewall-cmd --permanent --zone=siem-lab \
  --add-rich-rule='rule family=ipv4 source address=172.25.250.20/32 port port=9997 protocol=tcp accept'
```

Apply:

```
sudo firewall-cmd --reload

sudo nmcli connection modify "$NET_PROFILE" connection.zone siem-lab

sudo nmcli connection up "$NET_PROFILE"

sudo firewall-cmd --get-active-zones

sudo firewall-cmd --zone=siem-lab --list-all
```

**Command overview:**

- `--permanent` saves the rules.
- `--new-zone` creates a dedicated rule set.
- `--add-rich-rule` permits a specific source and port.
- `--reload` applies saved settings.
- `connection.zone` assigns the adapter.

| Port     | Purpose               | Allowed source      |
| -------- | --------------------- | ------------------- |
| TCP 22   | SSH and file transfer | Host and Windows VM |
| TCP 8000 | Splunk HTTPS          | Host and Windows VM |
| TCP 9997 | Encrypted forwarding  | Windows VM          |
| TCP 8089 | Splunk management     | Not opened remotely |

---
