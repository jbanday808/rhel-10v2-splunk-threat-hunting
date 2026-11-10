## Appendix Use the complete ZIP on Windows and upload to GitHub

The downloadable `rhel-splunk-threat-hunting-complete.zip` contains an assembled source project named `rhel-splunk-threat-hunting`. It includes the complete Word and Markdown guides, all 52 step files, configuration files, scripts, hunting searches, LDAP examples, NGINX overrides, and GitHub Actions workflows.

Vendor operating-system images, Splunk installers, vendor add-on packages, certificates, and live credentials are obtained or generated on your machines using the guide. Their download and setup instructions are included in the project.

### Package step 1 Download and extract on Windows 11

Save the ZIP in your Windows Downloads folder. Use **Extract All** in File Explorer, or open Windows PowerShell and run:

```powershell
$ZipFile = Join-Path $env:USERPROFILE 'Downloads\rhel-splunk-threat-hunting-complete.zip'
$ExtractRoot = Join-Path $env:USERPROFILE 'Documents\SIEMLab-Complete'

if (Test-Path -LiteralPath $ExtractRoot) {
    throw 'Choose a new extraction folder to preserve existing work.'
}

Expand-Archive -LiteralPath $ZipFile -DestinationPath $ExtractRoot
$Project = Join-Path $ExtractRoot 'rhel-splunk-threat-hunting'
Set-Location -LiteralPath $Project
Get-ChildItem -Force
```

**Command overview:** `Join-Path` builds paths for your Windows account; `Test-Path` checks for an existing folder; `Expand-Archive` extracts the ZIP; `Set-Location` opens the project; `Get-ChildItem -Force` shows all entries, including `.github`.

Open **start-here/START_HERE_WINDOWS.md** first in the current GitHub layout. The `.zip` itself is a download package; GitHub receives the extracted project contents.

### Package step 2 Review the included folders

| Folder or file | Contents |
| --- | --- |
| `README.md` | Project purpose, deployment order, and links. |
| `start-here/START_HERE_WINDOWS.md` | Windows extraction, checks, and GitHub upload instructions. |
| `apps/LAB_SIEM` | Splunk server settings, role, permissions, and dashboard. |
| `apps/LAB_UF_WINDOWS` | Windows event inputs and verified TLS forwarding settings. |
| `apps/Splunk_TA_nginx/local` | Custom NGINX inputs to apply after installing the vendor add-on. |
| `configs` | rsyslog, log rotation, NGINX, and systemd examples. |
| `scripts/rhel` | Storage preparation, backups, deployment checks, and NGINX helpers. |
| `scripts/windows` | Audit setup, Sysmon, forwarder deployment, lab activity, and package checks. |
| `scripts/azure` | OIDC identity-setup and trust instructions. |
| `sysmon` | The lab's Sysmon XML configuration. |
| `hunts` | Original hunting searches plus NGINX and integrity searches. |
| `docs/steps` and `docs/appendices` | The full procedures split into numbered files. |
| `docs` | The full Word and text guides, architecture, version records, and LDAP examples. |
| `evidence/sanitized` | Validation and investigation templates with results marked Pending. |
| `.github/workflows` | Linux and Windows project checks, OIDC inspection, and Azure OIDC validation. |
| `FILE_MANIFEST.json` | Initial file list and SHA-256 values for package verification. |

The package has the final assembled custom files. When using those files, follow the guide's installation, review, and deployment instructions; you can skip recreating a file with a `cat >` block when the included file already supplies it. Retain later additions if you choose to recreate earlier configuration files. The packaged `[lab]` index includes the integrity setting described in its appendix.

### Package step 3 Verify the extracted files

