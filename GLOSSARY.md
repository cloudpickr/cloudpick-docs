---
description: 클라우드 문서에서 자주 등장하는 용어를 벤더 중립적으로 정리합니다.
---

# 용어집

> 문서 기준: 2026년 5월

클라우드 문서에서 자주 등장하는 용어를 벤더 중립적으로 정리합니다.

| 용어 | 의미 |
| --- | --- |
| Region | 지리적으로 분리된 데이터센터 클러스터입니다. 서울, 도쿄, 버지니아 같은 단위로 이해할 수 있습니다. |
| Availability Zone / Zone | 하나의 리전 안에서 독립적으로 장애가 격리되는 데이터센터 또는 데이터센터 그룹입니다. |
| Edge Location | 사용자와 가까운 위치에 배치된 소규모 인프라입니다. CDN, DNS, 엣지 보안에 주로 사용됩니다. |
| VPC / VNet / VCN | 클라우드 안에 만드는 논리적으로 격리된 가상 네트워크입니다. |
| Subnet | VPC 안에서 IP 대역을 더 작게 나눈 네트워크 영역입니다. |
| IAM | Identity and Access Management. 누가 어떤 리소스에 무엇을 할 수 있는지 관리하는 체계입니다. |
| MFA | Multi-Factor Authentication. 비밀번호 외 추가 인증 수단을 요구하는 방식입니다. |
| Least Privilege | 최소 권한 원칙. 필요한 최소 권한만 부여하는 보안 원칙입니다. |
| Load Balancer | 여러 서버로 트래픽을 분산하는 장치 또는 서비스입니다. |
| NAT Gateway | 프라이빗 리소스가 인터넷으로 나갈 수 있게 하되, 외부에서 직접 들어오는 접근은 막는 서비스입니다. |
| Object Storage | 파일을 객체 단위로 저장하는 스토리지입니다. 이미지, 백업, 로그, 데이터레이크에 자주 사용됩니다. |
| Block Storage | VM에 디스크처럼 붙여 사용하는 스토리지입니다. |
| File Storage | 여러 서버가 같은 파일 시스템을 공유할 수 있게 해주는 스토리지입니다. |
| Serverless | 서버 관리 부담을 줄이고 코드나 컨테이너 실행에 집중하게 해주는 실행 모델입니다. |
| Container | 애플리케이션과 실행 환경을 함께 패키징한 배포 단위입니다. |
| Kubernetes | 컨테이너를 배포, 확장, 복구하는 오케스트레이션 플랫폼입니다. |
| IaC | Infrastructure as Code. 인프라를 코드로 정의하고 재현 가능하게 관리하는 방식입니다. |
| CI/CD | Continuous Integration / Continuous Delivery 또는 Deployment. 빌드, 테스트, 배포를 자동화하는 방식입니다. |
| Observability | 로그, 메트릭, 트레이스를 통해 시스템 상태를 이해하는 능력입니다. |
| RPO | Recovery Point Objective. 장애 시 허용 가능한 데이터 손실 시간입니다. |
| RTO | Recovery Time Objective. 장애 후 서비스를 복구해야 하는 목표 시간입니다. |
| DR | Disaster Recovery. 재해복구. 리전 장애나 대규모 장애에 대비한 복구 전략입니다. |
| FinOps | 클라우드 비용을 엔지니어링, 재무, 비즈니스 팀이 함께 관리하는 운영 모델입니다. |
| Landing Zone | 멀티 계정/구독/프로젝트 환경을 안전하고 일관되게 운영하기 위한 초기 기반 구조입니다. |
| RAG | Retrieval-Augmented Generation. 외부 지식 검색 결과를 LLM 답변 생성에 함께 사용하는 AI 아키텍처입니다. |
| Vector Store | 텍스트나 이미지의 의미를 벡터로 저장하고 유사도 검색을 제공하는 저장소입니다. |
| LLM | Large Language Model. 대량의 텍스트로 학습된 대형 언어 모델입니다. GPT, Claude, Gemini 등이 있습니다. |
| Foundation Model | 파운데이션 모델. 대규모 데이터로 사전 학습되어 다양한 작업에 범용적으로 쓰이는 AI 모델입니다. |
| Prompt | 모델에게 보내는 입력 메시지입니다. 질문, 지시, 맥락을 포함합니다. |
| Prompt Engineering | 모델이 더 좋은 답을 생성하도록 프롬프트를 설계하고 개선하는 기법입니다. |
| Token | 모델이 텍스트를 처리하는 단위입니다. 대략 단어 한 개가 1\~2 토큰이며, 대부분 API는 토큰 수로 과금합니다. |
| Embedding | 텍스트나 이미지를 의미 기반의 숫자 배열(벡터)로 변환한 것입니다. 유사도 검색에 사용됩니다. |
| Fine-tuning | 사전 학습된 모델을 특정 데이터로 추가 학습하여 도메인에 맞게 조정하는 기법입니다. |
| Inference | 추론. 학습된 모델이 입력을 받아 출력을 생성하는 과정입니다. 학습보다 빠르고 저렴합니다. |
| Hallucination | 환각. LLM이 사실이 아닌 내용을 그럴듯하게 생성하는 현상입니다. RAG 등으로 완화합니다. |
| Agent | 에이전트. LLM이 도구를 호출하거나 여러 단계를 수행하여 작업을 자동화하는 구조입니다. |
| MLOps | ML 모델의 학습/배포/모니터링을 자동화·표준화하는 운영 체계입니다. DevOps의 ML 버전입니다. |
| ANN | Approximate Nearest Neighbor. 근사 최근접 이웃 탐색. 벡터 검색에서 속도를 위해 정확도를 약간 양보하는 알고리즘입니다. |
| HNSW | Hierarchical Navigable Small World. 그래프 기반 ANN 알고리즘입니다. |

{% hint style="info" %}
같은 개념이라도 벤더마다 이름이 다를 수 있습니다. 예를 들어 AWS는 VPC, Azure는 VNet, OCI는 VCN이라는 용어를 사용합니다.
{% endhint %}
