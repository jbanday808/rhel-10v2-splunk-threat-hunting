# Uploaded Benchmark Metadata — Measured Locally

This file describes the **user-supplied archive**, not a downloaded or evaluated live VM, and not a digitally authenticated vendor checksum.

| Field | Observed value |
| --- | --- |
| Package name | `U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark(1).zip` |
| Embedded XML | `U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml` |
| Benchmark title | Red Hat Enterprise Linux 10 STIG SCAP Benchmark |
| XML XCCDF benchmark id | `xccdf_mil.disa.stig_benchmark_RHEL_10_STIG` |
| Benchmark version | `001.001` (V1R1) |
| Benchmark status date | `2026-09-17` |
| SCAP data stream | SCAP 1.3 (source data-stream collection, single stream) |
| Source stream timestamp | `2026-10-22T10:05:24.860-04:00` |
| Total rules | **396** |
| High severity (CAT I) | **28** |
| Medium severity (CAT II) | **364** |
| Low severity (CAT III) | **4** |
| XCCDF profiles | **11** |
| External XML extraction | Not needed; ZIP has just one XML file |

**Uploaded ZIP SHA-256:**

```text
84d547f9dc099eaeb882c19d49a5b5f2f664f702cad0250d343121ba8689fa7f
```

**Embedded XML SHA-256:**

```text
47d7a6c9fb544a510a69b871422adfc4967ddd53f2c35e669c1fcbb029f29c93
```

These hashes identify **this uploaded copy**; they are **not** proof that DISA signed the package. Obtain and verify official provenance or signatures according to your organization.

## Profiles actually present in the V1R1 XML

The nine full profiles each select **396** rules:

| Full profile ID suffix | Benchmark profile title |
| --- | --- |
| `MAC-1_Classified` | I - Mission Critical Classified |
| `MAC-1_Public` | I - Mission Critical Public |
| `MAC-1_Sensitive` | I - Mission Critical Sensitive |
| `MAC-2_Classified` | II - Mission Support Classified |
| `MAC-2_Public` | II - Mission Support Public |
| `MAC-2_Sensitive` | II - Mission Support Sensitive |
| `MAC-3_Classified` | III - Administrative Classified |
| `MAC-3_Public` | III - Administrative Public |
| `MAC-3_Sensitive` | III - Administrative Sensitive |

Full ID prefix: `xccdf_mil.disa.stig_profile_`.

Additional profiles:

- `xccdf_mil.disa.stig_profile_Disable_Slow_Rules` — special selection (not a system categorization).
- `xccdf_mil.disa.stig_profile_CAT_I_Only` — restricted CAT-I-focused selection (**not suitable as proof of full STIG assessment**).

**Do not choose a profile based on a guessed mission impact level.** For a private learning lab, a chosen full profile serves as an example only; the profile label does not become a formal FIPS 199 or DoD categorization.

## Verify the user-supplied bytes after private transfer

```bash
sha256sum /path/to/your/rhel10-v1r1.zip
sha256sum /path/to/your/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml
oscap info /path/to/your/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml
```

**Command overview:** Compute local SHA-256 fingerprints and list the actual supported benchmark profiles. Only use paths to private storage outside the Git repository.

## V1R1 versus Red Hat vendor's V1R2

The official [DISA STIG downloads](https://www.cyber.mil/stigs/downloads/) listed **RHEL 10 STIG SCAP Benchmark V1R1** with an October 23, 2026 upload date. Separately, [Red Hat DISA STIG guidance](https://access.redhat.com/compliance/disa-stig) and its 2026 SCAP Security Guide release notes describe **V1R2** as the RHEL 10.2 vendor content baseline. These publications are not interchangeable by filename, profile ID, rule set or scan score. Record **tool version, content version, profile, host, scan time and assessment method** with each finding.
