---
description: CloudPick에 오신 것을 환영합니다.
---

# CloudPick Docs

CloudPick은 **멀티클라우드 환경에서 올바른 의사결정을 내리기 위한 벤더 중립 가이드**입니다.

멀티클라우드를 기본값으로 권장하지 않습니다. 단일 벤더, 하이브리드, 멀티클라우드는 각각의 비용과 책임이 있으며, 워크로드와 조직 상황에 따라 선택해야 합니다. 온프레미스와 망분리 중심 운영이 왜 필요했는지 이해하고, 현대 환경에서 통제 방식을 어떻게 확장할 수 있는지 설명합니다.

각 벤더의 공식 문서는 자기 서비스만 설명합니다. CloudPick은 주요 글로벌 클라우드 벤더를 같은 기준으로 나란히 놓고, "이 상황에서 무엇을 선택해야 하는가"를 돕습니다. 모든 내용은 벤더 공식 문서와 업계 표준(NIST, CNCF, FinOps Foundation)을 근거로 하며, 개인 의견이나 추측은 배제합니다.

클라우드를 처음 접하는 분부터 멀티클라우드 아키텍처를 설계하는 분까지, 각자의 수준과 목적에 맞는 읽기 경로를 제공합니다.

{% hint style="info" %}
모든 기술 내용은 벤더 공식 문서 또는 업계 표준 자료를 근거로 합니다. 실제 도입·운영 시에는 각 벤더의 최신 공식 문서를 함께 확인하세요.
{% endhint %}

## 어디서부터 읽을까?

{% tabs %}
{% tab title="☁️ 처음 시작" %}
1. [클라우드 시작하기](about-cloud/getting-started.md)
2. [벤더 비교하기](about-cloud/compare-clouds.md)
3. [리전과 가용영역](about-cloud/regions-and-zones.md)
4. [공동 책임 모델](about-cloud/shared-responsibility.md)
5. [비용 구조 이해하기](about-cloud/pricing-model.md)
6. [멀티클라우드 이해하기](about-cloud/why-multicloud.md)
7. [벤더 선택 의사결정](about-cloud/decision-framework.md)
{% endtab %}

{% tab title="⚙️ 구축·운영" %}
1. [DevOps 시작하기](devops/getting-started.md)
2. [계정과 조직 구조](about-cloud/accounts-and-organizations.md) → [랜딩존](governance/landing-zone.md)
3. [비용 구조](about-cloud/pricing-model.md) → [FinOps](governance/finops.md)
4. [Well-Architected Framework](about-cloud/well-architected.md)
5. [재해복구](governance/dr.md)
6. [모니터링](devops/monitoring.md) → [SLI/SLO](devops/slo.md) → [관찰가능성](devops/observability.md)
7. [원격 접근 관리](devops/remote-access.md)
8. [데이터베이스 운영](database/operations.md)
{% endtab %}

{% tab title="🔒 보안·규제" %}
1. [클라우드 보안 시작하기](security/getting-started.md)
2. [공동 책임 모델](about-cloud/shared-responsibility.md)
3. [IAM 개요](about-cloud/iam-overview.md) → [IAM 심화](security/iam.md)
4. [시크릿 관리](security/secrets.md)
5. [데이터 보호](security/data-protection.md)
6. [망분리와 네트워크 격리](security/network-isolation.md)
7. [제로 트러스트](security/zero-trust.md)
8. [규정 준수](governance/compliance.md)
9. [DevSecOps](devops/devsecops.md)
10. [보안 사고 대응](security/incident-response.md)
{% endtab %}

{% tab title="🚚 마이그레이션" %}
1. [애플리케이션 마이그레이션](compute/migration.md)
2. [데이터베이스 마이그레이션](database/migration.md)
3. [스토리지 마이그레이션](storage/migration.md)
4. [모더나이제이션](compute/modernization.md)
5. [벤더 종속성과 출구 전략](governance/exit-strategy.md)
{% endtab %}

{% tab title="🤖 AI 도입" %}
1. [AI 시작하기](ai/getting-started.md)
2. [AI 플랫폼과 모델 비교](ai/ai-ml.md) — 모델 카탈로그, Applied/Physical AI, 추론 비용
3. [프롬프트 엔지니어링](ai/prompt-engineering.md)
4. [RAG 고급 패턴](ai/rag-patterns.md)
5. [벡터 스토어와 임베딩](ai/vector-store.md)
6. [AI 에이전트](ai/agents.md) — 코딩/Desktop/자율 운영 에이전트
7. [에이전트 도입 가이드](ai/agent-adoption.md) — AX 전략, 롤아웃, 거버넌스
8. [LLM 채널 선택 가이드](ai/1p-vs-3p.md) — 직접 이용 vs 클라우드 제공, Seat vs API
9. [LLM 라이선스와 비용 관리](ai/licensing.md) — 티어, 쿼터, 비용 관리
10. [LLMOps](ai/llmops.md) — 평가, 에이전트 관측, 운영
11. [멀티클라우드 AI](ai/multicloud-ai.md) — 비용, GPU, 벤더 조합
12. [AI 보안](security/ai-security.md) — 가드레일, 프롬프트 인젝션 방어
{% endtab %}

