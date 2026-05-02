# 리전과 가용영역

## 왜 리전이 중요한가

자체 전산센터를 운영한다고 가정해 보겠습니다. 서울에 IDC 하나만 두면 운영은 단순하지만, 그 건물에 화재나 정전이 발생하면 서비스 전체가 중단됩니다. 서울과 부산에 각각 IDC를 두고 이중화하면 한쪽에 장애가 나도 다른 쪽에서 서비스를 유지할 수 있습니다.

클라우드의 **리전(Region)**과 **가용영역(Availability Zone)**은 바로 이 이중화 개념을 벤더가 대규모로 구현한 것입니다. 리전을 선택하는 것은 단순히 "서버 위치"를 고르는 것이 아니라, 다음 세 가지를 결정하는 것입니다.

- **지연 시간(Latency)** — 사용자와 서버 간의 물리적 거리가 응답 속도를 결정합니다.
- **데이터 주권(Data Sovereignty)** — 법률에 따라 특정 데이터는 특정 국가 내에 저장해야 합니다.
- **재해복구(Disaster Recovery)** — 자연재해나 대규모 장애에 대비한 지리적 분산이 필요합니다.

## 핵심 개념

### 리전 (Region)

**리전**은 지리적으로 분리된 데이터센터 클러스터입니다. 각 리전은 독립적인 전력, 냉각, 네트워크를 갖추고 있으며, 다른 리전과 물리적으로 수십~수천 km 떨어져 있습니다. 온프레미스로 비유하면, 서울 IDC와 부산 IDC처럼 서로 다른 도시에 위치한 데이터센터에 해당합니다.

### 가용영역 (Availability Zone)

**가용영역(AZ)**은 하나의 리전 내에 있는 독립된 데이터센터(또는 데이터센터 그룹)입니다. 같은 리전 내의 AZ들은 고속 전용 네트워크로 연결되어 있어 지연 시간이 매우 낮지만(보통 1ms 이내), 각 AZ는 독립된 전력과 냉각 시스템을 갖추고 있어 하나의 AZ에 장애가 발생해도 다른 AZ는 영향을 받지 않습니다.

온프레미스로 비유하면, 같은 도시 내에 있지만 서로 다른 건물에 위치한 서버실과 비슷합니다. 같은 건물 내 다른 층에 서버를 분산하는 것보다 훨씬 높은 수준의 격리를 제공합니다.

### 엣지 로케이션 / PoP (Point of Presence)

**엣지 로케이션**은 리전보다 사용자에게 더 가까운 위치에 배치된 소규모 인프라입니다. 주로 CDN(Content Delivery Network)이나 DNS 서비스에 사용되며, 정적 콘텐츠를 캐싱하여 사용자에게 빠르게 전달하는 역할을 합니다. 온프레미스로 비유하면, 본사 서버실 외에 각 지사에 설치한 캐시 서버와 비슷합니다.

## 3사 비교

3사 모두 리전과 가용영역이라는 기본 개념을 공유하지만, 세부 구조와 용어에 차이가 있습니다.

| 개념 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **최상위 지리 구분** | 파티션 (상업, GovCloud, 중국) | Geography (지리) | — (별도 구분 없음) |
| **리전** | Region | Region | Region |
| **가용영역** | Availability Zone (AZ) | Availability Zone | Zone |
| **리전당 최소 AZ** | 3개 | 3개 (AZ 지원 리전) | 3개 |
| **엣지/PoP** | Edge Location, Local Zone | PoP, Azure Front Door | Edge PoP, Cloud CDN |
| **온프레미스 확장** | Outposts, Local Zone | Azure Local, Azure Stack | Google Distributed Cloud |
| **멀티리전 스토리지** | S3 Cross-Region Replication | GRS/GZRS | Multi-region, Dual-region |
| **글로벌 리전 수** | 38개 리전, 120+ AZ | 60개 이상 리전 | 40개 리전, 121 Zone |

> 리전 수는 2025년 기준이며, 각 벤더는 지속적으로 새로운 리전을 추가하고 있습니다.

### AWS의 리전 구조

AWS는 **Region → Availability Zone** 구조를 사용합니다. 각 리전은 최소 3개의 AZ로 구성되며, AZ 간 거리는 수 km에서 최대 100km 이내입니다. AZ 간 모든 트래픽은 암호화됩니다.

AWS만의 특징으로 **Local Zone**이 있습니다. Local Zone은 리전의 확장으로, 특정 도시에 컴퓨팅·스토리지 리소스를 배치하여 초저지연이 필요한 워크로드를 지원합니다.

### Azure의 리전 구조

Azure는 **Geography → Region → Availability Zone** 구조를 사용합니다. Geography(지리)는 데이터 보존 및 규정 준수 경계를 정의하며, 하나 이상의 리전을 포함합니다. 예를 들어, "한국" Geography에는 Korea Central(서울)과 Korea South(부산) 두 개의 리전이 포함됩니다.

Azure의 특징은 **리전 쌍(Region Pair)** 개념입니다. 같은 Geography 내의 두 리전이 쌍으로 지정되어, 플랫폼 업데이트 시 동시에 적용되지 않도록 보장합니다. 한국의 경우 Korea Central과 Korea South가 리전 쌍입니다.

### GCP의 리전 구조

GCP는 **Region → Zone** 구조를 사용합니다. AWS/Azure와 유사하지만, GCP만의 특징으로 **Multi-region**과 **Dual-region** 개념이 있습니다. 이는 주로 Cloud Storage에서 사용되며, 데이터를 여러 리전에 자동으로 복제하여 가용성을 높입니다.

