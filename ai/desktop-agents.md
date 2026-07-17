---
description: AI Desktop Agent와 Frontier Agent의 시장 현황, 개발자/비개발자 도구 구분, 기업 AX 전략을 정리합니다.
---

# AI Desktop Agent와 Frontier Agent

> 문서 기준: 2026년 7월

## 개요

AI 에이전트가 채팅 인터페이스를 넘어 **데스크톱 운영체제, 업무 도구, IT 인프라에 직접 작용**하는 시대입니다. 두 가지 새로운 카테고리가 형성되고 있습니다:

| 카테고리 | 정의 | 대상 |
| --- | --- | --- |
| **Desktop Agent** | 로컬 파일, 앱, 브라우저, 이메일 등에 접근하여 업무를 수행하는 에이전트 | 전 직원 (개발자 포함) |
| **Frontier Agent** | 수 시간–수 일간 자율적으로 목표를 추구하는 전문 에이전트. 사람의 상시 감독 없이 동작 | DevOps, 보안, FinOps 등 도메인 전문가 |

{% hint style="info" %}
Desktop Agent는 **사람이 직접 사용하는 업무 동반자**이고, Frontier Agent는 **IT 시스템을 자율적으로 운영하는 전문가**입니다. 둘 다 [AI 에이전트](agents.md)의 확장이지만 배포·거버넌스·비용 모델이 다릅니다.
{% endhint %}

---

## Desktop Agent 시장

### 주요 제품

| 제품 | 제공사 | 핵심 기능 | 상태 |
| --- | --- | --- | --- |
| **Claude Desktop / Cowork** | Anthropic | MCP 확장, Desktop Extensions, Computer Use, 에이전틱 업무 수행 | GA |
| **Amazon Quick Desktop** | AWS | 로컬 파일 인덱싱, 커넥터(M365/Slack/Salesforce), 리서치, 자동화, Python 샌드박스 | 프리뷰 (2026.04) |
| **ChatGPT Desktop + Work** | OpenAI | Computer Use, 에이전트, 로컬 파일/앱 접근, Deep Research | GA |
| **Codex Desktop** | OpenAI | 개발자 특화. 병렬 에이전트, Git worktree, 스킬/플러그인, MCP | GA |
| **Microsoft 365 Copilot** | Microsoft | M365 깊은 통합 (Word/Excel/PPT/Outlook/Teams), Agent Store, Copilot Studio | GA |
| **Gemini Desktop / Spark** | Google | Workspace 통합, 로컬 파일 작업, 멀티스텝 에이전트 | GA (일부 프리뷰) |

### 개발자 도구 vs 업무 도구

같은 모델을 쓰더라도 **환경과 권한이 다릅니다.**

| | 업무용 Desktop Agent | 개발자용 Coding Agent |
| --- | --- | --- |
| **사용 환경** | 데스크톱 앱, 오피스, 이메일, 파일 | 터미널, IDE, 코드 저장소, CI/CD |
| **작용 대상** | 문서, 프레젠테이션, 캘린더, CRM, 로컬 파일 | 코드베이스, 테스트, PR, 인프라 |
| **대표 제품** | Claude Cowork, Quick Desktop, ChatGPT Work, Copilot | Claude Code, Kiro, Codex, Cursor, Copilot Coding |
| **리스크** | 고객 데이터, 규제 콘텐츠, 외부 발송 | 소스 IP, 시크릿, 프로덕션 변경 |
| **권한 모델** | 커넥터 허용 목록, 읽기 자유/쓰기·발송은 승인 | 파일시스템/네트워크 샌드박스, git 권한 |

{% hint style="info" %}
코딩 에이전트와 Desktop Agent는 **보완 관계**입니다. 엔지니어에게는 코딩 에이전트, 나머지 직원에게는 업무 Desktop Agent를 배포하되, 거버넌스 프레임워크는 통합하는 것이 권장됩니다.
{% endhint %}

---

## Frontier Agent — 자율 운영 에이전트

