---
title: "AI 에이전트"
description: "AI 에이전트의 개념, 아키텍처, 프로토콜, 벤더 플랫폼, 코딩/Desktop/자율 운영 에이전트를 비교합니다."
---

> 문서 기준: 2026년 7월

## 프롬프팅에서 에이전트로

기존 LLM은 **한 번의 프롬프트 → 한 번의 응답** 구조입니다. AI 에이전트는 **목표를 받으면 스스로 계획하고, 도구를 호출하며, 결과를 검증하고, 필요하면 재시도하는** 자율적 실행 루프를 갖습니다.

| 구분 | LLM 프롬프팅 | AI 에이전트 |
| --- | --- | --- |
| 실행 방식 | 단일 요청-응답 | 다단계 루프 (관찰→사고→행동→반복) |
| 외부 연동 | 제한적 | 도구 호출 (API, DB, 파일시스템) |
| 자율성 | 사용자가 매 단계 지시 | 목표만 주면 스스로 분해·실행 |

**에이전트가 불필요한 경우:** 단순 질의응답, 정형화된 파이프라인(Step Functions 등), 실시간 응답이 필요한 경우.

---

## 에이전트 유형

| 유형 | 대상 | 예시 | 특징 |
| --- | --- | --- | --- |
| **Desktop Agent** (업무) | 전 직원 | Claude Cowork, Amazon Quick, ChatGPT Work, M365 Copilot, Gemini | 로컬 파일·앱 접근, Computer Use, MCP 커넥터 |
| **Coding Agent** (개발) | 엔지니어링 | Kiro, Claude Code, Codex, Grok Build, Copilot, Antigravity, OpenCode | 터미널/IDE/Git, 코드 생성·수정·테스트·PR |
| **자율 운영 에이전트** | DevOps/보안/FinOps | AWS DevOps/Security/FinOps Agent, Security Copilot, Google SecOps Agents | 수 시간–수 일 자율 실행, 사람 상시 감독 없음 |

### Desktop Agent — 왜 등장했는가

LLM 채팅은 브라우저 안에 갇혀 있었습니다. Desktop Agent는 로컬 파일 접근, OS 조작(Computer Use), 외부 도구 연결(MCP), 장시간 자율 실행으로 이 한계를 넘습니다.

| 구분 | 셀프호스팅 (OpenClaw, Hermes 등) | 관리형 (Claude Cowork, Quick, Copilot) |
| --- | --- | --- |
| 배포 | 사용자 직접 설치 | IT가 MDM/SSO로 중앙 배포 |
| 모델 | 로컬/개인 API 키 | 벤더 호스팅 (프론티어 모델) |
| 데이터 통제 | 로컬 제어 (조직 정책 적용 어려움) | DLP, 커넥터 허용 목록, 감사 로그 |
| 장점 | 프라이버시, 커스터마이징 | 거버넌스, 프론티어 모델, 기업 도구 통합 |

:::note
엔터프라이즈 Desktop Agent의 만족도는 **모델 성능보다 IT의 데이터소스 연결 범위**에 좌우됩니다. 이 세팅을 조직 단위로 체계적으로 하는 것이 AX입니다 — [에이전트 도입 가이드](../../ai/agent-adoption/) 참고.
:::

### 자율 운영 에이전트

각 클라우드 벤더가 도메인 특화 자율 에이전트를 출시하고 있습니다. AWS는 "Frontier Agent", Microsoft는 "Copilot Agents", Google은 "AI Agents"로 브랜딩합니다.

| 도메인 | AWS | Microsoft | Google Cloud |
| --- | --- | --- | --- |
| 보안 | Security Agent (GA) | Security Copilot Agents (GA) | Security Operations Agents (프리뷰) |
| DevOps/SRE | DevOps Agent (GA) | Azure Copilot | — |
| FinOps | FinOps Agent (프리뷰) | Azure Copilot 비용 최적화 | — |
| 코딩 | Kiro (IDE/CLI/Web) | GitHub Copilot | Antigravity |

---

## 아키텍처 패턴

| 패턴 | 설명 | 적합한 경우 |
| --- | --- | --- |
| **ReAct** | 추론과 행동을 번갈아 수행 | 단일 에이전트, 단순 도구 호출 |
| **Plan-and-Execute** | 전체 계획 후 순차 실행 | 복잡한 다단계 작업 |
| **멀티에이전트** | 역할별 전문 에이전트 협업 | 대규모 워크플로, 도메인 분리 |
| **Human-in-the-Loop** | 위험한 행동 전 사람 승인 | 프로덕션, 고위험 작업 |

---

## 에이전트 프로토콜 — MCP, A2A, ACP

