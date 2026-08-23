---
title: "クラウド管理ツール（コンソール、CLI、SDK）"
description: "コンソール、CLI、SDK、Cloud Shellの役割とIaCとの関係をベンダー別に比較します。"
---

> 文書基準: 2026年5月

## クラウドを扱う3つの方法

オンプレミス環境でサーバーを管理する方法を思い浮かべてみましょう。サーバールームに直接行ってモニターとキーボードで作業したり、SSHでリモート接続したり、自動化スクリプトを通じてAPIを呼び出したりすることができます。クラウドでも同じ3つのアプローチがあります。

- **コンソール（Web UI）** — サーバールームに直接行って作業することに似ています。視覚的にリソースを確認・管理でき、最初に学習するときや現状を把握するときに役立ちます。
- **CLI（Command Line Interface）** — SSHでリモート接続してコマンドで作業することに似ています。反復作業をスクリプトで自動化でき、運用業務に適しています。
- **SDK（Software Development Kit）** — アプリケーションコードからAPIを呼び出すことに似ています。プログラミング言語でクラウドリソースを制御でき、アプリケーション統合に適しています。

実務ではこの3つを状況に応じて組み合わせて使用します。コンソールで現状を確認し、CLIで反復作業を自動化し、SDKでアプリケーションにクラウドサービスを統合するのが一般的です。

## コンソール（Web UI）

