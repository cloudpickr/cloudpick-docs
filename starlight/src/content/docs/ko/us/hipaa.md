---
title: "HIPAA/HITECH"
description: "미국 헬스케어 데이터 보호 규제 HIPAA/HITECH의 PHI 정의, BAA 체결 구조, HITRUST CSF와의 관계, 암호화·감사 로그 요건을 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

HIPAA(Health Insurance Portability and Accountability Act, 1996)는 미국의 헬스케어 정보 보호 연방법으로, HHS(보건복지부) 산하 OCR(민권실, Office for Civil Rights)이 집행을 담당합니다. 2009년 제정된 HITECH(Health Information Technology for Economic and Clinical Health Act)는 전자 의료 기록 확산에 맞춰 HIPAA의 집행력을 강화하고, 데이터 유출 시 통지 의무(Breach Notification Rule)를 신설했습니다. 두 법은 통상 함께 "HIPAA/HITECH"로 묶여 언급됩니다.

HIPAA는 단일 인증 제도가 아니라 준수해야 할 법적 요건 체계이며, "HIPAA 인증"이라는 공식 자격은 존재하지 않습니다. 조직 스스로 요건을 충족하고 이를 문서·감사로 입증하는 구조입니다.

## PHI(보호대상 건강정보) 정의

PHI(Protected Health Information)는 다음 조건을 모두 만족하는 정보를 말합니다.

- 의료 제공자, 건강보험, 고용주, 의료 정보 교환기관 등이 생성·수령한 정보
- 개인의 과거·현재·미래의 신체적·정신적 건강 상태, 의료 서비스 제공, 그에 대한 비용 지불과 관련된 정보
- 개인을 특정할 수 있는(individually identifiable) 정보

전자 형태(ePHI)뿐 아니라 서면 기록, 검사 결과, 영상, 청구서, 심지어 개인 식별 정보가 포함된 구두 대화까지 포함됩니다. 클라우드 아키텍처 관점에서는 주로 ePHI가 저장·전송·처리 대상이 됩니다.

## Covered Entity, Business Associate, BAA 체결 구조

HIPAA는 규제 대상을 두 그룹으로 나눕니다.

- **Covered Entity(적용 대상 기관)**: 의료를 제공하거나 비용을 지불하는 기관 — 의료 제공자, 건강보험사, 의료 정보 교환기관
- **Business Associate(업무 위탁 대상자)**: Covered Entity를 대신해 PHI를 수집·저장·전송하는 제3자 — 클라우드 벤더, SaaS 제공사, 데이터 처리 업체가 대부분 여기 해당

Covered Entity가 PHI 처리를 외부에 위탁할 때는 **BAA(Business Associate Agreement)**라는 법적 계약을 반드시 체결해야 하며, BAA는 Business Associate가 PHI를 어떤 목적으로 다룰 수 있는지, 어떤 보안·프라이버시 요건을 준수해야 하는지를 명시합니다. Business Associate가 다시 하위 벤더(Subcontractor)에 위탁하는 경우에도 동일하게 하위 BAA 체결이 필요합니다.

:::note
클라우드 서비스 제공자는 대부분 Business Associate 지위로 간주됩니다. 즉 클라우드 벤더와 BAA를 체결하는 것이 PHI를 해당 클라우드에 올리기 위한 법적 전제 조건입니다.
:::

## 벤더별 BAA 적용 서비스 범위 확인법

주요 클라우드 벤더는 표준 계약의 일부로 BAA를 제공하지만, **BAA 체결이 모든 서비스를 자동으로 커버하는 것은 아닙니다.**

- **AWS**: AWS Artifact를 통해 계정 단위로 BAA를 체결할 수 있으며, "HIPAA 적격(HIPAA-eligible) 서비스" 목록에 포함된 서비스만 BAA 보호 범위에 들어갑니다.
- **Azure**: 표준 온라인 서비스 약관(Online Services Terms)의 일부로 BAA를 제공하며, 상대적으로 폭넓은 서비스를 포괄하는 것으로 알려져 있으나 역시 서비스별 목록 확인이 필요합니다.
- **Google Cloud**: 표준 약관을 통해 BAA를 제공하며, 지정된 적격 서비스만 대상입니다.

아키텍처 설계 시 반드시 각 벤더의 최신 "HIPAA 적격 서비스 목록" 공식 페이지에서 사용하려는 서비스가 포함되어 있는지 확인해야 하며, 목록에 없는 서비스로 PHI를 처리·저장하면 BAA 보호를 받지 못합니다. 또한 BAA는 책임 공유 모델의 벤더 측 몫만 다루므로, 서비스를 안전하게 구성하고 PHI 접근을 제한하며 암호화하는 것은 여전히 고객(Covered Entity/Business Associate)의 책임입니다.

