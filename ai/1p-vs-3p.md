---
description: 동일한 FM을 1P(모델 제공사 직접)와 3P(클라우드 플랫폼 경유)로 소비할 때의 차이를 비교합니다.
---

# LLM 채널 선택 가이드

> 문서 기준: 2026년 8월

## 개요

FM을 도입할 때 **두 가지 독립적인 선택**이 있습니다. 이 둘은 별개의 결정입니다.

| 선택 축 | 질문 | 옵션 |
| --- | --- | --- |
| **① 이용 형태** | 누가, 어떻게 쓰나? | Seat(채팅 UI) / API(코드 통합) / 셀프호스팅 |
| **② 채널** | 어디서 구매·운영하나? | 직접 이용(1P) / 클라우드 제공(3P) / 모델사+클라우드 결제 |

```
예) "Claude를 API로 Bedrock에서 사용" 
     → 이용 형태: API  
     → 채널: 클라우드 제공 (3P Inference)

예) "ChatGPT를 전 직원에게 Enterprise로 제공"
     → 이용 형태: Seat (Enterprise)
     → 채널: 직접 이용 (1P)
```

이 문서는 먼저 **① 이용 형태**(Seat vs API)를 정리한 뒤, **② 채널**(1P vs 3P)을 비교합니다.

---

## ① 이용 형태: Seat vs API

| 구분 | Seat 기반 플랜 | API 플랜 |
| --- | --- | --- |
| **이용 주체** | 조직원 개인 (개발자 포함) | 애플리케이션·서비스·자동화 시스템 |
| **사용 방식** | 제공사가 만든 UI/도구를 직접 사용 (채팅, Claude Code, Copilot 등) | 자사 제품·서비스에 모델을 프로그래밍 방식으로 내장 |
| **과금 단위** | 사용자 수(석) 기준 구독료 | 토큰·요청량 기준 사용량 과금 |
| **적합한 용도** | 개인 생산성 — 문서 작성, 분석, 코딩, 리서치 | 고객 대상 기능, 대규모 자동화, 배치 처리, 시스템 통합 |
| **통제 단위** | 사용자/그룹/관리자 정책 | API 키·서비스 계정, 프로젝트별 예산, 호출 한도 |
| **비용 예측** | 석 수 × 단가 = 고정 | 사용량에 따라 변동 |

{% hint style="warning" %}
**"Seat = 비개발자, API = 개발자"가 아닙니다.** 개발자도 Claude Code, Copilot 같은 코딩 에이전트를 Seat 플랜으로 사용합니다. 핵심 구분은 **사람이 직접 쓰는가**(Seat) vs **시스템에 내장하는가**(API)입니다.
{% endhint %}

**선택 기준:**
- 조직원이 AI 도구를 **직접** 사용 (채팅, 코딩, 분석) → **Seat** (Business/Team/Enterprise)
- 자사 제품·서비스에 LLM을 **내장**하여 고객에게 제공 → **API**
- 둘 다 필요 → **Seat + API를 별도로 운영** (대부분의 엔터프라이즈)

### API를 쓸 때: 왜 3P(클라우드 경유)를 선택하나

엔터프라이즈가 API를 코드에서 호출할 때, 모델사 직접(1P)보다 **3P(Bedrock/Vertex/Azure Foundry)를 선택하는 경우가 많습니다.**

| 3P를 선택하는 이유 | 설명 |
| --- | --- |
| **기존 클라우드 커밋 소진** | AWS EDP, Azure EA/MACC가 있으면 LLM 비용을 기존 약정에서 차감 가능 |
| **네트워크 격리** | VPC/Private Link로 트래픽이 퍼블릭 인터넷을 경유하지 않음 |
| **컴플라이언스 활용** | 클라우드 벤더의 기존 인증(HIPAA, SOC 2 등) 활용 가능 |
| **통합 빌링/거버넌스** | 기존 청구서에 합산, 비용 태그로 팀별 추적, IAM으로 접근 제어 |
| **단일 계약** | 조달 부서가 새 벤더를 추가할 필요 없이 기존 계약 내 사용 |
| **멀티모델 접근** | 하나의 플랫폼에서 여러 모델을 동일 API로 전환 가능 |

| 그래도 1P를 선택하는 이유 | 설명 |
| --- | --- |
| **최신 모델/기능** | 신규 모델과 베타 기능이 1P에 먼저 출시 |
| **풀 기능** | Fine-tuning, Realtime API 등 3P에 없거나 지연되는 기능 |
| **간단한 시작** | 카드 등록 즉시 사용, 클라우드 설정 불필요 |
| **클라우드 비종속** | 특정 클라우드에 의존하지 않음 |

{% hint style="info" %}
대규모 엔터프라이즈의 일반적 패턴: **프로덕션은 3P** (거버넌스, 커밋 소진, 격리) + **실험은 1P** (최신 기능, 빠른 시작).
{% endhint %}

---

## ② 채널: 어디서 구매·운영하나

