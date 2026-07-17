---
description: AI의 산업별 적용(Applied AI), 물리 세계 연결(Physical AI), 에이전틱 앱의 활용 사례를 정리합니다.
---

# AI 활용 패턴

> 문서 기준: 2026년 7월

## Applied AI (산업별 AI 서비스)

AI/ML을 직접 구축하지 않고, 특정 업무에 바로 적용할 수 있는 완성형 AI 서비스입니다.

| 영역 | 예시 | 벤더 서비스 |
| --- | --- | --- |
| 컨택센터 (AICC) | 음성 봇, 실시간 상담 지원 | Amazon Connect, Azure AI Contact Center, Google Cloud CCAI |
| 문서 처리 | OCR, 문서 분류, 데이터 추출 | Textract, Document Intelligence, Document AI |
| 코드 생성 | 코드 자동완성, 리뷰 | Kiro (구 Amazon Q Developer), GitHub Copilot, Gemini Code Assist |
| BI 자연어 질의 | 자연어로 데이터 분석 | Amazon Quick, Copilot in Power BI, Gemini in Looker |

### 2025-2026 Applied AI 주요 변화

**공통 트렌드:** 코파일럿(Copilot)에서 **에이전틱 AI**로 전환 — 사람이 지시하면 돕는 방식에서, 에이전트가 자율적으로 워크플로우를 완수하는 방식으로 이동.

| 영역 | 변화 | 시기 |
| --- | --- | --- |
| **컨택센터** | Amazon Connect에 자율 AI 에이전트 도입 (음성/채팅/이메일/SMS), Nova Sonic 음성(30+ 언어), MCP 기반 도구 접근 | 2025.12 (re:Invent) |
| **산업별 AI** | Amazon Connect가 4개 스위트로 확장: Customer(컨택센터), Decisions(공급망), Talent(채용), Health(헬스케어) | 2026.04 |
| **컨택센터** | Dynamics 365 Contact Center 에이전틱 AI + 옴니채널 강화 | 2025.10–2026.03 |
| **컨택센터** | Google CCaaS 4.0–4.45, Agent Assist Hub로 Knowledge Assist 교체 | 2026.02–07 |
| **문서 처리** | Azure Content Understanding GA — Doc Intelligence + LLM/멀티모달 추론 결합 | 2025.11 |
| **문서 처리** | Google Document AI Gemini Layout Parser — 레이아웃 인식 Markdown 출력 | 2025-2026 |
| **BI** | Amazon QuickSight → **Amazon Quick** 으로 진화 (Quick Sight은 Quick 산하 BI 기능으로 존속) | 2025.10– |
| **BI** | Gemini in Looker — 대화형 분석, 대시보드 에이전트, 에이전틱 워크플로우 | 2025.04–2026 |
| **BI** | Copilot in Power BI — 에이전틱 분석, 웹 모델링 지원 | 2025.07–2026.06 |
| **헬스케어** | Amazon Connect Health (HIPAA) — 환자 검증/스케줄링/임상 노트/의료 코딩 에이전트 | 2026.03 |

---

## Physical AI (물리 세계 AI)

IoT, 로보틱스, 디지털 트윈 등 물리 세계와 연결되는 AI입니다.

| 영역 | 클라우드 연관 서비스 |
| --- | --- |
| IoT + 엣지 추론 | AWS IoT Greengrass, Azure IoT Operations, Google Cloud Edge TPU |
| 디지털 트윈 | AWS IoT TwinMaker, Azure Digital Twins, NVIDIA Omniverse |
| 로보틱스 시뮬레이션 | NVIDIA Isaac / Omniverse (클라우드 GPU), Nebius Physical AI Cloud |
| 안전 시스템 | NVIDIA Halos for Robotics |

### 2025-2026 Physical AI 주요 변화

| 영역 | 변화 | 벤더 |
| --- | --- | --- |
| **로보틱스 시뮬레이션** | 오픈 모델(Cosmos, GR00T) 공개, 데이터 팩토리 참조 아키텍처 제공 | NVIDIA (Azure/Nebius에서 호스팅) |
| **엣지 디바이스** | Greengrass C/C++/Rust SDK (<0.5MB), 비루트 설치 — 리소스 제약 디바이스 대응 | AWS (2026.04) |
| **엣지 운영** | IoT Operations 2603 — 클라우드→엣지 관리, 노코드 데이터플로우, 엣지 ML 추론 | Azure (2026.04) |
| **안전** | 로보틱스용 풀스택 안전 시스템(Halos) 출시 | NVIDIA (2026.06) |
| **제조 디지털 트윈** | 주요 OEM(FANUC, ABB, KUKA 등)이 시뮬레이션 기반 가상 커미셔닝 도입 | 멀티 벤더 |

{% hint style="info" %}
Physical AI는 클라우드 서비스만으로 완성되지 않습니다. 시뮬레이션 플랫폼(NVIDIA Omniverse/Isaac 등), 클라우드 GPU 인프라, 엣지 배포 런타임, 디지털 트윈 서비스가 결합됩니다. 각 서비스의 최신 현황은 공식 문서를 확인하세요.
{% endhint %}

---

## Agentic Apps (AI 에이전트)

자율적으로 도구를 호출하고 멀티스텝 작업을 수행하는 AI 앱입니다.

| 사례 | 동작 방식 |
| --- | --- |
| 코딩 에이전트 | 버그 리포트를 받으면 코드를 분석·수정·테스트 후 PR 생성 |
| 고객 지원 에이전트 | 문의 분류 → CRM 조회 → 환불 처리 → 결과 이메일 발송 |
| 데이터 분석 에이전트 | 자연어 질문 → SQL 변환 → 실행 → 시각화 보고서 생성 |

{% hint style="info" %}
벤더별 에이전트 플랫폼, 코딩 에이전트, 프로토콜(MCP/A2A/ACP) 상세는 [AI 에이전트](agents.md)를, Desktop Agent와 자율 운영 에이전트는 [Desktop Agent와 자율 운영 에이전트](desktop-agents.md)를 참고하세요.
{% endhint %}

## 관련 문서

- [AI 플랫폼과 모델 비교](ai-ml.md) — 모델 카탈로그, ML 플랫폼, 추론 비용
- [AI 에이전트](agents.md) — 에이전트 아키텍처, 프로토콜, 코딩 에이전트
- [Desktop Agent와 자율 운영 에이전트](desktop-agents.md) — Desktop Agent, Frontier Agent
- [에이전트 도입 가이드](agent-adoption.md) — AX 전략, 롤아웃
