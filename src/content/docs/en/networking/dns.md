---
title: "DNS"
description: "Compares managed DNS, routing policies, DNSSEC, and Private DNS across vendors."
---

> Last reviewed: August 2026

## Overview

**DNS** (Domain Name System) is the service that translates a domain name (e.g., example.com) into an IP address. Since it's the first step of every internet communication, if DNS goes down, the entire service becomes unreachable.

On-premises, you'd run BIND or Windows DNS yourself, but managed cloud DNS runs on a global Anycast network with no single point of failure. AWS Route 53, Google Cloud Cloud DNS, and Azure DNS all offer a **100% availability SLA**.

:::note
If DNS goes down, the service URL itself stops responding, making the entire service unreachable. In production, keep **TTL low** (300 seconds or less) so DNS failover propagates quickly.
:::

Beyond simple name resolution, DNS also includes traffic management features such as geographic routing, health-check-based failover, and weighted distribution.

## DNS Record Types

Commonly used DNS record types.

| Record | Purpose | Example |
| --- | --- | --- |
| **A** | Maps a domain to an IPv4 address | `example.com → 93.184.216.34` |
| **AAAA** | Maps a domain to an IPv6 address | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | Aliases to another domain name | `www.example.com → example.com` |
| **MX** | Specifies mail servers (with priority) | `example.com → 10 mail.example.com` |
| **TXT** | Text information (SPF, DKIM, domain ownership verification) | `v=spf1 include:_spf.google.com ~all` |
| **NS** | Specifies the authoritative name servers for the domain | `example.com → ns1.example.com` |
| **SRV** | Specifies a service location (including port) | `_sip._tcp.example.com → 10 60 5060 sip.example.com` |
| **PTR** | Reverse-maps an IP to a domain | `34.216.184.93.in-addr.arpa → example.com` |
| **ALIAS/ANAME** | Similar to CNAME but usable at the root domain | AWS Alias, Azure Alias, Google Cloud's own ALIAS record type (Public Zone only) |

### AWS's Alias Record Characteristics

AWS Route 53's **Alias Record** looks like a CNAME, but it's resolved internally by AWS rather than through a DNS query, so it's usable at the root domain (zone apex) and incurs no cost. It's used to point to AWS resources such as ELB, CloudFront, and S3 website hosting.

## Hosted Zones (Public vs Private)

A DNS hosted zone is the container that manages a domain's records. A **Public Zone** manages records reachable from the internet, and a **Private Zone** manages records resolved only inside a VPC/VNet.

### Split-Horizon DNS

A pattern where the same domain returns different records depending on the origin of the request.

- Internal users (within the VPC) → respond with a private IP
- External users (internet) → respond with a public IP

This lets you use the same domain for an internal API endpoint without exposing it externally.

### Vendor Implementations

| Vendor | Public Zone | Private Zone | Split-horizon |
| --- | --- | --- | --- |
| AWS | Route 53 Public Hosted Zone | Route 53 Private Hosted Zone (VPC association) | Implemented by separating Public/Private Zones |
| Azure | Azure Public DNS Zone | Azure Private DNS Zone (VNet link, auto registration) | Public/Private Zone separation |
| Google Cloud | Cloud DNS Public Zone | Cloud DNS Private Zone (VPC binding) | Native split-horizon support |
| OCI | OCI DNS Public Zone | OCI DNS Private Views (VCN association) | DNS Views for conditional responses |

### Usage Scenarios

- **Hybrid environments**: name resolution between on-premises↔cloud (conditional forwarding)
- **Multi-VPC**: centralized DNS management — a shared services VPC connects its Private Zone to other VPCs
- **Security isolation**: use convenient names for internal DB/API endpoints without exposing them externally

For DNS integration in a multicloud environment (conditional forwarding, cross-vendor resolution), see [Multicloud Connectivity — DNS Integration Strategy](../../networking/multicloud-connectivity/).

## Product Comparison

| Vendor | Product | Positioning |
| --- | --- | --- |
| AWS | Route 53 | All-in-one: domain registration + DNS + health checks + routing policies. 100% SLA |
| Azure | Azure DNS + Traffic Manager | DNS hosting and traffic routing are separate services. **100% SLA** |
| Google Cloud | Cloud DNS | 100% SLA. Native DNSSEC support. No built-in health checks |
| OCI | OCI DNS | Global Anycast. Provides routing policy via Traffic Management |

### Routing Policies

Routing policies for controlling traffic at the DNS level.