{% hint style="info" %}
"같은 모델인데 왜 채널에 따라 경험이 다른가?"를 이해하는 것이 이 섹션의 목적입니다. 모델 자체의 성능 비교는 [AI 플랫폼과 모델 비교](ai-ml.md)를 참고하세요.
{% endhint %}

### 채널 아키텍처 패턴

FM 제공사가 고객에게 모델을 전달하는 경로는 크게 **4가지 패턴**으로 나뉩니다. 이 구분을 먼저 이해하면 각 제공사의 복잡한 오퍼링이 정리됩니다.

| 패턴 | 비유 | 운영 주체 | 빌링 | 기능 범위 |
| --- | --- | --- | --- | --- |
| **A. 직접 이용** (1P) | 직영몰 | 모델사 | 모델사 직접 청구 | 풀 기능 (최신 우선) |
| **B. 모델사 서비스 + 클라우드 결제** | 백화점 입점 매장 | 모델사 | 클라우드 마켓플레이스 (커밋 소진 가능) | 풀 기능 (1P와 동일) |
| **C. 클라우드 제공** (3P Inference) | PB/편집숍 | 클라우드 벤더 | 클라우드 청구서 통합 | 클라우드 API 범위 (일부 기능 지연/미지원) |
| **D. 셀프호스팅** (오픈웨이트) | 직접 요리 | 고객 자체 | 인프라 비용 (GPU/서버) | 라이선스 조건 내 커스터마이징 자유 |

### 제공사별 매핑

| 제공사 | A. 직접 이용 | B. 모델사 서비스 + 클라우드 결제 | C. 클라우드 제공 (3P Inference) | D. 셀프호스팅 |
| --- | --- | --- | --- | --- |
| **OpenAI** | api.openai.com (Enterprise) | — | Azure Foundry, Bedrock | ✗ (비공개 웨이트) |
| **Anthropic** | api.anthropic.com (Enterprise) | Claude Platform on AWS (CCU 빌링) | Bedrock Claude, Vertex AI Claude | ✗ (비공개 웨이트) |
| **Upstage** | console.upstage.ai | — | AWS/Azure Marketplace, SageMaker | ✅ Solar Open (오픈웨이트) |
| **LG EXAONE** | 직접 계약 | — | Marketplace | ✅ 오픈웨이트 (Hugging Face) |
| **Meta Llama** | — | — | Bedrock, Vertex, Azure (호스팅) | ✅ 오픈웨이트 (주 사용 경로) |
| **Mistral** | api.mistral.ai | — | Bedrock, Azure, Vertex | ✅ 오픈웨이트 일부 |

### 패턴별 특성 비교

| 비교 항목 | A. 직접 이용 | B. 모델사 서비스 + 클라우드 결제 | C. 클라우드 제공 | D. 셀프호스팅 |
| --- | --- | --- | --- | --- |
| 신규 모델 제공 | 최초 | 1P와 거의 동시 | 수일~수주 지연 | 오픈웨이트 공개 시점 |
| 플랫폼 기능 | 전체 | 전체 | 클라우드 API 범위 내 | 없음 (직접 구축) |
| Fine-tuning | 풀 옵션 | 풀 옵션 | 제한적이거나 지연 | 완전 자유 (자체 GPU) |
| 에이전트/도구 | 최신 (Claude Code, Codex 등) | 최신 | 자체 프레임워크 (AgentCore 등) | 직접 구축 (LangGraph 등) |
| VPC/네트워크 격리 | Enterprise 전용 | 마켓플레이스 내 격리 | 지원 (리전/서비스별 확인) | 완전 격리 (자체 인프라) |
| 컴플라이언스 | 제공사 인증 | 제공사 + 클라우드 인증 | 클라우드 인증 활용 가능 (구성 필요) | 자체 책임 |
| 커밋 소진 | 불가 | 가능 | 가능 | 불가 (인프라 비용만) |
| 운영 부담 | 없음 | 없음 | 낮음 | 높음 (GPU, 모델 서빙, 업데이트) |

{% hint style="info" %}
**패턴 D(셀프호스팅/오픈웨이트)** 의 상세 — 대표 모델, 선택 이유, 라이선스 주의사항은 [AI 플랫폼과 모델 비교](ai-ml.md)를 참고하세요.
{% endhint %}

### 실제 예시: "Claude Code를 쓰고 싶은데"

| 요구사항 | 적합한 패턴 |
| --- | --- |
| 최신 Claude Code + 빠른 업데이트 | **A. 직접 이용** |
| Claude Code + AWS EDP 소진 + AWS 청구서 | **B. 모델사 서비스 + 클라우드 결제** (Claude Platform on AWS) |
| Claude API만 필요 + VPC 격리 + 기존 AWS 거버넌스 | **C. 클라우드 제공** (Bedrock Claude) |

{% hint style="warning" %}
**패턴 B는 모든 제공사가 제공하는 것이 아닙니다.** Anthropic의 "Claude Platform on AWS"가 대표적이며, OpenAI는 현재 이에 해당하는 별도 오퍼링이 없습니다. 제공사별 가용한 패턴을 위 매핑 표에서 확인하세요.
{% endhint %}

---

## 주요 FM별 채널 현황

