---
description: 대용량 데이터를 클라우드로 이전하는 온라인/오프라인 전송 방법과 도구를 벤더별로 비교합니다.
---

# 스토리지 마이그레이션

> 문서 기준: 2026년 5월

## 개요

온프레미스나 다른 클라우드에 있는 대용량 데이터를 클라우드로 이전하는 작업입니다. 단순히 `aws s3 cp`로 올리면 될 것 같지만, 수 TB~수 PB 규모에서는 네트워크 대역폭, 비용, 시간 모두가 큰 제약이 됩니다.

### 마이그레이션 유형

| 유형 | 설명 | 대상 |
| --- | --- | --- |
| **온라인 전송** | 네트워크를 통해 데이터 전송 | 수 GB~수 TB, 빠른 네트워크 환경 |
| **오프라인 전송** | 물리 장치에 데이터를 담아 배송 | 수십 TB~수 PB, 제한적 네트워크 환경 |
| **하이브리드 복제** | 초기 오프라인 + 이후 온라인 증분 | 대용량 + 지속 업데이트 필요 |
| **파일 게이트웨이** | 온프레미스 캐시 + 클라우드 저장소 | 점진적 전환, 접근 지연 허용 |

## 전송 방법 선택 기준

데이터 크기와 네트워크 속도에 따라 전송 시간이 결정됩니다.

| 데이터 크기 | 1Gbps 네트워크 | 10Gbps 네트워크 | 권장 방법 |
| --- | --- | --- | --- |
| 100GB | 약 15분 | 약 2분 | 온라인 (일반 전송) |
| 1TB | 약 2.5시간 | 약 15분 | 온라인 (DataSync, Storage Transfer Service) |
| 10TB | 약 25시간 | 약 2.5시간 | 온라인 + 전용 연결 (Direct Connect, ExpressRoute) |
| 100TB | 약 10일 | 약 25시간 | 오프라인 (Snowball, Data Box) |
| 1PB | 약 100일 | 약 10일 | 오프라인 (Snowmobile, Data Box Heavy) |

> 위 수치는 예시이며 리전/시점에 따라 달라집니다. 최신 가격은 각 벤더 공식 가격표를 확인하세요.

{% hint style="warning" %}
실제 전송 시간은 네트워크 효율성, 재시도, 검증 시간을 포함하면 위 계산의 1.5~2배가 일반적입니다.
{% endhint %}

## 비용 고려사항

스토리지 마이그레이션은 전송 방법 선택이 비용에 큰 영향을 줍니다.

| 항목 | 온라인 전송 | 오프라인 전송 |
| --- | --- | --- |
| **이그레스 비용 (반출 시)** | GB당 $0.05~$0.126 | 디바이스 고정 요금 |
| **수집 비용** | 무료 (대부분) | 무료 |
| **저장 비용** | 동일 | 동일 |
| **장비 임대비** | 없음 | $50~$15,000 (크기별) |
| **전송 시간** | 네트워크 속도 의존 | 2~3주 고정 |
| **인력 비용** | 자동화 가능 | 장비 수령/반송 처리 필요 |

> 위 수치는 예시이며 리전/시점에 따라 달라집니다. 최신 가격은 각 벤더 공식 가격표를 확인하세요.

{% hint style="info" %}
**팁:** 10TB 이상의 일회성 마이그레이션이라면 오프라인 전송이 일반적으로 더 저렴하고 빠릅니다. 지속적인 동기화나 소규모 이전은 온라인 방식이 유리합니다.
{% endhint %}

## 온라인 전송 서비스

