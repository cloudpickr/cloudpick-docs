---
title: "ストレージ移行"
description: "大容量データをクラウドへ移行するオンライン/オフライン転送方法とツールをベンダー別に比較します。"
---

> 文書基準: 2026年5月

## 概要

オンプレミスや他のクラウドにある大容量データをクラウドへ移行する作業です。単純に`aws s3 cp`でアップロードすれば済みそうに思えますが、数TB~数PB規模ではネットワーク帯域幅、コスト、時間のすべてが大きな制約になります。

### 移行の種類

| 種類 | 説明 | 対象 |
| --- | --- | --- |
| **オンライン転送** | ネットワークを通じたデータ転送 | 数GB~数TB、高速なネットワーク環境 |
| **オフライン転送** | 物理デバイスにデータを格納して配送 | 数十TB~数PB、限られたネットワーク環境 |
| **ハイブリッド複製** | 初期オフライン + その後オンライン増分 | 大容量 + 継続的な更新が必要 |
| **ファイルゲートウェイ** | オンプレミスキャッシュ + クラウドストレージ | 段階的な移行、アクセス遅延を許容 |

## 転送方法の選定基準

データサイズとネットワーク速度によって転送時間が決まります。

| データサイズ | 1Gbpsネットワーク | 10Gbpsネットワーク | 推奨方法 |
| --- | --- | --- | --- |
| 100GB | 約15分 | 約2分 | オンライン(一般転送) |
| 1TB | 約2.5時間 | 約15分 | オンライン(DataSync、Storage Transfer Service) |
| 10TB | 約25時間 | 約2.5時間 | オンライン + 専用接続(Direct Connect、ExpressRoute) |
| 100TB | 約10日 | 約25時間 | オフライン(Snowball、Data Box) |
| 1PB | 約100日 | 約10日 | オフライン(Snowmobile、Data Box Heavy) |

> 上記の数値は例であり、リージョン/時期によって異なります。最新価格は各ベンダーの公式価格表を確認してください。

:::caution
実際の転送時間は、ネットワーク効率、再試行、検証時間を含めると上記の計算の1.5~2倍が一般的です。
:::

## コストに関する考慮事項

ストレージ移行では、転送方法の選択がコストに大きな影響を与えます。

| 項目 | オンライン転送 | オフライン転送 |
| --- | --- | --- |
| **イグレスコスト(搬出時)** | GBあたり$0.05~$0.126 | デバイス固定料金 |
| **取り込みコスト** | 無料(ほとんどの場合) | 無料 |
| **保存コスト** | 同一 | 同一 |
| **機器レンタル費** | なし | $50~$15,000(サイズ別) |
| **転送時間** | ネットワーク速度に依存 | 2~3週間固定 |
| **人件費** | 自動化可能 | 機器の受け取り/返送対応が必要 |

> 上記の数値は例であり、リージョン/時期によって異なります。最新価格は各ベンダーの公式価格表を確認してください。

:::note
**ヒント:** 10TB以上の一回限りの移行であれば、オフライン転送が一般的により安価で高速です。継続的な同期や小規模な移行にはオンライン方式が有利です。
:::

## オンライン転送サービス

