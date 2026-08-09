---
title: "ベンダー比較"
description: "主要ベンダーの特徴、強み、マルチクラウド連携サービスを比較します。"
---

> 文書基準: 2026年5月

## 一目で見る比較

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **運営会社** | Amazon | Microsoft | Google | Oracle |
| **リリース** | 2006年 | 2010年 | 2008年 | 2016年（Gen2） |
| **市場シェア** | 28% | 21% | 14% | 非公開 |
| **サービスポートフォリオ** | 非常に広い | 非常に広い | 広い | コア領域に集中 |
| **リージョン数** | [39](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) | [70+](https://azure.microsoft.com/explore/global-infrastructure/geographies) | [43](https://cloud.google.com/about/locations) | [50+](https://www.oracle.com/cloud/public-cloud-regions/) |
| **韓国リージョン** | ソウル | ソウル、釜山 | ソウル | ソウル、春川 |
| **強み** | 広いサービスポートフォリオ | エンタープライズ統合（M365、AD） | AI/MLとデータ分析 | データベースと価格競争力 |
| **コンソール** | [Console](https://console.aws.amazon.com) | [Portal](https://portal.azure.com) | [Console](https://console.cloud.google.com) | [Console](https://cloud.oracle.com) |

:::note
市場シェアの出典: [Synergy Research Group — Q4 2025](https://www.srgresearch.com/articles/genai-helps-drive-quarterly-cloud-revenues-to-119-billion-as-growth-rate-jumped-yet-again-in-q4)。リージョン数、サービス数などは急速に変化するため、各ベンダーの公式ページで最新状況を確認してください。
:::

## 主要サービスマッピング

特定のベンダーに慣れている読者が、他のベンダーの同等サービスを探す際の参考にしてください。

| 領域 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **仮想マシン** | EC2 | Virtual Machines | Compute Engine | Compute |
| **マネージドK8s** | EKS | AKS | GKE | OKE |
| **サーバーレス関数** | Lambda | Functions | Cloud Functions | OCI Functions |
| **サーバーレスコンテナ** | Fargate | Container Apps | Cloud Run | Container Instances |
| **オブジェクトストレージ** | S3 | Blob Storage | Cloud Storage | Object Storage |
| **ブロックストレージ** | EBS | Managed Disks | Persistent Disk | Block Volume |
| **マネージドRDB** | RDS / Aurora | Azure SQL / Flexible Server | Cloud SQL / AlloyDB | Autonomous DB |
| **NoSQL（ドキュメント）** | DynamoDB | Cosmos DB | Firestore / Bigtable | NoSQL Database |
| **データウェアハウス** | Redshift | Synapse Analytics | BigQuery | Autonomous DW |
| **VPC** | VPC | VNet | VPC（グローバル） | VCN |
| **ロードバランサー（L7）** | ALB | Application Gateway | Cloud Load Balancing | Load Balancer |
| **DNS** | Route 53 | Azure DNS | Cloud DNS | OCI DNS |
| **CDN** | CloudFront | Front Door / CDN | Cloud CDN | — |
| **IAM** | IAM + Identity Center | Entra ID | Cloud IAM | IAM with Identity Domains |
| **シークレット管理** | Secrets Manager | Key Vault | Secret Manager | Vault |
| **脅威検知** | GuardDuty | Defender for Cloud | Security Command Center | Cloud Guard |
| **IaC** | CloudFormation / CDK | Bicep / ARM | Deployment Manager | Resource Manager |
| **CI/CD** | CodePipeline / CodeBuild | Azure DevOps | Cloud Build | DevOps Service |
| **データ移行（大容量）** | Snowball / DataSync | Data Box / Data Factory | Transfer Appliance / Storage Transfer | OCI Data Transfer |
| **DBマイグレーション** | Database Migration Service (DMS) | Azure Database Migration Service | Database Migration Service | OCI Database Migration |
| **メッセージキュー** | SQS | Service Bus | Cloud Tasks / Pub/Sub | OCI Queue |
| **イベントストリーミング** | MSK（Kafka） | Event Hubs | Pub/Sub | Streaming（Kafka互換） |
| **検索** | OpenSearch Service | Azure AI Search | —（マーケットプレイス） | OCI Search with OpenSearch |
| **データパイプライン（ETL）** | Glue / MWAA | Data Factory / Synapse Pipelines | Dataflow / Cloud Composer | OCI Data Integration |
| **モニタリング** | CloudWatch | Azure Monitor | Cloud Monitoring | OCI Monitoring |
| **AI/LLMプラットフォーム** | Amazon Bedrock | Microsoft Foundry | Gemini Enterprise Agent Platform | OCI Enterprise AI |

:::note
サービス名は急速に変更される可能性があります。Google Cloudは自社基準でAWS/Azureサービスをマッピングした[比較文書](https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison)を別途管理しています。
:::

## ベンダー別の特徴

### AWS — 広いサービスポートフォリオ

Amazonのeコマースインフラから出発したAWSは、成熟したサービスポートフォリオを保有しています。新しいサービスカテゴリを早期にリリースするケースが多く、グローバルなコミュニティとパートナーエコシステムが広範です。

- **主な強み:** サービスの多様性、グローバルリージョン数、豊富なコミュニティ/ドキュメント
- **差別化ポイント:** Amazon Bedrock（AI OSへ進化）、Nova 2モデルのリリース、きめ細かいIAM
- **注意点:** サービス数が200以上と多く、初期選定に時間が必要。イグレスコスト構造を事前に確認すること
- **韓国リージョン:** ソウル 4 AZ（2016年〜）

### Azure — エンタープライズ統合の強者

Microsoftのエンタープライズソフトウェアエコシステム（Microsoft 365、Active Directory、Dynamics 365）と緊密に統合されます。既存のMicrosoft環境を利用する企業にとって、導入経路が比較的明確です。

- **主な強み:** Microsoft 365/AD統合、ハイブリッド（Azure Arc、Azure Stack）、エンタープライズ契約（EA）
- **差別化ポイント:** Microsoft Foundry（旧Azure AI Foundry）、ソウル-釜山リージョンペアによる国内DR、GitHub/VS Code統合
- **注意点:** サービスのリブランディングが頻繁なため、最新名称を公式ドキュメントで確認すること。リージョンごとにサービス可用性が異なる場合がある
- **韓国リージョン:** ソウル（Korea Central）3 AZ + 釜山（Korea South）

### Google Cloud — AI/MLとデータ分析

Googleの検索・データ処理インフラから発展したGoogle Cloudは、AI/MLと大規模データ分析で差別化されています。グローバルVPC、SUD（自動割引）など独自の設計思想を持っています。

- **主な強み:** AI/ML（Gemini Enterprise、TPU）、データ分析（BigQuery）、コンテナ（GKE）
- **差別化ポイント:** Gemini Enterprise Agent Platform（旧Vertex AI）、グローバルVPC（リージョン非依存）、Shared Fateセキュリティモデル
- **注意点:** エンタープライズ導入時はサポートプランと韓国語リソースの可用性を事前に確認すること
- **韓国リージョン:** ソウル 3 Zone（2020年〜）

### OCI — データベースと価格競争力

Oracleのデータベース技術力をクラウドに拡張したOCIは、Oracle DBワークロードに強みがあります。イグレスコストポリシーがマルチクラウド構成に有利な場合があり、専用ベアメタルインスタンスを提供します。

- **主な強み:** Autonomous Database、Oracle DB最適化、イグレス無料枠（10TB/月）
- **差別化ポイント:** OCI Enterprise AI（旧OCI Generative AI）、イグレス10TB/月無料、Dedicated Region（顧客DCへのOCI設置）
- **注意点:** Oracle DB以外のワークロードはサービスカタログとサードパーティエコシステムの規模を事前に確認すること
- **韓国リージョン:** ソウル（`ap-seoul-1`）、春川（`ap-chuncheon-1`）

## ベンダー間マルチクラウド連携サービス

主要CSPは競合関係にありながらも、顧客のマルチクラウド需要に対応して、ベンダー間の直接連携サービスをリリースしています。単一ベンダーに全面依存しない顧客が増える中、「競合他社のインフラ上でも自社サービスを使えるように」する戦略が広がっています。

| カテゴリ | 説明 | 詳細 |
| --- | --- | --- |
| **ネットワーク直接接続** | ベンダー間の専用ネットワークによるプライベート接続。インターネットを経由しないため遅延とセキュリティの両面で有利 | [マルチクラウドコネクティビティ](../../networking/multicloud-connectivity/) |
| **他クラウド内へのDB配置** | 競合他社のデータセンター内に自社DBをネイティブ配置。アプリはAWS/Azure/Google Cloudに置き、DBのみOracleを使う構成が可能 | [マネージドRDB — Database@Cloud](../../database/managed-rdb/#database-cloud-db) |
| **マルチクラウド管理プラットフォーム** | 他クラウドのサーバー、Kubernetes、DBを自社コンソールで統合管理。運用ツールを一元化したい需要に対応 | 下記参照 |

### マルチクラウド管理プラットフォーム

他クラウドのリソースを自社の管理ツールで統合管理できるサービスです。

| サービス | ベンダー | 説明 |
| --- | --- | --- |
| **[Azure Arc](https://azure.microsoft.com/products/azure-arc/)** | Azure | AWS/Google Cloud/オンプレミスのサーバー、Kubernetes、DBをAzure Portalで統合管理 |
| **[GKE Enterprise（旧Anthos）](https://cloud.google.com/kubernetes-engine/enterprise/docs)** | Google Cloud | AWS/Azure/オンプレミスのKubernetesをGoogle Cloudで統合管理 |
| **[OCI Multicloud](https://docs.oracle.com/en/solutions/oci-best-practices/deploy-multicloud-oci-oracle-database-services1.html)** | OCI | Azure/AWS/Google Cloudとの連携のための統合ソリューション |

## ベンダーが提供する公式比較資料

### Microsoft Azure

Azureは、AWSおよびGoogle Cloudユーザー向けの移行ガイドを最も体系的に提供しています。

- [AWSエキスパート向けAzure](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/)
  - [AWSとAzureのサービス比較](https://learn.microsoft.com/ko-kr/azure/architecture/aws-professional/services)
- [Google Cloudエキスパート向けAzure](https://learn.microsoft.com/ko-kr/azure/architecture/gcp-professional/)

### Google Cloud

- [AWSおよびAzureサービスをGoogle Cloudと比較](https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison)

### Oracle Cloud

- [OCI Migration Hub（オンプレミスおよび他クラウドからOCIへ）](https://www.oracle.com/cloud/migrate-applications-to-oracle-cloud/)
- [OCI Cloud Adoption Framework](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/home.htm)

### AWS

AWSは他社と異なり直接的なサービス比較ページを提供していませんが、他ベンダーから移行するユーザー向けのガイドを提供しています。

- [AWSへのクラウド移行](https://aws.amazon.com/ko/cloud-migration/)
- [AWSサービス概要（全サービス一覧）](https://aws.amazon.com/ko/products/)

## 性能比較の際の注意点

ベンダー間のネットワーク性能を単純比較して「どのベンダーがより速い」と結論づけるのは困難です。性能は次の要因によって大きく左右されます。

- **リージョンの位置** — ユーザーに近いリージョンを選ぶことが、ベンダー選定より重要です。
- **バックボーンネットワーク** — 各ベンダーのグローバルバックボーン構造は異なります。
- **ワークロードの特性** — 帯域幅 vs レイテンシ vs パケット処理量のどれが重要かによって結果が異なります。
- **測定条件** — 時間帯、ISP、測定ツールによって結果は変動します。

### ベンダー公式ネットワーク性能資料

- [AWS — Network Monitor](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/what-is-network-monitor.html)
- [Azure — ネットワーク往復遅延時間統計](https://learn.microsoft.com/en-us/azure/networking/azure-network-latency)
- [Google Cloud — Performance Dashboard](https://cloud.google.com/network-intelligence-center/docs/performance-dashboard/concepts/overview)

### 参考用測定ツール

以下のツールは参考用であり、特定時点の測定結果がベンダーの全般的な性能を代表するものではありません。

- [GCPing](https://gcping.com) — Google Cloudリージョン別レイテンシ測定
- [Azure Speed Test 2.0](https://azurespeedtest.azurewebsites.net) — Azureリージョン別レイテンシ測定
- [Kentik Cloud Latency Map](https://clm.kentik.com/) — マルチベンダーリージョン間レイテンシ
- [Cloud Ping Test](https://cloudping.me) — マルチベンダー同時比較

## よくある間違い

- **「市場シェアが高いベンダーが最善だ」** — シェアは汎用的な指標にすぎず、自社ワークロードに最適かどうかとは別問題です。サービスの適合性とチームの力量がより重要です。
- **「サービス名が同じなら機能も同じだ」** — ベンダー間の同等サービスであっても、機能範囲、制約、課金方式は異なります。必ず公式ドキュメントで詳細仕様を確認してください。
- **「ベンダー比較表一つで決定できる」** — 比較表はあくまで出発点です。PoC、コストシミュレーション、チームのフィードバックを経て初めて実質的な判断が可能になります。

## チェックリスト

- [ ] コアワークロードに必要なサービスが候補ベンダーの韓国リージョンで提供されているか確認したか？
- [ ] ベンダー別公式比較資料（サービスマッピング）を参考に、同等サービスを識別したか？
- [ ] チームが実際に使用するベンダーのCLI/SDK/ドキュメントを直接体験してみたか？

## 参考資料

### コミュニティおよびリサーチ

- [Synergy Research Group](https://www.srgresearch.com/) — クラウド市場シェアの四半期レポート
- [Gartner Magic Quadrant for Cloud Infrastructure](https://www.gartner.com/reviews/market/cloud-infrastructure-and-platform-services) — クラウドベンダー評価
- [CNCF Cloud Native Survey](https://www.cncf.io/reports/cncf-annual-survey-2024/) — クラウド採用状況統計
- [Public Cloud Services Comparison](https://comparecloud.in) — コミュニティベースのサービス比較
