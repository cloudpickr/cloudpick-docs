---
title: "Secrets Management"
description: "Compares secrets management, KMS, and certificate management services across vendors, and explains automated rotation and external tool integration."
---

> Last reviewed: August 2026

## Overview

Applications use sensitive information (secrets) such as database passwords, API keys, and certificates. Hardcoding these into source code or environment variables carries a high risk of exposure. A **secrets management service** encrypts sensitive information, manages it centrally, and lets applications look it up securely at runtime.

### Why It's Needed

- **Prevent leaks** — prevent incidents such as passwords committed to Git or API keys exposed in logs.
- **Automatic rotation** — periodically and automatically change passwords to minimize damage if one is leaked.
- **Audit** — record who accessed which secret and when.
- **Centralized management** — manage secrets used by multiple services in one place.

## Product Comparison

### Secrets Management

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | Secrets Manager | Automatic rotation (native integration with RDS, Redshift, etc.). Cross-account sharing |
| AWS | SSM Parameter Store | Simple key-value storage. Has a free tier. Automatic rotation is limited |
| Azure | Key Vault (Secrets) | Integrated management of secrets + keys + certificates |
| Google Cloud | Secret Manager | Built-in version management. Access control via IAM |
| OCI | OCI Vault (Secrets) | Secret storage + version management. Access control via IAM policies |

### Encryption Key Management (KMS)

Services that manage the keys used to encrypt secrets.

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | KMS (Key Management Service) | Vendor-managed keys / customer-managed keys (CMK) / BYOK |
| Azure | Key Vault (Keys) | HSM support. Dedicated HSM via Managed HSM |
| Google Cloud | Cloud KMS | Supports HSM and external key management (EKM) |
| OCI | OCI Vault (Keys) | Software keys / HSM keys. BYOK support |

### Certificate Management

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | ACM (Certificate Manager) | Free public certificate issuance. Automatic integration with ALB/CloudFront |
| Azure | App Service Certificates / Key Vault | Certificate lifecycle managed in Key Vault |
| Google Cloud | Certificate Manager | Free managed certificates. Automatic integration with Load Balancer |
| OCI | OCI Certificates | Certificate issuance and lifecycle management. Load Balancer integration |

## Key Differences

**AWS** — offers two options: Secrets Manager and Parameter Store. Use Secrets Manager when automatic rotation is needed, and Parameter Store (free) for simple configuration value storage. Since 2025–2026, the Managed External Secrets feature provides standardized management and automated rotation for third-party credentials (Salesforce, MongoDB Atlas, Confluent Cloud, Jenkins, etc.).

**Azure** — manages secrets, encryption keys, and certificates all through a single Key Vault. Management is simpler since the services aren't split apart.

**Google Cloud** — Secret Manager provides version management by default, letting you track secret change history and roll back to a previous version. It also natively supports rotation schedules — set the rotation frequency, and Secret Manager sends Pub/Sub notifications that trigger Cloud Functions to perform the actual rotation.

**OCI** — Vault manages secrets and encryption keys together in one service, with a choice between HSM keys and software keys. Fine-grained access control is possible via IAM policies.

## Encryption Key Management Models

There are three models depending on who generates and manages the encryption key.

| Model | Description | Characteristics |
| --- | --- | --- |
| **Vendor-managed keys** | The vendor generates, manages, and rotates the key | Default. Minimal user involvement |
| **Customer-managed keys (CMK/CMEK)** | The user generates and manages the key in KMS | The user directly manages key policy, rotation cadence, and access control |
| **BYOK (Bring Your Own Key)** | The user brings a key from outside and uploads it to KMS | The key origin is kept outside the cloud. Addresses regulatory requirements |
| **EKM/HYOK (External Key Management)** | The key resides in an external HSM; KMS only references it | The key is never stored in the cloud. The strictest level of control |

:::note
Regulated industries (finance, healthcare, government) commonly use CMK or BYOK, while general web services are often well served by vendor-managed keys.
:::

## Automatic Secret Rotation

Periodically and automatically changing secrets minimizes damage in the event of a leak.

| Vendor | Automatic rotation support |
| --- | --- |
| AWS Secrets Manager | Native rotation for RDS, DocumentDB, Redshift. Custom rotation functions can be written with Lambda. Managed External Secrets extends automated rotation to third-party credentials (Salesforce, MongoDB Atlas, Confluent Cloud, Jenkins, etc.) |
| Azure Key Vault | Automatic certificate renewal. Secret rotation is implemented via Event Grid + Function App |
| Google Cloud Secret Manager | Natively supports rotation schedules — set the rotation frequency and time, and Secret Manager sends notifications to a Pub/Sub topic. A subscribing Cloud Function executes the actual rotation logic |
| OCI Vault | Supports secret rotation (native for Autonomous DB, MySQL). Custom rotation via Function |

### External Secret Store Integration

When using an external secrets management solution such as HashiCorp Vault or CyberArk, you can integrate it with cloud-native services.

