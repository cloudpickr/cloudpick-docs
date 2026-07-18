---
title: "AI 플랫폼과 모델 비교"
description: "벤더별 AI 플랫폼, 모델 카탈로그, GPU/AI 칩, Applied AI 서비스를 비교합니다."
---

# AI 플랫폼과 모델 비교

> 문서 기준: 2026년 7월 | 이 문서는 변동이 빠른 영역으로 분기별 리뷰 대상입니다.

## 개요

:::note
**AI가 처음이라면** [AI 시작하기](getting-started.md)를 먼저 읽어보시는 것을 권장합니다. 이 문서는 AI 서비스 비교에 초점을 둡니다.
:::

### 전통 ML에서 생성형 AI까지

| 세대 | 핵심 기술 | 특징 | 클라우드 서비스 예시 |
| --- | --- | --- | --- |
| **전통 ML** | 회귀, 분류, 클러스터링 | 정형 데이터 기반, 피처 엔지니어링 필요 | SageMaker, Azure ML, Vertex AI |
| **딥러닝** | CNN, RNN, Transformer | 비정형 데이터(이미지, 텍스트, 음성) 처리. GPU 필수 | GPU 인스턴스, 관리형 학습 플랫폼 |
| **생성형 AI** | 파운데이션 모델 (LLM, 멀티모달) | 텍스트/이미지/코드 생성. API 호출로 사용 | Bedrock, Microsoft Foundry, Gemini |
| **에이전틱 AI** | LLM + 도구 호출 + 자율 실행 | 목표 부여 시 스스로 계획·실행·검증 | AgentCore, Foundry Agents, [상세→](agents.md) |

**패러다임 전환:** 전통 ML은 "데이터를 모아 모델을 직접 학습"하는 방식이었습니다. 2017년 Google이 발표한 **Transformer 아키텍처** ("Attention Is All You Need")가 전환점이 되었습니다. 대규모 텍스트를 병렬로 학습할 수 있게 되면서 GPT, BERT 등 파운데이션 모델이 탄생했고, 이후 "이미 학습된 모델을 API로 호출"하는 생성형 AI 시대가 열렸습니다. 에이전틱 AI에서는 이 모델이 도구를 사용해 "스스로 작업을 완수"하는 단계로 진화하고 있습니다.

### 이런 상황에서 유용합니다

- **챗봇/상담 자동화** — 고객 문의에 24시간 응답하고 싶을 때
- **문서 요약/분류** — 대량의 보고서, 이메일, 계약서를 빠르게 분석할 때
- **번역/콘텐츠 생성** — 다국어 지원, 마케팅 카피 생성, 제품 설명 자동화
- **코드 작성/리뷰** — 개발 생산성 향상, 보안 취약점 탐지
- **데이터 분석** — 자연어 질문으로 데이터 인사이트 얻기

온프레미스에서 AI/ML을 하려면 GPU 서버 구매, 프레임워크 설치, 학습 인프라 구성을 직접 해야 합니다. 클라우드에서는 GPU를 시간 단위로 빌리고, 관리형 플랫폼에서 모델을 학습·배포할 수 있습니다.

## 생성형 AI 모델 유형

| 유형 | 입력 → 출력 | 대표 서비스 | 사용 사례 |
| --- | --- | --- | --- |
| **텍스트 (LLM)** | 텍스트 → 텍스트 | GPT-5.6, Claude Fable 5, Gemini 3.5 | 챗봇, 요약, 코드 생성 |
| **이미지 생성** | 텍스트 → 이미지 | DALL-E, MAI-Image, Imagen, Titan Image | 마케팅, 디자인 |
| **음성 (TTS/STT)** | 텍스트 ↔ 음성 | Polly, MAI-Voice, Azure Speech, Cloud TTS | 회의록, ARS, 접근성 |
| **비디오 생성** | 텍스트 → 비디오 | Nova Reel, Veo 3.1, Gemini Omni | 광고, 숏폼 |
| **멀티모달** | 텍스트+이미지+음성 → 텍스트 | GPT-5.6, Gemini 3.5 Pro, Claude Fable 5 | 문서 이해, 이미지 분석 |
| **임베딩** | 텍스트/이미지 → 벡터 | Titan Embeddings, Gemini Embedding, Cohere Embed | RAG, 유사도 검색 |

## 생성형 AI 서비스

### 파운데이션 모델 API

