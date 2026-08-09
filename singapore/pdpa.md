---
description: 싱가포르 PDPA의 개요, 국경 간 이전 제한과 2026년 4월 가이드 개정, 아세안 리전 설계 시사점, DNC 등 실무 유의점을 정리합니다.
---

# PDPA (개인정보보호법)

> 문서 기준: 2026년 8월

## 개요

PDPA(Personal Data Protection Act, 개인정보보호법)는 2012년 제정된 싱가포르의 개인정보 보호 일반법입니다. 개인정보보호위원회(Personal Data Protection Commission, PDPC)가 집행 기관 역할을 수행하며, 법률상으로는 정보통신미디어개발청(IMDA)이 PDPC로 지정되어 개인정보 보호 기능을 수행하는 구조입니다.

PDPA는 동의(Consent), 목적 제한(Purpose Limitation), 고지(Notification), 열람·정정(Access & Correction), 정확성(Accuracy), 보호(Protection), 보유기간 제한(Retention Limitation), **이전 제한(Transfer Limitation)**, 책임성(Accountability), 유출 통지(Breach Notification) 등의 의무를 규정합니다. 2020년 개정법으로 도입된 **데이터 이동성 의무(Data Portability Obligation, Part 6B)**는 아직 시행령이 마련되지 않아 발효되지 않은 상태이므로, 현재는 준수 의무 대상이 아닙니다.

{% hint style="info" %}
유출 통지 의무의 신고 기준은 (1) 개인에게 중대한 피해(재산상 손실, 신원 도용, 신체적 피해, 명예훼손 등)를 초래하거나 초래할 우려가 있는 경우, (2) 영향받는 개인이 500명 이상인 경우 중 하나만 충족해도 적용됩니다. PDPC는 평가 완료 시점부터 늦어도 3일(영업일 기준이 아닌 역일) 이내 신고를 기대한다고 안내하고 있습니다.
{% endhint %}

위반 시 PDPC는 최대 **100만 싱가포르달러(S$1M)** 또는 연매출 1,000만 싱가포르달러(S$10M)를 초과하는 기업의 경우 **연간 싱가포르 매출의 10%** 중 더 큰 금액을 과징금으로 부과할 수 있습니다.

## 국경 간 이전 제한 (Transfer Limitation Obligation)

PDPA Part 4에 규정된 이전 제한 의무는, 조직이 개인정보를 싱가포르 국외로 이전하려면 **수령 측이 PDPA에 상응하는 수준의 보호를 제공한다는 점을 확인하기 위한 적절한 조치**를 취하지 않는 한 이전을 금지합니다. 즉 데이터가 국경을 넘는 순간에도 원본과 동등한 보호 수준이 유지되어야 한다는 "동등 보호(comparable protection)" 원칙이 핵심입니다.

기존에 인정되던 이전 메커니즘은 다음과 같습니다.

- 개인의 이전 동의
- 계약상 장치(Contractual Clauses)
- 구속력 있는 기업 규칙(Binding Corporate Rules, BCR)
- 개인과의 계약 이행에 필요한 이전 등 법정 예외 사유
- 장관이 PDPA에 준하는 보호 수준을 갖췄다고 고시한 국가·지역으로의 이전

### 2026년 4월 가이드 개정 — CBPR·PRP 인증 경로 정비

PDPC는 **2026년 4월 14일**, 국경 간 데이터 이전 가이드를 개정해 발표했습니다. 이는 같은 시기 시행된 PDPA 개정 시행규칙(PDPA Amendment Regulations 2026)에 맞춰 규제 당국의 기대 수준을 정리한 것으로, 핵심은 인정되는 이전 메커니즘 전반을 최신 규정에 맞춰 재정리한 것입니다. CBPR·PRP 인증 경로 자체는 **2020년 6월 인정 발표, 2021년 2월 시행규칙 반영으로 이미 존재해 왔으며**, 이번 개정은 이를 포함한 전체 체계를 정비한 것입니다.

- **APEC CBPR(Cross-Border Privacy Rules, 국경 간 프라이버시 규칙) 인증**을 보유한 수령 조직(개인정보처리자, controller 성격)은 이전 제한 의무의 요건을 충족한 것으로 간주됩니다.
- **APEC PRP(Privacy Recognition for Processors, 처리자 프라이버시 인증) 인증**을 보유한 수탁 조직(데이터 중개자, data intermediary 성격)도 마찬가지로 요건 충족으로 인정됩니다. 데이터 중개자는 CBPR 또는 PRP 중 하나 혹은 둘 다를 보유하면 됩니다.
- 개별 계약서(SCC 유사 조항)를 매 거래마다 체결·검토하는 대신, **인증 취득만으로 국경 간 이전의 법적 근거를 확보**하는 경로가 명확히 정리되어 있습니다.

{% hint style="warning" %}
CBPR·PRP는 APEC 회원국 간에만 통용되는 인증 체계입니다. 이전 대상 국가·기업이 APEC CBPR/PRP 인증 시스템에 참여하지 않는 경우에는 여전히 계약상 장치나 BCR 등 기존 메커니즘을 활용해야 합니다. 한국은 APEC CBPR 시스템 참여국이므로, 한국 리전·한국 소재 계열사와의 데이터 이전 설계 시 이 인증 경로의 실익을 검토할 가치가 있습니다.
{% endhint %}

## 한국 기업의 아세안 리전 설계 시사점

