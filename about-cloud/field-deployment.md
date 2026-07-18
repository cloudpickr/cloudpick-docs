---
description: 현장 배포 엔지니어(FDE)의 역할, 필요 역량, 그리고 멀티클라우드 환경에서의 실무 지식을 정리합니다.
---

# 현장 배포 (Field Deployment)

> 문서 기준: 2026년 7월

현장 배포 엔지니어(Forward Deployment Engineer, FDE)는 고객 환경에 직접 임베드되어 제품을 프로덕션에 안착시키는 역할입니다. 설계나 자문이 아닌, 실제 프로덕션 코드를 작성하고 소유합니다.

이 문서는 FDE가 멀티클라우드 환경에서 알아야 할 핵심 지식을 정리합니다. CloudPick의 기존 문서를 FDE 관점에서 큐레이션하고, FDE 특화 맥락을 보충합니다.

{% hint style="info" %}
"FDE"라는 타이틀은 조직마다 다를 수 있습니다(Deployment Engineer, Field Engineer, Implementation Engineer 등). 이 문서는 타이틀이 아닌 **역할** — 고객 현장에서 프로덕션 코드를 소유하며 제품을 딜리버리하는 엔지니어 — 을 기준으로 합니다.
{% endhint %}

---

## 역할의 기원과 확산

Palantir가 2000년대 중반, 미국 정보기관에 Gotham을 배포하면서 만든 역할입니다. 기밀 데이터, 미문서화된 스키마, 기존 배포 방식의 실패 → 엔지니어를 고객 현장에 직접 파견하여 문제를 해결하는 모델이 탄생했습니다.

2024년 이후 AI 제품이 같은 문제에 직면하면서 폭발적으로 확산되었습니다. 강력하지만 범용적인 제품(LLM, 에이전트)이 고객의 복잡한 레거시 환경에서 실제 가치를 만들려면, 현장에서 코드를 쓰는 사람이 필요하기 때문입니다.

### 2025-2026 주요 이벤트

| 시기 | 이벤트 | 규모 |
| --- | --- | --- |
| 2026년 5월 | OpenAI Deployment Company 설립 (TPG 주도 투자) | ~$4B |
| 2026년 5월 | Anthropic 엔터프라이즈 서비스 JV "Ode" (Blackstone, Goldman Sachs) | ~$1.5B |
| 2026년 6월 | AWS Forward Deployed Engineering 조직 신설 | ~$1B |
| 2025-2026 | FDE 채용 공고 전년 대비 800%~1,000%+ 증가 | 39+ 기업, 220+ 오픈 포지션 |

---

## FDE vs Solutions Architect

FDE와 SA(Solutions Architect)는 모두 고객과 기술을 연결하지만, 핵심 차이는 **코드 소유권**과 **임베드 깊이**에 있습니다.

| 기준 | Solutions Architect (SA) | Forward Deployment Engineer (FDE) |
| --- | --- | --- |
| **주 활동 시점** | 프리세일 ~ 초기 구현 | 포스트세일 ~ 프로덕션 운영 |
| **핵심 업무** | 아키텍처 설계, 기술 검증, PoC | 프로덕션 코드 작성, 통합, 라이브 운영 |
| **코드 소유** | 낮음 (PoC/데모 수준) | 높음 (프로덕션 코드 직접 소유) |
| **고객 관계** | 자문형 (Advisory) | 임베드형 (Embedded) |
| **산출물** | 아키텍처 다이어그램, 제안서, 통합 가이드 | 프로덕션 코드, 커스텀 통합, 배포 스크립트 |
| **성공 지표** | 세일즈 전환율, 플랫폼 채택률 | 배포 성공률, 시스템 안정성, TTV(Time-to-Value) |
| **보상 (2026 기준)** | $160K-$270K+ TC | $180K-$550K+ TC (프론티어 AI 랩 기준 $1M+) |

### 언제 누구를 채용하는가

- **SA**: 제품의 PMF가 명확하고, 기술적 이의가 딜 성사를 막을 때
- **FDE**: 제품이 강력하지만 고객 환경에서 작동시키려면 맞춤 코드가 필요할 때
- **SI**: 대규모 시스템 구축 프로젝트를 납기 내에 인력 투입으로 완수해야 할 때
- **둘 다**: 대형 엔터프라이즈 계약 — SA가 아키텍처를 설계하고, FDE가 실행

### FDE vs SI (시스템 통합사)

