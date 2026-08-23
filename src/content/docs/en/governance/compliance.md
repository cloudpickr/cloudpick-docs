---
title: "Compliance"
description: "A vendor-by-vendor guide to global cloud compliance certifications such as ISO 27001 and SOC 2, and how to operate compliance in practice."
---

> Last reviewed: August 2026

## Overview

Compliance in the cloud follows a **shared responsibility model**, dividing accountability between vendor and user. Vendors get their infrastructure layer's security controls certified, while users must ensure their workload configurations meet regulatory requirements.

:::note
For background on the shared responsibility model, see [Shared Responsibility Model](../../about-cloud/shared-responsibility/).
:::

:::caution
**Certification is a prerequisite, not a guarantee.** Even if a vendor holds national or international certification, an audit will flag issues if the user's VPC, IAM, and encryption configurations don't meet regulatory requirements. Audits also cover organizational business processes (collection/use/destruction procedures, change management, access rights management) in addition to technical security.
:::

## Compliance by Country

Public procurement certifications, personal data protection laws, and industry-specific regulations vary by country and region, directly affecting architectural decisions such as region selection, data residency, and isolation level. Country-specific details are covered in the relevant country document.

- **Korea** — ISMS-P, CSAP, financial-sector/network segregation, sovereign FM: [Korea guide](../../korea/) · [Compliance (Korea)](../../korea/governance/compliance/)
- **United States** — FedRAMP, HIPAA, ITAR/EAR, state privacy laws, AI policy: [US overview](../../us/)
- **EU** — GDPR and data sovereignty, DORA, NIS2 and the AI Act, member-state schemes, sovereign AI: [EU overview](../../eu/)
- **Japan** — ISMAP, APPI, Government Cloud, AI landscape: [Japan overview](../../japan/)
- **Singapore** — MTCS, PDPA, GCC/IM8, AI governance: [Singapore overview](../../singapore/)

## Major International Certifications

### ISO/IEC 27001:2022 — Information Security Management System

An international standard for information security management. Most global CSPs hold this by default. The **2022 revision** is the current standard; certificates for the prior 2013 version expired on October 31, 2025. Organizations that haven't yet transitioned to the 2022 version must obtain new certification (or transition recertification).

Key changes: controls were restructured from 114 to 93, with 11 new controls added, including "threat intelligence," "cloud service security," and "data masking."

