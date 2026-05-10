# 객체 스토리지

> 문서 기준: 2026년 5월

## 개요

자체 전산센터에서 파일을 저장하려면 NAS나 SAN을 구매하고, 용량이 부족해지면 디스크를 추가해야 합니다. 용량 계획을 잘못하면 공간이 부족하거나 과잉 투자가 됩니다.

**객체 스토리지**는 용량 제한 없이 파일을 저장할 수 있는 클라우드 스토리지입니다. 용량을 미리 정할 필요 없이, 저장한 만큼만 비용을 지불합니다. 이미지, 동영상, 백업, 로그, 데이터 레이크 등 거의 모든 비정형 데이터를 저장하는 데 사용됩니다.

> S3를 아시는 분을 위해: Azure는 Blob Storage, GCP는 Cloud Storage, OCI는 Object Storage입니다.

### 왜 객체 스토리지인가

- **매우 저렴** — GB당 월 $0.02\~0.03 수준으로, 블록 스토리지(GB당 $0.08\~0.10)나 파일 스토리지보다 훨씬 저렴합니다. 아카이브 클래스를 사용하면 GB당 $0.001 이하까지 낮출 수 있습니다. 단, 아카이브 클래스는 데이터 복구(retrieval) 시 별도 비용과 대기 시간이 발생합니다.
- **무제한 용량** — 저장 용량에 상한이 없습니다. 1KB부터 수 PB까지 동일한 방식으로 저장합니다.
- **내구성** (Durability) — 각 벤더 모두 **99.999999999% (11 nines)** 내구성을 제공합니다. 이는 1,000만 개의 객체를 저장하면 1만 년에 1개를 잃을 확률입니다. 여러 AZ에 자동 복제되어 데이터 유실 가능성이 사실상 없습니다.
- **HTTP API 접근** — 파일 시스템(폴더/경로)이 아닌 키-값(Key-Value) 구조로, REST API를 통해 어디서든 접근합니다.
- **S3 호환 API** — AWS S3가 사실상 표준 API가 되어, 대부분의 벤더와 도구가 S3 호환 API를 지원합니다.

## 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | S3 (Simple Storage Service) | 사실상 업계 표준. 스토리지 클래스 다양 (Standard, IA, Glacier 등) |
| Azure | Blob Storage | Hot/Cool/Cold/Archive 티어. Data Lake Storage Gen2 통합 |
| GCP | Cloud Storage | Standard/Nearline/Coldline/Archive. Multi-region/Dual-region 자동 복제 |
| OCI | OCI Object Storage | Standard/Infrequent Access/Archive 티어. S3 호환 API 지원 |

### 스토리지 클래스 (접근 빈도별 비용 최적화)

데이터는 시간이 지나면 접근 빈도가 줄어듭니다. 각 벤더 모두 접근 빈도에 따라 저장 비용을 낮출 수 있는 스토리지 클래스를 제공합니다. 저장 비용은 낮아지지만 조회 비용은 높아지므로, 접근 패턴에 맞는 클래스를 선택해야 합니다.

| 접근 빈도 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| 자주 접근 | S3 Standard | Hot | Standard | Standard |
| 가끔 접근 | S3 Standard-IA | Cool | Nearline (30일) | Infrequent Access |
| 드물게 접근 | S3 Glacier Instant | Cold | Coldline (90일) | — |
| 아카이브 | S3 Glacier Deep Archive | Archive | Archive (365일) | Archive |
| **자동 전환** | S3 Intelligent-Tiering | — | Autoclass | Auto-Tiering |

AWS S3 Intelligent-Tiering과 GCP Autoclass는 접근 패턴을 자동으로 분석하여 최적의 클래스로 이동시켜 줍니다. 수동으로 수명 주기 정책을 설정할 필요가 없어 운영 부담이 줄어듭니다.

## 핵심 차이점

**AWS S3** — 2006년 출시로 가장 오래되었고, S3 API가 업계 사실상 표준이 되었습니다. 대부분의 3rd party 도구, 다른 클라우드 벤더, 온프레미스 스토리지까지 S3 호환 API를 지원합니다. S3 Tables, S3 Metadata, S3 Vectors 등 스토리지 자체에 분석 기능을 내장하는 방향으로 가장 적극적으로 진화하고 있습니다.

**Azure Blob Storage** — Blob Storage와 Data Lake Storage Gen2가 동일한 스토리지 계정에서 통합됩니다. 계층적 네임스페이스(폴더 구조)를 지원하여 빅데이터 워크로드에서 파일 관리가 편리합니다. Microsoft Fabric과의 통합으로 분석 파이프라인 구성이 간편합니다.

