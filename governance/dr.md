---
description: RPO/RTO, BIA, DR 전략 유형(Backup&Restore~Active-Active), 벤더별 DR 서비스를 비교합니다.
---

# 재해복구 (DR)

> 문서 기준: 2026년 5월

## DR이란

**재해복구** (Disaster Recovery)는 자연재해, 하드웨어 장애, 인적 오류 등으로 인해 서비스가 중단되었을 때, 사전에 정의된 목표 시간 내에 서비스를 복구하는 계획과 프로세스입니다.

## 재해의 정의

DR 계획을 세우려면 먼저 "무엇을 재해로 볼 것인가"를 정의해야 합니다. 재해는 단일 리소스 장애와는 다른 차원의 사건입니다.

### 재해 유형

| 분류 | 예시 | 영향 범위 |
| --- | --- | --- |
| **자연재해** | 지진, 홍수, 태풍, 화재, 정전 | 단일 또는 복수 데이터센터, 리전 |
| **하드웨어/인프라 장애** | 전원 공급 장치 고장, 네트워크 백본 단절, 스토리지 클러스터 손상 | 단일 AZ ~ 리전 |
| **소프트웨어/플랫폼 장애** | 클라우드 벤더의 리전 단위 서비스 장애, 배포 실패 | 단일 서비스 ~ 리전 |
| **인적 오류** | 실수로 인한 삭제, 잘못된 변경, 구성 오류 | 단일 리소스 ~ 전체 계정 |
| **보안 사고** | 랜섬웨어, 데이터 유출, 크리덴셜 탈취 | 데이터, 계정, 리전 |
| **외부 공급망 문제** | 외부 API/서비스 중단, SaaS 벤더 장애 | 해당 의존성 범위 |

### 재해 수준 분류

장애 범위에 따라 재해 수준을 구분하여 대응 전략을 차등 적용합니다.

| 수준 | 정의 | 대응 방안 |
| --- | --- | --- |
| **로컬 장애** | 단일 서버, 단일 리소스 장애 | 오토스케일링, 헬스 체크 기반 자동 복구 |
| **AZ 장애** | 단일 가용영역 전체 중단 | 멀티 AZ 배포, AZ 간 자동 페일오버 |
| **리전 장애** | 전체 리전 중단 (드물지만 발생) | 크로스 리전 복제, 리전 간 DR |
| **벤더 장애** | 클라우드 벤더 전체 장애 | 멀티클라우드 DR (비용/복잡도 높음) |

{% hint style="info" %}
**핵심:** AZ 장애까지는 고가용성(HA) 설계로, 리전 장애 이상은 DR 설계로 대응하는 것이 일반적입니다. 모든 장애를 DR로 해결하려 하면 비용이 과도해지고, 반대로 DR 없이 HA만 구성하면 리전 장애 시 복구 불가능합니다.
{% endhint %}

### 재해와 고가용성의 차이

**고가용성** (High Availability, HA)은 개별 장애가 발생해도 서비스가 중단되지 않도록 하는 설계입니다. **DR**은 HA로 막을 수 없는 규모의 장애(리전 단위 재해)에 대비한 복구 전략입니다.

| 관점 | 고가용성 (HA) | 재해복구 (DR) |
| --- | --- | --- |
| **목표** | 중단 없는 서비스 유지 | 재해 후 서비스 복구 |
| **대상 장애** | AZ 이내 장애 | 리전 단위 이상 장애 |
| **구현** | 멀티 AZ, 로드밸런서, 자동 페일오버 | 크로스 리전 복제, DR 사이트 |
| **비용** | 상대적으로 낮음 | 높음 (이중 인프라) |

## 핵심 지표: RPO와 RTO

| 지표 | 정의 | 비즈니스 의미 |
| --- | --- | --- |
| **RPO** (Recovery Point Objective) | 복구 시 허용 가능한 최대 데이터 손실 시간 | "최대 몇 분/시간 전 데이터까지 잃어도 되는가?" |
| **RTO** (Recovery Time Objective) | 장애 발생 후 서비스 복구까지 허용 가능한 최대 시간 | "최대 몇 분/시간 안에 서비스가 돌아와야 하는가?" |

RPO와 RTO는 비즈니스 요구사항에서 도출됩니다. 기술팀이 임의로 정하는 것이 아니라, 비즈니스 영향 분석(BIA)을 통해 결정합니다.

## 비즈니스 목표와의 얼라인먼트

### 비즈니스 영향 분석 (BIA)

DR 목표를 설정하기 전에 다음을 먼저 정의해야 합니다:

1. **핵심 비즈니스 프로세스 식별** — 어떤 시스템이 중단되면 매출/고객에 직접 영향을 주는가?
2. **중단 비용 산정** — 시간당/분당 중단 비용은 얼마인가? (매출 손실, 위약금, 평판 손상)
3. **RPO/RTO 도출** — 중단 비용과 DR 구축 비용의 균형점에서 목표를 설정
4. **티어 분류** — 모든 시스템에 동일한 DR 수준을 적용하면 비용이 과도. 중요도별 티어 분류

| 티어 | RPO | RTO | DR 전략 | 예시 |
| --- | --- | --- | --- | --- |
| **Tier 1** (미션 크리티컬) | 0 (데이터 손실 불가) | 수 분 | Active-Active / Hot Standby | 결제 시스템, 거래 플랫폼 |
| **Tier 2** (비즈니스 크리티컬) | 수 분\~1시간 | 1\~4시간 | Warm Standby | 주문 관리, CRM |
| **Tier 3** (일반 업무) | 수 시간\~24시간 | 24시간 | Pilot Light / Backup & Restore | 내부 도구, 개발 환경 |

## DR 전략 유형

