---
description: AWS, Azure, GCP, OCI 주요 벤더의 특징, 강점, 멀티클라우드 연동 서비스를 비교합니다.
---

# 벤더 비교하기

> 문서 기준: 2026년 5월

## 한눈에 보기

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **운영사** | Amazon | Microsoft | Google | Oracle |
| **출시** | 2006년 | 2010년 | 2008년 | 2016년 (Gen2) |
| **시장 점유율** | 1위 (~31%) | 2위 (~25%) | 3위 (~11%) | 4위 (~2%) |
| **서비스 수** | 200+ | 200+ | 150+ | 80+ |
| **한국 리전** | 서울 (4 AZ) | 서울, 부산 | 서울 (3 Zone) | 서울, 춘천 |
| **강점** | 가장 넓은 포트폴리오, 최대 커뮤니티 | 엔터프라이즈(M365, AD), 하이브리드 | AI/ML(Vertex AI, TPU), 데이터(BigQuery) | DB(Autonomous DB), 가격 경쟁력 |
| **콘솔** | [Console](https://console.aws.amazon.com) | [Portal](https://portal.azure.com) | [Console](https://console.cloud.google.com) | [Console](https://cloud.oracle.com) |

{% hint style="info" %}
시장 점유율은 Synergy Research Group 2024년 기준 추정치이며, 측정 방법에 따라 차이가 있을 수 있습니다. 이 문서는 CloudPick에서 우선 다루는 AWS, Azure, GCP, OCI를 중심으로 비교합니다.
{% endhint %}

## 주요 서비스 매핑

특정 벤더에 익숙한 독자가 다른 벤더의 동등 서비스를 찾을 때 참고하세요.

| 영역 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **가상머신** | EC2 | Virtual Machines | Compute Engine | Compute |
| **관리형 K8s** | EKS | AKS | GKE | OKE |
| **서버리스 함수** | Lambda | Functions | Cloud Functions | OCI Functions |
| **서버리스 컨테이너** | Fargate | Container Apps | Cloud Run | Container Instances |
| **객체 스토리지** | S3 | Blob Storage | Cloud Storage | Object Storage |
| **블록 스토리지** | EBS | Managed Disks | Persistent Disk | Block Volume |
| **관리형 RDB** | RDS / Aurora | Azure SQL / Flexible Server | Cloud SQL / AlloyDB | Autonomous DB |
| **NoSQL (문서)** | DynamoDB | Cosmos DB | Firestore / Bigtable | NoSQL Database |
| **데이터 웨어하우스** | Redshift | Synapse Analytics | BigQuery | Autonomous DW |
| **VPC** | VPC | VNet | VPC (글로벌) | VCN |
| **로드밸런서 (L7)** | ALB | Application Gateway | Cloud Load Balancing | Load Balancer |
| **DNS** | Route 53 | Azure DNS | Cloud DNS | OCI DNS |
| **CDN** | CloudFront | Front Door / CDN | Cloud CDN | — |
| **IAM** | IAM + Identity Center | Entra ID | Cloud IAM | IAM with Identity Domains |
| **시크릿 관리** | Secrets Manager | Key Vault | Secret Manager | Vault |
| **위협 탐지** | GuardDuty | Defender for Cloud | Security Command Center | Cloud Guard |
| **IaC** | CloudFormation / CDK | Bicep / ARM | Deployment Manager | Resource Manager |
| **CI/CD** | CodePipeline / CodeBuild | Azure DevOps | Cloud Build | DevOps Service |
| **모니터링** | CloudWatch | Azure Monitor | Cloud Monitoring | OCI Monitoring |
| **AI/LLM 플랫폼** | Bedrock | Azure OpenAI / Foundry | Vertex AI | OCI Generative AI |

{% hint style="info" %}
서비스명은 빠르게 변경될 수 있습니다. Google Cloud는 자사 기준으로 AWS/Azure 서비스를 매핑한 [비교 문서](https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison)를 별도로 관리하고 있습니다.
{% endhint %}

## 각 사 특징

{% tabs %}
{% tab title="AWS — 가장 넓은 서비스 포트폴리오" %}
Amazon의 이커머스 인프라에서 출발한 AWS는 가장 오래되고 가장 넓은 서비스 포트폴리오를 보유합니다. 새로운 서비스 카테고리를 가장 먼저 출시하는 경우가 많고, 글로벌 커뮤니티와 파트너 생태계가 가장 큽니다.

- **핵심 강점:** 서비스 다양성, 글로벌 리전 수, 커뮤니티/문서 풍부
- **차별점:** Lambda(서버리스 선구자), S3(객체 스토리지 표준), 가장 세분화된 IAM
- **주의점:** 서비스 수가 200+로 많아 초기 선택에 시간이 필요함. 이그레스 비용 구조를 사전에 확인할 것
- **한국 리전:** 서울 4 AZ (2016~)
{% endtab %}

{% tab title="Azure — 엔터프라이즈 통합의 강자" %}
Microsoft의 엔터프라이즈 소프트웨어 생태계(Microsoft 365, Active Directory, Dynamics 365)와 긴밀하게 통합됩니다. 기존 Microsoft 환경을 사용하는 기업에서 가장 자연스러운 선택입니다.

- **핵심 강점:** Microsoft 365/AD 통합, 하이브리드(Azure Arc, Azure Stack), 엔터프라이즈 계약(EA)
- **차별점:** 서울-부산 리전 쌍으로 국내 DR 가능, GitHub/VS Code 통합
- **주의점:** 서비스 리브랜딩이 빈번하므로 최신 명칭을 공식 문서에서 확인할 것. 리전별 서비스 가용성이 다를 수 있음
- **한국 리전:** 서울(Korea Central) 3 AZ + 부산(Korea South)
{% endtab %}

{% tab title="GCP — AI/ML과 데이터 분석" %}
Google의 검색·데이터 처리 인프라에서 발전한 GCP는 AI/ML과 대규모 데이터 분석에서 차별화됩니다. 글로벌 VPC, SUD(자동 할인) 등 독특한 설계 철학을 가지고 있습니다.

- **핵심 강점:** AI/ML(Vertex AI, TPU, Gemini), 데이터 분석(BigQuery), 컨테이너(GKE)
- **차별점:** 글로벌 VPC(리전 종속 아님), SUD(약정 없이 자동 할인), Shared Fate 보안 모델
- **주의점:** 엔터프라이즈 도입 시 지원 플랜과 한국어 리소스 가용성을 사전에 확인할 것
- **한국 리전:** 서울 3 Zone (2020~)
{% endtab %}

{% tab title="OCI — 데이터베이스와 가격 경쟁력" %}
Oracle의 데이터베이스 기술력을 클라우드로 확장한 OCI는 Oracle DB 워크로드에서 압도적 성능을 제공합니다. 이그레스 비용이 타사 대비 매우 저렴하고, 전용 베어메탈 인스턴스를 제공합니다.

- **핵심 강점:** Autonomous Database, Oracle DB 최적화, 이그레스 비용 저렴(10TB/월 무료)
- **차별점:** 이그레스 10TB/월 무료, Dedicated Region(고객 DC에 OCI 설치), MySQL HeatWave
- **주의점:** Oracle DB 외 워크로드는 서비스 카탈로그와 서드파티 생태계 규모를 사전에 확인할 것
- **한국 리전:** 서울(`ap-seoul-1`), 춘천(`ap-chuncheon-1`)
{% endtab %}
{% endtabs %}

## 벤더 간 멀티클라우드 연동 서비스

주요 CSP는 경쟁 관계이면서도, 고객의 멀티클라우드 수요에 대응하여 벤더 간 직접 연동 서비스를 출시하고 있습니다.

| 카테고리 | 대표 서비스 | 설명 | 상세 |
| --- | --- | --- | --- |
| **네트워크 직접 연결** | AWS Interconnect–multicloud, Google Cross-Cloud Interconnect, Oracle Interconnect | 벤더 간 전용 네트워크로 프라이빗 연결 | [멀티클라우드 커넥티비티 (심화)](../networking/multicloud-connectivity.md#cross-cloud-interconnect) |
| **타 클라우드 내 DB 배치** | Oracle Database@Azure/AWS/GCP | 경쟁사 데이터센터 안에 Oracle DB를 네이티브 배치 | [관리형 RDB — Database@Cloud](../database/managed-rdb.md#database-cloud-db) |
| **멀티클라우드 관리 플랫폼** | Azure Arc, GKE Enterprise, OCI Multicloud | 타 클라우드 리소스를 자사 도구로 통합 관리 | 아래 참조 |

### 멀티클라우드 관리 플랫폼

타 클라우드의 리소스를 자사 관리 도구로 통합 관리할 수 있는 서비스입니다.

| 서비스 | 벤더 | 설명 |
| --- | --- | --- |
| **[Azure Arc](https://azure.microsoft.com/products/azure-arc/)** | Azure | AWS/GCP/온프레미스의 서버, Kubernetes, DB를 Azure Portal에서 통합 관리 |
| **[GKE Enterprise (구 Anthos)](https://cloud.google.com/kubernetes-engine/enterprise/docs)** | GCP | AWS/Azure/온프레미스의 Kubernetes를 GCP에서 통합 관리 |
| **[OCI Multicloud](https://docs.oracle.com/en/solutions/oci-best-practices/deploy-multicloud-oci-oracle-database-services1.html)** | OCI | Azure/AWS/GCP와의 연동을 위한 통합 솔루션 |

## 벤더가 제공하는 공식 비교 자료

### Microsoft Azure

Azure는 AWS와 GCP 사용자를 위한 전환 가이드를 가장 체계적으로 제공합니다.

- [AWS 전문가를 위한 Azure](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/)
  - [AWS와 Azure 서비스 비교](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/services)
- [GCP 전문가를 위한 Azure](https://learn.microsoft.com/ko-kr/azure/architecture/gcp-professional/)

### Google Cloud

- [AWS와 Azure 서비스를 Google Cloud와 비교](https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison)

### Oracle Cloud

- [OCI Migration Hub (온프레미스 및 타 클라우드에서 OCI로)](https://www.oracle.com/cloud/migrate-applications-to-oracle-cloud/)
- [OCI Cloud Adoption Framework](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/home.htm)

### AWS

AWS는 직접적인 서비스 비교 페이지를 제공하지 않습니다. 마이그레이션 가이드를 중심으로 자료를 제공합니다.

- [AWS 클라우드 마이그레이션](https://aws.amazon.com/ko/cloud-migration/)

## 3rd Party 비교 자료

- [Public Cloud Services Comparison](https://comparecloud.in) — AWS, Azure, GCP, Oracle Cloud 서비스 카테고리별 비교
  - [소스 코드](https://github.com/ilyas-it83/CloudComparer/)

## 속도 비교

### 벤더 공식 네트워크 성능 자료

- [AWS — Infrastructure Performance](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/what-is-network-monitor.html)
- [Azure — 네트워크 왕복 지연 시간 통계](https://learn.microsoft.com/en-us/azure/networking/azure-network-latency)
- [GCP — Performance Dashboard](https://cloud.google.com/network-intelligence-center/docs/performance-dashboard/concepts/overview)

### 브라우저 기반 측정 도구

- [GCPing](https://gcping.com) — GCP 리전별 지연 시간 측정
- [Azure Speed Test 2.0](https://azurespeedtest.azurewebsites.net) — Azure 리전별 지연 시간 측정
- [Kentik Cloud Latency Map](https://clm.kentik.com/) — AWS, Azure, GCP, Oracle 리전 간 지연 시간
- [Cloud Ping Test](https://webping.cloud) — 멀티 벤더 동시 비교

## 참고하기

### 커뮤니티 및 리서치

- [Synergy Research Group](https://www.srgresearch.com/) — 클라우드 시장 점유율 분기별 보고
- [Gartner Magic Quadrant for Cloud Infrastructure](https://www.gartner.com/reviews/market/cloud-infrastructure-and-platform-services) — 클라우드 벤더 평가
- [CNCF Cloud Native Survey](https://www.cncf.io/reports/cncf-annual-survey-2024/) — 클라우드 채택 현황 통계
