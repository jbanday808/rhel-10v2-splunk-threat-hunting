# 06 — Host-Based Micro-Perimeters and Network Segmentation

## Architecture limitation

VMware VMnet8 `172.25.250.0/24` is **one network segment**. It is not full east–west microsegmentation. Source-restricted `firewalld` rules establish **host-level micro-perimeters** for selected services; dynamic ZTNA/SDN, service identities and continuous policy evaluation are still future work.

**Run firewall commands only on the appropriate VM console with recovery access.** Never change a remote firewall without a tested out-of-band console and a known-good backup.

## Step 1 — Confirm active zone and save a private snapshot (RHEL-SPLUNK01)

```bash
sudo firewall-cmd --state
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --zone=siem-lab --list-all
sudo firewall-cmd --zone=siem-lab --list-rich-rules
sudo firewall-cmd --zone=siem-lab --list-ports
sudo ss -lntp
sudo cp -a /etc/firewalld "/root/firewalld-before-zt-$(date -u +%Y%m%dT%H%M%SZ)"
```

**Command overview:** `firewall-cmd` displays existing rules; `ss` lists listeners; `cp -a` saves configurations in root-only local storage. If `siem-lab` is not the interface zone, stop and resolve it against [Step 18](../steps/18-configure-the-rhel-firewall.md). Never publish private backup content.

## Step 2 — Define an explicit desired policy

The [JSON policy matrix](../../configs/zero-trust/allowed-flows.example.json) describes an **illustrative desired policy**, not a command file automatically pushed to a firewall.

| Flow | Source | Destination | Port | Expected |
| --- | --- | --- | --- | --- |
| Browser management | Host `.1` | Splunk `.10` | TCP 8000 | Allow |
| Windows forwarding | WINHUNT01 `.20` | Splunk `.10` | TCP 9997 | Allow |
| Directory authentication | Splunk `.10` | IdM `.30` | TCP 636 | Allow |
| Name lookup | Splunk `.10` | IdM `.30` | TCP/UDP 53 | Allow |
| Splunk management API from lab peers | Any unauthorized VM | Splunk `.10` | TCP 8089 | Deny |
| Browser management from unexpected source | Unauthorized peer | Splunk `.10` | TCP 8000 | Deny |

**Separate SSH 22** from these data paths; approve explicit management sources and protect your recovery path. Other IdM enrollment, Kerberos, CA, time and update dependencies must be reviewed separately.

## Step 3 — Inspect broad rules before narrowing

```bash
sudo firewall-cmd --zone=siem-lab --query-port=8000/tcp
sudo firewall-cmd --zone=siem-lab --query-port=9997/tcp
sudo firewall-cmd --zone=siem-lab --list-services
sudo firewall-cmd --zone=siem-lab --list-rich-rules
```

**Explanation:** `--query-port` checks whether the entire zone allows a service. If a broad `8000/tcp` rule is present, adding a source-limited `accept` rich rule **does not revoke that broad permission**. Audit any service definitions, other zones, IPv6 listeners, forwarding policies and trusted source zones as well.

## Step 4 — Add approved source-specific rules to the *runtime* configuration

Only after a VM console is available:

```bash
sudo firewall-cmd --zone=siem-lab \
  --add-rich-rule='rule family="ipv4" source address="172.25.250.1/32" port port="8000" protocol="tcp" accept'
sudo firewall-cmd --zone=siem-lab \
  --add-rich-rule='rule family="ipv4" source address="172.25.250.20/32" port port="9997" protocol="tcp" accept'
sudo firewall-cmd --zone=siem-lab --list-rich-rules
```

**Command overview:** These *runtime-only* rules allow Splunk Web only from the physical host, and forwarder traffic only from WINHUNT01. They **do not persist after reload** until saved. **They do not, alone, block broad rules**.

The original Step 18 may already include the latter source allowlist. Duplicate requests are normally idempotent, but inspect current policy first.

## Step 5 — Remove *only* superseded broad access after testing

For example, if `--query-port=8000/tcp` displayed **yes**, and you have documented source-restricted access plus console recovery, evaluate removing the broad runtime allowance:

```bash
sudo firewall-cmd --zone=siem-lab --remove-port=8000/tcp
```

For any existing `8000` acceptance from WINHUNT01 and any other broader source, use **the exact currently listed rich-rule string** to remove it, **only if** WINHUNT01 no longer requires that access. Do not guess or remove unrelated allowed rules. Repeat the process separately for `9997/tcp` if it was broadly open. Existing SSH rules must remain approved and reachable.

**Do not use `--set-target=DROP` blindly:** dropping your own SSH, IdM, DNS or update connectivity may strand the VM. `firewalld` decisions can involve overlapping sources and service definitions. Review the **effective** policy; test both IPv4 and IPv6 if applicable.

## Step 6 — Test *both* allowed and denied paths

From **Windows host PowerShell**, if the host's adapter is allowed:

```powershell
Test-NetConnection 172.25.250.10 -Port 8000
Test-NetConnection 172.25.250.10 -Port 8089
```

From **WINHUNT01 PowerShell**:

```powershell
Test-NetConnection 172.25.250.10 -Port 9997
Test-NetConnection 172.25.250.10 -Port 8000
```

From **RHEL-SPLUNK01**:

```bash
getent hosts idm01.lab.test
sudo -u splunk openssl s_client -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test -verify_return_error </dev/null
```

**Expected:** `.1 → 8000` works, `.20 → 9997` works, `.20 → 8000` is denied if its access was intentionally removed, unauthorized access to management 8089 fails, LDAPS certificates verify. A service that is simply **not listening** is not proof of a firewall denial; corroborate with firewalld logs/packet capture or controlled source-vs-source testing.

## Step 7 — Persist only after positive and negative tests

Once all requirements and rollback are verified:

```bash
sudo firewall-cmd --runtime-to-permanent
sudo firewall-cmd --zone=siem-lab --list-all
```

**Command overview:** Saves the *entire current runtime configuration* permanently. **Use only if runtime changes were fully reviewed**, because other unplanned runtime changes would be saved too.

## Step 8 — IdM DNS/LDAPS ingress and egress plan

On **RHEL-IDM01** inspect currently installed IdM-related firewalld services. For an IdM deployment, DNS 53 and LDAPS 636 are not necessarily its only ports: Kerberos, HTTP, LDAP, CA, NTP and enrollment traffic may be required depending on your configured services. **Do not restrict IdM by copying the Splunk zone rules.** Define an IdM-specific allowlist only after dependency mapping and service-owner review. The Splunk VM must retain outbound DNS/LDAPS and update access.

## Step 9 — Rollback and recovery

If a runtime rule causes an outage, use the **VM console** to remove *only that rule* or reapply the verified known-good zone configuration. A firewall reload discards runtime-only edits and restores the permanent policy **if the permanent policy was not changed**. Avoid `systemctl stop firewalld` or assigning `trusted` as a quick fix.

**Proof of Zero Trust:** Document both allow and deny behavior, not just that ports were configured. This **still does not** establish a centralized policy engine, dynamic microsegmentation, or DoD Target Level.
