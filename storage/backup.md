---
description: 통합 백업 서비스, RPO/RTO 트레이드오프, 3-2-1 규칙, 랜섬웨어 대비를 벤더별로 비교합니다.
---

# 백업과 복구

> 문서 기준: 2026년 5월

## 개요

온프레미스에서는 백업 소프트웨어를 설치하고, 테이프 라이브러리나 별도 스토리지에 백업을 수행합니다. 백업 대상(VM, DB, 파일)마다 도구가 다르고, 보존 정책 관리도 수동입니다.

클라우드에서는 **통합 백업 서비스**를 통해 여러 서비스(VM, 블록 스토리지, 파일, 데이터베이스 등)의 백업을 하나의 정책으로 관리할 수 있습니다. 스케줄, 보존 기간, 크로스 리전 복제를 중앙에서 설정하고, 복구도 콘솔에서 수행합니다.

## 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | AWS Backup | EBS, EFS, RDS, DynamoDB, S3 등 통합. 크로스 리전/크로스 계정 백업 지원 |
| Azure | Azure Backup | VM, Disks, Files, SQL, Blob 등 통합. Recovery Services Vault로 관리 |
| GCP | Backup and DR Service | Compute Engine, GKE, Cloud SQL 등 통합 |
| OCI | OCI Backup | Block Volume, Boot Volume, DB 시스템 백업. 정책 기반 자동 백업 |

### 개별 서비스 백업

통합 서비스 외에도 각 스토리지/DB 서비스 자체에 백업 기능이 내장되어 있습니다.

| 대상 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **블록 디스크** | EBS 스냅샷 | Managed Disk 스냅샷 | Persistent Disk 스냅샷 | Block Volume 백업 |
| **VM 전체** | AMI | VM Image / Restore Point | Machine Image | Custom Image |
| **관리형 DB** | RDS 자동 백업 + 스냅샷 | Azure SQL 자동 백업 | Cloud SQL 자동 백업 | DB System 자동 백업 |
| **객체 스토리지** | S3 버전 관리 + Replication | Blob 버전 관리 + Replication | Object Versioning | Object Storage 버전 관리 + Replication |

## 핵심 차이점

**AWS Backup** — 가장 많은 AWS 서비스를 지원하며, 크로스 계정 백업으로 보안 계정에 백업을 격리할 수 있습니다. Backup Vault Lock으로 백업 삭제를 방지하는 WORM(Write Once Read Many) 기능도 제공합니다.

**Azure Backup** — Recovery Services Vault 하나로 VM, 디스크, 파일, SQL을 통합 관리합니다. Azure Site Recovery와 연동하면 백업과 DR을 하나의 체계로 운영할 수 있습니다.

**GCP Backup and DR** — 관리 콘솔에서 백업 계획을 정의하고, 복구 시 원본 또는 다른 위치로 복원할 수 있습니다.

**OCI Backup** — Block Volume, Boot Volume, DB 시스템의 정책 기반 자동 백업을 지원하며, 크로스 리전 복제로 DR을 구성할 수 있습니다.

## 백업 주기와 비용

백업은 주기가 짧을수록 데이터 손실이 적지만 저장 비용이 증가합니다. 워크로드별로 적절한 주기를 선택해야 합니다.

| 전략 | 주기 | 비용 | 적합한 워크로드 |
| --- | --- | --- | --- |
| 일 1회 스냅샷 | 24시간 | 낮음 | 개발/테스트 환경 |
| 시간별 스냅샷 | 1시간 | 중간 | 일반 업무 시스템 |
| 실시간 복제 (동기) | 연속 | 높음 | 금융, 결제 등 미션 크리티컬 |
| 아카이브 백업 | 주/월 단위 | 매우 낮음 | 규정 준수용 장기 보관 |

{% hint style="info" %}
백업 주기는 목표 복구 시점(RPO)으로부터 도출됩니다. RPO/RTO와 비즈니스 얼라인먼트에 대해서는 [재해복구](../governance/dr.md)에서 자세히 다룹니다.
{% endhint %}

## 백업 유형

데이터 양과 복원 시간의 트레이드오프에 따라 백업 방식을 선택합니다.

| 유형 | 설명 | 장점 | 단점 |
| --- | --- | --- | --- |
| **Full Backup** | 전체 데이터를 매번 복사 | 단일 백업으로 완전 복원 가능 | 저장 공간과 시간 많이 소요 |
| **Incremental Backup** | 마지막 백업 이후 변경분만 저장 | 저장 공간/시간 절약 | 복원 시 Full + 모든 Incremental 필요 |
| **Differential Backup** | 마지막 Full 이후 변경분 저장 | 복원 시 Full + 최근 Differential 1개만 필요 | Incremental보다 공간 더 사용 |
| **Snapshot** | 특정 시점의 디스크 상태를 증분으로 저장 | 빠른 생성/복원, 블록 레벨 증분 | 일부 벤더는 같은 리전에만 저장 |

