---
title: "コンプライアンス（Compliance）"
description: "ISO 27001、SOC 2など、グローバルクラウドのコンプライアンス認証とコンプライアンス運用方法をベンダー別に案内します。"
---

> 文書基準: 2026年8月

## 概要

クラウドにおけるコンプライアンスは、**共同責任モデル** に基づいてベンダーと利用者が責任を分担します。ベンダーはインフラ層のセキュリティ統制について認証を取得し、利用者は自身のワークロード構成が規制要件を満たすよう管理します。

:::note
共同責任モデルの概念的な背景は[共同責任モデル](../../about-cloud/shared-responsibility/)を参照してください。
:::

:::caution
**認証はあくまで前提条件であり、保証ではありません。** ベンダーが国内・国際認証を保有していても、利用者が構成したVPC、IAM、暗号化設定が規制要件を満たさなければ監査で問題になります。また、技術的なセキュリティだけでなく、組織の業務プロセス（収集・利用・破棄の手続き、変更管理、アクセス権限管理など）も審査対象です。
:::

## 国別コンプライアンス

国・地域ごとに公共調達認証、個人情報保護法、業界別規制が異なり、リージョン選択・データレジデンシー・分離レベルといったアーキテクチャ上の決定に直接影響します。国別の詳細は該当する国のドキュメントで扱います。

- **韓国** — ISMS-P、CSAP、金融業界規制（電子金融監督規定・網分離）: [韓国付録](../../korea/index/) · [コンプライアンス（韓国）](../../korea/governance/compliance/)
- **米国** — FedRAMP、HIPAA、ITAR/EAR: [米国概要](../../us/index/)
- **EU** — GDPR・データ主権、DORA、NIS2・EU AI Act: [EU概要](../../eu/index/)
- **日本** — ISMAP、APPI: [日本概要](../../japan/index/)
- **シンガポール** — MTCS、PDPA: [シンガポール概要](../../singapore/index/)

## 国際的な主要認証

### ISO/IEC 27001:2022 — 情報セキュリティマネジメントシステム

国際標準の情報セキュリティ管理体系です。ほとんどのグローバルCSPが基本として保有しています。**2022年改訂版**が現行の標準であり、以前の2013年版の認証書は2025年10月31日をもって失効しました。まだ2022年版へ移行していない組織は、新規認証（または移行再認証）を受ける必要があります。

主な変更点: 統制項目が114個から93個に再構成され、「脅威インテリジェンス」「クラウドサービスセキュリティ」「データマスキング」など11個の新規統制が追加されました。

