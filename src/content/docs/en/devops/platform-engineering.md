---
title: "Platform Engineering"
description: "Explains the concepts, tools, and multicloud standardization of platform engineering and the IDP (Internal Developer Platform)."
---

> Last reviewed: September 2026

## Overview

:::note[Prerequisites and related documents]
This is an advanced topic that assumes the CI/CD and automation concepts from [Getting Started with DevOps](../../devops/getting-started/) and [Kubernetes operations](../../devops/kubernetes-operations/). Read those first for basic pipeline concepts. This document focuses on building an Internal Developer Platform (IDP) for developer self-service.
:::

If [DevOps](../../devops/getting-started/) is "collaboration between development and operations," **platform engineering** is "building a platform that lets developers deploy as a self-service without thinking about infrastructure."

Instead of a developer opening a Jira ticket to request something from the infrastructure team, they provision their own environment by following the Golden Path the platform provides.

## Adoption gate — when and how

Platform engineering is not something every organization needs. Before picking tools, first decide **whether to adopt it, when, and at what scope**.

| Decision axis | Signals that support adoption | Signals it is still too early |
| --- | --- | --- |
| **Organization size** | Many development teams (roughly 5+ teams / 50+ people); infrastructure requests become a bottleneck as the number of services grows | A few teams can handle infrastructure themselves |
| **Repetitive work** | Environment provisioning and deployment requests recur, and ticket queues grow longer | Requests are infrequent and standardization pays off little |
| **Self-service demand** | Developers want to deploy without knowing infrastructure details; a Golden Path is needed | Team requirements diverge so much that agreeing on a standard path is hard |
| **Operating staff** | You can secure a dedicated team to run and improve the platform like a product | You have people to build the platform but no one to maintain it (risk of it being abandoned after adoption) |

**Build vs. buy:**

- **Buy/assemble (recommended starting point)** — A combination of mature OSS and managed services such as Backstage (portal) + Crossplane/Terraform (provisioning) + Argo CD (delivery). Most organizations do not need to build their own framework from scratch.
- **Build your own** — Only when regulatory, security, or scale requirements cannot be met by off-the-shelf tools. You must be able to bear the maintenance cost of the platform itself.

**Centralization scope:** Rather than forcing a single company-wide platform, a realistic compromise is to **centralize the common foundation (authentication, policy, observability, cost tagging) while delegating areas that need team autonomy (choice of language and framework)**. Starting narrowly with the one or two most repetitive Golden Paths and expanding incrementally carries lower failure risk.

## IDP (Internal Developer Platform)

| Component | Role | Key tools |
| --- | --- | --- |
| **Developer portal** | Service catalog, owner tracking, onboarding | Backstage (CNCF Incubating), Port, Cortex |
| **Infrastructure self-service** | Request an environment via PR → automatic provisioning | Crossplane, Terraform + Atlantis, Pulumi Operator |
| **Golden Path** | A recommended architecture template for a quick start | Backstage Software Templates, Cookiecutter |
| **CI/CD pipeline (shared)** | Standardized build/deploy pipeline templates | Argo CD, Flux, Tekton, GitHub Actions reusable workflows |
| **Secrets management** | Injects vendor secrets into K8s/apps | External Secrets Operator, HashiCorp Vault |
| **Observability stack** | Unified collection of metrics, logs, traces | OpenTelemetry, Prometheus, Grafana, Loki |
| **Policy engine (guardrails)** | Automatically enforces security/cost/compliance | OPA/Gatekeeper, Kyverno, Checkov, tfsec |
| **Cost visibility** | Cost allocation and alerts per team/service | OpenCost, Kubecost, Infracost |
| **Environment management** | Create/delete ephemeral (preview) environments | Argo CD ApplicationSet, vCluster |
| **Internal module registry** | Vetted Terraform modules, Helm charts | Terraform Registry (private), Harbor |

### Open-Source Ecosystem Map

**Portal & catalog:**
- Backstage (Spotify, CNCF Incubating) — the broadest ecosystem, rich plugins
- Port — SaaS, no code required
- Cortex — SaaS, strong scorecards

**GitOps & deployment:**
- Argo CD — the K8s deployment standard, multi-cluster
- Flux — lightweight, CNCF Graduated
- Tekton — K8s-native CI/CD pipeline

**Infrastructure abstraction:**
- Crossplane — manages cloud resources via K8s CRDs, multicloud
- Terraform + Atlantis — automates PR-based plan/apply

**Policy & governance:**
- OPA/Gatekeeper — K8s Admission Control
- Kyverno — YAML-based policy (lower barrier to entry than OPA)

**Observability:**
- OpenTelemetry — the vendor-neutral instrumentation standard (CNCF Graduated)
- Prometheus + Grafana — the de facto standard for metrics collection/visualization

**Secrets:**
- HashiCorp Vault — the most mature, multicloud
- External Secrets Operator — connects vendor secret managers to K8s

## Multicloud Standardization

One of the core values of platform engineering is **abstracting away vendor differences**.

| Abstraction layer | Method | Tools |
| --- | --- | --- |
| **Infrastructure provisioning** | Vendor-neutral IaC | [Crossplane](https://www.crossplane.io/) (K8s-native), Terraform modules |
| **Deployment** | Unified GitOps | Argo CD (multi-cluster) |
| **Secrets** | Unified secrets management | External Secrets Operator |
| **Observability** | Unified metrics/logs | OpenTelemetry + Grafana |

## Platform as a Product

The platform team treats internal developers as "customers" and operates the platform as a "product."

- **User feedback** — Regularly survey developer satisfaction
- **SLO** — Set availability/response time targets for the platform itself
- **Roadmap** — Prioritize features based on user needs
- **Documentation** — Self-service guides, API docs, troubleshooting guides

## Common Mistakes

- **Building the platform without developer feedback** — It becomes an internal tool nobody uses. Involve developers as users from the start and build a feedback loop.
- **Enforcing the Golden Path with no exceptions allowed** — Without flexibility, developers work around it. Distinguish between guardrails (what's forbidden) and the Golden Path (the recommended route).
- **The platform team directly handling every infrastructure request** — The ticket queue becomes a bottleneck. Self-service automation is the core of platform engineering.

## Checklist

- [ ] Can developers create environments as a self-service, without an infrastructure team ticket?
- [ ] Are SLOs (availability, deployment pipeline success rate) defined for the platform itself?
- [ ] Is there a regular developer satisfaction survey and a process to act on the feedback?

## References

### Standards and Community

- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
- [Backstage Documentation](https://backstage.io/docs/)
- [Crossplane Documentation](https://docs.crossplane.io/)
- [Humanitec Platform Orchestrator](https://humanitec.com/)
- [Team Topologies — Platform Teams](https://teamtopologies.com/)
