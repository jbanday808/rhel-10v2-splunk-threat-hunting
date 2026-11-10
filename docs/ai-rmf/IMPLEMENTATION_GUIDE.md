# Complete Step-by-Step Guide — Adding NIST RMF for AI to the Splunk Lab

**Environment:** Windows 11 host → VS Code connected to Ubuntu WSL → existing GitHub repository.  
**Project:** https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting  
**Status:** Documentation/assessment planning; AI functionality is **not deployed**.  
**Scope:** Optional future **AI-assisted, read-only summarization of approved Splunk security alerts**. Analyst retains final authority.

This guide joins **NIST AI RMF** (four functions) and the **NIST SP 800-37** security/privacy RMF (seven steps). Do not confuse AI RMF alignment with a federal ATO.

## Phase 1 — Preserve and prepare the existing repository

### Step 1: Confirm prerequisites on Windows 11

Use VS Code's **Connect to WSL** window. The commands below run in **Ubuntu WSL**, not in the RHEL Splunk VM.

```bash
sudo apt update
sudo apt install -y git python3 python3-venv
git --version
python3 --version
```

**Command overview:** `apt update` refreshes Ubuntu package metadata; `apt install` installs Git and Python; `--version` prints installed versions.

### Step 2: Open the existing GitHub checkout

```bash
mkdir -p ~/projects
cd ~/projects
test -d rhel-10v2-splunk-threat-hunting/.git || git clone https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting.git
cd rhel-10v2-splunk-threat-hunting
git status
git remote -v
```

**Explanation:** `mkdir -p` creates the parent folder if absent; `test -d` avoids cloning twice; `git clone` retrieves the repository only when missing; `git status` checks for uncommitted work; `git remote -v` verifies the origin.

**Do not run `git init`:** The repository and existing MIT license are already on GitHub.

### Step 3: Check out the proposed AI RMF branch

```bash
git fetch origin
git switch -c feature/nist-ai-rmf-governance --track origin/feature/nist-ai-rmf-governance
code .
```

If the branch already exists locally, use `git switch feature/nist-ai-rmf-governance` and `git pull --ff-only` instead.

**Explanation:** `git fetch` downloads remote history; `git switch` selects the AI RMF work; `code .` opens the project in VS Code.

### Step 4: Inspect the new folders

```bash
find docs/ai-rmf examples/ai-rmf -type f | sort
git status
```

**Explanation:** `find` lists documentation and examples. `git status` should show a clean branch after fetching it; existing source files remain untouched.

## Phase 2 — Define the AI capability correctly

### Step 5: Record the AI use case

Read [01-use-case-scope.md](01-use-case-scope.md). In [ai-use-case.example.json](../../examples/ai-rmf/ai-use-case.example.json), replace `TBD` owner/reviewer placeholders only when actual personnel and decisions are known.

**Proposed input:** synthetic or approved redacted Splunk alert summaries from existing SPL searches.  
**Proposed output:** analyst-readable draft triage summary containing source event identifiers, uncertainty, and an evidence list.  
**Forbidden:** automatic blocking, account changes, disabling logs, sending raw logs to an unapproved provider, claiming AI detections are verified when they are not.

**Exit criterion:** written use-case scope and a clear indication that the AI is still `proposed_not_deployed`.

### Step 6: Identify boundaries and trust zones

Use [02-system-boundary-and-flow.md](02-system-boundary-and-flow.md). Record the current RHEL-SPLUNK01, WINHUNT01, and RHEL-IDM01 systems. Treat any model service as a **future separate component**, not a fourth already-installed VM.

**Exit criterion:** diagram distinguishes *existing telemetry* from *optional future AI processing*, with no direct AI write access to Splunk or endpoints.

## Phase 3 — Apply both NIST frameworks

### Step 7: PREPARE (SP 800-37)

Assign an owner, security reviewer, privacy reviewer when applicable, and intended decision authority. Document stakeholders, mission, data types, dependencies, and whether AI is appropriate.

**Evidence:** use-case inventory, diagram, roles, and assumptions. No sign-off is implied by creating a Markdown file.

### Step 8: CATEGORIZE (SP 800-37)

Identify information types, confidentiality/integrity/availability concerns, and potential harm. Use **FIPS 199** and organizational procedures when an actual system categorization is required.

**Important:** Do **not** label the lab FedRAMP Moderate, CUI, or authorized at any FIPS level without the appropriate facts and organizational determination. Status stays **Pending**.

### Step 9: GOVERN and MAP (NIST AI RMF)

Use [04-ai-rmf-core.md](04-ai-rmf-core.md) to define accountability, acceptable use, intended purpose, operators, provenance, deployment context, misuse, prompt-injection surfaces, and stakeholders.

**Evidence:** governance checklist, use-case card, risk register. NIST AI RMF functions are ongoing outcomes, not mandatory linear steps.

