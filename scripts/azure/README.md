# Azure OIDC setup

Start with the complete OIDC appendix in `docs/appendices`. Run the claims workflow first and copy its exact subject.

`configure-oidc-identity.sh` combines Cloud Shell Bash steps 3 through 6 for a first-time setup. Read it before running it in Azure Cloud Shell; it creates a DEV resource group, Entra application, federated trust, and Reader role assignment. Use the manual steps when resuming an existing identity. It does not create a client password.

Return to WSL or Windows GitHub CLI for repository settings and manual workflow runs. Record actual IDs and run results, and keep tokens out of source control.
