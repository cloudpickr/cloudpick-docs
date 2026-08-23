---
title: "EU Member-State Cloud Security Schemes"
description: "Covers Germany's BSI C5, France's ANSSI SecNumCloud, Spain's ENS, Italy's ACN, and other EU member-state cloud security certification and procurement schemes, along with hyperscaler compliance status."
---

> Last reviewed: August 2026

## Overview

With a unified EU-wide cloud security certification scheme (EUCS) still unfinalized, individual member states continue to control public procurement and regulated-industry cloud adoption through their own national schemes. Germany's BSI C5 and France's ANSSI SecNumCloud are the most mature and internationally referenced schemes, while Spain's ENS and Italy's ACN frameworks each gatekeep cloud procurement for their own public sectors in their own way. This document summarizes what architects deploying public-sector or regulated-industry workloads into the EU market need to prepare for, country by country.

:::note
National schemes are grounded in **each country's own laws and administrative procedures, not an EU Regulation**. Certification passed in one member state is therefore not automatically recognized in another, and mutual recognition across schemes will only become possible once an EU-wide framework such as EUCS is completed.
:::

## Germany — BSI C5

**C5 (Cloud Computing Compliance Criteria Catalogue)** is a catalogue of cloud security compliance criteria operated by Germany's Federal Office for Information Security (BSI, Bundesamt für Sicherheit in der Informationstechnik).

- **C5:2020**: consisting of 121 criteria, it has functioned as Germany's de facto standard cloud security audit benchmark since 2020. ENISA used C5:2020 as foundational material when designing the requirements for the EUCS Substantial tier.
- **C5:2026**: a revised edition whose final version was published in early April 2026 (though some reports cite late March 2026). It builds on the C5:2020 criteria while expanding and subdividing them into 168 criteria across 17 domains. **The new criteria become binding starting with the assessment period beginning June 1, 2027**, though early adoption is permitted before then.
- **Procurement status**: C5 is not a law, so there is no direct legal penalty for non-compliance, but **compliance with C5 is effectively mandatory for cloud procurement targeting German federal agencies**. Regulated industries such as finance and healthcare also commonly require C5 compliance when selecting vendors.
- **Hyperscaler status**: AWS, Microsoft Azure, Google Cloud, SAP, IONOS, and others hold C5 compliance attestations, with major vendors renewing their audits annually.

## France — ANSSI SecNumCloud

**SecNumCloud** is a cloud service qualification issued by France's national cybersecurity agency (ANSSI, Agence nationale de la sécurité des systèmes d'information). The current standard is **version 3.2** (revised in 2022), under which more than 360 technical and operational requirements are assessed by PASSI-accredited auditors (ANSSI-approved audit bodies).

### The Sovereignty Requirement Is the Key Differentiator

The single biggest difference between SecNumCloud 3.2 and other national schemes is its **capital and governance sovereignty requirement**.

- The company's headquarters must be located in France or within the EU
- Non-EU ownership cannot exceed 24% for any individual shareholder or 39% in aggregate
- The service must be governed exclusively by EU law (insulating it from extraterritorial data-access demands, such as those under the US CLOUD Act or FISA Section 702)

:::caution
Because of this requirement, **US-headquartered hyperscalers such as AWS, Microsoft, and Google cannot obtain SecNumCloud qualification directly under their own name.** Instead, they pursue an indirect path through joint ventures with French partners, with progress varying by vendor (see "Status of Partnership Certifications" below).
:::

### Status of Partnership Certifications (as of July 2026)

| Partnership | Vendor | Status |
| --- | --- | --- |
| **S3NS** (a Thales × Google Cloud joint venture) | Google Cloud | **Obtained SecNumCloud 3.2 qualification on December 17, 2025** — the first case of simultaneously certifying more than 20 IaaS, CaaS, and PaaS services under its PREMI3NS offering. A second-phase expansion review covering services such as Cloud Run, Cloud Build, Cloud Spanner, and Bigtable is underway in the first half of 2026 |
| **Bleu** (a Capgemini × Orange joint venture) | Microsoft Azure/M365 | Passed the first review stage (J0, application acceptance) and is undergoing review with a target of obtaining qualification in the first half of 2026. **As of August 2026, it has not yet obtained full SecNumCloud 3.2 qualification** |

