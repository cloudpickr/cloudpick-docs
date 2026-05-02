# Well-Architected Framework

## Well-Architected란?

건물을 설계할 때 내진 설계, 방화 구획, 에너지 효율 등의 건축 기준이 있듯이, 클라우드 워크로드를 설계할 때도 따라야 할 모범 사례가 있습니다. 이를 체계적으로 정리한 것이 **Well-Architected Framework**입니다.

온프레미스 환경에서는 서버를 구매하고 설치하는 데 시간이 오래 걸리기 때문에, 설계를 신중하게 하는 경향이 있습니다. 반면 클라우드에서는 리소스를 몇 분 만에 생성할 수 있어, "일단 만들고 나중에 고치자"는 접근이 쉽습니다. 하지만 이렇게 만들어진 워크로드는 보안 취약점, 비용 낭비, 장애 취약성 등의 문제를 안게 됩니다.

Well-Architected Framework은 이러한 문제를 사전에 방지하기 위한 설계 원칙과 체크리스트를 제공합니다. 새로운 워크로드를 설계할 때뿐 아니라, 기존 워크로드를 점검하고 개선할 때도 활용할 수 있습니다.

## 핵심 원칙 (Pillar) 비교

3사 모두 Well-Architected Framework을 제공하지만, 핵심 원칙(Pillar)의 구성과 강조점에 차이가 있습니다.

| 원칙 영역 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **운영 우수성** | Operational Excellence | Operational Excellence | Operational Excellence |
| **보안** | Security | Security | Security, Privacy, Compliance |
| **안정성** | Reliability | Reliability | Reliability |
| **성능 효율성** | Performance Efficiency | Performance Efficiency | Performance Optimization |
| **비용 최적화** | Cost Optimization | Cost Optimization | Cost Optimization |
| **지속 가능성** | Sustainability | — | — |
| **Pillar 수** | **6개** | **5개** | **5개** (+ 시스템 설계 원칙) |

### AWS — 6개 Pillar

AWS는 2012년에 가장 먼저 Well-Architected Framework을 발표했으며, 현재 6개의 Pillar로 구성되어 있습니다.

1. **운영 우수성 (Operational Excellence)** — 워크로드를 효과적으로 운영하고 지속적으로 개선하는 방법
2. **보안 (Security)** — 데이터, 시스템, 자산을 보호하는 방법
3. **안정성 (Reliability)** — 장애로부터 복구하고 가용성을 유지하는 방법
4. **성능 효율성 (Performance Efficiency)** — 리소스를 효율적으로 사용하여 성능 요구사항을 충족하는 방법
5. **비용 최적화 (Cost Optimization)** — 불필요한 비용을 제거하고 투자 수익을 극대화하는 방법
6. **지속 가능성 (Sustainability)** — 환경에 미치는 영향을 최소화하는 방법

AWS만의 특징은 **지속 가능성(Sustainability)** Pillar입니다. 2021년에 추가되었으며, 에너지 효율적인 리소스 선택, 사용량 최적화 등 환경적 영향을 고려한 설계 원칙을 다룹니다.

### Azure — 5개 Pillar

Azure의 Well-Architected Framework은 5개의 Pillar로 구성되어 있습니다.

1. **안정성 (Reliability)** — 장애 복구, 가용성, 복원력
2. **보안 (Security)** — 위협 보호, 데이터 보안, ID 관리
3. **비용 최적화 (Cost Optimization)** — 비용 관리, 리소스 최적화
4. **운영 우수성 (Operational Excellence)** — 운영 프로세스, 모니터링, 배포
5. **성능 효율성 (Performance Efficiency)** — 확장성, 성능 최적화

Azure의 특징은 Microsoft의 엔터프라이즈 경험이 반영되어 있다는 점입니다. 특히 하이브리드 환경과 Microsoft 제품군(Active Directory, Microsoft 365 등)과의 통합을 고려한 가이드가 포함되어 있습니다.

### GCP — 5개 Pillar + 시스템 설계 원칙

GCP는 **Architecture Framework**이라는 이름으로 Well-Architected 가이드를 제공합니다. 5개의 Pillar 외에 **시스템 설계 원칙(System Design Principles)**을 별도로 다루는 것이 특징입니다.

1. **운영 우수성 (Operational Excellence)** — 효율적인 운영, 자동화, 모니터링
2. **보안, 개인정보, 컴플라이언스 (Security, Privacy, Compliance)** — 보안과 규제 준수를 하나의 Pillar로 통합
3. **안정성 (Reliability)** — 가용성, 복원력, 재해복구
4. **비용 최적화 (Cost Optimization)** — 비용 관리, 리소스 최적화
5. **성능 최적화 (Performance Optimization)** — 확장성, 지연 시간 최적화

GCP의 특징은 **보안과 컴플라이언스를 하나의 Pillar로 통합**한 점입니다. 이는 GCP의 Shared Fate 모델과 일맥상통하며, 보안과 규제 준수를 분리할 수 없는 하나의 주제로 다루고 있습니다.

## 리뷰 도구

각 벤더는 Well-Architected Framework에 기반한 워크로드 리뷰 도구를 제공합니다.

