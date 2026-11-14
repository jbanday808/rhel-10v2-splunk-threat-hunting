# Deployment order

1. Follow [Steps 1 through 20](../steps/README.md) for VMware, RHEL, storage, certificates, and Splunk.
2. Follow Steps 21 through 30 for the Windows endpoint, Sysmon, forwarding, hunts, and dashboard.
   For the **optional Kali Linux analysis VM**, reserve resources in Steps 1, 3, and 4; after Step 27, follow [Step 28.16](../steps/28-generate-harmless-hunting-activity.md#step-2816--optional-kali-linux-analysis-workstation) and the [offline Kali guide](../network-defense/KALI_DEPLOYMENT.md). The three core VMs and six Splunk indexes remain the base lab.
3. Follow Steps 31 through 44 for IdM, verified LDAPS, group mappings, and access tests.
4. Follow Steps 45 through 52 for alerts, cleanup, backups, documentation, and export.
5. Follow [the appendices](../appendices/README.md) for phases, integrity, Azure OIDC, NGINX, Windows ZIP upload, password redaction, and HEC.

6. **Optional network analysis:** use the [network-defense guide](../../start-here/START_HERE_NETWORK_DEFENSE.md) or [Arkime guide](../../start-here/START_HERE_ARKIME.md) for synthetic offline exercises and separately validated sensor work.

The assembled files are already supplied. Review and deploy them at the applicable steps rather than recreating an older version over later additions. VM observations remain Pending until you actually test them.
