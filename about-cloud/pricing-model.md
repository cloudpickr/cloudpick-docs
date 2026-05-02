# 비용 구조 이해하기

## 온프레미스 vs 클라우드 비용 구조

자체 전산센터를 운영하려면 서버를 구매하기 전부터 비용이 발생합니다. 서버 구매비, 상면(랙 공간) 임대료, 전력 및 냉각 비용, 네트워크 장비, 그리고 이 모든 것을 관리할 인력 비용까지 — 서비스를 시작하기도 전에 수억 원의 초기 투자가 필요합니다. 이를 **CAPEX(Capital Expenditure, 자본 지출)**라고 합니다.

클라우드는 이 구조를 **OPEX(Operational Expenditure, 운영 지출)**로 전환합니다. 초기 투자 없이, 사용한 만큼만 비용을 지불합니다. 서버를 1시간 사용하면 1시간분만, 1TB를 저장하면 1TB분만 과금됩니다.

| 항목 | 온프레미스 (CAPEX) | 클라우드 (OPEX) |
| --- | --- | --- |
| **초기 투자** | 서버, 네트워크 장비 구매 (수억 원) | 없음 |
| **과금 방식** | 구매 후 감가상각 (3~5년) | 사용량 기반 종량제 |
| **확장** | 추가 장비 구매 (수 주~수 개월) | 즉시 확장 가능 |
| **축소** | 장비 처분 어려움 | 즉시 축소, 비용 절감 |
| **유지보수** | 자체 인력 필요 | 벤더가 관리 |

다만, 클라우드가 항상 저렴한 것은 아닙니다. 24시간 365일 일정한 부하로 운영되는 워크로드는 온프레미스가 더 경제적일 수 있습니다. 클라우드의 비용 이점은 **탄력적인 사용 패턴**에서 극대화됩니다.

## 핵심 과금 모델

### 온디맨드 (On-Demand / Pay-As-You-Go)

가장 기본적인 과금 방식입니다. 약정 없이 사용한 만큼만 지불합니다. 자유롭게 시작하고 중단할 수 있어 개발/테스트 환경이나 트래픽 예측이 어려운 워크로드에 적합합니다.

### 예약/약정 할인 (Reserved / Committed)

1년 또는 3년 사용을 약정하면 온디맨드 대비 30~72% 할인을 받을 수 있습니다. 자체 전산센터에서 3년 장기 임대 계약을 하면 월 임대료가 낮아지는 것과 비슷합니다. 안정적으로 운영되는 프로덕션 워크로드에 적합합니다.

### 스팟/프리엠티블 인스턴스 (Spot / Preemptible)

벤더의 유휴 리소스를 온디맨드 대비 60~90% 할인된 가격에 사용할 수 있습니다. 단, 벤더가 리소스를 회수할 수 있으므로 언제든 중단될 수 있습니다. 배치 처리, 데이터 분석, CI/CD 빌드 등 중단에 강한 워크로드에 적합합니다.

### 프리 티어 (Free Tier)

3사 모두 신규 사용자를 위한 무료 사용 범위를 제공합니다. 클라우드를 처음 시작할 때 비용 부담 없이 학습하고 실험할 수 있습니다.

## 3사 비교

| 과금 모델 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **온디맨드** | On-Demand | Pay-As-You-Go | On-Demand |
| **약정 할인 (인스턴스)** | Reserved Instances (RI) | Reserved VM Instances | — |
| **약정 할인 (유연)** | Savings Plans | Azure Savings Plan | Committed Use Discounts (CUD) |
| **스팟** | Spot Instances | Spot VMs | Spot VMs |
| **자동 할인** | — | — | Sustained Use Discounts (SUD) |
| **프리 티어** | 12개월 무료 + Always Free | 12개월 무료 + Always Free | 90일 $300 크레딧 + Always Free |
| **과금 단위** | 초 단위 (Linux), 시간 단위 (Windows) | 초 단위 | 초 단위 |

### 핵심 차이점

**GCP의 SUD(Sustained Use Discounts)** — GCP만의 독특한 할인 모델입니다. 별도의 약정 없이, 한 달 동안 일정 시간 이상 인스턴스를 사용하면 자동으로 할인이 적용됩니다. 사용 시간이 늘어날수록 할인율이 높아지며, 최대 30%까지 할인됩니다. 약정 관리가 번거로운 조직에 유리합니다.

