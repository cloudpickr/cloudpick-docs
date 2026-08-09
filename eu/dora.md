---
description: DORA의 적용 대상, CTPP 지정 현황, ICT 리스크 관리·집중리스크·출구전략 요건을 정리합니다.
---

# DORA (금융 디지털 운영 복원력법)

> 문서 기준: 2026년 8월

## 개요

**DORA(Digital Operational Resilience Act, 디지털 운영 복원력법)** 는 EU 금융권의 ICT 리스크 관리를 표준화하는 규정입니다. 한국 금융기관의 EU 현지법인·지점, EU 금융기관에 클라우드·ICT 서비스를 제공하는 벤더, 그리고 이들과 계약하는 국내 IT 공급사 모두 DORA의 영향권에 들 수 있습니다. DORA는 규정(Regulation)이므로 각 회원국의 별도 입법 없이 EU 전역에 직접 적용됩니다.

## 적용 개시와 대상

DORA는 2023년 1월 16일 발효되었고, **2025년 1월 17일부터 적용**되었습니다.

- **대상 금융기관**: 은행, 보험사, 투자회사, 결제기관, 암호자산 서비스 제공자 등 20개 유형(EU 집행위 2026년 검토 문서 기준), 약 2만여 개로 추산되는 EU 규제 금융기관. 감독은 EBA(유럽은행감독청)·EIOPA(유럽보험연금감독청)·ESMA(유럽증권시장감독청), 즉 **ESAs(European Supervisory Authorities)** 가 유형별로 분담합니다.
- **대상 ICT 제3자 제공자**: 위 금융기관에 "중요하거나 필수적인 기능"을 지원하는 ICT 서비스 제공자(클라우드, 데이터센터, 소프트웨어 벤더 등)도 간접적으로 DORA 요건의 적용을 받습니다. 금융기관이 이들과 맺는 계약에 DORA가 요구하는 조항(접근권, 감사권, 종료 조항 등)을 반영해야 하기 때문입니다.

{% hint style="info" %}
DORA는 벤더의 본사 소재지와 무관하게, **EU 금융기관과 계약 관계에 있는 모든 ICT 제3자 제공자**에게 실질적으로 적용됩니다. 한국 소재 SaaS·클라우드 서비스라도 EU 금융기관 고객이 있다면 DORA 계약 요건의 상대방이 될 수 있습니다.
{% endhint %}

## CTPP 지정 현황

DORA는 시스템적으로 중요한 ICT 제3자 제공자를 **CTPP(Critical ICT Third-Party Provider, 핵심 ICT 제3자 제공자)** 로 지정해 직접 감독(oversight)하는 체계를 도입했습니다.

**2025년 11월 18일**, ESAs가 최초의 CTPP 명단을 발표했습니다. 총 **19개** 기관이 지정되었으며, **AWS, Google Cloud, Microsoft** 등 하이퍼스케일러 3사와 데이터센터 운영사, 통신사, 핀테크 전문 기업들이 포함되었습니다.

지정 기준은 다음을 종합 평가합니다.

- 장애 발생 시 시스템적 영향도
- 의존하는 금융기관의 수와 중요도
- 시장 집중도
- 대체 제공자로의 전환 가능성

**지정된 CTPP의 신규 의무**:

- EU 역외에 본사를 둔 CTPP는 지정 후 12개월 이내에 EU 자회사 설립 의무 (EU 내 조정 창구 역할)
- ESAs에 연간 감독 수수료 납부
- 리스크 평가, 인시던트 보고 등 금융기관에 준하는 수준의 규제 감독 대상화
- 위반 시 제재 가능성 노출 (기존에는 금융기관만 직접 규제 대상이었으나, DORA 이후 벤더도 직접 감독 대상이 됨)

## ICT 리스크 관리 핵심 요건

DORA가 금융기관에 요구하는 핵심 요건은 크게 다섯 갈래입니다.

