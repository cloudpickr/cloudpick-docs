# 클라우드란?

## 클라우드의 정의

**클라우드 컴퓨팅(Cloud Computing)**은 서비스 구축을 위한 인프라를 빠르고, 높은 효율성과 함께, 규모의 경제를 이용해 비용을 절감할 수 있도록 도와주는 서비스입니다.

미국 국립표준기술연구소(NIST)는 클라우드 컴퓨팅을 다음과 같이 정의하고 있습니다:

> 최소한의 관리 노력이나 서비스 제공자와의 상호작용으로 빠르게 프로비저닝하고 해제할 수 있는, 구성 가능한 컴퓨팅 리소스(네트워크, 서버, 스토리지, 애플리케이션, 서비스)의 공유 풀에 온디맨드로 네트워크 접근을 가능하게 하는 모델

쉽게 말해, 자체 전산센터에서 서버를 구매하고 랙에 설치하고 네트워크를 구성하던 과정을 API 호출 한 번으로 대체할 수 있는 서비스입니다.

다만, 모두에게 잘 알려진 비용 절감이나 안정적인 운영을 클라우드를 사용하는 것만으로 기대하기는 어렵습니다. 클라우드의 운영 방식에 맞춰서 애플리케이션의 아키텍처를 변경하는 과정이 필요합니다. 아키텍처를 변경하고 관리형 서비스를 최대한 활용하면, 운영 리소스를 효율화해 가용한 인적·비용 자원을 비즈니스에 집중할 수 있게 됩니다.

## 클라우드의 핵심 특성

NIST가 정의한 클라우드의 5대 핵심 특성을 온프레미스 환경과 비교하면 다음과 같습니다.

### 온디맨드 셀프서비스 (On-Demand Self-Service)

자체 전산센터에서 서버를 추가하려면 구매 요청 → 승인 → 발주 → 납품 → 설치까지 수 주에서 수 개월이 걸립니다. 클라우드에서는 웹 콘솔이나 API를 통해 몇 분 안에 서버를 생성할 수 있습니다. 별도의 승인 프로세스나 물리적 작업 없이, 필요한 시점에 필요한 만큼의 리소스를 직접 프로비저닝할 수 있습니다.

### 광범위한 네트워크 접근 (Broad Network Access)

온프레미스 환경에서는 VPN이나 전용선을 통해서만 내부 시스템에 접근할 수 있는 경우가 많습니다. 클라우드 서비스는 인터넷을 통해 어디서든 표준 프로토콜로 접근할 수 있습니다. 노트북, 스마트폰, 태블릿 등 다양한 디바이스에서 동일한 서비스를 이용할 수 있습니다.

### 리소스 풀링 (Resource Pooling)

자체 전산센터에서는 각 부서나 프로젝트별로 서버를 할당하면, 사용률이 낮은 서버도 다른 곳에 재할당하기 어렵습니다. 클라우드 벤더는 대규모 리소스 풀을 운영하며, **멀티테넌트(Multi-Tenant)** 모델로 여러 고객에게 동적으로 리소스를 할당합니다. 사용자는 리소스의 물리적 위치를 정확히 알 필요 없이, 리전(Region) 수준에서 위치를 지정할 수 있습니다.

### 빠른 탄력성 (Rapid Elasticity)

온프레미스에서 트래픽 급증에 대비하려면 최대 부하 기준으로 서버를 미리 확보해야 합니다. 평소에는 대부분의 리소스가 유휴 상태로 남게 됩니다. 클라우드에서는 트래픽에 따라 리소스를 자동으로 확장(Scale Out)하거나 축소(Scale In)할 수 있습니다. 이벤트 기간에만 서버를 10배로 늘렸다가, 이벤트가 끝나면 원래대로 줄이는 것이 가능합니다.

### 측정 가능한 서비스 (Measured Service)

자체 전산센터에서는 서버를 구매하면 사용 여부와 관계없이 감가상각 비용이 발생합니다. 클라우드는 **종량제(Pay-As-You-Go)** 모델로, 실제 사용한 만큼만 비용을 지불합니다. 컴퓨팅은 시간 또는 초 단위, 스토리지는 GB 단위, 네트워크는 전송량 단위로 과금됩니다. 사용량은 실시간으로 모니터링되며, 투명하게 확인할 수 있습니다.

## 서비스 모델: IaaS, PaaS, SaaS

클라우드 서비스는 벤더가 관리하는 범위에 따라 세 가지 모델로 나뉩니다. 자체 전산센터에 비유하면 다음과 같습니다.

