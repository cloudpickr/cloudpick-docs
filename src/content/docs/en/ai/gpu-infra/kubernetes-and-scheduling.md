---
title: "GPU Kubernetes and Scheduling"
description: "Covers GPU node pools/device plugins, MIG/time-slicing sharing, ResourceQuota/anti-hoarding, gang scheduling (Kueue/Volcano), and DCGM observability from a vendor-neutral perspective."
---

> Last reviewed: September 2026 | This is a fast-moving area subject to quarterly review.

:::note
This document covers how to schedule, share, and govern GPUs on Kubernetes. General Kubernetes operations such as cluster upgrades and node management are in [Kubernetes Operations](../../devops/kubernetes-operations/); GPU cluster communication and placement are in [GPU Workload Characteristics and Reference Architecture](../../ai/gpu-infra/workload-and-architecture/).
:::

## Overview

When multiple teams and multiple jobs share one GPU cluster, how the scheduler allocates GPUs determines utilization and fairness. Kubernetes treats GPUs as extended resources and must accommodate the opposing demands of training jobs (needing many GPUs all-or-nothing) and inference jobs (continuously holding a small number of GPUs).

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

The core problem of a shared cluster is **one team hoarding GPUs** and starving other jobs.

- **ResourceQuota** — Set an upper bound on GPUs available per namespace (team) to control totals.
- **Priority/preemption** — Set job priority with PriorityClass and preempt lower-priority jobs to yield GPUs to higher-priority ones.
- **Anti-hoarding** — Apply fair-share/reclaim policies of a queue-based scheduler to reclaim GPUs held idle but unused.
- **Queue-based allocation** — Manage per-team allotments and waiting queues at the gang-scheduling tier below.

## Gang Scheduling

Distributed training can only start once it acquires **all** the GPUs it needs at the same time. Acquiring only some while waiting for the rest ties up the acquired GPUs idle, wasting resources and risking deadlock. Gang scheduling schedules jobs all-or-nothing.

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

GPU clusters cannot be diagnosed for bottlenecks with CPU-centric observability alone. Collect GPU utilization, memory, temperature, and NVLink/fabric traffic with [NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/index.html).

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
- [OCI — OKE GPU nodes](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengusinggpus.htm)
