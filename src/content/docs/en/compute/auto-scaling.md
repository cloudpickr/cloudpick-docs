---
title: "Auto Scaling"
description: "Compares VM auto scaling, predictive scaling, and application-level scaling across vendors."
---

> Last reviewed: May 2026

## Overview

VMs let you create servers quickly, but responding to traffic changes is still your responsibility. When traffic spikes, you have to manually add servers, and when it drops, you have to remove them again. If this process is too slow, the service goes down; if it overshoots, cost is wasted.

**Auto scaling** automates this decision and execution. It monitors metrics such as CPU utilization and request count, and automatically adds servers when a threshold is exceeded, then automatically removes them when load decreases.

:::caution
Auto scaling **takes several minutes to scale out**. It may not respond quickly enough to sudden traffic spikes (on the order of seconds). Also, a misconfigured policy can automatically amplify an outage, so careful policy design and testing are important.
:::

## Types of scaling policies

Auto scaling is categorized by the policy that decides "when to scale."

| Policy | Trigger | Characteristics | When to use |
| --- | --- | --- | --- |
| **Target Tracking** | Automatically adjusts to keep a specific metric at a target value | Simplest. Suitable for most workloads | Default choice. General web services |
| **Step Scaling** | Scales in multiple steps based on how far the threshold is exceeded | Fine-grained control | Complex workloads with varied traffic patterns |
| **Simple Scaling** | Scales by a fixed amount when threshold is exceeded | Older approach. Longer cooldown | Legacy compatibility. Target Tracking recommended for new setups |
| **Predictive** | Predicts traffic with ML and scales ahead of time | Effective for predictable, periodic patterns | Recurring daily/weekly traffic (commute hours, weekends) |
| **Scheduled** | Scales at a specified time | For planned events where predictive scaling doesn't apply | Promotions, Black Friday, large-scale events |

:::caution
For workloads where CPU is not the bottleneck (I/O-bound, memory-bound, DB connection pool exhaustion), CPU-based scaling won't react even after a traffic surge. Choose the metric that reflects the workload's actual bottleneck.
:::

### Example policy combinations by workload

| Workload pattern | Recommended policy combination | Reason |
| --- | --- | --- |
| **General web service** (gradual traffic increase) | Target Tracking (validate target value with load testing) | Simple and usually sufficient |
| **Commute pattern** (spike at 9am, drop at 6pm daily) | Predictive + Target Tracking | Predictive scales ahead, Target fine-tunes |
| **Event/promotion** (surge at a specific time) | Scheduled + Target Tracking | Scale ahead of start, then auto-adjust |
| **Batch/data processing** (queue-based) | Target Tracking (based on queue depth) | Scale by pending work count, not CPU |
| **Unpredictable spikes** (gaming, viral) | High minimum instance count + CDN/cache + rate limiting | Scaling speed can't keep up; secure headroom in advance |

:::note
For most workloads, **start with a single metric-based Target Tracking (Target Utilization) policy**. All vendors support this approach, and it's fine to add complex policy combinations later, once you've observed traffic patterns closely. Behavior differs by vendor when multiple policies are applied (AWS: selects the largest capacity, Google Cloud: uses the highest signal), so check the official documentation.
:::

### Cooldown time

This is the wait time after a scaling event before the next scaling action. Too short and scaling thrashes excessively; too long and it responds slowly to traffic changes. It should never be shorter than the app's startup time.

| Vendor | Default | Cold start mitigation |
| --- | --- | --- |
| AWS | 300 seconds | Warm Pool (pre-initialized instances on standby) |
| Azure | 5 minutes | Instance Protection, Custom Script Extension |
| Google Cloud | 60 seconds (Initial Delay) | Auto-healing + pre-built images |
| OCI | 300 seconds | Configurable cooldown period |

## Limitations of auto scaling

| Limitation | Description | Mitigation |
| --- | --- | --- |
| **Cold start time** | New instance boot + app readiness takes several minutes | Pre-initialized instance pools, maintaining a minimum instance count, pre-built (golden) images |
| **Stateful workloads** | Instances with session/cache/disk data lose it on scale-in | Move state to external storage (Valkey, DB) |
| **Unpredictable spikes** | Scaling speed can't keep up with traffic growth | Reserve minimum capacity, CDN/cache, rate limiting, graceful degradation |
| **Quota exhaustion** | Scale-out fails silently when account/region vCPU limits are exceeded | Check quotas in advance, request increases, set up scaling failure alerts |

## Mixing Spot/Preemptible instances

