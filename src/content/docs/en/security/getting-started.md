---
title: "Getting Started with Cloud Security"
description: "A structured reading guide to the security section, organizing the cloud security approach and the areas it protects."
---

> Last reviewed: August 2026

## Security Starts with "What to Protect"

The first step in cloud security is not setting up a firewall. You should approach it in the order **asset identification → threat modeling → protection priority**.

1. **Asset identification** — if you don't know what to protect, you don't know what to block.
2. **Data classification** — grade data as Public / Internal / Confidential / Restricted, and determine the level of protection appropriate for each grade.
3. **Threat modeling** — identify who might target what, and through which paths.
4. **Protection priority** — address the threats with the greatest potential impact first.

## A Shift in Cloud Security Perspective

On-premises and cloud environments take different approaches to security.

| On-premises (traditional) | Cloud (modern) |
| --- | --- |
| Perimeter defense (blocking with firewalls) | Zero trust (verify every request) |
| Prevention-focused | Detection + automated response after the fact (audit logs, anomaly detection) |
| Manual audits (quarterly) | Continuous auditing (real-time compliance) |
| Static policy | Policy as code (OPA, SCP, Azure Policy) |
| Change control boards | Guardrails + automated blocking (preventive controls) |

:::note
Key takeaway: don't simply block everything up front. Instead, **verify with audits, block with policy, and catch with detection**.
:::

## Structure of Protection Areas — A Reading Guide to the Security Section

Cloud security is built from multiple layers. Below is a mapping of each layer to its corresponding CloudPick documentation.

| Layer | Role | CloudPick documentation |
| --- | --- | --- |
| Governance & policy | Scope of responsibility, compliance | [Shared Responsibility Model](../../about-cloud/shared-responsibility/), [Compliance](../../governance/compliance/) |
| Identity & access control | Who can do what | [IAM Deep Dive](../../security/iam/), [Zero Trust](../../security/zero-trust/) |
| Network security | Traffic isolation and filtering | [VPC/Subnets](../../networking/vpc-subnet/) |
| Data protection | Encryption, key management, DLP | [Data Protection](../../security/data-protection/), [Secrets Management](../../security/secrets/) |
| Detection & response | Threat detection, incident response | [Security Posture Management](../../security/security-posture/), [Incident Response](../../security/incident-response/) |
| DevSecOps | Pipeline security | [DevSecOps](../../devops/devsecops/) |
| AI security | Model/data protection | [AI Security](../../security/ai-security/) |

## Security Maturity Stages

Don't try to apply everything at once. Build maturity in stages.

| Stage | Focus | Examples |
| --- | --- | --- |
| 1. Foundations | Least-privilege IAM, MFA, basic encryption | Locking the root account, enabling default encryption |
| 2. Visibility | Logging, auditing, asset inventory | Enabling CloudTrail, Config, Security Hub |
| 3. Automation | Policy as code, automated detection/blocking | SCP, GuardDuty, automated isolation |
| 4. Continuous | Red teaming, security chaos engineering, threat intelligence | Penetration testing, regular threat modeling |

## Common Mistakes

- **Adopting security tools before identifying assets** — turning on GuardDuty/Defender without knowing what to protect just piles up alerts without any way to prioritize them
- **Trying to apply everything at once** — ignoring the maturity stages and attempting to adopt zero trust all at once, ending up with nothing fully completed
- **Operating without audit logs enabled** — failing to turn on CloudTrail/Activity Log makes it impossible to trace the cause when an incident occurs

## Checklist

- [ ] Have you identified the assets to protect and completed data classification (public/internal/confidential/restricted)?
- [ ] Have you enabled audit logs (CloudTrail, Activity Log, Audit Log) across all accounts?
- [ ] Have you completed security maturity stage 1 (least-privilege IAM, MFA, basic encryption) first?

## References

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [Azure Security Documentation](https://learn.microsoft.com/azure/security/)
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
