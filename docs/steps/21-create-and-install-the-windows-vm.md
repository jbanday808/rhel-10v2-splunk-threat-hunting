**Step 21 — Create and install the Windows VM**

In VMware Workstation Pro:

1. Create `WINHUNT01`.
2. Assign 8 GB RAM and 4 total virtual CPUs.
3. Create a 100 GB disk.
4. Select UEFI and Secure Boot.
5. Enable the encryption required for the virtual TPM.
6. Add TPM 2.0.
7. Attach the adapter to VMnet8.
8. Install Windows 11.
9. Create your administrator account.
10. Install Windows updates.
11. Install VMware Tools.
12. Restart.

Keep the VM encryption password securely.

VMware documents Secure Boot, encryption, and virtual TPM setup for Windows 11 guests. [knowledge.broadcom.com](https://knowledge.broadcom.com/external/article/315650?utm_source=chatgpt.com)

Inside the **Windows VM**, open administrator Windows PowerShell:

```
Rename-Computer -NewName WINHUNT01 -Restart
```

After restarting:

```
Get-NetAdapter | Format-Table Name,InterfaceIndex,Status,MacAddress
```

For a fresh VM with one adapter named `Ethernet`:

```
$Adapter = Get-NetAdapter -Name Ethernet

Set-NetIPInterface `
  -InterfaceIndex $Adapter.ifIndex `
  -AddressFamily IPv4 `
  -Dhcp Disabled

New-NetIPAddress `
  -InterfaceIndex $Adapter.ifIndex `
  -IPAddress 172.25.250.20 `
  -PrefixLength 24 `
  -DefaultGateway 172.25.250.2

Set-DnsClientServerAddress `
  -InterfaceIndex $Adapter.ifIndex `
  -ServerAddresses 172.25.250.2

Get-NetIPConfiguration

w32tm.exe /query /status
```

Substitute the actual adapter name if different.

**Command overview:**

- `Rename-Computer` sets the guest name.
- `Get-NetAdapter` identifies its adapter.
- `Set-NetIPInterface` disables DHCP.
- `New-NetIPAddress` sets the fixed address.
- `Set-DnsClientServerAddress` sets DNS.
- `w32tm` checks the clock.

---
