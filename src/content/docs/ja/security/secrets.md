---
title: "シークレット管理"
description: "シークレット管理、KMS、証明書管理サービスをベンダー別に比較し、自動ローテーションと外部ツール連携について説明します。"
---

> 文書基準: 2026年5月

## 概要

アプリケーションはDBパスワード、APIキー、証明書などの機密情報(シークレット)を使用します。これらをソースコードや環境変数にハードコーディングすると、漏洩リスクが大きくなります。**シークレット管理サービス**は機密情報を暗号化して一元管理し、アプリケーションが実行時に安全に取得できるようにします。

### なぜ必要か

- **漏洩防止** — Gitにコミットされたパスワード、ログに露出したAPIキーなどの事故を防ぎます。
- **自動ローテーション** (Rotation) — パスワードを定期的に自動変更し、漏洩時の被害を最小化します。
- **監査** (Audit) — 誰がいつどのシークレットにアクセスしたかを記録します。
- **一元管理** — 複数のサービスが使用するシークレットを一箇所で管理します。

## 製品比較

### シークレット管理

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | Secrets Manager | 自動ローテーション(RDS、Redshiftなどネイティブ連携)。クロスアカウント共有 |
| AWS | SSM Parameter Store | シンプルなキー・バリュー保存。無料ティアあり。自動ローテーションは限定的 |
| Azure | Key Vault (Secrets) | シークレット＋鍵＋証明書の統合管理 |
| Google Cloud | Secret Manager | バージョン管理を内蔵。IAMでアクセス制御 |
| OCI | OCI Vault (Secrets) | シークレット保存＋バージョン管理。IAMポリシーでアクセス制御 |

### 暗号化鍵管理 (KMS)

シークレットを暗号化する鍵自体を管理するサービスです。

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | KMS (Key Management Service) | ベンダー管理鍵 / 顧客管理鍵(CMK) / BYOK |
| Azure | Key Vault (Keys) | HSM対応。Managed HSMで専用HSM |
| Google Cloud | Cloud KMS | HSM、外部鍵管理(EKM)対応 |
| OCI | OCI Vault (Keys) | ソフトウェア鍵 / HSM鍵。BYOK対応 |

### 証明書管理

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | ACM (Certificate Manager) | 無料の公的証明書発行。ALB/CloudFront自動連携 |
| Azure | App Service Certificates / Key Vault | Key Vaultで証明書のライフサイクル管理 |
| Google Cloud | Certificate Manager | 無料のマネージド証明書。Load Balancer自動連携 |
| OCI | OCI Certificates | 証明書発行およびライフサイクル管理。Load Balancer連携 |

## 主な違い

**AWS** — Secrets ManagerとParameter Storeの2つの選択肢があります。自動ローテーションが必要ならSecrets Manager、単純な設定値の保存であればParameter Store(無料)が適しています。

**Azure** — Key Vault一つでシークレット、暗号化鍵、証明書をすべて管理します。サービスが分かれていないため、管理がシンプルです。

**Google Cloud** — Secret Managerがバージョン管理を標準で提供しており、シークレットの変更履歴を追跡し、以前のバージョンへロールバックできます。

**OCI** — Vault一つでシークレットと暗号化鍵を統合管理し、HSM鍵とソフトウェア鍵を選択できます。IAMポリシーによってきめ細かなアクセス制御が可能です。

## 暗号化鍵管理モデル

暗号化鍵を誰が生成・管理するかによって、3つのモデルがあります。

| モデル | 説明 | 特徴 |
| --- | --- | --- |
| **ベンダー管理鍵 (Vendor-Managed)** | ベンダーが鍵の生成・管理・ローテーションを行う | デフォルト。ユーザー側の関与が最小限 |
| **顧客管理鍵 (CMK/CMEK)** | ユーザーがKMSで鍵を生成・管理 | 鍵ポリシー、ローテーション周期、アクセス制御をユーザーが直接管理 |
| **BYOK (Bring Your Own Key)** | ユーザーが外部で鍵を用意しKMSにアップロード | 鍵の原本を外部に保管。規制要件への対応 |
| **EKM/HYOK (External Key Management)** | 外部HSMに鍵を置き、KMSは参照のみ | 鍵がクラウドに保存されない。最も厳格な統制 |

:::note
規制産業(金融、医療、公共)ではCMKまたはBYOKが一般的であり、一般的なWebサービスではベンダー管理鍵で十分な場合が多いです。
:::

## シークレットの自動ローテーション (Rotation)

シークレットを定期的に自動変更することで、漏洩時の被害を最小化できます。

| ベンダー | 自動ローテーション対応 |
| --- | --- |
| AWS Secrets Manager | RDS、DocumentDB、Redshiftのネイティブローテーション。Lambdaでカスタムローテーション関数を作成可能 |
| Azure Key Vault | 証明書の自動更新。シークレットはEvent Grid + Function Appでローテーションを実装 |
| Google Cloud Secret Manager | シークレットのバージョン管理のみ提供。ローテーションロジックはCloud Scheduler + Cloud Functionで実装 |
| OCI Vault | Secret Rotation対応 (Autonomous DB、MySQLネイティブ)。Functionでカスタムローテーション |

### 外部シークレットストアとの連携

HashiCorp Vault、CyberArkなど外部のシークレット管理ソリューションを使用する場合、クラウドネイティブサービスと統合できます。

