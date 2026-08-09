---
title: "Cloud Management Tools (Console, CLI, SDK)"
description: "Compares the roles of the console, CLI, SDK, and Cloud Shell across vendors, and their relationship to IaC."
---

> Last reviewed: May 2026

## Three Ways to Work with the Cloud

Think about how you'd manage servers in an on-premises environment. You could go to the server room and work directly with a monitor and keyboard, connect remotely over SSH, or call APIs through automation scripts. The cloud offers the same three approaches.

- **Console (web UI)** — Similar to going directly to the server room to work. It lets you view and manage resources visually, which is useful when you're first learning or checking current status.
- **CLI (Command Line Interface)** — Similar to connecting remotely over SSH and working with commands. Repetitive tasks can be automated with scripts, making it well suited to operations work.
- **SDK (Software Development Kit)** — Similar to calling an API from application code. It lets you control cloud resources from a programming language, making it well suited to application integration.

In practice, you mix all three depending on the situation. It's common to check status via the console, automate repetitive tasks via the CLI, and integrate cloud services into applications via the SDK.

## Console (Web UI)

Each vendor provides a console for managing cloud resources from a web browser.

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Name** | AWS Management Console | Azure Portal | Google Cloud Console | OCI Console |
| **URL** | [console.aws.amazon.com](https://console.aws.amazon.com) | [portal.azure.com](https://portal.azure.com) | [console.cloud.google.com](https://console.cloud.google.com) | [cloud.oracle.com](https://cloud.oracle.com) |
| **Korean language support** | Supported | Supported | Partial | Partial |
| **Mobile app** | AWS Console Mobile App | Azure Mobile App | Google Cloud App | OCI Mobile App |
| **Characteristics** | Separate console per service, region selection required | Unified dashboard, resource-group centric | Project-centric, strong search | Compartment-centric, clean UI |

### Caveats When Using the Console

- **Check the region** — In AWS and Google Cloud, you must explicitly select a region in the console. Creating resources in the wrong region is a common mistake.
- **Avoid manual production changes** — Manual changes made through the console are hard to trace and impossible to reproduce. It's recommended to manage production environments via CLI or IaC.

:::caution
Making direct changes to a production environment through the console leaves no change history and cannot be reproduced. Treat **changes via an IaC pipeline** as the rule, and use the console only for status checks and emergency response.
:::

## CLI (Command Line Interface)

Each vendor provides a CLI tool for managing cloud resources from a terminal.

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **CLI name** | AWS CLI (`aws`) | Azure CLI (`az`) | Google Cloud CLI (`gcloud`) | OCI CLI (`oci`) |
| **Additional CLI** | — | Azure PowerShell | — | — |
| **Install** | [Install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) | [Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli) | [Install guide](https://cloud.google.com/sdk/docs/install) | [Install guide](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) |
| **Authentication** | `aws login` (browser auth, CLI v2.32+) | `az login` (browser auth) | `gcloud auth login` (browser auth) | `oci session authenticate` (browser auth) |
| **Output formats** | JSON, YAML, Table, Text | JSON, YAML, Table, TSV | JSON, YAML, Table, CSV | JSON, Table |

### Basic Usage Examples

```bash
# AWS — list EC2 instances
aws ec2 describe-instances --region ap-northeast-2

# Azure — list VMs
az vm list --resource-group my-rg --output table

# Google Cloud — list Compute Engine instances
gcloud compute instances list --project my-project

# OCI — list Compute instances
oci compute instance list --compartment-id <compartment-ocid>
```

Azure also provides **Azure PowerShell** in addition to the CLI. Organizations that primarily use PowerShell on Windows may find Azure PowerShell more familiar.

## SDK (Software Development Kit)

Each vendor provides SDKs for major programming languages, letting you call cloud services directly from application code.

| Language | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Python** | Boto3 | azure-sdk-for-python | google-cloud-python | oci-python-sdk |
| **JavaScript/TypeScript** | AWS SDK for JavaScript | azure-sdk-for-js | google-cloud-node | oci-typescript-sdk |
| **Java** | AWS SDK for Java | azure-sdk-for-java | google-cloud-java | oci-java-sdk |
| **Go** | AWS SDK for Go | azure-sdk-for-go | google-cloud-go | oci-go-sdk |
| **.NET (C#)** | AWS SDK for .NET | Azure SDK for .NET | Google Cloud .NET | oci-dotnet-sdk |
| **Install docs** | [AWS SDK guide](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html) | [Azure SDK guide](https://learn.microsoft.com/azure/developer/) | [Cloud Client Libraries](https://cloud.google.com/apis/docs/cloud-client-libraries) | [OCI SDK guide](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdks.htm) |

Unlike the CLI, an SDK integrates directly into application code, so you can implement error handling, retry logic, and asynchronous calls using the features of your programming language.

## Cloud Shell

Every vendor provides a **Cloud Shell** that lets you use the CLI directly from a browser. No local installation is needed, making it useful for quick tests or emergency response.

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Name** | AWS CloudShell | Azure Cloud Shell | Google Cloud Shell | OCI Cloud Shell |
| **Preinstalled tools** | AWS CLI, Python, Node.js, Git, etc. | Azure CLI, PowerShell, Terraform, etc. | gcloud, kubectl, Terraform, Python, etc. | OCI CLI, Python, Terraform, etc. |
| **Storage** | 1GB per region | 5GB (Azure Files) | 5GB (home directory) | 5GB (home directory) |
| **Cost** | Free | Free (storage cost separate) | Free | Free |
| **Editor** | Built-in editor | Monaco editor (VS Code based) | Theia editor (VS Code based) | Built-in editor |

## Relationship to Infrastructure as Code (IaC)

The console, CLI, and SDK are all **imperative** approaches to directly creating and managing resources. They give step-by-step instructions like "create a server" or "connect a network."

In contrast, **IaC** is a **declarative** approach. You define only the desired end state — "there should be 3 servers and 1 network" — and the tool compares it against the current state and automatically applies the necessary changes.

| Approach | Characteristics | Example tools |
| --- | --- | --- |
| **Imperative** | Executed step by step. Suited to quick tests and emergency response | CLI scripts, SDK code |
| **Declarative** | Defines the end state. Suited to reproducibility, version control, and team collaboration | Terraform, CloudFormation, Bicep, CDK |

In practice, the standard approach is to check status via the console, respond to emergencies via the CLI, and **manage production infrastructure with IaC**.

:::note
For details on comparing IaC tools, Terraform state management, module design, and drift management, see [Infrastructure as Code (IaC)](../../devops/iac/).
:::

## Common Mistakes

- **"Creating it through the console is enough"** — Resources created via the console leave no history, making them impossible to reproduce or audit. Production should be managed with IaC.
- **"CLI and SDK are the same thing"** — The CLI is a tool for running one-off commands in a terminal, while the SDK is a library integrated into application code. Their purposes differ.
- **"Cloud Shell means no local installation is needed"** — Cloud Shell is a temporary environment, and its state may reset when the session ends. Ongoing operations require a local CLI installation.

## Checklist

- [ ] Is CLI authentication set up with browser-based temporary credentials instead of long-lived credentials (access keys)?
- [ ] Have you established the principle that production changes go through an IaC pipeline rather than the console?
- [ ] Have you installed the CLI for the vendor you'll use and run basic commands (resource listing)?

## References

### AWS

- [AWS CLI install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS SDK installation (by language)](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html)
- [AWS CloudShell documentation](https://docs.aws.amazon.com/cloudshell/latest/userguide/)

### Azure

- [Azure CLI install guide](https://learn.microsoft.com/cli/azure/install-azure-cli)
- [Azure SDK installation (by language)](https://learn.microsoft.com/azure/developer/)
- [Azure Cloud Shell documentation](https://learn.microsoft.com/azure/cloud-shell/overview)

### Google Cloud

- [Google Cloud CLI install guide](https://cloud.google.com/sdk/docs/install)
- [Google Cloud Client Libraries (by language)](https://cloud.google.com/apis/docs/cloud-client-libraries)
- [Google Cloud Shell documentation](https://cloud.google.com/shell/docs)

### OCI

- [OCI CLI install guide](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- [OCI SDK](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdks.htm)
- [OCI Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro.htm)
