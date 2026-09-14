---
title: "GPU Kubernetes and Scheduling"
description: "Covers GPU node pools/device plugins, MIG/time-slicing sharing, ResourceQuota/anti-hoarding, gang scheduling (Kueue/Volcano), and DCGM observability from a vendor-neutral perspective."
---

> Last reviewed: September 2026 | This is a fast-moving area subject to quarterly review.

:::note
This document covers how to schedule, share, and govern GPUs on Kubernetes. General Kubernetes operations such as cluster upgrades and node management are in [Kubernetes Operations](../../devops/kubernetes-operations/); GPU cluster communication and placement are in [GPU Workload Characteristics and Reference Architecture](../../ai/gpu-infra/workload-and-architecture/).
:::

## Overview

GPUs are expensive and scarce. So rather than one team monopolizing them, multiple teams and jobs usually **share one GPU cluster.** What decides "who gets how many GPUs, and when" is the scheduler, and a bad allocation leaves costly GPUs idle or lets one team monopolize them.

Kubernetes (the standard tool for automatically placing and managing containers) treats GPUs as a special resource. The hard part is that one cluster must accept two jobs of opposite nature — a **training job** starts only when it gets "all the GPUs it needs at once," while an **inference job** runs by "holding a few GPUs for a long time."

:::note
If Kubernetes itself is new to you, we recommend reading [Container Services](../../compute/containers/) and [Kubernetes Operations](../../devops/kubernetes-operations/) first. This document covers only the **GPU-specific** parts on top of that.
:::

## GPU Node Pools and Device Plugins

Kubernetes does not recognize GPUs by default, so you install a vendor device plugin along with drivers/operators to expose GPUs as schedulable resources.

