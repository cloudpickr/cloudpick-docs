---
title: "API Gateway"
description: "API Gateway의 역할, 인증 연동, 배포 전략을 벤더별로 비교합니다."
---

> 문서 기준: 2026년 8월

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
| Google Cloud | Firebase Auth / Identity Platform | 소셜 로그인, 멀티팩터 인증 |
| Google Cloud | Service Account + IAM | 서비스 간 인증 |
| OCI | OCI IAM / Identity Domains | OAuth 2.0, JWT 검증 |

### 추가 기능

| 기능 | AWS | Azure | Google Cloud | OCI |
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
| Azure | API Management (APIM) | 개발자 포털 내장. 멀티 클라우드/하이브리드 API 통합. AI Gateway 티어(Public Preview, 2026.06)로 AI 모델 및 MCP 서버 전용 게이트웨이 제공 |
| Google Cloud | Apigee | 엔터프라이즈 API 관리 플랫폼. 분석/수익화 기능 |
| Google Cloud | API Gateway | 경량. Cloud Functions/Cloud Run 연동에 적합 |
| OCI | OCI API Gateway | OCI Functions 연동. 인증, 속도 제한, 요청 변환 지원 |

## 핵심 차이점

**AWS API Gateway** — Lambda와의 통합이 가장 깊어, 서버리스 백엔드를 API로 노출하는 데 최적화되어 있습니다. 용도별로 3가지 타입(REST API / HTTP API / WebSocket API)이 분리되어 있으며, HTTP API는 REST API 대비 비용이 약 1/3 수준입니다. 대부분의 새 프로젝트는 HTTP API로 시작하고, 캐싱·WAF·Usage Plan이 필요한 경우에만 REST API를 선택합니다.

**Azure API Management** — 개발자 포털, API 버전 관리, 정책 엔진이 내장된 풀 기능 플랫폼입니다. 단일 서비스에서 REST, WebSocket, GraphQL을 모두 처리합니다. 온프레미스 API와 클라우드 API를 하나의 게이트웨이로 통합할 수 있습니다. 2026년 6월 AI Gateway 티어(Public Preview)가 추가되어 AI 모델과 MCP 서버에 특화된 게시·보안·거버넌스 기능을 제공합니다. v2 티어(Basic v2, Standard v2, Premium v2)가 모두 GA되어 유연한 가격/성능 선택이 가능합니다.

**Google Cloud Apigee** — API를 제품으로 관리하는 엔터프라이즈 플랫폼입니다. 단일 서비스에서 모든 프로토콜을 처리하며, API 사용량 분석, 수익화(monetization), 파트너 관리 기능이 강점입니다. Gemini Code Assist 통합으로 자연어 기반 API 스펙 생성이 GA되었으며, API Hub를 통한 에이전트 등록·평가와 Git 기반 동기화를 지원합니다.

**OCI API Gateway** — OCI Functions와 네이티브 연동되며, 단일 서비스에서 인증(JWT 검증), 속도 제한, 요청 변환을 정책 기반으로 설정할 수 있습니다.

## API 배포 단계와 버전 관리

API는 프로덕션에 배포되면 변경이 어렵기 때문에, 개발→스테이징→프로덕션의 단계적 배포와 버전 관리가 중요합니다.

| 기능 | AWS API Gateway | Azure APIM | Google Cloud Apigee | OCI API Gateway |
| --- | --- | --- | --- | --- |
| **Stage/Environment** | Stages (dev, staging, prod) | Environments | Environments (test, prod) | Deployments |
| **Canary 배포** | Canary Deployment (가중치 기반) | Revision + Release | Revision + TargetServer | Route Rule (가중치) |
| **버전 관리** | API Version (v1, v2 별도 엔드포인트) | API Revision + Version | API Revision + Version | Spec Version |
| **롤백** | 이전 Deployment로 전환 | Revision 전환 | Revision 전환 | 이전 Deployment로 전환 |

## 점진적 배포 전략

:::note
API를 외부에 공개한 뒤에는 **하위 호환성 유지**가 핵심입니다. 기존 소비자가 있는 엔드포인트는 삭제하거나 응답 형식을 바꾸지 말고, 새 버전(`/v2`)을 추가하는 방식으로 관리하세요.
:::

