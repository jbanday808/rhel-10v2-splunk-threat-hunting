## Appendix GitHub Actions OpenID Connect with Azure

OpenID Connect, or **OIDC**, lets a GitHub Actions job obtain a short-lived Azure login without storing an Azure client password. This addition uses Microsoft Entra ID and Azure for the GitHub project created in Step 52. LDAPS continues to handle human sign-in to Splunk.

The working example authenticates a manually started GitHub job and reads one DEV resource group. It uses a GitHub-hosted runner and grants **Reader** access only at that group's scope. A GitHub-hosted runner has no direct route into the lab's private VMnet8 network; this workflow does not deploy to `172.25.250.10`.

### OIDC step 1 Confirm prerequisites and execution locations

You need an Azure subscription, permission to create an Entra application and service principal, and permission to create a resource group and assign its Azure roles. Role assignment requires an appropriate Azure role such as Role Based Access Control Administrator, User Access Administrator, or Owner at the relevant scope. Entra application permissions and Azure resource permissions are separate.

| Task | Where to perform it |
| --- | --- |
| Create workflows and run GitHub CLI commands | The existing WSL project in VS Code, after Step 52. |
| Create the Azure identity, trust, and role assignment | Azure Cloud Shell using Bash. |
| Execute the workflows | GitHub Actions on `ubuntu-24.04`. |
| View lab events or change Splunk settings | RHEL-SPLUNK01 or Splunk Web, as in the earlier steps. |

The example repository is `jbanday808/rhel-10v2-splunk-threat-hunting` and the trusted branch is `main`. If your Step 52 repository has a different owner or name, replace that exact value in both workflow guards below before committing them. Confirm Actions is enabled in the repository's **Settings → Actions → General**.

In the WSL terminal:

```bash
cd "$HOME/projects/rhel-splunk-threat-hunting"
gh auth status
gh repo view --json nameWithOwner,defaultBranchRef
git branch --show-current
git status --short
mkdir -p .github/workflows
```

**Command overview:** `cd` selects the exported project; `gh auth status` checks GitHub access; `gh repo view` identifies the repository and default branch; `git branch` shows your branch; `git status` shows pending changes; `mkdir -p` creates the workflow folder.

Confirm the repository and `main` branch before continuing. Review any existing changes instead of overwriting them.

### OIDC step 2 Capture the actual GitHub subject

Azure must trust the exact OIDC `sub` value GitHub issues. Newer repositories can include immutable owner and repository IDs, while older repositories can use the earlier name-based format. Capturing the actual value also detects a custom subject template.

Create `.github/workflows/oidc-claims.yml` in VS Code with this complete content:

```yaml
name: Inspect OIDC trust claims

on:
  workflow_dispatch:

permissions: {}

jobs:
  claims:
    if: >-
      github.ref == 'refs/heads/main' &&
      github.repository == 'jbanday808/rhel-10v2-splunk-threat-hunting'
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    permissions:
      id-token: write
    steps:
      - name: Display selected trust claims
        shell: bash
        run: |
          python3 - <<'PY'
          import base64
          import json
          import os
          import urllib.parse
          import urllib.request

          url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"]
          separator = "&" if "?" in url else "?"
          url += separator + urllib.parse.urlencode({
              "audience": "api://AzureADTokenExchange"
          })
          request = urllib.request.Request(url, headers={
              "Authorization": "bearer " + os.environ[
                  "ACTIONS_ID_TOKEN_REQUEST_TOKEN"
              ]
          })
          with urllib.request.urlopen(request, timeout=30) as response:
              encoded = json.load(response)["value"].split(".")[1]
          encoded += "=" * (-len(encoded) % 4)
          claims = json.loads(base64.urlsafe_b64decode(encoded))
          keys = ("iss", "aud", "sub", "repository", "ref",
                  "repository_id", "repository_owner_id", "event_name")
          print(json.dumps({key: claims.get(key) for key in keys},
                           indent=2))
          PY
```

**Workflow overview:** `workflow_dispatch` provides a manual start; the job guard permits only this repository's `main` branch; `id-token: write` allows token requests. The Python code requests a token for Azure's audience and displays only the selected identity claims. It does not print the token or its bearer credential. Decoding these claims is for setup inspection; Azure performs signature validation during the actual exchange.

Commit only the intended file after reviewing its contents:

```bash
git add .github/workflows/oidc-claims.yml
git diff --cached --check
git diff --cached
git commit -m 'Add OIDC subject inspection workflow'
git push origin main

gh workflow run oidc-claims.yml --ref main
gh run list --workflow oidc-claims.yml --limit 5
```

**Command overview:** `git add` stages the workflow; `git diff` checks and displays staged changes; `git commit` records them; `git push` sends them to GitHub; `gh workflow run` starts the manual job; `gh run list` lists its runs.

