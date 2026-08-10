---
title: "멀티클라우드 네트워크 설계 기초"
description: "멀티클라우드 네트워크를 시작하기 위한 CIDR 계획, 클라우드 간 연결 방식 비교, 선택 기준을 설명합니다."
---

> 문서 기준: 2026년 5월

:::note
트랜짓 아키텍처, 이그레스 비용, DNS 통합 등 심화 내용은 [멀티클라우드 네트워크 아키텍처](../../networking/multicloud-connectivity/)를 참고하세요.
:::

## 왜 클라우드 간 네트워킹이 중요한가

멀티클라우드 환경에서 가장 먼저 부딪히는 기술적 과제는 "**클라우드 A의 워크로드가 클라우드 B의 워크로드와 어떻게 통신하는가?**" 입니다. 단일 벤더 내에서는 VPC 피어링이나 프라이빗 링크로 간단히 해결되지만, 벤더 경계를 넘으면 네트워크 설계, 비용, 보안 모두 복잡해집니다.

## CIDR 계획 — IP 충돌 방지

멀티클라우드의 첫 번째 규칙: **모든 클라우드의 VPC/VNet CIDR이 겹치지 않아야 합니다.**

IP가 겹치면 라우팅이 불가능하고, 나중에 변경하려면 워크로드를 재배포해야 합니다. 처음부터 전체 IP 공간을 계획하세요.

### 권장 설계 패턴

RFC 1918 프라이빗 대역을 벤더별로 분할합니다.

| 대역 | 할당 | 예시 |
| --- | --- | --- |
| `10.0.0.0/8` | AWS | `10.0.0.0/16` (prod), `10.1.0.0/16` (dev) |
| `172.16.0.0/12` | Azure | `172.16.0.0/16` (prod), `172.17.0.0/16` (dev) |
| `192.168.0.0/16` | Google Cloud / 기타 | `192.168.0.0/20` (Google Cloud), `192.168.16.0/20` (기타) |

:::note
**팁:** `/16` 단위로 벤더에 할당하고, 그 안에서 `/24` 서브넷을 나누면 향후 확장에 유연합니다. 온프레미스가 있다면 온프레미스 대역도 반드시 포함하여 계획하세요.
:::

### 주의사항

- Google Cloud는 VPC가 글로벌이므로 리전별 서브넷만 다르면 됩니다
- Azure VNet은 리전 단위이므로 리전마다 별도 CIDR 할당 필요

## 클라우드 간 연결 방식

### Site-to-Site VPN

가장 빠르게 시작할 수 있는 방법입니다. 인터넷을 통해 IPsec 터널을 구성합니다.

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **서비스명** | Site-to-Site VPN | VPN Gateway | Cloud VPN | Site-to-Site VPN |
| **최대 대역폭** | 1.25 Gbps (터널당) | 10 Gbps (VpnGw5) | 3 Gbps (HA VPN) | 250 Mbps (터널당) |
| **HA 구성** | 2 터널 기본 제공 | Active-Active 모드 | HA VPN (99.99% SLA) | 이중화 터널 권장 |
| **비용 (서울)** | ~$0.05/h + 이그레스 | ~$0.19/h (VpnGw1) | ~$0.075/h + 이그레스 | 시간당 과금 + 이그레스 |

> 위 수치는 문서 작성 시점 기준이며 변동될 수 있습니다. 최신 가격은 각 벤더 공식 가격표를 확인하세요.

**AWS ↔ Google Cloud 연결 예시:**
1. AWS에서 Customer Gateway(Google Cloud의 외부 IP) + VPN Connection 생성
2. Google Cloud에서 External VPN Gateway(AWS의 외부 IP) + HA VPN 터널 생성
3. BGP로 경로 교환 (AWS ASN: 64512, Google Cloud ASN: 65001 등)

:::note
**언제 사용:** 대역폭 1Gbps 이하, 빠른 PoC, 비용 민감한 환경
:::

### 전용 연결 (Dedicated Interconnect)

물리적 전용 회선으로 연결합니다. 지연시간이 낮고 대역폭이 크지만, 설치에 수 주가 걸립니다.

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **서비스명** | Direct Connect | ExpressRoute | Cloud Interconnect | FastConnect |
| **최대 대역폭** | 100 Gbps | 100 Gbps | 200 Gbps | 100 Gbps |
| **최소 약정** | 없음 (포트 시간당 과금) | 없음~1년 | 없음 | 없음 (포트 시간당 과금) |
| **이그레스 할인** | 일반 대비 ~50% 할인 | 무제한 이그레스 포함 | 일반 대비 할인 | 이그레스 10TB/월 무료 |

