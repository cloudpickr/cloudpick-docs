---
description: VPC/VNet/VCN 개념, 서브넷 설계, 보안 계층, NAT, VPC 간 연결 방식을 4사 비교합니다.
---

# VPC와 서브넷

> 문서 기준: 2026년 5월

## 개요

온프레미스에서는 물리적인 네트워크 장비(스위치, 라우터, 방화벽)로 네트워크를 구성합니다. 클라우드에서는 이 모든 것을 소프트웨어로 정의합니다.

**VPC** (Virtual Private Cloud)는 클라우드 안에 만드는 논리적으로 격리된 가상 네트워크입니다. 온프레미스의 사내 네트워크에 해당하며, IP 대역, 서브넷, 라우팅, 방화벽 규칙을 사용자가 직접 설계합니다.

{% hint style="info" %}
AWS VPC를 아시는 분을 위해: GCP는 VPC가 글로벌이고, OCI는 VCN이라 부릅니다.
{% endhint %}

서브넷은 가용영역(AZ) 단위로 배치되며, 여러 AZ에 서브넷을 분산하면 장애 도메인을 분리하여 고가용성을 확보할 수 있습니다. 리전과 가용영역의 개념은 [리전과 가용영역](../about-cloud/regions-and-zones.md)에서 자세히 다룹니다.

## 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | VPC | 리전 단위. 서브넷은 AZ 단위 |
| Azure | VNet (Virtual Network) | 리전 단위. 서브넷은 리전 내 자유 배치 |
| GCP | VPC | **글로벌** (리전에 종속되지 않음). 서브넷이 리전 단위 |
| OCI | VCN (Virtual Cloud Network) | 리전 단위. 서브넷은 리전 또는 AD 단위 |

### 보안 (네트워크 방화벽)

클라우드 네트워크 보안은 여러 계층으로 구성됩니다.

| 계층 | AWS | Azure | GCP | OCI | 비고 |
| --- | --- | --- | --- | --- | --- |
| **인스턴스 단위** | Security Groups (상태 유지) | NSG | Firewall Rules (태그 기반) | Security Lists / NSG | 가장 기본. 인바운드/아웃바운드 규칙 |
| **서브넷 단위** | Network ACL (상태 비유지) | NSG (서브넷 연결) | — | Security Lists (서브넷 연결) | 서브넷 경계에서 필터링 |
| **VPC 단위 (IDS/IPS)** | Network Firewall | Azure Firewall | Cloud Firewall | OCI Network Firewall | L7 검사, 위협 인텔리전스, 도메인 필터링 |
| **DDoS 방어** | Shield (Standard 무료 / Advanced 유료) | DDoS Protection | Cloud Armor | OCI WAF (DDoS 보호 포함) | L3/L4 DDoS 자동 완화 |
| **웹 앱 방화벽 (WAF)** | AWS WAF | Azure WAF | Cloud Armor WAF | OCI WAF | L7 공격 차단 (SQL Injection, XSS 등) |

Security Groups/NSG만으로 기본 보안은 가능하지만, 프로덕션 환경에서는 VPC 단위 방화벽과 WAF를 추가하여 심층 방어(Defense in Depth)를 구성하는 것을 권장합니다.

### NAT (Network Address Translation)

프라이빗 서브넷의 인스턴스는 인터넷에서 직접 접근할 수 없지만, 소프트웨어 업데이트나 외부 API 호출을 위해 아웃바운드 인터넷 접근이 필요한 경우가 있습니다. **NAT Gateway**는 프라이빗 인스턴스가 인터넷으로 나갈 수 있게 하면서, 외부에서의 인바운드 접근은 차단합니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | NAT Gateway | AZ 단위. 고가용성을 위해 AZ별로 생성 권장 |
| Azure | NAT Gateway | 서브넷 단위 연결 |
| GCP | Cloud NAT | 리전 단위. VM에 외부 IP 없이 인터넷 접근 가능 |
| OCI | NAT Gateway | VCN 단위. 프라이빗 서브넷의 아웃바운드 인터넷 접근 |

{% hint style="warning" %}
NAT Gateway는 시간당 비용 + 데이터 처리 비용이 발생합니다. 대량 아웃바운드 트래픽이 있는 경우 비용에 주의해야 합니다.
{% endhint %}

### 프라이빗 연결 (온프레미스 ↔ 클라우드)

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Direct Connect / Site-to-Site VPN | |
| Azure | ExpressRoute / VPN Gateway | |
| GCP | Cloud Interconnect / Cloud VPN | |
| OCI | FastConnect / Site-to-Site VPN | |

## 핵심 차이점