- **Multi-region** — 대륙 단위(예: `asia`)로 데이터를 분산 저장합니다.
- **Dual-region** — 지정한 두 개의 리전에 데이터를 복제합니다.

## 한국 리전 현황

| 벤더 | 리전 이름 | 리전 코드 | AZ/Zone 수 | 출시 시기 |
| --- | --- | --- | --- | --- |
| **AWS** | 아시아 태평양(서울) | `ap-northeast-2` | 4개 AZ | 2016년 1월 |
| **Azure** | Korea Central | `koreacentral` | 3개 AZ | 2017년 2월 |
| **Azure** | Korea South | `koreasouth` | — (AZ 미지원) | 2017년 2월 |
| **GCP** | 서울 | `asia-northeast3` | 3개 Zone | 2020년 1월 |

AWS는 2016년에 가장 먼저 한국 리전을 개설했으며, 현재 4개의 AZ를 운영하고 있습니다. Azure는 서울과 부산 두 개의 리전을 보유하고 있어 국내에서 리전 간 DR 구성이 가능합니다. GCP는 2020년에 서울 리전을 개설했으며, 3개의 Zone을 운영하고 있습니다.

## 리전 선택 시 고려사항

리전을 선택할 때는 다음 요소를 종합적으로 고려해야 합니다.

### 지연 시간

사용자가 주로 위치한 지역과 가까운 리전을 선택합니다. 한국 사용자 대상 서비스라면 한국 리전이 최선이며, 글로벌 서비스라면 주요 사용자 분포에 따라 여러 리전에 배포하는 것이 좋습니다.

### 서비스 가용성

모든 클라우드 서비스가 모든 리전에서 제공되는 것은 아닙니다. 특히 최신 서비스나 AI/ML 관련 서비스는 특정 리전에서만 사용할 수 있는 경우가 많습니다. 사용하려는 서비스가 해당 리전에서 제공되는지 반드시 확인해야 합니다.

- [AWS 리전별 서비스 목록](https://aws.amazon.com/ko/about-aws/global-infrastructure/regional-product-services/)
- [Azure 리전별 제품](https://azure.microsoft.com/ko-kr/explore/global-infrastructure/products-by-region/)
- [GCP 리전별 제품](https://cloud.google.com/about/locations#products)

### 비용 차이

같은 서비스라도 리전에 따라 가격이 다릅니다. 일반적으로 미국 리전이 가장 저렴하고, 아시아 리전은 상대적으로 비쌉니다. 지연 시간이 크게 중요하지 않은 배치 처리 워크로드라면, 비용이 낮은 리전을 선택하는 것도 방법입니다.

### 컴플라이언스

산업별 규제에 따라 특정 리전을 사용해야 하는 경우가 있습니다. 예를 들어, 한국의 금융 데이터는 국내 리전에 저장해야 하는 규제가 있을 수 있습니다.

## 한국에서의 고려사항

### 데이터 주권 규제

한국의 **개인정보보호법**은 개인정보의 국외 이전 시 정보주체의 동의 또는 법적 근거를 요구합니다. **신용정보법**은 금융 분야의 개인신용정보에 대해 더 엄격한 규제를 적용합니다. 이러한 규제를 충족하려면 한국 리전에 데이터를 저장하는 것이 가장 안전한 방법입니다.

각 CSP는 다음과 같이 대응하고 있습니다.

- **AWS** — 한국 리전에서 데이터 저장 위치를 명시적으로 지정할 수 있으며, AWS Artifact를 통해 한국 규제 관련 컴플라이언스 보고서를 제공합니다.
- **Azure** — Korea Central/South 리전에 데이터를 저장하도록 정책을 설정할 수 있으며, Azure Policy를 통해 리전 제한을 강제할 수 있습니다.
- **GCP** — Organization Policy를 통해 리소스 생성 가능 리전을 제한할 수 있으며, VPC Service Controls로 데이터 유출을 방지할 수 있습니다.

### DR(재해복구) 전략

한국 리전에 장애가 발생했을 때를 대비한 DR 구성 시, 일본(도쿄, 오사카) 리전이 가장 일반적인 선택입니다. 한국-일본 간 네트워크 지연 시간은 약 30~50ms 수준으로, 비동기 복제 기반의 DR에 적합합니다.

Azure의 경우 한국 내에 서울-부산 리전 쌍이 있어, 데이터 주권 규제가 엄격한 경우에도 국내에서 DR을 구성할 수 있다는 장점이 있습니다.

## 참고하기

### AWS

- [AWS 글로벌 인프라](https://aws.amazon.com/ko/about-aws/global-infrastructure/)
- [리전 및 가용 영역](https://aws.amazon.com/ko/about-aws/global-infrastructure/regions_az/)
- [리전별 서비스 목록](https://aws.amazon.com/ko/about-aws/global-infrastructure/regional-product-services/)

### Azure

- [Azure 지역](https://azure.microsoft.com/ko-kr/explore/global-infrastructure/geographies/)
- [리전별 제품](https://azure.microsoft.com/ko-kr/explore/global-infrastructure/products-by-region/)
- [가용성 영역](https://learn.microsoft.com/ko-kr/azure/reliability/availability-zones-overview)

### GCP

- [Google Cloud 위치](https://cloud.google.com/about/locations)
- [리전 및 영역](https://cloud.google.com/compute/docs/regions-zones)
- [Geography and regions](https://cloud.google.com/docs/get-started/geography-and-regions)
