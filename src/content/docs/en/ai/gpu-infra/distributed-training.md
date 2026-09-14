---
title: "Distributed Training Standard Architecture"
description: "Summarizes data/tensor/pipeline parallelism (DP/TP/PP), 3D hybrid parallelism, distributed training frameworks, and checkpoint strategy from a vendor-neutral perspective."
---

> Last reviewed: September 2026 | This is a fast-moving area subject to quarterly review.

:::note
This document covers parallelism strategies for distributed training. For the cluster communication tier, placement, and fabric, see [GPU Workload Characteristics and Reference Architecture](../../ai/gpu-infra/workload-and-architecture/); for scheduling on Kubernetes, see [GPU Kubernetes and Scheduling](../../ai/gpu-infra/kubernetes-and-scheduling/).
:::

## Overview

When a model and its data do not fit in a single GPU's memory, training must be split across multiple GPUs. The ways to split are broadly **data parallelism (DP)**, **tensor parallelism (TP)**, and **pipeline parallelism (PP)**; large-scale training combines these into **3D parallelism**. Each approach has different trade-offs in communication volume, memory savings, and implementation complexity.

:::note
The parallelism concepts and frameworks in this document (DeepSpeed, Megatron-LM, PyTorch FSDP) run on top of CUDA/NCCL and are not vendor-bound. Switching clouds generally keeps the parallelism strategy portable. Actual performance depends on [inter-node fabric performance](../../ai/gpu-infra/workload-and-architecture/#inter-node-high-speed-fabric--vendor-mapping).
:::

## Data Parallelism (DP)

Replicate the entire model on each GPU, split the data batch for processing, then synchronize gradients. It is the simplest approach and the standard when the model fits on a single GPU.

- **Communication pattern** — Gradient all-reduce every step (cluster-wide collective)
- **Limitation** — Cannot be used if the model itself exceeds a single GPU's memory
- **Memory optimization (FSDP/ZeRO)** — Shard model parameters, gradients, and optimizer states across GPUs to train larger models beyond single-GPU memory limits while keeping data parallelism

## Tensor Parallelism (TP)

Split the matrix operations of an individual layer across multiple GPUs. Several GPUs compute one layer simultaneously.

- **Communication pattern** — Frequent collective communication within a layer (very latency-sensitive)
- **Applicability** — Because communication is frequent, it is mainly used between GPUs connected by **intra-node NVLink**
- **Effect** — Essential when a single layer exceeds GPU memory

## Pipeline Parallelism (PP)

Divide the model's layers into stages, place them on different GPU groups, and stream micro-batches through the pipeline.

- **Communication pattern** — Passes activations only at stage boundaries (relatively low communication volume)
- **Applicability** — Because communication is low, it is easy to scale **across nodes**
- **Limitation** — Pipeline bubbles (idle periods) occur; mitigate with the number of micro-batches

## 3D Hybrid Parallelism

Large-scale pre-training combines the three approaches hierarchically. Typically **TP intra-node, PP inter-node, and DP on top**.

| Parallelism | Communication volume | Memory savings | Latency sensitivity | Recommended placement |
| --- | --- | --- | --- | --- |
| **Data parallel (DP)** | High (gradient all-reduce) | None (large with FSDP/ZeRO) | Medium | Cluster-wide |
| **Tensor parallel (TP)** | Very high (within a layer) | Large | Very high | Intra-node (NVLink) |
| **Pipeline parallel (PP)** | Low (stage boundaries) | Large | Low | Inter-node |

:::caution
The more parallelism dimensions you add, the more sharply implementation and debugging complexity rise. If the model fits on a single node (e.g., 8x GPU), FSDP/ZeRO-based data parallelism alone is often sufficient without 3D parallelism. Extending latency-sensitive TP across nodes can cause throughput to collapse depending on fabric performance.
:::

## Distributed Training Frameworks

| Framework | Main parallelism | Characteristics |
| --- | --- | --- |
| [PyTorch FSDP](https://docs.pytorch.org/docs/stable/fsdp.html) | DP (sharding) | PyTorch-native, distributes parameters/optimizer states |
| [DeepSpeed](https://www.deepspeed.ai/) | DP(ZeRO) + PP + TP | ZeRO staged memory optimization, offloading support |
| [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) | TP + PP + DP | TP implementation optimized for large-scale Transformer pre-training |

:::note
Framework choice is vendor-neutral. However, each cloud's managed training platform (SageMaker, Vertex AI, Azure ML, etc.) provides distributed-training libraries/recipes with these frameworks pre-integrated; using them automates communication setup and topology optimization at the cost of lock-in to that platform.
:::

## Checkpoint Strategy

Large-scale training runs for hours to weeks, so checkpointing to withstand node failures is essential. Checkpoint design is a matter of **balancing save frequency against storage bandwidth**.

- **Frequency** — Too frequent, and save overhead leaves GPUs idle; too infrequent, and the compute lost on failure grows.
- **Storage bandwidth** — Writing hundreds of GB to several TB of checkpoints in a short time makes [storage-tier](../../ai/gpu-infra/workload-and-architecture/#reference-architecture--three-tier-communication-model) throughput a bottleneck.
- **Asynchronous/distributed saving** — Save in the background without stopping training, or have each GPU save only its own shard in parallel to cut time.
- **Automatic resume** — The flow of resuming from the last checkpoint after failure detection is covered in [Inference Serving, Reliability, and Cost — Reliability and Failure Handling](../../ai/gpu-infra/serving-reliability-cost/#reliability-and-failure-handling).

## Related Documents

- **Cluster communication tier, fabric, placement** — [GPU Workload Characteristics and Reference Architecture](../../ai/gpu-infra/workload-and-architecture/)
- **Gang scheduling, quotas** — [GPU Kubernetes and Scheduling](../../ai/gpu-infra/kubernetes-and-scheduling/)
- **Automatic failure resume, capacity operations** — [Inference Serving, Reliability, and Cost](../../ai/gpu-infra/serving-reliability-cost/)
- **Training pipeline within the AI system lifecycle** — [AI System Lifecycle and Engineering](../../ai/lifecycle/)

## Common Mistakes

- **Introducing unnecessary 3D parallelism** — Adding tensor/pipeline parallelism to a model well served by a single node, increasing only complexity and debugging cost
- **Extending tensor parallelism across nodes** — Widening latency-sensitive TP beyond NVLink, creating a communication bottleneck
- **Only raising checkpoint frequency** — Not scaling storage bandwidth accordingly, increasing GPU idle time during saves
- **Overlooking optimizer-state memory** — Not accounting for the memory taken by optimizer states/gradients beyond parameters, causing OOM

## Checklist

- [ ] Did you calculate whether the model and optimizer states fit in single-GPU/single-node memory?
- [ ] If a single node suffices, did you first consider FSDP/ZeRO data parallelism?
- [ ] Did you limit tensor parallelism to intra-node (NVLink) and place pipeline parallelism across nodes?
- [ ] Did you design checkpoint frequency together with storage bandwidth?
- [ ] Did you verify the automatic-resume flow on failure?

## References

### Common (vendor-neutral)

- [PyTorch FSDP](https://docs.pytorch.org/docs/stable/fsdp.html)
- [DeepSpeed](https://www.deepspeed.ai/)
- [NVIDIA Megatron-LM](https://github.com/NVIDIA/Megatron-LM)
- [NVIDIA NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)

### Vendor-specific distributed training

- [AWS — SageMaker distributed training](https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training.html)
- [Azure — Azure ML distributed training](https://learn.microsoft.com/azure/machine-learning/concept-distributed-training)
- [Google Cloud — Vertex AI distributed training](https://cloud.google.com/vertex-ai/docs/training/distributed-training)
- [OCI — Data Science distributed training](https://docs.oracle.com/en-us/iaas/Content/data-science/using/jobs-distributed-jobs.htm)