各ベンダーは、Webブラウザからクラウドリソースを管理できるコンソールを提供しています。

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **名称** | AWS Management Console | Azure Portal | Google Cloud Console | OCI Console |
| **URL** | [console.aws.amazon.com](https://console.aws.amazon.com) | [portal.azure.com](https://portal.azure.com) | [console.cloud.google.com](https://console.cloud.google.com) | [cloud.oracle.com](https://cloud.oracle.com) |
| **コンソール現地言語** | 主要言語に対応 | 主要言語に対応 | 言語により差あり | 言語により差あり |
| **モバイルアプリ** | AWS Console Mobile App | Azure Mobile App | Google Cloud App | OCI Mobile App |
| **特徴** | サービス別独立コンソール、リージョン選択必須 | 統合ダッシュボード、リソースグループ中心 | プロジェクト中心、検索機能が強力 | Compartment中心、シンプルなUI |

### コンソール使用時の注意点

- **リージョン確認** — AWSとGoogle Cloudはコンソールでリージョンを明示的に選択する必要があります。誤ったリージョンでリソースを作成してしまうミスがよく発生します。
- **本番環境の変更は控える** — コンソールでの手動変更は追跡が困難で再現できません。本番環境はCLIまたはIaCで管理することを推奨します。

:::caution
コンソールで本番環境を直接変更すると、変更履歴が残らず再現も不可能になります。**IaCパイプラインを通じた変更**を原則とし、コンソールは現状確認と緊急対応のみに使用してください。
:::

## CLI（Command Line Interface）

各ベンダーは、ターミナルからクラウドリソースを管理できるCLIツールを提供しています。

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **CLI名称** | AWS CLI（`aws`） | Azure CLI（`az`） | Google Cloud CLI（`gcloud`） | OCI CLI（`oci`） |
| **追加CLI** | — | Azure PowerShell | — | — |
| **インストール** | [インストールガイド](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html) | [インストールガイド](https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli) | [インストールガイド](https://cloud.google.com/sdk/docs/install) | [インストールガイド](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) |
| **認証** | `aws login`（ブラウザ認証、CLI v2.32+） | `az login`（ブラウザ認証） | `gcloud auth login`（ブラウザ認証） | `oci session authenticate`（ブラウザ認証） |
| **出力形式** | JSON、YAML、Table、Text | JSON、YAML、Table、TSV | JSON、YAML、Table、CSV | JSON、Table |

### 基本使用例

```bash
# AWS — EC2インスタンス一覧の取得
aws ec2 describe-instances --region us-east-1

# Azure — VM一覧の取得
az vm list --resource-group my-rg --output table

# Google Cloud — Compute Engineインスタンス一覧の取得
gcloud compute instances list --project my-project

# OCI — Computeインスタンス一覧の取得
oci compute instance list --compartment-id <compartment-ocid>
```

AzureはCLIのほかに**Azure PowerShell**も提供しています。Windows環境で主にPowerShellを使用している組織であれば、Azure PowerShellの方が馴染みやすいかもしれません。

## SDK（Software Development Kit）

各ベンダーは主要プログラミング言語向けのSDKを提供しており、アプリケーションコードから直接クラウドサービスを呼び出すことができます。

| 言語 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Python** | Boto3 | azure-sdk-for-python | google-cloud-python | oci-python-sdk |
| **JavaScript/TypeScript** | AWS SDK for JavaScript | azure-sdk-for-js | google-cloud-node | oci-typescript-sdk |
| **Java** | AWS SDK for Java | azure-sdk-for-java | google-cloud-java | oci-java-sdk |
| **Go** | AWS SDK for Go | azure-sdk-for-go | google-cloud-go | oci-go-sdk |
| **.NET (C#)** | AWS SDK for .NET | Azure SDK for .NET | Google Cloud .NET | oci-dotnet-sdk |
| **インストールドキュメント** | [AWS SDKガイド](https://docs.aws.amazon.com/ko_kr/sdkref/latest/guide/overview.html) | [Azure SDKガイド](https://learn.microsoft.com/ko-kr/azure/developer/) | [Cloud Client Libraries](https://cloud.google.com/apis/docs/cloud-client-libraries) | [OCI SDKガイド](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdks.htm) |

SDKはCLIと異なりアプリケーションコードに直接統合されるため、エラー処理、リトライロジック、非同期呼び出しなどをプログラミング言語の機能を活用して実装できます。

## Cloud Shell

各ベンダーとも、ブラウザからすぐにCLIを使用できる**Cloud Shell**を提供しています。別途インストールなしでWebブラウザのみでCLI作業が可能なため、素早いテストや緊急対応の際に便利です。

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **名称** | AWS CloudShell | Azure Cloud Shell | Google Cloud Shell | OCI Cloud Shell |
| **事前インストールツール** | AWS CLI、Python、Node.js、Gitなど | Azure CLI、PowerShell、Terraformなど | gcloud、kubectl、Terraform、Pythonなど | OCI CLI、Python、Terraformなど |
| **ストレージ** | リージョンごとに1GB | 5GB（Azure Files） | 5GB（ホームディレクトリ） | 5GB（ホームディレクトリ） |
| **料金** | 無料 | 無料（ストレージ費用は別途） | 無料 | 無料 |
| **エディタ** | 内蔵エディタ | Monacoエディタ（VS Codeベース） | Theiaエディタ（VS Codeベース） | 内蔵エディタ |

## コードで管理するインフラ（IaC）との関係

コンソール、CLI、SDKは、リソースを直接作成・管理する**命令型**（Imperative）方式です。「サーバーを作れ」「ネットワークを接続しろ」のように一段階ずつ指示します。

これと対比される**宣言型**（Declarative）方式が**IaC**です。「サーバー3台、ネットワーク1個があるべきだ」のように望ましい最終状態のみを定義すれば、ツールが現在の状態と比較して必要な変更を自動的に適用します。

| 方式 | 特徴 | ツール例 |
| --- | --- | --- |
| **命令型** | 順番に実行。素早いテスト、緊急対応に適する | CLIスクリプト、SDKコード |
| **宣言型** | 最終状態を定義。再現性、バージョン管理、チーム協業に適する | Terraform、CloudFormation、Bicep、CDK |

実務では、コンソールで現状を確認し、CLIで緊急対応を行い、**本番インフラはIaCで管理する**のが標準です。

:::note
IaCツールの比較、Terraformの状態管理、モジュール設計、ドリフト管理などの詳細は[コードで管理するインフラ（IaC）](../../devops/iac/)を参照してください。
:::

## よくある間違い

- **「コンソールで作れば終わりだ」** — コンソールで作成したリソースは履歴が残らず、再現と監査が不可能です。本番環境はIaCで管理する必要があります。
- **「CLIとSDKは同じものだ」** — CLIはターミナルで単発コマンドを実行するツールであり、SDKはアプリケーションコードに統合するライブラリです。用途が異なります。
- **「Cloud Shellならローカルインストールは不要だ」** — Cloud Shellは一時的な環境であり、セッション終了時に状態が初期化される場合があります。継続的な運用にはローカルCLIのインストールが必要です。

## チェックリスト

- [ ] CLI認証を、長期的な認証情報（アクセスキー）ではなくブラウザベースの一時認証に設定したか？
- [ ] 本番環境の変更をコンソールではなくIaCパイプラインを通じて行う原則を確立したか？
- [ ] 使用するベンダーのCLIをインストールし、基本コマンド（リソース照会）を実行してみたか？

## 参考資料

### AWS

- [AWS CLIインストールガイド](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html)
- [AWS SDKインストール（言語別）](https://docs.aws.amazon.com/ko_kr/sdkref/latest/guide/overview.html)
- [AWS CloudShellドキュメント](https://docs.aws.amazon.com/ko_kr/cloudshell/latest/userguide/)

### Azure

- [Azure CLIインストールガイド](https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli)
- [Azure SDKインストール（言語別）](https://learn.microsoft.com/ko-kr/azure/developer/)
- [Azure Cloud Shellドキュメント](https://learn.microsoft.com/ko-kr/azure/cloud-shell/overview)

### Google Cloud

- [Google Cloud CLIインストールガイド](https://cloud.google.com/sdk/docs/install)
- [Google Cloud Client Libraries（言語別）](https://cloud.google.com/apis/docs/cloud-client-libraries)
- [Google Cloud Shellドキュメント](https://cloud.google.com/shell/docs)

### OCI

- [OCI CLIインストールガイド](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- [OCI SDK](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdks.htm)
- [OCI Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro.htm)
