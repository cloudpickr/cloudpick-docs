---
title: "Database Migration"
description: "Compares DB migration strategies (Rehost/Replatform/Refactor) and downtime-minimization techniques across vendors."
---

> Last reviewed: May 2026

## Overview

**Migration services** are used when moving an on-premises DB to the cloud, or moving a DB between clouds. Simple backup/restore can work, but for large-scale DBs, **online migration** — continuously synchronizing data while minimizing downtime — is needed.

### Types of migration

| Type | Description | Downtime |
| --- | --- | --- |
| **Homogeneous migration** | Moving between the same engine (MySQL → MySQL) | Minimal (real-time sync via CDC) |
| **Heterogeneous migration** | Switching to a different engine (Oracle → PostgreSQL) | Requires schema conversion + data movement |
| **Continuous replication** | Real-time on-premises ↔ cloud synchronization | None (hybrid operation) |

## Product comparison

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | DMS (Database Migration Service) | Homogeneous/heterogeneous migration. Continuous replication via CDC (Change Data Capture) |
| AWS | SCT (Schema Conversion Tool) | Automatic schema conversion for heterogeneous migration |
| Azure | Azure Database Migration Service | Online/offline migration. Optimized for moving to Azure SQL |
| Azure | Azure Migrate | Assessment/execution for full workload migration, including DBs |
| Google Cloud | Database Migration Service | MySQL, PostgreSQL, SQL Server → Cloud SQL/AlloyDB |
| Google Cloud | Datastream | CDC-based real-time replication. Can stream to BigQuery |
| OCI | OCI Database Migration | Oracle/MySQL → OCI DB. Supports online migration (zero downtime) |

## Key differences

**AWS DMS** — Supports the widest range of source/target engine combinations. You can migrate from diverse sources like Oracle, SQL Server, MongoDB, and S3 to an AWS DB. Combined with SCT, it automates schema conversion for heterogeneous migration.

**Azure** — Specialized for migration to Azure SQL, making SQL Server workload transitions the smoothest. Azure Migrate lets you perform a pre-migration assessment (compatibility, cost estimate).

**Google Cloud Datastream** — Provides CDC-based real-time replication, and can stream directly into BigQuery to build an analytics pipeline.

**OCI Database Migration** — Can perform online migration (zero downtime) of Oracle/MySQL DBs into OCI, and supports GoldenGate-based real-time replication.

## Migration strategies

Database migration broadly falls into 3 strategies (the DB-related subset of the 6 Rs). Complexity and cost differ, so choose according to workload characteristics.

| Strategy | Description | Suitable for | Example |
| --- | --- | --- | --- |
| **Rehost** | Move the same engine to the cloud as-is. "Lift and Shift" | Goal is fast migration, no engine change needed | MySQL → RDS MySQL, Oracle → OCI DB System |
| **Replatform** | Keep the engine but move to a managed service. Some optimization applied | Goal is reducing operational burden, minimal code change | MySQL → Aurora MySQL, PostgreSQL → AlloyDB |
| **Refactor** | Change the engine or redesign the architecture | Goal is a fundamental improvement in performance/cost/scalability | Oracle → PostgreSQL, splitting a monolithic DB into DynamoDB + RDS |

### Strategy selection criteria

- **When time constraints are significant** → Rehost (fastest)
- **When you want to reduce operational cost** → Replatform (move to managed)
- **When resolving license cost or scalability limits** → Refactor (highest impact, highest cost/risk)

:::caution
Heterogeneous migration (e.g., Oracle → PostgreSQL) is not simple data movement. It includes **schema conversion, rewriting procedures/triggers, and modifying application queries**. Starting without a sufficient assessment phase can take several times longer than expected.
:::

## The risk of carrying DB-internal logic (procedures/triggers) over as-is

On-premises DBs often implement a significant portion of business logic as **stored procedures**, **triggers**, and **user-defined functions (UDFs)**. During migration, there's often a desire to carry these over unchanged, but this creates the following problems in a cloud environment.

### Scalability limits

- **The DB instance becomes the bottleneck** — Since procedures run inside the DB, business-logic load consumes DB CPU/memory. It can't be distributed across read replicas, so you're limited to vertical scaling of the DB instance.
- **No horizontal scaling** — The application layer can scale infinitely via auto scaling, but the DB cannot. If logic lives in the DB, overall system scalability is bound by DB performance.

### Increased vendor lock-in

- **Locked to a specific DB engine** — Oracle PL/SQL, SQL Server T-SQL, and PostgreSQL PL/pgSQL are not compatible with each other. Switching to a managed service or moving to a different cloud requires rewriting all the logic.
- **Heterogeneous migration becomes harder** — When switching from Oracle to PostgreSQL, data can be moved with DMS, but procedures require manual conversion, and conversion tools (SCT, etc.) don't support every syntax.

