---
description: 플랫폼 엔지니어링과 IDP(Internal Developer Platform)의 개념, 도구, 멀티클라우드 표준화를 설명합니다.
---

# 플랫폼 엔지니어링

> 문서 기준: 2026년 5월

## 개요

[DevOps](getting-started.md)가 "개발과 운영의 협업"이라면, **플랫폼 엔지니어링**은 "개발자가 인프라를 의식하지 않고 셀프서비스로 배포할 수 있는 플랫폼을 만드는 것"입니다.

개발자가 Jira 티켓을 열어 인프라팀에 요청하는 대신, 플랫폼이 제공하는 Golden Path를 따라 스스로 환경을 프로비저닝합니다.

## IDP (Internal Developer Platform)

| 컴포넌트 | 역할 | 주요 도구 |
| --- | --- | --- |
| **개발자 포털** | 서비스 카탈로그, 소유자 추적, 온보딩 | Backstage (CNCF Incubating), Port, Cortex |
| **인프라 셀프서비스** | PR로 환경 요청 → 자동 프로비저닝 | Crossplane, Terraform + Atlantis, Pulumi Operator |
| **Golden Path** | 권장 아키텍처 템플릿으로 빠른 시작 | Backstage Software Templates, Cookiecutter |
| **CI/CD 파이프라인 (공통)** | 표준화된 빌드/배포 파이프라인 템플릿 | Argo CD, Flux, Tekton, GitHub Actions reusable workflows |
| **시크릿 관리** | 벤더 시크릿을 K8s/앱에 주입 | External Secrets Operator, HashiCorp Vault |
| **관측가능성 스택** | 메트릭, 로그, 트레이스 통합 수집 | OpenTelemetry, Prometheus, Grafana, Loki |
| **정책 엔진 (가드레일)** | 보안/비용/규정 준수 자동 강제 | OPA/Gatekeeper, Kyverno, Checkov, tfsec |
| **비용 가시성** | 팀/서비스별 비용 할당, 알림 | OpenCost, Kubecost, Infracost |
| **환경 관리** | 임시 환경(Preview Env) 생성/삭제 | Argo CD ApplicationSet, vCluster |
| **내부 모듈 레지스트리** | 검증된 Terraform 모듈, Helm 차트 | Terraform Registry (private), Harbor |

### 오픈소스 생태계 맵

**포털 & 카탈로그:**
- Backstage (Spotify, CNCF Incubating) — 가장 넓은 생태계, 플러그인 풍부
- Port — SaaS, 코드 불필요
- Cortex — SaaS, 스코어카드 강점

**GitOps & 배포:**
- Argo CD — K8s 배포 표준, 멀티 클러스터
- Flux — 경량, CNCF Graduated
- Tekton — K8s 네이티브 CI/CD 파이프라인

**인프라 추상화:**
- Crossplane — K8s CRD로 클라우드 리소스 관리, 멀티클라우드
- Terraform + Atlantis — PR 기반 plan/apply 자동화

**정책 & 거버넌스:**
- OPA/Gatekeeper — K8s Admission Control
- Kyverno — YAML 기반 정책 (OPA보다 진입장벽 낮음)

**관측가능성:**
- OpenTelemetry — 벤더 중립 계측 표준 (CNCF Graduated)
- Prometheus + Grafana — 메트릭 수집/시각화 사실상 표준

**시크릿:**
- HashiCorp Vault — 가장 성숙, 멀티클라우드
- External Secrets Operator — K8s에서 벤더 시크릿 매니저 연동

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

## 자주 하는 실수

- **개발자 피드백 없이 플랫폼을 구축** — 아무도 사용하지 않는 내부 도구가 됩니다. 초기부터 개발자를 사용자로 참여시키고 피드백 루프를 만드세요.
- **Golden Path를 강제하여 모든 예외를 차단** — 유연성이 없으면 개발자가 우회합니다. 가드레일(금지 사항)과 Golden Path(권장 경로)를 구분하세요.
- **플랫폼 팀이 모든 인프라 요청을 직접 처리** — 티켓 큐가 병목이 됩니다. 셀프서비스 자동화가 플랫폼 엔지니어링의 핵심입니다.

## 체크리스트

- [ ] 개발자가 인프라 팀 티켓 없이 환경을 셀프서비스로 생성할 수 있는가?
- [ ] 플랫폼 자체의 SLO(가용성, 배포 파이프라인 성공률)가 정의되어 있는가?
- [ ] 정기적인 개발자 만족도 조사와 피드백 반영 프로세스가 있는가?

## 참고하기

### 표준 및 커뮤니티

- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
- [Backstage 문서](https://backstage.io/docs/)
- [Crossplane 문서](https://docs.crossplane.io/)
- [Humanitec Platform Orchestrator](https://humanitec.com/)
- [Team Topologies — Platform Teams](https://teamtopologies.com/)
