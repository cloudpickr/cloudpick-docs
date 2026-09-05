---
title: "GDPR and Data Sovereignty"
description: "Covers the GDPR cross-border transfer framework, the EU Data Boundary, a comparison of sovereign cloud options, and the state of the EUCS certification scheme."
---

> Last reviewed: August 2026

## Overview

:::note[Prerequisites and related documents]
For EU cloud regulation overall, see the [EU Guide](../../eu/); for general data protection principles, see [Data Protection](../../security/data-protection/) first. This document focuses on the GDPR cross-border transfer framework and sovereign cloud options.
:::

The General Data Protection Regulation (GDPR) has continued to evolve since taking effect in 2018. Changes in recent years have shown up less in the statutory text itself than in the strengthening of demands around **"where personal data is physically processed, and by whom."** This document outlines the cross-border transfer framework encountered when global enterprises expand cloud workloads to the EU or process EU customer data, and examines the "Sovereign Cloud" options that have emerged against this backdrop.

## GDPR Cross-Border Transfer Framework

Chapter V of the GDPR requires separate safeguards for transfers of personal data outside the EU. The main mechanisms used in practice are as follows.

| Mechanism | Description |
| --- | --- |
| **Adequacy Decision** | When the European Commission recognizes that a given country's level of personal data protection is equivalent to the GDPR, transfers to that country require no additional safeguards |
| **SCCs (Standard Contractual Clauses)** | European Commission-approved standard clauses executed between contracting parties for transfers to countries without an adequacy decision. The 2021 revision is the current version |
| **BCRs (Binding Corporate Rules)** | Binding internal rules applied to transfers within a multinational corporate group |

### Adequacy Decisions Overview (Japan, Korea, UK, US DPF, etc.)

The European Commission has adopted **adequacy decisions** for key trading partners including Japan (2019), the Republic of Korea (December 2021), the United Kingdom, Switzerland, Canada, and the United States (EU-US Data Privacy Framework, 2023).

:::caution
**Adequacy decisions apply in principle to transfers from the EU to the recipient country (EU → destination country).** In other words, personal data can be transferred from the EU to an adequacy-recognized country without additional safeguards such as SCCs. However, in the reverse direction, where a non-EU company directly collects or processes personal data of individuals in the EU (subject to GDPR Article 3 extraterritorial reach), GDPR compliance obligations apply directly. An adequacy decision does not exempt a company from GDPR compliance obligations themselves.
:::

When a global enterprise uses cloud services in an EU region to process EU customer data or transfers data overseas, it must, regardless of the direction of transfer, confirm that the vendor contract (the DPA, or Data Processing Addendum) includes SCCs, and that the region and governance options the vendor offers satisfy its own data classification requirements.

## EU Data Boundary

The **EU Data Boundary** is a data-residency initiative that Microsoft has pursued, aimed at storing and processing the data of EU/EFTA customers only within the EU/EFTA.

- **January 2023**: Phase 1 — customer data and pseudonymized personal data for core cloud services such as Microsoft 365, Dynamics 365, and Power Platform stored within the EU
- **February 26, 2025**: Completion (Phase 3) — extended to **Professional Services Data**, including support logs and case notes, storing them within the EU/EFTA as well; Microsoft announced the completion of enhanced data residency and transparency (though some limited operational exceptions for cross-border access/transfer remain under documented conditions)

Other vendors are expanding similar in-region data-processing guarantees, but the "EU Data Boundary" name and its scope (which includes Professional Services Data) are specific to Microsoft's initiative. The scope of EU-region data-residency guarantees for other vendors must be verified individually in each vendor's contractual documentation (the DPA).

## Comparing Sovereign Cloud Options

In response to demand to keep not just data storage location but also **operating personnel, administrative access, and legal jurisdiction in emergencies** confined to the EU, major vendors have operated or announced the following "sovereign cloud" options.

