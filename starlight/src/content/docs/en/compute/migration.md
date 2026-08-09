---
title: "Application Migration"
description: "Compares workload migration strategies (the 7 Rs), assessment/execution phases, and lift-and-shift vs. refactoring trade-offs across vendors."
---

> Last reviewed: May 2026

## Overview

This is the work of moving applications and infrastructure from on-premises or another cloud into the cloud. It's not simply copying VMs — it's a process of re-evaluating the entire application's architecture, dependencies, and operational model.

:::note
For database migration, see [Database Migration](../../database/migration/); for large-scale file transfer, see [Storage Migration](../../storage/migration/).
:::

:::caution
**Prepare your governance foundation before migrating.** If you move workloads without account/organization structure, networking (VPC/subnets), IAM policy, a tagging scheme, and logging in place, you'll have to rebuild everything later. Review [Getting Started with Cloud Governance](../../governance/getting-started/) → [Landing Zone](../../governance/landing-zone/) first.
:::

## The 7R migration strategy

The **7R framework**, proposed by Gartner and extended by AWS, is the standard for classifying migration strategies per workload.

| Strategy | Description | Difficulty | Effect |
| --- | --- | --- | --- |
| **Retire** | Discontinue a workload that's no longer needed | Low | Immediate cost savings |
| **Retain** | Keep it on-premises (hybrid) | Low | No migration cost |
| **Relocate** | Move as-is at the hypervisor level (e.g., VMware Cloud on AWS) | Low | Fast transition with minimal change |
| **Rehost** | VM-level Lift & Shift | Low | Fast transition, limited cloud benefits |
| **Replatform** | Partial transition to managed services (e.g., DB to RDS) | Medium | Reduced operational burden |
| **Repurchase** | Switch to SaaS (e.g., a homegrown CRM → Salesforce) | Medium | Delegated operational responsibility |
| **Refactor** | Redesign as cloud-native (serverless, microservices) | High | Maximizes scalability/efficiency |

### Strategy selection criteria

| Situation | Recommended strategy |
| --- | --- |
| Tight data center exit deadline | Relocate or Rehost |
| Low business value, short-lived workload | Retire |
| Functionality already available as a commercial solution | Repurchase (SaaS) |
| Core workload where you want to maximize cloud benefits (scalability, cost) | Refactor |
| Legacy system that needs stable operation with no changes | Retain |
| Want to reduce operational burden while keeping the code | Replatform |

:::caution
**Caution:** Trying to Refactor every workload causes time and cost to spike. Most enterprises use a hybrid approach — **Rehost/Replatform as the default, and Refactor only the core workloads**.
:::

## Lift-and-shift vs. refactoring trade-offs

A comparison of the two most common options: Rehost (Lift & Shift) and Refactor.

| Item | Rehost (Lift & Shift) | Refactor (cloud-native) |
| --- | --- | --- |
| **Migration duration** | Weeks to months | Months to years |
| **Development cost** | Low (minimal change) | High (redesign/reimplementation) |
| **Operational cost** | Similar to on-premises | Can be reduced via cloud optimization |
| **Scalability** | Limited (VM-based) | High (serverless, horizontal scaling) |
| **Disaster recovery** | Retains existing approach | Cloud-native HA/DR |
| **Risk** | Low | High (redesign may fail) |
| **Leveraging cloud benefits** | Limited | Maximal |
| **Data center exit deadline** | Can meet even short deadlines | Requires a long timeframe |

:::note
**Common pattern:** If there's a data center exit deadline, a realistic strategy is to **first migrate via Rehost, then gradually Replatform/Refactor after stabilizing**. Trying to Refactor every workload from the start tends to cause schedule delays and quality issues.
:::

## Migration process

Large-scale migration is a project that goes through multiple phases.

| Phase | Key activities |
| --- | --- |
| **1. Discovery** | Collect inventory — identify servers, applications, dependencies, and usage |
| **2. Assessment** | Decide the 7R strategy per workload, estimate cost, analyze risk |
| **3. Planning** | Decide migration order (waves), rollback plan, downtime budget |
| **4. Landing Zone** | Build the cloud account/network/security foundation (see [Landing Zone](../../governance/landing-zone/)) |
| **5. Migration** | Perform the actual data/application transfer |
| **6. Validation** | Performance/functional testing, user acceptance testing |
| **7. Cutover** | Traffic switchover, heightened monitoring |
| **8. Optimize** | Optimize the cloud environment (cost, performance, security) |

### Migration waves

Migrating hundreds or thousands of workloads at once is risky. Migration is typically carried out in **waves**.

- **Pilot wave** — Build experience with simple, low-risk workloads (e.g., internal tools, dev environments)
- **Core waves** — Group applications and migrate them sequentially
- **Critical wave** — Migrate business-critical workloads last (after sufficient validation)

## Minimizing downtime

Production workloads need to minimize downtime.

