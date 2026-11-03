## Appendix HTTP Event Collector endpoint and curl test

**Question 154 answer: A.** Use `/services/collector`, or `https://172.25.250.10:8088/services/collector` in this lab. HEC defaults to HTTPS on port 8088; use your configured port if different.

This adds an application-event input alongside the port 9997 receiver. Send only the harmless payload below: the local `identity` redaction rule does not cover source type `siem:hec`.

### HEC step 1 Identify the endpoint

| Path | Use |
| --- | --- |
| `/services/collector` | Receive JSON event envelopes. Correct choice for Question 154. |
| `/services/collector/event` | Explicit JSON event endpoint. |
| `/services/collector/raw` | Receive raw text; requires a request channel. |
| `/services/collector/health` | Check whether HEC can accept data. |

Splunk Web on port 8000 is the administration interface. The management API usually uses port 8089. Send this exercise's data to the HEC listener on port 8088.

### HEC step 2 Enable the collector in Splunk Web

Sign in as a Splunk administrator at `https://172.25.250.10:8000`. Open **Settings > Data Inputs > HTTP Event Collector > Global Settings**. Enable **All Tokens**, select **Enable SSL**, use port **8088**, and save. Keep deployment-server distribution off for this standalone lab.

Confirm `lab` exists and the Step 15 certificate is current, includes IP `172.25.250.10`, and is readable by Splunk. The client uses its verified public CA.

### HEC step 3 Configure the lab TLS certificate

The ZIP supplies this global-settings example:

```bash
mkdir -p configs/hec
cat > configs/hec/inputs.conf.example <<'EOF'
[http]
disabled = 0
port = 8088
enableSSL = 1
serverCert = /opt/splunk/etc/auth/lab/splunk01.pem
EOF
```

**Command overview:** The example defines global HEC and certificate settings. It contains no token and is not automatically installed.

On RHEL-SPLUNK01, back up the existing HEC local configuration before editing:

```bash
sudo install -d -m 0700 /var/backups/siem-lab
sudo install -d -o splunk -g splunk -m 0700 \
  /opt/splunk/etc/apps/splunk_httpinput/local
sudo bash -c 'if test -f /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf; then
  cp -a /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf \
    /var/backups/siem-lab/hec-inputs-$(date -u +%Y%m%dT%H%M%SZ).conf
fi'
sudoedit /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf
```

**Command overview:** `install -d` prepares protected folders; `cp -a` preserves the existing file in a timestamped backup; `sudoedit` opens the live file.

Merge these settings into the single `[http]` stanza, adding it once if absent. Preserve other settings and `[http://…]` token stanzas; never overwrite the complete file with this example.

Apply ownership, check the settings, and restart:

```bash
sudo chown splunk:splunk /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf
sudo chmod 0600 /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf
sudo restorecon -v /opt/splunk/etc/apps/splunk_httpinput/local/inputs.conf
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
sudo ss -lntp 'sport = :8088'
```

**Command overview:** Ownership and mode protect the file; `restorecon` restores SELinux labeling; `btool` checks configuration; `systemctl` restarts Splunk; `ss` checks the listener. Resolve errors before testing. Verify HEC's `[http]` certificate separately from the browser connection.

### HEC step 4 Create a dedicated lab token

In **Settings > Data Inputs > HTTP Event Collector**, choose **New Token**. Name it `siem-lab-curl`. Set default source type to `siem:hec`, default index to `lab`, and allowed indexes to only `lab`. Review and submit. Ensure this individual token is enabled. Leave indexer acknowledgment off for this simple exercise; an acknowledgment-enabled client needs a channel and acknowledgment polling.

Keep the token in your password manager and use the hidden prompt. Keep live HEC configurations, backups, and full `btool inputs list` output outside GitHub; they can contain tokens.

### HEC step 5 Review the payload and send it with curl

Run as `labadmin` in the RHEL project root. Review `examples/hec/event.json` and `scripts/rhel/send-hec-event.sh`, then execute:

```bash
bash scripts/rhel/send-hec-event.sh
```

