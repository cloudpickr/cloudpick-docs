---
title: "GDPRとデータ主権"
description: "GDPRの域外移転体系、EU Data Boundary、ソブリンクラウドオプションの比較とEUCS認証スキームの動向を整理します。"
---

> 文書基準: 2026年8月

## 概要

GDPR（General Data Protection Regulation、EU一般データ保護規則）は、2018年の施行以降も進化を続けています。近年の変化は、法文自体よりも**「個人データが物理的にどこで、誰によって処理されるか」**という要求が強化される方向で現れています。本文書は、韓国企業がEUへクラウドワークロードを拡張したり、EU顧客データを処理したりする際に直面する域外移転体系と、これを背景に登場した「ソブリンクラウド（Sovereign Cloud）」オプションについて整理します。

## GDPR域外移転体系

GDPR第5章（Chapter V）は、EU域外への個人データ移転に対して別途の保護措置を要求しています。実務で用いられる主なメカニズムは以下のとおりです。

| メカニズム | 説明 |
| --- | --- |
| **十分性認定（Adequacy Decision）** | EU欧州委員会が特定国の個人データ保護水準をGDPRと同等と認めた場合、その国への移転には追加の保護措置が不要 |
| **標準契約条項（SCC、Standard Contractual Clauses）** | 十分性認定のない国へ移転する際に契約当事者間で締結する、EU欧州委員会承認の標準条項。2021年改訂版が現行基準 |
| **BCR（Binding Corporate Rules）** | 多国籍企業グループ内部の移転に適用される拘束力のある社内規則 |

### 韓国の十分性認定（2021）

韓国は2021年12月17日、EU欧州委員会から**十分性認定**を受けました。個人情報保護委員会とEUの間の交渉は2021年3月に妥結し、同年12月に正式採択されました。

:::caution
**韓国の十分性認定はEU→韓国方向にのみ適用されます。** つまり、EUから韓国へ個人データを移転する際にはSCCなどの別途の保護措置なしに移転が可能ですが、逆方向（韓国企業がEU居住者の個人データを直接収集・処理する場合、すなわちGDPRの域外適用対象となる場合）には、GDPR自体の遵守義務が別途適用されます。十分性認定はGDPR遵守義務そのものを免除するものではありません。
:::

韓国企業がEUリージョンのクラウドを利用してEU顧客データを処理する場合、移転方向にかかわらず、ベンダーとの契約（DPA、Data Processing Addendum）にSCCが含まれているか、そしてベンダーが提供するリージョン・ガバナンスオプションが自社のデータ分類要件を満たすかを確認する必要があります。

## EU Data Boundary

**EU Data Boundary**は、Microsoftが推進してきたデータレジデンシー強化のイニシアチブで、EU・EFTA顧客のデータをEU/EFTA域内でのみ保存・処理することを目標としています。

- **2023年1月**: 第1段階 — Microsoft 365、Dynamics 365、Power Platformなど中核クラウドサービスの顧客データ・仮名化された個人データをEU域内に保存
- **2025年2月26日**: 完成（第3段階） — サポートログ、ケースノートなど**プロフェッショナルサービスデータ（Professional Services Data）**までEU/EFTA域内保存に拡張、データレジデンシー・透明性強化の完了を発表

他のベンダーも同様の方向でリージョン内データ処理の保証を拡大していますが、「EU Data Boundary」という名称と範囲（プロフェッショナルサービスデータを含む）はMicrosoft固有のイニシアチブです。他ベンダーのEUリージョンデータレジデンシー保証範囲は、各ベンダーの契約文書（DPA）で個別に確認する必要があります。

## ソブリンクラウドオプションの比較

データ保存場所にとどまらず、**運用要員・管理アクセス・緊急時の法的管轄**までEU域内に制限しようとする需要に対応し、主要ベンダーは以下のような「ソブリンクラウド」オプションを運用・発表しています。

| ベンダー | オプション | 形態 | 現状 |
| --- | --- | --- | --- |
| **AWS** | European Sovereign Cloud | 独立リージョン（物理的・論理的に既存のAWSリージョンと分離） | 2026年1月15日に正式リリース（GA）、ドイツ・ブランデンブルクが最初のリージョン。長期78億ユーロの投資を発表、ベルギー・オランダ・ポルトガルにソブリンLocal Zoneを拡張予定 |
| **Microsoft** | Bleu（フランス）/ Delos Cloud（ドイツ） | パートナー運用ソブリンクラウド（ナショナルパートナークラウド） | BleuはOrange・Capgeminiの合弁会社（SecNumCloud認証を目標）、Delos CloudはSAPの子会社。2025年11月に相互支援協定を締結、Delos-Microsoft間のMoUにより緊急時（他国政府によるサービス制限など）にDelosがMicrosoftクラウドのコードにアクセスできる法的権利を確保 |
| **OCI** | EU Sovereign Cloud | 物理的に分離されたEU専用リージョン | 2023年6月から運用中、フランクフルト・マドリードリージョン。EU法人・EU居住スタッフのみが運用、商用OCIと比べ追加料金なし |
| **Google Cloud** | 主権パートナーシップ（T-Systems・Thales/S3NS・Proximus） | パートナー企業運用リージョン | ドイツはT-Systems、フランスはThales子会社S3NS（SecNumCloud目標）、ベルギー・ルクセンブルクはProximusと協力。2026年5月にThales-Google Cloudがドイツで新たなソブリンクラウドパートナーシップを発表 |

