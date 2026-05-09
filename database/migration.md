# 데이터베이스 마이그레이션

## 개요

온프레미스 DB를 클라우드로 이전하거나, 클라우드 간 DB를 이동할 때 **마이그레이션 서비스**를 사용합니다. 단순 백업/복원으로도 가능하지만, 대규모 DB에서는 다운타임을 최소화하면서 지속적으로 데이터를 동기화하는 **온라인 마이그레이션**이 필요합니다.

### 마이그레이션 유형

| 유형 | 설명 | 다운타임 |
| --- | --- | --- |
| **동종 마이그레이션** | 같은 엔진 간 이동 (MySQL → MySQL) | 최소 (CDC로 실시간 동기화) |
| **이종 마이그레이션** | 다른 엔진으로 전환 (Oracle → PostgreSQL) | 스키마 변환 + 데이터 이동 필요 |
| **지속적 복제** | 온프레미스 ↔ 클라우드 실시간 동기화 | 없음 (하이브리드 운영) |

## 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | DMS (Database Migration Service) | 동종/이종 마이그레이션. CDC(Change Data Capture)로 지속 복제 |
| AWS | SCT (Schema Conversion Tool) | 이종 마이그레이션 시 스키마 자동 변환 |
| Azure | Azure Database Migration Service | 온라인/오프라인 마이그레이션. Azure SQL로의 이동에 최적화 |
| Azure | Azure Migrate | DB 포함 전체 워크로드 마이그레이션 평가/실행 |
| GCP | Database Migration Service | MySQL, PostgreSQL, SQL Server → Cloud SQL/AlloyDB |
| GCP | Datastream | CDC 기반 실시간 복제. BigQuery로 스트리밍 가능 |

## 핵심 차이점

**AWS DMS** — 가장 많은 소스/타겟 엔진 조합을 지원합니다. Oracle, SQL Server, MongoDB, S3 등 다양한 소스에서 AWS DB로 마이그레이션할 수 있습니다. SCT와 함께 사용하면 이종 마이그레이션의 스키마 변환을 자동화합니다.

**Azure** — Azure SQL로의 마이그레이션에 특화되어 있으며, SQL Server 워크로드 이전이 가장 매끄럽습니다. Azure Migrate로 마이그레이션 전 평가(호환성, 비용 추정)를 수행할 수 있습니다.

**GCP Datastream** — CDC 기반 실시간 복제를 제공하며, BigQuery로 직접 스트리밍하여 분석 파이프라인을 구성할 수 있습니다.

## 참고하기

### AWS

- [AWS DMS 문서](https://docs.aws.amazon.com/ko_kr/dms/)
- [AWS SCT 문서](https://docs.aws.amazon.com/ko_kr/SchemaConversionTool/)

### Azure

- [Azure Database Migration Service 문서](https://learn.microsoft.com/ko-kr/azure/dms/)
- [Azure Migrate 문서](https://learn.microsoft.com/ko-kr/azure/migrate/)

### GCP

- [Database Migration Service 문서](https://cloud.google.com/database-migration/docs)
- [Datastream 문서](https://cloud.google.com/datastream/docs)
