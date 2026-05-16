---
description: 관리형 RDB와 클라우드 네이티브 DB의 차이, HA 구성, PITR을 벤더별로 비교합니다.
---

# 관리형 RDB

> 문서 기준: 2026년 5월

## 개요

온프레미스에서 데이터베이스를 운영하려면 서버 설치, OS 패치, DB 엔진 설치, 백업 설정, 복제 구성, 장애 조치를 모두 직접 해야 합니다. **관리형 RDB**는 이 운영 부담을 벤더가 대신 처리하고, 사용자는 데이터와 쿼리에만 집중할 수 있게 합니다.

{% hint style="info" %}
AWS RDS를 아시는 분을 위해: Azure는 Azure SQL/Flexible Server, GCP는 Cloud SQL, OCI는 Autonomous Database입니다.
{% endhint %}

### DBA 역할의 변화

| 영역 | 온프레미스 DBA | 관리형 RDB 환경 |
| --- | --- | --- |
| OS/패치 관리 | 직접 수행 | 벤더가 처리 |
| 백업/복구 | 스크립트 작성, 테스트 | 자동 백업 + PITR 내장 |
| HA/복제 구성 | 직접 설계·운영 | 멀티 AZ 체크박스 |
| 성능 튜닝 | 쿼리 + 인프라 모두 | **쿼리/스키마 최적화에 집중** |
| 용량 계획 | 디스크 구매·확장 | 온라인 확장 또는 자동 확장 |

{% hint style="warning" %}
특별한 이유가 없다면 관리형을 우선 선택하세요. VM에 직접 설치하는 경우는 "관리형이 지원하지 않는 엔진/버전", "OS 레벨 접근 필요", "BYOL 라이선스 비용 절감" 등 명확한 요건이 있을 때입니다.
{% endhint %}

## 제품 비교

### 범용 관리형 RDB

| 벤더 | 제품 | 지원 엔진 |
| --- | --- | --- |
| AWS | RDS | MySQL, PostgreSQL, MariaDB, Oracle, SQL Server |
| AWS | Aurora | MySQL/PostgreSQL 호환. 자체 설계 분산 스토리지 |
| Azure | Azure SQL Database | SQL Server 기반 |
| Azure | Azure Database for MySQL/PostgreSQL | 오픈소스 엔진 관리형 |
| GCP | Cloud SQL | MySQL, PostgreSQL, SQL Server |
| GCP | AlloyDB | PostgreSQL 호환. 자체 설계. 벡터 검색 내장 |
| OCI | Autonomous Database | Oracle DB 기반. 자동 튜닝/패치/스케일링 |
| OCI | MySQL HeatWave | MySQL 호환. OLTP + OLAP 통합 처리 |

### 클라우드 네이티브 DB란

일반 관리형(RDS, Cloud SQL)은 기존 DB 엔진을 그대로 사용하되 운영만 자동화한 것입니다. Aurora, AlloyDB 같은 **클라우드 네이티브 DB**는 스토리지 계층을 자체 설계하여 근본적으로 다른 아키텍처를 가집니다.

| 항목 | 일반 관리형 | 클라우드 네이티브 |
| --- | --- | --- |
| **스토리지** | 인스턴스에 연결된 블록 디스크 | 컴퓨팅과 분리된 분산 스토리지 |
| **복제** | 별도 인스턴스에 데이터 전체 복사 | 스토리지 자체가 멀티 AZ 복제 |
| **읽기 복제본 추가** | 데이터 복사 필요 (느림) | 동일 스토리지 공유 (빠름) |
| **장애 조치** | 대기 인스턴스로 전환 (수십 초) | 새 컴퓨팅 연결 (수 초) |
| **용량** | 디스크 크기 사전 지정 | 자동 확장 |

## 핵심 차이점

**AWS Aurora** — MySQL/PostgreSQL 호환. 스토리지가 3개 AZ에 6개 복사본으로 자동 복제됩니다. Aurora Serverless로 유휴 시 비용 0 가능.

**Azure SQL Database** — SQL Server 기반. 기존 SQL Server 워크로드를 가장 쉽게 마이그레이션할 수 있습니다. Hyperscale 티어에서 100TB까지 확장.

**GCP AlloyDB** — PostgreSQL 호환. 벡터 검색이 내장되어 AI 워크로드와의 통합이 강점입니다.

**OCI Autonomous Database** — Oracle DB 기반. 자동 튜닝, 자동 패치, 자동 스케일링. MySQL HeatWave로 OLTP+OLAP 통합 처리도 지원합니다.

## Database@Cloud

Oracle은 자사 데이터베이스를 경쟁사 데이터센터 안에 직접 배치하는 전략을 추진하고 있습니다.

| 서비스 | 배치 위치 | 특징 |
| --- | --- | --- |
| [Oracle Database@Azure](https://www.oracle.com/cloud/azure/) | Azure DC | Azure Portal에서 네이티브 프로비저닝 |
| [Oracle Database@AWS](https://www.oracle.com/cloud/aws/) | AWS DC | AWS 콘솔에서 직접 사용 |
| [Oracle Database@Google Cloud](https://www.oracle.com/cloud/google/) | GCP DC | GCP 콘솔에서 직접 사용 |

앱과 DB가 같은 데이터센터에 있어 레이턴시 최소화, 이그레스 비용 없음, 데이터 주권 충족이 가능합니다.

## 언제 무엇을 선택할 것인가

| 상황 | 추천 |
| --- | --- |
| MySQL/PostgreSQL + 고가용성 + 자동 스토리지 확장 | AWS Aurora |
| 기존 SQL Server 워크로드 마이그레이션 | Azure SQL Database |
| PostgreSQL + AI/벡터 검색 통합 | GCP AlloyDB |
| Oracle DB + 자동 튜닝/패치 | OCI Autonomous Database |
| 유휴 시 비용 0 (개발/테스트) | Aurora Serverless, Azure SQL Serverless |
| OLTP + OLAP 통합 MySQL | OCI MySQL HeatWave |

## 운영: HA와 백업

### 고가용성 옵션

| 기능 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **멀티 AZ 동기 복제** | RDS Multi-AZ, Aurora 스토리지 복제 | Zone-redundant HA | Cloud SQL HA | ADB 자동 HA |
| **읽기 복제본** | Aurora Read Replica | Read Replica | Cloud SQL Read Replica | ADB Read-only Replica |
| **크로스 리전 복제** | Aurora Global Database | Geo-replication | Cross-Region Replica | Autonomous Data Guard |

### 자동 백업 및 PITR

| 벤더 | 백업 보존 기간 | PITR |
| --- | --- | --- |
| AWS RDS / Aurora | 최대 35일 | 초 단위 복구 |
| Azure SQL Database | 최대 35일 | 초 단위 복구 |
| GCP Cloud SQL / AlloyDB | 최대 365일 | 초 단위 복구 |
| OCI Autonomous Database | 최대 60일 | 초 단위 복구 |

{% hint style="info" %}
백업 전략과 DR 구성 상세는 [백업과 복구](../storage/backup.md), [재해복구](../governance/dr.md)를 참고하세요.
{% endhint %}

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
