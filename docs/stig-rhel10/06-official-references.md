# 06 — Official STIG, OpenSCAP and RHEL 10 References

- **[DISA STIG Downloads — DoD Cyber Exchange](https://www.cyber.mil/stigs/downloads/)**: Official source for STIG and SCAP packages. The RHEL 10 STIG SCAP Benchmark V1R1 is listed with an October 23, 2026 upload date.
- **[Red Hat DISA STIG](https://access.redhat.com/compliance/disa-stig)**: Supported RHEL minor versions and current vendor profile baseline; as of inspection, RHEL 10.2 vendor SCAP content is aligned with V1R2.
- **[Red Hat SCAP Security Guide Release Notes](https://api.access.redhat.com/articles/7047972)**: Documents RHEL 10 vendor content updates and V1R2 alignment.
- **[Red Hat RHEL 10 Security Hardening](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/security_hardening/security_hardening)**: Scanner installation, profile discovery, assessment, and warnings about automatic remediation.
- **[OpenSCAP User Manual](https://static.open-scap.org/openscap-1.4.1/oscap_user_manual.html)**: `oscap info`, XCCDF evaluations, source data streams, ARF and reports.
- **[OpenSCAP Getting Started](https://www.open-scap.org/getting-started/)**: Example `xccdf eval --profile ... --results-arf ... --report ...` workflow.
- **[NIST SP 800-37 Rev. 2](https://csrc.nist.gov/pubs/sp/800/37/r2/final)**: Security and privacy RMF.
- **[NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)**: Control catalog; final control selection and assessment are organizational decisions.
- **[DISA STIG Viewer](https://www.cyber.mil/stigs/stig-tools/)**: Review and checklist workflow if selected by an organization. Validate specific result-import compatibility.
- **[Red Hat RHEL 10 firewalld instructions](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/configuring_firewalls_and_packet_filters/using-and-configuring-firewalld)**: Network security and zone management.

## Version caution

Your supplied **DISA V1R1 XML** and Red Hat's **V1R2 vendor-profile alignment** have different provenance and possibly different rule coverage. Never label a V1R1 scan “V1R2-compliant.” Recheck the official baseline on the scan date. A live compliance determination is not made by this documentation.
