---
title: "CSAP (Cloud Security Assurance Program)"
description: "An overview of Korea's CSAP (Cloud Security Assurance Program), its tier system, and vendor-by-vendor certification status."
---

> Last reviewed: August 2026

## Overview

CSAP (Cloud Security Assurance Program, 클라우드 서비스 보안인증제) is a mandatory certification that any provider seeking to supply cloud services to Korean government and public institutions must obtain. The Korea Internet & Security Agency (KISA) performs the assessment, evaluating the physical, technical, and administrative security controls of a cloud service.

Certification is categorized by service type — IaaS, SaaS (standard/simplified), and DaaS — and is valid for five years. Since February 2024, a **three-tier High/Medium/Low system** has fully replaced the prior single-standard scheme, with requirements now varying by system criticality.

:::caution
In April 2026, the Ministry of Science and ICT (MSIT) and the National Intelligence Service (NIS) jointly announced that they would restructure the CSAP system into a unified, NIS-led verification framework. The tier system and certification status described below reflect this document's review date (August 2026); procedures will change following the restructuring, planned to take effect in July 2027. See [2026 Restructuring — Toward a Unified NIS Verification System](#2026-restructuring--toward-a-unified-nis-verification-system) for details.
:::

## Tier System (High/Medium/Low)

| Tier | Target systems | Key requirements |
| --- | --- | --- |
| **High** | Systems directly tied to core national interests such as security and diplomacy, and internal administrative systems at government agencies | Blocks external networks (effectively mandating a private cloud), adds four requirements: integrated security audit log management, automated account/access rights management, and automated security patching |
| **Medium** | General public-sector systems that process personal data or sensitive information | Carries forward the existing IaaS certification level. Clarifies requirements for system isolation and physical zone separation. Requires physical network separation and domestic residency of operating personnel |
| **Low** | Systems handling public data that contains no personal information | Introduced in 2024. Reasonably relaxes requirements relative to the High/Medium tiers, serving as an entry point for foreign cloud providers |

All three tiers commonly require **domestic data storage (localization)**, **support for Korean-developed encryption algorithms (ARIA, SEED, etc.)**, and **domestic residency of operating personnel**. The Medium and High tiers additionally require physical network separation, which has acted as a barrier to entry for hyperscalers that rely on their standard global regional infrastructure.

## Vendor Certification Status

### Hyperscalers

| Vendor | Certified tier | Date obtained | Notes |
| --- | --- | --- | --- |
| Microsoft Azure | Low | December 2024 | First of the three hyperscalers to obtain certification |
| Google Cloud | Low | February 2025 | |
| AWS | Low | March 28, 2025 | Covers compute, storage, networking, database, and security services in the Seoul region |
| OCI (Oracle) | Preparing, targeting Medium tier | — | Reports indicate OCI is preparing to apply for Medium tier or higher, aiming at database-centric workloads, but official confirmation of completion is still needed |

By the first half of 2025, all three of AWS, Azure, and Google Cloud had obtained CSAP Low-tier certification, opening a path for Korean public institutions to use hyperscalers for public data systems that do not handle personal information. Note, however, that the Low tier cannot be applied to systems handling sensitive information.

### Domestic CSPs

| Vendor | Status |
| --- | --- |
| Naver Cloud | Holds CSAP certification for numerous IaaS/SaaS services. Continues to participate in government programs, including the public-sector SaaS development and verification program |
| KT Cloud | KT G-Cloud (IaaS) has held CSAP certification from October 2021 through October 2026 |
| NHN Cloud | Has obtained CSAP certification for its OpenStack-based infrastructure, expanding its share of the public cloud market |
| Samsung SDS | The Samsung Cloud Platform holds CSAP certification and participates in public-sector projects linked with the National Information Resources Service (NIRS), among others |
| Kakao Cloud | Previously held CSAP certification, but is reported not to have expressed intent to participate in the 2025 public-sector SaaS development and verification program |

:::note
Public-sector SaaS has faced a **duplicate certification problem**, requiring separate CSAP certification for each underlying IaaS environment it runs on. For example, offering a service across KT Cloud, NHN Cloud, and the NIRS Daegu center (Samsung SDS environment) has required obtaining three to four duplicate certifications — one of the factors behind the push to restructure the system.
:::

## 2026 Restructuring — Toward a Unified NIS Verification System

On April 20, 2026, MSIT and the NIS jointly announced a restructuring of the public-sector cloud security verification system. The key points are as follows.

- The verification previously performed in duplicate by MSIT (private-sector CSAP) and the NIS (public-sector security suitability review) will be **consolidated into "NIS Cloud Security Verification."**
- Of CSAP's four existing standards, **standards 1–3 will be folded into MSIT's ISMS and shift to voluntary certification (optional to obtain)**, while **Annex 4, the public-sector security requirement, will be folded into the NIS review**.
- As a result, the private-sector-facing CSAP system that MSIT has operated for ten years will be phased out in stages.
- **The effective date is July 2027**, following roughly a one-year grace period after the relevant notice is amended. Services that have already obtained CSAP certification before then will **retain their current five-year validity period unchanged**.

This restructuring extends a trend under discussion since late 2025 to simplify the dual-track process of "obtain CSAP, then undergo NIS verification." In December 2025, MSIT stated it was pursuing an amendment to the relevant notice that would allow public-sector market entry through NIS security suitability review alone, excluding items already verified during CSAP certification from re-review.

## Considerations for Public-Sector Adoption

- **Tier selection is based on system criticality.** Because vendors certified at the Low tier cannot be used for systems handling personal data or sensitive information, organizations should finalize their data classification and target tier early in adoption.
- **Physical network separation requirements** (Medium/High tiers) directly affect architecture design. Since it is often difficult to port a hyperscaler's standard global architecture as-is, confirm domestic-region and dedicated-infrastructure options in advance.
- **SaaS inherits the CSAP tier of its underlying IaaS.** In addition to the SaaS's own certification, check the certification tier and scope of the IaaS it runs on.
- **In anticipation of post-2027 procedural changes**, when planning new procurement contracts or long-term certification roadmaps, it is safer to also factor in the transition timeline toward the unified NIS verification system.
- CSAP is only a precondition for public-sector procurement in Korea; procurement itself still requires separate steps such as registration on the [Digital Service Mall](https://www.digitalmarket.kr) and use of the Public Procurement Service's Nara Jangteo system.

## References

- [CSAP tier system fully in effect… High tier gets "stronger security certification" — ZDNet Korea](https://zdnet.co.kr/view/?no=20240206112330)
- [CSAP High/Medium tier system in effect..."Security and diplomacy mandated to use private cloud" — Ajunews](https://www.ajunews.com/view/20240206093321587)
- [Public cloud certification to be unified under the NIS...CSAP dismantled after 10 years — ZDNet Korea](https://zdnet.co.kr/view/?no=20260420130424)
- [Public cloud security "unified under the NIS"... CSAP integrated into ISMS — Boannews](https://m.boannews.com/html/detail.html?idx=143270)
- [Cloud Security Assurance Program (CSAP) — Korea Internet & Security Agency (KISA)](https://www.kisa.or.kr/1050603)
