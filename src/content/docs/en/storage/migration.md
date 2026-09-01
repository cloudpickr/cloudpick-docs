---
title: "Storage Migration"
description: "Compares online/offline transfer methods and tools for moving large-scale data to the cloud across vendors."
---

> Last reviewed: August 2026

## Overview

Migration refers to moving large volumes of data from on-premises or another cloud into the cloud. It might seem as simple as running `aws s3 cp`, but at a scale of several TB to several PB, network bandwidth, cost, and time all become major constraints.

### Migration Types

| Type | Description | Target |
| --- | --- | --- |
| **Online transfer** | Transfers data over the network | A few GB to a few TB, fast network environments |
| **Offline transfer** | Ships data on a physical device | Tens of TB to several PB, limited network environments |
| **Hybrid replication** | Initial offline transfer followed by ongoing online increments | Large data volumes requiring continuous updates |
| **File gateway** | On-premises cache + cloud storage backend | Gradual transition, tolerant of access latency |

## Choosing a Transfer Method

Transfer time is determined by data size and network speed.

| Data size | 1Gbps network | 10Gbps network | Recommended method |
| --- | --- | --- | --- |
| 100GB | ~15 minutes | ~2 minutes | Online (standard transfer) |
| 1TB | ~2.5 hours | ~15 minutes | Online (DataSync, Storage Transfer Service) |
| 10TB | ~25 hours | ~2.5 hours | Online + dedicated connection (Direct Connect, ExpressRoute) |
| 100TB | ~10 days | ~25 hours | Offline (Snowball, Data Box) |
| 1PB | ~100 days | ~10 days | Offline (Snowmobile, Data Box Heavy) |

> The figures above are illustrative and vary by region/time. Check each vendor's official pricing page for current rates.

:::caution
Actual transfer time, including network efficiency, retries, and verification time, is typically 1.5–2x the calculations above.
:::

## Cost Considerations

For storage migration, the choice of transfer method has a major impact on cost.

| Item | Online transfer | Offline transfer |
| --- | --- | --- |
| **Egress cost (on export)** | $0.05–$0.126 per GB | Fixed device fee |
| **Ingestion cost** | Free (mostly) | Free |
| **Storage cost** | Same | Same |
| **Device rental fee** | None | $50–$15,000 (varies by size) |
| **Transfer time** | Depends on network speed | Fixed at 2–3 weeks |
| **Labor cost** | Can be automated | Requires handling device pickup/return |

> The figures above are illustrative and vary by region/time. Check each vendor's official pricing page for current rates.

:::note
**Tip:** For a one-time migration of 10TB or more, offline transfer is generally cheaper and faster. For ongoing synchronization or small-scale migrations, the online method is preferable.
:::

## Online Transfer Services