| 영역 | 요건 |
| --- | --- |
| **ICT 리스크 관리 프레임워크** | 이사회 승인 하의 전사 ICT 리스크 관리 체계, 정기 검토 |
| **인시던트 분류·보고** | 중대 ICT 인시던트를 정해진 기한 내 감독기관에 보고 (초기 보고 → 중간 보고 → 최종 보고 단계) |
| **복원력 테스트** | 취약점 스캔부터 위협 기반 침투 테스트(TLPT, Threat-Led Penetration Testing)까지 등급별 테스트 |
| **ICT 제3자 리스크 관리** | 정보 등록부(Register of Information) 유지, 계약 필수 조항, 집중리스크 평가 |
| **정보 공유** | 사이버 위협 정보를 동종 기관 간 자발적으로 공유하는 체계 |

## 집중 리스크와 출구 전략

DORA에서 클라우드 아키텍처와 가장 직접적으로 연결되는 부분은 **ICT 제3자 리스크 관리** 조항입니다.

- **정보 등록부(Register of Information)**: 금융기관은 모든 ICT 제3자 계약(직접·간접, 하위 아웃소싱 포함)을 등록부로 관리하고, 감독기관 요청 시 제출해야 합니다.
- **집중리스크(Concentration Risk) 평가**: 특정 소수 벤더(특히 CTPP로 지정된 하이퍼스케일러)에 대한 과도한 의존을 정기적으로 평가해야 합니다. 단일 클라우드 벤더에 핵심 기능이 집중되어 있다면 대안 마련 계획이 필요합니다.
- **출구 전략(Exit Strategy) 문서화**: "중요하거나 필수적인 기능"을 지원하는 ICT 서비스에 대해서는 **서면 출구 전략을 수립하고 정기적으로 검증**해야 합니다. 명단에 오른 19개 CTPP와의 계약 관계가 있다면, 해당 벤더에 대한 출구 계획을 문서화하고 최소 연 1회 점검하는 것이 실무적으로 권장됩니다.

{% hint style="info" %}
집중리스크 평가와 출구 전략 수립의 구체적 방법론(자산 인벤토리, 트리거 시나리오, 이전 절차)은 [벤더 종속성과 출구 전략](../governance/exit-strategy.md)에서 다룹니다. DORA는 이 방법론이 **금융권에서는 선택이 아니라 규제 의무**라는 점을 명확히 한 사례입니다.
{% endhint %}

## 아키텍처·실무 시사점

- **멀티클라우드는 집중리스크 완화 수단이지, 목표 자체가 아닙니다.** DORA는 "여러 벤더를 써야 한다"고 규정하지 않습니다. 단일 벤더 사용이 리스크 평가·완화 계획과 함께 문서화되어 있다면 규제상 문제는 아닙니다.
- **CTPP 벤더와의 계약서에 DORA 필수 조항이 반영되었는지 확인**해야 합니다 (접근·감사권, 데이터 위치, 하위 아웃소싱 통지, 종료 지원 의무 등). 대형 벤더는 이미 DORA 대응 계약 조항(addendum)을 표준 제공하는 경우가 많습니다.
- **인시던트 대응 프로세스에 DORA 보고 기한을 반영**해야 합니다. 벤더의 인시던트 통지 SLA가 금융기관의 감독기관 보고 기한보다 느리면 규제 위반으로 이어질 수 있습니다.
- **랜딩존 설계 단계에서부터 정보 등록부용 메타데이터(계약 범위, 데이터 위치, 하위 처리자)를 체계적으로 관리**하는 것이 사후 감사보다 효율적입니다.

## 참고하기

- [EUR-Lex — DORA (Regulation (EU) 2022/2554)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- [EIOPA — Digital Operational Resilience Act](https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en)
- [ESMA — Digital Operational Resilience Act](https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/digital-operational-resilience-act-dora)
- [ESAs — 핵심 ICT 제3자 제공자(CTPP) 지정 발표 (2025.11)](https://www.lexology.com/library/detail.aspx?g=b3331558-10d0-4936-b215-4cfb1c2b33d6)
- [AWS Security Blog — DORA CTPP 지정 관련](https://aws.amazon.com/blogs/security/aws-designated-as-a-critical-third-party-provider-under-eus-dora-regulation)
- [Microsoft — DORA란 무엇인가](https://learn.microsoft.com/en-us/compliance/dora/dora-what-is-dora)
