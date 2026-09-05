---
title: "데이터베이스 운영"
description: "RDB 확장 패턴, NoSQL 키 설계, 캐시 운영, 슬로쿼리 관리, HA/백업을 다룹니다."
---

> 문서 기준: 2026년 8월

## 개요

클라우드 관리형 DB는 인프라 운영(패치, 백업, HA)을 자동화하지만, **데이터 설계와 쿼리 성능은 자동으로 좋아지지 않습니다.** 이 문서는 DB를 선택한 뒤 운영 단계에서 알아야 할 핵심 주제를 다룹니다.

:::note
DB 선택 가이드는 [관리형 RDB](../../database/managed-rdb/), [NoSQL](../../database/nosql/), [캐시](../../database/cache/)를 참고하세요. 이 문서는 "선택한 뒤 어떻게 운영하는가"에 집중합니다.
:::

## RDB 확장 패턴

RDB는 NoSQL과 달리 수평 확장(샤딩)이 어렵습니다. 대부분의 확장은 **읽기 분산**으로 이루어집니다.

| 단계 | 방법 | 효과 | 예시 |
| --- | --- | --- | --- |
| 1. **수직 확장** | 인스턴스 타입 업그레이드 (CPU/메모리 증가) | 가장 단순. 한계 있음 | db.r5.large → db.r5.4xlarge |
| 2. **읽기 복제본** | 읽기 트래픽을 복제본으로 분산 | 읽기 80%+ 워크로드에 효과적 | 상품 목록 조회를 복제본에서 처리 |
| 3. **캐시 레이어** | 자주 읽는 데이터를 캐시(Redis/Valkey)에 저장 | DB 부하 대폭 감소. 밀리초 응답 | 세션, 인기 상품, 설정값을 캐시 |
| 4. **CQRS** | 쓰기(Command)와 읽기(Query) DB를 분리 | 각각 독립적으로 최적화 가능 | 주문 쓰기는 RDB, 검색/대시보드는 별도 읽기 DB |
| 5. **샤딩** | 데이터를 여러 DB에 분산 저장 | 최후의 수단. 앱 복잡도 급증 | 사용자 ID 기준으로 DB 분할 |

:::note
대부분의 웹 서비스는 읽기가 80–90%입니다. 읽기 복제본 + 캐시 조합으로 RDB 부하의 대부분을 해결할 수 있습니다.
:::

## 쿼리 성능 관리

| 문제 | 증상 | 대응 |
| --- | --- | --- |
| **무분별한 JOIN** | 다수 테이블 JOIN 시 응답이 수 초 이상 걸림 | 읽기 복제본 분리, 비정규화, DW로 분석 쿼리 이관 |
| **인덱스 미설계** | 풀 테이블 스캔. 데이터 증가에 따라 점점 느려짐 | 실행 계획(EXPLAIN) 확인, 쿼리 패턴에 맞는 인덱스 추가 |
| **슬로쿼리 방치** | 특정 쿼리가 DB 전체 성능 저하 | 슬로쿼리 로그 활성화, 정기 리뷰, 쿼리 리팩터링 |
| **DB를 스토리지처럼 사용** | 로그/이벤트를 RDB에 무한 적재 | 시계열 데이터는 객체 스토리지/시계열 DB로 분리 |

:::caution
OLTP(트랜잭션)와 OLAP(분석)을 같은 DB에서 처리하면 서로 성능을 압박합니다. 분석 쿼리가 많아지면 [데이터 분석 플랫폼](../../database/analytics/)으로 분리하세요.
:::

### 인덱스 설계 기본

**카디널리티(Cardinality)**: 컬럼에 포함된 고유 값의 수입니다. 사용자 ID(수백만 개)는 카디널리티가 높고, 성별(2개)은 낮습니다. 카디널리티가 높은 컬럼에 인덱스를 걸어야 효과가 큽니다.

