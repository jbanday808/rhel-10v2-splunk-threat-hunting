# 05 — RHEL STIG Lifecycle, Drift Monitoring and Updates

## Recommended lifecycle

1. Record the **authorized baseline** and method (e.g., uploaded DISA V1R1 SCAP 1.3, or a separate approved Red Hat RHEL 10.2 V1R2 vendor profile).
2. Maintain a vetted **asset inventory** and backup/restore routine for Splunk and IdM.
3. Repeat the same scan **after every material hardening/configuration change** and before/after version upgrades.
4. Reassess log forwarding, SELinux, sshd, directory authentication, system crypto, package signatures, open ports, mounts and index permissions.
5. Triage new errors and failing rules; update a POA&M and assign owners.
6. Repeat functional tests for DNS, Kerberos, LDAPS, Splunk searches, forwarders, systemd and data volumes.
7. Check the official DISA download library and Red Hat versioned content; if upgrading the baseline, keep old and new reports **separate**.
8. Document exceptions and reviewer decisions; never convert unassessed controls into compliant statuses.
9. Verify recovery and clear outdated evidence according to the local security policy.
10. Schedule a practical lab review cadence (e.g., monthly and after major change); this is a **suggestion**, not a STIG-mandated review period.

## Separate DISA V1R1 and Red Hat vendor V1R2 workflows

The **uploaded** scan source has DISA profile IDs beginning `xccdf_mil.disa.stig_profile_` and XML named `U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml`.

Red Hat's **vendor** content for the appropriate installed RHEL 10 minor version is normally under:

```bash
/usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml
```

Use:

```bash
rpm -q scap-security-guide
oscap info /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml
```

This vendor stream uses `xccdf_org.ssgproject.content_profile_stig` (or `stig_gui` for supported GUI installations), and version alignment should be verified from installed RPM and Red Hat publication. **Do not run one with the other's profile ID** or claim identical coverage.

## Do not auto-publish raw results

GitHub Actions in this repo validates Python/Markdown/JSON and offline example fixtures only. It does **not** connect to VMware, scan a private RHEL host, run STIG fixes or demonstrate an approved government configuration.

## Future compatible improvements

- Add approved maintenance windows and host-specific review records.
- Add a separate private automation controller only after testing supported OpenSCAP/SCAP content and service dependencies.
- Maintain a reviewed exception/tailoring process if an actual authority approves it.
- Integrate **sanitized** compliance trend metrics with Splunk only after the source/type and access limits are approved.
- Preserve an offline backout strategy and documented change provenance.
