---
description: 네이버, LG AI연구원, 카카오, KT, 업스테이지, NC AI, SKT 등 국내 FM 제공사의 모델·라이선스·제공 채널을 비교합니다.
---

# 국내 파운데이션 모델 제공사 비교

> 문서 기준: 2026년 8월

## 개요

한국에는 대기업 계열사부터 스타트업까지 다수의 파운데이션 모델(FM) 제공사가 있습니다. 이 문서는 주요 제공사의 최신 모델, 라이선스 구조, 제공 채널을 정리하고, 글로벌 모델 대비 국내 모델을 선택할 때 고려할 기준을 다룹니다.

{% hint style="info" %}
모델 버전과 라이선스 조건은 빠르게 바뀝니다. 아래 표는 2026년 8월 기준이며, 도입 전 각 사의 공식 문서에서 최신 조건을 재확인하세요.
{% endhint %}

## 제공사별 현황

| 제공사 | 대표 모델 | 최신 버전(2026.8 기준) | 라이선스 | 주요 제공 채널 |
| --- | --- | --- | --- | --- |
| 네이버(클라우드) | HyperCLOVA X | SEED(경량/오픈), THINK(추론 특화), DASH(경량·고속) 라인업. 2025.12 SEED 32B THINK/8B Omni, 2026 상반기 SEED 4B 옴니모달(국방 특화) 공개 | SEED 시리즈 일부(0.5B~3B급)는 오픈소스 공개, 상위 모델은 API 전용 | 네이버클라우드 CLOVA Studio API (Basic/Exclusive/Neurocloud 요금제) |
| LG AI연구원 | EXAONE | EXAONE 4.0(하이브리드 추론), EXAONE 4.5(멀티모달) | 연구·교육 목적 무료 공개, **상업적 이용은 LG AI Research와 별도 라이선스 계약 필요** | Hugging Face 모델 공개, LG AI Research 자체 API, 교육기관 대상 라이선스 확대 |
| 카카오 | Kanana | Kanana-2 시리즈(2026.1 업데이트 4종), Kanana-2 경량 SLM 4종(2026.7, 1.3B/3B) | Apache 2.0 기반 Kanana Open License — **상업적 이용 허용** | Hugging Face 오픈소스 배포. 온디바이스 구동 최적화 |
| KT | 믿:음(Mi:dm) | 믿:음 K 2.5 Pro(2026.2, MWC26 공개). 이전 Mi:dm K 2.0(2025.7)은 Base 11.5B + 온디바이스 Mini 2.3B 구성 | 자체 서비스/B2B 공급 중심(공개 라이선스 정보 제한적) | KT 자체 엔터프라이즈 AI 플랫폼을 통한 B2B·B2G 공급(AICC, 챗봇, 문서인식, 법률·금융 특화 등) |
| 업스테이지 | Solar | Solar Pro 2(31B, 하이브리드 채팅/추론, 2025.7 정식 출시) | 폐쇄형 API 서비스(오픈소스 아님) | Upstage Console API, Amazon Bedrock Marketplace, AWS SageMaker JumpStart, AWS Marketplace |
| NC AI | VARCO | VARCO-VISION 2.0(2025.7, 멀티모달 4종 오픈소스), VARCO 3D 2.0, VARCO Voice(다국어 음성) | 오픈소스 공개(모델별 상이) | Hugging Face, AWS SageMaker 기반 인프라. AWS Private Cloud를 통한 도메인 데이터 커스터마이징 지원 예정 |
| SK텔레콤 | A.X | A.X 4.0(2025.4.30 오픈소스 공개). Qwen2.5 기반에 한국어 데이터를 대규모 추가 학습 | 오픈소스 공개 | GitHub/Hugging Face, SKT 자체 서비스('에이닷') 연동 |

## 한국어 성능과 벤치마크

한국어 LLM 평가에는 KMMLU(한국어 지식 이해), KoBEST, HAE-RAE 등이 사용됩니다. 예를 들어 SK텔레콤은 A.X 4.0이 KMMLU에서 78.3점을 기록해 GPT-4o(72.5점)를 상회했다고 발표했습니다. 다만 벤치마크 점수는 제공사 자체 발표에 기반한 경우가 많으므로, 도입 전 자사 업무 데이터 기반의 별도 평가(RAG 정확도, 도메인 용어 처리 등)를 병행하는 것을 권장합니다.

