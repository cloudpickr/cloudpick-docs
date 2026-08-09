---
title: "Understanding Multicloud"
description: "Explains the definition of multicloud, motivations for adoption, current adoption rates, and key challenges."
---

> Last reviewed: August 2026

## What is multicloud

Multicloud is a **strategy of deliberately combining and operating two or more public cloud vendors**. It's not simply about holding accounts with multiple vendors — it means distributing workloads purposefully across vendors and operating them in an integrated way.

:::note
ISO/IEC 22123-1 defines multicloud as *"a cloud deployment model in which public cloud services provided by two or more cloud service providers are used."*
:::

Let's distinguish multicloud from similar-sounding but distinct concepts.

| Strategy | Definition | Example |
| --- | --- | --- |
| **Multicloud** | Combining 2 or more public clouds | AWS (compute) + Google Cloud (AI/ML) |
| **Hybrid cloud** | Connecting on-premises + public cloud | In-house data center + AWS Direct Connect |
| **Multi-account** | Operating multiple accounts within a single vendor | Separating dev/staging/prod with AWS Organizations |

:::note
In practice, these three often overlap. If you operate "on-premises + AWS + Google Cloud," you are simultaneously hybrid and multicloud.
:::

## Adoption status

Multicloud is already a mainstream strategy.

- According to the CNCF Annual Survey 2024, about 60% of enterprises use 2 or more clouds.
- The Flexera 2024 State of the Cloud Report finds that 89% of enterprises have adopted a multicloud strategy.

## Motivations for adoption

### Avoiding vendor lock-in

Concentrating all workloads with a single vendor weakens your pricing negotiation power and leaves you vulnerable to the vendor's policy changes. Multicloud secures negotiating leverage and keeps the option of migration open in the long term.

### Regulation and data sovereignty

Depending on national regulations, certain data may need to be stored in a specific region, or only certified vendors may be usable. This leads to configurations where workloads are distributed across multiple vendors.

### Best-of-breed service specialization

A strategy of combining each vendor's strengths.

- **AI/ML**: Train with Google Cloud Vertex AI + BigQuery, serve with Amazon SageMaker AI
- **Data analytics**: Google Cloud BigQuery (analytics) + AWS S3 (storage)
- **Enterprise**: Azure Entra ID (identity integration) + AWS (infrastructure)
- **Database-centric**: OCI Autonomous Database + AWS (application servers)

### M&A and organizational integration

During a merger or acquisition, if the acquired company uses a different vendor, coexisting as multicloud is often more realistic than immediate consolidation.

### Availability and disaster recovery

A pattern of placing core services on standby with a different vendor to prepare for a single vendor's global outage. However, since cost and complexity are high, it's rare to adopt multicloud for this reason alone.

## Challenges

Multicloud is not free. Make sure you're prepared to accept the costs below before proceeding.

### Increased operational complexity

- Each vendor has a different network model, IAM system, and monitoring tools
- Even with IaC (Terraform, etc.) abstraction, vendor-specific differences can't be fully hidden
- Root-causing incidents is harder than with a single vendor

### Fragmented team expertise

- It's difficult for engineers to master 2–3 vendors deeply
- Silos like "AWS team / Azure team" erase the benefits of integrated operations
- The pool of candidates with multicloud experience is narrow

### Egress costs

Moving data between clouds incurs egress (outbound) fees. Architectures that frequently transfer large volumes of data between clouds can see costs rise sharply. See [Understanding the Cost Structure](../../about-cloud/pricing-model/) for each vendor's free tier and pricing.

:::note
Using dedicated connections (Direct Connect, ExpressRoute, etc.) lowers the egress rate, but adds circuit costs.
:::

### Fragmented observability

- Each vendor's monitoring tools (CloudWatch, Azure Monitor, Cloud Monitoring) are separate
- Adopting a third-party tool such as Datadog or Grafana Cloud becomes essentially required for unified observability
- Distributed tracing becomes more complex when it crosses cloud boundaries

### Expanded security perimeter

