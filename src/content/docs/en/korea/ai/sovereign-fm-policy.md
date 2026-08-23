---
title: "Sovereign AI and Independent Foundation Model Policy"
description: "Covers the Korean government's sovereign AI policy, the selection process for its independent AI foundation model project, and implications for enterprise architects."
---

> Last reviewed: August 2026 (second phase evaluation results reflected)

## Overview

Sovereign AI refers to a country securing, through its own technology, AI models and infrastructure optimized for its own data, language, culture, and industrial context. Concerned about technological, economic, and cultural dependence on global AI models, the Korean government has made "becoming one of the world's top three AI powers" a core national goal, pursuing the development of an independent foundation model alongside the buildout of national AI infrastructure.

This document covers the progress of that policy initiative as of August 2026, and the implications for enterprise architects to consider.

## The Independent AI Foundation Model Project

### Purpose and Scale

The Independent AI Foundation Model project, led jointly by the Ministry of Science and ICT (MSIT) and the National IT Industry Promotion Agency (NIPA), aims to develop a domestic foundation model competitive with top-tier global models such as GPT and Gemini. Selected development teams receive concentrated support in the form of GPU infrastructure, training data, and project funding.

Under the first supplementary budget, the GPU lease support budget is approximately **KRW 157.6 billion** (data and talent support are separate line items). The overall project budget is not officially confirmed — media reports vary widely, ranging from roughly KRW 200 billion to KRW 530 billion (phase-by-phase budgets may also be adjusted during the funding review process).

:::note
Korea's AI capability was ranked around 6th in the world as of 2024, and the government frames this project as the first gateway to becoming one of the "top three AI powers," after the United States and China.
:::

### Selection Method — Phased Narrowing Through Competition

The project was designed as a **tournament-style competitive structure**: it selects multiple teams up front, then runs a phase evaluation every six months to progressively narrow the field, ultimately leaving just two teams standing.

### Selection Timeline (July 2025 – August 2026)

| Date | Development |
| --- | --- |
| July 21, 2025 | Elite-team application deadline — 15 teams applied in total |
| July 25, 2025 | 10 teams confirmed as having passed the written evaluation |
| August 2025 | After a presentation evaluation, **5 first-round elite teams** were finalized — Naver Cloud, Upstage, SK Telecom, NC AI, and LG AI Research |
| December 30, 2025 | First phase evaluation presentation (interim results disclosed) |
| January 15, 2026 | First phase evaluation results officially announced — **Naver Cloud and NC AI eliminated**; 3 teams (LG AI Research, SK Telecom, Upstage) survive, and an additional open call begins |
| January 15, 2026 | Government announces an additional open call for one elite team to fill the gap left by the eliminated teams |
| February 12, 2026 | Additional application deadline (two consortia applied: Motif Technologies and Trillion Labs) |
| February 20, 2026 | **Motif Technologies** is selected and joins as the 4th elite team |
| August 8–11, 2026 | **Second phase evaluation** conducted, covering 4 teams — LG AI Research, SK Telecom, Upstage, and Motif Technologies. Combining global benchmarks, expert review, and evaluation by a 200-person citizen panel |
| August 18, 2026 | **Second phase evaluation results announced** — **Upstage, SK Telecom, and LG AI Research** advance to the third phase; **Motif Technologies eliminated**. Motif scored 47 points on the global AAII (the only Korean model in the global top 10) but scored only 14.1 points in user evaluations (usability and applicability), resulting in an overall score of 65.8 and elimination. Third-phase teams will receive approximately 1,000 B200 GPUs each (roughly ₩40 billion per team, ₩120 billion total) |
| August 18, 2026 | Government announces review of strategic restructuring beyond "Dokpamo" toward **frontier-level AI model development**. Acknowledging the limits of the existing distributed competition model, the government is exploring plans to link and integrate related projects (including Dokpamo and Mitos-level frontier AI development). Both an SPC (special-purpose company) involving multiple firms and a single-company-led approach remain under consideration |

:::caution
Following the second phase evaluation results, objection and appeal procedures for Motif Technologies are expected to proceed. The third phase evaluation will commence after those procedures conclude, selecting the final two teams. The specific direction of the government's frontier AI strategy restructuring (including whether the Dokpamo initiative will continue) is to be announced separately.
:::

## National AI Infrastructure — The National AI Computing Center

Separately from the independent model development effort, the government is building national AI computing infrastructure to supply GPUs.

- The government has announced a roadmap targeting **more than 50,000 GPUs**, supplying them to K-LLM development teams on a lease basis.
- On August 3, 2026, a groundbreaking ceremony for the **National AI Computing Center** was held at the Solasido Data Center Park site in Haenam County, South Jeolla Province, formally starting construction. The first-phase buildout is reported at roughly 15,000 chips.
- As of August 2026, the GPU model has reportedly not yet been finalized ("B200 not confirmed"), with the latest AI chips under consideration.
- In February 2026, the government codified sovereign-AI-related policy as a pillar of national AI strategy through the "AI Basic Plan (2026–2028)."

