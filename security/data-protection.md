---
description: 전송 중/저장 시 암호화, WAF, 네트워크 보안을 벤더별로 비교합니다.
---

# 데이터 보호와 워크로드 보안

> 문서 기준: 2026년 5월

## 개요

클라우드 보안은 크게 세 가지 영역으로 나뉩니다.

- **전송 중 보안 (In Transit)** — 네트워크를 통해 이동하는 데이터 보호
- **저장 시 보안 (At Rest)** — 스토리지/DB에 저장된 데이터 보호
- **워크로드 보안** — 실행 중인 서버/컨테이너/애플리케이션 보호

## 전송 중 보안 (Encryption in Transit)

데이터가 네트워크를 이동할 때 도청이나 변조를 방지합니다.

| 구간 | 방법 | 비고 |
| --- | --- | --- |
| **사용자 ↔ 서비스** | TLS/HTTPS | CDN, LB에서 TLS 종료. 무료 인증서 제공 (ACM, Let's Encrypt 등) |
| **서비스 ↔ 서비스** | mTLS, VPC 내부 통신 | 서비스 메시(Istio, App Mesh)로 자동 mTLS |
| **리전 ↔ 리전** | 벤더 백본 암호화 | AWS/Azure/Google Cloud 모두 리전 간 트래픽 자동 암호화 |
| **온프레미스 ↔ 클라우드** | VPN (IPsec) / 전용선 | Direct Connect, ExpressRoute, Cloud Interconnect |

각 벤더 모두 관리형 서비스 간 통신은 기본적으로 TLS로 암호화됩니다.

## 저장 시 보안 (Encryption at Rest)

저장된 데이터가 물리적으로 탈취되어도 읽을 수 없도록 암호화합니다.

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **기본 암호화** | 대부분 서비스 기본 활성화 (S3, EBS 등) | 모든 서비스 기본 활성화 | 모든 데이터 기본 암호화 | 모든 데이터 기본 암호화 |
| **키 관리** | KMS (벤더 관리 키 / 고객 관리 키) | Key Vault | Cloud KMS | OCI Vault |
| **고객 키** (CMK/CMEK) | KMS Customer Managed Key | Key Vault Customer Key | Cloud KMS CMEK | Vault Customer Managed Key |
| **자체 키** (BYOK) | KMS External Key Store | Key Vault BYOK | Cloud External Key Manager (EKM) | Vault BYOK |
| **HSM** | CloudHSM | Managed HSM | Cloud HSM | Vault HSM 키 |

키 관리 수준에 따라 보안과 운영 복잡도가 달라집니다:

- **벤더 관리 키** — 가장 간단. 벤더가 키 생성/교체/관리. 대부분의 워크로드에 적합.
- **고객 관리 키** (CMK) — 키 교체 주기, 접근 정책을 직접 제어. 규제 요건 충족.
- **자체 키** (BYOK/EKM) — 키를 온프레미스 HSM에서 관리. 가장 엄격한 규제 대응.

## 워크로드 보안

실행 중인 인프라와 애플리케이션을 보호합니다.

### 네트워크 보안

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Security Groups, Network ACL, Network Firewall | SG: 인스턴스 단위. Network Firewall: VPC 단위 IDS/IPS |
| Azure | NSG, Azure Firewall | Azure Firewall: L7 필터링 + 위협 인텔리전스 |
| Google Cloud | Firewall Rules, Cloud Armor | Cloud Armor: DDoS 방어 + WAF |
| OCI | Security Lists, NSG, OCI Network Firewall | Network Firewall: L7 IDS/IPS |

### 웹 애플리케이션 방화벽 (WAF)

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | [AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html) | ALB/CloudFront/API Gateway에 연결. 관리형 규칙 + 커스텀 규칙 |
| Azure | [Azure WAF](https://learn.microsoft.com/azure/web-application-firewall/overview) (Front Door / App Gateway) | OWASP CRS 3.2 기본 제공. 정책 기반 관리 |
| Google Cloud | [Cloud Armor](https://cloud.google.com/armor/docs) | DDoS + WAF 통합. 사전 구성된 WAF 규칙 + 적응형 보호(ML) |
| OCI | [OCI WAF](https://docs.oracle.com/en-us/iaas/Content/WAF/home.htm) | Load Balancer/Edge 연동. OWASP 규칙 세트 제공 |

#### OWASP와 WAF 규칙

[OWASP Top 10](https://owasp.org/www-project-top-ten/)은 웹 애플리케이션의 가장 흔한 보안 위협을 정리한 업계 표준입니다. 각 벤더의 WAF는 이 위협에 대응하는 **관리형 규칙 세트**를 제공합니다.

아래는 OWASP Top 10 중 **WAF 규칙으로 완화 가능한 주요 항목**을 발췌한 것입니다:

| OWASP Top 10 위협 | WAF 규칙 대응 | 벤더별 관리형 규칙 |
| --- | --- | --- |
| A01 — Broken Access Control | 경로 탐색, 강제 브라우징 차단 | AWS Managed Rules (Core), Azure CRS, Cloud Armor 사전 구성 규칙 |
| A03 — Injection (SQL/XSS) | SQL Injection, XSS 패턴 매칭 | AWS SQLi/XSS Rule Group, Azure CRS, Cloud Armor `sqli-v33-stable` |
| A05 — Security Misconfiguration | 알려진 취약 경로 차단 | AWS Known Bad Inputs, Azure CRS |
| A06 — Vulnerable Components | 알려진 CVE 익스플로잇 차단 | AWS Managed Rules (CVE), Azure Bot Manager |
| A07 — Authentication Failures | 브루트포스, 크리덴셜 스터핑 차단 | AWS Account Takeover Prevention, Azure Rate Limiting |

#### 관리형 규칙 vs 커스텀 규칙

| 구분 | 관리형 규칙 (Managed Rules) | 커스텀 규칙 |
| --- | --- | --- |
| **관리 주체** | 벤더 또는 보안 파트너가 업데이트 | 사용자가 직접 작성·유지 |
| **적합한 경우** | OWASP Top 10 기본 방어, 빠른 적용 | 애플리케이션 특화 로직, 비즈니스 규칙 |
| **업데이트** | 새 위협 발견 시 벤더가 자동 업데이트 | 사용자가 직접 업데이트 |
| **비용** | 규칙 그룹당 과금 (AWS), 기본 포함 (Azure/Google Cloud/OCI) | 규칙 수에 따라 과금 |

**실무 권장:**

- **1단계** — 관리형 OWASP 규칙 세트를 먼저 적용 (Count 모드로 시작하여 오탐 확인 후 Block 전환)
- **2단계** — 애플리케이션 특화 커스텀 규칙 추가 (특정 API 경로 보호, 지역 기반 차단 등)
- **3단계** — Rate Limiting 규칙으로 DDoS/브루트포스 완화
- **로깅** — WAF 로그를 S3/Log Analytics/Cloud Logging에 저장하여 공격 패턴 분석

위협 탐지(GuardDuty, Defender, SCC, Cloud Guard)와 컨테이너/런타임 보안(Inspector, Defender for Containers 등)은 [보안 태세 관리](security-posture.md)에서 상세히 다룹니다.

## 관련 문서

{% content-ref url="security-posture.md" %}
[보안 태세 관리](security-posture.md)
{% endcontent-ref %}

{% content-ref url="secrets.md" %}
[시크릿 관리](secrets.md)
{% endcontent-ref %}

{% content-ref url="iam.md" %}
[IAM 실무 설계와 보안 운영](iam.md)
{% endcontent-ref %}

{% content-ref url="../networking/vpc-subnet.md" %}
[VPC와 서브넷](../networking/vpc-subnet.md)
{% endcontent-ref %}

## 참고하기

### AWS

- [AWS 보안 문서](https://docs.aws.amazon.com/ko_kr/security/)
- [AWS KMS 문서](https://docs.aws.amazon.com/ko_kr/kms/)
- [AWS WAF 문서](https://docs.aws.amazon.com/ko_kr/waf/)

### Azure

- [Azure 보안 문서](https://learn.microsoft.com/ko-kr/azure/security/)
- [Azure Key Vault 문서](https://learn.microsoft.com/ko-kr/azure/key-vault/)
- [Azure WAF 문서](https://learn.microsoft.com/ko-kr/azure/web-application-firewall/)

### Google Cloud

- [Google Cloud 보안 문서](https://cloud.google.com/security)
- [Cloud KMS 문서](https://cloud.google.com/kms/docs)
- [Cloud Armor 문서](https://cloud.google.com/armor/docs)

### OCI

- [OCI Vault 문서](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/home.htm)
- [OCI WAF 문서](https://docs.oracle.com/en-us/iaas/Content/WAF/home.htm)
