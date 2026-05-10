---
description: 관리형 RDB와 클라우드 네이티브 DB의 차이, HA 구성, PITR을 벤더별로 비교합니다.
---

# 관리형 RDB

> 문서 기준: 2026년 5월

## 개요

온프레미스에서 데이터베이스를 운영하려면 서버 설치, OS 패치, DB 엔진 설치, 백업 설정, 복제 구성, 장애 조치를 모두 직접 해야 합니다. **관리형 RDB** (Relational Database)는 이 운영 부담을 벤더가 대신 처리하고, 사용자는 데이터와 쿼리에만 집중할 수 있게 합니다.

{% hint style="info" %}
**RDS를 아시는 분을 위해:** Azure는 Azure SQL/Flexible Server, GCP는 Cloud SQL, OCI는 Autonomous Database입니다.
{% endhint %}

자동 백업, 패치 적용, 멀티 AZ 복제, 읽기 전용 복제본(Read Replica) 등을 설정 몇 번으로 구성할 수 있습니다.

## 관리형 RDB vs VM에 직접 설치

클라우드에서도 EC2/VM에 직접 DB를 설치하여 운영하는 경우가 있습니다. 관리형 서비스의 편의성을 포기하면서까지 VM에 설치하는 이유는 대부분 **관리형이 지원하지 않는 요건** 때문입니다.

### VM에 DB를 직접 설치하는 이유

| 이유 | 설명 |
| --- | --- |
| **관리형이 지원하지 않는 엔진/버전** | 관리형이 제공하지 않는 DB 엔진(예: SAP HANA, Cassandra, 특수 NoSQL), 또는 관리형의 최신 기능 지원 이전의 특정 버전/패치 |
| **관리형이 제한하는 기능** | 특정 확장 프로그램, 커스텀 스토리지 엔진, 커널 파라미터 조정, OS 레벨 접근 필요 |
| **라이선스 비용** | 관리형 Oracle/SQL Server 라이선스 비용이 BYOL(Bring Your Own License)보다 비쌀 때 |
| **완전한 제어** | DBA가 OS, 파일 시스템, 백업 도구까지 직접 선택하고 싶을 때 |
| **특수 HA/DR 요구사항** | 관리형이 지원하지 않는 복제 방식(예: Oracle Data Guard Active-Active, 3rd party 복제 도구) |
| **멀티클라우드 이식성** | 같은 DB를 여러 클라우드에 일관되게 배포하고 싶을 때 (관리형은 벤더 종속적) |

### 트레이드오프

| 항목 | 관리형 RDB | VM 직접 설치 |
| --- | --- | --- |
| **OS 패치** | 자동 | 사용자 책임 |
| **DB 엔진 패치** | 자동 또는 예약 적용 | 사용자 책임 |
| **백업/복구** | 자동 (PITR 포함) | 사용자가 구성 |
| **HA 구성** | 설정 몇 번으로 완료 | DBA가 수동 구성 (수 일~수 주) |
| **모니터링** | 기본 제공 | CloudWatch/Azure Monitor 등 별도 구성 |
| **스케일링** | 클릭으로 변경 | 수동 리사이즈 또는 복제 전환 |
| **24x7 운영 부담** | 벤더 SLA | 자체 DBA 필요 |
| **비용** | 관리 프리미엄 포함 | 인프라 비용만 (단, 인력 비용 별도) |

{% hint style="warning" %}
**판단 기준:** 특별한 이유가 없다면 관리형을 우선 선택하는 것이 일반적입니다. VM 설치는 "관리형으로는 안 되는 요건이 명확할 때"의 선택이며, 선택 시 DBA 인력과 운영 도구를 함께 계획해야 합니다.
{% endhint %}

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
| **용량 관리** | 디스크 크기 사전 지정 | 자동 확장 (최대 128\~256 TiB) |

Aurora는 데이터를 3개 AZ에 걸쳐 6개 복사본으로 자동 복제하며, 컴퓨팅(DB 인스턴스)과 스토리지가 분리되어 있어 인스턴스를 추가/제거해도 데이터 복사가 필요 없습니다. AlloyDB도 유사하게 컴퓨팅과 스토리지를 분리한 아키텍처를 사용합니다.

## 핵심 차이점

{% tabs %}
{% tab title="AWS Aurora" %}
MySQL/PostgreSQL과 호환되면서 최대 5배(MySQL) / 3배(PostgreSQL) 성능을 제공한다고 AWS가 주장합니다. 스토리지가 3개 AZ에 6개 복사본으로 자동 복제됩니다.
{% endtab %}