제공사별 모델 목록과 접근 가능 채널은 [AI 플랫폼과 모델 비교](ai-ml.md)를 참고하세요. 한국 FM(Upstage, EXAONE 등)은 [FM 제공사 비교 (한국)](../korea/ai/fm-providers.md)를 참고하세요. 패턴별 특성 비교 표는 위 **패턴별 특성 비교** 절을 사용합니다.

---

## 선택 가이드 (평가 축)

월 지출액만으로 1P/3P를 고정하지 마세요. 아래 축을 먼저 정리한 뒤 채널을 고릅니다.

| 평가 축 | 1P(직접)가 유리한 때 | 3P(클라우드 제공)가 유리한 때 |
| --- | --- | --- |
| **기능·출시 속도** | 최신 모델·에이전트 기능이 즉시 필요 | 플랫폼 API 범위로 충분, 수일~수주 지연 허용 |
| **네트워크·컴플라이언스** | Enterprise급 격리만으로 충분 | VPC/리전 거버넌스·기존 인증 상속이 필요 |
| **조달·커밋** | 클라우드 커밋이 거의 없음 | EDP/EA/CUD 등 커밋 소진이 큼 |
| **운영** | 모델사 콘솔 운영을 수용 | 기존 클라우드 IAM·관측·예산 체계에 통합 |
| **규모·쿼터** | PoC·소규모, 쿼터 여유 | 프로덕션 트래픽·예약 용량·프라이빗 오퍼 협상 |

{% hint style="warning" %}
대규모(대략 월 수만 달러 이상)에서는 **토큰 단가보다 조달 구조**(커밋 소진, 예약 용량, 프라이빗 오퍼)가 더 큰 비용 변수인 경우가 많습니다. 금액 임계값은 조직마다 다르므로 공식 견적·계약 조건을 확인하세요.
{% endhint %}

---

## 국가별 채널 선택

국가별 규제·주권 요건에 따른 채널 선택은 각 국가 가이드를 참고하세요.

- [한국](../korea/index.md) · [FM 제공사 비교 (한국)](../korea/ai/fm-providers.md)
- [미국](../us/index.md) · [EU](../eu/index.md) · [일본](../japan/index.md) · [싱가포르](../singapore/index.md)

---

## 요금제와 비용 관리

각 제공사의 라이선스 티어(Seat 플랜, API 티어), 3P 예약 용량(PTU, Provisioned Throughput), 비용 관리 도구와 패턴은 [LLM 라이선스와 비용 관리](licensing.md)에서 다룹니다.

---

## 자주 하는 실수

- **"3P가 비싸다"는 가정** — 공시 토큰 단가는 대체로 유사합니다. 기존 클라우드 커밋이 있으면 3P가 실효 비용에서 유리할 수 있습니다. 다만 청구 단위(CCU 등)와 운영 비용은 별도 확인이 필요합니다.
- **단일 채널 올인** — 1P만 쓰면 클라우드 거버넌스 연동이 약할 수 있고, 3P만 쓰면 최신 기능에 지연이 있을 수 있습니다. 조직 상황에 맞게 병행을 검토하세요.
- **쿼터를 사후에 고려** — 프로덕션 트래픽을 예측하지 않고 시작하면, 쿼터 한도에 도달해 서비스 장애로 이어집니다. 규모가 크면 사전에 예약 용량을 확보하세요.

## 체크리스트

- [ ] 월간 예상 토큰 소비량을 추정했는가
- [ ] 기존 클라우드 커밋(EDP/EA/CUD)이 있는지 확인했는가
- [ ] 데이터 레지던시·격리 요건을 대상 관할권 기준으로 정리했는가 (국가 가이드 참고)
- [ ] 필요한 기능(Fine-tuning, 에이전트, 실시간)이 어느 채널에서 제공되는지 확인했는가
- [ ] 쿼터/Rate Limit이 프로덕션 트래픽을 감당하는지 확인했는가
- [ ] 하이브리드(1P+3P) 운영 시 모델 버전 동기화 전략이 있는가

## 관련 문서

- [AI 플랫폼과 모델 비교](ai-ml.md) — 벤더별 FM 카탈로그, GPU/가속기
- [멀티클라우드 AI](multicloud-ai.md) — 벤더 조합 전략
- [LLMOps](llmops.md) — 비용 추적, 평가, 운영
- [FinOps](../governance/finops.md) — 클라우드 비용 거버넌스

## 참고하기

### 모델 제공사

- [OpenAI API Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [OpenAI API 가격](https://openai.com/api/pricing/)
- [Anthropic Claude 플랜·가격](https://claude.com/pricing)
- [Anthropic API 문서](https://docs.anthropic.com/)
- [Upstage Console](https://console.upstage.ai/)

### 클라우드 채널

- [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Amazon Bedrock 가격](https://aws.amazon.com/bedrock/pricing/)
- [Azure AI Foundry Quotas and Limits](https://learn.microsoft.com/en-us/azure/foundry/openai/quotas-limits)
- [Azure OpenAI 가격](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
- [Vertex AI Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs)