- **IaaS(Infrastructure as a Service)** — 건물을 임대하는 것과 비슷합니다. 건물(서버, 네트워크, 스토리지)은 제공되지만, 내부 인테리어(OS, 미들웨어, 애플리케이션)는 직접 구성해야 합니다.
- **PaaS(Platform as a Service)** — 사무실을 임대하는 것과 비슷합니다. 책상과 의자(런타임, 미들웨어)까지 갖춰져 있어서, 업무(애플리케이션 코드)에만 집중할 수 있습니다.
- **SaaS(Software as a Service)** — 호텔에 투숙하는 것과 비슷합니다. 모든 것이 준비되어 있고, 서비스를 그대로 사용하기만 하면 됩니다.

| 서비스 모델 | 사용자 관리 영역 | AWS 예시 | Azure 예시 | GCP 예시 |
| --- | --- | --- | --- | --- |
| **IaaS** | OS, 미들웨어, 앱, 데이터 | EC2, EBS, VPC | Virtual Machines, VNet | Compute Engine, VPC |
| **PaaS** | 앱, 데이터 | Elastic Beanstalk, RDS | App Service, Azure SQL | App Engine, Cloud SQL |
| **SaaS** | 데이터(설정) | WorkMail, Chime | Microsoft 365, Dynamics 365 | Google Workspace |

서비스 모델에 따라 사용자와 벤더의 책임 범위가 달라집니다. 이 부분은 [공동 책임 모델](shared-responsibility.md)에서 자세히 다룹니다.

## 배포 모델: 퍼블릭, 프라이빗, 하이브리드

클라우드는 누가 인프라를 소유하고 운영하느냐에 따라 세 가지 배포 모델로 나뉩니다.

### 퍼블릭 클라우드 (Public Cloud)

AWS, Azure, GCP 같은 벤더가 소유·운영하는 인프라를 인터넷을 통해 여러 고객이 공유하는 모델입니다. 초기 투자 없이 바로 사용할 수 있고, 탄력적인 확장이 가능합니다. CloudPick에서 다루는 대부분의 내용은 퍼블릭 클라우드를 기준으로 합니다.

### 프라이빗 클라우드 (Private Cloud)

특정 조직만을 위해 운영되는 클라우드입니다. 자체 데이터센터에 구축하거나, 벤더가 전용 인프라를 제공하는 형태입니다. 보안과 규제 요건이 엄격한 금융·공공 분야에서 많이 사용됩니다.

### 하이브리드 클라우드 (Hybrid Cloud)

퍼블릭 클라우드와 프라이빗 클라우드(또는 온프레미스)를 연결하여 함께 사용하는 모델입니다. 민감한 데이터는 프라이빗 환경에, 탄력적인 워크로드는 퍼블릭 클라우드에 배치하는 방식으로 운영합니다.

| 배포 모델 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **퍼블릭** | AWS 리전 | Azure 리전 | GCP 리전 |
| **프라이빗/온프레미스 확장** | Outposts | Azure Stack, Azure Local | Google Distributed Cloud |
| **하이브리드 관리** | EKS Anywhere, ECS Anywhere | Azure Arc | Anthos |

## 왜 멀티클라우드인가?

하나의 클라우드 벤더만 사용하는 것이 가장 단순하지만, 실무에서는 여러 벤더를 함께 사용하는 **멀티클라우드(Multi-Cloud)** 전략을 채택하는 조직이 늘고 있습니다.

- **벤더 종속(Vendor Lock-in) 회피** — 특정 벤더에 과도하게 의존하면, 가격 인상이나 서비스 변경에 대응하기 어렵습니다.
- **서비스별 강점 활용** — 예를 들어, AI/ML은 GCP, 엔터프라이즈 통합은 Azure, 가장 넓은 서비스 포트폴리오는 AWS처럼 각 벤더의 강점을 조합할 수 있습니다.
- **규제 대응** — 특정 데이터는 국내에, 특정 워크로드는 해외에 배치해야 하는 규제 요건을 충족할 수 있습니다.
- **가용성 극대화** — 하나의 벤더에 장애가 발생해도 다른 벤더로 서비스를 유지할 수 있습니다.

CloudPick은 AWS, Azure, GCP 3사를 중심으로 각 벤더의 개념과 차이점을 비교하여, 멀티클라우드 환경에서 올바른 의사결정을 내릴 수 있도록 돕는 것을 목표로 합니다.

## 한국에서의 고려사항

### 한국 리전 보유 현황

