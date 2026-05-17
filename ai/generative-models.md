---
description: 생성형 AI 모델을 유형별(텍스트, 이미지, 음성, 비디오, 멀티모달)로 분류하고 벤더별 서비스를 비교합니다.
---

# 생성형 AI 모델 유형별 비교

> 문서 기준: 2026년 5월

## 개요

생성형 AI 모델은 텍스트뿐 아니라 이미지, 음성, 비디오, 멀티모달 등 다양한 유형으로 확장되고 있습니다. 이 문서는 "어떤 유형의 모델이 있고, 각 벤더에서 뭘 쓸 수 있는지"를 정리합니다.

플랫폼/서비스 비교("어떤 플랫폼을 쓸까")는 [AI 플랫폼과 모델 비교](ai-ml.md)를 참고하세요.

## 모델 유형별 비교

| 유형 | 입력 → 출력 | 벤더 서비스/모델 | 사용 사례 |
| --- | --- | --- | --- |
| **텍스트 (LLM)** | 텍스트 → 텍스트 | Bedrock(Claude, Llama), Microsoft Foundry(GPT 시리즈), Vertex AI(Gemini) | 챗봇, 요약, 코드 생성 |
| **이미지 생성** | 텍스트 → 이미지 | Bedrock(Titan Image, Stable Diffusion), Microsoft Foundry(DALL-E), Vertex AI(Imagen) | 마케팅 소재, 디자인 프로토타입 |
| **음성 합성 (TTS)** | 텍스트 → 음성 | Amazon Polly, Azure Speech, Google Cloud Text-to-Speech, OCI Speech | ARS, 오디오북, 접근성 |
| **음성 인식 (STT)** | 음성 → 텍스트 | Amazon Transcribe, Azure Speech, Google Cloud Speech-to-Text, OCI Speech | 회의록, 자막, 음성 검색 |
| **비디오 생성** | 텍스트/이미지 → 비디오 | Amazon Nova Reel, Vertex AI(Veo) | 광고, 숏폼 콘텐츠 |
| **멀티모달** | 텍스트+이미지+음성 → 텍스트 | GPT-4o, Gemini, Claude(비전) | 문서 이해, 이미지 분석, 비디오 요약 |
| **임베딩** | 텍스트/이미지 → 벡터 | Titan Embeddings, Microsoft Foundry Embeddings, Vertex AI Embeddings | RAG, 유사도 검색 |

## 모델 선택 기준

| 기준 | 고려사항 |
| --- | --- |
| **정확도/품질** | 벤치마크 점수, 한국어 성능 차이 |
| **비용** | 입력/출력 토큰당 가격, 이미지 생성 건당 가격 |
| **지연 시간** | 첫 토큰 시간(TTFT), 전체 응답 시간 |
| **컨텍스트 윈도우** | 128K, 200K, 1M+ 토큰 — 긴 문서 처리 능력 |
| **파인튜닝 가능 여부** | 도메인 특화 필요 시 |
| **데이터 프라이버시** | 모델에 데이터가 학습되는지 여부 |
| **리전/규제** | 한국 리전 가용 여부, 데이터 주권 |

## 벤더별 모델 마켓플레이스

| 벤더 | 서비스 | 특징 |
| --- | --- | --- |
| AWS | [Bedrock Model Catalog](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) | Anthropic, Meta, Mistral 등 다수 3rd party 모델 호스팅 |
| Azure | [Azure AI Model Catalog](https://learn.microsoft.com/azure/ai-studio/how-to/model-catalog-overview) | OpenAI 독점 + 오픈소스 모델 카탈로그 |
| Google Cloud | [Vertex AI Model Garden](https://cloud.google.com/model-garden) | Google + 오픈소스 모델 |
| 공통 | Custom Model Import | 자체 모델 배포(BYOM)도 가능 |

{% hint style="info" %}
모델 목록과 가격은 매우 빠르게 변합니다. 최신 정보는 각 벤더의 모델 카탈로그 페이지를 확인하세요.
{% endhint %}

## 자주 하는 실수

- **최대/최신 모델을 모든 태스크에 사용** — 단순 분류나 추출 작업에 GPT-4o급 모델을 사용하여 비용이 10배 이상 증가. 태스크 난이도에 맞는 모델 선택 필요
- **컨텍스트 윈도우 크기만 보고 모델 선택** — 1M 토큰을 지원해도 긴 입력의 중간 부분 정확도가 떨어지는 "Lost in the Middle" 문제 존재
- **데이터 프라이버시 정책을 확인하지 않음** — 일부 모델/플랜에서 입력 데이터가 학습에 사용될 수 있으므로 엔터프라이즈 약관을 반드시 확인

## 체크리스트

- [ ] 태스크 유형(텍스트, 이미지, 음성, 멀티모달)에 맞는 모델 유형을 선택했는가
- [ ] 비용(토큰당 가격)과 품질의 균형을 고려하여 태스크별로 적절한 크기의 모델을 배정했는가
- [ ] 모델의 데이터 처리 정책(학습 사용 여부, 데이터 보존 기간)을 확인했는가

## 관련 문서

- [AI 플랫폼과 모델 비교](ai-ml.md) — 플랫폼/서비스 비교
- [벡터 스토어](vector-store.md) — 임베딩 저장 및 검색
- [RAG 고급 패턴](rag-patterns.md) — RAG에서의 모델 활용
- [LLMOps](llmops.md) — 모델 운영 및 평가

## 참고하기

- [AWS Bedrock 지원 모델](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Microsoft Foundry 모델 목록](https://learn.microsoft.com/azure/ai-services/openai/concepts/models)
- [Vertex AI Model Garden](https://cloud.google.com/model-garden)
- [OCI Enterprise AI(구 OCI Generative AI)](https://docs.oracle.com/iaas/Content/generative-ai/home.htm)
