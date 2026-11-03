> **Preferred for this project owner:** use [START_HERE_WSL.md](START_HERE_WSL.md) to publish to the existing public GitHub repository. The older Windows guide also discusses creating a new repository, which is not needed here.

# Start here on Windows 11

1. Extract the ZIP into a new folder. Open this file inside `rhel-splunk-threat-hunting`.
2. Read [the Windows ZIP and GitHub walkthrough](docs/appendices/05-use-the-complete-zip-on-windows-and-upload-to-github.md). It contains the complete PowerShell commands for extraction, file checks, sign-in, staging, and upload.
3. Run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\windows\Test-Project.ps1 -VerifyManifest` after reviewing the validator. This is a read-only package check.
4. Install Git and GitHub CLI, sign in, initialize a local repository, review staged files, and upload using the walkthrough. Use a separate clone and merge if your remote repository already exists.
5. Follow [the deployment order](docs/deployment-order.md) when building or updating the VMs. The endpoint-changing scripts run only in WINHUNT01.

[Complete Word guide](docs/RHEL_10_2_Splunk_Complete_Guide_with_LDAP.docx) · [Complete text guide](docs/RHEL_10_2_Splunk_Complete_Guide_with_LDAP.md) · [All 52 steps](docs/steps/README.md) · [Appendices](docs/appendices/README.md)

This is a source package. Obtain vendor installers separately and generate real certificates and credentials on your own machines. No VM deployment or Azure login is claimed by the package.