Frontier Agent는 수 시간–수 일간 자율적으로 목표를 추구하는 도메인 특화 에이전트입니다. 주요 클라우드 벤더가 경쟁적으로 출시하고 있습니다.

### 벤더별 Frontier Agent

| 도메인 | AWS | Microsoft | Google Cloud |
| --- | --- | --- | --- |
| **보안** | [Security Agent](https://aws.amazon.com/security-agent/) (GA 2026.03, Continuum 통합) | [Security Copilot Agents](https://learn.microsoft.com/en-us/copilot/security/agents-overview) (GA, Defender/Entra/Intune/Purview/Sentinel) | [Security Operations Agents](https://cloud.google.com/security/ai-threat-defense) (프리뷰, 위협 분류/헌팅/탐지) |
| **DevOps/SRE** | [DevOps Agent](https://aws.amazon.com/devops-agent/) (GA 2026.03, 멀티클라우드) | [Azure Copilot](https://azure.microsoft.com/en-us/products/copilot) (인프라 운영/마이그레이션) | Agentic SOC (프리뷰) |
| **FinOps/비용** | [FinOps Agent](https://aws.amazon.com/finops-agent/) (프리뷰 2026.06) | Azure Copilot 비용 최적화 | — (별도 브랜드 없음) |
| **코딩** | [Kiro](https://kiro.dev/) (IDE/CLI GA, Web 프리뷰) | [GitHub Copilot](https://github.com/features/copilot) (Agent Mode, Agent Merge) | [Antigravity](https://antigravity.google/) (Agent-first IDE) |

### Kiro 제품군 (AWS)

| 제품 | 설명 |
| --- | --- |
| **Kiro IDE** | VS Code 기반 에이전틱 IDE. Spec-driven 개발, Hooks |
| **Kiro CLI** | 터미널 코딩 에이전트 (구 Amazon Q Developer CLI) |
| **Kiro Web** | 브라우저 기반. 협업 + 자율(Autonomous) 모드 |

### Amazon Q Developer 상태

Q Developer IDE 플러그인/유료 구독은 유지보수 모드 (신규 가입 중단 2026.05, EOS 2027.04). CLI는 Kiro CLI로 대체. AWS 콘솔/모바일/Chat Apps 내 Q는 계속 활성.

### Microsoft Agent 거버넌스

Microsoft는 [Agent 365](https://learn.microsoft.com/en-us/microsoft-365-copilot/agents/) (GA 2026.05)로 조직 내 에이전트를 중앙 관리합니다. Copilot Studio에서 커스텀 에이전트를 빌드하고, Agent Store에서 배포하며, Entra + Purview로 권한/감사를 통합합니다.

### Google Cloud 에이전트 생태계

Google은 [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder)에서 Agent Builder + ADK(오픈소스)로 커스텀 에이전트를 구축하고, 보안 운영에는 Mandiant + Wiz 통합 기반의 Security Operations Agents를 제공합니다.

---

## 기업 AX (AI Transformation) 전략

### 롤아웃 단계

| 단계 | 기간 | 활동 |
| --- | --- | --- |
| **1. 기반 구축** | 4–8주 | SSO, DLP, 허용 커넥터, 데이터 분류, 비용 예산, 감사 로깅 설정 |
| **2. 파일럿** | 6–12주 (1–2개 팀) | 고빈도/저규제 워크플로(운영, 마케팅, 지원) 적용. 시간 절감·오류율·섀도 AI 감소 측정 |
| **3. 부서 확장** | 분기 단위 | 역할별 플레이북 + 챔피언 선정. 리스크 등급별 커넥터 확장 |
| **4. 전사 배포** | 지속 | Desktop Agent(전 직원) + Coding Agent(엔지니어링) + Frontier Agent(IT 운영) 병행 |

{% hint style="warning" %}
**거버넌스를 파일럿 단계부터 내장하세요.** "나중에 붙이겠다"는 접근이 2026년 에이전트 도입 실패의 가장 흔한 패턴입니다.
{% endhint %}

### 도구 선택 기준

| 기존 생태계 | 권장 Desktop Agent | 권장 Coding Agent | 권장 Frontier Agent |
| --- | --- | --- | --- |
| Microsoft 365 중심 | Microsoft 365 Copilot | GitHub Copilot | Security Copilot, Azure Copilot |
| AWS 중심 | Amazon Quick Desktop | Kiro | DevOps Agent, Security Agent, FinOps Agent |
| 멀티클라우드/중립 | Claude Desktop 또는 ChatGPT Desktop | Claude Code, Kiro, Codex | 벤더 조합 |
| Google Workspace 중심 | Gemini Desktop | Gemini Code Assist / Antigravity | Security Operations Agents |

### 거버넌스 프레임워크

| 영역 | 제어 방법 |
| --- | --- |
| **접근** | Enterprise SKU만 허용 (개인 Pro 차단), SSO + SCIM, CASB/MDM |
| **데이터** | 커넥터 허용 목록, 학습 비활성화, 민감 폴더 접근 전 분류, DLP |
| **행동 경계** | 읽기 = 자유, 쓰기/발송/결제 = 승인 필요. 감사 로그 (프롬프트, 도구 호출, 출력) |
| **비용** | Seat + 에이전트 사용 시간 과금 모니터링. 역할별 모델 티어 제한 |
| **에이전트 ID** | 에이전트를 비인간 ID로 관리 — 최소 권한, PBAC. 하드코딩된 앱 ACL은 에이전트 규모에서 깨짐 |

---

## 자주 하는 실수

- **"전사 Day 1 배포"** — 거버넌스 없이 전 직원에게 에이전트를 배포하면 데이터 유출, 비용 폭주, 섀도 AI 확산
- **업무 에이전트에 코딩 에이전트를 강제** — 개발자와 비개발자의 필요 환경이 다름. 하나의 도구로 통일하려 하면 양쪽 모두 불만족
- **Frontier Agent를 사람 승인 없이 운영** — 자율 에이전트라도 고위험 행동(프로덕션 변경, 보안 정책 수정)에는 Human-in-the-Loop 필요

## 체크리스트

- [ ] Desktop Agent와 Coding Agent를 역할별로 분리 배포했는가
- [ ] Enterprise SKU를 사용하고 개인 계정 사용을 차단했는가
- [ ] 커넥터/MCP 서버 허용 목록을 정의했는가
- [ ] 에이전트의 행동 경계(읽기/쓰기/발송)를 설정했는가
- [ ] Frontier Agent의 자율 범위와 승인 정책을 정의했는가
- [ ] 비용 모니터링 (Seat + 사용량)을 설정했는가
- [ ] 파일럿 성과 지표(시간 절감, 오류율, 채택률)를 정의했는가

## 관련 문서

- [AI 에이전트](agents.md) — 에이전트 아키텍처, 프로토콜(MCP/A2A), 코딩 에이전트 상세
- [LLM 채널 선택: 1P vs 3P](1p-vs-3p.md) — Seat vs API, 채널 패턴, 요금제
- [AI 보안](../security/ai-security.md) — 가드레일, 프롬프트 인젝션, CI/CD 에이전트 보안
- [제로 트러스트](../security/zero-trust.md) — 비인간 ID 관리, 워크로드 ID

## 참고하기

- [AWS Frontier Agents](https://aws.amazon.com/ai/frontier-agents/)
- [AWS DevOps Agent](https://aws.amazon.com/devops-agent/)
- [AWS Security Agent](https://aws.amazon.com/security-agent/)
- [AWS FinOps Agent](https://aws.amazon.com/finops-agent/)
- [Kiro](https://kiro.dev/)
- [Amazon Quick Desktop](https://aws.amazon.com/quick/download/)
- [Microsoft Security Copilot Agents](https://learn.microsoft.com/en-us/copilot/security/agents-overview)
- [Google Cloud Security Operations — AI Agents](https://cloud.google.com/security/ai-threat-defense)
