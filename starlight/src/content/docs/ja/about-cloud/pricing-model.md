---
title: "コスト構造を理解する"
description: "オンデマンド、予約、スポット課金モデルと、イグレスなどの隠れたコスト項目をベンダー別に比較します。"
---

> 文書基準: 2026年5月

## オンプレミス vs クラウドのコスト構造

自社データセンターを運用するには、サーバーを購入する前からコストが発生します。サーバー購入費、フロアスペース（ラックスペース）の賃料、電力・冷却コスト、ネットワーク機器、そしてこれらすべてを管理する人件費まで — サービスを開始する前から数億ウォン規模の初期投資が必要です。これを**資本支出** (CAPEX, Capital Expenditure)と呼びます。家を買うのに似ています — 大金を先に払い、その後も維持費を負担し続けます。

クラウドはこの構造を**OPEX** (Operational Expenditure、運用支出)へと転換します。初期投資なしに、使った分だけコストを支払います。家賃で暮らすのに似ています — 必要なときに入居し、不要になれば退去すればよいのです。

| 項目 | オンプレミス（CAPEX） | クラウド（OPEX） |
| --- | --- | --- |
| **初期投資** | サーバー、ネットワーク機器の購入（数億ウォン） | なし |
| **課金方式** | 購入後の減価償却（3~5年） | 使用量ベースの従量課金 |
| **拡張** | 追加機器の購入（数週間~数か月） | 即座に拡張可能 |
| **縮小** | 機器の処分が困難 | 即座に縮小、コスト削減 |
| **保守** | 自社人員が必要 | ベンダーが管理 |

ただし、クラウドが常に安いわけではありません。24時間365日一定の負荷で運用されるワークロードは、オンプレミスの方が経済的な場合があります。クラウドのコストメリットは**弾力的な使用パターン**において最大化されます。

## 中核課金モデル

| モデル | 割引率 | コミットメント | 中断リスク | 適したワークロード |
| --- | --- | --- | --- | --- |
| **オンデマンド** | なし（基準価格） | — | なし | 開発/テスト、トラフィック予測が難しいサービス |
| **予約/コミットメント** | 30~72% | 1年または3年 | なし（契約保証） | 安定したプロダクション、24/7運用 |
| **スポット/プリエンプティブル** | 60~90% | — | **あり**（ベンダーが回収可能） | バッチ、CI/CD、データ分析 |
| **無料枠** | 100%（無料範囲内） | — | 無料範囲超過時に課金または中断 | 学習、PoC、小規模実験 |

### オンデマンド (On-Demand / Pay-As-You-Go)

最も基本的な課金方式です。コミットメントなしで使った分だけ支払います。自由に開始・中断できるため、開発/テスト環境やトラフィック予測が難しいワークロードに適しています。

### 予約/コミットメント割引 (Reserved / Committed)

1年または3年の使用をコミットすると、オンデマンド比30~72%の割引を受けられます。ただし、コミットメント期間中は使用の有無にかかわらずコストが発生します。安定して運用されるプロダクションワークロードに適しており、使用量が不確実なワークロードにはかえって損になる場合があります。コミットメント戦略の策定と詳細比較は[FinOps](../../governance/finops/)を参照してください。

### スポット/プリエンプティブルインスタンス (Spot / Preemptible)

ベンダーの遊休リソースをオンデマンド比60~90%割引された価格で使用できます。ただし、ベンダーがリソースを回収する可能性があるため、いつでも中断される可能性があります。バッチ処理、データ分析、CI/CDビルドなど、中断に強いワークロードに適しています。

中断時の対応:

- **中断シグナル** — ベンダーが回収の2分前（AWS）または30秒前（Google Cloud/Azure）に、メタデータエンドポイントへ通知を送ります。アプリケーションはこのシグナルを検知し、進行中の作業をチェックポイントとして保存し、正常終了する必要があります。
- **状態復旧** — 作業状態を外部ストレージ（S3、Blobなど）に定期的に保存（チェックポイント）し、新しいインスタンスが起動したら最後のチェックポイントから再開します。
- **自動リトライ** — Auto Scaling GroupやManaged Instance Groupが、中断されたインスタンスを自動的に置き換えます。作業キュー（SQSなど）と組み合わせることで、失敗した作業が別のインスタンスで自動的に再処理されます。

