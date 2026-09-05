---
title: "서비스 메시"
description: "서비스 메시의 개념, 사이드카 vs 사이드카리스 모델, 벤더별 관리형 서비스를 비교합니다."
---

> 문서 기준: 2026년 8월

## 개요

[컨테이너 서비스](../../compute/containers/)로 마이크로서비스를 운영하면, 서비스 간 통신이 복잡해집니다. **서비스 메시** (Service Mesh)는 이 통신을 인프라 계층에서 관리하여 애플리케이션 코드 변경 없이 보안, 관찰가능성, 트래픽 제어를 제공합니다.

### 서비스 메시가 해결하는 문제

| 문제 | 서비스 메시의 해결 |
| --- | --- |
| 서비스 간 암호화 (mTLS) | 자동 인증서 발급/교체, 모든 통신 암호화 |
| 트래픽 라우팅 | Canary 배포, A/B 테스트, 트래픽 분할 |
| 서킷 브레이커 | 장애 서비스 자동 격리, 재시도/타임아웃 |
| 관찰가능성 | 서비스 간 지연/에러율 자동 수집 (코드 변경 없이) |
| 접근 제어 | 서비스 간 통신 정책 (어떤 서비스가 어떤 서비스를 호출 가능한지) |

## 사이드카 vs 사이드카리스

| 모델 | 방식 | 장점 | 단점 |
| --- | --- | --- | --- |
| **사이드카** (Sidecar) | 각 Pod에 프록시 컨테이너(Envoy 등) 주입 | 성숙한 생태계, 기능 풍부 | 리소스 오버헤드 (메모리/CPU), 레이턴시 추가 |
| **사이드카리스** (Sidecarless) | 노드 레벨 또는 커널 레벨에서 처리 | 리소스 절약, 레이턴시 최소 | 아직 초기 단계, 기능 제한적 |

대표 구현:
- 사이드카: Istio (Envoy), Linkerd (linkerd2-proxy)
- 사이드카리스: Istio Ambient Mesh (ztunnel), Cilium Service Mesh (eBPF)

## 주요 솔루션 비교

| 솔루션 | 프록시 | 특징 |
| --- | --- | --- |
| [Istio](https://istio.io/) | Envoy | 가장 기능 풍부. Ambient Mesh로 사이드카리스 지원. 복잡도 높음 |
| [Linkerd](https://linkerd.io/) | linkerd2-proxy (Rust) | 경량, 단순. 리소스 오버헤드 최소. 기능은 Istio 대비 제한적 |
| [Consul Connect](https://www.consul.io/docs/connect) | Envoy | HashiCorp 생태계 통합. 멀티 플랫폼 (K8s + VM) |

## 벤더 관리형 서비스

| 벤더 | 서비스 | 기반 | 특징 |
| --- | --- | --- | --- |
| AWS | [App Mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html) (유지보수 모드) / ECS Service Connect | Envoy | App Mesh는 신규 도입 비권장. ECS Service Connect 또는 VPC Lattice 권장 |
| AWS | [VPC Lattice](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html) | AWS 네이티브 | 서비스 간 연결을 VPC 수준에서 관리. 사이드카 불필요 |
| Azure | [Istio add-on for AKS](https://learn.microsoft.com/azure/aks/istio-about) | Istio | AKS 네이티브 통합. 컨트롤 플레인 관리형 |
| Google Cloud | [Cloud Service Mesh](https://cloud.google.com/service-mesh/docs) | Istio 기반 | GKE 통합. 관리형 컨트롤 플레인 + 데이터 플레인 |
| OCI | 자체 관리형 없음 | — | OKE에서 Istio/Linkerd 직접 설치 |

## 언제 도입해야 하는가

| 기준 | 도입 권장 | 도입 불필요 |
| --- | --- | --- |
| 서비스 수 | 10개 이상, 팀 간 경계 존재 | 모놀리스 또는 서비스 3–5개 |
| 보안 요구 | 서비스 간 mTLS 필수 (규제/감사) | 내부 통신 암호화 불필요 |
| 트래픽 제어 | Canary/A-B 배포, 세밀한 라우팅 필요 | 단순 롤링 배포로 충분 |
| 관찰가능성 | 서비스 간 지연/에러 추적 필요 | APM으로 충분 |

:::note
**서비스 메시는 복잡도를 추가합니다.** 서비스 수가 적거나 팀이 작다면, 서비스 메시 없이 네이티브 기능(Security Group, IAM, ALB 라우팅)으로 충분할 수 있습니다. "필요할 때" 도입하세요.
:::

## 자주 하는 실수

- **서비스 수가 적은데 서비스 메시를 도입** — 서비스 3–5개 규모에서는 복잡도만 추가됩니다. 네이티브 기능(Security Group, IAM, ALB 라우팅)으로 충분한지 먼저 검토하세요.
- **사이드카 리소스 오버헤드를 무시** — Envoy 프록시가 Pod마다 추가되면 메모리/CPU 사용량이 상당합니다. 리소스 요청/제한을 설정하지 않으면 노드 자원이 부족해집니다.
- **mTLS 도입 후 디버깅 어려움을 대비하지 않음** — 모든 통신이 암호화되면 기존 패킷 캡처 도구가 동작하지 않습니다. 메시 레벨 로깅과 분산 추적을 함께 구성하세요.

## 체크리스트

- [ ] 서비스 메시 도입이 필요한 명확한 요구사항(mTLS, 트래픽 분할, 관찰가능성)이 있는가
- [ ] 사이드카 프록시의 리소스 요청/제한을 설정하고 노드 용량을 확인했는가
- [ ] 메시 컨트롤 플레인 장애 시 데이터 플레인(기존 연결)이 유지되는지 확인했는가

## 참고하기

### AWS

- [AWS VPC Lattice 문서](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html)

### Azure

- [Azure AKS Istio add-on](https://learn.microsoft.com/azure/aks/istio-about)

### Google Cloud

- [Google Cloud Cloud Service Mesh](https://cloud.google.com/service-mesh/docs)

### 표준 및 커뮤니티

- [Istio 문서](https://istio.io/latest/docs/)
- [Linkerd 문서](https://linkerd.io/2/overview/)
- [CNCF Service Mesh Landscape](https://landscape.cncf.io/card-mode?category=service-mesh)
