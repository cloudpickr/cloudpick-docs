---
title: "Data Pipeline and ETL"
description: "Compares the concept of data pipelines (ETL/ELT), vendor services, and choosing between batch and streaming."
---

> Last reviewed: August 2026

## Overview

To use raw data in an [analytics platform](../../database/analytics/) or an ML pipeline, you need an **Extract → Transform → Load** process.

| Aspect | ETL | ELT |
| --- | --- | --- |
| **Where transformation happens** | Midway through the pipeline (a separate engine) | In the target system, after loading |
| **Suitable for** | Complex data cleaning, limited load capacity on the target system | Target has ample compute, like BigQuery/Redshift |
| **Trend** | Traditional approach | Becoming mainstream by leveraging cloud DW compute power |

## Comparison of vendor services

| Vendor | Batch ETL/ELT | Streaming | Orchestration |
| --- | --- | --- | --- |
| AWS | [Glue](https://docs.aws.amazon.com/glue/) (serverless Spark) | [Kinesis Data Streams](https://docs.aws.amazon.com/kinesis/) | [Step Functions](https://docs.aws.amazon.com/step-functions/), [MWAA](https://docs.aws.amazon.com/mwaa/) (Airflow) |
| Azure | [Data Factory](https://learn.microsoft.com/azure/data-factory/) | [Stream Analytics](https://learn.microsoft.com/azure/stream-analytics/) | Data Factory pipelines, [Synapse Pipelines](https://learn.microsoft.com/azure/synapse-analytics/) |
| Google Cloud | [Dataflow](https://cloud.google.com/dataflow/docs) (Apache Beam) | Dataflow (unified) | [Cloud Composer](https://cloud.google.com/composer/docs) (Airflow), [Workflows](https://cloud.google.com/workflows/docs) |
| OCI | [OCI Data Integration](https://docs.oracle.com/en-us/iaas/data-integration/home.htm) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) + [Data Flow](https://docs.oracle.com/en-us/iaas/data-flow/using/home.htm) (Spark) | OCI Data Integration pipelines |

## Batch vs. streaming

| Item | Batch | Streaming |
| --- | --- | --- |
| **Latency** | Minutes to hours | Seconds to minutes |
| **Cost** | Billed only for execution time (serverless) | Runs continuously (or event-driven) |
| **Complexity** | Low | High (ordering, deduplication, handling delays) |
| **Suitable for** | Daily/weekly reports, large-scale migration | Real-time dashboards, anomaly detection, recommendations |

## Zero-ETL

An approach that automatically replicates/synchronizes data from an operational DB to an analytics platform **without a pipeline**. The goal is to eliminate the burden of building and maintaining ETL pipelines.

### The ETL → ELT → Zero-ETL progression

| Generation | Approach | Burden |
| --- | --- | --- |
| ETL | Transform in a separate engine, then load | Build, operate, and monitor the pipeline |
| ELT | Load first, then transform in the DW | Pipeline is simplified, but transformation logic is still needed |
| Zero-ETL | Automatic source-to-target replication, no pipeline needed | Just configure it (in theory) |

### Zero-ETL status by vendor

| Vendor | Service | Source → target |
| --- | --- | --- |
| AWS | Aurora Zero-ETL to Redshift | Aurora MySQL/PostgreSQL → Redshift |
| AWS | DynamoDB Zero-ETL to Redshift | DynamoDB → Redshift |
| Azure | Fabric Mirroring | Azure SQL/Cosmos DB → Microsoft Fabric |
| Google Cloud | BigQuery continuous queries + change streams | Spanner/Bigtable → BigQuery |
| OCI | GoldenGate + Autonomous DB | Operational DB → Autonomous DW |

### Remaining limitations

| Limitation | Description |
| --- | --- |
| **Vendor lock-in** | Only supports source→target within the same vendor. There is no cross-vendor Zero-ETL |
| **No transformation logic** | It only replicates data "as-is" — business transformations (cleansing, aggregation, joining) still require a separate process |
| **Handling schema changes** | If the source schema changes, synchronization breaks or requires manual intervention |
| **Limited source support** | Not every DB is supported. Only certain engines/versions are available |

:::note
Zero-ETL is suitable for **simple replication**, and complex transformation, multi-source joins, or cross-vendor integration still requires an ETL/ELT pipeline. Realistically, a combination of Zero-ETL + lightweight ELT is likely.
:::

## What to choose when

| Requirement | Recommendation |
| --- | --- |
| Simple replication (same vendor, no transformation needed) | Zero-ETL |
| Serverless batch ETL (Spark) | Glue, Dataflow, Data Flow |
| Code-free ETL (GUI-based) | Data Factory, OCI Data Integration |
| Unified batch+streaming (Apache Beam) | Google Cloud Dataflow |
| Workflow orchestration (DAG) | Airflow (MWAA, Cloud Composer), Step Functions |
| Real-time streaming analytics | Kinesis Analytics, Stream Analytics, Dataflow |

## Common mistakes

- **Adopting streaming for a workload where batch would suffice** — Choosing streaming when real-time processing isn't needed only adds complexity and cost. Daily/weekly reports are fine with batch.
- **Expecting Zero-ETL to be a cure-all** — Zero-ETL only supports simple replication. If business transformation (cleansing, aggregation, joining) is needed, an ETL/ELT pipeline is still required.
- **Operating without pipeline monitoring** — If you can't detect data delays, schema changes, or failed jobs, analytical results end up based on stale data.

## Checklist

- [ ] Have you defined the workload's acceptable latency (minutes/hours/days) and chosen batch vs. streaming accordingly?
- [ ] Are alerting and retry policies set up for pipeline failures?
- [ ] Is there a schema evolution strategy so the pipeline doesn't break when the source schema changes?

## References

### AWS

- [AWS Glue documentation](https://docs.aws.amazon.com/glue/)
- [Amazon Kinesis documentation](https://docs.aws.amazon.com/kinesis/)

### Azure

- [Azure Data Factory documentation](https://learn.microsoft.com/azure/data-factory/)
- [Azure Stream Analytics documentation](https://learn.microsoft.com/azure/stream-analytics/)

### Google Cloud

- [Dataflow documentation](https://cloud.google.com/dataflow/docs)
- [Cloud Composer documentation](https://cloud.google.com/composer/docs)

### OCI

- [OCI Data Integration documentation](https://docs.oracle.com/en-us/iaas/data-integration/home.htm)
- [OCI Data Flow documentation](https://docs.oracle.com/en-us/iaas/data-flow/using/home.htm)
