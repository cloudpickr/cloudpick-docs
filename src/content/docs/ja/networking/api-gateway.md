---
title: "API Gateway"
description: "API Gatewayの役割、認証連携、デプロイ戦略をベンダー別に比較します。"
---

> 文書基準: 2026年8月

## 概要

バックエンドサービスを外部にAPIとして公開する際、認証、レート制限、リクエスト変換、モニタリングなどをサービスごとに実装すると重複が発生します。**API Gateway**は、こうした共通の関心事を一箇所で処理する入口(Front Door)の役割を果たします。

オンプレミスでリバースプロキシ(Nginx、HAProxy)に認証/ルーティングロジックを組み込んでいたのと似ていますが、クラウドのAPI Gatewayはマネージドでスケーリング、モニタリング、開発者ポータルまで統合的に提供します。

### 主な機能

- **認証/認可** — APIキー、OAuth、JWT、IAMベースのアクセス制御
- **レート制限** (Throttling) — 秒間リクエスト数の制限によるバックエンド保護
- **リクエスト/レスポンス変換** — ヘッダー追加、ボディマッピング、プロトコル変換
- **キャッシング** — 繰り返しリクエストへのレスポンスキャッシング
- **モニタリング** — リクエスト数、レイテンシ、エラー率の自動収集
- **開発者ポータル** — APIドキュメントの自動生成、キー発行

### 認証/認可連携

API Gateway自体は認証ロジックを処理せず、外部の認証サービスと連携します。

| ベンダー | 認証サービス | 備考 |
| --- | --- | --- |
| AWS | Cognito | ユーザープール + ソーシャルログイン。API Gatewayとネイティブ連携 |
| AWS | Lambda Authorizer | カスタム認証ロジックをLambdaで実装 |
| Azure | Entra ID(旧Azure AD) | OAuth 2.0 / OpenID Connect |
| Azure | APIM Policy (validate-jwt) | JWTトークン検証をポリシーとして設定 |
| Google Cloud | Firebase Auth / Identity Platform | ソーシャルログイン、多要素認証 |
| Google Cloud | Service Account + IAM | サービス間認証 |
| OCI | OCI IAM / Identity Domains | OAuth 2.0、JWT検証 |

### 追加機能

| 機能 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **利用プラン/クォータ** | Usage Plans + API Keys | Subscription + Quota Policy | Apigee Rate Limiting | Rate Limiting Policy |
| **リクエスト検証** | Request Validator(モデルスキーマ) | APIM Policy (validate-content) | Apigee OAS Validation | Request Validation Policy |
| **カスタムドメイン** | Custom Domain + ACM証明書 | Custom Domain + Managed Certificate | Custom Domain + SSL | Custom Domain + SSL証明書 |
| **WebSocket** | WebSocket API | —(SignalR別途) | —(Firebase Realtime別途) | — |
| **GraphQL** | AppSync | —(サードパーティ) | —(サードパーティ) | — |

## 製品比較

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | API Gateway (REST/HTTP/WebSocket) | Lambdaとネイティブ統合。サーバーレスAPI構成に最適 |
| AWS | AppSync | GraphQL専用。リアルタイムサブスクリプション対応 |
| Azure | API Management (APIM) | 開発者ポータル内蔵。マルチクラウド/ハイブリッドAPI統合。AI Gatewayティア（Public Preview、2026.06）でAIモデル・MCPサーバー専用ゲートウェイ提供 |
| Google Cloud | Apigee | エンタープライズAPI管理プラットフォーム。分析/収益化機能 |
| Google Cloud | API Gateway | 軽量。Cloud Functions/Cloud Run連携に適合 |
| OCI | OCI API Gateway | OCI Functions連携。認証、レート制限、リクエスト変換に対応 |

## 主な違い

**AWS API Gateway** — Lambdaとの統合が最も深く、サーバーレスバックエンドをAPIとして公開するのに最適化されています。用途別に3種類(REST API / HTTP API / WebSocket API)が分かれており、HTTP APIはREST API比で約1/3のコストです。ほとんどの新規プロジェクトはHTTP APIから始め、キャッシング・WAF・Usage Planが必要な場合にのみREST APIを選択します。

