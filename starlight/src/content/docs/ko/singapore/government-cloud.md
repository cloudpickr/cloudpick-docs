---
title: "정부 클라우드 (GCC·IM8·SGTS)"
description: "싱가포르 정부 클라우드 체계 — GCC(Government Commercial Cloud)의 구조와 GCC+, IM8 보안 정책 개혁, SG Tech Stack, 정부 조달 참여 요건을 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

싱가포르 정부는 자체 데이터센터를 구축하는 대신, 상용 하이퍼스케일러 위에 표준화된 보안·거버넌스 계층을 얹는 방식으로 정부 클라우드를 운영합니다. 이 체계의 중심에는 **GCC(Government Commercial Cloud, 정식 명칭은 Government on Commercial Cloud)** 가 있으며, 정부기술청(Government Technology Agency of Singapore, GovTech)이 주관합니다.

GCC는 **CODEX(Core Operations, Development Environment, and eXchange)** 라는 상위 전략 프로젝트의 한 축입니다. CODEX는 스마트네이션(Smart Nation) 전략 산하 핵심 국가 프로젝트로 지정되어 있으며, GCC(인프라 계층) 외에도 SG Tech Stack(SGTS, 개발 계층)과 정부 데이터 아키텍처(Government Data Architecture, 데이터 계층)를 포함합니다.

:::note
GCC는 한국의 국가정보자원관리원(NIRS)이나 클라우드 기반 공공기관 정보자원 통합 사업처럼 **정부기관이 직접 사용하는 내부용 플랫폼**입니다. 민간 벤더가 "GCC에 입점"하는 구조가 아니라, 정부기관이 AWS·Azure·GCP 위에 GovTech가 제공하는 보안·거버넌스 래퍼(wrapper)를 씌워 시스템을 운영하는 방식입니다. 민간 기업이 싱가포르 정부 대상 사업에 참여하려면 GeBIZ 조달 포털 등록과 MTCS 인증 등 별도 트랙을 거쳐야 합니다.
:::

## GCC(Government Commercial Cloud)의 구조

GCC는 "래퍼(wrapper) 플랫폼"으로 소개됩니다. 정부기관이 클라우드 인프라를 직접 구축·유지보수하는 대신, GCC가 제공하는 표준화된 프레임워크 위에서 상용 클라우드 서비스를 이용하는 구조입니다. 공식 프레임워크는 다음 구성 요소로 이뤄집니다.

- **온보딩(Onboarding)** — TechPass(GovTech의 IAM 솔루션) 기반 자동화된 계정·권한 발급
- **과금(Billing)** — 기관별 클라우드 사용료 통합 관리
- **애플리케이션 계층** — AWS·Microsoft Azure·Google Cloud(GCP) 3사를 대상으로 함 (Oracle Cloud 등 다른 벤더는 GCC 프레임워크에 포함되지 않음)
- **모니터링·로깅·점프호스트** — 중앙화된 관측성과 감사 추적
- **온프레미스 연계** — 정부기관 내부 시스템과의 하이브리드 연결
- **거버넌스·정책·데이터 레지던시** — 싱가포르 내 데이터 상주 요건 등 정책 통제

### GCC 1.0에서 GCC 2.0으로

초기 GCC(1.0)는 벤더 아웃소싱 지원 모델로 운영되었으나, 온보딩 지연·서비스 요청 과다 등의 문제로 재설계되었습니다. GCC 2.0은 하이퍼스케일러별로 순차 정식 가동되었습니다.

| 클라우드 | GCC 2.0 정식 가동(GA) |
| --- | --- |
| AWS | 2022년 5월 4일 |
| Microsoft Azure | 2022년 11월 30일 |
| Google Cloud (GCP) | 2023년 7월 7일 |

GCC 2.0의 핵심 특징은 다음과 같습니다.

- **간소화된 온보딩** — TechPass만으로 온보딩 가능, 서비스 요청(service request) 없이 자동화된 워크플로로 계정 발급
- **SEED(Secure Engineering Environment Device Platform)** — 전통적 경계 기반 보안에서 **제로 트러스트** 모델로 전환. 비준수 단말의 접근을 자동 차단
- **Policy-as-Code** — 정책을 코드로 정의·적용해 프로비저닝되는 모든 리소스에 기본적으로 컴플라이언스 점검을 적용하고, 실시간으로 보안 취약점을 점검
- **IaC(Infrastructure as Code)** 기반 코어 클라우드 플랫폼 구성

### GCC+ — Confidential 등급 워크로드로 확장

GCC 2.0이 다루는 일반(Confidential Cloud-Eligible 이하) 등급 시스템과 달리, **Confidential로 분류된 고민감 시스템**은 **GCC+**로 별도 온보딩됩니다. GCC+는 강화된 암호화·키 관리 분리, 싱가포르 국내 리전 상주 등 더 엄격한 통제를 적용해 이전에는 클라우드 이전이 어려웠던 민감 워크로드(법 집행·보건 데이터 처리 시스템 등)의 클라우드 전환 경로를 제공합니다.

