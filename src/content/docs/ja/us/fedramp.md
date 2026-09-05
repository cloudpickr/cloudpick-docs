---
title: "FedRAMP"
description: "米国連邦機関のクラウド調達のためのセキュリティ認可制度FedRAMPの概要、2026年のFedRAMP 20x改編の現況、分離リージョン、CMMC・DoD SRGを整理します。"
---

> 文書基準: 2026年8月

## 概要

FedRAMP(Federal Risk and Authorization Management Program)は、米国連邦機関がクラウドサービスを調達する際にセキュリティ性を検証する政府全体共通の認可制度です。GSA(連邦調達庁)傘下のFedRAMP PMOが運営し、NIST SP 800-53の統制体系に基づいてクラウドサービスプロバイダー(CSP)のセキュリティ統制を評価・認可します。核心的な趣旨は「一度認可を受ければ複数機関で再利用」(Do Once, Use Many Times)であり、個々の機関がそれぞれセキュリティ審査を繰り返すことなく、FedRAMP認可を受けたサービスを再利用できるようにすることです。

FedRAMPは法的に民間企業への義務事項ではありませんが、連邦機関にSaaS/PaaS/IaaSを納入しようとするほぼすべてのクラウドサービスプロバイダーにとって必須の参入要件です。

## Moderate/High基準(従来体系)

FedRAMPは、FIPS 199の影響度分類に基づき、データの機密性・完全性・可用性が損なわれた場合の被害規模に応じてセキュリティ統制レベルを区分してきました。

| 区分 | 対象 | 特徴 |
| --- | --- | --- |
| **Low** | 損傷時の影響が限定的な公開情報システム | 統制数が最小 |
| **Moderate** | ほとんどの連邦機関業務システム、CUI(統制対象非分類情報)を含む | 商用SaaS/PaaSの標準目標基準。統制項目約320件超 |
| **High** | 法執行、緊急サービス、金融システムなど、損傷時に深刻な影響 | 統制項目約420件超、認可の難易度・コストが最高 |

商用クラウドサービスの大半はModerate基準で認可を取得し、High基準は国土安全保障省・司法省など機密性の高い機関システムに主に要求されます。

## 2026年のFedRAMP 20x改編現況(fedramp.gov公式基準)

