# 클라우드란?

## 이 문서의 위치

이 문서는 멀티클라우드 환경을 이해하기 위한 기초 개념을 정리합니다. 이미 클라우드를 사용하고 있다면 [왜 멀티클라우드인가?](why-multicloud.md)부터 읽는 것을 권장합니다.

## 클라우드의 정의

**클라우드 컴퓨팅(Cloud Computing)**은 서비스 구축을 위한 인프라를 빠르고, 높은 효율성과 함께, 규모의 경제를 이용해 비용을 절감할 수 있도록 도와주는 서비스입니다.

쉽게 말해, 자체 전산센터에서 서버를 구매하고 랙에 설치하고 네트워크를 구성하던 과정을 API 호출 한 번으로 대체할 수 있는 서비스입니다.

다만, 모두에게 잘 알려진 비용 절감이나 안정적인 운영을 클라우드를 사용하는 것만으로 기대하기는 어렵습니다. 클라우드의 운영 방식에 맞춰서 애플리케이션의 아키텍처를 변경하는 과정이 필요합니다. 아키텍처를 변경하고 관리형 서비스를 최대한 활용하면, 운영 리소스를 효율화해 가용한 인적·비용 자원을 비즈니스에 집중할 수 있게 됩니다.

> NIST SP 800-145는 클라우드 컴퓨팅을 "최소한의 관리 노력이나 서비스 제공자와의 상호작용으로 빠르게 프로비저닝하고 해제할 수 있는, 구성 가능한 컴퓨팅 리소스의 공유 풀에 온디맨드로 네트워크 접근을 가능하게 하는 모델"로 정의합니다.

## 클라우드의 핵심 특성 (요약)

NIST가 정의한 클라우드의 5대 핵심 특성입니다.

| 특성 | 설명 | 온프레미스 대비 |
| --- | --- | --- |
| **온디맨드 셀프서비스** | 웹 콘솔/API로 몇 분 안에 리소스 생성 | 구매→설치 수 주~수 개월 → 즉시 |
| **광범위한 네트워크 접근** | 인터넷을 통해 어디서든 표준 프로토콜로 접근 | VPN/전용선 필요 → 불필요 |
| **리소스 풀링** | 멀티테넌트 모델로 동적 할당, 리전 수준 위치 지정 | 부서별 고정 할당 → 공유 풀 |
| **빠른 탄력성** | 트래픽에 따라 자동 확장/축소 | 최대 부하 기준 사전 확보 → 실시간 조정 |
| **측정 가능한 서비스** | 사용량 기반 종량제 (초/시간/GB 단위) | 감가상각 고정비 → 변동비 |

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

하나의 클라우드 벤더만 사용하는 것이 가장 단순하지만, 실무에서는 여러 벤더를 함께 사용하는 **멀티클라우드(Multi-Cloud)** 전략을 채택하는 조직이 늘고 있습니다. CNCF 2024 조사에 따르면 기업의 약 60%가 2개 이상의 클라우드를 사용합니다.

멀티클라우드의 도입 동기와 도전 과제는 [왜 멀티클라우드인가?](why-multicloud.md)에서 자세히 다룹니다.

CloudPick은 글로벌 4사(AWS, Azure, GCP, OCI)와 국내 4사(NCP, KT Cloud, NHN Cloud, Kakao Cloud)를 포함하여, 멀티클라우드 환경에서 올바른 의사결정을 내릴 수 있도록 돕는 것을 목표로 합니다.

## 한국에서의 고려사항

### 한국 리전 보유 현황

2025년 기준, 한국(서울)에 리전을 보유한 주요 클라우드 벤더는 다음과 같습니다.

| 구분 | 벤더 | 한국 리전 |
| --- | --- | --- |
| 글로벌 | AWS | `ap-northeast-2` (서울) — 4개 AZ |
| 글로벌 | Azure | `koreacentral` (서울), `koreasouth` (부산) |
| 글로벌 | GCP | `asia-northeast3` (서울) — 3개 Zone |
| 글로벌 | OCI | `ap-seoul-1` (서울), `ap-chuncheon-1` (춘천) |
| 국내 | Naver Cloud Platform | 수도권 2개 리전 |
| 국내 | KT Cloud | 수도권, 대전 등 |
| 국내 | NHN Cloud | 판교, 평촌 |
| 국내 | Kakao Cloud | 판교, 안산 |

### 클라우드 보안 인증

한국에서 공공·금융 분야에 클라우드를 도입하려면 보안 인증이 필요합니다. 기존에는 CSAP(클라우드 보안 인증 제도)이 대표적이었으나, 현재 N2SF(국가망보안체계) 도입과 국정원 통합 등 제도 변화가 진행 중입니다.

도입 검토 시 각 벤더의 공식 컴플라이언스 페이지에서 최신 인증 현황을 확인하시기 바랍니다.

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

### 표준 및 프레임워크

- [NIST SP 800-145 — The NIST Definition of Cloud Computing](https://csrc.nist.gov/publications/detail/sp/800-145/final) — 클라우드 컴퓨팅 공식 정의
- [ISO/IEC 17788 — Cloud computing: Overview and vocabulary](https://www.iso.org/standard/60544.html) — 클라우드 용어 표준
- [ISO/IEC 22123 — Cloud computing: Concepts and terminology](https://www.iso.org/standard/82758.html) — 멀티클라우드 포함 최신 표준

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
