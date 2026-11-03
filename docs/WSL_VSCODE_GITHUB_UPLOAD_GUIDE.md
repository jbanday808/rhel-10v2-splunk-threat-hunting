# Complete VS Code + WSL guide — RHEL 10.2 Splunk Threat Hunting Lab

**Project:** `rhel-10v2-splunk-threat-hunting`  
**GitHub:** https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting  
**Platform:** Windows 11 + Ubuntu WSL + VS Code (Remote WSL).  
**Purpose:** Merge the supplied, expanded project ZIP into the **existing** GitHub repository while preserving the MIT `LICENSE` and Git history.

## 1. What you already have, and what was added

The original ZIP contained 183 files, including 52 numbered deployment steps, seven appendices, 13 `.spl` searches, and 22 screenshots. Those have been preserved. New items include GitHub Copilot instructions and prompts, `SECURITY.md`, `CONTRIBUTING.md`, `AGENTS.md`, screenshot index, publication checklists, diagram, VS Code extension suggestions, a WSL verification script, and this guide. The old OIDC workflow repository guard was corrected to `jbanday808/rhel-10v2-splunk-threat-hunting`.

**The ZIP deliberately omits LICENSE** because your existing GitHub `main` branch already contains an MIT `LICENSE` file. Keep that original file. No live deployment, LDAP authentication, Splunk alert, Azure login, or endpoint collection has been performed by creating this ZIP.

## 2. Know which machine runs each command

| Computer | Tasks |
| --- | --- |
| Windows 11 physical host | Download ZIP; VMware Workstation; manage the VMnet8 NAT network |
| Ubuntu WSL + VS Code | Edit files; use Git/GitHub; run Python static tests; review; publish |
| RHEL-SPLUNK01 | Install/configure Splunk Enterprise; XFS /splunkdata; indexes, certificates, logging |
| WINHUNT01 | Configure Windows audit logging, Sysmon and Universal Forwarder |
| RHEL-IDM01 | Configure IdM, DNS, CA, LDAP groups and directory accounts |
| Splunk Web | Configure admin, LDAP strategy, dashboards and alerts after validation |

Never run the VM configuration scripts on your Windows physical host or in WSL. The `scripts/windows/*.ps1` files are intended for the dedicated Windows lab VM when explicitly documented.

## 3. Prepare Windows 11 and VS Code

1. Open **PowerShell** on Windows, not a WSL terminal. Run `wsl --status` and `wsl --list --verbose`. If WSL is not installed, run `wsl --install -d Ubuntu` in administrator PowerShell, restart as prompted, create a Linux username, and reopen Ubuntu.
2. Install VS Code on Windows and its **WSL** extension. Optional: GitHub Copilot and YAML/Python extensions.
3. Open Ubuntu (WSL) from the Start menu. Run `pwd` and `uname -a` to confirm a Linux shell.
4. Work in **`~/projects`**, the WSL/Linux filesystem, rather than under `/mnt/c`, for better Git performance and consistent Linux permissions.
5. Download **the completed ZIP** using your browser and copy its path; use the ZIP included in this response, not the original smaller source ZIP.

**Command overview:** `wsl --status` checks the installation; `wsl --install -d Ubuntu` installs the Linux distribution; `pwd` displays your current directory.

## 4. Install Git, GitHub CLI, ZIP tools, and Python in WSL

Open a WSL terminal (or VS Code terminal labeled `WSL: Ubuntu`), then run:

```bash
sudo apt update
sudo apt install -y git gh unzip rsync python3 tree
git --version
gh --version
python3 --version
```

**Explanation:** `apt update` refreshes package information; `apt install -y` installs the named packages; `git` manages source changes; `gh` logs in to GitHub; `unzip` extracts your project; `rsync` copies the files without deleting remote content; `python3` runs validation; `tree` displays folders.

If Ubuntu's package repository does not provide `gh`, install GitHub CLI using its official distribution instructions rather than a third-party package source.

