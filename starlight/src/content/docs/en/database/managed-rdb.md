---
title: "Managed RDB"
description: "Compares the difference between managed RDB and cloud-native DB, HA configuration, and PITR across vendors."
---

> Last reviewed: June 2026

## Overview

Running a database on-premises requires you to handle server installation, OS patching, DB engine installation, backup configuration, replication setup, and failover entirely yourself. A **managed RDB** has the vendor take on this operational burden instead, letting you focus solely on data and queries.

:::note
For those familiar with AWS RDS: Azure has Azure SQL/Flexible Server, Google Cloud has Cloud SQL, and OCI has Autonomous Database.
:::

### The changing role of the DBA

| Area | On-premises DBA | Managed RDB environment |
| --- | --- | --- |
| OS/patch management | Performed directly | Handled by the vendor |
| Backup/recovery | Writing and testing scripts | Automatic backup + built-in PITR |
| HA/replication setup | Designed and operated directly | A multi-AZ checkbox |
| Performance tuning | Both queries and infrastructure | **Focus on query/schema optimization** |
| Capacity planning | Purchasing/expanding disks | Online expansion or auto-scaling |

:::caution
Choose managed by default unless there's a specific reason not to. Installing directly on a VM makes sense when there's a clear requirement, such as "the managed offering doesn't support this engine/version," "OS-level access is required," or "reducing BYOL license costs."
:::

:::note
For operations after choosing a DB — scaling patterns, query performance, caching, HA, backup — see [Database Operations](../../database/operations/).
:::

## Product comparison

### General-purpose managed RDB

| Vendor | Product | Type | Supported engines |
| --- | --- | --- | --- |
| AWS | RDS | Managed | MySQL, PostgreSQL, MariaDB, Oracle, SQL Server |
| AWS | Aurora | **Native** | MySQL/PostgreSQL compatible. In-house designed distributed storage |
| Azure | Azure SQL Database | Managed | Based on SQL Server |
| Azure | Azure Database for MySQL/PostgreSQL | Managed | Managed open-source engines |
| Google Cloud | Cloud SQL | Managed | MySQL, PostgreSQL, SQL Server |
| Google Cloud | AlloyDB | **Native** | PostgreSQL compatible. In-house design. Built-in vector search |
| OCI | Autonomous Database | **Native** | Based on Oracle DB. Automatic tuning/patching/scaling |
| OCI | MySQL HeatWave | Managed | MySQL compatible. Unified OLTP + OLAP processing |

### What is a cloud-native DB

Standard managed offerings (RDS, Cloud SQL) use the existing DB engine as-is, with only operations automated. **Cloud-native DBs** such as Aurora and AlloyDB have a fundamentally different architecture, having designed the storage layer themselves.

| Item | Standard managed | Cloud-native |
| --- | --- | --- |
| **Storage** | Block disk attached to the instance | Distributed storage decoupled from compute |
| **Replication** | Full data copy to a separate instance | The storage layer itself is multi-AZ replicated |
| **Adding a read replica** | Requires copying data (slow) | Shares the same storage (fast) |
| **Failover** | Switch to a standby instance (tens of seconds) | Attach new compute (seconds) |
| **Capacity** | Disk size pre-specified | Auto-scaling |

### Globally distributed DB

A DB that distributes data worldwide across regions and allows reads/writes in each region. Unlike a standard managed offering's "cross-region read replica," some services support **multi-region writes**.

| Type | Vendor | Product | Multi-region writes | Consistency |
| --- | --- | --- | --- | --- |
| **RDB** | AWS | Aurora Global Database | — (reads distributed only; writes single-region) | Strong consistency (primary) |
| **RDB** | Google Cloud | Spanner | Supported | Strong consistency (global transactions) |
| **NoSQL** | Azure | Cosmos DB | Supported | 5 selectable consistency levels |
| **NoSQL** | AWS | DynamoDB Global Tables | Supported | Eventual consistency (across regions) |
| **RDB** | OCI | Autonomous Data Guard | — (cross-region replication) | Strong consistency (primary) |

### Why global DBs are hard

Synchronizing data across regions is constrained by physics (the speed of light). The Seoul↔Virginia round-trip is around 200ms, so synchronously replicating every write drastically degrades performance.

