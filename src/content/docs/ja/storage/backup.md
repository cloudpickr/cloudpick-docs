---
title: "バックアップと復旧"
description: "統合バックアップサービス、RPO/RTOのトレードオフ、3-2-1ルール、ランサムウェア対策をベンダー別に比較します。"
---

> 文書基準: 2026年8月

## 概要

オンプレミスではバックアップソフトウェアをインストールし、テープライブラリや別のストレージにバックアップを実行します。バックアップ対象(VM、DB、ファイル)ごとにツールが異なり、保存ポリシーの管理も手動です。

クラウドでは**統合バックアップサービス**を通じて、複数のサービス(VM、ブロックストレージ、ファイル、データベースなど)のバックアップを1つのポリシーで管理できます。スケジュール、保存期間、クロスリージョン複製を一元的に設定し、復旧もコンソールから実行します。

## 製品比較

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | AWS Backup | EBS、EFS、RDS、DynamoDB、S3などを統合。クロスリージョン/クロスアカウントバックアップに対応 |
| Azure | Azure Backup | VM、Disks、Files、SQL、Blobなどを統合。Recovery Services Vaultで管理 |
| Google Cloud | Backup and DR Service | Compute Engine、GKE、Cloud SQLなどを統合 |
| OCI | OCI Backup | Block Volume、Boot Volume、DBシステムのバックアップ。ポリシーベースの自動バックアップ |

### 個別サービスバックアップ

統合サービス以外にも、各ストレージ/DBサービス自体にバックアップ機能が内蔵されています。

| 対象 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **ブロックディスク** | EBSスナップショット | Managed Diskスナップショット | Persistent Diskスナップショット | Block Volumeバックアップ |
| **VM全体** | AMI | VM Image / Restore Point | Machine Image | Custom Image |
| **マネージドDB** | RDS自動バックアップ + スナップショット | Azure SQL自動バックアップ | Cloud SQL自動バックアップ | DB System自動バックアップ |
| **オブジェクトストレージ** | S3バージョニング + Replication | Blobバージョニング + Replication | Object Versioning | Object Storageバージョニング + Replication |

## 主な違い

**AWS Backup** — 最も多くのAWSサービスをサポートしており、クロスアカウントバックアップによってセキュリティアカウントにバックアップを隔離できます。Backup Vault Lockでバックアップの削除を防ぐWORM(Write Once Read Many)機能も提供します。

**Azure Backup** — 1つのRecovery Services VaultでVM、ディスク、ファイル、SQLを統合管理します。Azure Site Recoveryと連携すれば、バックアップとDRを1つの体系で運用できます。

**Google Cloud Backup and DR** — 管理コンソールでバックアップ計画を定義し、復旧時に元の場所または別の場所へ復元できます。

**OCI Backup** — Block Volume、Boot Volume、DBシステムのポリシーベースの自動バックアップをサポートし、クロスリージョン複製でDRを構成できます。

## バックアップ周期とコスト

バックアップは周期が短いほどデータ損失は少なくなりますが、保存コストが増加します。ワークロードごとに適切な周期を選択する必要があります。

| 戦略 | 周期 | コスト | 適したワークロード |
| --- | --- | --- | --- |
| 日次1回スナップショット | 24時間 | 低い | 開発/テスト環境 |
| 時間別スナップショット | 1時間 | 中程度 | 一般業務システム |
| リアルタイム複製(同期) | 連続 | 高い | 金融、決済などミッションクリティカル |
| アーカイブバックアップ | 週/月単位 | 非常に低い | コンプライアンス用長期保管 |

:::note
バックアップ周期は目標復旧時点(RPO)から導出されます。RPO/RTOとビジネスアラインメントについては[災害復旧](../../governance/dr/)で詳しく扱います。
:::

## バックアップの種類

データ量と復元時間のトレードオフに応じてバックアップ方式を選択します。

| 種類 | 説明 | メリット | デメリット |
| --- | --- | --- | --- |
| **Full Backup** | 全データを毎回コピー | 単一バックアップで完全復元が可能 | 保存容量と時間を多く消費 |
| **Incremental Backup** | 最後のバックアップ以降の変更分のみ保存 | 保存容量/時間を節約 | 復元時にFull + すべてのIncrementalが必要 |
| **Differential Backup** | 最後のFull以降の変更分を保存 | 復元時にFull + 最新のDifferential1つのみ必要 | Incrementalより容量を多く使用 |
| **Snapshot** | 特定時点のディスク状態を増分で保存 | 高速な作成/復元、ブロックレベルの増分 | 一部ベンダーは同じリージョンにのみ保存 |

クラウドではほとんどの場合**スナップショットベースの増分バックアップ**を使用します。最初のバックアップは全体コピーですが、以降は変更されたブロックのみを保存するため効率的です。

:::note
**スナップショット ≠ バックアップ。** スナップショットが同じアカウント/リージョンにのみある場合、アカウントのハッキングやリージョン障害時に復旧が不可能になります。3-2-1原則を適用し、最低1つは別のアカウントや別のリージョンに保管してください。
:::

