---
title: "Object Storage"
description: "Compares object storage services, storage classes, and the evolution of lakehouse architecture across vendors."
---

> Last reviewed: August 2026

## Overview

To store files in your own data center, you must purchase NAS or SAN and add disks as capacity runs short. Poor capacity planning leads to either running out of space or overinvesting.

**Object storage** is cloud storage that lets you store files without a capacity limit. You don't need to decide capacity in advance — you pay only for what you store. It's used to store nearly all types of unstructured data, including images, videos, backups, logs, and data lakes.

:::note
Services equivalent to AWS S3: Azure's Blob Storage, Google Cloud's Cloud Storage, and OCI's Object Storage.
:::

### Why Object Storage

- **Very inexpensive** — At around $0.02–0.03 per GB per month, it's far cheaper than block storage ($0.08–0.10 per GB) or file storage. Using an archive class can bring this down to below $0.001 per GB, though archive classes incur separate retrieval costs and wait times.
- **Unlimited capacity** — There's no upper bound on storage capacity. From 1KB to several PB, storage works the same way.
- **Durability** — Every vendor offers **99.999999999% (11 nines)** durability. This means, if you store 10 million objects, you would expect to lose one roughly every 10,000 years. Data is automatically replicated across multiple AZs, making data loss practically nonexistent.
- **HTTP API access** — Instead of a file system (folders/paths), it uses a key-value structure, accessible from anywhere via REST API.
- **S3-compatible API** — AWS S3 has become the de facto standard API, and most vendors and tools support an S3-compatible API.

## Product Comparison

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | S3 (Simple Storage Service) | The de facto industry standard. A wide range of storage classes (Standard, IA, Glacier, etc.) |
| Azure | Blob Storage | Hot/Cool/Cold/Archive tiers. Integrated with Data Lake Storage Gen2 |
| Google Cloud | Cloud Storage | Standard/Nearline/Coldline/Archive. Automatic replication with Multi-region/Dual-region |
| OCI | OCI Object Storage | Standard/Infrequent Access/Archive tiers. Supports an S3-compatible API |

### Storage Classes (Cost Optimization by Access Frequency)

Access frequency for data tends to decrease over time. Every vendor offers storage classes that lower storage costs based on access frequency. Storage cost decreases but retrieval cost increases, so choose a class that matches your access pattern.

| Access frequency | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| Frequent access | S3 Standard | Hot | Standard | Standard |
| Occasional access | S3 Standard-IA | Cool | Nearline (30 days) | Infrequent Access |
| Rare access | S3 Glacier Instant | Cold | Coldline (90 days) | — |
| Archive | S3 Glacier Deep Archive | Archive | Archive (365 days) | Archive |
| **Automatic tiering** | S3 Intelligent-Tiering | — | Autoclass | Auto-Tiering |

AWS S3 Intelligent-Tiering, Google Cloud Autoclass, and OCI Auto-Tiering automatically analyze access patterns and move data to the optimal class, reducing operational burden since manual lifecycle policies aren't required.

:::note
If you're unsure, start with the standard class, then set up automatic transitions via a lifecycle policy after analyzing access patterns. Using an automatic tiering service removes the need for manual policy configuration.
:::

:::caution
**Archive class caution:** While storage cost is very low, retrieval incurs separate costs and wait times (several hours to 12 hours). There's also a minimum retention period (90–365 days), and early deletion incurs a fee. Don't place data that might be accessed frequently into an archive class.
:::

## Key Differences

**AWS S3** — Launched in 2006 as one of the first object storage services in the public cloud, the S3 API has been widely adopted as an industry-compatible standard. Most third-party tools, other cloud vendors, and on-premises storage support an S3-compatible API. AWS is evolving storage itself to embed analytics and AI capabilities, with services like S3 Tables, S3 Metadata, S3 Vectors, and **S3 Annotations**. S3 Annotations lets you attach up to 1GB of queryable context (metadata) directly to an object, allowing AI agents to discover, understand, and process data without a separate metadata system.

**Azure Blob Storage** — Blob Storage and Data Lake Storage Gen2 are unified within the same storage account. Hierarchical namespace (folder structure) support makes file management convenient for big data workloads. Integration with Microsoft Fabric simplifies building analytics pipelines.

**Google Cloud Cloud Storage** — Multi-region and Dual-region options automatically replicate data across multiple regions without separate replication configuration. Autoclass supports automatic storage class transitions, and BigLake enables direct querying from BigQuery.

**OCI Object Storage** — Supports an S3-compatible API, with Auto-Tiering automatically switching between Standard and Infrequent Access based on access patterns. A free egress policy of 10TB/month provides a significant cost advantage for large data transfers.

## When to Choose What

| When | Choose this |
| --- | --- |
| You want to make full use of the S3-compatible API ecosystem | AWS S3 |
| You need big data + hierarchical namespace (folder structure) | Azure Data Lake Storage Gen2 |
| You want automatic multi-region replication with no extra setup | Google Cloud Cloud Storage (Multi-region) |
| You want automatic storage class transitions | AWS S3 Intelligent-Tiering, Google Cloud Autoclass, OCI Auto-Tiering |
| You want to reduce large-scale egress costs | OCI Object Storage (10TB/month free) |
| You want to run SQL analytics directly on object storage | AWS Athena + S3, or Google Cloud BigQuery External Tables |

:::caution
**Be sure to check egress cost.** Putting data into object storage is free, but taking it out (egress) incurs a cost. For workloads that transfer large volumes of data externally, this is a key TCO factor in vendor selection.
- AWS/Azure/Google Cloud: egress $0.08–0.12/GB (varies by region)
- OCI: **10TB/month free**, then $0.0085/GB

