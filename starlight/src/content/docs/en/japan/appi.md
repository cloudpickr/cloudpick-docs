---
title: "APPI (Japan's Act on the Protection of Personal Information)"
description: "Covers the cross-border transfer requirements under Japan's Act on the Protection of Personal Information (APPI), whether Korea and Japan mutually recognize each other's adequacy, the impact on cloud region selection, handling of My Number, and the 2025–2026 revision trends."
---

> Last reviewed: August 2026

## Overview

The Act on the Protection of Personal Information (APPI, 個人情報保護法) is the foundational law that applies broadly to businesses handling personal information in Japan, and it is overseen by the Personal Information Protection Commission (PPC, 個人情報保護委員会). Like Korea's Personal Information Protection Act, it sets out obligations covering the full lifecycle of personal data — collection, use, provision, and retention — and the provision most directly relevant to cloud architecture is the **cross-border transfer regulation (provision to a third party located in a foreign country)** under Article 28.

Japan has no separate law mandating data localization, but in practice the cross-border transfer procedures required under APPI and the obligation to "understand the external environment" (外的環境の把握) have a substantial effect on cloud region selection.

## Cross-Border Transfer Requirements

Article 28 of APPI requires one of the following three routes when providing personal data to a third party located in a foreign country.

### 1. Individual Consent

Under this route, the data subject's consent is obtained after providing advance information about the personal information protection system of the recipient's country and the protective measures the recipient will take. This is the most principle-based route, but it imposes a heavy operational burden on cloud services that handle large volumes of user data.

### 2. Establishing a Compliant Framework

To transfer data without consent, the transferring party must ensure — through contracts, intra-group rules, or similar means — that the recipient continuously implements personal information protection measures at a level equivalent to APPI. In practice, this is achieved through contracts equivalent to Standard Contractual Clauses (SCC), group-wide personal information protection policies (a BCR-like framework), or obtaining APEC Cross-Border Privacy Rules (CBPR) certification.

### 3. Countries Designated by Rule

Transfers to a country or region designated by PPC rule as having "a personal information protection framework equivalent to that of Japan" are permitted without the above procedures. As of August 2026, the **EU and the United Kingdom** are the only jurisdictions to have received this designation, and the designation requirements include regulation comparable to that applying to personal information handlers, the existence of an independent supervisory authority, and the possibility of mutual cooperation.

:::caution
Korea is not included on this list of "countries designated by rule." In other words, when transferring personal data from Japan to Korea, the country-level special exemption cannot be applied, and either the ① individual consent route or the ② compliant-framework route above must be established individually.
:::

## Whether Korea and Japan Mutually Recognize Each Other's Adequacy

As of August 2026, **no mutual adequacy (equivalence) recognition based on the domestic laws of both countries has been established** between Korea and Japan.

- **Japan → Korea direction**: as explained above, Korea is not on the list of countries designated under Article 28 of APPI, so either individual consent or a compliant framework must be established individually.
- **Korea → Japan direction**: Article 28-8 of Korea's Personal Information Protection Act provides a procedure allowing overseas transfer where the Personal Information Protection Commission recognizes that the level of protection in the recipient country is substantially equivalent to that of Korea, but as of August 2026 there is no confirmed case of Japan having been designated as such an "equivalence-recognized" country. Korea's Personal Information Protection Commission has, in its 2025–2026 policy plans, stated that it is at the stage of reviewing the United States, the United Kingdom, and Japan as candidates for expanded mutual data-transfer cooperation (verification needed — since designation status is fluid, checking the latest official notices is recommended).
- For reference, Korea and the EU have an adequacy decision dating from 2021, renewed in September 2025, and Japan also received an adequacy decision from the EU in 2019. However, these are each separate bilateral relationships with the EU and are distinct from any direct mutual recognition between Korea and Japan.

As long as this situation persists, Korean companies moving Japanese user data to a Korea region, or conversely sending data from a Japanese cloud to Korea, need to design individual mechanisms — such as an SCC-style contract or a consent procedure — at the contract and terms-of-service level.

## Impact on Cloud Region Selection and Data Residency

APPI does not mandate that data be kept in a specific region, but the following two factors have a substantial practical effect on region selection.

