---
description: 블록/파일 스토리지 차이, 볼륨 타입, AZ 종속성, 안티패턴을 벤더별로 비교합니다.
---

# 블록·파일 스토리지

> 문서 기준: 2026년 5월

## 개요

객체 스토리지는 HTTP API로 접근하는 비정형 데이터에 적합하지만, 데이터베이스처럼 빠른 I/O가 필요하거나, 여러 서버가 동시에 같은 파일에 접근해야 하는 경우에는 다른 스토리지가 필요합니다.

| 유형 | 접근 방식 | 온프레미스 비유 | 대표 용도 |
| --- | --- | --- | --- |
| **블록** | 디바이스 마운트 (디스크) | 서버에 장착한 SSD/HDD | DB, OS 부팅 디스크 |
| **파일** | 파일 시스템 마운트 (NFS/SMB) | NAS (공유 폴더) | 여러 서버가 동시 접근하는 공유 데이터 |
| **객체** | HTTP API (키-값) | — | 이미지, 백업, 데이터 레이크 |

### 왜 블록/파일 스토리지가 필요한가

객체 스토리지는 HTTP API로 접근하므로 저렴하고 확장성이 좋지만, **OS 부팅, DB 엔진, 여러 서버의 동시 쓰기**처럼 파일 시스템이 필요한 워크로드에는 사용할 수 없습니다.

| 용도 | 왜 블록/파일인가 | 객체로 대체 불가한 이유 |
| --- | --- | --- |
| OS 부팅 디스크 | 블록 디바이스로 마운트 필수 | OS는 HTTP API로 부팅 불가 |
| DB 데이터 파일 | 저지연 랜덤 I/O, POSIX 파일 시스템 필요 | DB 엔진이 블록 디바이스 요구 |
| 컨테이너 Persistent Volume | StatefulSet에 블록/파일 마운트 | 상태 유지 워크로드 |
| 공유 설정/미디어 (다수 서버 동시 접근) | NFS/SMB 마운트로 동시 R/W | 객체는 동시 쓰기 불가 |
| HPC 스크래치 (대규모 병렬 I/O) | Lustre 등 병렬 파일 시스템 | 처리량 수십 GB/s 필요 |

{% hint style="info" %}
온프레미스에서는 SAN/DAS에 FC/iSCSI로 연결하고 RAID를 직접 구성했습니다. 클라우드에서는 API로 볼륨을 생성/연결하며, 복제와 내구성은 벤더가 보장합니다. NAS(NetApp, Isilon)에 해당하는 파일 스토리지도 관리형으로 제공되어 용량 계획 없이 자동 확장됩니다. 단, 클라우드 블록 스토리지는 네트워크 연결이므로 온프레미스 DAS보다 지연이 약간 높을 수 있습니다.
{% endhint %}

## 블록 스토리지

온프레미스에서 서버에 SSD를 장착하듯, 클라우드에서는 VM에 가상 디스크를 연결합니다. 하나의 볼륨은 기본적으로 하나의 인스턴스에 연결되며, 가장 빠른 I/O 성능을 제공합니다.

{% hint style="warning" %}
클라우드 블록 스토리지는 네트워크를 통해 연결되므로, 인스턴스의 네트워크 대역폭을 스토리지 I/O와 앱 트래픽이 공유합니다. 인스턴스 타입별로 스토리지 전용 대역폭 상한이 있으며, 이를 초과하면 I/O가 스로틀링됩니다. 고성능 DB 워크로드에서는 인스턴스 타입 선택 시 스토리지 대역폭 스펙을 반드시 확인하세요.
{% endhint %}

### 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | EBS (Elastic Block Store) | 볼륨 타입이 가장 세분화 |
| Azure | Managed Disks | Premium SSD v2, Ultra Disk |
| GCP | Persistent Disk / Hyperdisk | 프로비저닝 후에도 IOPS/처리량 동적 변경 가능 |
| OCI | OCI Block Volumes | Balanced/Higher Performance/Ultra High Performance. 온라인 크기 변경 |

### 볼륨 타입별 사용 사례

