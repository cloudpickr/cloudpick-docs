---
description: 멀티클라우드 AI 아키텍처 패턴, RAG 파이프라인, GPU 가용성을 벤더별로 비교합니다.
---

# 멀티클라우드 AI

> 문서 기준: 2026년 7월 | 이 문서는 변동이 빠른 영역으로 분기별 리뷰 대상입니다.

{% hint style="info" %}
이 문서는 심화 내용입니다. AI 서비스 비교가 처음이라면 [AI 시작하기](getting-started.md)와 [AI 플랫폼과 모델 비교](ai-ml.md)를 먼저 읽는 것을 권장합니다.
{% endhint %}

## 왜 멀티클라우드 AI인가

각 클라우드 벤더는 AI/ML 영역에서 서로 다른 강점을 가지고 있습니다. 단일 벤더에 종속되지 않고 워크로드 특성에 맞는 최적의 서비스를 조합하면 비용, 성능, 모델 다양성 측면에서 이점을 얻을 수 있습니다.

- **AWS** — Amazon Bedrock/SageMaker AI. 최대 규모 모델 카탈로그 + 자체 AI 칩(Trainium/Inferentia)
- **Azure** — Microsoft Foundry. OpenAI GPT 시리즈 주력 + Microsoft 생태계 통합
- **Google Cloud** — Gemini Enterprise Agent Platform. 자체 Gemini 멀티모달 + TPU 인프라
- **OCI** — OCI Enterprise AI. Dedicated AI Cluster(RDMA 전용 GPU) + 이그레스 10TB 무료

{% hint style="info" %}
각 벤더의 AI 플랫폼 상세 비교, 모델 카탈로그, Fine-tuning 옵션은 [AI 플랫폼과 모델 비교](ai-ml.md)를 참고하세요.
{% endhint %}

## GPU 가용성

AI 학습 및 추론에 필수적인 GPU 인스턴스를 주요 CSP별로 비교합니다.

### NVIDIA GPU 세대별 비교

현재 클라우드에서 제공되는 주요 NVIDIA 데이터센터 GPU의 스펙 비교입니다.

| 항목 | H100 (Hopper) | H200 (Hopper) | B200 (Blackwell) | GB200 (Blackwell) |
| --- | --- | --- | --- | --- |
| **메모리** | 80GB HBM3 | 141GB HBM3e | 192GB HBM3e | 384GB (2×192GB) |
| **대역폭** | 3.35 TB/s | 4.8 TB/s | 8.0 TB/s | 16 TB/s (Superchip) |
| **NVLink** | 900 GB/s | 900 GB/s | 1.8 TB/s | NVL72 도메인 |
| **TDP** | 700W | 700W | 1000W | 1200W (Superchip) |
| **적합 워크로드** | 학습/추론 범용 | 대규모 추론, 긴 컨텍스트 | 차세대 학습 | 조 단위 파라미터 프론티어 모델 |
| **H100 대비 추론 성능** | 1× | ~1.4× | ~4× | ~30× |

**선택 가이드:**

- **H100/H200** — 가장 넓은 리전 가용성. 중규모 학습, Fine-tuning, 일반 추론에 적합. H200은 H100과 동일 아키텍처이나 메모리·대역폭이 대폭 증가하여 긴 컨텍스트 추론에 강점
- **B200** — 2026년 주력 GPU. H100 대비 메모리 2.4배, 대역폭 2.4배, LLM 추론 4배 빠름. 네이티브 FP4 지원으로 양자화 모델 추론 효율 극대화
- **GB200 NVL72** — Grace CPU + B200 GPU를 하나의 Superchip으로 결합. 최대 72 GPU를 단일 NVLink 도메인으로 연결하여 조 단위 파라미터 모델 학습에 사용. 가용 리전 제한적

{% hint style="info" %}
대부분의 엔터프라이즈 AI 워크로드(RAG 추론, Fine-tuning, 중규모 학습)는 **H100/H200으로 충분**합니다. B200은 대규모 학습이나 높은 추론 처리량이 필요할 때, GB200은 프론티어 모델 학습에만 필요합니다. GPU 세대가 높을수록 리전 가용성이 제한적이고 약정 확보가 어려우므로, 워크로드에 맞는 최소 사양을 선택하세요.
{% endhint %}

