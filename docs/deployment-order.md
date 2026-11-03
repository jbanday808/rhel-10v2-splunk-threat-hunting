# Deployment order

1. Follow [Steps 1 through 20](steps/README.md) for VMware, RHEL, storage, certificates, and Splunk.
2. Follow Steps 21 through 30 for the Windows endpoint, Sysmon, forwarding, hunts, and dashboard.
3. Follow Steps 31 through 44 for IdM, verified LDAPS, group mappings, and access tests.
4. Follow Steps 45 through 52 for alerts, cleanup, backups, documentation, and export.
5. Follow [the appendices](appendices/README.md) for phases, integrity, OIDC, NGINX, Windows ZIP upload, password redaction, and HEC.

The assembled files are already supplied. Review and deploy them at the applicable steps rather than recreating an older version over later additions. VM observations remain Pending until you actually test them.
