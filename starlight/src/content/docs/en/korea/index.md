---
title: "Korea Appendix"
description: "Guides specific to the Korean market — CSAP, network separation, sovereign AI policy, and domestic FM providers"
---

> Last reviewed: August 2026

## Overview

This section covers the regulations and ecosystem you encounter when adopting and operating cloud in the Korean market. Where the earlier vendor-neutral documents covered common global architecture, this appendix focuses on the laws, institutions, and supplier landscape unique to Korea.

It is organized to help enterprise architects who are adopting cloud in the public or financial sector, or bringing generative AI into line with Korea's domestic regulatory environment.

## Status of Korea Regions

| Vendor | Region code | AZs / Zones | Launched |
| --- | --- | --- | --- |
| AWS | `ap-northeast-2` (Seoul) | 4 AZs | 2016 |
| Azure | `koreacentral` (Seoul), `koreasouth` (Busan) | 3 AZs (Central) | 2017 |
| Google Cloud | `asia-northeast3` (Seoul) | 3 Zones | 2020 |
| OCI | `ap-seoul-1`, `ap-chuncheon-1` | 3 FDs | 2020 |

:::note
Azure (Seoul–Busan) and OCI (Seoul–Chuncheon) each have two regions in Korea, so you can design DR without data leaving the country. For AWS and Google Cloud, Tokyo and Osaka are the nearest DR candidates. For the region concepts themselves, see [Regions and Availability Zones](../../about-cloud/regions-and-zones/).
:::

### DR Configuration Based on Korean Regions

| Vendor | Primary | Secondary candidate | Latency | Notes |
| --- | --- | --- | --- | --- |
| AWS | `ap-northeast-2` (Seoul) | `ap-northeast-1` (Tokyo), `ap-northeast-3` (Osaka) | ~30-50ms | Cross-border transfer |
| Azure | `koreacentral` (Seoul) | `koreasouth` (Busan) | ~5ms | **In-country DR possible** |
| Azure | `koreacentral` (Seoul) | `japaneast` (Tokyo) | ~30ms | Cross-border transfer |
| Google Cloud | `asia-northeast3` (Seoul) | `asia-northeast1` (Tokyo), `asia-northeast2` (Osaka) | ~30-50ms | Cross-border transfer |
| OCI | `ap-seoul-1` (Seoul) | `ap-chuncheon-1` (Chuncheon) | ~5ms | **In-country DR possible** |
| OCI | `ap-seoul-1` (Seoul) | `ap-tokyo-1` (Tokyo) | ~30ms | Cross-border transfer |

:::caution
If you use an overseas region for DR, you must meet the cross-border data transfer requirements under Korea's Personal Information Protection Act and Credit Information Act. For DR strategy types, see [Disaster Recovery (DR)](../../governance/dr/).
:::

### Dedicated connectivity and community in Korea

Korean PoPs for dedicated connections (Direct Connect / ExpressRoute / Interconnect / FastConnect) are typically KINX and LG U+. For multicloud Cloud Exchange, consider [KINX Cloud Hub](https://www.kinx.net/service/cloud/), Megaport (Seoul PoP), and Equinix Fabric (Seoul DC). For the concepts, see [Multicloud Networking](../../networking/multicloud-networking/).

Local user communities: [AWSKRUG](https://www.awskr.org/), [GDG Cloud Korea](https://gdg.community.dev/gdg-cloud-korea/).

In large public-sector and financial projects, local SIs such as Samsung SDS, LG CNS, and SK C&C commonly build the overall system, while the product company's FDE handles that company's AI/SaaS integration.

## Topics Covered

### Security and Regulation

- **[Compliance (Korea)](../korea/governance/compliance/)** — a consolidated overview of Korea's certification and regulatory landscape, including ISMS-P, CSAP, and financial-sector regulations, with pointers to each detailed document.
- **[CSAP (Cloud Security Assurance Program)](../korea/security/csap/)** — the mandatory gateway for public-sector cloud adoption in Korea, covering the tier system, hyperscaler and domestic CSP certification status, and the National Intelligence Service's unified verification system planned for 2027.
- **[Network Separation and Isolation](../korea/security/network-isolation/)** — network separation regulation in the financial and public sectors, the financial-sector network separation improvement roadmap underway since 2024, and how the shift to the National Network Security Framework (N²SF) affects cloud, SaaS, and generative AI adoption.

### AI and Sovereign Policy

- **[Sovereign FM Policy](../korea/ai/sovereign-fm-policy/)** — the Ministry of Science and ICT's (MSIT) independent AI foundation model project, the progress of its elite-team selection process, and the implications for enterprise architects.
- **[FM Provider Comparison](../korea/ai/fm-providers/)** — a comparison of the latest models, licenses, and delivery channels from domestic foundation model providers such as Naver, LG AI Research, Kakao, KT, Upstage, and NC AI.

:::note
This section covers policy and regulatory developments that change quickly. We recommend checking the sources in the "References" section at the bottom of each document to confirm the latest official announcements.
:::

## Related Documents

- [Data Protection and Workload Security](../security/data-protection/)
- [Sovereign Landing Zone](../governance/landing-zone/#sovereign-landing-zone)

