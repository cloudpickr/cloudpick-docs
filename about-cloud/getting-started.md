---
description: 클라우드의 정의, IaaS/PaaS/SaaS 서비스 모델, 퍼블릭/프라이빗/하이브리드 배포 모델을 설명합니다.
---

# 클라우드 시작하기

> 문서 기준: 2026년 5월

## 클라우드의 정의

**클라우드 컴퓨팅** (Cloud Computing)은 컴퓨팅 리소스(서버, 스토리지, 네트워크 등)를 인터넷을 통해 온디맨드로 제공받는 서비스입니다. 잘 활용하면 인프라 구축 속도, 운영 효율성, 비용 구조 면에서 이점을 얻을 수 있습니다.

인프라 프로비저닝 관점에서, 자체 전산센터에서 서버를 구매하고 랙에 설치하고 네트워크를 구성하던 과정을 API 호출로 대체할 수 있습니다. 단, 보안 검토, 규제 요건 확인, 접근 통제 설계 등 사전 준비는 여전히 필요합니다.

다만, 모두에게 잘 알려진 비용 절감이나 안정적인 운영을 클라우드를 사용하는 것만으로 기대하기는 어렵습니다. 클라우드의 운영 방식에 맞춰서 애플리케이션의 아키텍처를 변경하는 과정이 필요합니다. 아키텍처를 변경하고 관리형 서비스를 최대한 활용하면, 운영 리소스를 효율화해 인적 자원과 예산을 비즈니스 가치 창출에 집중할 수 있게 됩니다. 단, 관리형 서비스 의존도가 높아질수록 벤더 종속성도 증가하므로 [출구 전략](../governance/exit-strategy.md)을 함께 고려해야 합니다.

{% hint style="info" %}
NIST SP 800-145는 클라우드 컴퓨팅을 다음과 같이 정의합니다.

> "최소한의 관리 노력이나 서비스 제공자와의 상호작용으로 빠르게 프로비저닝하고 해제할 수 있는, 구성 가능한 컴퓨팅 리소스의 공유 풀에 온디맨드로 네트워크 접근을 가능하게 하는 모델"
{% endhint %}

## 클라우드의 핵심 특성 (요약)

NIST가 정의한 클라우드의 5대 핵심 특성입니다.

| 특성 | 설명 | 온프레미스 대비 |
| --- | --- | --- |
| **온디맨드 셀프서비스** | 웹 콘솔/API로 몇 분 안에 리소스 생성 | 구매→설치 수 주~수 개월 → 즉시 |
| **광범위한 네트워크 접근** | 인터넷을 통해 어디서든 표준 프로토콜로 접근 | VPN/전용선 필요 → 불필요 |
| **리소스 풀링** | 멀티테넌트 모델로 동적 할당, 리전 수준 위치 지정 | 부서별 고정 할당 → 공유 풀 |
| **빠른 탄력성** | 트래픽에 따라 자동 확장/축소 | 최대 부하 기준 사전 확보 → 실시간 조정 |
| **측정 가능한 서비스** | 사용량 기반 종량제 (초/시간/GB 단위) | 감가상각 고정비 → 변동비 |

## 왜 클라우드를 사용하는가

NIST 5대 특성이 실무에서 어떤 가치를 만드는지, 온프레미스와 비교한 구체적 시나리오입니다.

### 탄력성 — 트래픽 변동에 즉시 대응

온프레미스에서는 블랙프라이데이나 신규 서비스 론칭 전에 수 주 전부터 서버를 추가 구매해야 합니다. 예측이 빗나가면 서버가 부족하거나(장애), 남거나(낭비) 합니다.

클라우드에서는 오토스케일링이 트래픽에 따라 수 분 내에 서버를 추가/제거합니다. 이벤트가 끝나면 자동으로 축소되어 비용이 줄어듭니다.

| 시나리오 | 온프레미스 | 클라우드 |
| --- | --- | --- |
| 이벤트 트래픽 10배 증가 | 수 주 전 서버 구매·설치 필요 | 오토스케일링으로 수 분 내 대응 |
| 이벤트 종료 후 | 남은 서버 유휴 (감가상각 진행) | 자동 축소, 비용 즉시 감소 |
| 예측 실패 시 | 서버 부족 → 장애 또는 긴급 구매 | 상한만 조정하면 즉시 확장 |

