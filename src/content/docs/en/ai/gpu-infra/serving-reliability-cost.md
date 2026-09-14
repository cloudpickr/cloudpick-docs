---
title: "Inference Serving, Reliability, and Cost"
description: "Covers GPU inference serving operations, automatic node-failure resume, capacity operations (Capacity Blocks/reservations/multi-region fallback), and GPU cost optimization from a vendor-neutral perspective."
---

> Last reviewed: September 2026 | This is a fast-moving area subject to quarterly review.

:::note
This document covers the operational stage of GPU infrastructure (inference serving, failure handling, capacity, cost). For training parallelism, see [Distributed Training Standard Architecture](../distributed-training/); for cluster architecture, see [GPU Workload Characteristics and Reference Architecture](../workload-and-architecture/).
:::

## Overview

For GPU infrastructure, cost and reliability are decided in the operational stage after you build it. This document covers inference serving (latency, autoscaling), failure recovery (checkpoints, node re-insertion), and GPU capacity assurance and cost optimization (commitments, spot, capacity reservations). In particular, as of 2026 the biggest constraint is not performance but **whether you can actually secure GPUs when you want them**.

Inference and training differ in nature. Training is a long, large, one-shot job, whereas inference must **respond quickly** whenever a user request arrives and **scale up and down automatically** with request volume.

## Inference Serving

Inference has an operational profile opposite to training. Training is long-running, communication-heavy, and batch-oriented, whereas inference is **latency-sensitive, request-based, and autoscaling-oriented**.