## 5. Configure Git, then authenticate to GitHub

```bash
git config --global user.name 'James Banday'
read -r -p 'Your verified GitHub email or GitHub noreply email: ' COMMIT_EMAIL
git config --global user.email "$COMMIT_EMAIL"
unset COMMIT_EMAIL
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
gh auth status
```

**Explanation:** `git config` sets the public author name and your selected verified/private commit email; `read` obtains the email without hardcoding it; `gh auth login --web` opens GitHub browser authentication; `gh auth setup-git` configures Git credential use; `gh auth status` checks the connection. Never paste tokens into project files.

## 6. Clone the existing GitHub repository (do not create a new one)

```bash
mkdir -p "$HOME/projects"
cd "$HOME/projects"
gh repo clone jbanday808/rhel-10v2-splunk-threat-hunting
cd rhel-10v2-splunk-threat-hunting
git remote -v
git branch --show-current
git status --short
ls -la
```

**Expected:** The remote points to `jbanday808/rhel-10v2-splunk-threat-hunting`, the branch is `main`, the working tree is clean, and `LICENSE` is present. If the folder already exists, **do not rerun `gh repo clone`**: enter the folder, check `git status`, and preserve existing work. Resolve uncommitted edits before merging.

**Explanation:** `mkdir -p` creates the projects folder; `cd` enters it; `gh repo clone` downloads existing history; `git remote -v` confirms destination; `git status --short` shows pending local modifications.

## 7. Locate the completed ZIP from WSL

If your browser saved the ZIP to Windows Downloads, get that directory by running:

```bash
WIN_PROFILE="$(powershell.exe -NoProfile -Command '$env:USERPROFILE' | tr -d '\r')"
WIN_DOWNLOADS="$(wslpath -u "$WIN_PROFILE")/Downloads"
printf 'Windows Downloads from WSL: %s\n' "$WIN_DOWNLOADS"
ls -lh "$WIN_DOWNLOADS"/*.zip
```

**Explanation:** `powershell.exe` obtains your Windows user directory; `tr -d '\r'` removes Windows-style carriage returns; `wslpath -u` converts the Windows path into a WSL path; `ls -lh` lists ZIP files.

If your ZIP is in another folder, enter its full WSL path directly, such as `/mnt/c/Users/<WindowsUser>/Downloads/rhel-10v2-splunk-threat-hunting-complete.zip`. **Do not copy the example path without replacing `<WindowsUser>`.**

## 8. Extract the ZIP to a separate staging location

Return to WSL, then run:

```bash
cd "$HOME/projects/rhel-10v2-splunk-threat-hunting"
read -r -p 'Full WSL path to completed ZIP: ' ZIP_PATH
test -f "$ZIP_PATH" || { echo 'ZIP not found'; exit 1; }
IMPORT_DIR="$(mktemp -d "$HOME/projects/splunk-import.XXXXXX")"
unzip -q "$ZIP_PATH" -d "$IMPORT_DIR"
test -f "$IMPORT_DIR/rhel-10v2-splunk-threat-hunting/README.md"
printf 'Import folder: %s\n' "$IMPORT_DIR"
```

**Explanation:** `read` saves the actual path supplied by you; `test -f` checks the ZIP; `mktemp -d` creates a unique staging directory; `unzip -q` extracts without overwriting your Git clone.

Do not unzip directly on top of the cloned checkout. This keeps Git history, your license, and existing changes safe.

## 9. Review the merge before copying into the clone

```bash
cd "$HOME/projects/rhel-10v2-splunk-threat-hunting"
rsync -avn --exclude='.git/' --exclude='LICENSE' \
  "$IMPORT_DIR/rhel-10v2-splunk-threat-hunting/" ./
```

**Explanation:** `rsync` copies files; `-a` preserves directory structure, `-v` displays paths, and `-n` is a **dry run** (no files are changed). The exclusions preserve `.git` and the remote `LICENSE`. No `--delete` option is used, so unrelated existing files are not removed.

