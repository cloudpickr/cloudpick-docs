---
description: 트랜짓 아키텍처 패턴, 이그레스 비용 상세 비교, DNS 통합 전략 등 멀티클라우드 네트워크 심화 내용입니다.
---

# 멀티클라우드 커넥티비티 (심화)

> 문서 기준: 2026년 5월

{% hint style="info" %}
연결 방식 개요와 CIDR 설계는 [멀티클라우드 네트워킹 개요](../networking/multicloud-networking.md)를 참고하세요.
{% endhint %}

## 트랜짓 아키텍처 패턴

### Hub-and-Spoke

중앙 허브를 두고 각 클라우드를 스포크로 연결하는 패턴입니다.

```mermaid
graph TD
    Hub[Hub VPC / Transit] --> AWS[AWS Spoke]
    Hub --> Azure[Azure Spoke]
    Hub --> Google Cloud[Google Cloud Spoke]
    Hub --> OCI[OCI Spoke]
```

- **허브 위치:** 가장 트래픽이 많은 벤더 또는 온프레미스
- **장점:** 보안 정책을 허브에서 중앙 관리, 라우팅 단순화
- **단점:** 허브가 병목/단일 장애점이 될 수 있음

### AWS Transit Gateway + 타 벤더 연결

| 구간 | 연결 방식 | 비고 |
| --- | --- | --- |
| AWS 내부 VPC 간 | Transit Gateway Attachment | 리전 내 ~$0.02/GB |
| AWS ↔ Azure | Site-to-Site VPN (TGW 연결) | BGP 경로 교환 |
| AWS ↔ Google Cloud | AWS Interconnect – multicloud | GA (2026.04) |
| AWS ↔ OCI | Oracle Interconnect for AWS | 2026년 내 출시 예정 |

## 이그레스 비용 비교

클라우드 간 데이터 이동의 가장 큰 비용 요소는 이그레스(아웃바운드) 요금입니다.

| 구간 | 단가 (서울 리전 기준) | 비고 |
| --- | --- | --- |
| AWS → 인터넷 | $0.126/GB (처음 10TB) | 이후 체감 |
| Azure → 인터넷 | $0.12/GB | 처음 5GB/월 무료 |
| Google Cloud → 인터넷 | $0.12/GB | 처음 200GB/월 무료 |
| OCI → 인터넷 | 10TB/월 무료, 이후 ~$0.0085/GB | 타사 대비 매우 저렴 |
| AWS → Direct Connect | ~$0.04/GB | 회선비 별도 |
| Azure → ExpressRoute | 포함 (Unlimited 플랜) | 회선비에 포함 |
| Google Cloud → Interconnect | ~$0.05/GB | 회선비 별도 |
| OCI → FastConnect | 10TB/월 무료에 포함 | 회선비 별도 |

> 위 수치는 문서 작성 시점 기준이며 변동될 수 있습니다. 최신 가격은 각 벤더 공식 가격표를 확인하세요.

### 비용 최적화 팁

- **데이터 지역성:** 자주 통신하는 워크로드는 같은 클라우드에 배치
- **전용 연결:** 월 1TB 이상 이동 시 VPN보다 전용 연결이 경제적
- **압축/캐싱:** 클라우드 경계를 넘는 데이터는 압축 후 전송
- **비동기 배치:** 실시간이 불필요한 데이터는 야간 배치로 이동

## DNS 통합 전략

멀티클라우드에서 서비스 디스커버리의 핵심은 DNS입니다. 각 벤더의 프라이빗 DNS가 분리되어 있으므로 통합 전략이 필요합니다.

### 각 벤더의 프라이빗 DNS

| 벤더 | 서비스 | 특징 |
| --- | --- | --- |
| AWS | Route 53 Private Hosted Zone | VPC 연결, 조건부 포워딩 |
| Azure | Azure Private DNS Zone | VNet 링크 |
| Google Cloud | Cloud DNS Private Zone | VPC 바인딩 |
| OCI | OCI DNS Private View | VCN 연결 |

### 통합 패턴: 조건부 포워딩

도메인 접미사 기반으로 각 클라우드의 프라이빗 DNS 엔드포인트로 포워딩합니다.

| 도메인 패턴 | 포워딩 대상 |
| --- | --- |
| `*.aws.internal` | Route 53 Inbound Endpoint |
| `*.azure.internal` | Azure DNS Private Resolver |
| `*.gcp.internal` | Cloud DNS Inbound Policy |
| `*.oci.internal` | OCI DNS Inbound Endpoint |
| `*.corp.internal` | 온프레미스 DNS |

