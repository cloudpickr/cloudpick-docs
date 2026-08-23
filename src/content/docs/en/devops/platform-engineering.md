---
title: "Platform Engineering"
description: "Explains the concepts, tools, and multicloud standardization of platform engineering and the IDP (Internal Developer Platform)."
---

> Last reviewed: May 2026

## Overview

If [DevOps](../../devops/getting-started/) is "collaboration between development and operations," **platform engineering** is "building a platform that lets developers deploy as a self-service without thinking about infrastructure."

Instead of a developer opening a Jira ticket to request something from the infrastructure team, they provision their own environment by following the Golden Path the platform provides.

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
