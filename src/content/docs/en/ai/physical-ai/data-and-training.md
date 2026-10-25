---
title: "Physical AI Data and Training"
description: "Compares edge inference and IoT hardware and the sensor data pipeline (Layer 1), digital twins, simulation, open datasets, and sim-to-real (Layer 2), and choosing training infrastructure matched to scale, from a vendor-neutral perspective."
---

> Last reviewed: September 2026 | This area changes quickly and is subject to quarterly review.

## Overview

This document covers the front end of the Physical AI pipeline — **from data entering the physical world to becoming a training asset**. For an overview of the full pipeline see [Physical AI Overview](../overview/); for the back end that deploys and operates trained models see [Deploy and Operate](../deploy-and-operate/).

## Layer 1 — Edge Inference and IoT

Data from the physical world is high-volume and real-time, making it impractical to send everything to the cloud. The baseline structure is to infer first on site (at the edge) and upload only what is needed to the cloud.

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| Edge runtime | [IoT Greengrass](https://docs.aws.amazon.com/greengrass/v2/developerguide/) | [Azure IoT Operations](https://learn.microsoft.com/azure/iot-operations/) / [IoT Edge](https://learn.microsoft.com/azure/iot-edge/) | [Google Distributed Cloud (Edge)](https://cloud.google.com/distributed-cloud) | [Roving Edge Infrastructure](https://docs.oracle.com/en-us/iaas/Content/Rover/overview.htm) |
| Edge ML inference | Greengrass ML components (SageMaker AI model deployment) | IoT Edge modules + Azure AI services | Edge TPU / Coral (verify current support status) | Build your own on RED compute |
| Industrial data ingestion | [IoT SiteWise](https://aws.amazon.com/iot-sitewise/) (OPC UA) | IoT Operations (OPC UA) | — (partner or self-built) | — (self-built) |

:::caution
**Azure Percept was retired in March 2023.** Even if older material presents Percept as edge AI hardware, comparable capability is now assembled from Azure IoT Edge / IoT Operations plus Azure Certified Device partner hardware (Microsoft did not designate a single official successor product). Do not build architecture assumptions on obsolete product names.
:::

### Edge Inference Hardware

If the edge runtime is the software layer, the choice of **accelerator hardware** beneath it determines feasibility and TCO. There are four criteria — the **compute performance** to run the target model, the **memory capacity** the model must fit into, the robot's **power and thermal budget**, and the **lifespan of the software ecosystem**.

| Family | Characteristics | Considerations |
| --- | --- | --- |
| Robotics-oriented edge modules (for example the [NVIDIA Jetson](https://developer.nvidia.com/embedded/jetson-modules) family) | Spans low-power compact modules to high-performance ones, and is a frequently considered option for on-device robotics VLA inference | Performance and memory differ greatly across generations and modules, with wide price spreads. Confirm first that the target model fits in that module's memory |
| General-purpose CPUs with integrated NPUs and small accelerators | Sufficient for lightweight vision such as classification and detection, with low power and unit cost | Often short on memory and bandwidth for large multimodal and VLA inference |
| FPGAs and industrial SoCs | Favorable for equipment where deterministic latency and long-term supply guarantees matter | High development difficulty and significant model porting cost |
| Cloud provider edge appliances | Extend cloud operational tooling and management to the field | Intended as field servers and gateways; they do not replace real-time control onboard the robot |

:::caution
**Do not compare on TOPS figures alone.** Vendor-quoted compute performance uses different baselines depending on precision (INT8, FP4, and so on) and whether sparsity is applied, so placing numbers from different conditions side by side is not a valid comparison. Actual inference speed is often governed by memory capacity and bandwidth and by how well the model fits, so **measuring the target model on the target module** is the reliable approach.
:::

:::caution
For edge accelerators, the **lifespan of the software ecosystem** matters as much as hardware lifespan. A product whose driver and runtime updates have stopped cannot support new kernels or new model formats, creating early replacement pressure. [Google Edge TPU / Coral](https://developers.google.com/coral/guides/faq) in the Layer 1 table above is one example: with no official product EOL notice, its [legacy API repository is archived and marked as no longer maintained](https://github.com/google-coral/edgetpu). The similarly named **Coral NPU is a separate thing — an open source NPU IP for silicon partners** — and is not the official successor to the Edge TPU module family, so do not read it as a continuation of the same product. **Verify current support status and driver update history directly** before placing such families in a new design. Prices are not fixed either and have been adjusted around generational transitions, so validate large-scale deployment plans with a fresh quote.
:::

### Sensor Data Pipeline — Ingestion, Storage, Labeling

Data arriving from the edge cannot be used for training as-is. Physical AI data is **multimodal — 1D time series (joint angles, current, temperature), 2D video, 3D point clouds, and equipment metadata mixed together** — so it must pass through ingestion, storage, and refinement/labeling before entering the training pipeline.

| Stage | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| Stream and video ingestion | [IoT Core](https://aws.amazon.com/iot-core/) (edge ingress) / [Kinesis Video Streams](https://aws.amazon.com/kinesis/video-streams/) and [Data Streams](https://aws.amazon.com/kinesis/data-streams/) (downstream landing) | [Event Hubs](https://learn.microsoft.com/azure/event-hubs/) + IoT Operations | [Pub/Sub](https://cloud.google.com/pubsub) | [OCI Streaming](https://www.oracle.com/cloud/streaming/) |
| Data lake | [S3](https://aws.amazon.com/s3/) | [Data Lake Storage](https://learn.microsoft.com/azure/storage/blobs/data-lake-storage-introduction) | [Cloud Storage](https://cloud.google.com/storage) | [Object Storage](https://www.oracle.com/cloud/storage/object-storage/) |
| Parallel file system for training | [FSx for Lustre](https://aws.amazon.com/fsx/lustre/) | [Azure Managed Lustre](https://azure.microsoft.com/products/managed-lustre) | [Managed Lustre](https://cloud.google.com/products/managed-lustre) / [Parallelstore](https://cloud.google.com/parallelstore) | [File Storage with Lustre](https://www.oracle.com/cloud/storage/file-storage-with-lustre/) |
| Labeling | [SageMaker Ground Truth](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html) (closed to new customers) | [Azure ML data labeling](https://learn.microsoft.com/azure/machine-learning/how-to-label-data) | — (managed service ended; partner or open source) | [OCI Data Labeling](https://www.oracle.com/artificial-intelligence/data-labeling/) |

:::caution
**Managed labeling services are shrinking rather than growing.** Google Cloud's Vertex AI data labeling was [shut down on October 3, 2024](https://cloud.google.com/vertex-ai/docs/deprecations), and AWS SageMaker Ground Truth stopped accepting new customers on July 30, 2026 (existing customers may continue to use it, with no new features planned). Ground Truth Plus reached end of support on June 30, 2026. Do not tie labeling to a single cloud's managed service; make a structure **replaceable by open source or partner tooling** your default.
:::

:::note
In GPU training, the bottleneck is often not computation but **data loading and checkpoint writes**. Reading directly from object storage leaves GPUs idle, so it is common to place a parallel file system in front of object storage for the training phase. For a general storage-tier comparison see [Block and File Storage](../../../storage/block-and-file/), and for checkpoint strategy see [Distributed Training](../../gpu-infra/distributed-training/).
:::

## Layer 2 — Digital Twins and Simulation

Training robots and vehicles only in the real world is costly, risky, and slow. This is why the sim-to-real approach took hold: generate and train on large volumes of scenarios in a **digital twin** and **simulation** that virtually replicate the physical environment, then transfer to reality.

| Item | AWS | Azure | Google Cloud | OCI | Cross-vendor |
| --- | --- | --- | --- | --- | --- |
| Digital twin | [IoT TwinMaker](https://aws.amazon.com/iot-twinmaker/) | [Azure Digital Twins](https://learn.microsoft.com/azure/digital-twins/) | — (self-built with Spanner Graph, BigQuery, etc.) | — | [NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/) |
| Robot and physics simulation | — (RoboMaker end of support; self-built) | — (partner or self-built) | — (partner or self-built) | — | [NVIDIA Isaac Sim / Isaac Lab](https://developer.nvidia.com/isaac/sim) |

:::caution
**AWS RoboMaker reached end of support on September 10, 2025.** Robot simulation on AWS is now assembled directly from GPU instances plus open source (Isaac Sim, Gazebo, and so on) with no dedicated managed service. Be careful not to place EOL services into new designs.
:::

:::note
In the digital twin and robot simulation layer, **the NVIDIA Omniverse and Isaac ecosystem is widely used.** The major clouds all support running this stack on GPU instances, and rather than depending on one cloud's proprietary managed product, checking **whether the stack can be moved and run on any cloud (portability)** first is the way to reduce lock-in.
:::

### Why Training Data Is Scarce

Simulation is a premise rather than an option because of **data scarcity**. Language models started from effectively unlimited pre-training data in the form of internet text, but data of "a robot actually picking up and moving an object" is orders of magnitude smaller. Physical AI training starts from a design that fills the gap with cheaper, more plentiful data.

| Data tier | Characteristics | Limitation |
| --- | --- | --- |
| Internet video, images, text | Effectively unlimited and cheap. Provides general knowledge about the world and objects | Not directly connected to a robot's body or joint commands |
| Human task video (egocentric) | Relatively plentiful. Provides hints about motion sequence and intent | Framed around a human body, so it does not transfer directly to a robot embodiment |
| Robot teleop episodes | Most accurate, containing actual joint commands | A human must directly operate the robot to produce it, making collection the most expensive |

**Teleoperation** is the practice of a person moving a robot directly with a controller or VR rig to produce demonstration data, and **imitation learning** trains a model to reproduce that data. It is the most reliable method, but human time is the cost, which makes it hard to scale.

:::note
For cloud cost estimation, this structure means **a cost axis exists separately from GPUs**. Data collection (equipment and labor), storage and transfer, and labeling costs arise independently of training compute, so estimating TCO from GPU hours alone will be far off.
:::

### Open Datasets and Benchmark Ecosystem

Because data scarcity is hard for any single organization to overcome alone, an open ecosystem has formed in which multiple institutions pool data and share evaluation tasks. When choosing a stack, **"which open assets can be used as-is on this stack"** becomes a practical criterion for judging lock-in.

| Category | Representative assets | What it is used for |
| --- | --- | --- |
| Cross-robot datasets | [Open X-Embodiment](https://github.com/google-deepmind/open_x_embodiment) ([paper](https://arxiv.org/abs/2310.08864)) | A collection consolidating robot data from many institutions. The baseline for cross-embodiment pre-training |
| Large manipulation datasets | [DROID](https://github.com/droid-dataset/droid) | Teleop data collected across diverse environments |
| Simulation benchmarks | [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO), [CALVIN](https://github.com/mees/calvin), [RoboCasa](https://github.com/robocasa/robocasa), [Meta-World](https://github.com/Farama-Foundation/Metaworld) | Compare policies by task success rate on standard task suites |
| Human task video | [Ego4D](https://ego4d-data.org/) | Egocentric task video. Corresponds to the middle tier of the three data tiers above |
| Open toolchains | [LeRobot](https://github.com/huggingface/lerobot) | An open source stack bundling data format, training, and evaluation |

:::caution
Open datasets have **licensing terms that differ per asset.** Some permit research use only or require attribution or disclosure of derivatives, so before using them as training assets in a commercial product, check each dataset's license together with the terms of its subcomponents (the parts contributed by individual institutions). For example, Open X-Embodiment is not under a single license — **terms differ per constituent dataset** — and Ego4D can carry separate terms for commercial use.
:::

:::note
Using a model pre-trained on open datasets can reduce the volume of initial data collection, but the real benefit depends on **whether your robot's embodiment and target task are represented in that data**. The same applies to benchmark scores: if measurement conditions differ, they are not comparable (see [What Determines Whether a Model Passes](../deploy-and-operate/#what-determines-whether-a-model-passes)).
:::

### Sim-to-Real Gap

The value of simulation is clear, but **a simulator's physics, sensor, and material models differ subtly from reality.** Differences in friction coefficients, lighting, sensor noise, and mechanical play accumulate, producing the phenomenon where a policy that succeeded in simulation fails on the real robot. This is the **sim-to-real gap**.

Three mitigations are common.

- **Domain randomization** — Randomly vary physical parameters such as friction, mass, lighting, and texture during training so that reality falls inside that distribution.
- **Small-scale fine-tuning on real data** — Finish a simulation-pretrained policy with a small amount of data from the actual robot.
- **Physical validation gate** — Use success rates on real equipment as the deployment criterion, separately from simulation success rates.

:::caution
**Do not use simulation success rates directly as deployment evidence.** Simulation metrics are useful for detecting regressions but do not guarantee real-world performance. When choosing a simulator, look not only at rendering quality but also at **physical fidelity in the target domain** (contact, friction, deformation, and so on).
:::

## Matching Training Infrastructure to Scale

A common misconception in Physical AI is that "training robot models always requires a large GPU cluster." In practice, most work is **fine-tuning a pre-trained robot foundation model to your own robots and tasks**, and this phase is nothing like LLM pre-training in scale. Small-scale PEFT and adapter training often completes as a short job on a single GPU.

| Stage | Nature of the work | Infrastructure pattern | Cost strategy |
| --- | --- | --- | --- |
| Initial validation | Small demonstration dataset, LoRA/PEFT adapter training | A single GPU instance | Spot/preemptible instances as the default. Interruption costs little to restart |
| Task specialization | Medium demonstration dataset, full fine-tuning | Single node, multiple GPUs plus a managed training job | A managed training service with automatic checkpoint and resume |
| Platformization | Many robots and tasks, repeated retraining | Multiple nodes plus a high-speed interconnect | Reserved or committed discounts. Requires automatic node recovery (see [Distributed Training](../../gpu-infra/distributed-training/)) |

:::note
The practical implication of this ladder is **do not make large commitments at the first stage**. The initial and task-specialization phases are often well served by spot/preemptible instances and pay-as-you-go, and reservations or commitments can wait until the retraining cadence becomes routine. Conversely, simulation occupies GPUs longer as you increase the number of parallel environments, so simulation frequently dominates cost over training. For vendor mapping of GPU instance families and interconnects, see [GPU Workloads and Architecture](../../gpu-infra/workload-and-architecture/).
:::

## Common Mistakes

- **Sending all data to the cloud** — A design that ignores latency, bandwidth, and cost fails at real-time control. Dividing inference to the edge comes first.
- **Using EOL products in new designs** — Do not adopt services that have ended or curtailed support — RoboMaker, Percept, managed labeling services — based only on older material.
- **Locking into a single vendor's simulator** — Tying the training pipeline to one cloud's proprietary simulation makes porting and comparison difficult.
- **Estimating TCO from GPU cost alone** — Data collection, storage, and labeling, plus simulation occupancy cost, arise separately from training compute.
- **Using simulation success rates as deployment evidence** — Deploying without a physical rollout validation gate lets the sim-to-real gap surface in the field.

## Checklist

### Data and Cost

- [ ] Have you designed the storage, refinement, and labeling layer for sensor data, and confirmed that labeling tooling is replaceable?
- [ ] Have you estimated data collection, storage, labeling, and simulation costs separately from GPU cost?
- [ ] Have you checked the licenses of the open datasets and benchmarks you plan to use, and whether they cover your own embodiment?

### Hardware and Training

- [ ] Did you select the edge accelerator by measuring the target model rather than by TOPS figures, and confirm the support lifespan of its drivers and runtime?
- [ ] Have you chosen an infrastructure stage matched to your training scale (without over-committing during initial validation)?
- [ ] Is the digital twin and simulation stack portable to another cloud (lock-in check)?
- [ ] Are the IoT and robotics services you plan to use currently supported (EOL check)?

## Related Documents

- [Physical AI Overview](../overview/) — Full pipeline, layered structure, and open problems
- [Deploy and Operate](../deploy-and-operate/) — Robotics foundation models, safety, architecture, fleet deployment
- [Block and File Storage](../../../storage/block-and-file/) — Parallel file system comparison
- [GPU Infrastructure](../../gpu-infra/workload-and-architecture/) — GPU clusters for cloud training and simulation
- [Distributed Training](../../gpu-infra/distributed-training/) — Multi-node training and checkpoint strategy

## Further Reading

### AWS

- [AWS IoT Greengrass Developer Guide](https://docs.aws.amazon.com/greengrass/v2/developerguide/)
- [AWS IoT TwinMaker](https://aws.amazon.com/iot-twinmaker/)
- [AWS IoT SiteWise](https://aws.amazon.com/iot-sitewise/)
- [Amazon FSx for Lustre](https://aws.amazon.com/fsx/lustre/)
- [Amazon SageMaker Ground Truth documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html)

### Azure

- [Azure IoT Operations documentation](https://learn.microsoft.com/azure/iot-operations/)
- [Azure Digital Twins documentation](https://learn.microsoft.com/azure/digital-twins/)
- [Azure Managed Lustre](https://azure.microsoft.com/products/managed-lustre)
- [Azure Machine Learning data labeling](https://learn.microsoft.com/azure/machine-learning/how-to-label-data)

### Google Cloud

- [Google Distributed Cloud](https://cloud.google.com/distributed-cloud)
- [Coral / Edge TPU](https://cloud.google.com/edge-tpu)
- [Google Cloud Managed Lustre](https://cloud.google.com/products/managed-lustre)
- [Google Cloud Parallelstore](https://cloud.google.com/parallelstore)

### OCI

- [Oracle Roving Edge Infrastructure](https://docs.oracle.com/en-us/iaas/Content/Rover/overview.htm)
- [OCI File Storage with Lustre](https://www.oracle.com/cloud/storage/file-storage-with-lustre/)
- [OCI Data Labeling](https://www.oracle.com/artificial-intelligence/data-labeling/)

### Open Datasets and Toolchains

- [Open X-Embodiment (repository)](https://github.com/google-deepmind/open_x_embodiment) · [paper](https://arxiv.org/abs/2310.08864)
- [LeRobot (open source robotics toolchain)](https://github.com/huggingface/lerobot)
- [Ego4D](https://ego4d-data.org/)