| 統合方式 | 説明 |
| --- | --- |
| **External Secrets Operator** | クラウドベンダーのシークレットストア(AWS Secrets Manager、Azure Key Vaultなど)のシークレットをKubernetes Secretへ自動同期 |
| **HashiCorp Vault Dynamic Secrets** | VaultがAWS IAM、DB認証情報を動的に生成 |
| **CSI Secret Store Driver** | Kubernetes Podにシークレットをファイルとしてマウント |

## 構成/プロパティ管理 (Configuration Management)

シークレット(パスワード、APIキー)とは異なり、**構成値**(feature flag、エンドポイントURL、タイムアウト値など)は機密ではありませんが、中央で管理し実行時に動的に変更する必要があります。各ベンダーはシークレット管理とは別に(または統合して)構成管理サービスを提供しています。

### シークレット vs 構成値

| 区分 | シークレット | 構成値 |
| --- | --- | --- |
| **例** | DBパスワード、APIキー、証明書 | Feature flag、エンドポイントURL、タイムアウト、環境別設定 |
| **暗号化** | 必須 (保存時＋転送時) | 任意 (機密性の高い設定は暗号化) |
| **アクセス制御** | 最小権限、監査必須 | チーム/サービス単位 |
| **ローテーション周期** | 定期的な自動ローテーションを推奨 | デプロイ/リリース時に変更 |
| **保存場所** | Secrets Manager / Key Vault | Parameter Store / App Configuration |

### ベンダー別構成管理サービス

| ベンダー | サービス | 特徴 |
| --- | --- | --- |
| AWS | [SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) | 階層型キー・バリュー保存。String/StringList/SecureStringタイプ。無料の標準ティア (10,000件)。高度なティアはポリシーベースの期限切れ/通知 |
| AWS | [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) | Feature flag＋構成デプロイ。段階的ロールアウト、検証後デプロイ、自動ロールバック |
| Azure | [Azure App Configuration](https://learn.microsoft.com/azure/azure-app-configuration/overview) | 中央構成ストア。Feature flagを内蔵。Key Vault参照でシークレット連携。ラベルで環境別に分離 |
| Google Cloud | [Runtime Configurator](https://cloud.google.com/deployment-manager/runtime-configurator) (レガシー) / [Firebase Remote Config](https://firebase.google.com/docs/remote-config) | Runtime Configuratorは制限的。サーバーアプリはSecret Managerに機密でない値も保存するパターンが一般的 |
| OCI | [OCI Resource Manager Variables](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/Concepts/resourcemanager.htm) / Vault | 専用の構成サービスなし。Vaultに機密でない値も保存するか、Object Storage＋アプリロジックで実装 |

### 実務パターン

- **環境別分離** — `dev/db-endpoint`、`prod/db-endpoint`のようにパスまたはラベルで環境を区別
- **Feature flag** — コードデプロイなしで機能をON/OFF。AWS AppConfig、Azure App Configurationがネイティブ対応
- **動的リロード** — 構成変更時にアプリケーションを再起動せずに反映。ポーリングまたはイベントベース
- **シークレット参照** — 構成サービスにシークレット値を直接保存せず、Secrets Manager/Key VaultのARN/URIを参照

:::note
**Google Cloud/OCIユーザー:** 専用の構成管理サービスが弱いため、Kubernetes ConfigMap＋External Secrets Operatorの組み合わせやHashiCorp Consulの利用を検討してください。マルチクラウド環境では、ベンダー中立な外部ツールが有利な場合があります。
:::

## よくある間違い

- **シークレットのハードコーディング** — ソースコードや設定ファイルにパスワードやAPIキーを直接記載すると、Git履歴に永久に残り漏洩リスクが大きくなります。
- **ローテーションなしで永続使用** — シークレットを一度生成した後にローテーションしないと、漏洩時の被害範囲が際限なく拡大します。
- **環境変数への直接保存** — シークレットを環境変数に平文で保存すると、プロセス一覧、ログ、クラッシュダンプに露出する可能性があります。シークレットストアから実行時に取得してください。

## チェックリスト

- [ ] すべてのシークレットを専用ストア(Secrets Manager、Key Vaultなど)で管理しているか
- [ ] 自動ローテーション(Rotation)を設定しているか
- [ ] pre-commit hookでシークレットのコミットを防止しているか (git-secrets、detect-secretsなど)
- [ ] シークレットアクセスの監査ログを有効化したか

## 参考資料

### AWS

- [AWS Secrets Manager ドキュメント](https://docs.aws.amazon.com/ko_kr/secretsmanager/)
- [AWS KMS ドキュメント](https://docs.aws.amazon.com/ko_kr/kms/)
- [AWS Certificate Manager ドキュメント](https://docs.aws.amazon.com/ko_kr/acm/)
- [SSM Parameter Store](https://docs.aws.amazon.com/ko_kr/systems-manager/latest/userguide/systems-manager-parameter-store.html)

### Azure

- [Azure Key Vault ドキュメント](https://learn.microsoft.com/ko-kr/azure/key-vault/)
- [Key Vault シークレット](https://learn.microsoft.com/ko-kr/azure/key-vault/secrets/)
- [Key Vault 証明書](https://learn.microsoft.com/ko-kr/azure/key-vault/certificates/)

### Google Cloud

- [Secret Manager ドキュメント](https://cloud.google.com/secret-manager/docs)
- [Cloud KMS ドキュメント](https://cloud.google.com/kms/docs)
- [Certificate Manager ドキュメント](https://cloud.google.com/certificate-manager/docs)

### OCI

- [OCI Vault ドキュメント](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/home.htm)
- [OCI Certificates ドキュメント](https://docs.oracle.com/en-us/iaas/Content/certificates/home.htm)