### 대용량 파일 전송

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | [DataSync](https://aws.amazon.com/datasync/) | NFS/SMB/S3 간 온라인 전송. 증분 전송 지원 |
| AWS | [Storage Gateway](https://aws.amazon.com/storagegateway/) | 온프레미스 캐시 + S3 백엔드 |
| Azure | [AzCopy](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10) | CLI 기반 고성능 Blob 전송 |
| Azure | [Azure File Sync](https://learn.microsoft.com/azure/storage/file-sync/) | 온프레미스 Windows 파일 서버와 Azure Files 동기화 |
| Google Cloud | [Storage Transfer Service](https://cloud.google.com/storage-transfer-service) | S3/Azure Blob/HTTP에서 Cloud Storage로 전송 |
| Google Cloud | [gsutil / gcloud storage](https://cloud.google.com/storage/docs/gsutil) | CLI 기반 병렬 전송 |
| OCI | [OCI Data Transfer](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm) | CLI와 오프라인 방식 모두 지원 |
| OCI | [rclone / OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) | 다목적 동기화 도구 |

### 객체 스토리지 간 복제

한 객체 스토리지에서 다른 객체 스토리지로 지속적으로 복제합니다. 멀티클라우드 환경이나 DR 목적으로 사용합니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | S3 Cross-Region Replication (CRR) | 같은 계정/다른 계정 모두 지원 |
| AWS | S3 Replication Time Control (RTC) | 15분 내 99.99% 복제 SLA |
| Azure | Blob Object Replication | 계정 간 비동기 복제 |
| Google Cloud | Cloud Storage Cross-Region / Multi-Region | 스토리지 클래스 선택 시 자동 복제 |
| OCI | Object Storage Replication | 리전 간/네임스페이스 간 복제 |

## 오프라인 전송 서비스

네트워크로 전송이 비현실적일 만큼 데이터가 크거나, 네트워크 환경이 제한적일 때 사용합니다.

| 벤더 | 제품 | 용량 | 특징 |
| --- | --- | --- | --- |
| AWS | [Snowcone](https://aws.amazon.com/snowcone/) | ~8 TB | 소형, 배낭 휴대 가능 |
| AWS | [Snowball Edge](https://aws.amazon.com/snowball/) | ~80 TB | 일반적인 대용량 이전 |
| AWS | Snowmobile | ~100 PB | 컨테이너 트럭 규모 (단, 2024년 이후 신규 주문 종료) |
| Azure | [Data Box Disk](https://azure.microsoft.com/products/databox/) | ~35 TB | SSD 기반 소용량 |
| Azure | [Data Box](https://azure.microsoft.com/products/databox/) | ~100 TB | 표준 장비 |
| Azure | Data Box Heavy | ~1 PB | 대용량 장비 |
| Google Cloud | [Transfer Appliance](https://cloud.google.com/transfer-appliance/docs) | TA40: ~40 TB, TA300: ~300 TB | 일반/대용량 |
| OCI | [Data Transfer Appliance](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm) | ~150 TB | 임대 장비로 전송 |
| OCI | Data Transfer Disk | ~32 TB | 고객이 디스크 구매 후 발송 |

> 위 수치는 예시이며 리전/시점에 따라 달라집니다. 최신 가격은 각 벤더 공식 가격표를 확인하세요.

### 오프라인 전송 단계

1. 벤더 콘솔/API에서 장치 주문
2. 벤더가 장치를 배송
3. 온프레미스에서 데이터를 장치에 복사
4. 장치를 벤더에게 반송
5. 벤더가 데이터센터에서 클라우드 스토리지로 업로드
6. 검증 후 장치의 데이터는 안전하게 삭제

전송 기간은 일반적으로 2~3주 정도 소요되며, 네트워크 이그레스 비용을 크게 절감할 수 있습니다.

## 하이브리드 캐시/게이트웨이

온프레미스 애플리케이션이 변경 없이 클라우드 스토리지를 사용하게 하는 방식입니다.

| 벤더 | 제품 | 제공 형태 |
| --- | --- | --- |
| AWS | [Storage Gateway](https://aws.amazon.com/storagegateway/) | File/Volume/Tape Gateway |
| Azure | [Azure File Sync](https://learn.microsoft.com/azure/storage/file-sync/) | 파일 서버 확장 |
| Google Cloud | [Cloud Storage FUSE](https://cloud.google.com/storage/docs/cloud-storage-fuse/overview) | 파일 시스템처럼 마운트 |
| OCI | [Storage Gateway](https://docs.oracle.com/en-us/iaas/Content/StorageGateway/home.htm) | NFS v4 인터페이스 |

## 검증과 무결성

대용량 데이터 전송 후에는 무결성 검증이 필수입니다.

- **체크섬 검증** — 각 파일의 MD5/SHA256 해시를 비교
- **파일 수/크기 비교** — 원본과 대상의 메타데이터 일치 확인
- **샘플링 테스트** — 무작위 파일을 다운로드하여 실제 열람 가능 확인
- **권한 유지 확인** — 소유자, 읽기/쓰기 권한, ACL 보존 여부

벤더 도구들은 대부분 자동 검증을 수행하지만, 중요 데이터는 수동 검증도 병행하는 것이 안전합니다.

## 자주 하는 실수

- **네트워크 전송 시간을 과소 추정** — 이론적 대역폭으로 계산하지만 실제는 1.5~2배 소요. 재시도, 검증, 네트워크 효율을 고려해야 함
- **전송 후 무결성 검증을 생략** — 체크섬 비교 없이 파일 수만 확인하여 손상된 파일을 뒤늦게 발견
- **이그레스 비용을 사전에 산정하지 않음** — 수십 TB 온라인 전송 시 이그레스 비용이 오프라인 장비 임대비보다 비쌀 수 있음

## 체크리스트

- [ ] 데이터 크기와 네트워크 속도를 기반으로 온라인/오프라인 전송 방법을 선택했는가
- [ ] 전송 완료 후 체크섬(MD5/SHA256) 기반 무결성 검증을 수행하는가
- [ ] 이그레스 비용과 장비 임대비를 비교하여 비용 최적 방법을 선택했는가

## 참고하기

### AWS

- [AWS Cloud Data Migration](https://aws.amazon.com/cloud-data-migration/)
- [AWS DataSync 문서](https://docs.aws.amazon.com/datasync/)
- [AWS Snow Family 문서](https://docs.aws.amazon.com/snowball/)
- [AWS Storage Gateway 문서](https://docs.aws.amazon.com/storagegateway/)

### Azure

- [Azure Storage migration overview](https://learn.microsoft.com/azure/storage/common/storage-migration-overview)
- [AzCopy 문서](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10)
- [Azure Data Box 문서](https://learn.microsoft.com/azure/databox/)
- [Azure File Sync 문서](https://learn.microsoft.com/azure/storage/file-sync/)

### Google Cloud

- [Storage Transfer Service 문서](https://cloud.google.com/storage-transfer-service/docs)
- [Transfer Appliance 문서](https://cloud.google.com/transfer-appliance/docs)
- [Cloud Storage FUSE 문서](https://cloud.google.com/storage/docs/cloud-storage-fuse/overview)

### OCI

- [OCI Data Transfer 문서](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm)
- [OCI Storage Gateway 문서](https://docs.oracle.com/en-us/iaas/Content/StorageGateway/home.htm)
- [OCI Object Storage Replication](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/usingreplication.htm)