## 벤더 생태계 구도

이들 중 네이버클라우드, 업스테이지, SK텔레콤, NC AI, LG AI연구원은 정부의 「독자 AI 파운데이션 모델」 프로젝트 1차 정예팀으로 선정된 바 있으나, 2025년 12월 1차 단계평가에서 네이버클라우드와 NC AI가 탈락하고 모티프테크놀로지스가 추가 합류하는 등 구도가 계속 바뀌고 있습니다. 자세한 선정 경과는 [소버린 AI·독자 파운데이션 모델 정책](sovereign-fm-policy.md) 문서를 참고하세요. NC AI는 이후 범용 LLM보다 3D·음성·번역 등 버티컬 생성 AI로 포지셔닝을 이동하는 모습을 보이고 있습니다.

## 글로벌 모델 대비 선택 기준

국내 FM과 GPT·Gemini·Claude 등 글로벌 모델 중 무엇을 선택할지는 벤더 우열이 아니라 **워크로드 요건**에 따라 판단해야 합니다.

- **규제·주권 요건**: 망분리 규제([망분리와 네트워크 격리](../security/network-isolation.md) 참고)나 공공 조달([CSAP](../security/csap.md) 참고) 대상 워크로드는 국내 리전에서 서비스되는 모델이 유리한 경우가 많습니다. 데이터가 해외로 이전되면 안 되는 워크로드는 국내 제공사의 국내 데이터센터 기반 API를 우선 검토하세요.
- **한국어·도메인 특화 성능**: 일반 상식·추론은 글로벌 최상위 모델이 여전히 앞서는 경우가 많지만, 한국어 어휘·존댓말·업계 용어 처리에서는 국내 모델이 강점을 보이는 사례가 보고됩니다. 반드시 자체 벤치마크로 검증하세요.
- **라이선스와 커스터마이징**: 카카오 Kanana, NC AI VARCO, SKT A.X는 상업적 이용이 가능한 오픈소스로 자체 인프라에 파인튜닝·배포가 가능합니다. 반면 EXAONE은 상업 이용 시 별도 계약이, Solar와 HyperCLOVA X 상위 모델은 API 이용이 기본 경로입니다. 온프레미스·VPC 폐쇄망 배포가 필요하면 라이선스 조건을 가장 먼저 확인해야 합니다.
- **벤더 지속가능성**: 소버린 AI 프로젝트의 단계평가 결과에서 보듯 국내 FM 생태계는 아직 유동적입니다. 특정 벤더에 장기 종속되는 아키텍처보다 API 게이트웨이를 통해 모델을 교체 가능하게 구성하는 것이 리스크를 줄입니다.
- **비용**: 업스테이지 Solar Pro 2는 100만 토큰당 0.5달러 수준으로 공개되는 등 국내 모델이 가격 경쟁력을 내세우는 경우가 있습니다. 다만 초당 처리량, 컨텍스트 길이 등 조건이 다르므로 단순 토큰 단가만으로 비교하지 마세요.
- **에이전틱·멀티모달 지원**: 카카오 Kanana-2, KT 믿:음 K, NC AI VARCO-VISION 등은 에이전틱 AI·멀티모달을 별도 라인업으로 강화하는 추세입니다. 단순 텍스트 생성을 넘어서는 유스케이스라면 해당 라인업의 성숙도를 별도로 확인하세요.

## 요구사항별 채널 선택 가이드

1P(모델사 직접)·3P(클라우드 제공) 채널 구분과 평가 축은 [1P vs 3P](../../ai/1p-vs-3p.md)를 참고하세요. 한국 엔터프라이즈의 전형적인 요구사항별 권장 채널은 다음과 같습니다.

