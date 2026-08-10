---
title: "Korea Market & Infrastructure"
description: "Covers Korea region status, in-country DR configurations, data sovereignty, dedicated-connectivity PoPs, and MSP/community resources for the Korean cloud market."
---

> Last reviewed: August 2026

## Overview

All four major global CSPs operate a region in Seoul, and some vendors support a DR configuration where data never leaves the country thanks to two domestic regions. This document covers Korea-specific infrastructure and ecosystem information not addressed in the vendor-neutral documents — region status, in-country DR combinations, dedicated-connectivity PoPs, and MSP/community resources.

## Status of Korea Regions

| Vendor | Region code | Number of AZs/Zones | Launch date |
| --- | --- | --- | --- |
| AWS | `ap-northeast-2` (Seoul) | 4 AZs | 2016 |
| Azure | `koreacentral` (Seoul), `koreasouth` (Busan) | 3 AZs (Central) | 2017 |
| Google Cloud | `asia-northeast3` (Seoul) | 3 Zones | 2020 |
| OCI | `ap-seoul-1` (Seoul), `ap-chuncheon-1` (Chuncheon) | 3 FDs | 2020 |

:::note
Azure (Seoul-Busan) and OCI (Seoul-Chuncheon) each have two domestic regions, enabling a DR configuration where data never leaves the country. For AWS/Google Cloud, Tokyo and Osaka are the closest DR candidates. For the concepts of regions and AZs, see [Regions and Availability Zones](../../about-cloud/regions-and-zones/).
:::

## DR Configuration Based on Korean Regions

| Vendor | Primary (Korea) | Secondary candidate | Latency | Notes |
| --- | --- | --- | --- | --- |
| AWS | `ap-northeast-2` (Seoul) | `ap-northeast-1` (Tokyo), `ap-northeast-3` (Osaka) | ~30-50ms | Cross-border transfer |
| Azure | `koreacentral` (Seoul) | `koreasouth` (Busan) | ~5ms | **In-country DR possible** |
| Azure | `koreacentral` (Seoul) | `japaneast` (Tokyo) | ~30ms | Cross-border transfer |
| Google Cloud | `asia-northeast3` (Seoul) | `asia-northeast1` (Tokyo), `asia-northeast2` (Osaka) | ~30-50ms | Cross-border transfer |
| OCI | `ap-seoul-1` (Seoul) | `ap-chuncheon-1` (Chuncheon) | ~5ms | **In-country DR possible** |
| OCI | `ap-seoul-1` (Seoul) | `ap-tokyo-1` (Tokyo) | ~30ms | Cross-border transfer |

:::caution
If you use an overseas region for DR, you must meet the cross-border data transfer requirements under Korea's Personal Information Protection Act and Credit Information Act. For workloads with strict data sovereignty requirements, prioritize reviewing vendors that offer in-country DR from the table above. For DR strategy types and RPO/RTO design, see [Disaster Recovery (DR)](../../governance/dr/).
:::

## Data Sovereignty

Korea's **Personal Information Protection Act** requires either the data subject's consent or a legal basis when transferring personal information overseas. The **Credit Information Act** applies even stricter regulations to personal credit information in the financial sector. When choosing a cloud vendor, you must verify whether a Korea region exists and where data is stored.

For how region restrictions can be enforced as policy (SCP, Azure Policy, etc.), see [Regions and Availability Zones — Data Sovereignty and Region Restrictions](../../about-cloud/regions-and-zones/).

## Dedicated-Connectivity PoPs and Cloud Exchange

Below is the PoP status available when setting up a dedicated connection (Direct Connect, ExpressRoute, Cloud Interconnect, FastConnect) within Korea.

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Korea PoP** | KINX, LG U+ | KINX, LG U+ | KINX | KINX |

**Domestic Cloud Exchange options:**

- **KINX**: the largest domestic IX (Internet Exchange). Has a PoP for AWS, Azure, Google Cloud, and OCI
- **Megaport**: a global Cloud Exchange. Has a Seoul PoP
- **Equinix Fabric**: the largest globally. Operates a Seoul data center

For the trade-offs between connection methods, see [Multicloud Networking](../../networking/multicloud-networking/).

## MSP and Community

Through a domestic MSP, you can get support for the following, beyond general managed operations:

- Local invoicing and Korean won (KRW) payment
- Support for regulatory compliance (CSAP, ISMS-P, etc.) — see [Compliance (Korea)](../governance/compliance/) for details

| Vendor | Community | Notes |
| --- | --- | --- |
| AWS | [AWSKRUG](https://www.awskr.org/) | Korean AWS user community |
| Google Cloud | [GDG Cloud Korea](https://gdg.community.dev/gdg-cloud-korea/) | Korean Google Cloud user community |

For general MSP cost structure and support plans, see [Support and Technical Assistance Plans](../../about-cloud/support-plans/).

## Related Documents

- [Regions and Availability Zones](../../about-cloud/regions-and-zones/)
- [Disaster Recovery (DR)](../../governance/dr/)
- [Multicloud Networking](../../networking/multicloud-networking/)
- [Support and Technical Assistance Plans](../../about-cloud/support-plans/)

## References

- [KINX](https://www.kinx.net/) — the largest domestic IX
- [AWS Seoul Region](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/)
- [Azure Korea Regions (Korea Central/South)](https://azure.microsoft.com/explore/global-infrastructure/geographies)
- [Google Cloud Seoul Region](https://cloud.google.com/about/locations)
- [OCI Regions](https://www.oracle.com/cloud/public-cloud-regions/)
