---
description: 미국 연방기관 클라우드 조달을 위한 보안 인가 제도 FedRAMP의 개요, 2026년 FedRAMP 20x 개편 현황, 격리 리전, CMMC·DoD SRG를 정리합니다.
---

# FedRAMP

> 문서 기준: 2026년 8월

## 개요

FedRAMP(Federal Risk and Authorization Management Program)는 미국 연방기관이 클라우드 서비스를 조달할 때 보안성을 검증하는 정부 전체 공통 인가 제도입니다. GSA(연방조달청) 산하 FedRAMP PMO가 운영하며, NIST SP 800-53 통제 체계를 기반으로 클라우드 서비스 제공자(CSP)의 보안 통제를 평가·인가합니다. 핵심 취지는 "한 번 인가받아 여러 기관에서 재사용"(Do Once, Use Many Times)으로, 개별 기관이 각자 보안 심사를 반복하지 않고 FedRAMP 인가를 받은 서비스를 재사용할 수 있게 하는 것입니다.

FedRAMP는 법적으로 민간 기업에 의무 사항은 아니지만, 연방기관에 SaaS/PaaS/IaaS를 납품하려는 사실상 모든 클라우드 서비스 제공자에게는 필수적인 진입 요건입니다.

## Moderate/High 기준 (전통 체계)

FedRAMP는 FIPS 199 영향도 분류를 바탕으로 데이터의 기밀성·무결성·가용성 손상 시 피해 규모에 따라 보안 통제 수준을 구분해 왔습니다.

| 구분 | 대상 | 특징 |
| --- | --- | --- |
| **Low** | 손상 시 영향이 제한적인 공개 정보 시스템 | 통제 수 최소 |
| **Moderate** | 대부분의 연방기관 업무 시스템, CUI(통제 미분류 정보) 포함 | 상용 SaaS/PaaS의 표준 목표 기준. 통제 항목 약 320여 개 |
| **High** | 법 집행, 응급 서비스, 금융 시스템 등 손상 시 심각한 영향 | 통제 항목 약 420여 개, 인가 난도·비용 최고 |

상용 클라우드 서비스 대부분은 Moderate 기준으로 인가를 받으며, High 기준은 국토안보부·법무부 등 민감도가 높은 기관 시스템에 주로 요구됩니다.

## 2026년 FedRAMP 20x 개편 현황 (fedramp.gov 공식 기준)

