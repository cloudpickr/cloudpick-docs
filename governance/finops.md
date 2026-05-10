---
description: FinOps 라이프사이클, 비용 관리 도구, 실무 적용 순서, FOCUS 스펙을 벤더별로 비교합니다.
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

## Showback vs Chargeback

비용을 조직 내부에 어떻게 배분할지 결정하는 모델입니다. [FinOps Foundation 공식 프레임워크](https://www.finops.org/framework/capabilities/allocation/)에서 정의합니다.

| 모델 | 설명 | 적합한 조직 |
| --- | --- | --- |
| **Showback** | 부서/팀별 사용 비용을 "보여주기만" 함. 실제 예산 이동 없음 | FinOps 초기 도입, 비용 인식 확산 단계 |
| **Chargeback** | 부서별 사용 비용을 실제 예산에서 차감 | 성숙한 조직, 부서별 P&L 있는 경우 |

### 구현을 위한 전제조건

Showback/Chargeback을 하려면 비용을 정확히 귀속시킬 수 있어야 합니다.

- **태그/라벨 표준화** — 모든 리소스에 `cost-center`, `project`, `owner`, `env` 태그 적용
- **계정/구독/프로젝트 분리** — 부서별 분리는 태그보다 확실한 비용 경계 ([계정과 조직 구조](../about-cloud/accounts-and-organizations.md) 참고)
- **공유 비용 배분 정책** — 네트워크, 보안 서비스 같은 공통 비용을 어떻게 나눌지 정의

## 약정 할인 전략

각 벤더는 1년 또는 3년 약정 시 최대 70\~72% 할인을 제공합니다. 하지만 약정한 만큼 사용하지 못하면 비용 낭비가 됩니다.

### 약정 상품 유형

| 유형 | 특징 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- | --- |
| **인스턴스 예약** | 특정 인스턴스 타입 고정 | Reserved Instances | Reserved VM Instances | — | — |
| **사용 금액 약정 (유연)** | 시간당 지출 금액 약정, 인스턴스 유형 변경 가능 | Savings Plans | Savings Plans | CUD (Flexible) | Universal Credits |
| **자동 할인** | 약정 없이 사용량에 따라 자동 할인 | — | — | SUD (Sustained Use Discount) | — |
| **스팟/Preemptible** | 중단 가능 대신 60\~90% 할인 | Spot Instances | Spot VMs | Spot VMs / Preemptible | Preemptible Instances |

### 적용 전략

- **70/30 원칙** — 안정적 베이스라인 워크로드의 70%는 약정, 30%는 온디맨드로 유연성 확보
- **단계적 약정** — 처음부터 3년 약정 대신 1년부터 시작하여 사용 패턴 검증
- **Spot 활용** — 중단에 강한 워크로드(배치, CI, 개발 환경)는 Spot으로 이동
- **주기적 재평가** — 분기마다 약정 활용률 확인

{% hint style="info" %}
**약정은 보험이 아니라 베팅입니다.** 사용량이 확실한 워크로드에만 적용하세요. 무조건 많이 약정하면 할인은 받지만 유연성을 잃습니다.
{% endhint %}

## 단위 경제 (Unit Economics)

"월 비용이 얼마인가?"보다 "사용자 1명당 비용", "트랜잭션 1건당 비용"을 추적하는 것이 사업 의사결정에 유용합니다.

| 지표 예시 | 계산 예 |
| --- | --- |
| 활성 사용자당 비용 | 월 인프라 비용 / 월간 활성 사용자 수 (MAU) |
| 트랜잭션당 비용 | 월 비용 / 월 처리된 요청 수 |
| 고객 획득당 인프라 비용 | 신규 고객 유치 비용 중 인프라 기여분 |
| 매출 대비 인프라 비중 | 월 인프라 비용 / 월 매출 |

단위 경제를 추적하면:

- 트래픽이 늘어날 때 비용 증가가 선형인지 확인 (선형이 아니면 확장성 문제)
- 서비스/기능별 수익성 평가
- 예산 수립 시 매출 성장 대비 인프라 증가를 예측

## 비용 이상 탐지

사람이 계속 모니터링하지 않고 머신러닝으로 비정상 비용 증가를 자동 탐지하는 기능입니다.

| 벤더 | 서비스 |
| --- | --- |
| AWS | [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html) |
| Azure | [Microsoft Cost Management — Anomaly Detection](https://learn.microsoft.com/azure/cost-management-billing/understand/analyze-unexpected-charges) |
| GCP | [Recommender / Cost Anomaly Detection](https://cloud.google.com/billing/docs/how-to/manage-anomalies) |
| OCI | [OCI Monitoring 알람 기반 구성](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm) |

### 탐지 시 확인할 것

- 의도된 트래픽 증가인가 (마케팅, 이벤트)
- 실수로 남겨진 리소스 (테스트용 대형 인스턴스, 미사용 NAT Gateway)
- 자동 스케일링 이상 (이벤트 이후에도 축소 안 됨)
- 보안 사고로 인한 악성 사용 (크립토 마이닝, 외부 공격)

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