### 채택 현황

GovTech가 2025년 3월 7일 기준으로 공개한 수치에 따르면, GCC에는 **3,006개 시스템**이 온보딩되어 있으며 **99.5%의 서비스 가용성**을 기록하고 있습니다. GovTech FY2024-2025 연차보고서는 **정부 디지털 서비스 거래의 99%가 온라인으로 완료**되고 있다고 밝혔습니다(이 수치는 GCC/GCC+가 직접 지원하는 거래 비율이 아니라 정부 거래의 온라인 완료율을 가리키므로 혼동하지 않아야 합니다). GCC 위에서 운영되는 대표 서비스로는 MyCareersFuture(구직 포털), GoBusiness(기업 대상 인허가 포털), WOGAA(정부 디지털 서비스 성과 모니터링), 국세청(IRAS)의 통합 세무 시스템 IRIN, 교육부의 홈베이스드러닝 플랫폼 Student Learning Space 등이 있습니다.

## IM8과 2024~2026년 정책 개혁

**IM8**은 「Instruction Manual on ICT&SS(Infocomm Technology & Smart Systems) Management」의 약칭으로, GovTech가 관장하는 정부기관 ICT 보안 정책·표준 전체를 가리킵니다. 데이터 보안 분류, 클라우드 보안, 애플리케이션·네트워크·엔드포인트 보안, 보안 운영 등을 포괄하며, 정부기관이 시스템을 도입·운영할 때 준수해야 하는 내부 규범집 역할을 합니다.

기존 IM8 체계에서는 정부 시스템이 원칙적으로 GCC 위에서 호스팅되어야 했고, SaaS 애플리케이션은 GCC 밖에서 호스팅될 수 없었습니다. 이 경직성이 SaaS 도입 속도를 늦춘다는 문제의식에서, GovTech는 **ICT&SS 정책 개혁(ICT&SS Policy Reform, 통칭 IM8 Reform)** 을 추진하고 있습니다.

개혁의 목표는 공식적으로 "기관이 적정 수준의 위험 통제(right-fit risk controls)로 신속하고 비용 효율적이며 혁신적인 시스템을 구축할 수 있도록 ICT&SS 정책을 단순화하는 것"으로 제시됩니다. 핵심 변화는 다음과 같습니다.

- **위험 기반 접근(Risk-Based Approach)** — 시스템을 저위험 클라우드, 중위험 클라우드, 고위험 클라우드, 저위험 온프레미스, 생성형 AI, 디지털 서비스, 샌드박스 등 유형별로 구분하고 각기 다른 통제 수준을 적용
- **System Security Plan(SSP) 템플릿 재정비** — 위험 유형별 기본 통제 세트를 사전 정의해 기관이 이를 커스터마이징하는 방식으로 전환
- **통제 카탈로그(Control Catalog) 재구성** — 동일한 위험 분류 체계에 맞춰 통제 항목을 재정렬
- **저위험 SaaS의 GCC 외부 호스팅 허용** — 저위험 용도에 한해 GCC 밖에서 호스팅되는 SaaS 애플리케이션 도입을 허용하는 방향으로 정책이 개편되는 중
- 시스템 소유 기관(digital system owner)에게 자사의 업무·기술 맥락에 맞춰 보안 계획을 스스로 조정할 수 있는 **재량권 확대**

:::caution
IM8 개혁은 2026년 8월 시점 **진행형 정책 전환**입니다. 저위험 SaaS의 GCC 외부 호스팅 허용 범위, 통제 카탈로그의 최종 확정 시점 등 세부 사항은 GovTech의 공식 정책 포털(info.standards.tech.gov.sg)에서 계속 갱신되고 있으므로, 실제 조달·컴플라이언스 대응 시에는 최신 공고를 직접 확인해야 합니다.
:::

## SGTS(Singapore Government Tech Stack)

SGTS는 GCC(인프라 계층)와 짝을 이루는 **개발 계층** 자산으로, GovTech가 제공하는 재사용 가능한 플랫폼·API·공통 서비스 모음입니다. 정부기관이 인프라를 처음부터 구축하지 않고도 신원 인증, 결제, 데이터 교환 등 공통 기능을 재사용해 디지털 서비스를 빠르게 만들 수 있도록 지원합니다. GovTech는 **사람(People)·플랫폼(Platform)·실천(Practice)** 3대 축으로 SGTS 확산 전략을 설명합니다.

40개 이상의 정부기관이 SGTS를 사용 중이며, 200개 이상의 클라우드 기반 시스템이 이를 통해 구축되었습니다. 대표 사례로 국민 디지털 신원 확인 서비스 **MyInfo**는 SGTS를 활용해 통상 1년 걸리던 개발 기간을 4개월로 단축했습니다. SGTS 산하에는 정부 개발자를 위한 멀티테넌트 SaaS 성격의 CI/CD 도구인 **SHIP-HATS**(Secure Hybrid Integration Pipeline – Hive Agile Testing Solutions)도 포함됩니다.

