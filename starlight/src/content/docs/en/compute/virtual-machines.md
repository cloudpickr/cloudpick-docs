---
title: "Virtual Machines"
description: "Compares general-purpose, Arm, and GPU virtual machine products and images (OS templates) across vendors."
---

> Last reviewed: July 2026

## Overview

Operating servers in your own data center requires purchasing hardware, installing it, configuring the OS, and setting up networking yourself. Provisioning equipment takes weeks, and changing specs requires a physical swap.

A **virtual machine** (VM) replaces this process with software. You can create a server with the specs you want in minutes, and delete it immediately once it's no longer needed. It's the cloud's most fundamental service, solving the flexibility problem of physical servers.

That said, with a VM you still have to manage OS patching, security configuration, and incident response yourself. To reduce this management burden, higher levels of abstraction such as containers and serverless have emerged.

## Product comparison

### General-purpose VM

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | EC2 (Elastic Compute Cloud) | 400+ instance types. Segmented into general-purpose, compute, memory, GPU, etc. |
| Azure | Virtual Machines | Strong for Windows workloads (Hybrid Benefit) |
| Google Cloud | Compute Engine | Custom Machine Type allows freely combining CPU/memory |
| OCI | OCI Compute | Flexible Shape allows freely combining CPU/memory. Ampere A1 free tier |

### Arm-based VM

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | EC2 Graviton (t4g, m7g, etc.) | In-house designed Arm processor. Better price-performance than x86 |
| Azure | Dpsv5/Dplsv5 series | Based on Ampere Altra |
| Google Cloud | Tau T2A | Arm-based general purpose |
| OCI | Ampere A1 Compute | Based on Ampere Altra. Free tier available |

### GPU / AI accelerators

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | P5, **G7**, G5, Inf2, Trn1/Trn2 | NVIDIA (H100, **RTX PRO 4500 Blackwell**) + in-house chips (Inferentia, Trainium). G7 is the first major cloud offering of RTX PRO Blackwell |
| Azure | NC, ND, NV series | NVIDIA A100, H100 |
| Google Cloud | A3, A2, G2 series + TPU v8 | NVIDIA H100 + in-house TPU (latest v8 generation) |
| OCI | GPU Instances (A10, A100, H100) | NVIDIA GPU. Bare Metal option available |

### Images (OS templates)

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | AMI (Amazon Machine Image) | 3rd-party images available on Marketplace |
| Azure | VM Image / Shared Image Gallery | |
| Google Cloud | Image / Image Family | |
| OCI | Custom Image / Platform Image | 3rd-party images available on Marketplace |

:::note
VMs are the **compute service with the greatest management burden**. You have to handle OS patching, security configuration, and high-availability setup yourself. If you want to reduce operational burden, consider a managed container service or serverless.
:::

## Key differences

- **AWS** — Has the widest variety of instance types, and its in-house Arm processor (Graviton) enables cost savings.
- **Azure** — Hybrid Benefit lets you leverage existing Windows licenses to reduce cost.
- **Google Cloud** — Offers Custom Machine Type for freely combining CPU and memory.
- **OCI** — Flexible Shape lets you freely combine CPU/memory, and offers an Ampere A1 free tier.

## What to choose when

| In this situation | Choose this |
| --- | --- |
| Windows workload + leveraging an existing license | Azure VM (Hybrid Benefit) |
| You need the widest selection of instance types | AWS EC2 |
| You want to freely combine CPU/memory in 1-vCPU increments | Google Cloud Compute Engine (Custom Machine Type) or OCI (Flexible Shape) |
| Your goal is Arm-based cost savings | AWS EC2 Graviton |
| You want to use an Arm VM on the free tier | OCI Ampere A1 |
| You need GPU/AI accelerators + in-house chips (Inferentia, Trainium) | AWS EC2 (P5, Inf2, Trn1) |
| You need a bare metal server | OCI Bare Metal or AWS Bare Metal |

## Purchasing options (pricing models)

For the same VM, price can vary greatly depending on the commitment model.

| Option | Description | Discount rate | Risk |
| --- | --- | --- | --- |
| **On-Demand (Pay-As-You-Go)** | Billed by the second/hour based on usage | 0% (baseline) | None |
| **Reserved** | 1- or 3-year commitment | Up to 72% | Charged even if unused |
| **Savings Plans / Savings Plan / CUD** | Commit to a spending amount per hour | Up to 72% | Flexible, but requires a usage commitment |
| **Spot / Preemptible** | Use spare capacity at a low price | Up to 90% | Can be reclaimed at any time |
| **Reserved Capacity** | Reserve capacity in a specific AZ/zone | — | Guarantees capacity availability |

### Purchasing options comparison

| Vendor | On-demand | Long-term commitment | Spot |
| --- | --- | --- | --- |
| AWS | On-Demand | Reserved Instance + Savings Plans | Spot Instance |
| Azure | Pay-As-You-Go | Reserved VM Instance + Savings Plan | Spot VM |
| Google Cloud | On-Demand | Committed Use Discount (CUD) | Preemptible / Spot VM |
| OCI | Pay-As-You-Go | Monthly Flex / Annual Flex / Universal Credits | Preemptible Instance |

> The figures above are as of the time this document was written and are subject to change. Check each vendor's official pricing page for the latest prices.

:::note
For details on cost structure, see [Understanding the Pricing Model](../../about-cloud/pricing-model/).
:::

## Placement groups and dedicated hosts

You can physically control VM placement to meet high-performance/compliance requirements.

| Feature | Description | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- | --- |
| **Same-rack placement** | Low-latency communication (HPC, distributed DBs) | Placement Group (Cluster) | Proximity Placement Group | Compact Placement | Cluster Network |
| **Spread placement** | Eliminate a single point of failure | Placement Group (Spread) | Availability Set | Spread Placement | Fault Domain |
| **Dedicated physical server** | Licensing/compliance | Dedicated Host | Dedicated Host | Sole-tenant Node | Dedicated VM Host |

## Common mistakes

- **Running everything on-demand and then complaining about cost** — For stable, predictable workloads, Reserved Instances or Savings Plans can save up to 72%. Analyze your usage pattern.
- **Choosing an instance type once and never revisiting it** — Vendors continuously release new generations. You can get higher performance for the same cost, so review regularly.
- **Manual configuration every time, without a golden image** — Repeating package installs and configuration every time you create an instance breaks consistency and wastes time. Manage AMIs/images through a build pipeline.

## Checklist

- [ ] Have you chosen an instance family that fits the workload's characteristics (CPU/memory/GPU)?
- [ ] Have you applied Reserved Instances or Savings Plans to stable, steady-state workloads?
- [ ] Is OS patching and security update automation (SSM, Update Management, etc.) configured?

## References

### AWS

- [Amazon EC2 documentation](https://docs.aws.amazon.com/ko_kr/ec2/)
- [Amazon EC2 instance types](https://docs.aws.amazon.com/ko_kr/ec2/latest/instancetypes/)

### Azure

- [Azure Virtual Machines documentation](https://learn.microsoft.com/ko-kr/azure/virtual-machines/)
- [Azure VM sizes](https://learn.microsoft.com/ko-kr/azure/virtual-machines/sizes/)

### Google Cloud

- [Google Compute Engine documentation](https://cloud.google.com/compute/docs)
- [Google Compute Engine machine types](https://cloud.google.com/compute/docs/machine-types)

### OCI

- [OCI Compute documentation](https://docs.oracle.com/en-us/iaas/Content/Compute/home.htm)
- [OCI Compute Shapes](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm)
