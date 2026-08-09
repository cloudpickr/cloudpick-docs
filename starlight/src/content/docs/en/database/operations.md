---
title: "Database Operations"
description: "Covers RDB scaling patterns, NoSQL key design, cache operations, slow query management, and HA/backup."
---

> Last reviewed: May 2026

## Overview

A managed cloud DB automates infrastructure operations (patching, backup, HA), but **data design and query performance don't automatically improve.** This document covers the key topics you need to know for the operational phase after you've chosen a DB.

:::note
For DB selection guides, see [Managed RDB](../../database/managed-rdb/), [NoSQL](../../database/nosql/), and [Cache](../../database/cache/). This document focuses on "how to operate it once you've chosen."
:::

## RDB scaling patterns

Unlike NoSQL, horizontal scaling (sharding) is difficult for an RDB. Most scaling is achieved through **read distribution**.

| Step | Method | Effect | Example |
| --- | --- | --- | --- |
| 1. **Vertical scaling** | Upgrade the instance type (increase CPU/memory) | Simplest. Has a limit | db.r5.large → db.r5.4xlarge |
| 2. **Read replicas** | Distribute read traffic to replicas | Effective for workloads that are 80%+ reads | Serving product-list queries from a replica |
| 3. **Cache layer** | Store frequently read data in a cache (Redis/Valkey) | Dramatically reduces DB load. Millisecond responses | Caching sessions, popular products, config values |
| 4. **CQRS** | Separate the write (command) and read (query) DBs | Each can be optimized independently | Order writes go to the RDB; search/dashboards use a separate read DB |
| 5. **Sharding** | Distribute data across multiple DBs | Last resort. Sharply increases app complexity | Splitting the DB by user ID |

:::note
Most web services are 80-90% reads. A combination of read replicas + cache can resolve most of the RDB's load.
:::

## Query performance management

| Problem | Symptom | Response |
| --- | --- | --- |
| **Indiscriminate JOINs** | Joining many tables makes responses take several seconds or more | Split off read replicas, denormalize, move analytical queries to a DW |
| **Missing indexes** | Full table scans. Gets progressively slower as data grows | Check the execution plan (EXPLAIN), add indexes matching query patterns |
| **Ignoring slow queries** | A specific query degrades performance for the entire DB | Enable the slow query log, review it regularly, refactor queries |
| **Using the DB as storage** | Unbounded accumulation of logs/events in the RDB | Move time-series data to object storage or a time-series DB |

:::caution
Processing OLTP (transactions) and OLAP (analytics) in the same DB puts pressure on each other's performance. As analytical queries grow, split them off into a [data analytics platform](../../database/analytics/).
:::

### Index design basics

**Cardinality**: the number of unique values in a column. A user ID (millions of values) has high cardinality, while gender (2 values) has low cardinality. Indexing high-cardinality columns has the greatest effect.

| Principle | Description |
| --- | --- |
| **Base it on the WHERE clause** | Index columns you filter on frequently |
| **Check cardinality** | Columns with many unique values benefit most from an index. Low-cardinality columns like booleans see little benefit |
| **Compound index order** | Place the most selective (highest-cardinality) column first |
| **Covering index** | Including the SELECT columns in the index lets queries respond without touching the table |
| **Beware excessive indexing** | Too many indexes degrade write performance. Consider your read/write ratio |

:::note
Before adding an index, always check how the current query behaves via `EXPLAIN` (the execution plan). Prioritize improving queries that cause full table scans first.
:::

## High availability (HA)

| Method | Behavior | RPO | RTO | Cost | Suitable for |
| --- | --- | --- | --- | --- | --- |
| **Multi-AZ synchronous replication** | Synchronous replication across multiple AZs within the same region. Automatic failover | 0 | Tens of seconds to a few minutes | Medium (standby instance cost) | Production default |
| **Read replicas** | Asynchronous replication. Read distribution + manual promotion for DR | A few seconds (replication lag) | A few minutes (manual promotion) | Low | Read-load distribution + lightweight DR |
| **Cross-region replication** | Asynchronous replication to another region. For regional-outage protection | A few seconds to a few minutes | A few minutes (manual promotion) | High (cross-region transfer) | Regional-outage DR |