**GCP Cloud Storage** — Multi-region과 Dual-region 옵션으로 별도 복제 설정 없이 여러 리전에 자동 복제됩니다. Autoclass로 스토리지 클래스 자동 전환을 지원하며, BigLake를 통해 BigQuery에서 직접 쿼리할 수 있습니다.

**OCI Object Storage** — S3 호환 API를 지원하며, Auto-Tiering으로 접근 패턴에 따라 Standard/Infrequent Access 간 자동 전환됩니다. 이그레스 10TB/월 무료 정책으로 대량 데이터 전송 시 비용 이점이 큽니다.

## 언제 무엇을 선택할 것인가

| 이럴 때 | 이것을 선택 |
| --- | --- |
| S3 호환 API 생태계를 최대한 활용하고 싶을 때 | AWS S3 |
| 빅데이터 + 계층적 네임스페이스(폴더 구조)가 필요할 때 | Azure Data Lake Storage Gen2 |
| 별도 설정 없이 멀티 리전 자동 복제를 원할 때 | GCP Cloud Storage (Multi-region) |
| 스토리지 클래스 자동 전환을 원할 때 | AWS S3 Intelligent-Tiering 또는 GCP Autoclass |
| 대량 이그레스 비용을 절감하고 싶을 때 | OCI Object Storage (10TB/월 무료) |
| 객체 스토리지에서 직접 SQL 분석을 하고 싶을 때 | AWS Athena + S3 또는 GCP BigQuery External Tables |

## 객체 스토리지의 진화

객체 스토리지는 단순 파일 저장소를 넘어 **데이터 레이크의 기본 저장소**로 자리잡았습니다. 과거에는 데이터 분석을 위해 별도의 데이터 웨어하우스에 데이터를 복사해야 했지만, 이제는 객체 스토리지에 데이터를 그대로 두고 직접 분석하는 **레이크하우스** (Lakehouse) 아키텍처가 표준이 되고 있습니다.

| 기능 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **데이터 레이크** | S3 + Lake Formation | Data Lake Storage Gen2 + Fabric | Cloud Storage + BigLake | OCI Object Storage + Data Lake |
| **테이블 저장 (Iceberg)** | S3 Tables | Data Lake Storage + Synapse | BigLake (Iceberg 네이티브) | — |
| **메타데이터 자동 관리** | S3 Metadata | Blob Index Tags | — | — |
| **벡터 저장/검색** | S3 Vectors (Preview) | AI Search + Blob 연동 | BigQuery Vector Index | AI Vector Search (Autonomous DB) |
| **SQL 직접 쿼리** | S3 Select, Athena | Query Acceleration, Synapse | BigQuery External Tables | OCI Data Flow (Spark) |

각 벤더 모두 "스토리지에서 데이터 플랫폼으로"의 방향을 추구하고 있습니다. AWS는 S3 자체에 기능을 내장하는 방향이고, Azure는 Data Lake Storage + Fabric 통합, GCP는 BigLake + BigQuery 통합으로 접근하고 있습니다.

## 참고하기

### AWS

- [Amazon S3 문서](https://docs.aws.amazon.com/ko_kr/s3/)
- [Amazon S3 스토리지 클래스](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/storage-class-intro.html)
- [S3 Intelligent-Tiering](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/intelligent-tiering.html)
- [S3 Tables 문서](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/s3-tables.html)
- [S3 Metadata 문서](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/s3-metadata.html)
- [AWS Lake Formation 문서](https://docs.aws.amazon.com/ko_kr/lake-formation/)
- [Amazon Athena 문서](https://docs.aws.amazon.com/ko_kr/athena/)

### Azure

- [Azure Blob Storage 문서](https://learn.microsoft.com/ko-kr/azure/storage/blobs/)
- [Azure Blob 액세스 계층](https://learn.microsoft.com/ko-kr/azure/storage/blobs/access-tiers-overview)
- [Data Lake Storage Gen2 문서](https://learn.microsoft.com/ko-kr/azure/storage/blobs/data-lake-storage-introduction)
- [Azure Synapse Analytics 문서](https://learn.microsoft.com/ko-kr/azure/synapse-analytics/)
- [Microsoft Fabric 문서](https://learn.microsoft.com/ko-kr/fabric/)

### GCP

- [Google Cloud Storage 문서](https://cloud.google.com/storage/docs)
- [Cloud Storage 클래스](https://cloud.google.com/storage/docs/storage-classes)
- [Autoclass 문서](https://cloud.google.com/storage/docs/autoclass)
- [BigLake 문서](https://cloud.google.com/biglake/docs)
- [BigQuery External Tables](https://cloud.google.com/bigquery/docs/external-data-cloud-storage)

### OCI

- [OCI Object Storage 문서](https://docs.oracle.com/en-us/iaas/Content/Object/home.htm)
- [OCI Object Storage 스토리지 티어](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/understandingstoragetiers.htm)
