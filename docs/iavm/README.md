# Information Assurance Vulnerability Management (IAVM)

This is a documentation workstream for recording vulnerability notices and
planning authorized assessment and remediation of the lab. It is **not** the
official IAVM system, an automated scanner, or evidence of DoD compliance.
Notice details may change; consult the authoritative IAVM notice and current
vendor advisories before taking action or reporting status.

## Notices

| Notice | Title | Source severity | Status in this lab |
| --- | --- | --- | --- |
| [2026-A-1195](notices/2026-A-1195.md) | Multiple Vulnerabilities in Splunk Enterprise | 5 - Critical; STIG CAT I | Assessment not run; remediation unverified |

The notice was supplied by the project owner, who confirmed it was cleared for
public release. Its contents have not been independently authenticated against
the IAVM system. The record distinguishes that notice from supplemental public
Splunk advisories and identifies a CVE-list discrepancy that needs review.

## Search

Use the repository's GitHub search, restricting it to `docs/iavm/notices`.
Search for a notice number, title, vendor, or CVE, for example
`path:docs/iavm/notices CVE-2026-76302`. Search results locate repository
documents; they do not establish that a system is affected or remediated.

## Report

1. A designated vulnerability-management owner should verify the current
   notice, scope, deadlines, supersession, and reporting requirements in the
   authoritative system.
2. Privately inventory the actual product, version, enabled components, and
   ownership. Compare them with the current vendor's affected-version and
   CVE-specific guidance. Keep asset identifiers and scan results private.
3. Use an approved change process, verified backups, and the vendor's
   release-specific upgrade instructions. Document any required authorization,
   exception, or CDR Override in the organization's approved system.
4. Verify the resulting version and applicable component-specific actions, then
   submit any required report through the authorized channel. A GitHub commit is
   not an official acknowledgment or report.
5. Update the [sanitized evidence template](../../evidence/sanitized/iavm-2026-a-1195-validation.md)
   only with information approved for publication. Store detailed findings,
   logs, screenshots, approvals, and backups outside this public repository.

## References

- [Supplied notice record](notices/2026-A-1195.md)
- [Splunk advisory SVD-2026-1008](https://advisory.splunk.com/advisories/SVD-2026-1008)
- [Related Splunk advisory SVD-2026-1007](https://advisory.splunk.com/advisories/SVD-2026-1007)
- [Splunk Enterprise downloads](https://www.splunk.com/en_us/download.html)
- [Repository security and sanitization guidance](../reference/security-and-sanitization.md)

## Help

Start with the notice's lab workflow and the existing
[installed-version inventory](../reference/versions.md). The documented Splunk Enterprise
system is `RHEL-SPLUNK01`; the Windows endpoint uses a separate Universal
Forwarder. Do not assume the Enterprise advisory automatically applies to the
forwarder or any other product. Ask the appropriate product owner and
vulnerability-management authority when scope or compliance requirements are
unclear.
