---
title: "AI Policy and Governance"
description: "Covers the trajectory of US federal AI executive orders, the state-federal preemption conflict, the NIST AI RMF, federal procurement AI requirements, and practical implications for cloud AI workloads."
---

> Last reviewed: August 2026

## Overview

US AI policy has shifted direction significantly with the change of administration since 2023, and the situation has remained fluid through 2025–2026 as executive orders have been issued and rescinded in succession. At the federal level, the axis has been reorganized around "promoting innovation over regulation," but state-level AI laws have continued to multiply at the same time, making the preemption conflict between the federal government and the states a central issue of 2026. This document summarizes the trajectory of federal executive orders, NIST's technical standards, federal procurement requirements, and major state law developments, and covers the practical implications for operating cloud AI workloads.

:::caution
AI policy has seen repeated announcements, rescissions, and re-announcements throughout the 2025–2026 administration transition, and there are differing interpretations even among press and law-firm reporting. The content below reflects facts confirmed against official White House (whitehouse.gov), NIST (nist.gov), and OMB documents; the latest status should always be reconfirmed against official sources before actual application.
:::

## The Trajectory of Federal AI Executive Orders

| Date | Action | Key content |
| --- | --- | --- |
| 10/30/2023 | **EO 14110** (Biden administration) | "Safe, Secure, and Trustworthy Development and Use of AI" — established AI safety evaluations, consideration of equity and civil rights, and guidelines for federal agency AI use |
| 1/20/2025 | **EO 14148** | Rescinded a batch of Biden administration executive orders, including EO 14110 |
| 1/23/2025 | **EO 14179** | "Removing Barriers to American Leadership in Artificial Intelligence" — characterized EO 14110 as "unnecessarily burdensome" and shifted the stance toward promoting innovation and reducing regulation |
| 7/23/2025 | **America's AI Action Plan** + 3 executive orders | "Winning the Race" — presented roughly 90 federal actions organized around three pillars (accelerating innovation, building AI infrastructure, and leading international AI diplomacy and security). Simultaneously signed measures included streamlined AI infrastructure permitting and an AI export program |
| 12/11/2025 | **EO 14365** | "Ensuring a National Policy Framework for Artificial Intelligence" — set the establishment of a unified federal AI policy and federal preemption of state AI laws as explicit policy goals |

:::note
The rescission of EO 14110 does not automatically invalidate everything it produced (for example, the NIST AI RMF and portions of draft procurement guidelines). NIST AI RMF 1.0 and the Generative AI Profile (AI 600-1) continue to exist as separate documents regardless of the executive order's status and remain in active use in procurement practice.
:::

## Federal Attempts to Preempt State AI Laws — An Ongoing Matter

Since 2025, the federal executive branch has pursued both legislative and executive-order paths in an attempt to neutralize state AI laws.

