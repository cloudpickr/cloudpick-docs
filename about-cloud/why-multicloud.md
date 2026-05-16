---
description: 멀티클라우드의 정의, 도입 동기, 채택 현황과 주요 과제를 설명합니다.
---

# 멀티클라우드 이해하기

> 문서 기준: 2026년 5월

## 멀티클라우드란

멀티클라우드는 **둘 이상의 퍼블릭 클라우드 벤더를 의도적으로 조합하여 운영하는 전략**입니다. 단순히 여러 벤더의 계정을 보유하는 것이 아니라, 워크로드를 목적에 맞게 분산 배치하고 통합 운영하는 것을 의미합니다.

{% hint style="info" %}
ISO/IEC 22123-1은 멀티클라우드를 다음과 같이 정의합니다.

> "둘 이상의 클라우드 서비스 제공자가 제공하는 퍼블릭 클라우드 서비스를 사용하는 클라우드 배포 모델"
{% endhint %}

비슷해 보이지만 다른 개념들과 구분해 봅시다.

| 전략 | 정의 | 예시 |
| --- | --- | --- |
| **멀티클라우드** | 2개 이상의 퍼블릭 클라우드를 조합 | AWS(컴퓨팅) + GCP(AI/ML) |
| **하이브리드 클라우드** | 온프레미스 + 퍼블릭 클라우드를 연결 | 사내 DC + AWS Direct Connect |
| **멀티 계정** | 단일 벤더 내에서 여러 계정을 운영 | AWS Organizations로 dev/staging/prod 분리 |

{% hint style="info" %}
실무에서는 이 세 가지가 겹치는 경우가 많습니다. "온프레미스 + AWS + GCP"를 운영한다면 하이브리드이면서 동시에 멀티클라우드입니다.
{% endhint %}

## 채택 현황

멀티클라우드는 이미 주류 전략입니다.

- CNCF Annual Survey 2024에 따르면, 기업의 약 60%가 2개 이상의 클라우드를 사용하고 있습니다.
- Flexera 2024 State of the Cloud Report는 기업의 89%가 멀티클라우드 전략을 채택했다고 보고합니다.

## 도입 동기

### 벤더 종속(Lock-in) 회피

단일 벤더에 모든 워크로드를 집중하면 가격 협상력이 약해지고, 벤더의 정책 변경에 취약해집니다. 멀티클라우드는 협상 카드를 확보하고, 장기적으로 이전 가능성을 열어둡니다.

### 규제와 데이터 주권

국가별 규제에 따라 특정 데이터를 특정 지역에 저장해야 하거나, 인증된 벤더만 사용해야 하는 경우가 있습니다. 이로 인해 워크로드를 여러 벤더에 분산 배치하는 구성이 발생합니다.

### 서비스 특화 (Best-of-Breed)

각 벤더의 강점을 조합하는 전략입니다.

- **AI/ML**: GCP Vertex AI + BigQuery로 학습, AWS SageMaker AI로 서빙
- **데이터 분석**: GCP BigQuery(분석) + AWS S3(저장)
- **엔터프라이즈**: Azure Entra ID(ID 통합) + AWS(인프라)
- **DB 중심**: OCI Autonomous DB + AWS(앱 서버)

### M&A와 조직 통합

인수합병 시 피인수 기업이 다른 벤더를 사용하고 있으면, 즉시 통합보다 멀티클라우드로 공존하는 것이 현실적입니다.

### 가용성과 재해복구

단일 벤더의 글로벌 장애에 대비하여 핵심 서비스를 다른 벤더에 대기(standby) 배치하는 패턴입니다. 다만 비용과 복잡도가 높아 실제로 이 목적만으로 멀티클라우드를 도입하는 경우는 드뭅니다.

## 도전 과제

멀티클라우드는 공짜가 아닙니다. 아래의 비용을 감수할 준비가 되어 있는지 먼저 확인하세요.

### 운영 복잡도 증가

- 벤더마다 다른 네트워크 모델, IAM 체계, 모니터링 도구
- IaC(Terraform 등)로 추상화해도 벤더별 차이를 완전히 숨길 수 없음
- 장애 발생 시 원인 파악이 단일 벤더 대비 어려움

### 팀 역량 분산

- 엔지니어가 2\~3개 벤더를 모두 깊이 있게 다루기 어려움
- "AWS 팀 / Azure 팀"으로 사일로가 생기면 통합 운영의 이점이 사라짐
- 채용 시 멀티클라우드 경험자 풀이 좁음

### 이그레스 비용

클라우드 간 데이터 이동에는 이그레스(outbound) 요금이 발생합니다. 대량의 데이터를 클라우드 간에 주고받는 아키텍처는 비용이 급격히 증가할 수 있습니다. 벤더별 무료 범위와 단가는 [비용 구조 이해하기](pricing-model.md)를 참고하세요.

{% hint style="info" %}
전용 연결(Direct Connect, ExpressRoute 등)을 사용하면 이그레스 단가가 낮아지지만, 회선 비용이 추가됩니다.
{% endhint %}