## Implications for Enterprise Architects

- **A shifting vendor landscape**: Following the second phase evaluation (August 18, 2026), three teams (LG AI Research, SK Telecom, Upstage) advance to the third phase, where the final two will be selected. Additionally, the government is exploring restructuring toward frontier-level AI development, meaning the program structure itself may change. Rather than fully committing your architecture to any single team's long-term roadmap, maintaining a **gateway/abstraction layer that treats the FM as a swappable component** is the safer approach to risk management.
- **Technical excellence ≠ selection**: In the second evaluation, Motif Technologies ranked 1st on the AAII global index (47 points, global top 10) but was eliminated due to low scores on user evaluation (usability and applicability). This signals that the government weighs actual service quality and industrial applicability more heavily than pure benchmark performance.
- **Connection to public-sector and regulated procurement**: models from vendors selected as elite teams are likely to be prioritized as "domestic sovereign model" candidates in public-sector and regulated-industry procurement. Organizations targeting the public sector should factor the eventual surviving team(s) into their procurement roadmap.
- **Frontier AI strategy shift**: The government recognizes the limits of the distributed competition model and is exploring resource concentration through mechanisms such as SPCs (special-purpose companies). This suggests the domestic FM ecosystem may shift from a multi-party competition to a concentrated, few-player structure.
- **Interaction with sovereignty requirements**: sovereign AI policy moves in tandem with other regulatory tracks such as [CSAP](../../security/csap/) and [network separation easing](../../security/network-isolation/). Workloads handling sensitive data should anticipate being required to use a domestic sovereign model instead of a global one.
- **Timing of GPU infrastructure availability**: the National AI Computing Center is still at the groundbreaking stage as of August 2026, and real service availability will take time. Organizations looking to adopt a domestic FM in the near term should take the more practical approach of accessing models through the vendor API/cloud delivery channels covered in [FM Provider Comparison](../fm-providers/).
- **Performance baseline**: the government has set the goal for the independent model at "95% or more of the performance of top-tier global models." Organizations evaluating adoption should treat this figure as a benchmark and separately validate performance on their own actual business tasks.

## Common Mistakes

- **Signing long-term contracts on the assumption that the final surviving teams are already settled** — as of August 2026, the third phase evaluation (among Upstage, SK Telecom, and LG AI Research) will determine the final two teams, and the government's frontier AI strategy restructuring may change the program structure entirely. Fully subordinating procurement to a specific team's roadmap is risky.
- **Oversimplifying "sovereign AI" as "domestic models, no exceptions"** — sovereign AI policy exists to secure alternatives for certain sensitive workloads (public sector, national security, regulated data), not to mandate converting every workload to a domestic model. Judge requirements on a per-workload basis.
- **Overestimating how soon the National AI Computing Center will be available** — as of August 2026 it is still at the groundbreaking stage, and actual service delivery will take considerable time. It's safer not to factor it into near-term adoption plans.

## References

- [Results of the elite-team open call for the "Independent AI Foundation Model" project — Ministry of Science and ICT](https://www.msit.go.kr/bbs/view.do?sCode=user&mId=307&mPid=208&bbsSeqNo=94&nttSeqNo=3186026)
- [5 elite teams confirmed for the Independent AI Foundation Model project — Byline Network](https://byline.network/2025/08/8042/)
- [First-round results of the Independent AI Foundation Model project revealed — Byline Network](https://byline.network/2025/12/30-493/)
- ['Dokpamo' first round: Naver and NC AI both eliminated…Government opens additional call for one elite team — ZDNet Korea](https://zdnet.co.kr/view/?no=20260115150326)
- [Korea's national AI team enters second-round selection…4 teams narrowing to 3 this month — ZDNet Korea](https://zdnet.co.kr/view/?no=20260803164056)
- [Dokpamo second phase evaluation begins on the 8th…200-person citizen panel to evaluate 'K-AI' — Byline Network](https://byline.network/2026/08/0806-3/)
- [Second Round of Dokpamo: Upstage, SKT, and LG Corp.… Reasons for Motif's Elimination from AAII Top Spot — Edaily](https://en.edaily.co.kr/news/eda202608185493/)
- [Government goes all-in on securing GPUs for 'sovereign AI'…reviewing extension of KRW 3 trillion program — Electronic Times](https://www.etnews.com/20260707000304)
- ["Building the AI highway in earnest"…National AI Computing Center kicks off 'sovereign infrastructure' with a 15,000-chip base — AI Times Korea](https://www.aitimes.kr/news/articleView.html?idxno=39891)
- ["National AI Computing Center GPU not confirmed as B200…latest AI chips to be adopted" — ZDNet Korea](https://zdnet.co.kr/view/?no=20260803165045)
- [Korea's national AI team — Namuwiki](https://namu.wiki/w/%EA%B5%AD%EA%B0%80%EB%8C%80%ED%91%9C%20AI)
