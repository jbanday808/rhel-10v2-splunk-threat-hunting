**Step 5 — Create and install the RHEL VM**

In VMware Workstation Pro:

1. Select **File → New Virtual Machine**.
2. Choose **Custom** to review the hardware.
3. Select a supported virtual hardware version.
4. Select your RHEL ISO.
5. Select the appropriate RHEL x64 guest option.
6. Name the VM `RHEL-SPLUNK01`.
7. Assign 16 GB RAM and 8 total virtual CPUs.
8. Select UEFI and Secure Boot.
9. Create a 100 GB OS disk.
10. Add a **separate new 250 GB disk**.
11. Select **Custom → VMnet8**.
12. Enable **Connected** and **Connect at power on**.

Confirm that your Workstation release supports the selected RHEL guest and kernel. Broadcom’s support table distinguishes support by Workstation release. [knowledge.broadcom.com](https://knowledge.broadcom.com/external/article/315653?utm_source=chatgpt.com)

During RHEL installation:

1. Select your language and keyboard.
2. Choose **Minimal Install**.
3. Enable networking.
4. Select **only the 100 GB disk** for the OS.
5. Leave the 250 GB disk untouched.
6. Give `/` approximately 70 GB or more.
7. Create `labadmin` with administrator privileges.
8. Keep SELinux enabled.
9. Complete installation and reboot.
10. Disconnect the ISO.

If RHEL is already installed, begin with the verification commands below.

---
