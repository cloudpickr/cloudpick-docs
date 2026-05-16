---
description: VM 오토스케일링, 예측 스케일링, 애플리케이션 레벨 스케일링을 벤더별로 비교합니다.
---

# 오토스케일링

> 문서 기준: 2026년 5월

## 개요

VM을 사용하면 서버를 빠르게 만들 수 있지만, 트래픽 변화에 대응하는 것은 여전히 사용자의 몫입니다. 트래픽이 급증하면 수동으로 서버를 추가하고, 줄어들면 다시 제거해야 합니다. 이 과정이 느리면 서비스가 다운되고, 과하면 비용이 낭비됩니다.

**오토스케일링**은 이 판단과 실행을 자동화합니다. CPU 사용률, 요청 수 등의 지표를 모니터링하다가 임계값을 넘으면 자동으로 서버를 추가하고, 부하가 줄면 자동으로 제거합니다.

이것이 클라우드에서 관리형 서비스가 중요한 이유입니다. 사람이 24시간 모니터링하지 않아도, 벤더가 제공하는 자동화 기능이 인프라를 탄력적으로 운영해 줍니다.

## 스케일링 정책 유형

오토스케일링은 "언제 스케일링할지"를 결정하는 정책에 따라 구분됩니다.

| 정책 | 트리거 | 특징 | 사용 시점 |
| --- | --- | --- | --- |
| **대상 추적 (Target Tracking)** | 특정 메트릭이 목표값 유지되도록 자동 조정 (예: CPU 50% 유지) | 가장 간단. 대부분의 워크로드에 적합 | 기본 선택. 일반적인 웹 서비스 |
| **단계 스케일링 (Step Scaling)** | 임계값 초과 정도에 따라 여러 단계로 스케일링 | 세밀한 제어 가능 | 트래픽 패턴이 다양한 복잡한 워크로드 |
| **단순 스케일링 (Simple Scaling)** | 임계값 초과 시 고정된 수만큼 스케일링 | 이전 방식. 쿨다운 시간 긴 편 | 레거시 호환. 신규는 Target Tracking 권장 |
| **예측 스케일링 (Predictive)** | ML로 트래픽 예측, 사전 확장 | 예측 가능한 주기적 패턴에 효과적 | 일/주 단위 반복 트래픽 (출퇴근, 주말) |
| **예약 스케일링 (Scheduled)** | 지정된 시간에 스케일링 | 예측 스케일링이 불가한 계획된 이벤트 | 프로모션, 블랙 프라이데이, 대규모 이벤트 |

### 쿨다운(Cooldown) 시간

스케일링 이벤트 후 다음 스케일링까지 대기하는 시간입니다. 너무 짧으면 스케일링이 과도하게 반복되고(thrashing), 너무 길면 트래픽 변화에 느리게 반응합니다.

### 워크로드별 정책 조합 예시

| 워크로드 패턴 | 추천 정책 조합 | 이유 |
| --- | --- | --- |
| **일반 웹 서비스** (트래픽 점진 증가) | Target Tracking (CPU 60~70%) | 단순하고 대부분 충분 |
| **출퇴근 패턴** (매일 9시 급증, 18시 감소) | Predictive + Target Tracking | 예측으로 사전 확장, Target으로 미세 조정 |
| **이벤트/프로모션** (특정 시점 급증) | Scheduled + Target Tracking | 시작 전 사전 확장, 이후 자동 조정 |
| **배치/데이터 처리** (큐 기반) | Target Tracking (큐 깊이 기준) | CPU가 아닌 대기 작업 수로 스케일링 |
| **게임/라이브** (예측 불가 스파이크) | Target Tracking + 높은 최소 인스턴스 수 | 콜드 스타트 방지를 위해 여유분 유지 |

{% hint style="info" %}
대부분의 워크로드는 **Target Tracking 하나로 시작**하세요. 복잡한 정책 조합은 트래픽 패턴을 충분히 관찰한 뒤에 추가해도 늦지 않습니다.
{% endhint %}

### 쿨다운 설정 가이드

