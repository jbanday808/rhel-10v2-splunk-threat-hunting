# START HERE — VS Code + WSL on Windows 11

Use this short route to edit the existing public threat-hunting repository:

**https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting**

1. Read the [current WSL and VS Code guide](../docs/reference/WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md) for the commands and expected results.
2. Check or install Ubuntu WSL, VS Code with its WSL extension, Git, GitHub CLI (`gh`), and Python 3.
3. Clone the **existing** GitHub repository into `~/projects`, or enter your existing clean checkout. Confirm the GitHub remote before editing.
4. Update local `main`, then create a new branch for one focused threat-hunting improvement.
5. Review changed files for passwords, raw logs, private evidence, and other information that should stay out of a public repository.
6. Run the repository validator, Python unit tests, and publication preflight listed in the [main README](../README.md#validate-and-publish).
7. Review the staged changes, push your branch, and open a pull request into `main`.
8. Check GitHub Actions and the proposed change. Merge after review and passing checks, then update your local `main`.

**Important:** The old project ZIP and its file counts are historical. Use the current GitHub checkout as the source of truth. Repository source checks do not deploy or validate RHEL-SPLUNK01, WINHUNT01, or RHEL-IDM01; those lab steps remain separate.