### 無料枠 (Free Tier)

各ベンダーはいずれも新規ユーザー向けの無料使用範囲を提供しています。ユーザーがサービスを直接体験し、慣れた後に自然と有料へ転換するよう設計された仕組みです。クラウドを初めて始める際、コスト負担なく学習・実験できます。

## ベンダー別比較

| 課金モデル | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **オンデマンド** | On-Demand | Pay-As-You-Go | On-Demand | Pay-As-You-Go |
| **コミットメント割引（インスタンス）** | Reserved Instances | Reserved VM Instances | — | — |
| **コミットメント割引（柔軟）** | Savings Plans | Azure Savings Plan | CUD (Committed Use) | Universal Credits |
| **スポット** | Spot Instances | Spot VMs | Spot VMs | Preemptible Instances |
| **自動割引** | — | — | SUD (Sustained Use) | — |
| **イグレス無料** | — | — | 200GB/月 | **10TB/月** |
| **無料枠** | 12か月 + Always Free | 12か月 + Always Free | 90日 $300 + Always Free | Always Free（潤沢） |
| **課金単位** | 秒単位 | 秒単位 | 秒単位 | 秒単位 |

### 中核的な違い

**Google CloudのSUD(Sustained Use Discounts)** — コミットメントなしで、1か月間一定時間以上使用すると自動的に最大30%割引。

**OCIのイグレスポリシー** — 月10TBまでイグレス無料。マルチクラウド環境でデータ移動が頻繁な場合、大きなコスト差を生みます。

**OCI Universal Credits** — すべてのOCIサービスに使用できる柔軟なコミットメントモデル。特定のサービスに縛られません。

## 隠れたコストへの注意事項

クラウドコストで最も見落とされがちな項目です。オンプレミスでは発生しなかったコストであるため、特に注意が必要です。

### データ転送(Egress)コスト

クラウドへデータをアップロードすること(Ingress)は無料ですが、クラウドから外部へデータを送出すること(Egress)は有料です。大容量データを頻繁に外部へ転送するワークロードでは、このコストが相当な額になる場合があります。

| ベンダー | 無料範囲 | 以降の単価 | 他クラウドへの移行時 |
| --- | --- | --- | --- |
| AWS | 月100GB | $0.09~0.12/GB（リージョンにより異なる） | 無料（申請が必要） |
| Azure | 月100GB | $0.08~0.12/GB | 無料（申請が必要） |
| Google Cloud | 月200GB | $0.08~0.12/GB | 無料（申請が必要） |
| OCI | **月10TB** | $0.0085/GB | 該当なし（デフォルトの無料範囲で十分） |

:::note
AWS、Azure、Google Cloudはいずれも、他のクラウドやオンプレミスへ完全に移行する場合にイグレスコストを免除するポリシーを提供しています。ただし、事前申請が必要であり、日常的なデータ転送には適用されません。
:::

### マルチクラウド間のデータ移動 — コストとレイテンシ

マルチクラウドを検討する際に最も大きな現実的な障壁は、**クラウド間のデータ転送コスト**と**物理的距離によるレイテンシ**です。

**データ重力(Data Gravity):** データが蓄積された場所にコンピューティングリソースが集まらざるを得ません。ペタバイト級のデータを別のベンダーへ移動するコストは、数千万円~数億円に達する場合があります。

**クラウド間分散時のレイテンシ:** Web(AWS) - DB(OCI)のように、階層をクラウド間で分けると、往復レイテンシ(RTT)が追加されます。同一リージョン内のAZ間RTTは約1msですが、クラウド間の専用接続は5~20msが追加されます。この差は、API呼び出しが多いサービスでは体感性能に大きな影響を与えます。

**マルチクラウド分散時の判断基準:**

| 質問 | はい → | いいえ → |
| --- | --- | --- |
| クラウド間のリアルタイムデータ交換が頻繁か? | 同一ベンダーに置く | 分散可能 |
| イグレスコストが月間予算の10%以上か? | データの配置を再検討 | 現状維持 |
| レイテンシ10ms追加がSLAに影響するか? | 同一ベンダー/リージョンに置く | 分散可能 |

