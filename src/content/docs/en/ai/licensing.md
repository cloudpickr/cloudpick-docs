---
title: LLM Licensing and Cost Management
description: FM provider license tiers (Seat/API), 3P reserved capacity, and cost management tools and patterns.
---

> Last reviewed: August 2026

## Seat Plans vs API Tiers

:::note[Prerequisites and related documents]
For foundation model and platform basics, see [Getting Started with AI](../../ai/getting-started/); for where to consume the same FM (1P direct vs 3P via cloud), see the [LLM Channel Selection Guide](../../ai/1p-vs-3p/) first. This document focuses on FM license tiers and cost management.
:::

Seat (per-user) and API (per-token) are separate billing models. Most enterprises use both.

### OpenAI — Seat Plans

| Plan | Price | Audience | Difference from Business |
| --- | --- | --- | --- |
| **Business** (formerly Team) | ~$25/seat/mo | Small teams (2+) | — |
| **Enterprise** | ~$45–75/seat/mo (negotiated, 150+) | Large orgs | SSO/SCIM, RBAC, audit logs, EKM, data residency, custom SLA, HIPAA eligible |

**When to upgrade Business → Enterprise:**
- 150+ seats or security/compliance requirements (SSO mandatory, audit logs, data residency)
- HIPAA-covered data processing
- Org-wide governance (role-based permissions, group credit limits)

### OpenAI — API Tiers

API tiers auto-upgrade based on cumulative spend. ([Official Rate Limits](https://platform.openai.com/docs/guides/rate-limits))

| Tier | Condition | Monthly Limit | RPM/TPM Level |
| --- | --- | --- | --- |
| Free | Allowed region | $100/mo | Low |
| Tier 1 | $5 spent | $100/mo | Medium |
| Tier 2 | $50 spent | $500/mo | Medium+ |
| Tier 3 | $100 spent | $1,000/mo | High |
| Tier 4 | $250 spent | $5,000/mo | High+ |
| Tier 5 | $1,000 spent | $200,000/mo | Maximum |

:::note
For exact per-model RPM/TPM limits, see the [Organization Limits page](https://platform.openai.com/settings/organization/limits).
:::

### Anthropic — Seat Plans

| Plan | Price | Audience | Difference from Team |
| --- | --- | --- | --- |
| **Team Standard** | ~$25/seat/mo ([official pricing](https://claude.com/pricing)) | Small teams (minimum seats/caps per official page) | — |
| **Team Premium** | ~$125/seat/mo ([official pricing](https://claude.com/pricing)) | High-usage teams | Higher usage allowance |
| **Enterprise** | Contract-based — seats + API usage, etc. ([official info](https://claude.com/pricing)) | Large orgs | SCIM, audit logs, Compliance API, CMEK, HIPAA/BAA, org-level spend caps |

### Anthropic — API Tiers

| Tier | Level | Notes |
| --- | --- | --- |
| **Start** | Entry | Low RPM/TPM |
| **Build** | Dev/Test | Medium |
| **Scale** | Production | High RPM/TPM, customizable via Enterprise contract |

Official Rate Limits: [platform.claude.com/docs/en/api/rate-limits](https://platform.claude.com/docs/en/api/rate-limits)

---

## 3P Reserved Capacity

| Vendor | Method | When to Use |
| --- | --- | --- |
| **Azure PTU** (Provisioned Throughput Unit) | Fixed hourly billing, guaranteed throughput | >150–200M tokens/mo steady traffic |
| **Bedrock Provisioned Throughput** | Reserved model units (1/6-month commit) | High-volume steady workloads + latency guarantees |
| **Bedrock On-demand** | Per-token billing, no reservation | Burst/experimental/irregular workloads |

:::note
Reserved capacity (PTU, Provisioned) incurs cost even when idle. Check vendor pricing pages for exact prices and break-even points.
:::

---

## Cost and Usage Management

### Tools by Channel

| Channel | Cost Tracking | Budget/Alerts | Team Allocation |
| --- | --- | --- | --- |
| **OpenAI** | Platform Usage Dashboard | Per-project monthly budget cap | Projects + API Keys |
| **Anthropic** | Console usage dashboard | Per-workspace spend cap | Workspaces |
| **Azure Foundry** | Microsoft Cost Management | Azure Budgets + alerts | Resource tags (`project`, `team`) |
| **Bedrock** | AWS Cost Explorer + CUR 2.0 | AWS Budgets + Cost Anomaly Detection | Inference profiles + cost allocation tags |

### Enterprise Cost Management Patterns

| Pattern | Description |
| --- | --- |
| **Showback** | Visualize team usage without actual chargeback. Awareness building |
| **Chargeback** | Deduct from team budgets. Effective at preventing agent cost runaway |
| **Model Routing** | Simple tasks → lightweight model; complex tasks → frontier model |
| **Token Budgets** | Daily/monthly token caps per project/team/user |
| **AI Gateway** | LiteLLM, Portkey, etc. for virtual key issuance, hard budgets, routing control |

---

## Related Documents

- [LLM Channel Selection Guide](../../ai/1p-vs-3p/) — Channel patterns, Seat vs API
- [AI Platforms and Model Comparison](../../ai/ai-ml/) — Model catalog, inference cost optimization
- [FinOps](../../governance/finops/) — Cloud cost governance
- [Agent Adoption Guide](../../ai/agent-adoption/) — Agent cost management

## References

Seat/API pricing, minimum seats, and tier limits change frequently. Verify against the official pages below.

### Model Providers

- [OpenAI Business/Enterprise Pricing](https://openai.com/business/pricing/)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [Anthropic (Claude) Plans](https://claude.com/pricing)
- [Anthropic API Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Upstage Console](https://console.upstage.ai/)

### Cloud Channels

- [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Azure OpenAI Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
- [Google Cloud Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing)
- [OCI Generative AI Pricing](https://www.oracle.com/artificial-intelligence/generative-ai/generative-ai-service/pricing/)
