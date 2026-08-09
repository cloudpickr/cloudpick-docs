---
title: "The State Privacy Law Landscape"
description: "Covers the absence of a federal comprehensive privacy law in the US, the common requirements shared across 20-plus state privacy laws, and multi-state compliance architecture."
---

> Last reviewed: August 2026

## Overview

The United States has **no federal comprehensive personal-data-protection law** comparable to the EU's GDPR. Instead, while sector-specific federal laws such as HIPAA (healthcare), GLBA (finance), and COPPA (children) operate individually, regulation of general consumer personal data has been left to each state to legislate independently. As a result, as of 2026, more than 20 states are enforcing their own (though substantially similar) privacy laws, leaving companies in a "patchwork" structure where requirements must be checked individually for every state in which they do business. This document summarizes the background to this structure, the common requirements shared across the major state laws currently in effect, and the implications for designing a multi-state compliance architecture.

## The Absence of a Federal Comprehensive Law

Several attempts have been made to enact a federal comprehensive privacy law, but all have failed to pass.

- **ADPPA (American Data Privacy and Protection Act, H.R.8152, introduced in the 117th Congress in 2022)**: passed the House Energy and Commerce Committee by a vote of 53–2 but was never brought to a floor vote, and died with the end of the 117th Congress.
- **APRA (American Privacy Rights Act, H.R.8818, introduced in the 118th Congress in 2024)**: a joint House-Senate draft was introduced, and a House Energy and Commerce subcommittee reviewed a discussion draft, but amid disagreement over whether it would preempt strong state laws like California's and over the scope of any private right of action, it never reached a formal committee vote or passage and remains pending.

As of August 2026, no new federal legislation has been enacted to replace these efforts, and state legislation and enforcement by state Attorneys General effectively remain the center of US privacy regulation.

:::note
The absence of a federal comprehensive law does not mean a regulatory vacuum. Sector-specific federal laws — healthcare ([HIPAA](../hipaa/)), finance (GLBA), children's online information (COPPA), and credit information (FCRA) — remain in effect and apply alongside state laws.
:::

## Status of State Privacy Laws in Effect (as of August 2026)

As of the first half of 2026, **roughly 20 states** have comprehensive consumer privacy laws in effect, with several additional states having enacted laws whose effective dates have not yet arrived. The states confirmed to be in effect are as follows.

| State | Law | Effective date |
| --- | --- | --- |
| California | CCPA (2018) / CPRA amendment (2023) | 1/1/2020 / 1/1/2023 |
| Virginia | VCDPA | 1/1/2023 |
| Colorado | CPA | 7/1/2023 |
| Connecticut | CTDPA | 7/1/2023 |
| Utah | UCPA | 12/31/2023 |
| Oregon, Montana, Texas (TDPSA), and others | Individual state laws | During 2024 |
| Delaware, Iowa, Maryland, Minnesota, Nebraska, New Hampshire, New Jersey, Tennessee, and others | Individual state laws | During 2024–2025 |
| Indiana, Kentucky, Rhode Island | Individual state laws | 1/1/2026 |

:::caution
The exact number and list of states in effect varies slightly across law-firm trackers and organizations such as the IAPP, depending on when the count was taken and how "comprehensive law" is defined. Because new state legislation continues to be enacted through 2026 (trackers report the cumulative number of states with enacted laws at roughly 20–22 as of the first half of 2026), the effective date should be reconfirmed with the relevant state Attorney General's office or a current tracker before entering a given state.
:::

## CCPA/CPRA — The De Facto Baseline

California was the first US state to enact a consumer privacy law (2018), and the 2023 CPRA amendment brought it requirements close to the GDPR (expanded rights, a new regulator), making it a reference model for other states' legislation. Its enforcement body, the **CPPA (California Privacy Protection Agency)**, is a dedicated privacy regulator — a rarity among US states.

The latest amended regulations, effective January 1, 2026, include the following.

- **Expanded scope of Sensitive Personal Information**: now includes neural data — though this addition stems not from the 2026 regulations but from a **statutory amendment effective January 1, 2025**
- **Regulation of Automated Decision-Making Technology (ADMT)**: transparency and opt-out requirements for automated decisions that have a significant effect, such as in employment, lending, or healthcare, though the actual compliance deadline is **January 1, 2027**
- **Cybersecurity audits and risk assessments**: risk-assessment obligations are being phased in starting in 2026, while mandatory cybersecurity audit certification is phased in between **2028 and 2030** depending on business size
- **Strengthened service-provider contract requirements**: contracts must specify prohibitions on use beyond the stated purpose, support for ADMT compliance, and subcontractor succession clauses