If the dry-run listing is correct, perform the merge:

```bash
rsync -av --exclude='.git/' --exclude='LICENSE' \
  "$IMPORT_DIR/rhel-10v2-splunk-threat-hunting/" ./
```

**Expected:** The complete source, `docs/steps`, `docs/appendices`, `screenshots`, `.github`, and new Copilot files appear in your checkout. Your original `.git/` and `LICENSE` remain unchanged.

## 10. Open the complete project in VS Code WSL

```bash
cd "$HOME/projects/rhel-10v2-splunk-threat-hunting"
code .
```

Check VS Code shows **WSL: Ubuntu** (not a Windows-only local workspace). In the Explorer sidebar, inspect these folders:

```text
rhel-10v2-splunk-threat-hunting/
├── .github/
│   ├── instructions/
│   ├── prompts/
│   ├── workflows/
│   └── copilot-instructions.md
├── .vscode/extensions.json
├── apps/LAB_SIEM/                # Splunk server app, TLS, indexes, dashboard
├── apps/LAB_UF_WINDOWS/          # Windows forwarder configuration
├── apps/Splunk_TA_nginx/         # Optional NGINX lab overlay
├── configs/                      # Linux logging, TLS examples, optional configurations
├── docs/
│   ├── appendices/               # 7 optional appendices
│   ├── steps/                    # 52 numbered steps
│   ├── images/                   # Reserved for new sanitized documentation screenshots
│   └── WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md
├── evidence/sanitized/          # Result templates, not raw logs
├── examples/                    # Synthetic events and examples
├── hunts/                       # 13 SPL searches
├── screenshots/                 # 22 author-provided screenshots
├── scripts/                     # RHEL, Windows, Azure and WSL helper scripts
├── sysmon/sysmon.xml
├── tests/
├── tools/publication_preflight.py
├── README.md
├── START_HERE_WSL.md
├── SECURITY.md
├── CONTRIBUTING.md
├── AGENTS.md
└── LICENSE                      # Existing GitHub license retained after merge
```

**Create folders manually in VS Code if needed:** right-click the repository root in Explorer → **New Folder**, type the relative folder path (for example `.github/prompts`); right-click that folder → **New File**, enter the exact name. Terminal alternative: `mkdir -p .github/prompts docs/images scripts/wsl tools`, then `touch docs/images/.gitkeep`. However, **the supplied completed ZIP already contains these files and folders**, so normally you only need the merge above. `touch` does not populate meaningful file contents; use the included complete files.

## 11. Run checks before staging changes

```bash
cd "$HOME/projects/rhel-10v2-splunk-threat-hunting"
python3 scripts/validate_project.py
python3 scripts/validate_project.py --verify-manifest
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
bash scripts/wsl/verify-repository.sh
```

**Explanation:** the project validator checks the original source design; `--verify-manifest` checks release hashes **before you edit any files**; `unittest` exercises offline Python tests; the WSL script counts key files and runs a first-pass publication check. These checks **do not connect to the lab** or prove LDAP, Windows collection, or Splunk service health.

Check the folders manually:

```bash
find docs/steps -maxdepth 1 -name '[0-9][0-9]-*.md' -type f | wc -l
find docs/appendices -maxdepth 1 -name '[0-9][0-9]-*.md' -type f | wc -l
find hunts -maxdepth 1 -name '*.spl' -type f | wc -l
find screenshots -maxdepth 1 -name '*.png' -type f | wc -l
tree -a -L 3 -I '.git|__pycache__'
```

**Expected counts:** 52 numbered steps, 7 appendices, 13 hunting `.spl` files, and 22 PNG screenshots.

## 12. Review privacy and secrets before making a public commit

The GitHub repository is **public**. Review the included DOCX, Markdown, YAML, configuration examples and each screenshot. In particular:

