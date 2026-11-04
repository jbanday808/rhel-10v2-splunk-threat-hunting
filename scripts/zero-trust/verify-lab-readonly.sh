#!/usr/bin/env bash
# Read-only lab verification. Execute interactively inside an owned RHEL 10.2 VM.
set -u
echo 'Zero Trust verification: READ ONLY. Does not validate a central PDP or DoD Target compliance.'
printf '%s\n' '--- Identity and OS ---'
hostnamectl || true
cat /etc/redhat-release || true
id || true
printf '%s\n' '--- Host protections ---'
getenforce || true
systemctl is-active firewalld || true
systemctl is-active auditd || true
printf '%s\n' '--- Active network policy ---'
firewall-cmd --get-active-zones || true
firewall-cmd --list-all || true
ss -lntp || true
printf '%s\n' '--- Splunk (only if installed here) ---'
if test -x /opt/splunk/bin/splunk; then
    systemctl status Splunkd.service --no-pager -l || true
    echo 'Splunk installed: review configuration with the designated splunk service identity.'
else
    echo 'Splunk not installed here (expected on the IdM VM).'
fi
echo 'Record actual results privately; do not paste unredacted output into public GitHub.'
