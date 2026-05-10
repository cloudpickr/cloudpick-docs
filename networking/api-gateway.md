# API Gateway

> 문서 기준: 2026년 5월

## 개요

백엔드 서비스를 외부에 API로 노출할 때, 인증, 속도 제한, 요청 변환, 모니터링 등을 각 서비스마다 구현하면 중복이 발생합니다. **API Gateway**는 이러한 공통 관심사를 한 곳에서 처리하는 진입점(Front Door) 역할을 합니다.

온프레미스에서 리버스 프록시(Nginx, HAProxy)에 인증/라우팅 로직을 넣던 것과 비슷하지만, 클라우드 API Gateway는 관리형으로 스케일링, 모니터링, 개발자 포털까지 통합 제공합니다.

### 주요 기능

- **인증/인가** — API 키, OAuth, JWT, IAM 기반 접근 제어
- **속도 제한** (Throttling) — 초당 요청 수 제한으로 백엔드 보호
- **요청/응답 변환** — 헤더 추가, 본문 매핑, 프로토콜 변환
- **캐싱** — 반복 요청에 대한 응답 캐싱
- **모니터링** — 요청 수, 지연 시간, 에러율 자동 수집
- **개발자 포털** — API 문서 자동 생성, 키 발급

### 인증/인가 연동

API Gateway 자체는 인증 로직을 처리하지 않고, 외부 인증 서비스와 연동합니다.

| 벤더 | 인증 서비스 | 비고 |
| --- | --- | --- |
| AWS | Cognito | 사용자 풀 + 소셜 로그인. API Gateway와 네이티브 연동 |
| AWS | Lambda Authorizer | 커스텀 인증 로직을 Lambda로 구현 |
| Azure | Entra ID (구 Azure AD) | OAuth 2.0 / OpenID Connect |
| Azure | APIM Policy (validate-jwt) | JWT 토큰 검증을 정책으로 설정 |
| GCP | Firebase Auth / Identity Platform | 소셜 로그인, 멀티팩터 인증 |
| GCP | Service Account + IAM | 서비스 간 인증 |
| OCI | OCI IAM / Identity Domains | OAuth 2.0, JWT 검증 |

### 추가 기능

| 기능 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **사용량 계획/쿼터** | Usage Plans + API Keys | Subscription + Quota Policy | Apigee Rate Limiting | Rate Limiting Policy |
| **요청 검증** | Request Validator (모델 스키마) | APIM Policy (validate-content) | Apigee OAS Validation | Request Validation Policy |
| **커스텀 도메인** | Custom Domain + ACM 인증서 | Custom Domain + Managed Certificate | Custom Domain + SSL | Custom Domain + SSL 인증서 |
| **WebSocket** | WebSocket API | — (SignalR 별도) | — (Firebase Realtime 별도) | — |
| **GraphQL** | AppSync | — (3rd party) | — (3rd party) | — |

## 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | API Gateway (REST/HTTP/WebSocket) | Lambda와 네이티브 통합. 서버리스 API 구성에 최적 |
| AWS | AppSync | GraphQL 전용. 실시간 구독 지원 |
| Azure | API Management (APIM) | 개발자 포털 내장. 멀티 클라우드/하이브리드 API 통합 |
| GCP | Apigee | 엔터프라이즈 API 관리 플랫폼. 분석/수익화 기능 |
| GCP | API Gateway | 경량. Cloud Functions/Cloud Run 연동에 적합 |
| OCI | OCI API Gateway | OCI Functions 연동. 인증, 속도 제한, 요청 변환 지원 |

## 핵심 차이점

**AWS API Gateway** — Lambda와의 통합이 가장 깊어, 서버리스 백엔드를 API로 노출하는 데 최적화되어 있습니다. HTTP API 타입은 비용이 REST API의 약 1/3 수준입니다.

**Azure API Management** — 개발자 포털, API 버전 관리, 정책 엔진이 내장된 풀 기능 플랫폼입니다. 온프레미스 API와 클라우드 API를 하나의 게이트웨이로 통합할 수 있습니다.

**GCP Apigee** — API를 제품으로 관리하는 엔터프라이즈 플랫폼입니다. API 사용량 분석, 수익화(monetization), 파트너 관리 기능이 강점입니다.

**OCI API Gateway** — OCI Functions와 네이티브 연동되며, 인증(JWT 검증), 속도 제한, 요청 변환을 정책 기반으로 설정할 수 있습니다.

## API 배포 단계와 버전 관리

API는 프로덕션에 배포되면 변경이 어렵기 때문에, 개발→스테이징→프로덕션의 단계적 배포와 버전 관리가 중요합니다.

| 기능 | AWS API Gateway | Azure APIM | GCP Apigee | OCI API Gateway |
| --- | --- | --- | --- | --- |
| **Stage/Environment** | Stages (dev, staging, prod) | Environments | Environments (test, prod) | Deployments |
| **Canary 배포** | Canary Deployment (가중치 기반) | Revision + Release | Revision + TargetServer | Route Rule (가중치) |
| **버전 관리** | API Version (v1, v2 별도 엔드포인트) | API Revision + Version | API Revision + Version | Spec Version |
| **롤백** | 이전 Deployment로 전환 | Revision 전환 | Revision 전환 | 이전 Deployment로 전환 |

### 점진적 배포 전략

- **Blue/Green** — 두 환경을 동시 운영 후 트래픽 전환. 롤백 즉시 가능
- **Canary** — 새 버전에 소량 트래픽(5~10%)을 보내고 모니터링 후 점진적 확대
- **A/B 테스트** — 사용자 세그먼트별로 다른 버전 노출

## 참고하기

### AWS

- [Amazon API Gateway 문서](https://docs.aws.amazon.com/ko_kr/apigateway/)
- [API Gateway 인증/인가](https://docs.aws.amazon.com/ko_kr/apigateway/latest/developerguide/apigateway-control-access-to-api.html)
- [Amazon Cognito 문서](https://docs.aws.amazon.com/ko_kr/cognito/)
- [AWS AppSync 문서](https://docs.aws.amazon.com/ko_kr/appsync/)

### Azure

- [Azure API Management 문서](https://learn.microsoft.com/ko-kr/azure/api-management/)
- [APIM 인증 정책](https://learn.microsoft.com/ko-kr/azure/api-management/authentication-authorization-overview)
- [Microsoft Entra ID 문서](https://learn.microsoft.com/ko-kr/entra/identity/)

### GCP

- [Apigee 문서](https://cloud.google.com/apigee/docs)
- [API Gateway 문서](https://cloud.google.com/api-gateway/docs)
- [Firebase Authentication 문서](https://firebase.google.com/docs/auth)
- [Identity Platform 문서](https://cloud.google.com/identity-platform/docs)

### OCI

- [OCI API Gateway 문서](https://docs.oracle.com/en-us/iaas/Content/APIGateway/home.htm)
