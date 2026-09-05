---
title: "AI Governance"
description: "Covers Singapore's AI governance framework — the NAIS 2.0 national AI strategy, the Model AI Governance Framework, AI Verify, IMDA's tools-first approach, the relationship with the PDPA, and ASEAN/Southeast Asia connections."
---

> Last reviewed: August 2026

## Overview

Singapore's approach to AI governance is designed **not around a single comprehensive AI law, but around layering a voluntary-compliance framework and practical tools on top of existing legislation (such as the PDPA)**. The Infocomm Media Development Authority (IMDA) and the Personal Data Protection Commission (PDPC) jointly lead policy, with three complementary layers working together: a national strategy (NAIS), a governance framework (the Model AI Governance Framework), and a testing tool (AI Verify).

:::note
Rather than imposing legal obligations tiered by risk level as the EU AI Act does, Singapore champions "tools over regulation." As of August 2026, there is no single law governing AI itself — the existing PDPA and sector-specific laws (such as financial regulation) apply to AI use instead.
:::

## NAIS and NAIS 2.0 — The National AI Strategy

Singapore published its first National AI Strategy (NAIS) in 2019, and in **December 2023** it published **NAIS 2.0**, subtitled "AI for the Public Good, for Singapore and the World," substantially expanding its scope. Subsequently, on **May 20, 2026**, **10 refreshed priorities** were announced, building on progress made since NAIS 2.0.

- Industry transformation through national AI missions (manufacturing, finance, telecommunications, healthcare) and mainstreaming AI adoption across all sectors
- Public-sector innovation through AI embedded across government
- Building AI research capacity broadly, cultivating bilingual AI talent, and attracting overseas researchers
- Broadening basic AI literacy across the population for inclusive growth
- Resource-efficient AI development and expanded access to compute infrastructure (such as **Kampong AI** in the one-north district and the national supercomputing center **ASPIRE 2B**)
- Promoting safe AI adoption through governance and social trust, and strengthening Singapore's position as an ASEAN AI hub (Singapore chairs ASEAN in 2027)

**More than S$1 billion will be invested in public AI research and talent development from 2025 to 2030**, and in **February 2026** a **National AI Council (NAIC)**, chaired by Prime Minister Lawrence Wong, was established to oversee the strategic direction of the national AI agenda.

## The Model AI Governance Framework — The Generative AI Edition (2024)

IMDA and the PDPC first published the **Model AI Governance Framework** (covering traditional AI, a voluntary reference document for responsible AI deployment by private companies) at the World Economic Forum in Davos in 2019, revising it in 2020. In response to the rapid spread of generative AI, IMDA and the **AI Verify Foundation** published a **proposed draft on January 16, 2024**, and, after gathering industry feedback, released the **final version on May 30, 2024** — the **Model AI Governance Framework for Generative AI**.

This framework sets out **nine dimensions** for addressing risks specific to generative AI, such as hallucination, copyright, and deepfakes.

| Dimension | Key content |
| --- | --- |
| Accountability | Incentive structures that ensure stakeholders act responsibly |
| Data | Quality management and governance of training data |
| Trusted development and deployment | Transparency around safety practices |
| Incident reporting | Systems for prompt notification and remediation |
| Testing and assurance | Third-party verification and standardized test protocols |
| Security | Addressing new threat vectors unique to AI |
| Content provenance | Transparency about the origin of generated content |
| Safety and alignment R&D | International cooperation on model alignment |
| AI for public good | Broadening access and sustainable development |

The framework is presented as an **early-stage implementation** step that can be progressively fleshed out into practical guidelines, on the premise that "no single intervention is sufficient to address existing and emerging AI risks." It is a voluntary reference document with no legal force.

## The Model AI Governance Framework — The Agentic AI Edition (2026)

