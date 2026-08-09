---
description: FedRAMP, HIPAA, ITAR/EAR 등 미국 시장 진출·운영에 필요한 규제 개요와 상세 문서로 안내합니다.
---

# 미국

> 문서 기준: 2026년 8월

## 개요

미국은 연방(federal)과 주(state)의 이원적 규제 체계를 가지고 있으며, 여기에 산업별 규제(헬스케어, 방산·항공우주, 금융 등)가 겹겹이 얹히는 구조입니다. 연방기관에 클라우드 서비스를 납품하려면 FedRAMP 인가가, 헬스케어 데이터를 다루려면 HIPAA/BAA 체계가, 방산·항공우주 기술 데이터를 다루려면 ITAR/EAR 수출통제가 각각 별도로 적용되며 서로 대체되지 않습니다. 이 섹션은 한국 엔터프라이즈 아키텍트가 미국 시장 진출·운영을 검토할 때 마주치는 핵심 규제 3가지를 다룹니다.

## 다루는 주제

- **[FedRAMP](fedramp.md)** — 연방기관 클라우드 조달을 위한 보안 인가 제도입니다. Moderate/High 기준, 2026년 진행 중인 FedRAMP 20x 개편 현황, GovCloud 등 격리 리전, CMMC 2.0·DoD SRG Impact Level을 정리합니다.
- **[HIPAA/HITECH](hipaa.md)** — 헬스케어 데이터(PHI) 보호 규제입니다. BAA(Business Associate Agreement) 체결 구조, 벤더별 적용 범위 확인법, HITRUST CSF와의 관계를 다룹니다.
- **[ITAR/EAR](itar.md)** — 방산·항공우주 기술 데이터 수출통제 규정입니다. US Persons 접근 제한이 클라우드 아키텍처에 갖는 의미와 FedRAMP와의 차이를 정리합니다.

{% hint style="info" %}
세 규제는 서로 독립적입니다. 예를 들어 FedRAMP High 인가를 받은 클라우드 환경이라고 해서 자동으로 ITAR 요건을 충족하는 것은 아니며, HIPAA도 별도의 BAA 체결이 필요합니다. 워크로드 성격에 맞는 규제를 개별적으로 확인해야 합니다.
{% endhint %}

## 관련 문서

- [규정 준수 (Compliance)](../governance/compliance.md)
- [데이터 보호와 워크로드 보안](../security/data-protection.md)

## 참고하기

- [FedRAMP 공식 사이트](https://www.fedramp.gov/)
- [HHS HIPAA 공식 페이지](https://www.hhs.gov/hipaa/)
- [DDTC (ITAR 관장 기관)](https://www.pmddtc.state.gov/)
- [BIS (EAR 관장 기관)](https://www.bis.gov/)
