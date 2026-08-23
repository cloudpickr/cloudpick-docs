---
title: "モニタリング"
description: "メトリクス/ログ/トレース、APM、SLOモニタリング、アラート運用の原則をベンダー別に比較します。"
---

> 文書基準: 2026年5月

:::note
マルチクラウド統合観測可能性は[統合観測可能性アーキテクチャ](../../devops/observability/)を参照してください。
:::

## 概要

オンプレミスでは、Nagios、Zabbixのようなツールをインストールしてサーバー状態を監視します。クラウドではベンダーが管理型モニタリングサービスを提供しており、エージェントのインストールやサーバー運用なしにメトリクス、ログ、トレースを収集し、アラートを設定できます。

### なぜモニタリングが重要か

- **障害検知** — サーバーダウン、応答遅延、エラー率の急増を素早く検知します。
- **原因分析** — 「遅い」という症状から、「どのサービスのどのクエリが遅いか」まで追跡します。
- **キャパシティプランニング** — トラフィックの推移を見てスケーリングのタイミングを判断します。
- **ビジネス上の意思決定** — デプロイ後の転換率、エラー率の変化を確認してロールバックの要否を決定します。

### 観測可能性（Observability）の3本柱

- **メトリクス**（Metrics） — CPU、メモリ、リクエスト数などの数値データ。ダッシュボードとアラートに使用。
- **ログ**（Logs） — アプリケーション/システムが出力するテキスト記録。問題の原因分析に使用。
- **トレース**（Traces） — 分散システムでリクエストが経由する経路の追跡。ボトルネック箇所の特定に使用。

この3つを**相関関係**（Correlation）として結び付けることが重要です。「エラー率が上昇した」（メトリクス）→「どのリクエストで?」（トレース）→「具体的に何のエラー?」（ログ）を一つの流れとして追跡できる必要があります。

### APM（Application Performance Monitoring）

インフラメトリクス（CPU、メモリ）だけでは「なぜ遅いのか」は分かりません。**APM**は、アプリケーションコードレベルで応答時間、DBクエリ時間、外部API呼び出し時間を測定し、ボトルネックを見つけます。

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | X-Ray + CloudWatch Application Signals | サービスマップ + SLOモニタリング |
| Azure | Application Insights | 自動計装。パフォーマンス異常の自動検知 |
| Google Cloud | Cloud Trace + Cloud Profiler | トレーシング + コードレベルのプロファイリング |
| OCI | OCI Application Performance Monitoring | 分散トレーシング + 合成モニタリング |

### なぜ複数の関係者が一緒に見る必要があるのか

モニタリングは運用チームだけのツールではありません。

- **開発者** — デプロイ後のエラー率/遅延の変化を直接確認。コードの問題を素早く把握。
- **運用/SRE** — インフラ状態、キャパシティ、SLO遵守状況をモニタリング。
- **製品/ビジネス** — 転換率、ユーザー体験指標を確認。

同じダッシュボードを共有すれば、「遅い」という報告に対して開発者、運用、ビジネスが同じデータを見て素早く意思決定できます。これがDevOpsで**可視性**（Visibility）が重要な理由です。

### アラートはアクションにつながるべき

アラート（Alert）は受け取ることが目的ではなく、**即座の対応が必要な状況**でのみ鳴るべきです。すべての警告をアラートとして送ると、疲労（Alert Fatigue）が蓄積し、結局重要なアラートを無視するようになります。

| レベル | 基準 | アクション |
| --- | --- | --- |
| **緊急（Page）** | ユーザーに影響。即座の対応が必要 | 当番呼び出し。自動復旧トリガー |
| **警告（Warning）** | まもなく問題になり得る | 業務時間内に確認。チケット作成 |
| **情報（Info）** | 参考用。対応不要 | ダッシュボードのみに表示。アラートは送らない |

:::caution
**Alert Fatigue（アラート疲労）** — 過剰なアラートは、かえって重要なアラートを見逃す原因になります。アクションを伴わずに受け取るだけのアラートは定期的に削除するか、Infoレベルに下げてください。
:::

持続可能なアラート運用のための原則:

- **アクションのないアラートは削除してください。** 受け取っても何もしないアラートはノイズです。
- **自動復旧をまず試みてください。** アラート → Lambda/Runbookで自動対応 → 失敗時のみ人を呼び出す。
- **定期的にアラートをレビューしてください。** 1か月間一度もアクションしなかったアラートは削除候補です。

## SLOモニタリング

SLOモニタリングは、サービスの信頼性を定量的に追跡する重要な活動です。各ベンダーは、SLO定義、エラーバジェットの追跡、バーンダウンチャートを提供する専用ツールを備えています。

:::note
SLI/SLO/SLAの概念、エラーバジェット運用、ベンダー別SLOツールの比較は[SLI/SLOとエラーバジェット](../../devops/slo/)を参照してください。
:::

