#!/usr/bin/env bash
# Assess an owned RHEL 10 VM using a private DISA SCAP XML. Does not modify system configuration.
# Usage: sudo bash scan-rhel10-readonly.sh /root/private/source.xml FULL_XCCDF_PROFILE_ID
set -euo pipefail
umask 077

[[ $# -eq 2 ]] || { echo "Usage: sudo bash $0 /root/private/source.xml FULL_XCCDF_PROFILE_ID" >&2; exit 64; }
[[ "$EUID" -eq 0 ]] || { echo "Run as root on the RHEL VM (sudo bash ...)" >&2; exit 77; }
command -v oscap >/dev/null 2>&1 || { echo "Missing OpenSCAP scanner" >&2; exit 69; }
command -v sha256sum >/dev/null 2>&1 || { echo "Missing sha256sum" >&2; exit 69; }

SOURCE_XML="$1"
PROFILE="$2"
[[ "$SOURCE_XML" = /* && "$SOURCE_XML" = *.xml ]] ||
  { echo "Use an absolute path to private SCAP XML" >&2; exit 65; }
[[ -f "$SOURCE_XML" && -r "$SOURCE_XML" ]] ||
  { echo "Cannot read source XML" >&2; exit 66; }
[[ "$PROFILE" =~ ^xccdf_mil[.]disa[.]stig_profile_MAC-[123]_(Public|Sensitive|Classified)$ ]] ||
  { echo "Specify a complete DISA V1R1 MAC-1/2/3 XCCDF profile, not CAT-I-only" >&2; exit 65; }
grep -q 'release 10' /etc/redhat-release ||
  { echo "This wrapper supports RHEL release 10 only" >&2; exit 65; }

SOURCE_INFO="$(oscap info "$SOURCE_XML")" ||
  { echo "Unable to read SCAP content: examine file and scanner version" >&2; exit 65; }
printf '%s\n' "$SOURCE_INFO" | grep -Fq "Id: $PROFILE" ||
  { echo "Selected full profile was not found in this data stream" >&2; exit 65; }

REPORT_BASE="/root/stig-rhel10/reports"
install -d -m 0700 "$REPORT_BASE"
HOST_SAFE="$(hostname -s | tr -cd '[:alnum:]_-')"
[[ -n "$HOST_SAFE" ]] || HOST_SAFE="rhel"
UTC_STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$REPORT_BASE/$HOST_SAFE-V1R1-$UTC_STAMP"
install -d -m 0700 "$OUT"

printf '%s\n' "$PROFILE" >"$OUT/selected-profile.txt"
sha256sum "$SOURCE_XML" >"$OUT/source-sha256.txt"
{
    cat /etc/redhat-release
    hostnamectl || true
    uname -r
    oscap --version
    rpm -q openscap-scanner scap-security-guide || true
    date -u -Is
} >"$OUT/host-identity.txt"

printf 'Assessment-only scan: %s\nProfile: %s\nPrivate reports: %s\n' "$(hostname -s)" "$PROFILE" "$OUT"
set +e
oscap xccdf eval \
    --profile "$PROFILE" \
    --results "$OUT/results.xml" \
    --results-arf "$OUT/results-arf.xml" \
    --report "$OUT/report.html" \
    "$SOURCE_XML" >"$OUT/scan.log" 2>&1
RC=$?
set -e
printf '%s\n' "$RC" >"$OUT/oscap-exit-code.txt"

if [[ "$RC" -eq 0 || "$RC" -eq 2 ]]; then
    [[ -s "$OUT/results.xml" && -s "$OUT/report.html" ]] ||
      { echo "Scan outputs missing/empty; inspect the private scan.log." >&2; exit 1; }
    if [[ "$RC" -eq 2 ]]; then
        echo "Evaluation completed with failing controls (OpenSCAP code 2)."
    else
        echo "Evaluation completed; rule-by-rule review is still required."
    fi
    echo "PRIVATE XCCDF: $OUT/results.xml"
    echo "PRIVATE HTML:  $OUT/report.html"
    echo "No system configuration was changed by this script."
    exit 0
fi

echo "Scanner execution error, code $RC; inspect $OUT/scan.log privately." >&2
exit "$RC"
