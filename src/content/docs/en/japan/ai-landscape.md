---
title: "Japan's AI Policy and Domestic Model Landscape"
description: "Covers Japan's AI Act (AI推進法) and AI Basic Plan, the Ministry of Economy, Trade and Industry's GENIAC program, the domestic LLM landscape (NTT tsuzumi, NEC cotomi, PFN PLaMo, and others), and the government procurement channel Gennai (源内)."
---

> Last reviewed: August 2026

## Overview

On May 28, 2025, Japan enacted the "Act on the Promotion of Research, Development, and Utilization of AI-Related Technologies" (commonly known as the **AI Act**, AI推進法 or AI新法), promulgating it on June 4 and bringing it into full effect on September 1. Based on this Act, the **AI Strategy Headquarters (人工知能戦略本部)** was established on that same September 1, elevated to a statutory body chaired by the Prime Minister with the full Cabinet participating, taking over the role previously played by the advisory AI Strategy Council (AI戦略会議).

At the AI Strategy Headquarters' first meeting on September 12, Prime Minister Ishiba directed that an AI Basic Plan be developed around four pillars — ① using AI (使う), ② creating AI (創る), ③ increasing AI's trustworthiness (信頼性を高める), and ④ collaborating with AI (協働する) — and on December 23, 2025, the Cabinet adopted the "AI Basic Plan — 'Japan's Resurgence' through 'Trustworthy AI'" (人工知能基本計画 ～「信頼できるAI」による「日本再起」～). This plan was updated with a revised edition on July 14, 2026, and as of this document's August 2026 reference date, the revised edition is the version currently in effect.

:::note
Rather than centering on ex-ante regulation like the EU AI Act, Japan's AI policy makes clear its **promotion-first** stance: promote adoption first, then investigate and respond to problems after the fact. The AI Act itself places more weight on establishing a national strategy and promotion framework than on direct penalty provisions targeting businesses.
:::

## GENIAC — METI's Program to Strengthen Generative AI Development Capacity

**GENIAC** (Generative AI Accelerator Challenge) is a program jointly operated by the Ministry of Economy, Trade and Industry (METI) and NEDO (New Energy and Industrial Technology Development Organization), aimed at cultivating the foundation-model development capacity of Japanese companies and research institutions. As of August 2026, GENIAC consists of the following tracks.

- Foundation model development projects
- Data utilization demonstration projects
- AI-readiness of manufacturing data (9 new themes adopted in May 2026)
- Robotics foundation model development (2 new themes adopted in May 2026)
- Data ecosystem development and other initiatives (9 new themes adopted in July 2026)
- The prize-based **GENIAC-PRIZE** program (a separate track)

Rather than concentrating investment in one or two companies, GENIAC distributes GPU computing resources and data across a large number of company and university consortia to promote competition. Many of the major domestic model developers discussed below — NTT, NEC, PFN, Sakana AI, ELYZA, and others — have received GENIAC support or participated in related consortia at some point.

## Landscape of Domestic Foundation Models (as of August 2026)

| Company/Model | Developer | Characteristics |
| --- | --- | --- |
| **tsuzumi 2** | NTT | Released October 2025. A lightweight model with roughly 30 billion parameters that can run on a single H100 GPU, notable for requiring a small amount of training data for domain-specific tuning |
| **cotomi v3** | NEC | An in-house NEC LLM, with strengths in lightweight, high-speed inference |
| **Sarashina2 mini** | SoftBank (SB Intuitions) | Developed by SB Intuitions, a SoftBank subsidiary. Industry-specific collaborations underway, including a jointly developed finance-specific model with Mizuho Financial Group |
| **Llama-3.1-ELYZA-JP-70B** | ELYZA (a KDDI subsidiary) | A startup founded out of the University of Tokyo research lab of Professor Yutaka Matsuo. KDDI acquired a 43.4% stake in 2024, making it a consolidated subsidiary. Numerous enterprise adoption cases in finance, insurance, and local government |
| **PLaMo series (2.0 Prime → 3.0 Prime)** | Preferred Networks (PFN) | Began offering PLaMo 2.0 Prime as a trial model for Gennai (源内) in March 2026; launched PLaMo 3.0 Prime for general release in June (reasoning/non-reasoning models, up to 256K-token context). Lineup diversified with the edge-device model PLaMo-VL and the translation-specific PLaMo翻訳 |
| **Takane 32B** | Fujitsu | An in-house Fujitsu LLM |
| **Sakana AI's model family** | Sakana AI | Founded in Tokyo by former Google researchers. Uses proprietary research techniques such as evolutionary model merging. Raised roughly ¥32 billion (approximately $200 million) in a Series B round in November 2025, valuing the company at roughly ¥400 billion (approximately $2.65 billion). Entered a strategic partnership with Google in January 2026 |
| **rinna model family** | rinna | Runs consumer-facing services such as the conversational character AI "AI Rinna" (over 8 million followers) alongside development of Japanese-specialized open models |