After the run completes:

```bash
read -r -p 'OIDC claims workflow run ID: ' CLAIMS_RUN_ID
gh run view "$CLAIMS_RUN_ID" --log
```

**Command overview:** `read -r` stores the run ID; `gh run view --log` displays its job log.

Confirm `iss` is `https://token.actions.githubusercontent.com`, `aud` is `api://AzureADTokenExchange`, and `ref` is `refs/heads/main`. Copy the complete `sub` string, preserving case and any IDs. A current immutable subject can have the following shape; the angle-bracket values here are placeholders:

```text
repo:jbanday808@<owner-id>/rhel-splunk-threat-hunting@<repo-id>:ref:refs/heads/main
```

An older repository may instead show `repo:jbanday808/rhel-10v2-splunk-threat-hunting:ref:refs/heads/main`. Use the observed value rather than constructing one from this example. Both workflows in this guide deliberately omit a GitHub `environment`; adding one can change the subject and requires matching Azure trust.

### OIDC step 3 Open Azure Cloud Shell and select the subscription

In the Azure portal, open **Cloud Shell**, select **Bash**, and use your intended DEV subscription. An ephemeral session can use **No storage account required**. If Cloud Shell has not been enabled for the subscription, register the `Microsoft.CloudShell` resource provider under **Subscriptions → your subscription → Resource providers** first. Keep the session open through the Azure setup steps; its local files and shell variables are temporary.

```bash
az account list --output table
read -r -p 'DEV Azure subscription ID: ' AZURE_SUBSCRIPTION_ID
az account set --subscription "$AZURE_SUBSCRIPTION_ID"

AZURE_TENANT_ID=$(az account show --query tenantId --output tsv)
az account show --query '{subscription:id,tenant:tenantId,name:name}' --output table

OIDC_RG=rg-siem-oidc-dev
OIDC_LOCATION=westus3
OIDC_APP_NAME=app-siem-github-oidc-dev

az group create --name "$OIDC_RG" --location "$OIDC_LOCATION" --output table
OIDC_RG_SCOPE=$(az group show --name "$OIDC_RG" --query id --output tsv)
```

**Command overview:** `az account list` shows available subscriptions; `read` collects the chosen ID; `az account set` selects it; `az account show` confirms subscription and tenant; `az group create` creates the DEV group; `az group show` retrieves its full scope. `--query` selects fields and `--output tsv` stores a plain value.

Use an approved region if `westus3` is unsuitable. If the resource group already exists, inspect it before reusing it. This example creates no Azure VM or Splunk cloud server.

### OIDC step 4 Create an identity without a client password

Run these creation commands once. If you resume an earlier setup, reuse its recorded application ID instead of creating duplicate applications.

```bash
AZURE_CLIENT_ID=$(az ad app create \
  --display-name "$OIDC_APP_NAME" \
  --sign-in-audience AzureADMyOrg \
  --query appId --output tsv)

OIDC_APP_OBJECT_ID=$(az ad app show \
  --id "$AZURE_CLIENT_ID" --query id --output tsv)

OIDC_SP_OBJECT_ID=$(az ad sp create \
  --id "$AZURE_CLIENT_ID" --query id --output tsv)

printf 'Client ID: %s\nTenant ID: %s\nSubscription ID: %s\nResource group: %s\n' \
  "$AZURE_CLIENT_ID" "$AZURE_TENANT_ID" "$AZURE_SUBSCRIPTION_ID" "$OIDC_RG"
```

**Command overview:** `az ad app create` registers a single-tenant application; `az ad app show` retrieves its directory object ID; `az ad sp create` creates the service principal used for Azure access; `printf` displays the values needed later. These commands do not create a client password.

Keep the application object ID and service principal object ID distinct. The client ID is used by `azure/login`; the service principal object ID receives the resource role.

### OIDC step 5 Create an exact federated trust

Paste the `sub` copied from the successful claims workflow:

```bash
read -r -p 'Exact main-branch OIDC sub from the GitHub log: ' OIDC_SUBJECT
export OIDC_SUBJECT

python3 - <<'PY'
import json
import os
from pathlib import Path

subject = os.environ["OIDC_SUBJECT"]
if not subject.endswith(":ref:refs/heads/main"):
    raise SystemExit("Expected the inspected main-branch subject.")
credential = {
    "name": "github-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": subject,
    "audiences": ["api://AzureADTokenExchange"],
    "description": "Main branch of the RHEL Splunk lab repository"
}
Path("github-main-federation.json").write_text(
    json.dumps(credential, indent=2) + "\n"
)
PY

cat github-main-federation.json

az ad app federated-credential create \
  --id "$OIDC_APP_OBJECT_ID" \
  --parameters github-main-federation.json

az ad app federated-credential list \
  --id "$OIDC_APP_OBJECT_ID" --output json
```

