# Complete GitHub Repository Creation and Copilot Integration Guide

**Repository:** `https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting`  
**Target branch:** `main`  
**Source document:** *RHEL 10.2 Splunk Threat Hunting Lab SOP* (52 steps plus Appendices A–G; revised November 1, 2026)  
**Package status:** Prepared scaffold. **No GitHub push or live Splunk deployment is implied.**

## Phase 1 — Review the existing repository

1. Open `https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting`.
2. Confirm the repository owner is `jbanday808`, branch is `main`, visibility is **Public**, and `LICENSE` already exists. Preserve the existing license and Git history.
3. Decide whether to publish the project as a public lab portfolio. Since the supplied SOP contains example passwords, **never upload the original document without redacting and rotating credentials as appropriate**.
4. Read the expected topology under `docs/reference/architecture.md` and `docs/reference/network-plan.md`. Do not change operational VM addresses merely to make docs match.

## Phase 2 — Install local development tools

On your Windows workstation, install **Git**, **Python 3**, and **Visual Studio Code**. The GitHub Copilot VS Code extension is optional but recommended for assisted editing. If available, use GitHub CLI for browser sign-in. Review any organization policy before connecting Copilot to sensitive files.

### Windows PowerShell checks

```powershell
git --version
python --version
code --version
gh --version
```

**Command Overview:** Each command prints the local version of the indicated tool. If one is missing, install it from its official publisher before continuing. `gh` is optional for the Git workflow.

## Phase 3 — Clone the existing GitHub repository

Open Windows PowerShell and run:

```powershell
$RepoPath = Join-Path $HOME 'Projects\rhel-10v2-splunk-threat-hunting'
New-Item -ItemType Directory -Path (Split-Path $RepoPath) -Force | Out-Null
git clone https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting.git $RepoPath
Set-Location $RepoPath
git status
```

**Command Overview:**

- `$RepoPath`: Defines the target local repository folder.
- `New-Item`: Creates the parent Projects directory if necessary.
- `git clone`: Copies the existing repository and preserves its Git history.
- `Set-Location`: Opens the local project directory.
- `git status`: Confirms the current branch and any pending changes.

**Expected result:** The local checkout contains `.git/` and the existing `LICENSE`. Do **not** manually replace or delete `.git/`.

> If the repo is already cloned, open that existing checkout and run `git pull --ff-only origin main` instead of cloning it again; review local uncommitted changes first.

## Phase 4 — Import all supplied files and folders

1. Download `rhel-10v2-splunk-threat-hunting-scaffold.zip` from the ChatGPT response.
2. Place it in your Windows Downloads folder.
3. Run the following, changing the ZIP path if needed:

```powershell
$ZipPath = Join-Path $HOME 'Downloads\rhel-10v2-splunk-threat-hunting-scaffold.zip'
$ImportPath = Join-Path $HOME 'Downloads\splunk-repo-import'
Expand-Archive -LiteralPath $ZipPath -DestinationPath $ImportPath -Force
$SourcePath = Join-Path $ImportPath 'rhel-10v2-splunk-threat-hunting'
Get-ChildItem -LiteralPath $SourcePath -Force |
    Copy-Item -Destination $RepoPath -Recurse -Force
Set-Location $RepoPath
```

**Command Overview:**

- `Expand-Archive`: Extracts the ZIP to a temporary import folder.
- `Get-ChildItem -Force`: Includes hidden GitHub files such as `.github/` and `.gitignore`.
- `Copy-Item -Recurse -Force`: Copies the prepared files and their subfolders into your *cloned* repository.
- `Set-Location`: Returns to the repository for validation.

**Expected result:** `README.md`, `.github/`, `apps/`, `hunts/`, `configs/`, `scripts/`, `docs/`, `evidence/sanitized/`, `sysmon/`, `tools/`, and `tests/` exist alongside the original `LICENSE`. The download does **not** contain `.git/`, so it cannot overwrite the existing Git history.

### Alternative: WSL/Linux

```bash
git clone https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting.git
cd rhel-10v2-splunk-threat-hunting
mkdir -p /tmp/splunk-repo-import
unzip /mnt/c/Users/YOUR_WINDOWS_USERNAME/Downloads/rhel-10v2-splunk-threat-hunting-scaffold.zip -d /tmp/splunk-repo-import
cp -a /tmp/splunk-repo-import/rhel-10v2-splunk-threat-hunting/. ./
```

**Command Overview:** `mkdir -p` creates the import folder; `unzip` extracts the package; `cp -a .../. ./` copies all files **including dotfiles** into the cloned repo. Replace `YOUR_WINDOWS_USERNAME` with the actual Windows profile folder name. If already cloned, skip `git clone` and use the existing checkout.

## Phase 5 — Verify the complete structure

From the repository root:

```powershell
python tools/validate_repository.py
python -m unittest discover -s tests -v
git status --short
```

**Command Overview:** The first command checks required files, sample XML, basic index names, ignored private artifacts and obvious secret patterns; the second runs simple tests; the third shows new or changed Git files.

**Expected result:** Static validation reports **PASS**. A pass does **not** prove that Splunk services, LDAPS, forwarders, dashboards or hunts work.

Review the complete list in `FILE_MANIFEST.json` and the folder map below. Git does not track empty folders; every intended published folder therefore contains at least one tracked file.

## Phase 6 — Review public-repository safety

