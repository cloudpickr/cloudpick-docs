---
title: "Getting Started with DevOps"
description: "Explains the definition of DevOps, GitOps, platform engineering, and SLI/SLO/error budgets."
---

> Last reviewed: May 2026

## Overview

In traditional IT organizations, the development team (Dev) writes code and the operations team (Ops) manages the servers. The development team wants to ship features fast, while the operations team wants to maintain stability — creating conflict. Deployments happen once every few weeks, and when an incident occurs, teams pass the blame back and forth.

**DevOps** is a culture and a set of practices that breaks down this wall. It's not about developers doing all the operations work themselves — it's about development and operations **having visibility into each other's work and collaborating** to deliver services faster and more reliably.

### What DevOps Is Not

- ❌ Developers handling all the server management themselves
- ❌ Using a specific tool makes you "DevOps"
- ❌ Renaming a team to the "DevOps team"

### Core Values of DevOps

- **Automation** — Automating repetitive work (build, test, deploy, infrastructure configuration) to reduce human error.
- **Visibility** — Developers can see production metrics, logs, and errors directly, allowing them to identify problems quickly.
- **Feedback loops** — Quickly checking user reaction and system state after deployment, then improving.
- **Small-batch deployment** — Instead of deploying one large change at once, deploy small changes frequently to reduce risk.

## Why DevOps in the Cloud

On-premises, purchasing servers takes weeks, and environment configuration is manual, making automation difficult. The cloud is the ideal environment for realizing DevOps.

- **Infrastructure as code** — Infrastructure can be created/deleted via API, enabling IaC.
- **Environment replication** — A test environment identical to production can be created in minutes.
- **Managed services** — You don't need to build CI/CD, monitoring, or logging yourself.
- **Pay-as-you-go** — Turn on test environments only when needed and delete them afterward to save cost.

:::note
For how to manage infrastructure as code, see [Infrastructure as Code (IaC)](../../devops/iac/); for build/test/deploy automation, see [CI/CD](../../devops/cicd/).
:::

## GitOps

**GitOps** is one of the DevOps practices, using a Git repository as the **single source of truth** for infrastructure and applications. It has become the standard deployment method especially in **Kubernetes environments**, because K8s's declarative manifests (YAML) naturally align with GitOps's philosophy that "the state declared in Git = the cluster state."

- Infrastructure/app changes = commit to Git → an agent detects it → automatically reflected in the cluster
- Rollback = revert to a previous commit in the Git history
- Audit = the Git log itself is the change history
- Drift detection = if the cluster state differs from Git, it's automatically reconciled

:::note
For a comparison of GitOps tools (ArgoCD, Flux, vendor-native), promotion strategies, cluster upgrades, and Day-2 operations, see [Kubernetes Operations](../../devops/kubernetes-operations/).
:::

## Platform Engineering

As DevOps matures, having developers handle infrastructure directly becomes a burden instead. **Platform engineering** is about building an internal platform so developers can consume infrastructure as a self-service.

- Developer: "I want to push to production with one deploy button."
- Platform team: Provides an internal platform that abstracts CI/CD, monitoring, and security.

Developers focus on their core job (writing code), while the platform team provides a safe and efficient deployment path.

:::note
For the components of an IDP (Internal Developer Platform), open-source tools, and adoption strategy, see [Platform Engineering](../../devops/platform-engineering/).
:::

## Benefits of Developers Participating in Operations

- **Faster incident response** — The person who wrote the code identifies the root cause fastest when looking at logs.
- **Better design quality** — Feeling the operational burden firsthand leads to writing code that's easier to operate.
- **Faster feedback** — Checking metrics directly after deployment lets you quickly identify the direction for improvement.

## SLI, SLO, and Error Budgets

A framework in DevOps/SRE for systematically defining "is the service reliable enough?" It's structured as SLI (measured indicator) → SLO (target value) → SLA (contract), with the error budget balancing deployment speed against stability.

:::note
For details, see [SLI/SLO and Error Budgets](../../devops/slo/).
:::

## Common Mistakes

- **Creating a "DevOps team" while keeping the existing silos** — DevOps is a culture, not a team name. It just creates another wall between the development team and the operations team.
- **Adopting tools without automation** — Installing Jenkins/ArgoCD has no effect if manual approval and manual deployment remain. Start by automating repetitive work.
- **Validating in a test environment that differs from production** — Incidents caused by environment differences keep recurring. Replicate identical environments with IaC.

## Checklist

- [ ] Does an automated pipeline exist from code commit through production deployment?
- [ ] Can developers view production metrics and logs directly?
- [ ] Are deployment frequency, lead time, change failure rate, and recovery time (the DORA 4 Metrics) being measured?

## References

### AWS

- [AWS DevOps Guide](https://docs.aws.amazon.com/ko_kr/whitepapers/latest/introduction-devops-aws/introduction-devops-aws.html)

### Azure

- [Introduction to Azure DevOps](https://learn.microsoft.com/ko-kr/devops/what-is-devops)

### Google Cloud

- [Google Cloud DevOps](https://cloud.google.com/devops)

### Standards and Community

- [DORA Metrics (DevOps Research and Assessment)](https://dora.dev/)
- [Platform Engineering Guide](https://platformengineering.org/)
