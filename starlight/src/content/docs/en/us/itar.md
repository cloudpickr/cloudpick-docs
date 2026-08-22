---
title: "ITAR/EAR"
description: "What ITAR/EAR, the export control regulations for defense/aerospace technical data, mean for cloud architecture, and how they differ from FedRAMP."
---

> Last reviewed: August 2026

## Overview

ITAR (International Traffic in Arms Regulations) and EAR (Export Administration Regulations) are US export control regulations that govern the transfer of defense, aerospace, and dual-use technology outside the United States.

- **ITAR**: Administered by the Directorate of Defense Trade Controls (DDTC) under the State Department, governing defense articles, services, and technical data listed on the United States Munitions List (USML).
- **EAR**: Administered by the Bureau of Industry and Security (BIS) under the Commerce Department, classifying and controlling commercial and dual-use items and technology (advanced semiconductors, encryption software, etc.) through the Export Control Classification Number (ECCN) system.

A given item or technology is classified under either ITAR or EAR, but not both, and ITAR is generally far stricter than EAR. ITAR violations can carry criminal fines of up to $1 million and up to 20 years of imprisonment per violation. EAR criminal penalties are at the same level — up to $1 million and up to 20 years of imprisonment per violation — while administrative (civil) penalties run up to approximately $370,000 per violation (inflation-adjusted; $374,474 as of 2025) or twice the value of the transaction, whichever is greater.

| Category | ITAR | EAR |
| --- | --- | --- |
| **Administering agency** | State Department DDTC | Commerce Department BIS |
| **Items covered** | Defense articles, services, and technical data (USML) | Commercial and dual-use items and technology (ECCN) |
| **Registration requirement** | Mandatory prior registration for manufacturers/exporters | No separate prior registration requirement |
| **License exceptions** | Very limited | Relatively more exceptions available |

:::note
Determining whether an item or technology falls under ITAR or EAR (jurisdiction/classification) is itself a specialized area of legal judgment. When self-determination is difficult, it is safer to go through DDTC's Commodity Jurisdiction (CJ) process or seek advice from an export control attorney.
:::

## What US Persons Access Restrictions Mean for the Cloud

Technical data controlled under ITAR may, in principle, only be accessed by a **US Person** (a US citizen, permanent resident, certain protected individuals, or an entity incorporated within the United States); a Foreign Person seeking access requires separate DDTC authorization (a license, TAA, etc.). Applied to a cloud environment, this means:

- Absent a separate exception, the default assumption is that servers storing the technical data are located within the United States (CONUS) and that operations/maintenance personnel are likewise restricted to US Persons. However, data protected by end-to-end encryption meeting the §120.54 requirements is not considered an "export" even when transferred to or stored outside the United States, so physical storage within the US is not a uniform legal obligation (see the end-to-end encryption carve-out below).
- Even actions such as a foreign national logging into a cloud console, uploading a file, or viewing a shared screen without authorization can be considered a "deemed export" of the data.
- As a result, nationality-based access control cannot be fully implemented through IAM policy alone; effective control requires designing organizational structure (a dedicated US Person team or subsidiary) together with the choice of cloud environment.
- **The 2020 encryption carve-out (End-to-End Encryption Carve-out)**: Under an amended rule effective March 25, 2020, ITAR technical data protected by FIPS 140-2-level end-to-end encryption is not considered "exported" even if it transits or is stored on a foreign server, provided the decryption means (keys) are not made available to any third party, including the cloud vendor. However, server-side encryption where the vendor holds the keys does not qualify for this carve-out, and if an unauthorized foreign person accesses the data in plaintext, it is considered an export regardless of encryption status. Arms-embargoed countries such as China, Russia, Iran, and North Korea are excluded from this carve-out as well.

## Differences from FedRAMP

ITAR and FedRAMP are distinct requirements of a different nature.

- FedRAMP is a **certification program** that evaluates and authorizes the security controls of cloud services, whereas ITAR is a **legal regulation** governing the export of specific technical data. There is no official credential called "ITAR certification"; compliance responsibility rests with the company (the exporter) handling the data itself.
- **Holding FedRAMP authorization does not mean ITAR compliance.** For example, even meeting the CUI-handling requirements of FedRAMP Moderate may not satisfy ITAR requirements without additional measures such as end-to-end encryption.
- In practice, regions designed as ITAR-ready environments, such as AWS GovCloud and Azure Government, often also hold FedRAMP High authorization, so the two are frequently mentioned together — but this is because the vendor designed its infrastructure to meet both requirements, not because FedRAMP authorization itself guarantees ITAR compliance. ITAR compliance must ultimately be demonstrated by the company handling the data itself.

