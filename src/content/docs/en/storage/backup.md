---
title: "Backup and Recovery"
description: "Compares integrated backup services, RPO/RTO trade-offs, the 3-2-1 rule, and ransomware preparedness across vendors."
---

> Last reviewed: August 2026

## Overview

On-premises, you install backup software and back up data to a tape library or separate storage. Each backup target (VM, DB, file) requires a different tool, and retention policy management is manual.

In the cloud, an **integrated backup service** lets you manage backups for multiple services (VMs, block storage, files, databases, etc.) under a single policy. You configure schedules, retention periods, and cross-region replication centrally, and perform recovery from the console.

## Product Comparison

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | AWS Backup | Integrates EBS, EFS, RDS, DynamoDB, S3, and more. Supports cross-region/cross-account backup |
| Azure | Azure Backup | Integrates VMs, Disks, Files, SQL, Blob, and more. Managed via Recovery Services Vault |
| Google Cloud | Backup and DR Service | Integrates Compute Engine, GKE, Cloud SQL, and more |
| OCI | OCI Backup | Backs up Block Volume, Boot Volume, and DB systems. Policy-based automatic backup |

### Individual Service Backups

Beyond integrated services, each storage/DB service also has built-in backup capabilities.

| Target | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Block disk** | EBS snapshot | Managed Disk snapshot | Persistent Disk snapshot | Block Volume backup |
| **Entire VM** | AMI | VM Image / Restore Point | Machine Image | Custom Image |
| **Managed DB** | RDS automated backup + snapshot | Azure SQL automated backup | Cloud SQL automated backup | DB System automated backup |
| **Object storage** | S3 versioning + Replication | Blob versioning + Replication | Object Versioning | Object Storage versioning + Replication |

## Key Differences

**AWS Backup** — Supports the widest range of AWS services and allows cross-account backup to isolate backups in a dedicated security account. Backup Vault Lock also provides WORM (Write Once Read Many) functionality to prevent backup deletion.

**Azure Backup** — A single Recovery Services Vault manages VMs, disks, files, and SQL in an integrated way. Combined with Azure Site Recovery, you can operate backup and DR under one system.

**Google Cloud Backup and DR** — Define backup plans in the management console and restore to the original or a different location during recovery.

**OCI Backup** — Supports policy-based automatic backup for Block Volume, Boot Volume, and DB systems, and DR can be configured through cross-region replication.

## Backup Frequency and Cost

Shorter backup intervals reduce data loss but increase storage cost. Choose the appropriate interval per workload.

| Strategy | Frequency | Cost | Suitable Workload |
| --- | --- | --- | --- |
| Daily snapshot | 24 hours | Low | Dev/test environments |
| Hourly snapshot | 1 hour | Medium | General business systems |
| Real-time replication (synchronous) | Continuous | High | Mission-critical, e.g. finance, payments |
| Archive backup | Weekly/monthly | Very low | Long-term retention for compliance |

:::note
Backup frequency is derived from the Recovery Point Objective (RPO). For details on aligning RPO/RTO with business needs, see [Disaster Recovery](../../governance/dr/).
:::

## Backup Types

Choose a backup method based on the trade-off between data volume and restore time.

| Type | Description | Advantages | Disadvantages |
| --- | --- | --- | --- |
| **Full Backup** | Copies all data every time | Complete restore from a single backup | Requires significant storage space and time |
| **Incremental Backup** | Stores only changes since the last backup | Saves storage space/time | Restore requires the full backup plus all incrementals |
| **Differential Backup** | Stores changes since the last full backup | Restore requires only the full backup plus the most recent differential | Uses more space than incremental |
| **Snapshot** | Stores disk state at a point in time incrementally | Fast creation/restore, block-level increments | Some vendors store only within the same region |

Cloud environments mostly use **snapshot-based incremental backup**. The first backup is a full copy, but subsequent backups store only the changed blocks, making it efficient.

:::note
**Snapshot ≠ backup.** If a snapshot exists only in the same account/region, recovery becomes impossible in the event of account compromise or a regional outage. Apply the 3-2-1 rule and keep at least one copy in a separate account or a different region.
:::

## The 3-2-1 Backup Rule

