**Step 35 — Configure Splunk DNS and trust the directory certificate**

On **RHEL-SPLUNK01**, run from the VM console:

```bash
sudo dnf install -y openldap-clients bind-utils
nmcli -f NAME,DEVICE,TYPE connection show --active
read -r -p 'Enter the Splunk VM Ethernet profile name: ' SPLUNK_PROFILE

sudo nmcli connection modify "$SPLUNK_PROFILE" \
  ipv4.dns 172.25.250.30 \
  ipv4.ignore-auto-dns yes
sudo nmcli connection up "$SPLUNK_PROFILE"

getent hosts idm01.lab.test
dig idm01.lab.test +short
dig docs.redhat.com +short
```

The first two checks must resolve IdM to `172.25.250.30`. The last confirms that IdM forwards external DNS requests. Splunk's address and gateway stay `.10` and `.2`. The Windows VM and physical host can keep their existing DNS and Splunk hosts-file entries.

Obtain the **public IdM CA certificate** over SSH. First display the IdM SSH fingerprint at its VM console:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
openssl x509 -in /etc/ipa/ca.crt -noout -fingerprint -sha256
```

Then, on **RHEL-SPLUNK01**:

```bash
mkdir -p "$HOME/siem-public"
scp labadmin@172.25.250.30:/etc/ipa/ca.crt "$HOME/siem-public/idm-ca.pem"
openssl x509 -in "$HOME/siem-public/idm-ca.pem" -noout -fingerprint -sha256

sudo install -d -o splunk -g splunk -m 700 /opt/splunk/etc/auth/ldap
sudo install -o splunk -g splunk -m 600 \
  "$HOME/siem-public/idm-ca.pem" /opt/splunk/etc/auth/ldap/idm-ca.pem
```

Compare the SSH fingerprint before accepting the connection, then compare the CA fingerprints. Copy the public CA certificate only. Keep the existing `/opt/splunk/etc/auth/lab/` certificates for Splunk Web and forwarder traffic.

**Command overview:** `nmcli` changes only the Splunk VM's DNS resolver; `scp` copies the public certificate securely; `openssl x509` displays its fingerprint; `install` saves the certificate with access limited to the Splunk service account.

**Summary:** Splunk can find the directory server and has a trusted copy of its signing certificate.

---