1. Read `SECURITY.md`, `docs/reference/security-and-sanitization.md` and `.gitignore`.
2. Confirm the source package contains no real password, HEC token, LDAP bind password, SSH key, CA private key, Splunk secret, private log or backup.
3. Confirm raw outputs stay **outside Git**: `evidence/raw/`, `private/`, `backups/`, `downloads/` and any original SOP with credentials.
4. If any actual password shown in the source SOP was used, rotate it before publication.
5. Do not commit a failing validation result as a successful test. Leave unverified checks **Pending**.
6. Inspect new files and the staged diff carefully; `.gitignore` does not prevent leaks in previously tracked files.

## Phase 7 — Publish to the GitHub main branch

```powershell
git add README.md .gitignore .gitattributes .editorconfig SECURITY.md CONTRIBUTING.md AGENTS.md FILE_MANIFEST.json .github apps configs docs evidence/sanitized hunts samples scripts sysmon tests tools
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "Add RHEL 10.2 Splunk threat hunting lab scaffold"
git push origin main
```

**Command Overview:**

- `git add`: Stages only the reviewed project files and folders.
- `git diff --cached --check`: Catches whitespace problems in staged files.
- `git diff --cached --stat`: Summarizes files changed.
- `git diff --cached`: Displays the exact content being committed; look for credentials before proceeding.
- `git commit`: Saves a local Git revision.
- `git push`: Uploads the commit to your repository's `main` branch.

**Expected result:** GitHub shows the project files on `main`, and the original MIT `LICENSE` remains present. If branch protection or another contributor's changes prevent a push, make a new branch and open a pull request instead of forcing an update.

### Authentication

If Git requires authentication, use Git Credential Manager or the browser-based `gh auth login` flow. Do not type access tokens into README files, shell histories or command arguments intended for publication.

## Phase 8 — Make GitHub Copilot use the repository context

1. Open Visual Studio Code.
2. Choose **File → Open Folder** and select the cloned `rhel-10v2-splunk-threat-hunting` folder.
3. Sign in to the GitHub Copilot extension with the eligible GitHub account.
4. Confirm `.github/copilot-instructions.md` appears in the Explorer.
5. Open Copilot Chat and ask it to read `README.md`, `docs/reference/deployment-order.md`, `docs/reference/architecture.md`, and `.github/copilot-instructions.md` before suggesting changes.
6. Use the reusable prompts in `.github/prompts/` when available in your VS Code version.
7. Check Copilot Chat references to confirm that `.github/copilot-instructions.md` was used. Copilot cannot assume the live lab passed validation from repository text alone.

**Suggested Copilot prompt:**

> Review this RHEL 10.2 Splunk threat-hunting repository using the README, the Copilot instructions, and the 52-step deployment plan. Check filenames, cross-file consistency, security risks, and missing documentation. Propose changes as small reviewed diffs. Do not deploy anything, invent validation results, or include secrets.

**Important distinction:** Having a repository connected to ChatGPT does **not** mean the active GitHub Copilot Chat session is synchronized. Saving repository-wide instructions and opening the checkout in VS Code provides a shared context for future Copilot interactions.

## Phase 9 — Add live evidence gradually

1. On the RHEL Splunk VM, verify `findmnt --mountpoint /splunkdata`, service status and version.
2. Verify Splunk configuration through `sudo -u splunk /opt/splunk/bin/splunk btool check` before a planned restart.
3. On WINHUNT01, validate the forwarder service, trusted certificate, Sysmon and Windows event channels.
4. Run `hunts/*.spl` in Splunk Search and capture exact sanitized observations.
5. For IdM, test verified LDAPS, mapped roles, denied access and local administrator recovery.
6. Save redacted screenshots under `docs/images/` using `docs/reference/screenshot-naming.md`; use single-sentence figure captions.
7. Change an evidence result from **Pending** only after actual observation, then commit updated records.

## Phase 10 — Keep GitHub and local Copilot work in sync

After editing files locally:

```powershell
git status
git pull --ff-only origin main
python tools/validate_repository.py
git add .
git diff --cached --check
git diff --cached
git commit -m "Document verified Splunk lab results"
git push origin main
```

**Command Overview:** Check the repo, fetch only compatible remote updates, validate, review changes, commit, then upload. Do not use `git add .` until you have reviewed local untracked files for secrets.

## How the source SOP maps to the repo

| SOP phase | File groups |
| --- | --- |
| Steps 1–9 | `README.md`, `docs/reference/network-plan.md`, `docs/deployment.md`, `.gitignore` |
| Steps 10–20 | `apps/LAB_SIEM/`, `configs/rsyslog/`, `configs/logrotate/`, `scripts/rhel/` |
| Steps 21–30 | `apps/LAB_UF_WINDOWS/`, `sysmon/`, `hunts/00`–`hunts/08`, dashboard XML |
| Steps 31–44 | `docs/ldap-integration.md`, `docs/ldap-*.example`, `evidence/sanitized/ldap-validation.md` |
| Steps 45–52 | Optional alert, backup helper, `docs/reference/versions.md`, `evidence/sanitized/validation.md` |
| Appendices A–G | `docs/optional/`, `configs/nginx/`, `configs/redaction/`, `hunts/09`–`hunts/12` |

### Reference

**RHEL 10.2 Splunk Threat Hunting Lab SOP:** Your supplied 150-page, revised November 1, 2026 guide describing lab deployment, validation and optional experiments.

**GitHub Copilot documentation:** GitHub's repository custom instructions guide explains `.github/copilot-instructions.md` and reusable prompt files: https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/configure-custom-instructions/add-repository-instructions-in-your-ide

**Splunk documentation:** Official product reference for checking Splunk apps, configurations and installed build compatibility: https://help.splunk.com/
