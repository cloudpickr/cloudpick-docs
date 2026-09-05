---
title: "現場デプロイメント（Field Deployment）"
description: "現場デプロイメントエンジニア（FDE）の役割、必要なスキル、そしてマルチクラウド環境での実務知識を整理します。"
---

> 文書基準: 2026年8月

現場デプロイメントエンジニア（Forward Deployment Engineer, FDE）は、顧客環境に直接エンベッドされ、製品をプロダクションに定着させる役割です。設計やアドバイザリーではなく、実際のプロダクションコードを作成し、所有します。

本文書は、FDEがマルチクラウド環境で知っておくべき中核知識を整理します。CloudPickの既存ドキュメントをFDEの観点からキュレーションし、FDE特有のコンテキストを補足します。

:::note
「FDE」というタイトルは組織によって異なる場合があります（Deployment Engineer、Field Engineer、Implementation Engineerなど）。本文書はタイトルではなく**役割** — 顧客現場でプロダクションコードを所有しながら製品をデリバリーするエンジニア — を基準とします。
:::

---

## 役割の起源と拡散

Palantirが2000年代半ば、米国情報機関にGothamを配備する際に生み出した役割です。機密データ、未文書化のスキーマ、既存デプロイ方式の失敗 → エンジニアを顧客現場に直接派遣して問題を解決するモデルが誕生しました。

2024年以降、AI製品が同じ問題に直面したことで爆発的に拡散しました。強力だが汎用的な製品（LLM、エージェント）が顧客の複雑なレガシー環境で実際の価値を生み出すには、現場でコードを書く人材が必要だからです。

### 2025-2026年 主要イベント

| 時期 | イベント | 規模 |
| --- | --- | --- |
| 2026年5月 | OpenAI Deployment Company設立（TPG主導の投資） | ~$4B |
| 2026年5月 | Anthropicエンタープライズサービス JV「Ode」（Blackstone、Goldman Sachs） | ~$1.5B |
| 2026年6月 | AWS Forward Deployed Engineering組織新設 | ~$1B |
| 2025-2026 | FDE求人公告が前年比800%～1,000%+増加 | 39+社、220+オープンポジション |

---

## FDE vs Solutions Architect

FDEとSA（Solutions Architect）はいずれも顧客と技術をつなぐ役割ですが、核心的な違いは**コード所有権**と**エンベッドの深さ**にあります。

| 基準 | Solutions Architect（SA） | Forward Deployment Engineer（FDE） |
| --- | --- | --- |
| **主な活動時期** | プリセール ～ 初期実装 | ポストセール ～ プロダクション運用 |
| **中核業務** | アーキテクチャ設計、技術検証、PoC | プロダクションコード作成、統合、ライブ運用 |
| **コード所有** | 低い（PoC/デモレベル） | 高い（プロダクションコードを直接所有） |
| **顧客関係** | アドバイザリー型（Advisory） | エンベッド型（Embedded） |
| **成果物** | アーキテクチャ図、提案書、統合ガイド | プロダクションコード、カスタム統合、デプロイスクリプト |
| **成功指標** | セールス転換率、プラットフォーム採用率 | デプロイ成功率、システム安定性、TTV（Time-to-Value） |
| **報酬（2026年基準）** | $160K-$270K+ TC | $180K-$550K+ TC（フロンティアAIラボ基準で$1M+） |

### いつ誰を採用するか

- **SA**: 製品のPMFが明確で、技術的な異議がディール成立を妨げているとき
- **FDE**: 製品は強力だが、顧客環境で稼働させるにはカスタムコードが必要なとき
- **SI**: 大規模システム構築プロジェクトを納期内に人員投入で完遂しなければならないとき
- **両方**: 大型エンタープライズ契約 — SAがアーキテクチャを設計し、FDEが実行

### FDE vs SI（システムインテグレーター）

FDEとSI（System Integrator）はいずれも顧客現場でコードを書きますが、**目的と所有構造**が異なります。

