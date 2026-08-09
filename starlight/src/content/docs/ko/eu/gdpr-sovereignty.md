---
title: "GDPR과 데이터 주권"
description: "GDPR 역외이전 체계, EU Data Boundary, 소버린 클라우드 옵션 비교와 EUCS 인증 스킴 동향을 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

GDPR(General Data Protection Regulation, EU 일반 개인정보보호법)은 2018년 시행 이후에도 계속 진화하고 있습니다. 최근 몇 년의 변화는 법 조문 자체보다 **"개인정보가 물리적으로 어디서, 누구에 의해 처리되는가"** 에 대한 요구가 강화되는 방향으로 나타납니다. 이 문서는 비EU 기업이 EU로 클라우드 워크로드를 확장하거나 EU 고객 데이터를 처리할 때 마주치는 역외이전 체계와, 이를 배경으로 등장한 "소버린 클라우드(Sovereign Cloud)" 옵션들을 정리합니다.

## GDPR 역외이전 체계

GDPR 제5장(Chapter V)은 EU 역외로의 개인정보 이전에 별도의 안전장치를 요구합니다. 실무에서 쓰이는 주요 메커니즘은 다음과 같습니다.

| 메커니즘 | 설명 |
| --- | --- |
| **적정성 결정 (Adequacy Decision)** | EU 집행위원회가 특정 국가의 개인정보 보호 수준을 GDPR과 동등하다고 인정하면, 해당 국가로의 이전에는 추가 안전장치가 필요 없음 |
| **표준계약조항 (SCC, Standard Contractual Clauses)** | 적정성 결정이 없는 국가로 이전할 때 계약 당사자 간 체결하는 EU 집행위원회 승인 표준 조항. 2021년 개정판이 현재 기준 |
| **BCR (Binding Corporate Rules)** | 다국적 기업 그룹 내부 이전에 적용하는 구속력 있는 사내 규칙 |

### 한국의 적정성 결정 (2021)

한국은 2021년 12월 17일 EU 집행위원회로부터 **적정성 결정**을 받았습니다. 개인정보보호위원회와 EU 간 협상이 2021년 3월 타결되었고, 같은 해 12월 정식 채택되었습니다.

:::caution
**한국의 적정성 결정은 EU → 한국 방향으로만 적용됩니다.** 즉 EU에서 한국으로 개인정보를 이전할 때는 SCC 등 별도 안전장치 없이 이전이 가능하지만, 반대 방향(한국 기업이 EU 거주자 개인정보를 직접 수집·처리하는 경우, 즉 GDPR 역외적용 대상이 되는 경우)에는 GDPR 자체의 준수 의무가 별도로 적용됩니다. 적정성 결정이 GDPR 준수 의무 자체를 면제해주는 것은 아닙니다.
:::

비EU 기업이 EU 리전의 클라우드를 사용해 EU 고객 데이터를 처리하는 경우, 이전 방향과 무관하게 벤더와의 계약(DPA, Data Processing Addendum)에 SCC가 포함되어 있는지, 그리고 벤더가 제공하는 리전·거버넌스 옵션이 자사의 데이터 분류 요건을 충족하는지를 확인해야 합니다.

## EU Data Boundary

**EU Data Boundary**는 Microsoft가 추진해 온 데이터 레지던시 강화 이니셔티브로, EU·EFTA 고객의 데이터를 EU/EFTA 역내에서만 저장·처리하는 것을 목표로 합니다.

- **2023년 1월**: 1단계 — Microsoft 365, Dynamics 365, Power Platform 등 핵심 클라우드 서비스의 고객 데이터·가명처리된 개인정보를 EU 역내 저장
- **2025년 2월 26일**: 완성(3단계) — 지원 로그, 케이스 노트 등 **전문 서비스 데이터(Professional Services Data)** 까지 EU/EFTA 역내 저장으로 확장, 데이터 레지던시·투명성 강화 완료 발표 (단, 일부 운영상 제한된 역외 접근·전송 예외는 문서화된 조건 하에 남아 있음)

다른 벤더들도 유사한 방향의 리전 내 데이터 처리 보장을 확장하고 있으나, "EU Data Boundary"라는 명칭과 범위(전문 서비스 데이터 포함)는 Microsoft 고유의 이니셔티브입니다. 다른 벤더의 EU 리전 데이터 레지던시 보장 범위는 각 벤더의 계약 문서(DPA)에서 개별 확인이 필요합니다.

## 소버린 클라우드 옵션 비교

데이터 저장 위치를 넘어 **운영 인력·관리 접근·긴급 상황 시 법적 관할**까지 EU 역내로 제한하려는 수요에 대응해, 주요 벤더가 다음과 같은 "소버린 클라우드" 옵션을 운영·발표했습니다.

| 벤더 | 옵션 | 형태 | 현황 |
| --- | --- | --- | --- |
| **AWS** | European Sovereign Cloud | 독립 리전(물리·논리적으로 기존 AWS 리전과 분리) | 2026년 1월 15일 정식 출시(GA), 독일 브란덴부르크가 첫 리전. 장기 78억 유로 투자 발표, 벨기에·네덜란드·포르투갈에 소버린 Local Zone 확장 예정 |
| **Microsoft** | Bleu (프랑스) / Delos Cloud (독일) | 파트너 운영 소버린 클라우드 (내셔널 파트너 클라우드) | Bleu는 Orange·Capgemini 합작사(SecNumCloud 인증 목표), Delos Cloud는 SAP 자회사. 2025년 11월 상호 지원 협약 체결, Delos-Microsoft 간 MoU로 비상 시(타국 정부의 서비스 제한 등) Delos가 Microsoft 클라우드 코드에 접근할 법적 권리 확보 |
| **OCI** | EU Sovereign Cloud | 물리적으로 분리된 EU 전용 리전 | 2023년 6월부터 운영 중, 프랑크푸르트·마드리드 리전. EU 법인·EU 거주 인력만 운영, 상용 OCI 대비 추가 요금 없음 |
| **Google Cloud** | 주권 파트너십 (T-Systems·Thales/S3NS·Proximus) | 파트너사 운영 리전 | 독일은 T-Systems, 프랑스는 Thales 자회사 S3NS(SecNumCloud 목표), 벨기에·룩셈부르크는 Proximus와 협력. 2026년 5월 Thales-Google Cloud가 독일 신규 소버린 클라우드 파트너십 발표 |