| Integration method | Description |
| --- | --- |
| **External Secrets Operator** | Automatically syncs secrets from a cloud vendor's secret store (AWS Secrets Manager, Azure Key Vault, etc.) into a Kubernetes Secret. Has reached v1.x GA for production stability |
| **HashiCorp Vault Dynamic Secrets** | Vault dynamically generates AWS IAM or DB credentials |
| **CSI Secret Store Driver** | Mounts secrets as files into Kubernetes pods |

## Configuration/Property Management

Unlike secrets (passwords, API keys), **configuration values** (feature flags, endpoint URLs, timeout values, etc.) are not sensitive but still need to be managed centrally and changed dynamically at runtime. Each vendor offers a configuration management service, separate from (or integrated with) secrets management.

### Secrets vs. Configuration Values

| Aspect | Secrets | Configuration values |
| --- | --- | --- |
| **Examples** | DB passwords, API keys, certificates | Feature flags, endpoint URLs, timeouts, environment-specific settings |
| **Encryption** | Required (at rest + in transit) | Optional (sensitive settings should be encrypted) |
| **Access control** | Least privilege, auditing required | Per team/service |
| **Rotation cadence** | Periodic automatic rotation recommended | Changed at deploy/release time |
| **Storage location** | Secrets Manager / Key Vault | Parameter Store / App Configuration |

### Vendor Configuration Management Services

| Vendor | Service | Characteristics |
| --- | --- | --- |
| AWS | [SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) | Hierarchical key-value storage. String/StringList/SecureString types. Free standard tier (10,000 parameters). Advanced tier adds policy-based expiration/notifications |
| AWS | [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) | Feature flags + configuration deployment. Gradual rollout, validation before deployment, automatic rollback |
| Azure | [Azure App Configuration](https://learn.microsoft.com/azure/azure-app-configuration/overview) | Centralized configuration store. Built-in feature flags. Secret integration via Key Vault references. Environment separation via labels |
| Google Cloud | [Runtime Configurator](https://cloud.google.com/deployment-manager/runtime-configurator) (legacy) / [Firebase Remote Config](https://firebase.google.com/docs/remote-config) | Runtime Configurator is limited. Server apps commonly store non-secret values in Secret Manager as well |
| OCI | [OCI Resource Manager Variables](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/Concepts/resourcemanager.htm) / Vault | No dedicated configuration service. Non-secret values are stored in Vault, or implemented with Object Storage + application logic |

### Practical Patterns

- **Environment separation** — distinguish environments by path or label, e.g., `dev/db-endpoint`, `prod/db-endpoint`
- **Feature flags** — turn features on/off without a code deployment. Natively supported by AWS AppConfig and Azure App Configuration
- **Dynamic reload** — apply configuration changes without restarting the application, via polling or events
- **Secret references** — instead of storing secret values directly in the configuration service, reference the ARN/URI in Secrets Manager/Key Vault

:::note
**Google Cloud/OCI users:** since dedicated configuration management services are weaker, consider a Kubernetes ConfigMap + External Secrets Operator combination, or HashiCorp Consul. In multi-cloud environments, a vendor-neutral external tool can be advantageous.
:::

## Common Mistakes

- **Hardcoding secrets** — writing passwords or API keys directly into source code or configuration files leaves them permanently in Git history, creating a high risk of exposure.
- **Using secrets permanently without rotation** — if a secret is never rotated after creation, the scope of damage from a leak grows unbounded.
- **Storing secrets directly in environment variables** — storing secrets as plaintext in environment variables can expose them in process lists, logs, and crash dumps. Look them up from a secret store at runtime instead.

## Checklist

- [ ] Are all secrets managed in a dedicated store (Secrets Manager, Key Vault, etc.)?
- [ ] Have you configured automatic rotation?
- [ ] Are you preventing secret commits with a pre-commit hook (git-secrets, detect-secrets, etc.)?
- [ ] Have you enabled audit logging for secret access?

## References

### AWS

- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/ko_kr/secretsmanager/)
- [AWS KMS Documentation](https://docs.aws.amazon.com/ko_kr/kms/)
- [AWS Certificate Manager Documentation](https://docs.aws.amazon.com/ko_kr/acm/)
- [SSM Parameter Store](https://docs.aws.amazon.com/ko_kr/systems-manager/latest/userguide/systems-manager-parameter-store.html)

### Azure

- [Azure Key Vault Documentation](https://learn.microsoft.com/ko-kr/azure/key-vault/)
- [Key Vault Secrets](https://learn.microsoft.com/ko-kr/azure/key-vault/secrets/)
- [Key Vault Certificates](https://learn.microsoft.com/ko-kr/azure/key-vault/certificates/)

### Google Cloud

- [Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [Cloud KMS Documentation](https://cloud.google.com/kms/docs)
- [Certificate Manager Documentation](https://cloud.google.com/certificate-manager/docs)

### OCI

- [OCI Vault Documentation](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/home.htm)
- [OCI Certificates Documentation](https://docs.oracle.com/en-us/iaas/Content/certificates/home.htm)
