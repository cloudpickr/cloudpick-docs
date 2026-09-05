---
title: "하이브리드/엣지 컴퓨팅"
description: "하이브리드 클라우드, 엣지 컴퓨팅, 멀티클라우드 아키텍처 패턴을 벤더별로 비교합니다."
---

> 문서 기준: 2026년 8월

## 개요

모든 워크로드가 퍼블릭 클라우드에 적합한 것은 아닙니다. 데이터 주권, 초저지연, 기존 투자 보호 등의 이유로 **온프레미스/엣지에 클라우드 인프라를 확장**하는 수요가 있습니다.

## 벤더별 하이브리드/엣지 솔루션

| 벤더 | 온프레미스 확장 | 엣지 | 멀티클라우드 관리 |
| --- | --- | --- | --- |
| AWS | [Outposts](https://aws.amazon.com/outposts/) (랙/서버) | [Local Zones](https://aws.amazon.com/about-aws/global-infrastructure/localzones/), [Wavelength](https://aws.amazon.com/wavelength/) | EKS Anywhere, ECS Anywhere |
| Azure | [Azure Stack HCI](https://learn.microsoft.com/azure/azure-local/), [Azure Local](https://learn.microsoft.com/azure/azure-local/) | Azure Edge Zones | [Azure Arc](https://azure.microsoft.com/products/azure-arc/) |
| Google Cloud | [Google Distributed Cloud](https://cloud.google.com/distributed-cloud) (Connected/Edge/Air-gapped) | GDC Edge | [GKE Enterprise](https://cloud.google.com/kubernetes-engine/enterprise/docs) |
| OCI | [Dedicated Region](https://www.oracle.com/cloud/cloud-at-customer/dedicated-region/), [Compute Cloud@Customer](https://www.oracle.com/cloud/cloud-at-customer/) | — | [OCI Multicloud](https://docs.oracle.com/en/solutions/oci-best-practices/deploy-multicloud-oci-oracle-database-services1.html) |

## 사용 사례

| 사례 | 요구사항 | 적합한 솔루션 |
| --- | --- | --- |
| **데이터 주권** | 데이터가 특정 국가/시설 밖으로 나가면 안 됨 | Dedicated Region, Azure Stack, GDC Air-gapped |
| **초저지연** | 공장 자동화, 실시간 게임, AR/VR | Local Zones, Wavelength, Edge Zones |
| **기존 투자 보호** | 온프레미스 장비 수명 남음 + 클라우드 서비스 사용 | Arc, GKE Enterprise, EKS Anywhere |
| **규제 (망분리)** | 인터넷 연결 불가 환경 | GDC Air-gapped, Dedicated Region |

## 멀티클라우드 아키텍처 패턴

| 패턴 | 설명 | 예시 |
| --- | --- | --- |
| **Split-stack** | 계층별로 다른 벤더 사용 | 프런트엔드(AWS CloudFront) + 백엔드/DB(OCI) |
| **Data Gravity** | 대용량 데이터는 한 곳에, 분석/AI는 여러 벤더에서 접근 | 데이터레이크(GCS) + ML(Vertex AI) + 서빙(AWS) |
| **Best-of-Breed** | 서비스 영역별 최적 벤더 선택 | AI(Google Cloud) + 엔터프라이즈 앱(Azure) + DB(OCI) |
| **Cloud-bursting** | 평상시 온프레미스, 피크 시 퍼블릭 확장 | 온프레미스 K8s + EKS/AKS/GKE 버스트 |
| **DR/Failover** | 주 벤더 장애 시 보조 벤더로 전환 | AWS(주) + Azure(DR) |

:::note
멀티클라우드 패턴은 복잡도를 추가합니다. [멀티클라우드 이해하기](../../about-cloud/why-multicloud/)에서 도입 동기와 트레이드오프를 먼저 검토하세요.
:::

## 자주 하는 실수

- **하이브리드 아키텍처에서 네트워크 지연을 과소평가** — 온프레미스와 클라우드 간 왕복 지연(수십 ms)을 고려하지 않고 동기 호출을 설계하면 성능이 급격히 저하됩니다.
- **엣지 장비의 운영 부담을 간과** — 엣지에 배포하면 물리적 접근이 어려운 환경에서 패치, 장애 복구, 모니터링을 원격으로 해야 합니다. 운영 자동화 없이 도입하면 관리 비용이 급증합니다.
- **멀티클라우드를 기본값으로 선택** — 명확한 비즈니스 요구(규제, DR, 벤더 종속 회피) 없이 멀티클라우드를 도입하면 복잡도와 비용만 증가합니다.

## 체크리스트

- [ ] 온프레미스↔클라우드 간 네트워크 대역폭과 지연을 측정했는가
- [ ] 엣지/온프레미스 장비의 원격 관리·모니터링·패치 자동화 방안이 있는가
- [ ] 하이브리드/멀티클라우드 도입의 비즈니스 근거(규제, DR, 비용)를 문서화했는가

## 참고하기

### AWS

- [AWS Outposts 문서](https://docs.aws.amazon.com/outposts/)

### Azure

- [Azure Arc 문서](https://learn.microsoft.com/azure/azure-arc/)

### Google Cloud

- [Google Distributed Cloud 문서](https://cloud.google.com/distributed-cloud)

### OCI

- [OCI Dedicated Region](https://www.oracle.com/cloud/cloud-at-customer/dedicated-region/)
- [OCI Alloy](https://www.oracle.com/cloud/alloy/)

### 표준 및 커뮤니티

- [CNCF Multi-Cloud Patterns](https://www.cncf.io/reports/cncf-annual-survey-2023/)
