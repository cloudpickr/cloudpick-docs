---
title: "미국 개요"
description: "FedRAMP, HIPAA, ITAR/EAR 등 미국 시장 진출·운영에 필요한 규제 개요와 상세 문서로 안내합니다."
---

> 문서 기준: 2026년 8월

## 개요

미국은 연방(federal)과 주(state)의 이원적 규제 체계를 가지고 있으며, 여기에 산업별 규제(헬스케어, 방산·항공우주, 금융 등)가 겹겹이 얹히는 구조입니다. 연방기관에 클라우드 서비스를 납품하려면 FedRAMP 인가가, 헬스케어 데이터를 다루려면 HIPAA/BAA 체계가, 방산·항공우주 기술 데이터를 다루려면 ITAR/EAR 수출통제가 각각 별도로 적용되며 서로 대체되지 않습니다. 이 섹션은 미국 시장을 다루는 아키텍트가 마주치는 핵심 규제와 정책(연방 조달·산업 규제·주 프라이버시법·AI 정책)을 다룹니다.

## 다루는 주제

- **[FedRAMP](../us/fedramp/)** — 연방기관 클라우드 조달을 위한 보안 인가 제도입니다. Moderate/High 기준, 2026년 진행 중인 FedRAMP 20x 개편 현황, GovCloud 등 격리 리전, CMMC 2.0·DoD SRG Impact Level을 정리합니다.
- **[HIPAA/HITECH](../us/hipaa/)** — 헬스케어 데이터(PHI) 보호 규제입니다. BAA(Business Associate Agreement) 체결 구조, 벤더별 적용 범위 확인법, HITRUST CSF와의 관계를 다룹니다.
- **[ITAR/EAR](../us/itar/)** — 방산·항공우주 기술 데이터 수출통제 규정입니다. US Persons 접근 제한이 클라우드 아키텍처에 갖는 의미와 FedRAMP와의 차이를 정리합니다.
- **[주(州) 프라이버시법](../us/state-privacy/)** — 연방 포괄법이 없는 미국의 주별 프라이버시 규제 지형입니다. CCPA/CPRA를 중심으로 시행 주 현황, 공통 요건, 멀티스테이트 대응 아키텍처를 다룹니다.
- **[AI 정책과 거버넌스](../us/ai-policy/)** — 연방 AI 행정명령 흐름, NIST AI RMF, 연방 조달의 AI 요건, 주별 AI법 동향과 클라우드 AI 워크로드 시사점을 정리합니다.

:::note
세 규제는 서로 독립적입니다. 예를 들어 FedRAMP High 인가를 받은 클라우드 환경이라고 해서 자동으로 ITAR 요건을 충족하는 것은 아니며, HIPAA도 별도의 BAA 체결이 필요합니다. 워크로드 성격에 맞는 규제를 개별적으로 확인해야 합니다.
:::

## 관련 문서

- [규정 준수 (Compliance)](../governance/compliance/)
- [데이터 보호와 워크로드 보안](../security/data-protection/)

## 참고하기

- [FedRAMP 공식 사이트](https://www.fedramp.gov/)
- [HHS HIPAA 공식 페이지](https://www.hhs.gov/hipaa/)
- [DDTC (ITAR 관장 기관)](https://www.pmddtc.state.gov/)
- [BIS (EAR 관장 기관)](https://www.bis.gov/)