2025년 기준, 한국(서울)에 리전을 보유한 주요 클라우드 벤더는 다음과 같습니다.

| 구분 | 벤더 | 한국 리전 |
| --- | --- | --- |
| 글로벌 | AWS | 아시아 태평양(서울) `ap-northeast-2` — 4개 AZ |
| 글로벌 | Azure | Korea Central(서울), Korea South(부산) |
| 글로벌 | GCP | asia-northeast3(서울) — 3개 Zone |
| 글로벌 | OCI | ap-seoul-1, ap-chuncheon-1 |
| 글로벌 | Alibaba Cloud | ap-northeast-2(서울) |
| 글로벌 | Tencent Cloud | ap-seoul(서울) |
| 국내 | Naver Cloud Platform | 한국(수도권 2개 리전) |
| 국내 | KT Cloud | 한국(수도권, 대전 등) |
| 국내 | NHN Cloud | 한국(판교, 평촌) |

### CSAP (클라우드 보안 인증)

한국에서 공공기관이나 금융기관에 클라우드 서비스를 제공하려면 **CSAP(Cloud Security Assurance Program, 클라우드 보안 인증)**을 취득해야 합니다. CSAP은 한국인터넷진흥원(KISA)이 운영하는 인증 제도로, IaaS와 SaaS 등급으로 나뉩니다.

글로벌 3사 중 AWS와 Azure는 한국 CSAP 인증을 취득하고 있으며, GCP도 인증을 추진하고 있습니다. 국내 벤더인 NCP, KT Cloud, NHN Cloud는 모두 CSAP 인증을 보유하고 있어, 공공·금융 분야에서 강점을 가지고 있습니다.

### 데이터 주권

한국의 **개인정보보호법**과 **신용정보법** 등은 특정 유형의 데이터를 국내에 저장하도록 요구하는 경우가 있습니다. 특히 금융 분야에서는 고유식별정보와 개인신용정보의 국외 이전에 대한 규제가 엄격합니다. 클라우드 벤더를 선택할 때 한국 리전의 유무와 데이터 저장 위치를 반드시 확인해야 합니다.

## 이 섹션에서 다루는 내용

CloudPick의 "클라우드의 개념" 섹션에서는 클라우드를 이해하기 위한 핵심 주제를 다음과 같이 다루고 있습니다.

| 문서 | 설명 |
| --- | --- |
| [벤더 비교하기](compare-clouds.md) | AWS, Azure, GCP의 강점과 공식 비교 자료, 속도 비교 도구를 정리합니다. |
| [리전과 가용영역](regions-and-zones.md) | 리전, 가용영역, 엣지 로케이션의 개념과 3사의 구조적 차이를 비교합니다. |
| [공동 책임 모델](shared-responsibility.md) | 벤더와 사용자의 보안 책임 경계를 서비스 모델별로 설명합니다. |
| [비용 구조 이해하기](pricing-model.md) | 온디맨드, 예약, 스팟 등 과금 모델과 3사의 핵심 차이를 비교합니다. |
| [콘솔, CLI, SDK](console-cli-sdk.md) | 클라우드를 다루는 세 가지 방법과 IaC 도구를 소개합니다. |
| [계정과 조직 구조](accounts-and-organizations.md) | Account, Subscription, Project 등 3사의 계정 체계를 비교합니다. |
| [Well-Architected Framework](well-architected.md) | 클라우드 아키텍처 설계의 모범 사례와 3사의 핵심 원칙을 비교합니다. |

## 참고하기

### AWS

- [클라우드 컴퓨팅이란?](https://aws.amazon.com/ko/what-is-cloud-computing/)
- [AWS란 무엇인가?](https://aws.amazon.com/ko/what-is-aws/)
- [AWS 글로벌 인프라](https://aws.amazon.com/ko/about-aws/global-infrastructure/)

### Azure

- [클라우드 컴퓨팅이란?](https://azure.microsoft.com/ko-kr/resources/cloud-computing-dictionary/what-is-cloud-computing)
- [Azure란?](https://azure.microsoft.com/ko-kr/resources/cloud-computing-dictionary/what-is-azure)
- [Azure 글로벌 인프라](https://azure.microsoft.com/ko-kr/explore/global-infrastructure/)

### GCP

- [What is Cloud Computing?](https://cloud.google.com/learn/what-is-cloud-computing)
- [Why Google Cloud](https://cloud.google.com/why-google-cloud)
- [Google Cloud 위치](https://cloud.google.com/about/locations)
