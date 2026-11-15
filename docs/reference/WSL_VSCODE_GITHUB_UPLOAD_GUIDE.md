# Edit the threat-hunting repository with WSL and VS Code

**Existing repository:** [jbanday808/rhel-10v2-splunk-threat-hunting](https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting)

This guide starts from the current GitHub repository. The older project ZIP and its file counts are historical; do not copy a ZIP over the current checkout. Make one focused change on a branch, check it, and open a pull request (PR) for review.

## 1. Know where the work happens

| Place | Use it for |
| --- | --- |
| Windows 11 host | Run VMware Workstation Pro and start WSL and VS Code. |
| Ubuntu in WSL | Clone the repository, edit files, run source checks, and prepare a PR. |
| RHEL-SPLUNK01, WINHUNT01, RHEL-IDM01 | Run the separately documented lab steps only when authorized. |

Editing a repository file does not change a lab machine or prove a detection works. Do not run the VM setup scripts on the Windows host or in WSL.

## 2. Prepare WSL and VS Code

In Windows PowerShell, check WSL:

```powershell
wsl --status
wsl --list --verbose
```

**Command overview:** The first command checks WSL; the second lists installed Linux distributions. **Expected result:** Ubuntu appears in the list. If it is missing, follow the [official WSL installation guide](https://learn.microsoft.com/windows/wsl/install), then finish the required restart and Linux account setup.

Install VS Code and its WSL extension from the [official VS Code WSL guide](https://code.visualstudio.com/docs/remote/wsl). Open Ubuntu and use its terminal for the commands below. Keep the checkout under `~/projects` in the Linux filesystem for reliable Git performance.

Install the tools needed for this repository:

```bash
sudo apt update
sudo apt install -y git python3
git --version
python3 --version
```

**Command overview:** Ubuntu refreshes package information, installs Git and Python, then prints their versions. **Expected result:** Both version commands complete successfully. Install GitHub CLI (`gh`) using its [official instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) if it is not already available.

## 3. Connect to GitHub and open the current checkout

Check your Git author settings and sign in through GitHub CLI:

```bash
git config --global user.name
git config --global user.email
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
gh auth status
```

**Command overview:** The first two commands show the name and email that will appear on commits; the `gh` commands authorize GitHub access through your browser. **Expected result:** `gh auth status` identifies your GitHub account. If either author setting is empty, set it to your chosen name or a verified GitHub email before committing. Never save a token in this repository.

Clone the existing repository once:

```bash
mkdir -p ~/projects
cd ~/projects
gh repo clone jbanday808/rhel-10v2-splunk-threat-hunting
cd rhel-10v2-splunk-threat-hunting
git remote -v
git status --short
code .
```

**Command overview:** These commands create a work folder, clone the existing GitHub repository, check the destination and local changes, then open it in VS Code. **Expected result:** The remote names `jbanday808/rhel-10v2-splunk-threat-hunting`, `git status --short` is empty, and VS Code shows a WSL window. If the folder already exists, enter it and inspect `git status` instead of cloning over it.

## 4. Make a focused branch

Before editing, update `main` and create a clearly named branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c docs/describe-your-change
```

**Command overview:** This moves to the current main branch, downloads its latest version without an automatic merge, and creates a separate branch. **Expected result:** Git reports the new branch name. Replace `docs/describe-your-change` with a unique name for the work you intend to do.

Use VS Code to edit only the files needed for that change. Keep real credentials, raw logs, private screenshots, personal identifiers, and TraceVector workspace backups outside Git. The [public evidence checklist](security-and-sanitization.md) explains what to review.

## 5. Check your change

From the repository root, run the required source checks:

```bash
python3 scripts/validate_project.py
python3 -B -m unittest discover -s tests -v
python3 tools/publication_preflight.py
git diff --check
git status --short
```

**Command overview:** The Python commands validate source structure, run offline tests, and check publication safety. The Git commands flag whitespace errors and show changed paths. **Expected result:** The checks finish successfully and `git status --short` lists only the files you meant to change. These checks do not connect to Splunk or prove live monitoring.

If you changed website JavaScript, also run `node --check` on each edited `.js` file. GitHub Actions checks the website JavaScript, Linux sources, and Windows sources when you open a PR.

## 6. Publish through a pull request

Stage the specific files you reviewed, inspect the staged change, then push the branch. Substitute the actual changed paths and a useful commit message:

```bash
git add path/to/changed-file
git diff --cached --check
git diff --cached
git commit -m 'Explain the focused change'
git push -u origin HEAD
gh pr create --base main --fill
```

**Command overview:** Git records and pushes your branch; `gh pr create` opens a PR into `main` using the commit details. **Expected result:** GitHub returns a PR URL. Review its title, description, files, and automated checks before merging. Avoid a direct push to `main` or a force push.

To watch the checks for the current branch:

```bash
gh pr checks --watch
```

**Command overview:** This displays GitHub Actions results until they finish. **Expected result:** Required checks pass. If one fails, investigate and correct the branch, then push the fix; GitHub will rerun the checks.

After review and passing checks, merge the PR using GitHub's web page or:

```bash
gh pr merge --squash --delete-branch
git switch main
git pull --ff-only origin main
```

**Command overview:** The first command merges the reviewed PR and removes its branch; the final two commands update your local `main`. **Expected result:** GitHub shows the PR as **Merged** and your local checkout includes it. Repository rules may require another reviewer or a merge queue; follow those rules rather than bypassing them.

## 7. Keep the Site and lab results distinct

The [TraceVector Site source](../../website/tracevector-lab/) lives in this GitHub repository, but changing it here does not automatically publish the hosted Site. Check the Site's separate release process before saying a change is live. Likewise, record an endpoint, syslog, or Splunk result as passed only after observing it in the authorized lab.

## References

- [GitHub CLI pull request creation](https://cli.github.com/manual/gh_pr_create)
- [GitHub CLI PR checks](https://cli.github.com/manual/gh_pr_checks)
- [GitHub CLI PR merge](https://cli.github.com/manual/gh_pr_merge)
- [Repository instructions](../../.github/copilot-instructions.md)
