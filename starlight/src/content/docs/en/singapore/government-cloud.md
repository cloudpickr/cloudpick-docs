---
title: "Government Cloud (GCC, IM8, SGTS)"
description: "Covers Singapore's government cloud framework — the structure of the Government Commercial Cloud (GCC) and GCC+, the IM8 security policy reform, SG Tech Stack, and requirements for participating in government procurement."
---

> Last reviewed: August 2026

## Overview

Rather than building its own data centers, the Singapore government runs its government cloud by layering a standardized security and governance layer on top of commercial hyperscalers. At the center of this framework is the **GCC (Government Commercial Cloud, formally Government on Commercial Cloud)**, led by the Government Technology Agency of Singapore (GovTech).

GCC is one pillar of a broader strategic project called **CODEX (Core Operations, Development Environment, and eXchange)**. CODEX is designated as a core national project under the Smart Nation strategy, and alongside GCC (the infrastructure layer) it also encompasses SG Tech Stack (SGTS, the development layer) and the Government Data Architecture (the data layer).

:::note
GCC is an **internal platform used directly by government agencies**, similar in spirit to Korea's National Information Resources Service (NIRS) or its cloud-based consolidation of public-sector IT resources. It is not a structure where private vendors "list" themselves on GCC — rather, government agencies operate systems on top of AWS, Azure, and GCP wrapped in the security and governance layer that GovTech provides. Private companies seeking to participate in business targeting the Singapore government must go through separate tracks, such as registering on the GeBIZ procurement portal and obtaining MTCS certification.
:::

## The Structure of GCC (Government Commercial Cloud)

GCC is introduced as a "wrapper platform." Rather than government agencies building and maintaining cloud infrastructure themselves, they use commercial cloud services on top of the standardized framework GCC provides. The official framework consists of the following components.

