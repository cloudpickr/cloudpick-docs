---
title: "Europe's Sovereign AI and Model Landscape"
description: "Covers the EU AI Continent Action Plan and AI Factories, European foundation model providers such as Mistral AI and Aleph Alpha, and the scope of AI services offered by hyperscaler sovereign clouds."
---

> Last reviewed: August 2026

## Overview

Beyond data sovereignty for cloud infrastructure, the EU has made **securing AI models and compute capacity themselves within the region** an explicit policy goal. This push to reduce dependence on US- and China-based foundation models (FMs) and to cultivate a European AI ecosystem combines government-led infrastructure investment (AI Factories/Gigafactories) with the cultivation of private FM providers (Mistral AI, Aleph Alpha, and others). This document summarizes the state of the EU's AI strategy, the European FM ecosystem, and the scope of AI services offered by hyperscaler sovereign clouds as of August 2026.

## The EU AI Strategy — the AI Continent Action Plan

The **AI Continent Action Plan** is the European Commission's roadmap for strengthening AI competitiveness, built around infrastructure investment, data accessibility, talent development, and regulatory alignment.

### InvestAI — A Funding Mobilization Framework

- At the Paris AI Action Summit in February 2025, European Commission President von der Leyen announced a goal to mobilize a total of **€200 billion in AI investment through the InvestAI initiative**. This includes **€20 billion in new EU funding for establishing AI Gigafactories**.
- InvestAI is a public-private structure in which the EU budget covers up to 17% of capital expenditure (CapEx), with member states matching at least the same amount.
- The June 2025 call for proposals drew **77 proposals from 16 member states (60 candidate sites)**, far exceeding initial expectations.

### AI Factories and Gigafactories — EuroHPC-Based Compute Infrastructure

AI Factories, operated by the **EuroHPC Joint Undertaking**, are hubs that open supercomputing infrastructure to startups, SMEs, and research institutions to support the development of trustworthy generative AI models.

| Date | Expansion |
| --- | --- |
| December 2024 | First round: 7 AI Factories selected (Finland, Germany, Greece, Italy, Luxembourg, Spain, Sweden) |
| March 2025 | Second round: 6 more added (Austria, Bulgaria, France, Germany, Poland, Slovenia) |
| October 2025 | Third round: 6 more added, plus 13 new AI Factory Antennas |
| As of August 2026 | **19 AI Factories plus 13 Antennas** operating across 15 or more member and associated states |

EuroHPC plans to procure at least nine new AI-specialized supercomputers between 2025 and 2026, expanding its existing AI compute capacity more than threefold, and the EU and participating countries have jointly invested more than €2.6 billion in AI Factories and Antennas.

A higher tier, **AI Gigafactories**, refers to ultra-large-scale frontier-model training hubs equipped with more than 100,000 AI accelerators per site; the European Commission aims to mobilize a total of **€20 billion** in investment through a dedicated AI Gigafactory fund (the exact split between public and private funding requires separate confirmation from official announcements). In January 2026, the EU Council amended the EuroHPC regulation to bring the development and operation of Gigafactories within EuroHPC's mandate, and **construction of the first Gigafactory is expected to begin in 2027**.

:::note
AI Factories (numerous, mid-scale, already 19 operating) and AI Gigafactories (few, ultra-large-scale, not yet under construction) are **separate tiers of initiative**. The two terms should not be confused.
:::

## European Foundation Model Providers

### Mistral AI — Europe's Largest Commercial FM Provider

Headquartered in Paris, Mistral AI is widely regarded as Europe's most advanced commercial FM provider.

- **Latest models**: has released Mistral Medium 3.5, OCR 4, and others, also distributed through hyperscaler channels such as Microsoft Foundry and Copilot Studio.
- **Expanded Microsoft partnership**: on July 21, 2026, announced an expanded strategic partnership with Microsoft, agreeing to **billions of dollars in AI infrastructure investment**. Mistral models are offered through Azure in a range of deployment forms — cloud, cloud-connected, and **fully disconnected environments** — to meet the data-control demands of regulated-industry and public-sector customers.
- **Independent infrastructure investment**: in February 2026, announced a **€1.2 billion AI data center investment** with EcoDataCenter, targeting a total of 200MW of compute capacity across Europe by the end of 2027 through a facility equipped with 13,800 Nvidia GB300 GPUs.
- Mistral also separately offers a "Sovereign Inference" service that runs exclusively within European jurisdiction, for regulated-industry and public-sector customers.

