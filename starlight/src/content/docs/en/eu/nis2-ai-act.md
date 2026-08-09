---
title: "NIS2 + EU AI Act"
description: "Covers NIS2's cybersecurity and incident-reporting obligations, the EU AI Act implementation timeline, and the 2026 Digital Omnibus deferral of high-risk AI obligations."
---

> Last reviewed: August 2026

## Overview

NIS2 (the Cybersecurity Directive) and the EU AI Act (the AI regulation) are laws with different purposes, but together they create requirements that organizations operating cloud and AI workloads need to review in tandem. NIS2 addresses "the cybersecurity obligations of organizations providing essential or important services," while the EU AI Act addresses "regulatory obligations scaled to the risk level of an AI system." Both laws are currently undergoing amendment and deferral as part of the European Commission's recent "Simplification" push, so it is important to track the latest implementation dates precisely.

## NIS2 — Cybersecurity Obligations

**NIS2 (Directive (EU) 2022/2555)** entered into force on January 16, 2023, and the deadline for member states' national transposition was **October 17, 2024**.

### Scope

NIS2 divides organizations into two groups by risk level.

| Category | Example entities |
| --- | --- |
| **Essential Entities** | Energy, transport, banking, financial market infrastructure, health, water and wastewater, **digital infrastructure (including cloud service providers)**, ICT service management, public administration, space |
| **Important Entities** | Postal and courier services, waste management, chemicals, food, manufacturing, digital providers (online marketplaces, etc.), research institutions |

:::note
**Cloud service providers themselves fall within NIS2's "Essential Entities" category (digital infrastructure).** In other words, not only companies that use cloud services but vendors themselves are directly subject to NIS2 regulation. If your organization supplies services to other essential/important entities, you must treat your vendors' NIS2 compliance posture as a subject of due diligence under the supply-chain security requirements (NIS2 Article 21).
:::

### Incident Reporting Deadlines

NIS2 mandates staged reporting deadlines.

1. **Within 24 hours** — early warning
2. **Within 72 hours** — incident notification plus initial impact assessment
3. **Within 1 month** — final report

### Status of Member State Transposition

:::caution
**Transposition status varies by country and continues to change.** Only a handful of member states — Belgium, Croatia, Italy, and Lithuania among them — met the original transposition deadline (October 17, 2024), and the European Commission opened infringement proceedings against a majority of member states in late 2024. As of the first half of 2026, the large majority of the 27 member states had completed transposing legislation (Luxembourg completed in May 2026), while **Ireland, Spain, France, and the Netherlands — against which the European Commission decided to refer cases to the Court of Justice in July 2026 — were still lagging**. This picture can change over time, so the latest transposition status in any given member state where you operate should be confirmed through that country's competent authority.
:::

In addition, the **Cybersecurity Act 2 (CSA2)** amendment announced by the European Commission on January 20, 2026, is part of a package that also revisits NIS2, and it includes a move toward simplifying divergent national implementation — meaning NIS2's own requirements may still be adjusted going forward.

## EU AI Act Timeline

The **EU AI Act (Regulation (EU) 2024/1689)** entered into force on August 1, 2024, and its provisions apply on a staggered schedule.

| Date | Application |
| --- | --- |
| **2025.2.2** | Prohibited AI practices (social scoring, real-time remote biometric identification, etc.) and AI literacy obligations take effect |
| **2025.8.2** | Obligations for GPAI (general-purpose AI) model providers take effect — transparency, copyright, and safety/security documentation obligations. However, **enforcement (sanction) powers only take effect from 2026.8.2**, making the first year effectively a grace period |
| **~~2026.8.2 (original)~~** | Originally the application date for high-risk AI system (Annex III) obligations, but this was **deferred by the Digital Omnibus** described below |

### High-Risk AI Obligations Deferred Under the Digital Omnibus (Confirmed)

In the first half of 2026, EU lawmakers reached a provisional agreement on the **AI Act Digital Omnibus**, which was passed by the European Parliament in plenary vote on June 16, 2026 (423 in favor, 57 against, 174 abstentions) and then received **final approval from the Council of the EU on June 29, 2026**. The key changes are as follows.

- **Standalone high-risk AI systems (Annex III)**: application date deferred by 16 months, from 2026.8.2 to **2027.12.2**
- **AI embedded in regulated products (Annex I, such as medical devices and machinery)**: application date deferred by 12 months, from 2027.8.2 to **2028.8.2**
- New provisions added: prohibitions on non-consensual AI-generated sexual imagery ("nudifier" apps) and child sexual abuse material (CSAM) were added to the Article 5 list of prohibited practices

:::note
As of August 9, 2026, this deferral is **already a settled legal fact** (not "still under debate"). However, the GPAI obligations (which took effect in August 2025) are not subject to this deferral and are already in force — only the Commission's power to sanction GPAI violations takes effect from 2026.8.2. Do not confuse the two dates.
:::

## Practical Impact on Cloud Architecture and AI Workloads

- **Automate NIS2 incident response**: the short 24-hour and 72-hour reporting deadlines are difficult to meet with manual processes. Reporting deadlines should be designed backward by linking cloud vendors' incident-notification SLAs with your own SOC (Security Operations Center) processes.
- **Document supply-chain due diligence**: if your organization is an NIS2 essential/important entity, your cloud/ICT vendors' NIS2 compliance posture (certifications, security controls) must be built into your contracting and audit processes.
- **Read the high-risk AI deferral as "more time," not "no need to worry"**: although Annex III high-risk AI obligations have been pushed to December 2027, data governance, model documentation, and human-oversight frameworks take time to build, so it is advantageous to factor them into design now. In particular, if you operate or plan workloads that fall into high-risk categories (recruitment, credit scoring, law enforcement-related, etc.), it is advisable to put data lineage and audit-log systems in place early.
- **GPAI obligations are already in effect**: if you develop or provide your own foundation model, or offer a service in the EU that embeds a GPAI model, you must already comply with the transparency, copyright, and safety documentation obligations.
- **Reconfirming the latest status is essential**: NIS2 transposition status and the AI Act's detailed implementing measures (harmonized standards, high-risk classification guidelines) continue to be updated, so it is safer to build a process for reconfirming them from official sources at project kickoff.

## References

- [EUR-Lex — NIS2 Directive (Directive (EU) 2022/2555)](https://eur-lex.europa.eu/eli/dir/2022/2555/oj)
- [ENISA — NIS2 Directive](https://www.enisa.europa.eu/topics/nis-directive)
- [EUR-Lex — EU AI Act (Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [artificialintelligenceact.eu — EU AI Act Explained](https://artificialintelligenceact.eu/)
- [European Commission — AI Regulatory Framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [Council of the EU — Final Approval of the AI Digital Omnibus Press Release (2026.6.29)](https://www.consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/)
