---
title: "コードで管理するインフラ（IaC）"
description: "IaCの概念、ベンダーネイティブ/マルチクラウドツールの比較、Terraformの状態管理とモジュール設計を扱います。"
---

> 文書基準: 2026年8月

## 概要

コンソールでクリックしてインフラを作成すれば速いですが、再現ができず、変更履歴も追跡できません。CLIスクリプトで自動化しても、「現在の状態がどうなっているか」をコードが把握していません。担当者が変わると、「このサーバーがなぜこのように設定されているのか」誰も分からない状況になります。

**IaC**（Infrastructure as Code）は、インフラの望ましい状態をコードとして定義し、バージョン管理、コードレビュー、自動デプロイ、変更追跡を可能にします。オンプレミスでサーバー設定を文書で管理していたものを、実行可能なコードに置き換えるということです。

| 方式 | 問題 | IaCで解決 |
| --- | --- | --- |
| コンソールクリック | 再現不可、履歴なし、ミスの追跡が困難 | コード＝ドキュメント＝実行可能な設計図 |
| CLIスクリプト | 現在の状態が不明、冪等性なし | 宣言的: 現在の状態と比較して差分のみ適用 |
| 手動ドキュメント化 | ドキュメントと実態の不一致 | コードがそのまま最新の状態（Single Source of Truth） |

### 命令型 vs 宣言型

- **命令型**（Imperative） — 「これを作れ、あれを削除しろ」と順序どおりに実行。CLIスクリプト。
- **宣言型**（Declarative） — 「最終状態はこれだ」を定義。ツールが現在の状態と比較して差分のみ適用。IaCの主流。

## 製品比較

### ベンダーネイティブIaC

| ベンダー | 製品 | 言語/形式 | 備考 |
| --- | --- | --- | --- |
| AWS | CloudFormation | YAML、JSON | AWS専用。スタック単位で管理 |
| AWS | CDK（Cloud Development Kit） | TypeScript、Python、Java、Go、C# | プログラミング言語でCloudFormationを生成 |
| Azure | Bicep | Bicep DSL | ARM Templateの簡潔な代替 |
| Azure | ARM Templates | JSON | Azureネイティブ。複雑だが完全な機能 |
| Google Cloud | Infrastructure Manager / Config Connector | HCL（Terraform） / K8s YAML | マネージドTerraform（サポート終了したDeployment Managerの後継）およびK8sベース管理 |
| OCI | OCI Resource Manager | HCL（Terraform） | Terraformベース。OCIネイティブの管理型サービス |

### マルチクラウドIaC

| 製品 | 言語 | 備考 |
| --- | --- | --- |
| Terraform / OpenTofu | HCL（HashiCorp Configuration Language） | 最も広く使用。全ベンダー対応。Terraform 1.15 / OpenTofu 1.13（2026年基準） |
| Pulumi | TypeScript、Python、Go、C#、Java | 一般的なプログラミング言語を使用。テストが容易。Pulumi Neo（エージェントインフラ）リリース |
| Crossplane | Kubernetes YAML | K8sクラスタからクラウドリソースを管理 |

### 統合リソース管理API

IaCツールがリソースを管理するには、各サービス別のAPIを呼び出す必要があります。AWSはこれを単一APIとして標準化しました。

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | Cloud Control API | すべてのAWS＋サードパーティリソースをCRUD-L単一APIで管理。TerraformなどIaCツールのバックエンドとして使用 |
| Azure | Azure Resource Manager（ARM）REST API | すべてのAzureリソースを単一の管理レイヤーで制御。AzAPI Terraformプロバイダーで直接呼び出し可能 |
| Google Cloud | Infrastructure Manager API / 個別API | マネージドTerraform実行APIおよびConfig Connector（K8s API） |
| OCI | OCI Resource Manager API | Terraform State管理＋リソースプロビジョニングAPI |

AWS Cloud Control APIは、Terraformが新しいAWSリソースをサポートする際に、個別サービスAPIの代わりにCloud Control APIをバックエンドとして使用できるため、新サービスリリース時のIaCサポートが速くなります。

## 主な違い

**AWS CloudFormation / CDK** — AWSサービスと最も速く連携します。新サービスリリース時、CloudFormationのサポートが最初に登場します。CDKはプログラミング言語の条件文、ループ、抽象化を活用できるため、大規模インフラ管理に有利です。CDK Mixins GA（2026.03）により再利用可能なインフラパターンの合成がより容易になりました。CDKはv2が現役で、Construct LibraryとCLIが別パッケージに分離されました。

**Azure Bicep** — ARM Templateの複雑なJSONを簡潔なDSLに置き換えます。VS Code拡張機能によりオートコンプリートと検証を提供します。

**Terraform** — マルチクラウド環境で事実上の標準です。一つの言語（HCL）でAWS、Azure、Google Cloudをすべて管理できます。状態ファイル（State）の管理が必要です。最新安定版は1.15で、動的モジュールソース（変数でsource/versionを指定）、variable/outputのdeprecation機構、インラインの型変換関数、Windows ARM64サポートが追加されました。

**OpenTofu** — TerraformのMPL-2.0オープンソースフォークで、CNCF Sandboxプロジェクト（2025.04加入）です。最新安定版は1.13で、状態ファイル暗号化、早期変数評価（early variable evaluation）、エフェメラル値（ephemeral values）などTerraformと差別化される機能を独自に開発しています。Terraform HCLとの高い互換性を維持しています。

**OCI Resource Manager** — Terraformベースの管理型IaCサービスで、状態ファイル管理とリソースプロビジョニングをOCIコンソールで統合運用できます。

## Terraformの状態管理

Terraformは現在のインフラ状態を`terraform.tfstate`ファイルに保存します。このファイルは次の役割を果たします。

