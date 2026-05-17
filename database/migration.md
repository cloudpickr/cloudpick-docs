---
description: DB 마이그레이션 전략(Rehost/Replatform/Refactor)과 다운타임 최소화 기법을 벤더별로 비교합니다.
---

# 데이터베이스 마이그레이션

> 문서 기준: 2026년 5월

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
| Google Cloud | Database Migration Service | MySQL, PostgreSQL, SQL Server → Cloud SQL/AlloyDB |
| Google Cloud | Datastream | CDC 기반 실시간 복제. BigQuery로 스트리밍 가능 |
| OCI | OCI Database Migration | Oracle/MySQL → OCI DB. 온라인 마이그레이션(Zero Downtime) 지원 |

## 핵심 차이점

**AWS DMS** — 가장 많은 소스/타깃 엔진 조합을 지원합니다. Oracle, SQL Server, MongoDB, S3 등 다양한 소스에서 AWS DB로 마이그레이션할 수 있습니다. SCT와 함께 사용하면 이종 마이그레이션의 스키마 변환을 자동화합니다.

**Azure** — Azure SQL로의 마이그레이션에 특화되어 있으며, SQL Server 워크로드 이전이 가장 매끄럽습니다. Azure Migrate로 마이그레이션 전 평가(호환성, 비용 추정)를 수행할 수 있습니다.

**Google Cloud Datastream** — CDC 기반 실시간 복제를 제공하며, BigQuery로 직접 스트리밍하여 분석 파이프라인을 구성할 수 있습니다.

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

{% hint style="warning" %}
이종 마이그레이션(Oracle → PostgreSQL 등)은 단순 데이터 이동이 아닙니다. **스키마 변환, 프로시저/트리거 재작성, 애플리케이션 쿼리 수정**까지 포함됩니다. 충분한 평가(Assessment) 단계 없이 시작하면 예상보다 몇 배 긴 기간이 소요될 수 있습니다.
{% endhint %}

## DB 내부 로직(프로시저/트리거)을 그대로 가져갈 때의 위험

온프레미스 DB에서는 비즈니스 로직의 상당 부분을 **저장 프로시저(Stored Procedure)**, **트리거(Trigger)**, **사용자 정의 함수(UDF)** 로 구현하는 경우가 많습니다. 마이그레이션 시 이를 그대로 옮기려는 요구가 자주 발생하지만, 클라우드 환경에서는 다음과 같은 문제가 생깁니다.

### 확장성 한계

- **DB 인스턴스가 병목** — 프로시저가 DB 내부에서 실행되므로, 비즈니스 로직 부하가 DB CPU/메모리를 소모합니다. 읽기 전용 복제본으로 분산할 수 없고, DB 인스턴스 수직 확장으로만 대응해야 합니다.
- **수평 확장 불가** — 애플리케이션 계층은 오토스케일링으로 무한히 확장할 수 있지만, DB는 그렇지 않습니다. 로직이 DB에 있으면 전체 시스템 확장성이 DB 성능에 묶입니다.

### 벤더 종속성 증가

- **특정 DB 엔진에 고정** — Oracle PL/SQL, SQL Server T-SQL, PostgreSQL PL/pgSQL은 서로 호환되지 않습니다. 관리형 서비스로 전환하거나 다른 클라우드로 이동할 때 전체 로직을 재작성해야 합니다.
- **이종 마이그레이션이 어려워짐** — Oracle → PostgreSQL로 전환 시, 데이터는 DMS로 옮기지만 프로시저는 수동 변환이 필요하고, 변환 도구(SCT 등)가 모든 구문을 지원하지 않습니다.

### 운영 및 관찰가능성 문제

- **버전 관리 어려움** — 애플리케이션 코드는 Git으로 관리되지만, 프로시저는 DB 안에 있어 버전 관리가 취약합니다.
- **테스트 자동화 어려움** — 단위 테스트, CI/CD 파이프라인에 프로시저를 통합하기 어렵습니다.
- **장애 원인 파악 지연** — APM, 분산 트레이싱 도구가 애플리케이션 코드는 추적하지만, 프로시저 내부는 블랙박스입니다.
- **디버깅 도구 제한** — IDE 지원이 애플리케이션 언어(Java, Python 등) 대비 빈약합니다.

### 보안 및 규정 준수 리스크

