**Step 45 — Create and test an alert**

In the **Threat Hunting Lab** app:

1. Run the encoded-PowerShell search.
2. Replace `earliest=-30m` with `earliest=-10m` in the search text.
3. Select **Save As → Alert**.
4. Name it `LAB - Encoded PowerShell`.
5. Schedule every five minutes.
6. If cron is requested, enter:
   ```
   */5 * * * *
   ```
7. Trigger when results are greater than zero.
8. Select **Add to Triggered Alerts**.
9. Use per-result suppression for 15 minutes on `host` and `ProcessGuid`.
10. Save under the administrator account.

Inside Windows, generate another marker:

```
$Payload = "Write-Output 'SIEM-LAB-ENCODED-TEST'"

$Encoded = [Convert]::ToBase64String(
    [Text.Encoding]::Unicode.GetBytes($Payload)
)

powershell.exe -NoProfile -EncodedCommand $Encoded
```

Check **Triggered Alerts** after the next scheduled run.

On RHEL, review the generated alert settings:

```
sudo cat /opt/splunk/etc/apps/LAB_SIEM/local/savedsearches.conf
```

If the file contains the lab alert, copy it to the source project:

```
sudo install -o labadmin -g labadmin -m 640 \
  /opt/splunk/etc/apps/LAB_SIEM/local/savedsearches.conf \
  "$HOME/rhel-splunk-threat-hunting/apps/LAB_SIEM/local/savedsearches.conf"
```

Also review and preserve `metadata/local.meta` if it contains the alert ownership and access settings.

**Command overview:** `cat` displays the settings; `install` copies the reviewed configuration to the project.

Scheduling and role behavior require an appropriate active license.

---