- **A failed legislative attempt**: the 2025 budget reconciliation bill (the "One Big Beautiful Bill Act") included a provision barring states from enforcing AI regulation for 10 years, but negotiations over a compromise carving out an exception for child safety broke down, and the provision was **struck from the bill by a 99–1 Senate vote**. A similar preemption provision was discussed for the FY2026 National Defense Authorization Act (NDAA) but was not included in the final version.
- **The executive-order path**: **EO 14365**, signed December 11, 2025, directed the establishment of an "AI Litigation Task Force" within the Department of Justice, which was **established on January 9, 2026**, to bring lawsuits in federal court arguing that state AI laws unduly burden interstate commerce or are preempted by federal regulation. A confirmed instance of actual intervention is the Department of Justice's participation, on April 24, 2026, in xAI's lawsuit challenging the Colorado AI Act. It also directed the Department of Commerce to publish, by March 11, 2026, a list of state AI laws deemed "unduly burdensome," and imposed a condition tying eligibility review of the **as-yet-unallocated remaining funds** within the BEAD (broadband infrastructure, $42 billion total) program to the repeal of "burdensome state AI regulation" (funds already allocated or disbursed, and the program's full $42 billion, were not made conditional across the board).

:::caution
**As of August 2026, no federal law invalidating state AI laws has been enacted.** Litigation and administrative action under EO 14365 are underway, but the executive order itself cannot directly invalidate state laws — that requires a court ruling (see the Colorado case below). Because this matter continues to shift on both the litigation and legislative fronts, the latest status should be reconfirmed through official White House and DOJ announcements.
:::

## NIST AI Risk Management Framework (AI RMF) 1.0 + the Generative AI Profile

**NIST AI RMF 1.0** (published January 2023) is a **voluntary** framework for organizations to manage AI system risk. It carries no legal force, but it has become a de facto reference standard in both federal procurement and private governance. It is organized around four core functions: Govern, Map, Measure, and Manage.

**NIST AI 600-1 (the Generative AI Profile)**, published July 26, 2024, extends the AI RMF specifically for generative AI, identifying **12 risk categories unique to, or exacerbated by, generative AI** — confabulation/hallucination, data poisoning, prompt injection, intellectual property infringement, over-reliance, and more — and prescribing response measures.

- Risks related to supply-chain vulnerabilities and third-party model evaluation are already included in the original document published July 26, 2024. Some media outlets have reported an update around March 2025, but as of August 2026 the latest official version confirmed on NIST's official site remains the version published 2024-07-26 (whether an official revision exists should be reconfirmed via NIST announcements).
- In December 2025, a draft **Cyber AI Profile (NIST IR 8596)** was published, connecting the AI RMF with the Cybersecurity Framework (CSF) 2.0 and extending its scope to managing the cybersecurity risk of AI systems themselves.

## AI Requirements in Federal Procurement — OMB Memoranda

In step with the executive-order transition, OMB (the Office of Management and Budget) also comprehensively revised its guidance on federal agency AI use and procurement on April 3, 2025. It rescinded the prior Biden-administration memo M-24-10 and replaced it with the following two memos.

- **M-25-21** (Accelerating Federal Use of AI through Innovation, Governance, and Public Trust): directs agencies to develop AI strategies, share AI capabilities across agencies, and expand investment. It requires agencies to identify and manage "High-Impact AI" — AI systems that serve as a principal basis for decisions with legal or otherwise significant effects — and, **starting in 2026, requires agencies to report their AI use cases and risk determinations annually in a public inventory**.
- **M-25-22** (Driving Efficient Acquisition of Artificial Intelligence in Government): sets three guiding principles — fostering a competitive AI procurement market, managing risk through performance tracking, and cross-agency collaborative procurement. It applies to **procurements announced on or after September 30, 2025**, and mandates a contract clause prohibiting vendors from using the government's non-public data to train commercial AI models without explicit consent.

:::note
Neither memo explicitly mandates the NIST AI RMF or AI 600-1, but in practice, vendors able to demonstrate alignment with the NIST framework are positioned favorably in procurement evaluations. Cloud/SaaS vendors seeking to provide AI services to government customers should treat documentation of NIST AI RMF alignment as an essential preparation item in practice.
:::

## State AI Law Trends

Contrary to the federal deregulatory stance, state-level AI legislation has continued to grow through 2026.

| State | Law | Status (as of August 2026) |
| --- | --- | --- |
| Colorado | Colorado AI Act (SB 24-205) | Original effective date of 2/1/2026 → delayed to 6/30/2026 by an August 2025 amendment → **repealed and replaced by SB 189 on 5/14/2026**, scaling back from comprehensive high-risk AI regulation to a disclosure-and-rights framework centered on Automated Decision-Making Technology (ADMT), with the effective date reset to **1/1/2027**. Separately, on 4/27/2026 a federal district court approved a stipulated stay agreed between the parties in the xAI lawsuit (with DOJ intervention in support), staying enforcement of the original act (SB 24-205) until 14 days after a merits ruling — a **procedural standstill**, not a ruling on the law's constitutionality |
| Texas | TRAIGA (Texas Responsible AI Governance Act, HB 149) | Effective 1/1/2026. Rather than Colorado-style comprehensive high-risk AI regulation, takes a narrower approach centered on **enumerated prohibited conduct** — AI that encourages suicide or crime, child sexual abuse material, non-consensual deepfakes, government social scoring, and the like — **plus a state-government AI-use disclosure requirement** |
| California | SB 53 (Transparency in Frontier AI Act), AB 2013 (Training Data Transparency Act) | Both effective 1/1/2026. SB 53 requires frontier model developers to disclose their safety frameworks; AB 2013 requires detailed disclosure of generative AI systems' training data sources, types, and whether they include copyrighted material or personal information |
| Illinois | HB 3773 and others | Effective 1/1/2026, regulating disclosure of AI use and preventing discrimination in areas such as employment |
| New York | RAISE Act and others | Includes provisions taking effect in 2027, directed at frontier model safety regulation |

:::caution
As the Colorado case shows, state AI law is a highly fluid area marked by repeated **effective-date delays, amendments, and litigation-driven enforcement halts**. Before operating or expanding AI services in a given state, the latest enforcement status should be individually confirmed with that state's Attorney General's office or a reliable legal tracker.
:::

## Practical Implications for Cloud AI Workloads

- **Treat NIST standards as the baseline rather than reflecting every federal executive-order change into contracts and compliance documentation in real time**: executive orders shift quickly with political transitions, but the NIST AI RMF and AI 600-1 function as a relatively stable technical standard and a common language for procurement practice. Adopting the NIST framework as the baseline for governance documentation reduces the rework burden when policy changes.
- **If targeting federal procurement, build M-25-21/M-25-22 requirements into the design early**: to respond to procurements announced on or after September 30, 2025, high-impact AI identification and risk-determination processes, and consent procedures for using public versus non-public data in training, need to be in place at the contract and architecture stages.
- **Don't generalize state AI law as "trending toward deregulation"**: while the federal government is moving toward deregulation and preemption, many states are continuing to enact new AI laws. Workloads involving automated decisions with significant consumer effects — particularly in employment, credit, and healthcare — should track the requirements of major states such as Colorado, California, and Illinois individually.
- **Proactively build a transparency and data-lineage framework**: California's AB 2013 (training-data disclosure) and Colorado's ADMT framework are both converging on requiring documentation of what data a system was trained on, how, and what decisions it is used for. A model and dataset lineage-management framework becomes a reusable asset across multiple states' requirements going forward.
- **Monitor preemption litigation outcomes**: the AI Litigation Task Force's attempts under EO 14365 to invalidate state laws (as in the Colorado case) could spread to other states, so when building a compliance plan around a specific state law, it is important to also consider the possibility that the law's legal force itself could be shaken by litigation.

## References

- [White House — Removing Barriers to American Leadership in AI (EO 14179)](https://www.whitehouse.gov/presidential-actions/2025/01/removing-barriers-to-american-leadership-in-artificial-intelligence/)
- [White House — America's AI Action Plan (July 2025)](https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf)
- [White House — Ensuring a National Policy Framework for AI (EO 14365, December 2025)](https://www.whitehouse.gov/presidential-actions/2025/12/eliminating-state-law-obstruction-of-national-artificial-intelligence-policy/)
- [NIST — AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST — AI RMF: Generative AI Profile (NIST AI 600-1)](https://www.nist.gov/itl/ai-risk-management-framework)
- [OMB — M-25-21, M-25-22 (whitehouse.gov OMB memoranda)](https://www.whitehouse.gov/omb/)
- [Colorado Attorney General — Colorado AI Act](https://coag.gov/)
- [Texas Attorney General — TRAIGA](https://www.texasattorneygeneral.gov/)
- [DOJ — Announcement of Intervention in xAI's Colorado AI Act Lawsuit (April 2026)](https://www.justice.gov/opa/pr/justice-department-intervenes-xai-lawsuit-challenging-colorados-algorithmic-discrimination)
- [NIST AI 600-1 Original PDF (published July 26, 2024)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