| 원칙 | 설명 |
| --- | --- |
| **WHERE 절 기준** | 자주 필터링하는 컬럼에 인덱스 |
| **카디널리티 확인** | 고유 값이 많은 컬럼이 인덱스 효과 큼. boolean 같은 저카디널리티는 효과 없음 |
| **복합 인덱스 순서** | 가장 선택적인(카디널리티 높은) 컬럼을 앞에 배치 |
| **커버링 인덱스** | SELECT 컬럼까지 인덱스에 포함하면 테이블 접근 없이 응답 가능 |
| **과도한 인덱스 주의** | 인덱스가 많으면 쓰기 성능 저하. 읽기/쓰기 비율 고려 |

:::note
인덱스 추가 전에 반드시 `EXPLAIN`(실행 계획)으로 현재 쿼리가 어떻게 동작하는지 확인하세요. 풀 테이블 스캔이 발생하는 쿼리부터 우선 개선합니다.
:::

## 고가용성 (HA)

| 방식 | 동작 | RPO | RTO | 비용 | 적합한 경우 |
| --- | --- | --- | --- | --- | --- |
| **멀티 AZ 동기 복제** | 같은 리전 내 여러 AZ에 동기 복제. 자동 페일오버 | 0 | 수십 초–수 분 | 중간 (대기 인스턴스 비용) | 프로덕션 기본 |
| **읽기 복제본** | 비동기 복제. 읽기 분산 + 수동 승격으로 DR 가능 | 수 초 (복제 지연) | 수 분 (수동 승격) | 낮음 | 읽기 부하 분산 + 간이 DR |
| **크로스 리전 복제** | 다른 리전에 비동기 복제. 리전 장애 대비 | 수 초–수 분 | 수 분 (수동 승격) | 높음 (리전 간 전송) | 리전 장애 DR |

### 벤더별 HA 서비스

| 기능 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **멀티 AZ 동기** | RDS Multi-AZ, Aurora 스토리지 복제 | Zone-redundant HA | Cloud SQL HA | ADB 자동 HA |
| **읽기 복제본** | Aurora Read Replica | Read Replica | Cloud SQL Read Replica | ADB Read-only Replica |
| **크로스 리전** | Aurora Global Database | Geo-replication | Cross-Region Replica | Autonomous Data Guard |

## 백업과 PITR

| 벤더 | 백업 보존 기간 | PITR |
| --- | --- | --- |
| AWS RDS / Aurora | 최대 35일 | 초 단위 복구 |
| Azure SQL Database | 최대 35일 | 초 단위 복구 |
| Google Cloud Cloud SQL / AlloyDB | 최대 365일 | 초 단위 복구 |
| OCI Autonomous Database | 최대 60일 | 초 단위 복구 |

:::note
백업 전략과 DR 구성 상세는 [백업과 복구](../../storage/backup/), [재해복구](../../governance/dr/)를 참고하세요.
:::

## 커넥션 풀 관리

DB 커넥션은 유한한 리소스입니다. 특히 서버리스/오토스케일링 환경에서 인스턴스가 급증하면 커넥션이 폭발합니다.

| 문제 | 대응 |
| --- | --- |
| 커넥션 고갈 | 커넥션 풀러(RDS Proxy, Cloud SQL Auth Proxy, PgBouncer) 사용 |
| 서버리스 함수 동시성 폭발 | Reserved Concurrency로 제한 + 커넥션 풀러 필수 |
| 유휴 커넥션 점유 | idle timeout 설정, 커넥션 재사용 |

## NoSQL 키 설계 안티패턴

NoSQL은 RDB와 달리 **쿼리 패턴을 먼저 정하고 키를 설계**해야 합니다. 운영 중 흔히 발생하는 증상(핫 파티션, 스로틀링)은 설계 단계의 키 설계 실수에서 비롯됩니다.

