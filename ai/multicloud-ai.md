# 멀티클라우드 AI 아키텍처

## 왜 멀티클라우드 AI인가

각 클라우드 벤더는 AI/ML 영역에서 서로 다른 강점을 가지고 있습니다. 단일 벤더에 종속되지 않고 워크로드 특성에 맞는 최적의 서비스를 조합하면 비용, 성능, 모델 다양성 측면에서 이점을 얻을 수 있습니다.

| 벤더 | 주요 AI 플랫폼 | 강점 |
| --- | --- | --- |
| AWS | [Amazon Bedrock](https://aws.amazon.com/bedrock/), [Amazon SageMaker](https://aws.amazon.com/sagemaker/) | 다양한 파운데이션 모델 선택지 (Anthropic, Meta, Mistral 등), 엔드투엔드 ML 파이프라인 |
| Azure | [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service) | OpenAI 모델 독점 호스팅 (GPT-4o, o1 등), 엔터프라이즈 보안 통합 |
| GCP | [Vertex AI](https://cloud.google.com/vertex-ai), [Gemini](https://cloud.google.com/gemini) | 자체 Gemini 모델, TPU 인프라, 멀티모달 강점 |
| OCI | [OCI AI Services](https://www.oracle.com/artificial-intelligence/ai-services/) | Oracle DB 네이티브 통합, 가격 경쟁력 |

## GPU 가용성

AI 학습 및 추론에 필수적인 GPU 인스턴스를 4사별로 비교합니다.

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| A100 인스턴스 | [p4d.24xlarge](https://aws.amazon.com/ec2/instance-types/p4/) (8×A100 40/80GB) | [ND A100 v4](https://learn.microsoft.com/en-us/azure/virtual-machines/nda100-v4-series) (8×A100 80GB) | [a2-highgpu-8g](https://cloud.google.com/compute/docs/gpus#a100-gpus) (8×A100 80GB) | [BM.GPU.A100-v2.8](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) (8×A100 80GB) |
| H100 인스턴스 | [p5.48xlarge](https://aws.amazon.com/ec2/instance-types/p5/) (8×H100 80GB) | [ND H100 v5](https://learn.microsoft.com/en-us/azure/virtual-machines/nd-h100-v5-series) (8×H100 80GB) | [a3-highgpu-8g](https://cloud.google.com/compute/docs/gpus#h100-gpus) (8×H100 80GB) | [BM.GPU.H100.8](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) (8×H100 80GB) |
| 예약 옵션 | Reserved Instances, Savings Plans | Reserved VM Instances | CUD (Committed Use Discount) | Capacity Reservation |
| 스팟/선점형 | Spot Instances | Spot VMs | Spot VMs (Preemptible) | Preemptible Instances |

> **참고**: GPU 인스턴스 가격은 리전, 약정 기간, 가용성에 따라 크게 달라집니다. 최신 가격은 각 벤더의 가격 계산기를 참조하세요.

## RAG 파이프라인

RAG(Retrieval-Augmented Generation) 파이프라인은 Vector DB, Embedding 모델, LLM의 조합으로 구성됩니다. 각 벤더별 주요 구성 요소를 비교합니다.

| 구성 요소 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| Vector DB | [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/serverless-vector-engine/), [Amazon Aurora pgvector](https://aws.amazon.com/about-aws/whats-new/2023/07/amazon-aurora-postgresql-pgvector-vector-storage-similarity-search/) | [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search), [Azure Cosmos DB (vCore)](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/vector-search) | [Vertex AI Vector Search](https://cloud.google.com/vertex-ai/docs/vector-search/overview), [AlloyDB](https://cloud.google.com/alloydb/docs/ai/work-with-embeddings) | [OCI Search with OpenSearch](https://www.oracle.com/cloud/search/), [Oracle Database 23ai](https://www.oracle.com/database/23ai/) |
| Embedding | [Amazon Titan Embeddings](https://aws.amazon.com/bedrock/titan/) (Bedrock) | [text-embedding-ada-002](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models) (Azure OpenAI) | [text-embedding-005](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings) (Vertex AI) | [Cohere Embed](https://docs.oracle.com/en-us/iaas/Content/generative-ai/embed-models.htm) (OCI Generative AI) |
| LLM | Bedrock (Claude, Llama 등) | Azure OpenAI (GPT-4o, o1) | Vertex AI (Gemini, Claude) | OCI Generative AI (Cohere, Llama) |
| 오케스트레이션 | [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) | [Azure AI Studio](https://azure.microsoft.com/en-us/products/ai-studio) | [Vertex AI RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview) | [OCI Generative AI Agents](https://www.oracle.com/artificial-intelligence/generative-ai/agents/) |

## 참고하기

| 벤더 | 공식 AI 문서 |
| --- | --- |
| AWS | [Amazon Bedrock 문서](https://docs.aws.amazon.com/bedrock/), [Amazon SageMaker 문서](https://docs.aws.amazon.com/sagemaker/) |
| Azure | [Azure AI Services 문서](https://learn.microsoft.com/en-us/azure/ai-services/), [Azure OpenAI Service 문서](https://learn.microsoft.com/en-us/azure/ai-services/openai/) |
| GCP | [Vertex AI 문서](https://cloud.google.com/vertex-ai/docs), [Gemini API 문서](https://cloud.google.com/gemini/docs) |
| OCI | [OCI AI Services 문서](https://docs.oracle.com/en-us/iaas/Content/ai/home.htm), [OCI Generative AI 문서](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm) |