- Remove real passwords, LDAP bind account secrets, Splunk HEC tokens, Azure secrets, certificate private keys, recovery keys, and raw exported logs.
- Scrub identifying event contents, personal email addresses, browser credentials and any unwanted public identifiers from screenshots.
- Keep `private/`, `backups/`, `downloads/`, `evidence/raw/`, VMware virtual disks and installers excluded.
- The ZIP contains sanitized instructions and sample test data, but a first-pass automated check cannot guarantee that every screenshot is safe.
- `.gitignore` does **not** remove content from history if it was previously committed. Rotate real credentials previously published anywhere.
- The OIDC workflow branch guards now reference the **current** GitHub repository. An existing Azure federated trust tied to the older name needs separate review before enabling OIDC.

After copying into the Git checkout:

```bash
python3 tools/publication_preflight.py
git status --short
git diff -- .github/workflows/oidc-claims.yml
git diff -- .github/workflows/azure-oidc.yml
```

**Explanation:** the preflight rejects selected dangerous file types and obvious secret patterns, but is **not** a substitute for reviewing images or documents.

## 13. Stage, inspect, and publish to the existing repo

Review changes **before** committing:

```bash
git add -A
git diff --cached --check
git diff --cached --stat
git diff --cached
```

**Explanation:** `git add -A` stages new, changed and deleted files; `--check` detects formatting errors; `--stat` summarizes what will be published; `git diff --cached` reveals the actual staged changes. If anything is sensitive, remove it before continuing.

Once you approve the staged changes:

```bash
git commit -m 'Complete RHEL 10.2 Splunk threat hunting lab project'
git push -u origin main
gh repo view jbanday808/rhel-10v2-splunk-threat-hunting --web
```

**Explanation:** `git commit` records the changes; `git push -u origin main` sends your commit to the **existing** GitHub `main` branch; `gh repo view --web` opens the updated repo. You may be asked to authenticate in your browser. Do not force-push; if the branch changed remotely, fetch and reconcile first.

## 14. Confirm publication on GitHub

On the GitHub Code tab check the README renders, `LICENSE` is still present, `.github/copilot-instructions.md` exists, there are 52 steps and 13 hunts, the screenshots appear as image files, and the Actions validation workflow reflects your latest commit. Do not enable Azure OIDC or upload raw log evidence as part of this check.

If `git push` says **rejected (non-fast-forward)**, do **not** use `--force`:

```bash
git fetch origin
git status
git log --oneline --decorate --graph --all -10
```

Inspect remote changes and merge/rebase carefully before pushing. If `git push` reports a permission or authorization error, check `gh auth status`, your repo access, and repository rules rather than placing tokens in scripts.

## 15. Future changes and GitHub Copilot integration

Use VS Code Copilot Chat with `README.md`, `.github/copilot-instructions.md` and the selected numbered step. The repository includes Copilot `.instructions.md` files and `.prompt.md` templates. For example:

> Review `apps/LAB_SIEM/local/indexes.conf` and `docs/steps/13-create-the-service-account-and-prepare-storage.md`. Explain any mismatch with the RHEL 10.2 SOP, preserve the six index names, and do not assume the data disk is blank.

To publish later validated results:

```bash
git status
git add docs evidence/sanitized hunts screenshots
git diff --cached
git commit -m 'Document verified Splunk hunting evidence'
git push
```

Only describe a test as passed if it was **actually observed**. Keep the evidence templates at `Pending` until you have real results and have sanitized them.

## References

- [Microsoft WSL documentation](https://learn.microsoft.com/windows/wsl/install): Explains how to install WSL and Ubuntu on Windows 11.
- [VS Code WSL development](https://code.visualstudio.com/docs/remote/wsl): Shows how VS Code opens and edits folders from the WSL environment.
- [GitHub CLI documentation](https://cli.github.com/manual/gh_auth_login): Explains browser-based GitHub sign-in from the terminal.
- [GitHub existing repository cloning](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository): Explains downloading an existing repository before editing.
- [GitHub Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/customize-copilot/add-repository-instructions): Explains how to give Copilot instructions for a repository.
