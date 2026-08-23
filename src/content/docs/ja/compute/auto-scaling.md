---
title: "オートスケーリング"
description: "VMオートスケーリング、予測スケーリング、アプリケーションレベルのスケーリングをベンダー別に比較します。"
---

> 文書基準: 2026年8月

## 概要

VMを使うとサーバーを素早く作成できますが、トラフィックの変化への対応は依然としてユーザーの責任です。トラフィックが急増すれば手動でサーバーを追加し、減少すれば再び削除する必要があります。この対応が遅れればサービスがダウンし、過剰であればコストが無駄になります。

**オートスケーリング**は、この判断と実行を自動化します。CPU使用率、リクエスト数などの指標を監視し、しきい値を超えると自動的にサーバーを追加し、負荷が減れば自動的に削除します。

:::caution
オートスケーリングは**スケールアウトに数分かかります**。突然のトラフィックスパイク(秒単位)には十分対応できない場合があります。また、誤った設定は障害を自動的に拡大させる可能性があるため、ポリシー設計とテストが重要です。
:::

## スケーリングポリシーの種類

オートスケーリングは「いつスケーリングするか」を決定するポリシーによって区分されます。

| ポリシー | トリガー | 特徴 | 使用時期 |
| --- | --- | --- | --- |
| **ターゲット追跡 (Target Tracking)** | 特定のメトリクスが目標値を維持するよう自動調整 | 最もシンプル。ほとんどのワークロードに適合 | 基本の選択。一般的なWebサービス |
| **ステップスケーリング (Step Scaling)** | しきい値の超過度合いに応じて複数段階でスケーリング | きめ細かい制御が可能 | トラフィックパターンが多様な複雑なワークロード |
| **シンプルスケーリング (Simple Scaling)** | しきい値超過時に固定数でスケーリング | 従来の方式。クールダウン時間が長め | レガシー互換。新規はTarget Trackingを推奨 |
| **予測スケーリング (Predictive)** | MLでトラフィックを予測し事前に拡張 | 予測可能な周期的パターンに効果的 | 日/週単位で繰り返すトラフィック(通勤、週末) |
| **予約スケーリング (Scheduled)** | 指定された時刻にスケーリング | 予測スケーリングが不可能な計画的イベント | プロモーション、ブラックフライデー、大規模イベント |

:::caution
CPUがボトルネックではないワークロード(I/Oバウンド、メモリバウンド、DBコネクションプール枯渇)では、CPUベースのスケーリングはトラフィック急増後も反応しません。ワークロードの実際のボトルネックメトリクスを選択してください。
:::

### ワークロード別ポリシー組み合わせ例

| ワークロードパターン | 推奨ポリシー組み合わせ | 理由 |
| --- | --- | --- |
| **一般的なWebサービス** (トラフィック緩やかに増加) | Target Tracking (負荷テストで目標値を検証) | シンプルでほとんどの場合十分 |
| **通勤パターン** (毎日9時に急増、18時に減少) | Predictive + Target Tracking | 予測で事前拡張、Targetで微調整 |
| **イベント/プロモーション** (特定時点で急増) | Scheduled + Target Tracking | 開始前に事前拡張、以降は自動調整 |
| **バッチ/データ処理** (キューベース) | Target Tracking (キューの深さ基準) | CPUではなく待機ジョブ数でスケーリング |
| **予測不可能なスパイク** (ゲーム、バイラル) | 高い最小インスタンス数 + CDN/キャッシュ + Rate Limiting | スケーリング速度では対応不可、事前に余裕を確保 |

:::note
ほとんどのワークロードは**メトリクスベースの自動調整(Target Tracking / Target Utilization)一つから始めて**ください。すべてのベンダーがこの方式をサポートしており、複雑なポリシーの組み合わせはトラフィックパターンを十分に観察した後に追加しても遅くありません。複数ポリシー適用時はベンダーごとに動作が異なるため(AWS: 最大容量を選択、Google Cloud: 最も高い信号を基準)、公式ドキュメントを確認してください。
:::

### クールダウン(Cooldown)時間

スケーリングイベント後、次のスケーリングまで待機する時間です。短すぎるとスケーリングが過度に繰り返され(thrashing)、長すぎるとトラフィックの変化への反応が遅くなります。アプリの起動時間より短くしてはいけません。

| ベンダー | デフォルト値 | コールドスタート緩和 |
| --- | --- | --- |
| AWS | 300秒 | Warm Pool (事前初期化されたインスタンスを待機) |
| Azure | 5分 | Instance Protection、Custom Script Extension |
| Google Cloud | 60秒 (Initial Delay) | Auto-healing + 事前ビルドイメージ |
| OCI | 300秒 | クールダウン期間を設定可能 |

## オートスケーリングの限界

| 限界 | 説明 | 対応方法 |
| --- | --- | --- |
| **コールドスタート時間** | 新規インスタンスの起動+アプリ準備に数分かかる | 事前初期化されたインスタンスプール、最小インスタンス数の維持、事前ビルドイメージ(Golden Image) |
| **状態を保持するワークロード** | セッション/キャッシュ/ディスクデータのあるインスタンスは縮小時に消失 | 状態を外部ストレージ(Valkey、DB)に分離 |
| **予測不可能なスパイク** | スケーリング速度がトラフィック増加に追いつかない | 最小容量の確保、CDN/キャッシュ、Rate Limiting、Graceful Degradation |
| **Quota枯渇** | アカウント/リージョンのvCPU上限超過時にスケールアウトが無音で失敗 | 事前のQuota確認、増設リクエスト、スケーリング失敗通知の設定 |