**Command overview:** `read` captures the exact subject; `export` makes it available to Python; the Python code creates the trust JSON; `cat` lets you inspect it; `az ad app federated-credential create` adds the trust; `list` confirms the stored issuer, subject, and audience.

Before creating the credential, confirm the JSON's subject identifies your actual repository and `main` branch. A branch-based trust can authorize eligible jobs on that branch, not just one workflow filename. Review workflow changes on `main` and enable available branch protections or rulesets. Do not broaden the subject to fix a mismatch.

### OIDC step 6 Grant Reader access to the DEV group

```bash
OIDC_ROLE_ASSIGNMENT_ID=$(az role assignment create \
  --assignee-object-id "$OIDC_SP_OBJECT_ID" \
  --assignee-principal-type ServicePrincipal \
  --role Reader \
  --scope "$OIDC_RG_SCOPE" \
  --query id --output tsv)

az role assignment list \
  --assignee "$OIDC_SP_OBJECT_ID" \
  --scope "$OIDC_RG_SCOPE" \
  --include-inherited --output table
```

**Command overview:** `az role assignment create` assigns the Reader role; `--assignee-object-id` identifies the service principal; `--scope` limits access to one resource group; `list` displays applicable assignments.

Confirm the dedicated identity has only the intended access. Reader is sufficient for this validation workflow; a later deployment task requires its own reviewed permissions. Allow time for identity and role changes to become available before testing.

### OIDC step 7 Add GitHub settings

Return to the **WSL project terminal**. Enter the values displayed in Cloud Shell:

```bash
read -r -p 'Azure client ID: ' AZURE_CLIENT_ID
read -r -p 'Azure tenant ID: ' AZURE_TENANT_ID
read -r -p 'Azure subscription ID: ' AZURE_SUBSCRIPTION_ID

gh secret set AZURE_CLIENT_ID --body "$AZURE_CLIENT_ID"
gh secret set AZURE_TENANT_ID --body "$AZURE_TENANT_ID"
gh secret set AZURE_SUBSCRIPTION_ID --body "$AZURE_SUBSCRIPTION_ID"
gh variable set AZURE_DEV_RESOURCE_GROUP --body rg-siem-oidc-dev

gh secret list
gh variable list
```

**Command overview:** `read` collects the identity IDs; `gh secret set` stores the three login settings; `gh variable set` stores the resource group name; the list commands confirm setting names without revealing secret values.

The IDs are configuration values, not client passwords. This workflow uses GitHub secrets for them, following Microsoft's setup pattern. No `AZURE_CLIENT_SECRET` or password-bearing `AZURE_CREDENTIALS` setting is needed.

### OIDC step 8 Create the Azure login workflow

Create `.github/workflows/azure-oidc.yml` with this complete content:

```yaml
name: Validate Azure OIDC access

on:
  workflow_dispatch:

permissions: {}

jobs:
  verify:
    if: >-
      github.ref == 'refs/heads/main' &&
      github.repository == 'jbanday808/rhel-10v2-splunk-threat-hunting'
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    permissions:
      id-token: write
    env:
      AZURE_CORE_OUTPUT: none
      AZURE_DEV_RESOURCE_GROUP: ${{ vars.AZURE_DEV_RESOURCE_GROUP }}
      EXPECTED_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      EXPECTED_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
    steps:
      - name: Sign in to Azure with OIDC
        uses: azure/login@a641126d1b8aa4d1fa005f4f92df94a3a4c4c906 # v3.1.0
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          audience: api://AzureADTokenExchange
      - name: Verify the subscription and DEV resource group
        shell: bash
        run: |
          set -euo pipefail
          test -n "$AZURE_DEV_RESOURCE_GROUP"
          actual_subscription=$(az account show --query id --output tsv)
          actual_tenant=$(az account show --query tenantId --output tsv)
          test "$actual_subscription" = "$EXPECTED_SUBSCRIPTION_ID"
          test "$actual_tenant" = "$EXPECTED_TENANT_ID"
          az group show --name "$AZURE_DEV_RESOURCE_GROUP" \
            --query '{name:name,location:location}' --output table
```

**Workflow overview:** The manual trigger and job guard select this repository's `main` branch. `id-token: write` allows an OIDC token request; it does not grant Azure write access. `azure/login` exchanges that token for Azure access. The script verifies the subscription and tenant, then reads the DEV group. No checkout step is needed because this example runs no repository code.

The action is pinned to the verified v3.1.0 release commit. Review Azure Login releases and update the pinned commit when adopting fixes; a commit pin does not update itself.

