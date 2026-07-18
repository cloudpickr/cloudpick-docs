---
title: LLM Licensing and Cost Management
description: FM provider license tiers (Seat/API), 3P reserved capacity, and cost management tools and patterns.
---

## Seat Plans vs API Tiers

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

### Anthropic — Seat Plans

| Plan | Price | Audience | Difference from Team |
| --- | --- | --- | --- |
| **Team Standard** | ~$25/seat/mo | Small teams (5+) | — |
| **Team Premium** | ~$125/seat/mo | High-usage teams | Higher usage allowance |
| **Enterprise** | Negotiated (seat + API usage separate) | Large orgs | SCIM, audit logs, Compliance API, CMEK, HIPAA/BAA, org-level spend caps |

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

## Official Pricing Pages

| Provider | URL |
| --- | --- |
| OpenAI Business/Enterprise | [openai.com/business/pricing](https://openai.com/business/pricing/) |
| OpenAI API | [openai.com/api/pricing](https://openai.com/api/pricing/) |
| Anthropic Plans | [claude.com/pricing](https://claude.com/pricing) |
| Anthropic API | [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Azure OpenAI | [azure.microsoft.com/pricing/details/azure-openai](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) |
| Bedrock | [aws.amazon.com/bedrock/pricing](https://aws.amazon.com/bedrock/pricing/) |

## Related Documents

- [LLM Channel Selection Guide](1p-vs-3p.md) — Channel patterns, Seat vs API
- [AI Platforms and Model Comparison](ai-ml.md) — Model catalog, inference cost optimization
- [FinOps](../governance/finops.md) — Cloud cost governance
- [Agent Adoption Guide](agent-adoption.md) — Agent cost management
