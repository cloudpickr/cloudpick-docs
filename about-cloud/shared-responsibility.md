# 공동 책임 모델

## 왜 공동 책임인가

자체 전산센터를 임대 건물에서 운영한다고 가정해 보겠습니다. 건물의 출입 통제, 소방 설비, 전력 공급은 빌딩 관리 업체가 책임집니다. 하지만 서버실 내부의 장비 관리, 데이터 백업, 접근 권한 설정은 입주사인 우리가 책임져야 합니다. 빌딩 관리 업체가 아무리 보안을 잘해도, 서버실 비밀번호를 "1234"로 설정하면 보안 사고는 우리 책임입니다.

클라우드도 동일한 구조입니다. 클라우드를 사용한다고 해서 모든 보안과 운영 책임이 벤더에게 넘어가는 것은 아닙니다. 벤더와 사용자가 각각 책임져야 할 영역이 명확히 나뉘어 있으며, 이를 **공동 책임 모델(Shared Responsibility Model)**이라고 합니다.

## 핵심 개념

### 벤더의 책임 영역 — "클라우드의 보안 (Security of the Cloud)"

클라우드 벤더는 클라우드 인프라 자체의 보안을 책임집니다.

- **물리적 보안** — 데이터센터 건물, 출입 통제, CCTV, 생체 인증
- **하드웨어** — 서버, 스토리지, 네트워크 장비의 관리 및 교체
- **하이퍼바이저** — 가상화 계층의 보안 및 격리
- **네트워크 인프라** — 글로벌 백본 네트워크, 리전 간 연결

### 사용자의 책임 영역 — "클라우드 안에서의 보안 (Security in the Cloud)"

사용자는 클라우드 위에서 운영하는 워크로드의 보안을 책임집니다.

- **데이터** — 저장 데이터의 암호화, 분류, 접근 제어
- **애플리케이션** — 코드의 보안 취약점, 패치 관리
- **접근 제어** — IAM 정책, 사용자 권한, MFA 설정
- **운영 체제** — OS 패치, 보안 설정 (IaaS의 경우)
- **네트워크 설정** — 보안 그룹, 방화벽 규칙, VPC 구성

### 서비스 모델에 따른 책임 경계 변화

사용하는 서비스 모델(IaaS, PaaS, SaaS)에 따라 사용자의 책임 범위가 달라집니다. SaaS로 갈수록 벤더가 더 많은 영역을 관리하고, IaaS로 갈수록 사용자의 관리 영역이 넓어집니다.

| 영역 | IaaS | PaaS | SaaS |
| --- | --- | --- | --- |
| **데이터** | 사용자 | 사용자 | 사용자 |
| **애플리케이션** | 사용자 | 사용자 | 벤더 |
| **런타임** | 사용자 | 벤더 | 벤더 |
| **미들웨어** | 사용자 | 벤더 | 벤더 |
| **운영 체제** | 사용자 | 벤더 | 벤더 |
| **가상화** | 벤더 | 벤더 | 벤더 |
| **서버/스토리지/네트워크** | 벤더 | 벤더 | 벤더 |
| **물리적 보안** | 벤더 | 벤더 | 벤더 |

예를 들어, EC2(IaaS)를 사용하면 OS 패치부터 사용자 책임이지만, RDS(PaaS)를 사용하면 OS 패치는 AWS가 담당합니다. Google Workspace(SaaS)를 사용하면 애플리케이션 관리까지 Google이 담당하고, 사용자는 데이터와 접근 권한만 관리하면 됩니다.

## 3사 비교

