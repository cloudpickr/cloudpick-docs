---
title: "Field Deployment"
description: "Summarizes the role of Forward Deployed Engineers (FDE), the skills they need, and practical knowledge for multicloud environments."
---

> Last reviewed: July 2026

A Forward Deployed Engineer (FDE) is embedded directly in a customer's environment to land the product in production. Rather than design or advisory work, they write and own real production code.

This document summarizes the core knowledge an FDE needs in multicloud environments. It curates CloudPick's existing documentation from an FDE perspective and adds FDE-specific context.

:::note
The title "FDE" varies across organizations (Deployment Engineer, Field Engineer, Implementation Engineer, etc.). This document is based on the **role** — an engineer who owns production code and delivers the product on-site at the customer — rather than the title.
:::

---

## Origin and Spread of the Role

Palantir created this role in the mid-2000s while deploying Gotham to U.S. intelligence agencies. Classified data, undocumented schemas, and failures of conventional deployment approaches led to a model in which engineers are dispatched directly to the customer site to solve problems.

Since 2024, AI products have faced the same problem, causing the role to spread explosively. For a powerful but general-purpose product (LLMs, agents) to create real value in a customer's complex legacy environment, someone needs to write code on-site.

### Major Events, 2025–2026

| Time | Event | Scale |
| --- | --- | --- |
| May 2026 | OpenAI Deployment Company founded (TPG-led investment) | ~$4B |
| May 2026 | Anthropic enterprise services JV "Ode" (Blackstone, Goldman Sachs) | ~$1.5B |
| June 2026 | AWS Forward Deployed Engineering organization established | ~$1B |
| 2025–2026 | FDE job postings up 800%–1,000%+ year over year | 39+ companies, 220+ open positions |

---

## FDE vs. Solutions Architect

FDEs and SAs (Solutions Architects) both connect customers with technology, but the key difference lies in **code ownership** and **depth of embedding**.

| Criterion | Solutions Architect (SA) | Forward Deployed Engineer (FDE) |
| --- | --- | --- |
| **Primary activity timing** | Pre-sale ~ initial implementation | Post-sale ~ production operations |
| **Core work** | Architecture design, technical validation, PoC | Writing production code, integration, live operations |
| **Code ownership** | Low (PoC/demo level) | High (directly owns production code) |
| **Customer relationship** | Advisory | Embedded |
| **Deliverables** | Architecture diagrams, proposals, integration guides | Production code, custom integrations, deployment scripts |
| **Success metrics** | Sales conversion rate, platform adoption rate | Deployment success rate, system stability, TTV (Time-to-Value) |
| **Compensation (2026)** | $160K–$270K+ TC | $180K–$550K+ TC (frontier AI labs: $1M+) |

### Who Gets Hired, and When

- **SA**: When product-market fit is clear and technical objections are blocking deal closure
- **FDE**: When the product is powerful but making it work in the customer's environment requires custom code
- **SI**: When a large-scale system build must be completed on schedule with headcount
- **Both**: For large enterprise deals — the SA designs the architecture, the FDE executes it

### FDE vs. SI (System Integrator)

FDEs and SIs (System Integrators) both write code on-site at the customer, but they differ in **purpose and ownership structure**.

