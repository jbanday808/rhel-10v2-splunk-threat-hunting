#!/usr/bin/env bash
set -euo pipefail
# Azure Cloud Shell Bash. Read OIDC steps 1 and 2 first. First-time identity setup only.

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


printf "Application object ID: %s\nService principal object ID: %s\nRole scope: %s\n" "$OIDC_APP_OBJECT_ID" "$OIDC_SP_OBJECT_ID" "$OIDC_RG_SCOPE"
