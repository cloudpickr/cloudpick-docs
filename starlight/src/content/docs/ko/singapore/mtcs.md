---
title: "MTCS (멀티티어 클라우드 보안 표준)"
description: "싱가포르 MTCS(SS 584) 클라우드 보안 표준의 등급 체계, 운영 기관, 하이퍼스케일러 인증 현황, 금융권 추가 요건을 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

MTCS(Multi-Tier Cloud Security, 멀티티어 클라우드 보안)는 싱가포르 표준 **SS 584**로 제정된 클라우드 보안 인증 제도입니다. 정보통신기술표준위원회(Information Technology Standards Committee, ITSC)가 개발하고 정보통신미디어개발청(Infocomm Media Development Authority, IMDA)과 엔터프라이즈 싱가포르(Enterprise Singapore)가 지원하며, 여러 등급으로 클라우드 보안 수준을 구분한 세계 최초의 다단계 클라우드 보안 표준으로 소개됩니다.

2013년 최초 제정 이후 SS 584:2015를 거쳐, 현재 기준이 되는 최신판은 **SS 584:2020**입니다. ISO/IEC 27001:2013과의 정합성을 강화하고, 제로 트러스트·지속적 모니터링 등 최신 보안 개념에 대한 통제 항목을 추가했습니다.

인증은 싱가포르 인증위원회(Singapore Accreditation Council, SAC)가 인가한 MTCS 인증기관(Certifying Body, CB)이 심사를 수행하며, 유효기간은 3년이고 매년 사후관리(surveillance) 심사를 받아야 유지됩니다.

:::note
MTCS는 한국의 CSAP처럼 법률상 강제되는 진입 규제라기보다, **공공 조달과 금융권 벤더 실사에서 폭넓게 요구되는 요건**으로 기능하는 산업 표준에 가깝습니다. IMDA가 발주하는 정부 클라우드 조달(Government Commercial Cloud 등)에서는 MTCS 인증이 요구 사항으로 명시되는 경우가 일반적입니다.
:::

## 등급 구분 (Level 1~3)

| 등급 | 대상 워크로드 | 특징 |
| --- | --- | --- |
| **Level 1** | 웹사이트 호스팅, 테스트·개발 환경, 시뮬레이션 등 비중요 업무 | 최소한의 기본 보안 통제만 요구하는 저비용 등급 |
| **Level 2** | 대다수 기업의 일반 업무 시스템, 미션 크리티컬 애플리케이션 포함 | 데이터 보안 위협에 대응하는 한층 강화된 통제 세트. 상용 클라우드 이용 기업 대부분이 목표로 하는 등급 |
| **Level 3** | 규제 산업, 정부 조달 대상 시스템, 민감·고영향 데이터 처리 시스템 | Level 1·2 통제에 더해 엄격한 추가 통제를 요구. 고위험·민감 시스템 대상 정부 조달에서 Level 3가 요구되는 경우가 많음 (모든 정부 조달에 일률 적용되는 것은 아님) |

세 등급 모두 서비스 유형(IaaS/PaaS/SaaS)별로 별도 인증 범위를 지정할 수 있어, 벤더가 자사 서비스 중 일부만 특정 등급으로 인증받는 경우도 흔합니다. 도입 검토 시에는 등급뿐 아니라 **인증 범위(어떤 서비스·리전이 포함되는지)** 를 반드시 확인해야 합니다.

## IMDA 운영 체계

- **ITSC(정보통신기술표준위원회)** 가 SS 584 표준 자체를 제·개정하고, IMDA와 엔터프라이즈 싱가포르가 이를 지원합니다.
- **SAC(싱가포르 인증위원회)** 가 심사를 수행할 인증기관(CB)을 인가합니다. CB는 국제 인증기관(BSI, DNV, TÜV, Ernst & Young Certify Point 등)이 다수를 차지합니다.
- 인증 획득 후에는 **3년 주기 갱신 + 매년 사후관리 심사**를 통해 인증 상태를 유지해야 하며, 심사에 실패하면 인증이 정지·취소될 수 있습니다.
- IMDA는 MTCS 인증 클라우드 서비스 목록과 인증서(QR 코드 포함)를 공식 웹사이트에 게시해 조달 담당자가 검증할 수 있도록 합니다.