- **リソースマッピング** — コードのリソースと実際のクラウドリソースIDを紐付け
- **依存関係の追跡** — 変更時にどのリソースを先に/後で処理するかを決定
- **パフォーマンス最適化** — 毎回すべてのリソースを照会せず、キャッシュされた状態を使用

### ローカル vs リモートバックエンド

:::caution
`terraform.tfstate`ファイルには、リソースID、IPなどが含まれており、シークレットが**平文で保存**される可能性があります。ローカルに保存せず、必ず**リモートバックエンドを使用**し、状態ファイルへのアクセス権限を最小化してください。
:::

| 方式 | 長所 | 短所 |
| --- | --- | --- |
| **ローカル状態** | 設定が簡単 | チーム協業不可、ファイル紛失リスク、シークレットがplaintextで保存 |
| **リモートバックエンド** | チーム協業、ロック（locking）、暗号化、バージョン管理 | 初期設定が必要 |

### リモートバックエンドのオプション

| バックエンド | ユースケース |
| --- | --- |
| **S3 + DynamoDB** | AWS環境。S3は状態保存、DynamoDBは同時実行ロック |
| **Azure Storage** | Azure環境。Blob Storage + Leaseベースのロック |
| **GCS** | Google Cloud環境。オブジェクトバージョン管理で履歴追跡 |
| **OCI Resource Manager** | OCI管理型バックエンド。状態と実行をOCIで統合管理 |
| **Terraform Cloud / HCP Terraform** | マルチクラウド。UI、ポリシー、チーム管理を統合 |

## モジュール設計のベストプラクティス

Terraformモジュールは再利用可能なインフラ単位です。

### 階層構造

```text
environments/
├── dev/
│   └── main.tf       # モジュール呼び出し
├── staging/
│   └── main.tf
└── prod/
    └── main.tf

modules/
├── vpc/              # 汎用VPCモジュール
├── eks-cluster/      # EKSクラスタモジュール
└── rds-instance/     # RDSモジュール
```

### ベストプラクティス

- **小さく分割する** — 1つのモジュールが多くのリソースを管理しすぎると再利用が難しくなる
- **入力変数で柔軟性を確保** — ハードコーディングを避け、`variables.tf`で公開する
- **出力（outputs）で依存関係を明示** — 他のモジュールが参照できるように
- **バージョン固定** — Gitタグまたは Terraform Registry のバージョンで固定
- **デフォルト値は慎重に** — プロダクションに不適切なデフォルト値（例: `deletion_protection = false`）は避ける

## ドリフト（Drift）管理

IaCの外部でリソースが手動変更されると、コードと実際の状態が不一致になります（ドリフト）。

| ベンダー | ドリフト検知ツール |
| --- | --- |
| AWS | CloudFormation Drift Detection、Config Rules |
| Azure | Policy、Blueprints Compliance |
| Google Cloud | Config Connector（K8sモデルでドリフトを自動修正） |
| OCI | Resource Manager Drift Detection |
| Terraform | `terraform plan`（現在の状態とコードを比較） |

ドリフトを根本的に防ぐには、**SCP/Azure Policy/Organization Policy**でコンソールでの手動変更を制限し、すべての変更をIaCパイプラインを通じてのみ実行するよう強制します。IaCコード自体のセキュリティ検証（Checkov、tfsecなど）は[DevSecOps](../../devops/devsecops/)を参照してください。

## よくある間違い

- **コンソールを直接修正してdriftを放置** — コンソールでリソースを手動変更すると、コードと実際の状態が不一致（drift）になります。これを放置すると、次の`apply`時に予期しない変更が発生します。
- **状態ファイルのローカル保存** — `terraform.tfstate`をローカルに保存すると、チーム協業が不可能になり、ファイル紛失時にインフラ管理が不可能になります。
- **モジュール化せずコピー＆ペースト** — 同一のコードを複数の環境にコピーすると、変更のたびにすべての箇所を手動で修正する必要があり、不整合が発生します。
- **Azureでユーザーアカウントを使ってIaCを実行** — 2025.10からAzure CLI/PowerShell/ARM APIにMFAが強制されます。CI/CDパイプラインが`az login --identity`（Managed Identity）またはサービスプリンシパル＋Federated Credentialを使用しない場合、中断されます。詳細は[IAM — Azure MFA義務化](../../security/iam/)を参照してください。

## チェックリスト

- [ ] リモート状態ストア（S3+DynamoDB、Azure Storage、GCSなど）を使用しているか
- [ ] drift検知を定期的に実施しているか（`terraform plan`、Config Rulesなど）
- [ ] 共通インフラをモジュールとして分離し再利用しているか
- [ ] `plan`の結果をコードレビューで確認するプロセスがあるか

## 関連ドキュメント

- [CI/CD](../../devops/cicd/)
- [クラウド管理ツール（コンソール、CLI、SDK）](../../about-cloud/console-cli-sdk/)

## 参考資料

### AWS

- [AWS CloudFormationドキュメント](https://docs.aws.amazon.com/ko_kr/cloudformation/)
- [AWS CDKドキュメント](https://docs.aws.amazon.com/ko_kr/cdk/)

### Azure

- [Bicepドキュメント](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/bicep/)
- [ARM Templatesドキュメント](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/templates/)

### Google Cloud

- [Config Connectorドキュメント](https://cloud.google.com/config-connector/docs)

### OCI

- [OCI Resource Managerドキュメント](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/home.htm)
- [OCI Terraform Provider](https://registry.terraform.io/providers/oracle/oci/latest/docs)

### マルチクラウド

- [Terraformドキュメント](https://developer.hashicorp.com/terraform/docs)
- [OpenTofuドキュメント](https://opentofu.org/docs/)
- [Pulumiドキュメント](https://www.pulumi.com/docs/)