- **GPU node pool** — Configure a dedicated GPU node pool separate from general-purpose nodes. (See [Node pool composition](../../compute/containers/#node-pool-composition).)
- **Device plugin / operator** — The [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html), which deploys drivers, device plugin, and DCGM together, is the de facto standard.
- **taint/toleration** — Taint GPU nodes so non-GPU workloads do not occupy expensive GPU nodes.

## GPU Sharing — MIG and Time-Slicing

Letting multiple jobs share a single GPU can raise utilization for small inference/development workloads.

| Method | Isolation level | Suitable workloads | Limitations |
| --- | --- | --- | --- |
| **MIG (Multi-Instance GPU)** | Hardware partition (memory/compute isolation) | Predictable multi-tenant inference | Supported-GPU/profile constraints, dynamic-change overhead |
| **MPS (Multi-Process Service)** | Shared process space (partial isolation) | Cooperative multi-process, small inference | No memory-isolation guarantee, fault propagation possible |
| **Time-slicing** | Time division (no isolation) | Development/experiments, bursty workloads | Interference/OOM risk, no fairness guarantee |

MIG is the strongest via hardware isolation, time-slicing has no isolation, and MPS sits in between with multiple processes sharing one GPU context. All three are common NVIDIA GPU features, not vendor-exclusive.

:::caution
Time-slicing does not isolate memory or compute, so one job's OOM or runaway affects other jobs on the same GPU. For production multi-tenancy, consider MIG (hardware isolation) first. MIG has limited supported GPU generations/profiles, so verify support for the target GPU first.
:::

## Quotas, Fairness, and Anti-Hoarding

The headache of a shared cluster is when **one team grabs GPUs and won't let go (monopoly, hoarding)**. Then other jobs can't get GPUs and keep starving. The mechanisms that prevent this:

- **ResourceQuota (total cap)** — Set an upper bound on the number of GPUs each team (namespace) can use.
- **Priority/preemption** — Rank jobs by priority (PriorityClass), and when an urgent job arrives, briefly push aside (preempt) a less urgent one to yield GPUs.
- **Reclaiming idle GPUs (anti-hoarding)** — A queue-based scheduler uses fair-share and reclaim rules to take back GPUs that are held but not actually used, and give them to other jobs.
- **Queue-based allocation** — The gang-scheduling tier below manages per-team shares and waiting lines.

## Gang Scheduling

Distributed training can only start once it secures **all** the GPUs it needs **at once**. For example, if a job needs 16 GPUs but grabs only 10 and waits for the other 6, those 10 do nothing and just tie up resources (in the worst case, a deadlock where jobs wait on each other). Gang scheduling prevents this by scheduling **"start only if all needed are secured, otherwise don't start at all (all-or-nothing)."** It means grabbing the whole "gang" together.

| Tool | Characteristics |
| --- | --- |
| [Kueue](https://kueue.sigs.k8s.io/) | Kubernetes-native job queuing, quotas/fair-share, hierarchical queues |
| [Volcano](https://volcano.sh/) | Batch scheduler, gang scheduling/queues/preemption integrated, HPC/AI-oriented |

:::note
Kueue and Volcano are both vendor-neutral open source and run on any cloud's Kubernetes. Managed training platforms (SageMaker HyperPod, Vertex AI, etc.) provide similar queuing/gang scheduling built in, so you can use them instead of building your own.
:::

## Vendor Managed Kubernetes GPU Support

| Item | AWS (EKS) | Azure (AKS) | Google Cloud (GKE) | OCI (OKE) |
| --- | --- | --- | --- | --- |
| **GPU node pool** | Managed node groups | GPU node pools | GPU node pools | GPU node pools |
| **Driver installation** | GPU Operator / EKS-optimized AMI | GPU Operator / AKS GPU image | GPU Operator / GKE driver auto-install | GPU Operator / OKE image |
| **GPU sharing** | MIG, MPS, time-slicing | MIG, MPS, time-slicing | MIG, MPS, time-slicing | MIG, MPS, time-slicing |

:::note
GPU sharing, gang scheduling, and operators mostly run at the open-source tier, so concepts are similar across vendors. However, the node-pool provisioning API, driver auto-install method, and supported GPU generations differ per vendor, so verify with each vendor's official documentation.
:::

## Observability — DCGM and GPU Metrics

GPU clusters cannot be diagnosed for bottlenecks with CPU-centric observability alone. Collect GPU utilization, memory, temperature, and network traffic with [NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/index.html) (Data Center GPU Manager, the standard tool for collecting GPU status and performance).

- **Key metrics** — GPU utilization (actual compute utilization, not mere allocation), memory usage, fabric bandwidth, power/temperature
- **The utilization trap** — "A GPU is allocated" and "a GPU is actually computing" are different. Low effective utilization is a sign of a data-loading or communication bottleneck.
- **SLO linkage** — Integrate collected GPU metrics into your [SLO](../../devops/slo/) and [Observability](../../devops/observability/) systems to continuously manage training throughput and inference latency.

## Related Documents

- **General Kubernetes operations (upgrades, node management)** — [Kubernetes Operations](../../devops/kubernetes-operations/)
- **Cluster communication, placement, managed clusters** — [GPU Workload Characteristics and Reference Architecture](../../ai/gpu-infra/workload-and-architecture/)
- **Parallelism strategies (TP/PP/DP)** — [Distributed Training Standard Architecture](../../ai/gpu-infra/distributed-training/)
- **Capacity operations, cost** — [Inference Serving, Reliability, and Cost](../../ai/gpu-infra/serving-reliability-cost/)

## Common Mistakes

- **Submitting distributed training without gang scheduling** — Acquiring only some GPUs and waiting, tying up resources and causing deadlock
- **Using time-slicing for production multi-tenancy** — No isolation, so one job's OOM propagates to others
- **Absence of ResourceQuota/preemption policies** — One team monopolizes (hoards) GPUs, starving other jobs
- **Watching only GPU allocation rate, not utilization** — Missing low effective utilization (data/communication bottlenecks), wasting expensive GPUs

## Checklist

- [ ] Did you taint the dedicated GPU node pool to block non-GPU workload occupancy?
- [ ] Did you consider MIG (hardware isolation) instead of time-slicing for multi-tenant inference?
- [ ] Did you set per-namespace ResourceQuota and PriorityClass/preemption policies?
- [ ] Did you apply gang scheduling (Kueue/Volcano or a managed built-in) to distributed training?
- [ ] Did you collect effective GPU utilization with DCGM and link it to SLOs?

## References

### Common (vendor-neutral)

- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html)
- [NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/index.html)
- [Kueue](https://kueue.sigs.k8s.io/)
- [Volcano](https://volcano.sh/)

### Vendor-specific

- [AWS — EKS GPU workloads](https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html)
- [Azure — AKS GPU node pools](https://learn.microsoft.com/azure/aks/gpu-cluster)
- [Google Cloud — GKE GPUs](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus)
- [OCI — OKE GPU nodes](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengrunninggpunodes.htm)
