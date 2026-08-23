---
title: "Data Protection and Workload Security"
description: "Compares encryption in transit/at rest, WAF, and network security across vendors."
---

> Last reviewed: August 2026

## Overview

Cloud security broadly falls into three areas.

- **Security in transit** — protecting data as it moves across the network
- **Security at rest** — protecting data stored in storage/databases
- **Workload security** — protecting running servers/containers/applications

## Encryption in Transit

Protects against eavesdropping or tampering as data moves across the network.

| Segment | Method | Notes |
| --- | --- | --- |
| **User ↔ service** | TLS/HTTPS | TLS terminated at the CDN or load balancer. Free certificates available (ACM, Let's Encrypt, etc.) |
| **Service ↔ service** | mTLS, VPC-internal communication | A service mesh (Istio, App Mesh) can automate mTLS |
| **Region ↔ region** | Vendor backbone encryption | AWS/Azure/Google Cloud all automatically encrypt inter-region traffic |
| **On-premises ↔ cloud** | VPN (IPsec) / dedicated line | Direct Connect, ExpressRoute, Cloud Interconnect |

Communication between managed services is encrypted with TLS by default across all vendors.

## Encryption at Rest

Encrypts stored data so it cannot be read even if it is physically stolen. All major CSPs provide default encryption, and the level of key management chosen affects the balance between security and operational complexity:

- **Vendor-managed keys** — simplest. The vendor generates/rotates/manages the keys. Suitable for most workloads.
- **Customer-managed keys** (CMK) — you control the rotation cadence and access policies directly. Meets regulatory requirements.
- **Your own keys** (BYOK/EKM/HYOK) — keys are managed in an on-premises HSM. Suitable for the strictest regulatory requirements.

:::note
For a vendor comparison of KMS services, details on CMK/BYOK/EKM, and HSM options, see [Secrets Management — Encryption Key Management Models](../../security/secrets/).
:::

## Post-Quantum Cryptography

:::note
**Who needs this section:** organizations that retain sensitive data (financial, healthcare, public sector) for 10+ years, or whose regulators require a PQC transition roadmap. If you only handle short-lived data, treat this as background awareness rather than an immediate action item.
:::

The algorithms used today for HTTPS, VPN, and data encryption — RSA, ECDH, and the like — could be broken once quantum computers become large enough. The problem isn't "after" quantum computers arrive — it's "now." Attackers can already collect encrypted traffic today and decrypt it later once a sufficiently powerful quantum computer exists — a **Harvest Now, Decrypt Later** attack.

In response, NIST has finalized new cryptographic standards, and major cloud vendors have begun their transition.

### NIST PQC Standards

| Standard | Purpose | Algorithm | Status |
| --- | --- | --- | --- |
| **FIPS 203** (ML-KEM) | Key exchange | Kyber-based lattice cryptography | Finalized August 2024 |
| **FIPS 204** (ML-DSA) | Digital signatures | Dilithium-based lattice cryptography | Finalized August 2024 |
| **FIPS 205** (SLH-DSA) | Digital signatures (stateless) | SPHINCS+-based hash signatures | Finalized August 2024 |
| **HQC** | Backup KEM | Code-based cryptography | Selected March 2025 |

### PQC Transition Status by Vendor

| Vendor | Status | Reference |
| --- | --- | --- |
| AWS | KMS supports ML-KEM hybrid TLS. PQ hybrid key exchange being applied to inter-service communication for S3, ACM, and others | [AWS Post-Quantum Cryptography](https://aws.amazon.com/security/post-quantum-cryptography/) |
| Azure | Microsoft Quantum Safe Program. ML-KEM/ML-DSA implemented in the SymCrypt library. TLS 1.3 hybrid key exchange supported | [Microsoft Quantum Safe](https://www.microsoft.com/en-us/security/blog/topic/quantum-safe/) |
| Google Cloud | PQC digital signatures (ML-DSA) in preview in Cloud KMS. ML-KEM hybrid deployment completed in Chrome/BoringSSL | [Google Cloud PQC](https://cloud.google.com/blog/products/identity-security/quantum-safe-digital-signatures-in-cloud-kms) |
| OCI | Has announced a PQC algorithm roadmap for OCI Vault and other services. Confirm hybrid TLS mode for Oracle Database and similar items against the official roadmap/release notes (link to be updated once specific product documentation is published) | [Oracle Security](https://www.oracle.com/security/) (general hub; check official documentation for a dedicated PQC page) |

### PQC Transition Strategy

1. **Inventory** — identify the encryption algorithms, certificates, and key sizes in use (a Crypto Agility Inventory)
2. **Hybrid mode** — use existing algorithms alongside PQC algorithms simultaneously to maintain compatibility during the transition
3. **Prioritization** — transition long-retention data (10+ year lifespan) and signing infrastructure first
4. **Testing** — since PQC algorithms have larger key/signature sizes, measure the network overhead and handshake latency impact

:::caution
The PQC transition is a multi-year project. You don't need to change every system right now, but establishing **crypto agility** — an architecture that lets you swap algorithms — ahead of time is the key priority.
:::

## Confidential Computing

While traditional encryption protects data "at rest" and "in transit," confidential computing protects data **"in use."** Data is processed inside a hardware-based Trusted Execution Environment (TEE), so even the cloud vendor's administrators cannot access the data being processed.

| Vendor | Product | GPU confidential computing | Reference |
| --- | --- | --- | --- |
| AWS | [Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/) | — (the Nitro architecture itself provides hypervisor-level isolation) | [AWS Nitro](https://aws.amazon.com/ec2/nitro/) |
| Azure | [Confidential VMs (AMD SEV-SNP, Intel TDX)](https://learn.microsoft.com/azure/confidential-computing/) | **NCC H100 v5** — NVIDIA H100 confidential GPU | [Azure Confidential Computing](https://azure.microsoft.com/solutions/confidential-compute/) |
| Google Cloud | [Confidential VMs (AMD SEV, Intel TDX)](https://cloud.google.com/confidential-computing) | **A3 Confidential VM** — H100 confidential GPU | [GCP Confidential Computing](https://cloud.google.com/confidential-computing/docs) |
| OCI | [Confidential Computing (AMD SEV)](https://docs.oracle.com/en-us/iaas/Content/Compute/References/confidential-compute.htm) | — | [OCI Compute](https://docs.oracle.com/en-us/iaas/Content/Compute/home.htm) |

**Key use cases:**
- Protecting both model IP and input data simultaneously in AI/ML inference (confidential GPUs)
- Multi-party data analysis — joint computation without exposing the underlying raw data
- Workloads with strict data sovereignty requirements (sovereign cloud combined with confidential computing)

:::note
For protecting AI workloads with confidential computing, see [AI Security — Confidential AI Inference](../../security/ai-security/); for sovereign cloud approaches to data sovereignty, see [Landing Zone — Sovereign Landing Zone](../../governance/landing-zone/#sovereign-landing-zone).
:::

## Workload Security

Protects running infrastructure and applications.

### Network Security

Protecting data in transit requires network-level access control.

:::note
For a vendor comparison of network firewalls (Security Groups/NSG/Firewall Rules), see [VPC and Subnets](../../networking/vpc-subnet/); for network isolation architecture patterns (air-gap, preventive guardrails), see [Network Segregation and Isolation](../../security/network-isolation/).
:::

### Web Application Firewall (WAF)

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | [AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html) | Attaches to ALB/CloudFront/API Gateway. Managed rules + custom rules |
| Azure | [Azure WAF](https://learn.microsoft.com/azure/web-application-firewall/overview) (Front Door / App Gateway) | OWASP CRS 3.2 included by default. Policy-based management |
| Google Cloud | [Cloud Armor](https://cloud.google.com/armor/docs) | Integrated DDoS + WAF. Preconfigured WAF rules + adaptive protection (ML) |
| OCI | [OCI WAF](https://docs.oracle.com/en-us/iaas/Content/WAF/home.htm) | Integrates with Load Balancer/Edge. Provides OWASP rule sets |

#### OWASP and WAF Rules

The [OWASP Top 10](https://owasp.org/www-project-top-ten/) is an industry-standard summary of the most common web application security threats. Each vendor's WAF provides **managed rule sets** that address these threats.

Below is an excerpt of OWASP Top 10 items that **can be mitigated with WAF rules**:

| OWASP Top 10 threat | WAF rule response | Vendor managed rules |
| --- | --- | --- |
| A01 — Broken Access Control | Blocks path traversal, forced browsing | AWS Managed Rules (Core), Azure CRS, Cloud Armor preconfigured rules |
| A03 — Injection (SQL/XSS) | Pattern matching for SQL injection, XSS | AWS SQLi/XSS Rule Group, Azure CRS, Cloud Armor `sqli-v33-stable` |
| A05 — Security Misconfiguration | Blocks known vulnerable paths | AWS Known Bad Inputs, Azure CRS |
| A06 — Vulnerable Components | Blocks known CVE exploits | AWS Managed Rules (CVE), Azure Bot Manager |
| A07 — Authentication Failures | Blocks brute force, credential stuffing | AWS Account Takeover Prevention, Azure Rate Limiting |

#### Managed Rules vs. Custom Rules

| Aspect | Managed rules | Custom rules |
| --- | --- | --- |
| **Ownership** | Updated by the vendor or a security partner | Written and maintained directly by the user |
| **Best for** | Baseline OWASP Top 10 defense, rapid deployment | Application-specific logic, business rules |
| **Updates** | Automatically updated by the vendor when new threats are found | Updated directly by the user |
| **Cost** | Charged per rule group (AWS), included by default (Azure/Google Cloud/OCI) | Charged by rule count |

**Practical recommendations:**

- **Step 1** — apply managed OWASP rule sets first (start in Count mode to check for false positives, then switch to Block)
- **Step 2** — add application-specific custom rules (protecting specific API paths, geo-based blocking, etc.)
- **Step 3** — mitigate DDoS/brute force with rate-limiting rules
- **Logging** — store WAF logs in S3/Log Analytics/Cloud Logging to analyze attack patterns

Threat detection (GuardDuty, Defender, SCC, Cloud Guard) and container/runtime security (Inspector, Defender for Containers, etc.) are covered in detail in [Security Posture Management](../../security/security-posture/).

## Common Mistakes

- **Switching WAF straight to Block mode** — switching to blocking mode without checking for false positives, causing legitimate traffic to be blocked. Verify in Count mode first
- **Adopting BYOK when vendor-managed keys would suffice** — choosing self-managed keys without a regulatory requirement, only increasing operational complexity and failure risk
- **Accessing managed services without a VPC Endpoint** — accessing S3, KMS, etc. via a NAT Gateway, resulting in unnecessary internet exposure and cost
- **Deferring PQC transition until "after quantum computers arrive"** — already exposed to Harvest Now, Decrypt Later attacks. Long-retention data needs hybrid mode applied starting now

## Checklist

- [ ] Is encryption at rest enabled for all storage/databases (verify default encryption)?
- [ ] Have WAF managed rules been applied in Count mode first, with false positives confirmed before switching to Block?
- [ ] Is access to managed services (S3, KMS, etc.) done via VPC Endpoint / Private Link?
- [ ] Have you inventoried the encryption algorithms in use and established a PQC transition roadmap?
- [ ] Have you evaluated confidential computing for sensitive AI inference workloads?

## Related Documents

- [Security Posture Management](../../security/security-posture/)
- [Secrets Management](../../security/secrets/)
- [Practical IAM Design and Security Operations](../../security/iam/)
- [VPC and Subnets](../../networking/vpc-subnet/)

## References

### AWS

- [AWS Security documentation](https://docs.aws.amazon.com/ko_kr/security/)
- [AWS KMS documentation](https://docs.aws.amazon.com/ko_kr/kms/)
- [AWS WAF documentation](https://docs.aws.amazon.com/ko_kr/waf/)

### Azure

- [Azure Security documentation](https://learn.microsoft.com/ko-kr/azure/security/)
- [Azure Key Vault documentation](https://learn.microsoft.com/ko-kr/azure/key-vault/)
- [Azure WAF documentation](https://learn.microsoft.com/ko-kr/azure/web-application-firewall/)

### Google Cloud

- [Google Cloud Security documentation](https://cloud.google.com/security)
- [Cloud KMS documentation](https://cloud.google.com/kms/docs)
- [Cloud Armor documentation](https://cloud.google.com/armor/docs)

### OCI

- [OCI Vault documentation](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/home.htm)
- [OCI WAF documentation](https://docs.oracle.com/en-us/iaas/Content/WAF/home.htm)

### Post-Quantum Cryptography / Confidential Computing

- [NIST FIPS 203 — ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- [NIST FIPS 204 — ML-DSA](https://csrc.nist.gov/pubs/fips/204/final)
- [AWS Post-Quantum Cryptography](https://aws.amazon.com/security/post-quantum-cryptography/)
- [Azure Confidential Computing](https://learn.microsoft.com/azure/confidential-computing/)
- [Google Cloud Confidential Computing](https://cloud.google.com/confidential-computing)
