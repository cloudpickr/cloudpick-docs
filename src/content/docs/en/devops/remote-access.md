---
title: "Remote Access Management"
description: "Compares managed services across vendors for securely accessing instances without SSH/RDP."
---

> Last reviewed: August 2026

## Overview

:::note[Prerequisites and related documents]
For network isolation and subnet design, see [VPC and Subnets](../../networking/vpc-subnet/); for identity and permission control, see [IAM](../../security/iam/) first. This document focuses on managed remote access that reaches instances without exposing public IPs.
:::

Traditionally, SSH (Linux) or RDP (Windows) is used to access servers. However, this comes with issues such as public IP exposure, SSH key management, and open security groups.

Cloud vendors provide **agent-based or proxy-based** managed access services, enabling secure access to instances in a private subnet without a public IP.

## Traditional Access vs Managed Access

| Item | Traditional (direct SSH/RDP) | Managed service |
| --- | --- | --- |
| **Public IP** | Required (or operate a separate Bastion Host) | Not required |
| **Port exposure** | Inbound 22/3389 must be allowed | No inbound rule needed |
| **Key management** | Manually distribute/rotate SSH keys | IAM-based authentication (no keys needed) |
| **Audit logs** | Requires separate configuration | Session logs recorded automatically |
| **Network path** | Internet → instance | Vendor internal channel (outbound only) |

## Vendor Service Comparison

