**Step 43 — Back up the directory and document recovery**

The Splunk configuration backup in Step 47 includes live LDAP settings and Splunk's trusted directory certificate. Keep it private because it also includes secrets needed by the installation. It does **not** back up the separate IdM directory.

On **RHEL-IDM01**, create an IdM backup during a planned lab interruption:

```bash
sudo ipa-backup
sudo ipactl status
sudo ls -ld /var/lib/ipa/backup/ipa-full-*
```

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

**Command overview:** `ipa-backup` creates a directory backup; `ipactl status` confirms services returned; `sudoedit` changes authentication locally; `btool check` validates configuration before restart.

**Summary:** Splunk and IdM have separate backups, and local Splunk authentication remains a recovery option.

References:

- [Red Hat IdM Backup and Restore Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/preparing_for_disaster_recovery_with_identity_management/backing-up-and-restoring-idm): This guide explains full directory backups and supported recovery procedures.

---