## 하이퍼스케일러 인증 현황 (2026년 8월 기준)

| 벤더 | 인증 등급 | 비고 |
| --- | --- | --- |
| AWS | Level 3 (SS 584:2020) | 2014년 업계 최초로 Level 3 취득. 2024년 12월 SS 584:2020 기준으로 갱신하며 인증 범위를 아시아태평양(싱가포르), 아시아태평양(서울), 미국 리전까지 확대 |
| Microsoft Azure | Level 3 | IaaS·PaaS에 대해 Level 3 인증을 세계 최초로 3개 서비스 분류(IaaS/PaaS/SaaS) 전체에서 취득한 CSP로 소개됨. Microsoft 365(Office 365)도 2021년 SS 584:2020 기준 Level 3 인증 별도 취득 |
| Google Cloud | Level 3(Tier 3) | Google Cloud 및 Google Workspace 서비스·데이터센터 사이트 일부를 대상으로 Tier 3 인증 취득 |
| Oracle Cloud Infrastructure (OCI) | Level 3 | 싱가포르·일본 리전을 대상으로 Level 3 인증 취득. Oracle Fusion Cloud Applications Suite도 2021년 12월 별도로 Level 3 인증 취득 |

4개 주요 하이퍼스케일러 모두 최소 일부 서비스·리전에 대해 MTCS Level 3 인증을 보유하고 있습니다. 다만 인증 범위는 벤더마다 다르므로, 실제 사용하려는 서비스와 리전이 인증서에 명시된 범위(scope)에 포함되는지를 계약 전 반드시 확인해야 합니다.

## 금융권 추가 요건

싱가포르 금융업권에서 클라우드를 도입하려면 MTCS 인증만으로는 충분하지 않고, 통화청(Monetary Authority of Singapore, MAS)이 제시하는 별도 프레임워크를 함께 충족해야 합니다.

