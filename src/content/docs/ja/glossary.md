---
title: "用語集"
description: "クラウドドキュメントに頻出する用語を、ベンダー中立の立場で整理します。"
---

> 文書基準: 2026年8月

クラウドドキュメントに頻出する用語を、ベンダー中立の立場で整理します。

## インフラの基本

| 用語 | 意味 |
| --- | --- |
| オンプレミス（On-Premises） | On-Premises。クラウドではなく、自社データセンターやオフィスで直接運用するインフラです。 |
| Region | 地理的に分離されたデータセンターのクラスターです。ソウル、東京、バージニアといった単位として理解できます。 |
| Availability Zone / Zone | 1つのリージョン内で独立して障害が分離されているデータセンター、またはデータセンターのグループです。AZと略して呼ばれます。 |
| CIDR | Classless Inter-Domain Routing。IPアドレスの範囲を表記する方式です。例: `10.0.0.0/16`は10.0.0.0〜10.0.255.255の範囲を意味します。 |
| Edge Location | 利用者に近い場所に配置された小規模インフラです。CDN、DNS、エッジセキュリティに主に使用されます。 |
| VPC / VNet / VCN | クラウド内に作成する、論理的に分離された仮想ネットワークです。 |
| Subnet | VPC内でIPアドレス帯をさらに小さく分割したネットワーク領域です。 |
| Load Balancer | 複数のサーバーにトラフィックを分散する装置またはサービスです。 |
| NAT Gateway | プライベートリソースがインターネットへ出られるようにしつつ、外部からの直接のアクセスは遮断するサービスです。 |
| Landing Zone | マルチアカウント/サブスクリプション/プロジェクト環境を安全かつ一貫して運用するための初期基盤構造です。 |

## コンピューティング

| 用語 | 意味 |
| --- | --- |
| Serverless | サーバー管理の負担を減らし、コードやコンテナの実行に集中できるようにする実行モデルです。 |
| Container | アプリケーションと実行環境を一緒にパッケージ化したデプロイ単位です。 |
| Kubernetes | コンテナのデプロイ、スケーリング、復旧を行うオーケストレーションプラットフォームです。 |
| イミュータブルインフラ（Immutable Infrastructure） | Immutable Infrastructure。実行中のサーバーを変更せず、新しいイメージに置き換える運用方式です。 |

## ストレージ

| 用語 | 意味 |
| --- | --- |
| Object Storage | ファイルをオブジェクト単位で保存するストレージです。画像、バックアップ、ログ、データレイクによく使用されます。 |
| Block Storage | VMにディスクのように接続して使用するストレージです。 |
| File Storage | 複数のサーバーが同じファイルシステムを共有できるようにするストレージです。 |

## セキュリティ

