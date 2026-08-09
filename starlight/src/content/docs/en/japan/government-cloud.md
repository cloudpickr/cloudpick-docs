---
title: "Japan Government Cloud (ガバメントクラウド)"
description: "Covers the registration status of providers on Japan's Digital Agency-led shared government/local-government cloud platform, its relationship with ISMAP, and the progress of local government system standardization."
---

> Last reviewed: August 2026

## Overview

Government Cloud (ガバメントクラウド, Government Cloud) is the shared cloud infrastructure that Japan's Digital Agency (デジタル庁) develops for common use by national government agencies and local governments. It is grounded in the "Act on Standardization of Information Systems of Local Governments" (地方公共団体情報システムの標準化に関する法律), enacted in 2021, and serves as the core implementation mechanism for the **cloud-by-default principle (クラウド・バイ・デフォルト原則)** adopted under the "Basic Policy on the Appropriate Use of Cloud Services in Government Information Systems."

The goal is to migrate not only the information systems of individual national ministries, but also the core operational systems (resident records, tax, welfare, and other work spanning 20 categories) run by more than 1,700 local governments nationwide, onto this shared platform. In other words, Government Cloud is not a specific data center or a single service — it is the totality of the list of cloud service providers (CSPs) that the Digital Agency has reviewed and designated as "available for use," together with the common functions and guidelines for building and operating systems on top of them.

:::note
Government Cloud shares a similar purpose with Korea's "public-sector cloud migration" policy, but it differs in that provider selection is run through an annual open call and review process led by the Digital Agency rather than a single central procurement authority, and it is tightly coupled with a separate piece of legislation on local government system standardization.
:::

Government Cloud provider selection began in 2020–2021, targeting the four hyperscalers AWS, Google Cloud, Microsoft Azure, and OCI, and the scope of eligible services has expanded through an annual open call each year since. In November 2023, Sakura Internet became the first Japan-based domestic provider to be conditionally adopted, and it received full accreditation in March 2026, completing the current five-provider lineup.

## Registered Provider Status (as of August 2026)

The following five providers are designated as eligible Government Cloud services for fiscal year 2026.

| Provider | Registration status | Notes |
| --- | --- | --- |
| Amazon Web Services (AWS) | Fully registered | Participated as a registered provider since the early days of the program (2021–2022) |
| Microsoft Azure | Fully registered | Participated as a registered provider since the early days of the program |
| Google Cloud | Fully registered | Participated as a registered provider since the early days of the program |
| Oracle Cloud Infrastructure (OCI) | Fully registered | Participated as a registered provider since the early days of the program |
| Sakura Internet (さくらのクラウド) | **Fully registered** (March 27, 2026) | Conditionally adopted in November 2023 → fully accredited in March 2026 after satisfying roughly 305 technical requirements by the end of fiscal year 2025 |

:::note
Sakura Internet is the only Japan-domestic (home-grown) provider registered on Government Cloud. After being conditionally adopted in November 2023 on the condition that it would "satisfy the full set of technical requirements by the end of fiscal year 2025," it progressively cleared its remaining requirements — controls, security certification, object storage, and more — reaching full accreditation in March 2026.
:::

## Relationship with ISMAP — A Dual-Gate Structure

Government Cloud and [ISMAP](../ismap/) are separate programs, but they are directly connected.

- **ISMAP registration is a prerequisite, not a sufficient condition.** To be selected as a Government Cloud provider, a given service must first be registered on the ISMAP Cloud Service List, but ISMAP registration alone does not automatically make a provider a Government Cloud provider.
- Even after ISMAP registration, a service must pass a separate **technical requirements review** (covering hundreds of items on performance, availability, security, governance, and more) conducted by the Digital Agency, and as Sakura Internet's case shows, meeting these requirements after conditional adoption can take several years.
- As a result, public cloud procurement in Japan requires passing a dual gate — **① ISMAP registration → ② Government Cloud provider review** — and as local government system migration expands, the practical influence of this gate is growing as well.
- Conversely, even after being accredited as a Government Cloud provider, losing ISMAP registration itself (for example, by failing a renewal review) makes it difficult to retain Government Cloud eligibility as well, so the two programs should effectively be treated as a single, continuous compliance cycle.

## Provider Selection Method — Annual Open Call and Review

Government Cloud providers are not fixed once and for all — the Digital Agency repeats an open call and review process on an annual basis.

1. **Annual open call**: the Digital Agency issues a procurement notice for "cloud services for the development of Government Cloud" for the given fiscal year (e.g., FY2026).
2. **Technical requirements review**: applicant providers are reviewed against hundreds of technical requirements covering performance, availability, security, governance, and audit response. ISMAP registration is a prerequisite for this stage.
3. **Conditional adoption option**: as with Sakura Internet, a provider that has not yet met all requirements at the time of review may still be conditionally adopted, subject to meeting them by a specified deadline.
4. **Full accreditation and renewal**: once compliance with the conditions is confirmed, the provider receives full accreditation, and it must respond to re-review in subsequent annual calls to retain its eligibility.