## 정부 조달 참여 요건과 MTCS의 관계

GCC·IM8·SGTS는 정부기관 내부용 체계이지만, 이를 뒷받침하는 상용 클라우드·SaaS를 공급하는 민간 벤더에게는 별도의 진입 요건이 적용됩니다.

- 정부기관은 클라우드·ICT 조달을 **GeBIZ**(Government Electronic Business System, 정부 통합 전자조달 포털)를 통해 진행해야 합니다. 이는 정부조달법(Government Procurement Act)과 각종 Instruction Manual에 근거한 의무 채널입니다.
- 정부 클라우드 조달에서 벤더의 클라우드 서비스에 **MTCS Level 3 인증**을 요구하는 경우가 많지만, 정확한 인증·자격 요건은 개별 입찰 공고·취급 데이터 등급·서비스 유형에 따라 달라지므로 사업별로 확인해야 합니다. MTCS 인증 체계와 등급 구조는 [MTCS (멀티티어 클라우드 보안 표준)](../mtcs/) 문서에서 자세히 다룹니다.
- GCC는 공통 플랫폼 차원에서 PDPA·IM8·MTCS Level 3에 부합하는 보안·거버넌스 가드레일을 제공하지만, 공식 자료는 개별 워크로드가 별도 절차 없이 인증을 완전히 자동 상속한다고 보장하지는 않습니다. 공동책임모델에 따라 서비스별 추가 설정·심사가 필요할 수 있습니다. 정부기관에 SaaS·플랫폼을 공급하려는 민간 벤더는 스스로 MTCS 인증 등 요건을 갖춰야 조달 대상에 오를 수 있습니다.

## 실무 시사점

- **GCC는 "정부 전용 사설 플랫폼"이지 별도의 인증 제도가 아닙니다.** 한국 기업이 싱가포르 정부 대상 사업(SI, SaaS 공급 등)을 검토한다면, GCC 자체에 인증받는 것이 목표가 아니라 GeBIZ 등록과 (입찰별로 요구되는) MTCS 인증 확보가 실질적인 진입 절차입니다.
- **IM8 개혁 흐름을 주시할 가치가 있습니다.** 저위험 SaaS의 GCC 외부 호스팅이 허용되는 방향으로 정책이 완화되고 있어, 향후 정부기관 대상 SaaS 판매 시 GCC 내부 인프라 종속성이 낮아질 가능성이 있습니다. 다만 개혁이 완료되지 않았으므로 개별 조달 공고의 요구 사항을 그때그때 확인해야 합니다.
- **CODEX·GCC·SGTS의 위계를 구분해 이해해야 합니다.** GCC(인프라)·SGTS(개발 플랫폼)·정부 데이터 아키텍처(데이터)는 각각 다른 계층을 다루므로, 정부기관 상대 제안서를 작성할 때 어느 계층에 대응하는 솔루션인지 명확히 해야 합니다.
- **컴플라이언스는 민간 시장과 별도 트랙입니다.** 민간 기업 대상 클라우드 규제(PDPA, MTCS)와 정부기관 내부 정책(IM8, GCC)은 운영 주체와 적용 대상이 다르므로, 두 트랙을 혼동해 하나의 인증만으로 양쪽 모두 충족된다고 가정해서는 안 됩니다.

## 참고하기

- [Government on Commercial Cloud (GCC) — GovTech Singapore](https://www.tech.gov.sg/products-and-services/for-government-agencies/software-development/government-on-commercial-cloud/)
- [Singapore Government Tech Stack (SGTS) — GovTech Singapore](https://www.tech.gov.sg/products-and-services/for-government-agencies/software-development/sg-tech-stack/)
- [About GCC 2.0 — Singapore Government Developer Portal](https://www.developer.tech.gov.sg/products/categories/infrastructure-and-hosting/gcc/about-gcc-2-0)
- [GCC Overview (GCC/GCC+ 분류 기준) — Singapore Government Developer Portal](https://www.developer.tech.gov.sg/products/categories/infrastructure-and-hosting/gcc/overview)
- [Government on Commercial Cloud (GCC 2.0) Fact Sheet — GovTech Singapore](https://www.developer.tech.gov.sg/assets/files/gcc-factsheet-121222.pdf)
- [Singapore Government ICT&SS Policy Reform Portal — GovTech Singapore](https://info.standards.tech.gov.sg/)
- [GeBIZ — Singapore Government e-Procurement Portal](https://www.gebiz.gov.sg/)
- [Tech Stacks Driving Singapore's Smart Nation Journey — GovTech (정부 거래 온라인 완료율 99% 출처)](https://www.tech.gov.sg/technews/tech-stacks-driving-singapore-smart-nation/)
- 금융권·공공 조달의 MTCS 요건은 [MTCS (멀티티어 클라우드 보안 표준)](../mtcs/)를, 개인정보 관련 규제는 [PDPA (개인정보보호법)](../pdpa/)를 참고하세요.