| 用語 | 意味 |
| --- | --- |
| IAM | Identity and Access Management。誰がどのリソースに対して何ができるかを管理する体系です。 |
| MFA | Multi-Factor Authentication。パスワード以外の追加認証手段を要求する方式です。 |
| Least Privilege | 最小権限の原則。必要最小限の権限のみを付与するセキュリティ原則です。 |
| JITアクセス（Just-In-Time Access） | Just-In-Time Access。常時権限の代わりに、必要な時にリクエスト→承認→時間制限付きで権限を付与するアクセス方式です。 |
| Zero Trust | 「決して信頼せず、常に検証せよ」というセキュリティモデルです。ネットワーク境界ではなく、IDとコンテキストに基づいてアクセスを制御します。 |
| 網分離（Network Segregation） | Network Segregation。業務ネットワークとインターネットを分離し、外部脅威が内部に到達するのを遮断する、韓国の主要なセキュリティ統制です。物理的分離と論理的分離（VPC分離等）で実装します。 |
| N2SF | 国家網セキュリティ体系。従来の一律的な網分離を、C（機密）/S（センシティブ）/O（公開）の等級別に差別化したセキュリティへ転換する、韓国のフレームワークです。2025年に韓国NCSC（国家サイバー安保センター）が1.0を公開しました。 |
| CSAP | クラウドセキュリティ認証制度。韓国の公共機関にクラウドを提供しようとするCSPが取得すべき認証です。上・中・下の3等級制で運用されます。 |
| SCP | Service Control Policy。AWS Organizationsでアカウントごとに許可/拒否するAPIを制限する予防的ガードレールです。Azure Policy、Google Cloud Organization Policyが同様の役割を果たします。 |
| ガードレール（Guardrail） | Guardrail。組織のポリシーを自動的に強制し、危険な設定や行為を事前に防ぐ予防的統制です。 |
| マイクロセグメンテーション（Microsegmentation） | Microsegmentation。ネットワークを細かく分割し、ワークロード間の通信を最小権限に制限する技法です。Zero Trustの中核的な実装手段です。 |
| ワークロードアイデンティティ（Workload Identity） | Workload Identity。人間ではなくアプリケーション/サービスに付与するIDです。長期的な認証情報なしにクラウドリソースへアクセスできるようにします。 |
| サービスアカウント（Service Account） | Service Account。人間ではなくアプリケーションや自動化プロセスが使用するアカウントです。 |
| 条件付きアクセス（Conditional Access） | Conditional Access。ユーザーの位置情報、デバイスの状態、時間などのコンテキストに応じてアクセスを許可/拒否するポリシーです。 |
| OIDC | OpenID Connect。OAuth 2.0の上に構築された認証プロトコルです。ユーザーの本人確認とSSOに使用されます。 |
| SAML | Security Assertion Markup Language。エンタープライズSSOに使用されるXMLベースの認証/認可標準です。 |
| 一時的な認証情報（Temporary Credentials） | Temporary Credentials。限られた時間のみ有効な認証情報です。STSトークン、セッショントークン等が該当します。同義語: 一時トークン。 |
| 長期的な認証情報（Long-term Credentials） | Long-term Credentials。有効期限なく有効な認証情報です。Access Key、API Key等が該当します。セキュリティ上、一時的な認証情報の使用が推奨されます。 |
| CSPM | Cloud Security Posture Management。クラウドの構成ミスを継続的に検知するセキュリティ管理体系です。 |
| CWPP | Cloud Workload Protection Platform。VM、コンテナ、サーバーレス等のワークロードのランタイムセキュリティを保護するプラットフォームです。 |
| SIEM | Security Information and Event Management。セキュリティイベントを収集・相関分析して脅威を検知するシステムです。 |
| SOAR | Security Orchestration, Automation and Response。セキュリティイベントへの自動対応をオーケストレーションするシステムです。 |
| CIS Benchmark | Center for Internet Securityが提供するセキュリティ構成のベースラインです。OS、クラウド、DB等さまざまな対象に対する標準を提供します。 |
| WAF | Web Application Firewall。WebアプリケーションをSQL Injection、XSS等のL7攻撃から保護するファイアウォールです。 |
| OWASP Top 10 | Webアプリケーションで最も一般的な10のセキュリティ脅威をまとめた業界標準のリストです。 |
| CVE | Common Vulnerabilities and Exposures。公開されたセキュリティ脆弱性に付与される一意の識別子です。 |
| CVSS | Common Vulnerability Scoring System。脆弱性の深刻度を0〜10のスコアで評価する標準です。 |
| SBOM | Software Bill of Materials。ソフトウェアに含まれるすべての構成要素（ライブラリ、パッケージ）の一覧です。 |

## DevOps / DevSecOps

| 用語 | 意味 |
| --- | --- |
| IaC | Infrastructure as Code。インフラをコードとして定義し、再現可能な形で管理する方式です。 |
| CI/CD | Continuous Integration / Continuous DeliveryまたはDeployment。ビルド、テスト、デプロイを自動化する方式です。 |
| Observability | オブザーバビリティ。ログ、メトリクス、トレースを通じてシステムの状態を把握する能力です。 |
| DevSecOps | セキュリティを開発（Dev）と運用（Ops）のパイプラインに最初から組み込むアプローチです。 |
| GitOps | Gitリポジトリを唯一の信頼できる情報源（Single Source of Truth）として使用し、インフラとアプリケーションのデプロイを自動化する運用方式です。 |
| シフトレフト（Shift-Left） | Shift-Left。セキュリティ検証を開発の初期段階へ移し、問題を早期に発見する原則です。 |
| SAST | Static Application Security Testing。ソースコードを実行せずに解析し、セキュリティ脆弱性を見つける手法です。 |
| DAST | Dynamic Application Security Testing。実行中のアプリケーションを外部から攻撃して脆弱性を見つける手法です。 |
| SCA | Software Composition Analysis。オープンソースの依存関係にある既知の脆弱性（CVE）とライセンス違反を検知する手法です。 |
| MLOps | MLモデルの学習/デプロイ/モニタリングを自動化・標準化する運用体系です。DevOpsのML版です。 |

