---
description: 생성형 AI 서비스, ML 플랫폼, GPU 인스턴스를 벤더별로 비교합니다.
---

# AI와 머신러닝 서비스

> 문서 기준: 2026년 5월 | 이 문서는 변동이 빠른 영역으로 분기별 리뷰 대상입니다.

## 개요

{% hint style="info" %}
**클라우드 AI가 처음이라면** [클라우드 AI 시작하기](getting-started.md)를 먼저 읽어보시는 것을 권장합니다. 이 문서는 AI 서비스 비교에 초점을 둡니다.
{% endhint %}

### 이런 상황에서 유용합니다

- **챗봇/상담 자동화** — 고객 문의에 24시간 응답하고 싶을 때
- **문서 요약/분류** — 대량의 보고서, 이메일, 계약서를 빠르게 분석할 때
- **번역/콘텐츠 생성** — 다국어 지원, 마케팅 카피 생성, 제품 설명 자동화
- **코드 작성/리뷰** — 개발 생산성 향상, 보안 취약점 탐지
- **데이터 분석** — 자연어 질문으로 데이터 인사이트 얻기

온프레미스에서 AI/ML을 하려면 GPU 서버 구매, 프레임워크 설치, 학습 인프라 구성을 직접 해야 합니다. 클라우드에서는 GPU를 시간 단위로 빌리고, 관리형 플랫폼에서 모델을 학습·배포할 수 있습니다.

2023년 이후 생성형 AI(Generative AI)의 등장으로, 직접 모델을 학습하지 않고 **파운데이션 모델을 API로 호출**하는 방식이 주류가 되고 있습니다.

## 생성형 AI 서비스

### 파운데이션 모델 API

직접 모델을 학습하지 않고, 벤더가 호스팅하는 대규모 언어 모델(LLM)을 API로 호출합니다. 각 벤더는 자체 개발 모델과 파트너 모델을 함께 제공하며, 생태계가 빠르게 확장되고 있습니다.

