---
title: "Physical AI Deploy and Operate"
description: "Summarizes robotics foundation models and agent connectivity (Layer 3), the functional safety layer, multicloud and edge architecture, and closed-loop operations and fleet deployment from a vendor-neutral perspective."
---

> Last reviewed: September 2026 | This area changes quickly and is subject to quarterly review.

## Overview

This document covers the back end of the Physical AI pipeline — **from deploying a trained model into the physical world to operating it safely**. For an overview of the full pipeline see [Physical AI Overview](./overview/); for the data and training layers see [Data and Training](./data-and-training/).

## Layer 3 — Robotics Foundation Models

### Basic Terms — Policy and Embodiment

The function that decides "what to do in this situation" is called a **policy**. Taking an **observation** — camera images, range sensors, joint angles — as input and producing an **action** — joint commands, motion commands — as output is the smallest unit of robot intelligence. Every model discussed below is a question of how to construct that policy.

Robot bodies differ. A manipulator arm, a quadruped, a humanoid, and an autonomous mobile robot (AMR) all differ in degrees of freedom and control method, and these different bodies are called **embodiments**. Transferring a policy learned on one body to another — **cross-embodiment transfer** — is a well-known unsolved problem in the field.

:::note
From a procurement perspective, embodiment is **a variable that determines model reusability**. Even for the same task, changing robot models may make accumulated data and trained policies unusable as-is, so hardware selection should account for "what assets get tied to this body."
:::

Just as LLMs generalized language, **robot foundation models** that aim to generalize robot perception, planning, and motion are emerging. The representative approach is VLA (Vision-Language-Action), which takes natural language instructions and connects vision, language, and action.

