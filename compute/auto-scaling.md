---
description: VM 오토스케일링, 예측 스케일링, 애플리케이션 레벨 스케일링을 벤더별로 비교합니다.
---

# 오토스케일링

> 문서 기준: 2026년 5월

## 개요

VM을 사용하면 서버를 빠르게 만들 수 있지만, 트래픽 변화에 대응하는 것은 여전히 사용자의 몫입니다. 트래픽이 급증하면 수동으로 서버를 추가하고, 줄어들면 다시 제거해야 합니다. 이 과정이 느리면 서비스가 다운되고, 과하면 비용이 낭비됩니다.

**오토스케일링**은 이 판단과 실행을 자동화합니다. CPU 사용률, 요청 수 등의 지표를 모니터링하다가 임계값을 넘으면 자동으로 서버를 추가하고, 부하가 줄면 자동으로 제거합니다.

{% hint style="warning" %}
오토스케일링은 **스케일 아웃에 수 분이 소요**됩니다. 갑작스러운 트래픽 스파이크(초 단위)에는 충분히 대응하지 못할 수 있습니다. 또한 잘못된 설정은 장애를 자동으로 확대시킬 수 있으므로, 정책 설계와 테스트가 중요합니다.
{% endhint %}

## 스케일링 정책 유형

오토스케일링은 "언제 스케일링할지"를 결정하는 정책에 따라 구분됩니다.

| 정책 | 트리거 | 특징 | 사용 시점 |
| --- | --- | --- | --- |
| **대상 추적 (Target Tracking)** | 특정 메트릭이 목표값 유지되도록 자동 조정 | 가장 간단. 대부분의 워크로드에 적합 | 기본 선택. 일반적인 웹 서비스 |
| **단계 스케일링 (Step Scaling)** | 임계값 초과 정도에 따라 여러 단계로 스케일링 | 세밀한 제어 가능 | 트래픽 패턴이 다양한 복잡한 워크로드 |
| **단순 스케일링 (Simple Scaling)** | 임계값 초과 시 고정된 수만큼 스케일링 | 이전 방식. 쿨다운 시간 긴 편 | 레거시 호환. 신규는 Target Tracking 권장 |
| **예측 스케일링 (Predictive)** | ML로 트래픽 예측, 사전 확장 | 예측 가능한 주기적 패턴에 효과적 | 일/주 단위 반복 트래픽 (출퇴근, 주말) |
| **예약 스케일링 (Scheduled)** | 지정된 시간에 스케일링 | 예측 스케일링이 불가한 계획된 이벤트 | 프로모션, 블랙 프라이데이, 대규모 이벤트 |

{% hint style="warning" %}
CPU가 병목이 아닌 워크로드(I/O 바운드, 메모리 바운드, DB 커넥션 풀 고갈)에서 CPU 기반 스케일링은 트래픽 폭증 후에도 반응하지 않습니다. 워크로드의 실제 병목 메트릭을 선택하세요.
{% endhint %}

### 워크로드별 정책 조합 예시

| 워크로드 패턴 | 추천 정책 조합 | 이유 |
| --- | --- | --- |
| **일반 웹 서비스** (트래픽 점진 증가) | Target Tracking (부하 테스트로 목표값 검증) | 단순하고 대부분 충분 |
| **출퇴근 패턴** (매일 9시 급증, 18시 감소) | Predictive + Target Tracking | 예측으로 사전 확장, Target으로 미세 조정 |
| **이벤트/프로모션** (특정 시점 급증) | Scheduled + Target Tracking | 시작 전 사전 확장, 이후 자동 조정 |
| **배치/데이터 처리** (큐 기반) | Target Tracking (큐 깊이 기준) | CPU가 아닌 대기 작업 수로 스케일링 |
| **예측 불가 스파이크** (게임, 바이럴) | 높은 최소 인스턴스 수 + CDN/캐시 + Rate Limiting | 스케일링 속도로는 대응 불가, 사전 여유분 확보 |

{% hint style="info" %}
대부분의 워크로드는 **메트릭 기반 자동 조정(Target Tracking / Target Utilization) 하나로 시작**하세요. 모든 벤더가 이 방식을 지원하며, 복잡한 정책 조합은 트래픽 패턴을 충분히 관찰한 뒤에 추가해도 늦지 않습니다. 다중 정책 적용 시 벤더마다 동작이 다르므로(AWS: 가장 큰 용량 선택, GCP: 가장 높은 신호 기준) 공식 문서를 확인하세요.
{% endhint %}

### 쿨다운(Cooldown) 시간

스케일링 이벤트 후 다음 스케일링까지 대기하는 시간입니다. 너무 짧으면 스케일링이 과도하게 반복되고(thrashing), 너무 길면 트래픽 변화에 느리게 반응합니다. 앱 기동 시간보다 짧으면 안 됩니다.

| 벤더 | 기본값 | 콜드 스타트 완화 |
| --- | --- | --- |
| AWS | 300초 | Warm Pool (사전 초기화된 인스턴스 대기) |
| Azure | 5분 | Instance Protection, Custom Script Extension |
| GCP | 60초 (Initial Delay) | Auto-healing + 사전 빌드 이미지 |
| OCI | 300초 | 쿨다운 기간 설정 가능 |

