---
title: "IAM Overview"
description: "Compares the fundamental concepts, authentication methods, and permission models of IAM across vendors."
---

> Last reviewed: May 2026

:::note
For practical operations such as managing identity types by category (people/devices/third parties), applying least privilege, and security review checklists, see [IAM Design and Security Operations in Practice](../../security/iam/).
:::

## Why IAM Matters

In the cloud, hundreds of services and thousands of resources are accessible via API. Misconfigured IAM can lead to security incidents such as data breaches or resource deletion. **The principle of least privilege** — granting only the minimum permissions necessary — is the fundamental rule.

## Core Concepts

- **User** — An identity representing a person or an application
- **Group** — Groups users together to grant permissions in bulk
- **Role** — A set of permissions that can be granted temporarily. Primarily used for service-to-service access
- **Policy** — A document defining who can do what, on which resources
- **MFA** — An additional authentication method beyond a password

## Product Comparison by Vendor

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | IAM + IAM Identity Center | Users, groups, roles, policies. Multi-account SSO via Identity Center |
| Azure | Microsoft Entra ID (formerly Azure AD) | Directory service + RBAC. Integrated with Microsoft 365 |
| Google Cloud | Cloud IAM | Project/folder/organization-level RBAC. Service accounts for service-to-service authentication |
| OCI | OCI IAM with Identity Domains | Users, groups, policies, compartment-based access control |

## Authentication Methods

| Method | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Console login** | Username + password + MFA | Entra ID account + MFA | Google account + MFA | Username + password + MFA |
| **CLI/SDK** | Access Key or `aws login` | `az login` (browser) | `gcloud auth login` (browser) | API Key or `oci session authenticate` |
| **Service-to-service** | IAM Role (temporary credentials) | Managed Identity | Service Account | Instance Principal |
| **External IdP integration** | SAML/OIDC Federation | Entra ID External ID | Workforce Identity Federation | SAML/OIDC Federation |

## Permission Management Models

| Vendor | Model | Characteristics |
| --- | --- | --- |
| **AWS** | Policy-based (JSON) | Combines identity-based and resource-based policies. Most granular but complex |
| **Azure** | RBAC (role-based) | Built-in/custom roles. Scoped to subscription/resource group/resource. Dynamic control via Conditional Access |
| **Google Cloud** | RBAC (role-based, hierarchical inheritance) | Inherits organization → folder → project. Direct use of external tokens via Workload Identity Federation |
| **OCI** | Policy-based (HCL-like) | Intuitive syntax such as `Allow group X to manage Y in compartment Z`. Compartment hierarchy inheritance |

## Comparison of Credential Types

| Vendor | Long-Term Credential | Role-Based (Recommended) | Federation |
| --- | --- | --- | --- |
| AWS | Access Key | IAM Role (Instance Profile, Task Role) | OIDC/SAML Federation |
| Azure | Service Principal Secret | Managed Identity | Entra External ID, Workload Identity Federation |
| Google Cloud | Service Account Key (JSON) | Attached Service Account | Workload Identity Federation |
| OCI | API Signing Key | Instance Principal | SAML/OIDC Federation |

## Common Mistakes

- **"It's more convenient to just grant admin permissions"** — Granting broad permissions for convenience widens the blast radius when an incident occurs. Apply the principle of least privilege from the start.
- **"It's fine to put an Access Key in code"** — Long-term credentials exposed in source code or config files carry a high risk of leakage. Use role-based temporary credentials instead.
- **"IAM is set once and done"** — If permissions aren't reviewed periodically as staff and services change, unused permissions accumulate over time.

## Checklist

- [ ] Have you enabled MFA on the root/global admin account and ensured it isn't used for daily work?
- [ ] Do you use roles (Role/Managed Identity/Service Account) instead of long-term credentials for service-to-service authentication?
- [ ] Have you applied the principle of least privilege to users and groups, and established a periodic permission review schedule?

## References

### AWS

- [AWS IAM Documentation](https://docs.aws.amazon.com/ko_kr/iam/)
- [IAM Identity Center](https://docs.aws.amazon.com/ko_kr/singlesignon/)

### Azure

- [Microsoft Entra ID Documentation](https://learn.microsoft.com/ko-kr/entra/identity/)
- [Azure RBAC](https://learn.microsoft.com/ko-kr/azure/role-based-access-control/)

### Google Cloud

- [Cloud IAM Documentation](https://cloud.google.com/iam/docs)

### OCI

- [OCI IAM Documentation](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
