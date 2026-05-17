---
description: 관리형 DNS, 라우팅 정책, DNSSEC, Private DNS를 벤더별로 비교합니다.
---

# DNS

> 문서 기준: 2026년 5월

## 개요

**DNS** (Domain Name System)는 도메인 이름(예: example.com)을 IP 주소로 변환하는 서비스입니다. 모든 인터넷 통신의 첫 단계이므로, DNS가 중단되면 서비스 전체가 접근 불가능해집니다.

온프레미스에서는 BIND나 Windows DNS를 직접 운영하지만, 클라우드 관리형 DNS는 글로벌 Anycast 네트워크에서 운영되어 단일 장애점이 없습니다. AWS Route 53, Google Cloud Cloud DNS, Azure DNS는 모두 **100% 가용성 SLA**를 제공합니다.

{% hint style="info" %}
DNS가 중단되면 서비스 URL 자체가 응답하지 않아 전체 서비스가 접근 불가능해집니다. 프로덕션 환경에서는 **TTL을 낮게** 유지하여(300초 이하) DNS 장애 조치 시 빠르게 전파되도록 하세요.
{% endhint %}

단순 이름 해석 외에도 지리적 라우팅, 헬스 체크 기반 장애 조치, 가중치 분배 등 트래픽 관리 기능을 포함합니다.

## DNS 레코드 유형

자주 사용하는 DNS 레코드 타입입니다.

| 레코드 | 용도 | 예시 |
| --- | --- | --- |
| **A** | 도메인을 IPv4 주소로 매핑 | `example.com → 93.184.216.34` |
| **AAAA** | 도메인을 IPv6 주소로 매핑 | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | 다른 도메인 이름으로 별칭 연결 | `www.example.com → example.com` |
| **MX** | 메일 서버 지정 (우선순위 포함) | `example.com → 10 mail.example.com` |
| **TXT** | 텍스트 정보 (SPF, DKIM, 도메인 소유권 증명) | `v=spf1 include:_spf.google.com ~all` |
| **NS** | 해당 도메인의 권한 있는 네임서버 지정 | `example.com → ns1.example.com` |
| **SRV** | 서비스 위치 지정 (포트 포함) | `_sip._tcp.example.com → 10 60 5060 sip.example.com` |
| **PTR** | IP를 도메인으로 역방향 매핑 | `34.216.184.93.in-addr.arpa → example.com` |
| **ALIAS/ANAME** | CNAME과 유사하되 루트 도메인에서 사용 가능 | AWS Alias, Azure Alias, Google Cloud 자체 ALIAS 레코드 타입(Public Zone 한정) |

### AWS의 Alias 레코드 특징

AWS Route 53의 **Alias Record**는 CNAME처럼 보이지만 DNS 쿼리가 아닌 AWS 내부에서 직접 리졸빙되어, 루트 도메인(zone apex)에도 사용 가능하고 비용도 없습니다. ELB, CloudFront, S3 웹사이트 호스팅 등 AWS 리소스를 가리킬 때 사용합니다.

## 호스팅존 (Public vs Private)

DNS 호스팅존은 도메인의 레코드를 관리하는 컨테이너입니다. **Public Zone**은 인터넷에서 접근 가능한 레코드를, **Private Zone**은 VPC/VNet 내부에서만 해석되는 레코드를 관리합니다.

### Split-horizon DNS

동일한 도메인에 대해 요청 출처에 따라 다른 레코드를 반환하는 패턴입니다.

- 내부 사용자(VPC 내) → 프라이빗 IP로 응답
- 외부 사용자(인터넷) → 퍼블릭 IP로 응답

이를 통해 내부 API 엔드포인트를 외부에 노출하지 않으면서 동일 도메인을 사용할 수 있습니다.

### 벤더별 구현

| 벤더 | Public Zone | Private Zone | Split-horizon |
| --- | --- | --- | --- |
| AWS | Route 53 Public Hosted Zone | Route 53 Private Hosted Zone (VPC 연결) | Public/Private Zone 분리로 구현 |
| Azure | Azure Public DNS Zone | Azure Private DNS Zone (VNet 링크, 자동 등록) | Public/Private Zone 분리 |
| Google Cloud | Cloud DNS Public Zone | Cloud DNS Private Zone (VPC 바인딩) | 네이티브 Split-horizon 지원 |
| OCI | OCI DNS Public Zone | OCI DNS Private Views (VCN 연결) | DNS Views로 조건부 응답 |

### 활용 시나리오

- **하이브리드 환경**: 온프레미스↔클라우드 간 이름 해석 (조건부 포워딩)
- **멀티 VPC**: 중앙 DNS 관리 — 공유 서비스 VPC에서 Private Zone을 다른 VPC에 연결
- **보안 격리**: 내부 DB/API 엔드포인트를 외부에 노출하지 않으면서 편리한 이름 사용

멀티클라우드 환경에서의 DNS 통합(조건부 포워딩, 크로스 벤더 리졸빙)은 [멀티클라우드 커넥티비티 — DNS 통합 전략](multicloud-connectivity.md)을 참고하세요.

