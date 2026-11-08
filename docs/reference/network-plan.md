# Network plan and permitted flows

- VMware network: `VMnet8`, NAT, `172.25.250.0/24`.
- Host virtual NIC: `.1`; NAT/DNS forwarder: `.2`; fixed guests `.10`, `.20`, `.30`.
- DHCP range `.100–.200`, outside the fixed guest addresses.
- `WINHUNT01 (.20)` → `RHEL-SPLUNK01 (.10)`: TCP **9997** for Splunk forwarder data.
- Authorized browser → `RHEL-SPLUNK01 (.10)`: TCP **8000** for HTTPS Web.
- `RHEL-SPLUNK01 (.10)` → `RHEL-IDM01 (.30)`: TCP **636** for verified LDAPS, and DNS when configured.
- Optional HEC **8088**: local test only unless a narrow allow rule is documented.

Do not expose VMnet8 Splunk or IdM services to the Internet. Confirm IPs are unused before configuration and adjust firewall rules to the correct source only. Reverse firewall rules after temporary tests.