:::caution
The parameter counts and performance figures in the table above reflect each company's disclosures as of the time stated, and model versions are updated on the order of months. When evaluating adoption, check each company's official announcements for the latest version and licensing terms.
:::

## The Government Procurement Channel — Gennai (源内, Gennai)

The Digital Agency has developed and operates **Gennai (源内)** in-house, a generative AI environment for use by government employees. Gennai is designed so that users can choose between global models — such as AWS Nova Lite and Anthropic Claude (Haiku/Sonnet 4.5, 4.6) — and domestic models alike.

- **March 6, 2026**: seven proposals were selected for trial as domestic LLMs with government procurement in mind — NTT Data's tsuzumi 2, KDDI/ELYZA's Llama-3.1-ELYZA-JP-70B, SoftBank's Sarashina2 mini, NEC's cotomi v3, Fujitsu's Takane 32B, PFN's PLaMo 2.0 Prime, and Custom Cloud's CC Gov-LLM.
- **May 2026**: of the seven selected proposals, formal contracts were signed with **five companies**, and the models deployed in the large-scale trial (on the Sakura environment) were narrowed down to **three**.
- **May 2026**: a large-scale trial began across all ministries (39 agencies), targeting roughly 180,000 users, expanding in stages (about 100,000 users as of May 2026, with the Ministry of Defense, MEXT, and others being added to reach the 180,000 target from June onward).
- **August 2026**: the domestic LLM evaluation environment is scheduled to be built (a stage preceding formal trial use within Gennai).
- **September–November 2026 (planned)**: A/B trial experiments are planned for the three domestic LLM models above.
- **January 2027 (planned)**: partial disclosure of evaluation and verification results.
- **April 2027 (planned)**: paid procurement begins for models that performed well.
- **April 24, 2026**: some Gennai functionality was open-sourced on GitHub under the MIT License and CC BY 4.0, aimed at supporting local governments and others in building their own AI infrastructure.

:::note
The results of Gennai's trials and procurement are functioning as a de facto benchmark through which domestic LLMs are validated in a real government operating environment. Organizations considering AI business targeting the public sector can treat the paid procurement results expected in 2027 as a key milestone to watch.
:::

## Cloud Delivery Channels

Most domestic models are distributed through (1) the developer's own API/platform (PLaMo API, Chat, Lite, etc.), (2) hyperscaler marketplaces and partnerships, and (3) government procurement channels such as Gennai. However, which hyperscaler marketplace a given model is officially listed on varies by company and by point in time and must be checked individually (verification needed). When adopting these models, enterprises should confirm not only the model's own performance but also which cloud environment provides it, and whether that environment offers the required SLA, region, and security certification (such as ISMAP).

## Practical Implications

- **A distributed rather than a concentrated competitive structure**: rather than concentrating resources on one or two national-champion models, Japan's approach is closer to supporting a large number of companies and consortia through GENIAC and letting them compete in the real-world government usage channel of Gennai, with strong models identified after the fact. Rather than designing for long-term lock-in to a single vendor, **a gateway/abstraction layer that treats the FM as a swappable component** is advantageous for risk management.
- **Gennai as a public procurement signal**: the results of Gennai's trials and procurement (expected in 2027) are likely to become a de facto authoritative indicator of which domestic models have been validated at government-scale workloads. Organizations targeting Japan's public sector or regulated industries should factor this timeline into their procurement roadmap.
- **The rise of industry-specific models**: with a growing number of industry-specific collaborations — Sarashina (finance), ELYZA (insurance, local government) — regulated-industry workloads may increasingly call for industry-specific domestic models rather than general-purpose ones.
- **Comparison with Korea's sovereign FM policy**: Korea, led by the Ministry of Science and ICT, takes a **top-down approach** through its [Independent AI Foundation Model Project](../../korea/ai/sovereign-fm-policy/), narrowing down to a small elite group of teams (four teams as of August 2026) through a six-month tournament cycle with concentrated GPU and budget support, whereas Japan is closer to a **bottom-up approach**, providing broad, distributed support through GENIAC and letting the market select strong models after the fact through real-world competition in Gennai. Both approaches ultimately share the goal of cultivating sovereign models tied to public procurement, but they carry different practical implications for the fluidity of the vendor ecosystem and the predictability of procurement timing.

