---
description: 데이터 웨어하우스, 데이터 레이크하우스, 분석 플랫폼을 벤더별로 비교합니다.
---

# 데이터 분석 플랫폼

> 문서 기준: 2026년 5월

## 개요

### OLTP vs OLAP — 왜 분리하는가

운영 데이터베이스([관리형 RDB](managed-rdb.md), [NoSQL](nosql.md))는 트랜잭션 처리(OLTP)에 최적화되어 있습니다. 대량 데이터를 집계·분석하려면 별도의 분석 플랫폼(OLAP)이 필요합니다.

**비유:** 운영 DB는 매장 계산대(빠른 개별 거래 처리)이고, 웨어하우스는 본사 경영분석팀(전 매장 데이터를 모아서 추이 분석)입니다. 계산대에서 경영분석을 하면 줄이 길어집니다.

운영 DB에서 대량 집계 쿼리를 돌리면:
- 트랜잭션 처리 성능 저하 (주문이 느려짐)
- 정규화된 스키마에서 분석 쿼리는 JOIN이 수십 개 → 느리고 복잡
- 그래서 운영 DB → ETL → 분석 전용 DB(웨어하우스)로 분리

| 구분 | OLTP (운영 DB) | OLAP (분석 플랫폼) |
| --- | --- | --- |
| **목적** | 개별 트랜잭션 처리 (주문, 결제) | 대량 데이터 집계·분석 (매출 추이, 사용자 행동) |
| **쿼리 패턴** | 소량 행 읽기/쓰기 (ms 단위) | 대량 행 스캔·집계 (초~분 단위) |
| **데이터 크기** | GB\~TB | TB\~PB |
| **스키마** | 정규화 (3NF) | 비정규화 (Star/Snowflake) 또는 스키마리스 |

## 벤더별 분석 플랫폼 비교

| 벤더 | 데이터 웨어하우스 | 특징 | 과금 모델 |
| --- | --- | --- | --- |
| AWS | [Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html) | 클러스터 기반 + Serverless 옵션. S3 데이터 직접 쿼리(Spectrum) | 노드 시간 또는 RPU(Serverless) |
| Azure | [Azure Synapse Analytics](https://learn.microsoft.com/azure/synapse-analytics/) | 통합 분석 플랫폼 (SQL + Spark + Data Explorer). 서버리스 SQL 풀 | DWU(전용) 또는 쿼리 데이터 처리량(서버리스) |
| GCP | [BigQuery](https://cloud.google.com/bigquery/docs) | 완전 서버리스. 인프라 관리 불필요. ML 내장(BQML) | 쿼리 스캔량 또는 슬롯(용량 예약) |
| OCI | [OCI Analytics Cloud](https://docs.oracle.com/en-us/iaas/analytics-cloud/index.html) + [Autonomous Data Warehouse](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html) | Oracle DB 기반 자동 튜닝. BI 시각화 통합 | OCPU 시간 |

### 핵심 차이점

**BigQuery (GCP)** — 완전 서버리스로 클러스터 관리가 불필요합니다. 쿼리가 스캔한 데이터량으로 과금되어, 사용하지 않으면 비용이 0입니다. BigQuery ML로 SQL만으로 ML 모델을 학습할 수 있습니다.

**Redshift (AWS)** — 전통적 클러스터 기반이지만 Serverless 옵션도 제공합니다. S3의 데이터를 Redshift Spectrum으로 직접 쿼리할 수 있어 데이터 레이크와 통합이 용이합니다.

**Synapse (Azure)** — SQL 분석, Apache Spark, Data Explorer를 하나의 플랫폼에서 제공합니다. 서버리스 SQL 풀로 데이터 레이크를 직접 쿼리할 수 있으며, Power BI와 네이티브 통합됩니다.

**Autonomous DW (OCI)** — Oracle Database 기반으로 자동 튜닝, 자동 스케일링을 제공합니다. 기존 Oracle 워크로드와 호환성이 높습니다.

## 데이터 레이크 vs 데이터 웨어하우스 vs 레이크하우스

| 아키텍처 | 특징 | 적합한 경우 |
| --- | --- | --- |
| **데이터 레이크** | 원시 데이터를 그대로 저장 (S3/ADLS/GCS). 스키마 온 리드 | 다양한 형식의 대량 데이터 저장, ML 학습 데이터 |
| **데이터 웨어하우스** | 정제된 데이터를 구조화하여 저장. 스키마 온 라이트 | 정형 데이터 분석, BI 리포트, 대시보드 |
| **레이크하우스** | 레이크 위에 웨어하우스 기능 추가 (Delta Lake, Iceberg) | 두 가지를 통합하고 싶을 때 |

벤더별 레이크하우스 접근:

| 벤더 | 레이크하우스 접근 |
| --- | --- |
| AWS | S3 + Glue Catalog + Redshift Spectrum + Athena (Apache Iceberg 지원) |
| Azure | ADLS Gen2 + Synapse + Delta Lake (Microsoft Fabric으로 통합) |
| GCP | GCS + BigQuery (BigLake로 외부 테이블 통합) |
| OCI | Object Storage + Autonomous DW + OCI Data Flow (Spark) |

## BI 시각화 도구

분석 결과를 사람이 보려면 BI(Business Intelligence) 도구가 필요합니다.

| 벤더 | BI 도구 | 특징 |
| --- | --- | --- |
| AWS | [Amazon QuickSight](https://aws.amazon.com/quick/quicksight/) | 서버리스 BI, Amazon Q 통합(자연어 질의, 생성형 BI) |
| Azure | [Power BI](https://powerbi.microsoft.com/) | 가장 넓은 사용자 기반, Excel 친화적, Copilot 통합 |
| GCP | [Looker / Looker Studio](https://cloud.google.com/looker) | LookML 기반 시맨틱 레이어, Looker Studio는 무료 |
| OCI | [OCI Analytics Cloud](https://docs.oracle.com/en-us/iaas/analytics-cloud/index.html) | Oracle 네이티브, 셀프서비스 시각화 |
| 3rd party | Tableau, Metabase, Apache Superset | 벤더 중립, 멀티클라우드 환경에서 유용 |

BI 도구가 중요한 이유:
- SQL 모르는 비즈니스 사용자도 데이터 활용 가능
- 대시보드로 실시간 모니터링
- 셀프서비스 분석 → 데이터팀 병목 해소

## 선택 기준

| 기준 | 권장 |
| --- | --- |
| 인프라 관리 최소화 + 쿼리 기반 과금 | BigQuery |
| 기존 AWS 데이터 레이크(S3)와 통합 | Redshift + Spectrum |
| SQL + Spark + BI 통합 플랫폼 | Synapse / Microsoft Fabric |
| Oracle DB 워크로드 + 자동 튜닝 | OCI Autonomous DW |
| 비용 예측 가능성 (고정 용량) | Redshift 클러스터 / BigQuery 슬롯 예약 |
| 간헐적 분석 (비용 최소화) | BigQuery 온디맨드 / Redshift Serverless / Synapse 서버리스 |

## 참고하기

### AWS

- [Amazon Redshift 문서](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html)

### Azure

- [Azure Synapse Analytics 문서](https://learn.microsoft.com/azure/synapse-analytics/)

### GCP

- [Google BigQuery 문서](https://cloud.google.com/bigquery/docs)

### OCI

- [OCI Autonomous Data Warehouse 문서](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html)

### 표준 및 커뮤니티

- [Apache Iceberg](https://iceberg.apache.org/)
- [Delta Lake](https://delta.io/)