## Compliant Environments: GovCloud, GCC High, and Others

| Environment | ITAR/EAR-relevant characteristics |
| --- | --- |
| **AWS GovCloud (US)** | Physically located within the United States; AWS operational personnel restricted to US citizens. Account owners must be a US Person and maintain valid DDTC registration. However, GovCloud application users (IAM users) themselves are not necessarily required to be US Persons — data access control is designed by the customer |
| **Microsoft GCC High** | An environment deploying Microsoft 365 on top of Azure Government infrastructure. Data centers within the United States, accessible only by vetted US citizen personnel. The only Microsoft 365 environment that meets DFARS 252.204-7012, ITAR, EAR, and CMMC Level 2/3 requirements. Note that standard GCC (the tier below GCC High) does not support ITAR/EAR — take care not to confuse the two |
| **Google Cloud Assured Workloads (ITAR control package)** | Data residency restricted to US regions, customer-managed encryption keys (CMEK) required, ITAR-related technical support routed to US Persons within the United States. Available at the Premium tier |
| **OCI Government Cloud** | Provides similar US personnel and data residency controls in Oracle's government-only regions |

## Practical Considerations for Defense/Aerospace Partnerships

- When a company exchanges technical data with a US defense/aerospace prime contractor, employees who are not US nationals are generally classified as a Foreign Person and cannot directly access ITAR technical data (e.g., Korean-national employees). This requires either obtaining DDTC authorization in advance — such as a Technical Assistance Agreement (TAA) or Manufacturing License Agreement (MLA) — or handling the data only through a separate organization or subsidiary staffed by US Persons within the United States.
- Because the act of uploading or downloading to the cloud can itself be considered an "export," it is essential to first confirm whether a collaboration or file-sharing service is ITAR-ready (e.g., GCC High) before selecting it. Standard commercial cloud services (standard GCC, general Microsoft 365, general Google Workspace, etc.) are not suitable for storing ITAR technical data.
- Leveraging the end-to-end encryption carve-out can create room for compliance without necessarily using US infrastructure, but implementation difficulty is high, since key management must be entirely controlled by the company itself (or a trusted US Person), not the vendor. Obtaining export control legal counsel before adoption is advisable.
- Contracts involving the same CUI (Controlled Unclassified Information) are often subject to CMMC/NIST SP 800-171 requirements in addition to and separately from ITAR. For details, see the CMMC 2.0 section in the [FedRAMP](../fedramp/) document.
- Dual-use technology subject to EAR (e.g., advanced semiconductor design data, certain encryption technologies) is relatively more flexible than ITAR but may still require a license, so it is essential to first determine whether the data is classified under ITAR or EAR.
- Unlike pursuing FedRAMP authorization, which is a goal in itself, ITAR/EAR compliance is not a standalone "authorization acquisition" project — it must be approached as an ongoing compliance framework spanning the organization's entire data-handling process (contracts, personnel, access control, cloud architecture).

:::caution
ITAR/EAR violations are a serious legal risk that can lead to criminal penalties. This document is a general overview from an architectural perspective; before proceeding with any actual contract or project, you must obtain export control legal counsel.
:::

## Related Documents

- [Compliance](../../governance/compliance/)
- [Network Segregation and Isolation](../../security/network-isolation/)

## References

- [DDTC (agency overseeing ITAR)](https://www.pmddtc.state.gov/)
- [BIS EAR official page](https://www.bis.gov/)
- [AWS GovCloud ITAR compliance guide](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-itar.html)
- [AWS ITAR compliance](https://aws.amazon.com/compliance/itar/)
- [Google Cloud Assured Workloads — ITAR data boundary](https://docs.cloud.google.com/assured-workloads/docs/control-packages/itar)
- [Microsoft GCC High overview](https://learn.microsoft.com/microsoft-365/enterprise/microsoft-365-government-gcc-high-and-dod)