- **싱가포르는 개방형 이전 정책을 취합니다.** 인도네시아·베트남 등 인접국이 데이터 로컬라이제이션(국내 저장 의무)을 강화하는 추세와 달리, 싱가포르는 "동등 보호가 확인되면 이전 허용"이라는 원칙 기반 접근을 유지합니다. 따라서 싱가포르를 아세안 데이터 허브로 활용하되, 개별 진출국의 로컬라이제이션 규제는 별도로 확인해야 합니다.
- **리전 아키텍처 설계 시 이전 메커니즘을 사전에 확정하세요.** 한국 본사·싱가포르 리전·제3국 계열사 간 데이터가 오가는 멀티리전 구조라면, 구간별로 계약상 장치·CBPR/PRP 인증·동의 중 어떤 메커니즘을 적용할지 데이터 흐름도 단계에서 미리 설계해야 감사 대응이 수월합니다.
- **인증 로드맵을 조기에 검토하세요.** CBPR/PRP는 자율 인증이 아니라 APEC이 인가한 책임기관(Accountability Agent)의 심사를 거쳐야 하므로, 취득까지 상당한 리드타임이 소요됩니다. 아세안 다국가 진출을 계획한다면 계약 기반 접근과 병행해 인증 취득을 조기에 검토하는 편이 유리합니다.
- **PDPA는 역외 적용 여지가 있습니다.** 싱가포르에 소재하지 않더라도 싱가포르 내 개인정보를 수집·처리하는 한국 기업(예: 싱가포르 고객을 대상으로 한 SaaS)에는 PDPA가 적용될 수 있으므로, 단순히 "리전을 싱가포르에 두지 않았다"는 이유로 적용 대상에서 제외된다고 단정해서는 안 됩니다.

## DNC(Do Not Call) 등 실무 유의점

PDPA에는 개인정보 처리 의무와 별개로 **DNC(Do Not Call) 조항**이 포함되어 있습니다. 개인은 자신의 싱가포르 전화번호를 다음 3개 등록부 중 하나 이상에 등록해 특정 유형의 마케팅 연락을 거부할 수 있습니다.

- No Voice Call Register (음성 통화 수신 거부)
- No Text Message Register (문자메시지 수신 거부)
- No Fax Message Register (팩스 수신 거부)

조직이 싱가포르 전화번호(휴대전화·유선·주거용·사업용 포함)로 마케팅 목적의 음성 통화·문자·팩스를 발송하려면, **명시적 동의를 받았거나 PDPA상 예외·제외 사유에 해당하지 않는 한** 사전에 DNC 등록부를 조회해 대상자가 등록되어 있는지 확인해야 합니다. 등록된 번호로 연락할 경우 위반으로 간주되어 PDPC에 신고될 수 있습니다.

{% hint style="info" %}
DNC 조회 의무는 B2C 마케팅 캠페인, 콜센터 아웃바운드, 문자 기반 프로모션 등 싱가포르 고객을 대상으로 한 마케팅 채널을 운영하는 한국 기업(특히 이커머스·핀테크·SaaS)에 실무적으로 자주 누락되는 항목입니다. CRM·마케팅 자동화 파이프라인에 DNC 조회 단계를 통합하는 것을 권장합니다.
{% endhint %}

## 책임성 증빙 — DPTM(Data Protection Trustmark) 인증

PDPC와 IMDA가 공동 개발한 **DPTM(Data Protection Trustmark)**은 조직의 PDPA 준수 수준과 개인정보 거버넌스 성숙도를 제3자가 검증하는 자발적 인증 제도입니다. 2025년에는 싱가포르 표준 **SS 714:2025**로 편입되어 국가 표준으로서의 위상이 강화되었습니다.

- 법정 의무 사항은 아니지만, 인증을 통해 거버넌스·책임성·고객 대응 체계를 대외적으로 입증할 수 있어 **B2B 계약이나 정부 조달의 벤더 실사 단계에서 가점 요소**로 작용하는 경우가 많습니다.
- 싱가포르에 현지 법인·자회사를 두고 소비자 대상 서비스를 운영하는 한국 기업이라면, PDPA의 책임성(Accountability) 의무를 이행하는 절차 중 하나로 DPTM 취득을 검토할 수 있습니다.
- 인증은 PDPC·IMDA가 인가한 인증기관이 수행하며, 조직 전체(enterprise-wide) 또는 특정 사업 단위 단위로 범위를 선택할 수 있습니다.

## 참고하기

- [Individual's Guide to the Do Not Call (DNC) Registry — PDPC](https://www.pdpc.gov.sg/individuals/e-services/how-to-register-with-the-do-not-call-dnc-registry-for-individuals/individuals-guide-to-the-do-not-call-dnc-registry)
- [Organisation's Guide to Singapore's Do Not Call (DNC) Provisions — PDPC](https://www.pdpc.gov.sg/about/do-not-call-registry/do-not-call-registry-for-organisations/organisations-guide-to-singapores-do-not-call-dnc-provisions)
- [The Transfer Limitation Obligation — PDPC](https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/advisory-guidelines/the-transfer-limitation-obligation---ch-19-(270717).pdf)
- [Data Protection Trustmark (DPTM) Certification — IMDA](https://www.imda.gov.sg/how-we-can-help/data-protection-trustmark-certification)
- [Accountability Within Industry — PDPC](https://www.pdpc.gov.sg/help-and-resources/2021/09/accountability/accountability-within-industry)
- [Fintech Singapore: PDPA Cross-border Data Transfers (2026) — Global Law Experts](https://globallawexperts.com/pdpa-crossborder-data-transfers-fintech-singapore-2026/)
- [Data Protection & Privacy 2026 - Singapore — Chambers and Partners](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/singapore/trends-and-developments)
- [Data Protection Laws and Regulations 2026 | Singapore — ICLG](https://iclg.com/practice-areas/data-protection-laws-and-regulations/singapore/)