| Item | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Service name** | [Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) | [Azure Bastion](https://learn.microsoft.com/azure/bastion/bastion-overview) | [Identity-Aware Proxy (IAP)](https://cloud.google.com/iap/docs/using-tcp-forwarding) | [OCI Bastion](https://docs.oracle.com/en-us/iaas/Content/Bastion/home.htm) |
| **Method** | Agent-based (SSM Agent) | Proxy-based (PaaS) | Proxy-based (TCP forwarding) | Proxy-based (managed Bastion) |
| **Public IP required** | No | No | No | No |
| **Inbound port** | None needed (outbound 443 only) | Not needed | Not needed | Not needed |
| **Authentication** | IAM policy | Entra ID + RBAC | IAM + IAP policy | IAM policy |
| **Session logs** | S3/CloudWatch Logs | Azure Monitor | Cloud Audit Logs | OCI Logging |
| **File transfer** | Supported (via S3 or port forwarding) | Native file upload | SCP over an IAP tunnel | Via SSH tunnel |
| **Cost** | Free (SSM Agent included by default) | Billed hourly by SKU | Free (IAP itself) | Free (per session) |

## Key Differences

**AWS Systems Manager Session Manager** — Works through the SSM Agent that's preinstalled on EC2. It's usable immediately with just IAM permissions, no separate infrastructure deployment, and no extra cost. Port forwarding lets you tunnel to other resources like RDS as well.

**Azure Bastion** — A PaaS service deployed into a VNet that lets you open SSH/RDP sessions directly from a browser (Azure Portal). No separate client installation is needed, but the Bastion host itself is billed hourly.

**Google Cloud Identity-Aware Proxy (IAP)** — Part of Google's zero-trust access model. TCP forwarding lets you create a tunnel not just for SSH/RDP but for any arbitrary port. The same IAP is also used for web application access control.

**OCI Bastion** — A managed Bastion service where you specify a TTL (up to 3 hours) when creating a session. It's automatically cleaned up after the session expires, leaving no long-lived access path.

:::note
**Reducing VPN reliance:** With AWS Verified Access supporting TCP/SSH/RDP/DB protocols in addition to HTTP(S), VPN reliance can be greatly reduced for the supported protocols. For a comparison of each vendor's ZTNA service, see [Zero Trust](../../security/zero-trust/).
:::

## Practical Recommendations

### Access Frequency and Operational Maturity

The frequency of direct access (shell login) to an instance is an indicator of operational maturity. More frequent access signals a lack of automation.

| Maturity level | Shell access frequency | Characteristics |
| --- | --- | --- |
| **Level 1 — Manual operations** | Daily, frequent | Log checks, config changes, deploys done manually. A pattern of living on the server |
| **Level 2 — Partially automated** | Several times a week | Deployment automated via CI/CD, monitoring dashboards built. Access only during incidents |
| **Level 3 — Observability-based** | Several times a month | Logs/metrics/traces are centralized and most issues resolved from the console. Access only for exceptional debugging |
| **Level 4 — Immutable/serverless** | Almost never | Problems resolved by replacing instances. Shell access itself is treated as a security event |

To reduce shell access, automate the following (target: Level 3 or higher):

| What used to be done in a shell | Alternative |
| --- | --- |
| Checking logs (`tail -f`) | Centralize with [Monitoring](../../devops/monitoring/) (CloudWatch Logs / Azure Monitor / Cloud Logging) |
| Editing config files | [Configuration management service](../../security/secrets/) (Parameter Store, App Configuration) + dynamic reload |
| Installing/updating packages | [Patch Manager](../../devops/patch-and-vulnerability/) + golden image pipeline |
| Restarting a service | Run Command or replacing an instance via Auto Scaling |
| Cleaning up disk space | CloudWatch Agent alert + automated script (EventBridge → Lambda) |
| Debugging (strace, tcpdump) | Mostly resolved with [observability](../../devops/observability/) tools. Session access only when unavoidable |

:::note
Think of it as: "**whenever you need to log into a server, that's an opportunity to automate it**." Regularly reviewing access logs to identify recurring reasons for access, and automating that work, naturally reduces access frequency.
:::

### Designing an Access Control Policy

Since shell access can't be eliminated entirely, design a policy for **who can access, when, and under what conditions**.

| Policy item | Recommendation |
| --- | --- |
| **Standing access** | Don't grant it. Use a Just-In-Time (JIT) approach: request when needed → approve → grant time-limited access |
| **Production access** | Require at least dual approval (dual control). Session recording is mandatory |
| **Development/test access** | Team-level autonomy, but with log recording |
| **Break-glass access** | A predefined emergency role. Post-hoc audit is mandatory. Reason must be recorded within 24 hours |
| **Access review** | Review access logs monthly. Identify unnecessary access patterns → automate |

**Examples of JIT access implementation:**

- **AWS** — IAM Identity Center + Permission Set (time-limited), or SSM Session Manager + Approval Workflow
- **Azure** — Privileged Identity Management (PIM) — approval + TTL when activating a role
- **Google Cloud** — PAM (Privileged Access Manager) — Just-In-Time access request/approval
- **OCI** — OCI Bastion session TTL (up to 3 hours) + IAM dynamic groups

### Access Method Selection Criteria

| Situation | Recommendation |
| --- | --- |
| Routine operations (log checks, config changes) | Use a managed service |
| Emergency incident response | Managed service + pre-configured permissions (break-glass) |
| Bulk command execution across servers | AWS Run Command / Azure Run Command / Google Cloud OS Config |
| Temporary access to dev/test environments | IAP tunnel or Session Manager port forwarding |
| SSH keys required by regulation | OCI Bastion (SSH key-based session) |

### Security Hardening Tips

- **Enforce MFA** — Set IAM policy to require MFA when starting a session
- **Session time limits** — Set an idle timeout and a maximum session duration
- **Centralize logging** — Send all session logs to a SIEM to detect anomalous access
- **Least privilege** — Scope the policy so access is limited to specific instances/tags
- **Network isolation** — Keep private subnets even when using a managed service

### Session Logging and Audit Trail

Shell access needs to be recorded: **who, when, on which instance, and what was executed**. This is the key evidence for audit response and incident analysis.

**Two layers of logs are needed:**

1. **API/management layer** — Records the act of "starting/ending a session" itself (who, when, where)
2. **Session layer** — Records "the commands and output executed within the session" (what was done)

| Vendor | API/management log | Session content log | Storage location |
| --- | --- | --- | --- |
| AWS | **CloudTrail** (`StartSession`, `TerminateSession`, `SendCommand`) | Session Manager session logging (command input/output stream) | CloudTrail → S3, session logs → S3/CloudWatch Logs |
| Azure | **Activity Log** (Bastion connection events) | Bastion diagnostic logs (connection metadata) | Log Analytics Workspace |
| Google Cloud | **Cloud Audit Logs** (IAP tunnel creation/termination) | OS Login audit logs (metadata only, command content not recorded) | Cloud Logging |
| OCI | **Audit Log** (Bastion session creation/expiration) | OCI Logging (session metadata) | OCI Logging / Object Storage |

**CloudTrail integration (AWS example):**

CloudTrail automatically records the "management actions" of session access:

- `StartSession` — Who opened a session on which instance (user ARN, instance ID, time)
- `TerminateSession` — Session end time
- `SendCommand` (Run Command) — Record of remote command execution (including command content)
- These events can integrate with [Security Posture Management](../../security/security-posture/)'s GuardDuty/Security Hub to automatically detect abnormal patterns

**Logging configuration checklist:**

- [ ] Confirm API audit logging is enabled (CloudTrail/Activity Log/Audit Logs — enabled by default in most cases)
- [ ] Enable session content logging (AWS: configure S3/CloudWatch in Session Manager Preferences)
- [ ] Enable command input/output recording (disabled by default on AWS — must be explicitly turned on)
- [ ] Set a log retention period (1-7 years depending on compliance requirements)
- [ ] Encrypt logs (encrypt at rest with KMS/Key Vault)
- [ ] Prevent log tampering (S3 Object Lock, immutable storage, etc.)
- [ ] SIEM integration (detect anomalous patterns: access at unusual hours, mass command execution, access to unapproved instances)

:::caution
**AWS Session Manager doesn't record command input/output by default.** You must explicitly enable logging to S3 or CloudWatch Logs in Session Manager Preferences. If not enabled, CloudTrail records only "who connected," not "what they did."
:::

## Common Mistakes

- **Opening SSH port 22 to 0.0.0.0/0** — This immediately exposes the instance to bot brute-force attacks. Using a managed access service removes the need to open an inbound port.
- **Sharing a common SSH key across multiple team members** — You can't identify who connected. Use IAM-based authentication to track access per individual.
- **Not enabling session logging** — There's no evidence of "who did what" when an incident occurs. AWS Session Manager is disabled by default, so it must be explicitly turned on.

## Checklist

- [ ] Do production instances have no public IP and get accessed only through a managed service (Session Manager/Bastion/IAP)?
- [ ] Is a JIT (Just-In-Time) approval workflow applied for production access?
- [ ] Is command input/output logged for every session, and does the retention period meet compliance requirements?

## References

### AWS

- [AWS Systems Manager Session Manager Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [AWS Run Command](https://docs.aws.amazon.com/systems-manager/latest/userguide/execute-remote-commands.html)

### Azure

- [Azure Bastion Documentation](https://learn.microsoft.com/azure/bastion/bastion-overview)
- [Azure Run Command](https://learn.microsoft.com/azure/virtual-machines/run-command-overview)

### Google Cloud

- [Google Cloud IAP TCP Forwarding Documentation](https://cloud.google.com/iap/docs/using-tcp-forwarding)

### OCI

- [OCI Bastion Documentation](https://docs.oracle.com/en-us/iaas/Content/Bastion/home.htm)
- [OCI IAM Dynamic Groups and Policies](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingdynamicgroups.htm)
