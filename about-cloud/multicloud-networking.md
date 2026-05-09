# 멀티클라우드 네트워킹

## 왜 클라우드 간 네트워킹이 중요한가

멀티클라우드 환경에서 가장 먼저 부딪히는 기술적 과제는 **"클라우드 A의 워크로드가 클라우드 B의 워크로드와 어떻게 통신하는가?"**입니다. 단일 벤더 내에서는 VPC 피어링이나 프라이빗 링크로 간단히 해결되지만, 벤더 경계를 넘으면 네트워크 설계, 비용, 보안 모두 복잡해집니다.

## CIDR 계획 — IP 충돌 방지

멀티클라우드의 첫 번째 규칙: **모든 클라우드의 VPC/VNet CIDR이 겹치지 않아야 합니다.**

IP가 겹치면 라우팅이 불가능하고, 나중에 변경하려면 워크로드를 재배포해야 합니다. 처음부터 전체 IP 공간을 계획하세요.

### 권장 설계 패턴

RFC 1918 프라이빗 대역을 벤더별로 분할합니다.

| 대역 | 할당 | 예시 |
| --- | --- | --- |
| `10.0.0.0/8` | AWS | `10.0.0.0/16` (prod), `10.1.0.0/16` (dev) |
| `172.16.0.0/12` | Azure | `172.16.0.0/16` (prod), `172.17.0.0/16` (dev) |
| `192.168.0.0/16` | GCP / 국내 클라우드 | `192.168.0.0/20` (NCP), `192.168.16.0/20` (GCP) |

> **팁:** `/16` 단위로 벤더에 할당하고, 그 안에서 `/24` 서브넷을 나누면 향후 확장에 유연합니다. 온프레미스가 있다면 온프레미스 대역도 반드시 포함하여 계획하세요.

### 주의사항

- GCP는 VPC가 글로벌이므로 리전별 서브넷만 다르면 됩니다
- Azure VNet은 리전 단위이므로 리전마다 별도 CIDR 할당 필요
- NCP Classic은 `/16` 고정, VPC는 `/16`~`/28` 선택 가능

## 클라우드 간 연결 방식

### Site-to-Site VPN

가장 빠르게 시작할 수 있는 방법입니다. 인터넷을 통해 IPsec 터널을 구성합니다.

| 항목 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **서비스명** | Site-to-Site VPN | VPN Gateway | Cloud VPN |
| **최대 대역폭** | 1.25 Gbps (터널당) | 10 Gbps (VpnGw5) | 3 Gbps (HA VPN) |
| **HA 구성** | 2 터널 기본 제공 | Active-Active 모드 | HA VPN (99.99% SLA) |
| **비용 (서울)** | ~$0.05/h + 이그레스 | ~$0.19/h (VpnGw1) | ~$0.075/h + 이그레스 |

**AWS ↔ GCP 연결 예시:**
1. AWS에서 Customer Gateway(GCP의 외부 IP) + VPN Connection 생성
2. GCP에서 External VPN Gateway(AWS의 외부 IP) + HA VPN 터널 생성
3. BGP로 경로 교환 (AWS ASN: 64512, GCP ASN: 65001 등)

> **언제 사용:** 대역폭 1Gbps 이하, 빠른 PoC, 비용 민감한 환경

### 전용 연결 (Dedicated Interconnect)

물리적 전용 회선으로 연결합니다. 지연시간이 낮고 대역폭이 크지만, 설치에 수 주가 걸립니다.

| 항목 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **서비스명** | Direct Connect | ExpressRoute | Cloud Interconnect |
| **최대 대역폭** | 100 Gbps | 100 Gbps | 200 Gbps |
| **한국 PoP** | KINX, LG U+ | KINX, LG U+ | KINX |
| **최소 약정** | 없음 (포트 시간당 과금) | 없음~1년 | 없음 |
| **이그레스 할인** | 일반 대비 ~50% 할인 | 무제한 이그레스 포함 | 일반 대비 할인 |

> **Azure ExpressRoute의 특이점:** 이그레스 요금이 회선 요금에 포함되어 있어, 대량 데이터 이동 시 가장 경제적일 수 있습니다.

### Cloud Exchange (KINX, Megaport, Equinix Fabric)

Cloud Exchange는 하나의 물리적 연결로 여러 클라우드에 동시 접속할 수 있는 서비스입니다. 멀티클라우드 환경에서 가장 효율적인 연결 방식입니다.

```
┌─────────┐     ┌──────────────┐     ┌─────────┐
│   AWS   │────▶│              │◀────│  Azure  │
│  (DX)   │     │  KINX / IX   │     │  (ER)   │
└─────────┘     │              │     └─────────┘
                │  Cloud       │
┌─────────┐     │  Exchange    │     ┌─────────┐
│   GCP   │────▶│              │◀────│   NCP   │
│  (CI)   │     │              │     │         │
└─────────┘     └──────────────┘     └─────────┘
```

**한국에서의 선택지:**
- **KINX**: 국내 최대 IX(Internet Exchange). AWS, Azure, GCP, NCP 모두 PoP 보유
- **Megaport**: 글로벌 Cloud Exchange. 서울 PoP 있음
- **Equinix Fabric**: 글로벌 최대. 서울 데이터센터 운영

> **언제 사용:** 3개 이상의 클라우드를 연결할 때, 온프레미스도 함께 연결할 때

## 트랜짓 아키텍처 패턴

### Hub-and-Spoke

중앙 허브를 두고 각 클라우드를 스포크로 연결하는 패턴입니다.

