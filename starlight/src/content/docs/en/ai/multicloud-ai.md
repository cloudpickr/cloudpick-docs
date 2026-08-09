---
title: Multicloud AI
description: Multicloud AI architecture patterns, RAG pipelines, and GPU availability compared across vendors.
---

> Document baseline: August 2026 | This is a fast-changing area subject to quarterly review.

:::note
This is advanced content. If new to AI service comparison, read [Getting Started with AI](../../ai/getting-started/) and [AI Platforms](../../ai/ai-ml/) first.
:::

## Why Multicloud AI

Each cloud vendor has distinct AI/ML strengths. Combining services matched to workload characteristics — without single-vendor lock-in — yields benefits in cost, performance, and model diversity.

- **AWS** — Bedrock/SageMaker AI. Largest model catalog + custom AI chips (Trainium/Inferentia)
- **Azure** — Microsoft Foundry. OpenAI GPT series primary + Microsoft ecosystem integration
- **Google Cloud** — Gemini Enterprise Agent Platform. Native Gemini multimodal + TPU infrastructure
- **OCI** — OCI Enterprise AI. Dedicated AI Clusters (RDMA GPU) + 10TB egress free

:::note
For a detailed comparison of each vendor's AI platform, model catalog, and fine-tuning options, see [AI Platforms](../../ai/ai-ml/).
:::

## GPU Availability

GPU instances essential for AI training and inference are compared across major CSPs.

### NVIDIA GPU Generation Comparison

| Spec | H100 (Hopper) | H200 (Hopper) | B200 (Blackwell) | GB200 (Blackwell) |
| --- | --- | --- | --- | --- |
| **Memory** | 80GB HBM3 | 141GB HBM3e | 192GB HBM3e | 384GB (2×192GB) |
| **Bandwidth** | 3.35 TB/s | 4.8 TB/s | 8.0 TB/s | 16 TB/s (Superchip) |
| **NVLink** | 900 GB/s | 900 GB/s | 1.8 TB/s | NVL72 domain |
| **TDP** | 700W | 700W | 1000W | 1200W (Superchip) |
| **Best for** | General training/inference | Large inference, long context | Next-gen training | Trillion-parameter frontier models |
| **Memory (vs H100)** | 1× | ~1.8× | ~2.4× | ~4.8× (2×B200 combined) |

