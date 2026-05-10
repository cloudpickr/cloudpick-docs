# 백업과 복구

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