**AWS/Azure의 Savings Plans** — 특정 인스턴스 유형에 묶이지 않고, 시간당 사용 금액을 약정하는 유연한 할인 모델입니다. 인스턴스 패밀리, 리전, OS를 변경해도 할인이 유지되어, 워크로드 변화가 잦은 환경에 적합합니다.

**프리 티어 차이** — AWS와 Azure는 12개월간 주요 서비스를 무료로 제공하고, GCP는 90일간 $300 크레딧을 제공합니다. 3사 모두 기간 제한 없는 Always Free 서비스도 별도로 제공합니다.

## 숨겨진 비용 주의사항

클라우드 비용에서 가장 자주 간과되는 항목들입니다. 온프레미스에서는 발생하지 않던 비용이므로 특히 주의가 필요합니다.

### 데이터 전송(Egress) 비용

클라우드로 데이터를 올리는 것(Ingress)은 무료이지만, 클라우드에서 외부로 데이터를 내보내는 것(Egress)은 유료입니다. 대용량 데이터를 자주 외부로 전송하는 워크로드에서는 이 비용이 상당할 수 있습니다.

> 참고: GCP는 2024년부터 다른 클라우드나 인터넷으로의 데이터 전송 비용을 일부 무료화하는 정책을 시행하고 있습니다.

### 스토리지 API 호출 비용

스토리지에 데이터를 저장하는 비용 외에, 데이터를 읽고 쓰는 API 호출에도 비용이 발생합니다. 소규모에서는 무시할 수 있지만, 수백만 건의 API 호출이 발생하는 워크로드에서는 무시할 수 없는 금액이 됩니다.

### 로그/모니터링 비용

CloudWatch(AWS), Azure Monitor(Azure), Cloud Logging(GCP) 등 모니터링 서비스의 로그 수집·저장 비용도 간과하기 쉽습니다. 로그 보존 기간과 수집 범위를 적절히 설정하지 않으면 예상치 못한 비용이 발생할 수 있습니다.

## 비용 관리 도구

각 벤더는 비용을 모니터링하고 최적화할 수 있는 도구를 제공합니다.

| 기능 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **비용 대시보드** | Cost Explorer | Cost Management + Billing | Cost Management |
| **예산 알림** | AWS Budgets | Azure Budgets | Budget Alerts |
| **이상 탐지** | Cost Anomaly Detection | Anomaly Alerts | Cost Anomaly Detection |
| **최적화 권장** | Trusted Advisor, Compute Optimizer | Azure Advisor | Recommender, Active Assist |

## 비용 추정 도구 (가격 계산기)

서비스 도입 전에 예상 비용을 산출할 수 있는 공식 가격 계산기를 제공합니다.

- [AWS Pricing Calculator](https://calculator.aws/)
- [Azure 가격 계산기](https://azure.microsoft.com/ko-kr/pricing/calculator/)
- [Google Cloud 가격 계산기](https://cloud.google.com/products/calculator)

## 한국에서의 고려사항

### 원화 결제

- **AWS** — 한국 원화(KRW) 결제를 지원합니다. 다만 환율 변동에 따라 실제 청구 금액이 달라질 수 있습니다.
- **Azure** — 한국 원화 결제를 지원합니다. EA(Enterprise Agreement) 계약 시 원화 고정 가격이 가능합니다.
- **GCP** — 한국 원화 결제를 지원합니다.

### 한국 리전 vs 해외 리전 가격 차이

일반적으로 한국 리전의 가격은 미국 리전(us-east-1, East US, us-central1 등) 대비 10~30% 높습니다. 지연 시간이 크게 중요하지 않은 워크로드(배치 처리, 백업 등)는 해외 리전을 활용하여 비용을 절감할 수 있습니다. 단, 데이터 주권 규제를 반드시 확인해야 합니다.

### 국내 파트너/리셀러

3사 모두 한국에 공식 파트너(리셀러)를 두고 있습니다. 파트너를 통해 결제하면 세금계산서 발행, 원화 결제, 기술 지원 등의 혜택을 받을 수 있으며, 볼륨 할인이 적용되는 경우도 있습니다.

### 세금 (부가세)

한국에서 클라우드 서비스를 이용하면 10% 부가가치세가 부과됩니다. 가격 계산기에 표시되는 금액은 세전 금액인 경우가 많으므로, 실제 청구 금액은 10%를 추가로 고려해야 합니다.

## 참고하기

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