The figures above are current as of this document's writing and may change. Check each vendor's official pricing page for current rates.
:::

## Usage Patterns

| Use case | Description | Why object storage |
| --- | --- | --- |
| Static web hosting | Serving SPAs and static sites | CDN integration, serverless, unlimited scaling |
| Data lake | Repository for raw data | No schema required, low-cost at large scale, supports diverse formats |
| Log/event archive | Storing audit logs and event streams | Append-only, automatic archiving via lifecycle policy |
| ML training data | Images, text, feature stores | Large-scale unstructured data, parallel reads |
| Backup/DR | DB snapshots, system images | 99.999999999% durability, cross-region replication |
| Media storage/streaming | Original video and image files | Large scale, CDN origin, input for transcoding pipelines |

:::note
For analytics services on top of a data lake, see [Data Analytics Services](../../database/analytics/); for building ETL/ELT pipelines, see [Data Pipelines](../../database/data-pipeline/); for event-triggered processing, see [Serverless](../../compute/serverless/).
:::

## The Evolution of Object Storage

Object storage has grown beyond simple file storage to become the **foundational storage layer for data lakes**. In the past, data had to be copied into a separate data warehouse for analysis, but now the **lakehouse** architecture — analyzing data directly where it sits in object storage — has become standard.

### The Lakehouse Pattern

Raw data stays in object storage and is structured using table formats (Iceberg, Delta Lake, Hudi), enabling direct SQL queries without a separate data warehouse.

**Medallion Architecture (Bronze/Silver/Gold):**

- **Bronze** — Raw data as-is (a mix of JSON, CSV, Parquet). Automatically archived via lifecycle policy
- **Silver** — Cleansed/transformed data (Parquet, schema applied)
- **Gold** — Business-level aggregates/marts (ready for immediate analysis)

### Event-Driven Pipelines

Object uploads trigger events that automatically run transformation/analysis.

| Vendor | Trigger | Processing |
| --- | --- | --- |
| AWS | S3 Event Notification | Lambda, Step Functions, EventBridge |
| Azure | Blob Trigger | Functions, Data Factory |
| Google Cloud | Cloud Storage Trigger | Cloud Functions, Dataflow |
| OCI | OCI Events | OCI Functions, Data Flow |

### Vendor Data Platform Services

| Feature | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Data lake** | S3 + Lake Formation | Data Lake Storage Gen2 + Fabric | Cloud Storage + BigLake | OCI Object Storage + Data Lake |
| **Table storage (Iceberg)** | S3 Tables | Data Lake Storage + Synapse | BigLake (native Iceberg) | — |
| **Automatic metadata management** | S3 Metadata | Blob Index Tags | — | — |
| **Vector storage/search** | S3 Vectors (Preview) | AI Search + Blob integration | BigQuery Vector Index | AI Vector Search (Autonomous DB) |
| **Direct SQL query** | S3 Select, Athena | Query Acceleration, Synapse | BigQuery External Tables | OCI Data Flow (Spark) |

:::note
Every vendor is pursuing a "storage to data platform" direction. AWS is embedding capabilities into S3 itself, Azure is integrating Data Lake Storage with Fabric, and Google Cloud is taking the BigLake + BigQuery integration approach.
:::

## Common Mistakes

- **No lifecycle policy configured** — Without a lifecycle policy, old data remains in a high-cost storage class indefinitely, accumulating unnecessary cost.
- **Leaving public access unblocked** — Failing to block public access to a bucket/container can expose sensitive data to the internet.
- **Versioning not enabled** — Without versioning enabled, accidentally overwritten or deleted data cannot be recovered.

## Checklist

- [ ] Is a lifecycle policy configured to automatically transition/delete old data?
- [ ] Is Block Public Access enabled?
- [ ] Is versioning or cross-region replication enabled?
- [ ] Is server-side encryption (SSE) applied?

## References

### AWS

- [Amazon S3 documentation](https://docs.aws.amazon.com/ko_kr/s3/)
- [Amazon S3 storage classes](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/storage-class-intro.html)
- [S3 Intelligent-Tiering](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/intelligent-tiering.html)
- [S3 Tables documentation](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/s3-tables.html)
- [S3 Metadata documentation](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/s3-metadata.html)
- [AWS Lake Formation documentation](https://docs.aws.amazon.com/ko_kr/lake-formation/)
- [Amazon Athena documentation](https://docs.aws.amazon.com/ko_kr/athena/)

### Azure

- [Azure Blob Storage documentation](https://learn.microsoft.com/ko-kr/azure/storage/blobs/)
- [Azure Blob access tiers](https://learn.microsoft.com/ko-kr/azure/storage/blobs/access-tiers-overview)
- [Data Lake Storage Gen2 documentation](https://learn.microsoft.com/ko-kr/azure/storage/blobs/data-lake-storage-introduction)
- [Azure Synapse Analytics documentation](https://learn.microsoft.com/ko-kr/azure/synapse-analytics/)
- [Microsoft Fabric documentation](https://learn.microsoft.com/ko-kr/fabric/)

### Google Cloud

- [Google Cloud Storage documentation](https://cloud.google.com/storage/docs)
- [Cloud Storage classes](https://cloud.google.com/storage/docs/storage-classes)
- [Autoclass documentation](https://cloud.google.com/storage/docs/autoclass)
- [BigLake documentation](https://cloud.google.com/biglake)
- [BigQuery External Tables](https://cloud.google.com/bigquery/docs/external-data-cloud-storage)

### OCI

- [OCI Object Storage documentation](https://docs.oracle.com/en-us/iaas/Content/Object/home.htm)
- [OCI Object Storage tiers](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/understandingstoragetiers.htm)