### OIDC step 9 Commit and validate the workflow

In WSL:

```bash
git add .github/workflows/azure-oidc.yml
git diff --cached --check
git diff --cached
git commit -m 'Add Azure OIDC login validation'
git push origin main

gh workflow run azure-oidc.yml --ref main
gh run list --workflow azure-oidc.yml --limit 5
```

**Command overview:** The Git commands review, commit, and push the workflow; `gh workflow run` starts it; `gh run list` shows its status and run ID.

Select the new run:

```bash
read -r -p 'Azure OIDC workflow run ID: ' AZURE_OIDC_RUN_ID
gh run watch "$AZURE_OIDC_RUN_ID" --exit-status
gh run view "$AZURE_OIDC_RUN_ID" --log
```

**Command overview:** `gh run watch --exit-status` waits for the result and returns failure if the run fails; `gh run view --log` displays the observed output.

Confirm the Azure login succeeds, subscription and tenant checks pass, and the expected DEV group appears. A manual run on another existing branch must skip the guarded job. That confirms the workflow guard; the exact federated subject remains the separate Azure trust restriction.

If a Git push is rejected because your GitHub CLI authentication lacks workflow permission, use `gh auth refresh --scopes workflow`, complete its sign-in, and retry the push. Check the repository or organization Actions policy if the pinned Azure action is blocked.

### OIDC step 10 Troubleshoot the actual result

| Observation | Check first |
| --- | --- |
| Token request variables are unavailable. | The job must run in GitHub Actions and have `id-token: write`. |
| Azure reports no matching federated identity. | Compare exact issuer, audience, and observed subject; check case, immutable IDs, branch, environment, and any custom subject template. |
| Azure cannot find the application or tenant. | Confirm the three GitHub secret values and the application's tenant. |
| Login succeeds but reading the group is denied. | Check the principal's Reader assignment, group scope, group name, and propagation delay. |
| A job is skipped. | Confirm the selected branch and exact repository name match its guard. |
| The workflow cannot connect to the private Splunk VM. | GitHub-hosted networking does not reach VMnet8 directly. Plan a separate private connectivity and runner design before adding VM deployment. |

Record the GitHub run URL, commit, observed subject, Azure client ID, role scope, and actual result in `docs/versions.md` or sanitized evidence. Do not record OIDC tokens, Azure access tokens, or session credentials.

### OIDC step 11 Disable access when the lab no longer needs it

To pause this integration, disable **Validate Azure OIDC access** from the workflow's Actions menu. To revoke its Azure exchange capability, return to Cloud Shell, confirm the dedicated application's recorded object ID, and remove its `github-main` federated credential:

```bash
read -r -p 'Dedicated OIDC application object ID: ' OIDC_APP_OBJECT_ID

az ad app federated-credential list \
  --id "$OIDC_APP_OBJECT_ID" --output table

read -r -p 'ID of its github-main federated credential: ' OIDC_FEDERATED_ID

az ad app federated-credential delete \
  --id "$OIDC_APP_OBJECT_ID" \
  --federated-credential-id "$OIDC_FEDERATED_ID"
```

**Command overview:** `read` selects the recorded application and credential IDs; `list` lets you verify the target; `delete` removes that specific trust. It does not delete the DEV resource group or the Splunk lab. Removing the trust prevents new token exchanges; already issued Azure access tokens remain valid until they expire.

**Summary:** GitHub issues a short-lived identity token, Entra verifies its exact trust claims, and Azure grants only the dedicated identity's resource permissions. The example verifies access to one DEV resource group while the original RHEL and LDAPS procedures remain available in the same guide.

References:

- [GitHub Azure OIDC Guide](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure): This guide explains GitHub token permissions and Azure trust for workflow authentication.
- [GitHub OIDC Reference](https://docs.github.com/en/actions/reference/security/oidc): This reference explains issuer, audience, subject formats, immutable IDs, and token request variables.
- [Microsoft Azure Login with OIDC Guide](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect): This guide explains Entra identities and GitHub settings for Azure Login.
- [Microsoft Federated Identity Setup Guide](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust): This guide explains creating an application's federated credential.
- [Azure Role Assignment Guide](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-cli): This guide explains assigning a role to a service principal at a specific scope.
- [Azure Cloud Shell Ephemeral Session Guide](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/ephemeral): This guide explains starting Bash without a persistent storage account.
- [Azure Login Action](https://github.com/Azure/login): This repository documents supported versions, inputs, and commit pinning.
- [Azure Login v3.1.0 Commit](https://github.com/Azure/login/commit/a641126d1b8aa4d1fa005f4f92df94a3a4c4c906): This release commit is the action version pinned in the example workflow.

---
