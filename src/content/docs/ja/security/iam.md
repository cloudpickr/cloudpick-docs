---
title: "IAM実務設計とセキュリティ運用"
description: "IAM実務設計、認証方式、権限モデル、最小権限ツール、長期認証情報のリスクをベンダー別に比較します。"
---

> 文書基準: 2026年8月

## 概要

本ドキュメントはIAMの**実務運用**に焦点を当てます — 認証情報の選択、ID種別ごとの適用、最小権限の実践、セキュリティ点検。

:::note
ベンダー別の製品比較、認証方式、権限モデルの概要は[IAM概要](../../about-cloud/iam-overview/)を参照してください。
:::

## 認証情報の種類

クラウドで認証する方法は大きく3つあります。**どのIDにどの認証情報を使うか**がセキュリティの要となります。

| 方式 | 特徴 | 適した対象 |
| --- | --- | --- |
| **長期認証情報** (Access Key, API Key) | 有効期限なし。漏洩時に即座に悪用され得る | ❌ 可能な限り使用しないこと |
| **ロールベースの一時認証情報** (IAM Role, Managed Identity) | 自動発行/失効。コードにシークレット不要 | ✅ デバイス/サービス (ワークロード) |
| **フェデレーション** (OIDC, SAML, Workload Identity) | 外部IdPトークンをクラウド権限に交換 | ✅ 人(SSO)、サードパーティ、CI/CD |

:::caution
**原則:** 人はSSO＋MFA＋フェデレーション、サービスはロールベースの一時認証情報、サードパーティはフェデレーション＋時間制限。長期キーは最後の手段です。
:::

:::danger
**長期キーが危険な理由:** Gitリポジトリ・ログ・環境変数に露出すると即座に悪用され得ます。退職者のキーが回収されないと、外部から継続的にアクセスされる可能性があります。ローテーションを自動化しないと、数年間同じキーが使用され続けます。
:::

:::tip
**ロールベース認証の利点:** トークンが自動発行/失効するため、漏洩時の被害が限定されます。コードにシークレットを組み込む必要がなく、ローテーションも自動で行われるため管理負担がありません。
:::

## ID種別ごとの適用

IAMで管理するIDは大きく3種類です。それぞれ作成/権限付与/回収の方法が異なります。

### 人(従業員/契約社員)

| ライフサイクル | やるべきこと | ベンダー別の方法 |
| --- | --- | --- |
| **入社** | アカウント作成＋グループ割り当て＋MFA強制 | AWS: Identity Centerでユーザー作成、または外部IdP(Okta、Microsoft Entra ID)連携。Azure: Entra IDユーザー作成。Google Cloud: Cloud IdentityまたはWorkspace。OCI: Identity Domainユーザー作成 |
| **部署異動** | 既存グループの削除＋新グループの割り当て | グループベースの権限であればグループのみ変更。個別ポリシーを付与していた場合は手動での整理が必要 |
| **退職** | アカウント無効化 → セッション無効化 → 一定期間後に削除 | 即座に削除すると監査追跡が不可能。無効化後90日間の保持を推奨 |
| **定期レビュー** | 未使用アカウント/過剰権限の検知 | AWS: Access Analyzer、Azure: Access Reviews、Google Cloud: IAM Recommender |

**実務原則:**
- 個別ユーザーに直接ポリシーを付与しないこと → **グループベース**の権限管理
- コンソールアクセスには**SSO＋MFA**必須
- 退職プロセスに「クラウドアカウントの無効化」をHRチェックリストに含める

### デバイス/サービス(ワークロード)

EC2、Lambda、コンテナ、CI/CDパイプラインなど**人ではないワークロード**に権限を付与する方法です。

| ベンダー | 推奨方式 | 説明 |
| --- | --- | --- |
| AWS | **IAM Role** (Instance Profile, Task Role, Execution Role) | EC2/ECS/Lambdaにロールを関連付けると、一時認証情報が自動的に注入される |
| Azure | **Managed Identity** (System-assigned / User-assigned) | VM/App Service/Functionに関連付け。トークンの自動発行/更新 |
| Google Cloud | **Attached Service Account** + Workload Identity | GKE PodにService Accountを関連付け。キーファイル不要 |
| OCI | **Instance Principal / Resource Principal** | Compute/Functionに動的グループマッチングで権限を付与 |