An industry-standard backup principle.

- **3** copies: the original plus 2 backups
- **2** types of media: different storage media or services
- **1** copy offsite: kept in a different region or a different account/subscription

Example of implementing 3-2-1 in the cloud:
- Original: an EBS volume in the production account
- Copy 1: an EBS snapshot in the same region
- Copy 2: a snapshot in a different region or an isolated backup account (cross-region/cross-account replication)

## Ransomware Preparedness

Backups themselves can become a ransomware target. Immutable backups are essential.

| Feature | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Immutable backup** | Backup Vault Lock (WORM) | Recovery Services Vault Immutability | Backup Vault Immutability | Immutable Backup |
| **MFA delete protection** | Backup Vault Lock | Soft Delete + MFA | Bucket Lock | Resource Lock |
| **Cross-account isolation** | Separate Backup Account + Vault replication | Cross-tenant Backup | Cross-Project Backup | Cross-Tenancy Backup |

## Relationship to DR

Backup is the **material** for DR (disaster recovery), not DR **itself**.

### Why Snapshot-Based Incremental Backup Falls Short of DR

| Limitation | Description |
| --- | --- |
| **RPO gap** | Snapshots are periodic (hourly/daily). Changes since the last snapshot are lost |
| **RTO delay** | Restoring a volume from a snapshot, attaching the instance, and starting the service can take tens of minutes to hours |
| **Infrastructure not included** | Snapshots cover disk data only. The entire infrastructure — network, LB, DNS, IAM, etc. — must be restored for the service to come up |
| **Dependency consistency** | Taking snapshots of DB + app + cache at different points in time can cause data inconsistency |
| **Lack of testing** | Even with snapshots, recovery may fail during an actual incident if the recovery procedure is never tested |

### Backup vs. DR Comparison

| Aspect | Backup (Snapshot) | DR (Disaster Recovery) |
| --- | --- | --- |
| Purpose | Prevent data loss | Ensure service continuity |
| Recovery target | Individual files/volumes/DB | Entire service (infrastructure + data + configuration) |
| RPO | Hours to days | Seconds to minutes (real-time replication) |
| RTO | Tens of minutes to hours | Seconds to minutes (automatic failover) |
| Method | Snapshot + cross-region copy | Pilot Light / Warm Standby / Active-Active |
| Cost | Low (storage cost only) | Incurs standby infrastructure cost |

:::note
See [Disaster Recovery](../../governance/dr/) for actual DR strategies and implementation methods.
:::

## Ongoing Practices

- **Perform regular recovery tests** — A backup is meaningless if it cannot be restored. Perform an actual recovery test at least once per quarter.
- **Review retention policies** — Revisit retention periods and storage classes as compliance requirements change or data grows.

## Common Mistakes

- **Keeping snapshots only in the same account/region** — Backups are lost together with the account/region in the event of account compromise or a regional outage. Replicate to a separate account/region per the 3-2-1 rule
- **Creating backups without recovery testing** — Discovering too late, during an actual incident, that the recovery procedure doesn't work or that data is corrupted
- **Not configuring immutable backups** — Ransomware can encrypt or delete backups too, making recovery impossible

## Checklist

- [ ] Does the 3-2-1 rule apply, keeping at least one backup in a separate account or different region?
- [ ] Is an actual recovery test performed at least once per quarter, with results documented?
- [ ] Is Backup Vault Lock / Immutability configured to prevent backup deletion?

## References

### AWS

- [AWS Backup documentation](https://docs.aws.amazon.com/ko_kr/aws-backup/)
- [EBS Snapshots documentation](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/EBSSnapshots.html)

### Azure

- [Azure Backup documentation](https://learn.microsoft.com/ko-kr/azure/backup/)
- [Azure Site Recovery documentation](https://learn.microsoft.com/ko-kr/azure/site-recovery/)

### Google Cloud

- [Backup and DR Service documentation](https://cloud.google.com/backup-disaster-recovery/docs)
- [Persistent Disk snapshots](https://cloud.google.com/compute/docs/disks/create-snapshots)

### OCI

- [OCI Block Volume backups](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/blockvolumebackups.htm)
- [OCI Boot Volume backups](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/bootvolumebackups.htm)
