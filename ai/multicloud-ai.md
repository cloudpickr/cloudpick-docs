---
description: 멀티클라우드 AI 아키텍처 패턴, RAG 파이프라인, GPU 가용성을 벤더별로 비교합니다.
---

# 멀티클라우드 AI 아키텍처

> 문서 기준: 2026년 5월

{% hint style="info" %}
이 문서는 심화 내용입니다. AI 서비스 비교가 처음이라면 [클라우드 AI 시작하기](getting-started.md)와 [AI와 머신러닝 서비스](ai-ml.md)를 먼저 읽는 것을 권장합니다.
{% endhint %}

## 왜 멀티클라우드 AI인가

각 클라우드 벤더는 AI/ML 영역에서 서로 다른 강점을 가지고 있습니다. 단일 벤더에 종속되지 않고 워크로드 특성에 맞는 최적의 서비스를 조합하면 비용, 성능, 모델 다양성 측면에서 이점을 얻을 수 있습니다.

| 벤더 | 주요 AI 플랫폼 | 강점 |
| --- | --- | --- |
| AWS | [Amazon Bedrock](https://aws.amazon.com/bedrock/), [Amazon SageMaker AI](https://aws.amazon.com/sagemaker/ai/) | 자체 **Amazon Nova** 모델 + Anthropic/OpenAI/Meta/Mistral/NVIDIA 등 최대 규모 모델 카탈로그, 자체 AI 칩(Trainium/Inferentia) |
| Azure | [Azure OpenAI / Microsoft Foundry](https://azure.microsoft.com/products/ai-services/openai-service) | OpenAI GPT 시리즈 주력, Microsoft 365/GitHub/Power Platform 통합, 엔터프라이즈 보안 |
| GCP | [Vertex AI](https://cloud.google.com/vertex-ai), [Gemini](https://cloud.google.com/gemini) | 자체 **Gemini 2.5** 네이티브 멀티모달, TPU 인프라, BigQuery/Search 통합 |
| OCI | [OCI Generative AI](https://docs.oracle.com/iaas/Content/generative-ai/home.htm), [OCI AI Services](https://www.oracle.com/artificial-intelligence/ai-services/) | Cohere/Llama/Grok 제공, **Dedicated AI Cluster** (RDMA 기반 전용 GPU 클러스터, 다른 테넌트와 공유 없음), Oracle DB 네이티브 벡터 검색 통합, 이그레스 10TB 무료로 멀티클라우드 AI 파이프라인에 유리 |

## GPU 가용성

AI 학습 및 추론에 필수적인 GPU 인스턴스를 주요 CSP별로 비교합니다.

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| A100 인스턴스 | [p4d.24xlarge](https://aws.amazon.com/ec2/instance-types/p4/) (8×A100 40/80GB) | [ND A100 v4](https://learn.microsoft.com/en-us/azure/virtual-machines/nda100-v4-series) (8×A100 80GB) | [a2-highgpu-8g](https://cloud.google.com/compute/docs/gpus#a100-gpus) (8×A100 80GB) | [BM.GPU.A100-v2.8](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) (8×A100 80GB) |
| H100 인스턴스 | [p5.48xlarge](https://aws.amazon.com/ec2/instance-types/p5/) (8×H100 80GB) | [ND H100 v5](https://learn.microsoft.com/en-us/azure/virtual-machines/nd-h100-v5-series) (8×H100 80GB) | [a3-highgpu-8g](https://cloud.google.com/compute/docs/gpus#h100-gpus) (8×H100 80GB) | [BM.GPU.H100.8](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) (8×H100 80GB) |
| 예약 옵션 | Reserved Instances, Savings Plans | Reserved VM Instances | CUD (Committed Use Discount) | Capacity Reservation |
| 스팟/선점형 | Spot Instances | Spot VMs | Spot VMs (Preemptible) | Preemptible Instances |

{% hint style="warning" %}
GPU 인스턴스 가격은 리전, 약정 기간, 가용성에 따라 크게 달라집니다. 최신 가격은 각 벤더의 가격 계산기를 참조하세요.
{% endhint %}

## RAG 파이프라인

RAG(Retrieval-Augmented Generation) 파이프라인은 Vector DB, Embedding 모델, LLM의 조합으로 구성됩니다. 각 벤더별 주요 구성 요소를 비교합니다.

| 구성 요소 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| Vector DB | [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/serverless-vector-engine/), [Amazon Aurora pgvector](https://aws.amazon.com/about-aws/whats-new/2023/07/amazon-aurora-postgresql-pgvector-vector-storage-similarity-search/) | [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search), [Azure Cosmos DB (vCore)](https://learn.microsoft.com/en-us/azure/cosmos-db/vector-search) | [Vertex AI Vector Search](https://cloud.google.com/vertex-ai/docs/vector-search/overview), [AlloyDB](https://cloud.google.com/alloydb/docs/ai/work-with-embeddings) | [OCI Search with OpenSearch](https://www.oracle.com/cloud/search/), [Oracle Database 23ai](https://www.oracle.com/database/23ai/) |
| Embedding | [Amazon Titan Embeddings](https://aws.amazon.com/bedrock/titan/) (Bedrock) | [text-embedding-ada-002](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models) (Azure OpenAI) | [text-embedding-005](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings) (Vertex AI) | [Cohere Embed](https://docs.oracle.com/en-us/iaas/Content/generative-ai/embed-models.htm) (OCI Generative AI) |
| LLM | Bedrock (Amazon Nova, Claude, OpenAI GPT-OSS, Llama, Mistral 등) | Azure OpenAI / Foundry (GPT-5 시리즈, Claude, Llama 등) | Vertex AI (Gemini 2.5, Claude, Llama 등) | OCI Generative AI (Cohere, Llama, Grok 등) |
| 오케스트레이션 | [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) | [Azure AI Studio](https://azure.microsoft.com/en-us/products/ai-studio) | [Vertex AI RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview) | [OCI Generative AI Agents](https://www.oracle.com/artificial-intelligence/generative-ai/agents/) |

## 아키텍처 선택 패턴

| 패턴 | 설명 | 적합한 경우 |
| --- | --- | --- |
| 단일 CSP AI 플랫폼 | 한 클라우드의 모델, 데이터, 배포 도구를 모두 사용 | 운영 단순성이 가장 중요할 때 |
| 모델 분산 | 모델은 여러 CSP의 API를 쓰고, 애플리케이션은 한 곳에서 운영 | 모델 품질과 비용을 비교하며 선택해야 할 때 |
| 데이터 근접형 | 데이터가 있는 클라우드에서 임베딩·검색·추론을 수행 | 데이터 이동 비용이나 규제가 중요할 때 |
| 중앙 RAG 플랫폼 | 하나의 공통 RAG 계층에서 여러 CSP 모델을 호출 | 조직 전체에 공통 AI 플랫폼을 제공할 때 |

## 설계 시 주의사항

- **데이터 이동 비용** — 대량 문서, 임베딩, 로그를 클라우드 간 이동하면 이그레스 비용이 커질 수 있습니다.
- **데이터 주권** — 개인정보, 금융 데이터, 의료 데이터는 저장 위치와 처리 위치를 명확히 해야 합니다.
- **모델 의존성** — 특정 모델의 API 형식, 토큰 제한, 함수 호출 방식에 종속되지 않도록 추상화 계층을 둡니다.
- **관측 가능성** — 프롬프트, 응답, 토큰 사용량, 지연 시간, 비용을 함께 모니터링합니다.
- **보안** — 프롬프트 인젝션, 민감정보 유출, 과도한 에이전트 권한을 통제해야 합니다.

{% hint style="info" %}
멀티클라우드 AI는 모든 벤더를 동시에 쓰는 것이 목표가 아닙니다. 데이터 위치, 모델 품질, 비용, 규제 요구사항에 따라 필요한 조합만 선택하는 것이 핵심입니다.
{% endhint %}

## 참고하기

### AWS

- [Amazon Bedrock 문서](https://docs.aws.amazon.com/bedrock/)
- [Amazon SageMaker AI 문서](https://docs.aws.amazon.com/sagemaker/)

### Azure

- [Azure AI Services 문서](https://learn.microsoft.com/en-us/azure/ai-services/)
- [Azure OpenAI Service 문서](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

### GCP

- [Vertex AI 문서](https://cloud.google.com/vertex-ai/docs)
- [Gemini API 문서](https://cloud.google.com/gemini/docs)

### OCI

- [OCI AI Services 문서](https://www.oracle.com/artificial-intelligence/ai-services/)
- [OCI Generative AI 문서](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)
