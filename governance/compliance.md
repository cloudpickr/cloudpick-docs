---
description: ISO 27001, SOC 2 등 글로벌 클라우드 규정 준수 인증과 컴플라이언스 운영 방법을 벤더별로 안내합니다.
---

# 규정 준수 (Compliance)

> 문서 기준: 2026년 8월

## 개요

클라우드에서 규정 준수는 **공동 책임 모델** 에 따라 벤더와 사용자가 책임을 나눕니다. 벤더는 인프라 계층의 보안 통제를 인증받고, 사용자는 자신의 워크로드 구성이 규제 요건을 충족하도록 관리합니다.

{% hint style="info" %}
공동 책임 모델의 개념적 배경은 [공동 책임 모델](../about-cloud/shared-responsibility.md)을 참고하세요.
{% endhint %}

{% hint style="warning" %}
**인증은 전제조건일 뿐 보증이 아닙니다.** 벤더가 국가·국제 인증을 가지고 있어도, 사용자가 구성한 VPC, IAM, 암호화 설정이 규제 요건을 충족하지 않으면 감사에서 문제가 됩니다. 또한 기술적 보안뿐 아니라 조직의 업무 프로세스(수집·이용·파기 절차, 변경 관리, 접근 권한 관리 등)도 심사 대상입니다.
{% endhint %}

## 국가별 컴플라이언스

국가·지역마다 공공 조달 인증, 개인정보 보호법, 산업별 규제가 다르며, 리전 선택·데이터 레지던시·격리 수준 같은 아키텍처 결정에 직접 영향을 줍니다. 국가별 상세는 해당 국가 문서에서 다룹니다.

- **한국** — ISMS-P, CSAP, 금융권 규제(전자금융감독규정·망분리): [컴플라이언스 (한국)](../korea/governance/compliance.md)
- **미국** — FedRAMP, HIPAA, ITAR/EAR: [미국 가이드](../us/index.md)
- **EU** — GDPR·데이터 주권, DORA, NIS2·EU AI Act: [EU 가이드](../eu/index.md)
- **일본** — ISMAP, APPI: [일본 가이드](../japan/index.md)
- **싱가포르** — MTCS, PDPA: [싱가포르 가이드](../singapore/index.md)

## 국제 주요 인증

### ISO/IEC 27001:2022 — 정보보호 관리체계

국제 표준의 정보보안 관리 체계. 대부분의 글로벌 CSP가 기본으로 보유합니다. **2022 개정판**이 현행 표준이며, 이전 2013 버전 인증서는 2025년 10월 31일부로 만료되었습니다. 아직 2022 버전으로 전환하지 않은 조직은 신규 인증(또는 전환 재인증)을 받아야 합니다.

주요 변경: 통제 항목이 114개에서 93개로 재구조화되고, "위협 인텔리전스", "클라우드 서비스 보안", "데이터 마스킹" 등 11개 신규 통제가 추가되었습니다.

