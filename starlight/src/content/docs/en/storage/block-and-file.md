---
title: "Block and File Storage"
description: "Compares block/file storage differences, volume types, AZ dependency, and anti-patterns across vendors."
---

> Last reviewed: August 2026

## Overview

Object storage, accessed via HTTP API, is well suited for unstructured data, but other storage types are needed when fast I/O like that of a database is required, or when multiple servers must access the same file simultaneously.

| Type | Access method | On-premises analogy | Typical use |
| --- | --- | --- | --- |
| **Block** | Device mount (disk) | SSD/HDD attached to a server | DB, OS boot disk |
| **File** | File system mount (NFS/SMB) | NAS (shared folder) | Shared data accessed concurrently by multiple servers |
| **Object** | HTTP API (key-value) | — | Images, backups, data lakes |

### Why Block/File Storage Is Needed

Object storage is accessed via HTTP API, so it is cheap and highly scalable, but it cannot be used for workloads that require a file system, such as **OS booting, DB engines, and concurrent writes from multiple servers**.

| Use case | Why block/file | Why object storage cannot replace it |
| --- | --- | --- |
| OS boot disk | Must be mounted as a block device | An OS cannot boot from an HTTP API |
| DB data files | Requires low-latency random I/O and a POSIX file system | DB engines require a block device |
| Container Persistent Volume | Block/file mounted for StatefulSets | Stateful workloads |
| Shared config/media (concurrent multi-server access) | Concurrent R/W via NFS/SMB mount | Object storage doesn't support concurrent writes |
| HPC scratch (large-scale parallel I/O) | Parallel file systems like Lustre | Requires tens of GB/s of throughput |

:::note
On-premises, you connected to SAN/DAS via FC/iSCSI and configured RAID yourself. In the cloud, you create/attach volumes via API, and the vendor guarantees replication and durability. File storage equivalent to NAS (NetApp, Isilon) is also offered as a managed service that scales automatically without capacity planning. Note, however, that cloud block storage is network-attached, so latency can be slightly higher than on-premises DAS.
:::

## Block Storage

Just as you would attach an SSD to an on-premises server, in the cloud you attach a virtual disk to a VM. A volume is normally attached to a single instance and provides the fastest I/O performance.

:::caution
Cloud block storage is attached over the network, so storage I/O and application traffic share the instance's network bandwidth. Each instance type has a dedicated storage bandwidth cap, and exceeding it throttles I/O. For high-performance DB workloads, be sure to check the storage bandwidth specification when choosing an instance type.
:::

### Product Comparison

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | EBS (Elastic Block Store) | The most granular set of volume types |
| Azure | Managed Disks | Premium SSD v2, Ultra Disk |
| Google Cloud | Persistent Disk / Hyperdisk | IOPS/throughput can be changed dynamically after provisioning |
| OCI | OCI Block Volumes | Balanced/Higher Performance/Ultra High Performance. Online resizing |

### Volume Types by Use Case

| Use case | AWS EBS | Azure Managed Disks | Google Cloud |
| --- | --- | --- | --- |
| General purpose (web server, dev) | gp3 | Premium SSD v2 | pd-balanced |
| High-performance DB (low latency required) | io2 Block Express | Ultra Disk | Hyperdisk Extreme |
| Big data, logs (sequential I/O) | st1 | Standard HDD | pd-standard |
| Archive (infrequent access) | sc1 | — | — |

Snapshot-based backup and recovery are covered in [Backup and Recovery](../../storage/backup/).

### Caution: AZ Dependency

A block storage volume is bound to the availability zone (AZ) where it was created and cannot be attached to an instance in a different AZ. This applies to every vendor.

| Vendor | Default behavior | AZ failure mitigation option |
| --- | --- | --- |
| AWS | EBS is bound to a single AZ | Restore to a different AZ from a snapshot |
| Azure | Managed Disk is bound to a single zone | ZRS (Zone-Redundant Storage) synchronously replicates across 3 AZs |
| Google Cloud | Persistent Disk is bound to a single zone | Regional Persistent Disk synchronously replicates across 2 zones |
| OCI | Block Volume is bound to a single AD | Block Volume replication (cross-AD) synchronously replicates to another AD |

If multi-AZ high availability is required, use snapshot-based recovery or the vendor's replication options.

### Operational Notes

- **You can expand but not shrink** — Increasing volume size can be done online, but shrinking is not supported. To shrink, create a new smaller volume and copy the data over.
- **Snapshot = backup + replication** — Snapshots can be copied to a different AZ or region and used for DR.
- **Machine images** — The entire OS + disk can be saved as an image to quickly clone identical servers (AWS AMI, Azure VM Image, Google Cloud Machine Image).
- **Performance changes** — AWS gp3 and Google Cloud Hyperdisk allow dynamic changes to IOPS/throughput without detaching the volume.

## File Storage

Equivalent to on-premises NAS. Multiple servers can access the same file system concurrently, mounted via NFS (Linux) or SMB (Windows). Existing applications that access data via a file path (`/data/file.txt`) can keep working unchanged, enabling migration to the cloud without code changes.

### Product Comparison

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | EFS (Elastic File System) | NFS. Serverless — capacity scales automatically, mountable from Lambda/containers |
| AWS | FSx | Provides Windows (SMB), Lustre (HPC), NetApp, and OpenZFS as managed services |
| Azure | Azure Files | Supports both SMB/NFS. Integrates with on-premises via Azure File Sync |
| Google Cloud | Filestore | NFS-based. Basic/Enterprise tiers |
| OCI | OCI File Storage | NFSv3. Supports snapshots and replication |

