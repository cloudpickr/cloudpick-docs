---
title: "IAM Practical Design and Security Operations"
description: "Compares IAM practical design, authentication methods, permission models, least-privilege tools, and long-term credential risks across vendors."
---

> Last reviewed: August 2026

## Overview

This document focuses on the **practical operation** of IAM — choosing credentials, applying them by identity type, practicing least privilege, and security checks.

:::note
For a vendor product comparison, authentication methods, and an overview of permission models, see [IAM Overview](../../about-cloud/iam-overview/).
:::

## Types of Credentials

There are broadly three ways to authenticate in the cloud. **Which credential you use for which identity** is the core of security.

| Method | Characteristics | Suitable for |
| --- | --- | --- |
| **Long-term credentials** (Access Key, API Key) | Never expire. Immediately exploitable if leaked | ❌ Avoid using if at all possible |
| **Role-based temporary credentials** (IAM Role, Managed Identity) | Automatically issued/expired. No secrets needed in code | ✅ Devices/services (workloads) |
| **Federation** (OIDC, SAML, Workload Identity) | Exchanges an external IdP token for cloud permissions | ✅ People (SSO), third parties, CI/CD |

:::caution
**Principle:** people should use SSO + MFA + federation, services should use role-based temporary credentials, and third parties should use federation + time limits. Long-term keys are a last resort.
:::

:::danger
**Why long-term keys are dangerous:** if exposed in a Git repository, log, or environment variable, they can be exploited immediately. If a departed employee's key isn't revoked, external access can continue indefinitely. Without automated rotation, the same key may remain in use for years.
:::

:::tip
**Advantages of role-based authentication:** tokens are automatically issued and expired, limiting the damage from a leak. There's no need to embed secrets in code, and rotation happens automatically, removing the management burden.
:::

## Applying Identity Types

There are broadly three types of identity managed under IAM. Each has a different method for creation, granting permissions, and revocation.

### People (employees/contractors)

| Lifecycle stage | What to do | Vendor-specific method |
| --- | --- | --- |
| **Onboarding** | Create the account + assign to a group + enforce MFA | AWS: create a user in Identity Center or integrate an external IdP (Okta, Microsoft Entra ID). Azure: create an Entra ID user. Google Cloud: Cloud Identity or Workspace. OCI: create an Identity Domain user |
| **Department transfer** | Remove existing groups + assign new groups | If permissions are group-based, only the group needs to change. If individual policies were attached, manual cleanup is required |
| **Offboarding** | Disable the account → invalidate sessions → delete after a retention period | Deleting immediately makes audit tracing impossible. Retaining a disabled account for 90 days is recommended |
| **Periodic review** | Detect unused accounts/excessive permissions | AWS: Access Analyzer, Azure: Access Reviews, Google Cloud: IAM Recommender |

**Practical principles:**
- Don't attach policies directly to individual users → manage permissions on a **group basis**
- Console access must require **SSO + MFA**
- Include "disable cloud account" in the HR offboarding checklist

### Devices/Services (Workloads)

How to grant permissions to **non-human workloads** such as EC2, Lambda, containers, and CI/CD pipelines.

| Vendor | Recommended method | Description |
| --- | --- | --- |
| AWS | **IAM Role** (Instance Profile, Task Role, Execution Role) | Attaching a role to EC2/ECS/Lambda automatically injects temporary credentials |
| Azure | **Managed Identity** (System-assigned / User-assigned) | Attached to VM/App Service/Function. Tokens are automatically issued/renewed |
| Google Cloud | **Attached Service Account** + Workload Identity | Attach a Service Account to a GKE Pod. No key file needed |
| OCI | **Instance Principal / Resource Principal** | Grant permissions to Compute/Function via dynamic group matching |

**Never do this:**
- Hardcode an Access Key/Service Account Key in an environment variable or code
- Share a single service account across multiple workloads (prevents permission separation)

**Do this instead:**
- Create a separate role/identity per workload (enables least privilege)
- Issue temporary credentials for CI/CD pipelines via OIDC Federation (e.g., GitHub Actions → AWS Role)

