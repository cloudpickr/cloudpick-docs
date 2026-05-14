---
description: 온디맨드, 예약, 스팟 과금 모델과 이그레스 등 숨겨진 비용 항목을 벤더별로 비교합니다.
---

# 비용 구조 이해하기

> 문서 기준: 2026년 5월

## 온프레미스 vs 클라우드 비용 구조

자체 전산센터를 운영하려면 서버를 구매하기 전부터 비용이 발생합니다. 서버 구매비, 상면(랙 공간) 임대료, 전력 및 냉각 비용, 네트워크 장비, 그리고 이 모든 것을 관리할 인력 비용까지 — 서비스를 시작하기도 전에 수억 원의 초기 투자가 필요합니다. 이를 **CAPEX** (Capital Expenditure, 자본 지출)라고 합니다. 집을 사는 것과 비슷합니다 — 큰 돈을 먼저 내고, 이후 유지비를 계속 부담합니다.

클라우드는 이 구조를 **OPEX** (Operational Expenditure, 운영 지출)로 전환합니다. 초기 투자 없이, 사용한 만큼만 비용을 지불합니다. 월세로 사는 것과 비슷합니다 — 필요할 때 들어가고, 필요 없으면 나가면 됩니다.

| 항목 | 온프레미스 (CAPEX) | 클라우드 (OPEX) |
| --- | --- | --- |
| **초기 투자** | 서버, 네트워크 장비 구매 (수억 원) | 없음 |
| **과금 방식** | 구매 후 감가상각 (3\~5년) | 사용량 기반 종량제 |
| **확장** | 추가 장비 구매 (수 주~수 개월) | 즉시 확장 가능 |
| **축소** | 장비 처분 어려움 | 즉시 축소, 비용 절감 |
| **유지보수** | 자체 인력 필요 | 벤더가 관리 |

다만, 클라우드가 항상 저렴한 것은 아닙니다. 24시간 365일 일정한 부하로 운영되는 워크로드는 온프레미스가 더 경제적일 수 있습니다. 클라우드의 비용 이점은 **탄력적인 사용 패턴**에서 극대화됩니다.

## 핵심 과금 모델

### 온디맨드 (On-Demand / Pay-As-You-Go)

가장 기본적인 과금 방식입니다. 약정 없이 사용한 만큼만 지불합니다. 자유롭게 시작하고 중단할 수 있어 개발/테스트 환경이나 트래픽 예측이 어려운 워크로드에 적합합니다.

### 예약/약정 할인 (Reserved / Committed)

1년 또는 3년 사용을 약정하면 온디맨드 대비 30\~72% 할인을 받을 수 있습니다. 단, 약정 기간 동안은 사용 여부와 관계없이 비용이 발생합니다. 안정적으로 운영되는 프로덕션 워크로드에 적합하며, 사용량이 불확실한 워크로드에는 오히려 손해가 될 수 있습니다. 약정 전략 수립과 상세 비교는 [FinOps](../governance/finops.md)를 참고하세요.

### 스팟/프리엠티블 인스턴스 (Spot / Preemptible)

벤더의 유휴 리소스를 온디맨드 대비 60\~90% 할인된 가격에 사용할 수 있습니다. 단, 벤더가 리소스를 회수할 수 있으므로 언제든 중단될 수 있습니다. 배치 처리, 데이터 분석, CI/CD 빌드 등 중단에 강한 워크로드에 적합합니다.

### 프리 티어 (Free Tier)

각 벤더 모두 신규 사용자를 위한 무료 사용 범위를 제공합니다. 클라우드를 처음 시작할 때 비용 부담 없이 학습하고 실험할 수 있습니다.

## 벤더별 비교

| 과금 모델 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **온디맨드** | On-Demand | Pay-As-You-Go | On-Demand | Pay-As-You-Go |
| **약정 할인 (인스턴스)** | Reserved Instances | Reserved VM Instances | — | — |
| **약정 할인 (유연)** | Savings Plans | Azure Savings Plan | CUD (Committed Use) | Universal Credits |
| **스팟** | Spot Instances | Spot VMs | Spot VMs | Preemptible Instances |
| **자동 할인** | — | — | SUD (Sustained Use) | — |
| **이그레스 무료** | — | — | 200GB/월 | **10TB/월** |
| **프리 티어** | 12개월 + Always Free | 12개월 + Always Free | 90일 $300 + Always Free | Always Free (넉넉) |
| **과금 단위** | 초 단위 | 초 단위 | 초 단위 | 초 단위 |