| 基準 | FDE | SI（システムインテグレーター） |
| --- | --- | --- |
| **所属** | 製品会社（モデル提供企業、SaaSベンダー） | 別のコンサルティング/SI法人 |
| **目的** | 自社製品を顧客環境に定着させ、製品フィードバックを本社に還流 | SOW（作業指示書）範囲のシステムを納期内に構築・納品 |
| **コード所有** | 製品コアへの貢献が可能。再利用可能なパターンを製品に還流 | 顧客所有。プロジェクト終了後は保守契約に移行 |
| **期間** | 製品が定着するまで（数週間～数か月、反復的） | SOW期間（数か月～数年、終了が明確） |
| **成功指標** | 製品採用率、TTV、製品改善への貢献 | 納期遵守、受入テスト通過、検収 |
| **人員モデル** | 少数精鋭（1～3名） | 大規模投入（数十～数百名） |
| **プレイブック** | なし（プレイブックがまだない場所で働く） | あり（方法論、成果物テンプレート） |
| **製品フィードバック** | 中核的役割 — 現場の問題を製品ロードマップに反映 | 限定的 — ベンダーとは別組織 |

:::note
公共・金融の大型プロジェクトでは、現地SIが全体システムを構築し、FDEは自社AI/SaaS統合のみを担当する**協業**構造が一般的です。国別のSI・調達構図は[韓国](../../korea/) · [米国](../../us/) · [EU](../../eu/) · [日本](../../japan/) · [シンガポール](../../singapore/)ガイドを参照してください。
:::

:::caution
2025-2026年の市場で「FDE」と表記された求人のうち約40%は、実質的にSE（Sales Engineer）やPS（Professional Services）をリブランディングしたものであることが知られています。コード所有権、プロダクション責任、クォータ/OTEの有無で区別できます。
:::

---

## FDEが知っておくべき中核知識

### 1週目：顧客環境への参入

顧客環境に初めて入る際に直面する現実です。この領域はSAや一般的なSWEが経験しない、FDE固有の課題です。

| 課題 | 説明 | 関連ドキュメント |
| --- | --- | --- |
| 他人のアカウントで作業する | 顧客のAWS/Azure/GCPアカウントで最小権限で作業 | [アカウントと組織構造](../../about-cloud/accounts-and-organizations/) |
| 交渉されたIAM | 顧客セキュリティチームと調整した制限付きアクセス権限 | [IAM概要](../../about-cloud/iam-overview/) |
| 網分離環境 | エアギャップ、プロキシ専用、制限されたインターネットアクセス | [網分離とネットワーク隔離](../../security/network-isolation/) |
| リモートアクセス制約 | 顧客ごとのVPN、踏み台ホスト、ゼロトラストアクセス | [リモートアクセス管理](../../devops/remote-access/) |
| コンプライアンス | 顧客の業界別規制（金融：PCI-DSS、医療：HIPAA、公共：FedRAMP） | [コンプライアンス](../../governance/compliance/) |

### インフラとクラウド

FDEは顧客環境に応じて、どのクラウドでも扱えなければなりません。

- [クラウド入門](../../about-cloud/getting-started/) — 基本概念
- [ベンダー比較](../../about-cloud/compare-clouds/) — 同一機能のベンダー別の違い
- [リージョンと可用性ゾーン](../../about-cloud/regions-and-zones/) — データ主権、レイテンシ
- [共同責任モデル](../../about-cloud/shared-responsibility/) — 顧客環境における責任境界

### セキュリティとガバナンス

顧客のセキュリティチームは、FDEにとって最も対応が難しいステークホルダーです。

- [IAM実践](../../security/iam/) — クロスアカウント、一時的な認証情報
- [シークレット管理](../../security/secrets/) — 顧客環境でのシークレットアクセス
- [データ保護](../../security/data-protection/) — 顧客データの取り扱い
- [ゼロトラスト](../../security/zero-trust/) — 現代のエンタープライズアクセスモデル
- [ランディングゾーン](../../governance/landing-zone/) — 顧客のクラウド基盤構造の理解

### 構築と運用

FDEがプロダクションコードを所有するなら、運用についても知っておく必要があります。