**Azure API Management** — 開発者ポータル、APIバージョン管理、ポリシーエンジンが内蔵されたフル機能プラットフォームです。単一サービスでREST、WebSocket、GraphQLすべてを処理します。オンプレミスAPIとクラウドAPIを1つのゲートウェイに統合できます。2026年6月にAI Gatewayティア（Public Preview）が追加され、AIモデルとMCPサーバーに特化した公開・セキュリティ・ガバナンス機能を提供します。v2ティア（Basic v2、Standard v2、Premium v2）がすべてGAとなり、柔軟な価格/性能選択が可能です。

**Google Cloud Apigee** — APIを製品として管理するエンタープライズプラットフォームです。単一サービスですべてのプロトコルを処理し、API利用状況分析、収益化(monetization)、パートナー管理機能が強みです。Gemini Code Assist統合による自然言語ベースのAPIスペック生成がGAとなり、API Hubを通じたエージェント登録・評価とGitベース同期をサポートします。

**OCI API Gateway** — OCI Functionsとネイティブ連携し、単一サービスで認証(JWT検証)、レート制限、リクエスト変換をポリシーベースで設定できます。

## APIデプロイ段階とバージョン管理

APIは本番にデプロイされると変更が難しいため、開発→ステージング→本番の段階的デプロイとバージョン管理が重要です。

| 機能 | AWS API Gateway | Azure APIM | Google Cloud Apigee | OCI API Gateway |
| --- | --- | --- | --- | --- |
| **Stage/Environment** | Stages (dev, staging, prod) | Environments | Environments (test, prod) | Deployments |
| **Canaryデプロイ** | Canary Deployment(重み付けベース) | Revision + Release | Revision + TargetServer | Route Rule(重み付け) |
| **バージョン管理** | API Version(v1、v2別エンドポイント) | API Revision + Version | API Revision + Version | Spec Version |
| **ロールバック** | 以前のDeploymentへ切り替え | Revision切り替え | Revision切り替え | 以前のDeploymentへ切り替え |

## 段階的デプロイ戦略

:::note
APIを外部に公開した後は、**後方互換性の維持**が重要です。既存の利用者がいるエンドポイントは削除したり応答形式を変更したりせず、新バージョン(`/v2`)を追加する方式で管理してください。
:::

| 戦略 | 説明 | ベンダー別実装 |
| --- | --- | --- |
| **Canary** | 新バージョンに少量のトラフィック(5〜10%)を送りモニタリング後に拡大 | AWS: API Gateway Canary Deployment(Stage重み付け)、Azure APIM: Revision + Traffic Split、Google Cloud Apigee: TargetServer重み付け |
| **Blue/Green** | 2つの環境を同時運用後にトラフィックを切り替え。即座にロールバック可能 | AWS: Stage切り替え、Azure APIM: Revision切り替え、Google Cloud: Revision切り替え |
| **バージョン分離** | `/v1`、`/v2`別エンドポイントで共存 | 全ベンダー対応。既存利用者への影響なく新バージョンを追加 |

:::caution
API Gateway自体のCanary機能は「ゲートウェイ設定変更」に対するCanaryです。バックエンドコードデプロイのCanaryは別途、Lambda Alias重み付け、ロードバランサーのTarget Group重み付け、またはサービスメッシュを使用する必要があります。
:::

## OpenAPI(Swagger)連携

オンプレミスでSwaggerによりAPIスペックを定義していたチームは、クラウドでも同じワークフローを維持できます。

- **Import**: OpenAPIスペックからAPI Gatewayを自動生成(AWS、Azure APIM、Apigeeすべて対応)
- **Export**: API GatewayからOpenAPIスペックを抽出してドキュメント化
- **IaC連携**: CloudFormation/TerraformでOpenAPIスペックをインラインで定義し、API構成をコードとして管理
- **開発者ポータル**: Azure APIM、ApigeeはOpenAPIスペックベースでインタラクティブなAPIドキュメントを自動生成

