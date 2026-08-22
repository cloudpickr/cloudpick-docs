---
title: "技術サポートとアドバイザー"
description: "CSP技術サポートプラン、MSPパートナーの役割、アドバイザーサービス、応答時間SLAをベンダー別に比較します。"
---

> 文書基準: 2026年5月

## 概要

クラウド運用中に障害、アーキテクチャに関する問い合わせ、コスト最適化のアドバイスが必要な場合、ベンダーの技術サポートを受けることができます。サポートには大きく**CSP(クラウドベンダー)直接サポート**と**MSP(パートナー)サポート**の2つの経路があります。

## CSP技術サポートプラン

各ベンダーはいずれも無料の基本サポートに加えて有料プランを提供しており、プランに応じて応答時間、サポート範囲、専任担当者(TAM)の配置が異なります。

| ベンダー | プラン体系 | 備考 |
| --- | --- | --- |
| AWS | Basic → Business Support+ → Enterprise → Unified Operations | [2027年1月から新体系適用](https://aws.amazon.com/premiumsupport/plans/) |
| Azure | Basic → Developer → Standard → Professional Direct → Unified | |
| Google Cloud | Basic → Standard → Enhanced → Premium | |
| OCI | Basic → Paid (Premier) | Premierは専任CSMを配置 |

本番ワークロードを運用している場合は、有料プランへの加入を推奨します。障害発生時の応答時間が大きく変わるほか、アーキテクチャレビューやコスト最適化のアドバイスも受けられます。

### TAM (Technical Account Manager)

上位プランでは専任の技術アカウントマネージャー(TAM)が配置されます。TAMは単純な障害対応にとどまらず、組織のクラウド運用全般を継続的に支援する役割を担います。

**TAMが行うこと:**

- 定期的なアーキテクチャレビューおよび改善の提言
- コスト最適化分析および契約(コミットメント)戦略のアドバイス
- 障害発生時の内部エスカレーションおよび優先対応
- ベンダー内部のロードマップ共有および新規サービス導入支援
- 運用成熟度評価およびWell-Architectedレビュー

| ベンダー | TAM配置プラン | 名称 |
| --- | --- | --- |
| AWS | Enterprise / Unified Operations | Technical Account Manager |
| Azure | Unified(旧Premier) | Designated Support Engineer |
| Google Cloud | Premium | Technical Account Manager |
| OCI | Premier | Customer Success Manager (CSM) |

:::note
TAMはベンダー内部組織との連携チャネルとしての役割を果たします。大規模導入や規制市場への参入時にTAMがいれば、ベンダー内部のリソース(セキュリティチーム、コンプライアンスチーム、サービスチーム)に迅速にアクセスできます。
:::

### 応答時間SLA

有料プランの最も大きな違いは、障害発生時の応答時間です。

| 深刻度 | 説明 | AWS Business Support+ | Azure Professional Direct | Google Cloud Enhanced | OCI Premier |
| --- | --- | --- | --- | --- | --- |
| **重大 (Critical)** | 本番停止 | < 15分 | < 1時間 | < 1時間 | < 1時間 |
| **緊急 (Urgent)** | 本番の一部影響 | < 4時間 | < 4時間 | < 4時間 | < 2時間 |
| **通常 (Normal)** | 非本番影響 | < 12時間 | < 8時間 | < 8時間 | < 6時間 |
| **問い合わせ (Low)** | 一般的な質問 | < 24時間 | < 24時間 | < 24時間 | < 24時間 |

:::note
表の値はベンダー公式SLA基準であり、プラン・契約によって異なる場合があります。最新の数値は各ベンダーの公式Supportページでご確認ください。
:::

## アドバイザー/推奨事項サービス

各ベンダーは環境を自動的に分析し、コスト削減、セキュリティ強化、パフォーマンス改善を推奨するサービスを提供しています。

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | Trusted Advisor | コスト、セキュリティ、パフォーマンス、耐障害性、サービス制限のチェック。全項目チェックはBusiness Support以上で利用可能 |
| Azure | Azure Advisor | コスト、セキュリティ、信頼性、運用の卓越性、パフォーマンスに関する推奨事項。全プランで利用可能 |
| Google Cloud | Recommender / Active Assist | コスト、セキュリティ、パフォーマンス、管理効率性に関する推奨事項。全プランで利用可能 |
| OCI | Cloud Advisor | コスト最適化、セキュリティ、パフォーマンスに関する推奨事項。全テナンシーで利用可能 |

これらのサービスを定期的に確認し推奨事項を適用すれば、コストとセキュリティの両方を改善できます。

:::caution
一部の推奨事項は、有料サポートプランでのみすべて表示されます。例: AWS Trusted AdvisorはBasicプランではコアチェックのみを提供し、全項目チェック(コスト最適化など)はBusiness Support以上で有効化されます。
:::

## MSP (Managed Service Provider) パートナー

### CSPとMSPの役割の違い

| 項目 | CSP (ベンダー直接) | MSP (パートナー) |
| --- | --- | --- |
| **役割** | インフラ提供 + 技術サポート | 顧客環境の運用代行 + コンサルティング |
| **サポート範囲** | ベンダーサービスに限定 | アーキテクチャ設計、運用、コスト最適化、マイグレーションなど包括的 |
| **費用** | サポートプラン料金(使用量に比例) | 下記参照 |

### MSP費用構造

MSPは一般的に**クラウド使用料に対して追加マージンを取りません**。CSPがパートナーにリセール割引(Base Discount)を提供し、MSPはこの割引分を収益として得る構造です。そのため顧客の立場からは、MSP経由で支払ってもCSP直接支払いと同一または類似の価格になります。

追加費用が発生するケース:

- **マネージド運用サービス** — 24/7モニタリング、障害対応、パッチ管理など運用代行
- **コンサルティング** — アーキテクチャ設計、マイグレーション計画、コスト最適化プロジェクト
- **セキュリティ監視** — SOC運用、インシデント対応

### MSPを通じて追加でできること

- マルチクラウド統合管理(AWS + Azureなどを一つの窓口で)
- 韓国の税金計算書(税務証憑)発行、ウォン建て決済
- コストレポート、FinOpsコンサルティング
- 規制対応(韓国のCSAP認証、ISMS-P認証など)への支援

## コミュニティサポート

有料プランがなくても、コミュニティを通じて技術的な質問への回答を得ることができます。他のユーザーやベンダーの担当者が回答しており、一般的な使用方法やトラブルシューティングに役立ちます。ただし応答時間が保証されないため、本番障害対応には適していません。

| ベンダー | コミュニティ | 備考 |
| --- | --- | --- |
| AWS | [re:Post](https://repost.aws/) | Q&Aコミュニティ。未回答の質問はAWSエンジニアにエスカレーション |
| AWS | [re:Post Knowledge Center](https://repost.aws/knowledge-center) | よくある質問集 |
| Azure | [Microsoft Q&A](https://learn.microsoft.com/ko-kr/answers/) | 製品別Q&A |
| Azure | [Tech Community](https://techcommunity.microsoft.com/) | ブログ、フォーラム、イベント |
| Google Cloud | [Google Cloud Community](https://www.googlecloudcommunity.com/) | ディスカッションフォーラム |
| Google Cloud | [Stack Overflow (google-cloudタグ)](https://stackoverflow.com/questions/tagged/google-cloud-platform) | 開発関連Q&A |
| OCI | [Oracle Cloud Community](https://community.oracle.com/mosc/categories/oci) | Oracle公式フォーラム |
| AWS | [AWSKRUG](https://www.awskr.org/) | 韓国のAWSユーザーコミュニティ |
| Google Cloud | [GDG Cloud Korea](https://gdg.community.dev/gdg-cloud-korea/) | 韓国のGoogle Cloudユーザーコミュニティ |

:::note
上記のリストは代表的なコミュニティのみを選別したものです。この他にもベンダー別・トピック別・地域別のコミュニティが数多く存在します。
:::

## よくある間違い

- **「無料プランでも障害対応ができる」** — Basicプランには応答時間SLAがありません。本番障害時に数日間待たされる可能性があります。
- **「サポートプランさえあればすべての問題を解決してくれる」** — CSPサポートは自社サービスの範囲に限定されます。アーキテクチャ設計や運用代行はMSPの領域です。
- **「コミュニティの回答を本番障害対応に使える」** — コミュニティは応答時間が保証されません。本番環境には有料サポートプランが必要です。

## チェックリスト

- [ ] 本番ワークロードの障害深刻度別に目標応答時間を定義し、それに合ったサポートプランを選択したか
- [ ] アドバイザーサービス(Trusted Advisor、Azure Advisorなど)の推奨事項を定期的に確認するプロセスがあるか
- [ ] MSPの必要性(運用代行、マルチクラウド統合管理、ウォン建て決済など)を検討したか

## 関連ドキュメント

- [Well-Architected Framework](../../about-cloud/well-architected/) — 運用の卓越性・信頼性の柱とサポート体系
- [クラウドを始める](../../about-cloud/getting-started/) — 導入初期に確認すべき運用準備
- [FinOps](../../governance/finops/) — サポートプラン・MSP費用をコストガバナンスに含める
- [モニタリング](../../devops/monitoring/) — 障害対応とサポートエスカレーションの連携

## 参考資料

### AWS

- [AWS Supportプラン](https://docs.aws.amazon.com/ko_kr/awssupport/latest/user/aws-support-plans.html)
- [AWS Trusted Advisor](https://docs.aws.amazon.com/ko_kr/awssupport/latest/user/trusted-advisor.html)
- [AWSパートナープログラム](https://aws.amazon.com/ko/partners/)

### Azure

- [Azureサポートプラン](https://learn.microsoft.com/ko-kr/azure/azure-portal/supportability/how-to-create-azure-support-request)
- [Azure Advisor](https://learn.microsoft.com/ko-kr/azure/advisor/)
- [Azureパートナー](https://partner.microsoft.com/ko-kr/)

### Google Cloud

- [Google Cloudサポート](https://cloud.google.com/support/docs)
- [Recommender](https://cloud.google.com/recommender/docs)
- [Google Cloudパートナー](https://cloud.google.com/find-a-partner)

### OCI

- [OCI Support](https://www.oracle.com/support/)
- [OCI Cloud Advisor](https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/Concepts/cloudadvisoroverview.htm)
- [OCIパートナー](https://www.oracle.com/kr/partnernetwork/)
