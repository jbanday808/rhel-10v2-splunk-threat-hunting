# TraceVector | James Banday

[Open the private hosted website](https://banday-network-workbench.jamesbanday.chatgpt.site) · [Guide and screenshots](../../docs/network-defense/INTERACTIVE_LAB.md)

This folder contains the buildless static source for the interactive lab reference website. The TraceVector design uses light green surfaces, larger black text, and crisp black details. Desktop body text is 18px; navigation, labels, and diagram cards are sized for easier reading.

| File | Purpose |
| --- | --- |
| `index.html` | Six-view interface, screenshot gallery, and dialogs |
| `styles.css` | Responsive layout, light green palette, larger black text, and focus states |
| `data.js` | Reviewed lab context and source links pinned to commit `393ed725efadca0c863c409ae0324ed51f1b94b8` |
| `app.js` | Navigation, filtering, copy controls, browser-local checklist, and JSON export |
| `icon.svg` | TraceVector TV monogram |
| `screenshots/` | Five reference captures; architecture and Tool library refreshed |

The Tool library contains seven software entries: the six existing analysis tools plus Splunk Enterprise for SIEM indexing, SPL search, and investigation. Splunk references specify RHEL-SPLUNK01 or Splunk Web instead of assuming Kali Bash. A separate MITRE ATT&CK panel uses selectable Candidate, Context only, and Gap examples linked to the reviewed mapping, hunt playbook, Navigator JSON, and validation template. These labels do not establish live detections. The architecture, ten checklist items, and browser storage key are preserved.

There are no build dependencies, external scripts, analytics, runtime credentials, or live lab connections. Source files do not include checklist contents from anyone's browser. The repository's MIT license applies.

## Preview locally

From the repository root, run:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory website/network-defense-lab
```

**Command Overview:** `python3 -m http.server` serves the static files; `--bind 127.0.0.1` limits the server to local access; `--directory` selects this folder. **Summary:** Open `http://127.0.0.1:8000` in the same computer's browser, and stop with Ctrl+C.

The hosted version's owner-only sign-in is enforced by Sites, not by this static source. Keep hosted deployments private. No GitHub Pages configuration or public deployment is added by this change.

## Validate

```bash
node --check website/network-defense-lab/data.js
node --check website/network-defense-lab/app.js
```

**Command Overview:** `node --check` checks JavaScript syntax without running the application. **Summary:** Browser checks separately cover architecture selection, tool search and details, traffic filters, deployment reviews, checklist persistence, export, and reset.

The website is a reference workspace, not a live monitoring console. Documentation, review checkboxes, screenshots, and source checks do not establish lab acceptance.