:::caution
FedRAMP 20xは2026年8月現在も進行中の改編であり、情報が急速に変化します。以下は[fedramp.gov](https://www.fedramp.gov/)の公式ページおよびお知らせを基準に確認した内容であり、実際の導入検討時には必ずfedramp.govの最新のお知らせを直接再確認する必要があります。
:::

FedRAMPは、既存のLow/Moderate/High 3段階体系を自動化ベースの**FedRAMP 20x**プログラムへ移行中です。

- **Certification Classシステム**: Class A/B/C/Dの4段階のCertification Classシステムが、2026年2月25日に公開されたNTC-0004(政策文書)に基づき導入されました。注意すべき点は、Classがセキュリティレベルの代替ではなく、**評価・認証の範囲(提出資料・証拠共有・審査方式)を定義する分類**であることです — FedRAMPの公式文書は「ベースラインは評価・認証の範囲を定義するものであり、クラウドサービス全体の品質やセキュリティレベルを示すものではない」と明記しています。既存のRev5 Moderateレベルのシステム(CUIなど非公開の連邦データを扱う)は、実務上Class Cの経路へ移行するものとして案内されています。
- **2026 Consolidated Rules (CR26)**: 2026年6月下旬に確定・発効された統合規則で、認可パッケージを機械可読(machine-readable)形式を中心に提出することを要求しており、従来のWord/Excelテンプレートベースのパッケージは段階的に廃止されます。CSPは変更が発生した際、自動化を通じて認可パッケージを継続的に最新状態に保つ必要があります。
- **現在の運用状況(2026年8月時点)**: 過渡期にあたり、Class Aパイプラインは8月上旬に開設され、Class B/Cは2026年8月31日開設予定です。また、fedramp.gov公式統計によると全体約529件の認可サービスのうち約28件が新しいFedRAMP 20x基準で認可を取得しており、残りの大多数は依然として従来のRev5(Low/Moderate/High)体系で運用されています。
- **Class D(High相当)は開発中**: 高リスク等級に該当するClass Dはまだ開発中であり、2027年第1～2四半期にパイロットが予定されています。
- **Rev5終了スケジュール**: 既存のRev5体系は2027年6月11日まで新規認可の受付を継続し、その後、既存のRev5認可を保有するサービスのための移行パスが2027年下半期に用意される予定です。

:::note
つまり2026年8月時点では、新しい20xシステムと従来のRev5システムが並存する過渡期です。調達対象の機関・サービスがどちらのシステムで認可を受けているかは、[FedRAMP Marketplace](https://marketplace.fedramp.gov/)で個別に確認する必要があります。
:::

## 分離リージョン: GovCloud、Azure Government、Assured Workloads、OCI Government

FedRAMP HighおよびDoD要件まで満たそうとするワークロードは、商用リージョンと物理的・論理的に分離された政府専用リージョンを使用する場合が多くあります。

| リージョン | 特徴 |
| --- | --- |
| **AWS GovCloud (US)** | FedRAMP High、DoD SRG IL2/4/5、ITAR/EAR、CJISに対応。米国内の物理的所在地、米国市民権者のみ運用アクセス可能。アカウント所有者はUS Personである必要あり |
| **Azure Government** | 商用Azureと物理的・論理的に分離、審査済みの米国人スタッフが運用。FedRAMP High、DoD IL4/5、CJIS、ITARに対応 |
| **Google Assured Workloads** | 専用の物理インフラの代わりに、標準GCPリージョン上でソフトウェア定義の統制(データレジデンシー、暗号鍵管理など)を適用する方式。IL5以上には専用環境を提供 |
| **OCI Government Cloud** | Oracleデータベース・エンタープライズアプリケーションに依存するワークロードを対象とした政府専用リージョン |

## CMMC 2.0およびDoD SRG Impact Level

**CMMC 2.0**(Cybersecurity Maturity Model Certification)は、国防総省(DoD)のサプライチェーン契約業者に適用されるサイバーセキュリティ認証制度で、3段階で構成されています。

- **Level 1 (Foundational)**: FCI(連邦契約情報)を扱う業者向け、自己評価
- **Level 2 (Advanced)**: CUIを扱う業者向け、NIST SP 800-171ベース、大半はC3PAO(第三者評価機関)による認証が必要
- **Level 3 (Expert)**: 最高機密度の情報向け、NIST SP 800-172の追加統制、政府(DIBCAC)主導の評価

CMMC最終規則(32 CFR Part 170)は2024年に発効し、契約に反映されるDFARS 252.204-7021改正規則は2025年11月10日から施行されました。ただし2026年8月現在、段階的施行スケジュール(Phase 2以降)は見直しのため一時保留されている状況で、**正確な施行段階は契約時点で必ず再確認が必要です。**

**DoD Cloud Computing SRG(Security Requirements Guide) Impact Level**は、国防総省情報の機密度に応じてクラウド環境を区分します。

| Impact Level | 対象情報 | インフラ要件 |
| --- | --- | --- |
| **IL2** | 公開可能な情報 | 商用クラウド水準 |
| **IL4** | CUIおよび非公開の非分類情報 | 強力な論理的分離、共有インフラを許可 |
| **IL5** | 高機密CUI、任務必須・国家安全保障システム情報 | 専用インフラ、米国市民権者による運用スタッフが必須 |
| **IL6** | 機密(SECRET)および国家安全保障システム情報 | 完全分離環境 |

IL1とIL3は別途存在せず(IL1は不要、IL3はIL4に統合)、FedRAMP Moderate認可がIL2の最小要件とおおむね対応します。

## 実務上の示唆

- 米連邦SaaS市場に参入するにはFedRAMP認可が事実上必須条件であり、認可取得には相当な時間とコストがかかります。FedRAMP 20xはこのプロセスを自動化・短縮しようとする試みですが、2026年8月現在まだ過渡期にあるため、新規参入企業はどちらのシステム(Rev5 vs 20x)で認可を準備すべきか、fedramp.govの最新ガイドラインに基づいて判断する必要があります。
- スポンサー機関(Sponsoring Agency)の確保、米国内の法人・運営組織の構成、米国人中心の運用スタッフなど、組織的な参入障壁が技術的統制と同様に大きな課題となります。
- 直接認可を推進するよりも、すでにFedRAMP認可を取得したインフラ(GovCloud、Azure Governmentなど)上にSaaSを構築するか、認可を受けたパートナーとリセラー/OEM形態で協力することが、初期参入戦略としてよく活用されます。
- 防衛・航空宇宙サプライチェーンに参加する場合、FedRAMPとは別にCMMC認証が要求されることがあるため、対象契約の種類に応じて別途確認が必要です。

## 参考資料

- [FedRAMP公式サイト](https://www.fedramp.gov/)
- [FedRAMP Marketplace](https://marketplace.fedramp.gov/)
- [FedRAMP 20xプログラム](https://www.fedramp.gov/20x/)
- [FedRAMPアップデートのお知らせ](https://www.fedramp.gov/blog/)
- [AWS GovCloud (US)コンプライアンス](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-compliance.html)
- [Azure Government公式ページ](https://azure.microsoft.com/en-us/explore/global-infrastructure/government/)
- [Google Cloud Assured Workloads概要](https://cloud.google.com/assured-workloads/docs/overview)
- [DoD Cloud Computing SRG (public.cyber.mil)](https://public.cyber.mil/dccs/)
- [CMMC公式情報 (DoD CIO)](https://dodcio.defense.gov/cmmc/)
