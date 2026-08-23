---
title: "リモートアクセス管理"
description: "SSH/RDPを使わずに安全にインスタンスへアクセスするマネージドサービスをベンダー別に比較します。"
---

> 文書基準: 2026年5月

## 概要

サーバーにアクセスする際、伝統的にSSH(Linux)やRDP(Windows)を使用します。しかし、パブリックIPの露出、SSHキー管理、セキュリティグループの開放といった問題があります。

クラウドベンダーは**エージェントベースまたはプロキシベース**のマネージドアクセスサービスを提供し、パブリックIPなしでもプライベートサブネットのインスタンスに安全にアクセスできるようにしています。

## 伝統的アクセス vs マネージドアクセス

| 項目 | 伝統的(SSH/RDP直接) | マネージドサービス |
| --- | --- | --- |
| **パブリックIP** | 必要(またはBastion Hostを別途運用) | 不要 |
| **ポート開放** | 22/3389のインバウンド許可が必要 | インバウンドルール不要 |
| **キー管理** | SSHキーの配布/交換を直接管理 | IAMベースの認証(キー不要) |
| **監査ログ** | 別途構成が必要 | セッションログの自動記録 |
| **ネットワーク経路** | インターネット → インスタンス | ベンダー内部チャネル(アウトバウンドのみ) |