| Item | Status |
| --- | --- |
| Representative stack | [NVIDIA Isaac GR00T](https://developer.nvidia.com/isaac/gr00t) — an open foundation model (VLA) for robots, with Omniverse/Cosmos-based simulation and synthetic data, and Jetson Thor on-device inference |
| Major clouds | Their own general-purpose robot foundation models remain limited — they generally run the NVIDIA stack on GPU infrastructure or offer it through partnerships |
| National policy | Japan adopted robotics foundation model development as a national project under GENIAC (see [Japan AI Landscape](../../../japan/ai-landscape/)) |

### Connecting the Physical World and Agents

If a robot foundation model handles perception, planning, and motion, the agent is the autonomous execution layer above it that **takes a goal, plans steps on its own, and calls tools, sensors, and actuators to execute them**. In Physical AI, unlike digital agents, **actions take effect immediately in the physical world**, so the connection method and permission boundaries are directly tied to safety.

- **Edge agent vs. cloud orchestration** — It is common to divide responsibility so that real-time judgment and control loops run autonomously on site (at the edge), while long-horizon planning, multi-robot coordination, and model updates are handled in the cloud. Even if the network is severed, the edge agent must be able to continue operating safely or stop safely.
- **Tool and actuator connectivity (MCP and similar)** — For an agent to read sensor values and issue higher-level tasks, a standardized connection layer is needed. However, a protocol such as MCP is a **high-level task instruction and tool-call layer**; real-time actuator control (motors, joints, and so on) is handled by a **separate deterministic low-level control layer** (fieldbus, robot middleware, and so on) with guaranteed latency and safety. The two must not be conflated. For general concepts of autonomous execution and tool calling, see [AI Agents](../../../ai/agents/); for agent-tool integration protocols, see [AI Agent Integration (MCP)](../../../mcp/).

#### Why the Layers Are Separated — Control Frequency Mismatch

This separation is not a design preference but a consequence of **physically different operating frequencies**. The low-level control loop holding motors and joints must run deterministically at sub-millisecond periods, while inference by a large multimodal model is far slower with much greater latency variance. The common structure therefore splits into two layers.

- **Slow layer (understanding and planning)** — Understands the scene and sets the next goal. It can be heavy and run at a slow period. It may even sit in the cloud.
- **Fast layer (execution and control)** — Converts a given goal into actual joint trajectories and executes them at a fixed period. It must be on site, and its latency must not fluctuate.

:::caution
Designs that place a large model directly inside the control loop are a common failure cause. Putting the model on-device makes it hard to meet real-time periods, while moving it to the cloud turns network latency and disconnection into control-quality problems. **Define which decisions must complete within how many milliseconds first**, then decide placement.
:::

#### Agent-to-Hardware Connection Standards

After MCP established itself as the standard connecting agents to data and software tools, **standards connecting agents to physical equipment** have begun to appear as well. In August 2026 Anthropic published a research preview of the **[Model Hardware Standard (MHS)](https://www.anthropic.com/news/model-hardware-standard-research-preview)**. Instead of building a custom adapter per device, it exposes devices through a common driver so that a single agent can operate multiple devices in parallel. Safety limits are **enforced at the driver level**, below the agent, so a model cannot talk its way past a hard limit.

:::caution
As of September 2026, MHS is a **research preview**, and its scope centers on scientific research instruments and advanced manufacturing equipment. It does not replace existing standards for industrial robot control (fieldbus, safety PLC, robot middleware), and it is separate from functional safety certification regimes. Rather than treating it as an architectural premise, read it as a signal that **the agent-to-hardware connection layer is moving toward standardization**.
:::

:::caution
When allowing an agent to call physical actuators (motors, valves, vehicle controls, and so on) directly, **explicitly restrict the permission scope (action space)** and require human approval and prior validation by the safety layer for hazardous actions. A wrong tool call by a digital agent ends with a retry, but a malfunction by a physical agent can cause irreversible harm.
:::

:::caution
Robot foundation models and **world models** are an early, rapidly developing area as of September 2026. Model names, versions, and performance figures change substantially with each vendor announcement, so this document covers only the range where mature comparison is possible and defers details to official source links.
:::

## Safety Layer — Autonomous Driving and Robotics

AI that moves in the physical world is directly tied to human life and equipment, making **functional safety** central. Domain-specific safety standards and certification regimes apply separately — [ISO 26262](https://www.iso.org/standard/68383.html) for autonomous driving, [ISO 13849](https://www.iso.org/standard/73481.html) and IEC 61508 for industrial machinery and robots — and the principle is to maintain an **independent safety layer** (safety stop, hardware interlocks, safety PLC) that operates regardless of the AI model's judgment.

Vendors and suppliers offer commercial stacks implementing this. For example, NVIDIA offers the safety system **Halos**.

- **Autonomous vehicles (AV)**: the [DRIVE](https://www.nvidia.com/en-us/solutions/autonomous-vehicles/) platform (AGX, Hyperion) with the Halos safety system (spanning cloud to vehicle, targeting ISO 26262), with simulation via Omniverse and Cosmos.
- **Robotics**: In June 2026 NVIDIA announced **[Halos for Robotics](https://developer.nvidia.com/blog/inside-nvidia-halos-for-robotics-a-full-stack-functional-safety-system-for-physical-ai/)** (IGX Thor, Holoscan Sensor Bridge, Halos OS, AI Systems Inspection Lab), extending its autonomous driving safety foundation to industrial robots, humanoids, and AMRs.

:::note
The safety layer is **a separate safety system, not a foundation model**. A foundation model (for example [Isaac GR00T](https://developer.nvidia.com/isaac/gr00t)) handles robot perception, planning, and motion, while the layer responsible for functional safety above it plays a different role. The safety layer acts as a final gate that **blocks or constrains any motion outside the permitted action space**, even one planned by an agent or model. Halos above is a commercial implementation example of this safety layer, starting in autonomous driving and extending to robotics in 2026.
:::

## Multicloud and Edge Architecture Considerations

### What Goes at the Edge, What Goes in the Cloud

Physical AI design starts by deciding where each task belongs — edge or cloud. The criteria are latency sensitivity, data volume (bandwidth), safety requirements, and behavior when the network is severed.

| Task | Primary location | Reason |
| --- | --- | --- |
| Real-time perception and control loop | Edge | Latency-sensitive and must not stop even when the network is severed |
| Safety stop and emergency shutdown | Edge | Cannot tolerate a cloud round trip |
| First-pass sensor data filtering and aggregation | Edge | Uploading all raw data costs too much bandwidth and money |
| Data storage and labeling | Cloud | Aggregate data from many machines and manage it as a training asset |
| Model training and retraining | Cloud | Requires large-scale GPUs and datasets (see [GPU Infrastructure](../gpu-infra/workload-and-architecture/)) |
| Synthetic data generation and simulation | Cloud | Digital twins and simulators require large-scale compute |
| Multi-robot fleet coordination, long-horizon planning | Cloud | Global coordination beyond an individual edge's field of view |
| Model version management and deployment (OTA) | Cloud → Edge | Managed centrally and distributed to the field |

### The Closed-Loop Operating Cycle

Physical AI is not deployed once and finished; it operates as a cycle in which field data returns to the model. Each stage of the [pipeline flow diagram in the overview](./overview/#what-physical-ai-is) corresponds to the following operating cycle.

1. **Edge inference** (`Edge Inference` in the diagram) — Perceive, decide, and control in real time on site, selecting only meaningful events and anomalous data.
2. **Telemetry collection and refinement** (`Telemetry` → `Data Lake, Labeling`) — Upload the selected data and operation logs to the cloud, store them, and refine and label them for training use.
3. **Cloud retraining and simulation** (`Cloud Training, Model Management` ↔ `Simulation, Digital Twin`) — Improve the model with collected data and validate new scenarios in the digital twin and simulation.
4. **OTA deployment** (`Deploy` → `Edge Inference`) — Deploy validated models and policies back to the edge. For general patterns such as signing and rollback against deployment failure or regression, see [Hybrid and Edge Computing](../../../compute/hybrid-and-edge/).

:::note
If the network is severed, stages 2–4 of this cycle pause, but stage 1 (edge inference and control) must **continue autonomously offline**. Assume disconnection is a normal state rather than an exception, and design the edge to operate safely on its own.
:::

### What Determines Whether a Model Passes

To run the closed loop, you need a criterion for "is this model fit to ship." In Physical AI, however, **a lower training loss does not mean a higher real success rate.** A model trained to faithfully reproduce demonstration data cannot recover once it falls into a state absent from those demonstrations.

The criterion must therefore be **the success rate of rollouts carried through to completion**, not a loss value. In practice, three tiers are recorded separately.

| Evaluation tier | What it measures | Limitation |
| --- | --- | --- |
| Offline metrics | Loss and prediction accuracy on validation data | Weakly correlated with success rate. Use for regression detection only |
| Simulation rollouts | Success rate completing the task in the simulator | Diverges from reality by the size of the sim-to-real gap |
| Physical rollouts | Success rate, intervention count, and recovery time on real equipment | Most trustworthy but most expensive |

:::caution
Robotics evaluation benchmarks are **less standardized than those for language models.** Vendor-reported success rates vary greatly with task definition, initial conditions, and whether retries are allowed, so check first **whether the measurement conditions are published** rather than focusing on the number itself. If the conditions differ, two models' success rates are not comparable. For general model evaluation, see [LLMOps](../llmops/).
:::

### Matching Deployment to Fleet Scale — Abort and Rollback Are Different Layers

Loading a model onto one robot and deploying to a fleet of thousands to tens of thousands are different problems. At fleet scale, the design hinges on **how fast a bad model spreads** and **whether it can be reversed once spread**.

- **Staged rollout** — Deploy to a small group first and expand, halting expansion if the failure rate exceeds a threshold.
- **Abort** — The mechanism that halts expansion. In many fleet OTA services, however, abort **cancels only targets that have not yet started** and deployments already in progress run to completion, so confirm the scope of your service's abort behavior in the vendor's documentation.
- **Rollback** — The mechanism that returns devices that already received the new version to their previous state. It is a separate layer from abort and works only if the device side has a recovery path such as **previous-version retention or an A/B partition**.

:::caution
"We set abort criteria, so we are safe" is the most common misconception. Abort only halts spread; it **cannot reverse devices already deployed to.** The rollback path must be designed separately on both the cloud-side deployment policy and the device-side recovery mechanism.
:::

:::note
Fleet deployment services often have **quotas that cannot be adjusted** (targets per job, number of dynamic groups, deployment package size, and so on). Discovering such limits late forces a change to the deployment structure itself, so during the pilot phase **check each vendor's current service quota documentation against your target fleet size** first. Also, in configurations where new devices are automatically added to a deployment group, there may be behavior where, depending on when they join, they skip the staged rollout and receive the deployment immediately.
:::

### Other Considerations

- **Data gravity and latency** — Sensor data is high-volume and latency-sensitive, so dividing work between on-site edge inference and cloud training is the baseline design. Decide first what is processed at the edge and what is uploaded.
- **Simulator portability** — If digital twins and simulation are tied to one cloud's proprietary service, porting becomes difficult. Prioritizing stacks such as NVIDIA Omniverse and Isaac that run anywhere given a GPU reduces lock-in.
- **On-device vs. cloud training split** — It is common to split training and synthetic data generation to cloud GPUs and real-time inference to on-device hardware (for example the Jetson family).
- **Safety and regulation** — Autonomous driving and industrial robots are subject to separate functional safety certification and regulation. Reflect certification requirements early in the architecture.
- **Check product lifecycle** — This area has many retired (EOL) products (for example Azure Percept, AWS RoboMaker, managed labeling services). Always confirm each service's current support status before designing.

## Common Mistakes

- **Bolting on safety later** — Autonomous driving and robots must design safety in from the start ("built-in," not "bolt-on").
- **Granting physical agents unlimited permissions** — Letting an autonomous agent call actuators without constraints turns a malfunction directly into physical harm. Action-space restriction and safety-layer validation are essential.
- **Setting abort criteria without designing a rollback path** — Spread stops, but devices already deployed to do not come back.
- **Placing a large model directly in the real-time control loop** — Failing to meet the control period leads to safety problems. Separate the slow planning layer from the fast control layer.
- **Using simulation success rates as deployment evidence** — Deploying without a physical rollout validation gate lets the sim-to-real gap surface in the field.

## Checklist

### Edge and Cloud Placement

- [ ] Have you distinguished inference to process at the edge from data to upload to the cloud?
- [ ] Does the edge operate autonomously and safely (offline) when the network is severed?
- [ ] Have you defined how many milliseconds each decision must complete within, and separated the slow planning layer from the fast control layer?
- [ ] Is the division of roles between on-device inference and cloud training clear?

### Safety and Regulation

- [ ] If agents call physical actuators, have you restricted the action space and added safety-layer validation?
- [ ] For autonomous driving or industrial robots, have you reflected functional safety certification requirements in the design?

### Deployment and Operations

- [ ] Have you defined the model pass criterion as rollout success rate rather than a loss value, with a physical validation gate?
- [ ] Have you designed both a staged rollout and a **rollback path** for fleet deployment (rather than assuming abort is sufficient)?
- [ ] Does your target fleet size fit within each vendor's non-adjustable service quotas?

## Related Documents

- [Physical AI Overview](./overview/) — Full pipeline, layered structure, and open problems
- [Data and Training](./data-and-training/) — Edge, data pipeline, simulation, training infrastructure
- [AI Agents](../../../ai/agents/) — Autonomous planning and execution concepts
- [AI Agent Integration (MCP)](../../../mcp/) — Agent-to-tool and system integration protocols
- [GPU Infrastructure](../gpu-infra/workload-and-architecture/) — GPU clusters for cloud training and simulation
- [LLMOps](../llmops/) — General model evaluation and operations
- [Japan AI Landscape](../../../japan/ai-landscape/) — Robotics foundation models as a national project (GENIAC)

## Further Reading

### Cross-vendor

- [NVIDIA Isaac GR00T (developer page)](https://developer.nvidia.com/isaac/gr00t)
- [NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/)
- [NVIDIA autonomous vehicle (DRIVE, Halos) solutions](https://www.nvidia.com/en-us/solutions/autonomous-vehicles/)
- [Anthropic Model Hardware Standard (research preview)](https://www.anthropic.com/news/model-hardware-standard-research-preview)