### Step 10: SELECT (SP 800-37)

Review the [illustrative SP 800-53 control crosswalk](05-control-crosswalk.md). Select and tailor controls only after categorization, applicable requirements, and the system boundary are established.

Candidate domains include least-privilege access, audit, encrypted transport/storage, data minimization, change control, vulnerability management, incident response, and continuous monitoring.

**Exit criterion:** documented control owner, implementation intent, evidence needed, and assessment status. Do not copy the example crosswalk as an official approved baseline.

### Step 11: IMPLEMENT (SP 800-37)

**Safe implementation sequence:**

1. Keep your current Splunk deployment unchanged.
2. Use **synthetic test events** before any real logs.
3. Use a reviewed, read-only Splunk saved search or manually exported sanitized events only if a future AI assistant is actually selected.
4. Store generated sample data outside production indexes, with retention defined.
5. Keep credentials in a secrets manager; never in GitHub, prompts, or example JSON.
6. Deny model access to endpoint management, firewall changes, service restarts, identity changes, or containment.
7. Add human approval before any investigation or security action is accepted.
8. Log model/provider/version, prompt/template ID, input evidence IDs, output, reviewer decision, and timestamps **without retaining raw secrets**.

**Exit criterion:** do not mark `Implemented` until real technical configuration is deployed and verified in your owned lab.

### Step 12: MEASURE and ASSESS

Follow [06-testing-and-assessment.md](06-testing-and-assessment.md) using sanitized synthetic events. Test whether the AI invents indicators, follows malicious instructions embedded in logs, leaks secrets, ignores missing evidence, or makes unsupported recommendations. Compare outputs with a human-created answer key.

**Exit criterion:** documented observed results, test dates, reviewers, failures, and retest history. A test plan is not a test result.

### Step 13: MANAGE, AUTHORIZE, and MONITOR

Complete the [risk register](../../examples/ai-rmf/ai-risk-register.example.csv), [POA&M template](10-poam-template.md), and [monitoring plan](07-monitoring-and-decision.md). Reject, mitigate, transfer, or accept each material risk according to documented authority.

**Authorization:** a reviewer may approve a *lab experiment* under lab policy, but that is **not** a U.S. federal ATO. The SP 800-37 `AUTHORIZE` step requires the appropriate authorizing official and formal risk decision.

**Monitoring:** reassess on model/provider/version changes, new data sources, access policy changes, observed model failures, and a defined review cadence.

## Phase 4 — Verify and publish

### Step 14: Validate the documentation and examples (WSL)

```bash
python3 -m json.tool examples/ai-rmf/ai-use-case.example.json >/dev/null
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_project.py
python3 tools/publication_preflight.py
git diff --check
git status
```

**Explanation:** `json.tool` validates JSON syntax; `unittest` runs local tests; `validate_project.py` checks the repository; `publication_preflight.py` scans for common public-repository risks; `git diff` checks formatting. These are **offline source checks**, not AI model tests or control effectiveness assessments.

### Step 15: Collect evidence without secrets

Update [evidence/sanitized/ai-rmf-validation.md](../../evidence/sanitized/ai-rmf-validation.md) with **Pending / Pass / Fail / Not Applicable** and *actual* evidence. Screenshot guidance is in [11-evidence-and-screenshots.md](11-evidence-and-screenshots.md).

Do not upload password screens, private CA keys, real customer data, raw logs, privileged tokens, unapproved model prompts containing sensitive information, or screenshots that accidentally expose them.

### Step 16: Review the pull request

If this change is available as a PR, inspect **Files changed**, verify no existing lab files were replaced, review GitHub Actions, and merge only when satisfied. Otherwise, for changes you made locally:

```bash
git add docs/ai-rmf examples/ai-rmf evidence/sanitized/ai-rmf-validation.md tests/test_ai_rmf_docs.py
git diff --cached --check
git diff --cached --stat
git commit -m "Document NIST AI RMF integration for proposed Splunk assistant"
git push origin feature/nist-ai-rmf-governance
```

**Explanation:** `git add` stages the selected files; `git diff` reviews them; `git commit` saves changes; `git push` publishes the feature branch, not the production `main` branch.

## Exit criteria and status rules

| Milestone | Evidence needed | Initial status |
| --- | --- | --- |
| Governance documented | AI use case + accountability | Documentation drafted |
| AI design reviewed | Boundary, data policy, threat model | Pending |
| NIST RMF categorization | Authorized classification and rationale | Pending |
| Controls implemented | Config, tests, assigned owners | Pending |
| AI evaluation completed | Observed TEVV results | Pending |
| Risk decision | Signed local approval or formal authorization as applicable | Not granted |
| Production/operational AI use | Deployment records and authorized access | Not deployed |

## References

Official NIST references and version notes: [08-official-references.md](08-official-references.md). NIST AI RMF 1.0 is being revised; verify the current publication before changing the documented framework version.