In response to the growing spread of agentic AI following the release of the generative AI edition, IMDA published a new framework specific to agentic AI, the **Model AI Governance Framework for Agentic AI**, on **January 22, 2026**. It addresses governance issues around accountability, delegation of authority, and monitoring that arise in agentic workflows — where AI systems plan and execute actions on their own — and it complements the existing generative AI edition of the framework. As of this document's August 2026 review date, organizations seeking the most current governance framework should consult both the generative AI edition and the agentic AI edition together.

## AI Verify — A Testing Framework and Foundation

**AI Verify** is an AI governance testing framework and software toolkit that IMDA and the PDPC released as an MVP for international pilot use in **May 2022**, before it was open-sourced in **June 2023**. Alongside this, IMDA launched the independent non-profit **AI Verify Foundation** in **June 2023** to dedicate itself to running the open-source community (legally, it is a separate non-profit entity, not a subsidiary of IMDA).

The AI Verify testing framework evaluates AI systems against the following **11 AI governance principles**:

Transparency, explainability, repeatability, safety, security, robustness, fairness, data governance, accountability, human agency and oversight, and inclusive growth/societal and environmental well-being.

This set of principles is mapped to major international frameworks — including the US NIST AI RMF, the Hiroshima Process International Code of Conduct, and ISO/IEC 42001 — from the EU, G7, OECD, and US, allowing for cross-referencing. The AI Verify Foundation counts AWS, Dell, Google, IBM, Microsoft, Red Hat, and Salesforce among its premier members, and it operates **Project Moonshot** (a large language model evaluation toolkit), the **Global AI Assurance Sandbox** (a real-world generative AI testing environment), and the **AI Tester Accreditation Programme**, Asia's first third-party test-lab accreditation program.

## IMDA's Approach — Tools Over Regulation

The defining feature of Singapore's AI governance is its approach of **building up a body of voluntary frameworks and practical tools instead of mandating a single comprehensive law**. Rather than enacting a separate comprehensive law to govern AI, IMDA builds on existing law (the PDPA, sector-specific regulation) with the Model AI Governance Framework (a voluntary reference document) and AI Verify (a voluntary testing tool), encouraging companies to build trustworthy AI on their own.

:::caution
"No dedicated regulation" is not the same as "no legal obligations." If an AI system processes personal data, PDPA obligations (consent, purpose limitation, transfer limitation, and so on) still apply in full, and in regulated industries such as finance, MAS's (Monetary Authority of Singapore) existing technology risk management regulations apply to AI use as well. "There is no AI-specific law" should not be misread as "AI is not regulated."
:::

## The Relationship Between the PDPA and AI

On **March 1, 2024**, the PDPC published the "Advisory Guidelines on Use of Personal Data in AI Recommendation and Decision Systems." Rather than creating new obligations, this document explains in detail **how existing PDPA obligations (consent, notification, accuracy, accountability, and so on) apply to AI-powered recommendation and decision-making systems**. It makes clear that organizations operating AI systems that use personal data for training or inference need to build the PDPA's purpose-limitation and notification obligations into their AI pipeline design from the outset.

In other words, AI governance and personal data protection in Singapore should not be understood as separate tracks — the **PDPA is the foundational law that applies directly to AI systems**, and the Model AI Governance Framework and AI Verify are voluntary complements layered on top of it.

## Connection to the ASEAN AI Governance Guide

Singapore's IMDA has chaired the **ASEAN Working Group on AI Governance (WG-AI)** since 2024. The working group's output is the **"ASEAN Guide on AI Governance and Ethics,"** a regional alignment framework that ASEAN member states can reference when designing, developing, and deploying traditional AI technology. In 2025, an **expanded version (a Generative AI annex)** was prepared to extend its coverage to generative AI.

Singapore's Model AI Governance Framework effectively served as the prototype for the ASEAN guide, illustrating how IMDA has scaled a national-level framework up to the regional level. Companies providing services across multiple ASEAN member states are likely to find that complying with Singapore's framework aligns substantially with the policy direction of other ASEAN member states as well.

## A Regional Model — SEA-LION

