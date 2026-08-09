---
title: "マルチクラウドAI"
description: "マルチクラウドAIのアーキテクチャパターン、RAGパイプライン、GPU可用性をベンダー別に比較します。"
---

> 文書基準: 2026年8月 | 本文書は変化の速い領域であり、四半期ごとのレビュー対象です。

:::note
本文書は発展的な内容です。AIサービスの比較が初めての場合は、[AI入門](../../ai/getting-started/)と[AIプラットフォームとモデルの比較](../../ai/ai-ml/)を先にお読みになることをお勧めします。
:::

## なぜマルチクラウドAIなのか

各クラウドベンダーはAI/ML領域でそれぞれ異なる強みを持っています。単一ベンダーに依存せず、ワークロードの特性に合った最適なサービスを組み合わせることで、コスト、性能、モデルの多様性の面でメリットを得ることができます。

- **AWS** — Amazon Bedrock/SageMaker AI。最大規模のモデルカタログ + 自社AIチップ(Trainium/Inferentia)
- **Azure** — Microsoft Foundry。OpenAI GPTシリーズを主力に + Microsoftエコシステムとの統合
- **Google Cloud** — Gemini Enterprise Agent Platform。自社Geminiマルチモーダル + TPUインフラ
- **OCI** — OCI Enterprise AI。Dedicated AI Cluster(RDMA専用GPU) + イグレス10TB無料

:::note
各ベンダーのAIプラットフォームの詳細比較、モデルカタログ、Fine-tuningオプションは[AIプラットフォームとモデルの比較](../../ai/ai-ml/)を参照してください。
:::

## GPU可用性

AI学習および推論に不可欠なGPUインスタンスを主要CSP別に比較します。

### NVIDIA GPU世代別比較

現在クラウドで提供されている主要なNVIDIAデータセンターGPUのスペック比較です。

| 項目 | H100(Hopper) | H200(Hopper) | B200(Blackwell) | GB200(Blackwell) |
| --- | --- | --- | --- | --- |
| **メモリ** | 80GB HBM3 | 141GB HBM3e | 192GB HBM3e | 384GB(2×192GB) |
| **帯域幅** | 3.35 TB/s | 4.8 TB/s | 8.0 TB/s | 16 TB/s(Superchip) |
| **NVLink** | 900 GB/s | 900 GB/s | 1.8 TB/s | NVL72ドメイン |
| **TDP** | 700W | 700W | 1000W | 1200W(Superchip) |
| **適したワークロード** | 学習/推論汎用 | 大規模推論、長いコンテキスト | 次世代学習 | 兆単位パラメータのフロンティアモデル |
| **メモリ(H100比)** | 1× | ~1.8× | ~2.4× | ~4.8×(2×B200合算) |