**구현 방법:**
1. 각 클라우드에 인바운드 DNS 엔드포인트 생성
2. 조건부 포워딩 규칙 설정 (도메인 접미사 기반)
3. 온프레미스 DNS 서버 또는 허브 VPC의 DNS를 중앙 포워더로 사용

{% hint style="info" %}
**팁:** Route 53 Resolver의 아웃바운드 엔드포인트를 허브로 사용하면, AWS에서 Azure/Google Cloud의 프라이빗 레코드를 조회할 수 있습니다.
{% endhint %}

## 벤더 간 직접 연결 (Cross-Cloud Interconnect)

주요 CSP는 경쟁 관계이면서도, 고객의 멀티클라우드 수요에 대응하여 벤더 간 전용 네트워크를 제공합니다. 인터넷을 거치지 않고 프라이빗하게 클라우드를 연결할 수 있습니다.

| 서비스 | 연결 구간 | 상태 (2026년 4월 기준) |
| --- | --- | --- |
| **[AWS Interconnect – multicloud](https://aws.amazon.com/interconnect/multicloud/)** | AWS ↔ Google Cloud | GA (2026.04). Azure, OCI는 2026년 내 추가 예정 |
| **[Google Cross-Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/cross-cloud-overview)** | Google Cloud ↔ AWS/Azure/OCI | GA. AWS와 공동 개발한 오픈 상호운용 스펙 기반 |
| **[Oracle Interconnect for Azure](https://docs.oracle.com/iaas/Content/multicloud/interconnect-azure.htm)** | OCI ↔ Azure | GA. 크로스 클라우드 데이터 전송 무료 |
| **[Oracle Interconnect for Google Cloud](https://docs.oracle.com/iaas/Content/Network/Concepts/access-to-google-cloud-platform.htm)** | OCI ↔ Google Cloud | GA. 크로스 클라우드 데이터 전송 무료 |
| **Oracle Interconnect for AWS** | OCI ↔ AWS | 2026년 내 출시 예정 (AWS Interconnect–multicloud 연동) |

{% hint style="info" %}
2025년 12월 AWS re:Invent에서 AWS와 Google Cloud가 오픈 상호운용 스펙 기반의 공동 멀티클라우드 인터커넥트를 발표했습니다. Microsoft Azure도 이 스펙에 참여를 확인했으며, Oracle도 AWS Interconnect–multicloud와의 연동을 발표(2026.04)했습니다.
{% endhint %}

### Cross-Cloud Interconnect vs 전용 연결 + IX

| 비교 항목 | Cross-Cloud Interconnect | 전용 연결 + IX (Direct Connect + ExpressRoute 등) |
| --- | --- | --- |
| **경유 지점** | 벤더 간 직접 연결 (단일 홉) | IX 또는 코로케이션 시설 경유 (2~3홉) |
| **설정 복잡도** | 콘솔에서 상대 벤더 선택 후 프로비저닝 | 양쪽 전용 연결 + IX 포트 + BGP 설정 |
| **레이턴시** | 최소 (같은 메트로 내 직접 연결) | IX 경유로 약간 높음 |
| **비용 구조** | 포트 비용 + 데이터 전송 (OCI는 전송 무료) | 양쪽 전용 연결 비용 + IX 포트 비용 |
| **가용 구간** | 벤더가 지원하는 구간만 | IX가 있는 모든 구간 |

**선택 기준:**

- 벤더 간 직접 연결이 지원되는 구간이면 Cross-Cloud Interconnect가 단순하고 레이턴시도 낮음
- 아직 지원되지 않는 구간(예: AWS ↔ Azure)이거나 온프레미스도 함께 연결해야 하면 IX 경유 방식 사용

## 참고하기

### AWS

- [AWS — Hybrid Connectivity](https://docs.aws.amazon.com/whitepapers/latest/hybrid-connectivity/hybrid-connectivity.html)
- [AWS Direct Connect](https://aws.amazon.com/ko/directconnect/)

### Azure

- [Azure — Hub-spoke Network Topology](https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke)
- [Azure ExpressRoute](https://azure.microsoft.com/ko-kr/products/expressroute/)

### Google Cloud

- [Google Cloud — Hybrid and Multi-cloud Network Architectures](https://cloud.google.com/architecture/network-hybrid-multicloud)
- [Google Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect)

### OCI

- [OCI FastConnect](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/fastconnect.htm)

### 표준 및 커뮤니티

- [KINX](https://www.kinx.net/) — 국내 최대 IX
- [Megaport](https://www.megaport.com/) — 글로벌 Cloud Exchange
- [NIST Multi-Cloud Security Public Working Group](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture)
- [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918)
