---
description: 물리적·논리적 망분리 개념, 클라우드에서의 네트워크 격리 구현 패턴, 규제 요건 대응을 설명합니다.
---

# 망분리와 네트워크 격리

> 문서 기준: 2026년 5월

## 개요

**망분리**(Network Segregation)는 업무망과 인터넷망을 분리하여 외부 위협이 내부 시스템에 도달하지 못하도록 하는 보안 통제입니다. 금융권(전자금융감독규정), 공공기관(국가정보보안기본지침), 의료(개인정보보호법) 등 규제 시장에서 핵심 보안 요건으로 적용됩니다.

온프레미스에서는 물리적으로 네트워크 장비를 분리하여 구현했습니다. 클라우드에서는 동일한 보안 목표를 **논리적 격리**로 달성할 수 있으며, 일부 규제 요건에서는 여전히 물리적 분리를 요구합니다.

{% hint style="warning" %}
망분리는 보안의 **한 계층**이지 전부가 아닙니다. 물리적으로 분리된 망에서도 내부자 위협, USB를 통한 악성코드 유입, 패치 지연으로 인한 취약점 노출은 발생합니다. 망분리와 함께 [제로 트러스트](zero-trust.md), [보안 태세 관리](security-posture.md)를 병행해야 합니다.
{% endhint %}

## 물리적 망분리 vs 논리적 망분리

| 구분 | 물리적 망분리 | 논리적 망분리 |
| --- | --- | --- |
| **방식** | 별도의 네트워크 장비·회선·단말 사용 | 동일 인프라에서 가상화·암호화·접근 통제로 분리 |
| **보안 수준** | 네트워크 레벨에서 완전 차단 | 설정 오류 시 경계 침투 가능 |
| **비용** | 장비·회선 이중화로 높음 | 상대적으로 낮음 |
| **유연성** | 변경에 수 주~수 개월 | 정책 변경으로 수 분 내 조정 |
| **패치/업데이트** | 폐쇄망 내 수동 반입 필요 → 지연 발생 | 통제된 경로로 자동화 가능 |
| **규제 적용** | CSAP 상 등급, 일부 금융 핵심 시스템 | CSAP 중/하 등급, 대부분의 클라우드 워크로드 |

### 물리적 망분리의 현실적 한계

물리적 망분리가 "절대 안전"을 보장하지는 않습니다.

- **패치 지연**: 폐쇄망은 인터넷 접근이 불가하여 보안 패치 적용이 수 주~수 개월 지연됩니다. 이 기간 동안 알려진 취약점에 노출됩니다.
- **내부자 위협**: 물리적 분리는 외부 공격을 차단하지만, 내부 권한을 가진 사용자의 데이터 유출은 막지 못합니다.
- **운영 복잡성**: 이중 단말, 망간 자료전송 시스템, 별도 인증 체계 등 운영 부담이 큽니다.
- **DR 제약**: 폐쇄망 환경에서 원격지 DR 구성이 어렵습니다.

## 클라우드에서의 네트워크 격리 구현

클라우드는 소프트웨어 정의 네트워크(SDN)를 기반으로 하므로, 물리적 장비 없이도 강력한 격리를 구현할 수 있습니다.

### 격리 수준별 구현 패턴

| 격리 수준 | 구현 방법 | 적합한 경우 |
| --- | --- | --- |
| **VPC/VNet 분리** | 워크로드별 독립 VPC, 라우팅 차단 | 일반적인 환경 분리 (dev/prod) |
| **프라이빗 서브넷** | 인터넷 게이트웨이 없는 서브넷, NAT 경유만 허용 | DB, 내부 API 등 외부 노출 불필요 시스템 |
| **VPC Endpoint / Private Link** | AWS 서비스 접근을 VPC 내부 경로로 한정 | S3, RDS 등 관리형 서비스 접근 시 인터넷 우회 |
| **전용선 (Direct Connect / ExpressRoute / Interconnect)** | 인터넷을 경유하지 않는 전용 네트워크 연결 | 온프레미스↔클라우드 간 통신 |
| **에어갭 (Air-gapped)** | 인터넷과 완전히 단절된 클라우드 환경 | 최고 수준 규제 (국방, 정보기관) |

