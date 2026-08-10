---
title: "한국 시장·인프라 현황"
description: "한국 리전 현황, 국내 DR 구성, 데이터 주권, 전용 연결 PoP, MSP·커뮤니티 등 한국 시장의 클라우드 인프라·생태계를 정리합니다."
---

> 문서 기준: 2026년 8월

## 개요

글로벌 4대 CSP는 모두 서울에 리전을 운영하며, 일부 벤더는 국내 2개 리전으로 데이터가 국외로 나가지 않는 DR 구성을 지원합니다. 이 문서는 벤더 중립 문서에서 다루지 않는 한국 특화 인프라·생태계 정보 — 리전 현황, 국내 DR 조합, 전용 연결 PoP, MSP·커뮤니티 — 를 정리합니다.

## 한국 리전 현황

| 벤더 | 리전 코드 | AZ/Zone 수 | 출시 시기 |
| --- | --- | --- | --- |
| AWS | `ap-northeast-2` (서울) | 4개 AZ | 2016년 |
| Azure | `koreacentral` (서울), `koreasouth` (부산) | 3개 AZ (Central) | 2017년 |
| Google Cloud | `asia-northeast3` (서울) | 3개 Zone | 2020년 |
| OCI | `ap-seoul-1` (서울), `ap-chuncheon-1` (춘천) | 3 FD | 2020년 |

:::note
Azure(서울-부산)와 OCI(서울-춘천)는 국내 2개 리전을 보유하여 데이터가 국외로 나가지 않는 DR 구성이 가능합니다. AWS/Google Cloud는 도쿄·오사카가 가장 가까운 DR 후보입니다. 리전·AZ 개념은 [리전과 가용영역](../../about-cloud/regions-and-zones/)을 참고하세요.
:::

## 한국 리전 기준 DR 구성

| 벤더 | 프라이머리 (한국) | 세컨더리 후보 | 지연 시간 | 비고 |
| --- | --- | --- | --- | --- |
| AWS | `ap-northeast-2` (서울) | `ap-northeast-1` (도쿄), `ap-northeast-3` (오사카) | 약 30~50ms | 국외 이전 |
| Azure | `koreacentral` (서울) | `koreasouth` (부산) | 약 5ms | **국내 DR 가능** |
| Azure | `koreacentral` (서울) | `japaneast` (도쿄) | 약 30ms | 국외 이전 |
| Google Cloud | `asia-northeast3` (서울) | `asia-northeast1` (도쿄), `asia-northeast2` (오사카) | 약 30~50ms | 국외 이전 |
| OCI | `ap-seoul-1` (서울) | `ap-chuncheon-1` (춘천) | 약 5ms | **국내 DR 가능** |
| OCI | `ap-seoul-1` (서울) | `ap-tokyo-1` (도쿄) | 약 30ms | 국외 이전 |

:::caution
국외 리전을 DR 대상으로 사용할 경우, 개인정보보호법·신용정보법에 따른 데이터 국외 이전 요건을 충족해야 합니다. 데이터 주권이 엄격한 워크로드는 위 표에서 국내 DR이 가능한 벤더를 우선 검토하세요. DR 전략 유형과 RPO/RTO 설계는 [재해복구 (DR)](../../governance/dr/)를 참고하세요.
:::

## 데이터 주권

한국의 **개인정보보호법**은 개인정보의 국외 이전 시 정보주체의 동의 또는 법적 근거를 요구합니다. **신용정보법**은 금융 분야의 개인신용정보에 대해 더 엄격한 규제를 적용합니다. 클라우드 벤더를 선택할 때 한국 리전의 유무와 데이터 저장 위치를 반드시 확인해야 합니다.

리전 제한을 정책으로 강제하는 방법(SCP, Azure Policy 등)은 [리전과 가용영역 — 데이터 주권과 리전 제한](../../about-cloud/regions-and-zones/)을 참고하세요.

## 전용 연결 PoP과 Cloud Exchange

국내에서 전용 연결(Direct Connect, ExpressRoute, Cloud Interconnect, FastConnect)을 구성할 때 이용할 수 있는 PoP 현황입니다.

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **한국 PoP** | KINX, LG U+ | KINX, LG U+ | KINX | KINX |

**국내 Cloud Exchange 선택지:**

- **KINX**: 국내 최대 IX(Internet Exchange). AWS, Azure, Google Cloud, OCI 모두 PoP 보유
- **Megaport**: 글로벌 Cloud Exchange. 서울 PoP 있음
- **Equinix Fabric**: 글로벌 최대. 서울 데이터센터 운영

연결 방식별 트레이드오프는 [멀티클라우드 네트워킹](../../networking/multicloud-networking/)을 참고하세요.

## MSP와 커뮤니티

국내 MSP를 통하면 일반적인 운영 대행 외에 다음을 지원받을 수 있습니다.

- 세금계산서 발행, 원화 결제
- 규제 대응 (CSAP, ISMS-P 등) 지원 — 상세는 [컴플라이언스 (한국)](../../korea/governance/compliance/)

| 벤더 | 커뮤니티 | 비고 |
| --- | --- | --- |
| AWS | [AWSKRUG](https://www.awskr.org/) | 한국 AWS 사용자 커뮤니티 |
| Google Cloud | [GDG Cloud Korea](https://gdg.community.dev/gdg-cloud-korea/) | 한국 Google Cloud 사용자 커뮤니티 |

MSP 비용 구조와 지원 플랜 일반은 [기술 지원과 지원 플랜](../../about-cloud/support-plans/)을 참고하세요.

## 관련 문서

- [리전과 가용영역](../../about-cloud/regions-and-zones/)
- [재해복구 (DR)](../../governance/dr/)
- [멀티클라우드 네트워킹](../../networking/multicloud-networking/)
- [기술 지원과 지원 플랜](../../about-cloud/support-plans/)

## 참고하기

- [KINX](https://www.kinx.net/) — 국내 최대 IX
- [AWS 서울 리전](https://aws.amazon.com/ko/about-aws/global-infrastructure/regions_az/)
- [Azure 한국 리전 (Korea Central/South)](https://azure.microsoft.com/explore/global-infrastructure/geographies)
- [Google Cloud 서울 리전](https://cloud.google.com/about/locations)
- [OCI 리전](https://www.oracle.com/cloud/public-cloud-regions/)