직접 모델을 학습하지 않고, 벤더가 호스팅하는 대규모 언어 모델(LLM)을 API로 호출합니다. 각 벤더는 자체 개발 모델과 파트너 모델을 함께 제공하며, 생태계가 빠르게 확장되고 있습니다.

| 모델 제공사 | 주요 모델 | 1P (직접) | 3P (클라우드 제공) |
| --- | --- | --- | --- |
| **OpenAI** | GPT-5.6 (Sol/Terra/Luna), GPT-5.5, o-시리즈 | [api.openai.com](https://platform.openai.com/) | Azure Foundry, Bedrock |
| **Anthropic** | Claude Fable 5, Opus 4.8, Sonnet 5, Haiku | [api.anthropic.com](https://platform.claude.com/) | Bedrock, Vertex AI |
| **Google** | Gemini 3.5 Pro/Flash, 3.1 Pro, Gemini Omni | [Gemini API](https://ai.google.dev/) | Vertex AI (네이티브) |
| **xAI** | Grok 4.3, Grok 4.1 Fast, Imagine | [x.ai/api](https://x.ai/api) | OCI, Vertex AI, Bedrock, Azure |
| **Meta** | Llama 4 (오픈웨이트) | [llama.meta.com](https://llama.meta.com/) | Bedrock, Vertex, Azure, OCI (호스팅) |
| **Amazon** | Nova Premier/Pro/Lite/Micro/Sonic | — (Bedrock 전용) | Bedrock |
| **Microsoft** | MAI (Image/Voice/Transcribe) | — (Foundry 전용) | Azure Foundry |
| **Mistral** | Large, Small, Codestral | [api.mistral.ai](https://api.mistral.ai/) | Bedrock, Azure, Vertex |
| **Upstage** | Solar Pro 3/2/Mini | [console.upstage.ai](https://console.upstage.ai/) | AWS/Azure Marketplace |
| **LG AI Research** | EXAONE 4.x | 직접 계약 | Marketplace, 셀프호스팅 |

:::note
**1P(직접)와 3P(클라우드 제공)의 차이** — 같은 모델이라도 채널에 따라 기능 범위, 쿼터, 빌링이 다릅니다. 채널 선택 기준은 [LLM 채널 선택 가이드](1p-vs-3p.md)를 참고하세요.
:::

### 클라우드 플랫폼별 특징

위 모델들을 호스팅하는 클라우드 플랫폼은 각각 고유한 부가 가치를 제공합니다:

| 플랫폼 | 강점 |
| --- | --- |
| [Amazon Bedrock](https://aws.amazon.com/bedrock/) | 멀티모델 단일 API, AgentCore, AWS IAM/VPC 통합, EDP 소진 |
| [Microsoft Foundry](https://azure.microsoft.com/products/ai-services/openai-service) | OpenAI 주력 채널, M365/GitHub 통합, Foundry Local(단절망), PTU |
| [Vertex AI / Gemini Platform](https://cloud.google.com/vertex-ai) | Gemini 네이티브, 2M 토큰, Model Garden 200+ 모델, ADK |
| [OCI Enterprise AI](https://docs.oracle.com/iaas/Content/generative-ai/home.htm) | Oracle DB 통합, 전용 GPU 클러스터(RDMA), 이그레스 10TB 무료 |

### AI 에이전트 / RAG

| 벤더 | 에이전트 플랫폼 | RAG |
| --- | --- | --- |
| AWS | [Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) | [Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) — Managed KB(Smart Parsing, Agentic Retriever), Web Search |
| Azure | [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/) | Azure AI Search |
| Google Cloud | [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) | Vertex AI RAG Engine |
| OCI | [OCI Enterprise AI Agents](https://docs.oracle.com/iaas/Content/generative-ai/agents.htm) | OCI Search 연동 |

### 코드 어시스턴트 / AI 에이전트

코딩 에이전트(Kiro, Claude Code, Codex, Copilot 등)와 에이전트 플랫폼(AgentCore, Foundry Agents 등)은 [AI 에이전트](agents.md)에서 다룹니다.

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
| AWS | P6 (NVIDIA B200), P6e (GB200 UltraServer), P5 (H100), Trn2 (Trainium), Inf2 (Inferentia) | Blackwell: P6-B200(8×B200), P6e-GB200(최대 72 GPU NVLink). 학습: Trainium, 추론: Inferentia로 비용 최적화 |
| Azure | ND GB200-v6, ND H200 v5, ND H100 v5 | GB200-v6: Blackwell 플래그십. DL 학습/생성형 AI/HPC |
| Google Cloud | A4X (GB200 NVL72), A4 (B200), A3 (H100), TPU v5p/v6e | A4: Blackwell 단일 GPU, A4X: GB200 NVL72 최초 클라우드 제공. TPU: Google 자체 AI 가속기 |
| OCI | GPU Instances (B200, H100, A100) | NVIDIA Blackwell + Bare Metal + RDMA 클러스터 지원 |

## 핵심 차이점

**Amazon Bedrock** — 자체 개발 **Amazon Nova 2** 모델군(Premier/Pro/Lite/Micro/Sonic/Omni)과 Anthropic Claude, OpenAI GPT 시리즈 등 다양한 제공사의 모델을 하나의 API로 접근할 수 있습니다. 모델 선택 폭이 가장 넓으며, AI 에이전트 구축을 위한 AgentCore 등 운영 체계가 강점입니다.

**Microsoft Foundry** — 구 Azure AI Foundry가 브랜드를 통합한 상위 플랫폼입니다. OpenAI GPT-5.5/5.4 시리즈를 엔터프라이즈 환경에서 쓸 수 있는 주요 경로이며, Anthropic, Meta 등 타사 모델도 폭넓게 제공합니다. 자체 **MAI 모델군**(Image-2.5, Voice-1, Transcribe-1)과 **Foundry Local**(로컬/단절망 실행)이 추가되었습니다. Microsoft 365, GitHub, Power Platform 등 기존 Microsoft 생태계와의 깊은 통합이 최대 강점입니다.

**Gemini Enterprise Agent Platform** — 구 Vertex AI가 에이전트 중심으로 전면 개편된 플랫폼입니다. Google 자체 **Gemini 3.x/2.5** 시리즈(3.5 Pro/3.5 Flash/3.1 Pro)의 네이티브 멀티모달 능력과 TPU 인프라가 강점입니다. Gemini 3.5 Pro GA (2026.06)는 2M 토큰 컨텍스트 윈도우와 Deep Think 추론을 지원하며, **Gemini Omni**(any-to-any 멀티모달 비디오 생성)와 Agent Studio를 통한 로우코드 에이전트 개발, Google Search/BigQuery와의 결합이 차별점입니다.

**OCI Enterprise AI** — 구 OCI Generative AI가 확장된 플랫폼입니다. Cohere, Meta Llama, xAI Grok 4.3, Google Gemini 등의 모델을 OCI 인프라에서 호스팅하며, 전용 AI 클러스터(Dedicated AI Cluster)와 RDMA 기반 Bare Metal GPU로 고성능 워크로드를 지원합니다. **AI Guardrails**(콘텐츠 모더레이션, PII 탐지, 프롬프트 인젝션 방어)와 **Enterprise AI Agents**(GA)가 추가되었습니다. OpenAI와의 파트너십으로 GPT-5.5/5.4 및 Codex를 OCI Marketplace에서 Oracle Universal Credits로 이용할 수 있게 될 예정이며, Oracle Database/애플리케이션과의 네이티브 통합이 강점입니다.

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

### AI 개발 수명주기 (AI-DLC)

AI 프로젝트의 전체 수명주기(문제 정의→데이터→모델→평가→배포→모니터링→개선)와 운영 상세는 [LLMOps](llmops.md)를 참고하세요.
- **비용 거버넌스** — AI 비용은 사용량에 비례하여 예측이 어렵습니다. 일/월 예산 상한, 태스크별 토큰 한도, 비용 초과 알림을 반드시 설정하세요.
- **데이터 드리프트** — RAG용 문서가 오래되면 답변 품질이 서서히 저하됩니다. 정기적인 데이터 갱신 파이프라인을 구성하세요.
- **규정 준수** — 입출력 로그의 PII 마스킹, 데이터 보존 정책, 모델의 학습 데이터 사용 여부를 지속적으로 관리해야 합니다.

:::note
생성형 AI의 DLC는 전통 ML보다 **반복 주기가 짧습니다**. 모델 학습에 수개월이 걸리는 전통 ML과 달리, 프롬프트 변경은 수 분, RAG 데이터 업데이트는 수 시간이면 반영됩니다. 이 빠른 주기에 맞는 평가·배포·롤백 체계가 필요합니다.
:::

:::caution
AI 서비스는 다른 클라우드 서비스보다 **변경 빈도가 매우 높습니다.** 모델명, API 엔드포인트, 가격이 수시로 바뀌므로, 이 문서의 기준 시점 이후 변경사항은 각 벤더의 공식 문서를 확인하세요.
:::

## AI 활용의 확장 방향

### Applied AI (산업별 완성형 서비스)

| 영역 | 벤더 서비스 | 트렌드 (2025-2026) |
| --- | --- | --- |
| 컨택센터 | Amazon Connect, Azure Contact Center, Google CCAI | 코파일럿 → 자율 에이전트 전환 |
| 문서 처리 | Textract, Document Intelligence, Document AI | LLM/멀티모달 추론 결합 |
| BI | Amazon Quick, Copilot in Power BI, Gemini in Looker | 에이전틱 분석, 대시보드 에이전트 |
| 헬스케어 | Amazon Connect Health, Azure Health Bot | HIPAA 에이전트 |

### Physical AI (물리 세계 연결)

| 영역 | 클라우드 서비스 |
| --- | --- |
| IoT + 엣지 추론 | AWS IoT Greengrass, Azure IoT Operations, Google Edge TPU |
| 디지털 트윈 | AWS IoT TwinMaker, Azure Digital Twins, NVIDIA Omniverse |
| 로보틱스 | NVIDIA Isaac, Halos for Robotics |

## 멀티클라우드 모델 접근의 변화 (2025-2026)

2025~2026년 사이, 모델 제공사와 클라우드 벤더 간 관계가 변화하고 있습니다. 가장 큰 변화는 OpenAI-Microsoft 독점의 종료이며, 그 외 제공사들도 채널을 확대하고 있습니다.

| 시기 | 이벤트 | 영향 |
| --- | --- | --- |
| 2026.04 | **OpenAI-Microsoft 독점 종료** | OpenAI 모델을 Azure 외 플랫폼에서도 제공 가능 |
| 2026.04 | **OpenAI 모델 → Bedrock 제공 시작** | 독점 종료 직후 GPT-5.x가 Bedrock에 등장 |
| 2025-2026 | **xAI Grok 멀티클라우드 확산** | Azure AI Foundry(2025.09), Vertex AI, OCI, Bedrock(2026.06 Grok 4.3 GA) |
| 2025-2026 | **Anthropic Claude 채널 강화** | 기존 Bedrock/Vertex에 더해 OCI 등 추가 채널 |

**운영 시사점:**

- 하나의 클라우드 벤더에 종속되지 않고 여러 경로로 동일 모델에 접근할 수 있게 되었습니다
- 모델 선택 시 "어떤 모델"뿐 아니라 "어떤 플랫폼에서 접근할 때 비용/SLA/리전이 유리한가"가 의사결정 기준이 됩니다
- [멀티클라우드 AI](multicloud-ai.md)에서 벤더 조합 전략을 상세히 다룹니다

## 추론 비용 최적화

생성형 AI의 주요 비용은 **추론(inference)**에서 발생합니다. 2025-2026년 벤더들이 도입한 비용 절감 옵션입니다.

| 전략 | 설명 | 벤더 지원 |
| --- | --- | --- |
| **Flex/배치 추론** | 지연 시간에 민감하지 않은 워크로드를 저우선순위로 처리하여 비용 절감 | Bedrock Flex Inference, Azure Batch API, Vertex Batch Predictions |
| **모델 라우팅** | 간단한 질의는 경량 모델(Flash/Haiku/mini), 복잡한 질의만 고성능 모델로 분기 | Bedrock IntelligentPromptRouter, 자체 구축 |
| **프롬프트 캐싱** | 동일한 시스템 프롬프트/컨텍스트를 캐싱하여 반복 토큰 비용 절감 | Anthropic Prompt Caching, OpenAI Cached Tokens, Gemini Context Caching |
| **장기 컨텍스트 vs RAG** | 모델 컨텍스트 윈도우 확장(1~2M+ 토큰)으로 RAG 없이도 충분한 경우 발생 | Gemini 3.5 Pro, Claude Opus 계열 |
| **GPU 가격 경쟁** | 하이퍼스케일러 간 GPU 인스턴스 가격 인하 추세 | AWS, Azure, GCP 경쟁적 인하 |

:::note
추론 비용은 모델별, 벤더별로 수시로 변경됩니다. 정확한 현재 가격은 각 벤더의 공식 가격 페이지를 확인하세요. 비용 추적과 예산 관리는 [LLMOps](llmops.md)에서 상세히 다룹니다.
:::

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
