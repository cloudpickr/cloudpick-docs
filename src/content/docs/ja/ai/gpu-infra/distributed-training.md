---
title: "分散学習の標準アーキテクチャ"
description: "データ・テンソル・パイプライン並列化（DP/TP/PP）と3Dハイブリッド並列化、分散学習フレームワーク、チェックポイント戦略をベンダー中立の視点で整理します。"
---

> 文書基準: 2026年9月 | この文書は変化の速い領域であり、四半期ごとのレビュー対象です。

:::note
この文書は分散学習の並列化戦略を扱います。クラスターの通信層・配置・ファブリックは[GPUワークロードの特性とリファレンスアーキテクチャ](../../ai/gpu-infra/workload-and-architecture/)を、Kubernetes上のスケジューリングは[GPU Kubernetesとスケジューリング](../../ai/gpu-infra/kubernetes-and-scheduling/)を参照してください。
:::

## 概要

モデルとデータが単一のGPUメモリに収まらない場合、複数のGPUに分けて学習する必要があります。分ける方式は大きく**データ並列（DP）**、**テンソル並列（TP）**、**パイプライン並列（PP）**の3つで、大規模学習ではこれらを組み合わせた**3D並列化**を使います。各方式は通信量・メモリ削減・実装の複雑さで異なるトレードオフを持ちます。

