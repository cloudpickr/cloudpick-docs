---
title: "オブジェクトストレージ"
description: "オブジェクトストレージサービス、ストレージクラス、レイクハウスアーキテクチャの進化をベンダー別に比較します。"
---

> 文書基準: 2026年7月

## 概要

自社の情報センターでファイルを保存するには、NASやSANを購入し、容量が不足すればディスクを追加する必要があります。容量計画を誤ると、容量不足や過剰投資につながります。

**オブジェクトストレージ**は容量制限なくファイルを保存できるクラウドストレージです。あらかじめ容量を決める必要はなく、保存した分だけ料金を支払います。画像、動画、バックアップ、ログ、データレイクなど、ほぼすべての非構造化データを保存するために使用されます。

:::note
AWS S3に相当するサービス: AzureはBlob Storage、Google CloudはCloud Storage、OCIはObject Storageです。
:::

### なぜオブジェクトストレージなのか

- **非常に安価** — GBあたり月$0.02–0.03程度で、ブロックストレージ(GBあたり$0.08–0.10)やファイルストレージよりもはるかに安価です。アーカイブクラスを使用すればGBあたり$0.001以下まで下げられます。ただし、アーカイブクラスはデータ復元(retrieval)時に別途料金と待機時間が発生します。
- **無制限の容量** — 保存容量に上限がありません。1KBから数PBまで同じ方式で保存します。
- **耐久性**(Durability) — どのベンダーも**99.999999999%(イレブンナイン)** の耐久性を提供します。これは1,000万個のオブジェクトを保存した場合、1万年に1個を失う確率です。複数のAZに自動複製され、データ損失の可能性は事実上ありません。
- **HTTP APIアクセス** — ファイルシステム(フォルダ/パス)ではなくキーバリュー(Key-Value)構造で、REST APIを通じてどこからでもアクセスします。
- **S3互換API** — AWS S3が事実上の標準APIとなり、ほとんどのベンダーとツールがS3互換APIをサポートしています。

## 製品比較

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | S3(Simple Storage Service) | 事実上の業界標準。多様なストレージクラス(Standard、IA、Glacierなど) |
| Azure | Blob Storage | Hot/Cool/Cold/Archiveティア。Data Lake Storage Gen2統合 |
| Google Cloud | Cloud Storage | Standard/Nearline/Coldline/Archive。Multi-region/Dual-region自動複製 |
| OCI | OCI Object Storage | Standard/Infrequent Access/Archiveティア。S3互換APIに対応 |

### ストレージクラス(アクセス頻度別のコスト最適化)

データは時間が経つにつれてアクセス頻度が下がります。どのベンダーもアクセス頻度に応じて保存コストを下げられるストレージクラスを提供しています。保存コストは下がりますが取得コストは上がるため、アクセスパターンに合ったクラスを選択する必要があります。

| アクセス頻度 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| 頻繁にアクセス | S3 Standard | Hot | Standard | Standard |
| たまにアクセス | S3 Standard-IA | Cool | Nearline(30日) | Infrequent Access |
| まれにアクセス | S3 Glacier Instant | Cold | Coldline(90日) | — |
| アーカイブ | S3 Glacier Deep Archive | Archive | Archive(365日) | Archive |
| **自動切り替え** | S3 Intelligent-Tiering | — | Autoclass | Auto-Tiering |

AWS S3 Intelligent-TieringとGoogle Cloud Autoclass、OCI Auto-Tieringは、アクセスパターンを自動的に分析し、最適なクラスへ移動させます。手動でライフサイクルポリシーを設定する必要がなく、運用負担が軽減されます。

:::note
確信が持てない場合は標準クラスから始め、アクセスパターンを分析した後にライフサイクルポリシー(Lifecycle Policy)で自動切り替えしてください。自動切り替えサービスを使用すれば、手動でのポリシー設定は不要です。
:::

:::caution
**アーカイブクラスの注意点:** 保存コストは非常に安価ですが、復元時に別途料金と待機時間(数時間～12時間)が発生します。また、最低保管期間(90～365日)があり、早期削除時には手数料が課されます。頻繁にアクセスする可能性のあるデータはアーカイブに入れないでください。
:::

## 主な違い

**AWS S3** — 2006年にリリースされたパブリッククラウド初期のオブジェクトストレージサービスで、S3 APIが業界互換の標準として広く採用されました。ほとんどのサードパーティツール、他のクラウドベンダー、オンプレミスストレージがS3互換APIをサポートしています。S3 Tables、S3 Metadata、S3 Vectors、**S3 Annotations**など、ストレージ自体に分析・AI機能を内蔵する方向へ進化しています。S3 Annotationsはオブジェクトに最大1GBのクエリ可能なコンテキスト(メタデータ)を直接付与でき、AIエージェントが別途のメタデータシステムなしにデータを発見・理解・処理できます。

