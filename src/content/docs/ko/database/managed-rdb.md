---
title: "관리형 RDB"
description: "관리형 RDB와 클라우드 네이티브 DB의 차이, HA 구성, PITR을 벤더별로 비교합니다."
---

> 문서 기준: 2026년 8월

## 개요

온프레미스에서 데이터베이스를 운영하려면 서버 설치, OS 패치, DB 엔진 설치, 백업 설정, 복제 구성, 장애 조치를 모두 직접 해야 합니다. **관리형 RDB**는 이 운영 부담을 벤더가 대신 처리하고, 사용자는 데이터와 쿼리에만 집중할 수 있게 합니다.

:::note
AWS RDS를 아시는 분을 위해: Azure는 Azure SQL/Flexible Server, Google Cloud는 Cloud SQL, OCI는 Autonomous Database입니다.
:::

### DBA 역할의 변화

| 영역 | 온프레미스 DBA | 관리형 RDB 환경 |
| --- | --- | --- |
| OS/패치 관리 | 직접 수행 | 벤더가 처리 |
| 백업/복구 | 스크립트 작성, 테스트 | 자동 백업 + PITR 내장 |
| HA/복제 구성 | 직접 설계·운영 | 멀티 AZ 체크박스 |
| 성능 튜닝 | 쿼리 + 인프라 모두 | **쿼리/스키마 최적화에 집중** |
| 용량 계획 | 디스크 구매·확장 | 온라인 확장 또는 자동 확장 |

:::caution
특별한 이유가 없다면 관리형을 우선 선택하세요. VM에 직접 설치하는 경우는 "관리형이 지원하지 않는 엔진/버전", "OS 레벨 접근 필요", "BYOL 라이선스 비용 절감" 등 명확한 요건이 있을 때입니다.
:::

:::note
DB 선택 후의 운영 — 확장 패턴, 쿼리 성능, 캐시, HA, 백업 — 은 [데이터베이스 운영](../../database/operations/)을 참고하세요.
:::

## 제품 비교

### 범용 관리형 RDB

| 벤더 | 제품 | 유형 | 지원 엔진 |
| --- | --- | --- | --- |
| AWS | RDS | 관리형 | MySQL, PostgreSQL, MariaDB, Oracle, SQL Server |
| AWS | Aurora | **네이티브** | MySQL/PostgreSQL 호환. 자체 설계 분산 스토리지 |
| AWS | Aurora DSQL | **네이티브** | PostgreSQL 호환 분산 SQL. 서버리스. 단일 리전 99.99%·멀티 리전 99.999% 가용성 설계. GA (2025.05). CDC 지원 GA (2026.07) |
| Azure | Azure SQL Database | 관리형 | SQL Server 기반 |
| Azure | Azure Database for MySQL/PostgreSQL | 관리형 | 오픈소스 엔진 관리형 |
| Google Cloud | Cloud SQL | 관리형 | MySQL, PostgreSQL, SQL Server |
| Google Cloud | AlloyDB | **네이티브** | PostgreSQL 호환. 자체 설계. 벡터 검색 내장. AlloyDB Omni(K8s Operator 1.7.0 GA)로 온프레미스/멀티클라우드 배포 지원. PostgreSQL 18 호환 |
| OCI | Autonomous Database | **네이티브** | Oracle DB 기반. 자동 튜닝/패치/스케일링 |
| OCI | MySQL HeatWave | 관리형 | MySQL 호환. OLTP + OLAP 통합 처리 |

### 클라우드 네이티브 DB란

일반 관리형(RDS, Cloud SQL)은 기존 DB 엔진을 그대로 사용하되 운영만 자동화한 것입니다. Aurora, AlloyDB 같은 **클라우드 네이티브 DB**는 스토리지 계층을 자체 설계하여 근본적으로 다른 아키텍처를 가집니다.

| 항목 | 일반 관리형 | 클라우드 네이티브 |
| --- | --- | --- |
| **스토리지** | 인스턴스에 연결된 블록 디스크 | 컴퓨팅과 분리된 분산 스토리지 |
| **복제** | 별도 인스턴스에 데이터 전체 복사 | 스토리지 자체가 멀티 AZ 복제 |
| **읽기 복제본 추가** | 데이터 복사 필요 (느림) | 동일 스토리지 공유 (빠름) |
| **장애 조치** | 대기 인스턴스로 전환 (수십 초) | 새 컴퓨팅 연결 (수 초) |
| **용량** | 디스크 크기 사전 지정 | 자동 확장 |

### 글로벌 분산 DB

리전을 넘어 전 세계에 데이터를 분산하고, 각 리전에서 읽기/쓰기가 가능한 DB입니다. 일반 관리형의 "크로스 리전 읽기 복제본"과 달리, **멀티 리전 쓰기**를 지원하는 서비스가 있습니다.

| 유형 | 벤더 | 제품 | 멀티 리전 쓰기 | 일관성 |
| --- | --- | --- | --- | --- |
| **RDB** | AWS | Aurora Global Database | — (읽기만 분산, 쓰기는 단일 리전) | 강한 일관성 (프라이머리) |
| **RDB** | AWS | Aurora DSQL | 지원 (액티브-액티브 멀티 리전) | 강한 일관성 (분산 트랜잭션) |
| **RDB** | Google Cloud | Spanner | 지원 | 강한 일관성 (글로벌 트랜잭션) |
| **NoSQL** | Azure | Cosmos DB | 지원 | 5가지 수준 선택 가능 |
| **NoSQL** | AWS | DynamoDB Global Tables | 지원 | 최종 일관성 (리전 간) |
| **RDB** | OCI | Autonomous Data Guard | — (크로스 리전 복제) | 강한 일관성 (프라이머리) |

### 글로벌 DB가 어려운 이유