:::note
この文書の並列化の概念とフレームワーク（DeepSpeed、Megatron-LM、PyTorch FSDP）はCUDA/NCCLの上で動作し、ベンダーに依存しません。クラウドを変えても並列化戦略自体はおおむね移植できます。実際の性能は[ノード間ファブリック性能](../../ai/gpu-infra/workload-and-architecture/#ノード間高速通信ファブリック--ベンダーマッピング)に左右されます。
:::

## データ並列 (Data Parallelism, DP)

モデル全体を各GPUに複製し、データバッチを分けて処理した後、勾配を同期します。最も単純で、モデルが単一のGPUに収まるときの標準です。

- **通信パターン** — ステップごとに勾配のall-reduce（全GPU collective）
- **限界** — モデル自体が単一のGPUメモリを超えると使用できない
- **メモリ最適化（FSDP/ZeRO）** — モデルパラメータ・勾配・オプティマイザ状態をGPU群に分散保存（sharding）し、データ並列を維持しながら単一GPUメモリの限界を超えてより大きなモデルを学習

## テンソル並列 (Tensor Parallelism, TP)

個々のレイヤーの行列演算自体を複数のGPUに分割します。一つのレイヤーを複数のGPUが同時に計算します。

- **通信パターン** — レイヤー内部で頻繁なcollective通信（遅延に非常に敏感）
- **適用範囲** — 通信頻度が高いため、主に**ノード内NVLink**で接続されたGPU間で使用
- **効果** — 単一のレイヤーがGPUメモリを超えるときに必須

## パイプライン並列 (Pipeline Parallelism, PP)

モデルのレイヤーを段階（stage）に分けて異なるGPUグループに配置し、マイクロバッチをパイプラインで流します。

- **通信パターン** — 段階の境界でのみactivationを伝達（通信量が相対的に少ない）
- **適用範囲** — 通信が少なく**ノード間**への拡張が容易
- **限界** — パイプラインバブル（idle区間）が発生し、マイクロバッチ数で緩和

## 3Dハイブリッド並列化

大規模な事前学習は3つの方式を階層的に組み合わせます。一般的に**ノード内はTP、ノード間はPP、その上にDP**を重ねます。

| 並列化 | 通信量 | メモリ削減 | 遅延敏感度 | 推奨配置 |
| --- | --- | --- | --- | --- |
| **データ並列 (DP)** | 高い（勾配all-reduce） | なし（FSDP/ZeRO使用時は大きい） | 中程度 | クラスター全体 |
| **テンソル並列 (TP)** | 非常に高い（レイヤー内部） | 大きい | 非常に高い | ノード内 (NVLink) |
| **パイプライン並列 (PP)** | 低い（段階の境界） | 大きい | 低い | ノード間 |

:::caution
並列化の次元を増やすほど、実装・デバッグの複雑さが急激に増加します。モデルが単一ノード（例: 8×GPU）に収まるなら、3D並列化なしでFSDP/ZeRO ベースのデータ並列だけで十分な場合が多いです。通信遅延に敏感なTPをノード間に拡張すると、ファブリック性能によってはスループットが急落することがあります。
:::

## 分散学習フレームワーク

| フレームワーク | 主な並列化 | 特徴 |
| --- | --- | --- |
| [PyTorch FSDP](https://docs.pytorch.org/docs/stable/fsdp.html) | DP (sharding) | PyTorchネイティブ、パラメータ/オプティマイザ状態を分散 |
| [DeepSpeed](https://www.deepspeed.ai/) | DP(ZeRO) + PP + TP | ZeRO段階別メモリ最適化、オフローディング対応 |
| [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) | TP + PP + DP | 大規模Transformer事前学習に最適化されたTP実装 |

:::note
フレームワークの選択はベンダー中立です。ただし各クラウドのマネージド学習プラットフォーム（SageMaker、Vertex AI、Azure MLなど）はこれらのフレームワークを事前統合した分散学習ライブラリ・レシピを提供しており、これを使うと通信設定・トポロジ最適化が自動化される代わりに、当該プラットフォームに依存します。
:::

## チェックポイント戦略

大規模学習は数時間～数週間実行されるため、ノード障害に備えたチェックポイントが必須です。チェックポイント設計は**保存頻度とストレージ帯域のバランス**の問題です。

- **頻度** — 頻繁すぎると保存オーバーヘッドでGPUがアイドル状態になり、まれすぎると障害時に失われる計算量が大きくなります。
- **ストレージ帯域** — 数百GB～数TB級のチェックポイントを短時間で書き込む必要があるため、[ストレージ層](../../ai/gpu-infra/workload-and-architecture/#リファレンスアーキテクチャ--3層通信モデル)のスループットがボトルネックになります。
- **非同期・分散保存** — 学習を止めずにバックグラウンドで保存するか、各GPUが自身のシャードのみを並列保存して時間を短縮します。
- **自動再開** — 障害検知後に最後のチェックポイントから再開する流れは[推論サービング・信頼性・コスト最適化 — 信頼性・障害対応](../../ai/gpu-infra/serving-reliability-cost/#信頼性障害対応)で扱います。

## 関連文書

- **クラスターの通信層・ファブリック・配置** — [GPUワークロードの特性とリファレンスアーキテクチャ](../../ai/gpu-infra/workload-and-architecture/)
- **gang scheduling・クォータ** — [GPU Kubernetesとスケジューリング](../../ai/gpu-infra/kubernetes-and-scheduling/)
- **障害の自動再開・容量運用** — [推論サービング・信頼性・コスト最適化](../../ai/gpu-infra/serving-reliability-cost/)
- **AIシステムライフサイクル内の学習パイプライン** — [AIシステムライフサイクルとエンジニアリング](../../ai/lifecycle/)

## よくある間違い

- **不要な3D並列化の導入** — 単一ノードで十分なモデルにテンソル・パイプライン並列を重ね、複雑さとデバッグコストのみが増加
- **テンソル並列をノード間に拡張** — 遅延に敏感なTPをNVLinkの外に広げ、通信ボトルネックが発生
- **チェックポイント頻度だけを上げる** — ストレージ帯域を一緒に増やさず、保存中のGPUアイドル時間が増加
- **オプティマイザ状態のメモリを見落とす** — パラメータ以外にオプティマイザ状態・勾配が占めるメモリを計算せず、OOMが発生

## チェックリスト

- [ ] モデル・オプティマイザ状態が単一GPU/単一ノードのメモリに収まるか計算したか
- [ ] 単一ノードで可能ならFSDP/ZeROデータ並列を優先的に検討したか
- [ ] テンソル並列をノード内（NVLink）に制限し、パイプライン並列をノード間に配置したか
- [ ] チェックポイント頻度とストレージ帯域を一緒に設計したか
- [ ] 障害時の自動再開の流れを検証したか

## 参考リンク

### 共通（ベンダー中立）

- [PyTorch FSDP](https://docs.pytorch.org/docs/stable/fsdp.html)
- [DeepSpeed](https://www.deepspeed.ai/)
- [NVIDIA Megatron-LM](https://github.com/NVIDIA/Megatron-LM)
- [NVIDIA NCCL ドキュメント](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)

### ベンダー別の分散学習

- [AWS — SageMaker 分散学習](https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training.html)
- [Azure — Azure ML 分散学習](https://learn.microsoft.com/azure/machine-learning/concept-distributed-training)
- [Google Cloud — Vertex AI 分散学習](https://cloud.google.com/vertex-ai/docs/training/distributed-training)
- [OCI — Data Science 分散学習](https://docs.oracle.com/en-us/iaas/data-science/using/distributed-training.htm)
