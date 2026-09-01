---
title: "FedRAMP"
description: "An overview of FedRAMP, the security authorization program for US federal cloud procurement, covering the status of the 2026 FedRAMP 20x overhaul, isolated government regions, and CMMC/DoD SRG."
---

> Last reviewed: August 2026

## Overview

FedRAMP (Federal Risk and Authorization Management Program) is a government-wide authorization program that verifies the security of cloud services procured by US federal agencies. It is operated by the FedRAMP PMO under the GSA (General Services Administration) and evaluates and authorizes the security controls of cloud service providers (CSPs) based on the NIST SP 800-53 control framework. Its core principle is "Do Once, Use Many Times" — allowing agencies to reuse a FedRAMP-authorized service rather than each agency repeating its own security review.

FedRAMP is not legally mandatory for private companies, but it is a de facto entry requirement for virtually any cloud service provider seeking to deliver SaaS/PaaS/IaaS to federal agencies.

## The Moderate/High Baselines (Traditional Framework)

FedRAMP has historically graded security control levels based on FIPS 199 impact categorization, which classifies the severity of harm from a loss of confidentiality, integrity, or availability.

| Tier | Applies to | Characteristics |
| --- | --- | --- |
| **Low** | Public information systems where impact from compromise is limited | Minimum number of controls |
| **Moderate** | Most federal agency operational systems, including systems handling CUI (Controlled Unclassified Information) | Standard target baseline for commercial SaaS/PaaS. Roughly 320 control items |
| **High** | Law enforcement, emergency services, financial systems, and other systems where compromise has severe impact | Roughly 420 control items; highest authorization difficulty and cost |

Most commercial cloud services are authorized at the Moderate baseline, while the High baseline is primarily required for sensitive systems at agencies such as the Department of Homeland Security and the Department of Justice.

## Status of the 2026 FedRAMP 20x Overhaul (per official fedramp.gov guidance)

