---
title: "Sustainability and GreenOps"
description: "Cloud sustainability (GreenOps) — comparing carbon emissions tracking, low-carbon design principles, and vendor-specific tools."
---

> Last reviewed: August 2026

## Overview

Cloud sustainability is a **shared responsibility** between vendor and customer. Vendors are responsible for data center efficiency (PUE) and the transition to renewable energy, while customers reduce unnecessary resource use through workload efficiency.

## Vendor Carbon Emissions Tracking Tools

| Vendor | Tool | Features |
| --- | --- | --- |
| AWS | [Customer Carbon Footprint Tool](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/what-is-ccft.html) | Per-account carbon emissions dashboard. Breaks down Scope 1/2/3 |
| Azure | [Emissions Impact Dashboard](https://learn.microsoft.com/azure/carbon-optimization/view-emissions) | Integrates with Microsoft Sustainability Manager. Per-region carbon intensity |
| Google Cloud | [Carbon Footprint](https://cloud.google.com/carbon-footprint) | Per-project emissions. Publishes per-region carbon index (CFE%) |
| OCI | [Sustainability dashboard](https://www.oracle.com/corporate/citizenship/sustainability/) | Per-region energy efficiency reports |

## Sustainable Design Principles

### Choosing Low-Carbon Regions

Each region has a different power mix (share of renewable energy). Workloads with flexible latency requirements can choose regions with lower carbon intensity.

- **AWS** — reported achieving its 100% renewable energy matching goal for operational power in 2023 (reported as sustained in subsequent years). Check per-account emissions with the [Customer Carbon Footprint Tool](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/what-is-ccft.html)
- **Azure** — check Microsoft's public sustainability disclosures for progress on renewable energy and carbon goals. Track emissions with the [Emissions Impact Dashboard](https://learn.microsoft.com/azure/carbon-optimization/view-emissions)
- **Google Cloud** — publishes per-region CFE (Carbon-Free Energy) percentages, with a goal of 24/7 carbon-free energy by 2030
- **OCI** — check Oracle's public disclosures for per-region renewable energy goals and status (e.g., EU regions). Cloud Advisor provides sustainability recommendations

### Resource Efficiency

| Principle | Method | Effect |
| --- | --- | --- |
| **Right-sizing** | Eliminate overprovisioning. Scale down based on CPU/memory utilization | Resource savings = energy savings |
| **Scheduling** | Stop dev environments during off-hours | Eliminates idle resources |
| **Serverless/managed services** | Shared infrastructure increases density | Higher energy efficiency than dedicated servers |
| **Efficient instances** | Choose Arm-based (Graviton, Ampere, Tau) | Lower power consumption for equivalent performance |
| **Data retention policy** | Delete unnecessary data, move to cold storage | Storage energy savings |

### Green Architecture Patterns

- **Asynchronous processing** — spreads out peak load to reduce maximum infrastructure capacity
- **Caching** — reduces compute by eliminating repeated operations/queries
- **Data locality** — placing data and compute in the same region to minimize network transfer

:::note
**GreenOps and FinOps move in the same direction.** Actions that cut costs (removing idle resources, right-sizing, moving to serverless) mostly reduce carbon emissions too. Practicing [FinOps](../../governance/finops/) is effectively practicing GreenOps.
:::

## GreenOps Operational Metrics

### Metrics to Track

| Metric | Description | Source |
| --- | --- | --- |
| Carbon emissions trend per workload | Monthly change in tCO₂e | Vendor carbon dashboard |
| Carbon efficiency per cost | $/tCO₂e | Combination of cost and carbon reports |
| Idle resource ratio | Share of instances with CPU utilization < 5% | Monitoring tools |
| Compute time reduced by scheduling | Savings from automatic shutdown outside business hours | Automation logs |
| Data retention policy savings | Storage reduced via lifecycle policies | Storage reports |

### Scope and Responsibility Boundaries

Scope concepts commonly seen in carbon emissions reports:

| Scope | Description | Meaning in the Cloud |
| --- | --- | --- |
| Scope 1 | Direct emissions (own facilities) | Not applicable to cloud users |
| Scope 2 | Indirect emissions (purchased electricity) | Vendor is responsible via data center power |
| Scope 3 | Value chain emissions | **The user's cloud usage** falls here |

Areas users can directly reduce: eliminating idle resources, right-sizing, choosing low-carbon regions, efficient architecture.

### Differences Between FinOps and GreenOps

They have much in common, but not always:

| Situation | FinOps View | GreenOps View |
| --- | --- | --- |
| A low-carbon region is more expensive | Choose the lowest-cost region | Choose the lowest-carbon region |
| Spot instances | Cost savings ✅ | Repeated restarts can actually reduce efficiency |
| Removing idle resources | Cost savings ✅ | Carbon savings ✅ (same) |
| Right-sizing | Cost savings ✅ | Carbon savings ✅ (same) |

### Decision Checklist

- [ ] Is this a workload that cannot change regions due to latency/SLA constraints?
- [ ] Is this a workload, like a batch job, whose execution time can be adjusted?
- [ ] Is the data retention period longer than regulatory requirements demand?
- [ ] Does carbon optimization avoid compromising security, availability, or compliance?

## Common Mistakes

- **Choosing a low-carbon region while ignoring latency requirements** — selecting a region far from users, causing response times to exceed the SLA
- **Tracking GreenOps metrics without taking real action** — building dashboards without following through on actions like removing idle resources or scheduling
- **Running FinOps and GreenOps as separate initiatives** — most cost-saving activities are also carbon-saving, so this creates duplicate organizations/processes

## Checklist

- [ ] Have you enabled the vendor carbon emissions dashboard (e.g., Customer Carbon Footprint Tool) and tracked monthly trends?
- [ ] Have you applied scheduling to automatically stop dev/test environments during off-hours?
- [ ] Do you prioritize Arm-based instances (Graviton, Ampere) for compatible workloads?

## References

### AWS

- [AWS Sustainability Pillar (Well-Architected)](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html)

### Azure

- [Azure Well-Architected — Sustainability](https://learn.microsoft.com/azure/well-architected/sustainability/)

### Google Cloud

- [Google Cloud Carbon Footprint](https://cloud.google.com/carbon-footprint)
- [Google Cloud Region Carbon-Free Energy](https://cloud.google.com/sustainability/region-carbon)

### OCI

- [Oracle Cloud Sustainability](https://www.oracle.com/corporate/citizenship/sustainability/)

### Standards and Community

- [Green Software Foundation](https://greensoftware.foundation/)