## 제품 비교

| 벤더 | 제품 | 포지셔닝 |
| --- | --- | --- |
| AWS | Route 53 | 도메인 등록 + DNS + 헬스 체크 + 라우팅 정책 올인원. 100% SLA |
| Azure | Azure DNS + Traffic Manager | DNS 호스팅과 트래픽 라우팅이 별도 서비스로 분리. **100% SLA** |
| Google Cloud | Cloud DNS | 100% SLA. DNSSEC 기본 지원. 자체 헬스 체크 없음 |
| OCI | OCI DNS | 글로벌 Anycast. Traffic Management로 라우팅 정책 제공 |

### 라우팅 정책

DNS 수준에서 트래픽을 제어할 수 있는 라우팅 정책입니다.

| 정책 | 설명 | AWS Route 53 | Azure Traffic Manager | Google Cloud Cloud DNS | OCI DNS Traffic Management |
| --- | --- | --- | --- | --- | --- |
| **지리적** | 사용자 위치 기반 라우팅 | Geolocation / Geoproximity | Geographic | Geolocation | Geolocation Steering |
| **가중치** | 비율 기반 분배 (A/B 테스트, 점진적 배포) | Weighted | Weighted | Weighted Round Robin | Load Balancer |
| **장애 조치** | 헬스 체크 실패 시 대체 엔드포인트로 전환 | Failover | Priority | — (별도 헬스 체크) | Failover |
| **지연 시간** | 가장 빠른 리전으로 라우팅 | Latency | Performance | — | — |
| **멀티밸류** | 여러 IP 반환 + 헬스 체크 | Multivalue Answer | — | — | — |

### 헬스 체크

| 벤더 | 기능 | 비고 |
| --- | --- | --- |
| AWS | Route 53 Health Checks | HTTP/HTTPS/TCP. CloudWatch 알람 연동. 장애 시 자동 DNS 전환 |
| Azure | Traffic Manager Probes | HTTP/HTTPS/TCP. 엔드포인트 모니터링 |
| Google Cloud | — | Cloud DNS 자체 헬스 체크 없음. Cloud Load Balancing 헬스 체크와 조합 |
| OCI | Health Checks | HTTP/HTTPS/TCP. DNS Traffic Management와 연동 |

## 핵심 차이점

- **AWS Route 53** — 도메인 등록부터 라우팅까지 올인원. 라우팅 정책이 가장 다양합니다(Geoproximity, Multivalue 등).
- **Azure** — DNS 호스팅(Azure DNS)과 글로벌 트래픽 라우팅(Traffic Manager)이 별도 서비스입니다. Traffic Manager는 DNS 기반 글로벌 로드밸런서 역할을 합니다.
- **Google Cloud Cloud DNS** — DNSSEC 기본 지원, Split-horizon 네이티브 지원이 강점입니다. 자체 헬스 체크가 없어 장애 조치는 Cloud Load Balancing과 조합해야 합니다.
- **OCI DNS** — Traffic Management로 지리적 라우팅, 장애 조치 등의 정책을 제공하며, Health Checks와 연동하여 자동 DNS 전환이 가능합니다.

## DNSSEC

**DNSSEC** (DNS Security Extensions)은 DNS 응답의 위변조를 방지하는 보안 확장입니다. 공격자가 DNS 응답을 가로채 악성 사이트로 유도하는 DNS 스푸핑/캐시 포이즈닝을 막습니다.

| 벤더 | 지원 수준 |
| --- | --- |
| AWS Route 53 | DNSSEC 서명 및 등록 지원 |
| Azure DNS | DNSSEC 서명 지원 |
| Google Cloud Cloud DNS | DNSSEC 서명 지원 (기본 활성화 옵션) |
| OCI DNS | DNSSEC 서명 지원 |

## 관련 문서

{% content-ref url="load-balancer.md" %}
[로드밸런서](load-balancer.md)
{% endcontent-ref %}

{% content-ref url="cdn.md" %}
[CDN](cdn.md)
{% endcontent-ref %}

{% content-ref url="multicloud-connectivity.md" %}
[멀티클라우드 커넥티비티](multicloud-connectivity.md)
{% endcontent-ref %}

## 참고하기

### AWS

- [Amazon Route 53 문서](https://docs.aws.amazon.com/ko_kr/route53/)
- [Route 53 라우팅 정책](https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/routing-policy.html)
- [Route 53 헬스 체크](https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/health-checks-creating.html)

### Azure

- [Azure DNS 문서](https://learn.microsoft.com/ko-kr/azure/dns/)
- [Azure Traffic Manager 문서](https://learn.microsoft.com/ko-kr/azure/traffic-manager/)
- [Azure DNS SLA (100%)](https://azure.microsoft.com/en-us/support/legal/sla/dns/v1_1/)

### Google Cloud

- [Cloud DNS 문서](https://cloud.google.com/dns/docs)
- [Cloud DNS ALIAS 레코드 개요](https://cloud.google.com/dns/docs/records-overview)

### OCI

- [OCI DNS 문서](https://docs.oracle.com/en-us/iaas/Content/DNS/home.htm)