:::note
"소버린 클라우드"는 벤더마다 정의와 범위가 다릅니다 — 데이터 저장 위치만 보장하는 수준부터, 운영 인력·키 관리·비상 시 법적 접근권까지 포함하는 수준까지 폭이 넓습니다. 도입 전 각 벤더가 구체적으로 무엇을 EU 역내로 제한하는지(저장 vs 처리 vs 운영 접근 vs 지배구조)를 계약 문서에서 확인해야 합니다.
:::

## EUCS 인증 스킴의 유동성

**EUCS(European Cybersecurity Certification Scheme for Cloud Services)** 는 ENISA가 주도하는 클라우드 서비스 공통 보안 인증 체계로, 원래 클라우드 벤더의 보안 수준을 EU 전역에서 상호 인정 가능한 등급(Basic/Substantial/High)으로 표준화하려는 목적이었습니다.

:::caution
**EUCS의 "주권성(Sovereignty) 요건"은 2026년 8월 현재까지 확정되지 않고 논쟁이 진행 중입니다.**

- 초기 초안은 최고 등급(High+) 인증에 EU 역외 기업의 지분·지배구조 배제(immunity) 요건을 포함했습니다.
- 2023년 개정 초안은 이를 완화해 High+ 등급에서만 데이터 현지화를 요구하고, "신뢰할 수 있는 역외 클라우드 제공자" 인증 가능성을 열어두었습니다.
- 2026년 1월 20일 EU 집행위원회가 발표한 **Cybersecurity Act 2(CSA2) 개정안**은 인증 체계를 기술적 기준 중심으로 재편하는 방향을 제시했으며, 이 흐름 속에서 EUCS·EU5G 스킴 작업이 재개될 것으로 예상됩니다.
- EUCS 최종안은 여전히 확정되지 않았으며, "주권성 요건을 포함할 것인가"는 EU 회원국 간 이견이 남아있는 사안입니다. **최신 확정 여부는 ENISA·EU 집행위원회 공식 발표를 통해 별도 확인이 필요합니다.**
:::

EUCS는 아직 자발적(voluntary) 인증이지만, NIS2와 Data Act(2024년 1월 발효, 2025년 9월부터 핵심 조항 적용 중)는 회원국·규제 당국이 공공기관·필수/중요 기관에게 EUCS 인증 벤더 사용을 의무화할 수 있는 권한을 부여하고 있어, 향후 조달 요건에 영향을 줄 가능성이 있습니다.

## 아키텍처 시사점

- **데이터 분류부터 시작**: 어떤 데이터가 EU 역내 저장·처리 의무 대상인지(공공조달 요건, 계약상 요구, 자체 리스크 정책)를 먼저 분류한 뒤 리전·벤더 옵션을 결정합니다.
- **소버린 옵션은 비용·기능 트레이드오프를 동반**: 소버린 리전은 일반 상용 리전 대비 서비스 가용 범위가 제한적이거나 신규 기능 반영이 늦을 수 있습니다. 필수 요건이 아니라면 일반 EU 리전 + 강화된 거버넌스(암호화, 접근 투명성 로그)로 충분한 경우가 많습니다.
- **DPA·계약서 검토가 리전 선택만큼 중요**: SCC 포함 여부, 하위 처리자(sub-processor) 목록, 비상 접근 조항을 계약 문서에서 직접 확인합니다.
- **EUCS 등 유동적 규제는 "확정 전제"로 설계하지 않기**: 최종 확정되지 않은 인증 요건을 아키텍처의 필수 전제 조건으로 삼기보다, 확정 시 전환 가능한 여지를 남겨둡니다.
- **소버린 랜딩존 설계와 연계**: EU 데이터 레지던시·처리 관할 요건을 랜딩존 가드레일에 반영하는 구체적 패턴은 [랜딩존 — 소버린 랜딩존](../../governance/landing-zone/#소버린-랜딩존-sovereign-landing-zone)을 참고하세요.

## 참고하기

- [EUR-Lex — GDPR (Regulation (EU) 2016/679)](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [EU 집행위원회 — 적정성 결정 Q&A (한국)](https://ec.europa.eu/commission/presscorner/detail/en/qanda_21_6916)
- [EU 집행위원회 — 데이터 보호 적정성 결정 목록](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en)
- [EDPB — 한국 적정성 결정 초안 의견](https://edpb.europa.eu/news/news/2021/edpb-adopts-opinion-draft-south-korea-adequacy-decision_en)
- [Microsoft — EU Data Boundary 완성 발표 (2025.2)](https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/)
- [AWS — European Sovereign Cloud 출시 발표 (2026.1)](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe)
- [Microsoft — 유럽 주권 솔루션 발표 (2025.6)](https://blogs.microsoft.com/blog/2025/06/16/announcing-comprehensive-sovereign-solutions-empowering-european-organizations/)
- [Google Cloud — Sovereign Cloud](https://cloud.google.com/sovereign-cloud)
- [Oracle — Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)