- [DevOps入門](../../devops/getting-started/) — CI/CD、自動化
- [モニタリング](../../devops/monitoring/) → [オブザーバビリティ](../../devops/observability/) — 顧客環境のデバッグ
- [SLI/SLO](../../devops/slo/) — 成功指標の定義
- [災害復旧](../../governance/dr/) — 顧客環境の障害対応
- [セキュリティインシデント対応](../../security/incident-response/) — インシデント時の顧客との協業

### データと統合

顧客のデータを理解し、連携させることがFDE業務の中核です。

- [データベース運用](../../database/operations/) — 顧客DBへのアクセスと連携
- [データベースマイグレーション](../../database/migration/) — データ移行

### AI/エージェントデプロイ

2025-2026年のFDE需要急増の直接的な原因です。

- [AI入門](../../ai/getting-started/) — AI製品の理解
- [RAG高度なパターン](../../ai/rag-patterns/) — 顧客データに基づくRAG構築
- [AIエージェント](../../ai/agents/) — エージェンティックワークフローのデプロイ
- [LLMOps](../../ai/llmops/) — 評価、コスト、運用、**エージェント観測**
- [AIセキュリティ](../../security/ai-security/) — ガードレール、プロンプトインジェクション対策

---

## FDEの技術スタック

顧客環境はそれぞれ異なりますが、FDEが共通して扱うツールです。

| カテゴリ | ツール |
| --- | --- |
| 言語 | Python, TypeScript, SQL, Go/Java, Bash |
| バックエンド | FastAPI, NestJS, Spring Boot |
| フロントエンド | React, Next.js（運用ダッシュボード、顧客ポータル） |
| データ | PostgreSQL, Spark, dbt, Airflow, Kafka |
| クラウド | AWS, Azure, GCP（EC2, K8s, Lambda, S3など） |
| コンテナ | Docker, Kubernetes, Helm |
| IaC | Terraform, Pulumi, CloudFormation |
| CI/CD | GitHub Actions, GitLab CI, Argo CD |
| 観測 | Datadog, Grafana, Prometheus, Sentry |
| AI/エージェント | LangGraph, CrewAI, Semantic Kernel, ベクトルDB |

---

## エージェンティックデリバリーへの転換

2026年現在、FDEの働き方が変化しています。

**これまで**: 現場で直接グルーコードを作成、手動統合、数週間～数か月を要する

**現在**: 少人数の人間チーム + AIエージェントの組み合わせ
- エージェントがスキャフォールディング、評価（eval）、長期ワークフローを実行
- 人間（FDE）はディスカバリー、ガバナンス、ゴーライブ（go-live）判断に集中
- AWS AI-Driven Development Lifecycleがこのパターンを公式化

**変わらないもの**: 顧客環境の曖昧さの解消、ステークホルダーの説得、プロダクション所有権 — これらは自動化されません。

---

## キャリアの視点

| 経路 | 説明 |
| --- | --- |
| ICトラック | FDE → Senior → Staff/Principal FDE |
| 製品転換 | 現場フィードバック → PM/TPM（製品ギャップを最もよく知る人） |
| GTMリーダーシップ | 技術営業/デプロイ組織のリード |
| 起業 | Palantir FDE出身の創業者多数 — 顧客の課題を最も深く理解できる立場 |

---

## 参考資料

- [Palantir Forward Deployed Engineeringモデル](https://fde.academy/blog/how-palantir-invented-the-forward-deployed-engineer-model)
- [Pragmatic Engineer: Forward Deployed Engineers](https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers)
- [FDE vs Solutions Architect (2026)](https://fde.academy/blog/forward-deployed-engineer-vs-solutions-architect)
- [Forbes: AI Giants Bet Billions On FDE (2026)](https://www.forbes.com/sites/janakirammsv/2026/05/28/ai-giants-bet-billions-on-the-most-expensive-job-in-enterprise/)
- [AWS Forward Deployed Engineering発表](https://www.aboutamazon.com/news/aws/aws-1-billion-forward-deployed-ai-engineers)
