---
title: "Domestic Foundation Model Provider Comparison"
description: "Compares the models, licenses, and delivery channels of domestic FM providers in Korea, including Naver, LG AI Research, Kakao, KT, Upstage, NC AI, and SKT."
---

> Last reviewed: August 2026

## Overview

Korea has a large number of foundation model (FM) providers, ranging from conglomerate affiliates to startups. This document summarizes the latest models, licensing structures, and delivery channels of the major providers, and covers what to consider when choosing a domestic model over a global one.

:::note
Model versions and license terms change quickly. The table below reflects the state as of August 2026 — reconfirm the latest terms in each provider's official documentation before adoption.
:::

## Provider Landscape

| Provider | Flagship model | Latest version (as of Aug 2026) | License | Key delivery channels |
| --- | --- | --- | --- | --- |
| Naver (Cloud) | HyperCLOVA X | SEED (lightweight/open), THINK (reasoning-focused), and DASH (lightweight, high-speed) lineups. SEED 32B THINK/8B Omni released Dec 2025; SEED 4B omni-modal (defense-specialized) released H1 2026 | Some SEED-series models (0.5B–3B class) are open-sourced; higher-tier models are API-only | Naver Cloud CLOVA Studio API (Basic/Exclusive/Neurocloud plans) |
| LG AI Research | EXAONE | EXAONE 4.0 (hybrid reasoning), EXAONE 4.5 (multimodal) | Free for research/education use; **commercial use requires a separate license agreement with LG AI Research** | Published on Hugging Face, LG AI Research's own API, expanding licensing for educational institutions |
| Kakao | Kanana | Kanana-2 series (4 models updated Jan 2026), 4 lightweight Kanana-2 SLMs (Jul 2026, 1.3B/3B) | Kanana Open License based on Apache 2.0 — **commercial use permitted** | Open-source distribution via Hugging Face. Optimized for on-device deployment |
| KT | Mi:dm (믿:음) | Mi:dm K 2.5 Pro (Feb 2026, unveiled at MWC26). Predecessor Mi:dm K 2.0 (Jul 2025) consisted of a Base 11.5B model plus an on-device Mini 2.3B | Primarily delivered via proprietary service/B2B channels (limited public license information) | B2B/B2G delivery through KT's own enterprise AI platform (AICC, chatbots, document recognition, legal/financial specialization, etc.) |
| Upstage | Solar | Solar Pro 2 (31B, hybrid chat/reasoning, officially launched Jul 2025) | Closed API service (not open source) | Upstage Console API, Amazon Bedrock Marketplace, AWS SageMaker JumpStart, AWS Marketplace |
| NC AI | VARCO | VARCO-VISION 2.0 (Jul 2025, 4 open-source multimodal models), VARCO 3D 2.0, VARCO Voice (multilingual speech) | Open source (varies by model) | Hugging Face, AWS SageMaker-based infrastructure. Domain-data customization support planned via AWS Private Cloud |
| SK Telecom | A.X | A.X 4.0 (open-sourced Apr 30, 2025). Built on Qwen2.5 with extensive additional Korean-language training | Open source | GitHub/Hugging Face, integrated with SKT's own service ('A.') |

## Korean-Language Performance and Benchmarks

Korean LLM evaluation commonly uses benchmarks such as KMMLU (Korean knowledge understanding), KoBEST, and HAE-RAE. For example, SK Telecom reported that A.X 4.0 scored 78.3 on KMMLU, surpassing GPT-4o's 72.5. That said, benchmark scores are often based on providers' own self-reported figures, so it's advisable to also run a separate evaluation against your own business data (RAG accuracy, domain-terminology handling, etc.) before adoption.

## The Vendor Ecosystem Landscape

Among these providers, Upstage, SK Telecom, and LG AI Research passed the government's Independent AI Foundation Model project second phase evaluation (results announced August 18, 2026) and advanced to the third phase. Motif Technologies, despite ranking 1st globally on the AAII index (47 points, the only Korean model in the global top 10), was eliminated due to low user evaluation scores (usability and applicability). Naver Cloud and NC AI had already been eliminated in the first phase evaluation (January 2026). NC AI, meanwhile, has shown signs of repositioning away from general-purpose LLMs and toward vertical generative AI in 3D, voice, and translation. See [Sovereign AI and Independent Foundation Model Policy](../sovereign-fm-policy/) for the full selection timeline.

## Channel Choice for Korean Enterprises

| Requirement | Recommended Channel |
| --- | --- |
| Korean-language specialization + multi-cloud | Upstage Solar, LG EXAONE (1P or AWS/Azure Marketplace) |
| Data sovereignty / network segregation | On-premises (Upstage, EXAONE, Llama) or a domestic-region 3P |
| Consuming existing AWS/Azure commits | 3P (Bedrock / Azure Foundry / Marketplace) |
| Immediate access to the latest global FMs | 1P (OpenAI, Anthropic direct) |
| Financial/public-sector compliance | 3P (inheriting cloud certifications) + on-premises hybrid |
| Responding to sovereign foundation model policy | Confirm which models participate in the policy before choosing a channel (for public-sector/financial procurement) |

The global 1P/3P patterns themselves are covered in [1P vs 3P Model Delivery](../../ai/1p-vs-3p/).

