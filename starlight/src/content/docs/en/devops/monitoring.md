---
title: "Monitoring"
description: "Compares metrics/logs/traces, APM, SLO monitoring, and alerting operational principles across vendors."
---

> Last reviewed: May 2026

:::note
For multicloud unified observability, see [Unified Observability Architecture](../../devops/observability/).
:::

## Overview

On-premises, tools like Nagios and Zabbix are installed to monitor server health. In the cloud, vendors provide managed monitoring services, letting you collect metrics, logs, and traces and configure alerts without installing agents or operating servers.

### Why Monitoring Matters

- **Incident detection** — Quickly detect server outages, response delays, and spikes in error rates.
- **Root cause analysis** — Trace from "it's slow" symptoms down to "which query in which service is slow."
- **Capacity planning** — Judge scaling timing by looking at traffic trends.
- **Business decisions** — Check conversion rate and error rate changes after deployment to decide whether to roll back.

### The Three Pillars of Observability

- **Metrics** — Numeric data such as CPU, memory, and request counts. Used for dashboards and alerting.
- **Logs** — Text records output by applications/systems. Used for root cause analysis.
- **Traces** — Track the path a request takes through a distributed system. Used to identify bottlenecks.

The key is connecting these three through **correlation**. You need to be able to trace "the error rate went up" (metric) → "in which request?" (trace) → "what exactly was the error?" (log) as a single flow.

### APM (Application Performance Monitoring)

Infrastructure metrics (CPU, memory) alone don't tell you "why it's slow." **APM** measures response time, DB query time, and external API call time at the application code level to find bottlenecks.

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | X-Ray + CloudWatch Application Signals | Service map + SLO monitoring |
| Azure | Application Insights | Automatic instrumentation. Automatic detection of performance anomalies |
| Google Cloud | Cloud Trace + Cloud Profiler | Tracing + code-level profiling |
| OCI | OCI Application Performance Monitoring | Distributed tracing + synthetic monitoring |

### Why Multiple Stakeholders Should Look Together

Monitoring isn't just a tool for the operations team.

- **Developers** — Check error rate/latency changes after deployment directly. Quickly identify code issues.
- **Operations/SRE** — Monitor infrastructure state, capacity, and SLO compliance.
- **Product/Business** — Check conversion rate and user experience metrics.

Sharing the same dashboard lets developers, operations, and business quickly make decisions from the same data when responding to an "it's slow" report. This is why **visibility** matters in DevOps.

### Alerts Must Lead to Action

The purpose of an alert isn't to be received — it should only fire for situations that **require immediate action**. Sending every warning as an alert builds up alert fatigue, causing important alerts to get ignored.

| Level | Criteria | Action |
| --- | --- | --- |
| **Urgent (Page)** | Impacts users. Requires immediate response | Page the on-call engineer. Trigger auto-remediation |
| **Warning** | Could become a problem soon | Check during business hours. Create a ticket |
| **Info** | For reference. No response needed | Display on dashboard only. No alert sent |

:::caution
**Alert Fatigue** — Too many alerts actually cause important ones to be missed. Regularly delete or downgrade to Info level any alert that's received without action.
:::

Principles for sustainable alert operations:

- **Remove alerts with no action.** An alert that's received but never acted on is just noise.
- **Try auto-remediation first.** Alert → automated response via Lambda/runbook → page a human only on failure.
- **Regularly review alerts.** An alert with zero action in the past month is a candidate for deletion.

## SLO Monitoring

SLO monitoring is a core activity for quantitatively tracking service reliability. Each vendor has dedicated tools for defining SLOs, tracking error budgets, and providing burndown charts.

:::note
For SLI/SLO/SLA concepts, error budget operations, and a comparison of vendor SLO tools, see [SLI/SLO and Error Budgets](../../devops/slo/).
:::

## Product Comparison

