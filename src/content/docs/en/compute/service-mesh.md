---
title: "Service Mesh"
description: "Compares the concept of a service mesh, the sidecar vs. sidecarless models, and vendor-managed services."
---

> Last reviewed: August 2026

## Overview

Operating microservices with [container services](../../compute/containers/) makes inter-service communication complex. A **service mesh** manages this communication at the infrastructure layer, providing security, observability, and traffic control without any application code changes.

### Problems a service mesh solves

| Problem | How the service mesh solves it |
| --- | --- |
| Inter-service encryption (mTLS) | Automatic certificate issuance/rotation, encrypting all communication |
| Traffic routing | Canary deployments, A/B testing, traffic splitting |
| Circuit breaking | Automatically isolating a failing service, retries/timeouts |
| Observability | Automatically collecting latency/error rates between services (no code changes) |
| Access control | Policies for inter-service communication (which service can call which) |

## Sidecar vs. sidecarless

| Model | Approach | Pros | Cons |
| --- | --- | --- | --- |
| **Sidecar** | A proxy container (Envoy, etc.) injected into each pod | Mature ecosystem, feature-rich | Resource overhead (memory/CPU), added latency |
| **Sidecarless** | Handled at the node level or kernel level | Saves resources, minimal latency | Still early-stage, limited features |

Representative implementations:
- Sidecar: Istio (Envoy), Linkerd (linkerd2-proxy)
- Sidecarless: Istio Ambient Mesh (ztunnel), Cilium Service Mesh (eBPF)

## Comparison of major solutions

| Solution | Proxy | Characteristics |
| --- | --- | --- |
| [Istio](https://istio.io/) | Envoy | Most feature-rich. Supports sidecarless via Ambient Mesh. High complexity |
| [Linkerd](https://linkerd.io/) | linkerd2-proxy (Rust) | Lightweight, simple. Minimal resource overhead. Fewer features than Istio |
| [Consul Connect](https://www.consul.io/docs/connect) | Envoy | Integrated with the HashiCorp ecosystem. Multi-platform (K8s + VM) |

## Vendor-managed services

| Vendor | Service | Based on | Characteristics |
| --- | --- | --- | --- |
| AWS | [App Mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html) (maintenance mode) / ECS Service Connect | Envoy | App Mesh is not recommended for new adoption. ECS Service Connect or VPC Lattice recommended |
| AWS | [VPC Lattice](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html) | AWS native | Manages inter-service connectivity at the VPC level. No sidecar required |
| Azure | [Istio add-on for AKS](https://learn.microsoft.com/azure/aks/istio-about) | Istio | Native AKS integration. Managed control plane |
| Google Cloud | [Cloud Service Mesh](https://cloud.google.com/service-mesh/docs) | Istio-based | GKE integration. Managed control plane + data plane |
| OCI | No self-managed offering | — | Install Istio/Linkerd directly on OKE |

## When to adopt

| Criterion | Recommended to adopt | Not necessary |
| --- | --- | --- |
| Number of services | 10+, with boundaries between teams | Monolith or 3-5 services |
| Security requirement | mTLS between services required (regulation/audit) | No need to encrypt internal traffic |
| Traffic control | Canary/A-B deployment, fine-grained routing needed | Simple rolling deployment is sufficient |
| Observability | Need to track latency/errors between services | APM is sufficient |

:::note
**A service mesh adds complexity.** If you have few services or a small team, native features (Security Group, IAM, ALB routing) may be sufficient without a service mesh. Adopt one "when you need it."
:::

## Common mistakes

- **Adopting a service mesh with few services** — At a scale of 3-5 services, it only adds complexity. First check whether native features (Security Group, IAM, ALB routing) are sufficient.
- **Ignoring sidecar resource overhead** — Adding an Envoy proxy to every pod adds up to significant memory/CPU usage. Without setting resource requests/limits, nodes run out of capacity.
- **Not preparing for the debugging difficulty mTLS introduces** — Once all traffic is encrypted, existing packet capture tools stop working. Set up mesh-level logging and distributed tracing together with mTLS.

## Checklist

- [ ] Do you have a clear requirement (mTLS, traffic splitting, observability) that justifies adopting a service mesh?
- [ ] Have you set resource requests/limits for sidecar proxies and confirmed node capacity?
- [ ] Have you confirmed that the data plane (existing connections) keeps working if the mesh control plane fails?

## References

### AWS

- [AWS VPC Lattice documentation](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html)

### Azure

- [Azure AKS Istio add-on](https://learn.microsoft.com/azure/aks/istio-about)

### Google Cloud

- [Google Cloud Cloud Service Mesh](https://cloud.google.com/service-mesh/docs)

### Standards and community

- [Istio documentation](https://istio.io/latest/docs/)
- [Linkerd documentation](https://linkerd.io/2/overview/)
- [CNCF Service Mesh Landscape](https://landscape.cncf.io/card-mode?category=service-mesh)
