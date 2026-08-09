---
title: "Glossary"
description: "A vendor-neutral glossary of terms commonly used across the cloud documentation."
---

> Last reviewed: May 2026

A vendor-neutral glossary of terms commonly used across the cloud documentation.

## Infrastructure Basics

| Term | Meaning |
| --- | --- |
| On-Premises | Infrastructure operated directly in your own data center or office rather than in the cloud. |
| Region | A geographically separated cluster of data centers. Think of units like Seoul, Tokyo, or Virginia. |
| Availability Zone / Zone | A data center or group of data centers within a single region that is independently isolated from failures. Commonly abbreviated as AZ. |
| CIDR | Classless Inter-Domain Routing. A notation for expressing IP address ranges. Example: `10.0.0.0/16` denotes the range 10.0.0.0–10.0.255.255. |
| Edge Location | Small-scale infrastructure placed close to users. Primarily used for CDN, DNS, and edge security. |
| VPC / VNet / VCN | A logically isolated virtual network created within the cloud. |
| Subnet | A network segment created by dividing an IP range within a VPC into smaller blocks. |
| Load Balancer | A device or service that distributes traffic across multiple servers. |
| NAT Gateway | A service that lets private resources reach the internet outbound while blocking direct inbound access from outside. |
| Landing Zone | The initial foundational structure for operating a multi-account/subscription/project environment safely and consistently. |

## Compute

| Term | Meaning |
| --- | --- |
| Serverless | An execution model that reduces the burden of server management, letting you focus on running code or containers. |
| Container | A deployment unit that packages an application together with its runtime environment. |
| Kubernetes | An orchestration platform for deploying, scaling, and recovering containers. |
| Immutable Infrastructure | An operational approach where running servers are never modified — instead, they're replaced with a new image. |

## Storage

| Term | Meaning |
| --- | --- |
| Object Storage | Storage that saves files as objects. Commonly used for images, backups, logs, and data lakes. |
| Block Storage | Storage attached to a VM like a disk. |
| File Storage | Storage that lets multiple servers share the same file system. |

## Security

| Term | Meaning |
| --- | --- |
| IAM | Identity and Access Management. A system for managing who can do what to which resources. |
| MFA | Multi-Factor Authentication. A method requiring an additional verification factor beyond a password. |
| Least Privilege | A security principle of granting only the minimum permissions necessary. |
| JIT Access | Just-In-Time Access. An access model of request→approval→time-limited grant, instead of standing permissions. |
| Zero Trust | A security model based on "never trust, always verify." Access is controlled based on identity and context rather than network perimeter. |
| Network Segregation | Separating business networks from the internet to block external threats from reaching internal systems. Implemented through physical separation and logical separation (such as VPC isolation). |
| N2SF | Korea's National Network Security Framework. A framework that shifts from uniform network segregation toward tiered security based on classification levels — C (Confidential), S (Sensitive), O (Open). Version 1.0 was published by Korea's NCSC in 2025. |
| CSAP | Korea's Cloud Security Assurance Program. A certification that CSPs must obtain to provide cloud services to Korean public sector agencies. Operated under a three-tier system: High, Medium, Low. |
| SCP | Service Control Policy. A preventive guardrail in AWS Organizations that restricts which APIs are allowed or denied per account. Azure Policy and Google Cloud Organization Policy serve a similar role. |
| Guardrail | A preventive control that automatically enforces organizational policy to block risky configurations or actions before they happen. |
| Microsegmentation | A technique that finely partitions the network to restrict communication between workloads to least privilege. A core implementation mechanism of Zero Trust. |
| Workload Identity | An identity granted to applications/services rather than people. It allows access to cloud resources without long-term credentials. |
| Service Account | An account used by an application or automated process rather than a person. |
| Conditional Access | A policy that allows or blocks access based on context such as the user's location, device state, and time. |
| OIDC | OpenID Connect. An authentication protocol built on top of OAuth 2.0. Used for user identity verification and SSO. |
| SAML | Security Assertion Markup Language. An XML-based authentication/authorization standard used for enterprise SSO. |
| Temporary Credentials | Credentials valid only for a limited period of time. Includes STS tokens and session tokens. Synonym: temporary tokens. |
| Long-term Credentials | Credentials valid without expiration. Includes access keys and API keys. Using temporary credentials is recommended for security. |
| CSPM | Cloud Security Posture Management. A security management framework that continuously detects cloud misconfigurations. |
| CWPP | Cloud Workload Protection Platform. A platform that protects the runtime security of workloads such as VMs, containers, and serverless functions. |
| SIEM | Security Information and Event Management. A system that collects and correlates security events to detect threats. |
| SOAR | Security Orchestration, Automation and Response. A system that orchestrates automated responses to security events. |
| CIS Benchmark | A security configuration baseline provided by the Center for Internet Security. Provides standards for a variety of targets including OS, cloud, and databases. |
| WAF | Web Application Firewall. A firewall that protects web applications from L7 attacks such as SQL injection and XSS. |
| OWASP Top 10 | An industry-standard list of the 10 most common security threats to web applications. |
| CVE | Common Vulnerabilities and Exposures. A unique identifier assigned to a publicly disclosed security vulnerability. |
| CVSS | Common Vulnerability Scoring System. A standard for scoring vulnerability severity on a scale of 0–10. |
| SBOM | Software Bill of Materials. A list of all components (libraries, packages) included in a piece of software. |

