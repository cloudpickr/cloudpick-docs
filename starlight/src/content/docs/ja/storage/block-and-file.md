---
title: "ブロック・ファイルストレージ"
description: "ブロック/ファイルストレージの違い、ボリュームタイプ、AZ依存性、アンチパターンをベンダー別に比較します。"
---

> 文書基準: 2026年5月

## 概要

オブジェクトストレージはHTTP APIでアクセスする非構造化データに適していますが、データベースのように高速なI/Oが必要な場合や、複数のサーバーが同時に同じファイルにアクセスする必要がある場合には、別のストレージが必要です。

| 種類 | アクセス方式 | オンプレミスの類似物 | 代表的な用途 |
| --- | --- | --- | --- |
| **ブロック** | デバイスマウント(ディスク) | サーバーに搭載したSSD/HDD | DB、OSブートディスク |
| **ファイル** | ファイルシステムマウント(NFS/SMB) | NAS(共有フォルダ) | 複数サーバーが同時にアクセスする共有データ |
| **オブジェクト** | HTTP API(キーバリュー) | — | 画像、バックアップ、データレイク |

### なぜブロック/ファイルストレージが必要なのか

オブジェクトストレージはHTTP APIでアクセスするため安価でスケーラビリティに優れていますが、**OSブート、DBエンジン、複数サーバーの同時書き込み**のようにファイルシステムが必要なワークロードには使用できません。

| 用途 | なぜブロック/ファイルなのか | オブジェクトで代替できない理由 |
| --- | --- | --- |
| OSブートディスク | ブロックデバイスとしてのマウントが必須 | OSはHTTP APIから起動できない |
| DBデータファイル | 低遅延ランダムI/O、POSIXファイルシステムが必要 | DBエンジンがブロックデバイスを要求する |
| コンテナのPersistent Volume | StatefulSetにブロック/ファイルをマウント | ステートフルなワークロード |
| 共有設定/メディア(複数サーバーが同時アクセス) | NFS/SMBマウントによる同時R/W | オブジェクトは同時書き込み不可 |
| HPCスクラッチ(大規模並列I/O) | Lustreなどの並列ファイルシステム | 数十GB/秒のスループットが必要 |

:::note
オンプレミスではSAN/DASにFC/iSCSIで接続し、RAIDを自ら構成していました。クラウドではAPIでボリュームを作成/接続し、複製と耐久性はベンダーが保証します。NAS(NetApp、Isilon)に相当するファイルストレージもマネージドで提供され、容量計画なしに自動拡張されます。ただし、クラウドのブロックストレージはネットワーク接続であるため、オンプレミスのDASよりわずかに遅延が高くなる場合があります。
:::

## ブロックストレージ

オンプレミスでサーバーにSSDを搭載するように、クラウドではVMに仮想ディスクを接続します。1つのボリュームは基本的に1つのインスタンスに接続され、最も高速なI/O性能を提供します。

:::caution
クラウドのブロックストレージはネットワークを通じて接続されるため、インスタンスのネットワーク帯域幅をストレージI/Oとアプリトラフィックが共有します。インスタンスタイプごとにストレージ専用帯域幅の上限があり、これを超えるとI/Oがスロットリングされます。高性能なDBワークロードでは、インスタンスタイプ選択時にストレージ帯域幅のスペックを必ず確認してください。
:::

### 製品比較

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | EBS(Elastic Block Store) | ボリュームタイプが最も細分化 |
| Azure | Managed Disks | Premium SSD v2、Ultra Disk |
| Google Cloud | Persistent Disk / Hyperdisk | プロビジョニング後もIOPS/スループットを動的に変更可能 |
| OCI | OCI Block Volumes | Balanced/Higher Performance/Ultra High Performance。オンラインでのサイズ変更 |

### ボリュームタイプ別ユースケース

| 用途 | AWS EBS | Azure Managed Disks | Google Cloud |
| --- | --- | --- | --- |
| 汎用(Webサーバー、開発) | gp3 | Premium SSD v2 | pd-balanced |
| 高性能DB(低遅延必須) | io2 Block Express | Ultra Disk | Hyperdisk Extreme |
| ビッグデータ、ログ(シーケンシャルI/O) | st1 | Standard HDD | pd-standard |
| アーカイブ(まれなアクセス) | sc1 | — | — |