### 벤더별 에어갭/전용 환경

인터넷과 완전히 분리된 클라우드 환경이 필요한 경우, 각 벤더는 다음 옵션을 제공합니다.

| 벤더 | 서비스 | 설명 |
| --- | --- | --- |
| AWS | Outposts | 고객 데이터센터에 AWS 인프라 설치. 로컬 처리 |
| AWS | Snow Family (Snowball Edge) | 완전 오프라인 환경에서 컴퓨팅/스토리지 제공 |
| Azure | Azure Stack Hub / HCI | 고객 DC에서 Azure 서비스 운영. 연결/비연결 모드 |
| Azure | Azure Government (격리 리전) | 미국 정부 전용 물리적 분리 리전 |
| GCP | Google Distributed Cloud (GDC) Air-gapped | 완전 오프라인 환경에서 GCP 서비스 운영 |
| OCI | Dedicated Region | 고객 DC에 OCI 전체 리전 설치. 완전 격리 |
| OCI | Roving Edge Infrastructure | 오프라인 환경용 이동식 컴퓨팅 |

### 일반적인 규제 시장 아키텍처 패턴

대부분의 금융/공공 워크로드는 에어갭까지 필요하지 않으며, 다음 패턴으로 규제 요건을 충족합니다.

```text
┌─────────────────────────────────────────────────┐
│  VPC (프로덕션)                                    │
│  ┌──────────────┐  ┌──────────────┐              │
│  │ Public Subnet │  │ Private Subnet│              │
│  │ (ALB/WAF만)  │  │ (앱/DB/내부API)│              │
│  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                      │
│         │    Security Group + NACL                │
│         │    (최소 권한 인바운드)                    │
│         │                  │                      │
│  ┌──────┴──────────────────┴───────┐             │
│  │       VPC Endpoint (S3, KMS 등)  │             │
│  └──────────────────────────────────┘             │
└─────────────────────┬───────────────────────────┘
                      │ 전용선 (Direct Connect 등)
              ┌───────┴───────┐
              │  온프레미스 DC  │
              └───────────────┘
```

**핵심 원칙:**

- 인터넷 노출 최소화 — Public Subnet에는 로드밸런서/WAF만 배치
- 관리형 서비스 접근은 VPC Endpoint 경유 — NAT Gateway/인터넷 우회
- 온프레미스 연결은 전용선 — VPN은 백업 경로로만 사용
- 모든 통신 암호화 — TLS 1.2+ 필수

## 규제 요건 매핑

| 규제/기준 | 요구사항 | 클라우드 대응 |
| --- | --- | --- |
| **전자금융감독규정** (금융) | 전산실 망분리, 내부망/DMZ/외부망 구분 | VPC 분리 + Private Subnet + 전용선 |
| **CSAP 상 등급** (공공) | 물리적 망분리 | Outposts, Azure Stack, GDC Air-gapped, Dedicated Region |
| **CSAP 중 등급** (공공) | 논리적 망분리 + 접근 통제 강화 | VPC 격리 + Private Link + 전용선 |
| **ISMS-P** (전 산업) | 네트워크 분리, 접근 통제, 암호화 | Security Group + NACL + VPC Endpoint + TLS |
| **N2SF (국가망보안체계)** | 등급별 차등 보안 (기밀/민감/공개) | 등급별 VPC 분리 + 등급 간 통신 통제 |
| **PCI DSS** (카드 결제) | CDE(카드 데이터 환경) 네트워크 격리 | 전용 VPC + 방화벽 + 로깅 |

## 안티패턴

