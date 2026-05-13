---
description: CloudPick에 오신 것을 환영합니다.
---

# CloudPick Docs

## 소개

CloudPick은 점점 복잡해지는 클라우드의 개념과 이론을 쉽게 설명하여, 독자가 빠르게 이해하고 실무에 적용할 수 있도록 돕는 것을 목표로 합니다.

{% hint style="info" %}
CloudPick은 AWS, Azure, GCP, OCI를 중심으로 설명하지만, 특정 벤더의 공식 문서를 대체하지 않습니다. 실제 도입·운영 시에는 각 벤더의 최신 공식 문서를 함께 확인하세요.
{% endhint %}

## 문서 작성 원칙

- CloudPick의 글은 빠른 이해를 위해 비유와 단순화된 표현을 사용할 수 있습니다. 벤더 공식 설명과 차이가 있을 경우 각 서비스 벤더의 공식 문서가 우선합니다.
- 용어나 단어들은 벤더 종속적이지 않은 표현을 지향합니다. 다만 특정 벤더에만 있는 개념은 해당 벤더의 용어로 설명할 수 있습니다.
- 벤더를 비교하는 내용은 가능한 한 중립적으로 표현합니다.
- 모든 기술 내용은 벤더 공식 문서 또는 업계 표준 자료(NIST, CNCF, FinOps Foundation 등)를 근거로 합니다. 각 문서 하단의 **참고하기** 섹션에 출처를 정리합니다.

## 변동성 정보 정책

클라우드 환경의 일부 정보는 빠르게 바뀝니다. CloudPick은 다음 원칙을 따릅니다.

- **문서 기준 시점** — 각 문서 상단에 `문서 기준: YYYY년 M월`을 표기합니다. 이 시점 이후 변경이 있을 수 있습니다.
- **변동성이 높은 정보** — 가격, 리전 수, 서비스 GA/Preview 상태, 시장 점유율, 지원 플랜 세부 수치 등은 문서에 구체적 수치보다 **"참고용 근사치"** 또는 **"공식 링크로 안내"** 를 원칙으로 합니다.
- **비교표의 벤더 서비스명** — 리브랜딩이 잦으므로 가능한 한 공식 문서 링크와 함께 제공합니다.
- **독자는 최신 수치가 필요하면 반드시 공식 문서를 재확인하세요.**

## 추천 읽기 순서

목적에 따라 아래 경로를 추천합니다.

### 클라우드를 처음 접하는 분

1. [클라우드란?](about-cloud/what-is-cloud.md)
2. [벤더 비교하기](about-cloud/compare-clouds.md)
3. [리전과 가용영역](about-cloud/regions-and-zones.md)
4. [공동 책임 모델](about-cloud/shared-responsibility.md)

### 멀티클라우드를 검토하는 분

1. [멀티클라우드 이해하기](about-cloud/why-multicloud.md)
2. [벤더 비교하기](about-cloud/compare-clouds.md)
3. [멀티클라우드 네트워킹](about-cloud/multicloud-networking.md) → [멀티클라우드 커넥티비티 (심화)](networking/multicloud-connectivity.md)
4. [IAM 개요](about-cloud/iam-overview.md) → [IAM과 접근 제어 (심화)](security/iam.md)

### 실무 운영을 준비하는 분

1. [계정과 조직 구조](about-cloud/accounts-and-organizations.md) → [랜딩존](governance/landing-zone.md)
2. [비용 구조 이해하기](about-cloud/pricing-model.md) → [FinOps](governance/finops.md)
3. [Well-Architected Framework](about-cloud/well-architected.md)
4. [재해복구](governance/dr.md)
5. [모니터링](devops/monitoring.md) → [통합 관찰가능성](devops/observability.md)
6. [원격 접근 관리](devops/remote-access.md)
7. [패치 관리와 취약점 대응](devops/patch-and-vulnerability.md)

### 보안 강화를 담당하는 분

1. [IAM과 접근 제어](security/iam.md)
2. [시크릿 관리](security/secrets.md)
3. [보안 태세 관리](security/security-posture.md)
4. [DevSecOps](devops/devsecops.md)
5. [규정 준수](governance/compliance.md)

### 마이그레이션/모더나이제이션 계획 중인 분

1. [애플리케이션 마이그레이션](compute/migration.md)
2. [데이터베이스 마이그레이션](database/migration.md)
3. [스토리지 마이그레이션](storage/migration.md)
4. [애플리케이션 모더나이제이션](compute/modernization.md)

### AI 도입을 검토하는 분

1. [클라우드 AI 시작하기](ai/getting-started.md)
2. [AI와 머신러닝 서비스](ai/ai-ml.md)
3. [벡터 스토어와 AI 데이터](ai/vector-store.md)
4. [RAG 고급 패턴](ai/rag-patterns.md)

## 대상 클라우드 벤더

| 벤더 | 홈페이지 | 콘솔 |
| --- | --- | --- |
| [AWS](https://aws.amazon.com/ko/) | Amazon Web Services | [Console](https://console.aws.amazon.com) |
| [Azure](https://azure.microsoft.com/ko-kr/) | Microsoft Azure | [Portal](https://portal.azure.com) |
| [GCP](https://cloud.google.com/) | Google Cloud Platform | [Console](https://console.cloud.google.com) |
| [OCI](https://www.oracle.com/kr/cloud/) | Oracle Cloud Infrastructure | [Console](https://cloud.oracle.com) |

## 빠른 이동

{% content-ref url="about-cloud/what-is-cloud.md" %}
[what-is-cloud.md](about-cloud/what-is-cloud.md)
{% endcontent-ref %}

{% content-ref url="about-cloud/compare-clouds.md" %}
[compare-clouds.md](about-cloud/compare-clouds.md)
{% endcontent-ref %}

{% content-ref url="GLOSSARY.md" %}
[GLOSSARY.md](GLOSSARY.md)
{% endcontent-ref %}

## 용어가 낯설다면

클라우드 용어가 익숙하지 않다면 [용어집](GLOSSARY.md)을 함께 참고하세요.
