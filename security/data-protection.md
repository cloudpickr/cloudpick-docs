---
description: 전송 중/저장 시 암호화, WAF, 위협 탐지, 컨테이너 보안을 4사 비교합니다.
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
| **리전 ↔ 리전** | 벤더 백본 암호화 | AWS/Azure/GCP 모두 리전 간 트래픽 자동 암호화 |
| **온프레미스 ↔ 클라우드** | VPN (IPsec) / 전용선 | Direct Connect, ExpressRoute, Cloud Interconnect |

각 벤더 모두 관리형 서비스 간 통신은 기본적으로 TLS로 암호화됩니다.

## 저장 시 보안 (Encryption at Rest)

저장된 데이터가 물리적으로 탈취되어도 읽을 수 없도록 암호화합니다.

| 항목 | AWS | Azure | GCP | OCI |
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
| GCP | Firewall Rules, Cloud Armor | Cloud Armor: DDoS 방어 + WAF |
| OCI | Security Lists, NSG, OCI Network Firewall | Network Firewall: L7 IDS/IPS |

### 웹 애플리케이션 방화벽 (WAF)

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | AWS WAF | ALB/CloudFront/API Gateway에 연결. 관리형 규칙 제공 |
| Azure | Azure WAF (Front Door / App Gateway) | OWASP 규칙 세트 기본 제공 |
| GCP | Cloud Armor | DDoS + WAF 통합. 적응형 보호 |
| OCI | OCI WAF | Load Balancer 연동. OWASP 규칙 세트 제공 |

### 위협 탐지

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | GuardDuty | 계정/네트워크/S3 위협 자동 탐지. ML 기반 |
| AWS | Security Hub | 보안 상태 통합 대시보드. 규정 준수 점검 |
| Azure | Microsoft Defender for Cloud | CSPM + CWPP. 멀티클라우드 지원 |
| GCP | Security Command Center | 취약점, 위협, 구성 오류 통합 탐지 |
| OCI | OCI Cloud Guard | 구성 오류 탐지 + 자동 교정. Security Zones로 정책 강제 |

### 컨테이너/런타임 보안

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Inspector | EC2/ECR/Lambda 취약점 자동 스캔 |
| Azure | Defender for Containers | 이미지 스캔 + 런타임 보호 |
| GCP | Container Threat Detection | GKE 런타임 위협 탐지 |
| OCI | OCI Vulnerability Scanning | Compute/Container 이미지 취약점 스캔 |

## 관련 문서

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
- [Amazon GuardDuty 문서](https://docs.aws.amazon.com/ko_kr/guardduty/)
- [AWS WAF 문서](https://docs.aws.amazon.com/ko_kr/waf/)
- [AWS Security Hub 문서](https://docs.aws.amazon.com/ko_kr/securityhub/)

### Azure

- [Azure 보안 문서](https://learn.microsoft.com/ko-kr/azure/security/)
- [Azure Key Vault 문서](https://learn.microsoft.com/ko-kr/azure/key-vault/)
- [Microsoft Defender for Cloud](https://learn.microsoft.com/ko-kr/azure/defender-for-cloud/)
- [Azure WAF 문서](https://learn.microsoft.com/ko-kr/azure/web-application-firewall/)

### GCP

- [Google Cloud 보안 문서](https://cloud.google.com/security/docs)
- [Cloud KMS 문서](https://cloud.google.com/kms/docs)
- [Security Command Center 문서](https://cloud.google.com/security-command-center/docs)
- [Cloud Armor 문서](https://cloud.google.com/armor/docs)

### OCI

- [OCI Cloud Guard 문서](https://docs.oracle.com/en-us/iaas/cloud-guard/home.htm)
- [OCI Security Zones 문서](https://docs.oracle.com/en-us/iaas/security-zone/home.htm)
- [OCI Vault 문서](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/home.htm)
- [OCI WAF 문서](https://docs.oracle.com/en-us/iaas/Content/WAF/home.htm)
