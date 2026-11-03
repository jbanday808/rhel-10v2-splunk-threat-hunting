# RHEL helpers

Run these inside RHEL-SPLUNK01 after reading their matching guide sections.

| File | Purpose and prerequisites |
| --- | --- |
| `prepare-storage.sh` | Step 13. Formats only the explicitly selected empty data disk after confirmation. Review `lsblk` first. |
| `backup-config.sh` | Step 47. Stops and restarts Splunk while backing up its sensitive configuration outside the repository. |
| `verify-server.sh` | Step 19. Reads service, storage, configuration, and HTTPS state. |
| `configure-linux-logging.sh` | Step 16. Configures the dedicated lab's local logging and creates test records. |
| `install-nginx-lab.sh` | NGINX appendix. Installs a loopback test server and local input overlay after the official add-on exists. Prompts before replacing the NGINX configuration. |
| `apply-nginx-log-acl.sh` | Grants the Splunk service account read access to NGINX logs. Retest after log rotation. |
| `check-integrity.sh` | Integrity appendix. Checks the local lab index during a brief service stop and restarts Splunk on exit. Hash coverage is a prerequisite. |
| `install-redaction-lab.sh` | Redaction appendix. Merges the dedicated identity stanzas into the existing app, backs up changes, prepares the fake test source, and restarts Splunk. |
| `generate-redaction-marker.sh` | Appends a fresh record with two dummy password values after the redaction configuration is active. |
| `send-hec-event.sh` | HEC appendix. Prompts for a token, verifies TLS, sends one dummy JSON event, and checks HEC response code zero. Run as labadmin after HEC setup. |

Example: `sudo bash scripts/rhel/install-nginx-lab.sh`.
The fishbucket reset remains an explicit optional command in the guide because it can replay already indexed records.