## DevOps / DevSecOps

| Term | Meaning |
| --- | --- |
| IaC | Infrastructure as Code. An approach to defining infrastructure as code and managing it reproducibly. |
| CI/CD | Continuous Integration / Continuous Delivery or Deployment. An approach to automating build, test, and deployment. |
| Observability | The ability to understand system state through logs, metrics, and traces. |
| DevSecOps | An approach that builds security into the development (Dev) and operations (Ops) pipeline from the start. |
| GitOps | An operational approach that uses a Git repository as the single source of truth to automate infrastructure and application deployment. |
| Shift-Left | A principle of moving security verification earlier in the development process to catch problems sooner. |
| SAST | Static Application Security Testing. A technique for finding security vulnerabilities by analyzing source code without executing it. |
| DAST | Dynamic Application Security Testing. A technique for finding vulnerabilities by attacking a running application from the outside. |
| SCA | Software Composition Analysis. A technique for detecting known vulnerabilities (CVEs) and license violations in open source dependencies. |
| MLOps | An operational framework for automating and standardizing the training/deployment/monitoring of ML models. The ML equivalent of DevOps. |

## Governance / FinOps

| Term | Meaning |
| --- | --- |
| CapEx | Capital Expenditure. An approach of investing heavily upfront, such as purchasing servers and equipment. |
| OpEx | Operational Expenditure. An approach of paying for usage as you go, as with the cloud. |
| FinOps | An operating model in which engineering, finance, and business teams jointly manage cloud costs. |
| Showback | A model that only shows cloud usage costs by department/team. It shares awareness of "how much our team is spending" without deducting from an actual budget. |
| Chargeback | A model that deducts department-level cloud usage costs from that team's actual budget (P&L). Teams bear direct responsibility for costs. |
| HA | High Availability. A design that minimizes service disruption by eliminating single points of failure. Multi-AZ deployment is a representative example. |
| SLI | Service Level Indicator. A measurable metric such as availability or response time. |
| SLO | Service Level Objective. The target value for an SLI. Example: "99.9% monthly availability." |
| SLA | Service Level Agreement. An SLO formally promised to an external customer through a contract. Violations typically carry consequences such as credit compensation. |
| Error Budget | The amount of downtime an SLO permits. Example: a 99.9% SLO allows an error budget of 43 minutes per month. |
| RPO | Recovery Point Objective. The maximum acceptable amount of data loss, measured in time, during a failure. |
| RTO | Recovery Time Objective. The target time within which service must be restored after a failure. |
| DR | Disaster Recovery. A recovery strategy prepared for regional or large-scale outages. |

## AI / Machine Learning

| Term | Meaning |
| --- | --- |
| LLM | Large Language Model. A large-scale language model trained on massive amounts of text. Examples include GPT, Claude, and Gemini. |
| Foundation Model | A model pretrained on large-scale data and used broadly across a wide range of tasks. |
| RAG | Retrieval-Augmented Generation. An AI architecture that combines external knowledge retrieval results with LLM response generation. |
| Vector Store | A storage system that stores the meaning of text or images as vectors and provides similarity search. |
| Embedding | A conversion of text or images into a meaning-based array of numbers (a vector). Used for similarity search. |
| ANN | Approximate Nearest Neighbor. An algorithm that trades a small amount of accuracy for speed in vector search. |
| Prompt | The input message sent to a model. Includes questions, instructions, and context. |
| Prompt Engineering | The technique of designing and refining prompts so a model produces better responses. |
| Token | The unit in which a model processes text. Roughly one word equals 1–2 tokens, and most APIs bill by token count. |
| Fine-tuning | The technique of further training a pretrained model on specific data to adapt it to a domain. |
| Inference | The process by which a trained model takes an input and generates an output. Faster and cheaper than training. |
| Hallucination | The phenomenon where an LLM plausibly generates content that isn't factually true. Mitigated through techniques such as RAG. |
| Agent | A structure in which an LLM calls tools or performs multiple steps to automate a task. |
