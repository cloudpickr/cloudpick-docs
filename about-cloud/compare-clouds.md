# 벤더 비교하기

## AWS, Azure, GCP 한눈에 보기

클라우드 벤더를 선택할 때 가장 먼저 궁금한 것은 "어떤 벤더가 어디에 강한가"입니다. 글로벌 3사의 주요 특징을 요약하면 다음과 같습니다.

| 항목 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **운영사** | Amazon Web Services | Microsoft | Google |
| **출시** | 2006년 | 2010년 | 2008년 |
| **시장 점유율** | 1위 (약 31%) | 2위 (약 25%) | 3위 (약 11%) |
| **서비스 수** | 200개 이상 | 200개 이상 | 150개 이상 |
| **한국 리전** | 서울 (4 AZ) | 서울, 부산 | 서울 (3 Zone) |
| **강점 영역** | 가장 넓은 서비스 포트폴리오, 가장 큰 커뮤니티 | 엔터프라이즈 통합 (Microsoft 365, Active Directory), 하이브리드 | AI/ML (Vertex AI, TPU), 데이터 분석 (BigQuery), 컨테이너 (GKE) |
| **콘솔** | [Console](https://console.aws.amazon.com) | [Portal](https://portal.azure.com) | [Console](https://console.cloud.google.com) |

> 시장 점유율은 Synergy Research Group 등 리서치 기관의 2024년 기준 추정치이며, 측정 방법에 따라 차이가 있을 수 있습니다.

각 벤더는 서로 다른 배경에서 출발했습니다. AWS는 Amazon의 이커머스 인프라에서, Azure는 Microsoft의 엔터프라이즈 소프트웨어에서, GCP는 Google의 검색·데이터 처리 인프라에서 발전했습니다. 이 배경이 각 벤더의 강점과 설계 철학에 영향을 미치고 있습니다.

## 벤더가 제공하는 공식 비교 자료

클라우드 벤더를 비교할 때 가장 좋은 출발점은 각 벤더가 직접 제공하는 공식 비교 자료입니다. 대부분의 벤더는 경쟁사 사용자를 위한 전환 가이드를 제공하고 있으며, 서비스 매핑 테이블과 아키텍처 차이점을 상세히 설명하고 있습니다.

### Microsoft Azure

Azure는 AWS와 GCP 사용자를 위한 전환 가이드를 가장 체계적으로 제공하고 있습니다. 서비스별 1:1 매핑뿐 아니라 아키텍처 개념의 차이까지 다루고 있어, 멀티클라우드 환경에서 참고하기 좋습니다.

- [AWS 전문가를 위한 Azure](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/)
  - [AWS와 Azure 서비스 비교](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/services)
  - [Azure 및 AWS의 지역 및 영역](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/regions-zones)
- [GCP 전문가를 위한 Azure](https://learn.microsoft.com/ko-kr/azure/architecture/gcp-professional/)
  - [GCP에서 Azure 서비스로 비교](https://learn.microsoft.com/ko-kr/azure/architecture/gcp-professional/services)

### Google Cloud

GCP는 AWS와 Azure의 서비스를 Google Cloud 서비스와 매핑하는 단일 페이지를 제공합니다. 서비스 카테고리별로 정리되어 있어 빠르게 대응 서비스를 찾을 수 있습니다.

- [AWS와 Azure 서비스를 Google Cloud와 비교](https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison)

### AWS

AWS는 경쟁사와의 직접적인 서비스 비교 페이지를 제공하지 않습니다. 대신 다른 클라우드에서 AWS로의 마이그레이션 가이드를 중심으로 자료를 제공하고 있습니다.

- [AWS 마이그레이션 허브](https://aws.amazon.com/ko/migration-hub/)
- [AWS 클라우드 마이그레이션](https://aws.amazon.com/ko/cloud-migration/)

## 3rd Party 비교 자료

벤더가 직접 제공하는 자료 외에, 커뮤니티에서 운영하는 비교 도구도 유용합니다.

- [Public Cloud Services Comparison](https://comparecloud.in) — AWS, Azure, GCP, IBM Cloud, Oracle Cloud, Alibaba Cloud, Huawei Cloud의 서비스를 카테고리별로 비교할 수 있습니다.
  - [소스 코드](https://github.com/ilyas-it83/CloudComparer/)

## 속도 비교

클라우드 선택 시 네트워크 지연 시간(Latency)도 중요한 고려 사항입니다. 아래 도구들을 사용하면 각 벤더의 리전별 응답 속도를 직접 측정할 수 있습니다.

### 여러 클라우드 동시 비교

- [CloudPing.info](https://www.cloudping.info/) — AWS, Azure 등 여러 클라우드의 리전별 지연 시간을 한 번에 측정할 수 있습니다.
- [Cloud Ping Test](https://webping.cloud) — AWS, Azure, GCP, IBM Cloud, Oracle Cloud, Alibaba Cloud, Digital Ocean을 동시에 비교합니다.
  - [소스 코드](https://github.com/goenning/webping.cloud)

### 특정 클라우드 리전별 비교

- [AWS CloudPing](https://www.cloudping.info/) — AWS 리전별 지연 시간 측정
- [Azure Speed Test 2.0](https://azurespeedtest.azurewebsites.net) — Azure 리전별 지연 시간 측정
  - [소스 코드](https://github.com/richorama/AzureSpeedTest2)
- [GCPing](https://gcping.com) — GCP 리전별 지연 시간 측정
  - [소스 코드](https://github.com/GoogleCloudPlatform/gcping)

## 한국에서의 고려사항

### 한국 리전 지연 시간

한국에서 서비스를 운영한다면, 한국 리전의 지연 시간이 가장 중요한 지표입니다. 위의 속도 비교 도구를 사용하여 직접 측정해 보는 것을 권장합니다. 일반적으로 한국 리전 간 지연 시간은 3사 모두 1~5ms 수준으로 큰 차이가 없습니다.

### DR(재해복구) 시 인접 리전

한국 리전에 장애가 발생했을 때를 대비한 DR 구성 시, 각 벤더의 인접 리전은 다음과 같습니다.

| 벤더 | 한국 리전 | 주요 DR 후보 리전 |
| --- | --- | --- |
| AWS | 서울 (`ap-northeast-2`) | 도쿄 (`ap-northeast-1`), 오사카 (`ap-northeast-3`) |
| Azure | Korea Central, Korea South | Japan East, Japan West |
| GCP | 서울 (`asia-northeast3`) | 도쿄 (`asia-northeast1`), 오사카 (`asia-northeast2`) |

Azure는 한국에 서울과 부산 두 개의 리전을 보유하고 있어, 국내에서 DR 구성이 가능하다는 점이 차별점입니다.

### 국내 파트너 생태계

각 벤더는 한국에 공식 파트너 네트워크를 운영하고 있습니다. 기술 지원, 컨설팅, 교육 등을 제공하는 파트너를 통해 도입을 진행하는 것이 일반적입니다.

- [AWS 파트너 찾기](https://partners.amazonaws.com/)
- [Azure 파트너 찾기](https://appsource.microsoft.com/ko-kr/marketplace/partner-dir)
- [Google Cloud 파트너 찾기](https://cloud.google.com/find-a-partner)

## 참고하기

### AWS

- [AWS란 무엇인가?](https://aws.amazon.com/ko/what-is-aws/)
- [AWS 제품](https://aws.amazon.com/ko/products/)
- [AWS 마이그레이션 허브](https://aws.amazon.com/ko/migration-hub/)

### Azure

- [Azure란?](https://azure.microsoft.com/ko-kr/resources/cloud-computing-dictionary/what-is-azure)
- [Azure 제품](https://azure.microsoft.com/ko-kr/products/)
- [AWS 전문가를 위한 Azure](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/)

### GCP

- [Why Google Cloud](https://cloud.google.com/why-google-cloud)
- [Google Cloud 제품](https://cloud.google.com/products)
- [AWS/Azure 서비스 비교](https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison)