## Selection Criteria Versus Global Models

Choosing between a domestic FM and a global model such as GPT, Gemini, or Claude should be based not on which vendor is "better" but on **workload requirements**.

- **Regulatory and sovereignty requirements**: workloads subject to network separation regulation (see [Network Separation and Isolation](../security/network-isolation/)) or public-sector procurement (see [CSAP](../security/csap/)) often benefit from models served in a domestic region. If a workload's data must not be transferred abroad, prioritize domestic providers' APIs backed by domestic data centers.
- **Korean-language and domain-specific performance**: top-tier global models often still lead on general knowledge and reasoning, but domestic models are reported to hold an edge in handling Korean vocabulary, honorifics, and industry-specific terminology. Always verify with your own benchmarks.
- **Licensing and customization**: Kakao Kanana, NC AI VARCO, and SKT A.X are open source with commercial use permitted, allowing fine-tuning and deployment on your own infrastructure. EXAONE, by contrast, requires a separate agreement for commercial use, and the higher-tier Solar and HyperCLOVA X models are primarily accessed via API. If on-premises or closed-VPC deployment is required, check license terms first.
- **Vendor sustainability**: as shown by the phase-evaluation results of the sovereign AI project, Korea's domestic FM ecosystem is still in flux. Configuring models to be swappable via an API gateway reduces risk compared to an architecture that's deeply locked into a specific vendor.
- **Cost**: Upstage's Solar Pro 2 has been advertised at around $0.5 per million tokens, and domestic models sometimes lead with price competitiveness. However, throughput and context length vary, so don't compare providers on token price alone.
- **Agentic and multimodal support**: Kakao Kanana-2, KT's Mi:dm K, and NC AI's VARCO-VISION are increasingly building out agentic AI and multimodal capabilities as separate product lines. For use cases beyond plain text generation, verify the maturity of the relevant lineup separately.

## Adoption Checklist

- [ ] Have you confirmed whether the workload is subject to network separation or CSAP requirements? (if so, prioritize domestic-region APIs)
- [ ] Have you reproduced Korean-language/domain benchmarks against your own business data? (don't rely solely on provider-reported figures)
- [ ] If on-premises/closed-VPC deployment is needed, have you confirmed the model's license permits commercial fine-tuning and redistribution?
- [ ] Have you put a gateway/abstraction layer in place to avoid tight coupling to a specific vendor's API?
- [ ] Have you checked whether your chosen vendor is exposed to policy variables such as the sovereign AI project's evaluation process?
- [ ] Have you compared context length, throughput (TPS), and SLA — not just token price?

## Related Documents

- [Sovereign AI and Independent Foundation Model Policy](../sovereign-fm-policy/)
- [CSAP (Cloud Security Assurance Program)](../security/csap/)
- [Network Separation and Isolation (Korea)](../security/network-isolation/)
- [Sovereign Landing Zone](../../../governance/landing-zone/#sovereign-landing-zone)

## References

- [Naver Cloud unveils lightweight omni-modal model…"optimized for defense environments" — Electronic Times](https://www.etnews.com/20260615000237)
- [Naver's top-tier reasoning model with advanced language capability, 'HyperCLOVA X' — Naver Cloud](https://www.navercloudcorp.com/ko/media/pressrelease/view/?seq=33058)
- [Next-generation hybrid AI, EXAONE 4.0 unveiled — LG AI Research](https://www.lgresearch.ai/blog/view?seq=575)
- [LG Reveals Next-Gen Multimodal AI 'EXAONE 4.5' — PR Newswire](https://www.prnewswire.com/news-releases/lg-reveals-next-gen-multimodal-ai-exaone-4-5-302736993.html)
- [Kakao adds 4 updated 'Kanana-2' models, released as open source — Kakao](https://www.kakaocorp.com/page/detail/11904)
- [Kakao releases 4 lightweight language models as open source... "global-level performance" — Kakao](https://www.kakaocorp.com/page/detail/12089)
- [Kakao's smarter language model Kanana 1.5, now open source for commercial use — tech.kakao.com](https://tech.kakao.com/posts/706)
- [KT unveils 'Mi:dm K' at MWC26…declares itself an agentic AI partner — Ajunews](https://www.ajunews.com/view/20260226085637155)
- [Solar Pro 2 – a 31-billion-parameter LLM with state-of-the-art reasoning, tool use, and multilingual performance — Upstage](https://www.upstage.ai/blog/ko/solar-pro-2-launch)
- [Upstage Releases Next-Generation "Solar Pro" Generative AI LLM on AWS — AWS Press Center](https://press.aboutamazon.com/aws/2024/12/upstage-releases-next-generation-solar-pro-generative-ai-llm-on-aws)
- ["Korea's original LLM 'VARCO' returns, more powerful and multimodal"...NC AI unveils 'VARCO-VISION 2.0' — AI Times Korea](https://www.aitimes.kr/news/articleView.html?idxno=35689)
- [SK Telecom releases A.dot X 4.0 knowledge model as open source — SK Telecom Newsroom](https://news.sktelecom.com/213534)
- [GitHub - SKT-AI/A.X-4.0](https://github.com/SKT-AI/A.X-4.0)