| 용도 | AWS EBS | Azure Managed Disks | GCP |
| --- | --- | --- | --- |
| 범용 (웹 서버, 개발) | gp3 | Premium SSD v2 | pd-balanced |
| 고성능 DB (저지연 필수) | io2 Block Express | Ultra Disk | Hyperdisk Extreme |
| 빅데이터, 로그 (순차 I/O) | st1 | Standard HDD | pd-standard |
| 아카이브 (드문 접근) | sc1 | — | — |

스냅샷을 통한 백업과 복구에 대해서는 [백업과 복구](backup.md)에서 다룹니다.

### 주의: 가용영역 종속

블록 스토리지 볼륨은 생성된 가용영역(AZ)에 종속됩니다. 다른 AZ의 인스턴스에는 연결할 수 없습니다. 이는 각 벤더 모두 동일합니다.

| 벤더 | 기본 동작 | AZ 장애 대응 옵션 |
| --- | --- | --- |
| AWS | EBS는 단일 AZ에 종속 | 스냅샷으로 다른 AZ에 복원 |
| Azure | Managed Disk는 단일 Zone에 종속 | ZRS(Zone-Redundant Storage) 옵션으로 3개 AZ에 동기 복제 |
| GCP | Persistent Disk는 단일 Zone에 종속 | Regional Persistent Disk로 2개 Zone에 동기 복제 |
| OCI | Block Volume은 단일 AD에 종속 | Block Volume 복제(Cross-AD)로 다른 AD에 동기 복제 |

멀티 AZ 고가용성이 필요한 경우, 스냅샷 기반 복구 또는 벤더별 복제 옵션을 활용해야 합니다.

### 운영 시 알아둘 점

- **확장은 되지만 축소는 안 됨** — 볼륨 크기를 늘리는 것은 온라인으로 가능하지만, 줄이는 것은 지원되지 않습니다. 축소가 필요하면 작은 볼륨을 새로 만들어 데이터를 복사해야 합니다.
- **스냅샷 = 백업 + 복제** — 스냅샷을 다른 AZ나 리전에 복사하여 DR용으로 활용할 수 있습니다.
- **머신 이미지** — OS + 디스크 전체를 이미지로 저장하여 동일한 서버를 빠르게 복제할 수 있습니다 (AWS AMI, Azure VM Image, GCP Machine Image).
- **성능 변경** — AWS gp3와 GCP Hyperdisk는 볼륨을 분리하지 않고도 IOPS/처리량을 동적으로 변경할 수 있습니다.

## 파일 스토리지

온프레미스의 NAS에 해당합니다. 여러 서버가 동시에 같은 파일 시스템에 접근할 수 있으며, NFS(Linux) 또는 SMB(Windows) 프로토콜로 마운트합니다. 기존 애플리케이션이 파일 경로(`/data/file.txt`)로 접근하는 방식을 그대로 사용할 수 있어, 코드 수정 없이 클라우드로 이전할 수 있습니다.

### 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | EFS (Elastic File System) | NFS. 서버리스 — 용량 자동 확장, Lambda/컨테이너에서도 마운트 가능 |
| AWS | FSx | Windows(SMB), Lustre(HPC), NetApp, OpenZFS를 관리형으로 제공 |
| Azure | Azure Files | SMB/NFS 모두 지원. Azure File Sync로 온프레미스 연동 |
| GCP | Filestore | NFS 기반. Basic/Enterprise 티어 |
| OCI | OCI File Storage | NFSv3. 스냅샷, 복제 지원 |

### 안티패턴: 배포 원본으로 사용하지 마세요

{% hint style="warning" %}
온프레미스에서 NAS를 웹 서버 배포 원본으로 쓰는 패턴을 클라우드에 그대로 가져오면, 파일 스토리지가 객체 스토리지보다 5\~10배 비싸기 때문에 비용이 급증합니다. 클라우드에서는 컨테이너 이미지나 객체 스토리지 + CDN을 사용하고, 파일 스토리지는 여러 서버가 동시에 읽고 쓰는 공유 데이터에만 사용하세요.
{% endhint %}

## 핵심 차이점

**AWS** — EBS 볼륨 타입이 가장 세분화되어 있고, FSx로 Windows/Lustre/NetApp/OpenZFS 4종의 파일 시스템을 관리형으로 제공합니다. EFS는 서버리스로 용량 관리가 불필요합니다.

**Azure** — Azure Files가 SMB와 NFS를 모두 지원하여 Windows/Linux 혼합 환경에 유리합니다. File Sync로 온프레미스 파일 서버를 클라우드와 동기화할 수 있습니다.

