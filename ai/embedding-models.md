---
description: 임베딩 모델의 차원, 다국어 지원, 비용을 기준으로 선택하는 가이드입니다.
---

# 임베딩 모델 선택 가이드

> 문서 기준: 2026년 5월

{% hint style="info" %}
임베딩과 벡터 스토어 기초는 [벡터 스토어와 AI 데이터](vector-store.md)를 먼저 참고하세요. 이 문서는 임베딩 모델 선택이라는 한 가지 주제에 집중합니다.
{% endhint %}

## 왜 임베딩 모델 선택이 중요한가

RAG, 시맨틱 검색, 추천 시스템의 성능은 임베딩 모델의 품질에 크게 좌우됩니다. 같은 데이터와 같은 벡터 스토어를 써도 임베딩 모델에 따라 검색 정확도와 비용이 크게 달라집니다.

선택 시 고려할 항목:

- **차원** — 품질 vs 저장 공간/검색 속도
- **다국어 지원** — 한국어 포함 언어 처리 품질
- **도메인** — 범용 vs 특정 분야 특화
- **비용** — API 호출 기반, 1M 토큰당 과금
- **출력 크기 조정** — 차원 축소 지원 여부

## 벤더별 주요 임베딩 모델

### AWS Bedrock

| 모델 | 차원 | 특징 | 참고 |
| --- | --- | --- | --- |
| Amazon Titan Embeddings G1 - Text | 1536 | 범용 텍스트 임베딩 | [문서](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) |
| Amazon Titan Text Embeddings V2 | 256/512/1024 | 차원 선택 가능, 정규화 옵션 | [문서](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) |
| Amazon Titan Multimodal Embeddings G1 | 256/384/1024 | 텍스트 + 이미지 | [문서](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-multiemb-models.html) |
| Cohere Embed 3 (English) | 1024 | 영어 특화, 고품질 | [문서](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed.html) |
| Cohere Embed 3 (Multilingual) | 1024 | 100+ 언어 | [문서](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed.html) |

### Azure OpenAI

