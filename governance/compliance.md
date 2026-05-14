---
description: 한국 ISMS-P, CSAP와 글로벌 ISO 27001, SOC 2 등 클라우드 규정 준수 인증을 벤더별로 안내합니다.
---

# 규정 준수 (Compliance)

> 문서 기준: 2026년 5월

## 개요

클라우드에서 규정 준수는 **공동 책임 모델** 에 따라 벤더와 사용자가 책임을 나눕니다. 벤더는 인프라 계층의 보안 통제를 인증받고, 사용자는 자신의 워크로드 구성이 규제 요건을 충족하도록 관리합니다.

{% hint style="info" %}
공동 책임 모델의 개념적 배경은 [공동 책임 모델](../about-cloud/shared-responsibility.md)
{% endhint %}

{% hint style="warning" %}
**인증은 전제조건일 뿐 보증이 아닙니다.** 벤더가 ISMS-P나 CSAP 인증을 가지고 있어도, 사용자가 구성한 VPC, IAM, 암호화 설정이 규제 요건을 충족하지 않으면 감사에서 문제가 됩니다.
{% endhint %}

## 한국 주요 인증

### ISMS-P (정보보호 및 개인정보보호 관리체계 인증)

- **근거 법률**: 정보통신망법, 개인정보 보호법
- **운영**: [KISA (한국인터넷진흥원)](https://isms.kisa.or.kr/)
- **대상**: 매출액 1,500억 원 이상 또는 일평균 이용자 100만 명 이상 등 일정 규모 이상의 정보통신 서비스 제공자
- **유효 기간**: 3년, 연 1회 사후 심사
- **클라우드 영향**: 클라우드에 민감 정보를 저장·처리하는 경우, 벤더의 ISMS-P 인증 범위 내 리전을 사용해야 함

공식 벤더별 페이지:

- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms)
- [GCP K-ISMS](https://cloud.google.com/security/compliance/k-isms)
- OCI: 공식 컴플라이언스 페이지에서 인증 현황 확인

### CSAP (클라우드 보안 인증제)

- **근거 법률**: 클라우드 컴퓨팅 발전법 제23조의2
- **운영**: [KISA](https://isms.kisa.or.kr/main/csap/intro/)
- **대상**: 공공기관에 클라우드 서비스를 제공하려는 모든 CSP
- **등급 체계** (2024년 상·중·하 등급제 전면 시행):

| 등급 | 대상 시스템 | 요구 수준 |
| --- | --- | --- |
| **상** | 민감 정보 처리 (주민등록번호 등 고유식별정보 포함) | 물리적 망 분리, 국내 리전, 국내 인력 운영 등 엄격 |
| **중** | 일반 행정 업무 시스템 | 상 등급 대비 완화 |
| **하** | 중요도 낮은 시스템 (글로벌 CSP 진입 가능) | 최소 보안 요건 |

**글로벌 CSP의 CSAP 인증 현황 (2025년 기준):**

| 벤더 | 등급 | 리전 | 참고 |
| --- | --- | --- | --- |
| AWS | 하 (Low-tier) | 서울 `ap-northeast-2` | [AWS CSAP 공지](https://aws.amazon.com/blogs/security/aws-achieves-cloud-security-assurance-program-csap-low-tier-certification-in-aws-seoul-region/) |
| Azure | 하 (Low-tier) | Korea Central / South | [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap) |
| GCP | 하 (Low-tier) | Seoul `asia-northeast3` | [GCP CSAP](https://cloud.google.com/security/compliance/csap) |
| OCI | — (공식 페이지 확인) | Seoul, Chuncheon | [Oracle 컴플라이언스](https://www.oracle.com/corporate/cloud-compliance/) |

{% hint style="info" %}
CSAP 제도는 국정원 보안적합성 검증과의 통합, N2SF(국가망보안체계) 연계 등 제도 변화가 논의 중입니다. 도입 전 [KISA 공식 사이트](https://isms.kisa.or.kr/main/csap/intro/)에서 최신 현황을 확인하세요.
{% endhint %}

### 금융권 관련 규제

금융 분야는 추가 규제가 적용됩니다.

- **전자금융거래법 / 전자금융감독규정** — 금융회사의 클라우드 이용 시 안전성 확보 요건
- **금융보안원 (FSI)** — 금융권 클라우드 이용 가이드 발간, 보안 컨설팅 제공
- **망분리 규제** — 개인신용정보 처리 시스템은 일반 업무망과 분리 운영 필요 (완화 논의 중)

공식 자료:

- [금융보안원 클라우드 이용 가이드](https://www.fsec.or.kr/) (통합 인덱스 활용)
- [금융위원회](https://www.fsc.go.kr/)

## 국제 주요 인증

### ISO/IEC 27001 — 정보보호 관리체계

국제 표준의 정보보안 관리 체계. 대부분의 글로벌 CSP가 기본으로 보유합니다.

- [AWS ISO 27001](https://aws.amazon.com/compliance/iso-27001-faqs/)
- [Azure ISO 27001](https://learn.microsoft.com/azure/compliance/offerings/offering-iso-27001)
- [GCP ISO 27001](https://cloud.google.com/security/compliance/iso-27001)
- [Oracle ISO 27001](https://www.oracle.com/corporate/cloud-compliance/)

### SOC 1 / SOC 2 / SOC 3

AICPA(미국 공인회계사 협회) 기반 감사 보고서. 엔터프라이즈 고객이 자주 요구합니다.

- **SOC 1** — 재무 보고 통제
- **SOC 2** — 보안, 가용성, 처리 무결성, 기밀성, 개인정보 보호
- **SOC 3** — SOC 2 요약 공개 보고서

각 벤더의 SOC 보고서는 **기밀 자료** 이므로 고객 계약 후 AWS Artifact, Azure Service Trust Portal 등을 통해 다운로드합니다.

### 산업별 규제

| 산업 | 주요 규제 | 적용 지역 |
| --- | --- | --- |
| **의료** | HIPAA, HITRUST | 미국 |
| **카드결제** | PCI DSS | 글로벌 |
| **공공 (미국)** | FedRAMP | 미국 연방 |
| **공공 (EU)** | C5 (독일), ENS (스페인) 등 | EU |
| **개인정보 (EU)** | GDPR | EU |

각 벤더의 해당 인증 현황은 **AWS Compliance Programs**, **Azure Trust Center**, **GCP Compliance**, **Oracle Cloud Compliance** 페이지에서 확인합니다.

## 벤더별 컴플라이언스 허브

인증 현황 전체 목록과 보고서 접근 방법은 각 벤더 공식 허브에서 관리됩니다.

| 벤더 | 허브 |
| --- | --- |
| AWS | [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/), [AWS Artifact (보고서)](https://aws.amazon.com/artifact/) |
| Azure | [Microsoft Trust Center](https://www.microsoft.com/trust-center), [Service Trust Portal](https://servicetrust.microsoft.com/) |
| GCP | [GCP Compliance Resource Center](https://cloud.google.com/security/compliance), [Google Compliance Reports Manager](https://cloud.google.com/security/compliance/compliance-reports-manager) |
| OCI | [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/) |

## 클라우드에서 규정 준수를 어떻게 운영하는가

인증 자체보다 **일상 운영에서 통제를 어떻게 유지하는가**가 감사의 핵심입니다.

### 1. 가드레일 자동화

수동 관리는 누락이 발생하므로 정책을 IaC로 코드화합니다.

| 벤더 | 도구 |
| --- | --- |
| AWS | [AWS Config](https://aws.amazon.com/config/), [AWS Security Hub](https://aws.amazon.com/security-hub/), SCP (Service Control Policy) |
| Azure | [Azure Policy](https://learn.microsoft.com/azure/governance/policy/overview), [Microsoft Defender for Cloud](https://azure.microsoft.com/products/defender-for-cloud) |
| GCP | [Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/overview), [Security Command Center](https://cloud.google.com/security-command-center) |
| OCI | [OCI Security Zones](https://docs.oracle.com/en-us/iaas/Content/security-zone/home.htm), [OCI Cloud Guard](https://docs.oracle.com/en-us/iaas/cloud-guard/home.htm) |

### 2. 감사 추적

모든 변경은 감사 로그로 남기고 중앙 저장소에 장기 보관합니다.

| 벤더 | 감사 로그 |
| --- | --- |
| AWS | [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) |
| Azure | [Azure Monitor Activity Log](https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log) |
| GCP | [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit) |
| OCI | [OCI Audit](https://docs.oracle.com/en-us/iaas/Content/Audit/Concepts/auditoverview.htm) |

### 3. 접근 통제와 최소 권한

최소 권한 원칙, MFA, 키 순환은 [IAM과 접근 제어](../security/iam.md)에서 다룹니다.

### 4. 데이터 보호

{% hint style="info" %}
저장/전송 암호화, 키 관리, 데이터 주권은 [데이터 보호와 워크로드 보안](../security/data-protection.md)
{% endhint %}

### 5. 지속 모니터링

감사 시점에만 통제를 맞추는 것이 아니라 상시 감지 체계를 운영합니다. 주요 벤더 모두 **컴플라이언스 대시보드** 를 제공합니다.

- AWS Security Hub — CIS Benchmark, NIST, PCI DSS 자동 검사 → [보안 태세 관리](../security/security-posture.md)에서 상세 설명
- Azure Defender for Cloud — Secure Score + 컴플라이언스 표준 자동 평가
- GCP Security Command Center — 컴플라이언스 프레임워크 매핑
- OCI Cloud Guard — 구성 오류 자동 감지

## 독자를 위한 체크리스트

멀티클라우드 환경에서 규정 준수를 고려할 때 확인할 사항:

- [ ] 처리/저장하는 데이터의 **민감도 분류** 는 끝났는가? (개인정보, 금융정보, 기밀정보 등)
- [ ] 해당 데이터에 적용되는 **법적 요건** 을 파악했는가? (국내법 + 해외법)
- [ ] 사용하려는 벤더가 필요한 **인증을 해당 리전에서 보유** 하는가?
- [ ] 공동 책임 모델에서 **사용자 책임 영역** 을 명확히 정의했는가?
- [ ] 감사 로그, 접근 통제, 암호화 등 **일상 운영 통제** 를 자동화했는가?
- [ ] 멀티클라우드 환경에서 **통합 감사** 가 가능한가? (개별 벤더 대시보드 분산 주의)

## 참고하기

### 한국 기관

- [KISA 인증 · 인정](https://isms.kisa.or.kr/)
- [개인정보보호위원회](https://www.pipc.go.kr/)
- [금융보안원](https://www.fsec.or.kr/)

### AWS

- [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)
- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- [AWS CSAP](https://aws.amazon.com/compliance/csap/)
- [AWS Artifact](https://aws.amazon.com/artifact/)

### Azure

- [Microsoft Trust Center](https://www.microsoft.com/trust-center)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms)
- [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap)
- [Azure Compliance Offerings](https://learn.microsoft.com/azure/compliance/)

### GCP

- [GCP Compliance Resource Center](https://cloud.google.com/security/compliance)
- [GCP K-ISMS](https://cloud.google.com/security/compliance/k-isms)
- [Google Compliance Reports Manager](https://cloud.google.com/security/compliance/compliance-reports-manager)

### OCI

- [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)
- [OCI Security Guide](https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm)

### 국제 표준

- [ISO/IEC 27001](https://www.iso.org/standard/27001)
- [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
