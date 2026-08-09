---
title: "Multicloud Network Architecture"
description: "Explains transit architectures such as Hub-and-Spoke, Cross-Cloud Interconnect, egress cost optimization, and multicloud DNS integration strategy."
---

> Last reviewed: August 2026

:::note
For an overview of connectivity methods and CIDR design, see [Multicloud Network Design Fundamentals](../../networking/multicloud-networking/).
:::

## Transit Architecture Patterns

### Hub-and-Spoke

A pattern that places a central hub and connects each cloud as a spoke.

```mermaid
graph TD
    Hub[Hub VPC / Transit] --> AWS[AWS Spoke]
    Hub --> Azure[Azure Spoke]
    Hub --> Google Cloud[Google Cloud Spoke]
    Hub --> OCI[OCI Spoke]
```

- **Hub location:** the vendor with the most traffic, or on-premises
- **Advantages:** security policy managed centrally at the hub, simplified routing
- **Disadvantages:** the hub can become a bottleneck/single point of failure

### Service Mapping by Inter-Cloud Connection Type

| Vendor | Internal transit | Direct inter-cloud connection |
| --- | --- | --- |
| AWS | Transit Gateway | AWS Interconnect – multicloud |
| Azure | Virtual WAN / VNet Peering | (partner integration: Google Cross-Cloud, Oracle Interconnect) |
| Google Cloud | Cloud Router / NCC | Google Cross-Cloud Interconnect |
| OCI | DRG (Dynamic Routing Gateway) | Oracle Interconnect (Azure, Google Cloud, AWS) |

## Direct Inter-Vendor Connections (Cross-Cloud Interconnect)

Major CSPs, despite being competitors, provide dedicated inter-vendor networks in response to customer demand for multicloud. This lets you connect clouds privately without going over the internet.

At AWS re:Invent in December 2025, AWS and Google Cloud announced a joint multicloud interconnect based on an **open interoperability spec**. Microsoft Azure has also confirmed participation in this spec, and Oracle announced integration as well (April 2026). This is not a single vendor's initiative — it's an industry-wide movement toward standardizing multicloud interoperability.

