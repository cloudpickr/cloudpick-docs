# 로드밸런서

> 문서 기준: 2026년 5월

## 개요

서버가 여러 대일 때, 사용자 요청을 어떤 서버로 보낼지 분배하는 것이 **로드밸런서**입니다. 온프레미스에서는 F5, Citrix 같은 하드웨어 장비를 사용하지만, 클라우드에서는 관리형 서비스로 제공됩니다.

오토스케일링과 함께 사용하면, 서버가 추가/제거될 때 자동으로 트래픽 분배 대상이 조정됩니다.

## 제품 비교

### L7 (HTTP/HTTPS) 로드밸런서

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | ALB (Application Load Balancer) | 경로/호스트 기반 라우팅, WebSocket, gRPC |
| Azure | Application Gateway | WAF 통합 가능 |
| GCP | External HTTP(S) Load Balancer | 글로벌 (단일 IP로 전 세계 서빙) |
| OCI | OCI Load Balancer | L7. 경로/호스트 기반 라우팅, SSL 종료 |

### L4 (TCP/UDP) 로드밸런서

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | NLB (Network Load Balancer) | 초저지연, 고정 IP |
| Azure | Azure Load Balancer | Standard/Basic 티어 |
| GCP | TCP/UDP Load Balancer | 리전 또는 글로벌 |
| OCI | OCI Network Load Balancer | L4. 초저지연, IP 해시/5-tuple 해시 |

### 글로벌 로드밸런서 / 가속기

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Global Accelerator | Anycast IP로 가장 가까운 엣지로 라우팅 |
| Azure | Front Door | 글로벌 L7 + CDN + WAF 통합 |
| GCP | Cloud Load Balancing | 기본적으로 글로벌 (단일 Anycast IP) |
| OCI | OCI DNS Traffic Management | DNS 기반 글로벌 트래픽 분배 |

## 핵심 구성 요소

로드밸런서는 어디로 보낼지(규칙)와 누구에게 보낼지(대상 그룹)를 설정해야 합니다. L7과 L4는 라우팅 방식이 다릅니다.

### L7 (HTTP/HTTPS)

| 개념 | AWS ALB | Azure App Gateway | GCP HTTP(S) LB | OCI Load Balancer |
| --- | --- | --- | --- | --- |
| **라우팅 규칙** | Listener Rule (경로/호스트/헤더) | URL Path Map | URL Map | Routing Policy (경로/호스트) |
| **대상 그룹** | Target Group | Backend Pool | Backend Service | Backend Set |
| **헬스 체크** | HTTP/HTTPS 헬스 체크 | Health Probe | Health Check | Health Check |

경로(`/api/*`), 호스트(`api.example.com`), 헤더 값 등으로 세밀하게 트래픽을 분배할 수 있습니다.

### L4 (TCP/UDP)

| 개념 | AWS NLB | Azure LB | GCP TCP/UDP LB | OCI Network LB |
| --- | --- | --- | --- | --- |
| **라우팅** | 포트 기반 | Frontend IP + Port | Forwarding Rule | Listener (포트 기반) |
| **대상 그룹** | Target Group (IP/인스턴스) | Backend Pool | Backend Service | Backend Set |
| **특징** | 고정 IP, 초저지연, TLS 패스스루 | Standard/Basic 티어 | 리전 또는 글로벌 | 초저지연, IP 해시 |

L4는 패킷 내용을 보지 않고 포트 단위로 분배하므로 지연이 매우 낮습니다. DB, gRPC, 게임 서버 등 HTTP가 아닌 프로토콜에 사용합니다.

## 핵심 차이점

- **AWS** — ALB/NLB가 리전 단위이며, 글로벌 라우팅은 Global Accelerator를 별도로 사용합니다.
- **Azure** — Front Door가 글로벌 L7 + CDN + WAF를 하나의 서비스로 통합합니다.
- **GCP** — 로드밸런서가 기본적으로 글로벌입니다. 하나의 IP로 전 세계 사용자에게 가장 가까운 백엔드로 라우팅합니다.
- **OCI** — Load Balancer(L7)와 Network Load Balancer(L4)를 분리 제공하며, DNS Traffic Management로 글로벌 트래픽 분배를 구성합니다.

## 참고하기

### AWS

- [Elastic Load Balancing 문서](https://docs.aws.amazon.com/ko_kr/elasticloadbalancing/)
- [AWS Global Accelerator 문서](https://docs.aws.amazon.com/ko_kr/global-accelerator/)

### Azure

- [Azure Load Balancer 문서](https://learn.microsoft.com/ko-kr/azure/load-balancer/)
- [Azure Front Door 문서](https://learn.microsoft.com/ko-kr/azure/frontdoor/)

### GCP

- [Google Cloud Load Balancing 문서](https://cloud.google.com/load-balancing/docs)

### OCI

- [OCI Load Balancer 문서](https://docs.oracle.com/en-us/iaas/Content/Balance/home.htm)
- [OCI Network Load Balancer 문서](https://docs.oracle.com/en-us/iaas/Content/NetworkLoadBalancer/home.htm)
