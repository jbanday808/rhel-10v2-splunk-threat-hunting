# TraceVector · Threat Hunting Lab source

[Open the private Site](https://tracevector-lab.jamesbanday.chatgpt.site) · [Guided hunts](https://tracevector-lab.jamesbanday.chatgpt.site/#scenarios) · [Guide and screenshots](../../docs/network-defense/INTERACTIVE_LAB.md)

This folder contains the five static application files from **TraceVector Site version 1**, published November 11, 2026. They match source commit `69ab9c0e7cfe50e00e92a087c643f0356419e805` byte for byte. Hosting metadata, credentials, personal notes, attachments, and backup files are excluded.

| File | Purpose |
| --- | --- |
| `index.html` | Page shell and script loading |
| `styles.css` | Responsive layout, colors, typography, and focus states |
| `context.js` | Eighteen guide links, 27 existing screenshot references, and 12 STIG evidence requirements |
| `scenarios.js` | Three guided SSH, sudo, and cron hunts with synthetic records and reference SPL |
| `app.js` | Nine workspace views, local tracking, detection drafts, proposals, and backup export/import |

The views are `#overview`, `#objectives`, `#scenarios`, `#evidence`, `#remediation`, `#detections`, `#docs`, `#progress`, and `#review`. The workspace includes six learning objectives and three steps per scenario.

## Preview locally

From the repository root on your own workstation, run:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory website/tracevector-lab
```

**Command Overview:** `python3 -m http.server` serves the files on port `8000`; `--bind 127.0.0.1` limits access to the local computer; `--directory` selects this source folder.

**Summary:** Open `http://127.0.0.1:8000` on the same computer and confirm the TraceVector overview loads. Stop the server with Ctrl+C.

No build step or package installation is required. Google Fonts and existing GitHub screenshot thumbnails load from external services; those resources require network access. Hosted owner-only sign-in is enforced by Sites and is not part of these static files. The repository's MIT license applies.

## Storage and backups

| Data | Browser storage |
| --- | --- |
| Progress, notes, evidence metadata, document tracking, STIG status, drafts, proposals, and activity | `localStorage`, key `tracevector.workspace.v1` |
| Local evidence attachments | IndexedDB database `tracevector-files`, store `files` |

The application starts without personal progress, proposals, or attachments. Storage is separate for each browser and site address.

**Export workspace** or **Export backup** downloads `tracevector-workspace.json` with workspace data and referenced attachments. **Import backup** validates the file and asks for confirmation before replacing local tracking, progress, and drafts. Export the current workspace first when its contents need to be preserved. Backups can contain private evidence and must stay outside Git.

The original [network-defense workbench](../network-defense-lab/) uses a different checklist format and storage key; its export cannot be imported as a current workspace backup.

## Hunting and review boundaries

The three scenarios map SSH failures to T1110.001, sudo activity to T1548.003, and cron activity to T1053.003. All scenario records are synthetic. The example `tracevector_lab` index is a training placeholder; map drafts to the existing six-index lab configuration and verify fields before using them in Splunk.

**Preview fixture** displays the selected template's fixed reference output. Edited SPL is not executed. Saved drafts record a hypothesis and validation plan without claiming a verified detection.

The Review queue stores Documentation, Screenshot update, Detection, and Remediation proposals. Review decisions are local records; `tracevector-proposal.md` exports a proposal for separate review and application. The application cannot commit, push, open a pull request, change lab hosts, or apply remediation.

Guide links and image references are a curated catalogue. They do not refresh automatically when GitHub changes. This source snapshot also retains the earlier workbench link and historical context descriptions as published.

## Check the source

From the repository root, run:

```bash
node --check website/tracevector-lab/context.js
node --check website/tracevector-lab/scenarios.js
node --check website/tracevector-lab/app.js
```

**Command Overview:** `node --check` parses each JavaScript file without running the application.

**Summary:** Each command should exit successfully without syntax errors. Browser behavior and appearance require separate checks.

Before publishing repository changes, also run the three checks in the [repository validation instructions](../../README.md#validate-and-publish). The original Site handoff reported 84 interaction checks passed; that historical result is distinct from syntax checks or later repository validation.

The current [screenshot gallery](../../docs/network-defense/INTERACTIVE_LAB.md#screenshot-gallery) shows an empty workspace. Interface screenshots, practice progress, and source checks do not establish live lab acceptance or STIG compliance.
