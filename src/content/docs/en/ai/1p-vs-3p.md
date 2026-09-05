---
title: LLM Channel Selection Guide
description: Compare consuming FMs directly (1P) vs. through cloud platforms (3P), and Seat vs. API usage patterns.
---

> Last reviewed: August 2026

## Overview

When adopting FMs, there are **two independent decisions**:

| Decision Axis | Question | Options |
| --- | --- | --- |
| **① Usage Type** | Who uses it and how? | Seat (chat UI) / API (code integration) / Self-hosting |
| **② Channel** | Where do you buy and operate? | Direct (1P) / Cloud-hosted (3P) / Provider + Cloud billing |

```
Example: "Claude via API on Bedrock"
     → Usage type: API
     → Channel: Cloud-hosted (3P Inference)

Example: "ChatGPT Enterprise for all employees"
     → Usage type: Seat (Enterprise)
     → Channel: Direct (1P)
```

---

## ① Usage Type: Seat vs API

| Aspect | Seat Plans | API Plans |
| --- | --- | --- |
| **User** | Individual employees (incl. developers) | Applications, services, automation systems |
| **How** | Use provider-built UI/tools directly (chat, Claude Code, Copilot) | Embed model programmatically in your product/service |
| **Billing** | Per-user subscription | Per-token/request usage-based |
| **Best for** | Personal productivity — writing, analysis, coding, research | Customer-facing features, large-scale automation, batch processing |
| **Control** | User/group/admin policies | API keys, per-project budgets, rate limits |
| **Cost predictability** | Seats × price = fixed | Variable with usage |

:::caution
**"Seat = non-developers, API = developers" is wrong.** Developers use coding agents (Claude Code, Copilot) on Seat plans. The key distinction is **human uses directly** (Seat) vs. **embedded in systems** (API).
:::

### Why Choose 3P for API Usage

| Reason for 3P | Explanation |
| --- | --- |
| **Consume existing cloud commits** | AWS EDP, Azure EA/MACC can offset LLM costs |
| **Network isolation** | VPC/PrivateLink — traffic stays off public internet |
| **Compliance leverage** | Reuse cloud vendor's existing certifications (HIPAA, SOC 2, etc.) |
| **Unified billing/governance** | Single invoice, cost tags for team tracking, IAM access control |
| **Single contract** | No procurement effort for new vendor |
| **Multi-model access** | Switch between models via same platform API |

| Reason to stay 1P | Explanation |
| --- | --- |
| **Latest models/features** | New models and beta features ship to 1P first |
| **Full functionality** | Fine-tuning, Realtime API, etc. may lag or be absent on 3P |
| **Simple start** | Register card, start immediately, no cloud setup |
| **Cloud-agnostic** | No dependency on specific cloud |

:::note
Common enterprise pattern: **Production on 3P** (governance, commit consumption, isolation) + **Experimentation on 1P** (latest features, fast start).
:::

---

## ② Channel: Where to Buy and Operate

### Channel Architecture Patterns

| Pattern | Analogy | Operator | Billing | Feature Scope |
| --- | --- | --- | --- | --- |
| **A. Direct (1P)** | Brand store | Model provider | Provider direct | Full (latest first) |
| **B. Provider service + Cloud billing** | Department store brand shop | Model provider | Cloud marketplace (commit-eligible) | Full (same as 1P) |
| **C. Cloud-hosted (3P Inference)** | Private-label/select shop | Cloud vendor | Cloud invoice | Cloud API scope (some features delayed) |
| **D. Self-hosting (open-weight)** | Cook it yourself | Customer | Infrastructure costs (GPU/server) | Full customization within license |

### Provider-Channel Mapping

| Provider | A. Direct | B. Provider + Cloud billing | C. Cloud-hosted (3P) | D. Self-hosting |
| --- | --- | --- | --- | --- |
| **OpenAI** | api.openai.com (Enterprise) | — | Azure Foundry, Bedrock | ✗ (closed weights) |
| **Anthropic** | api.anthropic.com (Enterprise) | Claude Platform on AWS (CCU billing) | Bedrock Claude, Vertex AI Claude | ✗ (closed weights) |
| **Meta Llama** | — | — | Bedrock, Vertex, Azure (hosted) | ✅ open-weight (primary path) |
| **Mistral** | api.mistral.ai | — | Bedrock, Azure, Vertex | ✅ open-weight (partial) |

### Pattern Comparison

| Aspect | A. Direct | B. Provider + Cloud billing | C. Cloud-hosted | D. Self-hosting |
| --- | --- | --- | --- | --- |
| New model availability | First | Near-simultaneous | Days to weeks delay | When open-weight released |
| Feature scope | Full | Full | Within cloud API | None (build yourself) |
| Fine-tuning | Full options | Full options | Limited or delayed | Complete freedom (own GPU) |
| VPC/Network isolation | Enterprise only | Within marketplace | Supported (check region/service) | Full isolation (own infra) |
| Commit consumption | No | Yes | Yes | No (infra costs only) |
| Operational burden | None | None | Low | High (GPU, model serving, updates) |