### 확장성 — 글로벌 서비스를 수 분 만에

온프레미스에서 해외 서비스를 시작하려면 현지 IDC 계약, 서버 배송, 네트워크 구성에 수 개월이 걸립니다.

클라우드에서는 원하는 리전을 선택하고 동일한 인프라 코드를 배포하면 수 분 내에 글로벌 서비스가 가능합니다.

| 시나리오 | 온프레미스 | 클라우드 |
| --- | --- | --- |
| 동남아 시장 진출 | IDC 계약 + 서버 구매 + 네트워크 (3~6개월) | 싱가포르 리전에 배포 (수 분) |
| 서비스 철수 결정 | 장비 처분, 계약 해지 (위약금) | 리소스 삭제 (즉시, 비용 0) |

{% hint style="info" %}
위 표는 인프라 프로비저닝 속도만을 비교한 것입니다. 실제 해외 진출 시에는 현지 규제, 데이터 주권, 규정 준수 검토가 선행되어야 합니다.
{% endhint %}

### 비용 구조 전환 — 고정비에서 변동비로

온프레미스는 서버를 구매하는 순간 감가상각이 시작되는 **자본 지출** (CapEx)입니다. 클라우드는 사용한 만큼만 내는 **운영 지출** (OpEx)로 전환합니다. 단, 아키텍처를 클라우드에 맞게 설계해야 이 이점을 누릴 수 있습니다. 온프레미스 방식 그대로 클라우드에 올리면(Lift & Shift) 오히려 비용이 증가할 수 있습니다.

{% hint style="warning" %}
**클라우드 = 자동으로 저렴해지는 것은 아닙니다.** 클라우드의 이점을 누리려면 아키텍처를 클라우드 네이티브로 설계하고, 비용을 지속적으로 모니터링해야 합니다. 상세 비용 구조는 [비용 구조 이해하기](pricing-model.md)를, 비용 최적화 운영은 [FinOps](../governance/finops.md)를 참고하세요.
{% endhint %}

### 운영 부담 감소 — 관리형 서비스 활용

온프레미스에서 데이터베이스를 운영하려면 OS 패치, DB 엔진 업데이트, 백업, 복제, 장애 조치를 모두 직접 해야 합니다.

클라우드의 관리형 서비스(RDS, Cloud SQL 등)는 이 운영 부담을 벤더가 대신 처리합니다. DBA는 스키마 설계와 쿼리 최적화에 집중할 수 있습니다.

## 서비스 모델: IaaS, PaaS, SaaS

클라우드 서비스는 벤더가 관리하는 범위에 따라 세 가지 모델로 나뉩니다. 자체 전산센터에 비유하면 다음과 같습니다.

- **IaaS(Infrastructure as a Service)** — 건물을 임대하는 것과 비슷합니다. 건물(서버, 네트워크, 스토리지)은 제공되지만, 내부 인테리어(OS, 미들웨어, 애플리케이션)는 직접 구성해야 합니다.
- **PaaS(Platform as a Service)** — 사무실을 임대하는 것과 비슷합니다. 책상과 의자(런타임, 미들웨어)까지 갖춰져 있어서, 업무(애플리케이션 코드)에만 집중할 수 있습니다.
- **SaaS(Software as a Service)** — 호텔에 투숙하는 것과 비슷합니다. 모든 것이 준비되어 있고, 서비스를 그대로 사용하기만 하면 됩니다.

| 서비스 모델 | 사용자 관리 영역 | AWS 예시 | Azure 예시 | Google Cloud 예시 |
| --- | --- | --- | --- | --- |
| **IaaS** | OS, 미들웨어, 앱, 데이터 | EC2, EBS, VPC | Virtual Machines, VNet | Compute Engine, VPC |
| **PaaS** | 앱, 데이터 | Elastic Beanstalk, RDS | App Service, Azure SQL | App Engine, Cloud SQL |
| **SaaS** | 데이터(설정) | WorkMail, Chime | Microsoft 365, Dynamics 365 | Google Workspace |