## ガバナンス / FinOps

| 用語 | 意味 |
| --- | --- |
| CapEx | Capital Expenditure。資本的支出。サーバー・設備の購入のように初期に大きなコストを投資する方式です。 |
| OpEx | Operational Expenditure。運用支出。クラウドのように使った分だけコストを支払う方式です。 |
| FinOps | クラウドコストをエンジニアリング、財務、ビジネスの各チームが共同で管理する運用モデルです。 |
| ショーバック（Showback） | Showback。部門/チーム別のクラウド使用コストを見せるだけの方式です。実際の予算からは差し引かず、「自分たちのチームがいくら使っているか」という認識を共有します。 |
| チャージバック（Chargeback） | Chargeback。部門別のクラウド使用コストを、当該チームの実際の予算（P&L）から差し引く方式です。チームがコストに直接責任を負います。 |
| HA | High Availability。高可用性。単一障害点を排除し、サービス中断を最小化する設計です。Multi-AZ配置が代表例です。 |
| SLI | Service Level Indicator。サービスレベル指標。可用率、応答時間等の測定可能な指標です。 |
| SLO | Service Level Objective。サービスレベル目標。SLIの目標値です。例: 「月間可用率99.9%」。 |
| SLA | Service Level Agreement。サービスレベル契約。SLOを外部顧客との契約として約束したものです。違反時にはクレジット補償等が伴います。 |
| エラーバジェット（Error Budget） | Error Budget。SLOで許容される障害時間です。例: 99.9% SLOなら月43分がエラーバジェットです。 |
| RPO | Recovery Point Objective。障害時に許容できるデータ損失時間です。 |
| RTO | Recovery Time Objective。障害後にサービスを復旧すべき目標時間です。 |
| DR | Disaster Recovery。災害復旧。リージョン障害や大規模障害に備えた復旧戦略です。 |

## AI / 機械学習

| 用語 | 意味 |
| --- | --- |
| LLM | Large Language Model。大量のテキストで学習された大規模言語モデルです。GPT、Claude、Gemini等があります。 |
| Foundation Model | ファウンデーションモデル。大規模データで事前学習され、さまざまなタスクに汎用的に使えるAIモデルです。 |
| RAG | Retrieval-Augmented Generation。外部知識の検索結果をLLMの回答生成に併用するAIアーキテクチャです。 |
| Vector Store | テキストや画像の意味をベクトルとして保存し、類似度検索を提供するストレージです。 |
| Embedding | テキストや画像を意味ベースの数値配列（ベクトル）に変換したものです。類似度検索に使用されます。 |
| ANN | Approximate Nearest Neighbor。近似最近傍探索。ベクトル検索において速度のために精度を多少犠牲にするアルゴリズムです。 |
| Prompt | モデルに送る入力メッセージです。質問、指示、文脈を含みます。 |
| Prompt Engineering | モデルがより良い回答を生成できるよう、プロンプトを設計・改善する技法です。 |
| Token | モデルがテキストを処理する単位です。おおよそ単語1つが1〜2トークンで、ほとんどのAPIはトークン数に応じて課金されます。 |
| Fine-tuning | 事前学習済みのモデルを特定のデータで追加学習させ、ドメインに合わせて調整する技法です。 |
| Inference | 推論。学習済みのモデルが入力を受け取り出力を生成する過程です。学習より高速で低コストです。 |
| Hallucination | ハルシネーション（幻覚）。LLMが事実ではない内容をもっともらしく生成する現象です。RAG等で緩和します。 |
| Agent | エージェント。LLMがツールを呼び出したり複数の手順を実行したりして、タスクを自動化する仕組みです。 |