- **Onboarding** — automated account and permission provisioning based on TechPass (GovTech's IAM solution)
- **Billing** — consolidated management of cloud usage costs across agencies
- **Application layer** — covers AWS, Microsoft Azure, and Google Cloud (GCP); other vendors such as Oracle Cloud are not included in the GCC framework
- **Monitoring, logging, and jump hosts** — centralized observability and audit trails
- **On-premises integration** — hybrid connectivity with agencies' internal systems
- **Governance, policy, and data residency** — policy controls such as requirements to keep data resident within Singapore

### From GCC 1.0 to GCC 2.0

Early GCC (1.0) operated on a vendor-outsourcing support model, but it was redesigned due to issues such as onboarding delays and an excessive volume of service requests. GCC 2.0 reached general availability in stages, hyperscaler by hyperscaler.

| Cloud | GCC 2.0 general availability (GA) |
| --- | --- |
| AWS | May 4, 2022 |
| Microsoft Azure | November 30, 2022 |
| Google Cloud (GCP) | July 7, 2023 |

Key characteristics of GCC 2.0 include:

- **Streamlined onboarding** — onboarding is possible with TechPass alone, with automated workflows provisioning accounts without a service request
- **SEED (Secure Engineering Environment Device Platform)** — a shift from traditional perimeter-based security to a **zero trust** model, automatically blocking access from non-compliant devices
- **Policy-as-Code** — policies are defined and applied as code, applying baseline compliance checks by default to all provisioned resources and checking for security vulnerabilities in real time
- A core cloud platform configured on an **Infrastructure as Code (IaC)** basis

### GCC+ — Extending to Confidential-Tier Workloads

Unlike the general (Confidential Cloud-Eligible or lower) tier of systems that GCC 2.0 handles, systems classified as **Confidential** and highly sensitive are onboarded separately through **GCC+**. GCC+ applies stricter controls — such as enhanced encryption, separated key management, and residency within Singapore-domestic regions — providing a cloud migration path for sensitive workloads (such as law-enforcement and health-data-processing systems) that were previously difficult to move to the cloud.

### Adoption Status

According to figures GovTech published as of March 7, 2025, **3,006 systems** have been onboarded to GCC, achieving **99.5% service availability**. GovTech's FY2024–2025 annual report states that **99% of government digital-service transactions are completed online** — a figure describing the overall online-completion rate for government transactions, not the share of transactions directly supported by GCC/GCC+, and the two should not be conflated. Representative services running on GCC include MyCareersFuture (a job-search portal), GoBusiness (a business licensing and permit portal), WOGAA (which monitors the performance of government digital services), the Inland Revenue Authority of Singapore's (IRAS) integrated tax system IRIN, and the Ministry of Education's home-based learning platform, Student Learning Space.

## IM8 and the 2024–2026 Policy Reform

**IM8** is short for the "Instruction Manual on ICT&SS (Infocomm Technology & Smart Systems) Management," referring to the full body of ICT security policies and standards for government agencies overseen by GovTech. It covers data-security classification, cloud security, application/network/endpoint security, and security operations, functioning as the internal rulebook agencies must follow when adopting and operating systems.

Under the existing IM8 framework, government systems were, in principle, required to be hosted on GCC, and SaaS applications could not be hosted outside of GCC. Recognizing that this rigidity was slowing SaaS adoption, GovTech is pursuing an **ICT&SS Policy Reform (commonly called the IM8 Reform)**.

The reform's stated goal is officially described as "simplifying ICT&SS policy so that agencies can build systems quickly, cost-effectively, and innovatively with right-fit risk controls." Key changes include:

- **A Risk-Based Approach** — classifying systems into types such as low-risk cloud, medium-risk cloud, high-risk cloud, low-risk on-premises, generative AI, digital services, and sandbox, and applying a different level of control to each
- **Revamped System Security Plan (SSP) templates** — shifting to a model where a predefined base set of controls per risk type is customized by the agency
- **Reorganized Control Catalog** — realigning control items to match the same risk classification structure
- **Allowing low-risk SaaS to be hosted outside GCC** — policy is being revised to permit adoption of SaaS applications hosted outside GCC for low-risk use cases
- **Expanded discretion** for digital system owners to tailor their security plans to their own operational and technical context

:::caution
As of August 2026, the IM8 reform remains an **ongoing policy transition**. Details such as the scope of permission for hosting low-risk SaaS outside GCC and the final confirmation date for the reorganized Control Catalog continue to be updated on GovTech's official policy portal (info.standards.tech.gov.sg), so the latest notices should be checked directly for actual procurement and compliance work.
:::

## SGTS (Singapore Government Tech Stack)

SGTS is the **development-layer** counterpart to GCC (the infrastructure layer) — a collection of reusable platforms, APIs, and common services provided by GovTech. It enables agencies to build digital services quickly by reusing common functions such as identity verification, payments, and data exchange, rather than building infrastructure from scratch. GovTech describes its strategy for scaling SGTS around three pillars: **People, Platform, and Practice**.

More than 40 government agencies use SGTS, and more than 200 cloud-based systems have been built on it. A representative example is **MyInfo**, the national digital identity verification service, which used SGTS to cut its development timeline from a typical one year down to four months. SGTS also includes **SHIP-HATS** (Secure Hybrid Integration Pipeline – Hive Agile Testing Solutions), a multi-tenant SaaS-style CI/CD toolset for government developers.

## Government Procurement Requirements and the Relationship with MTCS

While GCC, IM8, and SGTS are internal frameworks for government agencies, separate entry requirements apply to private vendors supplying the commercial cloud and SaaS that underpin them.

- Government agencies must conduct cloud/ICT procurement through **GeBIZ** (Government Electronic Business System, the government's integrated e-procurement portal). This is a mandatory channel grounded in the Government Procurement Act and various Instruction Manuals.
- In government cloud procurement, a vendor's cloud service is often required to hold **MTCS Level 3 certification**, but the precise certification and eligibility requirements vary by individual tender notice, the classification of data handled, and the type of service, so they should be confirmed on a project-by-project basis. The MTCS certification framework and tier structure are covered in detail in [MTCS (Multi-Tier Cloud Security Standard)](../mtcs/).
- At the common-platform level, GCC provides security and governance guardrails aligned with PDPA, IM8, and MTCS Level 3, but official materials do not guarantee that individual workloads automatically inherit this certification in full without any separate process. Under a shared-responsibility model, additional configuration and review may be required on a per-service basis. Conversely, private vendors seeking to supply SaaS or platforms to government agencies must independently obtain requirements such as MTCS certification to be eligible for procurement.

## Practical Implications

- **GCC is a "government-only private platform," not a separate certification program.** For companies considering business targeting the Singapore government (SI, SaaS supply, etc.), the goal is not to be certified on GCC itself — registering on GeBIZ and obtaining MTCS Level 3 certification is the actual entry procedure.
- **The IM8 reform is worth watching closely.** Policy is loosening in the direction of allowing low-risk SaaS to be hosted outside GCC, which may reduce dependence on GCC-internal infrastructure for future SaaS sales targeting government agencies. However, since the reform is not yet complete, the requirements of each individual procurement notice should be checked as they are issued.
- **Understand the hierarchy among CODEX, GCC, and SGTS.** Because GCC (infrastructure), SGTS (development platform), and the Government Data Architecture (data) each address a different layer, proposals aimed at government agencies should make clear which layer the proposed solution addresses.
- **Compliance runs on a separate track from the private market.** Private-sector cloud regulation (PDPA, MTCS) and internal government policy (IM8, GCC) have different operating bodies and different scopes of application, so the two tracks should not be conflated — a single certification does not satisfy both.

## References

- [Government on Commercial Cloud (GCC) — GovTech Singapore](https://www.tech.gov.sg/products-and-services/for-government-agencies/software-development/government-on-commercial-cloud/)
- [Singapore Government Tech Stack (SGTS) — GovTech Singapore](https://www.tech.gov.sg/products-and-services/for-government-agencies/software-development/sg-tech-stack/)
- [About GCC 2.0 — Singapore Government Developer Portal](https://www.developer.tech.gov.sg/products/categories/infrastructure-and-hosting/gcc/about-gcc-2-0)
- [GCC Overview (criteria for the GCC/GCC+ distinction) — Singapore Government Developer Portal](https://www.developer.tech.gov.sg/products/categories/infrastructure-and-hosting/gcc/overview)
- [Government on Commercial Cloud (GCC 2.0) Fact Sheet — GovTech Singapore](https://www.developer.tech.gov.sg/assets/files/gcc-factsheet-121222.pdf)
- [Singapore Government ICT&SS Policy Reform Portal — GovTech Singapore](https://info.standards.tech.gov.sg/)
- [GeBIZ — Singapore Government e-Procurement Portal](https://www.gebiz.gov.sg/)
- [Tech Stacks Driving Singapore's Smart Nation Journey — GovTech (source of the 99% online-transaction-completion figure)](https://www.tech.gov.sg/technews/tech-stacks-driving-singapore-smart-nation/)
- For MTCS requirements in financial and public-sector procurement, see [MTCS (Multi-Tier Cloud Security Standard)](../mtcs/); for personal-data-related regulation, see [PDPA (Personal Data Protection Act)](../pdpa/).
