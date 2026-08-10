---
title: "Hybrid/Edge Computing"
description: "Compares hybrid cloud, edge computing, and multi-cloud architecture patterns across vendors."
---

> Last reviewed: May 2026

## Overview

Not every workload is suited to the public cloud. There is demand for **extending cloud infrastructure to on-premises/edge** environments for reasons such as data sovereignty, ultra-low latency, and protecting existing investments.

## Hybrid/edge solutions by vendor

| Vendor | On-premises extension | Edge | Multi-cloud management |
| --- | --- | --- | --- |
| AWS | [Outposts](https://aws.amazon.com/outposts/) (rack/server) | [Local Zones](https://aws.amazon.com/about-aws/global-infrastructure/localzones/), [Wavelength](https://aws.amazon.com/wavelength/) | EKS Anywhere, ECS Anywhere |
| Azure | [Azure Stack HCI](https://learn.microsoft.com/azure/azure-local/), [Azure Local](https://learn.microsoft.com/azure/azure-local/) | Azure Edge Zones | [Azure Arc](https://azure.microsoft.com/products/azure-arc/) |
| Google Cloud | [Google Distributed Cloud](https://cloud.google.com/distributed-cloud) (Connected/Edge/Air-gapped) | GDC Edge | [GKE Enterprise](https://cloud.google.com/kubernetes-engine/enterprise/docs) |
| OCI | [Dedicated Region](https://www.oracle.com/cloud/cloud-at-customer/dedicated-region/), [Compute Cloud@Customer](https://www.oracle.com/cloud/cloud-at-customer/) | — | [OCI Multicloud](https://docs.oracle.com/en/solutions/oci-best-practices/deploy-multicloud-oci-oracle-database-services1.html) |

## Use cases

| Case | Requirement | Suitable solution |
| --- | --- | --- |
| **Data sovereignty** | Data must not leave a specific country/facility | Dedicated Region, Azure Stack, GDC Air-gapped |
| **Ultra-low latency** | Factory automation, real-time gaming, AR/VR | Local Zones, Wavelength, Edge Zones |
| **Protecting existing investment** | On-premises equipment still has useful life + wants to use cloud services | Arc, GKE Enterprise, EKS Anywhere |
| **Regulation (closed network / air-gap)** | Environment with no internet connectivity | GDC Air-gapped, Dedicated Region |

## Multi-cloud architecture patterns

| Pattern | Description | Example |
| --- | --- | --- |
| **Split-stack** | Different vendors for different layers | Frontend (AWS CloudFront) + backend/DB (OCI) |
| **Data gravity** | Keep large-volume data in one place; access it from multiple vendors for analytics/AI | Data lake (GCS) + ML (Vertex AI) + serving (AWS) |
| **Best-of-breed** | Choose the optimal vendor per service area | AI (Google Cloud) + enterprise apps (Azure) + DB (OCI) |
| **Cloud-bursting** | On-premises normally, burst to public cloud at peak | On-premises K8s + EKS/AKS/GKE bursting |
| **DR/Failover** | Switch to a secondary vendor if the primary vendor has an outage | AWS (primary) + Azure (DR) |

:::note
Multi-cloud patterns add complexity. Review the motivations and trade-offs first in [Understanding Multi-cloud](../../about-cloud/why-multicloud/) before adopting one.
:::

## Common mistakes

- **Underestimating network latency in hybrid architectures** — Designing synchronous calls without accounting for round-trip latency (tens of ms) between on-premises and cloud sharply degrades performance.
- **Overlooking the operational burden of edge equipment** — Deploying to the edge means patching, incident recovery, and monitoring must be done remotely in environments with difficult physical access. Adopting this without operational automation causes management costs to spike.
- **Defaulting to multi-cloud** — Adopting multi-cloud without a clear business need (regulation, DR, avoiding vendor lock-in) only increases complexity and cost.

## Checklist

- [ ] Have you measured network bandwidth and latency between on-premises and cloud?
- [ ] Do you have a plan for remote management, monitoring, and patch automation for edge/on-premises equipment?
- [ ] Have you documented the business justification (regulation, DR, cost) for adopting hybrid/multi-cloud?

## References

### AWS

- [AWS Outposts documentation](https://docs.aws.amazon.com/outposts/)

### Azure

- [Azure Arc documentation](https://learn.microsoft.com/azure/azure-arc/)

### Google Cloud

- [Google Distributed Cloud documentation](https://cloud.google.com/distributed-cloud)

### OCI

- [OCI Dedicated Region](https://www.oracle.com/cloud/cloud-at-customer/dedicated-region/)
- [OCI Alloy](https://www.oracle.com/cloud/alloy/)

### Standards and community

- [CNCF Multi-Cloud Patterns](https://www.cncf.io/reports/cncf-annual-survey-2023/)
