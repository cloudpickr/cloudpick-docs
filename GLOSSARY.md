---
description: 클라우드 문서에서 자주 등장하는 용어를 벤더 중립적으로 정리합니다.
---

# 용어집

> 문서 기준: 2026년 5월

클라우드 문서에서 자주 등장하는 용어를 벤더 중립적으로 정리합니다.

## 인프라 기본

| 용어 | 의미 |
| --- | --- |
| 온프레미스 | On-Premises. 클라우드가 아닌 자체 데이터센터 또는 사무실에서 직접 운영하는 인프라입니다. |
| Region | 지리적으로 분리된 데이터센터 클러스터입니다. 서울, 도쿄, 버지니아 같은 단위로 이해할 수 있습니다. |
| Availability Zone / Zone | 하나의 리전 안에서 독립적으로 장애가 격리되는 데이터센터 또는 데이터센터 그룹입니다. AZ라고 줄여 부릅니다. |
| CIDR | Classless Inter-Domain Routing. IP 주소 범위를 표기하는 방식입니다. 예: `10.0.0.0/16`은 10.0.0.0\~10.0.255.255 범위를 의미합니다. |
| Edge Location | 사용자와 가까운 위치에 배치된 소규모 인프라입니다. CDN, DNS, 엣지 보안에 주로 사용됩니다. |
| VPC / VNet / VCN | 클라우드 안에 만드는 논리적으로 격리된 가상 네트워크입니다. |
| Subnet | VPC 안에서 IP 대역을 더 작게 나눈 네트워크 영역입니다. |
| Load Balancer | 여러 서버로 트래픽을 분산하는 장치 또는 서비스입니다. |
| NAT Gateway | 프라이빗 리소스가 인터넷으로 나갈 수 있게 하되, 외부에서 직접 들어오는 접근은 막는 서비스입니다. |
| Landing Zone | 멀티 계정/구독/프로젝트 환경을 안전하고 일관되게 운영하기 위한 초기 기반 구조입니다. |

## 컴퓨팅

| 용어 | 의미 |
| --- | --- |
| Serverless | 서버 관리 부담을 줄이고 코드나 컨테이너 실행에 집중하게 해주는 실행 모델입니다. |
| Container | 애플리케이션과 실행 환경을 함께 패키징한 배포 단위입니다. |
| Kubernetes | 컨테이너를 배포, 확장, 복구하는 오케스트레이션 플랫폼입니다. |
| 불변 인프라 | Immutable Infrastructure. 실행 중인 서버를 수정하지 않고, 새 이미지로 교체하는 운영 방식입니다. |

## 스토리지

| 용어 | 의미 |
| --- | --- |
| Object Storage | 파일을 객체 단위로 저장하는 스토리지입니다. 이미지, 백업, 로그, 데이터레이크에 자주 사용됩니다. |
| Block Storage | VM에 디스크처럼 붙여 사용하는 스토리지입니다. |
| File Storage | 여러 서버가 같은 파일 시스템을 공유할 수 있게 해주는 스토리지입니다. |

## 보안