| 모델 | 차원 | 특징 | 참고 |
| --- | --- | --- | --- |
| text-embedding-3-small | 1536 (최대) | 저비용, 기본 품질 | [문서](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#embeddings) |
| text-embedding-3-large | 3072 (최대) | 최고 품질 | [문서](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#embeddings) |
| text-embedding-ada-002 | 1536 | 이전 세대 (호환성용) | [문서](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#embeddings) |

text-embedding-3 시리즈는 **Matryoshka Representation** 를 지원하여 `dimensions` 파라미터로 차원을 축소해도 품질 저하가 적습니다.

### Google Cloud Vertex AI

| 모델 | 차원 | 특징 | 참고 |
| --- | --- | --- | --- |
| text-embedding-005 (gecko) | 768 | 영어 중심 최신 버전 | [문서](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings) |
| text-multilingual-embedding-002 | 768 | 다국어 (한국어 포함) | [문서](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings) |
| multimodalembedding@001 | 128/256/512/1408 | 텍스트 + 이미지 + 비디오 | [문서](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings) |

### OCI Generative AI

| 모델 | 차원 | 특징 | 참고 |
| --- | --- | --- | --- |
| cohere.embed-english-v3.0 | 1024 | 영어 특화 | [문서](https://docs.oracle.com/en-us/iaas/Content/generative-ai/embed-models.htm) |
| cohere.embed-multilingual-v3.0 | 1024 | 100+ 언어 | [문서](https://docs.oracle.com/en-us/iaas/Content/generative-ai/embed-models.htm) |

## 선택 가이드

### 언어 요건에 따라

| 주요 언어 | 권장 모델 |
| --- | --- |
| 영어만 | text-embedding-3-large (Azure), Cohere Embed 3 English |
| 한국어 포함 다국어 | Cohere Embed Multilingual, text-multilingual-embedding-002 (Google Cloud), Titan Text Embeddings V2 |
| 일본어/중국어 포함 | Cohere Embed Multilingual (지원 언어 공식 목록 확인) |

### 사용 규모에 따라

| 규모 | 권장 방향 |
| --- | --- |
| 프로토타입/소규모 (수만 건 이하) | 기본 품질 모델 + 1536/1024차원 |
| 중규모 (수십만\~수백만 건) | 차원 축소 모델 (text-embedding-3-small with dimensions=512 등) |
| 대규모 (수천만 건 이상) | 저차원 모델 + 양자화(Quantization) |

{% hint style="info" %}
차원이 높을수록 품질은 올라가지만 저장 공간, 검색 속도, 비용이 모두 증가합니다. 대부분의 프로덕션에서는 **512\~1024차원**이 균형점입니다.
{% endhint %}

### 멀티모달 요건

텍스트 외에 이미지/오디오/비디오도 검색해야 한다면:

- **Amazon Nova Multimodal Embeddings** — 텍스트+이미지+비디오+오디오 통합 ([공식 발표](https://aws.amazon.com/blogs/machine-learning/power-video-semantic-search-with-amazon-nova-multimodal-embeddings/))
- **Amazon Titan Multimodal Embeddings G1** — 텍스트+이미지
- **Google Cloud multimodalembedding@001** — 텍스트+이미지+비디오

## 성능 평가

임베딩 모델은 공식 벤치마크로 비교할 수 있습니다.

- **MTEB** (Massive Text Embedding Benchmark) — 검색, 분류, 클러스터링 등 다양한 과제 평가 ([Hugging Face Leaderboard](https://huggingface.co/spaces/mteb/leaderboard))
- **BEIR** — 정보 검색 특화 벤치마크

실무에서는 공개 벤치마크만으로 부족하므로, **자체 데이터로 Recall@K** 등을 측정하는 것이 필수입니다.

## 차원 축소 전략

저장 비용이 부담스러울 때 차원 축소를 고려합니다.

| 방법 | 설명 | 품질 영향 |
| --- | --- | --- |
| **Matryoshka** | 모델이 지원하는 저차원 출력 (예: 3072 → 512) | 비교적 작음 |
| **Quantization** (양자화) | float32 → int8 등 정밀도 축소 | 작음 (일부 벤더 자동 지원) |
| **PCA/차원 축소 알고리즘** | 사후 처리 | 품질 저하 가능, 권장하지 않음 |

Azure의 `text-embedding-3-large`는 `dimensions=1024`로 호출하면 3072의 대부분 품질을 유지하면서 저장 공간이 1/3로 줄어듭니다 ([공식 문서](https://learn.microsoft.com/azure/ai-services/openai/how-to/embeddings?tabs=console#change-the-embeddings-dimensions)).

## 참고하기

### AWS

- [Amazon Bedrock Embedding Models 개요](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Amazon Titan Text Embeddings V2](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)
- [Amazon Titan Multimodal Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-multiemb-models.html)
- [Cohere Embed 모델](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed.html)

### Azure

- [Azure OpenAI Embeddings](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#embeddings)
- [Embeddings 사용 가이드](https://learn.microsoft.com/azure/ai-services/openai/how-to/embeddings)
- [Azure OpenAI Embeddings tutorial](https://learn.microsoft.com/azure/ai-services/openai/tutorials/embeddings)

### Google Cloud

- [Vertex AI Text Embeddings](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings)
- [Vertex AI Multimodal Embeddings](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings)
- [Vertex AI Embedding 모델 목록](https://cloud.google.com/vertex-ai/generative-ai/docs/models#embeddings)

### OCI

- [OCI Generative AI Embedding 모델](https://docs.oracle.com/en-us/iaas/Content/generative-ai/embed-models.htm)

### 벤치마크 및 평가

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [BEIR Benchmark](https://github.com/beir-cellar/beir)