### Operational and observability issues

- **Difficult version control** — Application code is managed in Git, but procedures live inside the DB, making version control fragile.
- **Difficult test automation** — Integrating procedures into unit tests and CI/CD pipelines is difficult.
- **Delayed root-causing of incidents** — APM and distributed tracing tools track application code, but the inside of a procedure is a black box.
- **Limited debugging tools** — IDE support is much weaker than for application languages (Java, Python, etc.).

### Security and compliance risk

- **Complex access-permission management** — When a procedure manipulates multiple tables internally, applying the principle of least privilege becomes difficult.
- **Low audit log resolution** — Often only the execution of the single procedure is logged, and its internal behavior isn't recorded.

### Recommended approach

| Situation | Recommended direction |
| --- | --- |
| **Need to move to the cloud quickly** | Rehost, keeping procedures, then gradually move them to the application layer afterward |
| **Moving to a managed DB** | Check the scope of procedure functionality the managed DB supports (e.g., some system procedures are restricted in managed offerings) |
| **Designing something new** | Keep business logic in the application layer; have the DB focus on storing/retrieving data |
| **Distributed transactions are required** | Consider the Saga pattern or an event-driven architecture instead of procedures |

:::note
**Core principle:** Procedures/triggers can be retained for legacy compatibility, but **avoid adding new logic inside the DB** — put it in the application layer instead. Over time, gradually migrating logic to the application is necessary to fully leverage the cloud's scalability and flexibility.
:::

## Migration process

DB migration is not a one-time data move but a project spanning multiple phases.

| Phase | Key activities |
| --- | --- |
| **1. Discovery** | Understand the current DB inventory (engine, version, size, performance, dependencies) |
| **2. Assessment** | Compatibility assessment, schema conversion needs, cost estimation, risk identification |
| **3. Planning** | Choose migration strategy (Rehost/Replatform/Refactor), finalize downtime budget, build a rollback plan |
| **4. Migration** | Schema migration → initial data load → CDC-based continuous replication → validation |
| **5. Validation** | Data integrity verification, application testing, performance comparison |
| **6. Cutover** | Switch the application to the new DB. Read-only mode → wait for replication to complete → cutover |

### Downtime-minimization strategies

Key techniques for reducing downtime in large-scale DB migrations.

| Technique | Description | When to use |
| --- | --- | --- |
| **CDC (Change Data Capture)** | Reads the source DB's transaction log and continuously replicates to the target | The default for online migration. Real-time sync after the initial load |
| **Blue/Green deployment** | Run the existing DB (Blue) and new DB (Green) simultaneously, then switch traffic | When rollback needs to be easy at cutover |
| **Read-only lock** | Switch the source DB to read-only just before cutover, then switch over once replication is complete | When a few minutes to tens of minutes of downtime is acceptable |
| **Dual writes** | The application writes to both DBs simultaneously | When zero downtime is required but complexity is high |

## Common mistakes

- **Underestimating the difficulty of heterogeneous migration** — Converting from Oracle to PostgreSQL requires rewriting not just data movement but the entire set of procedures, triggers, and queries. Starting without an assessment can multiply the schedule several times over.
- **Not monitoring CDC replication lag** — If replication lag is significant at cutover time, data loss occurs. Monitor replication lag metrics continuously.
- **Immediately decommissioning the source DB after cutover** — Unexpected issues can surface after the switch. Keep the source DB around for a period to preserve rollback capability.

## Checklist

- [ ] Did you perform a compatibility assessment before migration and identify items requiring conversion?
- [ ] Have you defined CDC replication-lag monitoring and cutover decision criteria (lag < N seconds)?
- [ ] Did you perform data integrity verification after cutover (record counts, checksums, sample comparison)?

## References

### AWS

- [AWS Database Migration Service (DMS) documentation](https://docs.aws.amazon.com/ko_kr/dms/)
- [AWS Schema Conversion Tool (SCT) documentation](https://docs.aws.amazon.com/ko_kr/SchemaConversionTool/)

### Azure

- [Azure Database Migration Service documentation](https://learn.microsoft.com/ko-kr/azure/dms/)
- [Azure Migrate documentation](https://learn.microsoft.com/ko-kr/azure/migrate/)

### Google Cloud

- [Database Migration Service documentation](https://cloud.google.com/database-migration/docs)
- [Datastream documentation](https://cloud.google.com/datastream/docs)

### OCI

- [OCI Database Migration documentation](https://docs.oracle.com/en-us/iaas/database-migration/index.html)
