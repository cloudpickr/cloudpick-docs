---
title: "Understanding the Cost Structure"
description: "Compares on-demand, reserved, and spot pricing models, plus hidden cost items such as egress, across vendors."
---

> Last reviewed: August 2026

## On-Premises vs. Cloud Cost Structure

Running your own data center incurs costs before you even purchase a server. Server purchase costs, rack space rental, power and cooling costs, network equipment, and even the personnel costs to manage all of it — hundreds of millions of won in upfront investment is required before you even launch a service. This is called **capital expenditure** (CapEx). It is similar to buying a house — you pay a large sum upfront, then continue to bear maintenance costs afterward.

Cloud shifts this structure to **OpEx** (Operational Expenditure). With no upfront investment, you pay only for what you use. It is similar to living in a rental — you move in when you need to, and move out when you don't.

| Item | On-Premises (CapEx) | Cloud (OpEx) |
| --- | --- | --- |
| **Upfront investment** | Purchasing servers and network equipment (hundreds of millions of won) | None |
| **Billing method** | Depreciation after purchase (3-5 years) | Usage-based pay-as-you-go |
| **Scaling up** | Purchasing additional equipment (weeks to months) | Instant scaling |
| **Scaling down** | Difficult to dispose of equipment | Instant scale-down, cost savings |
| **Maintenance** | Requires your own staff | Managed by the vendor |

That said, cloud isn't always cheaper. Workloads that run at a constant load 24/7/365 may be more economical on-premises. The cost advantage of cloud is maximized with **elastic usage patterns**.

## Core Pricing Models

| Model | Discount Rate | Commitment | Interruption Risk | Suitable Workloads |
| --- | --- | --- | --- | --- |
| **On-Demand** | None (base price) | — | None | Dev/test, services with unpredictable traffic |
| **Reserved/Committed** | 30-72% | 1 or 3 years | None (contract-guaranteed) | Stable production, 24/7 operations |
| **Spot/Preemptible** | 60-90% | — | **Yes** (vendor can reclaim) | Batch, CI/CD, data analytics |
| **Free Tier** | 100% (within free limits) | — | Billed or stopped once free limits are exceeded | Learning, PoCs, small-scale experiments |

### On-Demand (Pay-As-You-Go)

The most basic pricing method. You pay only for what you use, with no commitment. Because you can start and stop freely, it suits dev/test environments or workloads with unpredictable traffic.

### Reserved/Committed Discounts

Committing to 1 or 3 years of usage earns you a 30-72% discount compared to on-demand. However, costs accrue during the commitment period regardless of actual usage. It suits stably operated production workloads, and can actually be a loss for workloads with uncertain usage. For commitment strategy and detailed comparisons, see [FinOps](../../governance/finops/).

### Spot/Preemptible Instances

You can use a vendor's idle resources at a 60-90% discount compared to on-demand. However, because the vendor can reclaim these resources, they can be interrupted at any time. They suit workloads resilient to interruption, such as batch processing, data analytics, and CI/CD builds.

Handling interruptions:

- **Interruption notice** — The vendor sends a notification to the metadata endpoint 2 minutes before reclamation (AWS) or 30 seconds before (Google Cloud/Azure). Your application must detect this signal, checkpoint any in-progress work, and shut down gracefully.
- **State recovery** — Periodically save job state to external storage (S3, Blob, and so on) as a checkpoint, and resume from the last checkpoint when a new instance starts.
- **Automatic retry** — An Auto Scaling Group or Managed Instance Group automatically replaces interrupted instances. Combined with a job queue (SQS, and so on), failed jobs are automatically reprocessed on another instance.

### Free Tier

Every vendor offers a free usage allowance for new users. It's a structure designed to let users try out the service directly and, once familiar, naturally transition to paid usage. It lets you learn and experiment without cost concerns when first starting out with cloud.

## Comparison by Vendor

| Pricing Model | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **On-demand** | On-Demand | Pay-As-You-Go | On-Demand | Pay-As-You-Go |
| **Committed discount (instance)** | Reserved Instances | Reserved VM Instances | — | — |
| **Committed discount (flexible)** | Savings Plans | Azure Savings Plan | CUD (Committed Use) | Universal Credits |
| **Spot** | Spot Instances | Spot VMs | Spot VMs | Preemptible Instances |
| **Automatic discount** | — | — | SUD (Sustained Use) | — |
| **Free egress** | — | — | 200GB/month | **10TB/month** |
| **Free tier** | 12 months + Always Free | 12 months + Always Free | 90 days $300 + Always Free | Always Free (generous) |
| **Billing unit** | Per second | Per second | Per second | Per second |

### Key Differences

**Google Cloud's SUD (Sustained Use Discounts)** — Automatic discount of up to 30% when usage exceeds a certain duration within a month, with no commitment required.

**OCI's egress policy** — Free egress up to 10TB per month. This can create a significant cost difference in multi-cloud environments where data movement is frequent.

**OCI Universal Credits** — A flexible commitment model usable across all OCI services, not tied to a specific service.

## Watch Out for Hidden Costs

These are the most commonly overlooked items in cloud costs. Because these costs don't arise on-premises, they warrant particular attention.

### Data Transfer (Egress) Costs

Uploading data to the cloud (ingress) is free, but sending data out of the cloud (egress) is billed. This cost can be substantial for workloads that frequently transfer large volumes of data externally.