| Criterion | FDE | SI (System Integrator) |
| --- | --- | --- |
| **Affiliation** | Product company (model company, SaaS vendor) | Separate consulting/SI firm |
| **Purpose** | Land the company's own product in the customer's environment and feed product feedback back to headquarters | Build and deliver a system within the SOW (statement of work) scope on schedule |
| **Code ownership** | Can contribute to the product core; reusable patterns feed back into the product | Owned by the customer; transitions to a maintenance contract after project completion |
| **Duration** | Until the product lands (weeks to months, recurring) | SOW duration (months to years, clearly ending) |
| **Success metrics** | Product adoption rate, TTV, contribution to product improvement | Meeting deadlines, passing acceptance tests, sign-off |
| **Staffing model** | Small elite team (1–3 people) | Large-scale staffing (dozens to hundreds) |
| **Playbook** | None (works where a playbook doesn't yet exist) | Exists (methodology, deliverable templates) |
| **Product feedback** | Core role — reflects field problems into the product roadmap | Limited — separate organization from the vendor |

:::note
In large public-sector and financial projects, a local SI commonly builds the overall system while the FDE handles only that company's AI/SaaS integration — a **collaborative** structure. For country-specific SI and procurement landscapes, see the [Korea](../../korea/), [United States](../../us/), [EU](../../eu/), [Japan](../../japan/), and [Singapore](../../singapore/) guides.
:::

:::caution
In the 2025–2026 market, about 40% of postings labeled "FDE" are reportedly just rebranded SE (Sales Engineer) or PS (Professional Services) roles. You can distinguish them by code ownership, production responsibility, and whether there's a quota/OTE component.
:::

---

## Core Knowledge FDEs Need

### Week 1: Entering the Customer Environment

The realities you encounter when first entering a customer environment. This is an FDE-specific challenge that SAs or typical SWEs don't experience.

| Challenge | Description | Related documentation |
| --- | --- | --- |
| Working in someone else's account | Operating with least privilege in the customer's AWS/Azure/GCP account | [Account and Organization Structure](../../about-cloud/accounts-and-organizations/) |
| Negotiated IAM | Restricted access permissions coordinated with the customer's security team | [IAM Overview](../../about-cloud/iam-overview/) |
| Air-gapped environments | Air gaps, proxy-only access, restricted internet access | [Network Isolation](../../security/network-isolation/) |
| Remote access constraints | Customer-specific VPNs, bastion hosts, zero-trust access | [Remote Access Management](../../devops/remote-access/) |
| Compliance | Industry-specific regulations of the customer (finance: PCI-DSS, healthcare: HIPAA, public sector: FedRAMP) | [Compliance](../../governance/compliance/) |

### Infrastructure and Cloud

An FDE must be able to work with whichever cloud the customer environment uses.

- [Getting Started with Cloud](../../about-cloud/getting-started/) — basic concepts
- [Comparing Vendors](../../about-cloud/compare-clouds/) — vendor differences for equivalent functionality
- [Regions and Availability Zones](../../about-cloud/regions-and-zones/) — data sovereignty, latency
- [Shared Responsibility Model](../../about-cloud/shared-responsibility/) — the boundary of responsibility in a customer environment

### Security and Governance

The customer's security team is often an FDE's toughest stakeholder.

- [IAM in Depth](../../security/iam/) — cross-account access, temporary credentials
- [Secrets Management](../../security/secrets/) — accessing secrets in a customer environment
- [Data Protection](../../security/data-protection/) — handling customer data
- [Zero Trust](../../security/zero-trust/) — modern enterprise access model
- [Landing Zone](../../governance/landing-zone/) — understanding the customer's cloud foundation

### Building and Operating

If an FDE owns production code, they also need to understand operations.

- [Getting Started with DevOps](../../devops/getting-started/) — CI/CD, automation
- [Monitoring](../../devops/monitoring/) → [Observability](../../devops/observability/) — debugging in the customer environment
- [SLI/SLO](../../devops/slo/) — defining success metrics
- [Disaster Recovery](../../governance/dr/) — responding to failures in the customer environment
- [Security Incident Response](../../security/incident-response/) — collaborating with the customer during an incident

### Data and Integration

Understanding and connecting the customer's data is at the core of FDE work.

- [Database Operations](../../database/operations/) — accessing and integrating with the customer's DB
- [Database Migration](../../database/migration/) — migrating data

### AI/Agent Deployment

The direct driver behind the surge in FDE demand in 2025–2026.

- [Getting Started with AI](../../ai/getting-started/) — understanding AI products
- [Advanced RAG Patterns](../../ai/rag-patterns/) — building RAG on customer data
- [AI Agents](../../ai/agents/) — deploying agentic workflows
- [LLMOps](../../ai/llmops/) — evaluation, cost, operations, **agent observability**
- [AI Security](../../security/ai-security/) — guardrails, prompt injection defense

---

## The FDE Tech Stack

Every customer environment differs, but these are the tools FDEs commonly work with.

| Category | Tools |
| --- | --- |
| Languages | Python, TypeScript, SQL, Go/Java, Bash |
| Backend | FastAPI, NestJS, Spring Boot |
| Frontend | React, Next.js (ops dashboards, customer portals) |
| Data | PostgreSQL, Spark, dbt, Airflow, Kafka |
| Cloud | AWS, Azure, GCP (EC2, K8s, Lambda, S3, etc.) |
| Containers | Docker, Kubernetes, Helm |
| IaC | Terraform, Pulumi, CloudFormation |
| CI/CD | GitHub Actions, GitLab CI, Argo CD |
| Observability | Datadog, Grafana, Prometheus, Sentry |
| AI/agents | LangGraph, CrewAI, Semantic Kernel, vector DBs |

---

## The Shift to Agentic Delivery

As of 2026, how FDEs work is changing.

**Before**: Writing glue code by hand on-site, manual integration, taking weeks to months

**Now**: A small human team combined with AI agents
- Agents handle scaffolding, evaluation, and long-running workflows
- Humans (FDEs) focus on discovery, governance, and go-live decisions
- AWS's AI-Driven Development Lifecycle formalizes this pattern

**What doesn't change**: Resolving ambiguity in the customer environment, persuading stakeholders, and production ownership — these are not automated.

---

## Career Perspective

| Path | Description |
| --- | --- |
| IC track | FDE → Senior → Staff/Principal FDE |
| Product transition | Field feedback → PM/TPM (the person who best understands product gaps) |
| GTM leadership | Leading a technical sales/deployment organization |
| Founding a company | Many founders are former Palantir FDEs — the position that understands customer problems most deeply |

---

## References

- [The Palantir Forward Deployed Engineering Model](https://fde.academy/blog/how-palantir-invented-the-forward-deployed-engineer-model)
- [Pragmatic Engineer: Forward Deployed Engineers](https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers)
- [FDE vs Solutions Architect (2026)](https://fde.academy/blog/forward-deployed-engineer-vs-solutions-architect)
- [Forbes: AI Giants Bet Billions On FDE (2026)](https://www.forbes.com/sites/janakirammsv/2026/05/28/ai-giants-bet-billions-on-the-most-expensive-job-in-enterprise/)
- [AWS Forward Deployed Engineering Announcement](https://www.aboutamazon.com/news/aws/aws-1-billion-forward-deployed-ai-engineers)
- [FDE Hiring Trends 2026](https://www.paraform.com/blog/forward-deployed-engineer-demand-quadrupled)