클라우드에서는 대부분 **스냅샷 기반 증분 백업**을 사용합니다. 첫 백업은 전체 복사지만, 이후에는 변경된 블록만 저장하여 효율적입니다.

{% hint style="info" %}
**스냅샷 ≠ 백업.** 스냅샷이 같은 계정/리전에만 있으면 계정 해킹이나 리전 장애 시 복구가 불가능합니다. 3-2-1 원칙을 적용하여 최소 1개는 별도 계정이나 다른 리전에 보관하세요.
{% endhint %}

## 3-2-1 백업 규칙

업계 표준 백업 원칙입니다.

- **3** 복사본: 원본 + 2개의 백업
- **2** 종류의 미디어: 서로 다른 저장 매체 또는 서비스
- **1** 개는 오프사이트: 다른 리전 또는 다른 계정/구독에 보관

클라우드에서 3-2-1을 구현하는 예:
- 원본: 프로덕션 계정의 EBS 볼륨
- 복사본 1: 같은 리전의 EBS 스냅샷
- 복사본 2: 다른 리전 또는 격리된 백업 계정의 스냅샷 (크로스 리전/크로스 계정 복제)

## 랜섬웨어 대비

백업 자체가 랜섬웨어 공격 대상이 될 수 있습니다. 불변(immutable) 백업이 필수입니다.

| 기능 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **불변 백업** | Backup Vault Lock (WORM) | Recovery Services Vault Immutability | Backup Vault Immutability | Immutable Backup |
| **MFA 삭제 보호** | Backup Vault Lock | Soft Delete + MFA | Bucket Lock | Resource Lock |
| **크로스 계정 격리** | Backup Account 분리 + Vault 복제 | Cross-tenant Backup | Cross-Project Backup | Cross-Tenancy Backup |

## DR과의 관계

백업은 DR(재해복구)의 **재료**이지 DR **자체**가 아닙니다.

### 스냅샷 증분 백업이 DR로 부족한 이유

| 한계 | 설명 |
| --- | --- |
| **RPO 갭** | 스냅샷은 주기적(매시간/매일). 마지막 스냅샷 이후 변경분은 유실 |
| **RTO 길다** | 스냅샷에서 볼륨 복원 → 인스턴스 연결 → 서비스 기동까지 수십 분~수 시간 |
| **인프라 미포함** | 스냅샷은 디스크 데이터만. 네트워크, LB, DNS, IAM 등 인프라 전체를 복구해야 서비스가 뜸 |
| **의존성 정합성** | DB + 앱 + 캐시를 각각 다른 시점에 스냅샷하면 데이터 불일치 발생 가능 |
| **테스트 부재** | 스냅샷이 있어도 복구 절차를 테스트하지 않으면 실제 장애 시 실패할 수 있음 |

### 백업 vs DR 비교

| 구분 | 백업 (스냅샷) | DR (재해복구) |
| --- | --- | --- |
| 목적 | 데이터 손실 방지 | 서비스 연속성 보장 |
| 복구 대상 | 개별 파일/볼륨/DB | 서비스 전체 (인프라 + 데이터 + 설정) |
| RPO | 시간~일 단위 | 초~분 단위 (실시간 복제) |
| RTO | 수십 분~수 시간 | 초~분 (자동 페일오버) |
| 방식 | 스냅샷 + 크로스 리전 복사 | Pilot Light / Warm Standby / Active-Active |
| 비용 | 저렴 (스토리지 비용만) | 대기 인프라 비용 발생 |

실제 DR 전략과 구현 방법은 [재해복구](../governance/dr.md)를 참고하세요.

{% content-ref url="../governance/dr.md" %}
[재해복구](../governance/dr.md)
{% endcontent-ref %}

## 지속적으로 해야 할 것

- **복구 테스트 정기 수행** — 백업이 있어도 복구가 안 되면 무의미합니다. 분기 1회 이상 실제 복구 테스트를 수행하세요.
- **보존 정책 검토** — 규정 요구사항 변경이나 데이터 증가에 따라 보존 기간과 스토리지 클래스를 재검토합니다.

## 참고하기

### AWS

- [AWS Backup 문서](https://docs.aws.amazon.com/ko_kr/aws-backup/)
- [EBS 스냅샷 문서](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/EBSSnapshots.html)

### Azure

- [Azure Backup 문서](https://learn.microsoft.com/ko-kr/azure/backup/)
- [Azure Site Recovery 문서](https://learn.microsoft.com/ko-kr/azure/site-recovery/)

### GCP

- [Backup and DR Service 문서](https://cloud.google.com/backup-disaster-recovery/docs)
- [Persistent Disk 스냅샷](https://cloud.google.com/compute/docs/disks/create-snapshots)

### OCI

- [OCI Block Volume 백업](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/blockvolumebackups.htm)
- [OCI Boot Volume 백업](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/bootvolumebackups.htm)