- **MAS TRM 가이드라인(Technology Risk Management Guidelines)** — 2021년 1월 개정판에서 금융회사(FI)의 클라우드·API·애자일 개발 활용 확대에 대응해, 제3자(아웃소싱) 공급자에 대한 감독 강화를 명시적으로 요구합니다. 법적 구속력은 없는 가이드라인이지만, MAS 검사 시 사실상의 준수 기준으로 작동합니다.
- **MAS Notice 655 (사이버 위생, Cyber Hygiene)** — TRM 가이드라인과 별개로 법적 구속력을 가지는 통지로, 최소 보안 기준선을 규정합니다.
- **OSPAR(Outsourced Service Provider's Audit Report)** — 싱가포르은행협회(Association of Banks in Singapore, ABS)가 제정한 감사 프레임워크로, 외부 감사인이 클라우드 등 아웃소싱 서비스 제공자의 통제를 ABS 가이드라인 기준으로 검증한 보고서입니다. 금융회사는 이 OSPAR 보고서를 받아 자체 벤더 실사 자료로 활용합니다. 2024년 3월 공개된 **OSPAR v2.0**은 2025년 1월 1일부터 매년 감사를 요구하며, 클라우드 서비스 제공자(IaaS/PaaS/SaaS)에 특화된 보완 통제 기준을 추가했습니다.

주요 하이퍼스케일러는 매년 OSPAR 감사 보고서를 발간해 싱가포르 금융회사 고객이 활용할 수 있도록 제공하고 있으며, 이 보고서의 대상 서비스 범위는 매년 확대되는 추세입니다.

## 공공·금융 진출 시 게이트 성격

- **공공 조달**: IMDA 산하 정부 클라우드 조달 체계에서는 MTCS Level 3 인증이 사실상의 참가 조건으로 작용합니다. 인증이 없는 벤더나 서비스는 입찰 참여 자체가 제한될 수 있습니다.
- **금융권**: MTCS 인증은 출발점일 뿐이며, 실제 도입 여부는 MAS TRM 가이드라인 준수 여부와 OSPAR 감사 보고서 확보 여부로 결정되는 경우가 많습니다. 도입 초기 단계에서 벤더의 최신 OSPAR 보고서를 요청해 감사 범위와 예외 사항을 확인하는 절차를 권장합니다.
- **실무 시사점**: 자국에서 이미 별도의 클라우드 보안 인증 체계에 익숙한 아키텍트라도(예: 한국의 CSAP·ISMS-P), 싱가포르는 별도의 인증 체계(MTCS)와 별도의 금융권 감사 체계(OSPAR)를 운영한다는 점에 유의해야 합니다. 두 체계는 상호 인정되지 않으므로, 싱가포르 진출 시에는 별도의 인증·감사 취득 로드맵을 세워야 합니다.

## 도입 전 확인 체크리스트

- **등급과 범위를 함께 확인**: 벤더가 제시하는 인증서에서 등급(Level)뿐 아니라 인증 대상 서비스 목록·리전이 실제 도입하려는 서비스와 일치하는지 확인합니다. IMDA 공식 웹사이트에 게시된 인증서(QR 코드 포함)로 유효성을 교차 검증할 수 있습니다.
- **갱신 주기 추적**: MTCS 인증은 3년 주기이며 매년 사후관리 심사를 거칩니다. 장기 계약을 체결할 경우 벤더의 최근 갱신·사후관리 이력을 계약 조건이나 SLA 부속서에 반영하는 것을 권장합니다.
- **금융권은 OSPAR를 별도로 요청**: MTCS Level 3 인증만으로는 MAS 규제 대응이 완결되지 않습니다. 벤더의 최신 OSPAR 보고서(v2.0 기준)를 별도로 확보해 감사 범위·예외 사항·통제 미비점(만약 있다면)을 내부 리스크 평가에 반영해야 합니다.
- **공공 조달은 사전 협의**: 정부 조달 참여를 목표로 한다면, IMDA·발주 기관과 사전 협의를 통해 요구되는 정확한 인증 등급과 범위를 확인하는 것이 좋습니다. 조달 공고마다 요구 수준이 달라질 수 있습니다.

## 참고하기

- [Cloud Computing and Services — Infocomm Media Development Authority (IMDA)](https://www.imda.gov.sg/regulations-and-licensing-listing/ict-standards-and-quality-of-service/it%20standards%20and%20frameworks/cloud%20computing%20and%20services)
- [MTCS Tier 3 — AWS Compliance](https://aws.amazon.com/compliance/aws-multitiered-cloud-security-standard-certification/)
- [AWS renews MTCS Level 3 certification under the SS584:2020 standard — AWS Security Blog](https://aws.amazon.com/blogs/security/aws-renews-mtcs-level-3-certification-under-the-ss5842020-standard)
- [Multi-Tier Cloud Security (MTCS) Standard for Singapore — Microsoft Learn](https://learn.microsoft.com/en-us/compliance/regulatory/offering-mtcs-singapore)
- [MTCS — Compliance | Google Cloud](https://cloud.google.com/security/compliance/mtcs)
- [Oracle's MTCS certification creates new opportunities for customers in Singapore — Oracle Cloud Infrastructure Blog](https://blogs.oracle.com/cloud-infrastructure/oracle-mtcs-certification-creates-new-opportunities-for-customers-in-singapore)
- [MAS Enhances Guidelines to Combat Heightened Cyber Risks — Monetary Authority of Singapore](https://www.mas.gov.sg/news/media-releases/2021/mas-enhances-guidelines-to-combat-heightened-cyber-risks)
- [OSPAR (Singapore) — Microsoft Azure Compliance](https://learn.microsoft.com/en-us/azure/compliance/offerings/offering-ospar-singapore)
- [OSPAR — Compliance | Google Cloud](https://cloud.google.com/security/compliance/ospar)
- [ABS OSPAR Guidelines v2.0 — Association of Banks in Singapore](https://abs.org.sg/docs/library/abs-ospar-guidelines-v2-0.pdf)
