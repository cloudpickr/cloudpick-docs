---
title: "HIPAA/HITECH"
description: "An overview of HIPAA/HITECH, the US regulation protecting healthcare data — the definition of PHI, the BAA structure, the relationship with HITRUST CSF, and encryption/audit log requirements."
---

> Last reviewed: August 2026

## Overview

HIPAA (Health Insurance Portability and Accountability Act, 1996) is the US federal law protecting healthcare information, enforced by the Office for Civil Rights (OCR) under the Department of Health and Human Services (HHS). HITECH (Health Information Technology for Economic and Clinical Health Act), enacted in 2009, strengthened HIPAA's enforcement power in response to the spread of electronic health records and introduced a data breach notification requirement (the Breach Notification Rule). The two laws are commonly referred to together as "HIPAA/HITECH."

HIPAA is not a single certification program but a framework of legal requirements that organizations must satisfy — there is no official credential called "HIPAA certification." Organizations must meet the requirements themselves and demonstrate this through documentation and audits.

## Definition of PHI (Protected Health Information)

PHI (Protected Health Information) refers to information that satisfies all of the following conditions:

- Created or received by a healthcare provider, health plan, employer, or healthcare clearinghouse
- Relates to an individual's past, present, or future physical or mental health condition, the provision of healthcare, or payment for that care
- Is individually identifiable

This includes not only electronic form (ePHI) but also paper records, test results, imaging, billing statements, and even verbal conversations that include personally identifiable information. From a cloud architecture perspective, ePHI is the primary form that is stored, transmitted, and processed.

## Covered Entity, Business Associate, and the BAA Structure

HIPAA divides regulated parties into two groups.

- **Covered Entity**: An organization that provides or pays for healthcare — healthcare providers, health plans, healthcare clearinghouses
- **Business Associate**: A third party that collects, stores, or transmits PHI on behalf of a Covered Entity — most cloud vendors, SaaS providers, and data processing companies fall into this category

When a Covered Entity outsources PHI processing to an external party, it must execute a legal contract called a **Business Associate Agreement (BAA)**, which specifies the purposes for which the Business Associate may handle PHI and the security/privacy requirements it must follow. When a Business Associate further subcontracts to a subcontractor, an equivalent subcontractor BAA must likewise be executed.

:::note
Cloud service providers are generally considered to hold Business Associate status. In other words, executing a BAA with a cloud vendor is a legal prerequisite for placing PHI on that cloud.
:::

## How to Verify Vendor-Specific BAA Coverage

Major cloud vendors offer a BAA as part of their standard agreements, but **executing a BAA does not automatically cover every service.**

- **AWS**: A BAA can be executed at the account level through AWS Artifact, but only services included on the "HIPAA-eligible services" list fall within BAA coverage.
- **Azure**: Offers a BAA as part of its standard Online Services Terms, and is known to cover a relatively broad range of services, though the service-specific list still needs to be checked.
- **Google Cloud**: Offers a BAA through its standard terms, covering only designated eligible services.

When designing architecture, it is essential to check the vendor's latest official "HIPAA-eligible services list" to confirm that the intended service is included — processing or storing PHI on a service not on the list forfeits BAA protection. Additionally, a BAA covers only the vendor's side of the shared responsibility model; securely configuring services, restricting PHI access, and encrypting data remain the responsibility of the customer (the Covered Entity/Business Associate).

## Relationship with HITRUST CSF

HITRUST CSF is a security framework operated not by a government body but by a private organization (the HITRUST Alliance), consolidating over 40 security and regulatory standards, including HIPAA, into a single framework.

- HIPAA is a law, while HITRUST CSF is a practical framework for complying with that law along with several other standards.
- Obtaining HITRUST CSF certification does not automatically mean "HIPAA compliance" (since HIPAA has no official certification program to begin with), but HITRUST certification, which involves a third-party audit, is widely used as strong circumstantial evidence of meeting HIPAA requirements.
- A significant portion of US hospitals and many health insurers have adopted HITRUST as a means of vendor evaluation and self-compliance demonstration, so for companies seeking to sell healthcare SaaS to US enterprise customers, HITRUST CSF certification often functions as a de facto market requirement.

## Encryption and Audit Log Requirements

The current HIPAA Security Rule has historically divided safeguards into "Required" and "Addressable" (allowing alternative measures). However, HHS announced a proposed rule (NPRM) in December 2024 (published in the Federal Register in January 2025) that would eliminate this distinction and make most safeguards mandatory.

:::caution
This proposed rule is **not finalized** as of August 2026. After the public comment period closed in March 2025, the target date for the final rule has been pushed back to July 2027, per the OMB Unified Agenda. The items below remain at the proposal stage; whether and when they will actually take effect must be reconfirmed through official HHS announcements.
:::

Key proposed changes:

- Encryption of ePHI at rest and in transit would generally become mandatory (with only limited exceptions)
- Multi-factor authentication (MFA) for access to PHI systems would become mandatory
- Near-real-time automated audit log monitoring, with strengthened log protection controls
- Stronger long-term log retention — the existing six-year retention requirement applies to documentation such as policies and procedures, and the proposal would extend it to cover logs as well
- Vulnerability scans at least every six months, and penetration testing at least annually

Regardless of whether the proposed rule is finalized, encryption at rest and in transit and access logging have already become established industry-standard practices, so it is prudent to build them into new architectures proactively.

## Implications for Healthcare SaaS Architecture

- **Use only eligible services**: Confirm at the design stage that every service through which PHI flows is included on the vendor's BAA-eligible services list.
- **Make encryption the default**: Adopt encryption at rest and in transit as a baseline architectural requirement even where current rules classify it as "addressable." This prepares you for future mandatory requirements.
- **Access control and audit logging**: Implement least-privilege access to PHI, MFA, centralized audit logging (integrated with a SIEM), and a long-term retention policy. For related architecture, see [Data Protection and Workload Security](../../security/data-protection/) and [Security Incident Response](../../security/incident-response/).
- **Consider HITRUST certification**: Since HITRUST CSF certification often becomes a de facto requirement when selling to US healthcare enterprise customers, build a certification roadmap in from the start.
- **Manage the subcontractor BAA chain**: Track, as part of contract management, whether a BAA has been executed with every downstream cloud/SaaS vendor your company uses.

## References

- [HHS HIPAA official page](https://www.hhs.gov/hipaa/)
- [HHS Covered Entities and Business Associates](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html)
- [HHS HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [AWS HIPAA compliance](https://aws.amazon.com/compliance/hipaa-compliance/)
- [Microsoft Azure HIPAA/HITECH](https://learn.microsoft.com/azure/compliance/offerings/offering-hipaa-us)
- [Google Cloud HIPAA compliance](https://cloud.google.com/security/compliance/hipaa)
- [HITRUST Alliance](https://hitrustalliance.net/)
