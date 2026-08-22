---
title: "데이터 보호와 워크로드 보안"
description: "전송 중/저장 시 암호화, WAF, 네트워크 보안을 벤더별로 비교합니다."
---

> 문서 기준: 2026년 8월

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

저장된 데이터가 물리적으로 탈취되어도 읽을 수 없도록 암호화합니다. 모든 주요 CSP는 기본 암호화를 제공하며, 키 관리 수준에 따라 보안과 운영 복잡도가 달라집니다:

- **벤더 관리 키** — 가장 간단. 벤더가 키 생성/교체/관리. 대부분의 워크로드에 적합.
- **고객 관리 키** (CMK) — 키 교체 주기, 접근 정책을 직접 제어. 규제 요건 충족.
- **자체 키** (BYOK/EKM/HYOK) — 키를 온프레미스 HSM에서 관리. 가장 엄격한 규제 대응.

:::note
벤더별 KMS 서비스 비교, CMK/BYOK/EKM 상세, HSM 옵션은 [시크릿 관리 — 암호화 키 관리 모델](../../security/secrets/)을 참고하세요.
:::

## 양자내성 암호화 (Post-Quantum Cryptography)

:::note
**이 섹션이 필요한 독자:** 10년 이상 보관하는 민감 데이터(금융, 의료, 공공)가 있거나, 규제 기관이 PQC 전환 로드맵을 요구하는 조직. 단기 보관 데이터만 다루는 경우 당장의 조치보다는 동향 파악 수준으로 읽으세요.
:::

오늘날 HTTPS, VPN, 데이터 암호화에 사용되는 RSA, ECDH 등의 알고리즘은 양자 컴퓨터가 충분히 커지면 깨질 수 있습니다. 문제는 양자 컴퓨터가 나온 "뒤"가 아니라 "지금"입니다. 공격자가 암호화된 트래픽을 지금 수집해두고, 양자 컴퓨터가 나온 후 복호화하는 **Harvest Now, Decrypt Later** 공격이 이미 가능하기 때문입니다.

이에 대응하여 NIST가 새로운 암호화 표준을 확정했고, 주요 클라우드 벤더가 전환을 시작했습니다.

### NIST PQC 표준

| 표준 | 용도 | 알고리즘 | 상태 |
| --- | --- | --- | --- |
| **FIPS 203** (ML-KEM) | 키 교환 | Kyber 기반 격자 암호 | 2024.8 최종 확정 |
| **FIPS 204** (ML-DSA) | 디지털 서명 | Dilithium 기반 격자 암호 | 2024.8 최종 확정 |
| **FIPS 205** (SLH-DSA) | 디지털 서명 (상태 비저장) | SPHINCS+ 기반 해시 서명 | 2024.8 최종 확정 |
| **HQC** | 백업 KEM | 코드 기반 암호 | 2025.3 선정 |

### 벤더별 PQC 전환 현황