**Azure Blob Storage** — Blob StorageとData Lake Storage Gen2が同一のストレージアカウントで統合されます。階層的な名前空間(フォルダ構造)をサポートし、ビッグデータワークロードでのファイル管理が容易です。Microsoft Fabricとの統合により、分析パイプラインの構成が簡単になります。

**Google Cloud Cloud Storage** — Multi-regionとDual-regionオプションにより、別途の複製設定なしに複数のリージョンへ自動複製されます。Autoclassでストレージクラスの自動切り替えをサポートし、BigLakeを通じてBigQueryから直接クエリできます。

**OCI Object Storage** — S3互換APIをサポートし、Auto-Tieringによりアクセスパターンに応じてStandard/Infrequent Access間を自動的に切り替えます。イグレス10TB/月無料のポリシーにより、大量データ転送時のコスト面で大きなメリットがあります。

## 何を選ぶべきか

| こういう場合 | これを選択 |
| --- | --- |
| S3互換APIのエコシステムを最大限活用したいとき | AWS S3 |
| ビッグデータ + 階層的な名前空間(フォルダ構造)が必要なとき | Azure Data Lake Storage Gen2 |
| 別途の設定なしにマルチリージョン自動複製を望むとき | Google Cloud Cloud Storage(Multi-region) |
| ストレージクラスの自動切り替えを望むとき | AWS S3 Intelligent-Tiering、Google Cloud Autoclass、OCI Auto-Tiering |
| 大量のイグレスコストを削減したいとき | OCI Object Storage(10TB/月無料) |
| オブジェクトストレージから直接SQL分析をしたいとき | AWS Athena + S3またはGoogle Cloud BigQuery External Tables |

:::caution
**イグレスコストを必ず確認してください。** オブジェクトストレージにデータを入れるのは無料ですが、取り出す(イグレス)ときに料金が発生します。大量データを外部へ転送するワークロードでは、ベンダー選定における中核的なTCO要素です。
- AWS/Azure/Google Cloud: イグレス$0.08~0.12/GB(リージョンにより異なる)
- OCI: **10TB/月無料**、以降$0.0085/GB

上記の数値は文書作成時点のものであり、変動する可能性があります。最新価格は各ベンダーの公式価格表を確認してください。
:::

## 活用パターン

| ユースケース | 説明 | なぜオブジェクトストレージなのか |
| --- | --- | --- |
| 静的Webホスティング | SPA、静的サイトの配信 | CDN連携、サーバーレス、無限にスケール |
| データレイク | 原本データの保存場所 | スキーマ不要、低コストな大容量、多様なフォーマット |
| ログ/イベントアーカイブ | 監査ログ、イベントストリームの保存 | append-only、ライフサイクルポリシーによる自動アーカイブ |
| ML学習データ | 画像、テキスト、特徴量ストア | 大容量の非構造化データ、並列読み取り |
| バックアップ/DR | DBスナップショット、システムイメージ | 耐久性99.999999999%、クロスリージョン複製 |
| メディア保存/ストリーミング | 動画、画像の原本 | 大容量、CDNオリジン、トランスコーディングパイプラインの入力 |

:::note
データレイク上での分析サービスは[データ分析サービス](../../database/analytics/)を、ETL/ELTパイプラインの構成は[データパイプライン](../../database/data-pipeline/)を、イベントトリガーベースの処理は[サーバーレス](../../compute/serverless/)を参照してください。
:::

## オブジェクトストレージの進化

オブジェクトストレージは単純なファイル保存場所を超え、**データレイクの基本ストレージ**として定着しました。かつてはデータ分析のために別途のデータウェアハウスへデータをコピーする必要がありましたが、今ではオブジェクトストレージにデータをそのまま置いて直接分析する**レイクハウス**(Lakehouse)アーキテクチャが標準になりつつあります。

### レイクハウスパターン

オブジェクトストレージに原本データをそのまま置き、テーブルフォーマット(Iceberg、Delta Lake、Hudi)で構造化することで、別途のデータウェアハウスなしに直接SQLクエリを実行します。

**メダリオンアーキテクチャ(Bronze/Silver/Gold):**