| Vendor | Option | Form | Status |
| --- | --- | --- | --- |
| **AWS** | European Sovereign Cloud | Independent region (physically and logically separated from existing AWS regions) | Reached general availability (GA) on January 15, 2026, with Brandenburg, Germany as the first region. Announced a long-term €7.8 billion investment, with plans to expand sovereign Local Zones to Belgium, the Netherlands, and Portugal |
| **Microsoft** | Bleu (France) / Delos Cloud (Germany) | Partner-operated sovereign cloud (national partner cloud) | Bleu is a joint venture between Orange and Capgemini (targeting SecNumCloud certification); Delos Cloud is an SAP subsidiary. A mutual-support agreement was signed in November 2025, and an MoU between Delos and Microsoft secures Delos's legal right to access Microsoft's cloud code in an emergency (such as a foreign government restricting service) |
| **OCI** | EU Sovereign Cloud | Physically separate, EU-dedicated regions | Operating since June 2023, with Frankfurt and Madrid regions. Operated only by EU legal entities and EU-resident personnel, with no additional fees compared to commercial OCI |
| **Google Cloud** | Sovereignty partnerships (T-Systems, Thales/S3NS, Proximus) | Partner-operated regions | Germany is handled by T-Systems, France by Thales subsidiary S3NS (targeting SecNumCloud), and Belgium/Luxembourg in partnership with Proximus. In May 2026, Thales and Google Cloud announced a new sovereign cloud partnership in Germany |

:::note
"Sovereign cloud" is defined differently, and with different scope, by each vendor — ranging from guaranteeing only data storage location to covering operating personnel, key management, and legal access rights in an emergency. Before adoption, confirm in the contractual documentation exactly what each vendor confines to the EU (storage vs. processing vs. operational access vs. governance).
:::

## The Fluid State of the EUCS Certification Scheme

**EUCS (European Cybersecurity Certification Scheme for Cloud Services)** is a common security certification framework for cloud services led by ENISA, originally intended to standardize cloud vendors' security levels into EU-wide, mutually recognized tiers (Basic/Substantial/High).

:::caution
**As of August 2026, EUCS's "sovereignty requirements" remain unsettled and under debate.**

- Early drafts included an immunity requirement excluding non-EU ownership and governance for the highest tier (High+) certification.
- The 2023 revised draft relaxed this, requiring data localization only for the High+ tier and leaving open the possibility of certifying "trusted non-EU cloud providers."
- The **Cybersecurity Act 2 (CSA2) amendment** announced by the European Commission on January 20, 2026, proposed reorganizing the certification framework around technical criteria, and work on the EUCS and EU5G schemes is expected to resume within that process.
- The final EUCS text remains unsettled, and whether it will include sovereignty requirements is still a matter of disagreement among EU member states. **The latest confirmed status must be verified separately through official ENISA and European Commission announcements.**
:::

EUCS remains a voluntary certification for now, but NIS2 and the Data Act (in force since January 2024, with core provisions applicable since September 2025) give member states and regulators the authority to mandate the use of EUCS-certified vendors for public bodies and essential/important entities, which could affect future procurement requirements.

## Architectural Implications

- **Start with data classification**: First classify which data is subject to EU in-region storage/processing obligations (public procurement requirements, contractual requirements, internal risk policy), then decide on region and vendor options.
- **Sovereign options come with cost/functionality trade-offs**: Sovereign regions may offer a narrower range of services or lag behind in rolling out new features compared to standard commercial regions. Where it is not a strict requirement, a standard EU region combined with strengthened governance (encryption, access transparency logging) is often sufficient.
- **Reviewing the DPA and contract matters as much as region selection**: Confirm directly in the contractual documentation whether SCCs are included, the list of sub-processors, and emergency access clauses.
- **Do not design around fluid regulations like EUCS as if they were settled**: Rather than treating unfinalized certification requirements as a mandatory architectural premise, leave room to adapt once they are finalized.
- **Link to sovereign landing zone design**: For concrete patterns that reflect EU data residency and processing jurisdiction requirements in landing zone guardrails, see [Landing Zone — Sovereign Landing Zone](../../governance/landing-zone/#sovereign-landing-zone).

## References

- [EUR-Lex — GDPR (Regulation (EU) 2016/679)](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [European Commission — Adequacy Decision Q&A (Korea)](https://ec.europa.eu/commission/presscorner/detail/en/qanda_21_6916)
- [European Commission — List of Data Protection Adequacy Decisions](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en)
- [EDPB — Opinion on the Draft Korea Adequacy Decision](https://edpb.europa.eu/news/news/2021/edpb-adopts-opinion-draft-south-korea-adequacy-decision_en)
- [Microsoft — EU Data Boundary Completion Announcement (2025.2)](https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/)
- [AWS — European Sovereign Cloud Launch Announcement (2026.1)](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe)
- [Microsoft — Announcing European Sovereign Solutions (2025.6)](https://blogs.microsoft.com/blog/2025/06/16/announcing-comprehensive-sovereign-solutions-empowering-european-organizations/)
- [Google Cloud — Sovereign Cloud](https://cloud.google.com/sovereign-cloud)
- [Oracle — Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)
