---
title: "Infrastructure as Code (IaC)"
description: "Covers IaC concepts, comparisons of vendor-native and multicloud tools, and Terraform state management and module design."
---

> Last reviewed: May 2026

## Overview

Creating infrastructure with console clicks is fast, but it's not reproducible and change history can't be tracked. Even if you automate with CLI scripts, the code has no way of knowing "what the current state actually is." When the person in charge changes, no one knows why a server is configured the way it is.

**IaC** (Infrastructure as Code) defines the desired state of infrastructure as code, enabling version control, code review, automated deployment, and change tracking. It replaces the documents that used to describe server configuration on-premises with executable code.

| Approach | Problem | Solved by IaC |
| --- | --- | --- |
| Console clicks | Not reproducible, no history, hard to trace mistakes | Code = documentation = an executable blueprint |
| CLI scripts | Current state unknown, no idempotency | Declarative: compares against current state and applies only the diff |
| Manual documentation | Docs and reality drift apart | Code is always the current state (single source of truth) |

### Imperative vs Declarative

- **Imperative** — "Create this, delete that" executed in order. CLI scripts.
- **Declarative** — Defines "this is the final state." The tool compares against the current state and applies only the difference. The IaC mainstream.

## Product Comparison

### Vendor-native IaC

| Vendor | Product | Language/format | Notes |
| --- | --- | --- | --- |
| AWS | CloudFormation | YAML, JSON | AWS-only. Managed by stack |
| AWS | CDK (Cloud Development Kit) | TypeScript, Python, Java, Go, C# | Generates CloudFormation from a programming language |
| Azure | Bicep | Bicep DSL | A concise alternative to ARM Templates |
| Azure | ARM Templates | JSON | Azure-native. Complex but full-featured |
| Google Cloud | Config Connector | Kubernetes YAML | Manages Google Cloud resources like K8s resources |
| OCI | OCI Resource Manager | HCL (Terraform) | Terraform-based. OCI-native managed offering |

### Multicloud IaC

| Product | Language | Notes |
| --- | --- | --- |
| Terraform / OpenTofu | HCL (HashiCorp Configuration Language) | Most widely used. Supports every vendor |
| Pulumi | TypeScript, Python, Go, C#, Java | Uses general-purpose programming languages. Easy to test |
| Crossplane | Kubernetes YAML | Manages cloud resources from a K8s cluster |

### Unified Resource Management API

For an IaC tool to manage resources, it must call each service's individual API. AWS has standardized this into a single API.

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | Cloud Control API | Manages all AWS + 3rd-party resources through a single CRUD-L API. Used as a backend by IaC tools like Terraform |
| Azure | Azure Resource Manager (ARM) REST API | Controls every Azure resource through a single management layer. Can be called directly via the AzAPI Terraform provider |
| Google Cloud | — (individual per-service APIs) | Config Connector abstracts via the K8s API, but there's no unified CRUD API |
| OCI | OCI Resource Manager API | Terraform state management + resource provisioning API |

Because Terraform can use Cloud Control API as the backend for new AWS resources instead of an individual service API, IaC support for newly released services arrives faster.

## Key Differences

**AWS CloudFormation / CDK** — Integrates fastest with AWS services. CloudFormation support is typically the first to arrive when a new service launches. CDK can leverage a programming language's conditionals, loops, and abstractions, making it advantageous for managing large-scale infrastructure.

**Azure Bicep** — Replaces the complex JSON of ARM Templates with a concise DSL. The VS Code extension provides autocomplete and validation.

**Terraform** — The de facto standard in multicloud environments. A single language (HCL) can manage AWS, Azure, and Google Cloud all at once. Requires state file management.

**OCI Resource Manager** — A Terraform-based managed IaC service that lets you operate state file management and resource provisioning together from the OCI console.

## Terraform State Management

Terraform stores the current infrastructure state in a `terraform.tfstate` file. This file serves the following roles:

- **Resource mapping** — Links resources in code to actual cloud resource IDs
- **Dependency tracking** — Determines which resources to process first/last on a change
- **Performance optimization** — Uses cached state instead of querying every resource each time

### Local vs Remote Backend

:::caution
The `terraform.tfstate` file contains resource IDs, IPs, etc., and secrets can be **stored in plaintext**. Don't store it locally — always **use a remote backend**, and minimize access permissions to the state file.
:::