This approach leaves room for new providers to enter each year, while also placing a recurring burden on existing registered providers to keep up with requirement changes at each cycle.

## Status of Local Government System Standardization (標準化)

The "Act on Standardization of Information Systems of Local Governments" requires that **20 categories of core operational systems** — resident records, tax, welfare, and more — be standardized nationwide to specifications set by the national government and migrated onto Government Cloud.

| Timing | Details |
| --- | --- |
| 2021 | The Standardization Act took effect, setting the principal migration deadline at the end of fiscal year 2025 (March 2026) |
| December 24, 2024 | The basic policy was revised — systems that are difficult to migrate are classified as "designated transition-support systems" (特定移行支援システム), with national support, including transition costs, extended through the end of fiscal year 2030 |
| As of the end of January 2026 | Overall migration completion rate: **38.4%** |
| As of the end of December 2025 | Of 34,592 target systems, **8,956 (25.9%)** are projected to be classified as designated transition-support systems — affecting 935 of 1,788 target local governments (52.3%) |
| As of the end of March 2026 (official confirmed figure) | Of 34,366 target systems, **10,013 (29.1%)** are confirmed as classified as designated transition-support systems — an upward revision from the December 2025 projection of 25.9% |

:::caution
Although the principal deadline (the end of fiscal year 2025, or the end of March 2026) has passed, a substantial number of systems have been pushed into fiscal year 2026 and beyond due to migration difficulty and shortages of development vendor resources. The national government has secured a budget of roughly ¥700 billion, including transition costs, and has extended the support deadline through the end of fiscal year 2030. The latest migration schedules for individual local governments and systems should be checked through announcements from the [Digital Agency](https://www.digital.go.jp/) and the Ministry of Internal Affairs and Communications.
:::

## Practical Implications

- **A dual review, not a single list**: ISMAP registration status alone cannot determine Government Cloud eligibility. Organizations targeting public procurement need to check the Digital Agency's Government Cloud provider list separately from the ISMAP list.
- **A domestic region/domestic provider option**: Sakura Internet has established itself as an alternative path for local governments and ministries sensitive to data residency or "domestic cloud" requirements. That said, the four hyperscalers still hold an edge in service breadth and feature maturity, so the right choice depends on the nature of the workload.
- **Design around continued migration delays**: with the standardization migration rate at only 38.4% as of January 2026 and the support deadline extended to fiscal year 2030, a multi-year transitional period in which legacy systems and Government Cloud-based systems coexist is expected to continue. Architecture and business planning should account for the integration and migration-support demand that will arise during this period.
- **Annual re-review risk**: because Government Cloud provider eligibility is renewed through an annual open call and review, it is safer not to assume that a given provider's registration is permanently fixed. When designing long-term contracts, it is worth including provisions that anticipate the possibility of a change in registration status.
- **A perspective for Korean and other global companies**: companies seeking to supply SaaS or platforms to Japan's public sector should first confirm whether their service runs on a hyperscaler region registered under Government Cloud (Tokyo, Osaka, etc.), and for local-government-facing business, it is prudent to build a long-term roadmap that accounts for the designated transition-support system timeline (extending to fiscal year 2030 at the latest).

## References

- [ISMAP Portal](https://www.ismap.go.jp/)
- [Basic Policy on Standardization of Local Government Information Systems (Digital Agency, September 2023)](https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/c58162cb-92e5-4a43-9ad5-095b7c45100c/f6ea9ca6/20230908_policies_local_governments_outline_03.pdf)
- [Materials on Local Government Information System Standardization and Government Cloud (Ministry of Internal Affairs and Communications, submitted to the Local Fiscal Affairs Council, February 13, 2026)](https://www.soumu.go.jp/main_content/001063741.pdf)
- [Materials on Unification and Standardization of Core Operational Systems (Digital Agency, submitted to the National/Local System Working Group, November 18, 2025)](https://www5.cao.go.jp/keizai-shimon/kaigi/special/reform/wg6/2025/shiryou3-2.pdf)
- [Sakura Internet Government Cloud Full Accreditation Press Release (March 27, 2026)](https://www.sakura.ad.jp/corporate/information/newsreleases/2026/03/27/1968224087/)
- [Sakura Internet Government Cloud Full Accreditation — Nikkei (March 2026)](https://www.nikkei.com/article/DGXZQOUF274430X20C26A3000000/)
- [Sakura Becomes First Domestic Company Fully Selected for Government Cloud in FY2026 — Jiji Press (March 27, 2026)](https://www.jiji.com/jc/article?k=2026032700944&g=pol)
- [Local Government System Standardization Migration Deadlines and Progress (Nikkei xTECH)](https://xtech.nikkei.com/atcl/nxt/column/18/00001/10106/)
- [What Is Government Cloud — NEC Column](https://jpn.nec.com/government/solution04/col_g.1/index.html)
- [Latest Migration Status of Local Government System Standardization (Digital Agency)](https://www.digital.go.jp/policies/local_governments)