**絶対にしてはいけないこと:**
- Access Key/Service Account Keyを環境変数やコードにハードコーディング
- 1つのサービスアカウントを複数のワークロードで共有 (権限分離が不可能)

**すべきこと:**
- ワークロードごとに個別のロール/IDを作成 (最小権限の適用が可能)
- CI/CDパイプラインはOIDC Federationで一時認証情報を発行 (GitHub Actions → AWS Roleなど)

:::danger
**Azure MFA義務化フェーズ2 (2025年10月に施行完了、現在適用中):** MicrosoftはAzure CLI、Azure PowerShell、IaCツール(Terraform azurermなど)、ARM API呼び出し経路にもMFAを強制します。ユーザーアカウントで`az login`した後にTerraformを実行していたパイプラインは、**サービスプリンシパル(Service Principal) + Federated Credential**または**Managed Identity**へ移行する必要があります。未移行のパイプラインは認証失敗で停止します。詳細は[Microsoft公式ガイド](https://learn.microsoft.com/entra/identity/authentication/concept-mandatory-multifactor-authentication)を参照してください。
:::

### サードパーティ(外部パートナー/SaaS/ベンダー)

外部組織やSaaSサービスに自社のクラウドリソースへのアクセスを許可する必要がある場合です。

| シナリオ | 推奨方法 | 注意事項 |
| --- | --- | --- |
| **外部SaaSが自社のS3/Blobへアクセス** | Cross-account Role (AWS)、Service Principal + RBAC (Azure)、Workload Identity Federation (Google Cloud) | 外部アカウントIDを信頼ポリシーに明記。ワイルドカード(`*`)は禁止 |
| **パートナー企業のエンジニアがコンソールアクセス** | 専用ロールの作成＋時間制限＋MFA強制 | 常時アクセス禁止。JIT方式で必要時のみ有効化 |
| **監査/コンサルティング会社** | 読み取り専用ロール＋特定リソースのみ | アカウント全体の読み取り権限付与は禁止。必要なサービスのみ |
| **CI/CD外部サービス (GitHub Actionsなど)** | OIDC Federation (キーなしでトークン交換) | 長期キーの代わりにOIDCを使用。リポジトリ/ブランチ条件を制限 |

**ベンダー別の外部アクセスメカニズム:**

| ベンダー | クロスアカウント/テナント | 外部IdP連携 |
| --- | --- | --- |
| AWS | Cross-account IAM Role (信頼ポリシーに外部アカウントIDを指定) | OIDC/SAML Federation、IAM Identity Center |
| Azure | B2B Collaboration (Entra IDゲスト)、Lighthouse (MSP用) | Entra External ID、Workload Identity Federation |
| Google Cloud | Cross-project IAM binding、Workload Identity Pool | Workforce Identity Federation、Workload Identity Federation |
| OCI | Cross-tenancy Policy (`define tenancy`)、Identity Domain Federation | SAML/OIDC Federation |

:::caution
**サードパーティアクセスの核心原則:** 長期キーを共有しないこと。ロールベースの一時アクセス＋最小権限＋時間制限＋監査ログ。契約終了時には信頼関係を即座に削除。
:::

## 最小権限実践ツール

最小権限の原則を守るには、実際に使用されている権限を監視し、不要な権限を継続的に排除する必要があります。IAM異常行動の検知(異常なAPI呼び出しなど)は[セキュリティ態勢管理](../../security/security-posture/)の脅威検知サービスと連携します。

| ベンダー | 製品 | 機能 |
| --- | --- | --- |
| AWS | IAM Access Analyzer | 未使用ロール/権限の検知。CloudTrailベースの最小権限ポリシー自動生成 |
| AWS | CloudTrail | すべてのAPI呼び出しを記録。誰が何をしたかを監査 |
| Azure | Entra ID Governance (Access Reviews) | 定期的な権限レビューの自動化。過剰権限の検知 |
| Google Cloud | IAM Recommender | 未使用権限の検知＋縮小の推奨 |
| Google Cloud | Policy Analyzer | 誰がどのリソースにアクセス可能かを分析 |

### 実践ガイド

- 最初は広い権限で開始しますが、一定期間後は実際に使用された権限のみ残して縮小します。
- 定期的に(四半期ごとに)未使用のロールと権限をレビューします。
- サービス間のアクセスには、長期認証情報(Access Key)の代わりにロール(Role)/管理IDを使用します。

## マルチクラウド統合認証情報 (Identity Federation)

複数のクラウドを使用する際、各ベンダーに個別のアカウントを作成すると管理が分断されます。**1つのIdP(Identity Provider)ですべてのクラウドにSSO(Single Sign-On)を構成する**ことが、マルチクラウドIAMの出発点です。

| アプローチ | 説明 | ツール |
| --- | --- | --- |
| **中央IdP + Federation** | 1つのIdPで認証後、各クラウドにSAML/OIDCで連携 | Microsoft Entra ID、Okta、Google Workspace |
| **AWS Identity Center** | AWS専用SSO。外部IdP連携も可能 | AWS IAM Identity Center |
| **クロスクラウドワークロードID** | サービス間の認証を長期キーなしで処理 | OIDC Federation、Workload Identity |

:::note
マルチクラウド環境でIdPを統合しないと、アカウント管理の分断、退職者処理の漏れ、権限監査の不可能化などの問題が発生します。最初にすべきことは、**1つのIdPを定め、すべてのクラウドを連携させる**ことです。
:::

## IAMセキュリティ点検チェックリスト

- [ ] ルート/グローバル管理者アカウントにMFAを設定しているか
- [ ] 日常業務にルートアカウントを使用していないか
- [ ] 長期認証情報(Access Key)を使用しているサービスがないか (ロールベースへ移行)
- [ ] 90日以上未使用のアカウント/ロールを無効化したか
- [ ] 過剰な権限(AdministratorAccessなど)を持つユーザーがいないか
- [ ] サービス間のアクセスにロール/Managed Identity/Instance Principalを使用しているか
- [ ] 外部アクセス(サードパーティ)に時間制限と条件を設定しているか
- [ ] CloudTrail/Activity Log/Audit Logが有効化されているか
- [ ] 定期的(四半期ごと)な権限レビューを実施しているか
- [ ] 退職者アカウントの無効化がHRプロセスに含まれているか
- [ ] マルチクラウド使用時、中央IdPでSSOを構成しているか

## よくある間違い

- **個別ユーザーに直接ポリシーを付与** — グループベースの管理を行わないため、退職/異動時に権限整理が漏れ、過剰権限が蓄積する
- **CI/CDに長期Access Keyを使用** — OIDC Federationの代わりに長期キーをシークレットに保存し、漏洩時に即座に悪用される可能性がある
- **退職者アカウントを即座に削除** — 無効化せずすぐに削除し、監査追跡が不可能になる。無効化後90日間の保持を推奨

## 参考資料

### AWS

- [AWS IAM ドキュメント](https://docs.aws.amazon.com/ko_kr/iam/)
- [IAM Identity Center ドキュメント](https://docs.aws.amazon.com/ko_kr/singlesignon/)
- [IAM Access Analyzer](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [IAM ベストプラクティス](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/best-practices.html)
- [Well-Architected — 権限の継続的縮小](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_continuous_reduction.html)

### Azure

- [Microsoft Entra ID ドキュメント](https://learn.microsoft.com/ko-kr/entra/identity/)
- [Azure RBAC ドキュメント](https://learn.microsoft.com/ko-kr/azure/role-based-access-control/)
- [Entra ID Governance](https://learn.microsoft.com/ko-kr/entra/id-governance/)
- [Conditional Access](https://learn.microsoft.com/ko-kr/entra/identity/conditional-access/)

### Google Cloud

- [Cloud IAM ドキュメント](https://cloud.google.com/iam/docs)
- [IAM Recommender](https://cloud.google.com/iam/docs/recommender-overview)
- [Policy Analyzer](https://cloud.google.com/policy-intelligence/docs/analyze-iam-policies)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)

### OCI

- [OCI IAM ドキュメント](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
- [OCI Identity Domains](https://docs.oracle.com/en-us/iaas/Content/Identity/domains/overview.htm)
- [OCI ポリシー構文](https://docs.oracle.com/iaas/Content/Identity/policyreference/policyreference.htm)