## Spot/Preemptibleインスタンスの混合

オートスケーリンググループにオンデマンドとSpotインスタンスを混合すると、中断を許容できるワークロードでコストを削減できます。ただし、Fallback戦略なしでは障害の原因になります。

| ベンダー | 方法 | 備考 |
| --- | --- | --- |
| AWS | ASG Mixed Instances Policy | オンデマンドベース+Spot比率を指定。複数インスタンスタイプのプール |
| Azure | VMSS Spot Priority Mix | Spot VM比率を設定。Eviction Policyを選択 |
| Google Cloud | MIG + Spot VMs | Spot VMをMIGに含める。Preemption時に自動再生成 |
| OCI | Instance Pool + Preemptible | Preemptibleインスタンスをプールに混合 |

## オートスケーリングが内蔵されたサービス

直接スケーリングポリシーを設定しなくてもプラットフォームが自動的に処理するサービスです。

| ベンダー | サービス | 説明 |
| --- | --- | --- |
| AWS | Elastic Beanstalk、ECS Service Auto Scaling、Lambda | アプリ展開時にスケーリング内蔵 |
| Azure | App Service (Auto Scale)、Container Apps、Functions | PaaSレベルの自動スケーリング |
| Google Cloud | Cloud Run、App Engine、GKE Autopilot | リクエストベースの自動拡張/縮小 |
| OCI | Container Instances、Functions | サーバーレス自動スケーリング |

:::note
VMレベルのオートスケーリングを直接設定する前に、ワークロードが上記サービスに適しているか先に検討してください。PaaS/サーバーレスを使用するとVMスケーリングポリシーは大幅に単純化されますが、同時実行制限・最大インスタンス数・ダウンストリーム保護の設定は別途必要です。
:::

## 主な違い

- **AWS** — Mixed Instances Policyでオンデマンド/Spotの混合展開。Warm Poolで事前初期化されたインスタンスを待機させコールドスタートを緩和。
- **Azure** — VMSSがVM展開とスケーリングを一つのリソースとして管理。Spot Priority Mixでコスト最適化。
- **Google Cloud** — MIGにAuto-healingが標準内蔵され、異常なインスタンスを自動的に置き換え。クールダウンが60秒と最も短く、素早い反応。
- **OCI** — Instance Poolベースのオートスケーリング。メトリクス/スケジュールベースのスケーリングをサポートし、Preemptibleインスタンスの混合が可能。

## オートスケーリング設定チェックリスト

- [ ] スケーリングメトリクスをワークロードのボトルネックに合わせて選択したか(CPU、リクエスト数、キューの深さ、応答時間など)
- [ ] Grace Period / Warm-up時間を設定したか(新規インスタンス起動直後のメトリクス不安定区間を無視)
- [ ] ヘルスチェックをLBとオートスケーリングの両方に設定したか
- [ ] Connection Draining / Deregistration Delayを設定したか(進行中のリクエスト完了を保証)
- [ ] アプリのGraceful Shutdown(SIGTERM処理)を実装したか
- [ ] 終了ポリシー(Termination Policy)を確認したか(AZバランス、Newest/Oldestなど)
- [ ] スケールイン保護が必要なインスタンス(展開中、長時間タスク)を除外したか
- [ ] 最小インスタンス数をコールドスタート許容範囲に合わせて設定したか
- [ ] 最大インスタンス数をコスト上限に合わせて設定したか
- [ ] リージョン/AZ別のvCPU Quotaを事前確認し増設をリクエストしたか
- [ ] Spot/Preemptible混合時のFallback(オンデマンド切り替え)戦略を設定したか
- [ ] スケーリングイベント通知と失敗通知を設定したか
- [ ] クールダウン時間がアプリ起動時間より長いか確認したか

## よくある間違い

- **CPUメトリクスのみでスケーリング設定** — I/Oバウンドやメモリバウンドのワークロードでは、CPUが低くてもサービスが遅くなります。実際のボトルネックメトリクス(リクエスト遅延、キューの深さなど)を選択してください。
- **クールダウン時間をアプリ起動時間より短く設定** — 新規インスタンスが準備できる前に次のスケーリングが発生し、不要なインスタンスが過度に生成されます。
- **最大インスタンス数を無制限に設定** — 障害状況でヘルスチェックの失敗が繰り返されるとインスタンスが無限に生成され、コストが急増します。必ず上限を設定してください。

## 参考資料

### AWS

- [AWS Auto Scaling 文書](https://docs.aws.amazon.com/ko_kr/autoscaling/)
- [Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/ko_kr/autoscaling/ec2/userguide/)

### Azure

- [Azure VM Scale Sets 文書](https://learn.microsoft.com/ko-kr/azure/virtual-machine-scale-sets/)
- [Azure Autoscale 文書](https://learn.microsoft.com/ko-kr/azure/azure-monitor/autoscale/autoscale-overview)

### Google Cloud

- [Google Cloud Autoscaler 文書](https://cloud.google.com/compute/docs/autoscaler)
- [Google Cloud MIG 文書](https://cloud.google.com/compute/docs/instance-groups)

### OCI

- [OCI Autoscaling 文書](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/autoscalinginstancepools.htm)