## 3-2-1バックアップルール

業界標準のバックアップ原則です。

- **3**つのコピー: 原本 + 2つのバックアップ
- **2**種類のメディア: 異なる保存媒体またはサービス
- **1**つはオフサイト: 別のリージョンまたは別のアカウント/サブスクリプションに保管

クラウドで3-2-1を実装する例:
- 原本: プロダクションアカウントのEBSボリューム
- コピー1: 同じリージョンのEBSスナップショット
- コピー2: 別のリージョンまたは隔離されたバックアップアカウントのスナップショット(クロスリージョン/クロスアカウント複製)

## ランサムウェア対策

バックアップ自体がランサムウェア攻撃の対象になり得ます。不変(immutable)バックアップが必須です。

| 機能 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **不変バックアップ** | Backup Vault Lock (WORM) | Recovery Services Vault Immutability | Backup Vault Immutability | Immutable Backup |
| **MFA削除保護** | Backup Vault Lock | Soft Delete + MFA | Bucket Lock | Resource Lock |
| **クロスアカウント隔離** | Backup Account分離 + Vault複製 | Cross-tenant Backup | Cross-Project Backup | Cross-Tenancy Backup |

## DRとの関係

バックアップはDR(災害復旧)の**材料**であり、DR**そのもの**ではありません。

### スナップショット増分バックアップがDRとして不十分な理由

| 限界 | 説明 |
| --- | --- |
| **RPOギャップ** | スナップショットは周期的(毎時/毎日)。最後のスナップショット以降の変更分は失われる |
| **RTO遅延** | スナップショットからのボリューム復元 → インスタンス接続 → サービス起動まで数十分～数時間 |
| **インフラ非包含** | スナップショットはディスクデータのみ。ネットワーク、LB、DNS、IAMなどインフラ全体を復旧しないとサービスが起動しない |
| **依存関係の整合性** | DB + アプリ + キャッシュをそれぞれ異なる時点でスナップショットすると、データ不整合が発生する可能性 |
| **テスト不足** | スナップショットがあっても復旧手順をテストしていなければ、実際の障害時に失敗する可能性 |

### バックアップ vs DR比較

| 区分 | バックアップ(スナップショット) | DR(災害復旧) |
| --- | --- | --- |
| 目的 | データ損失防止 | サービス継続性の保証 |
| 復旧対象 | 個別ファイル/ボリューム/DB | サービス全体(インフラ + データ + 設定) |
| RPO | 時間～日単位 | 秒～分単位(リアルタイム複製) |
| RTO | 数十分～数時間 | 秒～分(自動フェイルオーバー) |
| 方式 | スナップショット + クロスリージョンコピー | Pilot Light / Warm Standby / Active-Active |
| コスト | 安価(ストレージコストのみ) | 待機インフラコストが発生 |

:::note
実際のDR戦略と実装方法は[災害復旧](../../governance/dr/)を参照してください。
:::

## 継続的に行うべきこと

- **復旧テストの定期実施** — バックアップがあっても復旧できなければ意味がありません。四半期に1回以上、実際の復旧テストを実施してください。
- **保存ポリシーの見直し** — 規制要件の変更やデータ増加に応じて、保存期間とストレージクラスを再検討します。

## よくある間違い

- **スナップショットを同じアカウント/リージョンにのみ保管** — アカウントのハッキングやリージョン障害時にバックアップまで一緒に失われる。3-2-1ルールに従い、別のアカウント/リージョンへの複製が必要
- **バックアップを作成したまま復旧テストを行わない** — 実際の障害時に復旧手順が機能しない、またはデータが破損していることを後になって発見する
- **不変(Immutable)バックアップを設定しない** — ランサムウェアがバックアップまで暗号化/削除し、復旧が不可能になる

## チェックリスト

- [ ] 3-2-1ルールに従い、最低1つのバックアップを別のアカウントまたは別のリージョンに保管しているか
- [ ] 四半期に1回以上、実際の復旧テストを実施し、結果を文書化しているか
- [ ] Backup Vault Lock / Immutability設定でバックアップの削除を防止しているか

## 参考資料

### AWS

- [AWS Backupドキュメント](https://docs.aws.amazon.com/ko_kr/aws-backup/)
- [EBSスナップショットドキュメント](https://docs.aws.amazon.com/ko_kr/ebs/latest/userguide/EBSSnapshots.html)

### Azure

- [Azure Backupドキュメント](https://learn.microsoft.com/ko-kr/azure/backup/)
- [Azure Site Recoveryドキュメント](https://learn.microsoft.com/ko-kr/azure/site-recovery/)

### Google Cloud

- [Backup and DR Serviceドキュメント](https://cloud.google.com/backup-disaster-recovery/docs)
- [Persistent Diskスナップショット](https://cloud.google.com/compute/docs/disks/create-snapshots)

### OCI

- [OCI Block Volumeバックアップ](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/blockvolumebackups.htm)
- [OCI Boot Volumeバックアップ](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/bootvolumebackups.htm)
