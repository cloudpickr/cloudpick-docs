# 기술 지원과 어드바이저

> 문서 기준: 2026년 5월

## 개요

클라우드 운영 중 장애, 아키텍처 문의, 비용 최적화 조언이 필요할 때 벤더의 기술 지원을 받을 수 있습니다. 지원은 크게 **CSP(클라우드 벤더) 직접 지원**과 **MSP(파트너) 지원** 두 가지 경로가 있습니다.

## CSP 지원 플랜

각 벤더 모두 무료 기본 지원 외에 유료 플랜을 제공하며, 플랜에 따라 응답 시간, 지원 범위, 전담 인력(TAM) 배정이 달라집니다.

| 벤더 | 플랜 체계 | 비고 |
| --- | --- | --- |
| AWS | Basic → Business Support+ → Enterprise → Unified Operations | [2027년 1월부터 새 체계 적용](https://aws.amazon.com/blogs/aws/changes-to-aws-support-plans/) |
| Azure | Basic → Developer → Standard → Professional Direct → Unified | |
| GCP | Basic → Standard → Enhanced → Premium | |
| OCI | Basic → Paid (Premier) | Premier는 전담 CSM 배정 |

프로덕션 워크로드를 운영한다면 유료 플랜 가입을 권장합니다. 장애 발생 시 응답 시간이 크게 달라지며, 아키텍처 리뷰나 비용 최적화 조언도 받을 수 있습니다.

## MSP (Managed Service Provider) 파트너

### CSP와 MSP의 역할 차이

| 항목 | CSP (벤더 직접) | MSP (파트너) |
| --- | --- | --- |
| **역할** | 인프라 제공 + 기술 지원 | 고객 환경 운영 대행 + 컨설팅 |
| **지원 범위** | 벤더 서비스에 한정 | 아키텍처 설계, 운영, 비용 최적화, 마이그레이션 등 포괄 |
| **비용** | 지원 플랜 요금 (사용량 비례) | 아래 참조 |

### MSP 비용 구조

MSP는 일반적으로 **클라우드 사용료에 대한 추가 마진을 받지 않습니다**. CSP가 파트너에게 리셀 할인(Base Discount)을 제공하고, MSP는 이 할인분을 수익으로 가져가는 구조입니다. 따라서 고객 입장에서는 MSP를 통해 결제해도 CSP 직접 결제와 동일하거나 유사한 가격입니다.

추가 비용이 발생하는 경우:

- **관리형 운영 서비스** — 24x7 모니터링, 장애 대응, 패치 관리 등 운영 대행
- **컨설팅** — 아키텍처 설계, 마이그레이션 계획, 비용 최적화 프로젝트
- **보안 관제** — SOC 운영, 침해 대응

### MSP를 통해 추가로 할 수 있는 것

- 멀티클라우드 통합 관리 (AWS + Azure 등을 하나의 창구로)
- 한국어 기술 지원 (CSP 직접 지원보다 접근성 높음)
- 세금계산서 발행, 원화 결제
- 비용 리포트, FinOps 컨설팅
- 규제 대응 (CSAP, ISMS-P 등) 지원

## 커뮤니티 지원

유료 플랜 없이도 커뮤니티를 통해 기술 질문에 대한 답변을 받을 수 있습니다. 다른 사용자나 벤더 직원이 답변하며, 일반적인 사용법이나 트러블슈팅에 유용합니다. 다만 응답 시간이 보장되지 않으므로 프로덕션 장애 대응에는 적합하지 않습니다.

| 벤더 | 커뮤니티 | 비고 |
| --- | --- | --- |
| AWS | [re:Post](https://repost.aws/) | Q&A 커뮤니티. 미답변 질문은 AWS 엔지니어에게 에스컬레이션 |
| AWS | [re:Post Knowledge Center](https://repost.aws/knowledge-center) | 자주 묻는 질문 모음 |
| Azure | [Microsoft Q&A](https://learn.microsoft.com/ko-kr/answers/) | 제품별 Q&A |
| Azure | [Tech Community](https://techcommunity.microsoft.com/) | 블로그, 포럼, 이벤트 |
| GCP | [Google Cloud Community](https://www.googlecloudcommunity.com/) | 토론 포럼 |
| GCP | [Stack Overflow (google-cloud 태그)](https://stackoverflow.com/questions/tagged/google-cloud-platform) | 개발 관련 Q&A |

## 어드바이저 / 권장 사항 서비스

각 벤더는 자동으로 환경을 분석하여 비용 절감, 보안 강화, 성능 개선을 권장하는 서비스를 제공합니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Trusted Advisor | 비용, 보안, 성능, 내결함성, 서비스 한도 검사. 상위 플랜에서 전체 검사 가능 |
| Azure | Azure Advisor | 비용, 보안, 안정성, 운영 우수성, 성능 권장 사항 |
| GCP | Recommender / Active Assist | 비용, 보안, 성능, 관리 효율성 권장 사항 |

이 서비스들은 정기적으로 확인하고 권장 사항을 적용하면 비용과 보안 모두 개선할 수 있습니다.

## 응답 시간 SLA

유료 플랜의 가장 큰 차이는 장애 발생 시 응답 시간입니다. 프로덕션 워크로드를 운영한다면 응답 시간을 확인하고 플랜을 선택해야 합니다.

### 심각도별 응답 시간 (4사 비교)

| 심각도 | 설명 | AWS Business Support+ | Azure Professional Direct | GCP Enhanced | OCI Premier |
| --- | --- | --- | --- | --- | --- |
| **위기 (Critical)** | 프로덕션 중단 | < 15분 | < 1시간 | < 1시간 | < 1시간 |
| **긴급 (Urgent)** | 프로덕션 일부 영향 | < 4시간 | < 4시간 | < 4시간 | < 2시간 |
| **일반 (Normal)** | 비프로덕션 영향 | < 12시간 | < 8시간 | < 8시간 | < 6시간 |
| **문의 (Low)** | 일반 질문 | < 24시간 | < 24시간 | < 24시간 | < 24시간 |

> 값은 각 벤더 공식 SLA 기준이며, 플랜 변경 시 달라질 수 있습니다. 정확한 수치는 벤더 공식 문서를 확인하세요.

### TAM (Technical Account Manager) 배정

상위 플랜에서는 전담 기술 계정 관리자가 배정됩니다.

| 벤더 | 플랜 | TAM 역할 |
| --- | --- | --- |
| AWS | Enterprise, Unified Operations | 전담 TAM. 아키텍처 리뷰, 비용 최적화, 운영 지원 |
| Azure | Unified (구 Premier) | Designated Support Engineer |
| GCP | Premium | Technical Account Manager |
| OCI | Premier | Customer Success Manager (CSM) |

## 참고하기

### AWS

- [AWS Support 플랜](https://docs.aws.amazon.com/ko_kr/awssupport/latest/user/aws-support-plans.html)
- [AWS Trusted Advisor](https://docs.aws.amazon.com/ko_kr/awssupport/latest/user/trusted-advisor.html)
- [AWS 파트너 프로그램](https://aws.amazon.com/ko/partners/)

### Azure

- [Azure 지원 플랜](https://learn.microsoft.com/ko-kr/azure/azure-portal/supportability/how-to-create-azure-support-request)
- [Azure Advisor](https://learn.microsoft.com/ko-kr/azure/advisor/)
- [Azure 파트너](https://partner.microsoft.com/ko-kr/)

### GCP

- [Google Cloud 지원](https://cloud.google.com/support/docs)
- [Recommender](https://cloud.google.com/recommender/docs)
- [Google Cloud 파트너](https://cloud.google.com/find-a-partner)

### OCI

- [OCI Support](https://www.oracle.com/cloud/support/)
- [OCI Cloud Advisor](https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/Concepts/cloudadvisoroverview.htm)
- [OCI 파트너](https://www.oracle.com/kr/partnernetwork/)
