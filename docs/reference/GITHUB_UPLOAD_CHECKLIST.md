# GitHub publication checklist

- [ ] Open VS Code in a **WSL** project folder under `~/projects`.
- [ ] Clone the existing `jbanday808/rhel-10v2-splunk-threat-hunting` repository.
- [ ] Preserve remote `.git` and MIT `LICENSE`.
- [ ] Extract ZIP into a **separate staging folder**, not on top of the checkout.
- [ ] Merge staged files using `rsync` without `--delete`.
- [ ] Run `python3 scripts/validate_project.py --verify-manifest` before edits.
- [ ] Run unit tests and `python3 tools/publication_preflight.py`.
- [ ] Check 52 numbered SOP steps, seven appendices, 13 hunts and 22 screenshots.
- [ ] Review every DOCX, Markdown file, screenshot and config example for private values.
- [ ] Confirm old Azure OIDC repository references are corrected in the live workflows.
- [ ] Run `git status`, `git diff --cached --check` and `git diff --cached`.
- [ ] Commit and push to `origin main`.
- [ ] Open GitHub and confirm README, folders, workflow and screenshots.
- [ ] Keep deployment validation labeled Pending until actually tested.