:::note
For details on **Pattern D (self-hosting/open-weight)** — representative models, reasons to choose it, and license caveats — see [AI Platforms and Model Comparison](../../ai/ai-ml/).
:::

### Real-World Example: "We Want to Use Claude Code"

| Requirement | Suitable Pattern |
| --- | --- |
| Latest Claude Code + fast updates | **A. Direct** |
| Claude Code + consuming AWS EDP + AWS invoice | **B. Provider service + Cloud billing** (Claude Platform on AWS) |
| Claude API only + VPC isolation + existing AWS governance | **C. Cloud-hosted** (Bedrock Claude) |

:::caution
**Pattern B is not offered by every provider.** Anthropic's "Claude Platform on AWS" is the representative example; OpenAI currently has no equivalent separate offering. Check the provider-channel mapping table above for what each provider offers.
:::

---

## Channel Availability by Major FMs

For the list of models and available channels by provider, see [AI Platforms and Model Comparison](../../ai/ai-ml/). For Korean FMs (Upstage, EXAONE, etc.), see [FM Provider Comparison (Korea)](../../korea/ai/fm-providers/). For the pattern comparison table, use the **Pattern Comparison** section above.

---

## Selection Guide (Evaluation Criteria)

Don't fix your 1P/3P choice based on monthly spend alone. Work through the criteria below first, then choose a channel.

| Criteria | 1P (Direct) favored when | 3P (Cloud-hosted) favored when |
| --- | --- | --- |
| **Features & release speed** | Latest models/agent features are needed immediately | Platform API scope is sufficient; a days-to-weeks delay is acceptable |
| **Network & compliance** | Enterprise-grade isolation is sufficient | VPC/regional governance or inheriting existing certifications is required |
| **Procurement & commits** | Little to no existing cloud commit | Significant EDP/EA/CUD commit consumption |
| **Operations** | Comfortable operating the provider's own console | Needs integration with existing cloud IAM, observability, and budget systems |
| **Scale & quota** | PoC/small scale, quota headroom | Production traffic, reserved capacity, private offer negotiation |

:::caution
At large scale (roughly tens of thousands of dollars per month or more), **procurement structure** (commit consumption, reserved capacity, private offers) is often a bigger cost factor than per-token pricing. Dollar thresholds vary by organization, so confirm with official quotes and contract terms.
:::

---

## Channel Choice by Country

For channel choice driven by country-specific regulation and sovereignty requirements, see each country guide.

- [Korea](../../korea/) · [FM Provider Comparison (Korea)](../../korea/ai/fm-providers/)
- [United States](../../us/) · [EU](../../eu/) · [Japan](../../japan/) · [Singapore](../../singapore/)

---

## Pricing Plans and Cost Management

Each provider's license tiers (Seat plans, API tiers), 3P reserved capacity (PTU, Provisioned Throughput), and cost management tools and patterns are covered in [LLM Licensing and Cost Management](../../ai/licensing/).

---

## Common Mistakes

- **Assuming "3P is expensive"** — Published per-token rates are usually similar. With existing cloud commits, 3P may be cheaper in effective cost.
- **All-in on a single channel** — 1P only = weak cloud governance integration; 3P only = delayed access to latest features. Evaluate a hybrid approach.
- **Not considering quotas upfront** — Production traffic without pre-secured quota/rate limits leads to service outages.

## Checklist

- [ ] Estimated monthly token consumption
- [ ] Checked for existing cloud commits (EDP/EA/CUD)
- [ ] Documented data residency and isolation requirements against the target jurisdiction (see country guides)
- [ ] Confirmed required features (fine-tuning, agents, real-time) are available on chosen channel
- [ ] Verified quota/rate limits can handle production traffic
- [ ] Model version sync strategy for hybrid (1P+3P) operations

## Related Documents

- [AI Platforms and Model Comparison](../../ai/ai-ml/) — vendor FM catalog, GPU/accelerators
- [Multi-cloud AI](../../ai/multicloud-ai/) — vendor combination strategy
- [LLMOps](../../ai/llmops/) — cost tracking, evaluation, operations
- [FinOps](../../governance/finops/) — cloud cost governance

## References

### Model Providers

- [OpenAI API Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [Anthropic Claude Plans & Pricing](https://claude.com/pricing)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Upstage Console](https://console.upstage.ai/)

### Cloud Channels

- [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Azure AI Foundry Quotas and Limits](https://learn.microsoft.com/en-us/azure/foundry/openai/quotas-limits)
- [Azure OpenAI Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
- [Vertex AI Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs)
