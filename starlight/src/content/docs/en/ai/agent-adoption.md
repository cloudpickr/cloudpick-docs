---
title: Agent Adoption Guide
description: Enterprise adoption strategy, rollout stages, tool selection, and governance for Desktop/Coding/Autonomous agents.
---

:::note
For technical architecture and protocols, see [AI Agents](agents.md).
:::

## Agent Types by Role

| Type | Audience | Examples |
| --- | --- | --- |
| **Desktop Agent** (work) | All employees | Claude Cowork, Amazon Quick, ChatGPT, M365 Copilot, Gemini |
| **Coding Agent** (dev) | Engineering | Kiro, Claude Code, Codex, Grok Build, GitHub Copilot, Antigravity, OpenCode |
| **Autonomous Ops Agent** (IT ops) | DevOps/Security/FinOps | AWS DevOps Agent, Security Copilot, Security Operations Agents |

---

## Rollout Stages

Timelines vary by org size, regulatory environment, and data readiness. Below is a reference framework.

| Stage | Reference Period | Activities |
| --- | --- | --- |
| **1. Foundation** | Weeks | SSO, DLP, allowed connectors, data classification, cost budget, audit logging |
| **2. Pilot** | 1–3 months (1–2 teams) | Apply to repetitive, measurable workflows. Measure time savings, error rates, shadow AI reduction |
| **3. Department Expansion** | Quarterly | Role-specific playbooks + champions. Expand connectors by risk tier |
| **4. Enterprise Rollout** | Ongoing | Desktop (all) + Coding (engineering) + Autonomous Ops (IT) in parallel |

:::caution
**Embed governance from the pilot stage.** Adding governance after adoption makes it far harder to control already-spread shadow AI.
:::

### Pilot Target Selection Criteria

- Repetitive, time-consuming workflows (report writing, data cleanup, internal inquiries)
- Low external-facing / PII processing (internal ops, technical documentation)
- Teams with measurable success metrics
- Change-receptive organizational culture

---

## Tool Selection Criteria

| Existing Ecosystem | Desktop Agent | Coding Agent | Autonomous Ops Agent |
| --- | --- | --- | --- |
| **Microsoft 365** | M365 Copilot | GitHub Copilot, Codex | Security Copilot, Azure Copilot |
| **AWS-centric** | Amazon Quick | Kiro, Claude Code, Codex | DevOps Agent, Security Agent, FinOps Agent |
| **Multi-cloud / Neutral** | Claude Desktop or ChatGPT | Claude Code, Kiro, Codex, Grok Build, OpenCode | Vendor combination |
| **Google Workspace** | Gemini Enterprise | Antigravity, Gemini Code Assist | Security Operations Agents |

:::note
Don't try to cover all roles with one tool. Work agents and coding agents differ in environment, permissions, and risk — separate deployment is standard.
:::

---

## Governance Framework

| Area | Control Methods |
| --- | --- |
| **Access Control** | Enterprise SKU only (block personal Pro), SSO + SCIM, CASB/MDM for unauthorized app blocking |
| **Data Protection** | Connector allowlists, model training disabled, sensitive data classification + access control, DLP integration |
| **Behavioral Boundaries** | Approval policies by access level (read may require approval for sensitive data; write/send/pay requires approval). All prompt/tool-call audit logs |
| **Cost Management** | Seat + usage billing monitoring, model tier limits by role, per-team budget caps |
| **Agent Identity** | Manage agents as non-human identities — least privilege, Policy-Based Access Control |

### Governance Tool Mapping

| Vendor | Agent Governance Tools |
| --- | --- |
| **Microsoft** | Agent 365 (central agent management), Copilot Studio, Entra + Purview |
| **AWS** | Bedrock AgentCore (policy/observability), IAM, CloudTrail, Quick Admin |
| **Google** | Gemini Enterprise Agent Platform (Registry, Gateway, Security Dashboard) |

---

## Measuring Success

| Metric | How to Measure |
| --- | --- |
| **Time savings** | Compare same-task duration before/after pilot |
| **Error rate** | Mistake/rework frequency before/after agent support |
| **Adoption rate** | Active users / deployed seats |
| **Shadow AI reduction** | Unauthorized AI tool usage (CASB logs) |
| **Cost efficiency** | Seat cost vs. productivity gain (time × labor cost) |

---

## Common Mistakes

- **Simultaneous enterprise-wide deployment** — Without governance readiness, deploying to all employees risks data leaks, cost overruns, and shadow AI proliferation.
- **Forcing a single tool** — Developers and non-developers have different environments. Role-specific tool deployment is standard.
- **Unsupervised autonomous agents** — High-risk actions (production changes, security policy modifications) require Human-in-the-Loop policies.
- **Scaling without measuring** — Without quantitative metrics from the pilot, proving ROI becomes impossible.

## Checklist

- [ ] Defined deployment targets per agent type (Desktop/Coding/Autonomous)
- [ ] Using Enterprise SKU; personal account usage blocked
- [ ] Connector/MCP server allowlist defined
- [ ] Behavioral boundaries (read/write/send) configured
- [ ] Approval policies for autonomous agents defined
- [ ] Cost monitoring (seat + usage) configured
- [ ] Pilot success metrics defined
- [ ] Shadow AI detection measures in place

## Related Documents

- [AI Agents](agents.md) — Architecture, protocols, coding agents
- [LLM Channel Selection Guide](1p-vs-3p.md) — Seat vs API, channel patterns
- [AI Security](../security/ai-security.md) — Guardrails, prompt injection
- [FinOps](../governance/finops.md) — Cost governance