### Metrics + Dashboards + Alerts

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | CloudWatch Metrics + Alarms | Automatically collects AWS service metrics. Supports custom metrics |
| Azure | Azure Monitor Metrics + Alerts | Integrated with Azure services. Routes alerts via Action Groups |
| Google Cloud | Cloud Monitoring | Automatic collection + custom metrics. PromQL-compatible |
| OCI | OCI Monitoring | Automatically collects OCI service metrics. Alarms + notifications |

### Logs

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | CloudWatch Logs | Log group/stream structure. Query with Logs Insights |
| Azure | Azure Monitor Logs (Log Analytics) | Analyze with KQL (Kusto Query Language) |
| Google Cloud | Cloud Logging | Automatic collection. SQL queries via Log Analytics |
| OCI | OCI Logging | Automatically collects service logs. Analyzed with Logging Analytics |

### Distributed Tracing

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | X-Ray | Traces requests across AWS services. OpenTelemetry-compatible |
| Azure | Application Insights | Automatic instrumentation. Detects performance anomalies |
| Google Cloud | Cloud Trace | Automatic collection. OpenTelemetry-compatible |
| OCI | OCI APM Tracing | Distributed tracing. OpenTelemetry-compatible |

### Unified Dashboards

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | CloudWatch Dashboards | |
| Azure | Azure Dashboards / Workbooks | Interactive reports via Workbooks |
| Google Cloud | Cloud Monitoring Dashboards | |
| OCI | OCI Monitoring Console | Custom dashboards |

## Key Differences

**AWS CloudWatch** — AWS service metrics are collected automatically, and alert → SNS → Lambda integration lets you build an auto-remediation pipeline. However, log query capability (Logs Insights) is more limited than competitors.

**Azure Monitor** — Application Insights provides application performance monitoring (APM) out of the box. KQL enables powerful log analysis, and Workbooks let you build interactive reports.

**Google Cloud Cloud Operations** — The most natural integration with OpenTelemetry. Cloud Logging automatically collects logs from every Google Cloud service, and you can export to BigQuery for long-term analysis.

**OCI Monitoring** — Automatically collects OCI service metrics and provides log analysis and visualization via Logging Analytics. Distributed tracing is also supported via APM Tracing.

### Multicloud Monitoring

Unified monitoring (Grafana, Datadog, OpenTelemetry, etc.) for environments using multiple vendors is covered in [Unified Observability Architecture](../../devops/observability/).

## Common Mistakes

- **Leaving alert fatigue unaddressed** — Configuring too many alerts buries important ones in noise and gets them ignored. Remove alerts that require no action or downgrade them to Info level.
- **Building dashboards but never looking at them** — An elaborately built dashboard that nobody looks at is meaningless. Establish a weekly review routine.
- **Collecting metrics without action** — Collecting metrics with no automated response (alert, scaling, runbook execution) when a threshold is exceeded provides no monitoring value.

## Checklist

- [ ] Are alert thresholds reviewed regularly for appropriateness?
- [ ] Is there a routine for reviewing key dashboards weekly?
- [ ] Are alerts routed to the correct owner/channel?
- [ ] Are alerts with zero action over the past month identified to remove noise?

## Related Documents

- [SLI/SLO and Error Budgets](../../devops/slo/)
- [Disaster Recovery](../../governance/dr/)

## References

### AWS

- [Amazon CloudWatch Documentation](https://docs.aws.amazon.com/ko_kr/cloudwatch/)
- [AWS X-Ray Documentation](https://docs.aws.amazon.com/ko_kr/xray/)

### Azure

- [Azure Monitor Documentation](https://learn.microsoft.com/ko-kr/azure/azure-monitor/)
- [Application Insights Documentation](https://learn.microsoft.com/ko-kr/azure/azure-monitor/app/app-insights-overview)

### Google Cloud

- [Cloud Monitoring Documentation](https://cloud.google.com/monitoring/docs)
- [Cloud Logging Documentation](https://cloud.google.com/logging/docs)
- [Cloud Trace Documentation](https://cloud.google.com/trace/docs)

### OCI

- [OCI Monitoring Documentation](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [OCI Logging Documentation](https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm)
- [OCI Application Performance Monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/index.html)