### 관찰가능성(Observability) 분산

- 각 벤더의 모니터링 도구(CloudWatch, Azure Monitor, Cloud Monitoring)가 분리됨
- 통합 관찰을 위해 Datadog, Grafana Cloud 등 3rd party 도구 도입이 사실상 필수
- 분산 추적(Distributed Tracing)이 클라우드 경계를 넘을 때 복잡해짐

### 보안 경계 확장

- 공격 표면(Attack Surface)이 벤더 수만큼 증가
- 통합 ID 관리(Okta, Entra ID 등)를 도입하지 않으면 계정 관리가 파편화됨
- 컴플라이언스 감사 범위가 넓어짐

### Day-2 운영 부담

초기 구축(Day-1) 이후의 지속적 운영(Day-2)에서 멀티클라우드의 복잡도가 드러납니다.

- **이중 IAM 감사** — 벤더별로 별도의 권한 리뷰, 미사용 계정 정리, 정책 감사를 수행해야 함
- **장애 소유권** — 클라우드 간 통신 장애 시 어느 벤더의 문제인지 판별이 어려움. 양쪽 벤더에 동시에 티켓을 열어야 하는 경우 발생
- **패치/업데이트 조율** — 벤더별 유지보수 일정이 다르므로, 동시 장애 가능성을 고려한 변경 관리 필요
- **비용 거버넌스** — 벤더별 빌링 체계가 달라 통합 비용 분석이 어려움. FinOps FOCUS 스펙 등 표준화 도구 필요

## 언제 멀티클라우드를 하지 말아야 하는가

다음 상황에서는 단일 벤더에 집중하는 것이 더 나은 선택입니다.

| 상황 | 이유 |
| --- | --- |
| 팀 규모가 작다 (10명 이하) | 멀티클라우드 운영 오버헤드를 감당할 여력이 없음 |
| 명확한 규제 요건이 없다 | 벤더 분리의 동기가 약함 |
| 데이터 이동이 빈번한 아키텍처 | 이그레스 비용이 이점을 상쇄 |
| 벤더 고유 서비스에 깊이 의존 | 추상화 비용이 너무 높음 (예: DynamoDB, Cosmos DB) |
| "남들이 하니까" | 전략 없는 멀티클라우드는 복잡도만 증가 |

{% hint style="warning" %}
**핵심 원칙:** 멀티클라우드는 목적이 아니라 수단입니다. "왜 여러 벤더를 써야 하는가?"에 명확한 답이 없다면, 단일 벤더에서 잘 운영하는 것이 더 좋은 전략입니다.
{% endhint %}

## 멀티클라우드를 시작하기 전 체크리스트

멀티클라우드 도입을 검토 중이라면, 아래 질문에 답해 보세요.

- [ ] 멀티클라우드를 도입해야 하는 구체적인 비즈니스/규제 이유가 있는가?
- [ ] 각 벤더에 배치할 워크로드의 기준이 명확한가?
- [ ] 클라우드 간 네트워크 연결 방식과 비용을 검토했는가?
- [ ] 통합 ID 관리(IdP 페더레이션) 전략이 있는가?
- [ ] 통합 모니터링/관찰가능성 도구를 선정했는가?
- [ ] IaC로 멀티 벤더를 관리할 역량이 있는가?
- [ ] 팀이 2개 이상의 벤더를 운영할 수 있는 규모인가?

---

## 참고하기

### AWS

- [AWS — Prescriptive Guidance: Strategy for multicloud](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-multicloud/welcome.html)

### Azure

- [Azure — Cloud Adoption Framework](https://learn.microsoft.com/azure/cloud-adoption-framework/)

### GCP

- [Google Cloud — Hybrid and Multi-cloud Reference Architectures](https://cloud.google.com/architecture/network-hybrid-multicloud)

### OCI

- [OCI — Multicloud Solutions](https://docs.oracle.com/en/solutions/oci-best-practices/deploy-multicloud-oci-oracle-database-services1.html)

### 표준 및 커뮤니티

- [ISO/IEC 22123-1 — Cloud computing: Concepts and terminology](https://www.iso.org/standard/82758.html) — 멀티클라우드 공식 정의
- [ISO/IEC 22123-3 — Multi-cloud reference architecture](https://www.iso.org/standard/90339.html) — 멀티클라우드 레퍼런스 아키텍처 표준
- [NIST SP 500-292 — Cloud Computing Reference Architecture](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture) — 클라우드 레퍼런스 아키텍처
- [NIST Multi-Cloud Security Public Working Group](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture) — 멀티클라우드 보안 레퍼런스
- [CNCF Annual Survey 2024](https://www.cncf.io/reports/cncf-annual-survey-2024/) — 클라우드 네이티브 채택 현황, 멀티클라우드 통계
- [FinOps Foundation — FOCUS Specification](https://finops.org/framework) — 멀티클라우드 비용 데이터 표준화
- [Cloud Security Alliance — Security Guidance](https://cloudsecurityalliance.org/research/guidance) — 멀티클라우드 보안 가이드
