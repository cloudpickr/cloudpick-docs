---
title: "EU 회원국별 클라우드 보안 스킴"
description: "독일 BSI C5, 프랑스 ANSSI SecNumCloud, 스페인 ENS, 이탈리아 ACN 등 EU 회원국 클라우드 보안 인증·조달 스킴과 하이퍼스케일러 대응 현황을 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

EU 차원의 통일된 클라우드 보안 인증 스킴(EUCS)이 아직 확정되지 않은 상태에서, 개별 회원국은 각자의 국가 스킴으로 공공조달·규제산업 클라우드 이용을 통제하고 있습니다. 독일의 BSI C5, 프랑스의 ANSSI SecNumCloud가 가장 성숙하고 국제적으로도 참조되는 스킴이며, 스페인 ENS와 이탈리아 ACN 체계도 각자의 방식으로 자국 공공부문 클라우드 조달을 게이트키핑합니다. 이 문서는 EU 시장에 공공·규제산업 워크로드를 배포하려는 아키텍트가 국가별로 무엇을 준비해야 하는지 정리합니다.

:::note
국가 스킴은 **EU 규정(Regulation)이 아니라 각국 법령·행정 절차**에 근거합니다. 따라서 특정 회원국에서 통과한 인증이 다른 회원국에서 자동으로 인정되지는 않으며, 스킴 간 상호 인정은 EUCS 등 EU 차원 프레임워크가 완성되어야 가능해집니다.
:::

## 독일 — BSI C5

**C5(Cloud Computing Compliance Criteria Catalogue)** 는 독일 연방정보보안청(BSI, Bundesamt für Sicherheit in der Informationstechnik)이 운영하는 클라우드 보안 준수 기준 카탈로그입니다.

- **C5:2020**: 121개 기준으로 구성되며, 2020년 이후 사실상 독일의 표준 클라우드 보안 감사 기준으로 자리 잡았습니다. ENISA가 EUCS Substantial 등급 요건을 설계할 때 C5:2020을 기초 자료로 삼았습니다.
- **C5:2026**: 2026년 4월 초(일부 보도는 3월 말로 표기)에 최종본이 공개된 개정판으로, C5:2020의 기준을 계승하면서 168개 기준(17개 영역)으로 세분화·확장했습니다. **새 기준은 2027년 6월 1일부터 시작하는 평가 기간부터 구속력을 가지며**, 그 이전에도 조기 적용은 허용됩니다.
- **조달상 지위**: C5는 법률이 아니므로 위반 시 직접적 법적 제재는 없지만, **독일 연방기관 대상 클라우드 조달에서는 C5 준수가 사실상 필수 요건**입니다. 금융·헬스케어 등 규제산업에서도 벤더 선정 시 C5 준수 여부를 표준적으로 요구합니다.
- **하이퍼스케일러 대응**: AWS, Microsoft Azure, Google Cloud, SAP, IONOS 등이 C5 준수 확인서(attestation)를 보유하고 있으며, 주요 벤더는 매년 감사를 갱신합니다.

## 프랑스 — ANSSI SecNumCloud