Overall, as of July 2026, **nine to ten providers** (OVHcloud, 3DS Outscale, Cloud Temple, Orange Business, Cegedim.cloud, Worldline, Oodrive, Whaller, S3NS, and others — the count varies depending on the aggregation basis; ANSSI's official catalogue, tallied by service type, confirms up to 10 provider names) hold SecNumCloud 3.2 qualification, and **12 providers** — including Bleu, Scaleway, and NumSpot — are undergoing review.

## Spain — ENS

**ENS (Esquema Nacional de Seguridad, National Security Framework)** is a security framework required for Spanish public-sector information systems, established under Royal Decree 311/2022. It consists of three tiers: **Basic, Medium, and High**.

- Cloud vendors seeking to contract with Spanish public bodies are required to obtain ENS certification at the tier corresponding to the sensitivity of the information handled.
- **Hyperscaler status**: AWS (renewed ENS High certification covering 174 services and 31 regions), Microsoft Azure (ENS High compliance verified through a BDO audit), and Google Cloud (ENS High certification for Google Cloud and Google Workspace) all hold **ENS High, the top tier**. This is because, unlike SecNumCloud with its capital-sovereignty requirement, ENS is a scheme centered on technical and operational security controls.

## Italy — ACN and the National Strategic Cloud (PSN)

Unlike Germany and France, Italy takes a **two-track approach that combines a certification-style scheme with physical sovereign infrastructure**.

1. **ACN cloud qualification (qualificazione)**: since January 19, 2023, Italy's National Cybersecurity Agency (ACN, Agenzia per la Cybersicurezza Nazionale) has handled public-sector cloud service qualification, having taken over the function from AgID. It uses a questionnaire-based process assessing confidentiality, integrity, and availability impact to classify the risk tier of cloud services and infrastructure for use by public bodies. As part of "Strategia Cloud Italia," the goal is to migrate roughly 75% of Italian public administration onto qualified cloud services.
2. **PSN (Polo Strategico Nazionale, National Strategic Cloud)**: physical sovereign infrastructure for public workloads requiring the highest level of reliability and resilience. Through its "Public Cloud PSN Managed" configuration, hyperscaler platforms are brought into a public-administration-dedicated region within PSN data centers, allowing agencies that need to migrate from legacy systems to do so in stages. **As of July 21, 2026, more than 280 central government bodies, regional health agencies, and hospital organizations have completed migration to PSN** (achieving the PNRR target).

:::note
In Italy's model, hyperscalers do not so much obtain individual qualifications directly from ACN in the manner of Germany's C5 or France's SecNumCloud; rather, they provide their services **through PSN, a physical gateway under Italian control**. The scope of certification at the individual-service level should be verified separately through vendor and PSN official announcements.
:::

## Relationship with EUCS — Harmonization Discussions Are Ongoing

Although the four national schemes above operate independently, once the EU-wide **EUCS (European Cybersecurity Certification Scheme for Cloud Services)** is finalized, it is expected to form the basis for mutual recognition among them.

- C5:2020 has already been incorporated as foundational material in designing the requirements for the EUCS Substantial tier.
- Work on EUCS stalled for years amid disagreement among member states over whether to include a "sovereignty requirement" at the highest (High+) tier, but it is being revived within the amendment process for the **Cybersecurity Act 2 (CSA2)**, announced January 20, 2026.
- **As of August 2026, EUCS remains unfinalized, and whether it will include a sovereignty requirement is still under debate.** (For further detail, see [GDPR and Data Sovereignty — The Fluid State of the EUCS Certification Scheme](../gdpr-sovereignty/#the-fluid-state-of-the-eucs-certification-scheme).)

Until then, national schemes function as "provisional but market-trusted evidence," with BSI C5 and SecNumCloud in particular serving as the de facto reference points during the transition to EUCS.

## National Procurement Gates — Summary

National schemes share the common feature that certification itself is not the goal — it functions as **a gate to pass for public and regulated-industry procurement**. That said, the nature of the gate differs by country.

| Country | Scheme | Nature | Can hyperscalers obtain it directly? |
| --- | --- | --- | --- |
| Germany | BSI C5 | Technical/operational control audit (no capital requirement) | Yes — AWS, Azure, Google Cloud, and others have already obtained it |
| France | SecNumCloud 3.2 | Technical/operational controls plus a **capital and governance sovereignty requirement** | No — requires going through a partnership (S3NS has obtained it; Bleu is under review) |
| Spain | ENS (Basic/Medium/High) | Technical/operational control audit (no capital requirement) | Yes — AWS, Azure, and Google Cloud have all obtained ENS High |
| Italy | ACN qualification + PSN | Questionnaire-based tiering combined with physical sovereign infrastructure | Via a PSN partnership |

## Practical Implications

- **Each country requires separate review.** With no single EU-wide certification in place, don't lump "entering the EU" into a single requirement — check the required scheme individually for each target member state (public-procurement counterparty, regulator).
- **Vendor choice itself is constrained for France-bound workloads.** If handling sensitive data for French public bodies or operators of vital importance (OIV/OSE), the field of vendor options narrows to those that directly hold SecNumCloud qualification (such as S3NS) or are close to obtaining it. For options still under review, such as Bleu, **do not assume full qualification will be obtained by a specific date in your contract or migration schedule.**
- **Germany and Spain offer a relatively wider choice of hyperscalers.** Since these two schemes have no capital-sovereignty requirement, major vendors already hold their top-tier certification, so the practical focus is less on vendor selection and more on confirming the certification scope (service list) and regional coverage.
- **For Italy, verify the infrastructure path rather than the certificate.** Alongside the ACN qualification tier, confirm — through vendor and PSN official documentation — whether the workload is delivered via PSN, and if so, how operational control and SLAs differ as a result.
- **Use national schemes as a temporary substitute for a finalized EUCS, but don't design around them as a fixed premise.** Once EUCS is finalized, the scope of mutual recognition and the requirements themselves could change, so an architecture that leaves room to adapt is safer than one that depends solely on a single national scheme.

## References

- [BSI — Introduction to C5](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/C5_Einfuehrung/C5_Einfuehrung_node.html)
- [BSI — C5:2026 Catalogue](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/C5_2025/C5_2025_node.html)
- [cyber.gouv.fr — SecNumCloud (ANSSI)](https://cyber.gouv.fr/)
- [Thales — S3NS Announces SecNumCloud Qualification (December 2025)](https://www.thalesgroup.com/en/news-centre/press-releases/s3ns-announces-secnumcloud-qualification-premi3ns-its-trusted-cloud)
- [Bleu — Announcement of Passing the SecNumCloud 3.2 J0 Review](https://www.bleucloud.fr/bleu-valide-le-j0-de-la-qualification-secnumcloud-3-2/)
- [AWS — Esquema Nacional de Seguridad (ENS) Compliance](https://aws.amazon.com/compliance/esquema-nacional-de-seguridad)
- [Google Cloud — ENS Compliance](https://cloud.google.com/security/compliance/ens)
- [ACN — Strategia Cloud Italia / Cloud Qualification](https://www.acn.gov.it/en/strategia/strategia-cloud-italia/qualificazione-cloud)
- [Polo Strategico Nazionale Official Site](https://www.polostrategiconazionale.it/en/)
- [ENISA — Candidate EUCS Scheme](https://certification.enisa.europa.eu/)
- [ANSSI — SecNumCloud Certification and Qualification Catalogue](https://messervices.cyber.gouv.fr/visas/catalogue-produits-services-profils-de-protection-sites-certifies-qualifies-agrees-anssi.pdf)
