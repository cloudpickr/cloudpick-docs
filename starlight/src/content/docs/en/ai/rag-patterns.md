---
title: Advanced RAG Patterns
description: Limitations of basic RAG and advanced patterns including chunking, re-ranking, and query expansion based on vendor guides.
---

> Document baseline: July 2026 | This is a fast-changing area subject to quarterly review.

:::note
For RAG basics, read the RAG section in [Getting Started](../../ai/getting-started/) and [Vector Stores and Embeddings](../../ai/vector-store/) first.
:::

## Limitations of Basic RAG

Simply "document → embedding → retrieve → pass to LLM" is insufficient for production quality. Common problems cited by Azure and AWS official guides:

- **Poor chunking** breaks context, degrading retrieval quality.
- **Without re-ranking**, the LLM references irrelevant context from retrieved results.
- **Ambiguous user queries** (pronouns, abbreviations) defeat vector search alone.

Sources:
- [Azure — Develop a RAG Solution: Chunking Phase](https://learn.microsoft.com/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [AWS — Writing best practices to optimize RAG applications](https://docs.aws.amazon.com/prescriptive-guidance/latest/writing-best-practices-rag/introduction.html)

## Chunking Strategies

How much and how documents are split determines retrieval quality.

### Chunking Methods

| Method | Description | Best For |
| --- | --- | --- |
| **Fixed-size** | Split at fixed token count (e.g., 512) | General text, blogs |
| **Sentence-based** | Split by sentence boundaries | Natural language documents |
| **Recursive** | Hierarchical: paragraph → sentence → word | Structured documents |
| **Semantic** | Group semantically similar sentences | Long explanatory text |
| **Document-structure** | Split by headings/sections | Manuals, wikis, technical docs |

Azure recommends trying `Fixed-size` → `Recursive` → `Document-structure` in order of increasing sophistication (see the [Chunking Phase guide](https://learn.microsoft.com/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)).

### Chunk Size Guide

- **Too small** — Insufficient context; retrieved fragments lose meaning.
- **Too large** — Multiple topics in one chunk degrades precision; increases token consumption.

General starting point (Azure guide):
- Chunk size: **500–1500 tokens**
- Overlap: 10–20% between chunks to prevent context loss

:::note
Chunk size is never "set and forget." Measure retrieval quality with representative queries and adjust iteratively.
:::

### Vendor Chunking Options

| Vendor | Supported Methods | Reference |
| --- | --- | --- |
| AWS Bedrock Knowledge Bases | Default, fixed-size, hierarchical, semantic | [KB Chunking Options](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html) |
| Azure AI Search | Auto-chunking with integrated vectorization, customizable | [Azure AI Search Chunking](https://learn.microsoft.com/azure/search/vector-search-how-to-chunk-documents) |
| Vertex AI RAG Engine | Chunk size/overlap configuration | [RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview) |

### Managed RAG Pipelines

Instead of building chunking, embedding, retrieval, and re-ranking yourself, **managed services** handle the entire pipeline.

| Vendor | Service | Strengths |
| --- | --- | --- |
| AWS | [Bedrock Managed Knowledge Base](https://aws.amazon.com/bedrock/knowledge-bases/) | Native data connectors, Smart Parsing (automatic multi-format parsing), Agentic Retriever (agent decomposes and searches complex multi-step queries). AgentCore Gateway integration |
| Azure | [Azure AI Search + Foundry](https://learn.microsoft.com/azure/search/) | Integrated vectorization, built-in semantic ranker, custom skill pipeline |
| Google Cloud | [Vertex AI RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview) | Source → embedding → retrieval unified |

:::note
Managed RAG is ideal for rapid prototyping. For fine-grained control over chunking logic or search algorithms, custom builds may be preferable.
:::

## Re-ranking

Vector search is fast but doesn't rank by true relevance. **Re-ranking** re-scores the top-N results with a separate model.

```mermaid
graph LR
    Q[Query] --> V[Vector Search<br/>Top 50]
    V --> R[Re-ranker<br/>Relevance Re-score]
    R --> T[Top 5]
    T --> L[LLM]
```

### Vendor Re-ranking Services

| Vendor | Service | Reference |
| --- | --- | --- |
| AWS | Bedrock Knowledge Bases Reranker (Amazon Rerank, Cohere Rerank) | [Reranker Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-reranker.html) |
| Azure | Azure AI Search Semantic Ranker | [Semantic Ranker](https://learn.microsoft.com/azure/search/semantic-search-overview) |
| Google Cloud | Vertex AI Ranking API | [Ranking API](https://cloud.google.com/generative-ai-app-builder/docs/ranking) |
| OCI | Cohere Rerank (OCI Enterprise AI) | [OCI Enterprise AI Models](https://docs.oracle.com/en-us/iaas/Content/generative-ai/pretrained-models.htm) |

## Hybrid Search

Vector search is weak at exact string matching (product codes like `SKU-12345`, proper nouns). **Hybrid search** combines vector search with traditional keyword search (BM25).

| Vendor | Hybrid Approach | Reference |
| --- | --- | --- |
| AWS | OpenSearch Vector + BM25 (RRF algorithm) | [Hybrid Search](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn-retrieval.html) |
| Azure | Azure AI Search hybrid query | [Hybrid Search](https://learn.microsoft.com/azure/search/hybrid-search-overview) |
| Google Cloud | Vertex AI Search (auto hybrid) | [Vertex AI Search](https://cloud.google.com/enterprise-search) |
| OCI | OCI AI Vector Search with SQL combination | [OCI AI Vector Search](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/oracle-ai-vector-search-autonomous-database.html) |

## Query Expansion and Transformation

When user queries are short or ambiguous, use an LLM to rewrite or expand the query.

- **Query Rewriting** — Resolve pronouns/abbreviations explicitly (e.g., "that" → "policy X discussed in the last meeting").
- **Multi-Query** — Generate multiple query versions and search each.
- **HyDE (Hypothetical Document Embeddings)** — LLM generates a hypothetical answer, then embeds that answer for retrieval.

Official guides:
- [Azure — Enrichment Phase of RAG](https://learn.microsoft.com/azure/architecture/ai-ml/guide/rag/rag-enrichment-phase)
- [AWS — RAG Optimization Guide](https://docs.aws.amazon.com/prescriptive-guidance/latest/writing-best-practices-rag/introduction.html)

## Evaluation

RAG systems require measuring **retrieval quality** and **response quality** separately.

### Retrieval Quality Metrics

| Metric | Meaning |
| --- | --- |
| **Recall@K** | Fraction of relevant docs in top-K results |
| **MRR** (Mean Reciprocal Rank) | Average reciprocal rank of correct document |
| **NDCG** | Ranking quality with position-weighted scoring |

### Response Quality Metrics

| Metric | Meaning |
| --- | --- |
| **Faithfulness** | Is the generated answer grounded in retrieved documents? |
| **Answer Relevance** | Does the answer actually address the question? |
| **Context Precision/Recall** | How accurate and sufficient is the retrieved context? |

### Evaluation Tools

| Tool | Description |
| --- | --- |
| [RAGAS](https://github.com/explodinggradients/ragas) | Open-source RAG evaluation framework |
| [Azure AI Evaluation SDK](https://learn.microsoft.com/azure/ai-studio/how-to/develop/evaluate-sdk) | Built-in Faithfulness, Relevance metrics |
| [Bedrock Evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html) | Integrated model/RAG evaluation |
| [Vertex AI Evaluation Service](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview) | Gen AI evaluation framework |

## Common Mistakes

- **Setting chunk size once and never adjusting** — Without measuring retrieval quality on representative queries, chunks may be too fragmented or mixed-topic.
- **Passing vector search results directly to LLM without re-ranking** — Irrelevant docs in top results cause hallucinations.
- **Not considering hybrid search** — Product codes and proper nouns requiring exact string matching won't be found by vector search alone.

## Checklist

- [ ] Chunk size and overlap tuned by measuring retrieval quality with representative queries
- [ ] Re-ranking (Semantic Ranker, Cohere Rerank, etc.) applied to improve result accuracy
- [ ] RAG evaluation metrics (Faithfulness, Answer Relevance) measured regularly

## References

### AWS
- [RAG Options and Architectures](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html)
- [Writing Best Practices to Optimize RAG Applications](https://docs.aws.amazon.com/prescriptive-guidance/latest/writing-best-practices-rag/introduction.html)
- [Bedrock Knowledge Bases Chunking](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html)
- [Bedrock Knowledge Bases Reranker](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-reranker.html)

### Azure
- [Design and Develop a RAG Solution](https://learn.microsoft.com/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)
- [RAG Chunking Phase](https://learn.microsoft.com/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [Azure AI Search Hybrid Search](https://learn.microsoft.com/azure/search/hybrid-search-overview)
- [Azure AI Search Semantic Ranker](https://learn.microsoft.com/azure/search/semantic-search-overview)

### Google Cloud
- [Vertex AI RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview)
- [Vertex AI Ranking API](https://cloud.google.com/generative-ai-app-builder/docs/ranking)
- [Vertex AI Evaluation Service](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)

### OCI
- [OCI AI Vector Search](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/oracle-ai-vector-search-autonomous-database.html)
- [OCI Enterprise AI Models](https://docs.oracle.com/en-us/iaas/Content/generative-ai/pretrained-models.htm)
