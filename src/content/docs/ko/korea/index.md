---
title: "한국 가이드"
description: "한국 환경 특화 가이드 — CSAP, 망분리, 소버린 AI 정책, 국산 FM 제공사"
---

> 문서 기준: 2026년 8월

## 개요

이 섹션은 한국 시장에서 클라우드를 도입·운영할 때 마주치는 규제와 생태계를 다룹니다. 앞선 벤더 중립 문서들이 글로벌 공통 아키텍처를 다뤘다면, 이 가이드는 한국 고유의 법·제도·공급사 환경에 초점을 맞춥니다.

엔터프라이즈 아키텍트가 공공·금융 부문에 클라우드를 도입하거나, 생성형 AI를 국내 규제 환경에 맞게 도입할 때 참고할 수 있도록 구성했습니다.

## 한국 리전 현황

| 벤더 | 리전 코드 | AZ/Zone 수 | 출시 시기 |
| --- | --- | --- | --- |
| AWS | `ap-northeast-2` (서울) | 4개 AZ | 2016년 |
| Azure | `koreacentral` (서울), `koreasouth` (부산) | 3개 AZ (Central) | 2017년 |
| Google Cloud | `asia-northeast3` (서울) | 3개 Zone | 2020년 |
| OCI | `ap-seoul-1`, `ap-chuncheon-1` | 3 FD | 2020년 |

:::note
Azure(서울-부산)와 OCI(서울-춘천)는 국내 2개 리전을 보유하여 데이터가 국외로 나가지 않는 DR 구성이 가능합니다. AWS/Google Cloud는 도쿄·오사카가 가장 가까운 DR 후보입니다. 리전 개념은 [리전과 가용영역](../../about-cloud/regions-and-zones/)을 참고하세요.
:::

### 한국 리전 기준 DR 구성

| 벤더 | 프라이머리 | 세컨더리 후보 | 지연 시간 | 비고 |
| --- | --- | --- | --- | --- |
| AWS | `ap-northeast-2` (서울) | `ap-northeast-1` (도쿄), `ap-northeast-3` (오사카) | 약 30~50ms | 국외 이전 |
| Azure | `koreacentral` (서울) | `koreasouth` (부산) | 약 5ms | **국내 DR 가능** |
| Azure | `koreacentral` (서울) | `japaneast` (도쿄) | 약 30ms | 국외 이전 |
| Google Cloud | `asia-northeast3` (서울) | `asia-northeast1` (도쿄), `asia-northeast2` (오사카) | 약 30~50ms | 국외 이전 |
| OCI | `ap-seoul-1` (서울) | `ap-chuncheon-1` (춘천) | 약 5ms | **국내 DR 가능** |
| OCI | `ap-seoul-1` (서울) | `ap-tokyo-1` (도쿄) | 약 30ms | 국외 이전 |

:::caution
국외 리전을 DR 대상으로 사용할 경우, 개인정보보호법·신용정보법에 따른 데이터 국외 이전 요건을 충족해야 합니다. DR 전략 유형은 [재해복구 (DR)](../../governance/dr/)를 참고하세요.
:::

### 한국 전용 연결·커뮤니티

전용 연결(Direct Connect / ExpressRoute / Interconnect / FastConnect)의 한국 PoP는 KINX, LG U+가 대표적입니다. 멀티클라우드 Cloud Exchange는 [KINX Cloud Hub](https://www.kinx.net/service/cloud/), Megaport(서울 PoP), Equinix Fabric(서울 DC)을 검토합니다. 개념은 [멀티클라우드 네트워킹](../../networking/multicloud-networking/)을 참고하세요.

로컬 사용자 커뮤니티: [AWSKRUG](https://www.awskr.org/), [GDG Cloud Korea](https://gdg.community.dev/gdg-cloud-korea/).

공공·금융 대형 프로젝트에서는 삼성SDS, LG CNS, SK C&C 등 현지 SI가 전체 시스템을 구축하고, 제품사 FDE는 자사 AI/SaaS 통합을 담당하는 협업 구조가 흔합니다.

## 다루는 주제

### 보안·규제

- **[컴플라이언스 (한국)](../../korea/governance/compliance/)** — ISMS-P, CSAP, 금융권 규제 등 한국 고유 인증·규제 체계를 한눈에 정리하고 각 상세 문서로 안내합니다.
- **[CSAP (클라우드 보안 인증)](../../korea/security/csap/)** — 공공기관 클라우드 도입의 필수 관문인 CSAP 제도의 등급 체계, 하이퍼스케일러·국내 CSP의 인증 현황, 2027년 예정된 국정원 단일 검증체계 개편을 정리합니다.
- **[망분리와 네트워크 격리](../../korea/security/network-isolation/)** — 금융·공공 부문의 망분리 규제, 2024년 이후 진행 중인 금융분야 망분리 개선 로드맵과 국가망보안체계(N²SF) 전환이 클라우드·SaaS·생성형 AI 도입에 미치는 영향을 다룹니다.

### AI·소버린 정책

- **[소버린 FM 정책](../../korea/ai/sovereign-fm-policy/)** — 과학기술정보통신부의 독자 AI 파운데이션 모델 프로젝트, 정예팀 선정 경과와 기업 아키텍트 관점의 시사점을 정리합니다.
- **[FM 제공사 비교](../../korea/ai/fm-providers/)** — 네이버, LG AI연구원, 카카오, KT, 업스테이지, NC AI 등 국내 파운데이션 모델 제공사의 최신 모델·라이선스·제공 채널을 비교합니다.

:::note
이 섹션의 내용은 빠르게 변하는 정책·규제 현황을 다룹니다. 각 문서 하단 "참고하기" 섹션의 출처를 통해 최신 공식 발표를 직접 확인하는 것을 권장합니다.
:::

## 관련 문서

- [데이터 보호와 워크로드 보안](../../security/data-protection/)
- [소버린 랜딩존](../../governance/landing-zone/#소버린-랜딩존-sovereign-landing-zone)

## 참고하기

- 국제 인증·벤더 허브는 [규정 준수 (Compliance)](../../governance/compliance/)를 참고하세요.
