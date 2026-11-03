**Step 33 — Install IdM with DNS and its certificate authority**

On **RHEL-IDM01**, allow IdM services from the private lab subnet. The zone commands below are for this new VM; if the zone already exists, inspect it before changing it.

```bash
sudo firewall-cmd --permanent --new-zone=idm-lab
sudo firewall-cmd --permanent --zone=idm-lab --add-source=172.25.250.0/24
sudo firewall-cmd --permanent --zone=idm-lab --add-service=freeipa-4
sudo firewall-cmd --permanent --zone=idm-lab --add-service=dns
sudo firewall-cmd --permanent --zone=idm-lab --add-service=ssh
sudo firewall-cmd --reload
sudo firewall-cmd --zone=idm-lab --list-all
```

Install the directory interactively so passwords are entered at prompts:

```bash
sudo -i
umask 0022
ipa-server-install \
  --hostname=idm01.lab.test \
  --ip-address=172.25.250.30 \
  --domain=lab.test \
  --realm=LAB.TEST \
  --setup-dns \
  --forwarder=172.25.250.2 \
  --reverse-zone=250.25.172.in-addr.arpa.
exit
```

Review the proposed settings. Enter separate strong passwords for **Directory Manager** and the **IdM `admin`** account. Retain the integrated certificate authority and confirm installation. These are directory credentials, separate from Splunk's local administrator password.

After successful installation:

```bash
sudo ipactl status
kinit admin
ipa dnsrecord-add lab.test splunk01 --a-rec=172.25.250.10
ipa dnsrecord-add lab.test winhunt01 --a-rec=172.25.250.20
ipa dnsrecord-add 250.25.172.in-addr.arpa. 10 --ptr-rec=splunk01.lab.test.
ipa dnsrecord-add 250.25.172.in-addr.arpa. 20 --ptr-rec=winhunt01.lab.test.
dig @172.25.250.30 idm01.lab.test +short
dig @172.25.250.30 -x 172.25.250.30 +short
dig @172.25.250.30 _ldap._tcp.lab.test SRV +short
```

Confirm the IdM address is `.30`, the reverse lookup returns `idm01.lab.test.`, and the LDAP service record exists. If an entry already exists, inspect it with `ipa dnsrecord-show` instead of repeatedly adding it. The LDAP discovery record normally advertises port `389`; Splunk will explicitly use encrypted port `636`.

The installer normally configures the IdM server to use its integrated DNS. Confirm that its resolver now uses `.30`; if necessary, set the directory VM's active NetworkManager profile to DNS `172.25.250.30`. Keep the gateway at `.2` and the DNS forwarder at `.2`.

**Command overview:** `firewall-cmd` allows the directory services within the lab; `ipa-server-install` creates the directory, DNS, and certificate authority; `--realm` names the authentication realm; `--forwarder` sends external DNS requests to VMware; `kinit admin` starts an IdM administrator session; `ipa dnsrecord-add` adds DNS records.

**Summary:** IdM now hosts the lab directory and provides DNS records and a certificate for `idm01.lab.test`.

References:

- [Red Hat IdM Installation Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/installing_identity_management/installing-an-idm-server-with-integrated-dns-with-an-integrated-ca-as-the-root-ca): This guide explains interactive installation with integrated DNS and a certificate authority.
- [Red Hat IdM DNS Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/working_with_dns_in_identity_management/index): This guide explains forward and reverse DNS records in IdM.

---