| Approach | Advantages | Disadvantages |
| --- | --- | --- |
| **Local state** | Simple to configure | No team collaboration, risk of file loss, secrets stored as plaintext |
| **Remote backend** | Team collaboration, locking, encryption, version control | Requires initial setup |

### Remote Backend Options

| Backend | Use case |
| --- | --- |
| **S3 + DynamoDB** | AWS environment. S3 stores state, DynamoDB provides concurrent-execution locking |
| **Azure Storage** | Azure environment. Blob Storage + Lease-based locking |
| **GCS** | Google Cloud environment. Object versioning tracks history |
| **OCI Resource Manager** | OCI-managed backend. Manages state and execution together within OCI |
| **Terraform Cloud / HCP Terraform** | Multicloud. Integrated UI, policy, and team management |

## Module Design Best Practices

A Terraform module is a reusable unit of infrastructure.

### Hierarchical Structure

```text
environments/
├── dev/
│   └── main.tf       # module calls
├── staging/
│   └── main.tf
└── prod/
    └── main.tf

modules/
├── vpc/              # general-purpose VPC module
├── eks-cluster/      # EKS cluster module
└── rds-instance/     # RDS module
```

### Best Practices

- **Break things down small** — If one module manages too many resources, reuse becomes difficult
- **Use input variables for flexibility** — Avoid hardcoding; expose values through `variables.tf`
- **Declare dependencies via outputs** — So other modules can reference them
- **Pin versions** — Pin to a Git tag or a Terraform Registry version
- **Be careful with defaults** — Avoid defaults unsuitable for production (e.g., `deletion_protection = false`)

## Drift Management

If a resource is changed manually outside of IaC, the code and the actual state fall out of sync (drift).

| Vendor | Drift detection tool |
| --- | --- |
| AWS | CloudFormation Drift Detection, Config Rules |
| Azure | Policy, Blueprints Compliance |
| Google Cloud | Config Connector (auto-corrects drift using the K8s model) |
| OCI | Resource Manager Drift Detection |
| Terraform | `terraform plan` (compares current state against code) |

To fundamentally prevent drift, restrict manual changes from the console using **SCP/Azure Policy/Organization Policy**, and enforce that all changes go through the IaC pipeline only. For security validation of the IaC code itself (Checkov, tfsec, etc.), see [DevSecOps](../../devops/devsecops/).

## Common Mistakes

- **Modifying directly in the console and leaving drift unaddressed** — Manually changing a resource in the console causes the code and actual state to diverge (drift). Leaving this unaddressed causes unexpected changes at the next `apply`.
- **Storing the state file locally** — Storing `terraform.tfstate` locally makes team collaboration impossible, and losing the file makes infrastructure management impossible.
- **Copy-pasting instead of modularizing** — Copying the same code across multiple environments means every location must be manually updated on a change, causing inconsistency.
- **Running IaC under a user account on Azure** — Starting October 2025, MFA is enforced for the Azure CLI/PowerShell/ARM API. If the CI/CD pipeline doesn't use `az login --identity` (Managed Identity) or a service principal + Federated Credential, it will break. See [IAM — Azure MFA Enforcement](../../security/iam/) for details.

## Checklist

- [ ] Are you using a remote state store (S3+DynamoDB, Azure Storage, GCS, etc.)?
- [ ] Do you perform drift detection regularly (`terraform plan`, Config Rules, etc.)?
- [ ] Is common infrastructure separated into reusable modules?
- [ ] Is there a process to review `plan` results during code review?

## Related Documents

> 📄 [CI/CD](../../devops/cicd/)

> 📄 [Cloud Management Tools (Console, CLI, SDK)](../../about-cloud/console-cli-sdk/)

## References

### AWS

- [AWS CloudFormation Documentation](https://docs.aws.amazon.com/ko_kr/cloudformation/)
- [AWS CDK Documentation](https://docs.aws.amazon.com/ko_kr/cdk/)

### Azure

- [Bicep Documentation](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/bicep/)
- [ARM Templates Documentation](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/templates/)

### Google Cloud

- [Config Connector Documentation](https://cloud.google.com/config-connector/docs)

### OCI

- [OCI Resource Manager Documentation](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/home.htm)
- [OCI Terraform Provider](https://registry.terraform.io/providers/oracle/oci/latest/docs)

### Multicloud

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [OpenTofu Documentation](https://opentofu.org/docs/)
- [Pulumi Documentation](https://www.pulumi.com/docs/)