- **Latency vs throughput** — Real-time serving targets low latency (fast response); batch inference targets high throughput (many at once). Balance the two with dynamic batching (gathering requests that arrive within a short window and processing them together).
- **Autoscaling** — Increase and decrease GPU replicas with request volume. But GPUs have a long time to load model weights into memory when starting up (cold start), so they react more slowly than CPUs. Keep at least a few always on, or pre-warm them.
- **Model-parallel serving** — Large models that do not fit on a single GPU use tensor parallelism even for inference. (See [parallelism strategies](../distributed-training/).)
- **Per-token cost and routing** — Token cost, prompt caching, and model routing for foundation-model APIs are covered in [LLMOps](../../../ai/llmops/) and [AI Platforms and Model Comparison — Inference Cost Optimization](../../../ai/ai-ml/#inference-cost-optimization).

## Reliability and Failure Handling

The more nodes, the higher the chance of hardware failure during training. At scales of hundreds of GPUs, failure is routine, not an exception. So plan on the premise that "failures will happen."

- **Failure detection** — Find and isolate faulty nodes quickly with node health checks and GPU error signals (Xid errors = GPU error codes reported by the NVIDIA driver, memory errors, communication link drops).
- **Resume from checkpoint** — Restart from the last saved point ([checkpoint](../distributed-training/#checkpoint-strategy)). Replace the failed node while the rest wait briefly and then re-sync.
- **Straggler handling** — If even one node slows down (network trouble or heat-induced slowdown), the whole job waits on it and slows together. Detect such stragglers and isolate/replace them.
- **Managed cluster auto-recovery** — [Managed GPU clusters](../workload-and-architecture/#managed-gpu-clusters) (e.g., SageMaker HyperPod) provide failure detection, auto-replacement, and checkpoint resume as a package to ease this burden.

## Capacity Operations

As of 2026, the latest-generation GPUs often are **not immediately available on demand**. Securing capacity is a first-class constraint of infrastructure design.

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Capacity reservation** | [Capacity Blocks for ML](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html), On-Demand Capacity Reservations | On-Demand Capacity Reservations | [Future Reservations](https://cloud.google.com/compute/docs/instances/reservations-overview), Calendar mode | Capacity Reservation |
| **Committed discounts** | Savings Plans, Reserved Instances | Reserved VM Instances | CUD (Committed Use Discount) | Universal Credits, commitments |
| **Preemptible** | Spot Instances | Spot VMs | Spot VMs | Preemptible Instances |

- **Capacity blocks/reservation queues** — Reserve GPU capacity for a specific period in advance. Large-scale training presupposes securing capacity before start.
- **Regional scarcity** — The latest GPUs exist only in a few regions with limited quantities. Verify actual availability of the desired region/generation in advance.
- **Multi-region/multicloud fallback** — Prepare alternative regions/generations as fallback against single-region capacity shortfalls. Consider data location and egress cost together.

:::caution
The newer the GPU generation, the more limited its regional availability and the greater the competition for commitments. "The instance type exists in the docs" and "you can secure the desired quantity in the desired region right now" are entirely different matters. Verify and reserve capacity early in design.
:::

:::note
The columns above are different in nature. **Capacity reservation** (Capacity Blocks, Future Reservations, etc.) is a mechanism to "secure quantity," whereas **committed discounts** (Savings Plans, CUD, RI, etc.) are financial commitments to "lower price." The two generally do not stack, so design capacity reservation and cost reduction separately. Also note that OCI Universal Credits is an account-level spend commitment, not a GPU-capacity discount.
:::

## Cost Optimization

GPUs are the most expensive resource in the cloud, so utilization and purchasing method govern cost.

- **Purchasing mix** — Allocate steady workloads to committed discounts (Savings Plans/CUD/RI), training/batch to preemptible (Spot), and predictable large-scale training to capacity reservations.
- **Preemptible + checkpoint** — Preemptible can be cheaper by tens of percent but may be interrupted, so combine it with [checkpoints](../distributed-training/#checkpoint-strategy) to resume on interruption.
- **Right-sizing** — Do not use an excessive GPU generation for the workload. Inference/fine-tuning often does not need the top generation.
- **Idle reclamation** — Reduce waste with [GPU sharing (MIG/time-slicing)](../kubernetes-and-scheduling/#gpu-sharing--mig-and-time-slicing) and idle-node scale-down.
- **GPU-hour FinOps** — A system to allocate/track GPU per-hour cost and utilization per team is covered in [FinOps](../../../governance/finops/), and model licenses/usage fees in [AI Licensing](../../../ai/licensing/).

## Related Documents

This is the final part (Part 4) of the GPU infrastructure series. The series starts at [GPU Workload Characteristics and Reference Architecture](../workload-and-architecture/).

- **Cluster architecture, managed clusters** — [GPU Workload Characteristics and Reference Architecture](../workload-and-architecture/)
- **Parallelism, checkpoints** — [Distributed Training Standard Architecture](../distributed-training/)
- **Scheduling, GPU sharing, observability** — [GPU Kubernetes and Scheduling](../kubernetes-and-scheduling/)
- **Cost allocation, budgets** — [FinOps](../../../governance/finops/)
- **Token/prompt cost** — [LLMOps](../../../ai/llmops/)

## Common Mistakes

- **Checking capacity last in design** — The desired region/generation GPU is unavailable, delaying the project schedule
- **Using the same configuration for inference as training** — Ignoring latency/autoscaling needs and applying a large-scale training configuration as-is, wasting cost
- **Using preemptible for training without checkpoints** — Losing all progress on interruption
- **Steady on-demand without utilization monitoring** — Keeping idle GPUs on on-demand, accumulating cost

## Checklist

- [ ] Did you apply dynamic batching, autoscaling, and cold-start mitigation to inference serving?
- [ ] Did you configure failure detection and checkpoint-based automatic resume for large-scale training?
- [ ] Did you verify and reserve GPU capacity for the desired region/generation in advance?
- [ ] Did you review a multi-region/fallback strategy together with data location and egress?
- [ ] Did you combine commitments/preemptible/capacity reservations to fit workload characteristics?
- [ ] Did you track GPU utilization per team and link it to FinOps?

## References

### AWS

- [EC2 Capacity Blocks for ML](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html)
- [Spot Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html)

### Azure

- [On-Demand Capacity Reservations](https://learn.microsoft.com/azure/virtual-machines/capacity-reservation-overview)
- [Azure Spot Virtual Machines](https://learn.microsoft.com/azure/virtual-machines/spot-vms)

### Google Cloud

- [Compute reservations](https://cloud.google.com/compute/docs/instances/reservations-overview)
- [Spot VMs](https://cloud.google.com/compute/docs/instances/spot)

### OCI

- [Capacity Reservation](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/reserve-capacity.htm)
- [Preemptible Instances](https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/preemptible.htm)
