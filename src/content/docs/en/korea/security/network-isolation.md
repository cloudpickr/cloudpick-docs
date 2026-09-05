---
title: "Network Separation and Isolation (Korea)"
description: "Covers network separation (mang-bunri) regulation in Korea's financial and public sectors, and cloud network isolation strategy."
---

> Last reviewed: August 2026

## Overview

Network separation (mang-bunri, 망분리) is a security regulation distinctive to Korea that physically or logically separates the business network from the internet network to block external intrusion and information leakage. The financial sector has required strong physical separation for decades under the Electronic Financial Supervision Regulation, and the public sector under the National Intelligence Service's (NIS) security guidelines.

However, as cloud, SaaS, and generative AI have become essential to daily operations, uniform physical separation has increasingly been criticized as an obstacle to efficiency and innovation, and **regulatory easing has been underway in earnest on both the financial and public-sector fronts since 2024**. This document covers the latest roadmap on both tracks, the impact on cloud/AI adoption, and how regulatory requirements map to architecture.

:::note
For **how to think about** network separation — the essential distinction between "separation" and "controlled connection," why the assumption "we did network separation, so we're safe" is dangerous, the trade-offs between physical and logical separation, and cloud isolation implementation patterns — see the general document [Network Segregation and Isolation](../../../security/network-isolation/). This document is the **Korea regulatory layer** that sits on top of those principles.
:::

## Easing Network Separation in Finance — The Financial Sector Network Separation Improvement Roadmap

### Background and Announcement

On August 13, 2024, the Financial Services Commission (FSC) announced the "Financial Sector Network Separation Improvement Roadmap." Its three core directions are:

1. Allowing financial companies to use **generative AI**
2. Substantially expanding the scope of permitted **cloud-based SaaS** usage
3. Improving financial companies' **research and development (R&D) environments** (permitting logical network separation)

### Phased Implementation

The roadmap has been implemented in phases through a regulatory sandbox.

- **Phase 1 sandbox** — prioritized generative AI use, expanded SaaS usage, and R&D environment improvements
- **Phase 2 sandbox** — reviewing whether to allow direct processing of personal credit information, pending verification of pseudonymized data usage
- **April 20, 2026** — an amendment to the enforcement rules of the Electronic Financial Supervision Regulation formally took effect, **officially permitting use, within the internal business network, of SaaS that has passed a security assessment by the Financial Security Institute**

### Conditions and Exceptions

The regulatory easing is not unconditional; it is designed so that only institutions with elevated security levels gain flexibility.

- SaaS must pass a **security assessment** by an incident response body such as the Financial Security Institute.
- Even after passing the assessment, ongoing obligations apply, including a **semiannual information security control implementation review** and reporting to an information security committee chaired by the CISO.
- **Areas that process unique identifiers such as resident registration numbers or personal credit information are excluded from the easing without exception.**

:::caution
Easing network separation in the financial sector does not mean "SaaS and generative AI can now be used freely." It applies only to services that have passed assessment, and only within business scopes that do not process unique identifiers or personal credit information. This distinction must be made explicit during procurement and architecture design.
:::

## Restructuring Network Separation in the Public Sector — The National Network Security Framework (N²SF)

### Concept

The National Network Security Framework (N²SF) is a new public-sector security paradigm led by the NIS. Rather than uniform physical network separation, it is a risk-based framework that **applies differentiated protection levels according to information sensitivity**. It classifies work data into Confidential (C), Sensitive (S), and Open (O) tiers, and applies modern security technologies — Remote Browser Isolation (RBI), AI-based Data Loss Prevention (AI-DLP), and Zero Trust — by tier, with the goal of creating dedicated segments where cloud and external AI can be used safely.

While the previous physical network separation policy had been maintained for roughly 18 years, N²SF was introduced to resolve the operational inefficiency caused by the spread of cloud and AI and the normalization of remote work. The NIS formally published version 1.0 of the related security guidelines in September 2025.

### Structure of Guideline 1.0

- **Classification tiers**: Class C (confidential — national security, defense, diplomacy), Class S (sensitive — personal data, internal review materials), Class O (open)
- **Security controls**: 6 major domains (authorization / authentication / separation-isolation / control / data / information assets), covering roughly 280 items
- **Application process**: preparation → C/S/O classification → threat identification → establishing security measures → adequacy assessment and adjustment (5 stages)
- **Information service models**: provides security design frameworks for 11 scenario types, including generative AI use, cloud collaboration, wireless work environments, and mobile connectivity

This represents a shift in the underlying policy question — from the binary "separated or not" to "what level of control is required."

### Pilot Programs and Rollout Schedule

- **2025**: Led by MSIT, pilot programs were run across the existing environments and two new systems at four institutions, including the Korean Intellectual Property Office and the National Security Research Institute, confirming that six RBI, AI-DLP, and Zero Trust models operate correctly on public networks.
- **2026**: A program worth roughly KRW 5.5 billion is planned. Of this, KRW 4.5 billion is allocated to an open call (6 projects) for porting the six verified models to other institutions, and roughly KRW 990 million to piloting wireless work environments.

### Differences from the Existing Network Separation Model