- [AWS ISO 27001](https://aws.amazon.com/compliance/iso-27001-faqs/)
- [Azure ISO 27001](https://learn.microsoft.com/azure/compliance/offerings/offering-iso-27001)
- [Google Cloud ISO 27001](https://cloud.google.com/security/compliance/iso-27001)
- [Oracle ISO 27001](https://www.oracle.com/corporate/cloud-compliance/)

### ISO/IEC 42001 — AIマネジメントシステム

AIシステムの開発・運用に関する国際標準の管理体系認証です。責任あるAIガバナンスのためのフレームワークを提供します。

- OCI AIサービス（Enterprise AI、AI Services）が2026年6月にISO/IEC 42001認証を取得
- [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)

### SOC 1 / SOC 2 / SOC 3

AICPA（米国公認会計士協会）に基づく監査報告書です。エンタープライズ顧客からよく求められます。

- **SOC 1** — 財務報告に関する統制
- **SOC 2** — セキュリティ、可用性、処理の完全性、機密性、プライバシー
- **SOC 3** — SOC 2の要約公開報告書

各ベンダーのSOC報告書は**機密資料**であるため、顧客契約後にAWS Artifact、Azure Service Trust Portalなどを通じてダウンロードします。

### 業界別規制

| 業界 | 主な規制 | 適用地域 | 備考 |
| --- | --- | --- | --- |
| **医療** | HIPAA、HITRUST | 米国 | |
| **カード決済** | PCI DSS v4.0.1 | グローバル | v4.0（2024年3月31日、従来のv3.2.1廃止）→ v4.0.1（2024年6月の正誤表）。2025年3月31日からv4.0の「将来日付」約50項目の義務化が完了 |
| **公共（米国）** | FedRAMP / FedRAMP 20x | 米国連邦 | 20x: 数か月単位の手動認可を、OSCALベースの機械可読エビデンス・自動検証中心に短縮する自動化優先プロセス（[fedramp.gov/20x](https://www.fedramp.gov/20x/)） |
| **公共（EU）** | C5（ドイツ）、ENS（スペイン）等 | EU | |
| **個人情報（EU）** | GDPR | EU | |
| **AI（EU）** | EU AI Act | EU | GPAI義務は2025年8月2日施行完了。高リスクAIは2026年8月2日適用。[EU AI Act全文](https://artificialintelligenceact.eu/) |
| **金融（EU）** | DORA | EU | 2025年1月17日適用開始。CTPP（Critical Third-Party Provider）指定手続きが進行中。[詳細](../../governance/landing-zone/) |

各ベンダーの該当認証状況は、**AWS Compliance Programs**、**Azure Trust Center**、**Google Cloud Compliance**、**Oracle Cloud Compliance**の各ページで確認します。

## ベンダー別コンプライアンスハブ

認証状況の全リストとレポートへのアクセス方法は、各ベンダーの公式ハブで管理されています。

| ベンダー | ハブ |
| --- | --- |
| AWS | [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)、[AWS Artifact（レポート）](https://aws.amazon.com/artifact/) |
| Azure | [Microsoft Trust Center](https://www.microsoft.com/trust-center)、[Service Trust Portal](https://servicetrust.microsoft.com/) |
| Google Cloud | [Google Cloud Compliance Resource Center](https://cloud.google.com/security/compliance)、[Google Compliance Reports Manager](https://cloud.google.com/security/compliance/compliance-reports-manager) |
| OCI | [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/) |

## クラウドにおけるコンプライアンス運用の実際

認証そのものよりも、**日常運用でどのように統制を維持するか**が監査の核心です。

### 1. ガードレールの自動化

手動管理では漏れが発生するため、ポリシーをIaCとしてコード化します。

| ベンダー | ツール |
| --- | --- |
| AWS | [AWS Config](https://aws.amazon.com/config/)、[AWS Security Hub](https://aws.amazon.com/security-hub/)、SCP（Service Control Policy） |
| Azure | [Azure Policy](https://learn.microsoft.com/azure/governance/policy/overview)、[Microsoft Defender for Cloud](https://azure.microsoft.com/products/defender-for-cloud) |
| Google Cloud | [Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/overview)、[Security Command Center](https://cloud.google.com/security-command-center) |
| OCI | [OCI Security Zones](https://docs.oracle.com/en-us/iaas/Content/security-zone/home.htm)、[OCI Cloud Guard](https://docs.oracle.com/en-us/iaas/cloud-guard/home.htm) |

### 2. 監査証跡

すべての変更を監査ログとして残し、中央リポジトリに長期保管します。

| ベンダー | 監査ログ |
| --- | --- |
| AWS | [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) |
| Azure | [Azure Monitor Activity Log](https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log) |
| Google Cloud | [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit) |
| OCI | [OCI Audit](https://docs.oracle.com/en-us/iaas/Content/Audit/Concepts/auditoverview.htm) |

### 3. アクセス統制と最小権限

最小権限の原則、MFA、鍵のローテーションは[IAMとアクセス制御](../../security/iam/)で扱います。

### 4. データ保護

:::note
保存時/転送時の暗号化、鍵管理、データ主権については[データ保護とワークロードセキュリティ](../../security/data-protection/)を参照してください。
:::

### 5. 継続的モニタリング

監査の時点だけ統制を合わせるのではなく、常時検知体制を運用します。主要ベンダーはいずれも**コンプライアンスダッシュボード**を提供しています。

- AWS Security Hub — CIS Benchmark、NIST、PCI DSSの自動検査。[セキュリティ態勢管理](../../security/security-posture/)で詳しく扱います
- Azure Defender for Cloud — Secure Score + コンプライアンス標準の自動評価
- Google Cloud Security Command Center — コンプライアンスフレームワークのマッピング
- OCI Cloud Guard — 構成ミスの自動検知

## 読者のためのチェックリスト

マルチクラウド環境でコンプライアンスを検討する際に確認すべき事項:

- [ ] 処理・保存するデータの**機微度分類**は完了しているか？（個人情報、金融情報、機密情報など）
- [ ] 当該データに適用される**法的要件**を把握しているか？（国内法＋海外法）
- [ ] 利用しようとするベンダーが、必要な**認証を該当リージョンで保有**しているか？
- [ ] 共同責任モデルにおける**利用者責任範囲**を明確に定義したか？
- [ ] 監査ログ、アクセス統制、暗号化など**日常運用統制**を自動化したか？
- [ ] マルチクラウド環境で**統合監査**が可能か？（個別ベンダーダッシュボードの分散に注意）

## 継続的に行うべきこと

- **認証更新周期の管理** — ISMS-Pは3年有効/年1回のフォローアップ審査、ISO 27001は3年周期/年1回のサーベイランス審査です。更新スケジュールをカレンダーに登録しましょう。
- **継続的コンプライアンス（Continuous Compliance）** — 手動点検の代わりに、AWS Config、Azure Policy、Google Cloud Organization Policyでポリシー違反をリアルタイムに検知します。
- **ポリシードリフトの検知** — IaCと実際の環境の差異を定期的に確認し、コンプライアンス状態を維持します。

## よくある間違い

- **ベンダー認証だけを信頼し、利用者責任範囲を放置する** — ベンダーがISMS-Pを保有していても、VPC、IAM、暗号化設定は利用者の責任のため監査で指摘される
- **監査の時点だけ統制を合わせ、普段はドリフトを放置する** — 年1回の審査直前だけ整理すると、日常運用での規定違反が積み重なる
- **データ分類をせず、すべてのデータに同一のセキュリティレベルを適用する** — 過剰保護でコストが急増するか、過小保護で規制違反が発生する

## チェックリスト

- [ ] 処理・保存するデータの機微度分類（個人情報、金融情報、機密情報）を完了したか
- [ ] AWS Config、Azure Policyなどでポリシー違反をリアルタイムに検知する継続的コンプライアンス体制を運用しているか
- [ ] 認証更新スケジュール（ISMS-Pフォローアップ審査、ISO 27001サーベイランス審査）をカレンダーに登録し管理しているか

## 参考資料

### 韓国の機関

- [KISA 認証・認定](https://isms.kisa.or.kr/)
- [個人情報保護委員会](https://www.pipc.go.kr/)
- [金融保安院](https://www.fsec.or.kr/)

### AWS

- [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)
- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- [AWS CSAP](https://aws.amazon.com/compliance/csap/)
- [AWS Artifact](https://aws.amazon.com/artifact/)

### Azure

- [Microsoft Trust Center](https://www.microsoft.com/trust-center)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms)
- [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap)
- [Azure Compliance Offerings](https://learn.microsoft.com/azure/compliance/)

### Google Cloud

- [Google Cloud Compliance Resource Center](https://cloud.google.com/security/compliance)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
- [Google Compliance Reports Manager](https://cloud.google.com/security/compliance/compliance-reports-manager)

### OCI

- [Oracle Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)
- [OCI Security Guide](https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm)

### 国際標準

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001)
- [ISO/IEC 42001](https://www.iso.org/standard/81230.html) — AIマネジメントシステム
- [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [EU AI Act全文](https://artificialintelligenceact.eu/)
- [EU DORA](https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en)
- [PCI DSS v4.0.1](https://www.pcisecuritystandards.org/)
- [FedRAMP 20x](https://www.fedramp.gov/20x/)
