# Threat Hunting Lab and Trellix Consultant Guide

## Reusable GitHub Action

**RHEL Splunk Threat Hunting Source Check** validates this lab's source layout and example configuration in GitHub Actions. It checks required files, Python/XML/JSON syntax, shell syntax when Bash is available, the six lab indexes, and selected TLS, redaction, and ingestion settings. It runs offline and needs no Splunk credentials.

```yaml
permissions:
  contents: read

jobs:
  source-check:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - name: Check lab source
        id: lab
        uses: jbanday808/rhel-10v2-splunk-threat-hunting@v1
        with:
          path: '.'
          verify-manifest: 'false'
```

Use this action for this lab or forks that retain its layout. Ubuntu 24.04 provides the required Bash and Python 3.10 or newer. Inputs are `path` (default `.`; inside the checked-out workspace) and `verify-manifest` (default `false`; only for the unchanged original download). Outputs are `result` (`passed` or `failed`) and `error-count`. Validation errors fail the step and add a count to the job summary. See the [action guide](docs/custom-github-action.md) for details, versioning, and release review steps. The action does not verify live deployments or provide a complete security audit.

## Lab and consultant guides

Threat hunting means looking for signs of an attack that may not have raised an alert. This repository contains a practice lab, example searches, and guides for explaining a hunt to customers and decision-makers.

## Choose where to start

| I want to… | Start here |
| --- | --- |
| Understand the Trellix threat hunter or consultant role | [Plain-language guide and PowerPoint](presentations/trellix-threat-hunting/README.md) |
| Learn how to plan and report a hunt | [Threat-hunting method](docs/security-operations/THREAT_HUNTING_METHOD.md) and [report template](docs/security-operations/templates/threat-hunt-report.md) |
| Explore sample hunting searches | [Splunk hunting reference](docs/reference/SPLUNK_THREAT_HUNTING_REFERENCE_GUIDE.md) and [hunt searches](hunts/) |
| Check whether records are ready for a hunt | [Event time and arrival guide](docs/reference/SEARCH_TIME_AND_INGESTION_LAG.md), [data-health search](hunts/00-data-health.spl), and [endpoint acceptance checks](docs/security-operations/endpoint-acceptance/README.md) |
| Learn to use syslog in a hunt | [Syslog practice guide](docs/security-operations/SYSLOG_HUNTING_GUIDE.md) |
| Build the practice lab | [Lab quick start](start-here/START_HERE_RHEL10v2.md) and [52-step guide](docs/steps/README.md) |
| Investigate network activity | [Network hunting guide](docs/network-defense/README.md) and [Arkime playbook](docs/arkime/HUNTING_PLAYBOOK.md) |
| Practice a guided hunt | [Current TraceVector Site](https://tracevector.jamesbanday.chatgpt.site/), [ten real-lab follow-up guides](docs/network-defense/tracevector-hunts/README.md), and [source](website/tracevector-lab/) |
| Review optional cloud identity hunts | [AWS account creation](docs/security-operations/AWS_ACCOUNT_CREATION_HUNT.md), [AWS permission changes](docs/security-operations/AWS_IAM_PERMISSION_CHANGE_HUNT.md), [Entra sign-ins](docs/security-operations/AZURE_ENTRA_SIGN_IN_HUNT.md), and [Entra role changes](docs/security-operations/AZURE_ENTRA_ROLE_CHANGE_HUNT.md) |
| Understand the tools, including AWS and Azure | [Tools and cloud hunting overview](docs/reference/tools-and-cloud.md) |

The [Trellix PowerPoint](presentations/trellix-threat-hunting/Trellix_Customer_Product_Brief.pptx) is a 56-slide customer product guide. The accompanying guide identifies the most useful slides for a threat-hunting conversation and explains the role in everyday language.

## How a hunt works

1. **Agree on the question.** For example: “Did someone misuse an employee account?”
2. **Look for clues.** Review the permitted records, such as sign-in and device activity.
3. **Check the story.** Compare the clues with normal activity and gather enough context to decide what they mean.
4. **Explain the result.** Share what was found, what remains uncertain, and what the customer can consider doing next.

An unusual event is a clue, not proof of an attack. Run tests only in an authorized environment and keep customer records and credentials out of this public repository.

## What is in the repository

| Folder | Purpose |
| --- | --- |
| [presentations](presentations/trellix-threat-hunting/) | Trellix customer presentation and plain-language role guide |
| [docs](docs/steps/README.md) and [start-here](start-here/README.md) | Lab instructions, hunting methods, investigation guides and templates |
| [hunts](hunts/) and [rules](rules/) | Sample searches and detection rules |
| [apps](apps/), [configs](configs/) and [sysmon](sysmon/) | Example settings used by the lab |
| [scripts](scripts/) and [tests](tests/) | Lab helpers and source checks |
| [examples](examples/), [evidence](evidence/sanitized/) and [screenshots](screenshots/) | Synthetic examples, validation templates and lab images |
| [website](website/) | Source for the guided threat-hunting and network-analysis workbenches |

The core practice environment describes Splunk on RHEL, a Windows endpoint, and a directory server. The six Splunk indexes are `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`. The files describe a lab and proposed exercises; they do not demonstrate a live deployment or a completed customer engagement. Trellix products are discussed in the presentation and have not been validated in this lab.

The guides retain Zeek, Wireshark, Splunk Enterprise, Arkime, RHEL 10.2, Kali Linux, VMware Workstation Pro, AWS, Azure and VS Code. Cloud log collection is a separate, unvalidated option; the existing Azure connection example does not automatically send cloud logs to Splunk.

<a id="validate-and-publish"></a>

## Check the files

From the repository root on RHEL or WSL:

```bash
python3 scripts/validate_project.py
python3 -B -m unittest discover -s tests -v
python3 tools/publication_preflight.py
```

These commands check the source files without connecting to the lab. Record live results only after observing them. The historical `FILE_MANIFEST.json` describes the original download, so its optional manifest check applies to that unchanged package. Before publishing evidence, follow the [sanitization checklist](docs/reference/security-and-sanitization.md).