> 위 수치는 문서 작성 시점 기준이며 변동될 수 있습니다. 최신 가격은 각 벤더 공식 가격표를 확인하세요.

:::note
**Azure ExpressRoute의 특이점:** 이그레스 요금이 회선 요금에 포함되어 있어, 대량 데이터 이동 시 가장 경제적일 수 있습니다.
:::

### Cloud Exchange (Megaport, Equinix Fabric 등)

Cloud Exchange는 하나의 물리적 연결로 여러 클라우드에 동시 접속할 수 있는 서비스입니다. 멀티클라우드 환경에서 가장 효율적인 연결 방식입니다.

```mermaid
graph LR
    AWS[AWS DX] --> IX[Cloud Exchange / IX]
    Azure[Azure ER] --> IX
    Google Cloud[Google Cloud CI] --> IX
    OCI[OCI FC] --> IX
```

**대표적인 선택지:**
- **Megaport**: 글로벌 Cloud Exchange. 주요 도시에 PoP 보유
- **Equinix Fabric**: 글로벌 최대. 전 세계 데이터센터 운영
- **각국 로컬 IX**: 국가별로 주요 CSP PoP를 모두 보유한 로컬 IX가 있는 경우가 많습니다 (예: 한국 KINX — [한국 가이드](../../korea/index/) 참고)

:::note
**언제 사용:** 3개 이상의 클라우드를 연결할 때, 온프레미스도 함께 연결할 때
:::

### 연결 방식 선택 가이드

| 기준 | Site-to-Site VPN | 전용 연결 (DX/ER/CI/FC) | Cloud Exchange (Megaport 등) |
| --- | --- | --- | --- |
| **대역폭** | ~1 Gbps | 10~100 Gbps | 1~10 Gbps |
| **지연 시간** | 인터넷 경유 (변동) | 전용 회선 (안정) | 전용 회선 (안정) |
| **구축 시간** | 수 분~수 시간 | 수 주~수 개월 | 수일~수 주 |
| **초기 비용** | 낮음 | 높음 (포트비, 회선비) | 중간 |
| **월 데이터 전송량** | < 1TB | > 5TB | 1~5TB |
| **연결 대상** | 1:1 (클라우드 2개) | 1:1 | 1:N (여러 클라우드 동시) |
| **적합한 상황** | PoC, 소규모, 빠른 시작 | 대용량, 안정성 필수, 프로덕션 | 3개 이상 클라우드 연결, 유연성 |

## 설계 시 체크리스트

- [ ] 모든 클라우드/온프레미스의 CIDR이 겹치지 않는가?
- [ ] 연결 방식(VPN vs 전용 연결 vs Cloud Exchange)을 대역폭/비용 기준으로 선택했는가?
- [ ] 이그레스 비용을 월 단위로 추정했는가?
- [ ] DNS 조건부 포워딩으로 크로스 클라우드 이름 해석이 가능한가?
- [ ] 허브 장애 시 대체 경로(failover)가 있는가?
- [ ] 보안 그룹/방화벽 규칙이 클라우드 간 트래픽을 허용하는가?

## 자주 하는 실수

- **CIDR 계획 없이 각 클라우드에서 기본 VPC 사용** — IP 대역이 겹쳐 나중에 연결이 불가능합니다. 처음부터 전체 IP 공간을 벤더별로 분할 계획하세요.
- **PoC에서 사용한 VPN을 그대로 프로덕션에 사용** — 대역폭 부족과 인터넷 경유 지연 변동으로 장애가 발생합니다. 월 1TB 이상이면 전용 연결을 검토하세요.
- **보안 그룹/방화벽에서 클라우드 간 트래픽을 허용하지 않음** — VPN/전용 연결을 구성해도 양쪽 방화벽 규칙이 없으면 통신이 안 됩니다.

## 관련 문서

트랜짓 아키텍처 패턴, 이그레스 비용 상세 비교, DNS 통합 전략은 아래 문서에서 다룹니다.

> 📄 [멀티클라우드 커넥티비티 (심화)](../../networking/multicloud-connectivity/)

## 참고하기

- [AWS Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)
- [Azure ExpressRoute](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)
- [Google Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/overview)
- [OCI FastConnect](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/fastconnect.htm)
- [RFC 1918 — Address Allocation for Private Internets](https://datatracker.ietf.org/doc/html/rfc1918)
