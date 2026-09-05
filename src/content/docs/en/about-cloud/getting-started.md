---
title: "Getting Started with Cloud"
description: "Explains the definition of cloud, the IaaS/PaaS/SaaS service models, and the public/private/hybrid deployment models."
---

> Last reviewed: August 2026

## Definition of Cloud

Cloud computing is a service that provides computing resources (servers, storage, networking, and more) on demand over the internet. Used well, it offers advantages in infrastructure build speed, operational efficiency, and cost structure.

From an infrastructure provisioning perspective, the process of purchasing servers, installing them in racks, and configuring networks in your own data center can be replaced with API calls. However, preparatory work such as security review, verifying regulatory requirements, and designing access control is still necessary.

That said, it is difficult to expect the well-known benefits of cost savings or stable operations simply by using the cloud. You need to change your application's architecture to match how the cloud operates. Changing the architecture and making the most of managed services can streamline operational resources, letting you focus your people and budget on creating business value. However, the more you depend on managed services, the more vendor lock-in increases, so you should also consider an [exit strategy](../../governance/exit-strategy/).

:::note
NIST SP 800-145 defines cloud computing as *"a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources that can be rapidly provisioned and released with minimal management effort or service provider interaction."*
:::

## Core Characteristics of Cloud (Summary)

Here are the five core characteristics of cloud as defined by NIST.

| Characteristic | Description | Compared to On-Premises |
| --- | --- | --- |
| **On-demand self-service** | Create resources within minutes via web console/API | Weeks to months to purchase and install → instant |
| **Broad network access** | Access from anywhere over the internet using standard protocols | VPN/dedicated line required → not required |
| **Resource pooling** | Dynamic allocation via multi-tenant model, region-level location assignment | Fixed allocation per department → shared pool |
| **Rapid elasticity** | Automatic scale up/down based on traffic | Pre-provisioned for peak load → real-time adjustment |
| **Measured service** | Usage-based pay-as-you-go (per second/hour/GB) | Fixed depreciation cost → variable cost |

## Why Use Cloud

Here are concrete scenarios, compared with on-premises, showing what practical value the five NIST characteristics create.

### Elasticity — Instant response to traffic fluctuations

On-premises, you must purchase additional servers weeks in advance before Black Friday or a new service launch. If your forecast is off, you either run short on servers (outage) or have excess (waste).

In the cloud, autoscaling adds or removes servers within minutes based on traffic. Once the event ends, capacity automatically scales down, reducing cost.

| Scenario | On-Premises | Cloud |
| --- | --- | --- |
| 10x increase in event traffic | Servers must be purchased and installed weeks in advance | Autoscaling responds within minutes |
| After the event ends | Remaining servers sit idle (depreciation continues) | Automatic scale-down, cost drops immediately |
| Forecast failure | Server shortage → outage or emergency purchase | Just adjust the limit for instant scaling |

### Scalability — Global service in minutes

On-premises, launching a service overseas requires months for local data center contracts, server shipping, and network configuration.

In the cloud, you can choose the region you want and deploy the same infrastructure code to go global within minutes.

| Scenario | On-Premises | Cloud |
| --- | --- | --- |
| Entering the Southeast Asia market | Data center contract + server purchase + networking (3-6 months) | Deploy to the Singapore region (minutes) |
| Decision to withdraw a service | Equipment disposal, contract termination (penalty fees) | Delete resources (instant, zero cost) |

:::note
The table above compares only infrastructure provisioning speed. In practice, entering an overseas market requires reviewing local regulations, data sovereignty, and compliance requirements first.
:::

### Cost structure shift — From fixed costs to variable costs

On-premises is **capital expenditure** (CapEx), where depreciation begins the moment you purchase a server. Cloud shifts this to **operational expenditure** (OpEx), where you pay only for what you use. However, you can only enjoy this benefit if you design your architecture for the cloud. Simply lifting and shifting your on-premises setup onto the cloud as-is can actually increase costs.

:::caution
**Cloud does not automatically become cheaper.** To realize the benefits of cloud, you need to design a cloud-native architecture and continuously monitor costs. For a detailed cost breakdown, see [Understanding the Cost Structure](../../about-cloud/pricing-model/); for cost optimization operations, see [FinOps](../../governance/finops/).
:::

### Reduced operational burden — Leveraging managed services

On-premises, operating a database requires you to handle OS patching, DB engine updates, backups, replication, and failover all yourself.

Managed cloud services (RDS, Cloud SQL, and so on) let the vendor handle this operational burden instead. DBAs can then focus on schema design and query optimization.

## Service Models: IaaS, PaaS, SaaS

Cloud services are divided into three models based on the scope the vendor manages. Compared to your own data center, they work as follows:

- **IaaS (Infrastructure as a Service)** — Similar to renting a building. The building (servers, network, storage) is provided, but you must configure the interior (OS, middleware, applications) yourself.
- **PaaS (Platform as a Service)** — Similar to renting an office. The desks and chairs (runtime, middleware) are already set up, so you can focus solely on the work (application code).
- **SaaS (Software as a Service)** — Similar to staying at a hotel. Everything is ready; you simply use the service as-is.