- **AWS**: 기본 300초 (5분), Warm Pool로 콜드 스타트 완화
- **Azure**: 기본 5분, VMSS의 Instance Protection으로 특정 인스턴스 보호
- **GCP**: 기본 60초 (Initial Delay), Auto-healing과 함께 동작
- **OCI**: 기본 300초, 쿨다운 기간 설정 가능

## 오토스케일링의 한계

오토스케일링은 만능이 아닙니다. 다음과 같은 상황에서는 한계가 있습니다.

| 한계 | 설명 | 대응 방안 |
| --- | --- | --- |
| **콜드 스타트 시간** | 새 인스턴스가 부팅되고 앱이 준비되기까지 수 분이 걸릴 수 있음. 그 사이 요청이 실패하거나 지연됨 | Warm Pool(AWS), 최소 인스턴스 수 유지, 컨테이너/서버리스 전환 |
| **상태 유지 워크로드** | 세션, 로컬 캐시, 디스크 데이터를 가진 인스턴스는 축소 시 데이터 유실 위험 | 상태를 외부 저장소(Valkey, DB)로 분리, Sticky Session 사용 |
| **예측 불가능한 트래픽 스파이크** | 갑작스러운 트래픽 급증 시 스케일링 속도가 트래픽 증가를 따라가지 못함 | 예측 스케일링(Predictive Scaling), 스케줄 기반 사전 확장, CDN/캐시 활용 |

## 제품 비교

### VM 오토스케일링

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Auto Scaling Groups | EC2 인스턴스 자동 확장/축소 |
| Azure | VM Scale Sets (VMSS) | VM 배포와 스케일링 통합 관리 |
| GCP | Managed Instance Groups (MIG) | Auto-healing(비정상 인스턴스 자동 교체) 내장 |
| OCI | OCI Autoscaling | Instance Pool 기반. 메트릭/스케줄 기반 스케일링 |

### 예측 스케일링

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Predictive Scaling | 최대 14일 트래픽 학습, 사전 확장 |
| Azure | Autoscale (Predictive) | Preview |
| GCP | Predictive Autoscaling | 과거 패턴 기반 |
| OCI | — | 스케줄 기반 스케일링으로 대응 |

### 애플리케이션 레벨 스케일링

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Application Auto Scaling | ECS, DynamoDB, Lambda 등 다양한 서비스 대상 |
| Azure | Autoscale | App Service, Functions, VMSS 등 |
| GCP | Autoscaler | Compute Engine, GKE 등 |
| OCI | OCI Autoscaling | Compute, OKE 등 |

## 핵심 차이점

- **AWS** — Auto Scaling Groups + Launch Template으로 인스턴스 유형, 구매 옵션(온디맨드/Spot) 혼합 배포가 가능합니다. Warm Pool로 미리 초기화된 인스턴스를 준비해 콜드 스타트를 완화할 수 있습니다.
- **Azure** — VMSS가 VM 배포와 스케일링을 하나의 리소스로 관리합니다.
- **GCP** — MIG에 Auto-healing이 기본 내장되어 비정상 인스턴스를 자동 교체합니다.
- **OCI** — Instance Pool 기반 오토스케일링으로 메트릭/스케줄 기반 스케일링을 지원합니다.

{% hint style="warning" %}
오토스케일링은 트래픽 증가에 대응하지만, **스케일 아웃에 수 분이 소요**됩니다. 갑작스러운 트래픽 스파이크(초단위)에는 충분히 대응하지 못할 수 있습니다. 예측 스케일링과 최소 인스턴스 수를 함께 설정하세요.
{% endhint %}

## 참고하기

### AWS

- [AWS Auto Scaling 문서](https://docs.aws.amazon.com/ko_kr/autoscaling/)
- [Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/ko_kr/autoscaling/ec2/userguide/)

### Azure

- [Azure VM Scale Sets 문서](https://learn.microsoft.com/ko-kr/azure/virtual-machine-scale-sets/)
- [Azure Autoscale 문서](https://learn.microsoft.com/ko-kr/azure/azure-monitor/autoscale/autoscale-overview)

### GCP

- [Google Cloud Autoscaler 문서](https://cloud.google.com/compute/docs/autoscaler)
- [Google Cloud MIG 문서](https://cloud.google.com/compute/docs/instance-groups)

### OCI

- [OCI Autoscaling 문서](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/autoscalinginstancepools.htm)
