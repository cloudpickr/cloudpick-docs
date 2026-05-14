---
description: 하이브리드 클라우드, 엣지 컴퓨팅, 멀티클라우드 아키텍처 패턴을 벤더별로 비교합니다.
---

# 하이브리드/엣지 컴퓨팅

> 문서 기준: 2026년 5월

## 개요

모든 워크로드가 퍼블릭 클라우드에 적합한 것은 아닙니다. 데이터 주권, 초저지연, 기존 투자 보호 등의 이유로 **온프레미스/엣지에 클라우드 인프라를 확장**하는 수요가 있습니다.

## 벤더별 하이브리드/엣지 솔루션

| 벤더 | 온프레미스 확장 | 엣지 | 멀티클라우드 관리 |
| --- | --- | --- | --- |
| AWS | [Outposts](https://aws.amazon.com/outposts/) (랙/서버) | [Local Zones](https://aws.amazon.com/about-aws/global-infrastructure/localzones/), [Wavelength](https://aws.amazon.com/wavelength/) | EKS Anywhere, ECS Anywhere |
| Azure | [Azure Stack HCI](https://learn.microsoft.com/azure/azure-stack/hci/), [Azure Local](https://learn.microsoft.com/azure/azure-local/) | Azure Edge Zones | [Azure Arc](https://azure.microsoft.com/products/azure-arc/) |
| GCP | [Google Distributed Cloud](https://cloud.google.com/distributed-cloud) (Connected/Edge/Air-gapped) | GDC Edge | [GKE Enterprise](https://cloud.google.com/kubernetes-engine/enterprise/docs) |
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
| **Best-of-Breed** | 서비스 영역별 최적 벤더 선택 | AI(GCP) + 엔터프라이즈 앱(Azure) + DB(OCI) |
| **Cloud-bursting** | 평상시 온프레미스, 피크 시 퍼블릭 확장 | 온프레미스 K8s + EKS/AKS/GKE 버스트 |
| **DR/Failover** | 주 벤더 장애 시 보조 벤더로 전환 | AWS(주) + Azure(DR) |

{% hint style="info" %}
멀티클라우드 패턴은 복잡도를 추가합니다. [멀티클라우드 이해하기](../about-cloud/why-multicloud.md)에서 도입 동기와 트레이드오프를 먼저 검토하세요.
{% endhint %}

## 참고하기

- [AWS Outposts 문서](https://docs.aws.amazon.com/outposts/)
- [Azure Arc 문서](https://learn.microsoft.com/azure/azure-arc/)
- [Google Distributed Cloud 문서](https://cloud.google.com/distributed-cloud/hosted/docs)
- [OCI Dedicated Region](https://docs.oracle.com/en-us/iaas/Content/dedicated-region/home.htm)
- [OCI Alloy](https://www.oracle.com/cloud/alloy/)
- [CNCF Multi-Cloud Patterns](https://www.cncf.io/blog/2023/03/29/multi-cloud-is-real/)
