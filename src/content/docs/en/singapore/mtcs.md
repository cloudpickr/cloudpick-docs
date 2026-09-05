---
title: "MTCS (Multi-Tier Cloud Security Standard)"
description: "Covers the tier system, operating bodies, hyperscaler certification status, and additional financial-sector requirements of Singapore's MTCS (SS 584) cloud security standard."
---

> Last reviewed: August 2026

## Overview

MTCS (Multi-Tier Cloud Security) is a cloud security certification scheme enacted as Singapore Standard **SS 584**. It was developed by the Information Technology Standards Committee (ITSC), with support from the Infocomm Media Development Authority (IMDA) and Enterprise Singapore, and is presented as the world's first multi-tiered cloud security standard, distinguishing cloud security levels across several tiers.

First enacted in 2013, it went through SS 584:2015, and the current version is **SS 584:2020**, which strengthened alignment with ISO/IEC 27001:2013 and added control items addressing recent security concepts such as zero trust and continuous monitoring.

Certification is assessed by MTCS Certifying Bodies (CBs) accredited by the Singapore Accreditation Council (SAC). Certificates are valid for three years and must undergo an annual surveillance audit to remain in effect.

:::note
Rather than being a legally mandated barrier to entry, MTCS is better understood as a national standard-based framework (SS 584) that functions as **a widely required qualification in public procurement and financial-sector vendor due diligence**. In government cloud procurement issued by IMDA (such as the Government Commercial Cloud), MTCS certification is commonly specified as a requirement.
:::

## Tier Structure (Level 1–3)

| Level | Target workloads | Characteristics |
| --- | --- | --- |
| **Level 1** | Non-critical operations such as website hosting, test/development environments, and simulations | A low-cost tier requiring only minimal baseline security controls |
| **Level 2** | General business systems at most organizations, including mission-critical applications | An enhanced control set addressing data security threats. The tier most commercial cloud users target |
| **Level 3** | Regulated industries, systems subject to government procurement, and systems processing sensitive or high-impact data | Requires strict additional controls on top of Level 1/2 controls. **Level 3 is often required for government procurement involving high-risk or sensitive systems (not uniformly applied to all government procurement)** |

All three levels can have separate certification scopes by service type (IaaS/PaaS/SaaS), so it is common for a vendor to have only some of its services certified at a given level. When evaluating adoption, be sure to check not just the level but also the **certification scope (which services and regions are included)**.

## IMDA Operating Framework

- The **ITSC (Information Technology Standards Committee)** develops and revises the SS 584 standard itself, supported by IMDA and Enterprise Singapore.
- The **SAC (Singapore Accreditation Council)** accredits the Certifying Bodies (CBs) that perform assessments. CBs are mostly international certification bodies such as BSI, DNV, TÜV, and Ernst & Young Certify Point.
- After certification, vendors must maintain their status through a **3-year renewal cycle plus annual surveillance audits**; failing an audit can lead to suspension or revocation of certification.
- IMDA publishes a list of MTCS-certified cloud services and certificates (including QR codes) on its official website so procurement staff can verify them.

## Hyperscaler Certification Status (as of August 2026)

| Vendor | Certified level | Notes |
| --- | --- | --- |
| AWS | Level 3 (SS 584:2020) | First in the industry to obtain Level 3 in 2014. Renewed against the SS 584:2020 standard in December 2024, expanding certification scope to the Asia Pacific (Singapore), Asia Pacific (Seoul), and US regions |
| Microsoft Azure | Level 3 | Presented as the first CSP in the world to obtain Level 3 certification across all three service categories (IaaS/PaaS/SaaS) for its IaaS/PaaS offerings. Microsoft 365 (Office 365) also separately obtained Level 3 certification against the SS 584:2020 standard in 2021 |
| Google Cloud | Level 3 (Tier 3) | Obtained Tier 3 certification for Google Cloud and Google Workspace services and a subset of data center sites |
| Oracle Cloud Infrastructure (OCI) | Level 3 | Obtained Level 3 certification for the Singapore and Japan regions. The Oracle Fusion Cloud Applications Suite also separately obtained Level 3 certification in December 2021 |

All four major hyperscalers hold MTCS Level 3 certification for at least some of their services and regions. However, since certification scope differs by vendor, it is essential to verify before contracting whether the specific service and region you intend to use falls within the scope specified in the certificate.

## Additional Financial-Sector Requirements

Adopting cloud in Singapore's financial sector requires more than MTCS certification alone — a separate framework set by the Monetary Authority of Singapore (MAS) must also be satisfied.

