# RHEL Splunk Threat Hunting Source Check

This composite action packages the repository's offline source validator. It is intended for this RHEL/Splunk threat-hunting lab and forks that retain the same files and layout. It is not a general validator for arbitrary Splunk installations.

## What it checks

- Required lab source files and all 52 numbered step guides.
- Python, XML, and JSON syntax; shell syntax through `bash -n` when Bash is available. Target Python files are parsed, never imported or executed.
- Presence of the six lab indexes: `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`.
- Selected Windows forwarding TLS controls, NGINX input settings, field extraction references, password redaction configuration, and the HEC TLS example.
- A limited check for private-key headers and nonportable scratch paths.
- Optionally, original download manifest hashes.

It does not install software, contact Splunk or cloud services, modify lab settings, execute target scripts, test SPL/KQL query semantics, or establish that a deployment is secure. The limited key-header check does not replace secret scanning or manual review of screenshots, history, and documents.

## Requirements and inputs

Use a Linux runner with Bash and Python 3.10 or newer; the release workflow tests Ubuntu 24.04 with Python 3.12. Check out the target source before using the action. The action loads its own bundled validator from the selected release and applies it to the target source tree.

| Input | Default | Meaning |
| --- | --- | --- |
| `path` | `.` | Target lab directory, relative to `GITHUB_WORKSPACE`. Absolute paths inside the workspace also work. Missing directories, paths outside the workspace, and source symlinks pointing outside the selected project are rejected. |
| `verify-manifest` | `false` | Set to `true` only to validate the unchanged original downloaded package against `FILE_MANIFEST.json`. Current repository edits intentionally differ from that historical manifest. Only `true` and `false` are accepted, ignoring case and surrounding whitespace. |

The action needs no secrets or token input. `contents: read` is enough for the caller's checkout. GitHub supplies `GITHUB_WORKSPACE`, `GITHUB_ACTION_PATH`, `GITHUB_OUTPUT`, and `GITHUB_STEP_SUMMARY`; callers do not need to set them. The action does not download dependencies.

## Usage and outputs

```yaml
name: Check lab source
on: [push, pull_request, workflow_dispatch]
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - id: lab
        uses: jbanday808/rhel-10v2-splunk-threat-hunting@v1
        with:
          path: '.'
      - name: Show result
        env:
          RESULT: ${{ steps.lab.outputs.result }}
          ERRORS: ${{ steps.lab.outputs.error-count }}
        run: printf 'Source result: %s; errors: %s\n' "$RESULT" "$ERRORS"
```

| Output | Meaning |
| --- | --- |
| `result` | `passed` if source validation succeeds; `failed` for validation or input errors. |
| `error-count` | Number of validation findings. An input or runner error is counted as one. |

Validation errors produce a nonzero exit code, which fails the workflow step. Outputs are written before that exit; workflows that deliberately inspect a failure can use `continue-on-error: true` and check the step's `outcome`. Infrastructure failures such as an unavailable interpreter or an unwritable GitHub output file may prevent outputs from being produced.

Logs and the summary show counts only. Parser messages and filenames can contain private text or runner commands, so the action does not print raw diagnostics. For details, run `python3 scripts/validate_project.py` in the target checkout in an appropriate private environment. Review and sanitize diagnostics before sharing them.

For a target checked out into a subdirectory, set `path` to that directory. The validator expects the complete lab source layout. To test the action's working copy in this repository, use `uses: ./` after checkout.

## Versioning and release review

The first version is `v1.0.0`; `v1` is the compatible major-version tag. Prefer a full release commit SHA when a workflow requires a fixed dependency. Minor and patch releases retain the input/output contract; incompatible changes require a new major version. Do not point consumers at `main`.

The **Test and release custom action** workflow runs the three repository publication checks, the action's success case, and an intentionally broken XML case that must fail. Its release job runs after those tests on a version-changing push to `main` or an eligible manual dispatch. The release workflow reads `ACTION_VERSION` and the release notes in `.github/action-release-notes.md`. Existing published versions are preserved; a normal code change does not move the released major tag.

Before a new version, review the diff, update `ACTION_VERSION` and release notes, and run:

```bash
python3 scripts/validate_project.py
python3 -B -m unittest discover -s tests -v
python3 tools/publication_preflight.py
```

Command overview: these checks validate source structure, exercise the automated test suite, and check Git-visible files for selected publication hazards. Expected result: each command exits with code zero. These results do not demonstrate a live Splunk deployment. Review the [sanitization checklist](reference/security-and-sanitization.md), screenshots, and Git history before publication.

After the release tests pass, review the published release and tags. GitHub Marketplace listing is a separate step in the release screen: choose **Publish this Action to the GitHub Marketplace**, resolve metadata errors, select **Code quality** as the primary category and optionally **Security** as a second category, then update/publish the release. The account owner must accept the Marketplace Developer Agreement and satisfy GitHub's two-factor authentication requirement. The owner should personally review any agreement or authentication prompt.

Marketplace requires a public repository and root action metadata. GitHub recommends keeping Marketplace repositories focused on the action; this repository retains the lab, documentation, and fixtures that the action validates. The Marketplace screen determines whether the submitted name and metadata are acceptable. See [GitHub's publication requirements](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace).
