---
description: FinOps 라이프사이클, 비용 관리 도구, 실무 적용 순서, FOCUS 스펙을 벤더별로 비교합니다.
---

# FinOps

> 문서 기준: 2026년 6월

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

### 단위 경제 (Unit Economics)

"월 비용이 얼마인가?"보다 "사용자 1명당 비용", "트랜잭션 1건당 비용"을 추적하는 것이 사업 의사결정에 유용합니다.

| 지표 예시 | 계산 예 |
| --- | --- |
| 활성 사용자당 비용 | 월 인프라 비용 / 월간 활성 사용자 수 (MAU) |
| 트랜잭션당 비용 | 월 비용 / 월 처리된 요청 수 |
| 매출 대비 인프라 비중 | 월 인프라 비용 / 월 매출 |

단위 경제를 추적하면 트래픽 증가 시 비용이 선형인지 확인하고, 서비스별 수익성을 평가할 수 있습니다.

## 주요 CSP 비용 관리 도구 비교

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| 비용 분석 | [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) | [Microsoft Cost Management](https://azure.microsoft.com/en-us/products/cost-management) | [Cloud Billing Reports](https://cloud.google.com/billing/docs/reports) | [OCI Cost Analysis](https://docs.oracle.com/iaas/Content/Billing/Concepts/costanalysisoverview.htm) |
| 예산/알림 | [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/) | [Azure Budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets) | [Budget Alerts](https://cloud.google.com/billing/docs/how-to/budgets) | [OCI Budgets](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm) |
| 추천/어드바이저 | [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/) | [Azure Advisor](https://azure.microsoft.com/en-us/products/advisor) | [Recommender](https://cloud.google.com/recommender/docs/overview) | [Cloud Advisor](https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/Concepts/cloudadvisoroverview.htm) |
| 비용 할당 | Cost Allocation Tags | Cost Allocation (Tags + Subscriptions) | Labels + Billing Account | Cost Tracking Tags + Compartments |

### AI 비용 거버넌스

AI 워크로드(LLM API 호출, GPU 학습/추론)는 전통적 클라우드 비용과 **근본적으로 다른 과금 구조**(토큰 기반, 모델별 가격 차이, 에이전트 루프에 의한 비결정적 소비)를 가집니다. 기존 FinOps의 사이징·예약 레버가 그대로 적용되지 않으므로 별도의 거버넌스가 필요합니다.

| 항목 | 기존 클라우드 비용 | AI 비용 |
| --- | --- | --- |
| 과금 단위 | 시간, GB, 요청 수 | 토큰(입력/출력), GPU-시간, 에이전트 세션 |
| 예측 가능성 | 리소스 수 × 단가로 추정 | 프롬프트 길이, 에이전트 루프 수에 따라 비결정적 |
| 최적화 레버 | 사이징, 예약, 스팟, 미사용 제거 | 모델 계층화, 토큰 예산, 프롬프트 캐싱, 서킷 브레이커 |

**실무 대응:**

- **태스크별 토큰 예산** — 에이전트/API 호출마다 최대 토큰 한도 설정
- **모델 계층화** — 간단한 분류는 경량 모델(GPT-5.4 mini, Haiku), 복잡한 추론은 고성능 모델
- **프롬프트 캐싱** — 반복되는 시스템 프롬프트를 캐싱하여 입력 토큰 절감
- **비용 태그** — AI 워크로드를 별도 태그(`ai:true`, `model:claude-fable-5`)로 분리 추적

### AWS FinOps Agent [Preview]

2026년 6월 FinOps X에서 발표된 [AWS FinOps Agent](https://siliconangle.com/2026/06/11/aws-launches-finops-agent-bring-ai-cost-governance-cloud-spend-finopsx/)(Feature Preview)는 비용 이상을 AI가 자동 탐지하고, 근본 원인을 분석하여 담당 팀에 Slack/Jira로 라우팅합니다.

| 기능 | 설명 |
| --- | --- |
| 이상 탐지 | 일별 비용 패턴에서 이상 자동 감지 |
| 근본 원인 분석 | 어떤 서비스/태그/리전에서 비용이 급증했는지 분석 |
| 팀 라우팅 | 비용 소유자에게 Slack/Jira 알림 자동 전송 |
| 상태 | Feature Preview (2026.06) |

## 실무 적용 순서

FinOps를 처음 시작할 때는 도구를 많이 도입하기보다, 비용을 설명할 수 있는 최소 기준을 먼저 만드는 것이 중요합니다.

| 단계 | 해야 할 일 | 산출물 |
| --- | --- | --- |
| 1 | 계정/구독/프로젝트 구조 정리 | 비용 소유 조직 매핑 |
| 2 | 태그/라벨 표준 정의 | `service`, `env`, `owner`, `cost-center` 등 |
| 3 | 예산과 알림 설정 | 월별 예산, 임계치 알림 |
| 4 | 큰 비용 항목부터 최적화 | 미사용 리소스, 과대 사이징, 스토리지 클래스 |
| 5 | 예약/약정 할인 검토 | RI, Savings Plans, CUD 등 |

---

## Inform — 가시성 확보

비용을 줄이기 전에, 먼저 **어디에 얼마가 쓰이는지** 정확히 파악해야 합니다.

- **태그/라벨 정책** — 모든 리소스에 팀, 환경, 비용 센터를 태깅하여 비용 귀속을 명확히 합니다.
- **비용 대시보드** — 벤더별 비용 분석 도구(AWS Cost Explorer, Azure Cost Management, Google Cloud Billing)로 일별/주별 추세를 시각화합니다.
- **이상 탐지 알림** — 예산 초과나 급격한 비용 증가 시 즉시 알림을 받도록 설정합니다.
- **FOCUS 스펙 활용** — 멀티클라우드 환경에서는 FinOps FOCUS 표준으로 벤더 간 비용 데이터를 통합합니다.

### 태그/라벨 정책 설계

FinOps의 출발점은 **누가, 무엇에, 얼마를 썼는가** 를 정확히 귀속시키는 것입니다. 계정/구독/프로젝트 단위 분리만으로는 부족한 경우(같은 계정에 여러 팀의 리소스가 있는 경우 등)가 많아, 태그/라벨이 필수입니다.

### 표준 태그 세트

벤더에 중립적으로 권장되는 최소 태그 세트입니다.

| 태그 키 | 값 예시 | 용도 |
| --- | --- | --- |
| `env` / `environment` | `prod`, `staging`, `dev` | 환경별 비용 분석, 배포 정책 |
| `owner` | `team-payments@company.com` | 책임자 식별, 알림 라우팅 |
| `cost-center` | `CC-1001` | 회계 시스템 연계, Chargeback |
| `project` / `workload` | `checkout-api`, `ml-pipeline` | 서비스 단위 비용 분석 |
| `service-tier` | `critical`, `standard`, `low` | SLO/DR 정책과 연계 |
| `data-classification` | `public`, `internal`, `confidential` | 보안/감사 요건 |
| `compliance` | `pci`, `hipaa`, `isms-p` | 규제 리소스 식별 |
| `managed-by` | `terraform`, `manual` | IaC 관리 여부, 드리프트 탐지 |

조직에 따라 `business-unit`, `customer`, `cost-allocation` 등을 추가할 수 있습니다.

### 태그 정책 원칙

- **일관된 대소문자와 표기** — `env` vs `Env` vs `environment`는 다른 키로 취급됨. 하나로 통일.
- **값 허용 목록 제한** — 자유 입력은 오타로 집계 실패. `prod`/`staging`/`dev`처럼 허용값 고정.
- **필수 태그 강제** — 태그 없는 리소스는 비용 귀속이 불가. 생성 시 강제.
- **상위 계층에서 상속** — 조직/OU/폴더/컴파트먼트 수준 태그가 하위 리소스에 자동 적용되면 운영 부담 감소.
- **기술 태그와 비용 태그 구분** — `app=nginx`는 기술, `cost-center=CC-1001`은 비용. 비용 리포트에서 노이즈 줄임.

### 벤더별 태그 거버넌스 도구

| 벤더 | 태그 강제/감사 | 참고 |
| --- | --- | --- |
| AWS | [AWS Tag Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html), [Resource Groups Tagging API](https://docs.aws.amazon.com/resourcegroupstagging/latest/APIReference/Welcome.html), [Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html) | Organization 수준에서 태그 정책 정의, Config Rule로 규정 위반 탐지 |
| Azure | [Azure Policy 태그 enforcement](https://learn.microsoft.com/azure/azure-resource-manager/management/tag-policies), [Cost allocation rules](https://learn.microsoft.com/azure/cost-management-billing/costs/allocate-costs) | Management Group 단위로 태그 정책 적용, 상속 정책 제공 |
| Google Cloud | [Resource Tags](https://cloud.google.com/resource-manager/docs/tags/tags-overview), [Labels](https://cloud.google.com/resource-manager/docs/creating-managing-labels), [Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/tags-organization-policy) | Resource Tags는 IAM과 정책에, Labels는 비용 분석에 사용 (용도 분리) |
| OCI | [Tag Namespaces](https://docs.oracle.com/en-us/iaas/Content/Tagging/Tasks/managingtagsandtagnamespaces.htm), [Tag Defaults](https://docs.oracle.com/en-us/iaas/Content/Tagging/Tasks/managingtagdefaults.htm), [Cost Tracking Tags](https://docs.oracle.com/en-us/iaas/Content/Tagging/Tasks/usingcosttrackingtags.htm) | Tag Namespace로 키 관리, Tag Defaults로 Compartment 수준 자동 태깅 |

### 배포 파이프라인에서의 강제

태그는 사람이 직접 붙이면 누락되기 쉽습니다. 정책 코드화로 강제합니다.

- **IaC 모듈 표준화** — Terraform 모듈에 필수 태그를 입력 변수로 강제. 누락 시 plan 단계에서 실패.
- **정책 게이트** — AWS SCP, Azure Policy, Google Cloud Organization Policy로 태그 없는 리소스 생성 거부.
- **CI/CD 검증** — PR 단계에서 `tflint`, `checkov`, `opa`로 태그 존재 여부 확인.
- **지속 감사** — AWS Config, Azure Resource Graph, Google Cloud Asset Inventory 쿼리로 정기 리포트.

### 시작 체크리스트

- [ ] 표준 태그 키 세트 정의 (8~10개 이내로 시작, 이후 확장)
- [ ] 태그 값 허용 목록 문서화 (예: `env` 값은 `prod`/`staging`/`dev`만)
- [ ] 조직/OU/폴더/컴파트먼트 수준의 상속 정책 적용
- [ ] IaC 모듈에 필수 태그 입력 강제
- [ ] 비용 할당 태그(Cost Allocation Tag) 활성화 — 벤더 기본은 비활성
- [ ] 기존 리소스의 누락 태그 보정 계획 (일괄 업데이트 스크립트)
- [ ] 월 1회 태그 규정 준수 리포트 생성
- [ ] Showback/Chargeback 리포트의 태그 기반 필드 확인

### 쇼백 vs 차지백 (Showback vs Chargeback)

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

### FOCUS 스펙

[FOCUS(FinOps Open Cost and Usage Specification)](https://focus.finops.org/)는 FinOps Foundation에서 주도하는 멀티클라우드 비용 데이터 표준화 스펙입니다. 벤더별로 다른 비용 데이터 형식을 하나의 스키마로 통합하여 멀티클라우드 환경에서 일관된 비용 분석을 가능하게 합니다.

**FOCUS v1.2** (2025.6)에서 AI/ML 워크로드 비용 가시성이 강화되었습니다:
- `ServiceCategory` / `ServiceName` 체계에서 AI 서비스 구분 표준화
- `PricingUnit`에 토큰(input/output), GPU-hour, 추론 요청 등 AI 과금 단위 반영
- `CommitmentDiscountStatus` 등 약정 관련 컬럼으로 GPU 예약 할인 추적 가능

| 벤더 | FOCUS 지원 현황 |
| --- | --- |
| AWS | [Data Exports — FOCUS 1.2 with AWS columns](https://docs.aws.amazon.com/cur/latest/userguide/table-columns-cur2.html) (CUR 2.0과는 별도 내보내기) |
| Azure | [Cost Management FOCUS export](https://learn.microsoft.com/en-us/azure/cost-management-billing/) |
| Google Cloud | [BigQuery 비용 내보내기 (FOCUS 호환)](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables) |
| OCI | [Cost Report (FOCUS 지원 진행 중)](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm) |

---

## Optimize — 최적화

### 자주 보는 비용 최적화 항목

- **컴퓨팅 사이징** — CPU/메모리 사용률이 낮은 VM을 축소하거나 종료합니다.
- **스케줄링** — 개발/테스트 환경은 업무 시간 외 자동 중지합니다.
- **스토리지 수명주기** — 오래된 로그와 백업은 저렴한 스토리지 클래스로 이동합니다.
- **이그레스 비용** — 리전 간, 클라우드 간 데이터 전송 경로를 점검합니다.
- **VPC 네트워킹 비용** — NAT Gateway, 크로스 AZ 트래픽 등 숨겨진 비용을 점검합니다.
- **약정 할인** — 안정적으로 사용하는 베이스라인 워크로드에 예약/약정을 적용합니다.

{% hint style="warning" %}
비용 최적화는 보안, 가용성, 성능을 훼손하지 않는 범위에서 진행해야 합니다. 특히 백업 보관 기간이나 DR 구성을 비용만 보고 줄이면 장애 시 더 큰 손실이 발생할 수 있습니다.
{% endhint %}

### VPC 네트워킹 비용 함정

VPC 관련 비용은 숨겨져 있어 예상치 못한 청구가 발생하기 쉽습니다.

| 비용 항목 | 설명 | 대응 |
| --- | --- | --- |
| **NAT Gateway** | 시간당 비용 + GB당 처리 비용. 대량 아웃바운드 시 월 수백~수천 달러 | VPC Endpoint로 AWS 서비스 접근 시 NAT 우회 |
| **크로스 AZ 트래픽** | 같은 리전이라도 AZ 간 통신은 GB당 과금 | 가능하면 같은 AZ 내 통신 유지, AZ-aware 라우팅 |
| **VPC Endpoint vs 인터넷 경유** | S3 등 접근 시 NAT Gateway 경유하면 처리 비용 발생 | Gateway Endpoint(S3, DynamoDB)는 무료 |
| **Transit Gateway** | 시간당 + GB당 데이터 처리 비용 | VPC 피어링(데이터 전송만 과금)과 비교 검토 |

**벤더별 차이:**

- **AWS** — 크로스 AZ 트래픽 $0.01/GB 양방향. NAT Gateway $0.045/시간 + $0.045/GB
- **Google Cloud** — 같은 존(Zone) 내 무료. 같은 리전 내 다른 존은 $0.01/GB
- **Azure** — 같은 VNet 내 무료. VNet 피어링은 인바운드/아웃바운드 각각 과금

> 위 수치는 문서 작성 시점 기준이며 변동될 수 있습니다. 최신 가격은 각 벤더 공식 가격표를 확인하세요.

관련: [VPC와 서브넷](../networking/vpc-subnet.md)

### 약정 할인 전략

각 벤더는 1년 또는 3년 약정 시 최대 70~72% 할인을 제공합니다. 하지만 약정한 만큼 사용하지 못하면 비용 낭비가 됩니다.

### 약정 상품 유형

| 유형 | 특징 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- | --- |
| **인스턴스 예약** | 특정 인스턴스 타입 고정 | Reserved Instances | Reserved VM Instances | — | — |
| **사용 금액 약정 (유연)** | 시간당 지출 금액 약정, 인스턴스 유형 변경 가능 | Savings Plans | Savings Plans | CUD (Flexible) | Universal Credits |
| **자동 할인** | 약정 없이 사용량에 따라 자동 할인 | — | — | SUD (Sustained Use Discount) | — |
| **스팟/Preemptible** | 중단 가능 대신 60~90% 할인 | Spot Instances | Spot VMs | Spot VMs / Preemptible | Preemptible Instances |

### 적용 전략

- **70/30 원칙** — 안정적 베이스라인 워크로드의 70%는 약정, 30%는 온디맨드로 유연성 확보
- **단계적 약정** — 처음부터 3년 약정 대신 1년부터 시작하여 사용 패턴 검증
- **Spot 활용** — 중단에 강한 워크로드(배치, CI, 개발 환경)는 Spot으로 이동
- **주기적 재평가** — 분기마다 약정 활용률 확인

{% hint style="info" %}
**약정은 확정 사용량에 대한 재무적 선택입니다.** 사용량이 확실한 워크로드에만 적용하세요. 사용량보다 크게 약정하면 할인은 받지만 유연성을 잃습니다.
{% endhint %}

## Operate — 운영

### 비용 이상 탐지

사람이 계속 모니터링하지 않고 머신러닝으로 비정상 비용 증가를 자동 탐지하는 기능입니다.

| 벤더 | 서비스 |
| --- | --- |
| AWS | [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html) |
| Azure | [Microsoft Cost Management — Anomaly Detection](https://learn.microsoft.com/azure/cost-management-billing/understand/analyze-unexpected-charges) |
| Google Cloud | [Recommender / Cost Anomaly Detection](https://cloud.google.com/billing/docs/how-to/manage-anomalies) |
| OCI | [OCI Monitoring 알람 기반 구성](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm) |

### 탐지 시 확인할 것

- 의도된 트래픽 증가인가 (마케팅, 이벤트)
- 실수로 남겨진 리소스 (테스트용 대형 인스턴스, 미사용 NAT Gateway)
- 자동 스케일링 이상 (이벤트 이후에도 축소 안 됨)
- 보안 사고로 인한 악성 사용 (크립토 마이닝, 외부 공격)

## 자주 하는 실수

- **태그 없이 리소스 생성** — 태그가 없으면 비용을 팀/서비스/환경에 귀속시킬 수 없어, 누가 얼마를 쓰는지 파악이 불가능합니다.
- **예산 알림 미설정** — 예산 알림 없이 운영하면 비정상적인 비용 증가를 수 주 후 청구서에서야 발견하게 됩니다.
- **약정 과대 구매** — 사용 패턴을 충분히 분석하지 않고 큰 약정을 구매하면, 미사용분이 낭비되고 유연성을 잃습니다.

## 체크리스트

- [ ] 모든 리소스에 태그 정책(env, owner, cost-center)을 적용하고 있는가
- [ ] 예산 알림(임계값 50%, 80%, 100%)을 설정했는가
- [ ] 월간 비용 리뷰를 정기적으로 수행하고 있는가
- [ ] 미사용 리소스(중지된 VM, 미연결 디스크, 빈 로드밸런서)를 정리하고 있는가

## 참고하기

### 프레임워크

- [FinOps Foundation](https://www.finops.org/)
- [FOCUS 스펙](https://focus.finops.org/)

### AWS

- [AWS Cost Management 문서](https://docs.aws.amazon.com/cost-management/)

### Azure

- [Microsoft Cost Management 문서](https://learn.microsoft.com/en-us/azure/cost-management-billing/)

### Google Cloud

- [Cloud Billing 문서](https://cloud.google.com/billing/docs)

### OCI

- [OCI Billing 문서](https://docs.oracle.com/en-us/iaas/Content/Billing/home.htm)