| 용어 | 의미 |
| --- | --- |
| IAM | Identity and Access Management. 누가 어떤 리소스에 무엇을 할 수 있는지 관리하는 체계입니다. |
| MFA | Multi-Factor Authentication. 비밀번호 외 추가 인증 수단을 요구하는 방식입니다. |
| Least Privilege | 최소 권한 원칙. 필요한 최소 권한만 부여하는 보안 원칙입니다. |
| JIT 접근 | Just-In-Time Access. 상시 권한 대신 필요 시 요청→승인→시간 제한 부여하는 접근 방식입니다. |
| Zero Trust | "절대 신뢰하지 말고, 항상 검증하라"는 보안 모델입니다. 네트워크 경계가 아닌 ID와 컨텍스트 기반으로 접근을 제어합니다. |
| 망분리 | Network Segregation. 업무망과 인터넷망을 분리하여 외부 위협의 내부 도달을 차단하는 보안 통제입니다. 물리적 분리와 논리적 분리(VPC 격리 등)로 구현합니다. |
| N2SF | 국가망보안체계. 기존 일률적 망분리를 C(기밀)/S(민감)/O(공개) 등급별 차등 보안으로 전환하는 프레임워크입니다. 2025년 NCSC에서 1.0 공개. |
| CSAP | 클라우드 보안 인증제. 공공기관에 클라우드를 제공하려는 CSP가 취득해야 하는 인증입니다. 상·중·하 3등급제로 운영됩니다. |
| SCP | Service Control Policy. AWS Organizations에서 계정별로 허용/차단할 API를 제한하는 예방적 가드레일입니다. Azure Policy, Google Cloud Organization Policy가 유사 역할을 합니다. |
| 가드레일 | Guardrail. 조직 정책을 자동으로 강제하여 위험한 설정이나 행위를 사전에 차단하는 예방적 통제입니다. |
| 마이크로세그멘테이션 | Microsegmentation. 네트워크를 세밀하게 분리하여 워크로드 간 통신을 최소 권한으로 제한하는 기법입니다. Zero Trust의 핵심 구현 수단입니다. |
| 워크로드 아이덴티티 | Workload Identity. 사람이 아닌 애플리케이션/서비스에 부여하는 ID입니다. 장기 자격 증명 없이 클라우드 리소스에 접근할 수 있게 합니다. |
| 서비스 계정 | Service Account. 사람이 아닌 애플리케이션이나 자동화 프로세스가 사용하는 계정입니다. |
| 조건부 접근 | Conditional Access. 사용자의 위치, 기기 상태, 시간 등 컨텍스트에 따라 접근을 허용/차단하는 정책입니다. |
| OIDC | OpenID Connect. OAuth 2.0 위에 구축된 인증 프로토콜입니다. 사용자 신원 확인과 SSO에 사용됩니다. |
| SAML | Security Assertion Markup Language. 엔터프라이즈 SSO에 사용되는 XML 기반 인증/인가 표준입니다. |
| 임시 자격 증명 | Temporary Credentials. 제한된 시간 동안만 유효한 인증 정보입니다. STS 토큰, 세션 토큰 등이 해당합니다. 동의어: 임시 토큰. |
| 장기 자격 증명 | Long-term Credentials. 만료 없이 유효한 인증 정보입니다. Access Key, API Key 등이 해당합니다. 보안상 임시 자격 증명 사용을 권장합니다. |
| CSPM | Cloud Security Posture Management. 클라우드 구성 오류를 지속적으로 탐지하는 보안 관리 체계입니다. |
| CWPP | Cloud Workload Protection Platform. VM, 컨테이너, 서버리스 등 워크로드의 런타임 보안을 보호하는 플랫폼입니다. |
| SIEM | Security Information and Event Management. 보안 이벤트를 수집·상관 분석하여 위협을 탐지하는 시스템입니다. |
| SOAR | Security Orchestration, Automation and Response. 보안 이벤트에 대한 자동 대응을 오케스트레이션하는 시스템입니다. |
| CIS Benchmark | Center for Internet Security에서 제공하는 보안 구성 기준선입니다. OS, 클라우드, DB 등 다양한 대상에 대한 표준을 제공합니다. |
| WAF | Web Application Firewall. 웹 애플리케이션을 SQL Injection, XSS 등 L7 공격으로부터 보호하는 방화벽입니다. |
| OWASP Top 10 | 웹 애플리케이션의 가장 흔한 10가지 보안 위협을 정리한 업계 표준 목록입니다. |
| CVE | Common Vulnerabilities and Exposures. 공개된 보안 취약점에 부여되는 고유 식별자입니다. |
| CVSS | Common Vulnerability Scoring System. 취약점의 심각도를 0\~10 점수로 평가하는 표준입니다. |
| SBOM | Software Bill of Materials. 소프트웨어에 포함된 모든 구성 요소(라이브러리, 패키지)의 목록입니다. |

## DevOps / DevSecOps

| 용어 | 의미 |
| --- | --- |
| IaC | Infrastructure as Code. 인프라를 코드로 정의하고 재현 가능하게 관리하는 방식입니다. |
| CI/CD | Continuous Integration / Continuous Delivery 또는 Deployment. 빌드, 테스트, 배포를 자동화하는 방식입니다. |
| Observability | 관찰가능성. 로그, 메트릭, 트레이스를 통해 시스템 상태를 이해하는 능력입니다. |
| DevSecOps | 보안을 개발(Dev)과 운영(Ops) 파이프라인에 처음부터 내장하는 접근 방식입니다. |
| GitOps | Git 저장소를 단일 진실 소스(Single Source of Truth)로 사용하여 인프라와 애플리케이션 배포를 자동화하는 운영 방식입니다. |
| 시프트-레프트 | Shift-Left. 보안 검증을 개발 초기 단계로 이동하여 문제를 빨리 발견하는 원칙입니다. |
| SAST | Static Application Security Testing. 소스 코드를 실행하지 않고 분석하여 보안 취약점을 찾는 기법입니다. |
| DAST | Dynamic Application Security Testing. 실행 중인 애플리케이션을 외부에서 공격하여 취약점을 찾는 기법입니다. |
| SCA | Software Composition Analysis. 오픈소스 의존성의 알려진 취약점(CVE)과 라이선스 위반을 탐지하는 기법입니다. |
| MLOps | ML 모델의 학습/배포/모니터링을 자동화·표준화하는 운영 체계입니다. DevOps의 ML 버전입니다. |