**SecNumCloud**는 프랑스 국가사이버보안청(ANSSI, Agence nationale de la sécurité des systèmes d'information)이 발급하는 클라우드 서비스 자격(qualification)입니다. 현재 기준은 **버전 3.2**(2022년 개정)이며, 360개 이상의 기술·운영 요구사항을 PASSI(ANSSI 승인 감사기관)가 심사합니다.

### 주권 요건이 핵심 차별점

SecNumCloud 3.2가 다른 국가 스킴과 가장 크게 다른 지점은 **자본·지배구조 주권 요건**입니다.

- 본사가 프랑스 또는 EU 역내에 있어야 하고
- EU 역외 지분은 개별 주주 기준 24%, 합산 기준 39%를 넘을 수 없으며
- 서비스에 배타적으로 EU법만 적용되어야 합니다(미국 CLOUD Act·FISA 702 등 역외 법의 데이터 접근 요구로부터 절연).

:::caution
이 요건 때문에 **AWS·Microsoft·Google 등 미국계 하이퍼스케일러는 자사 명의로는 SecNumCloud 자격을 직접 취득할 수 없습니다.** 대신 이들은 프랑스 파트너와의 합작법인을 통해 우회 경로를 취하고 있으며, 그 진행 상황은 벤더마다 다릅니다(아래 "파트너십 인증 취득 현황" 참고).
:::

### 파트너십 인증 취득 현황 (2026년 7월 기준)

| 파트너십 | 벤더 | 현황 |
| --- | --- | --- |
| **S3NS** (Thales × Google Cloud 합작사) | Google Cloud | **2025년 12월 17일 SecNumCloud 3.2 자격 취득** — PREMI3NS 서비스로 IaaS·CaaS·PaaS 20여 개 서비스를 동시에 인증받은 최초 사례. 2026년 상반기 중 Cloud Run·Cloud Build·Cloud Spanner·Bigtable 등을 포함한 2차 확장 심사 진행 중 |
| **Bleu** (Capgemini × Orange 합작사) | Microsoft Azure/M365 | 심사 1단계(J0, 신청 접수)를 통과했으며 2026년 상반기 자격 취득을 목표로 심사 진행 중. **2026년 8월 현재 완전한 SecNumCloud 3.2 자격은 아직 취득하지 않음** |

전체적으로 2026년 7월 기준 자격 보유 사업자는 **9~10개**(OVHcloud, 3DS Outscale, Cloud Temple, Orange Business, Cegedim.cloud, Worldline, Oodrive, Whaller, S3NS 등 — ANSSI 공식 카탈로그의 서비스 유형별 집계 기준으로는 10개 사업자명까지 확인됨)이며, Bleu·Scaleway·NumSpot 등 **12개 사업자**가 심사 진행 중입니다.

## 스페인 — ENS

**ENS(Esquema Nacional de Seguridad, 국가보안체계)** 는 왕령(Royal Decree) 311/2022에 근거해 스페인 공공부문 정보시스템에 요구되는 보안 프레임워크로, **기본(Basic)·중간(Medium)·상(High)** 3단계로 구성됩니다.

- 스페인 공공기관과 계약하려는 클라우드 벤더는 취급 정보의 민감도에 따라 해당 등급의 ENS 인증을 요구받습니다.
- **하이퍼스케일러 대응**: AWS(174개 서비스, 31개 리전 대상 ENS High 갱신 인증), Microsoft Azure(BDO 감사를 통한 ENS High 준수 확인), Google Cloud(Google Cloud·Google Workspace ENS High 인증)가 모두 **최고 등급인 ENS High 인증을 보유**하고 있습니다. 이는 자본 주권 요건을 두는 SecNumCloud와 달리, ENS가 기술·운영 보안 통제 중심 스킴이기 때문입니다.

## 이탈리아 — ACN과 국가전략클라우드(PSN)

이탈리아는 독일·프랑스와 달리 **인증형 스킴과 물리적 소버린 인프라를 결합**한 이원 구조를 취합니다.

1. **ACN 클라우드 자격분류(qualificazione)**: 2023년 1월 19일부터 국가사이버보안청(ACN, Agenzia per la Cybersicurezza Nazionale)이 AgID로부터 업무를 이관받아 공공부문 클라우드 서비스 자격분류를 담당합니다. 기밀성·무결성·가용성 영향도를 평가하는 설문 기반 절차로, 공공기관이 사용할 클라우드 서비스·인프라의 위험 등급을 분류합니다. "Strategia Cloud Italia"의 일환으로 이탈리아 공공행정의 약 75%를 자격분류된 클라우드로 이전하는 것이 목표입니다.
2. **PSN(Polo Strategico Nazionale, 국가전략클라우드)**: 최고 수준의 신뢰성·복원력이 요구되는 공공 워크로드를 위한 물리적 소버린 인프라입니다. "Public Cloud PSN Managed" 구성을 통해 하이퍼스케일러 플랫폼을 PSN 데이터센터 내 공공행정 전용 리전으로 편입시켜, 레거시 전환이 필요한 기관도 단계적으로 이전할 수 있게 합니다. **2026년 7월 21일 기준 280개 이상의 중앙행정기관·지역보건기구·병원기관이 PSN으로 이전을 완료**했습니다(PNRR 목표 달성).

:::note
이탈리아 모델에서는 하이퍼스케일러가 ACN으로부터 **독일 C5·프랑스 SecNumCloud 방식의 개별 자격증을 직접 취득**하기보다, **PSN이라는 이탈리아 통제 하의 물리적 게이트웨이를 통해 서비스를 제공**하는 방식에 가깝습니다. 개별 서비스 단위의 인증 범위는 벤더·PSN 공식 발표로 별도 확인이 필요합니다.
:::

## EUCS와의 관계 — 통합 논의는 진행 중

위 4개 국가 스킴은 각자 독자적으로 운영되지만, EU 차원의 **EUCS(European Cybersecurity Certification Scheme for Cloud Services)** 가 완성되면 상호 인정의 기초가 될 것으로 예상됩니다.

- C5:2020은 EUCS Substantial 등급 요건 설계의 기초 자료로 이미 반영되었습니다.
- EUCS 작업은 최고 등급(High+)의 "주권성 요건" 포함 여부를 둘러싼 회원국 간 이견으로 수년간 정체되었다가, 2026년 1월 20일 발표된 **Cybersecurity Act 2(CSA2)** 개정 흐름 속에서 재개되는 중입니다.
- **2026년 8월 현재 EUCS는 여전히 확정되지 않았고, 주권성 요건 포함 여부는 논쟁이 진행 중입니다.** (자세한 경과는 [GDPR과 데이터 주권 — EUCS 인증 스킴의 유동성](../../eu/gdpr-sovereignty/#eucs-인증-스킴의-유동성) 참고)

그때까지 국가 스킴은 "잠정적이지만 시장에서 신뢰받는 증빙"으로 기능하며, 특히 BSI C5와 SecNumCloud는 EUCS 전환기의 사실상 기준으로 참조되고 있습니다.

## 국가별 조달 게이트 — 요약

국가 스킴은 인증 자체가 목적이 아니라 **공공·규제산업 조달의 통과 요건**으로 기능한다는 공통점이 있습니다. 다만 게이트의 성격은 국가마다 다릅니다.

| 국가 | 스킴 | 성격 | 하이퍼스케일러 직접 취득 가능 여부 |
| --- | --- | --- | --- |
| 독일 | BSI C5 | 기술·운영 통제 감사 (자본 요건 없음) | 가능 — AWS·Azure·Google Cloud 등 취득 완료 |
| 프랑스 | SecNumCloud 3.2 | 기술·운영 통제 + **자본·지배구조 주권 요건** | 불가 — 파트너십(S3NS는 취득 완료, Bleu는 심사 중) 경유 필요 |
| 스페인 | ENS (Basic/Medium/High) | 기술·운영 통제 감사 (자본 요건 없음) | 가능 — AWS·Azure·Google Cloud 모두 ENS High 취득 |
| 이탈리아 | ACN 자격분류 + PSN | 설문 기반 등급분류 + 물리적 소버린 인프라 결합 | PSN 파트너십 경유 방식 |

## 실무 시사점

- **국가별로 별도 검토가 필요합니다.** EU 단일 인증이 없는 현재, "EU 진출"을 단일 요건으로 뭉뚱그리지 말고 목표 회원국(공공조달 상대·규제 당국)별로 요구 스킴을 개별 확인해야 합니다.
- **프랑스향 워크로드는 벤더 선택 자체가 제약됩니다.** 프랑스 공공기관·중요 인프라 사업자(OIV/OSE) 대상 민감 데이터를 다룬다면, SecNumCloud 자격을 직접 보유했거나(S3NS 등) 취득이 임박한 벤더로 선택지가 좁혀집니다. Bleu처럼 심사 진행 중인 옵션은 **완전 자격 취득 시점을 계약·마이그레이션 일정에 전제하지 않아야** 합니다.
- **독일·스페인은 상대적으로 하이퍼스케일러 선택 폭이 넓습니다.** 자본 주권 요건이 없는 두 스킴은 이미 주요 벤더가 최고 등급 인증을 보유하고 있어, 벤더 선정보다는 인증 범위(서비스 목록)와 리전 커버리지 확인이 실무의 핵심입니다.
- **이탈리아는 인증서가 아니라 인프라 경로를 확인해야 합니다.** ACN 자격분류 등급과 함께, 워크로드가 PSN 경유로 제공되는지, 그 경우 운영 통제·SLA가 어떻게 달라지는지를 벤더·PSN 공식 문서에서 확인합니다.
- **국가 스킴을 EUCS 확정의 임시 대체재로 활용하되, 고정 전제로 설계하지 않습니다.** EUCS가 최종 확정되면 상호 인정 범위나 요건이 바뀔 수 있으므로, 특정 국가 스킴에만 의존하는 아키텍처보다 전환 여지를 남긴 설계가 안전합니다.

## 참고하기

- [BSI — C5 소개](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/C5_Einfuehrung/C5_Einfuehrung_node.html)
- [BSI — C5:2026 카탈로그](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/C5_2025/C5_2025_node.html)
- [cyber.gouv.fr — SecNumCloud (ANSSI)](https://cyber.gouv.fr/)
- [Thales — S3NS SecNumCloud 자격 취득 발표 (2025.12)](https://www.thalesgroup.com/en/news-centre/press-releases/s3ns-announces-secnumcloud-qualification-premi3ns-its-trusted-cloud)
- [Bleu — SecNumCloud 3.2 J0 심사 통과 공지](https://www.bleucloud.fr/bleu-valide-le-j0-de-la-qualification-secnumcloud-3-2/)
- [AWS — Esquema Nacional de Seguridad(ENS) 준수](https://aws.amazon.com/compliance/esquema-nacional-de-seguridad)
- [Google Cloud — ENS 준수](https://cloud.google.com/security/compliance/ens)
- [ACN — Strategia Cloud Italia / 클라우드 자격분류](https://www.acn.gov.it/en/strategia/strategia-cloud-italia/qualificazione-cloud)
- [Polo Strategico Nazionale 공식 사이트](https://www.polostrategiconazionale.it/en/)
- [ENISA — EUCS 후보 스킴](https://certification.enisa.europa.eu/)
- [ANSSI — SecNumCloud 인증·자격 카탈로그](https://messervices.cyber.gouv.fr/visas/catalogue-produits-services-profils-de-protection-sites-certifies-qualifies-agrees-anssi.pdf)