| 프로토콜 | 역할 | 핵심 |
| --- | --- | --- |
| [MCP](https://modelcontextprotocol.io/) | 에이전트 → 도구/데이터 | JSON-RPC 2.0, Tools/Resources/Prompts. 사실상 표준 |
| [A2A](https://github.com/google/A2A) | 에이전트 → 에이전트 (크로스 벤더) | Agent Card, Task Lifecycle, SSE/gRPC |
| [ACP](https://agentcommunicationprotocol.dev/) | 에이전트 → 에이전트 (사내 피어) | REST 네이티브, SDK 불필요 |

세 프로토콜 모두 [AAIF (Linux Foundation)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) 거버넌스 하에 있습니다.

---

## 벤더별 에이전트 플랫폼

| 벤더 | 플랫폼 | 특징 |
| --- | --- | --- |
| AWS | [Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) | 프레임워크 비종속, Harness, Memory, Gateway, MCP |
| Azure | [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/) | Responses API, MCP, Agent 365 거버넌스 |
| Google | [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) | ADK(오픈소스), A2A 네이티브, Agent Runtime |
| OCI | [OCI Enterprise AI Agents](https://docs.oracle.com/iaas/Content/generative-ai/agents.htm) | RAG 에이전트, Oracle DB 연동, AI Guardrails |

### 오픈소스 프레임워크

| 프레임워크 | 특징 |
| --- | --- |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 상태 머신 기반 멀티에이전트 |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 역할 기반 협업 |
| [Strands Agents](https://strandsagents.com/) | AWS 오픈소스, 모델 비종속 |
| [AG2](https://ag2.ai/) (구 AutoGen) | 커뮤니티 포크, 오픈소스 AgentOS |
| [Microsoft Agent Framework](https://github.com/microsoft/autogen) | AutoGen 후속, 2026.04 GA |

---

## 코딩 에이전트

| 제품 | 제공사 | 특징 |
| --- | --- | --- |
| [Kiro](https://kiro.dev/) | AWS | Spec-driven, Hooks, IDE/CLI/Web |
| [Claude Code](https://github.com/anthropics/claude-code) | Anthropic | Agent Teams, 29 hooks, 플러그인 |
| [Codex](https://openai.com/codex/) | OpenAI | 병렬 에이전트, Computer Use |
| [Grok Build](https://x.ai/news/grok-build-cli) | xAI | 8 병렬 서브에이전트, Git worktree 격리 |
| [GitHub Copilot](https://github.com/features/copilot) | Microsoft | Agent Mode, Agent Merge, Cloud Sessions |
| [Antigravity](https://antigravity.google/) | Google | Agent-first IDE, Managed Agents |
| [OpenCode](https://opencode.ai/) | Anomaly | 오픈소스, 모델 비종속 |

---

## 배포와 운영

| 항목 | 내용 |
| --- | --- |
| **비용** | 루프 실행으로 토큰 수~수십 배 소비. 태스크당 예산, 루프 제한, 모델 계층화 필요 |
| **평가** | 태스크 성공률, 도구 선택 정확도, 환각률. 벤더별 평가 서비스 활용 |
| **관측** | OpenTelemetry 기반 트레이싱. 에이전트 특화 지표는 [LLMOps](../../ai/llmops/) 참고 |
| **보안** | 프롬프트 인젝션, 권한 상승, 데이터 유출, 무한 루프. 상세는 [AI 보안](../../security/ai-security/) 참고 |

### Desktop Agent 고유 리스크

| 리스크 | 대응 |
| --- | --- |
| 장시간 실행 비용 급증 | 세션 예산, 자동 중단 |
| 크로스 앱 인젝션 | 커넥터 허용 목록, 입력 정화 |
| 자율 에이전트 드리프트 | 체크포인트, kill switch, diff 리뷰 |
| 섀도 AI | 공식 Desktop Agent로 동등 경험 제공 |

---

## 체크리스트

- [ ] 에이전트가 필요한 작업인지 판단 (단순 프롬프트로 충분한지)
- [ ] 도구별 최소 권한 + 화이트리스트
- [ ] 가드레일 (입력/출력/실행 제한)
- [ ] Human-in-the-Loop 정책
- [ ] 트레이싱·모니터링 (OpenTelemetry)
- [ ] 비용 예산 및 서킷 브레이커
- [ ] 도입 전략은 [에이전트 도입 가이드](../../ai/agent-adoption/) 참고

## 관련 문서

- [에이전트 도입 가이드](../../ai/agent-adoption/) — AX 전략, 롤아웃, 거버넌스
- [AI 플랫폼과 모델 비교](../../ai/ai-ml/) — 모델 카탈로그
- [LLMOps](../../ai/llmops/) — 에이전트 관측, 평가, 비용
- [AI 보안](../../security/ai-security/) — 가드레일, 프롬프트 인젝션
- [LLM 채널 선택 가이드](../../ai/1p-vs-3p/) — Seat vs API, 채널 패턴

## 참고하기

- [Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Gemini Agent Platform](https://cloud.google.com/products/agent-builder)
- [MCP](https://modelcontextprotocol.io/) · [A2A](https://github.com/google/A2A) · [ACP](https://agentcommunicationprotocol.dev/)
- [Kiro](https://kiro.dev/) · [Claude Code](https://github.com/anthropics/claude-code) · [Codex](https://openai.com/codex/)
