---
title: "Japan"
description: "A cloud regulatory guide for entering and operating in the Japanese market — ISMAP (government cloud procurement certification) and APPI (Act on the Protection of Personal Information)"
---

> Last reviewed: August 2026


This section is a regulatory guide for Korean enterprise architects who plan to supply cloud services to the Japanese market or operate services using Japanese regions. Japan maintains a de facto entry gate for public-sector cloud procurement in the form of **ISMAP** (Information system Security Management and Assessment Program), and **APPI** (Act on the Protection of Personal Information) applies broadly to the handling of personal data. Both systems serve purposes similar to Korea's CSAP and Personal Information Protection Act, but their requirements and procedures must be satisfied separately.

The Japanese cloud market is notable for hyperscalers (AWS, Azure, Google Cloud, OCI) competing on a two-region footprint of Tokyo and Osaka, while domestic providers such as Sakura Internet (さくらインターネット) participate in the Government Cloud and are expanding their foothold in the public and financial sectors, which are sensitive to domestic-region requirements. There is no law that explicitly mandates data localization, but in practice the combination of ISMAP's procurement-gate nature and APPI's obligations around cross-border transfers and "understanding the external environment" has a substantial effect on region selection and contract design.

## Topics Covered

- **[ISMAP (Japan Government Cloud Procurement Certification)](../japan/ismap/)** — covers the program overview, registration process, the distinction between ISMAP and ISMAP-LIU, registration status of hyperscalers and major providers, its gate-like nature that excludes unregistered services from public procurement, and implications for Korean companies entering the market.
- **[APPI (Japan's Act on the Protection of Personal Information)](../japan/appi/)** — covers the three routes for cross-border transfer requirements, whether Korea and Japan mutually recognize each other's adequacy, the impact on cloud region selection, handling of sensitive information such as My Number, and the 2025–2026 triennial review trends.
- **[Government Cloud (ガバメントクラウド)](../japan/government-cloud/)** — covers the Digital Agency-led shared cloud infrastructure for national and local government, the status of registered CSPs (AWS/Azure/Google Cloud/OCI/Sakura Internet), the dual-gate structure with ISMAP, and the progress of local government system standardization.
- **[Japan's AI Policy and Domestic Model Landscape](../japan/ai-landscape/)** — covers the AI Act and AI Basic Plan, METI's GENIAC program, the domestic LLM landscape (NTT tsuzumi, NEC cotomi, PFN PLaMo, and others), the government procurement channel Gennai (源内), and a comparison with Korea's sovereign FM policy.

:::note
This section covers fast-moving announcements from Japanese government and regulatory bodies. It is recommended that you verify the latest status directly through the official sources listed in the "References" section at the bottom of each document.
:::

## Related Documents

> 📄 [Data Protection and Workload Security](../security/data-protection/)

> 📄 [Compliance](../governance/compliance/)

## References

- [ISMAP Portal](https://www.ismap.go.jp/)
- [Personal Information Protection Commission (PPC), Japan](https://www.ppc.go.jp/)
