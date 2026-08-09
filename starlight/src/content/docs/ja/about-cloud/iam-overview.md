---
title: "IAM概要"
description: "IAMの基本概念、認証方式、権限モデルをベンダー別に比較します。"
---

> 文書基準: 2026年5月

:::note
ID種別ごとの管理（人/デバイス/サードパーティ）、最小権限の実践、セキュリティ点検チェックリストなどの実務運用は、[IAM実践設計とセキュリティ運用](../../security/iam/)を参照してください。
:::

## なぜIAMが重要なのか

クラウドでは数百のサービスと数千のリソースがAPIでアクセス可能です。IAMの設定を誤ると、データ漏洩やリソース削除といったセキュリティインシデントにつながります。**最小権限の原則** — 必要な最小限の権限のみを付与することが基本原則です。

## 中核概念

- **ユーザー** (User) — 人またはアプリケーションを表すID
- **グループ** (Group) — ユーザーをまとめて権限を一括付与
- **ロール** (Role) — 一時的に付与できる権限セット。サービス間アクセスに主に使用
- **ポリシー** (Policy) — 「誰が、何を、どのリソースに」できるかを定義する文書
- **MFA** — パスワード以外の追加認証手段

## ベンダー別製品比較

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | IAM + IAM Identity Center | ユーザー、グループ、ロール、ポリシー。Identity Centerでマルチアカウントの SSO |
| Azure | Microsoft Entra ID（旧Azure AD） | ディレクトリサービス + RBAC。Microsoft 365と統合 |
| Google Cloud | Cloud IAM | プロジェクト/フォルダ/組織レベルのRBAC。サービスアカウントによるサービス間認証 |
| OCI | OCI IAM with Identity Domains | ユーザー、グループ、ポリシー、コンパートメントベースのアクセス制御 |

## 認証方式

| 方式 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **コンソールログイン** | ユーザー名 + パスワード + MFA | Entra IDアカウント + MFA | Googleアカウント + MFA | ユーザー名 + パスワード + MFA |
| **CLI/SDK** | Access Keyまたは`aws login` | `az login`（ブラウザ） | `gcloud auth login`（ブラウザ） | API Keyまたは`oci session authenticate` |
| **サービス間** | IAM Role（一時的な認証情報） | Managed Identity | Service Account | Instance Principal |
| **外部IdP連携** | SAML/OIDC Federation | Entra ID外部ID | Workforce Identity Federation | SAML/OIDC Federation |

## 権限管理モデル

| ベンダー | モデル | 特徴 |
| --- | --- | --- |
| **AWS** | ポリシーベース（JSON） | ID ベース + リソースベースのポリシーの組み合わせ。最も細かいが複雑 |
| **Azure** | RBAC（ロールベース） | 組み込み/カスタムロール。範囲（サブスクリプション/リソースグループ/リソース）指定。Conditional Accessによる動的制御 |
| **Google Cloud** | RBAC（ロールベース、階層継承） | 組織→フォルダ→プロジェクトの継承。Workload Identity Federationで外部トークンを直接使用 |
| **OCI** | ポリシーベース（HCL類似） | `Allow group X to manage Y in compartment Z`という直感的な構文。コンパートメント階層の継承 |

## 認証情報方式の比較

| ベンダー | 長期認証情報 | ロールベース（推奨） | フェデレーション |
| --- | --- | --- | --- |
| AWS | Access Key | IAM Role（Instance Profile, Task Role） | OIDC/SAML Federation |
| Azure | Service Principal Secret | Managed Identity | Entra External ID, Workload Identity Federation |
| Google Cloud | Service Account Key（JSON） | Attached Service Account | Workload Identity Federation |
| OCI | API Signing Key | Instance Principal | SAML/OIDC Federation |

## よくある間違い

- **「管理者権限を付与すれば楽だ」** — 利便性のために広範な権限を付与すると、インシデント発生時の被害範囲が拡大します。最小権限の原則を最初から適用してください。
- **「Access Keyをコードに入れても問題ない」** — 長期認証情報がソースコードや設定ファイルに露出すると、漏洩リスクが大きくなります。ロール（Role）ベースの一時認証情報を使用してください。
- **「IAMは一度設定すれば終わりだ」** — 人員の異動やサービスの変更に応じて権限を定期的に見直さないと、未使用の権限が蓄積されます。

## チェックリスト

- [ ] ルート/グローバル管理者アカウントにMFAを有効化し、日常業務に使用しないようにしているか?
- [ ] サービス間認証に長期認証情報の代わりにロール（Role/Managed Identity/Service Account）を使用しているか?
- [ ] ユーザーとグループに最小権限の原則を適用し、定期的な権限レビューのスケジュールを策定したか?

## 参考資料

### AWS

- [AWS IAMドキュメント](https://docs.aws.amazon.com/ko_kr/iam/)
- [IAM Identity Center](https://docs.aws.amazon.com/ko_kr/singlesignon/)

### Azure

- [Microsoft Entra IDドキュメント](https://learn.microsoft.com/ko-kr/entra/identity/)
- [Azure RBAC](https://learn.microsoft.com/ko-kr/azure/role-based-access-control/)

### Google Cloud

- [Cloud IAMドキュメント](https://cloud.google.com/iam/docs)

### OCI

- [OCI IAMドキュメント](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