:::caution
FedRAMP 20x is an overhaul still in progress as of August 2026, and details are changing rapidly. The information below reflects what has been confirmed on the official [fedramp.gov](https://www.fedramp.gov/) pages and announcements; anyone evaluating actual adoption must re-verify the latest guidance directly on fedramp.gov.
:::

FedRAMP is transitioning from its traditional three-tier Low/Moderate/High framework to the automation-first **FedRAMP 20x** program.

- **Certification Class framework**: A four-tier Class A/B/C/D Certification Class framework was introduced based on NTC-0004 (a policy document) published on February 25, 2026. Importantly, a Class is not a substitute for a security level — it is **a classification that defines the scope of assessment and authorization** (the materials to be submitted, how evidence is shared, and how the review is conducted). FedRAMP's official documentation states that "the baseline defines the scope of assessment and authorization, not the overall quality or security level of the cloud service." Existing Rev5 Moderate-level systems (handling non-public federal data such as CUI) are, in practice, guided to transition to the Class C path.
- **2026 Consolidated Rules (CR26)**: A consolidated rule finalized and effective in late June 2026 that requires authorization packages to be submitted primarily in machine-readable format, phasing out the legacy Word/Excel template-based packages. CSPs must use automation to keep their authorization packages continuously up to date whenever changes occur.
- **Current operational status (as of August 2026)**: This is a transitional period: the Class A pipeline opened in early August, while Classes B/C are scheduled to open on August 31, 2026. Per official fedramp.gov statistics, of roughly 529 total authorized services, approximately 28 have been authorized under the new FedRAMP 20x framework, while the large majority still operate under the existing Rev5 (Low/Moderate/High) framework.
- **Class D (High-equivalent) under development**: Class D, corresponding to the high-risk tier, is still under development, with a pilot planned for Q1–Q2 2027.
- **Rev5 sunset timeline**: The existing Rev5 framework will continue accepting new authorizations through June 11, 2027, after which a transition path for services holding existing Rev5 authorizations is expected to be established in the second half of 2027.

:::note
In other words, as of August 2026 the new 20x framework and the existing Rev5 framework coexist in a transitional period. Which framework a given target agency or service was authorized under must be individually verified on the [FedRAMP Marketplace](https://marketplace.fedramp.gov/).
:::

## Isolated Regions: GovCloud, Azure Government, Assured Workloads, OCI Government

Workloads that need to meet FedRAMP High and DoD requirements often use government-only regions that are physically and logically separated from commercial regions.

| Region | Characteristics |
| --- | --- |
| **AWS GovCloud (US)** | Supports FedRAMP High, DoD SRG IL2/4/5, ITAR/EAR, and CJIS. Physically located within the United States; operational access limited to US citizens. Account owners must be a US Person |
| **Azure Government** | Physically and logically isolated from commercial Azure, operated by vetted US personnel. Supports FedRAMP High, DoD IL4/5, CJIS, and ITAR |
| **Google Assured Workloads** | Applies software-defined controls (data residency, encryption key management, etc.) on top of standard GCP regions rather than separate physical infrastructure. IL5 and above are provided a dedicated environment |
| **OCI Government Cloud** | A government-only region targeted at workloads dependent on Oracle databases and enterprise applications |

## CMMC 2.0 and DoD SRG Impact Levels

**CMMC 2.0** (Cybersecurity Maturity Model Certification) is a cybersecurity certification program that applies to contractors in the Department of Defense (DoD) supply chain, structured across three levels.

- **Level 1 (Foundational)**: For contractors handling FCI (Federal Contract Information); self-assessment
- **Level 2 (Advanced)**: For contractors handling CUI; based on NIST SP 800-171; most require certification by a C3PAO (third-party assessment organization)
- **Level 3 (Expert)**: For the highest-sensitivity information; adds NIST SP 800-172 controls; assessment led by the government (DIBCAC)

The CMMC final rule (32 CFR Part 170) took effect in 2024, and the amended DFARS 252.204-7021 rule incorporating it into contracts took effect on November 10, 2025. However, as of August 2026, the phased implementation schedule (following Phase 2) is understood to be temporarily on hold for review, so **the exact implementation phase must be reconfirmed at the time of contracting.**

**DoD Cloud Computing SRG (Security Requirements Guide) Impact Levels** classify cloud environments based on the sensitivity of DoD information.

| Impact Level | Information covered | Infrastructure requirements |
| --- | --- | --- |
| **IL2** | Publicly releasable information | Commercial cloud level |
| **IL4** | CUI and non-public unclassified information | Strong logical separation; shared infrastructure permitted |
| **IL5** | Highly sensitive CUI, mission-critical and national security system information | Dedicated infrastructure; operational personnel must be US citizens |
| **IL6** | Classified (SECRET) and national security system information | Fully isolated environment |

IL1 and IL3 do not exist as separate levels (IL1 is unnecessary; IL3 has been merged into IL4), and FedRAMP Moderate authorization roughly corresponds to the minimum requirements of IL2.

## Practical Implications

- FedRAMP authorization is a de facto essential condition for entering the US federal SaaS market, and obtaining it requires significant time and cost. FedRAMP 20x is an attempt to automate and shorten this process, but as of August 2026 it remains in a transitional period, so companies entering the market should decide which framework (Rev5 vs. 20x) to pursue authorization under based on the latest guidance on fedramp.gov.
- Organizational barriers to entry — securing a Sponsoring Agency, establishing a US legal entity and operational organization, staffing predominantly with US personnel — are often as significant as the technical controls themselves.
- Rather than pursuing authorization directly, a common initial market-entry strategy is to build SaaS on top of infrastructure that already holds FedRAMP authorization (GovCloud, Azure Government, etc.) or to partner with an authorized party as a reseller/OEM.
- For companies participating in the defense/aerospace supply chain, CMMC certification may be required separately from FedRAMP, so this should be verified individually depending on the type of contract involved.

## References

- [FedRAMP official site](https://www.fedramp.gov/)
- [FedRAMP Marketplace](https://marketplace.fedramp.gov/)
- [FedRAMP 20x program](https://www.fedramp.gov/20x/)
- [FedRAMP update announcements](https://www.fedramp.gov/blog/)
- [AWS GovCloud (US) compliance](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-compliance.html)
- [Azure Government official page](https://azure.microsoft.com/en-us/explore/global-infrastructure/government/)
- [Google Cloud Assured Workloads overview](https://cloud.google.com/assured-workloads/docs/overview)
- [DoD Cloud Computing SRG (public.cyber.mil)](https://public.cyber.mil/dccs/)
- [CMMC official information (DoD CIO)](https://dodcio.defense.gov/cmmc/)
