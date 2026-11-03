# GitHub Copilot instructions — RHEL 10.2 Splunk Threat Hunting Lab

You are editing a public security-engineering portfolio project based on a 52-step SOP. Keep examples readable, evidence-based and secure.

- Infrastructure: VMware Workstation Pro VMnet8 `172.25.250.0/24`; RHEL Splunk `.10`; Windows `.20`; IdM `.30`; gateway `.2`.
- Six index names must remain `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, `lab`.
- Splunk app paths use `apps/LAB_SIEM/` and `apps/LAB_UF_WINDOWS/`; optional experiments must be explicitly labeled optional.
- Explain commands in simple language and state what expected **testable** result looks like.
- Do not claim deployments, security scans, alerts, connections, or tests completed without observed evidence.
- Never output or commit plaintext passwords, CA/private keys, Splunk tokens, LDAP binding secrets, GitHub secrets, raw logs, endpoint identifiers or unredacted screenshots.
- Keep templates under `docs/*.example` or `configs/**/*.example` if they are not intended to be deployed as-is.
- Prefer least privilege, TLS verification, SELinux Enforcing, input/source validation, and private backups.
- Never overwrite existing on-host configuration without backup and merge review. Never format a disk as a repair action.
- Check `.gitignore`, `SECURITY.md`, and `python3 scripts/validate_project.py` before recommending a commit.
- Scope all activity generation and hunting demonstrations to the owned isolated lab.
- Ask for verified Splunk version and existing stanzas before changing installation-specific settings.
- Provide a brief Command Overview and Summary when explaining shell or PowerShell commands.

- The source ZIP includes all 52 `docs/steps/*.md`, seven `docs/appendices/*.md`, and evidence screenshots under `screenshots/`.
- The authoritative repository is `jbanday808/rhel-10v2-splunk-threat-hunting` on `main`; do not initialize a new GitHub repository.
- Do not change real IdM, Azure OIDC, or Splunk service settings through editing repository files alone.
- Before publication, run `python3 scripts/validate_project.py`, `python3 -B -m unittest discover -s tests -v`, and `python3 tools/publication_preflight.py`.