| 전략 | 설명 | 벤더별 구현 |
| --- | --- | --- |
| **Canary** | 새 버전에 소량 트래픽(5–10%)을 보내고 모니터링 후 확대 | AWS: API Gateway Canary Deployment (Stage 가중치), Azure APIM: Revision + Traffic Split, Google Cloud Apigee: TargetServer 가중치 |
| **Blue/Green** | 두 환경을 동시 운영 후 트래픽 전환. 롤백 즉시 가능 | AWS: Stage 전환, Azure APIM: Revision 전환, Google Cloud: Revision 전환 |
| **버전 분리** | `/v1`, `/v2` 별도 엔드포인트로 공존 | 모든 벤더 지원. 기존 소비자 영향 없이 새 버전 추가 |

:::caution
API Gateway 자체의 Canary 기능은 "게이트웨이 설정 변경"에 대한 Canary입니다. 백엔드 코드 배포의 Canary는 별도로 Lambda Alias 가중치, 로드밸런서 Target Group 가중치, 또는 서비스 메시를 사용해야 합니다.
:::

## OpenAPI(Swagger) 연동

온프레미스에서 Swagger로 API 스펙을 정의하던 팀은 클라우드에서도 동일한 워크플로우를 유지할 수 있습니다.

- **Import**: OpenAPI 스펙으로 API Gateway를 자동 생성 (AWS, Azure APIM, Apigee 모두 지원)
- **Export**: API Gateway에서 OpenAPI 스펙을 추출하여 문서화
- **IaC 연동**: CloudFormation/Terraform에서 OpenAPI 스펙을 인라인으로 정의하여 API 구성을 코드로 관리
- **개발자 포털**: Azure APIM, Apigee는 OpenAPI 스펙 기반으로 인터랙티브 API 문서를 자동 생성

## API 테스트 도구

| 도구 | 역할 | API Gateway와의 관계 |
| --- | --- | --- |
| Postman | API 수동 테스트, 컬렉션 관리, 환경 변수 | Stage별 URL을 환경으로 관리, 인증 토큰 자동 갱신 |
| Swagger UI | OpenAPI 스펙 기반 인터랙티브 문서 | API Gateway에서 export한 스펙으로 자동 생성 |
| 벤더 콘솔 테스트 | AWS 콘솔 Test 탭, APIM Test 탭 | 배포 전 빠른 검증 |
| curl / httpie | CLI 기반 빠른 테스트 | CI/CD 파이프라인에서 스모크 테스트 |

클라우드 API는 인증 흐름(OAuth, API Key, IAM Sig v4)이 복잡하고, 환경(dev/staging/prod)별 전환이 빈번하므로 Postman 같은 도구로 환경 변수와 인증을 체계적으로 관리하는 것이 효율적입니다.

## 자주 하는 실수

- **REST API와 HTTP API를 구분하지 않고 REST API로 시작** — AWS에서 HTTP API가 비용 1/3이고 대부분의 요구를 충족합니다. 캐싱·WAF·Usage Plan이 필요한 경우에만 REST API를 선택하세요.
- **API 버전 관리 없이 기존 응답 형식을 변경** — 기존 소비자(클라이언트)가 즉시 깨집니다. 새 버전(`/v2`)을 추가하고 기존 버전을 유지하세요.
- **API Gateway의 Canary를 백엔드 코드 배포 Canary로 착각** — API Gateway Canary는 게이트웨이 설정 변경에 대한 것입니다. 백엔드 코드 배포는 Lambda Alias 가중치나 LB Target Group으로 별도 구성해야 합니다.

## 체크리스트

- [ ] 인증/인가(API Key, JWT, IAM)가 모든 엔드포인트에 적용되어 있는가?
- [ ] 속도 제한(Throttling)이 설정되어 백엔드 과부하를 방지하고 있는가?
- [ ] OpenAPI 스펙이 IaC와 동기화되어 API 구성이 코드로 관리되고 있는가?

## 관련 문서

- [로드밸런서](../../networking/load-balancer/) — L4/L7 트래픽 분배와 API 진입점 역할 분담
- [서버리스](../../compute/serverless/) — API 백엔드로 함수·컨테이너 연결
- [메시지 큐와 이벤트 스트리밍](../../database/messaging/) — 비동기 처리로의 오프로드
- [제로 트러스트](../../security/zero-trust/) — API 접근 통제와 ID 기반 검증
- [시크릿 관리](../../security/secrets/) — API 키·토큰 수명주기

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

### Google Cloud

- [Apigee 문서](https://cloud.google.com/apigee/docs)
- [API Gateway 문서](https://cloud.google.com/api-gateway/docs)
- [Firebase Authentication 문서](https://firebase.google.com/docs/auth)
- [Identity Platform 문서](https://cloud.google.com/identity-platform/docs)

### OCI

- [OCI API Gateway 문서](https://docs.oracle.com/en-us/iaas/Content/APIGateway/home.htm)
