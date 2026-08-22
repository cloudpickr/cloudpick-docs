---
title: "Multicloud Network Design Fundamentals"
description: "Explains CIDR planning, a comparison of inter-cloud connection methods, and selection criteria for getting started with multicloud networking."
---

> Last reviewed: May 2026

:::note
For advanced topics such as transit architecture, egress cost, and DNS integration, see [Multicloud Network Architecture](../../networking/multicloud-connectivity/).
:::

## Why Inter-Cloud Networking Matters

The first technical challenge encountered in a multicloud environment is: "**how does a workload in Cloud A communicate with a workload in Cloud B?**" Within a single vendor, this is simply solved with VPC peering or a private link, but once you cross vendor boundaries, network design, cost, and security all become more complex.

## CIDR Planning — Preventing IP Conflicts

The first rule of multicloud: **no VPC/VNet CIDR across any cloud should overlap.**

If IPs overlap, routing becomes impossible, and changing it later requires redeploying workloads. Plan the entire IP space from the start.

### Recommended Design Pattern

Split the RFC 1918 private ranges by vendor.

| Range | Allocation | Example |
| --- | --- | --- |
| `10.0.0.0/8` | AWS | `10.0.0.0/16` (prod), `10.1.0.0/16` (dev) |
| `172.16.0.0/12` | Azure | `172.16.0.0/16` (prod), `172.17.0.0/16` (dev) |
| `192.168.0.0/16` | Google Cloud / other | `192.168.0.0/20` (Google Cloud), `192.168.16.0/20` (other) |

:::note
**Tip:** Assign at the `/16` level per vendor, and split into `/24` subnets within that — it's flexible for future expansion. If there's an on-premises environment, be sure to include its range in the plan too.
:::

### Cautions

- Since a Google Cloud VPC is global, only the per-region subnets need to differ
- An Azure VNet is regional, so a separate CIDR must be allocated per region

## Inter-Cloud Connection Methods

### Site-to-Site VPN

The fastest way to get started. Builds an IPsec tunnel over the internet.

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Service name** | Site-to-Site VPN | VPN Gateway | Cloud VPN | Site-to-Site VPN |
| **Max bandwidth** | 1.25 Gbps (per tunnel) | 10 Gbps (VpnGw5) | 3 Gbps (HA VPN) | 250 Mbps (per tunnel) |
| **HA configuration** | 2 tunnels provided by default | Active-Active mode | HA VPN (99.99% SLA) | Redundant tunnels recommended |
| **Cost (example)** | ~$0.05/h + egress | ~$0.19/h (VpnGw1) | ~$0.075/h + egress | Hourly billing + egress. Varies by region |

> The figures above are as of the time of writing and are subject to change. Check each vendor's official pricing for the latest figures.

**Example AWS ↔ Google Cloud connection:**
1. On AWS, create a Customer Gateway (Google Cloud's external IP) + VPN Connection
2. On Google Cloud, create an External VPN Gateway (AWS's external IP) + HA VPN tunnel
3. Exchange routes via BGP (AWS ASN: 64512, Google Cloud ASN: 65001, etc.)

:::note
**When to use:** bandwidth under 1Gbps, a quick PoC, cost-sensitive environments
:::

### Dedicated Connection (Dedicated Interconnect)

A connection over a dedicated physical circuit. Low latency and high bandwidth, but installation takes several weeks.

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Service name** | Direct Connect | ExpressRoute | Cloud Interconnect | FastConnect |
| **Max bandwidth** | 100 Gbps | 100 Gbps | 200 Gbps | 100 Gbps |
| **PoP** | Vendor IX/colocation. See country guides | Same | Same | Same |
| **Minimum commitment** | None (billed hourly per port) | None to 1 year | None | None (billed hourly per port) |
| **Egress discount** | ~50% discount vs. standard | Unlimited egress included | Discount vs. standard | 10TB/month egress free |

> The figures above are as of the time of writing and are subject to change. Check each vendor's official pricing for the latest figures.

:::note
**Azure ExpressRoute's distinctive point:** egress fees are included in the circuit fee, which can be the most economical option for large-volume data movement.
:::

### Cloud Exchange (Megaport, Equinix Fabric)

A Cloud Exchange is a service that lets you connect to multiple clouds simultaneously through a single physical connection. It's the most efficient connection method in a multicloud environment.

```mermaid
graph LR
    AWS[AWS DX] --> IX[Cloud Exchange / IX]
    Azure[Azure ER] --> IX
    Google Cloud[Google Cloud CI] --> IX
    OCI[OCI FC] --> IX
```

**Cloud Exchange options (global):**
- **Megaport**, **Equinix Fabric** — PoPs in many regions. Check country guides for whether a local PoP exists in the target country
- Country-specific IXes (e.g., KINX in Korea) are covered in country guides such as [Korea](../../korea/)

:::note
**When to use:** when connecting 3 or more clouds, or when on-premises must also be connected
:::

### Connection Method Selection Guide

| Criterion | Site-to-Site VPN | Dedicated connection (DX/ER/CI/FC) | Cloud Exchange |
| --- | --- | --- | --- |
| **Bandwidth** | ~1 Gbps | 10-100 Gbps | 1-10 Gbps |
| **Latency** | Via internet (variable) | Dedicated circuit (stable) | Dedicated circuit (stable) |
| **Build time** | Minutes to hours | Weeks to months | Days to weeks |
| **Initial cost** | Low | High (port fee, circuit fee) | Medium |
| **Monthly data transfer volume** | < 1TB | > 5TB | 1-5TB |
| **Connection target** | 1:1 (2 clouds) | 1:1 | 1:N (multiple clouds simultaneously) |
| **Suitable for** | PoC, small scale, quick start | Large volume, high reliability required, production | Connecting 3+ clouds, flexibility |

## Design Checklist

- [ ] Do the CIDRs of every cloud/on-premises environment avoid overlap?
- [ ] Was the connection method (VPN vs. dedicated connection vs. Cloud Exchange) chosen based on bandwidth/cost?
- [ ] Was the egress cost estimated on a monthly basis?
- [ ] Is cross-cloud name resolution possible via DNS conditional forwarding?
- [ ] Is there an alternate path (failover) for a hub failure?
- [ ] Do security group/firewall rules allow inter-cloud traffic?

## Common Mistakes

- **Using the default VPC in each cloud without CIDR planning** — Overlapping IP ranges make connectivity impossible later. Plan the entire IP space by vendor from the start.
- **Using the VPN from a PoC directly in production** — Insufficient bandwidth and variable internet-path latency cause incidents. Consider a dedicated connection for over 1TB/month.
- **Not allowing inter-cloud traffic in security groups/firewalls** — Even with a VPN/dedicated connection configured, communication fails without firewall rules on both sides.

## Related Documents

Transit architecture patterns, a detailed egress cost comparison, and DNS integration strategy are covered in the following document.

- [Multicloud Connectivity (advanced)](../../networking/multicloud-connectivity/)

## References

- [AWS Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)
- [Azure ExpressRoute](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)
- [Google Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/overview)
- [OCI FastConnect](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/fastconnect.htm)
- [RFC 1918 — Address Allocation for Private Internets](https://datatracker.ietf.org/doc/html/rfc1918)
- [Megaport](https://www.megaport.com/) — global Cloud Exchange
- [Equinix Fabric](https://www.equinix.com/products/equinix-fabric) — global Cloud Exchange. See country guides for local IXes