FDE와 SI(System Integrator)는 모두 고객 현장에서 코드를 작성하지만, **목적과 소유 구조**가 다릅니다.

| 기준 | FDE | SI (시스템 통합사) |
| --- | --- | --- |
| **소속** | 제품 회사 (모델사, SaaS 벤더) | 별도 컨설팅/SI 법인 |
| **목적** | 자사 제품을 고객 환경에 안착시키고, 제품 피드백을 본사에 환류 | SOW(작업 명세서) 범위의 시스템을 납기 내 구축·납품 |
| **코드 소유** | 제품 코어에 기여 가능. 재사용 가능한 패턴을 제품에 환류 | 고객 소유. 프로젝트 종료 후 유지보수 계약으로 전환 |
| **기간** | 제품이 안착할 때까지 (수주~수개월, 반복) | SOW 기간 (수개월~수년, 종료 명확) |
| **성공 지표** | 제품 채택률, TTV, 제품 개선에 기여 | 납기 준수, 인수 테스트 통과, 검수 |
| **인력 모델** | 소수 정예 (1~3명) | 대규모 투입 (수십~수백 명) |
| **플레이북** | 없음 (플레이북이 아직 없는 곳에서 일함) | 있음 (방법론, 산출물 템플릿) |
| **제품 피드백** | 핵심 역할 — 현장 문제를 제품 로드맵에 반영 | 제한적 — 벤더와 별도 조직 |

{% hint style="info" %}
한국 시장에서 SI(삼성SDS, LG CNS, SK C&C 등)는 대규모 공공/금융 프로젝트에서 지배적입니다. FDE는 이들과 **경쟁이 아닌 협업** 관계가 많습니다 — SI가 전체 시스템을 구축하고, FDE는 자사 AI/SaaS 제품의 통합 파트를 담당하는 구조입니다.
{% endhint %}

{% hint style="warning" %}
2025-2026 시장에서 "FDE"로 표기된 공고 중 약 40%는 실질적으로 SE(Sales Engineer)나 PS(Professional Services)를 리브랜딩한 것으로 알려져 있습니다. 코드 소유권, 프로덕션 책임, 쿼터/OTE 유무로 구분할 수 있습니다.
{% endhint %}

---

## FDE가 알아야 할 핵심 지식

### 1주차: 고객 환경 진입

고객 환경에 처음 들어갈 때 마주치는 현실입니다. 이 영역은 SA나 일반 SWE가 경험하지 않는, FDE 고유의 과제입니다.

| 과제 | 설명 | 관련 문서 |
| --- | --- | --- |
| 남의 계정에서 일하기 | 고객의 AWS/Azure/GCP 계정에서 최소 권한으로 작업 | [계정과 조직 구조](accounts-and-organizations.md) |
| 협상된 IAM | 고객 보안팀과 조율한 제한된 접근 권한 | [IAM 개요](iam-overview.md) |
| 망분리 환경 | 에어갭, 프록시 전용, 제한된 인터넷 접근 | [망분리와 네트워크 격리](../security/network-isolation.md) |
| 원격 접근 제약 | 고객별 VPN, 배스천 호스트, 제로 트러스트 접근 | [원격 접근 관리](../devops/remote-access.md) |
| 규정 준수 | 고객의 산업별 규제 (금융: PCI-DSS, 의료: HIPAA, 공공: FedRAMP) | [규정 준수](../governance/compliance.md) |

### 인프라와 클라우드

FDE는 고객 환경에 따라 어떤 클라우드든 다룰 수 있어야 합니다.

- [클라우드 시작하기](getting-started.md) — 기본 개념
- [벤더 비교하기](compare-clouds.md) — 같은 기능의 벤더별 차이
- [리전과 가용영역](regions-and-zones.md) — 데이터 주권, 지연 시간
- [공동 책임 모델](shared-responsibility.md) — 고객 환경에서 책임 경계

### 보안과 거버넌스

고객 보안팀은 FDE에게 가장 까다로운 이해관계자입니다.

- [IAM 심화](../security/iam.md) — 크로스 어카운트, 임시 자격 증명
- [시크릿 관리](../security/secrets.md) — 고객 환경의 시크릿 접근
- [데이터 보호](../security/data-protection.md) — 고객 데이터 취급
- [제로 트러스트](../security/zero-trust.md) — 현대 엔터프라이즈 접근 모델
- [랜딩존](../governance/landing-zone.md) — 고객의 클라우드 기반 구조 이해

### 구축과 운영