### 大容量ファイル転送

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | [DataSync](https://aws.amazon.com/datasync/) | NFS/SMB/S3間のオンライン転送。増分転送に対応 |
| AWS | [Storage Gateway](https://aws.amazon.com/storagegateway/) | オンプレミスキャッシュ + S3バックエンド |
| Azure | [AzCopy](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10) | CLIベースの高性能Blob転送 |
| Azure | [Azure File Sync](https://learn.microsoft.com/azure/storage/file-sync/) | オンプレミスのWindowsファイルサーバーとAzure Filesの同期 |
| Google Cloud | [Storage Transfer Service](https://cloud.google.com/storage-transfer-service) | S3/Azure Blob/HTTPからCloud Storageへの転送 |
| Google Cloud | [gsutil / gcloud storage](https://cloud.google.com/storage/docs/gsutil) | CLIベースの並列転送 |
| OCI | [OCI Data Transfer](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm) | CLIとオフライン方式の両方に対応 |
| OCI | [rclone / OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) | 多目的同期ツール |

### オブジェクトストレージ間の複製

あるオブジェクトストレージから別のオブジェクトストレージへ継続的に複製します。マルチクラウド環境やDR目的で使用します。

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | S3 Cross-Region Replication (CRR) | 同一アカウント/異なるアカウントの両方に対応 |
| AWS | S3 Replication Time Control (RTC) | 15分以内に99.99%複製するSLA |
| Azure | Blob Object Replication | アカウント間の非同期複製 |
| Google Cloud | Cloud Storage Cross-Region / Multi-Region | ストレージクラス選択時に自動複製 |
| OCI | Object Storage Replication | リージョン間/ネームスペース間の複製 |

## オフライン転送サービス

ネットワークでの転送が非現実的なほどデータが大きい場合や、ネットワーク環境が限られている場合に使用します。

| ベンダー | 製品 | 容量 | 特徴 |
| --- | --- | --- | --- |
| AWS | [Snowcone](https://aws.amazon.com/snowcone/) | ~8 TB | 小型、バックパックで持ち運び可能 |
| AWS | [Snowball Edge](https://aws.amazon.com/snowball/) | ~80 TB | 一般的な大容量移行 |
| AWS | Snowmobile | ~100 PB | コンテナトラック規模(ただし2024年以降新規注文終了) |
| Azure | [Data Box Disk](https://azure.microsoft.com/products/databox/) | ~35 TB | SSDベースの小容量 |
| Azure | [Data Box](https://azure.microsoft.com/products/databox/) | ~100 TB | 標準機器 |
| Azure | Data Box Heavy | ~1 PB | 大容量機器 |
| Google Cloud | [Transfer Appliance](https://cloud.google.com/transfer-appliance/docs) | TA40: 約40 TB、TA300: 約300 TB | 一般/大容量 |
| OCI | [Data Transfer Appliance](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm) | ~150 TB | レンタル機器での転送 |
| OCI | Data Transfer Disk | ~32 TB | 顧客がディスクを購入して発送 |

> 上記の数値は例であり、リージョン/時期によって異なります。最新価格は各ベンダーの公式価格表を確認してください。

### オフライン転送の手順

1. ベンダーのコンソール/APIで機器を注文
2. ベンダーが機器を配送
3. オンプレミスでデータを機器にコピー
4. 機器をベンダーへ返送
5. ベンダーがデータセンターからクラウドストレージへアップロード
6. 検証後、機器のデータを安全に削除

転送期間は一般的に2~3週間程度かかり、ネットワークのイグレスコストを大幅に削減できます。

## ハイブリッドキャッシュ/ゲートウェイ

オンプレミスのアプリケーションを変更せずにクラウドストレージを使用できるようにする方式です。

| ベンダー | 製品 | 提供形態 |
| --- | --- | --- |
| AWS | [Storage Gateway](https://aws.amazon.com/storagegateway/) | File/Volume/Tape Gateway |
| Azure | [Azure File Sync](https://learn.microsoft.com/azure/storage/file-sync/) | ファイルサーバーの拡張 |
| Google Cloud | [Cloud Storage FUSE](https://cloud.google.com/storage/docs/cloud-storage-fuse/overview) | ファイルシステムのようにマウント |
| OCI | [Storage Gateway](https://docs.oracle.com/en-us/iaas/Content/StorageGateway/home.htm) | NFS v4インターフェース |

## 検証と整合性

大容量データ転送後には整合性検証が必須です。

- **チェックサム検証** — 各ファイルのMD5/SHA256ハッシュを比較
- **ファイル数/サイズの比較** — 原本と対象のメタデータの一致を確認
- **サンプリングテスト** — ランダムなファイルをダウンロードして実際に閲覧可能か確認
- **権限維持の確認** — 所有者、読み書き権限、ACLの保持状況

ベンダーのツールはほとんどの場合自動検証を行いますが、重要なデータは手動検証も併用するのが安全です。

## よくある間違い

- **ネットワーク転送時間を過小評価** — 理論的な帯域幅で計算するが、実際は1.5~2倍かかる。再試行、検証、ネットワーク効率を考慮する必要がある
- **転送後の整合性検証を省略** — チェックサム比較なしにファイル数のみ確認し、破損したファイルを後になって発見する
- **イグレスコストを事前に算定しない** — 数十TBのオンライン転送では、イグレスコストがオフライン機器のレンタル費より高くなる場合がある

## チェックリスト

- [ ] データサイズとネットワーク速度に基づいてオンライン/オフライン転送方法を選択したか
- [ ] 転送完了後にチェックサム(MD5/SHA256)ベースの整合性検証を実施しているか
- [ ] イグレスコストと機器レンタル費を比較し、コスト最適な方法を選択したか

## 参考資料

### AWS

- [AWS Cloud Data Migration](https://aws.amazon.com/cloud-data-migration/)
- [AWS DataSyncドキュメント](https://docs.aws.amazon.com/datasync/)
- [AWS Snow Familyドキュメント](https://docs.aws.amazon.com/snowball/)
- [AWS Storage Gatewayドキュメント](https://docs.aws.amazon.com/storagegateway/)

### Azure

- [Azure Storage migration overview](https://learn.microsoft.com/azure/storage/common/storage-migration-overview)
- [AzCopyドキュメント](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10)
- [Azure Data Boxドキュメント](https://learn.microsoft.com/azure/databox/)
- [Azure File Syncドキュメント](https://learn.microsoft.com/azure/storage/file-sync/)

### Google Cloud

- [Storage Transfer Serviceドキュメント](https://cloud.google.com/storage-transfer-service/docs)
- [Transfer Applianceドキュメント](https://cloud.google.com/transfer-appliance/docs)
- [Cloud Storage FUSEドキュメント](https://cloud.google.com/storage/docs/cloud-storage-fuse/overview)

### OCI

- [OCI Data Transferドキュメント](https://docs.oracle.com/en-us/iaas/Content/DataTransfer/home.htm)
- [OCI Storage Gatewayドキュメント](https://docs.oracle.com/en-us/iaas/Content/StorageGateway/home.htm)
- [OCI Object Storage Replication](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/usingreplication.htm)
