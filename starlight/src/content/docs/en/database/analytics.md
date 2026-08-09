---
title: "Data Analytics Platforms"
description: "Compares data warehouses, data lakehouses, and analytics platforms across vendors."
---

> Last reviewed: May 2026

## Overview

### OLTP vs. OLAP — why they're separated

Operational databases ([managed RDB](../../database/managed-rdb/), [NoSQL](../../database/nosql/)) are optimized for transaction processing (OLTP). Aggregating and analyzing large volumes of data requires a separate analytics platform (OLAP).

**Analogy:** An operational DB is a store's checkout counter (fast, individual transaction processing), while a warehouse is the headquarters' business analytics team (aggregating data across all stores to analyze trends). Running business analytics at the checkout counter makes the line grow long.

Running large aggregation queries against an operational DB causes:
- Degraded transaction processing performance (orders slow down)
- Analytical queries against a normalized schema requiring dozens of joins — slow and complex
- Hence the separation: operational DB → ETL → dedicated analytics DB (warehouse)

| Aspect | OLTP (operational DB) | OLAP (analytics platform) |
| --- | --- | --- |
| **Purpose** | Individual transaction processing (orders, payments) | Aggregating/analyzing large volumes of data (revenue trends, user behavior) |
| **Query pattern** | Reading/writing small numbers of rows (ms scale) | Scanning/aggregating large numbers of rows (seconds to minutes) |
| **Data size** | GB-TB | TB-PB |
| **Schema** | Normalized (3NF) | Denormalized (star/snowflake) or schemaless |

## Analytics platform comparison by vendor

| Vendor | Data warehouse | Characteristics | Billing model |
| --- | --- | --- | --- |
| AWS | [Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html) | Cluster-based + Serverless option. Query S3 data directly (Spectrum) | Node-hours or RPU (Serverless) |
| Azure | [Azure Synapse Analytics](https://learn.microsoft.com/azure/synapse-analytics/) | Unified analytics platform (SQL + Spark + Data Explorer). Serverless SQL pool | DWU (dedicated) or query data processed (serverless) |
| Google Cloud | [BigQuery](https://cloud.google.com/bigquery/docs) | Fully serverless. No infrastructure management. Built-in ML (BQML) | Query data scanned, or slots (reserved capacity) |
| OCI | [OCI Analytics Cloud](https://docs.oracle.com/en-us/iaas/analytics-cloud/index.html) + [Autonomous Data Warehouse](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html) | Auto-tuning based on Oracle DB. Integrated BI visualization | OCPU-hours |

### Key differences

**BigQuery (Google Cloud)** — Fully serverless, requiring no cluster management. Billed based on the amount of data scanned per query, and BigQuery ML supports SQL-based ML training.

**Redshift (AWS)** — Offers both cluster-based and Serverless options. Data in S3 can be queried directly via Redshift Spectrum, making integration with a data lake straightforward.

**Synapse (Azure)** — Provides SQL analytics, Apache Spark, and Data Explorer on a single platform. The serverless SQL pool can query a data lake directly, and it integrates natively with Power BI.

**Autonomous DW (OCI)** — Based on Oracle Database, it offers auto-tuning and auto-scaling. Highly compatible with existing Oracle workloads.

## Data lake vs. data warehouse vs. lakehouse

| Architecture | Characteristics | Suitable for |
| --- | --- | --- |
| **Data lake** | Stores raw data as-is (S3/ADLS/GCS). Schema-on-read | Storing large volumes of varied-format data, ML training data |
| **Data warehouse** | Stores refined data in a structured form. Schema-on-write | Structured data analytics, BI reporting, dashboards |
| **Lakehouse** | Adds warehouse capabilities on top of a lake (Delta Lake, Iceberg) | When you want to unify both |

Lakehouse approach by vendor:

| Vendor | Lakehouse approach |
| --- | --- |
| AWS | S3 + Glue Catalog + Redshift Spectrum + Athena (Apache Iceberg support) |
| Azure | ADLS Gen2 + Synapse + Delta Lake (unified via Microsoft Fabric) |
| Google Cloud | GCS + BigQuery (external table integration via BigLake) |
| OCI | Object Storage + Autonomous DW + OCI Data Flow (Spark) |

## BI visualization tools

Turning analysis results into something people can see requires a BI (Business Intelligence) tool.

| Vendor | BI tool | Characteristics |
| --- | --- | --- |
| AWS | [Amazon Quick Sight](https://aws.amazon.com/quick/) | BI functionality under Amazon Quick (formerly QuickSight). AI-agent-based natural language querying, dashboards, analytics. Also accessible via the Quick Desktop app |
| Azure | [Power BI](https://powerbi.microsoft.com/) | Widest user base, Excel-friendly, Copilot integration |
| Google Cloud | [Looker / Looker Studio](https://cloud.google.com/looker) | LookML-based semantic layer; Looker Studio is free |
| OCI | [OCI Analytics Cloud](https://docs.oracle.com/en-us/iaas/analytics-cloud/index.html) | Oracle-native, self-service visualization |
| 3rd party | Tableau, Metabase, Apache Superset | Vendor-neutral, useful in multi-cloud environments |

Why BI tools matter:
- Business users who don't know SQL can still use data
- Real-time monitoring via dashboards
- Self-service analytics relieves the data team's bottleneck

## Selection criteria

| Criterion | Recommendation |
| --- | --- |
| Minimize infrastructure management + query-based billing | BigQuery |
| Integrating with an existing AWS data lake (S3) | Redshift + Spectrum |
| Unified SQL + Spark + BI platform | Synapse / Microsoft Fabric |
| Oracle DB workload + auto-tuning | OCI Autonomous DW |
| Cost predictability (fixed capacity) | Redshift cluster / BigQuery reserved slots |
| Intermittent analytics (minimize cost) | BigQuery on-demand / Redshift Serverless / Synapse serverless |

## Common mistakes

- **Running analytical queries directly against the operational DB** — Without separating OLTP and OLAP, analytical queries degrade transaction processing performance. Always split off a dedicated analytics platform.
- **Overusing `SELECT *` under scan-based billing** — In scan-volume-based billing models like BigQuery, not specifying only the needed columns can increase cost by tens of times.
- **Loading data into a data lake without governance** — Piling up data with no schema management, access control, or data catalog turns it into a "data swamp."

## Checklist

- [ ] Are OLTP (operational) and OLAP (analytics) workloads physically separated?
- [ ] Do you understand the analytics platform's billing model (scan volume/slots/nodes) and have you set a cost ceiling?
- [ ] Is a data catalog and access control policy in place?

## References

### AWS

- [Amazon Redshift documentation](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html)
- [Amazon Quick documentation](https://docs.aws.amazon.com/quick/latest/userguide/what-is.html)
- [Amazon Quick Desktop download](https://aws.amazon.com/quick/download/)

### Azure

- [Azure Synapse Analytics documentation](https://learn.microsoft.com/azure/synapse-analytics/)

### Google Cloud

- [Google BigQuery documentation](https://cloud.google.com/bigquery/docs)

### OCI

- [OCI Autonomous Data Warehouse documentation](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html)

### Standards and community

- [Apache Iceberg](https://iceberg.apache.org/)
- [Delta Lake](https://delta.io/)