서비스 모델에 따라 사용자와 벤더의 책임 범위가 달라집니다. 이 부분은 [공동 책임 모델](shared-responsibility.md)에서 자세히 다룹니다.

## 배포 모델: 퍼블릭, 프라이빗, 하이브리드

클라우드는 누가 인프라를 소유하고 운영하느냐에 따라 세 가지 배포 모델로 나뉩니다.

### 퍼블릭 클라우드 (Public Cloud)

AWS, Azure, Google Cloud 같은 벤더가 소유·운영하는 인프라를 인터넷을 통해 여러 고객이 공유하는 모델입니다. 초기 투자 없이 바로 사용할 수 있고, 탄력적인 확장이 가능합니다. CloudPick에서 다루는 대부분의 내용은 퍼블릭 클라우드를 기준으로 합니다.

### 프라이빗 클라우드 (Private Cloud)

특정 조직만을 위해 운영되는 클라우드입니다. 자체 데이터센터에 구축하거나, 벤더가 전용 인프라를 제공하는 형태입니다. 보안과 규제 요건이 엄격한 금융·공공 분야에서 많이 사용됩니다.

### 하이브리드 클라우드 (Hybrid Cloud)

퍼블릭 클라우드와 프라이빗 클라우드(또는 온프레미스)를 연결하여 함께 사용하는 모델입니다. 민감한 데이터는 프라이빗 환경에, 탄력적인 워크로드는 퍼블릭 클라우드에 배치하는 방식으로 운영합니다.

| 배포 모델 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **퍼블릭** | AWS 리전 | Azure 리전 | Google Cloud 리전 | OCI 리전 |
| **프라이빗/온프레미스 확장** | Outposts | Azure Stack, Azure Local | Google Distributed Cloud | Dedicated Region |
| **하이브리드 관리** | EKS Anywhere, ECS Anywhere | Azure Arc | Anthos | OCI Multicloud |

## 멀티클라우드 이해하기

하나의 클라우드 벤더만 사용하는 것이 가장 단순하지만, 실무에서는 여러 벤더를 함께 사용하는 **멀티클라우드** (Multi-Cloud) 전략을 채택하는 조직이 늘고 있습니다. CNCF 2024 조사에 따르면 기업의 약 60%가 2개 이상의 클라우드를 사용합니다.

멀티클라우드의 도입 동기와 도전 과제는 [멀티클라우드 이해하기](why-multicloud.md)에서 자세히 다룹니다.

CloudPick은 주요 글로벌 클라우드 벤더를 중심으로, 멀티클라우드 환경에서 올바른 의사결정을 내릴 수 있도록 돕는 것을 목표로 합니다.

## 자주 하는 실수

- **"클라우드로 옮기면 자동으로 비용이 줄어든다"** — 온프레미스 구조 그대로 올리면(Lift & Shift) 오히려 비용이 증가할 수 있습니다. 클라우드 네이티브 아키텍처 전환이 필요합니다.
- **"클라우드는 벤더가 다 관리해 준다"** — 서비스 모델(IaaS/PaaS/SaaS)에 따라 사용자 책임 범위가 다릅니다. 데이터와 접근 제어는 항상 사용자 책임입니다.
- **"프리 티어로 충분히 운영할 수 있다"** — 프리 티어는 학습과 PoC용입니다. 무료 범위를 초과하면 예상치 못한 과금이 발생할 수 있으므로 예산 알림을 설정하세요.

## 체크리스트

- [ ] 사용할 벤더의 프리 티어 범위와 제한 조건을 확인했는가?
- [ ] 루트/관리자 계정에 MFA(다중 인증)를 활성화했는가?
- [ ] 예산 알림(Budget Alert)을 설정하여 예상치 못한 과금을 방지했는가?

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

### Google Cloud

- [What is Cloud Computing?](https://cloud.google.com/learn/what-is-cloud-computing)
- [Why Google Cloud](https://cloud.google.com/why-google-cloud)
- [Google Cloud 위치](https://cloud.google.com/about/locations)

### OCI

- [OCI란?](https://www.oracle.com/kr/cloud/what-is-cloud-computing/)
- [OCI 서비스](https://www.oracle.com/kr/cloud/)
- [OCI 글로벌 인프라](https://www.oracle.com/cloud/cloud-regions/)