スナップショットによるバックアップと復旧については[バックアップと復旧](../../storage/backup/)で扱います。

### 注意: 可用性ゾーン依存性

ブロックストレージのボリュームは、作成された可用性ゾーン(AZ)に依存します。別のAZのインスタンスには接続できません。これはどのベンダーでも共通です。

| ベンダー | デフォルトの動作 | AZ障害への対応オプション |
| --- | --- | --- |
| AWS | EBSは単一AZに依存 | スナップショットで別のAZに復元 |
| Azure | Managed Diskは単一Zoneに依存 | ZRS(Zone-Redundant Storage)オプションで3つのAZに同期複製 |
| Google Cloud | Persistent Diskは単一Zoneに依存 | Regional Persistent Diskで2つのZoneに同期複製 |
| OCI | Block Volumeは単一ADに依存 | Block Volume複製(Cross-AD)で別のADに同期複製 |

マルチAZの高可用性が必要な場合は、スナップショットベースの復旧またはベンダー別の複製オプションを活用する必要があります。

### 運用時に知っておくべきこと

- **拡張はできるが縮小はできない** — ボリュームサイズを増やすことはオンラインで可能ですが、減らすことはサポートされていません。縮小が必要な場合は、小さいボリュームを新規作成してデータをコピーする必要があります。
- **スナップショット = バックアップ + 複製** — スナップショットを別のAZやリージョンにコピーして、DR用途に活用できます。
- **マシンイメージ** — OS + ディスク全体をイメージとして保存し、同一のサーバーを素早く複製できます(AWS AMI、Azure VM Image、Google Cloud Machine Image)。
- **性能変更** — AWS gp3とGoogle Cloud Hyperdiskは、ボリュームを切り離すことなくIOPS/スループットを動的に変更できます。

## ファイルストレージ

オンプレミスのNASに相当します。複数のサーバーが同時に同じファイルシステムにアクセスでき、NFS(Linux)またはSMB(Windows)プロトコルでマウントします。既存のアプリケーションがファイルパス(`/data/file.txt`)でアクセスする方式をそのまま使用できるため、コード変更なしにクラウドへ移行できます。

### 製品比較

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | EFS(Elastic File System) | NFS。サーバーレス — 容量自動拡張、Lambda/コンテナからもマウント可能 |
| AWS | FSx | Windows(SMB)、Lustre(HPC)、NetApp、OpenZFSをマネージドで提供 |
| Azure | Azure Files | SMB/NFSの両方に対応。Azure File Syncでオンプレミス連携 |
| Google Cloud | Filestore | NFSベース。Basic/Enterpriseティア |
| OCI | OCI File Storage | NFSv3。スナップショット、複製に対応 |

### アンチパターン: デプロイの原本として使用しない

:::caution
オンプレミスでNASをWebサーバーのデプロイ原本として使うパターンをそのままクラウドに持ち込むと、ファイルストレージはオブジェクトストレージより5~10倍高価なため、コストが急増します。クラウドではコンテナイメージやオブジェクトストレージ + CDNを使用し、ファイルストレージは複数サーバーが同時に読み書きする共有データにのみ使用してください。
:::

## 主な違い

**AWS** — EBSのボリュームタイプが最も細分化されており、FSxでWindows/Lustre/NetApp/OpenZFSの4種類のファイルシステムをマネージドで提供します。EFSはサーバーレスで容量管理が不要です。

**Azure** — Azure FilesがSMBとNFSの両方をサポートし、Windows/Linux混在環境に有利です。File Syncでオンプレミスのファイルサーバーをクラウドと同期できます。

**Google Cloud** — Hyperdiskによりブロックストレージの性能をプロビジョニング後も動的に調整できます。FilestoreはEnterpriseティアでリージョン間複製をサポートします。

**OCI** — Block Volumesはオンラインでのサイズ変更と性能ティア変更をサポートし、File StorageはNFSv3ベースでスナップショットとクロスAD複製を提供します。

## 何を選ぶべきか