| 항목 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **모델 이름** | Shared Responsibility Model | Shared Responsibility | Shared Fate |
| **기본 구조** | 전통적 공동 책임 | AWS와 유사 | 공동 운명 모델 |
| **벤더의 추가 지원** | Well-Architected Tool, Trusted Advisor | Defender for Cloud, Secure Score | Security Command Center, Assured Workloads |
| **보안 기본값** | 사용자가 명시적으로 설정 | 사용자가 명시적으로 설정 | 보안 기본값이 더 엄격 (예: 공개 버킷 차단) |
| **공식 문서** | [공동 책임 모델](https://aws.amazon.com/ko/compliance/shared-responsibility-model/) | [클라우드의 공동 책임](https://learn.microsoft.com/ko-kr/azure/security/fundamentals/shared-responsibility) | [Shared Fate](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate) |

### AWS — Shared Responsibility Model

AWS는 가장 전통적인 공동 책임 모델을 제시합니다. "클라우드의 보안"과 "클라우드 안에서의 보안"을 명확히 구분하며, 사용자가 자신의 책임 영역을 직접 관리해야 합니다. AWS는 이를 지원하기 위해 다양한 보안 서비스(GuardDuty, Security Hub, IAM Access Analyzer 등)를 제공하지만, 활성화와 설정은 사용자의 몫입니다.

### Azure — Shared Responsibility

Azure의 공동 책임 모델은 AWS와 구조적으로 유사합니다. 다만 Azure는 Microsoft의 엔터프라이즈 보안 생태계(Active Directory, Defender, Sentinel 등)와 긴밀하게 통합되어 있어, 기존 Microsoft 환경을 사용하는 조직에서는 보안 관리가 상대적으로 수월할 수 있습니다.

### GCP — Shared Fate (공동 운명 모델)

GCP는 전통적인 공동 책임 모델에서 한 발 더 나아가 **공동 운명 모델(Shared Fate)**을 제시합니다. 핵심 차이점은 다음과 같습니다.

- **벤더의 적극적 관여** — GCP는 고객이 보안을 잘 구성할 수 있도록 더 적극적으로 도구와 가이드를 제공합니다.
- **보안 기본값 강화** — 예를 들어, Cloud Storage 버킷은 기본적으로 공개 접근이 차단되어 있습니다.
- **Assured Workloads** — 규제 요건에 맞는 워크로드 환경을 자동으로 구성해 줍니다.
- **Security Command Center** — 보안 취약점을 자동으로 탐지하고 권장 조치를 제시합니다.

쉽게 말해, AWS/Azure가 "여기까지는 우리 책임, 나머지는 당신 책임"이라는 입장이라면, GCP는 "당신의 보안 성공이 곧 우리의 성공이므로, 함께 책임지겠다"는 입장입니다.

## 실무에서 자주 놓치는 부분

공동 책임 모델을 이해하고 있어도, 실무에서 자주 발생하는 보안 실수가 있습니다.

### 스토리지 공개 접근 설정

S3 버킷, Azure Blob, GCS 버킷을 실수로 퍼블릭으로 설정하여 데이터가 유출되는 사고가 빈번합니다. 이는 벤더의 책임이 아니라 사용자의 설정 실수입니다.

- **AWS** — S3 Block Public Access를 계정 수준에서 활성화하는 것을 권장합니다.
- **Azure** — Storage Account의 공개 접근을 비활성화하는 것을 권장합니다.
- **GCP** — 조직 정책으로 공개 접근을 차단할 수 있으며, 기본적으로 차단되어 있습니다.

### IAM 과다 권한

"일단 되게 하자"는 마음으로 관리자 권한을 부여하고, 이후 축소하지 않는 경우가 많습니다. **최소 권한 원칙(Principle of Least Privilege)**을 적용하여, 필요한 최소한의 권한만 부여해야 합니다.

### 암호화 키 관리

클라우드 벤더는 기본적으로 저장 데이터를 암호화하지만, 암호화 키의 관리 방식은 사용자가 선택해야 합니다. 벤더 관리 키(기본값)를 사용할지, 고객 관리 키(CMK/CMEK)를 사용할지, 또는 자체 키(BYOK)를 가져올지 결정해야 합니다.

## 한국에서의 고려사항

### CSAP (클라우드 보안 인증)

**CSAP(Cloud Security Assurance Program)**은 한국인터넷진흥원(KISA)이 운영하는 클라우드 보안 인증 제도입니다. 공공기관이 클라우드 서비스를 도입할 때 CSAP 인증을 받은 서비스를 우선적으로 검토하도록 되어 있습니다.

CSAP은 공동 책임 모델과 밀접한 관련이 있습니다. 벤더가 CSAP 인증을 받았다는 것은 벤더 책임 영역의 보안이 한국 기준을 충족한다는 의미이며, 사용자 책임 영역의 보안은 여전히 사용자가 관리해야 합니다.

각 CSP의 CSAP 대응 현황은 다음과 같습니다.

- **AWS** — IaaS/SaaS CSAP 인증 취득. 한국 공공 분야에서 가장 많이 사용되는 글로벌 CSP입니다.
- **Azure** — IaaS/SaaS CSAP 인증 취득. Microsoft 365 등 SaaS 서비스와의 통합이 강점입니다.
- **GCP** — CSAP 인증을 추진 중입니다.

### ISMS-P 인증

**ISMS-P(정보보호 및 개인정보보호 관리체계 인증)**는 한국의 정보보호 관리체계 인증 제도입니다. 일정 규모 이상의 사업자는 ISMS-P 인증이 의무이며, 클라우드 환경에서도 동일하게 적용됩니다.

클라우드 환경에서 ISMS-P 인증을 받으려면, 벤더의 보안 인증(CSAP, SOC 2, ISO 27001 등)과 함께 사용자 측의 보안 관리 체계도 갖추어야 합니다. 이는 공동 책임 모델의 사용자 책임 영역에 해당합니다.

### 금융 분야 추가 규제

금융 분야에서는 **전자금융감독규정**에 따라 클라우드 이용 시 추가적인 보안 요건을 충족해야 합니다. 금융보안원의 클라우드 이용 가이드라인을 참고하여, 데이터 분류, 접근 통제, 감사 로그 등을 적절히 구성해야 합니다.

## 참고하기

### AWS

- [공동 책임 모델](https://aws.amazon.com/ko/compliance/shared-responsibility-model/)
- [AWS 보안](https://aws.amazon.com/ko/security/)
- [AWS Artifact (컴플라이언스 보고서)](https://aws.amazon.com/ko/artifact/)

### Azure

- [클라우드의 공동 책임](https://learn.microsoft.com/ko-kr/azure/security/fundamentals/shared-responsibility)
- [Azure 보안](https://azure.microsoft.com/ko-kr/explore/security)
- [Azure 컴플라이언스](https://learn.microsoft.com/ko-kr/azure/compliance/)

### GCP

- [Shared Fate (공동 운명 모델)](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate)
- [Google Cloud 보안](https://cloud.google.com/security)
- [컴플라이언스 리소스 센터](https://cloud.google.com/security/compliance)