## 製品比較

### メトリクス + ダッシュボード + アラート

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | CloudWatch Metrics + Alarms | AWSサービスメトリクスを自動収集。カスタムメトリクス対応 |
| Azure | Azure Monitor Metrics + Alerts | Azureサービス統合。Action Groupsでアラートをルーティング |
| Google Cloud | Cloud Monitoring | 自動収集 + カスタムメトリクス。PromQL互換 |
| OCI | OCI Monitoring | OCIサービスメトリクスを自動収集。アラーム + 通知 |

### ログ

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | CloudWatch Logs | ロググループ/ストリーム構造。Logs Insightsでクエリ |
| Azure | Azure Monitor Logs（Log Analytics） | KQL（Kusto Query Language）で分析 |
| Google Cloud | Cloud Logging | 自動収集。Log AnalyticsでSQLクエリ |
| OCI | OCI Logging | サービスログを自動収集。Logging Analyticsで分析 |

### 分散トレーシング

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | X-Ray | AWSサービス間のリクエスト追跡。OpenTelemetry互換 |
| Azure | Application Insights | 自動計装。パフォーマンス異常検知 |
| Google Cloud | Cloud Trace | 自動収集。OpenTelemetry互換 |
| OCI | OCI APM Tracing | 分散トレーシング。OpenTelemetry互換 |

### 統合ダッシュボード

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | CloudWatch Dashboards | |
| Azure | Azure Dashboards / Workbooks | Workbooksでインタラクティブなレポート |
| Google Cloud | Cloud Monitoring Dashboards | |
| OCI | OCI Monitoring Console | カスタムダッシュボード |

## 主な違い

**AWS CloudWatch** — AWSサービスメトリクスが自動的に収集され、アラート → SNS → Lambda連携で自動復旧パイプラインを構成できます。ただし、ログクエリ（Logs Insights）は他社と比べて機能が限定的です。

**Azure Monitor** — Application Insightsがアプリケーションパフォーマンスモニタリング（APM）を標準で提供します。KQLで強力なログ分析が可能で、Workbooksでインタラクティブなレポートを作成できます。

**Google Cloud Cloud Operations** — OpenTelemetryとの統合が最も自然です。Cloud LoggingがすべてのGoogle Cloudサービスのログを自動収集し、BigQueryにエクスポートして長期分析が可能です。

**OCI Monitoring** — OCIサービスメトリクスを自動収集し、Logging Analyticsでログ分析と可視化を提供します。APM Tracingで分散トレーシングにも対応しています。

### マルチクラウドモニタリング

複数ベンダーを使用する環境での統合モニタリング（Grafana、Datadog、OpenTelemetryなど）は[統合観測可能性アーキテクチャ](../../devops/observability/)で扱います。

## よくある間違い

- **アラート疲労の放置** — アラートを設定しすぎると、重要なアラートがノイズに埋もれて無視されます。アクションが不要なアラートは削除するか、Infoレベルに下げてください。
- **ダッシュボードを作っただけで見ない** — ダッシュボードを精巧に作っても誰も見なければ意味がありません。週次レビューのルーティンを作ってください。
- **メトリクス収集だけでアクションなし** — メトリクスを収集していても、閾値超過時の自動対応（アラート、スケーリング、Runbook実行）がなければ、モニタリングの価値がありません。

## チェックリスト

- [ ] アラートの閾値が適切かどうか定期的にレビューしているか
- [ ] 主要ダッシュボードを週次でレビューするルーティンがあるか
- [ ] アラートが正しい担当者/チャネルにルーティングされているか
- [ ] 1か月間アクションのないアラートを識別してノイズを除去しているか

## 関連ドキュメント

- [SLI/SLOとエラーバジェット](../../devops/slo/)
- [災害復旧](../../governance/dr/)

## 参考資料

### AWS

- [Amazon CloudWatchドキュメント](https://docs.aws.amazon.com/ko_kr/cloudwatch/)
- [AWS X-Rayドキュメント](https://docs.aws.amazon.com/ko_kr/xray/)

### Azure

- [Azure Monitorドキュメント](https://learn.microsoft.com/ko-kr/azure/azure-monitor/)
- [Application Insightsドキュメント](https://learn.microsoft.com/ko-kr/azure/azure-monitor/app/app-insights-overview)

### Google Cloud

- [Cloud Monitoringドキュメント](https://cloud.google.com/monitoring/docs)
- [Cloud Loggingドキュメント](https://cloud.google.com/logging/docs)
- [Cloud Traceドキュメント](https://cloud.google.com/trace/docs)

### OCI

- [OCI Monitoringドキュメント](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [OCI Loggingドキュメント](https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm)
- [OCI Application Performance Monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/index.html)