- [AWS ISO 27001](https://aws.amazon.com/compliance/iso-27001-faqs/)
- [Azure ISO 27001](https://learn.microsoft.com/azure/compliance/offerings/offering-iso-27001)
- [Google Cloud ISO 27001](https://cloud.google.com/security/compliance/iso-27001)
- [Oracle ISO 27001](https://www.oracle.com/corporate/cloud-compliance/)

### ISO/IEC 42001 — AI 관리 체계

AI 시스템의 개발·운영에 대한 국제 표준 관리 체계 인증입니다. 책임 있는 AI 거버넌스를 위한 프레임워크를 제공합니다.

- OCI AI 서비스(Enterprise AI, AI Services)가 2026년 6월 ISO/IEC 42001 인증을 취득
- [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)

### SOC 1 / SOC 2 / SOC 3

AICPA(미국 공인회계사 협회) 기반 감사 보고서. 엔터프라이즈 고객이 자주 요구합니다.

- **SOC 1** — 재무 보고 통제
- **SOC 2** — 보안, 가용성, 처리 무결성, 기밀성, 개인정보 보호
- **SOC 3** — SOC 2 요약 공개 보고서

각 벤더의 SOC 보고서는 **기밀 자료** 이므로 고객 계약 후 AWS Artifact, Azure Service Trust Portal 등을 통해 다운로드합니다.

### 산업별 규제

| 산업 | 주요 규제 | 적용 지역 | 비고 |
| --- | --- | --- | --- |
| **의료** | HIPAA, HITRUST | 미국 | |
| **카드결제** | PCI DSS v4.0.1 | 글로벌 | v4.0(2024.3.31, 기존 v3.2.1 폐기) → v4.0.1(2024.6 정오표). 2025.3.31부터 v4.0의 "미래 날짜" ~50개 항목 의무화 완료 |
| **공공 (미국)** | FedRAMP / FedRAMP 20x | 미국 연방 | 20x: 수개월 단위 수동 인가를 OSCAL 기반 기계판독 증거·자동 검증 중심으로 단축하는 자동화 우선 프로세스 ([fedramp.gov/20x](https://www.fedramp.gov/20x/)) |
| **공공 (EU)** | C5 (독일), ENS (스페인) 등 | EU | |
| **개인정보 (EU)** | GDPR | EU | |
| **AI (EU)** | EU AI Act | EU | GPAI 의무 2025.8.2 시행 완료. 고위험 AI 2026.8.2 적용. [EU AI Act 전문](https://artificialintelligenceact.eu/) |
| **금융 (EU)** | DORA | EU | 2025.1.17 적용 개시. CTPP(Critical Third-Party Provider) 지정 절차 진행 중. [상세](../governance/landing-zone.md) |

각 벤더의 해당 인증 현황은 **AWS Compliance Programs**, **Azure Trust Center**, **Google Cloud Compliance**, **Oracle Cloud Compliance** 페이지에서 확인합니다.

## 벤더별 컴플라이언스 허브

인증 현황 전체 목록과 보고서 접근 방법은 각 벤더 공식 허브에서 관리됩니다.

| 벤더 | 허브 |
| --- | --- |
| AWS | [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/), [AWS Artifact (보고서)](https://aws.amazon.com/artifact/) |
| Azure | [Microsoft Trust Center](https://www.microsoft.com/trust-center), [Service Trust Portal](https://servicetrust.microsoft.com/) |
| Google Cloud | [Google Cloud Compliance Resource Center](https://cloud.google.com/security/compliance), [Google Compliance Reports Manager](https://cloud.google.com/security/compliance/compliance-reports-manager) |
| OCI | [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/) |

## 클라우드에서 규정 준수를 어떻게 운영하는가

인증 자체보다 **일상 운영에서 통제를 어떻게 유지하는가**가 감사의 핵심입니다.

### 1. 가드레일 자동화

수동 관리는 누락이 발생하므로 정책을 IaC로 코드화합니다.

| 벤더 | 도구 |
| --- | --- |
| AWS | [AWS Config](https://aws.amazon.com/config/), [AWS Security Hub](https://aws.amazon.com/security-hub/), SCP (Service Control Policy) |
| Azure | [Azure Policy](https://learn.microsoft.com/azure/governance/policy/overview), [Microsoft Defender for Cloud](https://azure.microsoft.com/products/defender-for-cloud) |
| Google Cloud | [Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/overview), [Security Command Center](https://cloud.google.com/security-command-center) |
| OCI | [OCI Security Zones](https://docs.oracle.com/en-us/iaas/Content/security-zone/home.htm), [OCI Cloud Guard](https://docs.oracle.com/en-us/iaas/cloud-guard/home.htm) |

### 2. 감사 추적

모든 변경은 감사 로그로 남기고 중앙 저장소에 장기 보관합니다.

| 벤더 | 감사 로그 |
| --- | --- |
| AWS | [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) |
| Azure | [Azure Monitor Activity Log](https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log) |
| Google Cloud | [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit) |
| OCI | [OCI Audit](https://docs.oracle.com/en-us/iaas/Content/Audit/Concepts/auditoverview.htm) |

### 3. 접근 통제와 최소 권한

최소 권한 원칙, MFA, 키 순환은 [IAM과 접근 제어](../security/iam.md)에서 다룹니다.

### 4. 데이터 보호

{% hint style="info" %}
저장/전송 암호화, 키 관리, 데이터 주권은 [데이터 보호와 워크로드 보안](../security/data-protection.md)을 참고하세요.
{% endhint %}

### 5. 지속 모니터링

감사 시점에만 통제를 맞추는 것이 아니라 상시 감지 체계를 운영합니다. 주요 벤더 모두 **컴플라이언스 대시보드** 를 제공합니다.

- AWS Security Hub — CIS Benchmark, NIST, PCI DSS 자동 검사. [보안 태세 관리](../security/security-posture.md)에서 상세히 다룹니다
- Azure Defender for Cloud — Secure Score + 컴플라이언스 표준 자동 평가
- Google Cloud Security Command Center — 컴플라이언스 프레임워크 매핑
- OCI Cloud Guard — 구성 오류 자동 감지

## 독자를 위한 체크리스트

멀티클라우드 환경에서 규정 준수를 고려할 때 확인할 사항:

- [ ] 처리/저장하는 데이터의 **민감도 분류** 는 끝났는가? (개인정보, 금융정보, 기밀정보 등)
- [ ] 해당 데이터에 적용되는 **법적 요건** 을 파악했는가? (국내법 + 해외법)
- [ ] 사용하려는 벤더가 필요한 **인증을 해당 리전에서 보유** 하는가?
- [ ] 공동 책임 모델에서 **사용자 책임 영역** 을 명확히 정의했는가?
- [ ] 감사 로그, 접근 통제, 암호화 등 **일상 운영 통제** 를 자동화했는가?
- [ ] 멀티클라우드 환경에서 **통합 감사** 가 가능한가? (개별 벤더 대시보드 분산 주의)

## 지속적으로 해야 할 것

- **인증 갱신 주기 관리** — 대부분의 인증은 3년 유효 + 연 1회 사후·감시심사 구조입니다(예: ISO 27001, 한국 ISMS-P). 갱신 일정을 캘린더에 등록하세요.
- **지속적 감사(Continuous Compliance)** — 수동 점검 대신 AWS Config, Azure Policy, Google Cloud Organization Policy로 정책 위반을 실시간 탐지합니다.
- **정책 드리프트 탐지** — IaC와 실제 환경의 차이를 정기적으로 확인하여 규정 준수 상태를 유지합니다.

## 자주 하는 실수

- **벤더 인증만 믿고 사용자 책임 영역을 방치** — 벤더가 인증을 가지고 있어도 VPC, IAM, 암호화 설정은 사용자 책임이므로 감사에서 지적됨
- **감사 시점에만 통제를 맞추고 평소에는 드리프트 방치** — 연 1회 심사 직전에만 정리하면 일상 운영에서 규정 위반이 누적됨
- **데이터 분류를 하지 않고 모든 데이터에 동일 보안 수준 적용** — 과보호로 비용이 폭증하거나, 과소보호로 규제 위반 발생

## 체크리스트

- [ ] 처리/저장하는 데이터의 민감도 분류(개인정보, 금융정보, 기밀정보)를 완료했는가
- [ ] AWS Config, Azure Policy 등으로 정책 위반을 실시간 탐지하는 지속적 감사 체계를 운영하는가
- [ ] 인증 갱신 일정(ISO 27001 감시심사 등)을 캘린더에 등록하고 관리하는가

## 참고하기

### AWS

- [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)
- [AWS Artifact](https://aws.amazon.com/artifact/)

### Azure

- [Microsoft Trust Center](https://www.microsoft.com/trust-center)
- [Azure Compliance Offerings](https://learn.microsoft.com/azure/compliance/)

### Google Cloud

- [Google Cloud Compliance Resource Center](https://cloud.google.com/security/compliance)
- [Google Compliance Reports Manager](https://cloud.google.com/security/compliance/compliance-reports-manager)

### OCI

- [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)
- [OCI Security Guide](https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm)

### 국제 표준

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001)
- [ISO/IEC 42001](https://www.iso.org/standard/81230.html) — AI 관리 체계
- [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [EU AI Act 전문](https://artificialintelligenceact.eu/)
- [EU DORA](https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en)
- [PCI DSS v4.0.1](https://www.pcisecuritystandards.org/)
- [FedRAMP 20x](https://www.fedramp.gov/20x/)
