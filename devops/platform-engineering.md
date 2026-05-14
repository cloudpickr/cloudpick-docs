---
description: 플랫폼 엔지니어링과 IDP(Internal Developer Platform)의 개념, 도구, 멀티클라우드 표준화를 설명합니다.
---

# 플랫폼 엔지니어링

> 문서 기준: 2026년 5월

## 개요

[DevOps](what-is-devops.md)가 "개발과 운영의 협업"이라면, **플랫폼 엔지니어링**은 "개발자가 인프라를 의식하지 않고 셀프서비스로 배포할 수 있는 플랫폼을 만드는 것"입니다.

개발자가 Jira 티켓을 열어 인프라팀에 요청하는 대신, 플랫폼이 제공하는 Golden Path를 따라 스스로 환경을 프로비저닝합니다.

## IDP (Internal Developer Platform)

| 구성 요소 | 역할 | 도구 예시 |
| --- | --- | --- |
| **개발자 포털** | 서비스 카탈로그, 문서, API 목록 | [Backstage](https://backstage.io/), [Port](https://www.getport.io/), [Humanitec](https://humanitec.com/) |
| **셀프서비스 인프라** | 개발자가 직접 환경 생성/삭제 | Terraform 모듈 + GitOps, Crossplane |
| **Golden Path** | 권장 아키텍처 템플릿 | Backstage Software Templates, Cookiecutter |
| **가드레일** | 보안/비용/규정 준수 자동 강제 | OPA, Azure Policy, AWS SCP |
| **관측가능성** | 서비스 상태 대시보드 | Grafana, Backstage TechDocs |

## 멀티클라우드 표준화

플랫폼 엔지니어링의 핵심 가치 중 하나는 **벤더 차이를 추상화**하는 것입니다.

| 추상화 계층 | 방법 | 도구 |
| --- | --- | --- |
| **인프라 프로비저닝** | 벤더 중립 IaC | [Crossplane](https://www.crossplane.io/) (K8s 네이티브), Terraform 모듈 |
| **배포** | 통합 GitOps | Argo CD (멀티 클러스터) |
| **시크릿** | 통합 시크릿 관리 | External Secrets Operator |
| **관측** | 통합 메트릭/로그 | OpenTelemetry + Grafana |

## Platform as a Product

플랫폼 팀은 내부 개발자를 "고객"으로 보고, 플랫폼을 "제품"으로 운영합니다.

- **사용자 피드백** — 정기적으로 개발자 만족도 조사
- **SLO** — 플랫폼 자체의 가용성/응답 시간 목표 설정
- **로드맵** — 기능 우선순위를 사용자 요구 기반으로 결정
- **문서화** — 셀프서비스 가이드, API 문서, 트러블슈팅 가이드

## 참고하기

- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
- [Backstage 문서](https://backstage.io/docs/)
- [Crossplane 문서](https://docs.crossplane.io/)
- [Humanitec Platform Orchestrator](https://humanitec.com/platform-orchestrator)
- [Team Topologies — Platform Teams](https://teamtopologies.com/)
