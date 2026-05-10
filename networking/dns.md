# DNS

> 문서 기준: 2026년 5월

## 개요

**DNS** (Domain Name System)는 도메인 이름(예: example.com)을 IP 주소로 변환하는 서비스입니다. 모든 인터넷 통신의 첫 단계이므로, DNS가 중단되면 서비스 전체가 접근 불가능해집니다.

온프레미스에서는 BIND나 Windows DNS를 직접 운영하지만, 클라우드 관리형 DNS는 글로벌 Anycast 네트워크에서 운영되어 단일 장애점이 없습니다. AWS Route 53과 GCP Cloud DNS는 **100% 가용성 SLA**를 제공합니다.

단순 이름 해석 외에도 지리적 라우팅, 헬스 체크 기반 장애 조치, 가중치 분배 등 트래픽 관리 기능을 포함합니다.

## 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Route 53 | 도메인 등록 + DNS + 헬스 체크 + 라우팅 정책 통합. 100% SLA |
| Azure | Azure DNS + Traffic Manager | DNS 호스팅과 트래픽 라우팅이 별도 서비스 |
| GCP | Cloud DNS | 100% SLA. Cloud Domains로 도메인 등록 |
| OCI | OCI DNS | 글로벌 Anycast. Traffic Management로 라우팅 정책 제공 |

### 라우팅 정책

DNS 수준에서 트래픽을 제어할 수 있는 라우팅 정책입니다.

| 정책 | 설명 | AWS Route 53 | Azure Traffic Manager | GCP Cloud DNS | OCI DNS Traffic Management |
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
| GCP | — | Cloud DNS 자체 헬스 체크 없음. Cloud Load Balancing 헬스 체크와 조합 |
| OCI | Health Checks | HTTP/HTTPS/TCP. DNS Traffic Management와 연동 |

## 핵심 차이점

**AWS Route 53** — 도메인 등록, DNS, 헬스 체크, 라우팅 정책을 하나의 서비스로 통합합니다. 라우팅 정책이 가장 다양하며(Geoproximity, Multivalue 등), 100% SLA를 제공하는 유일한 AWS 서비스입니다.

**Azure** — DNS 호스팅(Azure DNS)과 트래픽 라우팅(Traffic Manager)이 별도 서비스로 분리되어 있습니다. Traffic Manager는 DNS 기반 글로벌 로드밸런서 역할을 합니다.

**GCP Cloud DNS** — 100% SLA를 제공하며, DNSSEC을 기본 지원합니다. 다만 자체 헬스 체크가 없어 장애 조치는 Cloud Load Balancing과 조합해야 합니다.

**OCI DNS** — 글로벌 Anycast 네트워크에서 운영되며, Traffic Management로 지리적 라우팅, 장애 조치 등의 정책을 제공합니다. Health Checks와 연동하여 자동 DNS 전환이 가능합니다.

## 참고하기

### AWS

- [Amazon Route 53 문서](https://docs.aws.amazon.com/ko_kr/route53/)
- [Route 53 라우팅 정책](https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/routing-policy.html)
- [Route 53 헬스 체크](https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/health-checks-creating.html)

### Azure

- [Azure DNS 문서](https://learn.microsoft.com/ko-kr/azure/dns/)
- [Azure Traffic Manager 문서](https://learn.microsoft.com/ko-kr/azure/traffic-manager/)

### GCP

- [Cloud DNS 문서](https://cloud.google.com/dns/docs)
- [Cloud DNS SLA](https://cloud.google.com/dns/sla)
- [Cloud Domains 문서](https://cloud.google.com/domains/docs)

### OCI

- [OCI DNS 문서](https://docs.oracle.com/en-us/iaas/Content/DNS/home.htm)
- [OCI Traffic Management](https://docs.oracle.com/en-us/iaas/Content/TrafficManagement/home.htm)
- [OCI Health Checks](https://docs.oracle.com/en-us/iaas/Content/HealthChecks/home.htm)