A flagship example representing the research and infrastructure pillar of the national AI strategy is **SEA-LION (Southeast Asian Languages In One Network)**. Developed by **AI Singapore**, a national program supported by the National Research Foundation and led by the National University of Singapore (NUS), SEA-LION is an open-source family of multilingual, multimodal language models designed to reflect the linguistic and cultural nuances — including low-resource languages — of 11 or more Southeast Asian languages. The latest version, **SEA-LION v4.5**, incorporates agentic capabilities and a custom speculative decoder for improved reasoning efficiency, and it is accompanied by **SEA-Guard**, a family of safety-filtering models tailored to Southeast Asian cultural context.

SEA-LION is regarded as a project symbolizing Singapore's national strategy of securing domestic and regional model capability that reflects Southeast Asian language and culture, rather than relying entirely on general-purpose LLMs developed in the West.

## Practical Implications

- **The absence of an AI-specific law does not mean there is no compliance burden.** Global enterprises operating AI services in Singapore need to reinterpret existing legislation — the PDPA for personal data, and MAS regulation for financial services — for their AI pipeline, and the PDPC's guidelines on AI recommendation and decision systems serve as a useful practical checklist.
- **AI Verify can be used as a tool to prepare for self-regulation.** While not a legal requirement, pre-assessing your own AI systems with the AI Verify testing framework can reduce the compliance burden when responding to other countries' AI regulation (such as the EU AI Act) later, by leveraging its mapping to international frameworks.
- **Singapore's framework offers a useful reference point for ASEAN expansion.** If you plan to offer AI services across multiple ASEAN markets, it is efficient to review Singapore's Model AI Governance Framework alongside the ASEAN Guide on AI Governance and Ethics to identify the regional common denominator.
- **It is worth evaluating the use of Southeast Asia-specific models such as SEA-LION.** For services where low-resource Southeast Asian languages and cultural context matter — such as customer service and content localization — it is advisable to include SEA-LION family models in your benchmarks to compare performance and cost against general-purpose Western LLMs.

## References

- [National AI Strategy — Smart Nation Singapore](https://www.smartnation.gov.sg/initiatives/national-ai-strategy/)
- [Update to Singapore's National AI Strategy: Refreshed Priorities to Harness AI for the Public Good — Ministry of Digital Development and Information (MDDI)](https://www.mddi.gov.sg/newsroom/update-to-singapore-s-national-ai-strategy--refreshed-priorities-to-harness-ai-for-the-public-good-factsheet/)
- [Model AI Governance Framework for Generative AI — AI Verify Foundation](https://aiverifyfoundation.sg/resources/mgf-gen-ai/)
- [New Model AI Governance Framework for Agentic AI — IMDA (January 22, 2026)](https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2026/new-model-ai-governance-framework-for-agentic-ai)
- [AI Verify Foundation — Overview and Testing Framework](https://aiverifyfoundation.sg/)
- [Singapore's Approach to AI Governance — PDPC](https://www.pdpc.gov.sg/organisations/resources/guidance-by-topic/singapores-approach-to-ai-governance)
- [Advisory Guidelines on Use of Personal Data in AI Recommendation and Decision Systems — PDPC](https://www.pdpc.gov.sg/organisations/regulations-decisions/regulatory-guidance/advisory-guidelines-on-use-of-personal-data-in-ai-recommendation-and-decision-systems)
- [ASEAN Working Group on AI Governance — IMDA](https://www.imda.gov.sg/about-imda/international-relations/asean-working-group-on-ai-governance)
- [ASEAN Guide on AI Governance and Ethics — ASEAN](https://asean.org/book/asean-guide-on-ai-governance-and-ethics/)
- [SEA-LION — AI Singapore](https://sea-lion.ai/)
- For general personal-data-protection obligations, see [PDPA (Personal Data Protection Act)](../pdpa/); for the AI-adoption context of government systems, see [Government Cloud](../government-cloud/).