## 오토스케일링의 한계

| 한계 | 설명 | 대응 방안 |
| --- | --- | --- |
| **콜드 스타트 시간** | 새 인스턴스 부팅 + 앱 준비까지 수 분 소요 | 사전 초기화된 인스턴스 풀, 최소 인스턴스 수 유지, 사전 빌드 이미지(Golden Image) |
| **상태 유지 워크로드** | 세션/캐시/디스크 데이터가 있는 인스턴스는 축소 시 유실 | 상태를 외부 저장소(Valkey, DB)로 분리 |
| **예측 불가 스파이크** | 스케일링 속도가 트래픽 증가를 따라가지 못함 | 최소 용량 확보, CDN/캐시, Rate Limiting, Graceful Degradation |
| **Quota 소진** | 계정/리전 vCPU 한도 초과 시 스케일 아웃이 무음 실패 | 사전 Quota 확인, 증설 요청, 스케일링 실패 알림 설정 |

## Spot/Preemptible 인스턴스 혼합

오토스케일링 그룹에 온디맨드와 Spot 인스턴스를 혼합하면 중단을 감당할 수 있는 워크로드에서 비용을 줄일 수 있습니다. 단, Fallback 전략 없이는 장애 원인이 됩니다.

| 벤더 | 방법 | 비고 |
| --- | --- | --- |
| AWS | ASG Mixed Instances Policy | 온디맨드 베이스 + Spot 비율 지정. 여러 인스턴스 타입 풀 |
| Azure | VMSS Spot Priority Mix | Spot VM 비율 설정. Eviction Policy 선택 |
| GCP | MIG + Spot VMs | Spot VM을 MIG에 포함. Preemption 시 자동 재생성 |
| OCI | Instance Pool + Preemptible | Preemptible 인스턴스를 풀에 혼합 |

## 오토스케일링이 내장된 서비스

직접 스케일링 정책을 설정하지 않아도 플랫폼이 자동으로 처리하는 서비스들입니다.

| 벤더 | 서비스 | 설명 |
| --- | --- | --- |
| AWS | Elastic Beanstalk, ECS Service Auto Scaling, Lambda | 앱 배포 시 스케일링 내장 |
| Azure | App Service (Auto Scale), Container Apps, Functions | PaaS 레벨 자동 스케일링 |
| GCP | Cloud Run, App Engine, GKE Autopilot | 요청 기반 자동 확장/축소 |
| OCI | Container Instances, Functions | 서버리스 자동 스케일링 |

{% hint style="info" %}
VM 레벨 오토스케일링을 직접 설정하기 전에, 워크로드가 위 서비스에 적합한지 먼저 검토하세요. PaaS/서버리스를 사용하면 VM 스케일링 정책은 크게 단순해지지만, 동시성 제한·최대 인스턴스 수·다운스트림 보호 설정은 별도로 필요합니다.
{% endhint %}

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

- **AWS** — Mixed Instances Policy로 온디맨드/Spot 혼합 배포. Warm Pool로 사전 초기화된 인스턴스를 대기시켜 콜드 스타트 완화.
- **Azure** — VMSS가 VM 배포와 스케일링을 하나의 리소스로 관리. Spot Priority Mix로 비용 최적화.
- **GCP** — MIG에 Auto-healing이 기본 내장되어 비정상 인스턴스를 자동 교체. 쿨다운이 60초로 가장 짧아 빠른 반응.
- **OCI** — Instance Pool 기반 오토스케일링. 메트릭/스케줄 기반 스케일링을 지원하며, Preemptible 인스턴스 혼합 가능.

## 오토스케일링 설정 체크리스트

- [ ] 스케일링 메트릭을 워크로드 병목에 맞게 선택했는가 (CPU, 요청 수, 큐 깊이, 응답 시간 등)
- [ ] Grace Period / Warm-up 시간을 설정했는가 (새 인스턴스 기동 직후 메트릭 불안정 구간 무시)
- [ ] 헬스 체크를 LB와 오토스케일링 양쪽에 설정했는가
- [ ] Connection Draining / Deregistration Delay를 설정했는가 (진행 중 요청 완료 보장)
- [ ] 앱의 Graceful Shutdown(SIGTERM 처리)을 구현했는가
- [ ] 종료 정책(Termination Policy)을 확인했는가 (AZ 균형, Newest/Oldest 등)
- [ ] 스케일 인 보호가 필요한 인스턴스(배포 중, 장시간 작업)를 제외했는가
- [ ] 최소 인스턴스 수를 콜드 스타트 허용 범위에 맞게 설정했는가
- [ ] 최대 인스턴스 수를 비용 상한에 맞게 설정했는가
- [ ] 리전/AZ별 vCPU Quota를 사전 확인하고 증설 요청했는가
- [ ] Spot/Preemptible 혼합 시 Fallback(온디맨드 전환) 전략을 설정했는가
- [ ] 스케일링 이벤트 알림과 실패 알림을 설정했는가
- [ ] 쿨다운 시간이 앱 기동 시간보다 긴지 확인했는가

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