California has recently shown an aggressive privacy enforcement posture. In February 2026, the **California Attorney General (Rob Bonta)** announced a **$2.75 million settlement with Disney/ABC** (reported as the largest CCPA-related settlement to date). Separately, the CPPA announced roughly **$1.1 million in penalties against PlayOn Sports** in March of the same year — with the Attorney General and the CPPA each operating along their own separate enforcement tracks.

## Common Requirements

Specific provisions vary by state, but because many state laws are modeled on either the Virginia VCDPA or the California CPRA, the following requirements are broadly shared.

- **Consumer rights**: access, correction, deletion, portability, and opt-out — most require a response within 45 days (extendable by an additional 45 days)
- **Three categories of opt-out rights**: opt-out from targeted advertising, the sale of personal information, and profiling that produces legal or otherwise significant effects
- **Sensitive information handling**: race/ethnicity, religion, health diagnoses, sexual orientation, immigration status, biometric/genetic information, precise geolocation, and information about children under 13 are separately classified as "sensitive information." Many states — including VCDPA and CPA states — require **opt-in (prior consent)** for processing sensitive information, contrasting with the opt-out default that applies to general personal information
- **Prohibition of dark patterns**: interface designs that impede or distort consumer choice (dark patterns) are prohibited, with explicit provisions in laws such as Texas's TDPSA
- **Duty to recognize Universal Opt-Out Mechanisms (UOOM)**: as of January 2026, 12 states — California, Colorado, Connecticut, Delaware, Maryland, Minnesota, Montana, Nebraska, New Hampshire, New Jersey, Oregon, and Texas — require automatic recognition and processing of browser-level opt-out signals, most notably the **Global Privacy Control (GPC)**. States whose laws are modeled on Virginia's, such as Virginia, Utah, Iowa, Indiana, Kentucky, and Tennessee, do not have this requirement
- **Cure period**: many states grant an initial cure period (e.g., 30 days) for early violations, but Colorado's cure period sunset on January 1, 2025, making immediate enforcement possible

## A Healthcare-Specific Case — Washington State's My Health My Data Act (MHMDA)

Washington's MHMDA (enacted 2023, with most provisions effective March 31, 2024) is a separate law regulating **health-related consumer data not covered by HIPAA**, and it differs in character from a general privacy law.

- Requires publishing a separate "Consumer Health Data Privacy Policy," as a standalone document free of marketing language
- Requires affirmative consent when collecting new categories of data or changing the purpose of use
- Prohibits geofencing-based location tracking within a 2,000-foot radius of healthcare facilities
- Recognizes a **private right of action** — violations are treated as violations of the Washington State Consumer Protection Act (CPA), so in addition to enforcement by the state Attorney General, consumers may sue directly, with remedies and damages governed by CPA standards (including a cap of up to $7,500 per violation)

Because MHMDA defines "health data" more broadly than HIPAA, it is risky to assume that HIPAA compliance alone is sufficient for healthcare and wellness apps.

## Structural Differences from GDPR

| Category | GDPR | Typical US state privacy law |
| --- | --- | --- |
| Scope | Extraterritorial application to processing targeting EU residents, under a single law | Based on state-specific revenue/data-volume thresholds, with the law itself varying by state |
| Consent model | In principle requires a lawful basis for processing, with opt-in required in many situations | In principle **opt-out** — businesses may process after providing notice (with sensitive information as an exceptional opt-in case) |
| Regulator | Each member state's DPA plus the EDPB | Mostly enforced by state Attorneys General; only California has a dedicated agency (the CPPA) |
| Private right of action | Broadly recognized | Most states leave enforcement exclusively to the Attorney General; only a few, such as California (limited to data breaches) and Washington's MHMDA, recognize a private right of action |
| Penalty scale | Up to €20 million or 4% of global annual revenue | Varies by state (e.g., TDPSA violations are capped at $7,500 per violation, but the Texas Attorney General has separately used other consumer-protection statutes to secure major settlements, including $1.4 billion from Meta and $1.375 billion from Google) |