**GCP** — Hyperdisk로 블록 스토리지 성능을 프로비저닝 후에도 동적으로 조절할 수 있습니다. Filestore는 Enterprise 티어에서 리전 간 복제를 지원합니다.

**OCI** — Block Volumes는 온라인 크기 변경과 성능 티어 변경을 지원하며, File Storage는 NFSv3 기반으로 스냅샷과 크로스 AD 복제를 제공합니다.

## 언제 무엇을 선택할 것인가

| 이럴 때 | 이것을 선택 |
| --- | --- |
| 고성능 DB용 저지연 블록 스토리지가 필요할 때 | AWS EBS io2 Block Express 또는 Azure Ultra Disk |
| 블록 스토리지 IOPS를 운영 중 동적으로 변경하고 싶을 때 | AWS EBS gp3 또는 GCP Hyperdisk |
| AZ 장애에도 블록 디스크가 유지되어야 할 때 | Azure ZRS Disk 또는 GCP Regional Persistent Disk |
| 여러 서버가 동시에 파일을 공유해야 할 때 (NFS) | AWS EFS 또는 GCP Filestore |
| Windows SMB + Linux NFS 혼합 환경일 때 | Azure Files |
| 온프레미스 파일 서버를 클라우드와 동기화할 때 | Azure File Sync |
| HPC용 고성능 파일 시스템이 필요할 때 | AWS FSx for Lustre |

## 통합 백업 관리

스냅샷은 개별 볼륨 단위이지만, 여러 서비스(VM, 블록, 파일, DB 등)의 백업을 하나의 정책으로 관리할 수 있는 통합 백업 서비스도 제공됩니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | AWS Backup | EBS, EFS, RDS, DynamoDB, S3 등 통합 관리. 크로스 리전/크로스 계정 백업 |
| Azure | Azure Backup | VM, Disks, Files, SQL, Blob 등 통합. Recovery Services Vault |
| GCP | Backup and DR Service | Compute Engine, GKE, Cloud SQL 등 통합 |
| OCI | OCI Backup | Block Volume, Boot Volume, DB 백업 통합 관리 |

{% hint style="info" %}
백업 주기 설계, 3-2-1 규칙, 랜섬웨어 대비, DR과의 관계 등 상세는 [백업과 복구](backup.md)를 참고하세요.
{% endhint %}

## 참고하기

### AWS

- [Amazon EBS 문서](https://docs.aws.amazon.com/ko_kr/ebs/)
- [EBS 볼륨 타입](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/ebs-volume-types.html)
- [EBS 스냅샷](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/EBSSnapshots.html)
- [Amazon EFS 문서](https://docs.aws.amazon.com/ko_kr/efs/)
- [Amazon FSx 문서](https://docs.aws.amazon.com/ko_kr/fsx/)
- [AMI(Amazon Machine Image)](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/AMIs.html)

### Azure

- [Azure Managed Disks 문서](https://learn.microsoft.com/ko-kr/azure/virtual-machines/managed-disks-overview)
- [디스크 유형 비교](https://learn.microsoft.com/ko-kr/azure/virtual-machines/disks-types)
- [ZRS(영역 중복 스토리지) 디스크](https://learn.microsoft.com/ko-kr/azure/virtual-machines/disks-redundancy#zone-redundant-storage-for-managed-disks)
- [Azure Files 문서](https://learn.microsoft.com/ko-kr/azure/storage/files/)
- [Azure File Sync](https://learn.microsoft.com/ko-kr/azure/storage/file-sync/)

### GCP

- [Persistent Disk 문서](https://cloud.google.com/compute/docs/disks)
- [Hyperdisk 문서](https://cloud.google.com/compute/docs/disks/hyperdisks)
- [Regional Persistent Disk](https://cloud.google.com/compute/docs/disks/regional-persistent-disk)
- [Filestore 문서](https://cloud.google.com/filestore/docs)
- [Machine Image](https://cloud.google.com/compute/docs/machine-images)

### OCI

- [OCI Block Volumes 문서](https://docs.oracle.com/en-us/iaas/Content/Block/home.htm)
- [OCI File Storage 문서](https://docs.oracle.com/en-us/iaas/Content/File/home.htm)