### HA services by vendor

| Feature | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Multi-AZ synchronous** | RDS Multi-AZ, Aurora storage replication | Zone-redundant HA | Cloud SQL HA | ADB automatic HA |
| **Read replica** | Aurora Read Replica | Read Replica | Cloud SQL Read Replica | ADB Read-only Replica |
| **Cross-region** | Aurora Global Database | Geo-replication | Cross-Region Replica | Autonomous Data Guard |

## Backup and PITR

| Vendor | Backup retention | PITR |
| --- | --- | --- |
| AWS RDS / Aurora | Up to 35 days | Second-level recovery |
| Azure SQL Database | Up to 35 days | Second-level recovery |
| Google Cloud Cloud SQL / AlloyDB | Up to 365 days | Second-level recovery |
| OCI Autonomous Database | Up to 60 days | Second-level recovery |

:::note
For backup strategy and DR configuration details, see [Backup and Recovery](../../storage/backup/) and [Disaster Recovery](../../governance/dr/).
:::

## Connection pool management

DB connections are a finite resource. In serverless/auto-scaling environments especially, connections can explode when instances spike.

| Problem | Response |
| --- | --- |
| Connection exhaustion | Use a connection pooler (RDS Proxy, Cloud SQL Auth Proxy, PgBouncer) |
| Serverless function concurrency spikes | Limit with Reserved Concurrency + a connection pooler is essential |
| Idle connections holding resources | Set idle timeouts, reuse connections |

## NoSQL key design anti-patterns

Unlike an RDB, NoSQL requires you to **define query patterns first and design keys accordingly**. Symptoms commonly seen in operations (hot partitions, throttling) originate from key design mistakes made at the design stage.

:::note
For key design patterns and principles, see [NoSQL Database — Key Design Patterns](../../database/nosql/).
:::

## Cache operations

Cache is a key tool for reducing DB load, but it has its own operational considerations.

:::note
For cache pattern definitions (Cache-Aside, Write-Through, Write-Behind, etc.) and a vendor service comparison, see [Cache](../../database/cache/).
:::

### Cache operations considerations

- **Cache stampede** — Hundreds of requests hit the DB simultaneously when a TTL expires. Prevent with random TTL jitter or lock-based refresh
- **Cache warm-up** — Right after a deploy/restart, the cache is empty and DB load spikes. A pre-warming script is needed
- **Memory management** — Check the eviction policy (LRU, LFU) for when cache memory is exceeded. Make sure important data isn't evicted
- **Don't use the cache as permanent storage** — Design assuming the cache can disappear at any time. The source of truth must always be the DB
- **Set a TTL on every key** — Caching without a TTL leaves data around forever, causing inconsistency with the DB

## Common mistakes

- **Adding indexes without EXPLAIN** — Adding an index without checking the execution plan can degrade write performance with no read improvement.
- **Operating in a serverless environment without a connection pooler** — When Lambda/Functions concurrency spikes, DB connections get exhausted. Always use a connection pooler such as RDS Proxy.
- **Backups configured but recovery never tested** — Even with backups in place, if the recovery procedure isn't validated, recovery can fail during an actual incident.

## Checklist

- [ ] Is the slow query log enabled, and do you have a process to review it regularly?
- [ ] Is high availability configured via multi-AZ or read replicas?
- [ ] Have you actually tested PITR (point-in-time recovery)?

## References

### Related documents

- [Managed RDB](../../database/managed-rdb/) — DB selection guide
- [NoSQL](../../database/nosql/) — NoSQL selection guide
- [Cache and In-Memory](../../database/cache/) — cache selection guide
