---
description: 클라우드 지속 가능성(GreenOps) — 탄소 배출 추적, 저탄소 설계 원칙, 벤더별 도구를 비교합니다.
---

# 지속 가능성과 GreenOps

> 문서 기준: 2026년 8월

## 개요

클라우드 지속 가능성은 벤더와 고객의 **공동 책임**입니다. 벤더는 데이터센터 효율(PUE), 재생 에너지 전환을 담당하고, 고객은 워크로드 효율화로 불필요한 리소스 사용을 줄입니다.

## 벤더별 탄소 배출 추적 도구

| 벤더 | 도구 | 특징 |
| --- | --- | --- |
| AWS | [Customer Carbon Footprint Tool](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/what-is-ccft.html) | 계정별 탄소 배출량 대시보드. Scope 1/2/3 구분 |
| Azure | [Emissions Impact Dashboard](https://learn.microsoft.com/azure/carbon-optimization/view-emissions) | Microsoft Sustainability Manager 연동. 리전별 탄소 강도 |
| Google Cloud | [Carbon Footprint](https://cloud.google.com/carbon-footprint) | 프로젝트별 배출량. 리전별 탄소 지수(CFE%) 공개 |
| OCI | [Sustainability 대시보드](https://www.oracle.com/corporate/citizenship/sustainability/) | 리전별 에너지 효율 리포트 |

## 지속 가능한 설계 원칙

### 저탄소 리전 선택

각 리전의 전력 믹스(재생 에너지 비율)가 다릅니다. 레이턴시 요건이 유연한 워크로드는 탄소 강도가 낮은 리전을 선택할 수 있습니다.

- **AWS** — 운영 전력 100% 재생 에너지 매칭 목표를 2023년에 달성 보고(이후 연도에도 유지 보고). [Customer Carbon Footprint Tool](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/what-is-ccft.html)로 계정별 배출량 확인
- **Azure** — 재생 에너지·탄소 목표 진행 상황은 Microsoft 지속가능성 공개 자료를 확인. 배출량 추적은 [Emissions Impact Dashboard](https://learn.microsoft.com/azure/carbon-optimization/view-emissions) 사용
- **Google Cloud** — 리전별 CFE(Carbon-Free Energy) 비율을 공개, 2030년 24/7 탄소 무배출 목표
- **OCI** — EU 등 리전별 재생 에너지 목표·현황은 Oracle 공개 자료 확인. Cloud Advisor로 지속가능성 권장사항 제공

### 리소스 효율화

| 원칙 | 방법 | 효과 |
| --- | --- | --- |
| **적정 사이징** | 오버프로비저닝 제거. CPU/메모리 사용률 기반 축소 | 리소스 절감 = 에너지 절감 |
| **스케줄링** | 비업무 시간 개발 환경 중지 | 유휴 리소스 제거 |
| **서버리스/관리형** | 공유 인프라로 밀도 향상 | 전용 서버 대비 에너지 효율 높음 |
| **효율적 인스턴스** | Arm 기반 (Graviton, Ampere, Tau) 선택 | 동일 성능 대비 전력 소비 낮음 |
| **데이터 보존 정책** | 불필요한 데이터 삭제, 콜드 스토리지 전환 | 스토리지 에너지 절감 |

### 그린 아키텍처 패턴

- **비동기 처리** — 피크 타임 분산으로 인프라 최대 용량 축소
- **캐싱** — 반복 연산/조회 제거로 컴퓨팅 절감
- **데이터 지역성** — 데이터와 컴퓨팅을 같은 리전에 배치하여 네트워크 전송 최소화

{% hint style="info" %}
**GreenOps와 FinOps는 방향이 같습니다.** 비용을 줄이는 행위(유휴 리소스 제거, 적정 사이징, 서버리스 전환)는 대부분 탄소 배출도 줄입니다. [FinOps](finops.md) 실천이 곧 GreenOps입니다.
{% endhint %}

## GreenOps 운영 지표

### 추적할 지표

| 지표 | 설명 | 출처 |
| --- | --- | --- |
| 워크로드별 탄소 배출량 추세 | 월별 tCO₂e 변화 | 벤더 탄소 대시보드 |
| 비용 대비 탄소 효율 | $/tCO₂e | 비용 + 탄소 리포트 조합 |
| 유휴 리소스 비율 | CPU 사용률 < 5% 인스턴스 비율 | 모니터링 도구 |
| 스케줄링으로 줄인 컴퓨팅 시간 | 업무 외 시간 자동 종료 절감량 | 자동화 로그 |
| 데이터 보존 정책 절감 | 수명주기 정책으로 줄인 스토리지 | 스토리지 리포트 |

### Scope와 책임 범위

탄소 배출 리포트에서 자주 나오는 Scope 개념:

| Scope | 설명 | 클라우드에서의 의미 |
| --- | --- | --- |
| Scope 1 | 직접 배출 (자사 시설) | 클라우드 사용자에게는 해당 없음 |
| Scope 2 | 간접 배출 (구매 전력) | 벤더가 데이터센터 전력으로 책임 |
| Scope 3 | 가치사슬 배출 | **사용자의 클라우드 사용**이 여기에 해당 |

사용자가 직접 줄일 수 있는 영역: 유휴 리소스 제거, 적정 사이징, 저탄소 리전 선택, 효율적 아키텍처.

### FinOps와 GreenOps의 차이

공통점이 많지만 항상 같지는 않습니다:

| 상황 | FinOps 관점 | GreenOps 관점 |
| --- | --- | --- |
| 저탄소 리전이 더 비쌈 | 비용 최저 리전 선택 | 탄소 최저 리전 선택 |
| 스팟 인스턴스 | 비용 절감 ✅ | 재시작 반복 시 오히려 비효율 가능 |
| 유휴 리소스 제거 | 비용 절감 ✅ | 탄소 절감 ✅ (동일) |
| 적정 사이징 | 비용 절감 ✅ | 탄소 절감 ✅ (동일) |

### 의사결정 체크리스트

- [ ] 레이턴시/SLA 때문에 리전을 바꿀 수 없는 워크로드인가?
- [ ] 배치 작업처럼 실행 시간을 조정할 수 있는 워크로드인가?
- [ ] 데이터 보존 기간이 규정 요구보다 과도하지 않은가?
- [ ] 탄소 최적화가 보안/가용성/규정 준수를 훼손하지 않는가?

## 자주 하는 실수

- **저탄소 리전을 선택했지만 레이턴시 요건을 무시** — 사용자와 먼 리전을 선택하여 응답 시간이 SLA를 초과
- **GreenOps 지표를 추적하지만 실제 조치를 하지 않음** — 대시보드만 만들고 유휴 리소스 제거나 스케줄링 같은 실행을 하지 않음
- **FinOps와 GreenOps를 별도 이니셔티브로 운영** — 대부분의 비용 절감 활동이 곧 탄소 절감인데 중복 조직/프로세스를 만듦

## 체크리스트

- [ ] 벤더 탄소 배출 대시보드(Customer Carbon Footprint Tool 등)를 활성화하고 월별 추이를 추적하는가
- [ ] 비업무 시간에 개발/테스트 환경을 자동 중지하는 스케줄링을 적용했는가
- [ ] Arm 기반 인스턴스(Graviton, Ampere)를 호환 가능한 워크로드에 우선 적용하는가

## 참고하기

### AWS

- [AWS Sustainability Pillar (Well-Architected)](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html)

### Azure

- [Azure Well-Architected — Sustainability](https://learn.microsoft.com/azure/well-architected/sustainability/)

### Google Cloud

- [Google Cloud Carbon Footprint](https://cloud.google.com/carbon-footprint)
- [Google Cloud Region Carbon-Free Energy](https://cloud.google.com/sustainability/region-carbon)

### OCI

- [Oracle Cloud Sustainability](https://www.oracle.com/corporate/citizenship/sustainability/)

### 표준 및 커뮤니티

- [Green Software Foundation](https://greensoftware.foundation/)