| Technique | Description | When to use |
| --- | --- | --- |
| **Continuous block-level replication** | Continuously replicates changed blocks from the source VM to the target | The default approach for most VM migration tools |
| **Blue/Green cutover** | Run old and new infrastructure in parallel, then switch via DNS/LB | Web services, APIs |
| **Database CDC** | Continuously replicate DB changes so cutover completes within minutes | DB migration |
| **Phased cutover** | Gradual transition by user/region/feature | Services with large user bases |

## Cutover checklist

Items to verify at the actual cutover moment.

- [ ] Data integrity verification complete (checksums, record counts)
- [ ] Application functional testing complete
- [ ] Performance benchmarks meet or exceed the existing environment
- [ ] Security settings verified (IAM, firewall, encryption)
- [ ] Backup/DR configuration complete
- [ ] Monitoring and alerting confirmed to be working
- [ ] Rollback plan and rollback decision point determined
- [ ] Stakeholders notified and Go/No-Go approval obtained
- [ ] Cutover time window confirmed (weekend/night)
- [ ] Response staff on standby in case of an incident

## Migration tools

:::note
**AI-assisted migration:** Each CSP offers services that use AI to automate migration assessment, code conversion, and testing. Notable examples include [AWS Transform](https://aws.amazon.com/transform/) (AI-based code conversion), [Azure Migrate with Copilot](https://learn.microsoft.com/azure/migrate/) (automated assessment), and [Google Cloud Dual Run](https://cloud.google.com/blog/products/databases/dual-run-for-mainframe-modernization) (parallel mainframe validation). These can significantly reduce manual analysis time for large-scale legacy conversions, but AI output still requires validation.
:::

### Assessment and discovery

| Vendor | Product | Capability |
| --- | --- | --- |
| AWS | [Application Discovery Service](https://aws.amazon.com/application-discovery/) | Agent-based/agentless on-premises inventory collection |
| AWS | [Migration Hub](https://aws.amazon.com/migration-hub/) | Central migration dashboard |
| Azure | [Azure Migrate](https://azure.microsoft.com/products/azure-migrate/) | Assessment plus integrated server/DB migration |
| Google Cloud | [Migration Center](https://cloud.google.com/migration-center/docs) | Portfolio assessment, dependency mapping |
| OCI | [Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm) | Integrated assessment and execution |

### VM/server migration

| Vendor | Product | Capability |
| --- | --- | --- |
| AWS | [Application Migration Service (MGN)](https://aws.amazon.com/application-migration-service/) | Block-level replication. Minimal-downtime Rehost |
| Azure | [Azure Migrate: Server Migration](https://learn.microsoft.com/azure/migrate/migrate-services-overview) | VMware/Hyper-V/physical servers → Azure VM |
| Google Cloud | [Migrate to Virtual Machines](https://cloud.google.com/migrate/virtual-machines/docs) | VMware/AWS/Azure → Compute Engine |
| OCI | [OCI Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm) | VMware/AWS → OCI |

### Containerization

| Vendor | Product | Capability |
| --- | --- | --- |
| AWS | [App2Container](https://aws.amazon.com/app2container/) | Containerize Java/.NET apps |
| Azure | [Migrate to containers](https://learn.microsoft.com/azure/migrate/tutorial-app-containerization-aspnet-kubernetes) | ASP.NET/Java → AKS |
| Google Cloud | [Migrate to Containers](https://cloud.google.com/migrate/containers/docs) | VM → GKE containers |

## Common mistakes

- **Starting migration without Discovery/Assessment** — Without understanding dependencies and traffic patterns, failures occur post-cutover and rollback becomes necessary.
- **Migrating workloads before a landing zone exists** — Moving without account structure, networking, IAM, and a tagging scheme in place means everything has to be rebuilt later.
- **Trying to Refactor all workloads at once** — Schedules collapse and quality issues arise. For most, Rehost followed by gradual improvement is more realistic.

## References

### AWS

- [AWS Cloud Migration](https://aws.amazon.com/cloud-migration/)
- [AWS Migration Hub](https://aws.amazon.com/migration-hub/)
- [AWS Application Migration Service](https://aws.amazon.com/application-migration-service/)
- [AWS Prescriptive Guidance: Migration Strategies (7R)](https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html)

### Azure

- [Azure Migrate](https://azure.microsoft.com/products/azure-migrate/)
- [Cloud Adoption Framework — Migrate](https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/)
- [Azure Migrate documentation](https://learn.microsoft.com/azure/migrate/)

### Google Cloud

- [Migration Center](https://cloud.google.com/migration-center/docs)
- [Migrate to Virtual Machines](https://cloud.google.com/migrate/virtual-machines/docs)
- [Migrate to Containers](https://cloud.google.com/migrate/containers/docs)

### OCI

- [OCI Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm)
- [OCI Migration Solutions](https://www.oracle.com/cloud/migration/)