### Anti-pattern: Don't Use It as a Deployment Source

:::caution
Carrying over the on-premises pattern of using NAS as a web server's deployment source into the cloud causes costs to spike, since file storage is 5–10x more expensive than object storage. In the cloud, use container images or object storage + CDN, and reserve file storage for shared data that multiple servers read and write concurrently.
:::

## Key Differences

**AWS** — EBS has the most granular set of volume types, and FSx provides four managed file systems: Windows, Lustre, NetApp, and OpenZFS. EFS is serverless, so no capacity management is required.

**Azure** — Azure Files supports both SMB and NFS, making it advantageous for mixed Windows/Linux environments. File Sync lets you synchronize an on-premises file server with the cloud.

**Google Cloud** — Hyperdisk allows block storage performance to be adjusted dynamically even after provisioning. Filestore supports cross-region replication on the Enterprise tier.

**OCI** — Block Volumes support online resizing and performance tier changes, while File Storage is NFSv3-based and offers snapshots and cross-AD replication.

## When to Choose What

| When | Choose this |
| --- | --- |
| You need low-latency block storage for a high-performance DB | AWS EBS io2 Block Express or Azure Ultra Disk |
| You want to change block storage IOPS dynamically during operation | AWS EBS gp3 or Google Cloud Hyperdisk |
| Block disks must survive an AZ failure | Azure ZRS Disk or Google Cloud Regional Persistent Disk |
| Multiple servers need to share files concurrently (NFS) | AWS EFS or Google Cloud Filestore |
| Mixed Windows SMB + Linux NFS environment | Azure Files |
| Synchronizing an on-premises file server with the cloud | Azure File Sync |
| You need a high-performance file system for HPC | AWS FSx for Lustre |

## Integrated Backup Management

Snapshots operate at the individual volume level, but integrated backup services are also available that manage backups for multiple services (VMs, block, files, DB, etc.) under a single policy.

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | AWS Backup | Integrated management of EBS, EFS, RDS, DynamoDB, S3, and more. Cross-region/cross-account backup |
| Azure | Azure Backup | Integrates VMs, Disks, Files, SQL, Blob, and more. Recovery Services Vault |
| Google Cloud | Backup and DR Service | Integrates Compute Engine, GKE, Cloud SQL, and more |
| OCI | OCI Backup | Integrated management of Block Volume, Boot Volume, and DB backups |

:::note
For details on backup frequency design, the 3-2-1 rule, ransomware preparedness, and the relationship to DR, see [Backup and Recovery](../../storage/backup/).
:::

## Common Mistakes

- **Using file storage as a web server's deployment source** — Carrying over the on-premises NAS pattern, incurring 5–10x the cost compared to object storage
- **Over-provisioning volume size** — Since shrinking isn't possible, you can't reduce it later. Allocate only what's needed and use online expansion
- **Overlooking block storage's AZ dependency** — Volumes cannot be attached to instances in a different AZ, delaying recovery during an AZ failure

## Checklist

- [ ] Have you chosen a storage type (block/file/object) that matches the workload's characteristics (DB, shared files, HPC)?
- [ ] Have you configured snapshot-based recovery or regional replication to account for block volumes' AZ dependency?
- [ ] Do you use file storage only when concurrent access from multiple servers is needed, and object storage + CDN for static content?

## References

### AWS

- [Amazon EBS documentation](https://docs.aws.amazon.com/ko_kr/ebs/)
- [EBS volume types](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/ebs-volume-types.html)
- [EBS snapshots](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/EBSSnapshots.html)
- [Amazon EFS documentation](https://docs.aws.amazon.com/ko_kr/efs/)
- [Amazon FSx documentation](https://docs.aws.amazon.com/ko_kr/fsx/)
- [AMI (Amazon Machine Image)](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/AMIs.html)

### Azure

- [Azure Managed Disks documentation](https://learn.microsoft.com/ko-kr/azure/virtual-machines/managed-disks-overview)
- [Disk type comparison](https://learn.microsoft.com/ko-kr/azure/virtual-machines/disks-types)
- [ZRS (Zone-Redundant Storage) disks](https://learn.microsoft.com/ko-kr/azure/virtual-machines/disks-redundancy#zone-redundant-storage-for-managed-disks)
- [Azure Files documentation](https://learn.microsoft.com/ko-kr/azure/storage/files/)
- [Azure File Sync](https://learn.microsoft.com/ko-kr/azure/storage/file-sync/)

### Google Cloud

- [Persistent Disk documentation](https://cloud.google.com/compute/docs/disks)
- [Hyperdisk documentation](https://cloud.google.com/compute/docs/disks/hyperdisks)
- [Regional Persistent Disk](https://cloud.google.com/compute/docs/disks/regional-persistent-disk)
- [Filestore documentation](https://cloud.google.com/filestore/docs)
- [Machine Image](https://cloud.google.com/compute/docs/machine-images)

### OCI

- [OCI Block Volumes documentation](https://docs.oracle.com/en-us/iaas/Content/Block/home.htm)
- [OCI File Storage documentation](https://docs.oracle.com/en-us/iaas/Content/File/home.htm)