| こういう場合 | これを選択 |
| --- | --- |
| 高性能DB用の低遅延ブロックストレージが必要なとき | AWS EBS io2 Block ExpressまたはAzure Ultra Disk |
| ブロックストレージのIOPSを運用中に動的に変更したいとき | AWS EBS gp3またはGoogle Cloud Hyperdisk |
| AZ障害時でもブロックディスクが維持される必要があるとき | Azure ZRS DiskまたはGoogle Cloud Regional Persistent Disk |
| 複数サーバーが同時にファイルを共有する必要があるとき(NFS) | AWS EFSまたはGoogle Cloud Filestore |
| Windows SMB + Linux NFS混在環境のとき | Azure Files |
| オンプレミスのファイルサーバーをクラウドと同期するとき | Azure File Sync |
| HPC用の高性能ファイルシステムが必要なとき | AWS FSx for Lustre |

## 統合バックアップ管理

スナップショットは個別ボリューム単位ですが、複数のサービス(VM、ブロック、ファイル、DBなど)のバックアップを1つのポリシーで管理できる統合バックアップサービスも提供されています。

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | AWS Backup | EBS、EFS、RDS、DynamoDB、S3などを統合管理。クロスリージョン/クロスアカウントバックアップ |
| Azure | Azure Backup | VM、Disks、Files、SQL、Blobなどを統合。Recovery Services Vault |
| Google Cloud | Backup and DR Service | Compute Engine、GKE、Cloud SQLなどを統合 |
| OCI | OCI Backup | Block Volume、Boot Volume、DBバックアップを統合管理 |

:::note
バックアップ周期の設計、3-2-1ルール、ランサムウェア対策、DRとの関係などの詳細は[バックアップと復旧](../../storage/backup/)を参照してください。
:::

## よくある間違い

- **ファイルストレージをWebサーバーのデプロイ原本として使用** — オンプレミスのNASパターンをそのまま持ち込み、オブジェクトストレージ比で5~10倍のコストが発生
- **ボリュームサイズを過度に大きくプロビジョニング** — 縮小ができないため後から減らせない。必要な分だけ割り当て、オンライン拡張を活用する
- **ブロックストレージのAZ依存性を見落とす** — 別のAZのインスタンスにボリュームを接続できず、AZ障害時に復旧が遅延する

## チェックリスト

- [ ] ワークロードの特性(DB、共有ファイル、HPC)に合ったストレージ種類(ブロック/ファイル/オブジェクト)を選択したか
- [ ] ブロックボリュームのAZ依存性を考慮し、スナップショットベースの復旧またはリージョン複製を構成したか
- [ ] ファイルストレージは複数サーバーの同時アクセスが必要な場合にのみ使用し、静的コンテンツはオブジェクトストレージ + CDNを使用しているか

## 参考資料

### AWS

- [Amazon EBSドキュメント](https://docs.aws.amazon.com/ko_kr/ebs/)
- [EBSボリュームタイプ](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/ebs-volume-types.html)
- [EBSスナップショット](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/EBSSnapshots.html)
- [Amazon EFSドキュメント](https://docs.aws.amazon.com/ko_kr/efs/)
- [Amazon FSxドキュメント](https://docs.aws.amazon.com/ko_kr/fsx/)
- [AMI(Amazon Machine Image)](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/AMIs.html)

### Azure

- [Azure Managed Disksドキュメント](https://learn.microsoft.com/ko-kr/azure/virtual-machines/managed-disks-overview)
- [ディスクタイプの比較](https://learn.microsoft.com/ko-kr/azure/virtual-machines/disks-types)
- [ZRS(ゾーン冗長ストレージ)ディスク](https://learn.microsoft.com/ko-kr/azure/virtual-machines/disks-redundancy#zone-redundant-storage-for-managed-disks)
- [Azure Filesドキュメント](https://learn.microsoft.com/ko-kr/azure/storage/files/)
- [Azure File Sync](https://learn.microsoft.com/ko-kr/azure/storage/file-sync/)

### Google Cloud

- [Persistent Diskドキュメント](https://cloud.google.com/compute/docs/disks)
- [Hyperdiskドキュメント](https://cloud.google.com/compute/docs/disks/hyperdisks)
- [Regional Persistent Disk](https://cloud.google.com/compute/docs/disks/regional-persistent-disk)
- [Filestoreドキュメント](https://cloud.google.com/filestore/docs)
- [Machine Image](https://cloud.google.com/compute/docs/machine-images)

### OCI

- [OCI Block Volumesドキュメント](https://docs.oracle.com/en-us/iaas/Content/Block/home.htm)
- [OCI File Storageドキュメント](https://docs.oracle.com/en-us/iaas/Content/File/home.htm)