FDE가 프로덕션 코드를 소유한다면, 운영도 함께 알아야 합니다.

- [DevOps 시작하기](../devops/getting-started.md) — CI/CD, 자동화
- [모니터링](../devops/monitoring.md) → [관찰가능성](../devops/observability.md) — 고객 환경 디버깅
- [SLI/SLO](../devops/slo.md) — 성공 지표 정의
- [재해복구](../governance/dr.md) — 고객 환경 장애 대응
- [보안 사고 대응](../security/incident-response.md) — 사고 시 고객과의 협업

### 데이터와 통합

고객의 데이터를 이해하고 연결하는 것이 FDE 업무의 핵심입니다.

- [데이터베이스 운영](../database/operations.md) — 고객 DB 접근과 연동
- [데이터베이스 마이그레이션](../database/migration.md) — 데이터 이관

### AI/에이전트 배포

2025-2026년 FDE 수요 폭증의 직접 원인입니다.

- [AI 시작하기](../ai/getting-started.md) — AI 제품 이해
- [RAG 고급 패턴](../ai/rag-patterns.md) — 고객 데이터 기반 RAG 구축
- [AI 에이전트](../ai/agents.md) — 에이전틱 워크플로우 배포
- [LLMOps](../ai/llmops.md) — 평가, 비용, 운영, **에이전트 관측**
- [AI 보안](../security/ai-security.md) — 가드레일, 프롬프트 인젝션 방어

---

## FDE의 기술 스택

고객 환경은 모두 다르지만, FDE가 공통적으로 다루는 도구입니다.

| 카테고리 | 도구 |
| --- | --- |
| 언어 | Python, TypeScript, SQL, Go/Java, Bash |
| 백엔드 | FastAPI, NestJS, Spring Boot |
| 프론트엔드 | React, Next.js (운영 대시보드, 고객 포탈) |
| 데이터 | PostgreSQL, Spark, dbt, Airflow, Kafka |
| 클라우드 | AWS, Azure, GCP (EC2, K8s, Lambda, S3 등) |
| 컨테이너 | Docker, Kubernetes, Helm |
| IaC | Terraform, Pulumi, CloudFormation |
| CI/CD | GitHub Actions, GitLab CI, Argo CD |
| 관측 | Datadog, Grafana, Prometheus, Sentry |
| AI/에이전트 | LangGraph, CrewAI, Semantic Kernel, 벡터DB |

---

## 에이전틱 딜리버리로의 전환

2026년 기준, FDE의 업무 방식이 변하고 있습니다.

**이전**: 현장에서 직접 글루코드 작성, 수동 통합, 수 주~수 개월 소요

**현재**: 소규모 인간 팀 + AI 에이전트 조합
- 에이전트가 스캐폴딩, 평가(eval), 장기 워크플로우 수행
- 인간(FDE)은 디스커버리, 거버넌스, 고라이브(go-live) 판단에 집중
- AWS AI-Driven Development Lifecycle이 이 패턴을 공식화

**바뀌지 않는 것**: 고객 환경의 모호성 해결, 이해관계자 설득, 프로덕션 소유권 — 이것들은 자동화되지 않습니다.

---

## 커리어 관점

| 경로 | 설명 |
| --- | --- |
| IC 트랙 | FDE → Senior → Staff/Principal FDE |
| 제품 전환 | 현장 피드백 → PM/TPM (제품 갭을 가장 잘 아는 사람) |
| GTM 리더십 | 기술 영업/배포 조직 리드 |
| 창업 | Palantir FDE 출신 창업자 다수 — 고객 문제를 가장 깊이 아는 위치 |

---

## 참고하기

- [Palantir Forward Deployed Engineering 모델](https://fde.academy/blog/how-palantir-invented-the-forward-deployed-engineer-model)
- [Pragmatic Engineer: Forward Deployed Engineers](https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers)
- [FDE vs Solutions Architect (2026)](https://fde.academy/blog/forward-deployed-engineer-vs-solutions-architect)
- [Forbes: AI Giants Bet Billions On FDE (2026)](https://www.forbes.com/sites/janakirammsv/2026/05/28/ai-giants-bet-billions-on-the-most-expensive-job-in-enterprise/)
- [AWS Forward Deployed Engineering 발표](https://www.aboutamazon.com/news/aws/aws-1-billion-forward-deployed-ai-engineers)
- [FDE Hiring Trends 2026](https://www.paraform.com/blog/forward-deployed-engineer-demand-quadrupled)
