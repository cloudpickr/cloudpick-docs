---
title: "ISMAP (Japan Government Cloud Procurement Certification)"
description: "Covers the overview, registration process, the distinction between ISMAP and ISMAP-LIU, hyperscaler registration status, and implications for Korean companies of Japan's cloud security assessment program for government information systems (ISMAP)."
---

> Last reviewed: August 2026

## Overview

ISMAP (Information system Security Management and Assessment Program, 政府情報システムのためのセキュリティ評価制度) is a program under which the security level required when Japanese government agencies procure cloud services is assessed and registered in advance. It began operating in June 2020. The National Cybersecurity Office (国家サイバー統括室, NCO — the organization created by reorganizing NISC in July 2025), the Digital Agency (デジタル庁), the Ministry of Internal Affairs and Communications, and the Ministry of Economy, Trade and Industry participate as the responsible ministries, while the Information-technology Promotion Agency (IPA) serves as the operating support body that assists with registration review.

The Japanese government has adopted a cloud-by-default principle (クラウド・バイ・デフォルト原則) through its "Basic Policy on the Appropriate Use of Cloud Services in Government Information Systems," and the Digital Agency's Government Cloud (ガバメントクラウド) — the shared cloud infrastructure for the government — also lists ISMAP registration as a condition of use. In other words, similar to Korea's CSAP (Cloud Security Assurance Program), ISMAP functions as the **de facto entry gate** for public-sector cloud procurement in Japan.

:::note
ISMAP is a Japan-specific program, separate from international certifications such as ISO 27001 and SOC 2. Even a vendor holding international certifications is, in principle, unable to supply cloud services to Japanese government agencies without ISMAP registration.
:::

## Registration Process

ISMAP registration generally proceeds in the following order.

1. **Determine the target service** — finalize the cloud service (including region and service scope) for which registration will be sought.
2. **Build and operate an internal control framework** — build an in-house security framework aligned with the ISMAP management standards (information security management standards, governance standards, management standards, etc.) and actually operate it.
3. **External audit** — undergo an external audit by an ISMAP-registered auditing body to assess compliance with the management standards.
4. **Registration application** — submit documentation, including the audit results, to IPA.
5. **Technical review** — IPA technically reviews the content of the audit results.
6. **Registration decision** — the ISMAP Steering Committee (the highest decision-making body of the ISMAP system) makes the final registration decision. The program aims, in principle, to reach a registration decision within six months of accepting the application.

Even after registration, a renewal review is conducted at least once a year, so this is not a one-time certification but a framework that must be maintained continuously.

### ISMAP and ISMAP-LIU

Out of concern that requiring the full ISMAP-level review even for SaaS handling relatively low-importance information would set the entry bar too high for small and medium-sized SaaS providers, **ISMAP-LIU** (ISMAP for Low-Impact Use) was introduced in November 2022.

| Category | ISMAP | ISMAP-LIU |
| --- | --- | --- |
| **Scope** | Government information systems in general (may include highly confidential information) | SaaS handling relatively low-confidentiality information |
| **Review items** | The full set of management standards | Narrowed down to focus on risks that significantly affect cloud infrastructure and configuration |
| **Audit scope** | Broad verification of management strategy | Focused on management strategy related to core risks |
| **Suitable for** | Large-scale infrastructure (IaaS/PaaS), services shared across multiple ministries | Small and medium-sized SaaS, SaaS for specific business functions |

