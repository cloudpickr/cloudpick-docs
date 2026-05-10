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
| OCI | OCI Database Migration | Oracle/MySQL → OCI DB. 온라인 마이그레이션(Zero Downtime) 지원 |

## 핵심 차이점

**AWS DMS** — 가장 많은 소스/타겟 엔진 조합을 지원합니다. Oracle, SQL Server, MongoDB, S3 등 다양한 소스에서 AWS DB로 마이그레이션할 수 있습니다. SCT와 함께 사용하면 이종 마이그레이션의 스키마 변환을 자동화합니다.

**Azure** — Azure SQL로의 마이그레이션에 특화되어 있으며, SQL Server 워크로드 이전이 가장 매끄럽습니다. Azure Migrate로 마이그레이션 전 평가(호환성, 비용 추정)를 수행할 수 있습니다.

**GCP Datastream** — CDC 기반 실시간 복제를 제공하며, BigQuery로 직접 스트리밍하여 분석 파이프라인을 구성할 수 있습니다.

**OCI Database Migration** — Oracle/MySQL DB를 OCI로 온라인 마이그레이션(Zero Downtime)할 수 있으며, GoldenGate 기반의 실시간 복제를 지원합니다.

## 마이그레이션 전략

데이터베이스 마이그레이션은 크게 3가지 전략(6R 중 DB 관련)으로 나뉩니다. 복잡도와 비용이 다르므로 워크로드 특성에 맞게 선택합니다.

| 전략 | 설명 | 적합한 경우 | 예시 |
| --- | --- | --- | --- |
| **Rehost** (리호스트) | 동일 엔진을 그대로 클라우드로 이동. "Lift and Shift" | 빠른 이전이 목표, 엔진 변경 불필요 | MySQL → RDS MySQL, Oracle → OCI DB System |
| **Replatform** (리플랫폼) | 엔진은 유지하되 관리형 서비스로 전환. 일부 최적화 적용 | 운영 부담 감소가 목표, 코드 변경 최소화 | MySQL → Aurora MySQL, PostgreSQL → AlloyDB |
| **Refactor** (리팩터) | 엔진을 변경하거나 아키텍처를 재설계 | 성능/비용/확장성 근본 개선이 목표 | Oracle → PostgreSQL, 모놀리식 DB → DynamoDB + RDS 분리 |

### 전략 선택 기준

- **시간 제약이 클 때** → Rehost (가장 빠름)
- **운영 비용을 줄이고 싶을 때** → Replatform (관리형 전환)
- **라이선스 비용 절감 또는 확장성 한계를 해결할 때** → Refactor (가장 높은 효과, 가장 높은 비용/위험)

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

### OCI

- [OCI Database Migration 문서](https://docs.oracle.com/en-us/iaas/database-migration/index.html)