:::danger
**Azure MFA Mandate Phase 2 (took effect October 2025, currently in force):** Microsoft now enforces MFA on the Azure CLI, Azure PowerShell, IaC tools (e.g., Terraform azurerm), and ARM API call paths as well. Pipelines that run `az login` with a user account before running Terraform must switch to a **service principal + federated credential** or a **managed identity**. Unconverted pipelines will fail authentication and stop working. See [Microsoft's official guidance](https://learn.microsoft.com/entra/identity/authentication/concept-mandatory-multifactor-authentication) for details.
:::

### Third Parties (external partners/SaaS/vendors)

For when an external organization or SaaS service needs access to your cloud resources.

| Scenario | Recommended method | Caution |
| --- | --- | --- |
| **External SaaS accessing your S3/Blob** | Cross-account Role (AWS), Service Principal + RBAC (Azure), Workload Identity Federation (Google Cloud) | Specify the external account ID explicitly in the trust policy. No wildcards (`*`) |
| **Partner engineer accessing the console** | Create a dedicated role + time limit + enforce MFA | No standing access. Activate only when needed via a JIT approach |
| **Auditing/consulting firms** | Read-only role + limited to specific resources | Don't grant full-account read access. Only the necessary services |
| **External CI/CD services (e.g., GitHub Actions)** | OIDC Federation (keyless token exchange) | Use OIDC instead of long-term keys. Restrict by repository/branch conditions |

**Vendor-specific external access mechanisms:**

| Vendor | Cross-account/tenant | External IdP integration |
| --- | --- | --- |
| AWS | Cross-account IAM Role (external account ID specified in trust policy) | OIDC/SAML Federation, IAM Identity Center |
| Azure | B2B Collaboration (Entra ID guests), Lighthouse (for MSPs) | Entra External ID, Workload Identity Federation |
| Google Cloud | Cross-project IAM binding, Workload Identity Pool | Workforce Identity Federation, Workload Identity Federation |
| OCI | Cross-tenancy Policy (`define tenancy`), Identity Domain Federation | SAML/OIDC Federation |

:::caution
**Core principle for third-party access:** never share long-term keys. Use role-based temporary access + least privilege + time limits + audit logging. Remove the trust relationship immediately when the contract ends.
:::

## Least-Privilege Enforcement Tools

To uphold the principle of least privilege, you need to continuously monitor actual permission usage and remove unnecessary permissions. IAM anomaly detection (abnormal API calls, etc.) integrates with the threat detection services covered in [Security Posture Management](../../security/security-posture/).

| Vendor | Product | Function |
| --- | --- | --- |
| AWS | IAM Access Analyzer | Detects unused roles/permissions. Automatically generates least-privilege policies based on CloudTrail |
| AWS | CloudTrail | Records every API call. Audits who did what |
| Azure | Entra ID Governance (Access Reviews) | Automates periodic permission reviews. Detects excessive permissions |
| Google Cloud | IAM Recommender | Detects unused permissions + recommends reductions |
| Google Cloud | Policy Analyzer | Analyzes who can access which resources |

### Practical Guidance

- Start with broad permissions, then narrow them down after a period of time to only what was actually used.
- Review unused roles and permissions regularly (quarterly).
- Use roles/managed identities for service-to-service access instead of long-term credentials (Access Keys).

## Multi-Cloud Unified Identity (Identity Federation)

Creating separate accounts with each vendor when using multiple clouds leads to fragmented management. **Configuring SSO (Single Sign-On) to all clouds from a single IdP (Identity Provider)** is the starting point for multi-cloud IAM.

| Approach | Description | Tools |
| --- | --- | --- |
| **Central IdP + federation** | Authenticate once with a single IdP, then federate to each cloud via SAML/OIDC | Microsoft Entra ID, Okta, Google Workspace |
| **AWS Identity Center** | AWS-native SSO. Can integrate with an external IdP | AWS IAM Identity Center |
| **Cross-cloud workload identity** | Handles service-to-service authentication without long-term keys | OIDC Federation, Workload Identity |

:::note
If you don't unify the IdP in a multi-cloud environment, problems arise: fragmented account management, missed offboarding, and impossible permission audits. The first thing to do is **choose a single IdP and federate all clouds to it**.
:::

## IAM Security Checklist

- [ ] Is MFA configured on the root/global admin account?
- [ ] Is the root account avoided for day-to-day work?
- [ ] Are there no services still using long-term credentials (Access Keys)? (Convert to role-based)
- [ ] Have accounts/roles unused for 90+ days been disabled?
- [ ] Are there no users with excessive permissions (e.g., AdministratorAccess)?
- [ ] Does service-to-service access use roles/Managed Identity/Instance Principal?
- [ ] Are time limits and conditions set for external (third-party) access?
- [ ] Is CloudTrail/Activity Log/Audit Log enabled?
- [ ] Are periodic (quarterly) permission reviews performed?
- [ ] Is disabling departed employees' accounts included in the HR process?
- [ ] When using multiple clouds, is SSO configured through a central IdP?

## Common Mistakes

- **Attaching policies directly to individual users** — without group-based management, permission cleanup gets missed during offboarding/transfers, and excessive permissions accumulate
- **Using long-term Access Keys in CI/CD** — storing long-term keys as secrets instead of using OIDC Federation makes them immediately exploitable if leaked
- **Deleting departed employees' accounts immediately** — deleting without first disabling makes audit tracing impossible. Retaining a disabled account for 90 days is recommended

## References

### AWS

- [AWS IAM Documentation](https://docs.aws.amazon.com/ko_kr/iam/)
- [IAM Identity Center Documentation](https://docs.aws.amazon.com/ko_kr/singlesignon/)
- [IAM Access Analyzer](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [IAM Best Practices](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/best-practices.html)
- [Well-Architected — Continuous Reduction of Permissions](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_continuous_reduction.html)

### Azure

- [Microsoft Entra ID Documentation](https://learn.microsoft.com/ko-kr/entra/identity/)
- [Azure RBAC Documentation](https://learn.microsoft.com/ko-kr/azure/role-based-access-control/)
- [Entra ID Governance](https://learn.microsoft.com/ko-kr/entra/id-governance/)
- [Conditional Access](https://learn.microsoft.com/ko-kr/entra/identity/conditional-access/)

### Google Cloud

- [Cloud IAM Documentation](https://cloud.google.com/iam/docs)
- [IAM Recommender](https://cloud.google.com/iam/docs/recommender-overview)
- [Policy Analyzer](https://cloud.google.com/policy-intelligence/docs/analyze-iam-policies)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)

### OCI

- [OCI IAM Documentation](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
- [OCI Identity Domains](https://docs.oracle.com/en-us/iaas/Content/Identity/domains/overview.htm)
- [OCI Policy Syntax](https://docs.oracle.com/iaas/Content/Identity/policyreference/policyreference.htm)