- The attack surface grows with the number of vendors
- Without adopting unified identity management (Okta, Entra ID, etc.), account management becomes fragmented
- The scope of compliance audits widens

### Day-2 operational burden

The complexity of multicloud becomes apparent in ongoing operations (Day-2) after initial build-out (Day-1).

- **Duplicate IAM audits** — Separate permission reviews, cleanup of unused accounts, and policy audits must be performed per vendor
- **Incident ownership** — When a communication failure occurs between clouds, it's hard to determine which vendor is at fault. You may need to open tickets with both vendors simultaneously
- **Patch/update coordination** — Since maintenance schedules differ by vendor, change management must account for the possibility of simultaneous outages
- **Cost governance** — Different billing systems per vendor make unified cost analysis difficult. Standardization tools such as the FinOps FOCUS spec are needed

## When you should not go multicloud

In the following situations, focusing on a single vendor is the better choice.

| Situation | Reason |
| --- | --- |
| Small team (10 people or fewer) | Cannot absorb the overhead of multicloud operations |
| No clear regulatory requirement | Weak motivation for vendor separation |
| Architecture with frequent data movement | Egress costs offset the benefits |
| Deep dependency on vendor-specific services | Abstraction cost is too high (e.g., DynamoDB, Cosmos DB) |
| "Because everyone else is doing it" | Multicloud without a strategy only adds complexity |

:::caution
**Core principle:** Multicloud is a means, not an end. If you don't have a clear answer to "why do we need multiple vendors?", operating well on a single vendor is the better strategy.
:::

## Checklist before starting multicloud

If you're considering adopting multicloud, answer the questions below.

- [ ] Is there a concrete business/regulatory reason to adopt multicloud?
- [ ] Are the criteria for which workloads go to which vendor clearly defined?
- [ ] Have you reviewed the network connectivity method and cost between clouds?
- [ ] Do you have a unified identity management (IdP federation) strategy?
- [ ] Have you selected a unified monitoring/observability tool?
- [ ] Do you have the capability to manage multiple vendors with IaC?
- [ ] Is your team large enough to operate 2 or more vendors?

---

## Common mistakes

- **"Multicloud automatically increases availability"** — Multicloud DR carries very high dual-operation cost and complexity. Single-vendor multi-region is often more realistic.
- **"We should do it because everyone else is doing it"** — Adopting it without a clear business/regulatory reason only adds complexity. Answer "why do we need it" first.
- **"Abstracting with Terraform makes vendor differences disappear"** — IaC can unify provisioning, but differences in the operational model — IAM, networking, monitoring — still remain.

## References

### AWS

- [AWS — Prescriptive Guidance: Strategy for multicloud](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-multicloud/welcome.html)

### Azure

- [Azure — Cloud Adoption Framework](https://learn.microsoft.com/azure/cloud-adoption-framework/)

### Google Cloud

- [Google Cloud — Hybrid and Multi-cloud Reference Architectures](https://cloud.google.com/architecture/network-hybrid-multicloud)

### OCI

- [OCI — Multicloud Solutions](https://docs.oracle.com/en/solutions/oci-best-practices/deploy-multicloud-oci-oracle-database-services1.html)

### Standards and community

- [ISO/IEC 22123-1 — Cloud computing: Concepts and terminology](https://www.iso.org/standard/82758.html) — Official multicloud definition
- [ISO/IEC 22123-3 — Multi-cloud reference architecture](https://www.iso.org/standard/90339.html) — Multicloud reference architecture standard
- [NIST SP 500-292 — Cloud Computing Reference Architecture](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture) — Cloud reference architecture
- [NIST Multi-Cloud Security Public Working Group](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture) — Multicloud security reference
- [CNCF Annual Survey 2024](https://www.cncf.io/reports/cncf-annual-survey-2024/) — Cloud-native adoption status, multicloud statistics
- [FinOps Foundation — FOCUS Specification](https://finops.org/framework) — Multicloud cost data standardization
- [Cloud Security Alliance — Security Guidance](https://cloudsecurityalliance.org/research/guidance) — Multicloud security guidance