Read `scripts/windows/Test-Project.ps1`, then run it from the extracted project in Windows PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\windows\Test-Project.ps1 -VerifyManifest
```

**Command overview:** `-NoProfile` opens a clean PowerShell process; `-ExecutionPolicy Bypass` permits this reviewed local check in that process; `-File` selects the validator; `-VerifyManifest` checks initial file hashes. It does not change the machine's persistent execution policy.

The validator checks required files, parses the PowerShell scripts and XML, and optionally verifies the initial manifest. On RHEL or WSL, run `python3 scripts/validate_project.py --verify-manifest` for Python, shell, XML, JSON, and project configuration checks. A source check does not replace the live Splunk, NGINX, Windows, or Azure validation steps.

The manifest describes the downloaded release. Editing a file changes its hash; use normal validation without `-VerifyManifest` after making your own changes.

### Package step 4 Install Git and GitHub CLI

On the physical Windows host, install Git for Windows and GitHub CLI from their official installers, or use WinGet:

```powershell
winget install --id Git.Git --exact --source winget
winget install --id GitHub.cli --exact --source winget
```

Close and reopen PowerShell so it picks up the installed command paths. Return to the extracted project, then check and authenticate:

```powershell
git --version
gh --version
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
gh api user --jq .login
```

**Command overview:** `winget install` installs the named tools; the version commands confirm them; `gh auth login` opens GitHub sign-in; `gh auth setup-git` connects Git to that authentication; `gh api user` displays the signed-in account.

Confirm the correct account before uploading. If the owner or repository name differs from the OIDC example, update both OIDC workflow guards and capture the actual subject before configuring Azure trust.

### Package step 5 Initialize and review a new local repository

From the extracted project root, use these commands only when it has no existing `.git` directory:

```powershell
git init -b main
git config user.name 'James Banday'
$CommitEmail = Read-Host 'Your verified GitHub email or GitHub noreply email'
git config user.email $CommitEmail

git add .
git diff --cached --check
git diff --cached --stat
git status --short
```

**Command overview:** `git init` creates the local repository and its main branch; `git config` sets this project's author details; `git add` stages included files; `git diff` checks and summarizes them; `git status` shows what will be committed.

Inspect the staged list. The included `.gitignore` excludes generated keys, certificates, installers, live authentication settings, backups, and raw evidence. Keep credentials out of source files. The `.gitattributes` file keeps shell files in Linux format and PowerShell files in Windows format.

### Package step 6 Commit and upload the extracted project

For a new GitHub repository:

```powershell
git commit -m 'Add complete RHEL Splunk lab with LDAP NGINX and Azure OIDC'

gh repo create rhel-splunk-threat-hunting `
  --private --source . --remote origin --push

gh repo view --web
```

**Command overview:** `git commit` records the reviewed project; `gh repo create` creates a private GitHub repository; `--source .` uses the extracted project; `--remote origin` connects it; `--push` uploads the commit; `gh repo view --web` opens the repository.

If that repository already exists, preserve it by cloning it into a separate folder first with `gh repo clone OWNER/REPOSITORY`. Copy and merge the extracted source files into that checkout, review `git status` and `git diff`, and commit and push there. Do not replace its `.git` directory or force-push over its history. For authentication that needs workflow-file permission, use `gh auth refresh --scopes workflow` and complete its sign-in.

Use the command-line upload so `.github`, nested configuration folders, and all source files are included together. Git tracks files rather than empty folders; `.gitkeep` files preserve the intended non-private empty folders in this package.

### Package step 7 Confirm GitHub and follow the deployment order

Open the repository's **Actions** tab and inspect **Validate project**. It checks source files on GitHub-hosted Linux and Windows machines. Its result does not claim the lab VMs are already deployed. Run the two OIDC workflows manually only after following the OIDC appendix in order.

Then follow these stages:

1. Complete VMware, networking, RHEL, storage, certificates, and the Splunk server through Step 20.
2. Configure the Windows endpoint, forwarder, Sysmon, hunting activity, and dashboard through Step 30.
3. Configure and validate IdM and LDAPS through Step 44.
4. Complete alerts, cleanup, backup, final checks, and documentation through Step 52.
5. Follow the data-phase, integrity, NGINX, and OIDC appendices as needed, recording actual results in the included evidence templates.

The RHEL helpers live under `scripts/rhel`, and Windows helpers live under `scripts/windows`. Their README files identify where each runs and its prerequisites. Storage formatting and credential-dependent operations remain explicit steps in the guide.

**Summary:** Extract the ZIP, review and validate the files, authenticate GitHub, commit the project, upload it, and then document the results of each live lab procedure.

References:

- [GitHub Local Project Upload Guide](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github): This guide explains importing a local project through Git and GitHub CLI.
- [GitHub Repository Creation Manual](https://cli.github.com/manual/gh_repo_create): This manual explains `--source`, `--remote`, and `--push`.
- [Git for Windows](https://git-scm.com/install/windows): This page provides the official Windows Git installer.
- [GitHub CLI Installation](https://cli.github.com/): This page provides GitHub CLI installation options.

---