| 벤더 | 현황 | 참고 |
| --- | --- | --- |
| AWS | KMS에서 ML-KEM 하이브리드 TLS 지원. S3, ACM 등 서비스 간 통신에 PQ 하이브리드 키 교환 적용 중 | [AWS Post-Quantum Cryptography](https://aws.amazon.com/security/post-quantum-cryptography/) |
| Azure | Microsoft Quantum Safe Program. SymCrypt 라이브러리에 ML-KEM/ML-DSA 구현. TLS 1.3 하이브리드 키 교환 지원 | [Microsoft Quantum Safe](https://www.microsoft.com/en-us/security/blog/topic/quantum-safe/) |
| Google Cloud | Cloud KMS에서 PQC 디지털 서명(ML-DSA) 프리뷰. Chrome/BoringSSL에 ML-KEM 하이브리드 배포 완료 | [Google Cloud PQC](https://cloud.google.com/blog/products/identity-security/quantum-safe-digital-signatures-in-cloud-kms) |
| OCI | OCI Vault 등에서 PQC 알고리즘 로드맵을 발표. Oracle Database TLS 하이브리드 모드 등은 공식 로드맵·릴리스 노트 기준으로 확인 (구체 제품 문서가 공개되면 링크로 교체) | [Oracle Security](https://www.oracle.com/security/) (일반 허브; PQC 전용 페이지는 공식 문서 확인) |

### PQC 전환 전략

1. **인벤토리** — 사용 중인 암호화 알고리즘, 인증서, 키 크기를 식별합니다 (Crypto Agility Inventory)
2. **하이브리드 모드** — 기존 알고리즘 + PQC 알고리즘을 동시에 사용하여 호환성을 유지하면서 전환합니다
3. **우선순위** — 장기 보관 데이터(10년+ 수명)와 서명 인프라부터 전환합니다
4. **테스트** — PQC 알고리즘은 키/서명 크기가 크므로 네트워크 오버헤드와 핸드셰이크 지연을 측정합니다

:::caution
PQC 전환은 수년이 걸리는 프로젝트입니다. 지금 당장 모든 시스템을 바꿀 필요는 없지만, **암호 민첩성(Crypto Agility)** 을 확보하여 알고리즘을 교체할 수 있는 아키텍처를 미리 갖추는 것이 핵심입니다.
:::

## 기밀 컴퓨팅 (Confidential Computing)

기존 암호화가 "저장 시"와 "전송 중"을 보호한다면, 기밀 컴퓨팅은 **"사용 중(In Use)"** 데이터를 보호합니다. 하드웨어 기반의 신뢰 실행 환경(TEE)에서 데이터를 처리하여, 클라우드 벤더의 관리자조차 처리 중인 데이터에 접근할 수 없습니다.

| 벤더 | 제품 | GPU 기밀 컴퓨팅 | 참고 |
| --- | --- | --- | --- |
| AWS | [Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/) | — (Nitro 아키텍처 자체가 하이퍼바이저 격리) | [AWS Nitro](https://aws.amazon.com/ec2/nitro/) |
| Azure | [Confidential VMs (AMD SEV-SNP, Intel TDX)](https://learn.microsoft.com/azure/confidential-computing/) | **NCC H100 v5** — NVIDIA H100 기밀 GPU | [Azure Confidential Computing](https://azure.microsoft.com/solutions/confidential-compute/) |
| Google Cloud | [Confidential VMs (AMD SEV, Intel TDX)](https://cloud.google.com/confidential-computing) | **A3 Confidential VM** — H100 기밀 GPU | [GCP Confidential Computing](https://cloud.google.com/confidential-computing/docs) |
| OCI | [Confidential Computing (AMD SEV)](https://docs.oracle.com/en-us/iaas/Content/Compute/References/confidential-compute.htm) | — | [OCI Compute](https://docs.oracle.com/en-us/iaas/Content/Compute/home.htm) |

**주요 활용 사례:**
- AI/ML 추론에서 모델 IP와 입력 데이터 동시 보호 (기밀 GPU)
- 멀티파티 데이터 분석 — 원본 데이터를 공개하지 않고 공동 연산
- 데이터 주권이 엄격한 워크로드 (소버린 클라우드 + 기밀 컴퓨팅 조합)

:::note
기밀 컴퓨팅을 활용한 AI 워크로드 보호는 [AI 보안 — 기밀 AI 추론](../../security/ai-security/)을, 데이터 주권 관련 소버린 클라우드는 [랜딩존 — 소버린 랜딩존](../../governance/landing-zone/#소버린-랜딩존-sovereign-landing-zone)을 참고하세요.
:::

## 워크로드 보안

실행 중인 인프라와 애플리케이션을 보호합니다.

### 네트워크 보안

전송 중인 데이터를 보호하려면 네트워크 수준의 접근 제어가 필수적입니다.

:::note
Security Groups/NSG/Firewall Rules 등 네트워크 방화벽의 벤더별 비교는 [VPC와 서브넷](../../networking/vpc-subnet/)을, 네트워크 격리 아키텍처 패턴(Air-gap, 예방적 가드레일)은 [망분리와 네트워크 격리](../../security/network-isolation/)를 참고하세요.
:::

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

위협 탐지(GuardDuty, Defender, SCC, Cloud Guard)와 컨테이너/런타임 보안(Inspector, Defender for Containers 등)은 [보안 태세 관리](../../security/security-posture/)에서 상세히 다룹니다.

## 자주 하는 실수

- **WAF를 Block 모드로 바로 적용** — 오탐(False Positive)을 확인하지 않고 차단 모드로 전환하여 정상 트래픽이 차단됨. Count 모드로 먼저 검증해야 함
- **벤더 관리 키로 충분한데 BYOK를 도입** — 규제 요건 없이 자체 키 관리를 선택하여 운영 복잡도와 장애 위험만 증가
- **VPC Endpoint 없이 관리형 서비스 접근** — S3, KMS 등을 NAT Gateway 경유로 접근하여 불필요한 인터넷 노출과 비용 발생
- **PQC 전환을 "양자 컴퓨터 등장 후"로 미루기** — Harvest Now, Decrypt Later 공격에 이미 노출 중. 장기 보관 데이터는 지금부터 하이브리드 모드 적용 필요

## 체크리스트

- [ ] 저장 시 암호화가 모든 스토리지/DB에 활성화되어 있는가 (기본 암호화 확인)
- [ ] WAF 관리형 규칙을 Count 모드로 먼저 적용하고 오탐을 확인한 후 Block으로 전환했는가
- [ ] 관리형 서비스(S3, KMS 등) 접근에 VPC Endpoint / Private Link를 사용하는가
- [ ] 사용 중인 암호화 알고리즘을 인벤토리하고 PQC 전환 로드맵을 수립했는가
- [ ] 민감 AI 추론 워크로드에 기밀 컴퓨팅 적용을 검토했는가

## 관련 문서

- [보안 태세 관리](../../security/security-posture/)
- [시크릿 관리](../../security/secrets/)
- [IAM 실무 설계와 보안 운영](../../security/iam/)
- [VPC와 서브넷](../../networking/vpc-subnet/)

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

### 양자내성 암호화 / 기밀 컴퓨팅

- [NIST FIPS 203 — ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- [NIST FIPS 204 — ML-DSA](https://csrc.nist.gov/pubs/fips/204/final)
- [AWS Post-Quantum Cryptography](https://aws.amazon.com/security/post-quantum-cryptography/)
- [Azure Confidential Computing](https://learn.microsoft.com/azure/confidential-computing/)
- [Google Cloud Confidential Computing](https://cloud.google.com/confidential-computing)