- **GCP** — VPC가 글로벌이어서 리전 간 서브넷을 하나의 VPC로 관리할 수 있습니다. AWS/Azure는 리전별로 VPC/VNet을 만들고 피어링해야 합니다.
- **AWS** — Security Groups(인스턴스 단위)와 Network ACL(서브넷 단위) 이중 방화벽 구조입니다.
- **Azure** — VNet 피어링이 글로벌로 가능하여 리전 간 연결이 간편합니다.
- **OCI** — VCN은 리전 단위이며, 서브넷을 리전 또는 AD 단위로 배치할 수 있습니다. Security Lists와 NSG를 조합하여 유연한 보안 구성이 가능합니다.

## 서브넷 설계 모범사례

서브넷은 **퍼블릭(Public)**, **프라이빗(Private)**, **격리(Isolated)** 3계층으로 나누는 것이 일반적입니다.

| 계층 | 용도 | 인터넷 접근 | 배치 리소스 |
| --- | --- | --- | --- |
| **퍼블릭** | 외부 트래픽 수신 | 인바운드/아웃바운드 모두 가능 | ALB, NAT Gateway, Bastion Host |
| **프라이빗** | 애플리케이션 계층 | NAT Gateway 통해 아웃바운드만 | EC2, ECS, EKS 워커 노드 |
| **격리** | DB, 내부 시스템 | 인터넷 접근 불가 (VPC 내부만) | RDS, ElastiCache |

### CIDR 계획

- **VPC CIDR**은 `/16` (65,536개 IP)을 권장. 너무 작으면 확장 어려움.
- **서브넷 CIDR**은 `/24` (256개 IP) 단위로 시작. 필요 시 `/20` (4,096개)로 확대.
- **AZ별로 서브넷 분산**. 최소 3개 AZ에 배치하여 고가용성 확보.
- **VPC 간 CIDR 중복 피하기**. 피어링/전용 연결 시 라우팅 불가.

멀티클라우드 환경의 CIDR 설계는 [멀티클라우드 커넥티비티](multicloud-connectivity.md)를 참고하세요.

## 라우팅 테이블

각 서브넷은 라우팅 테이블에 연결됩니다. 라우팅 테이블은 트래픽의 목적지에 따라 어디로 전송할지 결정합니다.

### 기본 라우팅 규칙

| 목적지 | 대상 | 설명 |
| --- | --- | --- |
| `10.0.0.0/16` (VPC CIDR) | `local` | VPC 내부 트래픽 |
| `0.0.0.0/0` (모든 외부) | Internet Gateway | 퍼블릭 서브넷 |
| `0.0.0.0/0` | NAT Gateway | 프라이빗 서브넷 (아웃바운드만) |
| `192.168.0.0/16` | VPC Peering / Transit Gateway | 다른 VPC/온프레미스 |

## VPC 간 연결

### VPC 피어링 vs Transit Gateway

| 방식 | 특징 | 사용 시점 |
| --- | --- | --- |
| **VPC 피어링** | 1:1 직접 연결, 전이적(transitive) 아님 | 소수의 VPC 연결 |
| **Transit Gateway / vWAN** | 허브-스포크, N:N 연결, 전이적 라우팅 | 다수의 VPC + 온프레미스 |

4사 비교:

| 벤더 | 1:1 피어링 | 허브-스포크 |
| --- | --- | --- |
| AWS | VPC Peering | Transit Gateway |
| Azure | VNet Peering (글로벌 가능) | Azure Virtual WAN |
| GCP | VPC Network Peering | 글로벌 VPC (피어링 불필요) |
| OCI | Local Peering Gateway (LPG) / Remote Peering Connector (RPC) | Dynamic Routing Gateway (DRG) |

### VPC 엔드포인트 (PrivateLink)

인터넷을 거치지 않고 VPC 내에서 벤더 서비스(S3, Blob 등)에 접근할 수 있습니다. 보안과 비용(데이터 전송) 모두 이점이 있습니다.

| 벤더 | 제품 |
| --- | --- |
| AWS | VPC Endpoint / PrivateLink |
| Azure | Private Endpoint / Private Link |
| GCP | Private Service Connect |
| OCI | Service Gateway / Private Endpoint |

## 참고하기

### AWS

- [Amazon VPC 문서](https://docs.aws.amazon.com/ko_kr/vpc/)
- [Amazon VPC Security Groups](https://docs.aws.amazon.com/ko_kr/vpc/latest/userguide/vpc-security-groups.html)

### Azure

- [Azure Virtual Network 문서](https://learn.microsoft.com/ko-kr/azure/virtual-network/)
- [Azure NSG 문서](https://learn.microsoft.com/ko-kr/azure/virtual-network/network-security-groups-overview)

### GCP

- [Google Cloud VPC 문서](https://cloud.google.com/vpc/docs)
- [Google Cloud 방화벽 규칙](https://cloud.google.com/firewall/docs/firewalls)

### OCI

- [OCI VCN 문서](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/overview.htm)
- [OCI Security Lists](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securitylists.htm)
- [OCI Network Security Groups](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/networksecuritygroups.htm)
