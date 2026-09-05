---
title: AI Agents
description: Concepts, architecture, protocols, vendor platforms, and comparison of coding/desktop/autonomous operations agents.
---

> Last reviewed: August 2026

## From Prompting to Agents

:::note[Prerequisites and related documents]
If you are new to AI, read [Getting Started with AI](../../ai/getting-started/) and [Prompt Engineering](../../ai/prompt-engineering/) first. This document focuses on the concepts, architecture, and vendor platforms of autonomous agents that build on top of them. For organizational adoption strategy, see the [Agent Adoption Guide](../../ai/agent-adoption/).
:::

Traditional LLMs follow a **single prompt → single response** pattern. AI agents have an **autonomous execution loop**: given a goal, they plan, call tools, verify results, and retry if needed.

| Aspect | LLM Prompting | AI Agent |
| --- | --- | --- |
| Execution | Single request-response | Multi-step loop (observe → think → act → repeat) |
| External integration | Limited | Tool calling (APIs, DBs, filesystem) |
| Autonomy | User directs each step | Given a goal, decomposes and executes independently |

**When agents are unnecessary:** Simple Q&A, well-defined pipelines (Step Functions, etc.), real-time response requirements.

---

## Agent Types

| Type | Audience | Examples | Characteristics |
| --- | --- | --- | --- |
| **Desktop Agent** (work) | All employees | Claude Cowork, Amazon Quick, ChatGPT Work, M365 Copilot, Gemini | Local file/app access, Computer Use, MCP connectors |
| **Coding Agent** (dev) | Engineering | Kiro, Claude Code, Codex, Grok Build, Copilot, Antigravity, OpenCode | Terminal/IDE/Git, code gen/edit/test/PR |
| **Autonomous Ops Agent** | DevOps/Security/FinOps | AWS DevOps/Security/FinOps Agent, Security Copilot, Google SecOps Agents | Hours-to-days autonomous execution, no constant human supervision |

### Desktop Agents — Why They Emerged

LLM chat was confined to the browser. Desktop Agents break this limit with local file access, OS manipulation (Computer Use), external tool connection (MCP), and long-running autonomous execution.

| Aspect | Self-hosted (OpenClaw, Hermes, etc.) | Managed (Claude Cowork, Quick, Copilot) |
| --- | --- | --- |
| Deployment | User installs | IT deploys via MDM/SSO |
| Model | Local / personal API key | Vendor-hosted (frontier models) |
| Data control | Local control (hard to enforce org policy) | DLP, connector allowlists, audit logs |
| Advantage | Privacy, customization | Governance, frontier models, enterprise tool integration |

**Claude Cowork status (2026.08):** macOS/Windows GA (April) → web, iOS, Android + cloud remote sessions (July). Chrome side panel integration, cross-device session continuity.

:::note
Enterprise Desktop Agent satisfaction depends more on **IT's data source connectivity scope** than model performance. Systematically setting this up org-wide is AX — see [Agent Adoption Guide](../../ai/agent-adoption/).
:::

### Autonomous Operations Agents

| Domain | AWS | Microsoft | Google Cloud |
| --- | --- | --- | --- |
| Security | Security Agent (GA) | Security Copilot Agents (GA) | Security Operations Agents (Preview) |
| DevOps/SRE | DevOps Agent (GA) | Azure Copilot | — |
| FinOps | FinOps Agent (Preview) | Azure Copilot Cost Optimization | — |
| Coding | Kiro (IDE/CLI/Web) | GitHub Copilot | Antigravity |

---

## Architecture Patterns

| Pattern | Description | When to Use |
| --- | --- | --- |
| **ReAct** | Alternates reasoning and action | Single agent, simple tool calls |
| **Plan-and-Execute** | Full plan then sequential execution | Complex multi-step tasks |
| **Multi-Agent** | Specialized agents collaborate by role | Large workflows, domain separation |
| **Human-in-the-Loop** | Human approval before risky actions | Production, high-risk operations |

---

## Agent Protocols — MCP, A2A, ACP