{% tab title="Azure SQL Database" %}
SQL Server 기반으로, 기존 SQL Server 워크로드를 가장 쉽게 마이그레이션할 수 있습니다. Hyperscale 티어에서 100TB까지 확장 가능합니다.
{% endtab %}

{% tab title="GCP AlloyDB" %}
PostgreSQL 호환이면서 Google 자체 설계로 트랜잭션 성능을 높였습니다. 벡터 검색이 내장되어 AI 워크로드와의 통합이 강점입니다.
{% endtab %}

{% tab title="OCI Autonomous Database" %}
Oracle DB 기반으로 자동 튜닝, 자동 패치, 자동 스케일링을 제공합니다. Oracle DB 워크로드에서 최고 성능을 발휘하며, MySQL HeatWave로 OLTP+OLAP 통합 처리도 지원합니다.
{% endtab %}
{% endtabs %}

## 언제 무엇을 선택할 것인가

| 이럴 때 | 이것을 선택 |
| --- | --- |
| MySQL/PostgreSQL 호환 + 고가용성 + 자동 스토리지 확장이 필요할 때 | AWS Aurora |
| 기존 SQL Server 워크로드를 최소 변경으로 마이그레이션할 때 | Azure SQL Database |
| PostgreSQL 호환 + AI/벡터 검색 통합이 필요할 때 | GCP AlloyDB |
| Oracle DB 워크로드 + 자동 튜닝/패치가 필요할 때 | OCI Autonomous Database |
| 유휴 시 비용 0이 필요한 개발/테스트 환경일 때 | AWS Aurora Serverless 또는 Azure SQL Serverless |
| OLTP + OLAP을 하나의 MySQL DB에서 처리하고 싶을 때 | OCI MySQL HeatWave |

## 고가용성 (HA) 구성

관리형 RDB는 다양한 HA 옵션을 제공합니다.

| 패턴 | 설명 | RPO | RTO |
| --- | --- | --- | --- |
| **Single-AZ** | 단일 AZ에 DB 인스턴스 1개 | 수동 복구 (백업 시점) | 수 시간 |
| **Multi-AZ 동기 복제** | 같은 리전 내 여러 AZ에 복제. 자동 장애 조치 | 0 (데이터 손실 없음) | 수십 초 \~ 수 분 |
| **읽기 전용 복제본** | 읽기 트래픽 분산. 비동기 복제 | 수 초 (복제 지연) | 수동 승격 |
| **크로스 리전 복제** | 다른 리전에 비동기 복제. DR용 | 수 초 \~ 수 분 | 수 분 (수동 승격) |
| **글로벌 DB** | 여러 리전에 저지연 동기 복제 | \~1초 | 초 단위 |

### HA 기능 매핑

| 기능 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **Multi-AZ 동기** | RDS Multi-AZ, Aurora 스토리지 복제 | Zone-redundant HA | Cloud SQL HA | ADB 자동 HA |
| **읽기 복제본** | RDS Read Replica, Aurora Read Replica | Read Replica | Cloud SQL Read Replica | ADB Read-only Replica |
| **크로스 리전 복제** | Aurora Global Database, RDS Cross-Region RR | Geo-replication, Failover Groups | Cloud SQL Cross-Region Replica | ADB Autonomous Data Guard |

## 자동 백업 및 PITR

대부분의 관리형 RDB는 **Point-in-Time Recovery** (PITR)를 제공합니다. 트랜잭션 로그를 지속적으로 저장하여 특정 시점으로 복구할 수 있습니다.

| 벤더 | 백업 보존 기간 | PITR 지원 |
| --- | --- | --- |
| AWS RDS / Aurora | 최대 35일 | 초 단위 복구 |
| Azure SQL Database | 최대 35일 (기본 7일) | 초 단위 복구 |
| GCP Cloud SQL / AlloyDB | 최대 365일 | 초 단위 복구 |
| OCI Autonomous Database | 최대 60일 | 초 단위 복구 |

수동 스냅샷은 보존 기간이 무제한이며, 규정 준수 장기 보관에 사용합니다.

## 관련 문서

{% content-ref url="../storage/backup.md" %}
[백업과 복구](../storage/backup.md)
{% endcontent-ref %}

{% content-ref url="../governance/dr.md" %}
[재해복구 (DR)](../governance/dr.md)
{% endcontent-ref %}

{% content-ref url="migration.md" %}
[데이터베이스 마이그레이션](migration.md)
{% endcontent-ref %}

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
