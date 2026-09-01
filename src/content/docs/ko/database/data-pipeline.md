---
title: "데이터 파이프라인과 ETL"
description: "데이터 파이프라인(ETL/ELT)의 개념, 벤더별 서비스, 배치 vs 스트리밍 선택을 비교합니다."
---

> 문서 기준: 2026년 5월

## 개요

원본 데이터를 [분석 플랫폼](../../database/analytics/)이나 ML 파이프라인에서 사용하려면 **추출(Extract) → 변환(Transform) → 적재(Load)** 과정이 필요합니다.

| 구분 | ETL | ELT |
| --- | --- | --- |
| **변환 위치** | 파이프라인 중간 (별도 엔진) | 적재 후 대상 시스템에서 변환 |
| **적합한 경우** | 데이터 정제가 복잡, 대상 시스템 부하 제한 | 대상이 BigQuery/Redshift처럼 연산 능력 충분 |
| **트렌드** | 전통적 방식 | 클라우드 DW의 연산력 활용으로 주류화 |

## 벤더별 서비스 비교

| 벤더 | 배치 ETL/ELT | 스트리밍 | 오케스트레이션 |
| --- | --- | --- | --- |
| AWS | [Glue](https://docs.aws.amazon.com/glue/) (서버리스 Spark) | [Kinesis Data Streams](https://docs.aws.amazon.com/kinesis/) | [Step Functions](https://docs.aws.amazon.com/step-functions/), [MWAA](https://docs.aws.amazon.com/mwaa/) (Airflow) |
| Azure | [Data Factory](https://learn.microsoft.com/azure/data-factory/) | [Stream Analytics](https://learn.microsoft.com/azure/stream-analytics/) | Data Factory 파이프라인, [Synapse Pipelines](https://learn.microsoft.com/azure/synapse-analytics/) |
| Google Cloud | [Dataflow](https://cloud.google.com/dataflow/docs) (Apache Beam) | Dataflow (통합) | [Cloud Composer](https://cloud.google.com/composer/docs) (Airflow), [Workflows](https://cloud.google.com/workflows/docs) |
| OCI | [OCI Data Integration](https://docs.oracle.com/en-us/iaas/data-integration/home.htm) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) + [Data Flow](https://docs.oracle.com/en-us/iaas/data-flow/using/home.htm) (Spark) | OCI Data Integration 파이프라인 |

## 배치 vs 스트리밍

| 항목 | 배치 | 스트리밍 |
| --- | --- | --- |
| **지연** | 분~시간 | 초~분 |
| **비용** | 실행 시간만 과금 (서버리스) | 상시 실행 (또는 이벤트 기반) |
| **복잡도** | 낮음 | 높음 (순서, 중복, 지연 처리) |
| **적합한 경우** | 일/주 단위 리포트, 대량 마이그레이션 | 실시간 대시보드, 이상 탐지, 추천 |

## Zero-ETL

운영 DB에서 분석 플랫폼으로 데이터를 **파이프라인 없이 자동으로** 복제/동기화하는 접근입니다. ETL 파이프라인 구축·유지보수 부담을 제거하는 것이 목표입니다.

### ETL → ELT → Zero-ETL 흐름

| 세대 | 방식 | 부담 |
| --- | --- | --- |
| ETL | 별도 엔진에서 변환 후 적재 | 파이프라인 구축·운영·모니터링 |
| ELT | 적재 후 DW에서 변환 | 파이프라인은 단순화, 변환 로직은 여전히 필요 |
| Zero-ETL | 소스 → 대상 자동 복제, 파이프라인 불필요 | 설정만 하면 됨 (이론상) |

### 벤더별 Zero-ETL 현황

| 벤더 | 서비스 | 소스 → 대상 |
| --- | --- | --- |
| AWS | Aurora Zero-ETL to Redshift | Aurora MySQL/PostgreSQL → Redshift |
| AWS | DynamoDB Zero-ETL to Redshift | DynamoDB → Redshift |
| Azure | Fabric Mirroring | Azure SQL/Cosmos DB → Microsoft Fabric |
| Google Cloud | BigQuery 연속 쿼리 + Change Streams | Spanner/Bigtable → BigQuery |
| OCI | GoldenGate + Autonomous DB | 운영 DB → Autonomous DW |

### 아직 남아있는 한계

| 한계 | 설명 |
| --- | --- |
| **벤더 종속** | 같은 벤더 내 소스→대상만 지원. 크로스 벤더 Zero-ETL은 없음 |
| **변환 로직 부재** | 데이터를 "그대로" 복제할 뿐, 비즈니스 변환(정제, 집계, 조인)은 별도 필요 |
| **스키마 변경 대응** | 소스 스키마가 바뀌면 동기화가 깨지거나 수동 개입 필요 |
| **지원 소스 제한** | 모든 DB가 지원되는 게 아님. 특정 엔진/버전만 가능 |

:::note
Zero-ETL은 **단순 복제**에 적합하고, 복잡한 변환·다중 소스 조인·크로스 벤더 통합은 여전히 ETL/ELT 파이프라인이 필요합니다. 현실적으로는 Zero-ETL + 경량 ELT 조합이 될 것입니다.
:::

## 언제 무엇을 선택할 것인가

| 요구사항 | 권장 |
| --- | --- |
| 단순 복제 (같은 벤더, 변환 불필요) | Zero-ETL |
| 서버리스 배치 ETL (Spark) | Glue, Dataflow, Data Flow |
| 코드 없는 ETL (GUI 기반) | Data Factory, OCI Data Integration |
| 배치+스트리밍 통합 (Apache Beam) | Google Cloud Dataflow |
| 워크플로 오케스트레이션 (DAG) | Airflow (MWAA, Cloud Composer), Step Functions |
| 실시간 스트리밍 분석 | Kinesis Analytics, Stream Analytics, Dataflow |

## 자주 하는 실수

- **배치로 충분한 워크로드에 스트리밍을 도입** — 실시간 처리가 필요 없는데 스트리밍을 선택하면 복잡도와 비용만 증가합니다. 일/주 단위 리포트는 배치로 충분합니다.
- **Zero-ETL을 만능으로 기대** — Zero-ETL은 단순 복제만 지원합니다. 비즈니스 변환(정제, 집계, 조인)이 필요하면 여전히 ETL/ELT 파이프라인이 필요합니다.
- **파이프라인 모니터링 없이 운영** — 데이터 지연, 스키마 변경, 실패한 작업을 감지하지 못하면 분석 결과가 오래된 데이터에 기반하게 됩니다.

## 체크리스트

- [ ] 워크로드의 지연 허용 범위(분/시간/일)를 정의하고 배치 vs 스트리밍을 선택했는가
- [ ] 파이프라인 실패 시 알림과 재시도 정책이 설정되어 있는가
- [ ] 소스 스키마 변경 시 파이프라인이 깨지지 않도록 스키마 진화(Schema Evolution) 전략이 있는가

## 참고하기

### AWS

- [AWS Glue 문서](https://docs.aws.amazon.com/glue/)
- [Amazon Kinesis 문서](https://docs.aws.amazon.com/kinesis/)

### Azure

- [Azure Data Factory 문서](https://learn.microsoft.com/azure/data-factory/)
- [Azure Stream Analytics 문서](https://learn.microsoft.com/azure/stream-analytics/)

### Google Cloud

- [Dataflow 문서](https://cloud.google.com/dataflow/docs)
- [Cloud Composer 문서](https://cloud.google.com/composer/docs)

### OCI

- [OCI Data Integration 문서](https://docs.oracle.com/en-us/iaas/data-integration/home.htm)
- [OCI Data Flow 문서](https://docs.oracle.com/en-us/iaas/data-flow/using/home.htm)