## ベンダー別サービス比較

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **サービス名** | [Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) | [Azure Bastion](https://learn.microsoft.com/azure/bastion/bastion-overview) | [Identity-Aware Proxy (IAP)](https://cloud.google.com/iap/docs/using-tcp-forwarding) | [OCI Bastion](https://docs.oracle.com/en-us/iaas/Content/Bastion/home.htm) |
| **方式** | エージェントベース(SSM Agent) | プロキシベース(PaaS) | プロキシベース(TCPフォワーディング) | プロキシベース(マネージドBastion) |
| **パブリックIP必要** | 不要 | 不要 | 不要 | 不要 |
| **インバウンドポート** | 不要(アウトバウンド443のみ) | 不要 | 不要 | 不要 |
| **認証** | IAMポリシー | Entra ID + RBAC | IAM + IAPポリシー | IAMポリシー |
| **セッションログ** | S3/CloudWatch Logs | Azure Monitor | Cloud Audit Logs | OCI Logging |
| **ファイル転送** | 対応(S3経由またはポートフォワーディング) | ネイティブファイルアップロード | SCP over IAPトンネル | SSHトンネル経由 |
| **コスト** | 無料(SSM Agentが標準搭載) | SKU別の時間課金 | 無料(IAP自体) | 無料(セッション単位) |

## 主な違い

**AWS Systems Manager Session Manager** — EC2に標準インストールされたSSM Agentを通じて動作します。別途インフラをデプロイすることなくIAM権限のみで即座に利用でき、追加コストもありません。ポートフォワーディングでRDSなど他のリソースへのトンネリングも可能です。

**Azure Bastion** — VNetにデプロイするPaaSサービスで、ブラウザ(Azure Portal)から直接SSH/RDPセッションを開けます。別途クライアントのインストールは不要ですが、Bastionホスト自体に時間課金が発生します。

**Google Cloud Identity-Aware Proxy (IAP)** — Googleのゼロトラストアクセスモデルの一部です。TCPフォワーディングを通じてSSH/RDPだけでなく、任意のポートへのトンネルを作成できます。Webアプリケーションのアクセス制御にも同じIAPを使用します。

**OCI Bastion** — マネージドBastionサービスで、セッション作成時にTTL(最大3時間)を指定します。セッション満了後は自動的にクリーンアップされ、長期的なアクセス経路が残りません。

:::note
**VPN依存度の低減:** AWS Verified AccessがHTTP(S)に加えてTCP/SSH/RDP/DBプロトコルまで対応したことで、対応プロトコルについてはVPN依存度を大幅に減らせます。各ベンダーのZTNAサービス比較は[ゼロトラスト](../../security/zero-trust/)を参照してください。
:::

## 実務推奨事項

### アクセス頻度と運用成熟度

インスタンスへの直接アクセス(シェルログイン)の頻度は、運用成熟度の指標です。アクセスが頻繁であるほど自動化が不足しているシグナルです。

| 成熟度段階 | シェルアクセス頻度 | 特徴 |
| --- | --- | --- |
| **Level 1 — 手動運用** | 毎日、随時 | ログ確認・設定変更・デプロイを手動で実施。サーバーに常駐するパターン |
| **Level 2 — 部分自動化** | 週数回 | CI/CDでデプロイを自動化、モニタリングダッシュボードを構築。障害時のみアクセス |
| **Level 3 — 可観測性ベース** | 月数回 | ログ/メトリクス/トレースが中央化され、ほとんどコンソールで解決。例外的なデバッグのみアクセス |
| **Level 4 — Immutable/Serverless** | ほぼなし | インスタンスの置き換えで問題を解決。シェルアクセス自体がセキュリティイベントとみなされる |

シェルアクセスを減らすには、次を自動化する必要があります(目標: Level 3以上):

| シェルで行っていたこと | 代替方法 |
| --- | --- |
| ログ確認(`tail -f`) | [モニタリング](../../devops/monitoring/)の中央化(CloudWatch Logs / Azure Monitor / Cloud Logging) |
| 設定ファイルの修正 | [構成管理サービス](../../security/secrets/)(Parameter Store, App Configuration) + 動的リロード |
| パッケージのインストール/更新 | [Patch Manager](../../devops/patch-and-vulnerability/) + ゴールデンイメージパイプライン |
| サービスの再起動 | Run CommandまたはAuto Scalingのインスタンス置き換え |
| ディスク整理 | CloudWatch Agentアラート + 自動スクリプト(EventBridge → Lambda) |
| デバッグ(strace, tcpdump) | [可観測性](../../devops/observability/)ツールでほとんど解決。避けられない場合のみセッションアクセス |

:::note
「**サーバーに入る必要が生じたら、それは自動化の機会**」と捉えましょう。アクセスログを定期的にレビューして繰り返されるアクセス理由を把握し、その作業を自動化すればアクセス頻度は自然に減少します。
:::

### アクセス制御ポリシー設計

シェルアクセスを完全になくすことはできないため、**誰が、いつ、どのような条件で**アクセスできるかポリシーを設計します。

| ポリシー項目 | 推奨 |
| --- | --- |
| **常時アクセス権限** | 付与しない。Just-In-Time (JIT)方式で必要時にリクエスト → 承認 → 時間制限付き付与 |
| **本番アクセス** | 最低2人承認(Dual Control)。セッション録画必須 |
| **開発/テストアクセス** | チーム単位で自律、ただしログ記録は必須 |
| **緊急アクセス(Break-glass)** | 事前定義された緊急ロール。事後監査必須。24時間以内の理由記録 |
| **アクセスレビュー** | 月1回のアクセスログレビュー。不要なアクセスパターンの識別 → 自動化 |

**JITアクセス実装例:**

- **AWS** — IAM Identity Center + Permission Set(時間制限)またはSSM Session Manager + 承認ワークフロー
- **Azure** — Privileged Identity Management (PIM) — ロール有効化時に承認 + TTL
- **Google Cloud** — PAM (Privileged Access Manager) — Just-In-Timeのアクセスリクエスト/承認
- **OCI** — OCI BastionセッションのTTL(最大3時間) + IAM動的グループ

### アクセス方式の選定基準

| 状況 | 推奨 |
| --- | --- |
| 日常的な運用(ログ確認、設定変更) | マネージドサービスを使用 |
| 緊急障害対応 | マネージドサービス + 事前権限設定(break-glass) |
| 大量サーバーへのコマンド実行 | AWS Run Command / Azure Run Command / Google Cloud OS Config |
| 開発/テスト環境への一時アクセス | IAPトンネルまたはSession Managerポートフォワーディング |
| 規定上SSHキーの使用が必須 | OCI Bastion(SSHキーベースのセッション) |

### セキュリティ強化のヒント

- **MFA強制** — セッション開始時にMFAを要求するようIAMポリシーを設定
- **セッション時間制限** — アイドルタイムアウトと最大セッション時間を設定
- **ログの中央化** — すべてのセッションログをSIEMに送信し、異常アクセスを検知
- **最小権限** — 特定のインスタンス/タグにのみアクセス可能となるようポリシー範囲を制限
- **ネットワーク分離** — マネージドサービスを使用してもプライベートサブネットを維持

### セッションログと監査証跡

シェルアクセスは、**誰が、いつ、どのインスタンスで、何を実行したか**を記録する必要があります。監査対応とインシデント分析の重要な証拠です。

**2つのレイヤーのログが必要です:**

1. **API/管理レイヤー** — 「セッションを開始/終了した行為」自体の記録(誰が、いつ、どこで)
2. **セッションレイヤー** — 「セッション内で実行したコマンドと出力」の記録(何をしたか)

| ベンダー | API/管理ログ | セッション内容ログ | 保存先 |
| --- | --- | --- | --- |
| AWS | **CloudTrail** (`StartSession`, `TerminateSession`, `SendCommand`) | Session Managerセッションロギング(コマンド入出力ストリーム) | CloudTrail → S3、セッションログ → S3/CloudWatch Logs |
| Azure | **Activity Log** (Bastion接続イベント) | Bastion診断ログ(接続メタデータ) | Log Analytics Workspace |
| Google Cloud | **Cloud Audit Logs** (IAPトンネル作成/終了) | OS Login監査ログ(メタデータのみ、コマンド内容は未記録) | Cloud Logging |
| OCI | **Audit Log** (Bastionセッション作成/満了) | OCI Logging(セッションメタデータ) | OCI Logging / Object Storage |

**CloudTrail連携(AWS例):**

CloudTrailはセッションアクセスの「管理行為」を自動的に記録します:

- `StartSession` — 誰がどのインスタンスにセッションを開いたか(ユーザーARN、インスタンスID、時刻)
- `TerminateSession` — セッション終了時点
- `SendCommand` (Run Command) — リモートコマンド実行記録(コマンド内容を含む)
- これらのイベントは[セキュリティポスチャー管理](../../security/security-posture/)のGuardDuty/Security Hubと連携し、異常パターンを自動検知できます

**ロギング設定チェックリスト:**

- [ ] API監査ログの有効化確認(CloudTrail/Activity Log/Audit Logs — ほとんどは標準で有効)
- [ ] セッション内容ロギングの有効化(AWS: Session Manager PreferencesでS3/CloudWatchを設定)
- [ ] コマンド入出力記録の有効化(AWSは既定で無効、明示的に有効化が必要)
- [ ] ログ保存期間の設定(コンプライアンス要件に応じて1年〜7年)
- [ ] ログの暗号化(KMS/Key Vaultで保存時暗号化)
- [ ] ログの改ざん防止(S3 Object Lock、Immutable Storageなど)
- [ ] SIEM連携(異常パターン検知: 異常な時間帯のアクセス、大量コマンド実行、未承認インスタンスへのアクセス)

:::caution
**AWS Session Managerは既定でコマンド入出力を記録しません。** Session Manager PreferencesでS3またはCloudWatch Logsへのロギングを明示的に有効化する必要があります。有効化しないと、CloudTrailには「誰が接続したか」のみが残り、「何をしたか」は残りません。
:::

## よくある間違い

- **SSHの22番ポートを0.0.0.0/0に開放** — ボットによる総当たり攻撃に即座に晒されます。マネージドアクセスサービスを使用すればインバウンドポートの開放は不要です。
- **共用SSHキーを複数のチームメンバーで共有** — 誰が接続したかの識別が不可能になります。IAMベースの認証で個人ごとのアクセスを追跡しましょう。
- **セッションロギングを有効化していない** — インシデント発生時に「誰が何をしたか」の証拠がありません。AWS Session Managerは既定で無効のため明示的に有効化する必要があります。

## チェックリスト

- [ ] 本番インスタンスにパブリックIPなしでマネージドサービス(Session Manager/Bastion/IAP)のみでアクセスしているか?
- [ ] 本番アクセス時にJIT(Just-In-Time)承認ワークフローが適用されているか?
- [ ] すべてのセッションのコマンド入出力がロギングされ、保存期間がコンプライアンス要件を満たしているか?

## 参考資料

### AWS

- [AWS Systems Manager Session Managerドキュメント](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [AWS Run Command](https://docs.aws.amazon.com/systems-manager/latest/userguide/execute-remote-commands.html)

### Azure

- [Azure Bastionドキュメント](https://learn.microsoft.com/azure/bastion/bastion-overview)
- [Azure Run Command](https://learn.microsoft.com/azure/virtual-machines/run-command-overview)

### Google Cloud

- [Google Cloud IAP TCPフォワーディングドキュメント](https://cloud.google.com/iap/docs/using-tcp-forwarding)

### OCI

- [OCI Bastionドキュメント](https://docs.oracle.com/en-us/iaas/Content/Bastion/home.htm)
- [OCI IAM動的グループとポリシー](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingdynamicgroups.htm)