- **Bronze** — 原本のまま(JSON、CSV、Parquetが混在)。ライフサイクルポリシーによる自動アーカイブ
- **Silver** — 精製/変換されたデータ(Parquet、スキーマ適用)
- **Gold** — ビジネス集計/マート(即座に分析可能)

### イベントドリブンパイプライン

オブジェクトのアップロード時にイベントをトリガーし、変換/分析を自動実行します。

| ベンダー | トリガー | 処理 |
| --- | --- | --- |
| AWS | S3 Event Notification | Lambda、Step Functions、EventBridge |
| Azure | Blob Trigger | Functions、Data Factory |
| Google Cloud | Cloud Storage Trigger | Cloud Functions、Dataflow |
| OCI | OCI Events | OCI Functions、Data Flow |

### ベンダー別データプラットフォームサービス

| 機能 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **データレイク** | S3 + Lake Formation | Data Lake Storage Gen2 + Fabric | Cloud Storage + BigLake | OCI Object Storage + Data Lake |
| **テーブル保存(Iceberg)** | S3 Tables | Data Lake Storage + Synapse | BigLake(Icebergネイティブ) | — |
| **メタデータ自動管理** | S3 Metadata | Blob Index Tags | — | — |
| **ベクトル保存/検索** | S3 Vectors(Preview) | AI Search + Blob連携 | BigQuery Vector Index | AI Vector Search(Autonomous DB) |
| **SQL直接クエリ** | S3 Select、Athena | Query Acceleration、Synapse | BigQuery External Tables | OCI Data Flow(Spark) |

:::note
どのベンダーも「ストレージからデータプラットフォームへ」という方向性を追求しています。AWSはS3自体に機能を内蔵する方向であり、AzureはData Lake Storage + Fabric統合、Google CloudはBigLake + BigQuery統合というアプローチを取っています。
:::

## よくある間違い

- **ライフサイクルポリシー未設定** — ライフサイクルポリシーなしで運用すると、古いデータが高コストなストレージクラスに留まり続け、不要なコストが積み上がります。
- **パブリックアクセスの放置** — バケット/コンテナのパブリックアクセスをブロックしないと、機密データがインターネットに露出する可能性があります。
- **バージョニング未有効化** — バージョニングを有効化していないと、誤って上書き/削除したデータを復旧できません。

## チェックリスト

- [ ] ライフサイクルポリシー(Lifecycle Policy)を設定し、古いデータを自動的に切り替え/削除しているか
- [ ] パブリックアクセスのブロック(Block Public Access)を有効化したか
- [ ] バージョニングまたはクロスリージョン複製を有効化したか
- [ ] サーバー側暗号化(SSE)が適用されているか

## 参考資料

### AWS

- [Amazon S3ドキュメント](https://docs.aws.amazon.com/ko_kr/s3/)
- [Amazon S3ストレージクラス](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/storage-class-intro.html)
- [S3 Intelligent-Tiering](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/intelligent-tiering.html)
- [S3 Tablesドキュメント](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/s3-tables.html)
- [S3 Metadataドキュメント](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/s3-metadata.html)
- [AWS Lake Formationドキュメント](https://docs.aws.amazon.com/ko_kr/lake-formation/)
- [Amazon Athenaドキュメント](https://docs.aws.amazon.com/ko_kr/athena/)

### Azure

- [Azure Blob Storageドキュメント](https://learn.microsoft.com/ko-kr/azure/storage/blobs/)
- [Azure Blobアクセス層](https://learn.microsoft.com/ko-kr/azure/storage/blobs/access-tiers-overview)
- [Data Lake Storage Gen2ドキュメント](https://learn.microsoft.com/ko-kr/azure/storage/blobs/data-lake-storage-introduction)
- [Azure Synapse Analyticsドキュメント](https://learn.microsoft.com/ko-kr/azure/synapse-analytics/)
- [Microsoft Fabricドキュメント](https://learn.microsoft.com/ko-kr/fabric/)

### Google Cloud

- [Google Cloud Storageドキュメント](https://cloud.google.com/storage/docs)
- [Cloud Storageクラス](https://cloud.google.com/storage/docs/storage-classes)
- [Autoclassドキュメント](https://cloud.google.com/storage/docs/autoclass)
- [BigLakeドキュメント](https://cloud.google.com/biglake)
- [BigQuery External Tables](https://cloud.google.com/bigquery/docs/external-data-cloud-storage)

### OCI

- [OCI Object Storageドキュメント](https://docs.oracle.com/en-us/iaas/Content/Object/home.htm)
- [OCI Object Storageストレージティア](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/understandingstoragetiers.htm)
