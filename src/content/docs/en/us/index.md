---
title: "United States Overview"
description: "A guide to the regulatory landscape for entering and operating in the US market — FedRAMP, HIPAA, and ITAR/EAR — with links to detailed documentation."
---

> Last reviewed: August 2026

## Overview

The United States operates a dual regulatory structure at the federal and state levels, layered further with industry-specific regulations (healthcare, defense/aerospace, finance, and so on). Delivering cloud services to federal agencies requires FedRAMP authorization, handling healthcare data requires the HIPAA/BAA framework, and handling defense/aerospace technical data requires ITAR/EAR export controls — each applies independently and none substitutes for another. This section covers the core regulations and policies architects encounter when working with the US market — federal procurement, industry regulations, state privacy laws, and AI policy.

## Topics Covered

- **[FedRAMP](../us/fedramp/)** — The security authorization program for federal agency cloud procurement. Covers the Moderate/High baselines, the status of the ongoing FedRAMP 20x overhaul as of 2026, isolated government regions, and CMMC 2.0/DoD SRG Impact Levels.
- **[HIPAA/HITECH](../us/hipaa/)** — Regulations protecting healthcare data (PHI). Covers the Business Associate Agreement (BAA) structure, how to verify vendor-specific coverage, and the relationship with HITRUST CSF.
- **[ITAR/EAR](../us/itar/)** — Export control regulations for defense/aerospace technical data. Covers what US Persons access restrictions mean for cloud architecture and how they differ from FedRAMP.
- **[The State Privacy Law Landscape](../us/state-privacy/)** — The landscape of state-by-state privacy regulation in the US, where no federal comprehensive law exists. Covers the status of states in effect, common requirements, and multi-state compliance architecture, centered on the CCPA/CPRA.
- **[AI Policy and Governance](../us/ai-policy/)** — Covers the trajectory of federal AI executive orders, the NIST AI RMF, AI requirements in federal procurement, state AI law trends, and implications for cloud AI workloads.

:::note
These three regulatory regimes are independent of one another. For example, a cloud environment authorized at FedRAMP High does not automatically satisfy ITAR requirements, and HIPAA still requires a separate BAA. Each regulation must be verified individually based on the nature of the workload.
:::

## Related Documents

- [Compliance](../governance/compliance/)
- [Data Protection and Workload Security](../security/data-protection/)

## References

- [FedRAMP official site](https://www.fedramp.gov/)
- [HHS HIPAA official page](https://www.hhs.gov/hipaa/)
- [DDTC (agency overseeing ITAR)](https://www.pmddtc.state.gov/)
- [BIS (agency overseeing EAR)](https://www.bis.gov/)
