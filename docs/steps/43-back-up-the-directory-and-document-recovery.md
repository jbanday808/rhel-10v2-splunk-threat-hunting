**Step 43 — Back up the directory and document recovery**

The Splunk configuration backup in Step 47 includes live LDAP settings and Splunk's trusted directory certificate. Keep it private because it also includes secrets needed by the installation. It does **not** back up the separate IdM directory.

On **RHEL-IDM01**, create an IdM backup during a planned lab interruption. Run these commands in the same terminal, one at a time:

```bash
sudo ipa-backup
sudo ipactl status
```

Wait for `The ipa-backup command was successful` and copy only the full directory path after `Backed up to` (for example, `/var/lib/ipa/backup/ipa-full-2026-11-09-03-06-08`). `ipactl status` should show the configured services running. Then verify the new backup without using a wildcard:

```bash
read -r -p 'Paste the full path shown after Backed up to: ' IDM_BACKUP_DIR
sudo ls -lh -- "$IDM_BACKUP_DIR/header" "$IDM_BACKUP_DIR/ipa-full.tar"
sudo test -s "$IDM_BACKUP_DIR/ipa-full.tar" && echo 'Backup archive is nonempty'
```

Expected result: both `header` and a nonempty `ipa-full.tar` appear in the directory just reported by `ipa-backup`. If you used `ipa-backup --gpg` instead, check for `ipa-full.tar.gpg` in place of `ipa-full.tar`. Keep the archive and backup contents out of GitHub.

If the backup succeeded but the original `sudo ls -ld /var/lib/ipa/backup/ipa-full-*` command reported “No such file or directory,” do **not** rerun the backup just for that message. Your shell tries to expand `*` before `sudo` runs; it might lack permission to list the backup directory. An escaped `\*` is also treated as a literal character. To list backup folders safely, run:

```bash
sudo find /var/lib/ipa/backup -mindepth 1 -maxdepth 1 -type d -name 'ipa-full-*' -print
```

Compare the result with the directory printed by `ipa-backup`, then run the exact-path file check above. If `header` or the archive is missing, investigate that backup before treating it as recoverable.

A full IdM backup temporarily takes IdM services offline. Protect the backup and copy it to separate secure storage. Validate recovery in an isolated VM using the matching RHEL and IdM versions; follow Red Hat's recovery procedure rather than starting a restored copy beside the original directory server.

If LDAP configuration prevents a successful lab test:

1. Sign in with the original **local Splunk `admin`**, open Authentication Methods, and select native Splunk authentication.
2. If Web access is unavailable, open the **RHEL-SPLUNK01 console** and run `sudoedit /opt/splunk/etc/system/local/authentication.conf`.
3. In the existing `[authentication]` section, set `authType = Splunk`. Preserve the remaining sections for investigation; do not create a second `[authentication]` section.
4. Run the commands below and retest the local account.

```bash
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

For a complete configuration restore, use the protected pre-LDAP backup and the isolated recovery procedure in Step 47. LDAP rollback does not require changing the Windows forwarder or its TCP `9997` receiver.

Record the lookup account's owner, password-rotation date, and certificate-renewal checks in private operational notes. When its password changes, update the bind password through Splunk Web and repeat the lookup and login tests. Check IdM service-certificate renewal health as well as the expiry of the copied CA certificate.

**Command overview:** `ipa-backup` creates the directory backup; `ipactl status` checks that services returned; `read -r` records the exact backup path for this terminal; `sudo ls` shows the backup files; `test -s` confirms the archive is not empty; `sudo find` searches the protected directory without a shell wildcard. `sudoedit` changes authentication locally, and `btool check` validates the configuration before restart.

**Summary:** Splunk and IdM have separate backups, and local Splunk authentication remains a recovery option.

References:

- [Red Hat IdM Backup and Restore Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/preparing_for_disaster_recovery_with_identity_management/backing-up-and-restoring-idm): This guide explains full directory backups and supported recovery procedures.

---
