# GitHub publication checklist

Use this checklist for a focused change to the current threat-hunting repository. Start from an up-to-date checkout and publish through a pull request so the project checks can run before the change is merged.

## Prepare the change

- [ ] Update the local `main` branch from `jbanday808/rhel-10v2-splunk-threat-hunting` and create a branch for one reviewable improvement.
- [ ] Read the [project overview](../../README.md), [contribution instructions](../../.github/copilot-instructions.md), and [sanitization checklist](security-and-sanitization.md).
- [ ] Keep the change within the threat-hunting scope. Preserve the six documented Splunk indexes and the RHEL, Windows, and IdM lab roles when editing lab instructions.
- [ ] Label synthetic examples, proposed searches, and pending validation accurately. Do not describe a draft as a live detection.

## Check before opening the pull request

- [ ] Review each changed file, image, and example for passwords, tokens, keys, raw logs, personal identifiers, customer information, and unredacted host details.
- [ ] Keep completed customer worksheets, browser backups, and real investigation evidence in an approved private location.
- [ ] Check new or changed relative links and confirm every screenshot caption describes what the image actually shows.
- [ ] Run the repository's source checks from its root:

  ```bash
  python3 scripts/validate_project.py
  python3 -B -m unittest discover -s tests -v
  python3 tools/publication_preflight.py
  ```

- [ ] Run `git diff --check`, inspect `git status`, and review the complete diff before committing.

## Publish and record the result

- [ ] Push the topic branch and open a pull request that explains the change, its checks, and any remaining live-lab validation.
- [ ] Wait for the GitHub project checks to pass; resolve review findings before merging.
- [ ] After merging, open the relevant GitHub pages and confirm the links, images, and instructions render as intended.
- [ ] If the change affects the hosted [TraceVector Site](https://tracevector.jamesbanday.chatgpt.site/), follow its [separate release checklist](../../website/tracevector-lab/README.md#check-a-site-release). Merging GitHub source alone does not publish a new Site version.

The optional `--verify-manifest` command applies only to the unchanged historical download described in the [project overview](../../README.md#validate-and-publish); it is not a gate for normal repository edits. These source checks do not prove Splunk ingestion, sensor deployment, or a completed assessment.