```mermaid
graph LR
    A["🗄️ Backup & Restore<br/>RPO: 시간 단위<br/>RTO: 시간 단위<br/>비용: 낮음"]
    B["💡 Pilot Light<br/>RPO: 분 단위<br/>RTO: 수십 분<br/>비용: 중간"]
    C["🔆 Warm Standby<br/>RPO: 초~분<br/>RTO: 분 단위<br/>비용: 높음"]
    D["⚡ Active-Active<br/>RPO: 0<br/>RTO: 거의 0<br/>비용: 매우 높음"]

    A -->|복구 목표 높임| B -->|복구 목표 높임| C -->|복구 목표 높임| D
```

| 전략 | RPO | RTO | 비용 | 설명 |
| --- | --- | --- | --- | --- |
| **Backup & Restore** | 시간 단위 | 시간 단위 | 낮음 | 정기 백업 후 장애 시 복원. 가장 저렴하지만 가장 느림 |
| **Pilot Light** | 분 단위 | 수십 분 | 중간 | 핵심 인프라만 최소 규모로 상시 가동. 장애 시 스케일업 |
| **Warm Standby** | 초\~분 | 분 단위 | 높음 | 축소된 규모의 전체 환경을 상시 가동. 장애 시 스케일업 |
| **Active-Active** | 0 | 거의 0 | 매우 높음 | 두 리전에서 동시에 트래픽 처리. 장애 시 자동 페일오버 |

## 주요 CSP DR 서비스 비교

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **DR 전용 서비스** | Elastic Disaster Recovery (DRS) | Azure Site Recovery | — (아키텍처 패턴 가이드) | OCI Full Stack DR |
| **크로스 리전 복제** | S3 CRR, RDS Cross-Region Read Replica | Geo-Redundant Storage, Azure SQL Geo-Replication | Multi-region Storage, Cloud SQL Cross-Region Replica | Object Storage Cross-Region Copy, Data Guard |
| **자동 페일오버** | Route 53 Health Check + Failover | Traffic Manager / Front Door | Cloud DNS + Global LB | OCI DNS + Traffic Management |
| **DR 오케스트레이션** | CloudFormation StackSets | Recovery Services Vault + Recovery Plans | — | Full Stack DR (복구 계획 자동 실행) |

## DR 테스트

DR 계획은 테스트하지 않으면 의미가 없습니다. 실제 장애 시 계획대로 동작하는지 정기적으로 검증해야 합니다.

### 테스트 유형

| 유형 | 설명 | 빈도 |
| --- | --- | --- |
| **Tabletop Exercise** | 시나리오 기반 토론. 실제 시스템 변경 없음 | 분기별 |
| **Walkthrough Test** | 복구 절차를 단계별로 실행하되, 프로덕션 영향 없이 | 반기별 |
| **Simulation Test** | 실제 페일오버를 수행하되, 제한된 범위에서 | 연 1회 |
| **Full Interruption Test** | 프로덕션 리전을 실제로 중단하고 DR 리전으로 전환 | 연 1회 (선택) |

### 테스트 시 확인 사항

- 실제 RTO가 목표 RTO 이내인가?
- 실제 RPO가 목표 RPO 이내인가? (데이터 손실량 확인)
- 페일백(원래 리전으로 복귀) 절차가 동작하는가?
- 런북/자동화 스크립트가 최신 상태인가?
- 담당자가 절차를 숙지하고 있는가?

{% hint style="info" %}
DR 계획은 **반드시 정기적으로 테스트**해야 합니다. 실제 장애가 날 때 처음으로 복구 절차를 실행하면 RTO를 달성할 수 없습니다. 최소 연 1회 Simulation Test 또는 Walkthrough Test를 수행하고 런북을 최신 상태로 유지하세요.
{% endhint %}

### Chaos Engineering과의 관계

DR 테스트를 넘어, 일상적으로 장애를 주입하여 시스템의 복원력을 검증하는 것이 Chaos Engineering입니다.

| 벤더 | 도구 |
| --- | --- |
| AWS | [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/) |
| Azure | [Azure Chaos Studio](https://learn.microsoft.com/en-us/azure/chaos-studio/) |
| GCP | — (3rd party: Gremlin, LitmusChaos) |
| OCI | — (3rd party: Gremlin, LitmusChaos) |

## 기존 문서와의 연계

{% content-ref url="../about-cloud/regions-and-zones.md" %}
[리전과 가용영역](../about-cloud/regions-and-zones.md)
{% endcontent-ref %}

{% content-ref url="../storage/backup.md" %}
[백업과 복구](../storage/backup.md)
{% endcontent-ref %}

{% content-ref url="../about-cloud/well-architected.md" %}
[Well-Architected Framework](../about-cloud/well-architected.md)
{% endcontent-ref %}

## 참고하기

### AWS

- [AWS Disaster Recovery 백서](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)
- [AWS Elastic Disaster Recovery](https://docs.aws.amazon.com/drs/)
- [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/)

### Azure

- [Azure Site Recovery 문서](https://learn.microsoft.com/en-us/azure/site-recovery/)
- [Azure 비즈니스 연속성](https://learn.microsoft.com/en-us/azure/reliability/business-continuity-management-program)
- [Azure Chaos Studio](https://learn.microsoft.com/en-us/azure/chaos-studio/)

### GCP

- [GCP DR 계획 가이드](https://cloud.google.com/architecture/dr-scenarios-planning-guide)
- [GCP 재해복구 아키텍처](https://cloud.google.com/architecture/disaster-recovery)

### OCI

- [OCI Full Stack DR](https://docs.oracle.com/en-us/iaas/disaster-recovery/index.html)
- [OCI 비즈니스 연속성 가이드](https://docs.oracle.com/en-us/iaas/disaster-recovery/index.html)
