# 관리형 RDB

## 개요

온프레미스에서 데이터베이스를 운영하려면 서버 설치, OS 패치, DB 엔진 설치, 백업 설정, 복제 구성, 장애 조치를 모두 직접 해야 합니다. **관리형 RDB(Relational Database)**는 이 운영 부담을 벤더가 대신 처리하고, 사용자는 데이터와 쿼리에만 집중할 수 있게 합니다.

자동 백업, 패치 적용, 멀티 AZ 복제, 읽기 전용 복제본(Read Replica) 등을 설정 몇 번으로 구성할 수 있습니다.

## 제품 비교

### 범용 관리형 RDB

| 벤더 | 제품 | 지원 엔진 |
| --- | --- | --- |
| AWS | RDS | MySQL, PostgreSQL, MariaDB, Oracle, SQL Server |
| AWS | Aurora | MySQL/PostgreSQL 호환. AWS 자체 설계 스토리지 엔진 |
| Azure | Azure SQL Database | SQL Server 기반 |
| Azure | Azure Database for MySQL/PostgreSQL/MariaDB | 오픈소스 엔진 관리형 |
| GCP | Cloud SQL | MySQL, PostgreSQL, SQL Server |
| GCP | AlloyDB | PostgreSQL 호환. Google 자체 설계 |
| OCI | OCI Autonomous Database | Oracle DB 기반. 자동 튜닝/패치/스케일링 |
| OCI | OCI MySQL HeatWave | MySQL 호환. OLTP + OLAP 통합 처리 |

### 클라우드 네이티브 DB

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Aurora Serverless | 사용량 기반 자동 스케일링. 유휴 시 비용 0 가능 |
| Azure | Azure SQL Serverless | 자동 일시 중지/재개 |
| GCP | AlloyDB | AI/ML 워크로드에 최적화. 벡터 검색 내장 |
| OCI | OCI Autonomous Database Serverless | 자동 스케일링. 유휴 시 자동 중지 가능 |

## 일반 관리형 RDB vs 클라우드 네이티브 DB

일반 관리형 RDB(RDS, Cloud SQL)는 기존 DB 엔진을 그대로 사용하되 운영만 자동화한 것입니다. 반면 Aurora, AlloyDB 같은 **클라우드 네이티브 DB**는 스토리지 계층을 자체 설계하여 근본적으로 다른 아키텍처를 가집니다.

| 항목 | 일반 관리형 (RDS, Cloud SQL) | 클라우드 네이티브 (Aurora, AlloyDB) |
| --- | --- | --- |
| **스토리지** | 인스턴스에 연결된 블록 디스크 (EBS 등) | 컴퓨팅과 분리된 분산 스토리지 계층 |
| **복제** | 별도 복제본 인스턴스 (데이터 전체 복사) | 스토리지 자체가 멀티 AZ 복제 (6개 복사본) |
| **스케일링** | 읽기 복제본 추가 시 데이터 복사 필요 | 읽기 복제본이 동일 스토리지 공유 (추가 빠름) |
| **장애 조치** | 대기 인스턴스로 전환 (수십 초) | 스토리지 유지 + 새 컴퓨팅 연결 (수 초) |
| **용량 관리** | 디스크 크기 사전 지정 | 자동 확장 (최대 128~256 TiB) |

Aurora는 데이터를 3개 AZ에 걸쳐 6개 복사본으로 자동 복제하며, 컴퓨팅(DB 인스턴스)과 스토리지가 분리되어 있어 인스턴스를 추가/제거해도 데이터 복사가 필요 없습니다. AlloyDB도 유사하게 컴퓨팅과 스토리지를 분리한 아키텍처를 사용합니다.

## 핵심 차이점

**AWS Aurora** — MySQL/PostgreSQL과 호환되면서 최대 5배(MySQL) / 3배(PostgreSQL) 성능을 제공한다고 AWS가 주장합니다. 스토리지가 3개 AZ에 6개 복사본으로 자동 복제됩니다.

**Azure SQL Database** — SQL Server 기반으로, 기존 SQL Server 워크로드를 가장 쉽게 마이그레이션할 수 있습니다. Hyperscale 티어에서 100TB까지 확장 가능합니다.

**GCP AlloyDB** — PostgreSQL 호환이면서 Google 자체 설계로 트랜잭션 성능을 높였습니다. 벡터 검색이 내장되어 AI 워크로드와의 통합이 강점입니다.

## 참고하기

### AWS

- [Amazon RDS 문서](https://docs.aws.amazon.com/ko_kr/rds/)
- [Amazon Aurora 문서](https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/AuroraUserGuide/)

### Azure

- [Azure SQL Database 문서](https://learn.microsoft.com/ko-kr/azure/azure-sql/)
- [Azure Database for PostgreSQL 문서](https://learn.microsoft.com/ko-kr/azure/postgresql/)

### GCP

- [Cloud SQL 문서](https://cloud.google.com/sql/docs)
- [AlloyDB 문서](https://cloud.google.com/alloydb/docs)

### OCI

- [OCI Autonomous Database 문서](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html)
- [OCI MySQL HeatWave 문서](https://docs.oracle.com/en-us/iaas/mysql-database/index.html)