| Service Model | User-Managed Scope | AWS Example | Azure Example | Google Cloud Example |
| --- | --- | --- | --- | --- |
| **IaaS** | OS, middleware, app, data | EC2, EBS, VPC | Virtual Machines, VNet | Compute Engine, VPC |
| **PaaS** | App, data | Elastic Beanstalk, RDS | App Service, Azure SQL | App Engine, Cloud SQL |
| **SaaS** | Data (settings) | WorkMail, Chime | Microsoft 365, Dynamics 365 | Google Workspace |

The division of responsibility between the user and the vendor varies by service model. This is covered in detail in [Shared Responsibility Model](../../about-cloud/shared-responsibility/).

## Deployment Models: Public, Private, Hybrid

Cloud is divided into three deployment models based on who owns and operates the infrastructure.

### Public Cloud

A model where infrastructure owned and operated by a vendor such as AWS, Azure, or Google Cloud is shared by multiple customers over the internet. You can start using it immediately with no upfront investment, and it allows elastic scaling. Most of the content covered in CloudPick is based on public cloud.

### Private Cloud

A cloud operated exclusively for a specific organization. It can be built in your own data center, or provided by a vendor as dedicated infrastructure. It is widely used in the finance and public sectors, where security and regulatory requirements are strict.

### Hybrid Cloud

A model that connects and uses public cloud and private cloud (or on-premises) together. It is typically operated by placing sensitive data in a private environment while placing elastic workloads in the public cloud.

| Deployment Model | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Public** | AWS Region | Azure Region | Google Cloud Region | OCI Region |
| **Private/On-Premises Extension** | Outposts | Azure Stack, Azure Local | Google Distributed Cloud | Dedicated Region |
| **Hybrid Management** | EKS Anywhere, ECS Anywhere | Azure Arc | Anthos | OCI Multicloud |

## Understanding Multi-Cloud

Using a single cloud vendor is the simplest approach, but in practice, more organizations are adopting a **multi-cloud** strategy that uses multiple vendors together. According to the CNCF 2024 survey, roughly 60% of enterprises use two or more clouds.

The motivations and challenges of adopting multi-cloud are covered in detail in [Understanding Multi-Cloud](../../about-cloud/why-multicloud/).

CloudPick aims to help you make sound decisions in a multi-cloud environment, centered around the major global cloud vendors.

## Common Mistakes

- **"Moving to the cloud automatically reduces costs"** — Lifting and shifting your on-premises structure as-is can actually increase costs. A shift to cloud-native architecture is required.
- **"The cloud vendor manages everything for you"** — The user's scope of responsibility differs depending on the service model (IaaS/PaaS/SaaS). Data and access control are always the user's responsibility.
- **"The free tier is enough to run on"** — The free tier is meant for learning and PoCs. Exceeding the free limits can result in unexpected charges, so set up budget alerts.

## Checklist

- [ ] Have you checked the free tier scope and limits of the vendor you plan to use?
- [ ] Have you enabled MFA (multi-factor authentication) on the root/admin account?
- [ ] Have you set up budget alerts to prevent unexpected charges?

## References

### Standards and Frameworks

- [NIST SP 800-145 — The NIST Definition of Cloud Computing](https://csrc.nist.gov/publications/detail/sp/800-145/final) — Official definition of cloud computing
- [ISO/IEC 17788 — Cloud computing: Overview and vocabulary](https://www.iso.org/standard/60544.html) — Cloud terminology standard
- [ISO/IEC 22123 — Cloud computing: Concepts and terminology](https://www.iso.org/standard/82758.html) — Latest standard including multi-cloud

### AWS

- [What is Cloud Computing?](https://aws.amazon.com/ko/what-is-cloud-computing/)
- [What is AWS?](https://aws.amazon.com/ko/what-is-aws/)
- [AWS Global Infrastructure](https://aws.amazon.com/ko/about-aws/global-infrastructure/)

### Azure

- [What is Cloud Computing?](https://azure.microsoft.com/ko-kr/resources/cloud-computing-dictionary/what-is-cloud-computing)
- [What is Azure?](https://azure.microsoft.com/ko-kr/resources/cloud-computing-dictionary/what-is-azure)
- [Azure Global Infrastructure](https://azure.microsoft.com/ko-kr/explore/global-infrastructure/)

### Google Cloud

- [What is Cloud Computing?](https://cloud.google.com/learn/what-is-cloud-computing)
- [Why Google Cloud](https://cloud.google.com/why-google-cloud)
- [Google Cloud Locations](https://cloud.google.com/about/locations)

### OCI

- [What is OCI?](https://www.oracle.com/kr/cloud/what-is-cloud-computing/)
- [OCI Services](https://www.oracle.com/kr/cloud/)
- [OCI Global Infrastructure](https://www.oracle.com/cloud/cloud-regions/)
