# Tools used for threat hunting

These tools support different parts of the investigation. Start with the question you want to answer, then choose the tools and records that can help.

| Tool | How it helps | Where to learn more |
| --- | --- | --- |
| Splunk Enterprise | Brings available event records together so an analyst can search for patterns. | [Splunk hunting reference](SPLUNK_THREAT_HUNTING_REFERENCE_GUIDE.md) |
| Syslog (with RHEL rsyslog) | Carries system and application activity into a local log file that Splunk can search. | [Simple syslog hunt](../security-operations/SYSLOG_HUNTING_GUIDE.md) |
| Zeek | Summarizes observed network conversations for later investigation. | [Zeek guide](../network-defense/ZEEK_DEPLOYMENT.md) |
| Wireshark | Lets an analyst inspect a permitted network capture in detail. | [Zeek and Wireshark](../network-defense/ZEEK_AND_WIRESHARK.md) |
| Arkime | Helps investigators search and review captured network sessions. | [Arkime hunting playbook](../arkime/HUNTING_PLAYBOOK.md) |
| RHEL 10.2 | Provides the Linux operating system for the Splunk lab server. | [RHEL and Splunk quick start](../../start-here/START_HERE_RHEL10v2.md) |
| Kali Linux | Provides an optional analysis workstation for the network tools. | [Kali deployment guide](../network-defense/KALI_DEPLOYMENT.md) |
| VMware Workstation Pro | Runs the lab computers as virtual machines on one host. | [Plan the virtual machines](../steps/03-plan-the-vm-resources.md) |
| AWS | Can provide cloud activity records, such as CloudTrail events, for an authorized investigation. | [AWS CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html) |
| Azure | Provides cloud services and activity records that may support an authorized investigation. | [Azure connection guide](../appendices/03-github-actions-openid-connect-with-azure.md) and [Microsoft Entra sign-in logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins) |
| VS Code | Helps you read and edit the lab's guides, searches and configuration examples. | [WSL and VS Code quick start](../../start-here/START_HERE_WSL.md) |

The core lab describes RHEL, Splunk, Windows and IdM virtual machines. Kali and network sensors are optional. The repository includes an optional Azure sign-in example for GitHub Actions; that example is **not** a cloud activity feed. AWS and Azure log collection into Splunk is not configured or validated by these files. Confirm the actual products, versions and data available in your environment.

## Worked cloud hunt guides

- [Review a new AWS IAM user](../security-operations/AWS_ACCOUNT_CREATION_HUNT.md)
- [Review an AWS IAM permission change](../security-operations/AWS_IAM_PERMISSION_CHANGE_HUNT.md)
- [Review a Microsoft Entra sign-in](../security-operations/AZURE_ENTRA_SIGN_IN_HUNT.md)

## A simple cloud hunting example

1. Agree with the cloud owner on the account, time period and records you may inspect.
2. Ask a question such as: “Was this cloud account change expected?” In AWS, CloudTrail event history can help review recent management activity for one account and Region. In Azure, the relevant evidence may include Microsoft Entra sign-in or audit records.
3. Compare the activity with authorized changes and other available evidence. A surprising event may have an ordinary explanation.
4. Explain what you observed, what you could not see, and who should review the next step.

CloudTrail event history covers management events, with a separate history for each Region and a 90-day window; other event types and longer retention need separate arrangements. See [AWS event history limits](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html). Check the customer's actual logging, retention, access and costs before planning a cloud hunt. Keep real account identifiers, credentials and raw records out of this public repository.
