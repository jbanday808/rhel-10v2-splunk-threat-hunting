# Step 51 — Open and review the project in WSL and VS Code

**Location:** Windows 11, Ubuntu WSL terminal, then VS Code (WSL window).

The latest repository name is `rhel-10v2-splunk-threat-hunting`. If you use the complete ZIP, follow [the current full WSL guide](../reference/WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md) to clone the repository, extract the ZIP into a separate staging folder and review its contents.

```bash
sudo apt update
sudo apt install -y git gh unzip rsync python3 tree
mkdir -p "$HOME/projects"
cd "$HOME/projects"
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
gh repo clone jbanday808/rhel-10v2-splunk-threat-hunting
cd rhel-10v2-splunk-threat-hunting
code .
```

**Command overview:** `apt` installs WSL tools; `gh auth login` authenticates through GitHub's browser flow; `gh repo clone` downloads the **existing** repository; `code .` opens it in VS Code WSL.

Do not use `git init` or create a duplicate remote repository. Never copy `.git` from the ZIP. The packaged ZIP intentionally excludes the original MIT LICENSE; preserve the LICENSE from your GitHub checkout.

The files document the lab; WSL is for file editing, testing, review, and publication, not for installing the three VMware guest systems.