## References

- [Full Enforcement of the AI Act — Cabinet Office (October 3, 2025)](https://www.cao.go.jp/press/new_wave/20251003.html)
- [Report on Domestic Developments Including the AI Act (Ministry of Internal Affairs and Communications, December 2, 2025)](https://www.soumu.go.jp/main_content/001043230.pdf)
- [First Meeting of the AI Strategy Headquarters (Prime Minister's Office, September 12, 2025)](https://www.kantei.go.jp/jp/103/actions/202509/12jinkoutchinou.html)
- [AI Basic Plan (Cabinet Office, adopted by the Cabinet on December 23, 2025)](https://www8.cao.go.jp/cstp/ai/ai_plan/aiplan_20251223.pdf)
- [AI Basic Plan — Latest Version Page (Cabinet Office, updated July 14, 2026)](https://www8.cao.go.jp/cstp/ai/ai_plan/ai_plan.html)
- [AI Strategy — Cabinet Office Council for Science, Technology and Innovation](https://www8.cao.go.jp/cstp/ai/index.html)
- [GENIAC Official Page (METI)](https://www.meti.go.jp/policy/mono_info_service/geniac/index.html)
- [New GENIAC Themes Adopted for Data Ecosystem Development and More (METI, July 2, 2026)](https://www.meti.go.jp/press/2026/07/20260702001/20260702001.html)
- [New GENIAC Themes Adopted for Manufacturing AI-Readiness and Robotics Foundation Models (METI, May 14, 2026)](https://www.meti.go.jp/press/2026/05/20260514001/20260514001.html)
- [Government AI (源内) Initiatives — Cabinet Secretariat (February 2026)](https://www.cas.go.jp/jp/seisaku/gskaigi/ebpm/dai1/shiryo8.pdf)
- [Gennai Domestic LLM Contracts Signed with Five Companies — Digital Agency (May 2026)](https://www.digital.go.jp/news/207cadc2-c218-42f6-92ec-c0eda476b49c)
- [Gennai Domestic LLM Trial Plan (A/B Experiment Schedule) — Digital Agency (July 2026)](https://www.digital.go.jp/news/7eef939d-1c58-4229-b210-7b5adc9af590)
- [Government-Certified AI Selection: Seven Domestic Models Under Trial — ITmedia (March 6, 2026)](https://www.itmedia.co.jp/aiplus/article/2603/06/1260306097/)
- [PLaMo 3.0 Prime General Release — Preferred Networks (June 22, 2026)](https://www.preferred.jp/ja/news/pr20260622)
- [PLaMo Selected as a Digital Agency Government AI Trial Model — Preferred Networks (March 12, 2026)](https://www.preferred.jp/ja/news/pr20260312)
- [Sakana AI Series B Coverage (Ledge.ai reports a differing figure; see official announcement below for the confirmed amount) — Ledge.ai](https://ledge.ai/articles/sakana_ai_series_b_200oku_fundraising)
- [Sakana AI Enters Strategic Partnership with Google — Business+IT](https://www.sbbit.jp/article/cont1/179274)
- [KDDI Makes ELYZA a Subsidiary — Nikkei xTECH](https://xtech.nikkei.com/atcl/nxt/news/24/00421/)
- [Sakana AI Series B (Approximately ¥32 Billion / $200 Million) Official Announcement — Sakana AI](https://sakana.ai/series-b/)
- [Independent AI Foundation Model Policy (Korea, for comparison)](../../korea/ai/sovereign-fm-policy/)