| 안티패턴 | 문제 | 올바른 접근 |
| --- | --- | --- |
| 모든 서브넷을 Public으로 구성 | 모든 리소스가 인터넷에 노출 | Private Subnet 기본, Public은 LB/Bastion만 |
| Security Group에 0.0.0.0/0 인바운드 허용 | 사실상 방화벽 없음 | 최소 권한 원칙, 필요한 포트/소스만 허용 |
| NAT Gateway로 모든 아웃바운드 허용 | 데이터 유출 경로 존재 | VPC Endpoint 우선, 아웃바운드도 제한 |
| 망분리만 하고 내부 모니터링 없음 | 내부 횡이동 탐지 불가 | VPC Flow Logs + 이상 탐지 + Network Policy |
| 물리적 망분리 후 패치 방치 | 알려진 취약점에 장기 노출 | 통제된 패치 경로 확보, 정기 취약점 스캔 |

## 체크리스트

- [ ] 워크로드 등급에 따라 VPC/서브넷 분리 전략을 수립했는가
- [ ] 인터넷 노출이 필요한 리소스를 최소화했는가 (Public Subnet 최소화)
- [ ] 관리형 서비스 접근에 VPC Endpoint / Private Link를 사용하는가
- [ ] 온프레미스 연결에 전용선을 사용하는가 (VPN은 백업만)
- [ ] Security Group / NACL에 최소 권한 원칙을 적용했는가
- [ ] VPC Flow Logs를 활성화하고 이상 탐지를 구성했는가
- [ ] 아웃바운드 트래픽도 제한하고 있는가 (데이터 유출 방지)
- [ ] 규제 요건에 맞는 격리 수준을 선택했는가 (논리적 vs 물리적)
- [ ] 폐쇄망 환경에서도 패치 적용 경로를 확보했는가

## 관련 문서

{% content-ref url="zero-trust.md" %}
[제로 트러스트](zero-trust.md)
{% endcontent-ref %}

{% content-ref url="../networking/vpc-subnet.md" %}
[VPC와 서브넷](../networking/vpc-subnet.md)
{% endcontent-ref %}

{% content-ref url="../governance/compliance.md" %}
[컴플라이언스](../governance/compliance.md)
{% endcontent-ref %}

## 참고하기

### 규제/표준

- [전자금융감독규정 (금융위원회)](https://www.law.go.kr/행정규칙/전자금융감독규정)
- [CSAP 클라우드 보안인증 (KISA)](https://isms.kisa.or.kr/main/csap/intro/)
- [N2SF 국가망보안체계 (국가정보원)](https://www.nis.go.kr)
- [PCI DSS v4.0 (PCI SSC)](https://www.pcisecuritystandards.org/)

### AWS

- [VPC 보안 모범사례](https://docs.aws.amazon.com/ko_kr/vpc/latest/userguide/vpc-security-best-practices.html)
- [AWS PrivateLink 문서](https://docs.aws.amazon.com/ko_kr/vpc/latest/privatelink/)
- [AWS Outposts 문서](https://docs.aws.amazon.com/ko_kr/outposts/)

### Azure

- [Azure 네트워크 보안 모범사례](https://learn.microsoft.com/ko-kr/azure/security/fundamentals/network-best-practices)
- [Azure Private Link 문서](https://learn.microsoft.com/ko-kr/azure/private-link/)
- [Azure Stack Hub 문서](https://learn.microsoft.com/ko-kr/azure-stack/operator/)

### GCP

- [VPC 보안 모범사례](https://cloud.google.com/architecture/framework/security/network-security)
- [Private Google Access 문서](https://cloud.google.com/vpc/docs/private-google-access)
- [Google Distributed Cloud 문서](https://cloud.google.com/distributed-cloud/hosted/docs)

### OCI

- [OCI 네트워크 보안 모범사례](https://docs.oracle.com/en-us/iaas/Content/Security/Reference/networking_security.htm)
- [OCI Dedicated Region 문서](https://docs.oracle.com/en-us/iaas/Content/dedicated-region/home.htm)