:::caution
マルチクラウドのメリット（ベンダーロックイン回避、最適なサービスの組み合わせ）とコスト/性能の制約を併せて検討してください。データ量が少ない階層（フロントエンド、静的アセット）は分散が容易で、データ量が多い階層（DB、分析）は一箇所に集約するのが一般的です。
:::

### ストレージAPI呼び出しコスト

ストレージにデータを保存するコストの他に、データの読み書きを行うAPI呼び出しにもコストが発生します。小規模では無視できますが、数百万件のAPI呼び出しが発生するワークロードでは無視できない金額になります。

### ログ/モニタリングコスト

CloudWatch(AWS)、Azure Monitor(Azure)、Cloud Logging(Google Cloud)などのモニタリングサービスのログ収集・保存コストも見落としがちです。ログの保存期間と収集範囲を適切に設定しないと、予想外のコストが発生する可能性があります。

## コスト管理ツール

各ベンダーはコストをモニタリング・最適化できるツールを提供しています。

| ベンダー | コストダッシュボード | 料金計算機 |
| --- | --- | --- |
| AWS | [Cost Explorer](https://aws.amazon.com/ko/aws-cost-management/aws-cost-explorer/) | [Pricing Calculator](https://calculator.aws/) |
| Azure | [Cost Management](https://azure.microsoft.com/ko-kr/products/cost-management/) | [料金計算機](https://azure.microsoft.com/ko-kr/pricing/calculator/) |
| Google Cloud | [Cost Management](https://cloud.google.com/cost-management) | [料金計算機](https://cloud.google.com/products/calculator) |
| OCI | [Cost Analysis](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm) | [Cost Estimator](https://www.oracle.com/cloud/costestimator.html) |

## よくある間違い

- **「クラウドは使った分しか請求されない」** — イグレス、API呼び出し、ログ保存など隠れたコスト項目があります。主要なコスト項目を事前に把握しておく必要があります。
- **「コミットメント割引は必ず得だ」** — 使用量が不確実なワークロードにコミットメントをかけると、かえって損になります。安定した使用パターンが確認された後にコミットしてください。
- **「無料枠は完全無料だ」** — 無料範囲を超えると自動的に課金されます。予算アラートを設定し、使用量をモニタリングしてください。

## チェックリスト

- [ ] 予算アラート（Budget Alert）を設定し、予想コスト超過時に通知を受け取れるようにしたか?
- [ ] イグレスコストを含む月間予想コストを、ベンダーの料金計算機でシミュレーションしたか?
- [ ] 開発/テスト環境のリソースを業務時間外に停止するポリシーを策定したか?

## 参考資料

### 標準およびフレームワーク

- [FinOps Foundation — FinOps Framework](https://finops.org/framework) — クラウドコスト管理フレームワーク
- [FinOps Foundation — FOCUS Specification](https://focus.finops.org/) — マルチクラウドコストデータ標準化仕様
- [Flexera State of the Cloud Report](https://info.flexera.com/CM-REPORT-State-of-the-Cloud) — 年次クラウドコスト/採用状況レポート

### AWS

- [AWS料金](https://aws.amazon.com/ko/pricing/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Cost Explorer](https://aws.amazon.com/ko/aws-cost-management/aws-cost-explorer/)
- [AWS無料利用枠](https://aws.amazon.com/ko/free/)

### Azure

- [Azure価格設定](https://azure.microsoft.com/ko-kr/pricing/)
- [Azure料金計算機](https://azure.microsoft.com/ko-kr/pricing/calculator/)
- [Azure Cost Management](https://azure.microsoft.com/ko-kr/products/cost-management/)
- [Azure無料アカウント](https://azure.microsoft.com/ko-kr/free/)

### Google Cloud

- [Google Cloud価格設定](https://cloud.google.com/pricing)
- [Google Cloud料金計算機](https://cloud.google.com/products/calculator)
- [Cost Management](https://cloud.google.com/cost-management)
- [Google Cloud無料プログラム](https://cloud.google.com/free)

### OCI

- [OCI価格設定](https://www.oracle.com/kr/cloud/pricing/)
- [OCI Cost Estimator](https://www.oracle.com/cloud/costestimator.html)
- [OCI Free Tier](https://www.oracle.com/cloud/free/)
