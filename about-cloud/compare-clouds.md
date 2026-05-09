# 벤더 비교하기

## 글로벌 4사 한눈에 보기

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **운영사** | Amazon | Microsoft | Google | Oracle |
| **출시** | 2006년 | 2010년 | 2008년 | 2016년 (Gen2) |
| **시장 점유율** | 1위 (~31%) | 2위 (~25%) | 3위 (~11%) | 4위 (~2%) |
| **서비스 수** | 200+ | 200+ | 150+ | 80+ |
| **한국 리전** | 서울 (4 AZ) | 서울, 부산 | 서울 (3 Zone) | 서울, 춘천 |
| **강점** | 가장 넓은 포트폴리오, 최대 커뮤니티 | 엔터프라이즈(M365, AD), 하이브리드 | AI/ML(Vertex AI, TPU), 데이터(BigQuery) | DB(Autonomous DB), 가격 경쟁력 |
| **콘솔** | [Console](https://console.aws.amazon.com) | [Portal](https://portal.azure.com) | [Console](https://console.cloud.google.com) | [Console](https://cloud.oracle.com) |

> 시장 점유율은 Synergy Research Group 2024년 기준 추정치이며, 측정 방법에 따라 차이가 있을 수 있습니다.

## 글로벌 4사 각 사 특징

### AWS — 가장 넓은 서비스 포트폴리오

Amazon의 이커머스 인프라에서 출발한 AWS는 가장 오래되고 가장 넓은 서비스 포트폴리오를 보유합니다. 새로운 서비스 카테고리를 가장 먼저 출시하는 경우가 많고, 글로벌 커뮤니티와 파트너 생태계가 가장 큽니다.

- **핵심 강점:** 서비스 다양성, 글로벌 리전 수, 커뮤니티/문서 풍부
- **차별점:** Lambda(서버리스 선구자), S3(객체 스토리지 표준), 가장 세분화된 IAM
- **한국 리전:** 서울 4 AZ (2016~)

### Azure — 엔터프라이즈 통합의 강자

Microsoft의 엔터프라이즈 소프트웨어 생태계(Microsoft 365, Active Directory, Dynamics 365)와 긴밀하게 통합됩니다. 기존 Microsoft 환경을 사용하는 기업에서 가장 자연스러운 선택입니다.

- **핵심 강점:** Microsoft 365/AD 통합, 하이브리드(Azure Arc, Azure Stack), 엔터프라이즈 계약(EA)
- **차별점:** 서울-부산 리전 쌍으로 국내 DR 가능, GitHub/VS Code 통합
- **한국 리전:** 서울(Korea Central) 3 AZ + 부산(Korea South)

### GCP — AI/ML과 데이터 분석

Google의 검색·데이터 처리 인프라에서 발전한 GCP는 AI/ML과 대규모 데이터 분석에서 차별화됩니다. 글로벌 VPC, SUD(자동 할인) 등 독특한 설계 철학을 가지고 있습니다.

- **핵심 강점:** AI/ML(Vertex AI, TPU, Gemini), 데이터 분석(BigQuery), 컨테이너(GKE)
- **차별점:** 글로벌 VPC(리전 종속 아님), SUD(약정 없이 자동 할인), Shared Fate 보안 모델
- **한국 리전:** 서울 3 Zone (2020~)

### OCI — 데이터베이스와 가격 경쟁력

Oracle의 데이터베이스 기술력을 클라우드로 확장한 OCI는 Oracle DB 워크로드에서 압도적 성능을 제공합니다. 이그레스 비용이 타사 대비 매우 저렴하고, 전용 베어메탈 인스턴스를 제공합니다.

- **핵심 강점:** Autonomous Database, Oracle DB 최적화, 이그레스 비용 저렴(10TB/월 무료)
- **차별점:** 이그레스 10TB/월 무료, Dedicated Region(고객 DC에 OCI 설치), MySQL HeatWave
- **한국 리전:** 서울(`ap-seoul-1`), 춘천(`ap-chuncheon-1`)

## 벤더 간 멀티클라우드 연동 서비스

글로벌 4사는 경쟁 관계이면서도, 고객의 멀티클라우드 수요에 대응하여 벤더 간 직접 연동 서비스를 출시하고 있습니다.

### 네트워크 직접 연결 (Cross-Cloud Interconnect)

벤더 간 전용 네트워크를 제공하여, 인터넷을 거치지 않고 프라이빗하게 클라우드를 연결합니다.

| 서비스 | 연결 구간 | 상태 (2026년 4월 기준) |
| --- | --- | --- |
| **[AWS Interconnect – multicloud](https://aws.amazon.com/interconnect/multicloud/)** | AWS ↔ GCP | GA (2026.04). Azure, OCI는 2026년 내 추가 예정 |
| **[Google Cross-Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/cross-cloud-overview)** | GCP ↔ AWS/Azure/OCI | GA. AWS와 공동 개발한 오픈 상호운용 스펙 기반 |
| **[Oracle Interconnect for Azure](https://docs.oracle.com/iaas/Content/multicloud/interconnect-azure.htm)** | OCI ↔ Azure | GA. 크로스 클라우드 데이터 전송 무료 |
| **[Oracle Interconnect for Google Cloud](https://docs.oracle.com/iaas/Content/Network/Concepts/access-to-google-cloud-platform.htm)** | OCI ↔ GCP | GA. 크로스 클라우드 데이터 전송 무료 |
| **Oracle Interconnect for AWS** | OCI ↔ AWS | 2026년 내 출시 예정 (AWS Interconnect–multicloud 연동) |

> 2025년 12월 AWS re:Invent에서 AWS와 Google Cloud가 오픈 상호운용 스펙 기반의 공동 멀티클라우드 인터커넥트를 발표했습니다. Microsoft Azure도 이 스펙에 참여를 확인했으며, Oracle도 AWS Interconnect–multicloud와의 연동을 발표(2026.04)했습니다.

### 타 클라우드 내 서비스 배치 (Database@Cloud)

자사 서비스를 경쟁사 데이터센터 안에 직접 배치하여, 고객이 단일 콘솔에서 멀티클라우드를 사용할 수 있게 합니다.

| 서비스 | 설명 |
| --- | --- |
| **[Oracle Database@Azure](https://www.oracle.com/cloud/azure/)** | Azure 데이터센터 내에 OCI Exadata를 배치. Azure Portal에서 Oracle DB를 네이티브로 프로비저닝 |
| **[Oracle Database@AWS](https://www.oracle.com/cloud/aws/)** | AWS 내에서 Oracle DB 서비스를 직접 사용 |
| **[Oracle Database@Google Cloud](https://www.oracle.com/cloud/google/)** | GCP 내에서 Oracle DB 서비스를 직접 사용 |

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

- [AWS에서 OCI로 마이그레이션](https://docs.oracle.com/en/solutions/migrate-aws-to-oci/)
- [OCI vs AWS 서비스 비교](https://docs.oracle.com/en-us/iaas/Content/General/Reference/awscomparison.htm)

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

### 글로벌 4사

- [AWS 제품](https://aws.amazon.com/ko/products/)
- [Azure 제품](https://azure.microsoft.com/ko-kr/products/)
- [Google Cloud 제품](https://cloud.google.com/products)
- [OCI 서비스](https://www.oracle.com/kr/cloud/)
- [한국클라우드산업협회](https://kcloud.or.kr/) — 국내 클라우드 업계 협의체