| 요구사항 | 권장 채널 |
| --- | --- |
| 한국어 특화 + 멀티클라우드 | Upstage Solar, LG EXAONE (1P 또는 AWS/Azure Marketplace) |
| 데이터 주권 / 망분리 | 온프레미스(Upstage, EXAONE, Llama) 또는 국내 리전 3P |
| 기존 AWS/Azure 커밋 소진 | 3P (Bedrock / Azure Foundry / Marketplace) |
| 최신 글로벌 FM 즉시 접근 | 1P (OpenAI, Anthropic 직접) |
| 금융/공공 컴플라이언스 | 3P (클라우드 인증 상속) + 온프레미스 하이브리드 |
| 독자파운데이션모델 정책 대응 | 정책 참여 모델 확인 후 채널 선택 (공공/금융 조달 시) |

## 도입 체크리스트

- [ ] 워크로드가 망분리·CSAP 대상인지 확인했는가 (대상이면 국내 리전 API를 우선 검토)
- [ ] 자체 업무 데이터로 한국어·도메인 벤치마크를 재현했는가 (제공사 발표 수치만으로 판단하지 않음)
- [ ] 온프레미스/VPC 폐쇄망 배포가 필요한 경우, 해당 모델의 라이선스가 상업적 파인튜닝·재배포를 허용하는지 확인했는가
- [ ] 특정 벤더 API에 강결합되지 않도록 게이트웨이/추상화 계층을 두었는가
- [ ] 선택한 벤더가 소버린 AI 프로젝트 평가 등 정책 변수에 노출되어 있는지 확인했는가
- [ ] 토큰 단가뿐 아니라 컨텍스트 길이, 처리량(TPS), SLA를 함께 비교했는가

## 관련 문서

- [소버린 AI·독자 파운데이션 모델 정책](sovereign-fm-policy.md)
- [CSAP (클라우드 보안 인증)](../security/csap.md)
- [망분리와 네트워크 격리 (한국)](../security/network-isolation.md)
- [소버린 랜딩존](../../governance/landing-zone.md#소버린-랜딩존-sovereign-landing-zone)

## 참고하기

- [네이버클라우드, 경량 옴니모달 모델 공개…"국방 환경 최적화" — 전자신문](https://www.etnews.com/20260615000237)
- [네이버, 최상급 언어 능력 갖춘 추론모델 'HyperCLOVA X' — 네이버클라우드](https://www.navercloudcorp.com/ko/media/pressrelease/view/?seq=33058)
- [차세대 하이브리드 AI, EXAONE 4.0 공개 — LG AI Research](https://www.lgresearch.ai/blog/view?seq=575)
- [LG Reveals Next-Gen Multimodal AI 'EXAONE 4.5' — PR Newswire](https://www.prnewswire.com/news-releases/lg-reveals-next-gen-multimodal-ai-exaone-4-5-302736993.html)
- [카카오, 업데이트된 'Kanana-2' 모델 4종 오픈소스로 추가 공개 — 카카오](https://www.kakaocorp.com/page/detail/11904)
- [카카오, 경량 언어모델 4종 오픈소스로 공개... "글로벌 수준 성능" — 카카오](https://www.kakaocorp.com/page/detail/12089)
- [더 똑똑해진 카카오의 언어모델 Kanana 1.5, 상업 활용 가능한 오픈소스 공개 — tech.kakao.com](https://tech.kakao.com/posts/706)
- [KT, MWC26서 '믿:음 K' 공개…에이전틱 AI 파트너 선언 — 아주경제](https://www.ajunews.com/view/20260226085637155)
- [Solar Pro 2 – 최첨단 추론, 도구 활용, 다국어 성능을 갖춘 310억 파라미터 LLM — Upstage](https://www.upstage.ai/blog/ko/solar-pro-2-launch)
- [Upstage Releases Next-Generation "Solar Pro" Generative AI LLM on AWS — AWS Press Center](https://press.aboutamazon.com/aws/2024/12/upstage-releases-next-generation-solar-pro-generative-ai-llm-on-aws)
- ["국내 원조 LLM '바르코', 더 강력하고 똑똑한 멀티모달로 돌아왔다"...NC AI, 'VARCO-VISION 2.0' 공개 — 인공지능신문](https://www.aitimes.kr/news/articleView.html?idxno=35689)
- [SK텔레콤, 에이닷 엑스 4.0 지식형 모델 오픈소스로 공개 — SK텔레콤 뉴스룸](https://news.sktelecom.com/213534)
- [GitHub - SKT-AI/A.X-4.0](https://github.com/SKT-AI/A.X-4.0)