| Category | Existing network separation | N²SF |
| --- | --- | --- |
| Separation method | Uniform physical separation | Tailored security by information tier (C/S/O) |
| Trust model | Trust based on the internal network | Zero Trust |
| Cloud/generative AI use | Restricted in principle | Enabled through tier-specific dedicated segments |
| Transition approach | — | Gradual transition based on each institution's system scale and budget |

:::note
Security experts advise that "a rushed, full-scale rollout aimed at scoring management evaluation points should not take precedence over establishing a clear purpose of use and budget plan first." Transitioning to N²SF is not a single switch to flip but a phased effort following each institution's own roadmap.
:::

## Mapping Regulatory Requirements

| Regulation/standard | Requirement | Cloud approach |
| --- | --- | --- |
| **Electronic Financial Supervision Regulation** (finance) | Data center network separation, separation of internal network/DMZ/external network | VPC separation + Private Subnet + dedicated line |
| **CSAP High tier** (public sector) | Physical network separation | Use dedicated public-sector infrastructure |
| **CSAP Medium tier** (public sector) | Logical network separation + enhanced access control | Domestic CSP, or a global CSP that has obtained Medium-tier certification |
| **ISMS-P** (all industries) | Network separation, access control, encryption | Security Group + NACL + VPC Endpoint + TLS |
| **N²SF 1.0 (National Network Security Framework)** | Tiered security by C/S/O classification, roughly 280 security control items | Tiered VPC separation + controlled inter-tier communication + mapping to the 6 major domains |

## Where Should Your Organization Start

The right starting point depends on your regulatory requirements.

| Your situation | First step | Target architecture |
| --- | --- | --- |
| **CSAP High tier (physical separation mandatory)** | Use dedicated public-sector infrastructure | Global CSPs currently lack High-tier certification |
| **CSAP Medium tier (logical separation)** | Domestic CSP, or a global CSP that has obtained Medium-tier certification | VPC isolation + Private Link + dedicated line |
| **CSAP Low tier / ISMS-P** | Global CSP public cloud | Apply standard cloud security best practices |
| **N²SF Class C (confidential)** | Dedicated public-sector infrastructure or an air-gapped environment | Complete internet blocking, domestic personnel operation |
| **N²SF Class S (sensitive)** | VPC isolation + dedicated line + enhanced access control | A level similar to CSAP Medium tier |
| **N²SF Class O (open)** | Public cloud with baseline security | Meets minimum security requirements |

:::note
Most organizations don't have all systems at the same tier. The core of N²SF is classifying systems by tier and applying a proportional isolation level to each. Rather than "everything at the highest tier" or "everything public," a mixed configuration is the realistic outcome. For implementation patterns by isolation level (VPC separation, private subnets, dedicated lines, air-gaps), see [Network Segregation and Isolation](../../../security/network-isolation/).
:::

## Impact on Cloud, SaaS, and Generative AI Adoption

- **Financial sector**: before using SaaS or generative AI within the internal business network, organizations must first confirm whether the target service has passed the Financial Security Institute's assessment. Workloads that process personal credit information or unique identifiers must still maintain a separate network separation scheme, requiring a dual-track architecture based on data classification.
- **Public sector**: institutions looking to adopt N²SF pilot models can plan their budget and target systems around the 2026 open-call schedule. Until full rollout, however, the existing physical network separation rules remain in effect, so plans should assume a period of parallel operation.
- **Common thread**: both tracks share the same underlying structure — not "full openness," but "conditional easing limited to services that have passed assessment and certification." Checking CSAP certification status (see the [CSAP document](../csap/)) alongside eligibility for network separation easing is a practical checkpoint.

## References

- [Electronic Financial Supervision Regulation (Financial Services Commission)](https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/%EC%A0%84%EC%9E%90%EA%B8%88%EC%9C%B5%EA%B0%90%EB%8F%85%EA%B7%9C%EC%A0%95)
- [CSAP Cloud Security Assurance Program (KISA)](https://isms.kisa.or.kr/main/csap/intro/)
- [N²SF National Network Security Framework 1.0 Security Guidelines (National Cyber Security Center resource library)](https://www.ncsc.go.kr)
- [NIS publishes the official N²SF security guidelines (Sept 30, 2025)](https://www.digitaltoday.co.kr/news/articleView.html?idxno=537182)
- [[Press release] "Financial Sector Network Separation Improvement Roadmap" announced — Financial Services Commission](https://www.fsc.go.kr/no010101/82885)
- [Can the 2026 financial-sector network separation easing become an opportunity to strengthen AI security? — Rsupport](https://www.rsupport.com/blog/ai-security-network-separation-finance/)
- [Financial Cloud Guide A to Z Part 2 – R&D network exceptions and the network separation improvement roadmap — AWS Tech Blog](https://aws.amazon.com/ko/blogs/tech/financial-cloud-guide-a-to-z-part2/)
- [From physical network separation to tailored security, the National Network Security Framework (N²SF) — Penta Security](https://www.pentasecurity.co.kr/insight/from-physical-isolation-to-custom-security-n2sf/)
- [N2SF set for full-scale rollout this year... KISA says security pilot programs are complete — Boannews](https://m.boannews.com/html/detail.html?idx=142634)
- [Guide to the transition to the National Network Security Framework (N2SF) — AhnLab](https://www.ahnlab.com/ko/contents/content-center/36104)