```
                    ┌───────────┐
         ┌─────────│  Hub VPC  │─────────┐
         │         │ (Transit) │         │
         │         └───────────┘         │
         │              │                │
    ┌────▼────┐    ┌────▼────┐    ┌─────▼────┐
    │  AWS    │    │  Azure  │    │   GCP    │
    │  Spoke  │    │  Spoke  │    │  Spoke   │
    └─────────┘    └─────────┘    └──────────┘
```

- **허브 위치:** 가장 트래픽이 많은 벤더 또는 온프레미스
- **장점:** 보안 정책을 허브에서 중앙 관리, 라우팅 단순화
- **단점:** 허브가 병목/단일 장애점이 될 수 있음

### AWS Transit Gateway + 타 벤더 VPN

AWS Transit Gateway를 허브로 사용하고, Azure/GCP를 VPN으로 연결하는 패턴이 한국에서 가장 흔합니다.

| 구간 | 연결 방식 | 비고 |
| --- | --- | --- |
| AWS 내부 VPC 간 | Transit Gateway Attachment | 리전 내 ~$0.02/GB |
| AWS ↔ Azure | Site-to-Site VPN (TGW 연결) | BGP 경로 교환 |
| AWS ↔ NCP | Site-to-Site VPN | NCP IPsec VPN 사용 |

## 이그레스 비용 비교

클라우드 간 데이터 이동의 가장 큰 비용 요소는 이그레스(아웃바운드) 요금입니다.

| 구간 | 단가 (서울 리전 기준) | 비고 |
| --- | --- | --- |
| AWS → 인터넷 | $0.126/GB (처음 10TB) | 이후 체감 |
| Azure → 인터넷 | $0.12/GB | 처음 5GB/월 무료 |
| GCP → 인터넷 | $0.12/GB | 처음 200GB/월 무료 |
| AWS → Direct Connect | ~$0.04/GB | 회선비 별도 |
| Azure → ExpressRoute | 포함 (Unlimited 플랜) | 회선비에 포함 |
| GCP → Interconnect | ~$0.05/GB | 회선비 별도 |
| NCP → 인터넷 | 무료 (일정량) → 이후 과금 | 플랜별 상이 |

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
| GCP | Cloud DNS Private Zone | VPC 바인딩 |

### 통합 패턴: 조건부 포워딩

```
┌─────────────────────────────────────────────────┐
│              통합 DNS 전략                        │
├─────────────────────────────────────────────────┤
│                                                 │
│  *.aws.internal  → Route 53 Inbound Endpoint   │
│  *.azure.internal → Azure DNS Private Resolver │
│  *.gcp.internal  → Cloud DNS Inbound Policy    │
│  *.corp.internal → 온프레미스 DNS               │
│                                                 │
└─────────────────────────────────────────────────┘
```

**구현 방법:**
1. 각 클라우드에 인바운드 DNS 엔드포인트 생성
2. 조건부 포워딩 규칙 설정 (도메인 접미사 기반)
3. 온프레미스 DNS 서버 또는 허브 VPC의 DNS를 중앙 포워더로 사용

> **팁:** Route 53 Resolver의 아웃바운드 엔드포인트를 허브로 사용하면, AWS에서 Azure/GCP의 프라이빗 레코드를 조회할 수 있습니다.

## 설계 시 체크리스트

- [ ] 모든 클라우드/온프레미스의 CIDR이 겹치지 않는가?
- [ ] 연결 방식(VPN vs 전용 연결 vs Cloud Exchange)을 대역폭/비용 기준으로 선택했는가?
- [ ] 이그레스 비용을 월 단위로 추정했는가?
- [ ] DNS 조건부 포워딩으로 크로스 클라우드 이름 해석이 가능한가?
- [ ] 허브 장애 시 대체 경로(failover)가 있는가?
- [ ] 보안 그룹/방화벽 규칙이 클라우드 간 트래픽을 허용하는가?

---

다음 문서에서는 공동 책임 모델을 통해 각 벤더와 사용자의 보안 책임 범위를 살펴봅니다.

## 참고하기

### 벤더 레퍼런스 아키텍처

- [Google Cloud — Hybrid and Multi-cloud Network Architectures](https://cloud.google.com/architecture/network-hybrid-multicloud)
- [AWS — Hybrid Connectivity](https://docs.aws.amazon.com/whitepapers/latest/hybrid-connectivity/hybrid-connectivity.html)
- [Azure — Hub-spoke Network Topology](https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke)

### 전용 연결 및 IX

- [AWS Direct Connect](https://aws.amazon.com/ko/directconnect/)
- [Azure ExpressRoute](https://azure.microsoft.com/ko-kr/products/expressroute/)
- [Google Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect)
- [KINX (한국인터넷교환노드)](https://www.kinx.net/) — 국내 최대 IX, 멀티클라우드 연결
- [Megaport](https://www.megaport.com/) — 글로벌 Cloud Exchange

### 표준 및 프레임워크

- [NIST Multi-Cloud Security Public Working Group](https://csrc.nist.gov/projects/mcspwg/nccp) — 멀티클라우드 네트워크 보안
- [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918) — 프라이빗 IP 대역 표준

### 국내 클라우드 VPN/전용연결

- [NCP IPsec VPN](https://www.ncloud.com/product/networking/ipsecVpn)
- [KT Cloud VPN](https://cloud.kt.com/product/networking/)
- [NHN Cloud VPN Gateway](https://www.nhncloud.com/kr/service/network)