## HITRUST CSF와의 관계

HITRUST CSF는 정부가 아닌 민간 조직(HITRUST Alliance)이 운영하는 보안 프레임워크로, HIPAA를 포함한 40여 개 보안·규제 표준을 하나로 통합해 제공합니다.

- HIPAA는 법이고, HITRUST CSF는 그 법을 포함한 여러 표준을 준수하기 위한 실무적 프레임워크입니다.
- HITRUST CSF 인증을 받는다고 자동으로 "HIPAA 준수"가 되는 것은 아니지만(HIPAA에는 애초에 공식 인증 제도가 없음), 제3자 감사를 거친 HITRUST 인증은 HIPAA 요건을 충족하고 있다는 강력한 정황 증거로 널리 활용됩니다.
- 미국 병원의 상당수와 건강보험사 다수가 HITRUST를 벤더 평가·자체 준수 입증 수단으로 채택하고 있어, 헬스케어 SaaS를 미국 엔터프라이즈 고객에게 판매하려는 경우 HITRUST CSF 인증이 사실상의 시장 요구 사항으로 작동하는 경우가 많습니다.

## 암호화·감사 로그 요건

현행 HIPAA Security Rule은 다수의 보호조치를 "필수(Required)"와 "권장(Addressable, 대안 채택 가능)"으로 구분해 왔습니다. 그러나 HHS는 2024년 12월(연방관보 게재 2025년 1월) 이 구분을 없애고 대부분의 보호조치를 의무화하는 개정안(NPRM)을 발표했습니다.

:::caution
이 개정안은 2026년 8월 현재 **확정되지 않았습니다.** 2025년 3월 의견수렴이 종료된 이후, OMB Unified Agenda 기준 최종 규칙 목표 시점이 2027년 7월로 재조정된 상태입니다. 아래 내용은 제안 단계이며, 실제 시행 여부·시점은 HHS 공식 발표로 재확인이 필요합니다.
:::

제안된 주요 변경 사항:

- ePHI의 저장(at rest) 및 전송(in transit) 시 암호화를 원칙적으로 의무화(제한적 예외만 허용)
- PHI 시스템 접근에 대한 다중 인증(MFA) 의무화
- 실시간에 가까운 자동화된 감사 로그 모니터링, 로그 보호 통제 강화
- 로그 장기 보관 강화 — 기존 6년 보존 요건은 정책·절차 등 문서에 적용되는 것이며, 이를 로그 영역까지 확장하려는 제안
- 최소 6개월 주기 취약점 스캔, 연 1회 침투 테스트

개정안 확정 여부와 무관하게, 저장·전송 구간 암호화와 접근 로그 기록은 이미 업계 표준 관행으로 자리 잡고 있어 신규 아키텍처에는 선제적으로 반영하는 것이 안전합니다.

## 헬스케어 SaaS 아키텍처 시사점

- **적격 서비스만 사용**: PHI가 흘러가는 모든 서비스가 벤더의 BAA 적격 목록에 포함되는지 설계 단계에서부터 확인합니다.
- **암호화 기본값화**: 현재 규정이 "권장"으로 분류하더라도 저장·전송 구간 암호화를 기본 아키텍처 요건으로 채택합니다. 향후 의무화에 대비할 수 있습니다.
- **접근 통제와 감사 로그**: PHI 접근 최소 권한 원칙, MFA, 중앙 집중식 감사 로그(SIEM 연동) 및 장기 보관 정책을 갖춥니다. 관련 아키텍처는 [데이터 보호와 워크로드 보안](../../security/data-protection/) 및 [보안 인시던트 대응](../../security/incident-response/) 참고.
- **HITRUST 인증 고려**: 미국 헬스케어 엔터프라이즈 고객 대상 영업 시 HITRUST CSF 인증이 사실상 필요 조건이 되는 경우가 많으므로, 초기부터 인증 획득 로드맵을 고려합니다.
- **하위 벤더 BAA 체인 관리**: 자사가 사용하는 모든 하위 클라우드·SaaS 벤더와 BAA 체결 여부를 계약 관리 차원에서 추적합니다.

## 참고하기

- [HHS HIPAA 공식 페이지](https://www.hhs.gov/hipaa/)
- [HHS Covered Entities and Business Associates](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html)
- [HHS HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [AWS HIPAA 컴플라이언스](https://aws.amazon.com/compliance/hipaa-compliance/)
- [Microsoft Azure HIPAA/HITECH](https://learn.microsoft.com/azure/compliance/offerings/offering-hipaa-us)
- [Google Cloud HIPAA 컴플라이언스](https://cloud.google.com/security/compliance/hipaa)
- [HITRUST Alliance](https://hitrustalliance.net/)