### Large File Transfer

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | [DataSync](https://aws.amazon.com/datasync/) | Online transfer between NFS/SMB/S3. Supports incremental transfer |
| AWS | [Storage Gateway](https://aws.amazon.com/storagegateway/) | On-premises cache + S3 backend |
| Azure | [AzCopy](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10) | CLI-based high-performance Blob transfer |
| Azure | [Azure File Sync](https://learn.microsoft.com/azure/storage/file-sync/) | Synchronizes an on-premises Windows file server with Azure Files |
| Google Cloud | [Storage Transfer Service](https://cloud.google.com/storage-transfer-service) | Transfers from S3/Azure Blob/HTTP into Cloud Storage |
| Google Cloud | [gsutil / gcloud storage](https://cloud.google.com/storage/docs/gsutil) | CLI-based parallel transfer |
| OCI | [OCI Data Transfer](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm) | Supports both CLI and offline methods |
| OCI | [rclone / OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) | General-purpose sync tool |

### Object Storage-to-Object Storage Replication

Continuously replicates from one object storage to another. Used for multi-cloud environments or DR purposes.

| Vendor | Product | Notes |
| --- | --- | --- |
| AWS | S3 Cross-Region Replication (CRR) | Supports both same-account and cross-account |
| AWS | S3 Replication Time Control (RTC) | SLA of 99.99% replicated within 15 minutes |
| Azure | Blob Object Replication | Asynchronous replication across accounts |
| Google Cloud | Cloud Storage Cross-Region / Multi-Region | Automatic replication when selecting the storage class |
| OCI | Object Storage Replication | Replication across regions/namespaces |

## Offline Transfer Services

Used when network transfer is impractical due to data size, or when the network environment is limited.

| Vendor | Product | Capacity | Feature |
| --- | --- | --- | --- |
| AWS | [Snowcone](https://aws.amazon.com/snowcone/) | ~8 TB | Compact, backpack-portable |
| AWS | [Snowball Edge](https://aws.amazon.com/snowball/) | ~80 TB | Common for large-scale migration |
| AWS | Snowmobile | ~100 PB | Shipping-container scale (note: new orders discontinued after 2024) |
| Azure | [Data Box Disk](https://azure.microsoft.com/products/databox/) | ~35 TB | SSD-based, small capacity |
| Azure | [Data Box](https://azure.microsoft.com/products/databox/) | ~100 TB | Standard device |
| Azure | Data Box Heavy | ~1 PB | Large-capacity device |
| Google Cloud | [Transfer Appliance](https://cloud.google.com/transfer-appliance/docs) | TA40: ~40 TB, TA300: ~300 TB | Standard/large-capacity |
| OCI | [Data Transfer Appliance](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm) | ~150 TB | Transfer via a rented device |
| OCI | Data Transfer Disk | ~32 TB | Customer purchases the disk and ships it |

> The figures above are illustrative and vary by region/time. Check each vendor's official pricing page for current rates.

### Offline Transfer Steps

1. Order the device through the vendor's console/API
2. The vendor ships the device
3. Copy data onto the device on-premises
4. Ship the device back to the vendor
5. The vendor uploads the data from its data center to cloud storage
6. After verification, the data on the device is securely erased

The process typically takes 2–3 weeks and can significantly reduce network egress costs.

## Hybrid Cache/Gateway

An approach that lets on-premises applications use cloud storage without any changes.

| Vendor | Product | Delivery form |
| --- | --- | --- |
| AWS | [Storage Gateway](https://aws.amazon.com/storagegateway/) | File/Volume/Tape Gateway |
| Azure | [Azure File Sync](https://learn.microsoft.com/azure/storage/file-sync/) | File server extension |
| Google Cloud | [Cloud Storage FUSE](https://cloud.google.com/storage/docs/cloud-storage-fuse/overview) | Mounted like a file system |
| OCI | [Storage Gateway](https://docs.oracle.com/en-us/iaas/Content/StorageGateway/home.htm) | NFS v4 interface |

## Verification and Integrity

Integrity verification is essential after large-scale data transfer.

- **Checksum verification** — Compare the MD5/SHA256 hash of each file
- **File count/size comparison** — Confirm metadata matches between source and destination
- **Sampling test** — Download random files to confirm they can actually be opened
- **Permission preservation check** — Verify owner, read/write permissions, and ACLs are preserved

Vendor tools mostly perform automatic verification, but it's safer to also perform manual verification for critical data.

## Common Mistakes

- **Underestimating network transfer time** — Calculating based on theoretical bandwidth, when actual transfers take 1.5–2x as long. Retries, verification, and network efficiency must be factored in
- **Skipping integrity verification after transfer** — Confirming only file counts without checksum comparison, discovering corrupted files too late
- **Not estimating egress cost in advance** — For tens of TB of online transfer, egress cost can exceed the rental fee for an offline device

## Checklist

- [ ] Have you chosen an online/offline transfer method based on data size and network speed?
- [ ] Do you perform checksum (MD5/SHA256)-based integrity verification after the transfer completes?
- [ ] Have you compared egress cost against device rental fee to choose the most cost-effective method?

## References

### AWS

- [AWS Cloud Data Migration](https://aws.amazon.com/cloud-data-migration/)
- [AWS DataSync documentation](https://docs.aws.amazon.com/datasync/)
- [AWS Snow Family documentation](https://docs.aws.amazon.com/snowball/)
- [AWS Storage Gateway documentation](https://docs.aws.amazon.com/storagegateway/)

### Azure

- [Azure Storage migration overview](https://learn.microsoft.com/azure/storage/common/storage-migration-overview)
- [AzCopy documentation](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10)
- [Azure Data Box documentation](https://learn.microsoft.com/azure/databox/)
- [Azure File Sync documentation](https://learn.microsoft.com/azure/storage/file-sync/)

### Google Cloud

- [Storage Transfer Service documentation](https://cloud.google.com/storage-transfer/docs)
- [Transfer Appliance documentation](https://cloud.google.com/transfer-appliance/docs)
- [Cloud Storage FUSE documentation](https://cloud.google.com/storage/docs/cloud-storage-fuse/overview)

### OCI

- [OCI Data Transfer documentation](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm)
- [OCI Storage Gateway documentation](https://docs.oracle.com/en-us/iaas/Content/StorageGateway/home.htm)
- [OCI Object Storage Replication](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/usingreplication.htm)