| Vendor | Free Allowance | Rate Beyond That | When Switching to Another Cloud |
| --- | --- | --- | --- |
| AWS | 100GB/month | $0.09-0.12/GB (varies by region) | Free (application required) |
| Azure | 100GB/month | $0.08-0.12/GB | Free (application required) |
| Google Cloud | 200GB/month | $0.08-0.12/GB | Free (application required) |
| OCI | **10TB/month** | $0.0085/GB | Not applicable (default free allowance is generally sufficient) |

:::note
AWS, Azure, and Google Cloud all offer policies that waive egress costs when fully migrating to another cloud or on-premises. However, advance application is required, and this does not apply to routine data transfer.
:::

### Multi-Cloud Data Movement — Cost and Latency

The biggest practical barriers when considering multi-cloud are **inter-cloud data transfer costs** and **latency caused by physical distance**.

**Data gravity:** Compute resources inevitably gravitate toward where data has accumulated. The cost of moving petabyte-scale data to another vendor can reach tens of millions to hundreds of millions of won.

**Latency when distributing across clouds:** Splitting tiers across clouds — for example, Web (AWS) and DB (OCI) — adds round-trip latency (RTT). RTT between AZs within the same region is about 1ms, but a dedicated connection between clouds adds 5-20ms. This difference can significantly affect perceived performance for services with heavy API call volume.

**Decision criteria for multi-cloud distribution:**

| Question | Yes → | No → |
| --- | --- | --- |
| Is real-time data exchange between clouds frequent? | Keep with the same vendor | Distribution possible |
| Is egress cost 10% or more of the monthly budget? | Reconsider data placement | Keep as-is |
| Would adding 10ms of latency affect the SLA? | Keep with the same vendor/region | Distribution possible |

:::caution
Weigh the benefits of multi-cloud (avoiding vendor lock-in, combining best-of-breed services) against cost/performance constraints. Layers with little data (frontend, static assets) are generally easy to distribute, while layers with a lot of data (DB, analytics) are generally consolidated in one place.
:::

### Storage API Call Costs

Beyond the cost of storing data, costs also arise from the API calls used to read and write it. This is negligible at small scale, but becomes a significant amount for workloads generating millions of API calls.

### Logging/Monitoring Costs

The costs of log collection and storage in monitoring services such as CloudWatch (AWS), Azure Monitor (Azure), and Cloud Logging (Google Cloud) are also easy to overlook. Failing to appropriately configure log retention periods and collection scope can result in unexpected costs.

## Cost Management Tools

Each vendor provides tools for monitoring and optimizing costs.

| Vendor | Cost Dashboard | Pricing Calculator |
| --- | --- | --- |
| AWS | [Cost Explorer](https://aws.amazon.com/ko/aws-cost-management/aws-cost-explorer/) | [Pricing Calculator](https://calculator.aws/) |
| Azure | [Cost Management](https://azure.microsoft.com/ko-kr/products/cost-management/) | [Pricing Calculator](https://azure.microsoft.com/ko-kr/pricing/calculator/) |
| Google Cloud | [Cost Management](https://cloud.google.com/cost-management) | [Pricing Calculator](https://cloud.google.com/products/calculator) |
| OCI | [Cost Analysis](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm) | [Cost Estimator](https://www.oracle.com/cloud/costestimator.html) |

## Common Mistakes

- **"Cloud only costs what you use"** — There are hidden cost items such as egress, API calls, and log storage. You need to identify the major cost items in advance.
- **"A committed discount is always a good deal"** — Committing for a workload with uncertain usage can actually result in a loss. Commit only after confirming a stable usage pattern.
- **"The free tier is completely free"** — Charges apply automatically once you exceed the free limits. Set up budget alerts and monitor usage.

## Checklist

- [ ] Have you set up budget alerts to be notified when estimated costs are exceeded?
- [ ] Have you simulated your expected monthly cost, including egress, using the vendor's pricing calculator?
- [ ] Have you established a policy to stop dev/test environment resources outside of business hours?

## References

### Standards and Frameworks

- [FinOps Foundation — FinOps Framework](https://finops.org/framework) — Cloud cost management framework
- [FinOps Foundation — FOCUS Specification](https://focus.finops.org/) — Standardization spec for multi-cloud cost data
- [Flexera State of the Cloud Report](https://info.flexera.com/CM-REPORT-State-of-the-Cloud) — Annual report on cloud cost/adoption trends

### AWS

- [AWS Pricing](https://aws.amazon.com/ko/pricing/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Cost Explorer](https://aws.amazon.com/ko/aws-cost-management/aws-cost-explorer/)
- [AWS Free Tier](https://aws.amazon.com/ko/free/)

### Azure

- [Azure Pricing](https://azure.microsoft.com/ko-kr/pricing/)
- [Azure Pricing Calculator](https://azure.microsoft.com/ko-kr/pricing/calculator/)
- [Azure Cost Management](https://azure.microsoft.com/ko-kr/products/cost-management/)
- [Azure Free Account](https://azure.microsoft.com/ko-kr/free/)

### Google Cloud

- [Google Cloud Pricing](https://cloud.google.com/pricing)
- [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)
- [Cost Management](https://cloud.google.com/cost-management)
- [Google Cloud Free Program](https://cloud.google.com/free)

### OCI

- [OCI Pricing](https://www.oracle.com/kr/cloud/pricing/)
- [OCI Cost Estimator](https://www.oracle.com/cloud/costestimator.html)
- [OCI Free Tier](https://www.oracle.com/cloud/free/)