### 핵심 차이점

**GCP의 SUD(Sustained Use Discounts)** — 약정 없이 한 달 동안 일정 시간 이상 사용하면 자동으로 최대 30% 할인.

**OCI의 이그레스 정책** — 월 10TB까지 이그레스 무료. 멀티클라우드 환경에서 데이터 이동이 빈번한 경우 큰 비용 차이를 만듦.

**OCI Universal Credits** — 모든 OCI 서비스에 사용 가능한 유연한 약정 모델. 특정 서비스에 묶이지 않음.

## 숨겨진 비용 주의사항

클라우드 비용에서 가장 자주 간과되는 항목들입니다. 온프레미스에서는 발생하지 않던 비용이므로 특히 주의가 필요합니다.

### 데이터 전송(Egress) 비용

클라우드로 데이터를 올리는 것(Ingress)은 무료이지만, 클라우드에서 외부로 데이터를 내보내는 것(Egress)은 유료입니다. 대용량 데이터를 자주 외부로 전송하는 워크로드에서는 이 비용이 상당할 수 있습니다.

{% hint style="info" %}
참고: GCP는 2024년부터 다른 클라우드나 인터넷으로의 데이터 전송 비용을 일부 무료화하는 정책을 시행하고 있습니다.
{% endhint %}

### 스토리지 API 호출 비용

스토리지에 데이터를 저장하는 비용 외에, 데이터를 읽고 쓰는 API 호출에도 비용이 발생합니다. 소규모에서는 무시할 수 있지만, 수백만 건의 API 호출이 발생하는 워크로드에서는 무시할 수 없는 금액이 됩니다.

### 로그/모니터링 비용

CloudWatch(AWS), Azure Monitor(Azure), Cloud Logging(GCP) 등 모니터링 서비스의 로그 수집·저장 비용도 간과하기 쉽습니다. 로그 보존 기간과 수집 범위를 적절히 설정하지 않으면 예상치 못한 비용이 발생할 수 있습니다.

## 비용 관리 도구

각 벤더는 비용을 모니터링하고 최적화할 수 있는 도구를 제공합니다.

| 벤더 | 비용 대시보드 | 가격 계산기 |
| --- | --- | --- |
| AWS | [Cost Explorer](https://aws.amazon.com/ko/aws-cost-management/aws-cost-explorer/) | [Pricing Calculator](https://calculator.aws/) |
| Azure | [Cost Management](https://azure.microsoft.com/ko-kr/products/cost-management/) | [가격 계산기](https://azure.microsoft.com/ko-kr/pricing/calculator/) |
| GCP | [Cost Management](https://cloud.google.com/cost-management) | [가격 계산기](https://cloud.google.com/products/calculator) |
| OCI | [Cost Analysis](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm) | [Cost Estimator](https://www.oracle.com/cloud/costestimator.html) |

## 참고하기

### 표준 및 프레임워크

- [FinOps Foundation — FinOps Framework](https://finops.org/framework) — 클라우드 비용 관리 프레임워크
- [FinOps Foundation — FOCUS Specification](https://focus.finops.org/) — 멀티클라우드 비용 데이터 표준화 스펙
- [Flexera State of the Cloud Report](https://info.flexera.com/CM-REPORT-State-of-the-Cloud) — 연간 클라우드 비용/채택 현황 리포트

### AWS

- [AWS 요금](https://aws.amazon.com/ko/pricing/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Cost Explorer](https://aws.amazon.com/ko/aws-cost-management/aws-cost-explorer/)
- [AWS 프리 티어](https://aws.amazon.com/ko/free/)

### Azure

- [Azure 가격 책정](https://azure.microsoft.com/ko-kr/pricing/)
- [Azure 가격 계산기](https://azure.microsoft.com/ko-kr/pricing/calculator/)
- [Azure Cost Management](https://azure.microsoft.com/ko-kr/products/cost-management/)
- [Azure 무료 계정](https://azure.microsoft.com/ko-kr/free/)

### GCP

- [Google Cloud 가격 책정](https://cloud.google.com/pricing)
- [Google Cloud 가격 계산기](https://cloud.google.com/products/calculator)
- [Cost Management](https://cloud.google.com/cost-management)
- [Google Cloud 무료 프로그램](https://cloud.google.com/free)

### OCI

- [OCI 가격 책정](https://www.oracle.com/kr/cloud/pricing/)
- [OCI Cost Estimator](https://www.oracle.com/cloud/costestimator.html)
- [OCI Free Tier](https://www.oracle.com/cloud/free/)