| Policy | Description | AWS Route 53 | Azure Traffic Manager | Google Cloud Cloud DNS | OCI DNS Traffic Management |
| --- | --- | --- | --- | --- | --- |
| **Geographic** | Route based on user location | Geolocation / Geoproximity | Geographic | Geolocation | Geolocation Steering |
| **Weighted** | Ratio-based distribution (A/B testing, gradual rollout) | Weighted | Weighted | Weighted Round Robin | Load Balancer |
| **Failover** | Switch to a backup endpoint on health-check failure | Failover | Priority | — (separate health checks) | Failover |
| **Latency-based** | Route to the fastest region | Latency | Performance | — | — |
| **Multivalue** | Return multiple IPs + health checks | Multivalue Answer | — | — | — |

### Health Checks

| Vendor | Feature | Notes |
| --- | --- | --- |
| AWS | Route 53 Health Checks | HTTP/HTTPS/TCP. Integrated with CloudWatch alarms. Automatic DNS failover on failure |
| Azure | Traffic Manager Probes | HTTP/HTTPS/TCP. Endpoint monitoring |
| Google Cloud | — | Cloud DNS has no built-in health checks. Combine with Cloud Load Balancing health checks |
| OCI | Health Checks | HTTP/HTTPS/TCP. Integrated with DNS Traffic Management |

## Key Differences

- **AWS Route 53** — All-in-one, from domain registration to routing. Offers the widest variety of routing policies (Geoproximity, Multivalue, etc.).
- **Azure** — DNS hosting (Azure DNS) and global traffic routing (Traffic Manager) are separate services. Traffic Manager acts as a DNS-based global load balancer.
- **Google Cloud Cloud DNS** — Its strengths are native DNSSEC support and native split-horizon support. It has no built-in health checks, so failover needs to be combined with Cloud Load Balancing.
- **OCI DNS** — Traffic Management provides geographic routing, failover, and other policies, and integrates with Health Checks for automatic DNS failover.

## DNSSEC

**DNSSEC** (DNS Security Extensions) is a security extension that prevents DNS response tampering. It blocks DNS spoofing/cache poisoning attacks, where an attacker intercepts a DNS response to redirect victims to a malicious site.

| Vendor | Support level |
| --- | --- |
| AWS Route 53 | Supports DNSSEC signing and registration |
| Azure DNS | Supports DNSSEC signing |
| Google Cloud Cloud DNS | Supports DNSSEC signing (default-enable option) |
| OCI DNS | Supports DNSSEC signing |

## Common Mistakes

- **Setting a TTL that's too long (e.g., 86400 seconds) while configuring failover** — DNS propagation can take up to 24 hours. Set TTL to 300 seconds or less for records requiring failover.
- **Using CNAME at the root domain (zone apex)** — This violates DNS standards and won't work. Use AWS Alias, Azure Alias, or Google Cloud's ALIAS record.
- **Configuring Failover routing without health checks** — Failover won't happen even if an incident occurs. Routing policy and health checks must always be configured together.

## Checklist

- [ ] Is the TTL on your production domain set to match failover requirements (recommended: 300 seconds or less)?
- [ ] Are health checks configured, and does automatic DNS failover work on an incident?
- [ ] Is DNSSEC enabled to prevent DNS spoofing/cache poisoning?

## Related Documents

- [Load Balancer](../../networking/load-balancer/)
- [CDN](../../networking/cdn/)
- [Multicloud Connectivity](../../networking/multicloud-connectivity/)

## References

### AWS

- [Amazon Route 53 Documentation](https://docs.aws.amazon.com/ko_kr/route53/)
- [Route 53 Routing Policies](https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/routing-policy.html)
- [Route 53 Health Checks](https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/health-checks-creating.html)

### Azure

- [Azure DNS Documentation](https://learn.microsoft.com/ko-kr/azure/dns/)
- [Azure Traffic Manager Documentation](https://learn.microsoft.com/ko-kr/azure/traffic-manager/)
- [Azure DNS SLA (100%)](https://azure.microsoft.com/en-us/support/legal/sla/dns/v1_1/)

### Google Cloud

- [Cloud DNS Documentation](https://cloud.google.com/dns/docs)
- [Cloud DNS ALIAS Record Overview](https://cloud.google.com/dns/docs/records-overview)

### OCI

- [OCI DNS Documentation](https://docs.oracle.com/en-us/iaas/Content/DNS/home.htm)