Mixing on-demand and Spot instances in an auto scaling group can reduce cost for workloads that can tolerate interruption. However, without a fallback strategy this becomes a source of outages.

| Vendor | Method | Notes |
| --- | --- | --- |
| AWS | ASG Mixed Instances Policy | Specify on-demand base + Spot ratio. Pool of multiple instance types |
| Azure | VMSS Spot Priority Mix | Configure Spot VM ratio. Choose an eviction policy |
| Google Cloud | MIG + Spot VMs | Include Spot VMs in the MIG. Automatic recreation on preemption |
| OCI | Instance Pool + Preemptible | Mix Preemptible instances into the pool |

## Services with built-in auto scaling

These services are automatically handled by the platform without you having to configure scaling policies directly.

| Vendor | Service | Description |
| --- | --- | --- |
| AWS | Elastic Beanstalk, ECS Service Auto Scaling, Lambda | Scaling built into app deployment |
| Azure | App Service (Auto Scale), Container Apps, Functions | PaaS-level auto scaling |
| Google Cloud | Cloud Run, App Engine, GKE Autopilot | Request-based auto scale up/down |
| OCI | Container Instances, Functions | Serverless auto scaling |

:::note
Before configuring VM-level auto scaling directly, first assess whether your workload fits one of the services above. Using PaaS/serverless greatly simplifies VM scaling policy, but concurrency limits, maximum instance counts, and downstream protection still need to be configured separately.
:::

## Key differences

- **AWS** — Deploys mixed on-demand/Spot instances via Mixed Instances Policy. Warm Pool keeps pre-initialized instances standing by to mitigate cold starts.
- **Azure** — VMSS manages VM deployment and scaling as a single resource. Spot Priority Mix optimizes cost.
- **Google Cloud** — Auto-healing is built into MIGs by default, automatically replacing unhealthy instances. Shortest cooldown (60 seconds) for the fastest response.
- **OCI** — Instance Pool-based auto scaling. Supports metric- and schedule-based scaling, with Preemptible instance mixing available.

## Auto scaling setup checklist

- [ ] Did you choose the scaling metric to match the workload's bottleneck (CPU, request count, queue depth, response time, etc.)?
- [ ] Did you set a Grace Period / warm-up time (to ignore the unstable metric window right after a new instance boots)?
- [ ] Did you configure health checks on both the load balancer and auto scaling?
- [ ] Did you set Connection Draining / Deregistration Delay (to guarantee in-flight requests complete)?
- [ ] Did you implement graceful shutdown (SIGTERM handling) in the app?
- [ ] Did you review the termination policy (AZ balance, Newest/Oldest, etc.)?
- [ ] Did you exclude instances that need scale-in protection (mid-deployment, long-running tasks)?
- [ ] Did you set the minimum instance count to fit an acceptable cold-start range?
- [ ] Did you set the maximum instance count to fit your cost ceiling?
- [ ] Did you check per-region/AZ vCPU quotas in advance and request increases?
- [ ] Did you set up a fallback (switch to on-demand) strategy when mixing Spot/Preemptible instances?
- [ ] Did you set up notifications for scaling events and scaling failures?
- [ ] Did you confirm the cooldown time is longer than the app's startup time?

## Common mistakes

- **Scaling based solely on CPU metrics** — In I/O-bound or memory-bound workloads, the service can slow down even while CPU stays low. Choose the metric that reflects the actual bottleneck (request latency, queue depth, etc.).
- **Setting cooldown shorter than app startup time** — The next scaling event fires before the new instance is ready, causing excessive, unnecessary instance creation.
- **Setting the maximum instance count to unlimited** — If health check failures repeat during an incident, instances can be created without bound and cost can explode. Always set an upper limit.

## References

### AWS

- [AWS Auto Scaling documentation](https://docs.aws.amazon.com/ko_kr/autoscaling/)
- [Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/ko_kr/autoscaling/ec2/userguide/)

### Azure

- [Azure VM Scale Sets documentation](https://learn.microsoft.com/ko-kr/azure/virtual-machine-scale-sets/)
- [Azure Autoscale documentation](https://learn.microsoft.com/ko-kr/azure/azure-monitor/autoscale/autoscale-overview)

### Google Cloud

- [Google Cloud Autoscaler documentation](https://cloud.google.com/compute/docs/autoscaler)
- [Google Cloud MIG documentation](https://cloud.google.com/compute/docs/instance-groups)

### OCI

- [OCI Autoscaling documentation](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/autoscalinginstancepools.htm)
