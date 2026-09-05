---
title: "Cache and In-Memory Databases"
description: "Compares the concept of in-memory caching, cache patterns, and vendor-managed services."
---

> Last reviewed: August 2026

## Overview

Database lookups incur disk I/O, taking several to tens of milliseconds. An **in-memory cache** stores frequently accessed data in memory, cutting response time down to microseconds.

:::note
For anti-patterns to watch for when operating a cache (using it as permanent storage, not setting TTLs, cache-dependent architecture, etc.), see [Database Operations — Cache Anti-Patterns](../../database/operations/#cache-operations-considerations).
:::

## Cache patterns

| Pattern | Behavior | Suitable for |
| --- | --- | --- |
| **Cache-Aside** | App checks the cache → on a miss, queries the DB → stores it in the cache | Read-heavy, most common |
| **Write-Through** | App writes to the cache → the cache synchronously writes to the DB | Consistency matters, write latency tolerable |
| **Write-Behind** | App writes to the cache → the cache asynchronously writes to the DB | Write performance matters, temporary inconsistency tolerable |
| **Read-Through** | The cache performs the DB lookup on the app's behalf | When the cache library supports DB integration |

## Comparison of vendor services

| Vendor | Service | Engine | Characteristics |
| --- | --- | --- | --- |
| AWS | [ElastiCache for Valkey](https://docs.aws.amazon.com/elasticache/) | Valkey (Redis fork) | **Default recommendation**. Serverless option. Vector search support |
| AWS | [ElastiCache for Redis](https://docs.aws.amazon.com/elasticache/) | Redis | For compatibility with existing workloads |
| AWS | [MemoryDB for Valkey](https://docs.aws.amazon.com/memorydb/) | Valkey | Durability guaranteed (disk persistence). Usable as a primary DB |
| Azure | [Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/) | Redis | Enterprise tier (based on Redis Enterprise) |
| Google Cloud | [Memorystore for Valkey](https://cloud.google.com/memorystore/docs) | Valkey | **Default recommendation**. Cluster mode, automatic failover |
| Google Cloud | [Memorystore for Redis](https://cloud.google.com/memorystore/docs) | Redis | For existing compatibility |
| OCI | [OCI Cache](https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm) | Redis-compatible | Managed Redis cluster |

:::note
**What is Valkey?** When Redis changed its license in 2024 (BSD → SSPL/RSALv2), Valkey emerged as an open-source fork under the Linux Foundation. It's compatible with existing Redis clients, and AWS and Google Cloud have switched to it as their default engine. New projects are recommended to use Valkey.
:::

## Valkey/Redis vs. Memcached

| Item | Valkey/Redis | Memcached |
| --- | --- | --- |
| **Data structures** | String, Hash, List, Set, Sorted Set, Stream | String only (key-value) |
| **Persistence** | RDB/AOF snapshots possible | None (pure cache) |
| **Replication/HA** | Replicas + automatic failover | None (client-side sharding) |
| **Pub/Sub** | Supported | Not supported |
| **Suitable for** | Session store, leaderboards, real-time analytics, Pub/Sub | Simple caching, large-object caching |

## What to choose when

| Requirement | Recommendation |
| --- | --- |
| DB read load distribution (general cache) | ElastiCache/Memorystore Valkey (or Redis) (Cache-Aside) |
| Session store (TTL + structured data) | Valkey / Redis (Hash type) |
| Primary DB replacement (durability required) | MemoryDB for Valkey |
| Simple key-value, maximum throughput | Memcached |
| Real-time leaderboard/counters | Valkey / Redis (Sorted Set) |

## Common mistakes

- **Using the cache as permanent storage** — A cache can disappear at any time. If original data isn't stored elsewhere, an outage causes data loss.
- **Not setting a TTL on every key** — Caching without TTLs leaves data around forever, causing inconsistency with the DB and eventual memory exhaustion.
- **Not implementing a fallback for cache failure** — In a cache-dependent architecture, if the cache goes down the entire service can stop. Always secure a direct-to-DB path for cache misses.

## Checklist

- [ ] Does every cache key have a TTL set that matches business requirements?
- [ ] Is a fallback path to query the DB directly implemented for cache failures?
- [ ] Have you checked cache memory usage monitoring and the eviction policy (LRU/LFU)?

## References

### Open source

- [Valkey official site](https://valkey.io/) — a Redis fork under the Linux Foundation
- [Valkey GitHub](https://github.com/valkey-io/valkey)

### AWS

- [Amazon ElastiCache documentation](https://docs.aws.amazon.com/elasticache/)
- [Amazon MemoryDB documentation](https://docs.aws.amazon.com/memorydb/)

### Azure

- [Azure Cache for Redis documentation](https://learn.microsoft.com/azure/azure-cache-for-redis/)

### Google Cloud

- [Memorystore documentation](https://cloud.google.com/memorystore/docs)

### OCI

- [OCI Cache documentation](https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm)