| 항목 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **도구 이름** | Well-Architected Tool | Well-Architected Review (Assessment) | Architecture Framework 체크리스트 |
| **위치** | AWS 콘솔 내장 | Azure Advisor + 별도 Assessment | 문서 기반 체크리스트 |
| **자동 분석** | 일부 자동 (Trusted Advisor 연동) | Azure Advisor가 자동 권장 | Recommender가 자동 권장 |
| **보고서** | PDF/JSON 내보내기 | Assessment 보고서 | — |
| **비용** | 무료 | 무료 | 무료 |

### AWS Well-Architected Tool

AWS 콘솔에 내장된 도구로, 워크로드를 정의하고 각 Pillar별 질문에 답하면 개선 사항을 제시합니다. **Well-Architected Labs**에서 실습 자료도 제공합니다.

### Azure Well-Architected Review

Azure Advisor가 자동으로 리소스를 분석하여 권장 사항을 제시하며, 별도의 Assessment 도구를 통해 체계적인 리뷰를 수행할 수 있습니다.

### GCP Architecture Framework

문서 기반의 체크리스트와 가이드를 제공하며, Recommender와 Active Assist가 자동으로 최적화 권장 사항을 제시합니다.

## Cloud Adoption Framework (CAF)

Well-Architected Framework이 개별 워크로드의 설계 모범 사례라면, **Cloud Adoption Framework(CAF)**은 조직 전체의 클라우드 전환 전략을 다룹니다. 기술뿐 아니라 조직 구조, 프로세스, 거버넌스, 인력 교육까지 포괄하는 상위 수준의 프레임워크입니다.

| 항목 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **이름** | AWS Cloud Adoption Framework | Azure Cloud Adoption Framework | Google Cloud Architecture Framework |
| **구성** | 6개 관점 (비즈니스, 인력, 거버넌스, 플랫폼, 보안, 운영) | 9단계 방법론 (전략, 계획, 준비, 채택, 거버넌스, 관리 등) | 아키텍처 프레임워크 내 도입 가이드 포함 |
| **특징** | 관점(Perspective)별 이해관계자 중심 | 단계별 실행 가이드, Landing Zone 포함 | 아키텍처 프레임워크와 통합 |

AWS와 Azure는 독립적인 CAF를 제공하며, GCP는 Architecture Framework 안에 도입 가이드를 포함하는 형태입니다. Azure의 CAF는 특히 상세한 단계별 가이드와 Landing Zone 구성 방법을 제공하여, 대규모 조직의 클라우드 전환에 많이 참고됩니다.

## 한국에서의 고려사항

### 한국어 문서 지원

- **AWS** — Well-Architected Framework 한국어 번역이 제공됩니다. Well-Architected Labs도 일부 한국어로 제공됩니다.
- **Azure** — Well-Architected Framework과 CAF 모두 한국어 번역이 잘 되어 있습니다. Microsoft Learn을 통해 체계적으로 학습할 수 있습니다.
- **GCP** — Architecture Framework의 한국어 번역은 제한적입니다. 영문 문서를 참고해야 하는 경우가 많습니다.

### 국내 컴플라이언스와 WAF 보안 Pillar

Well-Architected Framework의 보안 Pillar를 적용할 때, 한국의 컴플라이언스 요건을 함께 고려해야 합니다.

- **ISMS-P** — 정보보호 관리체계 인증. WAF의 보안 Pillar와 상당 부분 매핑됩니다.
- **CSAP** — 클라우드 보안 인증. 벤더 측 보안 요건을 다루며, WAF의 공동 책임 모델과 연결됩니다.
- **개인정보보호법** — 데이터 보호 관련 요건. WAF의 데이터 보호 가이드와 함께 적용해야 합니다.

### 아키텍처 지원 프로그램

각 벤더는 한국에서 아키텍처 설계를 지원하는 프로그램을 운영하고 있습니다.

- **AWS** — Solutions Architect(SA)가 Well-Architected Review를 무료로 지원합니다. 파트너를 통한 리뷰도 가능합니다.
- **Azure** — FastTrack for Azure 프로그램을 통해 아키텍처 설계를 지원합니다.
- **GCP** — Customer Engineer(CE)가 아키텍처 설계를 지원하며, 파트너를 통한 컨설팅도 가능합니다.

## 참고하기

### AWS

- [Well-Architected Framework](https://aws.amazon.com/ko/architecture/well-architected/)
- [Well-Architected Tool](https://aws.amazon.com/ko/well-architected-tool/)
- [Well-Architected Labs](https://www.wellarchitectedlabs.com/)
- [Cloud Adoption Framework](https://aws.amazon.com/ko/cloud-adoption-framework/)

### Azure

- [Well-Architected Framework](https://learn.microsoft.com/ko-kr/azure/well-architected/)
- [Well-Architected Review](https://learn.microsoft.com/ko-kr/assessments/azure-architecture-review/)
- [Cloud Adoption Framework](https://learn.microsoft.com/ko-kr/azure/cloud-adoption-framework/)

### GCP

- [Architecture Framework](https://cloud.google.com/architecture/framework)
- [Architecture Center](https://cloud.google.com/architecture)
- [Cloud 설정 체크리스트](https://cloud.google.com/docs/enterprise/setup-checklist)