## APIテストツール

| ツール | 役割 | API Gatewayとの関係 |
| --- | --- | --- |
| Postman | API手動テスト、コレクション管理、環境変数 | Stage別URLを環境として管理、認証トークンの自動更新 |
| Swagger UI | OpenAPIスペックベースのインタラクティブドキュメント | API Gatewayからexportしたスペックで自動生成 |
| ベンダーコンソールテスト | AWSコンソールTestタブ、APIM Testタブ | デプロイ前の迅速な検証 |
| curl / httpie | CLIベースの迅速なテスト | CI/CDパイプラインでのスモークテスト |

クラウドAPIは認証フロー(OAuth、API Key、IAM Sig v4)が複雑で、環境(dev/staging/prod)別の切り替えが頻繁なため、Postmanのようなツールで環境変数と認証を体系的に管理することが効率的です。

## よくある間違い

- **REST APIとHTTP APIを区別せずREST APIで開始** — AWSではHTTP APIがコスト1/3で、ほとんどの要件を満たします。キャッシング・WAF・Usage Planが必要な場合にのみREST APIを選択してください。
- **APIバージョン管理なしに既存の応答形式を変更** — 既存の利用者(クライアント)が即座に壊れます。新バージョン(`/v2`)を追加し既存バージョンを維持してください。
- **API GatewayのCanaryをバックエンドコードデプロイのCanaryと誤解** — API Gateway Canaryはゲートウェイ設定変更に対するものです。バックエンドコードデプロイはLambda Alias重み付けやLB Target Groupで別途構成する必要があります。

## チェックリスト

- [ ] 認証/認可(API Key、JWT、IAM)がすべてのエンドポイントに適用されているか?
- [ ] レート制限(Throttling)が設定されバックエンドの過負荷を防いでいるか?
- [ ] OpenAPIスペックがIaCと同期され、API構成がコードとして管理されているか?

## 関連ドキュメント

- [ロードバランサー](../../networking/load-balancer/) — L4/L7トラフィック分散とAPI入口の役割分担
- [サーバーレス](../../compute/serverless/) — APIバックエンドとして関数・コンテナを接続
- [メッセージキューとイベントストリーミング](../../database/messaging/) — 非同期処理へのオフロード
- [ゼロトラスト](../../security/zero-trust/) — APIアクセス制御とID基盤の検証
- [シークレット管理](../../security/secrets/) — APIキー・トークンのライフサイクル

## 参考資料

### AWS

- [Amazon API Gatewayドキュメント](https://docs.aws.amazon.com/ko_kr/apigateway/)
- [API Gateway認証/認可](https://docs.aws.amazon.com/ko_kr/apigateway/latest/developerguide/apigateway-control-access-to-api.html)
- [Amazon Cognitoドキュメント](https://docs.aws.amazon.com/ko_kr/cognito/)
- [AWS AppSyncドキュメント](https://docs.aws.amazon.com/ko_kr/appsync/)

### Azure

- [Azure API Managementドキュメント](https://learn.microsoft.com/ko-kr/azure/api-management/)
- [APIM認証ポリシー](https://learn.microsoft.com/ko-kr/azure/api-management/authentication-authorization-overview)
- [Microsoft Entra IDドキュメント](https://learn.microsoft.com/ko-kr/entra/identity/)

### Google Cloud

- [Apigeeドキュメント](https://cloud.google.com/apigee/docs)
- [API Gatewayドキュメント](https://cloud.google.com/api-gateway/docs)
- [Firebase Authenticationドキュメント](https://firebase.google.com/docs/auth)
- [Identity Platformドキュメント](https://cloud.google.com/identity-platform/docs)

### OCI

- [OCI API Gatewayドキュメント](https://docs.oracle.com/en-us/iaas/Content/APIGateway/home.htm)
