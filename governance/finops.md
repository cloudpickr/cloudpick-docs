# FinOps

## FinOps란

FinOps(Cloud Financial Operations)는 [FinOps Foundation](https://www.finops.org/)에서 정의한 클라우드 비용 관리 프레임워크입니다. 엔지니어링, 재무, 비즈니스 팀이 협력하여 클라우드 비용의 가시성을 확보하고 최적화하는 것을 목표로 합니다.

FinOps의 3단계 라이프사이클:

| 단계 | 설명 |
| --- | --- |
| **Inform** | 비용 가시성 확보 — 누가, 무엇에, 얼마를 쓰고 있는지 파악 |
| **Optimize** | 비용 최적화 — 사이징, 예약, 스팟 활용, 미사용 리소스 제거 |
| **Operate** | 지속적 운영 — 예산 설정, 이상 탐지, 거버넌스 자동화 |

## 4사 비용 관리 도구 비교

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| 비용 분석 | [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) | [Microsoft Cost Management](https://azure.microsoft.com/en-us/products/cost-management) | [Cloud Billing Reports](https://cloud.google.com/billing/docs/reports) | [OCI Cost Analysis](https://www.oracle.com/cloud/costanalysis/) |
| 예산/알림 | [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/) | [Azure Budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets) | [Budget Alerts](https://cloud.google.com/billing/docs/how-to/budgets) | [OCI Budgets](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm) |
| 추천/어드바이저 | [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/) | [Azure Advisor](https://azure.microsoft.com/en-us/products/advisor) | [Recommender](https://cloud.google.com/recommender/docs/overview) | [Cloud Advisor](https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/Concepts/cloudadvisoroverview.htm) |
| 비용 할당 | Cost Allocation Tags | Cost Allocation (Tags + Subscriptions) | Labels + Billing Account | Cost Tracking Tags + Compartments |

## FOCUS 스펙

[FOCUS(FinOps Open Cost and Usage Specification)](https://focus.finops.org/)는 FinOps Foundation에서 주도하는 멀티클라우드 비용 데이터 표준화 스펙입니다.

FOCUS의 목표:
- 벤더별로 다른 비용 데이터 형식을 하나의 스키마로 통합
- 멀티클라우드 환경에서 일관된 비용 분석 가능
- 벤더 간 비용 비교를 위한 공통 용어 정의

| 벤더 | FOCUS 지원 현황 |
| --- | --- |
| AWS | [CUR 2.0 (FOCUS 호환)](https://docs.aws.amazon.com/cur/latest/userguide/table-columns-cur2.html) |
| Azure | [Cost Management FOCUS export](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/focus-overview) |
| GCP | [BigQuery 비용 내보내기 (FOCUS 호환)](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/focus) |
| OCI | [Cost Report (FOCUS 지원 진행 중)](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm) |

## 참고하기

| 리소스 | 링크 |
| --- | --- |
| FinOps Foundation | [https://www.finops.org/](https://www.finops.org/) |
| FOCUS 스펙 | [https://focus.finops.org/](https://focus.finops.org/) |
| AWS 비용 관리 | [AWS Cost Management 문서](https://docs.aws.amazon.com/cost-management/) |
| Azure 비용 관리 | [Microsoft Cost Management 문서](https://learn.microsoft.com/en-us/azure/cost-management-billing/) |
| GCP 비용 관리 | [Cloud Billing 문서](https://cloud.google.com/billing/docs) |
| OCI 비용 관리 | [OCI Billing 문서](https://docs.oracle.com/en-us/iaas/Content/Billing/home.htm) |
