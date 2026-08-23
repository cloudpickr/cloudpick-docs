---
title: "FinOps"
description: "FinOpsのライフサイクル、コスト管理ツール、実務適用の手順、FOCUS仕様をベンダー別に比較します。"
---

> 文書基準: 2026年8月

## FinOpsとは

FinOps（Cloud Financial Operations）は、[FinOps Foundation](https://www.finops.org/)が定義するクラウドコスト管理のフレームワークです。エンジニアリング、財務、ビジネスの各チームが協力し、クラウドコストの可視性を確保し最適化することを目標とします。

FinOpsの3段階のライフサイクル:

| 段階 | 説明 |
| --- | --- |
| **Inform** | コストの可視性確保 — 誰が、何に、いくら使っているかを把握 |
| **Optimize** | コスト最適化 — サイジング、リザーブド、スポットの活用、未使用リソースの削除 |
| **Operate** | 継続的運用 — 予算設定、異常検知、ガバナンスの自動化 |

:::note
FinOpsは単にコストを削減する活動ではありません。必要な場所にはコストをかけつつ、コストとビジネス価値の関係を透明にする運用方式です。
:::

### 単位経済（Unit Economics）

「月間コストはいくらか」よりも「利用者1人当たりのコスト」「トランザクション1件当たりのコスト」を追跡する方が、事業上の意思決定に有用です。

| 指標の例 | 計算例 |
| --- | --- |
| アクティブ利用者当たりコスト | 月間インフラコスト / 月間アクティブ利用者数（MAU） |
| トランザクション当たりコスト | 月間コスト / 月間処理リクエスト数 |
| 売上に対するインフラ比率 | 月間インフラコスト / 月間売上 |

単位経済を追跡すれば、トラフィック増加時にコストが線形かどうかを確認でき、サービスごとの収益性を評価できます。

## 主要CSPのコスト管理ツール比較

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| コスト分析 | [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) | [Microsoft Cost Management](https://azure.microsoft.com/en-us/products/cost-management) | [Cloud Billing Reports](https://cloud.google.com/billing/docs/reports) | [OCI Cost Analysis](https://docs.oracle.com/iaas/Content/Billing/Concepts/costanalysisoverview.htm) |
| 予算/アラート | [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/) | [Azure Budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets) | [Budget Alerts](https://cloud.google.com/billing/docs/how-to/budgets) | [OCI Budgets](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm) |
| 推奨/アドバイザー | [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/) | [Azure Advisor](https://azure.microsoft.com/en-us/products/advisor) | [Recommender](https://cloud.google.com/recommender/docs/overview) | [Cloud Advisor](https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/Concepts/cloudadvisoroverview.htm) |
| コスト配分 | Cost Allocation Tags | Cost Allocation (Tags + Subscriptions) | Labels + Billing Account | Cost Tracking Tags + Compartments |

### AIコストガバナンス

AIワークロード（LLM API呼び出し、GPU学習/推論）は、従来のクラウドコストとは**根本的に異なる課金構造**（トークンベース、モデルごとの価格差、エージェントループによる非決定的な消費）を持ちます。既存のFinOpsのサイジング・リザーブドのレバーがそのまま適用できないため、別途のガバナンスが必要です。

| 項目 | 従来のクラウドコスト | AIコスト |
| --- | --- | --- |
| 課金単位 | 時間、GB、リクエスト数 | トークン（入力/出力）、GPU時間、エージェントセッション |
| 予測可能性 | リソース数 × 単価で推定 | プロンプト長、エージェントループ数に応じて非決定的 |
| 最適化レバー | サイジング、リザーブド、スポット、未使用削除 | モデル階層化、トークン予算、プロンプトキャッシング、サーキットブレーカー |

**実務での対応:**

- **タスク別トークン予算** — エージェント/API呼び出しごとに最大トークン上限を設定
- **モデル階層化** — 単純な分類は軽量モデル（GPT-5.4 mini、Haiku）、複雑な推論は高性能モデル
- **プロンプトキャッシング** — 繰り返されるシステムプロンプトをキャッシュして入力トークンを削減
- **コストタグ** — AIワークロードを別タグ（`ai:true`、`model:claude-fable-5`）で分離追跡

### AWS FinOps Agent [Preview]

2026年6月のFinOps Xで発表された[AWS FinOps Agent](https://siliconangle.com/2026/06/11/aws-launches-finops-agent-bring-ai-cost-governance-cloud-spend-finopsx/)(Feature Preview)は、コストの異常をAIが自動検知し、根本原因を分析して担当チームにSlack/Jiraでルーティングします。

| 機能 | 説明 |
| --- | --- |
| 異常検知 | 日次のコストパターンから異常を自動検知 |
| 根本原因分析 | どのサービス/タグ/リージョンでコストが急増したかを分析 |
| チームルーティング | コストオーナーへSlack/Jira通知を自動送信 |
| ステータス | Feature Preview（2026年6月） |

## 実務適用の手順

FinOpsを始めて導入する際は、ツールを数多く導入するよりも、コストを説明できる最低限の基準を先に作ることが重要です。

| 段階 | やるべきこと | 成果物 |
| --- | --- | --- |
| 1 | アカウント/サブスクリプション/プロジェクト構造の整理 | コスト所有組織のマッピング |
| 2 | タグ/ラベル標準の定義 | `service`、`env`、`owner`、`cost-center`等 |
| 3 | 予算とアラートの設定 | 月次予算、閾値アラート |
| 4 | 大きなコスト項目から最適化 | 未使用リソース、過大サイジング、ストレージクラス |
| 5 | リザーブド/コミット割引の検討 | RI、Savings Plans、CUD等 |

---

## Inform — 可視性の確保

コストを削減する前に、まず**どこにいくら使われているか**を正確に把握する必要があります。

- **タグ/ラベルポリシー** — すべてのリソースにチーム、環境、コストセンターをタグ付けし、コストの帰属を明確にします。
- **コストダッシュボード** — ベンダー別のコスト分析ツール(AWS Cost Explorer、Azure Cost Management、Google Cloud Billing)で日次/週次の傾向を可視化します。
- **異常検知アラート** — 予算超過や急激なコスト増加時に即座に通知を受け取れるよう設定します。
- **FOCUS仕様の活用** — マルチクラウド環境では、FinOps FOCUS標準でベンダー間のコストデータを統合します。

### タグ/ラベルポリシーの設計

FinOpsの出発点は、**誰が、何に、いくら使ったか**を正確に帰属させることです。アカウント/サブスクリプション/プロジェクト単位の分離だけでは不十分な場合（同一アカウントに複数チームのリソースがある場合など）が多く、タグ/ラベルが必須です。

### 標準タグセット

ベンダー中立的に推奨される最小限のタグセットです。

| タグキー | 値の例 | 用途 |
| --- | --- | --- |
| `env` / `environment` | `prod`、`staging`、`dev` | 環境別コスト分析、デプロイポリシー |
| `owner` | `team-payments@company.com` | 責任者の識別、通知ルーティング |
| `cost-center` | `CC-1001` | 会計システム連携、Chargeback |
| `project` / `workload` | `checkout-api`、`ml-pipeline` | サービス単位のコスト分析 |
| `service-tier` | `critical`、`standard`、`low` | SLO/DRポリシーとの連携 |
| `data-classification` | `public`、`internal`、`confidential` | セキュリティ/監査要件 |
| `compliance` | `pci`、`hipaa`、`isms-p` | 規制対象リソースの識別 |
| `managed-by` | `terraform`、`manual` | IaC管理の有無、ドリフト検知 |

組織によっては`business-unit`、`customer`、`cost-allocation`等を追加できます。

### タグポリシーの原則

- **一貫した大文字/小文字と表記** — `env`と`Env`と`environment`は異なるキーとして扱われる。一つに統一する。
- **値の許可リストを制限** — 自由入力は誤字により集計に失敗する。`prod`/`staging`/`dev`のように許可値を固定する。
- **必須タグの強制** — タグのないリソースはコスト帰属が不可能。作成時に強制する。
- **上位階層からの継承** — 組織/OU/フォルダ/コンパートメントレベルのタグが下位リソースに自動適用されると運用負担が軽減する。
- **技術タグとコストタグの区別** — `app=nginx`は技術タグ、`cost-center=CC-1001`はコストタグ。コストレポートのノイズを減らす。

### ベンダー別タグガバナンスツール

| ベンダー | タグ強制/監査 | 備考 |
| --- | --- | --- |
| AWS | [AWS Tag Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html)、[Resource Groups Tagging API](https://docs.aws.amazon.com/resourcegroupstagging/latest/APIReference/Welcome.html)、[Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html) | Organizationレベルでタグポリシーを定義、Config Ruleで違反を検知 |
| Azure | [Azure Policy タグenforcement](https://learn.microsoft.com/azure/azure-resource-manager/management/tag-policies)、[Cost allocation rules](https://learn.microsoft.com/azure/cost-management-billing/costs/allocate-costs) | Management Group単位でタグポリシーを適用、継承ポリシーを提供 |
| Google Cloud | [Resource Tags](https://cloud.google.com/resource-manager/docs/tags/tags-overview)、[Labels](https://cloud.google.com/resource-manager/docs/creating-managing-labels)、[Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/tags-organization-policy) | Resource TagsはIAMとポリシーに、Labelsはコスト分析に使用（用途を分離） |
| OCI | [Tag Namespaces](https://docs.oracle.com/en-us/iaas/Content/Tagging/Tasks/managingtagsandtagnamespaces.htm)、[Tag Defaults](https://docs.oracle.com/en-us/iaas/Content/Tagging/Tasks/managingtagdefaults.htm)、[Cost Tracking Tags](https://docs.oracle.com/en-us/iaas/Content/Tagging/Tasks/usingcosttrackingtags.htm) | Tag Namespaceでキーを管理、Tag DefaultsでCompartmentレベルの自動タグ付け |

### デプロイパイプラインでの強制

タグは人が手動で付けると漏れが発生しやすくなります。ポリシーのコード化によって強制します。

- **IaCモジュールの標準化** — Terraformモジュールに必須タグを入力変数として強制。漏れがあればplan段階で失敗する。
- **ポリシーゲート** — AWS SCP、Azure Policy、Google Cloud Organization Policyでタグのないリソース作成を拒否する。
- **CI/CD検証** — PR段階で`tflint`、`checkov`、`opa`によりタグの有無を確認する。
- **継続的監査** — AWS Config、Azure Resource Graph、Google Cloud Asset Inventoryのクエリで定期的にレポートする。

### 開始チェックリスト

- [ ] 標準タグキーセットを定義（8〜10個以内で開始し、その後拡張）
- [ ] タグ値の許可リストを文書化（例: `env`の値は`prod`/`staging`/`dev`のみ）
- [ ] 組織/OU/フォルダ/コンパートメントレベルの継承ポリシーを適用
- [ ] IaCモジュールに必須タグの入力を強制
- [ ] コスト配分タグ（Cost Allocation Tag）を有効化 — ベンダーの初期設定は無効
- [ ] 既存リソースの漏れたタグを補正する計画（一括更新スクリプト）
- [ ] 月1回のタグ規定準拠レポートを生成
- [ ] Showback/Chargebackレポートのタグベースのフィールドを確認

### ショーバック vs チャージバック（Showback vs Chargeback）

コストを組織内部にどのように配分するかを決めるモデルです。[FinOps Foundation公式フレームワーク](https://www.finops.org/framework/capabilities/allocation/)で定義されています。

| モデル | 説明 | 適した組織 |
| --- | --- | --- |
| **Showback** | 部門/チーム別の使用コストを「見せるだけ」。実際の予算移動なし | FinOps初期導入、コスト意識の浸透段階 |
| **Chargeback** | 部門別の使用コストを実際の予算から差し引く | 成熟した組織、部門別P&Lがある場合 |

### 実装のための前提条件

Showback/Chargebackを行うには、コストを正確に帰属させられる必要があります。

- **タグ/ラベルの標準化** — すべてのリソースに`cost-center`、`project`、`owner`、`env`タグを適用
- **アカウント/サブスクリプション/プロジェクトの分離** — 部門別の分離はタグよりも確実なコスト境界（[アカウントと組織構造](../../about-cloud/accounts-and-organizations/)を参照）
- **共有コスト配分ポリシー** — ネットワーク、セキュリティサービスといった共通コストをどう分けるか定義する

### FOCUS仕様

[FOCUS（FinOps Open Cost and Usage Specification）](https://focus.finops.org/)は、FinOps Foundationが主導するマルチクラウドコストデータの標準化仕様です。ベンダーごとに異なるコストデータ形式を単一のスキーマに統合し、マルチクラウド環境で一貫したコスト分析を可能にします。

**FOCUS v1.2**（[2025年5月29日批准](https://focus.finops.org/focus-specification/)）では、SaaS/PaaS・仮想通貨（トークン等）・複数通貨の正規化サポートが強化されました。AI/MLのコスト分析に特に関連する変更点は次のとおりです。
- トークン等の**仮想通貨（virtual currency）**のライフサイクル・単価比較のユースケース（input/outputトークン課金パターンの追跡）
- `PricingCurrency`系のカラムで、国の通貨とトークン等の課金単位を正規化
- コミット・割引関連のカラムで、GPUリザーブド等のコミット割引を追跡可能

カラムの定義とベンダー別のエクスポート対応範囲は、[FOCUS仕様](https://focus.finops.org/focus-specification/)と各CSPのエクスポートドキュメントを基準に確認してください。

| ベンダー | FOCUS対応状況 |
| --- | --- |
| AWS | [Data Exports — FOCUS 1.2 with AWS columns](https://docs.aws.amazon.com/cur/latest/userguide/table-columns-cur2.html)（CUR 2.0とは別のエクスポート） |
| Azure | [Cost Management FOCUS export](https://learn.microsoft.com/en-us/azure/cost-management-billing/) |
| Google Cloud | [BigQuery コストエクスポート（FOCUS互換）](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables) |
| OCI | [Cost Report（FOCUS対応進行中）](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm) |

---

## Optimize — 最適化

### よく見られるコスト最適化項目

- **コンピューティングのサイジング** — CPU/メモリ使用率の低いVMを縮小または停止します。
- **スケジューリング** — 開発/テスト環境は業務時間外に自動停止します。
- **ストレージのライフサイクル** — 古いログとバックアップは安価なストレージクラスへ移動します。
- **イグレスコスト** — リージョン間、クラウド間のデータ転送経路を点検します。
- **VPCネットワーキングコスト** — NAT Gateway、クロスAZトラフィック等の隠れたコストを点検します。
- **コミット割引** — 安定的に使用するベースラインワークロードにリザーブド/コミットを適用します。

:::caution
コスト最適化は、セキュリティ、可用性、パフォーマンスを損なわない範囲で行う必要があります。特にバックアップ保持期間やDR構成をコストだけを見て縮小すると、障害発生時により大きな損失が生じる可能性があります。
:::

### VPCネットワーキングコストの落とし穴

VPC関連のコストは見えにくいため、予期しない請求が発生しやすい領域です。

| コスト項目 | 説明 | 対応 |
| --- | --- | --- |
| **NAT Gateway** | 時間当たりのコスト＋GB当たりの処理コスト。大量のアウトバウンド時は月数百〜数千ドル | VPC EndpointでAWSサービスにアクセスする際にNATを迂回 |
| **クロスAZトラフィック** | 同一リージョンでもAZ間通信はGB当たりで課金 | 可能な限り同一AZ内の通信を維持、AZ-awareルーティング |
| **VPC Endpoint vs インターネット経由** | S3等へのアクセス時にNAT Gateway経由だと処理コストが発生 | Gateway Endpoint（S3、DynamoDB）は無料 |
| **Transit Gateway** | 時間当たり＋GB当たりのデータ処理コスト | VPCピアリング（データ転送のみ課金）と比較検討 |

**ベンダー別の違い:**

- **AWS** — クロスAZトラフィック $0.01/GB（双方向）。NAT Gateway $0.045/時間 + $0.045/GB
- **Google Cloud** — 同一ゾーン内は無料。同一リージョン内の別ゾーンは$0.01/GB
- **Azure** — 同一VNet内は無料。VNetピアリングはインバウンド/アウトバウンドそれぞれ課金

> 上記の数値は文書作成時点のものであり、変動する可能性があります。最新の価格は各ベンダーの公式価格表を確認してください。

関連: [VPCとサブネット](../../networking/vpc-subnet/)

### コミット割引戦略

各ベンダーは1年または3年のコミットにより最大70〜72%の割引を提供します。ただし、コミットした分を使い切れない場合はコストの浪費になります。

### コミット商品のタイプ

| タイプ | 特徴 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- | --- |
| **インスタンスリザーブド** | 特定のインスタンスタイプを固定 | Reserved Instances | Reserved VM Instances | — | — |
| **使用金額コミット（柔軟）** | 時間当たりの支出金額をコミット、インスタンスタイプの変更可能 | Savings Plans | Savings Plans | CUD (Flexible) | Universal Credits |
| **自動割引** | コミットなしで使用量に応じて自動割引 | — | — | SUD (Sustained Use Discount) | — |
| **スポット/Preemptible** | 中断される可能性がある代わりに60〜90%割引 | Spot Instances | Spot VMs | Spot VMs / Preemptible | Preemptible Instances |

### 適用戦略

- **70/30原則** — 安定したベースラインワークロードの70%はコミット、30%はオンデマンドで柔軟性を確保
- **段階的コミット** — 最初から3年コミットではなく1年から始めて使用パターンを検証
- **スポットの活用** — 中断に強いワークロード（バッチ、CI、開発環境）はスポットへ移行
- **定期的な再評価** — 四半期ごとにコミット活用率を確認

:::note
**コミットは確定使用量に対する財務的な選択です。** 使用量が確実なワークロードにのみ適用してください。使用量より大きくコミットすると割引は得られますが柔軟性を失います。
:::

## Operate — 運用

### コスト異常検知

人が常時監視しなくても、機械学習で異常なコスト増加を自動検知する機能です。

| ベンダー | サービス |
| --- | --- |
| AWS | [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html) |
| Azure | [Microsoft Cost Management — Anomaly Detection](https://learn.microsoft.com/azure/cost-management-billing/understand/analyze-unexpected-charges) |
| Google Cloud | [Recommender / Cost Anomaly Detection](https://cloud.google.com/billing/docs/how-to/manage-anomalies) |
| OCI | [OCI Monitoring アラームベースの構成](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm) |

### 検知時に確認すべきこと

- 意図されたトラフィック増加か（マーケティング、イベント）
- 誤って残されたリソース（テスト用の大型インスタンス、未使用のNAT Gateway）
- オートスケーリングの異常（イベント後も縮小されない）
- セキュリティインシデントによる悪意ある使用（クリプトマイニング、外部攻撃）

## よくある間違い

- **タグなしでリソースを作成する** — タグがなければコストをチーム/サービス/環境に帰属させることができず、誰がいくら使っているか把握できません。
- **予算アラート未設定** — 予算アラートなしで運用すると、異常なコスト増加を数週間後に請求書で初めて発見することになります。
- **コミットの過剰購入** — 使用パターンを十分に分析せず大きなコミットを購入すると、未使用分が浪費され柔軟性を失います。

## チェックリスト

- [ ] すべてのリソースにタグポリシー(env、owner、cost-center)を適用しているか
- [ ] 予算アラート(閾値50%、80%、100%)を設定したか
- [ ] 月次コストレビューを定期的に実施しているか
- [ ] 未使用リソース(停止中のVM、未接続ディスク、空のロードバランサー)を整理しているか

## 参考資料

### フレームワーク

- [FinOps Foundation](https://www.finops.org/)
- [FOCUS仕様](https://focus.finops.org/)

### AWS

- [AWS Cost Management ドキュメント](https://docs.aws.amazon.com/cost-management/)

### Azure

- [Microsoft Cost Management ドキュメント](https://learn.microsoft.com/en-us/azure/cost-management-billing/)

### Google Cloud

- [Cloud Billing ドキュメント](https://cloud.google.com/billing/docs)

### OCI

- [OCI Billing ドキュメント](https://docs.oracle.com/en-us/iaas/Content/Billing/home.htm)
