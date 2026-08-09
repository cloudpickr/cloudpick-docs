---
title: "Compliance"
description: "A vendor-by-vendor guide to cloud compliance certifications, covering Korea's ISMS-P and CSAP alongside global standards like ISO 27001 and SOC 2."
---

> Last reviewed: August 2026

## Overview

Compliance in the cloud follows a **shared responsibility model**, dividing accountability between vendor and user. Vendors get their infrastructure layer's security controls certified, while users must ensure their workload configurations meet regulatory requirements.

:::note
For background on the shared responsibility model, see [Shared Responsibility Model](../../about-cloud/shared-responsibility/).
:::

:::caution
**Certification is a prerequisite, not a guarantee.** Even if a vendor holds ISMS-P or CSAP certification, an audit will flag issues if the user's VPC, IAM, and encryption configurations don't meet regulatory requirements. Audits also cover organizational business processes (collection/use/destruction procedures, change management, access rights management) in addition to technical security.
:::

### Key differences: ISMS-P vs. ISO 27001

| Category | ISMS-P | ISO 27001 |
| --- | --- | --- |
| **Scope** | Must fully satisfy all 80+22 criteria | Organizations can choose their scope (Statement of Applicability allows "not applicable") |
| **Privacy** | Included (requirements at each stage of personal data processing) | Not included (requires separate ISO 27701) |
| **Nature** | Legally mandatory in Korea for certain entities (information and communications service providers, etc.) | Voluntary international certification |
| **Common ground** | Both audit business processes (policy, personnel, change management), not just technology | ← Same |

## Major Korean Certifications

### ISMS-P (Personal Information & Information Security Management System)

- **Legal basis**: Network Act, Personal Information Protection Act
- **Operated by**: [KISA (Korea Internet & Security Agency)](https://isms.kisa.or.kr/)
- **Scope**: Information and communications service providers above certain size thresholds — annual revenue of KRW 150 billion or more, or an average of 1 million or more daily users, among other criteria
- **Validity**: 3 years, with annual follow-up audits
- **Cloud impact**: When storing or processing sensitive information in the cloud, organizations must use regions within the vendor's ISMS-P certification scope

Official vendor pages:

- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
- OCI: check certification status on the official compliance page

### CSAP (Korea's Cloud Security Assurance Program)

- **Legal basis**: Article 23-2 of the Cloud Computing Act
- **Operated by**: [KISA](https://isms.kisa.or.kr/main/csap/intro/)
- **Scope**: Any CSP seeking to provide cloud services to Korean public sector agencies
- **Tier system** (three-tier High/Medium/Low system fully in effect since 2024):

| Tier | Target systems | Requirements |
| --- | --- | --- |
| **High** | Sensitive information processing (including unique identifiers such as resident registration numbers) | Strict — physical network segregation, domestic region, domestic personnel operation |
| **Medium** | General administrative systems | Relaxed compared to High tier |
| **Low** | Lower-criticality systems (accessible to global CSPs) | Minimum security requirements |

**Global CSP CSAP certification status (as of 2025):**

| Vendor | Tier | Region | Reference |
| --- | --- | --- | --- |
| AWS | Low-tier | Seoul `ap-northeast-2` | [AWS CSAP announcement](https://aws.amazon.com/blogs/security/aws-achieves-cloud-security-assurance-program-csap-low-tier-certification-in-aws-seoul-region/) |
| Azure | Low-tier | Korea Central / South | [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap) |
| Google Cloud | Low-tier | Seoul `asia-northeast3` | [Google Cloud CSAP](https://cloud.google.com/security/compliance/csap) |
| OCI | — (check official page) | Seoul, Chuncheon | [Oracle Compliance](https://www.oracle.com/corporate/cloud-compliance/) |

:::note
Following the release of N2SF (National Network Security Framework) 1.0 in September 2025, CSAP is being integrated with the tiered security system it introduces. Check the [KISA official site](https://isms.kisa.or.kr/main/csap/intro/) and [NCSC](https://www.ncsc.go.kr) for the latest status before adoption.
:::

### Financial sector regulations

The financial sector is subject to additional regulations.

- **Electronic Financial Transactions Act / Electronic Financial Supervision Regulation** — safety requirements for financial institutions using cloud services
- **Financial Security Institute (FSI)** — publishes cloud usage guidelines for the financial sector and provides security consulting
- **Network segregation regulation** — systems processing personal credit information must be operated separately from general business networks. This is transitioning to tiered application under N2SF 1.0 (see [Network Segregation and Isolation](../../security/network-isolation/))

Official resources:

- [FSI Cloud Usage Guide](https://www.fsec.or.kr/) (use the consolidated index)
- [Financial Services Commission](https://www.fsc.go.kr/)

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
- [ ] Have you identified the **legal requirements** that apply to that data? (domestic law + foreign law)
- [ ] Does the vendor you intend to use **hold the necessary certifications in that region**?
- [ ] Have you clearly defined **user responsibilities** under the shared responsibility model?
- [ ] Have you automated **day-to-day operational controls** such as audit logging, access control, and encryption?
- [ ] Is **unified auditing** possible across a multi-cloud environment? (watch for fragmentation across individual vendor dashboards)

## Ongoing Practices

- **Manage certification renewal cycles** — ISMS-P is valid for 3 years with an annual follow-up audit; ISO 27001 runs on a 3-year cycle with an annual surveillance audit. Add renewal dates to your calendar.
- **Continuous compliance** — instead of manual checks, use AWS Config, Azure Policy, or Google Cloud Organization Policy to detect policy violations in real time.
- **Policy drift detection** — regularly check for differences between IaC and the actual environment to maintain compliance status.

## Common Mistakes

- **Relying solely on vendor certification while neglecting user responsibilities** — even if the vendor holds ISMS-P, VPC, IAM, and encryption configuration remain the user's responsibility and will be flagged in an audit
- **Aligning controls only at audit time and letting drift accumulate otherwise** — cleaning up only right before the annual review lets compliance violations accumulate in daily operations
- **Applying uniform security levels to all data without classification** — over-protection drives costs up, while under-protection creates regulatory violations

## Checklist

- [ ] Have you completed sensitivity classification (personal information, financial information, confidential information) of the data you process/store?
- [ ] Are you running continuous compliance with real-time policy violation detection via AWS Config, Azure Policy, or similar tools?
- [ ] Are certification renewal schedules (ISMS-P follow-up audits, ISO 27001 surveillance audits) registered and managed on a calendar?

## References

### Korean institutions

- [KISA Certification & Accreditation](https://isms.kisa.or.kr/)
- [Personal Information Protection Commission](https://www.pipc.go.kr/)
- [Financial Security Institute](https://www.fsec.or.kr/)

### AWS

- [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)
- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- [AWS CSAP](https://aws.amazon.com/compliance/csap/)
- [AWS Artifact](https://aws.amazon.com/artifact/)

### Azure

- [Microsoft Trust Center](https://www.microsoft.com/trust-center)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms)
- [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap)
- [Azure Compliance Offerings](https://learn.microsoft.com/azure/compliance/)

### Google Cloud

- [Google Cloud Compliance Resource Center](https://cloud.google.com/security/compliance)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
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