### 벤더별 GPU 인스턴스

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **B200 (Blackwell)** | [P6-B200](https://aws.amazon.com/ec2/instance-types/p6/) (8×B200 180GB) | [ND GB200-v6](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nd-gb200-v6-series) | [A4](https://cloud.google.com/blog/products/compute/introducing-a4-vms-powered-by-nvidia-b200-gpu-aka-blackwell/) (8×B200) | BM.GPU.B200.8 (8×B200) |
| **GB200 (NVLink)** | [P6e-GB200 UltraServer](https://aws.amazon.com/ec2/instance-types/p6/) (최대 72 GPU) | ND GB200-v6 (NVLink 도메인) | [A4X](https://cloud.google.com/blog/products/compute/new-a4x-vms-powered-by-nvidia-gb200-gpus) (GB200 NVL72) | — |
| H100 인스턴스 | [p5.48xlarge](https://aws.amazon.com/ec2/instance-types/p5/) (8×H100 80GB) | [ND H100 v5](https://learn.microsoft.com/en-us/azure/virtual-machines/nd-h100-v5-series) (8×H100 80GB) | [a3-highgpu-8g](https://cloud.google.com/compute/docs/gpus#h100-gpus) (8×H100 80GB) | [BM.GPU.H100.8](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) (8×H100 80GB) |
| A100 인스턴스 | [p4d.24xlarge](https://aws.amazon.com/ec2/instance-types/p4/) (8×A100 40/80GB) | [ND A100 v4](https://learn.microsoft.com/en-us/azure/virtual-machines/nda100-v4-series) (8×A100 80GB) | [a2-highgpu-8g](https://cloud.google.com/compute/docs/gpus#a100-gpus) (8×A100 80GB) | [BM.GPU.A100-v2.8](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) (8×A100 80GB) |
| RTX PRO / 추론 특화 | [G7](https://aws.amazon.com/ec2/instance-types/g7/) (NVIDIA RTX PRO 4500 Blackwell) | — | — | — |
| 자체 AI 칩 | Trainium2 (Trn2), Inferentia2 (Inf2) | Maia 100 | **TPU v8** (8세대) | — |
| 예약 옵션 | Reserved Instances, Savings Plans | Reserved VM Instances | CUD (Committed Use Discount) | Capacity Reservation |
| 스팟/선점형 | Spot Instances | Spot VMs | Spot VMs (Preemptible) | Preemptible Instances |

{% hint style="warning" %}
GPU 인스턴스 가격은 리전, 약정 기간, 가용성에 따라 크게 달라집니다. 최신 가격은 각 벤더의 가격 계산기를 참조하세요.
{% endhint %}

{% hint style="info" %}
**기밀 AI 추론:** 모델 IP나 민감 입력 데이터를 처리 중에도 보호해야 한다면 **기밀 컴퓨팅 GPU**(Azure NCC H100 v5, GCP A3 Confidential VM)를 사용할 수 있습니다. 벤더별 기밀 컴퓨팅 비교는 [데이터 보호 — 기밀 컴퓨팅](../security/data-protection.md#기밀-컴퓨팅-confidential-computing)을 참고하세요.
{% endhint %}

## RAG 파이프라인

RAG(Retrieval-Augmented Generation) 파이프라인은 Vector DB, Embedding 모델, LLM, 오케스트레이션의 조합으로 구성됩니다. 각 벤더별 주요 서비스:

- **AWS** — OpenSearch Serverless + Titan Embeddings + Bedrock Knowledge Bases
- **Azure** — AI Search + Microsoft Foundry + Azure AI Studio
- **Google Cloud** — Vertex AI Vector Search + Gemini Embedding + RAG Engine
- **OCI** — OCI Search/Oracle 23ai + Cohere Embed + Enterprise AI Agents

{% hint style="info" %}
RAG 파이프라인 구현 패턴(하이브리드 검색, 청킹 전략, 리랭킹, 오케스트레이션)의 상세는 [RAG 고급 패턴](rag-patterns.md)을 참고하세요.
{% endhint %}

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
- **관찰가능성** — 프롬프트, 응답, 토큰 사용량, 지연 시간, 비용을 함께 모니터링합니다.
- **보안** — 프롬프트 인젝션, 민감정보 유출, 과도한 에이전트 권한을 통제해야 합니다.

{% hint style="info" %}
멀티클라우드 AI는 모든 벤더를 동시에 쓰는 것이 목표가 아닙니다. 데이터 위치, 모델 품질, 비용, 규제 요구사항에 따라 필요한 조합만 선택하는 것이 핵심입니다.
{% endhint %}

## 자주 하는 실수

- **모든 벤더의 AI 서비스를 동시에 도입** — 멀티클라우드 AI는 필요한 조합만 선택하는 것인데, 모든 벤더를 병행하여 운영 복잡도와 비용이 폭증
- **데이터 이동 비용을 사전에 산정하지 않음** — 임베딩, 문서, 로그를 클라우드 간 이동하면 이그레스 비용이 예상보다 크게 발생
- **모델 API 형식에 직접 종속** — 추상화 계층 없이 특정 벤더의 함수 호출 방식에 코드를 맞추어 모델 교체가 어려워짐

## 체크리스트

- [ ] 멀티클라우드 AI 도입 사유(모델 품질, 비용, 규제)를 명확히 정의했는가
- [ ] 데이터 이동 비용(이그레스)을 사전에 산정하고 데이터 근접형 아키텍처를 검토했는가
- [ ] 모델 호출에 추상화 계층(LangChain 등)을 두어 벤더 교체가 가능한 구조인가

## 참고하기

### AWS

- [Amazon Bedrock 문서](https://docs.aws.amazon.com/bedrock/)
- [Amazon SageMaker AI 문서](https://docs.aws.amazon.com/sagemaker/)

### Azure

- [Azure AI Services 문서](https://learn.microsoft.com/en-us/azure/ai-services/)
- [Microsoft Foundry(구 Azure OpenAI) Service 문서](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

### Google Cloud

- [Vertex AI 문서](https://cloud.google.com/vertex-ai/docs)
- [Gemini API 문서](https://cloud.google.com/gemini/docs)

### OCI

- [OCI AI Services 문서](https://www.oracle.com/artificial-intelligence/ai-services/)
- [OCI Enterprise AI(구 OCI Generative AI) 문서](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)
