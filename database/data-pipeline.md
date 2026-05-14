---
description: 데이터 파이프라인(ETL/ELT)의 개념, 벤더별 서비스, 배치 vs 스트리밍 선택을 비교합니다.
---

# 데이터 파이프라인과 ETL

> 문서 기준: 2026년 5월

## 개요

원본 데이터를 [분석 플랫폼](analytics.md)이나 ML 파이프라인에서 사용하려면 **추출(Extract) → 변환(Transform) → 적재(Load)** 과정이 필요합니다.

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
| GCP | [Dataflow](https://cloud.google.com/dataflow/docs) (Apache Beam) | Dataflow (통합) | [Cloud Composer](https://cloud.google.com/composer/docs) (Airflow), [Workflows](https://cloud.google.com/workflows/docs) |
| OCI | [OCI Data Integration](https://docs.oracle.com/en-us/iaas/data-integration/home.htm) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) + [Data Flow](https://docs.oracle.com/en-us/iaas/data-flow/home.htm) (Spark) | OCI Data Integration 파이프라인 |

## 배치 vs 스트리밍

| 항목 | 배치 | 스트리밍 |
| --- | --- | --- |
| **지연** | 분~시간 | 초~분 |
| **비용** | 실행 시간만 과금 (서버리스) | 상시 실행 (또는 이벤트 기반) |
| **복잡도** | 낮음 | 높음 (순서, 중복, 지연 처리) |
| **적합한 경우** | 일/주 단위 리포트, 대량 마이그레이션 | 실시간 대시보드, 이상 탐지, 추천 |

## 언제 무엇을 선택할 것인가

| 요구사항 | 권장 |
| --- | --- |
| 서버리스 배치 ETL (Spark) | Glue, Dataflow, Data Flow |
| 코드 없는 ETL (GUI 기반) | Data Factory, OCI Data Integration |
| 배치+스트리밍 통합 (Apache Beam) | GCP Dataflow |
| 워크플로 오케스트레이션 (DAG) | Airflow (MWAA, Cloud Composer), Step Functions |
| 실시간 스트리밍 분석 | Kinesis Analytics, Stream Analytics, Dataflow |

## 참고하기

### AWS

- [AWS Glue 문서](https://docs.aws.amazon.com/glue/)
- [Amazon Kinesis 문서](https://docs.aws.amazon.com/kinesis/)

### Azure

- [Azure Data Factory 문서](https://learn.microsoft.com/azure/data-factory/)
- [Azure Stream Analytics 문서](https://learn.microsoft.com/azure/stream-analytics/)

### GCP

- [Dataflow 문서](https://cloud.google.com/dataflow/docs)
- [Cloud Composer 문서](https://cloud.google.com/composer/docs)

### OCI

- [OCI Data Integration 문서](https://docs.oracle.com/en-us/iaas/data-integration/home.htm)
- [OCI Data Flow 문서](https://docs.oracle.com/en-us/iaas/data-flow/home.htm)