:::note
As of April 1, 2025, the ISMAP-LIU pre-application (事前申請) procedure was abolished. Responsibility for confirming low-impact status has now shifted to the government procuring agency at the time of procurement, and the registration procedure itself is now operated in a manner largely similar to standard ISMAP. Check the [ISMAP Portal](https://www.ismap.go.jp/) for the latest operating details.
:::

## Registration Status of Hyperscalers and Major Providers (as of August 2026)

| Provider | Registration status | Notes |
| --- | --- | --- |
| AWS | Registered (includes Tokyo and Osaka regions, numerous services) | Has maintained registration since the early days of the ISMAP program, with renewal repeated before each expiry |
| Microsoft Azure | Registered (includes Japan East/Japan West and contractually available overseas regions) | Related services such as Microsoft 365 are also registered |
| Google Cloud | Registered (individual services such as Looker are also registered progressively) | Registration timing can differ by service, so check the latest list |
| Oracle Cloud Infrastructure (OCI) | Registered (initially registered June 2021, subsequently expanded to PaaS, Exadata Cloud@Customer, etc.) | |
| Sakura Internet (さくらのクラウド) | Registered (December 2021) | The first domestic Japanese provider to also be selected as a Government Cloud provider |
| Cloudflare | Registered (announced January 2026, effective from December 22, 2025) | Includes numerous services such as CDN/WAF, DDoS protection, Zero Trust, and Workers |

:::caution
The table above is a summary as of the time it was verified via web search. The scope, region, and validity period of registered services vary by provider and are updated from time to time. For actual procurement and design work, always verify the target service name and region directly on the [ISMAP Cloud Service List](https://www.ismap.go.jp/csm).
:::

## Gate-Like Nature: Exclusion from Public Procurement When Unregistered

ISMAP functions less like a certification and more like a **list of procurement-eligible services**. Government agencies are, in principle, required to procure from among the services listed on the ISMAP Cloud Service List or the ISMAP-LIU list, so services not on the list are effectively excluded from government procurement without a separate individual review. ISMAP registration is also a condition of participation in the Government Cloud, so as local government systems increasingly migrate to the Government Cloud, ISMAP's reach is trending to extend beyond the central government to local governments and public bodies as a whole.

## Practical Implications for Entering Japan's Public-Sector SaaS Market

- **Both an entry barrier and a trust signal**: ISMAP is a prerequisite for entering Japan's public sector, but registration itself is also used as a signal that demonstrates security maturity to large private-sector and regulated-industry customers. It is worth considering even for companies that are not targeting public procurement.
- **Audit and review cost and duration**: selecting an external auditing body, addressing the management standards, IPA's technical review, and the Steering Committee's decision can together take anywhere from several months to nearly a year, so this should be factored into a Japan market-entry roadmap early on.
- **Room to leverage ISMAP-LIU**: companies starting with a specific-purpose SaaS rather than a government-wide system may find the ISMAP-LIU route relatively less burdensome. However, since the abolition of pre-application in April 2025 has brought the procedure closer to standard ISMAP, the latest requirements should be checked.
- **Local entity and local audit response required**: Japanese-language documentation and collaboration with Japan-based auditing bodies are effectively essential during the audit and review process.
- **Example: Korean Company Registration Cases**: as of the time this document was written, no publicly available cases of Korea-affiliated companies registered on the ISMAP Cloud Service List could be confirmed (verification needed — checking the latest registration status directly on the ISMAP Portal is recommended).

## References

- [ISMAP Portal](https://www.ismap.go.jp/) — the official source for the registered service list and program rules
- [ISMAP Program Overview (NISC, Digital Agency, Ministry of Internal Affairs and Communications, Ministry of Economy, Trade and Industry, November 2023)](https://www.ismap.go.jp/csm/sys_attachment.do?sys_id=4560318293da26102e57189dc7373c60)
- [ISMAP-LIU Introduction Materials (April 1, 2025)](https://www.ismap.go.jp/csm/sys_attachment.do?sys_id=097c91ad8369fa10aa68c6a8beaad316)
- [Cabinet Cybersecurity Center: Information system Security Management and Assessment Program (ISMAP)](https://www.cyber.go.jp/policy/group/general/ismap.html)
- [AWS ISMAP Compliance Page](https://aws.amazon.com/compliance/ismap/)
- [Microsoft ISMAP Compliance Page](https://learn.microsoft.com/compliance/regulatory/offering-ismap)
- [Google Cloud ISMAP Registration Announcement](https://cloud.google.com/blog/ja/products/identity-security/google-cloud-completes-ismap-registration-for-looker)
- [Oracle Cloud Infrastructure ISMAP Compliance](https://www.oracle.com/jp/corporate/cloud-compliance/ismap/)
- [Sakura Cloud ISMAP Information](https://manual.sakura.ad.jp/cloud/ismap/index.html)
- [Cloudflare ISMAP Registration Announcement (January 2026)](https://www.cloudflare.com/press/press-releases/2026/cloudflare-successfully-completes-ismap-registration-to-support-japans/)