### Aleph Alpha — From Sovereign-AI Icon to a Canadian Joint Venture

Headquartered in Heidelberg, Germany, Aleph Alpha (founded 2019) grew into a flagship "sovereign AI" company with the goal of enabling European governments and regulators to operate high-performance AI without ceding data control to US big tech. Its PhariaAI platform is used in classified-level work environments within German federal ministries.

:::caution
**In April 2026, Canadian AI company Cohere and Aleph Alpha announced a deal to "join forces."** As of August 2026, official materials still describe this as a planned transaction rather than a completed acquisition, and the widely reported figure of roughly $20 billion is understood to be the combined enterprise value following the deal rather than a disclosed acquisition price. Digital ministers from both Germany and Canada attended the announcement event, and the deal was reported as having the backing of both governments, following on from the **Germany-Canada Sovereign Technology Alliance** launched around the Munich Security Conference in early 2026. Germany's digital ministry characterized the deal as holding "geopolitically and economically significant value."

However, this case also **shows that the definition of "European sovereign AI" itself is fluid.** Aleph Alpha still maintains its headquarters and workforce in Germany and continues to serve government workloads, but in governance terms it has become part of a merged entity with a Canadian company. Whether "sovereign" refers to the geographic location of data processing or extends to capital and governance structure varies by country, just as it does for France's SecNumCloud (see [EU Member-State Cloud Security Schemes](../national-schemes/)), and as the Aleph Alpha case shows, that boundary continues to be redefined by market conditions.
:::

### EuroLLM/OpenEuroLLM — Open Multilingual Model Projects

Separate from private commercial models, the EU also supports **open FM projects** in which academia, industry, and EuroHPC centers jointly participate.

- **OpenEuroLLM**: a €37.4 million project led by Charles University in Prague (Jan Hajič), co-led by AMD Silo AI, with a 20-institution consortium participating. It aims to develop a fully open (data, code, and weights published) LLM family supporting all official EU languages, jointly curating training data on EuroHPC supercomputers such as LUMI, Leonardo, and MareNostrum.
- According to the Year 1 progress report published in March 2026, the plan is to release an 8-billion-parameter model **during summer 2026**, with larger models to follow in sequence afterward. **Whether this timeline was actually achieved needs to be separately confirmed through the project's official announcements as of the time this document was written (August 2026).**
- A key differentiator from commercial models is that EU AI Act compliance and accessibility for European SMEs and startups are explicitly written into the project's design goals.

## The Scope of AI Services on Hyperscaler EU Sovereign Clouds