:::note
推論スループット(トークン/秒など)はモデル・精度・バッチ・フレームワーク・システム構成によって大きく変わります。「H100比n倍」のようなベンチマーク倍率はベンダー発表資料の特定条件に紐づいているため、導入前に[NVIDIAデータシート](https://www.nvidia.com/en-us/data-center/)と各CSPのインスタンスドキュメントを確認してください。
:::

**選択ガイド:**

- **H100/H200** — リージョン可用性が比較的広い。中規模学習、Fine-tuning、一般的な推論に適する。H200はH100と同一のアーキテクチャ系統で、メモリ・帯域幅が大きく長いコンテキストの推論に有利
- **B200** — 2026年の主力世代候補。H100比でメモリ・帯域幅が大きく、ネイティブFP4などにより量子化推論の効率が高い傾向。実際のスループットはワークロードごとに測定
- **GB200 NVL72** — Grace CPU + B200 GPUをSuperchipとして結合。多数のGPUを単一のNVLinkドメインにまとめて超大型モデルの学習に使用。利用可能なリージョン・コミットメントの確保が限定的な場合がある

:::note
大半のエンタープライズAIワークロード(RAG推論、Fine-tuning、中規模学習)は**H100/H200で十分**です。B200は大規模学習や高い推論スループットが必要な場合に、GB200はフロンティアモデルの学習にのみ必要です。GPU世代が高いほどリージョン可用性が限定的でコミットメントの確保が難しくなるため、ワークロードに見合った最小スペックを選択してください。
:::

### ベンダー別GPUインスタンス

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **B200 (Blackwell)** | [P6-B200](https://aws.amazon.com/ec2/instance-types/p6/) (8×B200 180GB) | [ND GB200-v6](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nd-gb200-v6-series) | [A4](https://cloud.google.com/blog/products/compute/introducing-a4-vms-powered-by-nvidia-b200-gpu-aka-blackwell/) (8×B200) | BM.GPU.B200.8 (8×B200) |
| **GB200 (NVLink)** | [P6e-GB200 UltraServer](https://aws.amazon.com/ec2/instance-types/p6/) (最大72 GPU) | ND GB200-v6(NVLinkドメイン) | [A4X](https://cloud.google.com/blog/products/compute/new-a4x-vms-powered-by-nvidia-gb200-gpus) (GB200 NVL72) | — |
| H100インスタンス | [p5.48xlarge](https://aws.amazon.com/ec2/instance-types/p5/) (8×H100 80GB) | [ND H100 v5](https://learn.microsoft.com/en-us/azure/virtual-machines/nd-h100-v5-series) (8×H100 80GB) | [a3-highgpu-8g](https://cloud.google.com/compute/docs/gpus#h100-gpus) (8×H100 80GB) | [BM.GPU.H100.8](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) (8×H100 80GB) |
| A100インスタンス | [p4d.24xlarge](https://aws.amazon.com/ec2/instance-types/p4/) (8×A100 40/80GB) | [ND A100 v4](https://learn.microsoft.com/en-us/azure/virtual-machines/nda100-v4-series) (8×A100 80GB) | [a2-highgpu-8g](https://cloud.google.com/compute/docs/gpus#a100-gpus) (8×A100 80GB) | [BM.GPU.A100-v2.8](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm) (8×A100 80GB) |
| RTX PRO / 推論特化 | [G7](https://aws.amazon.com/ec2/instance-types/g7/) (NVIDIA RTX PRO 4500 Blackwell) | — | — | — |
| 自社AIチップ | Trainium2 (Trn2), Inferentia2 (Inf2) | Maia 100 | **TPU v8**(第8世代) | — |
| 予約オプション | Reserved Instances, Savings Plans | Reserved VM Instances | CUD (Committed Use Discount) | Capacity Reservation |
| スポット/プリエンプティブル | Spot Instances | Spot VMs | Spot VMs (Preemptible) | Preemptible Instances |

:::caution
GPUインスタンスの価格はリージョン、コミット期間、可用性によって大きく異なります。最新の価格は各ベンダーの価格計算ツールを参照してください。
:::

:::note
**機密AI推論:** モデルIPや機密性の高い入力データを処理中も保護する必要がある場合は、**機密コンピューティングGPU**(Azure NCC H100 v5, GCP A3 Confidential VM)を使用できます。ベンダー別の機密コンピューティング比較は[データ保護 — 機密コンピューティング](../../security/data-protection/#기밀-컴퓨팅-confidential-computing)を参照してください。
:::

## RAGパイプライン

RAG(Retrieval-Augmented Generation)パイプラインは、Vector DB、Embeddingモデル、LLM、オーケストレーションの組み合わせで構成されます。各ベンダーの主要サービス:

- **AWS** — OpenSearch Serverless + Titan Embeddings + Bedrock Knowledge Bases
- **Azure** — AI Search + Microsoft Foundry + Azure AI Studio
- **Google Cloud** — Vertex AI Vector Search + Gemini Embedding + RAG Engine
- **OCI** — OCI Search/Oracle 23ai + Cohere Embed + Enterprise AI Agents

:::note
RAGパイプラインの実装パターン(ハイブリッド検索、チャンキング戦略、リランキング、オーケストレーション)の詳細は[RAG高度パターン](../../ai/rag-patterns/)を参照してください。
:::

## アーキテクチャ選択パターン

| パターン | 説明 | 適したケース |
| --- | --- | --- |
| 単一CSP AIプラットフォーム | 1つのクラウドのモデル、データ、デプロイツールをすべて使用 | 運用のシンプルさが最も重要な場合 |
| モデル分散 | モデルは複数CSPのAPIを使用し、アプリケーションは1か所で運用 | モデルの品質とコストを比較しながら選択する必要がある場合 |
| データ近接型 | データが存在するクラウドでエンベディング・検索・推論を実行 | データ移動コストや規制が重要な場合 |
| 中央RAGプラットフォーム | 1つの共通RAG層から複数CSPのモデルを呼び出し | 組織全体に共通のAIプラットフォームを提供する場合 |

## 設計時の注意事項

- **データ移動コスト** — 大量の文書、エンベディング、ログをクラウド間で移動すると、イグレス費用が大きくなる可能性があります。
- **データ主権** — 個人情報、金融データ、医療データは保存場所と処理場所を明確にする必要があります。
- **モデル依存性** — 特定モデルのAPI形式、トークン制限、関数呼び出し方式に依存しないよう、抽象化レイヤーを設けます。
- **可観測性** — プロンプト、応答、トークン使用量、レイテンシ、コストを併せてモニタリングします。
- **セキュリティ** — プロンプトインジェクション、機密情報の漏えい、過度なエージェント権限を統制する必要があります。

:::note
マルチクラウドAIは、すべてのベンダーを同時に使うことが目標ではありません。データの所在、モデルの品質、コスト、規制要件に応じて、必要な組み合わせだけを選択することが要点です。
:::

## よくある間違い

- **すべてのベンダーのAIサービスを同時に導入** — マルチクラウドAIは必要な組み合わせだけを選択するものだが、すべてのベンダーを並行して運用し複雑度とコストが急増
- **データ移動コストを事前に算定しない** — エンベディング、文書、ログをクラウド間で移動すると、イグレス費用が想定より大きく発生
- **モデルAPI形式に直接依存** — 抽象化レイヤーなしに特定ベンダーの関数呼び出し方式にコードを合わせ、モデルの入れ替えが困難になる

## チェックリスト

- [ ] マルチクラウドAI導入の理由(モデル品質、コスト、規制)を明確に定義したか
- [ ] データ移動コスト(イグレス)を事前に算定し、データ近接型アーキテクチャを検討したか
- [ ] モデル呼び出しに抽象化レイヤー(LangChainなど)を設け、ベンダーの入れ替えが可能な構造になっているか

## 参考資料

### AWS

- [Amazon Bedrockドキュメント](https://docs.aws.amazon.com/bedrock/)
- [Amazon SageMaker AIドキュメント](https://docs.aws.amazon.com/sagemaker/)

### Azure

- [Azure AI Servicesドキュメント](https://learn.microsoft.com/en-us/azure/ai-services/)
- [Microsoft Foundry(旧Azure OpenAI) Serviceドキュメント](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

### Google Cloud

- [Vertex AIドキュメント](https://cloud.google.com/vertex-ai/docs)
- [Gemini APIドキュメント](https://cloud.google.com/gemini/docs)

### OCI

- [OCI AI Servicesドキュメント](https://www.oracle.com/artificial-intelligence/ai-services/)
- [OCI Enterprise AI(旧OCI Generative AI)ドキュメント](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)