| 벤더 | 플랫폼 | 주요 제공 모델군 | 비고 |
| --- | --- | --- | --- |
| AWS | [Amazon Bedrock](https://aws.amazon.com/bedrock/) | **Amazon Nova** (Nova Premier/Pro/Lite/Micro/Sonic), Anthropic Claude (Opus/Sonnet/Haiku), OpenAI GPT-OSS, Meta Llama, Mistral, NVIDIA Nemotron, AI21, Cohere ([지원 모델 목록](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html)) | 단일 API로 멀티 모델 선택. Amazon Nova는 텍스트/이미지/비디오/음성 멀티모달 |
| Azure | [Microsoft Foundry(구 Azure OpenAI)](https://azure.microsoft.com/products/ai-services/openai-service) | OpenAI (GPT-5 시리즈, o-시리즈), Anthropic Claude, Meta Llama, Mistral, Cohere 등 ([Foundry 모델 카탈로그](https://ai.azure.com/catalog)) | OpenAI 주력, 엔터프라이즈 보안/규정 준수 |
| Google Cloud | [Vertex AI Model Garden](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models) | Google **Gemini 2.5** 시리즈 (Pro/Flash/Flash-Lite), Anthropic Claude, Meta Llama, Mistral, AI21 ([Model Garden](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)) | Gemini는 네이티브 멀티모달, Model Garden에 200+ 모델 |
| OCI | [OCI Enterprise AI(구 OCI Generative AI)](https://docs.oracle.com/iaas/Content/generative-ai/home.htm) | Cohere Command, Meta Llama, xAI Grok 등 ([지원 모델 목록](https://docs.oracle.com/en-us/iaas/Content/generative-ai/pretrained-models.htm)) | Oracle DB 네이티브 통합, **Dedicated AI Cluster** (전용 RDMA GPU, 타 테넌트 비공유), 이그레스 10TB 무료 |

{% hint style="info" %}
**모델 생태계는 빠르게 변합니다.** 최근에는 벤더 간 파트너십이 강화되어 "한 벤더 플랫폼에서 여러 제공사 모델 접근"이 일반화되었습니다:

- **Amazon Bedrock** — Anthropic(전략적 투자 파트너), OpenAI GPT 시리즈, Meta, Mistral, NVIDIA 등 다수 제공사 호스팅
- **Microsoft Foundry** — OpenAI 독점 파트너십 외에 Anthropic, Meta, Mistral 등 확장
- **Gemini Enterprise Agent Platform** — Google 자체 Gemini + Anthropic Claude + 타사 모델 카탈로그

정확한 현재 모델 목록은 각 벤더의 공식 모델 페이지에서 확인하세요. 모델명/버전은 수개월마다 변경될 수 있습니다.
{% endhint %}

### AI 에이전트 / RAG

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Bedrock Agents + Knowledge Bases | 문서 기반 RAG 자동 구성. 도구 호출(Tool Use) 지원 |
| Azure | Azure AI Agent Service | OpenAI Assistants API 기반. Azure 서비스 연동 |
| Google Cloud | Vertex AI Agent Builder | 검색 + 대화 + RAG 통합 |
| OCI | OCI Enterprise AI Agents | RAG 기반 에이전트. OCI Search 연동 |

### 코드 어시스턴트

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Kiro | AI 코딩 에이전트. 코드 생성, 변환, 보안 스캔 |
| Azure | GitHub Copilot | 코드 자동 완성. VS Code/JetBrains 통합 |
| Google Cloud | Gemini Code Assist | 코드 생성, 설명, 변환 |
| OCI | 전용 코드 어시스턴트 없음 | OCI Enterprise AI API를 통한 코드 생성 가능 (Cohere Command, Llama). IDE 통합 플러그인은 미제공 |

## ML 플랫폼

직접 모델을 학습하고 배포해야 하는 경우 사용합니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | SageMaker AI | 학습, 튜닝, 배포, MLOps 통합 플랫폼 |
| Azure | Azure Machine Learning | 노트북, AutoML, 파이프라인, 모델 레지스트리 |
| Google Cloud | Vertex AI | 학습, 배포, 파이프라인, Feature Store 통합 |
| OCI | OCI Data Science | 노트북, 모델 학습/배포, 파이프라인 |

### GPU / AI 가속기

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | P5 (NVIDIA H100), Trn2 (Trainium), Inf2 (Inferentia) | 학습: Trainium, 추론: Inferentia로 비용 최적화 |
| Azure | ND H100 v5, ND H200 v5 | NVIDIA 최신 GPU |
| Google Cloud | A3 (H100), TPU v5p | TPU: Google 자체 AI 가속기. 대규모 학습에 강점 |
| OCI | GPU Instances (A100, H100) | NVIDIA GPU. Bare Metal + RDMA 클러스터 지원 |

## 핵심 차이점

**Amazon Bedrock** — 자체 개발 **Amazon Nova 2** 모델군(Premier/Pro/Lite/Micro/Sonic/Omni)과 Anthropic Claude, OpenAI GPT 시리즈 등 다양한 제공사의 모델을 하나의 API로 접근할 수 있습니다. 모델 선택 폭이 가장 넓으며, AI 에이전트 구축을 위한 AgentCore 등 운영 체계가 강점입니다.

**Microsoft Foundry** — 구 Azure AI Foundry가 브랜드를 통합한 상위 플랫폼입니다. OpenAI GPT 시리즈를 엔터프라이즈 환경에서 쓸 수 있는 주요 경로이며, Anthropic, Meta 등 타사 모델도 폭넓게 제공합니다. Microsoft 365, GitHub, Power Platform 등 기존 Microsoft 생태계와의 깊은 통합이 최대 강점입니다.

**Gemini Enterprise Agent Platform** — 구 Vertex AI가 에이전트 중심으로 전면 개편된 플랫폼입니다. Google 자체 **Gemini 2.5** 시리즈(Pro/Flash/Flash-Lite)의 네이티브 멀티모달 능력과 TPU 인프라가 강점입니다. Agent Studio를 통한 로우코드 에이전트 개발과 Google Search/BigQuery와의 결합이 차별점입니다.

**OCI Enterprise AI** — 구 OCI Generative AI가 확장된 플랫폼입니다. Cohere, Meta Llama, xAI Grok 4.3 등의 모델을 OCI 인프라에서 호스팅하며, 전용 AI 클러스터(Dedicated AI Cluster)와 RDMA 기반 Bare Metal GPU로 고성능 워크로드를 지원합니다. Oracle Database/애플리케이션과의 네이티브 통합이 강점입니다.

## ML 파이프라인과 MLOps

직접 모델을 학습하고 운영할 때는 MLOps 파이프라인을 구성합니다.

### ML 라이프사이클

```mermaid
graph LR
    A[데이터 수집] --> B[데이터 준비/라벨링]
    B --> C[피처 엔지니어링]
    C --> D[모델 학습]
    D --> E[평가]
    E --> F[모델 배포]
    F --> G[모니터링]
    G --> A
```

### 단계별 도구

| 단계 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **데이터 준비** | SageMaker AI Data Wrangler, Ground Truth | Azure ML Data Labeling | Vertex AI Data Labeling | OCI Data Labeling |
| **피처 스토어** | SageMaker AI Feature Store | Azure ML Feature Store | Vertex AI Feature Store | OCI Feature Store |
| **학습/튜닝** | SageMaker AI Training + Automatic Model Tuning | Azure ML + AutoML | Vertex AI Training + Hyperparameter Tuning | OCI Data Science Training |
| **모델 레지스트리** | SageMaker AI Model Registry | Azure ML Model Registry | Vertex AI Model Registry | OCI Model Catalog |
| **배포** | SageMaker AI Endpoints + Serverless | Azure ML Online/Batch Endpoints | Vertex AI Endpoints | OCI Model Deployment |
| **모니터링** | SageMaker AI Model Monitor | Azure ML Data Drift Detection | Vertex AI Model Monitoring | OCI Model Monitoring |
| **파이프라인** | SageMaker AI Pipelines | Azure ML Pipelines | Vertex AI Pipelines (Kubeflow 기반) | OCI Data Science Jobs + Pipelines |

### 생성형 AI vs 전통 ML 선택

| 요구사항 | 권장 접근 |
| --- | --- |
| 자연어 대화, 요약, 번역 | 파운데이션 모델 API (Bedrock/Microsoft Foundry/Vertex AI) |
| 도메인 특화 지식 + 일반 LLM | RAG (파운데이션 모델 + 벡터 스토어) |
| 특정 태스크에 고도로 최적화 | Fine-tuning 또는 커스텀 모델 학습 |
| 이미지/객체 인식 | 사전 학습 비전 모델 또는 Computer Vision API |
| 시계열 예측, 이상 탐지 | 전통 ML (SageMaker AI/Vertex AI 등) |
| 초경량 엣지 배포 | 전통 ML + 모델 양자화 |

{% hint style="warning" %}
AI 서비스는 다른 클라우드 서비스보다 **변경 빈도가 매우 높습니다.** 모델명, API 엔드포인트, 가격이 수시로 바뀌므로, 이 문서의 기준 시점 이후 변경사항은 각 벤더의 공식 문서를 확인하세요.
{% endhint %}

## AI 활용의 확장 방향

AI는 모델 API 호출을 넘어 다양한 형태로 확장되고 있습니다.

### Applied AI (산업별 AI 서비스)

AI/ML을 직접 구축하지 않고, 특정 업무에 바로 적용할 수 있는 완성형 AI 서비스입니다.

| 영역 | 예시 | 벤더 서비스 |
| --- | --- | --- |
| 컨택센터 (AICC) | 음성 봇, 실시간 상담 지원 | Amazon Connect, Azure AI Contact Center, Google Cloud CCAI |
| 문서 처리 | OCR, 문서 분류, 데이터 추출 | Textract, Document Intelligence, Document AI |
| 코드 생성 | 코드 자동완성, 리뷰 | Amazon Q Developer, GitHub Copilot, Gemini Code Assist |
| BI 자연어 질의 | 자연어로 데이터 분석 | Amazon Q in QuickSight, Copilot in Power BI, Gemini in Looker |

### Physical AI (물리 세계 AI)

IoT, 로보틱스, 디지털 트윈 등 물리 세계와 연결되는 AI입니다.

| 영역 | 클라우드 연관 서비스 |
| --- | --- |
| IoT + 엣지 추론 | AWS IoT Greengrass, Azure IoT Edge, Google Cloud Edge TPU |
| 디지털 트윈 | AWS IoT TwinMaker, Azure Digital Twins |
| 로보틱스 시뮬레이션 | AWS RoboMaker, NVIDIA Isaac (클라우드 GPU) |

### Agentic Apps (AI 에이전트)

자율적으로 도구를 호출하고 멀티스텝 작업을 수행하는 AI 앱입니다.

| 벤더 | 서비스 | 특징 |
| --- | --- | --- |
| AWS | [Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) | 도구 호출, 지식 베이스 연동, 코드 실행 |
| Azure | [Azure AI Agent Service](https://learn.microsoft.com/azure/ai-services/agents/) | 멀티 에이전트 오케스트레이션, Azure 서비스 통합 |
| Google Cloud | [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder) | Grounding, 검색 연동, 엔터프라이즈 |

**오케스트레이션 패턴:**

- 단일 에이전트 (도구 호출 루프)
- 멀티 에이전트 (역할 분담, 감독자 패턴)
- Human-in-the-loop (승인 단계)

## 자주 하는 실수

- **Fine-tuning부터 시작** — RAG로 충분한 문제를 Fine-tuning으로 해결하려 하여 비용과 시간을 낭비. RAG를 먼저 시도해야 함
- **모델 버전을 고정하지 않음** — 벤더가 모델을 업데이트하면 기존 프롬프트의 동작이 달라져 프로덕션 품질이 갑자기 저하됨
- **단일 모델에 모든 워크로드를 처리** — 간단한 분류 작업에도 최대 모델을 사용하여 비용이 불필요하게 증가. 태스크별 모델 분리 필요

## 체크리스트

- [ ] 워크로드 특성(대화, 요약, 코드 생성 등)에 맞는 모델을 선택하고 비용/품질을 비교했는가
- [ ] 모델 ID/버전을 코드에 고정하고, 업그레이드 시 평가를 거쳐 전환하는가
- [ ] RAG → Fine-tuning → 직접 학습 순서로 단계적으로 접근하고 있는가

## 참고하기

### AWS

- [Amazon Bedrock 문서](https://docs.aws.amazon.com/ko_kr/bedrock/)
- [Amazon SageMaker AI 문서](https://docs.aws.amazon.com/ko_kr/sagemaker/)
- [Kiro](https://kiro.dev/)

### Azure

- [Microsoft Foundry(구 Azure OpenAI) Service 문서](https://learn.microsoft.com/ko-kr/azure/ai-services/openai/)
- [Azure Machine Learning 문서](https://learn.microsoft.com/ko-kr/azure/machine-learning/)

### Google Cloud

- [Vertex AI 문서](https://cloud.google.com/vertex-ai/docs)
- [Gemini API 문서](https://cloud.google.com/vertex-ai/generative-ai/docs)

### OCI

- [OCI AI Services 문서](https://www.oracle.com/artificial-intelligence/ai-services/)
- [OCI Data Science 문서](https://docs.oracle.com/en-us/iaas/data-science/using/data-science.htm)
- [OCI Enterprise AI(구 OCI Generative AI) 문서](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)