:::note
키 설계 패턴과 원칙은 [NoSQL 데이터베이스 — 키 설계 패턴](../../database/nosql/)을 참고하세요.
:::

## 캐시 운영

캐시는 DB 부하를 줄이는 핵심 도구이지만, 운영 시 고유한 주의점이 있습니다.

:::note
캐시 패턴 정의(Cache-Aside, Write-Through, Write-Behind 등)와 벤더별 서비스 비교는 [캐시](../../database/cache/)를 참고하세요.
:::

### 캐시 운영 주의사항

- **캐시 스탬피드** — TTL 만료 시 동시에 수백 요청이 DB로 몰림. 랜덤 TTL 지터 또는 락 기반 갱신으로 방지
- **캐시 웜업** — 배포/재시작 직후 캐시가 비어 DB 부하 급증. 사전 워밍 스크립트 필요
- **메모리 관리** — 캐시 메모리 초과 시 eviction 정책(LRU, LFU) 확인. 중요 데이터가 밀려나지 않도록
- **캐시를 영구 저장소처럼 사용하지 않기** — 캐시는 언제든 사라질 수 있는 전제로 설계. 원본은 반드시 DB에
- **모든 키에 TTL 설정** — TTL 없이 캐시하면 데이터가 영원히 남아 DB와 불일치 발생

## 자주 하는 실수

- **인덱스를 EXPLAIN 없이 추가** — 실행 계획을 확인하지 않고 인덱스를 추가하면 쓰기 성능만 저하되고 읽기 개선 효과가 없을 수 있습니다.
- **서버리스 환경에서 커넥션 풀러 없이 운영** — Lambda/Functions의 동시성이 급증하면 DB 커넥션이 고갈됩니다. RDS Proxy 등 커넥션 풀러를 반드시 사용하세요.
- **백업은 설정했지만 복구 테스트를 하지 않음** — 백업이 있어도 복구 절차를 검증하지 않으면 실제 장애 시 복구에 실패할 수 있습니다.

## 체크리스트

- [ ] 슬로쿼리 로그를 활성화하고 정기적으로 리뷰하는 프로세스가 있는가
- [ ] 멀티 AZ 또는 읽기 복제본으로 고가용성이 구성되어 있는가
- [ ] PITR(Point-in-Time Recovery) 복구를 실제로 테스트해본 적이 있는가

## 관련 문서

- [관리형 RDB](../../database/managed-rdb/) — DB 선택 가이드
- [NoSQL](../../database/nosql/) — NoSQL 선택 가이드
- [캐시와 인메모리](../../database/cache/) — 캐시 선택 가이드

## 참고하기

### AWS

- [Amazon RDS 사용 설명서](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Amazon Aurora 사용 설명서](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)
- [Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
- [RDS 읽기 복제본으로 작업하기](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)

### Azure

- [Azure Database for PostgreSQL 문서](https://learn.microsoft.com/azure/postgresql/)
- [Azure SQL Database 고가용성](https://learn.microsoft.com/azure/azure-sql/database/high-availability-sla)
- [Azure SQL Database 읽기 복제본(읽기 배율 확장)](https://learn.microsoft.com/azure/azure-sql/database/read-scale-out)

### Google Cloud

- [Cloud SQL 고가용성 개요](https://cloud.google.com/sql/docs/postgres/high-availability)
- [Cloud SQL 읽기 복제본](https://cloud.google.com/sql/docs/postgres/replication)
- [Cloud SQL Auth Proxy](https://cloud.google.com/sql/docs/postgres/sql-proxy)

### OCI

- [OCI Autonomous Database 문서](https://docs.oracle.com/en-us/iaas/autonomous-database/index.html)
- [Autonomous Data Guard](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-data-guard.html)

### 표준·도구

- [PostgreSQL EXPLAIN 문서](https://www.postgresql.org/docs/current/sql-explain.html)
- [PgBouncer — 경량 커넥션 풀러](https://www.pgbouncer.org/)