**Command overview:** The sender hides token entry, prepares private temporary files, sends one JSON event with a unique `SIEM-LAB-HEC-…` ID, checks the response, and removes temporary files. Keep shell tracing off.

Its curl request is:

```bash
curl --fail-with-body --silent --show-error \
  --connect-timeout 10 --max-time 30 \
  --cacert "$CA_FILE" \
  --header "@$WORK_DIR/headers" \
  --data-binary "@$WORK_DIR/event.json" \
  "$HEC_URL" > "$WORK_DIR/response.json"
```

**Command overview:** The sender sets `HEC_URL` to this lab's collector, `CA_FILE` to `/home/labadmin/siem-public/ca.pem`, and `WORK_DIR` to its private temporary folder. `--cacert` verifies trust and the address; `--header @file` reads the protected `Authorization: Splunk <token>` header; `--data-binary @file` sends JSON. Timeouts bound the request. HTTP errors and nonzero HEC response codes fail the test.

The JSON envelope contains `index`, `sourcetype`, `source`, `host`, and `event`; its harmless event begins with `action=hec_check`. The helper prints the unique ID and avoids automatic retries, which could duplicate accepted events.

### HEC step 6 Confirm the event is indexed

Copy the newly printed test ID into this Splunk search:

```spl
index=lab sourcetype=siem:hec source="hec:siem-lab"
"SIEM-LAB-HEC-REPLACE-WITH-EXACT-ID" earliest=-15m latest=now
| table _time host source sourcetype _raw
```

**Command overview:** The search displays the stored event. Confirm at least one result with the expected metadata and exact ID. HTTP acceptance alone does not prove indexing.

The ZIP also includes this reusable search:

```bash
cat > hunts/12-hec-ingestion-check.spl <<'EOF'
index=lab sourcetype=siem:hec source="hec:siem-lab"
"SIEM-LAB-HEC-" earliest=-24h latest=now
| table _time host source sourcetype _raw
EOF
```

**Command overview:** The heredoc saves the recent-event search. Use an exact test ID for a specific validation run and record observations in `evidence/sanitized/hec-validation.md`.

### HEC step 7 Troubleshoot and control client access

For connection failures, check the service, listener, and URL. For TLS failures, check the CA, expiry, and certificate names. For authorization failures, check global and token enablement and the `Splunk` header prefix. Check that `lab` exists and is allowed. For missing search results, check permissions, metadata, time range, and indexing health.

This exercise sends from RHEL-SPLUNK01 to its own lab address, so it needs no remote-client firewall opening. To use WINHUNT01 as a client later, permit only its address in the existing `siem-lab` firewall zone:

```bash
sudo firewall-cmd --permanent --zone=siem-lab \
  --add-rich-rule='rule family=ipv4 source address=172.25.250.20/32 port port=8088 protocol=tcp accept'
sudo firewall-cmd --reload
sudo firewall-cmd --zone=siem-lab --list-rich-rules
```

**Command overview:** The optional rule allows TCP 8088 from the Windows lab endpoint; reload applies it, and the list command verifies it. A remote client also needs the verified public CA and a dedicated token. Disable unused test tokens in Splunk Web after the exercise, and remove this optional firewall rule if remote collection is no longer needed.

**Summary:** Use `/services/collector` for HEC JSON events, enable TLS and a dedicated token, send a unique curl marker, and verify the indexed event in Splunk.

References:

- [Splunk Input Endpoint Reference](https://help.splunk.com/en/splunk-enterprise/rest-api-reference/10.6/input-endpoints/input-endpoint-descriptions): Defines HEC paths and the standard event endpoint.
- [Splunk Web HEC Setup](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.6/get-data-with-http-event-collector/set-up-and-use-http-event-collector-in-splunk-web): Explains global enablement, token creation, and allowed indexes.
- [Splunk Inputs Configuration Reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/inputs.conf): Defines the HEC listener's `[http]` TLS and port settings.
- [curl Manual](https://curl.se/docs/manpage.html): Defines the certificate, header-file, payload, and failure options used by the sender.