- **Obligation to understand the external environment**: when personal data is stored on a cloud server operated by a foreign business, the operator must understand the personal information protection system of the country where that server is located and reflect the resulting safety-control measures in its disclosure items on the handling of personal information (retained personal information disclosure, related to Article 32). There is an exception under which this is not treated as "provision to a foreign third party" if the cloud provider does not handle the personal data under contract and appropriate access controls are in place, but even in that case the obligation to understand the external environment itself remains.
- **Practical trend**: to reduce the burden described above, many businesses preferentially choose a Japan region (Tokyo, Osaka, etc.), or at minimum document the legal system of the region where data is stored and disclose it to users. When Korean companies provide cloud services to the Japanese market, deciding on the use of a Japan region at the initial architecture design stage is a way to reduce compliance burden further down the line.

## Handling of My Number and Other Sensitive Information

Japan's My Number (マイナンバー, personal number) system is governed by a separate law from APPI — the "Act on the Use of Numbers to Identify a Specific Individual in Administrative Procedures" (the Number Act) — and stricter handling restrictions than those under APPI apply to "specific personal information."

- If a cloud service is designed to store or process My Number, it is, in principle, treated as an "entrustment" (委託), under which the entrusting party (the customer company) retains responsibility while the entrusted party (the cloud provider) also incurs an obligation to implement safety-control measures.
- Conversely, an exceptional configuration in which the arrangement is not treated as an entrustment is possible if the cloud provider contractually agrees not to handle My Number and technically ensures this through access controls.
- In practice, ISMAP-registered services are often used as a reference benchmark for a security level suitable for handling My Number and other sensitive information. ISMAP itself is not a legal certification for handling My Number, so ultimate suitability must be judged through individual contracts and the design of safety-control measures.

:::note
My Number (personal number) requirements are similar in character to Korea's resident registration number (unique identifying information) regulations, but the underlying laws and supervisory authorities differ. When entering the Japanese market, it should be kept in mind that APPI compliance alone may not satisfy My Number-related requirements.
:::

## 2025–2026 Revision Trends (Triennial Review)

APPI includes a provision requiring that its implementation status be reviewed roughly once every three years and that necessary measures be taken (the so-called triennial review clause). The progress of the current review is as follows.

| Date | Development |
| --- | --- |
| November 2023 | PPC begins review discussions |
| June 2024 | Interim summary published |
| December 2024 | Review committee report published |
| March 2025 | Institutional issues organized |
| January 9, 2026 | PPC publishes "Policy for Amending the Act on the Protection of Personal Information for the So-Called Triennial Review" (4 pillars, 12 items) |
| April 7, 2026 | Amendment bill approved by the Cabinet and submitted to the Diet |
| July 17, 2026 | Amended law promulgated |

The 2026 amendment is built around four pillars — promoting appropriate data use, regulation proportionate to risk, prevention of improper use, and other institutional refinements — covering matters such as the use of data for AI training, information asymmetry between platform operators and users, and strengthened penalties for improper use. As of the time this document was written, the effective date and the subordinate guidelines and enforcement rules are being announced progressively, so the detailed impact on cloud architecture should be confirmed through PPC's follow-up guideline announcements (verification needed).

## References

- [Personal Information Protection Commission (PPC) Official Site](https://www.ppc.go.jp/)
- [Guidelines on the Act on the Protection of Personal Information (Provision to a Third Party Located in a Foreign Country)](https://www.ppc.go.jp/personalinfo/legal/guidelines_offshore/)
- [PPC: Cross-Border Transfer of Data Between Japan and the EU/UK (Mutual Recognition)](https://www.ppc.go.jp/enforcement/cooperation/cooperation/sougoninshou/)
- [PPC: Report on the Review of the EU and UK Designation (March 2023)](https://www.ppc.go.jp/files/pdf/20230322_review_report.pdf)
- [PPC: FAQ — Understanding the External Environment](https://www.ppc.go.jp/all_faq_index/faq1-q10-25/)
- [Personal Information Protection Commission (Korea) — Country Information](https://www.pipc.go.kr/np/default/page.do?mCode=D060010000)
- [Regulation on the Operation of Overseas Transfer of Personal Information (Korea, National Law Information Center)](https://www.law.go.kr/LSW/admRulLsInfoP.do?admRulSeq=2100000230332)