The sovereign cloud options covered in [GDPR and Data Sovereignty](../gdpr-sovereignty/#comparing-sovereign-cloud-options) are expanding their AI service offerings, but **the same AI service portfolio available in standard commercial regions is not necessarily offered as-is.**

- **AWS European Sovereign Cloud**: at its GA announcement in January 2026, AWS stated that more than 90 service categories, including AI, would be available, but the announcement materials did not specify the exact availability of individual AI/ML services such as Bedrock and SageMaker.
- **Microsoft EU Data Boundary / Bleu, Delos**: the EU Data Boundary guarantees EU-region processing of customer data for Microsoft 365, Dynamics 365, Power Platform, and most Azure services, but whether generative AI services such as Azure OpenAI are covered to the same extent needs to be checked on a per-service basis.
- **S3NS (Google Cloud × Thales)**: PREMI3NS, which obtained SecNumCloud qualification in December 2025, launched with more than 20 IaaS, CaaS, and PaaS services, and the second-phase expansion review in the first half of 2026 included services such as Cloud Run, Dataproc, and Confidential VM. Whether generative AI services such as Vertex AI and Gemini will be brought within SecNumCloud certification requires official confirmation.

:::caution
The **scope of AI services available under sovereign regions and partnerships is continuing to expand and can change with each official announcement.** Don't assume that "using a sovereign cloud means access to all AI services on equal footing" — verify, at the service level and through official vendor documentation, whether the specific AI service you intend to use is actually included in the target region's or partnership's certification and offering scope.
:::

## Comparison with Korea's Sovereign FM Policy

The EU and Korea share the goal of "reducing dependence on global FMs," but their approaches differ. Korea's [Independent AI Foundation Model Project](../../korea/ai/sovereign-fm-policy/) is a **tournament-style, national-champion selection structure** in which the government selects a small elite group of teams (a second-round evaluation involving four teams as of August 2026), provides concentrated budget and GPU support, and narrows the field down to a final one or two teams. The EU, by contrast, takes a **distributed, open-ecosystem approach**: it encourages hyperscaler partnerships and investment in private commercial companies such as Mistral AI, while simultaneously running multi-country, multi-institution open collaboration projects such as OpenEuroLLM, and broadening compute access through AI Factories to a large number of startups and research institutions rather than a small handful of champions. That said, as the Cohere-Aleph Alpha merger shows, Europe too has not been able to fully insulate its national champion from market forces — a point worth noting for Korea's own policy design, since designating a specific company as a "national champion" for support can, over the long term, expose that policy to governance and capital-structure volatility risk.

## Practical Implications

- **Put a gateway layer in place that treats the FM as a swappable component.** Europe's FM landscape is reorganizing quickly, as seen in Mistral's absorption into hyperscaler channels and Aleph Alpha's change in governance structure. An abstraction layer is more advantageous for risk management than binding architecture directly to a specific vendor's API.
- **For regulated workloads requiring "fully disconnected deployment," consider on-premises/air-gapped options from providers like Mistral.** For workloads where data cannot leave the organization's control — such as those in the public sector or finance — an isolated-deployment option from a European FM provider may be more suitable than a hyperscaler API-based approach.
- **Verify the AI service scope of sovereign clouds at the service level, per region and partnership.** Whether "sovereign" guarantees only the data storage location or covers the full AI service stack varies by vendor and point in time.
- **Open projects (EuroLLM, etc.) may not yet offer the same commercial SLA and support structure as commercial models.** Licensing and support levels should be verified separately before production adoption.
- **Reconfirming the latest status is essential.** The expansion of AI Factories, partnership and governance changes at companies like Mistral and Aleph Alpha, and the scope of AI services included in sovereign clouds are all rapidly evolving matters, so it is advisable to build in a process to reconfirm through official sources at the start of a project.

## References

- [European Commission — AI Continent](https://commission.europa.eu/topics/competitiveness/ai-continent_en)
- [European Commission — AI Factories](https://digital-strategy.ec.europa.eu/en/policies/ai-factories)
- [European Commission — AI Gigafactories](https://commission.europa.eu/topics/competitiveness/competitiveness-coordination-tool-projects/ai-gigafactories_en)
- [Microsoft — Announcing Expanded Mistral Partnership (July 2026)](https://news.microsoft.com/source/2026/07/21/microsoft-and-mistral-expand-strategic-partnership-to-give-enterprises-and-regulated-industries-frontier-ai-they-can-control/)
- [CNBC — Cohere Announces Aleph Alpha Acquisition (April 2026)](https://www.cnbc.com/2026/04/24/cohere-aleph-alpha-germany-ai-europe-expansion.html)
- [OpenEuroLLM Official Site](https://openeurollm.eu/)
- [OpenEuroLLM — Year One Progress Report](https://openeurollm.eu/blog/first-year-progress-and-next-steps)
- [AWS — European Sovereign Cloud Launch Announcement (January 2026)](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe)
- [Thales — S3NS Announces SecNumCloud Qualification (December 2025)](https://www.thalesgroup.com/en/news-centre/press-releases/s3ns-announces-secnumcloud-qualification-premi3ns-its-trusted-cloud)
- [Cohere — Official Announcement of the Aleph Alpha Deal (April 2026)](https://cohere.com/blog/cohere-alephalpha-join-forces)