| Protocol | Role | Key Points |
| --- | --- | --- |
| [MCP](https://modelcontextprotocol.io/) | Agent → Tools/Data | **2026-07-28 spec**: stateless core, Extensions framework, Tasks, MCP Apps. 400M+ monthly SDK downloads |
| [A2A](https://github.com/google-a2a/A2A) | Agent → Agent (cross-vendor) | v1.0 (March 2026 GA). Multi-protocol bindings, signed Agent Cards, 150+ participating orgs |
| [ACP](https://agentcommunicationprotocol.dev/) | Agent → Agent (internal peers) | REST-native, no SDK required |

All three protocols are under [AAIF (Linux Foundation)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) governance.

### MCP 2026-07-28 Key Changes

The largest revision of MCP since launch. Key changes:

- **Stateless core** — Protocol-level sessions (`Mcp-Session-Id`) and `initialize` handshake removed. Serverless/edge deployment now possible
- **Extensions framework** — Reverse-DNS identifiers with independent versioning. Tasks and MCP Apps graduated as official Extensions
- **Tasks** — Standard lifecycle for async long-running operations
- **MCP Apps** — Server-rendered interactive UI sandboxed at the host
- **Authorization hardening** — OAuth 2.1-based authorization improvements
- **Formal deprecation policy** — Roots, Sampling, and Logging marked deprecated

Already supported by AgentCore Gateway and Claude products.

---

## Vendor Agent Platforms

| Vendor | Platform | Strengths |
| --- | --- | --- |
| AWS | [Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) | Framework-agnostic, Harness, Memory, Gateway, MCP |
| Azure | [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/) | Responses API, MCP, Agent 365 governance |
| Google | [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) | ADK (open-source), A2A native, Agent Runtime |
| OCI | [OCI Enterprise AI Agents](https://docs.oracle.com/iaas/Content/generative-ai/agents.htm) | RAG agents, Oracle DB integration, AI Guardrails |

### Open-Source Frameworks

| Framework | Characteristics |
| --- | --- |
| [LangGraph](https://github.com/langchain-ai/langgraph) | State machine-based multi-agent |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Role-based collaboration |
| [Strands Agents](https://strandsagents.com/) | AWS open-source, model-agnostic |
| [AutoGen](https://github.com/microsoft/autogen) | Microsoft, conversational multi-agent |

---

## Coding Agents

| Product | Provider | Characteristics |
| --- | --- | --- |
| [Kiro](https://kiro.dev/) | AWS | Spec-driven, Hooks, IDE/CLI/Web |
| [Claude Code](https://github.com/anthropics/claude-code) | Anthropic | Agent Teams, 29 hooks, plugins |
| [Codex](https://openai.com/codex/) | OpenAI | Parallel agents, Computer Use |
| [Grok Build](https://x.ai/news/grok-build-cli) | SpaceXAI | 8 parallel sub-agents, Git worktree isolation |
| [GitHub Copilot](https://github.com/features/copilot) | Microsoft | Agent Mode, Agent Merge, Cloud Sessions |
| [Antigravity](https://antigravity.google/) | Google | Agent-first IDE, Managed Agents |
| [OpenCode](https://opencode.ai/) | Anomaly | Open-source, model-agnostic |

---

## Deployment and Operations

| Area | Details |
| --- | --- |
| **Cost** | Loop execution consumes 10–100× tokens. Per-task budgets, loop limits, model tiering required |
| **Evaluation** | Task success rate, tool selection accuracy, hallucination rate |
| **Observability** | OpenTelemetry-based tracing. Agent-specific metrics in [LLMOps](../../ai/llmops/) |
| **Security** | Prompt injection, privilege escalation, data exfiltration, infinite loops. Details in [AI Security](../../security/ai-security/) |

### Desktop Agent Risks

| Risk | Mitigation |
| --- | --- |
| Long-running session cost explosion | Session budgets, auto-termination |
| Cross-app injection | Connector allowlists, input sanitization |
| Autonomous agent drift | Checkpoints, kill switch, diff review |
| Shadow AI | Provide equivalent experience via official Desktop Agent |

---

## Checklist

- [ ] Determined whether an agent is actually needed (vs. simple prompting)
- [ ] Least-privilege + allowlist per tool
- [ ] Guardrails (input/output/execution limits)
- [ ] Human-in-the-Loop policy defined
- [ ] Tracing & monitoring (OpenTelemetry)
- [ ] Cost budgets and circuit breakers
- [ ] Adoption strategy per [Agent Adoption Guide](../../ai/agent-adoption/)

## Related Documents

- [Agent Adoption Guide](../../ai/agent-adoption/) — AX strategy, rollout, governance
- [AI Platform and Model Comparison](../../ai/ai-ml/) — model catalog
- [LLMOps](../../ai/llmops/) — agent observability, evaluation, cost
- [AI Security](../../security/ai-security/) — guardrails, prompt injection
- [LLM Channel Selection Guide](../../ai/1p-vs-3p/) — seat vs. API, channel patterns

## References

- [Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Gemini Agent Platform](https://cloud.google.com/products/agent-builder)
- [MCP](https://modelcontextprotocol.io/) · [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) · [A2A](https://github.com/google-a2a/A2A) · [ACP](https://agentcommunicationprotocol.dev/)
- [Kiro](https://kiro.dev/) · [Claude Code](https://github.com/anthropics/claude-code) · [Codex](https://openai.com/codex/)
