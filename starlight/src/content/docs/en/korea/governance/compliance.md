---
title: "Compliance (Korea)"
description: "A rundown of Korea's cloud compliance certifications and requirements, including ISMS-P, CSAP, and financial-sector regulations."
---

> Last reviewed: August 2026

## Overview

Adopting cloud in Korea requires meeting Korea-specific certifications and regulations in addition to international ones such as ISO 27001 and SOC 2. The **general principles of compliance** — the shared responsibility model, automating compliance operations, and so on — are covered in [Compliance](../../../governance/compliance/); this document is the **Korea regulatory layer** that sits on top of those principles.

## ISMS-P (Personal Information & Information Security Management System)

- **Legal basis**: Network Act, Personal Information Protection Act
- **Operated by**: [KISA (Korea Internet & Security Agency)](https://isms.kisa.or.kr/)
- **Scope**: Information and communications service providers with annual ICT-sector revenue of KRW 10 billion or more, or an average of 1 million or more daily users, among other criteria (the KRW 150 billion revenue threshold applies separately to categories such as tertiary general hospitals and universities)
- **Validity**: 3 years, with annual follow-up audits
- **Cloud impact**: When storing or processing sensitive information in the cloud, organizations must use regions within the vendor's ISMS-P certification scope

Official vendor pages:

- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
- OCI: check certification status on the official compliance page

### Key differences: ISMS-P vs. ISO 27001

| Category | ISMS-P | ISO 27001 |
| --- | --- | --- |
| **Scope** | Must fully satisfy all 80+22 criteria | Organizations can choose their scope (Statement of Applicability allows "not applicable") |
| **Privacy** | Included (requirements at each stage of personal data processing) | Not included (requires separate ISO 27701) |
| **Nature** | Legally mandatory in Korea for certain entities (information and communications service providers, etc.) | Voluntary international certification |
| **Common ground** | Both audit business processes (policy, personnel, change management), not just technology | ← Same |

## CSAP (Cloud Security Assurance Program)

- **Legal basis**: Article 23-2 of the Cloud Computing Act
- **Operated by**: [KISA](https://isms.kisa.or.kr/main/csap/intro/)
- **Scope**: Any CSP seeking to provide cloud services to Korean public sector agencies
- **Tier system** (three-tier High/Medium/Low system fully in effect since 2024):

| Tier | Target systems | Requirements |
| --- | --- | --- |
| **High** | Systems related to national security, diplomacy, and other critical national interests; internal administrative systems of government agencies | Strict — physical network separation, domestic region, domestic personnel operation |
| **Medium** | General public-sector systems that process personal information or important information | Relaxed compared to High tier — e.g., logical network separation |
| **Low** | Public data systems that contain no personal information (accessible to global CSPs) | Minimum security requirements |

**Global CSP CSAP certification status (as of 2025):**

| Vendor | Tier | Region | Reference |
| --- | --- | --- | --- |
| AWS | Low-tier | Seoul `ap-northeast-2` | [AWS CSAP announcement](https://aws.amazon.com/blogs/security/aws-achieves-cloud-security-assurance-program-csap-low-tier-certification-in-aws-seoul-region/) |
| Azure | Low-tier | Korea Central / South | [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap) |
| Google Cloud | Low-tier | Seoul `asia-northeast3` | [Google Cloud CSAP](https://cloud.google.com/security/compliance/csap) |
| OCI | — (check official page) | Seoul, Chuncheon | [Oracle Compliance](https://www.oracle.com/corporate/cloud-compliance/) |

:::note
Following the release of N²SF (National Network Security Framework) 1.0 in September 2025, CSAP is undergoing integration with the tiered security system it introduces. Check the [KISA official site](https://isms.kisa.or.kr/main/csap/intro/) and [NCSC](https://www.ncsc.go.kr) for the latest status before adoption.
:::

:::note
Detailed requirements per CSAP tier, hyperscaler and domestic CSP certification status, and developments toward the National Intelligence Service's unified verification system planned for 2027 are covered in depth in [CSAP (Cloud Security Assurance Program)](../security/csap/).
:::

## Financial Sector Regulations

The financial sector is subject to additional regulations.

- **Electronic Financial Transactions Act / Electronic Financial Supervision Regulation** — safety requirements for financial institutions using cloud services
- **Financial Security Institute (FSI)** — publishes cloud usage guidelines for the financial sector and provides security consulting
- **Network separation (mang-bunri) regulation** — systems processing personal credit information must be operated separately from general business networks. This is transitioning to tiered application under N²SF 1.0 (see [Network Separation and Isolation](../../security/network-isolation/))

Official resources:

- [FSI Cloud Usage Guide](https://www.fsec.or.kr/) (use the consolidated index)
- [Financial Services Commission (FSC)](https://www.fsc.go.kr/)

## References

- [KISA Certification & Accreditation](https://isms.kisa.or.kr/)
- [Personal Information Protection Commission](https://www.pipc.go.kr/)
- [Financial Security Institute](https://www.fsec.or.kr/)

- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/) / [AWS CSAP](https://aws.amazon.com/compliance/csap/)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms) / [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