리전 간 데이터 동기화는 물리 법칙(빛의 속도)에 제약됩니다. 대륙 간 RTT는 수백 ms에 달하므로, 모든 쓰기를 동기적으로 복제하면 성능이 크게 저하됩니다.

| 트레이드오프 | 설명 |
| --- | --- |
| **강한 일관성 + 멀티 리전 쓰기** | Spanner만 지원. 비용 매우 높음. TrueTime(원자 시계) 기반 |
| **최종 일관성 + 멀티 리전 쓰기** | DynamoDB Global Tables, Cosmos DB. 충돌 해결 전략 필요 |
| **강한 일관성 + 단일 리전 쓰기** | Aurora Global DB. 읽기만 분산. 가장 단순하지만 쓰기 지연 존재 |

:::caution
글로벌 DB는 비용이 높고 설계가 복잡합니다. 대부분의 워크로드는 다음 순서로 검토하세요:
1. 단일 리전으로 충분한가? (CDN + API 캐싱으로 읽기 지연 해결)
2. 읽기만 분산하면 되는가? (크로스 리전 읽기 복제본)
3. 쓰기도 분산해야 하는가? (글로벌 DB — 충돌 해결/일관성 트레이드오프 수용 필요)
:::

## 핵심 차이점

**AWS Aurora** — MySQL/PostgreSQL 호환. 스토리지가 3개 AZ에 6개 복사본으로 자동 복제됩니다. Aurora Serverless로 유휴 시 비용 0 가능.

**Azure SQL Database** — SQL Server 기반. 기존 SQL Server 워크로드를 가장 쉽게 마이그레이션할 수 있습니다. Hyperscale 티어에서 100TB까지 확장.

**Google Cloud AlloyDB** — PostgreSQL 호환. 벡터 검색이 내장되어 AI 워크로드와의 통합이 강점입니다. AlloyDB Omni를 통해 온프레미스, 멀티클라우드(GDC 포함) 환경에도 배포할 수 있으며, PostgreSQL 18 호환과 투명 데이터 암호화(TDE)를 지원합니다.

**OCI Autonomous Database** — Oracle DB 기반. 자동 튜닝, 자동 패치, 자동 스케일링. MySQL HeatWave로 OLTP+OLAP 통합 처리도 지원합니다.

## Database@Cloud

Oracle은 자사 데이터베이스를 경쟁사 데이터센터 안에 직접 배치하는 전략을 추진하고 있습니다.

| 서비스 | 배치 위치 | 특징 |
| --- | --- | --- |
| [Oracle Database@Azure](https://www.oracle.com/cloud/azure/) | Azure DC | Azure Portal에서 네이티브 프로비저닝 |
| [Oracle Database@AWS](https://www.oracle.com/cloud/aws/) | AWS DC | AWS 콘솔에서 직접 프로비저닝. Oracle AI Database@AWS로 리브랜딩. 22개 리전 확대(2026.08). 싱가포르·밀라노 추가 |
| [Oracle Database@Google Cloud](https://www.oracle.com/cloud/google/) | Google Cloud DC | Google Cloud 콘솔에서 직접 사용 |

앱과 DB가 같은 데이터센터에 있어 레이턴시 최소화, 이그레스 비용 없음, 데이터 주권 충족이 가능합니다.

## 언제 무엇을 선택할 것인가

| 상황 | 추천 |
| --- | --- |
| MySQL/PostgreSQL + 고가용성 + 자동 스토리지 확장 | AWS Aurora |
| 기존 SQL Server 워크로드 마이그레이션 | Azure SQL Database |
| PostgreSQL + AI/벡터 검색 통합 | Google Cloud AlloyDB |
| Oracle DB + 자동 튜닝/패치 | OCI Autonomous Database |
| 유휴 시 비용 0 (개발/테스트) | Aurora Serverless, Azure SQL Serverless |
| OLTP + OLAP 통합 MySQL | OCI MySQL HeatWave |

## 자주 하는 실수

- **싱글 AZ 배포** — 프로덕션 DB를 단일 AZ에 배포하면 해당 AZ 장애 시 서비스가 완전히 중단됩니다. Multi-AZ를 반드시 활성화하세요.
- **백업 미테스트** — 자동 백업을 설정해 놓고 실제 복구 테스트를 하지 않으면, 장애 시 복구가 실패하거나 예상보다 오래 걸릴 수 있습니다.
- **인덱스 없이 운영** — 적절한 인덱스 없이 운영하면 데이터 증가에 따라 쿼리 성능이 급격히 저하되고, 전체 테이블 스캔으로 DB 부하가 증가합니다.

## 체크리스트

- [ ] Multi-AZ(또는 고가용성 구성)를 활성화했는가
- [ ] 자동 백업을 설정하고 복구 테스트를 수행했는가
- [ ] 슬로우 쿼리 로그를 활성화하고 모니터링하고 있는가
- [ ] 연결 풀링(RDS Proxy, PgBouncer 등)을 설정했는가

## 참고하기

### AWS

- [Amazon RDS 문서](https://docs.aws.amazon.com/ko_kr/rds/)
- [Amazon Aurora 문서](https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/AuroraUserGuide/)

### Azure

- [Azure SQL Database 문서](https://learn.microsoft.com/ko-kr/azure/azure-sql/)
- [Azure Database for PostgreSQL 문서](https://learn.microsoft.com/ko-kr/azure/postgresql/)

### Google Cloud

- [Cloud SQL 문서](https://cloud.google.com/sql/docs)
- [AlloyDB 문서](https://cloud.google.com/alloydb/docs)

### OCI

- [OCI Autonomous Database 문서](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html)
- [OCI MySQL HeatWave 문서](https://docs.oracle.com/en-us/iaas/mysql-database/index.html)