{% hint style="warning" %}
FedRAMP 20x는 2026년 8월 현재도 진행 중인 개편으로, 정보가 빠르게 바뀝니다. 아래는 [fedramp.gov](https://www.fedramp.gov/) 공식 페이지와 공지사항을 기준으로 확인한 내용이며, 실제 도입 검토 시에는 반드시 fedramp.gov 최신 공지를 직접 재확인해야 합니다.
{% endhint %}

FedRAMP는 기존 Low/Moderate/High 3단계 체계를 자동화 기반의 **FedRAMP 20x** 프로그램으로 전환하는 중입니다.

- **Certification Class 체계**: Class A/B/C/D 4단계의 Certification Class 체계가 2026년 2월 25일 공개된 NTC-0004(정책 문서)에 근거해 도입되었습니다. 주의할 점은 Class가 보안 등급의 대체가 아니라 **평가·인증의 범위(제출 자료·증거 공유·검토 방식)를 정의하는 분류**라는 것입니다 — FedRAMP 공식 문서는 "베이스라인은 평가·인증의 범위를 정의하며, 클라우드 서비스의 전체 품질이나 보안 수준을 나타내는 것이 아니다"라고 명시합니다. 기존 Rev5 Moderate 수준 시스템(CUI 등 비공개 연방 데이터)은 실무상 Class C 경로로 이행하는 대응 관계가 안내되고 있습니다.
- **2026 Consolidated Rules (CR26)**: 2026년 6월 하순 확정·발효된 통합 규칙으로, 인가 패키지를 기계 판독 가능한(machine-readable) 형식 중심으로 제출하도록 요구하며, 기존 Word/Excel 템플릿 기반 패키지는 단계적으로 퇴출됩니다. CSP는 변경 사항 발생 시 자동화를 통해 인가 패키지를 지속적으로 최신 상태로 유지해야 합니다.
- **현재 운영 상태(2026년 8월 기준)**: Class A 파이프라인이 8월 초 열렸고 Class B/C는 2026년 8월 31일 오픈 예정인 과도기이며, fedramp.gov 공식 통계 기준 전체 약 529개 인가 서비스 중 약 28개가 신규 FedRAMP 20x 기준으로 인가를 받았고, 나머지 대다수는 여전히 기존 Rev5(Low/Moderate/High) 체계로 운영되고 있습니다.
- **Class D(High급) 개발 중**: 고위험 등급에 해당하는 Class D는 아직 개발 중이며, 2027년 1~2분기 파일럿이 예정되어 있습니다.
- **Rev5 종료 일정**: 기존 Rev5 체계는 2027년 6월 11일까지 신규 인가 접수를 유지하며, 이후 기존 Rev5 인가 보유 서비스를 위한 전환 경로가 2027년 하반기에 마련될 예정입니다.

{% hint style="info" %}
즉 2026년 8월 시점에서는 신규 20x 체계와 기존 Rev5 체계가 병존하는 과도기입니다. 조달 대상 기관·서비스가 어떤 체계로 인가받았는지는 [FedRAMP Marketplace](https://marketplace.fedramp.gov/)에서 개별 확인이 필요합니다.
{% endhint %}

## 격리 리전: GovCloud, Azure Government, Assured Workloads, OCI Government

FedRAMP High 및 DoD 요건까지 충족하려는 워크로드는 상용 리전과 물리적·논리적으로 분리된 정부 전용 리전을 사용하는 경우가 많습니다.

| 리전 | 특징 |
| --- | --- |
| **AWS GovCloud (US)** | FedRAMP High, DoD SRG IL2/4/5, ITAR/EAR, CJIS 지원. 미국 내 물리적 위치, 미국 시민권자만 운영 접근. 계정 소유자는 US Person이어야 함 |
| **Azure Government** | 상용 Azure와 물리적·논리적으로 격리, 심사받은 미국인 인력 운영. FedRAMP High, DoD IL4/5, CJIS, ITAR 지원 |
| **Google Assured Workloads** | 별도 물리 인프라 대신 표준 GCP 리전 위에 소프트웨어 정의 통제(데이터 상주, 암호화 키 관리 등)를 적용하는 방식. IL5 이상은 전용 환경 제공 |
| **OCI Government Cloud** | Oracle 데이터베이스·엔터프라이즈 애플리케이션 의존 워크로드를 겨냥한 정부 전용 리전 |

## CMMC 2.0 및 DoD SRG Impact Level

**CMMC 2.0**(Cybersecurity Maturity Model Certification)은 국방부(DoD) 공급망 계약업체에 적용되는 사이버보안 인증 제도로, 3단계로 구성됩니다.

- **Level 1 (Foundational)**: FCI(연방 계약 정보)를 다루는 업체 대상, 자체 평가
- **Level 2 (Advanced)**: CUI를 다루는 업체 대상, NIST SP 800-171 기반, 대부분 C3PAO(제3자 평가기관) 인증 필요
- **Level 3 (Expert)**: 최고 민감도 정보 대상, NIST SP 800-172 추가 통제, 정부(DIBCAC) 주도 평가

CMMC 최종 규칙(32 CFR Part 170)은 2024년 발효되었고, 계약에 반영하는 DFARS 252.204-7021 개정 규칙은 2025년 11월 10일부터 시행되었습니다. 다만 2026년 8월 현재 단계적 시행 일정(Phase 2 이후)이 검토를 위해 일시 보류된 상태로 파악되며, **정확한 시행 단계는 계약 시점에 반드시 재확인이 필요합니다.**

**DoD Cloud Computing SRG(Security Requirements Guide) Impact Level**은 국방부 정보의 민감도에 따라 클라우드 환경을 구분합니다.

| Impact Level | 대상 정보 | 인프라 요건 |
| --- | --- | --- |
| **IL2** | 공개 가능 정보 | 상용 클라우드 수준 |
| **IL4** | CUI 및 비공개 비분류 정보 | 강한 논리적 분리, 공유 인프라 허용 |
| **IL5** | 고민감 CUI, 임무 필수·국가안보 시스템 정보 | 전용 인프라, 미국 시민권자 운영 인력 필수 |
| **IL6** | 기밀(SECRET) 및 국가안보 시스템 정보 | 완전 격리 환경 |

IL1과 IL3은 별도로 존재하지 않으며(IL1은 불필요, IL3은 IL4로 통합), FedRAMP Moderate 인가가 IL2의 최소 요건과 대략 대응합니다.

## 한국 기업 시사점

- 미 연방 SaaS 시장에 진입하려면 FedRAMP 인가가 사실상 필수 조건이며, 인가 획득에는 상당한 시간과 비용이 소요됩니다. FedRAMP 20x가 이 과정을 자동화·단축하려는 시도이지만 2026년 8월 현재 여전히 과도기이므로, 신규 진입 기업은 어떤 체계(Rev5 vs 20x)로 인가를 준비할지 fedramp.gov 최신 지침을 기준으로 판단해야 합니다.
- 스폰서 기관(Sponsoring Agency) 확보, 미국 내 법인·운영 조직 구성, 미국인 중심 운영 인력 등 조직적 진입장벽이 기술적 통제 못지않게 큽니다.
- 직접 인가를 추진하기보다, 이미 FedRAMP 인가를 받은 인프라(GovCloud, Azure Government 등) 위에 SaaS를 구축하거나 인가받은 파트너와 리셀러/OEM 형태로 협력하는 것이 초기 진입 전략으로 흔히 활용됩니다.
- 국방·항공우주 공급망에 참여하는 경우 FedRAMP와 별개로 CMMC 인증이 요구될 수 있으므로, 대상 계약 유형에 따라 별도로 확인해야 합니다.

## 참고하기

- [FedRAMP 공식 사이트](https://www.fedramp.gov/)
- [FedRAMP Marketplace](https://marketplace.fedramp.gov/)
- [FedRAMP 20x 프로그램](https://www.fedramp.gov/20x/)
- [FedRAMP 업데이트 공지](https://www.fedramp.gov/updates/)
- [AWS GovCloud (US) 컴플라이언스](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-compliance.html)
- [Azure Government 공식 페이지](https://azure.microsoft.com/en-us/explore/global-infrastructure/government/)
- [Google Cloud Assured Workloads 개요](https://cloud.google.com/assured-workloads/docs/overview)
- [DoD Cloud Computing SRG (public.cyber.mil)](https://public.cyber.mil/dccs/)
- [CMMC 공식 정보 (DoD CIO)](https://dodcio.defense.gov/cmmc/)
