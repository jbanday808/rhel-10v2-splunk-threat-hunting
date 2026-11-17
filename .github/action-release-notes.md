Initial release of **RHEL Splunk Threat Hunting Source Check**.

- Reuse the bundled lab validator in any checkout that retains this repository's lab layout.
- Check required files, Python/XML/JSON syntax, Bash syntax, six lab indexes, and selected TLS, redaction, and ingestion settings.
- Configure `path` and optional `verify-manifest` inputs.
- Read `result` and `error-count` outputs and a count-only job summary.
- Reject targets outside the workspace and source links that escape the selected project.
- Run offline without Splunk credentials or connections to lab services.

Requires a Linux runner with Bash and Python 3.10 or newer. Ubuntu 24.04 is tested by the release workflow. This checks source examples; live lab behavior, SPL semantics, and a full security audit remain separate.

Usage: `jbanday808/rhel-10v2-splunk-threat-hunting@v1`.

See [the action guide](https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting/blob/main/docs/custom-github-action.md) for inputs, outputs, examples, and limitations.
