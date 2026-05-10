---
description: FinOps 라이프사이클, 비용 관리 도구, 실무 적용 순서, FOCUS 스펙을 4사 비교합니다.
---

# FinOps

> 문서 기준: 2026년 5월

## FinOps란

FinOps(Cloud Financial Operations)는 [FinOps Foundation](https://www.finops.org/)에서 정의한 클라우드 비용 관리 프레임워크입니다. 엔지니어링, 재무, 비즈니스 팀이 협력하여 클라우드 비용의 가시성을 확보하고 최적화하는 것을 목표로 합니다.

FinOps의 3단계 라이프사이클:

| 단계 | 설명 |
| --- | --- |
| **Inform** | 비용 가시성 확보 — 누가, 무엇에, 얼마를 쓰고 있는지 파악 |
| **Optimize** | 비용 최적화 — 사이징, 예약, 스팟 활용, 미사용 리소스 제거 |
| **Operate** | 지속적 운영 — 예산 설정, 이상 탐지, 거버넌스 자동화 |

{% hint style="info" %}
FinOps는 단순히 비용을 줄이는 활동이 아닙니다. 필요한 곳에는 비용을 쓰되, 비용과 비즈니스 가치의 관계를 투명하게 만드는 운영 방식입니다.
{% endhint %}

## 주요 CSP 비용 관리 도구 비교

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| 비용 분석 | [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) | [Microsoft Cost Management](https://azure.microsoft.com/en-us/products/cost-management) | [Cloud Billing Reports](https://cloud.google.com/billing/docs/reports) | [OCI Cost Analysis](https://docs.oracle.com/iaas/Content/Billing/Concepts/costanalysisoverview.htm) |
| 예산/알림 | [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/) | [Azure Budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets) | [Budget Alerts](https://cloud.google.com/billing/docs/how-to/budgets) | [OCI Budgets](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm) |
| 추천/어드바이저 | [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/) | [Azure Advisor](https://azure.microsoft.com/en-us/products/advisor) | [Recommender](https://cloud.google.com/recommender/docs/overview) | [Cloud Advisor](https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/Concepts/cloudadvisoroverview.htm) |
| 비용 할당 | Cost Allocation Tags | Cost Allocation (Tags + Subscriptions) | Labels + Billing Account | Cost Tracking Tags + Compartments |

## 실무 적용 순서

FinOps를 처음 시작할 때는 도구를 많이 도입하기보다, 비용을 설명할 수 있는 최소 기준을 먼저 만드는 것이 중요합니다.

| 단계 | 해야 할 일 | 산출물 |
| --- | --- | --- |
| 1 | 계정/구독/프로젝트 구조 정리 | 비용 소유 조직 매핑 |
| 2 | 태그/라벨 표준 정의 | `service`, `env`, `owner`, `cost-center` 등 |
| 3 | 예산과 알림 설정 | 월별 예산, 임계치 알림 |
| 4 | 큰 비용 항목부터 최적화 | 미사용 리소스, 과대 사이징, 스토리지 클래스 |
| 5 | 예약/약정 할인 검토 | RI, Savings Plans, CUD 등 |

## 자주 보는 비용 최적화 항목

- **컴퓨팅 사이징** — CPU/메모리 사용률이 낮은 VM을 축소하거나 종료합니다.
- **스케줄링** — 개발/테스트 환경은 업무 시간 외 자동 중지합니다.
- **스토리지 수명주기** — 오래된 로그와 백업은 저렴한 스토리지 클래스로 이동합니다.
- **이그레스 비용** — 리전 간, 클라우드 간 데이터 전송 경로를 점검합니다.
- **약정 할인** — 안정적으로 사용하는 베이스라인 워크로드에 예약/약정을 적용합니다.

{% hint style="warning" %}
비용 최적화는 보안, 가용성, 성능을 훼손하지 않는 범위에서 진행해야 합니다. 특히 백업 보관 기간이나 DR 구성을 비용만 보고 줄이면 장애 시 더 큰 손실이 발생할 수 있습니다.
{% endhint %}

## FOCUS 스펙

[FOCUS(FinOps Open Cost and Usage Specification)](https://focus.finops.org/)는 FinOps Foundation에서 주도하는 멀티클라우드 비용 데이터 표준화 스펙입니다.

FOCUS의 목표:
- 벤더별로 다른 비용 데이터 형식을 하나의 스키마로 통합
- 멀티클라우드 환경에서 일관된 비용 분석 가능
- 벤더 간 비용 비교를 위한 공통 용어 정의

| 벤더 | FOCUS 지원 현황 |
| --- | --- |
| AWS | [CUR 2.0 (FOCUS 호환)](https://docs.aws.amazon.com/cur/latest/userguide/table-columns-cur2.html) |
| Azure | [Cost Management FOCUS export](https://learn.microsoft.com/en-us/azure/cost-management-billing/) |
| GCP | [BigQuery 비용 내보내기 (FOCUS 호환)](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables) |
| OCI | [Cost Report (FOCUS 지원 진행 중)](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm) |

## 참고하기

### 프레임워크

- [FinOps Foundation](https://www.finops.org/)
- [FOCUS 스펙](https://focus.finops.org/)

### AWS

- [AWS Cost Management 문서](https://docs.aws.amazon.com/cost-management/)

### Azure

- [Microsoft Cost Management 문서](https://learn.microsoft.com/en-us/azure/cost-management-billing/)

### GCP

- [Cloud Billing 문서](https://cloud.google.com/billing/docs)

### OCI

- [OCI Billing 문서](https://docs.oracle.com/en-us/iaas/Content/Billing/home.htm)