{% tab title="🚀 현장 배포" %}
1. [현장 배포 개요](about-cloud/field-deployment.md) — FDE 역할, SA와의 차이
2. [계정과 조직 구조](about-cloud/accounts-and-organizations.md) — 고객 환경 진입
3. [IAM 개요](about-cloud/iam-overview.md) → [IAM 심화](security/iam.md) — 협상된 접근 권한
4. [망분리와 네트워크 격리](security/network-isolation.md) — 에어갭, 프록시 환경
5. [원격 접근 관리](devops/remote-access.md) — 고객 VPN, 배스천
6. [공동 책임 모델](about-cloud/shared-responsibility.md) — 고객 환경의 책임 경계
7. [모니터링](devops/monitoring.md) → [관찰가능성](devops/observability.md) — 현장 디버깅
8. [AI 에이전트](ai/agents.md) → [LLMOps](ai/llmops.md) — 에이전틱 딜리버리
9. [규정 준수](governance/compliance.md) — 산업별 규제 대응
10. [벤더 종속성과 출구 전략](governance/exit-strategy.md) — 고객의 락인 우려 대응
{% endtab %}
{% endtabs %}

## 대상 클라우드 벤더

| 벤더 | 홈페이지 | 콘솔 |
| --- | --- | --- |
| [AWS](https://aws.amazon.com/ko/) | Amazon Web Services | [Console](https://console.aws.amazon.com) |
| [Azure](https://azure.microsoft.com/ko-kr/) | Microsoft Azure | [Portal](https://portal.azure.com) |
| [Google Cloud](https://cloud.google.com/) | Google Cloud | [Console](https://console.cloud.google.com) |
| [OCI](https://www.oracle.com/kr/cloud/) | Oracle Cloud Infrastructure | [Console](https://cloud.oracle.com) |

클라우드 용어가 낯설다면 [용어집](GLOSSARY.md)을 함께 참고하세요.

---

## 이 문서 다음에는

CloudPick은 <strong>무엇을 선택할지</strong>를 돕는 비교 가이드입니다. 각 서비스의 사용법, 튜토리얼, 핸즈온은 벤더 공식 자료를 병행하세요.

| 벤더 | 공식 학습 플랫폼 | 자격증 |
| --- | --- | --- |
| AWS | [AWS Skill Builder](https://skillbuilder.aws/) | Cloud Practitioner → SA Associate → Specialty |
| Azure | [Microsoft Learn](https://learn.microsoft.com/training/) | AZ-900 → AZ-104/204 → Specialty |
| Google Cloud | [Google Cloud Skills Boost](https://www.cloudskillsboost.google/) | Cloud Digital Leader → Associate → Professional |
| OCI | [OCI Training](https://education.oracle.com/oracle-cloud-infrastructure) | Foundations → Architect Associate → Professional |

각 문서 하단의 **참고하기** 링크도 해당 주제의 공식 문서로 바로 연결됩니다.

---

## 문서 작성 원칙

> CloudPick의 제1원칙입니다. 모든 기여자는 이 원칙을 따릅니다.

- **공식 문서 기반** — 모든 기술 내용은 벤더 공식 문서 또는 업계 표준 자료(NIST, CNCF, FinOps Foundation 등)를 근거로 합니다. 추측성 내용은 배제합니다.
- **중립성** — 벤더를 비교하는 내용은 가능한 한 중립적으로 표현합니다.
- **출처 명시** — 각 문서 하단 **참고하기** 섹션에 공식 문서 링크를 정리합니다.
- **변동성 관리** — 가격, 리전 수, GA/Preview 상태 등 빠르게 바뀌는 정보는 구체적 수치 대신 공식 링크로 안내합니다. 각 문서 상단에 `문서 기준: YYYY년 M월`을 표기합니다.
- **용어 표기** — 한글을 주 표기로 하되, 전문 용어나 약어는 첫 등장 시 영문을 병기합니다 (예: 가용영역(Availability Zone)). 외래어 표기법을 준수합니다 (예: '메시지 큐' ○, '메세지 큐' ✗). 벤더명은 공식 최신 명칭을 사용합니다 (예: Microsoft Entra ID). 정식 표기는 [용어집](GLOSSARY.md)을 따릅니다.