| Service | Connection segment | Status (as of June 2026) |
| --- | --- | --- |
| [**AWS Interconnect – multicloud**](https://aws.amazon.com/interconnect/multicloud/) | AWS ↔ Google Cloud | GA (April 2026). Azure, OCI to be added within 2026 |
| [**Google Cross-Cloud Interconnect**](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/cross-cloud-overview) | Google Cloud ↔ AWS/Azure/OCI | GA. Based on the open interoperability spec |
| [**Oracle Interconnect for Azure**](https://docs.oracle.com/iaas/Content/multicloud/interconnect-azure.htm) | OCI ↔ Azure | GA. Cross-cloud data transfer is free |
| [**Oracle Interconnect for AWS**](https://docs.oracle.com/iaas/Content/multicloud/interconnect-aws.htm) | OCI ↔ AWS | LA (Limited Availability, May 2026). Single us-east-1 region. Expansion planned at GA |
| [**Oracle Interconnect for Google Cloud**](https://docs.oracle.com/iaas/Content/Network/Concepts/access-to-google-cloud-platform.htm) | OCI ↔ Google Cloud | GA. Cross-cloud data transfer is free |

### Availability Matrix

> ✅ GA = Generally Available, 🔶 LA = Limited Availability (restricted regions), Planned = not yet released

| | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **AWS** | — | Planned (2026) | ✅ GA | 🔶 LA |
| **Azure** | Planned (2026) | — | ✅ GA | ✅ GA |
| **Google Cloud** | ✅ GA | ✅ GA | — | ✅ GA |
| **OCI** | 🔶 LA | ✅ GA | ✅ GA | — |

### Cross-Cloud Interconnect vs Dedicated Connection + IX

| Comparison item | Cross-Cloud Interconnect | Dedicated connection + IX (Direct Connect + ExpressRoute, etc.) |
| --- | --- | --- |
| **Path** | Direct inter-vendor connection (single hop) | Via an IX or colocation facility (2-3 hops) |
| **Setup complexity** | Select the counterpart vendor in the console, then provision | Dedicated connections on both sides + IX port + BGP configuration |
| **Latency** | Minimal (direct connection within the same metro) | Slightly higher via the IX |
| **Cost structure** | Port cost + data transfer (free transfer on OCI) | Both-side dedicated connection cost + IX port cost |
| **Available segments** | Only segments the vendor supports | Any segment where an IX exists |

**Selection criteria:**

- If direct inter-vendor connectivity is supported for the segment, Cross-Cloud Interconnect is simpler and has lower latency
- For segments not yet supported (e.g., AWS ↔ Azure), or when on-premises must also be connected, use the IX-based approach

## Egress Cost Comparison

The largest cost factor in moving data between clouds is egress (outbound) fees.

| Segment | Unit price (Seoul region) | Notes |
| --- | --- | --- |
| AWS → internet | $0.126/GB (first 10TB) | Decreases afterward |
| Azure → internet | $0.12/GB | First 100GB/month free ([Bandwidth pricing](https://azure.microsoft.com/pricing/details/bandwidth/)) |
| Google Cloud → internet | $0.12/GB | First 200GB/month free |
| OCI → internet | 10TB/month free, then ~$0.0085/GB | Very cheap compared to competitors |
| AWS → Direct Connect | ~$0.04/GB | Circuit cost separate |
| Azure → ExpressRoute | Included (Unlimited plan) | Included in circuit cost |
| Google Cloud → Interconnect | ~$0.05/GB | Circuit cost separate |
| OCI → FastConnect | Included in the 10TB/month free tier | Circuit cost separate |

> The figures above are as of the time of writing and are subject to change. Check each vendor's official pricing for the latest figures.

### Cost Optimization Tips

- **Data locality:** place frequently-communicating workloads in the same cloud
- **Dedicated connections:** for over 1TB/month, a dedicated connection is more economical than a VPN
- **Compression/caching:** compress data before transferring it across cloud boundaries
- **Asynchronous batching:** move data that doesn't require real-time delivery in a nightly batch

## DNS Integration Strategy

DNS is at the core of service discovery in a multicloud environment. Since each vendor's private DNS is separate, an integration strategy is needed.

### Each Vendor's Private DNS

| Vendor | Service | Characteristics |
| --- | --- | --- |
| AWS | Route 53 Private Hosted Zone | VPC association, conditional forwarding |
| Azure | Azure Private DNS Zone | VNet link |
| Google Cloud | Cloud DNS Private Zone | VPC binding |
| OCI | OCI DNS Private View | VCN association |

### Integration Pattern: Conditional Forwarding

Forward to each cloud's private DNS endpoint based on the domain suffix.

| Domain pattern | Forwarding target |
| --- | --- |
| `*.aws.internal` | Route 53 Inbound Endpoint |
| `*.azure.internal` | Azure DNS Private Resolver |
| `*.gcp.internal` | Cloud DNS Inbound Policy |
| `*.oci.internal` | OCI DNS Inbound Endpoint |
| `*.corp.internal` | On-premises DNS |

**Implementation steps:**
1. Create an inbound DNS endpoint in each cloud
2. Set up conditional forwarding rules (based on domain suffix)
3. Use the on-premises DNS server or the hub VPC's DNS as the central forwarder

:::note
**Tip:** Using Route 53 Resolver's outbound endpoint as the hub lets AWS look up private records in Azure/Google Cloud.
:::

## Common Mistakes

- **Not estimating egress cost in advance** — Inter-cloud data movement can reach thousands of dollars a month. Calculate data flow and cost together during architecture design.
- **Not configuring DNS conditional forwarding, causing cross-cloud name resolution to fail** — Each cloud's private DNS is isolated by default. Always configure an inbound endpoint + forwarding rules.
- **Configuring only a single VPN tunnel with no hub network redundancy** — A hub failure stops all inter-cloud communication. Secure Active-Active or an alternate path.

## Checklist

- [ ] Is the monthly inter-cloud egress cost estimated, with threshold alerts configured?
- [ ] Can every cloud's private records be resolved mutually via DNS conditional forwarding?
- [ ] Has the alternate path (failover) been tested for a hub failure?

## References

### AWS

- [AWS — Hybrid Connectivity](https://docs.aws.amazon.com/whitepapers/latest/hybrid-connectivity/hybrid-connectivity.html)
- [AWS Direct Connect](https://aws.amazon.com/ko/directconnect/)
- [AWS Interconnect](https://aws.amazon.com/interconnect/)

### Azure

- [Azure — Hub-spoke Network Topology](https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke)
- [Azure ExpressRoute](https://azure.microsoft.com/ko-kr/products/expressroute/)

### Google Cloud

- [Google Cloud — Hybrid and Multi-cloud Network Architectures](https://cloud.google.com/architecture/network-hybrid-multicloud)
- [Google Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect)

### OCI

- [OCI FastConnect](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/fastconnect.htm)
- [Oracle Interconnect for Azure](https://docs.oracle.com/iaas/Content/multicloud/interconnect-azure.htm)

### Standards and Community

- [KINX](https://www.kinx.net/) — the largest domestic IX
- [Megaport](https://www.megaport.com/) — a global Cloud Exchange
- [NIST Multi-Cloud Security Public Working Group](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture)
- [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918)