- [AWS ISO 27001](https://aws.amazon.com/compliance/iso-27001-faqs/)
- [Azure ISO 27001](https://learn.microsoft.com/azure/compliance/offerings/offering-iso-27001)
- [Google Cloud ISO 27001](https://cloud.google.com/security/compliance/iso-27001)
- [Oracle ISO 27001](https://www.oracle.com/corporate/cloud-compliance/)

### ISO/IEC 42001 — AI Management System

An international standard management system certification for the development and operation of AI systems. It provides a framework for responsible AI governance.

- OCI's AI services (Enterprise AI, AI Services) obtained ISO/IEC 42001 certification in June 2026
- [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)

### SOC 1 / SOC 2 / SOC 3

Audit reports based on AICPA (American Institute of Certified Public Accountants) standards, frequently requested by enterprise customers.

- **SOC 1** — financial reporting controls
- **SOC 2** — security, availability, processing integrity, confidentiality, privacy
- **SOC 3** — public summary version of SOC 2

Each vendor's SOC reports are **confidential materials**, downloaded after a customer agreement through channels such as AWS Artifact or the Azure Service Trust Portal.

### Industry-specific regulations

| Industry | Key regulation | Applicable region | Notes |
| --- | --- | --- | --- |
| **Healthcare** | HIPAA, HITRUST | United States | |
| **Card payments** | PCI DSS v4.0.1 | Global | v4.0 (2024-03-31, superseding v3.2.1) → v4.0.1 (2024-06 errata). As of 2025-03-31, all ~50 previously "future-dated" v4.0 requirements are mandatory |
| **Public sector (US)** | FedRAMP / FedRAMP 20x | US federal | 20x: an automation-first process that shortens months-long manual authorization into OSCAL-based, machine-readable evidence and automated verification ([fedramp.gov/20x](https://www.fedramp.gov/20x/)) |
| **Public sector (EU)** | C5 (Germany), ENS (Spain), etc. | EU | |
| **Privacy (EU)** | GDPR | EU | |
| **AI (EU)** | EU AI Act | EU | GPAI obligations took effect 2025-08-02. High-risk AI provisions apply from 2026-08-02. [Full text of the EU AI Act](https://artificialintelligenceact.eu/) |
| **Finance (EU)** | DORA | EU | Applicable since 2025-01-17. CTPP (Critical Third-Party Provider) designation process ongoing. [Details](../../governance/landing-zone/) |

Check each vendor's certification status on their **AWS Compliance Programs**, **Azure Trust Center**, **Google Cloud Compliance**, and **Oracle Cloud Compliance** pages.

## Vendor Compliance Hubs

The full list of certifications and how to access reports is managed at each vendor's official hub.

| Vendor | Hub |
| --- | --- |
| AWS | [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/), [AWS Artifact (reports)](https://aws.amazon.com/artifact/) |
| Azure | [Microsoft Trust Center](https://www.microsoft.com/trust-center), [Service Trust Portal](https://servicetrust.microsoft.com/) |
| Google Cloud | [Google Cloud Compliance Resource Center](https://cloud.google.com/security/compliance), [Google Compliance Reports Manager](https://cloud.google.com/security/compliance/compliance-reports-manager) |
| OCI | [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/) |

## How Compliance Is Operated in the Cloud

The core of an audit isn't the certification itself but **how controls are maintained in day-to-day operations**.

### 1. Automate guardrails

Manual management leads to gaps, so policies should be codified as IaC.

| Vendor | Tools |
| --- | --- |
| AWS | [AWS Config](https://aws.amazon.com/config/), [AWS Security Hub](https://aws.amazon.com/security-hub/), SCP (Service Control Policy) |
| Azure | [Azure Policy](https://learn.microsoft.com/azure/governance/policy/overview), [Microsoft Defender for Cloud](https://azure.microsoft.com/products/defender-for-cloud) |
| Google Cloud | [Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/overview), [Security Command Center](https://cloud.google.com/security-command-center) |
| OCI | [OCI Security Zones](https://docs.oracle.com/en-us/iaas/Content/security-zone/home.htm), [OCI Cloud Guard](https://docs.oracle.com/en-us/iaas/cloud-guard/home.htm) |

### 2. Audit trails

Log every change as an audit record and retain it long-term in a central repository.

| Vendor | Audit logs |
| --- | --- |
| AWS | [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) |
| Azure | [Azure Monitor Activity Log](https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log) |
| Google Cloud | [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit) |
| OCI | [OCI Audit](https://docs.oracle.com/en-us/iaas/Content/Audit/Concepts/auditoverview.htm) |

### 3. Access control and least privilege

Least privilege, MFA, and key rotation are covered in [IAM and Access Control](../../security/iam/).

### 4. Data protection

:::note
For encryption at rest and in transit, key management, and data sovereignty, see [Data Protection and Workload Security](../../security/data-protection/).
:::

### 5. Continuous monitoring

Rather than aligning controls only around audit time, run an ongoing detection system. All major vendors offer a **compliance dashboard**.

- AWS Security Hub — automated checks against CIS Benchmark, NIST, PCI DSS. Covered in detail in [Security Posture Management](../../security/security-posture/)
- Azure Defender for Cloud — Secure Score plus automated compliance standard assessment
- Google Cloud Security Command Center — compliance framework mapping
- OCI Cloud Guard — automatic misconfiguration detection

## Reader Checklist

Things to verify when considering compliance in a multi-cloud environment:

- [ ] Has **sensitivity classification** of the data you process/store been completed? (personal information, financial information, confidential information, etc.)
- [ ] Have you identified the **legal requirements** that apply to that data? (applicable jurisdiction(s))
- [ ] Does the vendor you intend to use **hold the necessary certifications in that region**?
- [ ] Have you clearly defined **user responsibilities** under the shared responsibility model?
- [ ] Have you automated **day-to-day operational controls** such as audit logging, access control, and encryption?
- [ ] Is **unified auditing** possible across a multi-cloud environment? (watch for fragmentation across individual vendor dashboards)

## Ongoing Practices

- **Manage certification renewal cycles** — most certifications run on a 3-year validity period with an annual follow-up or surveillance audit (e.g., ISO 27001). For country-specific certification cycles, see the country guides, and add renewal dates to your calendar.
- **Continuous compliance** — instead of manual checks, use AWS Config, Azure Policy, or Google Cloud Organization Policy to detect policy violations in real time.
- **Policy drift detection** — regularly check for differences between IaC and the actual environment to maintain compliance status.

## Common Mistakes

- **Relying solely on vendor certification while neglecting user responsibilities** — even if the vendor holds ISO 27001 or similar certification, VPC, IAM, and encryption configuration remain the user's responsibility and will be flagged in an audit
- **Aligning controls only at audit time and letting drift accumulate otherwise** — cleaning up only right before the annual review lets compliance violations accumulate in daily operations
- **Applying uniform security levels to all data without classification** — over-protection drives costs up, while under-protection creates regulatory violations

## Checklist

- [ ] Have you completed sensitivity classification (personal information, financial information, confidential information) of the data you process/store?
- [ ] Are you running continuous compliance with real-time policy violation detection via AWS Config, Azure Policy, or similar tools?
- [ ] Are certification renewal schedules (ISO 27001 surveillance audits and country-specific certifications) registered and managed on a calendar?

## References

Country regulators and local certification links live in the [Korea](../../korea/governance/compliance/), [United States](../../us/), [EU](../../eu/), [Japan](../../japan/), and [Singapore](../../singapore/) guides.

### AWS

- [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)
- [AWS Artifact](https://aws.amazon.com/artifact/)

### Azure

- [Microsoft Trust Center](https://www.microsoft.com/trust-center)
- [Azure Compliance Offerings](https://learn.microsoft.com/azure/compliance/)

### Google Cloud

- [Google Cloud Compliance Resource Center](https://cloud.google.com/security/compliance)
- [Google Compliance Reports Manager](https://cloud.google.com/security/compliance/compliance-reports-manager)

### OCI

- [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)
- [OCI Security Guide](https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm)

### International standards

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001)
- [ISO/IEC 42001](https://www.iso.org/standard/81230.html) — AI Management System
- [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [Full text of the EU AI Act](https://artificialintelligenceact.eu/)
- [EU DORA](https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en)
- [PCI DSS v4.0.1](https://www.pcisecuritystandards.org/)
- [FedRAMP 20x](https://www.fedramp.gov/20x/)