| Trade-off | Description |
| --- | --- |
| **Strong consistency + multi-region writes** | Only Spanner supports this. Very high cost. Based on TrueTime (atomic clocks) |
| **Eventual consistency + multi-region writes** | DynamoDB Global Tables, Cosmos DB. Requires a conflict-resolution strategy |
| **Strong consistency + single-region writes** | Aurora Global DB. Only reads are distributed. Simplest but has write latency |

:::caution
Global DBs are expensive and complex to design. For most workloads, review in this order:
1. Is a single region sufficient? (Solve read latency with CDN + API caching)
2. Do only reads need to be distributed? (Cross-region read replica)
3. Do writes also need to be distributed? (Global DB — requires accepting conflict-resolution/consistency trade-offs)
:::

## Key differences

**AWS Aurora** — MySQL/PostgreSQL compatible. Storage is automatically replicated as 6 copies across 3 AZs. Aurora Serverless can bring cost to zero while idle.

**Azure SQL Database** — Based on SQL Server. Provides the smoothest migration path for existing SQL Server workloads. Scales up to 100TB in the Hyperscale tier.

**Google Cloud AlloyDB** — PostgreSQL compatible. Built-in vector search is a strength for AI workload integration.

**OCI Autonomous Database** — Based on Oracle DB. Automatic tuning, automatic patching, automatic scaling. MySQL HeatWave also supports unified OLTP+OLAP processing.

## Database@Cloud

Oracle is pursuing a strategy of placing its own database directly inside competitors' data centers.

| Service | Location | Characteristics |
| --- | --- | --- |
| [Oracle Database@Azure](https://www.oracle.com/cloud/azure/) | Azure DC | Native provisioning from the Azure Portal |
| [Oracle Database@AWS](https://www.oracle.com/cloud/aws/) | AWS DC | Direct provisioning from the AWS console. Oracle Autonomous AI Database Serverless GA (2026.06). DB@AWS available across 20 regions total |
| [Oracle Database@Google Cloud](https://www.oracle.com/cloud/google/) | Google Cloud DC | Used directly from the Google Cloud console |

With the app and DB in the same data center, this minimizes latency, eliminates egress cost, and satisfies data sovereignty requirements.

## What to choose when

| Situation | Recommendation |
| --- | --- |
| MySQL/PostgreSQL + high availability + automatic storage expansion | AWS Aurora |
| Migrating an existing SQL Server workload | Azure SQL Database |
| PostgreSQL + integrated AI/vector search | Google Cloud AlloyDB |
| Oracle DB + automatic tuning/patching | OCI Autonomous Database |
| Zero cost while idle (dev/test) | Aurora Serverless, Azure SQL Serverless |
| Unified OLTP + OLAP MySQL | OCI MySQL HeatWave |

## Common mistakes

- **Single-AZ deployment** — Deploying a production DB in a single AZ means the service goes down completely if that AZ fails. Always enable multi-AZ.
- **Not testing backups** — Setting up automatic backups without actually testing recovery can mean recovery fails or takes longer than expected during an incident.
- **Operating without indexes** — Operating without proper indexes causes query performance to degrade sharply as data grows, and full table scans increase DB load.

## Checklist

- [ ] Have you enabled multi-AZ (or another high-availability configuration)?
- [ ] Have you set up automatic backups and performed a recovery test?
- [ ] Have you enabled and are you monitoring the slow query log?
- [ ] Have you configured connection pooling (RDS Proxy, PgBouncer, etc.)?

## References

### AWS

- [Amazon RDS documentation](https://docs.aws.amazon.com/ko_kr/rds/)
- [Amazon Aurora documentation](https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/AuroraUserGuide/)

### Azure

- [Azure SQL Database documentation](https://learn.microsoft.com/ko-kr/azure/azure-sql/)
- [Azure Database for PostgreSQL documentation](https://learn.microsoft.com/ko-kr/azure/postgresql/)

### Google Cloud

- [Cloud SQL documentation](https://cloud.google.com/sql/docs)
- [AlloyDB documentation](https://cloud.google.com/alloydb/docs)

### OCI

- [OCI Autonomous Database documentation](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html)
- [OCI MySQL HeatWave documentation](https://docs.oracle.com/en-us/iaas/mysql-database/index.html)