## 거버넌스 / FinOps

| 용어 | 의미 |
| --- | --- |
| CapEx | Capital Expenditure. 자본 지출. 서버·장비 구매처럼 초기에 큰 비용을 투자하는 방식입니다. |
| OpEx | Operational Expenditure. 운영 지출. 클라우드처럼 사용한 만큼 비용을 지불하는 방식입니다. |
| FinOps | 클라우드 비용을 엔지니어링, 재무, 비즈니스 팀이 함께 관리하는 운영 모델입니다. |
| 쇼백 | Showback. 부서/팀별 클라우드 사용 비용을 보여주기만 하는 방식입니다. 실제 예산에서 차감하지 않고 "우리 팀이 얼마 쓰고 있는지" 인식을 공유합니다. |
| 차지백 | Chargeback. 부서별 클라우드 사용 비용을 해당 팀의 실제 예산(P&L)에서 차감하는 방식입니다. 팀이 비용에 직접 책임을 집니다. |
| HA | High Availability. 고가용성. 단일 장애점을 제거하여 서비스 중단을 최소화하는 설계입니다. Multi-AZ 배치가 대표적입니다. |
| SLI | Service Level Indicator. 서비스 수준 지표. 가용률, 응답 시간 등 측정 가능한 지표입니다. |
| SLO | Service Level Objective. 서비스 수준 목표. SLI의 목표값입니다. 예: "월간 가용률 99.9%". |
| SLA | Service Level Agreement. 서비스 수준 계약. SLO를 외부 고객과 계약으로 약속한 것입니다. 위반 시 크레딧 보상 등이 따릅니다. |
| 에러 버짓 | Error Budget. SLO에서 허용하는 장애 시간입니다. 예: 99.9% SLO면 월 43분이 에러 버짓입니다. |
| RPO | Recovery Point Objective. 장애 시 허용 가능한 데이터 손실 시간입니다. |
| RTO | Recovery Time Objective. 장애 후 서비스를 복구해야 하는 목표 시간입니다. |
| DR | Disaster Recovery. 재해복구. 리전 장애나 대규모 장애에 대비한 복구 전략입니다. |

## AI / 머신러닝

| 용어 | 의미 |
| --- | --- |
| LLM | Large Language Model. 대량의 텍스트로 학습된 대형 언어 모델입니다. GPT, Claude, Gemini 등이 있습니다. |
| Foundation Model | 파운데이션 모델. 대규모 데이터로 사전 학습되어 다양한 작업에 범용적으로 쓰이는 AI 모델입니다. |
| RAG | Retrieval-Augmented Generation. 외부 지식 검색 결과를 LLM 답변 생성에 함께 사용하는 AI 아키텍처입니다. |
| Vector Store | 텍스트나 이미지의 의미를 벡터로 저장하고 유사도 검색을 제공하는 저장소입니다. |
| Embedding | 텍스트나 이미지를 의미 기반의 숫자 배열(벡터)로 변환한 것입니다. 유사도 검색에 사용됩니다. |
| ANN | Approximate Nearest Neighbor. 근사 최근접 이웃 탐색. 벡터 검색에서 속도를 위해 정확도를 약간 양보하는 알고리즘입니다. |
| Prompt | 모델에게 보내는 입력 메시지입니다. 질문, 지시, 맥락을 포함합니다. |
| Prompt Engineering | 모델이 더 좋은 답을 생성하도록 프롬프트를 설계하고 개선하는 기법입니다. |
| Token | 모델이 텍스트를 처리하는 단위입니다. 대략 단어 한 개가 1\~2 토큰이며, 대부분 API는 토큰 수로 과금합니다. |
| Fine-tuning | 사전 학습된 모델을 특정 데이터로 추가 학습하여 도메인에 맞게 조정하는 기법입니다. |
| Inference | 추론. 학습된 모델이 입력을 받아 출력을 생성하는 과정입니다. 학습보다 빠르고 저렴합니다. |
| Hallucination | 환각. LLM이 사실이 아닌 내용을 그럴듯하게 생성하는 현상입니다. RAG 등으로 완화합니다. |
| Agent | 에이전트. LLM이 도구를 호출하거나 여러 단계를 수행하여 작업을 자동화하는 구조입니다. |