- **접근 권한 관리 복잡** — 프로시저가 내부에서 여러 테이블을 조작하면, 최소 권한 원칙 적용이 어려워집니다.
- **감사 로그의 해상도 낮음** — 프로시저 하나의 실행만 기록되고, 내부 동작은 로그로 남지 않는 경우가 많습니다.

### 권장 접근 방향

| 상황 | 권장 방향 |
| --- | --- |
| **일단 클라우드로 빠르게 이동해야 할 때** | Rehost로 프로시저 유지 → 이후 점진적으로 애플리케이션 계층으로 이동 |
| **관리형 DB로 전환할 때** | 관리형 DB가 지원하는 프로시저 기능 범위 확인 (예: 일부 System Procedure는 관리형에서 제한됨) |
| **새로 설계하는 경우** | 비즈니스 로직을 애플리케이션 계층에 두고, DB는 데이터 저장/조회에 집중 |
| **분산 트랜잭션이 필요한 경우** | 프로시저 대신 Saga 패턴, 이벤트 기반 아키텍처 고려 |

{% hint style="info" %}
**핵심 원칙:** 프로시저/트리거는 레거시 호환성을 위해서는 유지할 수 있지만, **신규 로직을 DB 내부에 추가하지 말고** 애플리케이션 계층에 두세요. 시간이 지나면 점진적으로 애플리케이션으로 이전해야 클라우드의 확장성과 유연성을 최대한 활용할 수 있습니다.
{% endhint %}

## 마이그레이션 프로세스

DB 마이그레이션은 일회성 데이터 이동이 아니라 여러 단계를 거치는 프로젝트입니다.

| 단계 | 주요 활동 |
| --- | --- |
| **1. Discovery** | 현재 DB 인벤토리 파악 (엔진, 버전, 크기, 성능, 의존성) |
| **2. Assessment** | 호환성 평가, 스키마 변환 필요성, 예상 비용 산정, 위험 요소 식별 |
| **3. Planning** | 마이그레이션 전략(Rehost/Replatform/Refactor) 선택, 다운타임 예산 확정, 롤백 계획 수립 |
| **4. Migration** | 스키마 이관 → 초기 데이터 로드 → CDC 기반 지속 복제 → 검증 |
| **5. Validation** | 데이터 무결성 검증, 애플리케이션 테스트, 성능 비교 |
| **6. Cutover** | 애플리케이션을 새 DB로 전환. 읽기 전용 모드 → 복제 완료 대기 → 전환 |

### 다운타임 최소화 전략

대규모 DB 마이그레이션에서 다운타임을 줄이는 핵심 기법입니다.

| 기법 | 설명 | 사용 시점 |
| --- | --- | --- |
| **CDC (Change Data Capture)** | 소스 DB의 트랜잭션 로그를 읽어 타깃에 지속 복제 | 온라인 마이그레이션의 기본. 초기 로드 후 실시간 동기화 |
| **Blue/Green 배포** | 기존 DB(Blue)와 신규 DB(Green)를 동시에 운영하다 트래픽 전환 | 전환 시 롤백이 쉬워야 할 때 |
| **읽기 전용 잠금** | Cutover 직전 소스 DB를 읽기 전용으로 전환, 복제 완료 후 전환 | 몇 분~수십 분의 다운타임 허용 가능할 때 |
| **듀얼 쓰기** | 애플리케이션이 두 DB에 동시에 쓰기 | 완벽한 무중단이 필요하지만 복잡도가 높음 |

## 참고하기

### AWS

- [AWS Database Migration Service (DMS) 문서](https://docs.aws.amazon.com/ko_kr/dms/)
- [AWS Schema Conversion Tool (SCT) 문서](https://docs.aws.amazon.com/ko_kr/SchemaConversionTool/)

### Azure

- [Azure Database Migration Service 문서](https://learn.microsoft.com/ko-kr/azure/dms/)
- [Azure Migrate 문서](https://learn.microsoft.com/ko-kr/azure/migrate/)

### Google Cloud

- [Database Migration Service 문서](https://cloud.google.com/database-migration/docs)
- [Datastream 문서](https://cloud.google.com/datastream/docs)

### OCI

- [OCI Database Migration 문서](https://docs.oracle.com/en-us/iaas/database-migration/index.html)
