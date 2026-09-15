---
title: "Physical AI データと学習"
description: "エッジ推論・IoTハードウェアとセンサーデータパイプライン(レイヤー1)、デジタルツイン・シミュレーション・公開データセット・Sim-to-Real(レイヤー2)、および規模に見合う学習インフラの選択をベンダー中立の視点で比較します。"
---

> 文書基準: 2026年9月 | この文書は変化の速い領域であり、四半期ごとのレビュー対象です。

## 概要

この文書はPhysical AIパイプラインの前段 — **物理世界からデータが入り、学習資産になるまで** — を扱います。全体パイプラインの概観は[Physical AI 概要](./overview/)を、学習済みモデルをデプロイ・運用する後段は[デプロイと運用](./deploy-and-operate/)を参照してください。

## レイヤー1 — エッジ推論とIoT

物理世界のデータは大量かつリアルタイムであり、すべてをクラウドへ送って処理するのは困難です。現場(エッジ)でまず推論し、必要なデータのみをクラウドへ上げる構造が基本です。

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| エッジランタイム | [IoT Greengrass](https://docs.aws.amazon.com/greengrass/v2/developerguide/) | [Azure IoT Operations](https://learn.microsoft.com/azure/iot-operations/) / [IoT Edge](https://learn.microsoft.com/azure/iot-edge/) | [Google Distributed Cloud (Edge)](https://cloud.google.com/distributed-cloud) | [Roving Edge Infrastructure](https://www.oracle.com/cloud/roving-edge-infrastructure/) |
| エッジML推論 | Greengrass MLコンポーネント (SageMaker AIモデルのデプロイ) | IoT Edgeモジュール + Azure AIサービス | Edge TPU / Coral (現行サポート状況の確認が必要) | RED上のコンピュートで自前構成 |
| 産業データ収集 | [IoT SiteWise](https://aws.amazon.com/iot-sitewise/) (OPC UA) | IoT Operations (OPC UA) | — (パートナー・自前構成) | — (自前構成) |

:::caution
**Azure Perceptは2023年3月に提供終了**しました。過去の資料でPerceptがエッジAIハードウェアとして紹介されていても、現在はAzure IoT Edge / IoT OperationsとAzure Certified Deviceパートナーハードウェアで同様の機能を構成します(Microsoftが単一の公式後継製品を指定したわけではありません)。古い製品名をアーキテクチャの前提にしないでください。
:::

### エッジ推論ハードウェア

エッジランタイムがソフトウェア層だとすれば、その下で実際に推論を実行する**アクセラレータハードウェア**の選択が実現可能性とTCOを左右します。判断基準は4つです — 目標モデルを動かす**演算性能**、モデルが載る**メモリ容量**、ロボットの**電力・発熱予算**、そして**ソフトウェアエコシステムの寿命**です。

| 系統 | 性格 | 留意点 |
| --- | --- | --- |
| ロボティクス向けエッジモジュール(例: [NVIDIA Jetson](https://developer.nvidia.com/embedded/jetson-modules)系) | 低電力の小型モジュールから高性能モジュールまで幅が広く、ロボティクスVLAのオンデバイス推論でよく検討される選択肢 | 世代・モジュール間で性能とメモリの差が大きく、価格帯も大きく開きます。目標モデルが該当モジュールのメモリに載るかを先に確認してください |
| 汎用CPU内蔵NPU・小型アクセラレータ | 分類・検出のような軽量ビジョンには十分で、電力・単価が低い | 大規模マルチモーダル・VLA推論にはメモリと帯域が不足する場合が少なくありません |
| FPGA・産業用SoC | 決定論的な遅延と長期供給の保証が重要な設備に有利 | 開発難度が高く、モデル移植のコストが大きくなります |
| クラウド事業者のエッジアプライアンス | クラウドの運用ツール・管理体系を現場へ拡張 | 現場サーバー・ゲートウェイ用途であり、ロボット搭載のリアルタイム制御を代替しません |

:::caution
**TOPSの数値だけで比較しないでください。** ベンダーが示す演算性能は精度(INT8・FP4など)と希薄化(sparsity)適用の有無で基準が変わるため、条件の異なる数値を並べても比較は成立しません。実際の推論速度はメモリ容量・帯域とモデルの適合性に左右されることが多いため、**目標モデルを対象モジュール上で実測する**ほうが確実です。
:::

:::caution
エッジアクセラレータでは、**ソフトウェアエコシステムの寿命**がハードウェアの寿命と同じくらい重要です。ドライバ・ランタイムの更新が止まった製品は新しいカーネルや新しいモデルフォーマットに対応できず、早期の置き換え圧力が生じます。上のレイヤー1の表にある[Google Edge TPU / Coral](https://developers.google.com/coral/guides/faq)がその例で、公式の製品EOL告知がない状態でも[レガシーAPIリポジトリがアーカイブされ「メンテナンスされていない」と明記](https://github.com/google-coral/edgetpu)されています。名称が似ている**Coral NPUはシリコンパートナー向けのオープンソースNPU IPで別物**であり、Edge TPUモジュール製品群の公式な後継ではないため、同一製品の後継として読まないでください。新規設計に入れる前に**現行のサポート状況とドライバ更新履歴を直接確認**してください。価格も固定値ではなく世代交代の時期に調整された事例があるため、大量展開の計画は見積もりを取り直して検証する必要があります。
:::

### センサーデータパイプライン — 収集・保存・ラベリング

エッジから上がってきたデータをそのまま学習に使うことはできません。Physical AIのデータは**1D時系列(関節角度・電流・温度)、2D映像、3D点群、設備メタデータが混在するマルチモーダル**であり、収集 → 保存 → 整備・ラベリングの段階を経てはじめて学習パイプラインに入ります。

| 段階 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| ストリーム・映像収集 | [IoT Core](https://aws.amazon.com/iot-core/) (エッジ入口) / [Kinesis Video Streams](https://aws.amazon.com/kinesis/video-streams/)・[Data Streams](https://aws.amazon.com/kinesis/data-streams/) (ダウンストリーム格納) | [Event Hubs](https://learn.microsoft.com/azure/event-hubs/) + IoT Operations | [Pub/Sub](https://cloud.google.com/pubsub) | [OCI Streaming](https://www.oracle.com/cloud/streaming/) |
| データレイク | [S3](https://aws.amazon.com/s3/) | [Data Lake Storage](https://learn.microsoft.com/azure/storage/blobs/data-lake-storage-introduction) | [Cloud Storage](https://cloud.google.com/storage) | [Object Storage](https://www.oracle.com/cloud/storage/object-storage/) |
| 学習用並列ファイルシステム | [FSx for Lustre](https://aws.amazon.com/fsx/lustre/) | [Azure Managed Lustre](https://azure.microsoft.com/products/managed-lustre) | [Managed Lustre](https://cloud.google.com/products/managed-lustre) / [Parallelstore](https://cloud.google.com/parallelstore) | [File Storage with Lustre](https://www.oracle.com/cloud/storage/file-storage-with-lustre/) |
| ラベリング | [SageMaker Ground Truth](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html) (新規顧客の受付終了) | [Azure MLデータラベリング](https://learn.microsoft.com/azure/machine-learning/how-to-label-data) | — (マネージドは終了、パートナー・OSS) | [OCI Data Labeling](https://www.oracle.com/artificial-intelligence/data-labeling/) |

:::caution
**マネージドのラベリングサービスはむしろ減少傾向にあります。** Google CloudのVertex AIデータラベリングは[2024年10月3日に終了](https://cloud.google.com/vertex-ai/docs/deprecations)しており、AWS SageMaker Ground Truthは2026年7月30日から新規顧客を受け付けません(既存顧客は継続利用可、新機能の追加予定なし)。Ground Truth Plusは2026年6月30日にサポートが終了しました。ラベリングを特定クラウドのマネージドサービスに縛って設計せず、**OSS・パートナーツールで代替可能な構造**を既定にしてください。
:::

:::note
GPU学習のボトルネックは演算ではなく**データロードとチェックポイント書き込み**であることが少なくありません。オブジェクトストレージから直接読むとGPUが遊ぶため、学習区間では並列ファイルシステムを前段に置きオブジェクトストレージと連携する構成が一般的です。ストレージ層の一般比較は[ブロック・ファイルストレージ](../../../storage/block-and-file/)、チェックポイント戦略は[分散学習](../gpu-infra/distributed-training/)を参照してください。
:::

## レイヤー2 — デジタルツインとシミュレーション

ロボット・車両を実世界だけで学習させると、コスト・リスク・時間が大きくなります。そのため物理環境を仮想に複製した**デジタルツイン**と**シミュレーション**で大量のシナリオを生成・学習し、現実へ移すsim-to-realのアプローチが定着しました。

| 項目 | AWS | Azure | Google Cloud | OCI | クロスベンダー |
| --- | --- | --- | --- | --- | --- |
| デジタルツイン | [IoT TwinMaker](https://aws.amazon.com/iot-twinmaker/) | [Azure Digital Twins](https://learn.microsoft.com/azure/digital-twins/) | — (Spanner Graph・BigQueryなどで自前構成) | — | [NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/) |
| ロボット・物理シミュレーション | — (RoboMakerサポート終了、自前構成) | — (パートナー・自前構成) | — (パートナー・自前構成) | — | [NVIDIA Isaac Sim / Isaac Lab](https://developer.nvidia.com/isaac/sim) |

:::caution
**AWS RoboMakerは2025年9月10日にサポートが終了**しました。現在AWSでのロボットシミュレーションは、専用のマネージドサービスなしにGPUインスタンス + OSS(Isaac Sim、Gazeboなど)で自前構成します。EOL(サポート終了)のサービスを新規設計に入れないよう注意してください。
:::

:::note
デジタルツイン・ロボットシミュレーション層は**NVIDIA Omniverse・Isaacエコシステムが広く活用されています。** 主要クラウドはいずれもこのスタックをGPUインスタンス上で実行する形で対応しており、特定クラウド専用のマネージド製品に依存するよりも、**どのクラウドでも移して実行できるか(可搬性)** を先に確認することがロックイン低減につながります。
:::

### 学習データはなぜ不足するのか

シミュレーションが選択肢ではなく前提になる理由は**データ希少性**にあります。言語モデルはインターネット上のテキストという事実上無限の事前学習データから出発しましたが、「ロボットが実際に物を掴んで運んだ」データは桁違いに少ないのが実情です。Physical AIの学習は、安価で豊富なデータで不足を補う設計から始まります。

| データ層 | 性格 | 限界 |
| --- | --- | --- |
| インターネット映像・画像・テキスト | 事実上無限で安価。一般常識・物体知識を提供 | ロボットの身体・関節指令と直接結びつかない |
| 人の作業映像(一人称) | 相対的に多い。動作順序・意図の手がかりを提供 | 人の身体基準のため、ロボットのembodimentへそのまま移せない |
| ロボットのteleopエピソード | 実際の関節指令を含み最も正確 | 人がロボットを直接操作して作るため、収集コストが最も高い |

**teleoperation(遠隔操作)** とは、人がコントローラやVR機器でロボットを直接動かして実演データを作る方式であり、そのデータをそのまま模倣するよう学習させるのが**模倣学習(imitation learning)** です。最も確実な方法ですが、人の時間がそのままコストになるため規模を拡大しにくいという制約があります。

:::note
クラウドのコスト算定の観点では、この構造は**GPUコストとは別の軸が存在する**ことを意味します。データ収集(機材・人件費)、保存・転送、ラベリングのコストが学習演算コストとは独立に発生するため、GPU時間だけでTCOを見積もると大きく外れます。
:::

### 公開データセットとベンチマークのエコシステム

データ希少性は一つの組織だけで埋めるのが難しいため、複数の機関がデータを持ち寄り評価課題を共有する公開エコシステムが形成されています。スタックを選ぶ際、**「このスタックでどの公開資産をそのまま使えるか」** はロックインを判断する実質的な基準になります。

| 区分 | 代表的な資産 | 何に使うか |
| --- | --- | --- |
| クロスロボットデータセット | [Open X-Embodiment](https://github.com/google-deepmind/open_x_embodiment) ([論文](https://arxiv.org/abs/2310.08864)) | 複数機関のロボットデータを統合したコレクション。cross-embodiment事前学習の基準線 |
| 大規模操作データセット | [DROID](https://github.com/droid-dataset/droid) | 多様な環境で収集したteleopデータ |
| シミュレーションベンチマーク | [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)、[CALVIN](https://github.com/mees/calvin)、[RoboCasa](https://github.com/robocasa/robocasa)、[Meta-World](https://github.com/Farama-Foundation/Metaworld) | 標準課題セットでの作業成功率によりポリシーを比較 |
| 人の作業映像 | [Ego4D](https://ego4d-data.org/) | 一人称の作業映像。上記データ3層の中間層に相当 |
| オープンツールチェーン | [LeRobot](https://github.com/huggingface/lerobot) | データ形式・学習・評価をまとめたOSSスタック |

:::caution
公開データセットは**ライセンス条件が資産ごとに異なります。** 研究用途のみ許諾される場合や、出典表示・派生物の公開を求める場合があるため、商用製品の学習資産として使う前に、各データセットのライセンスとその構成要素(個々の機関が寄与した部分)の条件を併せて確認する必要があります。例えばOpen X-Embodimentは単一ライセンスではなく**構成データセットごとに条件が異なり**、Ego4Dは商用利用に別途の規約が適用される場合があります。
:::

:::note
公開データセットで事前学習されたモデルを使えば初期のデータ収集量を減らせますが、**自社ロボットのembodimentと対象作業がそのデータに含まれているか**が実際の効果を分けます。ベンチマークの成績も同様に、測定条件が異なれば比較対象になりません([何をもって合格と判定するか](./deploy-and-operate/#何をもって合格と判定するか)参照)。
:::

### Sim-to-Real Gap

シミュレーションの価値は明確ですが、**シミュレータの物理・センサー・材質モデルは現実と微妙に異なります。** 摩擦係数、照明、センサーノイズ、部品のガタつきといった差が積み重なり、シミュレーションで成功したポリシーが実機で失敗する現象を**Sim-to-Real Gap**と呼びます。

一般的な緩和策は3つあります。

- **ドメインランダム化** — 摩擦・質量・照明・テクスチャなどの物理パラメータを学習中にランダムに揺らし、現実がその分布に収まるようにします。
- **実機データによる少量のファインチューニング** — シミュレーションで事前学習したポリシーを、実機データで仕上げ調整します。
- **実機検証ゲート** — シミュレーション成功率とは別に、実機での成功率をデプロイ基準として設けます。

:::caution
**シミュレーション成功率をそのままデプロイ根拠にしないでください。** シミュレーションの指標は回帰検知には有用ですが、現実の性能を保証しません。シミュレータを選ぶ際も、レンダリング品質だけでなく**対象ドメインの物理精度**(接触・摩擦・変形など)を併せて確認する必要があります。
:::

## 規模に見合う学習インフラ

Physical AIでありがちな誤解が「ロボットモデルの学習には必ず大規模GPUクラスタが要る」というものです。実際には**事前学習済みのロボット基盤モデルを自社のロボット・作業に合わせるファインチューニング**が大半であり、この区間はLLMの事前学習とは規模がまったく異なります。小規模なPEFT・アダプタ学習は、単一GPUの短時間ジョブで終わることが多くあります。

| 段階 | 作業の性格 | インフラパターン | コスト戦略 |
| --- | --- | --- | --- |
| 初期検証 | 実演データが少量、LoRA・PEFTアダプタの学習 | 単一GPUインスタンス1台 | スポット・プリエンプティブルインスタンスを既定に。中断されても再開コストが小さい |
| 作業特化 | 実演データが中規模、全体のファインチューニング | 単一ノード複数GPU + マネージド学習ジョブ | 自動チェックポイント・再開のあるマネージド学習サービス |
| プラットフォーム化 | 多数のロボット・多数の作業、反復的な再学習 | 複数ノード + 高速インターコネクト | 予約・コミット割引。ノードの自動復旧が必要([分散学習](../gpu-infra/distributed-training/)参照) |

:::note
このはしごの実質的な含意は、**最初の段階で大規模なコミットをしない**ことです。初期・作業特化の区間はスポット/プリエンプティブルインスタンスと従量課金で十分な場合が多く、予約・コミットは再学習サイクルが定例化してから検討しても遅くありません。逆にシミュレーションは並列環境数を増やすほどGPUを長く占有するため、学習よりシミュレーションがコストを支配するケースが頻繁にあります。GPUインスタンスファミリー・インターコネクトのベンダーマッピングは[GPUワークロードとアーキテクチャ](../gpu-infra/workload-and-architecture/)を参照してください。
:::

## よくある間違い

- **すべてのデータをクラウドへ送る** — 遅延・帯域・コストを無視した設計はリアルタイム制御で破綻します。エッジ推論の分担が先です。
- **EOL製品を新規設計に使う** — RoboMaker・Percept・マネージドのラベリングサービスのように、サポートが終了または縮小したサービスを古い資料だけで採用しないでください。
- **単一ベンダーのシミュレータに依存** — 特定クラウド専用のシミュレーションに学習パイプラインを縛ると、移行・比較が困難になります。
- **GPUコストだけでTCOを見積もる** — データ収集・保存・ラベリングとシミュレーションの占有コストが、学習演算とは別に発生します。
- **シミュレーション成功率をデプロイ根拠に使う** — 実機rolloutの検証ゲートなしにデプロイすると、Sim-to-Real Gapが現場で顕在化します。

## チェックリスト

### データ・コスト

- [ ] センサーデータの保存・整備・ラベリング層を設計し、ラベリングツールの代替可能性を確認したか?
- [ ] データ収集・保存・ラベリング・シミュレーションのコストをGPUコストとは別に算定したか?
- [ ] 利用する公開データセット・ベンチマークのライセンスと自社embodimentのカバー範囲を確認したか?

### ハードウェア・学習

- [ ] エッジアクセラレータをTOPSの数値ではなく目標モデルの実測で選定し、ドライバ・ランタイムのサポート寿命を確認したか?
- [ ] 学習規模に見合うインフラ段階を選んだか(初期検証で過度なコミットをしていないか)?
- [ ] デジタルツイン・シミュレーションスタックが他のクラウドへ移行可能か(ロックイン点検)?
- [ ] 利用予定のIoT・ロボティクスサービスは現行サポート状態か(EOL確認)?

## 関連文書

- [Physical AI 概要](./overview/) — 全体パイプライン・階層構造・未解決問題
- [デプロイと運用](./deploy-and-operate/) — ロボティクス基盤モデル・安全・アーキテクチャ・フリートデプロイ
- [ブロック・ファイルストレージ](../../../storage/block-and-file/) — 並列ファイルシステムの比較
- [GPUインフラ](../gpu-infra/workload-and-architecture/) — クラウド学習・シミュレーション用GPUクラスタ
- [分散学習](../gpu-infra/distributed-training/) — 複数ノード学習・チェックポイント戦略

## 参考リンク

### AWS

- [AWS IoT Greengrass開発者ガイド](https://docs.aws.amazon.com/greengrass/v2/developerguide/)
- [AWS IoT TwinMaker](https://aws.amazon.com/iot-twinmaker/)
- [AWS IoT SiteWise](https://aws.amazon.com/iot-sitewise/)
- [Amazon FSx for Lustre](https://aws.amazon.com/fsx/lustre/)
- [Amazon SageMaker Ground Truthドキュメント](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html)

### Azure

- [Azure IoT Operationsドキュメント](https://learn.microsoft.com/azure/iot-operations/)
- [Azure Digital Twinsドキュメント](https://learn.microsoft.com/azure/digital-twins/)
- [Azure Managed Lustre](https://azure.microsoft.com/products/managed-lustre)
- [Azure Machine Learningデータラベリング](https://learn.microsoft.com/azure/machine-learning/how-to-label-data)

### Google Cloud

- [Google Distributed Cloud](https://cloud.google.com/distributed-cloud)
- [Coral / Edge TPU](https://cloud.google.com/edge-tpu)
- [Google Cloud Managed Lustre](https://cloud.google.com/products/managed-lustre)
- [Google Cloud Parallelstore](https://cloud.google.com/parallelstore)

### OCI

- [Oracle Roving Edge Infrastructure](https://www.oracle.com/cloud/roving-edge-infrastructure/)
- [OCI File Storage with Lustre](https://www.oracle.com/cloud/storage/file-storage-with-lustre/)
- [OCI Data Labeling](https://www.oracle.com/artificial-intelligence/data-labeling/)

### 公開データセット・ツールチェーン

- [Open X-Embodiment (リポジトリ)](https://github.com/google-deepmind/open_x_embodiment) · [論文](https://arxiv.org/abs/2310.08864)
- [LeRobot (OSSロボティクスツールチェーン)](https://github.com/huggingface/lerobot)
- [Ego4D](https://ego4d-data.org/)
