# Complete file/folder creation matrix (VS Code + WSL)

Use this historical ZIP matrix alongside `WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md`. Its paths describe the original package; the listed top-level documentation files now live in [`docs/reference/`](README.md). Do not create empty placeholders over working source files.

| Folder / file | Function | How created |
| --- | --- | --- |
| `README.md` | Public project landing page | Original ZIP, updated with WSL guide |
| `START_HERE_WSL.md` | Owner-specific WSL quick start | Added to ZIP |
| `.gitignore`, `.gitattributes`, `.editorconfig` | Ignore unsafe files, normalize line endings, editor basics | Original ZIP; ignore patterns strengthened |
| `.github/copilot-instructions.md`, `instructions/`, `prompts/` | Repository-wide and file-specific Copilot guidance | Added to ZIP |
| `.github/workflows/` | Offline source-validation and optional manual Azure OIDC workflows | Original ZIP, corrected repository guard |
| `.vscode/extensions.json` | VS Code extension recommendations | Added to ZIP |
| `apps/LAB_SIEM/` | Splunk indexes, inputs, props, transforms, role, UI | Original ZIP |
| `apps/LAB_UF_WINDOWS/` | Windows Universal Forwarder collection and TLS output | Original ZIP |
| `apps/Splunk_TA_nginx/` | Optional NGINX add-on overrides | Original ZIP |
| `configs/` | Rsyslog, logrotate, PKI extension, systemd, NGINX, HEC, redaction | Original ZIP |
| `docs/steps/` | 52 ordered procedures | Original ZIP, Steps 51/52 updated |
| `docs/appendices/` | Seven detailed optional appendices | Original ZIP |
| `docs/images/` | New sanitized image references | Original ZIP, README added |
| `docs/WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md` | Complete current upload walkthrough | Added to ZIP |
| `docs/architecture.md`, `docs/architecture-diagram.md` | Architecture explanation and diagram | Original and added |
| `evidence/sanitized/` | Pending validation records | Original ZIP |
| `screenshots/` | 22 existing author-supplied PNG images and new index | Original ZIP, index added |
| `hunts/` | 13 ready-to-review SPL searches | Original ZIP |
| `scripts/rhel/`, `scripts/windows/`, `scripts/azure/` | Lab-specific helper scripts | Original ZIP |
| `scripts/wsl/verify-repository.sh` | WSL-only read-only local checks | Added to ZIP |
| `tests/`, `tools/publication_preflight.py` | Offline tests and publication preflight | Original and added |
| `SECURITY.md`, `CONTRIBUTING.md`, `AGENTS.md` | Safe publishing and agent policy | Added to ZIP |
| `FILE_MANIFEST.json`, `docs/project-file-list.md` | Complete package inventory | Regenerated |
| `LICENSE` | **Existing GitHub MIT license** | Preserve from cloned GitHub repository, not in ZIP |