- **MAS TRM Guidelines (Technology Risk Management Guidelines)** — the January 2021 revision explicitly calls for stronger oversight of third-party (outsourced) providers in response to financial institutions' growing use of cloud, APIs, and agile development. Though a non-binding guideline, it functions as a de facto compliance benchmark during MAS inspections.
- **MAS Notice 655 (Cyber Hygiene)** — a legally binding notice, separate from the TRM Guidelines, that sets minimum security baselines.
- **OSPAR (Outsourced Service Provider's Audit Report)** — an audit framework established by the Association of Banks in Singapore (ABS), under which an external auditor verifies a cloud or other outsourced service provider's controls against ABS guidelines. Financial institutions use the resulting OSPAR report as part of their own vendor due diligence. **OSPAR v2.0**, published in March 2024, requires annual audits starting January 1, 2025, and adds supplementary control criteria specific to cloud service providers (IaaS/PaaS/SaaS).

Major hyperscalers publish OSPAR audit reports annually for use by their Singapore financial-sector customers, and the scope of services covered by these reports has been expanding each year.

## Gatekeeping Role in Public Sector and Financial Sector Entry

- **Public procurement**: within IMDA's government cloud procurement framework, MTCS Level 3 certification functions as a de facto condition of participation. Vendors or services without certification may be barred from bidding altogether.
- **Financial sector**: MTCS certification is only the starting point — actual adoption decisions are often determined by compliance with the MAS TRM Guidelines and possession of an OSPAR audit report. It is advisable to request a vendor's latest OSPAR report early in the adoption process to review its audit scope and any exceptions.
- **Global enterprise entry implications**: Architects already familiar with international frameworks such as ISO/IEC 27001 or SOC 2 in their home markets should note that Singapore operates its own cloud security certification scheme (MTCS) and a separate financial-sector audit framework (OSPAR). Because international standards do not grant automatic full mutual recognition, organizations must plan a dedicated certification and audit roadmap when entering Singapore's public and financial sectors.

## Pre-Adoption Checklist

- **Verify both level and scope**: confirm that the certificate a vendor presents matches, in both level and the list of certified services/regions, what you actually intend to adopt. Certificates (including QR codes) published on the official IMDA website can be used to cross-check validity.
- **Track the renewal cycle**: MTCS certification runs on a 3-year cycle with annual surveillance audits. For long-term contracts, it is advisable to reflect a vendor's recent renewal and surveillance history in contract terms or SLA annexes.
- **Request OSPAR separately for financial-sector use**: MTCS Level 3 certification alone does not complete MAS regulatory compliance. Obtain a vendor's latest OSPAR report (v2.0 baseline) separately and reflect its audit scope, exceptions, and any control gaps in your internal risk assessment.
- **Coordinate public procurement in advance**: if targeting government procurement participation, it is best to confirm the exact certification level and scope required through prior consultation with IMDA or the procuring agency, as requirements can vary by tender.

## References

- [Cloud Computing and Services — Infocomm Media Development Authority (IMDA)](https://www.imda.gov.sg/regulations-and-licensing-listing/ict-standards-and-quality-of-service/it%20standards%20and%20frameworks/cloud%20computing%20and%20services)
- [MTCS Tier 3 — AWS Compliance](https://aws.amazon.com/compliance/aws-multitiered-cloud-security-standard-certification/)
- [AWS renews MTCS Level 3 certification under the SS584:2020 standard — AWS Security Blog](https://aws.amazon.com/blogs/security/aws-renews-mtcs-level-3-certification-under-the-ss5842020-standard)
- [Multi-Tier Cloud Security (MTCS) Standard for Singapore — Microsoft Learn](https://learn.microsoft.com/en-us/compliance/regulatory/offering-mtcs-singapore)
- [MTCS — Compliance | Google Cloud](https://cloud.google.com/security/compliance/mtcs)
- [Oracle's MTCS certification creates new opportunities for customers in Singapore — Oracle Cloud Infrastructure Blog](https://blogs.oracle.com/cloud-infrastructure/oracle-mtcs-certification-creates-new-opportunities-for-customers-in-singapore)
- [MAS Enhances Guidelines to Combat Heightened Cyber Risks — Monetary Authority of Singapore](https://www.mas.gov.sg/news/media-releases/2021/mas-enhances-guidelines-to-combat-heightened-cyber-risks)
- [OSPAR (Singapore) — Microsoft Azure Compliance](https://learn.microsoft.com/en-us/azure/compliance/offerings/offering-ospar-singapore)
- [OSPAR — Compliance | Google Cloud](https://cloud.google.com/security/compliance/ospar)
- [ABS OSPAR Guidelines v2.0 — Association of Banks in Singapore](https://abs.org.sg/docs/library/abs-ospar-guidelines-v2-0.pdf)