:::note
「ソブリンクラウド」はベンダーごとに定義と範囲が異なります — データ保存場所のみを保証する水準から、運用要員・鍵管理・緊急時の法的アクセス権まで含む水準まで幅広くあります。導入前に、各ベンダーが具体的に何をEU域内に制限しているのか（保存 vs 処理 vs 運用アクセス vs ガバナンス）を契約文書で確認する必要があります。
:::

## EUCS認証スキームの流動性

**EUCS（European Cybersecurity Certification Scheme for Cloud Services）**は、ENISAが主導するクラウドサービス共通セキュリティ認証体系で、本来はクラウドベンダーのセキュリティ水準をEU全域で相互承認可能な等級（Basic/Substantial/High）に標準化することを目的としていました。

:::caution
**EUCSの「主権性（Sovereignty）要件」は2026年8月現在も確定しておらず、議論が進行中です。**

- 初期草案は、最高等級（High+）認証にEU域外企業の持分・支配構造の排除（immunity）要件を含んでいました。
- 2023年の改訂草案はこれを緩和し、High+等級でのみデータローカライゼーションを要求し、「信頼できる域外クラウド提供者」認証の可能性を残しました。
- 2026年1月20日にEU欧州委員会が発表した**Cybersecurity Act 2（CSA2）改正案**は、認証体系を技術的基準中心に再編する方向性を示しており、この流れの中でEUCS・EU5Gスキームの作業が再開されると見込まれています。
- EUCSの最終案は依然として確定しておらず、「主権性要件を含めるかどうか」はEU加盟国間で意見の相違が残る事案です。**最新の確定状況はENISA・EU欧州委員会の公式発表を通じて別途確認が必要です。**
:::

EUCSは現時点では任意（voluntary）の認証ですが、NIS2とData Act（2024年1月発効、2025年9月から主要条項適用中）は、加盟国・規制当局が公共機関・必須/重要機関に対してEUCS認証ベンダーの使用を義務化できる権限を付与しており、今後の調達要件に影響を与える可能性があります。

## アーキテクチャへの示唆

- **データ分類から始める**: どのデータがEU域内での保存・処理義務の対象なのか（公共調達要件、契約上の要求、自社のリスクポリシー）をまず分類したうえで、リージョン・ベンダーオプションを決定します。
- **ソブリンオプションはコスト・機能のトレードオフを伴う**: ソブリンリージョンは一般商用リージョンと比べてサービス提供範囲が限定的だったり、新機能の反映が遅れたりする場合があります。必須要件でなければ、一般EUリージョン+強化されたガバナンス（暗号化、アクセス透明性ログ）で十分な場合が多いです。
- **DPA・契約書のレビューがリージョン選択と同じくらい重要**: SCCの有無、下位処理者（sub-processor）一覧、緊急時アクセス条項を契約文書で直接確認します。
- **EUCSなど流動的な規制を「確定前提」で設計しない**: 最終的に確定していない認証要件をアーキテクチャの必須前提条件とするのではなく、確定時に切り替え可能な余地を残しておきます。
- **ソブリンランディングゾーン設計との連携**: EUデータレジデンシー・処理管轄要件をランディングゾーンのガードレールに反映する具体的なパターンについては、[ランディングゾーン — ソブリンランディングゾーン](../../governance/landing-zone/#소버린-랜딩존-sovereign-landing-zone)を参考にしてください。

## 参考資料

- [EUR-Lex — GDPR (Regulation (EU) 2016/679)](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [EU欧州委員会 — 十分性認定Q&A（韓国）](https://ec.europa.eu/commission/presscorner/detail/en/qanda_21_6916)
- [EU欧州委員会 — データ保護十分性認定リスト](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en)
- [EDPB — 韓国十分性認定草案意見](https://edpb.europa.eu/news/news/2021/edpb-adopts-opinion-draft-south-korea-adequacy-decision_en)
- [Microsoft — EU Data Boundary完成発表（2025.2）](https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/)
- [AWS — European Sovereign Cloudリリース発表（2026.1）](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe)
- [Microsoft — 欧州主権ソリューション発表（2025.6）](https://blogs.microsoft.com/blog/2025/06/16/announcing-comprehensive-sovereign-solutions-empowering-european-organizations/)
- [Google Cloud — Sovereign Cloud](https://cloud.google.com/sovereign-cloud)
- [Oracle — Cloud Compliance](https://www.oracle.com/corporate/cloud-compliance/)
