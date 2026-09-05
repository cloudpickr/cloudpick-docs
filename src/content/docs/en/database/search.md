---
title: "Search and Log Analytics"
description: "Compares full-text search, vector search, and log analytics services across vendors."
---

> Last reviewed: August 2026

## Overview

:::note[Prerequisites and related documents]
For transactional data storage, see [Managed RDB](../../database/managed-rdb/) and [NoSQL](../../database/nosql/) first. This document focuses on search-engine workloads such as full-text search, log analysis, and tokenization. AI-based semantic search connects to [Vector Stores](../../ai/vector-store/).
:::

### Where search is needed in practice

| Use case | Description | Why DB LIKE/WHERE won't do |
| --- | --- | --- |
| Product/content search | E-commerce product search, internal document search | Needs tokenization/morphological analysis, synonyms, ranking |
| Log/access log analysis | Finding error patterns across hundreds of millions of log entries | RDBs are unsuited to scanning large volumes of text |
| Security event detection (SIEM) | Real-time detection of anomalous patterns | Needs a combination of time series + full-text search + aggregation |
| AI question answering (RAG) | Finding documents semantically similar to a user's question | Keyword matching can't capture meaning |
| Autocomplete/recommendations | Real-time suggestions while typing | Needs ms-level response + prefix matching + popularity weighting |

### Comparing search approaches — keyword vs. semantic vs. hybrid

| Approach | How it works | Pros | Cons |
| --- | --- | --- | --- |
| **Keyword (BM25)** | Inverted index + TF-IDF/BM25 scoring | Exact term matching, fast, predictable | Searching "car" won't find "automobile" |
| **Semantic (vector)** | Converts text into embedding vectors → cosine similarity | Meaning-based, handles synonyms/multiple languages | Weak at exact proper-noun/code search |
| **Hybrid** | Combines keyword + vector results (RRF, etc.) | Combines the strengths of both | Increased complexity, requires tuning |

For vector search details, see [Vector Store](../../ai/vector-store/).

### Technology lineage

```
Apache Lucene (search engine library)
  ├─ Apache Solr (2004~, standalone search server)
  └─ Elasticsearch (2010~, distributed search + analytics)
       └─ OpenSearch (2021~, AWS fork, Apache 2.0 license)
```

- **Solr**: Still used, but there are almost no cloud-managed offerings. Often remains in on-premises legacy systems
- **Elasticsearch**: Elastic changed its license (SSPL). Offered as managed via Elastic Cloud
- **OpenSearch**: Forked by AWS. The mainstream managed option in the cloud. A similar story to Valkey (license issue → open-source fork)

### Why log analytics is really "search"

The core of log analytics is **finding patterns in large volumes of unstructured text**. Because full-text search engines (inverted indexes) are well suited to this task, the ELK/EFK stack (Elasticsearch + Logstash/Fluentd + Kibana) has become the de facto standard for log analytics.

### Summary of search types

"Search" uses entirely different services depending on the purpose.

| Type | Purpose | Representative technology |
| --- | --- | --- |
| **Full-text search** | Text keyword matching, morphological analysis | Elasticsearch/OpenSearch, Solr |
| **Vector search** (semantic) | Meaning-based similarity search (AI/RAG) | Vector DB, pgvector |
| **Log analytics** | Collecting, searching, and visualizing large volumes of logs | OpenSearch, Loki, BigQuery |

This document focuses on full-text search and log analytics.

## Comparison of vendor services

| Vendor | Full-text search | AI search (hybrid) | Log analytics |
| --- | --- | --- | --- |
| AWS | [OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) | OpenSearch + k-NN | [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/) |
| Azure | [Azure AI Search](https://learn.microsoft.com/azure/search/) | AI Search (vector + keyword + semantic) | [Log Analytics](https://learn.microsoft.com/azure/azure-monitor/logs/data-platform-logs) |
| Google Cloud | — (Firestore full-text search is limited) | [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs) | [Cloud Logging](https://cloud.google.com/logging/docs) + [BigQuery](https://cloud.google.com/bigquery/docs) |
| OCI | [OCI Search with OpenSearch](https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm) | OpenSearch + k-NN | [OCI Logging Analytics](https://docs.oracle.com/en-us/iaas/logging-analytics/home.htm) |

## What to choose when

| Requirement | Recommendation |
| --- | --- |
| Product catalog search (keyword + filters) | OpenSearch, Azure AI Search |
| AI-based question answering (RAG) | [Vector Store](../../ai/vector-store/) + hybrid search |
| Large-scale log search + dashboards | OpenSearch (Dashboards), Log Analytics, Cloud Logging |
| Cost-minimized long-term log retention + querying | S3 + Athena, BigQuery, OCI Object Storage + Logging Analytics |
| Multilingual and CJK morphological analysis needed | OpenSearch (nori, kuromoji plugins), Azure AI Search (language-specific analyzers) |

## Common mistakes

- **Trying to replace full-text search with the RDB's LIKE search** — As data grows, this causes performance to degrade sharply due to full table scans. Adopt a search engine if you need full-text search.
- **Setting an excessive number of shards** — In OpenSearch/Elasticsearch, too many shards increases cluster overhead. Design around 10–50GB per shard.
- **Setting log retention to unlimited** — Permanently storing all logs in a search engine causes storage cost to explode. Use hot/warm/cold tiers and move older logs to object storage.

## Checklist

- [ ] Have you defined your search requirements (keyword/semantic/hybrid) and chosen a suitable service?
- [ ] Have you set an index lifecycle management (ILM) policy and log retention period?
- [ ] If multilingual or CJK search is needed, have you configured an appropriate morphological analyzer (nori, kuromoji, etc.)?

## References

### AWS

- [Amazon OpenSearch Service documentation](https://docs.aws.amazon.com/opensearch-service/)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/)

### Azure

- [Azure AI Search documentation](https://learn.microsoft.com/azure/search/)
- [Log Analytics documentation](https://learn.microsoft.com/azure/azure-monitor/logs/data-platform-logs)

### Google Cloud

- [Vertex AI Search documentation](https://cloud.google.com/generative-ai-app-builder/docs)
- [Cloud Logging documentation](https://cloud.google.com/logging/docs)

### OCI

- [OCI Search with OpenSearch](https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm)
- [OCI Logging Analytics](https://docs.oracle.com/en-us/iaas/logging-analytics/home.htm)