The core difference is that **the US still operates fundamentally on an "opt-out plus notice" model**. Unlike GDPR, it does not require a lawful basis for the processing itself; the default structure simply requires businesses to disclose their processing purposes in a privacy policy and guarantee consumers the right to opt out. That said, high-risk categories such as sensitive information, children's data, and health information are increasingly converging toward an opt-in approach similar to GDPR's, as an exception to this default.

## Multi-State Compliance Architecture

For organizations operating in multiple states simultaneously, it is more practical to converge on a common architecture than to handle each state individually.

- **Data mapping**: build an enterprise-wide inventory of what personal information is collected and stored, from residents of which states, for what purpose, and through which vendors/services. Tag sensitive-information categories separately
- **Consent Management Platform (CMP)**: branch opt-in/opt-out handling by geographic location (state) to account for differing state requirements. Logic to automatically detect UOOM signals such as GPC and map them to opt-outs from sale and targeted advertising is essential
- **Adopting the highest common denominator**: rather than running a different UX per state, many companies apply California CPRA-level requirements (among the strictest) uniformly to all US users to reduce operational complexity
- **Separate handling paths for sensitive information and health data**: design consent and deletion workflows for MHMDA-type health data, biometric information, and precise geolocation that are separate from those for general personal information
- **Vendor and DPA management**: verify that contracts (DPAs) with cloud/SaaS vendors include service-provider obligations — prohibition of use beyond the stated purpose, subcontractor succession, and support for consumer requests. See [Data Protection and Workload Security](../../security/data-protection/) for related architecture
- **Automating breach-notification response**: it is advisable to pre-map the differing breach-notification deadlines and thresholds across states so that, in the event of an incident, the applicable state requirements can be determined automatically. See [Security Incident Response](../../security/incident-response/) for related content

## Practical Implications

- **Don't design around the assumption of eventual federal legislation**: both ADPPA and APRA have repeatedly failed, and as of August 2026 there is still no finalized bill, only renewed discussion. Architecture should be designed on the premise that the state-level patchwork will persist for the foreseeable future.
- **Treat the California baseline as a de facto floor**: given the CPPA's aggressive enforcement posture and CPRA's broad requirements (ADMT, risk assessments, neural data, and more), designing to meet California's requirements often satisfies most other states' requirements as well.
- **Handling UOOM/GPC signals is a legal requirement in many states, not an option**: since 12 or more states require it, a banner-based consent UI alone is insufficient — a technical implementation that automatically recognizes browser signals is necessary.
- **HIPAA compliance alone is not enough for health and biometric data**: MHMDA-type state laws were enacted specifically to target gaps HIPAA does not cover, so health and wellness services require separate review.
- **Build in a process for reconfirming currency**: because new state privacy laws continue to be enacted every year, governance should include a step, at each point of business expansion, to reconfirm through official sources whether the target state's law is in effect.

## References

- [California Privacy Protection Agency (CPPA)](https://cppa.ca.gov/)
- [California Attorney General — CCPA](https://oag.ca.gov/privacy/ccpa)
- [Colorado Attorney General — Colorado Privacy Act](https://coag.gov/resources/colorado-privacy-act/)
- [Virginia Attorney General — VCDPA Summary](https://www.oag.state.va.us/consumer-protection/files/tips-and-info/Virginia-Consumer-Data-Protection-Act-Summary-2-2-23.pdf)
- [Washington State Attorney General — My Health My Data Act](https://www.atg.wa.gov/protecting-washingtonians-personal-health-data-and-privacy)
- [Texas Attorney General — Data Privacy and Security Initiative](https://www.texasattorneygeneral.gov/)
- [IAPP — US State Privacy Legislation Tracker](https://iapp.org/resources/article/us-state-privacy-legislation-tracker/)
- [US Congress — ADPPA (H.R.8152) Committee Report](https://www.congress.gov/committee-report/117th-congress/house-report/669/1)
- [US Congress — APRA (H.R.8818) Bill Status](https://www.congress.gov/bill/118th-congress/house-bill/8818/all-info)
- [California Privacy Protection Agency — Announcement of Finalized 2026 Regulations](https://cppa.ca.gov/announcements/2025/20250923.html)
- [California Attorney General — Disney/ABC Settlement Announcement (February 2026)](https://oag.ca.gov/news/press-releases/california-wont-let-it-go-attorney-general-bonta-announces-275-million)
- [CPPA — PlayOn Sports Penalty Announcement (March 2026)](https://privacy.ca.gov/2026/03/youth-sports-media-company-to-pay-1-1-million-fine-change-practices-over-privacy-violations/)
