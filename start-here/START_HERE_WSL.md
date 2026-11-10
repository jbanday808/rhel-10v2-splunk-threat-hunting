# START HERE — VS Code + WSL on Windows 11

This is the preferred guide for the owner of the existing public repository:

**https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting**

1. Read [the complete VS Code + WSL upload guide](../docs/reference/WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md).
2. Install/check Ubuntu WSL, VS Code Remote - WSL, `git`, `gh`, `unzip`, `rsync`, and `python3`.
3. Clone the **existing** GitHub repository into `~/projects` (do not use `git init`).
4. Extract the complete project ZIP into a separate staging folder.
5. Copy the staged files into the clone while **keeping `.git` and the remote's MIT `LICENSE` unchanged**.
6. Run `python3 scripts/validate_project.py`, `python3 -B -m unittest discover -s tests -v`, and the public-repo preflight.
7. Check all screenshots, Markdown, DOCX, configuration examples and Git changes before the push.
8. Commit and push to `origin main` from the WSL terminal.

**Important:** The ZIP contains project source, documentation, screenshots, and tests. It does not include private keys, real credentials, or Splunk/Windows vendor installers. Deployment to RHEL-SPLUNK01 / WINHUNT01 / RHEL-IDM01 must be done separately in the owned lab.
