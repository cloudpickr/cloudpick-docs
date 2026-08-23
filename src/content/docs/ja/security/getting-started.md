---
title: "クラウドセキュリティを始める"
description: "クラウドセキュリティのアプローチと保護領域を構造化し、セキュリティセクションの読み方ガイドを提供します。"
---

> 文書基準: 2026年5月

## セキュリティは「何を保護するか」から

クラウドセキュリティの最初のステップは、ファイアウォールを設定することではありません。**資産識別 → 脅威モデリング → 保護優先順位**の順にアプローチする必要があります。

1. **資産識別** — 何を保護すべきか分からなければ、何を防ぐべきかも分かりません。
2. **データ分類** — 公開 / 内部 / 機密 / 極秘に等級を分け、各等級に応じた保護レベルを決定します。
3. **脅威モデリング** — 誰が、どの経路で、何を狙う可能性があるかを識別します。
4. **保護優先順位** — 最も大きな影響を与えうる脅威から対応します。

## クラウドセキュリティの視点の転換

オンプレミスとクラウドではセキュリティのアプローチが異なります。

| オンプレミス（従来型） | クラウド（現代型） |
| --- | --- |
| 境界防御（ファイアウォールで防ぐ） | ゼロトラスト（すべてのリクエストを検証） |
| 事前遮断中心 | 事後検知＋自動対応（監査ログ、異常検知） |
| 手動監査（四半期ごと） | 継続的監査（リアルタイムのコンプライアンス） |
| 静的ポリシー | Policy as Code（OPA、SCP、Azure Policy） |
| 変更管理委員会 | ガードレール＋自動遮断（予防的統制） |

:::note
核心メッセージ: まず無条件に遮断するのではなく、**監査（Audit）で確認し、ポリシー（Policy）で防ぎ、検知（Detection）で捕える**。
:::

## 保護領域の構造 — セキュリティセクションの読み方ガイド

クラウドセキュリティは複数のレイヤーで構成されます。各レイヤーに対応するCloudPickドキュメントをマッピングします。

| レイヤー | 役割 | CloudPickドキュメント |
| --- | --- | --- |
| ガバナンス＆ポリシー | 責任範囲、コンプライアンス | [責任共有モデル](../../about-cloud/shared-responsibility/)、[コンプライアンス](../../governance/compliance/) |
| アイデンティティ＆アクセス制御 | 誰が何をできるか | [IAM詳細](../../security/iam/)、[ゼロトラスト](../../security/zero-trust/) |
| ネットワークセキュリティ | トラフィックの隔離とフィルタリング | [VPC/サブネット](../../networking/vpc-subnet/) |
| データ保護 | 暗号化、鍵管理、DLP | [データ保護](../../security/data-protection/)、[シークレット管理](../../security/secrets/) |
| 検知＆対応 | 脅威検知、インシデント対応 | [セキュリティ態勢管理](../../security/security-posture/)、[インシデント対応](../../security/incident-response/) |
| DevSecOps | パイプラインセキュリティ | [DevSecOps](../../devops/devsecops/) |
| AIセキュリティ | モデル/データ保護 | [AIセキュリティ](../../security/ai-security/) |

## セキュリティ成熟度の段階

一度にすべてを適用しようとしないでください。段階的に成熟度を高めていきます。

| 段階 | 焦点 | 例 |
| --- | --- | --- |
| 1. 基本 | IAM最小権限、MFA、暗号化の基本 | ルートアカウントのロック、基本暗号化の有効化 |
| 2. 可視性 | ロギング、監査、資産インベントリ | CloudTrail、Config、Security Hubの有効化 |
| 3. 自動化 | Policy as Code、自動検知/遮断 | SCP、GuardDuty、自動隔離 |
| 4. 継続的 | レッドチーム、カオスセキュリティ、脅威インテリジェンス | 侵入テスト、脅威モデリングの定例化 |

## よくある間違い

- **セキュリティツールから導入し、資産識別を飛ばす** — 何を保護すべきか分からないままGuardDuty/Defenderを有効化すると、アラートが溜まるだけで優先順位を決められません
- **すべてを一度に適用しようとする** — セキュリティ成熟度の段階を無視してゼロトラストまで一気に導入しようとし、結局何も完成しません
- **監査ログを有効化せずに運用** — CloudTrail/Activity Logを有効化していないため、インシデント発生時に原因追跡が不可能になります

## チェックリスト

- [ ] 保護対象の資産を識別し、データ分類(公開/内部/機密/極秘)を完了したか
- [ ] 監査ログ(CloudTrail、Activity Log、Audit Log)をすべてのアカウントで有効化したか
- [ ] セキュリティ成熟度1段階目(IAM最小権限、MFA、基本暗号化)を先に完了したか

## 参考資料

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [Azure Security Documentation](https://learn.microsoft.com/azure/security/)
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