:::note
Inference throughput (tokens/sec, etc.) varies widely by model, precision, batch size, framework, and system configuration. Benchmark multiples such as "n× vs H100" are tied to specific conditions in vendor-published materials, so check the [NVIDIA datasheets](https://www.nvidia.com/en-us/data-center/) and each CSP's instance documentation before adopting.
:::

**Selection guide:**
- **H100/H200** — Relatively wide region availability. Suited to mid-scale training, fine-tuning, and general inference. H200 shares the same architecture family as H100 but has more memory and bandwidth, favoring long-context inference.
- **B200** — A leading candidate for the 2026 flagship generation. Greater memory and bandwidth than H100, with native FP4 support tending to improve quantized-inference efficiency. Actual throughput should be measured per workload.
- **GB200 NVL72** — Combines Grace CPU + B200 GPU into a Superchip. Links many GPUs in a single NVLink domain for training extremely large models. Region availability and commitment capacity can be limited.

:::note
Most enterprise AI workloads (RAG inference, fine-tuning, mid-scale training) are well served by **H100/H200**. Choose the minimum GPU tier matching your workload — higher generations have limited region availability and harder reservation.
:::

### Vendor GPU Instances

| GPU | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **B200** | P6-B200 (8×B200) | ND GB200-v6 | A4 (8×B200) | BM.GPU.B200.8 |
| **GB200 NVLink** | P6e-GB200 UltraServer (up to 72) | ND GB200-v6 (NVLink) | A4X (GB200 NVL72) | — |
| **H100** | p5.48xlarge (8×H100) | ND H100 v5 (8×H100) | a3-highgpu-8g (8×H100) | BM.GPU.H100.8 |
| **A100** | p4d.24xlarge (8×A100) | ND A100 v4 (8×A100) | a2-highgpu-8g (8×A100) | BM.GPU.A100-v2.8 |
| **RTX PRO / Inference-Optimized** | G7 (NVIDIA RTX PRO 4500 Blackwell) | — | — | — |
| **Custom AI Chips** | Trainium2, Inferentia2 | Maia 100 | TPU v8 | — |
| **Reserved Options** | Reserved Instances, Savings Plans | Reserved VM Instances | CUD (Committed Use Discount) | Capacity Reservation |
| **Spot/Preemptible** | Spot Instances | Spot VMs | Spot VMs | Preemptible Instances |

:::caution
GPU instance pricing varies significantly by region, commitment term, and availability. Check each vendor's pricing calculator for current rates.
:::

:::note
**Confidential AI inference:** If model IP or sensitive input data must be protected even while being processed, **confidential computing GPUs** (Azure NCC H100 v5, GCP A3 Confidential VM) are an option. For a vendor comparison of confidential computing, see [Data Protection — Confidential Computing](../../security/data-protection/#confidential-computing).
:::

## RAG Pipeline Services

| Vendor | Vector Search | Embedding | Managed RAG |
| --- | --- | --- | --- |
| **AWS** | OpenSearch Serverless | Titan Embeddings | Bedrock Knowledge Bases |
| **Azure** | AI Search | Microsoft Foundry | AI Search + Foundry |
| **Google Cloud** | Vertex AI Vector Search | Gemini Embedding | RAG Engine |
| **OCI** | OCI Search / Oracle 23ai | Cohere Embed | Enterprise AI Agents |

:::note
For RAG implementation patterns (hybrid search, chunking, re-ranking, orchestration), see [Advanced RAG Patterns](../../ai/rag-patterns/).
:::

## Architecture Selection Patterns

| Pattern | Description | When to Use |
| --- | --- | --- |
| Single CSP AI Platform | Use one cloud's models, data, and deployment tools | Operational simplicity is top priority |
| Model Distribution | Use multiple CSP APIs; application runs in one place | Need to compare model quality and cost |
| Data Proximity | Embed/search/infer where the data lives | Data movement cost or regulation matters |
| Central RAG Platform | Common RAG layer calling multiple CSP models | Org-wide shared AI platform needed |

## Design Considerations

- **Data movement costs** — Moving large documents, embeddings, and logs between clouds incurs egress charges.
- **Data sovereignty** — PII, financial, and health data require clear storage/processing location boundaries.
- **Model dependency** — Avoid coupling to specific vendor API formats, token limits, or function-calling conventions. Add an abstraction layer.
- **Observability** — Monitor prompts, responses, token usage, latency, and cost together.
- **Security** — Control prompt injection, sensitive data exfiltration, and excessive agent permissions.

:::note
Multicloud AI is not about using every vendor simultaneously. The goal is selecting only the combinations needed based on data location, model quality, cost, and regulatory requirements.
:::

## Common Mistakes

- **Adopting all vendors' AI services at once** — Multicloud AI means selecting needed combinations, not running everything in parallel. Ops complexity and cost explode.
- **Not estimating data movement costs upfront** — Embeddings, documents, and logs crossing clouds incur larger-than-expected egress fees.
- **Direct coupling to model API formats** — Without an abstraction layer, model/vendor swaps become extremely difficult.

## Checklist

- [ ] Clearly defined rationale for multicloud AI (model quality, cost, regulation)
- [ ] Estimated data movement costs (egress) and evaluated data-proximity architecture
- [ ] Abstraction layer (LangChain, etc.) in place for vendor-swappable model calls

## References

### AWS
- [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Amazon SageMaker AI](https://docs.aws.amazon.com/sagemaker/)

### Azure
- [Azure AI Services](https://learn.microsoft.com/en-us/azure/ai-services/)
- [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

### Google Cloud
- [Vertex AI](https://cloud.google.com/vertex-ai/docs)
- [Gemini API](https://cloud.google.com/gemini/docs)

### OCI
- [OCI AI Services](https://www.oracle.com/artificial-intelligence/ai-services/)
- [OCI Enterprise AI](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)
