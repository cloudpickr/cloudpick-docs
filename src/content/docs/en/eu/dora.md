---
title: "DORA (Digital Operational Resilience Act)"
description: "Covers DORA's scope of application, the status of CTPP designations, and ICT risk management, concentration risk, and exit strategy requirements."
---

> Last reviewed: August 2026

## Overview

**DORA (Digital Operational Resilience Act)** is a regulation that standardizes ICT risk management across the EU financial sector. Non-EU financial institutions' EU subsidiaries and branches, vendors that provide cloud/ICT services to EU financial institutions, and domestic IT suppliers that contract with them can all fall within DORA's reach. Because DORA is a Regulation, it applies directly across the EU without requiring separate implementing legislation in each member state.

## Applicability and Scope

DORA entered into force on January 16, 2023, and **has applied since January 17, 2025**.

- **Covered financial entities**: EU-regulated financial entities across 20 categories (per the EU Commission's 2026 review document), estimated at around 20,000, including banks, insurers, investment firms, payment institutions, and crypto-asset service providers. Supervision is divided by category among the EBA (European Banking Authority), EIOPA (European Insurance and Occupational Pensions Authority), and ESMA (European Securities and Markets Authority) — collectively, the **ESAs (European Supervisory Authorities)**.
- **Covered ICT third-party providers**: ICT service providers (cloud, data center, software vendors, etc.) that support "critical or important functions" for the above financial entities are also indirectly subject to DORA requirements. This is because financial entities must reflect DORA-mandated clauses (access rights, audit rights, termination clauses, etc.) in their contracts with these providers.

:::note
Regardless of a vendor's headquarters location, DORA effectively applies to **any ICT third-party provider that has a contractual relationship with an EU financial entity**. Even a SaaS or cloud service based outside the EU can become a counterparty subject to DORA's contractual requirements if it has EU financial-entity customers.
:::

## Status of CTPP Designations

DORA introduces a regime for directly overseeing systemically important ICT third-party providers by designating them as **CTPPs (Critical ICT Third-Party Providers)**.

On **November 18, 2025**, the ESAs published the first list of CTPPs. A total of **19** entities were designated, including the three hyperscalers **AWS, Google Cloud, and Microsoft**, along with data center operators, telecommunications companies, and fintech specialists.

The designation criteria are assessed comprehensively across:

- Systemic impact in the event of a disruption
- The number and importance of the financial entities that depend on the provider
- Market concentration
- The feasibility of switching to an alternative provider

**New obligations for designated CTPPs**:

- A CTPP headquartered outside the EU must establish an EU subsidiary within 12 months of designation (serving as the EU coordination point)
- Pay an annual oversight fee to the ESAs
- Become subject to regulatory oversight at a level comparable to financial entities, including risk assessments and incident reporting
- Exposure to potential sanctions for non-compliance (previously only financial entities were directly regulated, but under DORA vendors are now also subject to direct oversight)

## Core ICT Risk Management Requirements

DORA's core requirements for financial entities fall into five broad areas.

| Area | Requirement |
| --- | --- |
| **ICT risk management framework** | An enterprise-wide ICT risk management framework approved by the board, with regular review |
| **Incident classification and reporting** | Major ICT incidents must be reported to supervisors within set deadlines (initial report → intermediate report → final report) |
| **Resilience testing** | Tiered testing ranging from vulnerability scans to TLPT (Threat-Led Penetration Testing) |
| **ICT third-party risk management** | Maintaining a Register of Information, mandatory contractual clauses, and concentration-risk assessment |
| **Information sharing** | A framework for voluntarily sharing cyber threat intelligence among peer institutions |

## Concentration Risk and Exit Strategy

The provisions of DORA most directly connected to cloud architecture are those on **ICT third-party risk management**.

- **Register of Information**: Financial entities must maintain a register of all ICT third-party contracts (direct and indirect, including sub-outsourcing) and submit it to supervisors upon request.
- **Concentration risk assessment**: Excessive reliance on a small number of vendors (particularly hyperscalers designated as CTPPs) must be assessed regularly. Where core functions are concentrated with a single cloud vendor, a contingency plan is required.
- **Exit strategy documentation**: For ICT services that support "critical or important functions," a **written exit strategy must be established and tested regularly**. If an organization has a contractual relationship with any of the 19 listed CTPPs, it is practically advisable to document an exit plan for that vendor and review it at least once a year.

:::note
The specific methodology for concentration-risk assessment and exit-strategy development (asset inventory, trigger scenarios, migration procedures) is covered in [Vendor Lock-in and Exit Strategy](../../governance/exit-strategy/). DORA is a clear example of this methodology becoming **a regulatory obligation rather than an option in the financial sector**.
:::

## Architectural and Practical Implications

- **Multi-cloud is a tool for mitigating concentration risk, not a goal in itself.** DORA does not mandate the use of multiple vendors. Using a single vendor is not itself a regulatory problem, provided it is documented alongside a risk assessment and mitigation plan.
- **Confirm that DORA-mandated clauses are reflected in contracts with CTPP vendors** (access and audit rights, data location, sub-outsourcing notification, termination-support obligations, etc.). Large vendors often already provide standard DORA-response contract addenda.
- **Reflect DORA reporting deadlines in incident-response processes.** If a vendor's incident-notification SLA is slower than the financial entity's supervisory reporting deadline, it can lead to a regulatory violation.
- **Systematically managing register-of-information metadata (contract scope, data location, sub-processors) from the landing zone design stage onward** is more efficient than reconstructing it after the fact for an audit.

## References

- [EUR-Lex — DORA (Regulation (EU) 2022/2554)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- [EIOPA — Digital Operational Resilience Act](https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en)
- [ESMA — Digital Operational Resilience Act](https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/digital-operational-resilience-act-dora)
- [ESAs — Critical ICT Third-Party Provider (CTPP) Designation Announcement (2025.11)](https://www.lexology.com/library/detail.aspx?g=b3331558-10d0-4936-b215-4cfb1c2b33d6)
- [AWS Security Blog — On AWS's Designation as a Critical Third-Party Provider Under DORA](https://aws.amazon.com/blogs/security/aws-designated-as-a-critical-third-party-provider-under-eus-dora-regulation)
- [Microsoft — What Is DORA](https://learn.microsoft.com/en-us/compliance/dora/dora-what-is-dora)
