---
title: "政府クラウド (GCC・IM8・SGTS)"
description: "シンガポール政府クラウド体系 — GCC(Government Commercial Cloud)の構造とGCC+、IM8セキュリティ政策改革、SG Tech Stack、政府調達参加要件を整理します。"
---

> 文書基準: 2026年8月

## 概要

シンガポール政府は自前のデータセンターを構築する代わりに、商用ハイパースケーラーの上に標準化されたセキュリティ・ガバナンス層を重ねる方式で政府クラウドを運用しています。この体系の中心には**GCC(Government Commercial Cloud、正式名称はGovernment on Commercial Cloud)** があり、政府技術庁(Government Technology Agency of Singapore、GovTech)が主管しています。

GCCは**CODEX(Core Operations, Development Environment, and eXchange)** という上位戦略プロジェクトの一つの軸です。CODEXはスマートネーション(Smart Nation)戦略傘下の中核国家プロジェクトに指定されており、GCC(インフラ層)のほかにSG Tech Stack(SGTS、開発層)と政府データアーキテクチャ(Government Data Architecture、データ層)を含みます。

:::note
GCCは、各国の政府クラウド専用センターや公共機関情報資源統合事業のように、**政府機関が直接利用する内部向けプラットフォーム**です。民間ベンダーが「GCCに出店する」構造ではなく、政府機関がAWS・Azure・GCPの上にGovTechが提供するセキュリティ・ガバナンスラッパー(wrapper)をかぶせてシステムを運用する方式です。民間企業がシンガポール政府向け事業に参加するには、GeBIZ調達ポータル登録やMTCS認証取得など別途のトラックを経る必要があります。
:::

## GCC(Government Commercial Cloud)の構造

GCCは「ラッパー(wrapper)プラットフォーム」として紹介されます。政府機関がクラウドインフラを直接構築・保守する代わりに、GCCが提供する標準化されたフレームワークの上で商用クラウドサービスを利用する構造です。公式フレームワークは以下の構成要素で成り立っています。

- **オンボーディング(Onboarding)** — TechPass(GovTechのIAMソリューション)に基づく自動化されたアカウント・権限発行
- **課金(Billing)** — 機関別クラウド利用料の統合管理
- **アプリケーション層** — AWS・Microsoft Azure・Google Cloud(GCP)の3社を対象とする(Oracle Cloudなど他のベンダーはGCCフレームワークに含まれない)
- **モニタリング・ロギング・踏み台ホスト** — 中央化された可観測性と監査証跡
- **オンプレミス連携** — 政府機関内部システムとのハイブリッド接続
- **ガバナンス・ポリシー・データレジデンシー** — シンガポール国内のデータ常駐要件などの政策統制

### GCC 1.0からGCC 2.0へ

初期のGCC(1.0)はベンダーアウトソーシング支援モデルで運用されていましたが、オンボーディング遅延・サービス要求過多などの問題により再設計されました。GCC 2.0はハイパースケーラーごとに順次正式稼働しました。

| クラウド | GCC 2.0正式稼働(GA) |
| --- | --- |
| AWS | 2022年5月4日 |
| Microsoft Azure | 2022年11月30日 |
| Google Cloud (GCP) | 2023年7月7日 |

GCC 2.0の核心的な特徴は以下のとおりです。

- **簡素化されたオンボーディング** — TechPassのみでオンボーディング可能、サービス要求(service request)なしに自動化されたワークフローでアカウント発行
- **SEED(Secure Engineering Environment Device Platform)** — 従来の境界ベースセキュリティから**ゼロトラスト**モデルへの転換。非準拠端末のアクセスを自動遮断
- **Policy-as-Code** — ポリシーをコードとして定義・適用し、プロビジョニングされるすべてのリソースにデフォルトでコンプライアンスチェックを適用、リアルタイムでセキュリティ脆弱性を点検
- **IaC(Infrastructure as Code)** 基盤のコアクラウドプラットフォーム構成

### GCC+ — Confidential等級ワークロードへの拡張

GCC 2.0が扱う一般(Confidential Cloud-Eligible以下)等級システムとは異なり、**Confidentialに分類された高機微システム**は**GCC+**へ別途オンボーディングされます。GCC+は強化された暗号化・鍵管理の分離、シンガポール国内リージョン常駐などより厳格な統制を適用し、これまでクラウド移行が難しかった機微ワークロード(法執行・保健データ処理システムなど)のクラウド転換経路を提供します。

### 採用状況

GovTechが2025年3月7日時点で公開した数値によると、GCCには**3,006のシステム**がオンボーディングされており、**99.5%のサービス可用性**を記録しています。GovTech FY2024-2025年次報告書は、**政府デジタルサービス取引の99%がオンラインで完結している**と明らかにしました(この数値はGCC/GCC+が直接支援する取引の割合ではなく、政府取引全体のオンライン完結率を指すものであり、混同しないよう注意が必要です)。GCC上で運用される代表的なサービスとしては、MyCareersFuture(求職ポータル)、GoBusiness(企業向け許認可ポータル)、WOGAA(政府デジタルサービス実績モニタリング)、国税庁(IRAS)の統合税務システムIRIN、教育省のホームベースドラーニングプラットフォームStudent Learning Spaceなどがあります。

## IM8と2024～2026年の政策改革

**IM8**は「Instruction Manual on ICT&SS(Infocomm Technology & Smart Systems) Management」の略称で、GovTechが管轄する政府機関ICTセキュリティ政策・標準全体を指します。データセキュリティ分類、クラウドセキュリティ、アプリケーション・ネットワーク・エンドポイントセキュリティ、セキュリティ運用などを包括し、政府機関がシステムを導入・運用する際に遵守すべき内部規範集の役割を果たします。

従来のIM8体系では、政府システムは原則としてGCC上でホスティングされる必要があり、SaaSアプリケーションはGCC外でホスティングできませんでした。この硬直性がSaaS導入速度を遅らせているという問題意識から、GovTechは**ICT&SS政策改革(ICT&SS Policy Reform、通称IM8 Reform)** を推進しています。

改革の目標は公式に「機関が適正水準のリスク統制(right-fit risk controls)により、迅速かつ費用対効果が高く革新的なシステムを構築できるようICT&SS政策を単純化すること」として提示されています。核心的な変化は以下のとおりです。

- **リスクベースアプローチ(Risk-Based Approach)** — システムを低リスククラウド、中リスククラウド、高リスククラウド、低リスクオンプレミス、生成AI、デジタルサービス、サンドボックスなど類型別に区分し、それぞれ異なる統制水準を適用
- **System Security Plan(SSP)テンプレートの再整備** — リスク類型別の基本統制セットを事前定義し、機関がこれをカスタマイズする方式に転換
- **統制カタログ(Control Catalog)の再構成** — 同一のリスク分類体系に合わせて統制項目を再整列
- **低リスクSaaSのGCC外部ホスティング許可** — 低リスク用途に限りGCC外でホスティングされるSaaSアプリケーションの導入を許可する方向で政策が改編中
- システム所有機関(digital system owner)が自らの業務・技術的コンテキストに合わせてセキュリティ計画を自ら調整できる**裁量権の拡大**

:::caution
IM8改革は2026年8月時点で**進行中の政策転換**です。低リスクSaaSのGCC外部ホスティング許可範囲、統制カタログの最終確定時期など詳細事項はGovTechの公式政策ポータル(info.standards.tech.gov.sg)で随時更新されているため、実際の調達・コンプライアンス対応時には最新の公告を直接確認する必要があります。
:::

## SGTS(Singapore Government Tech Stack)

SGTSはGCC(インフラ層)と対をなす**開発層**資産で、GovTechが提供する再利用可能なプラットフォーム・API・共通サービス群です。政府機関がインフラを一から構築しなくても、本人認証、決済、データ交換など共通機能を再利用してデジタルサービスを素早く作れるよう支援します。GovTechは**人(People)・プラットフォーム(Platform)・実践(Practice)** の3つの軸でSGTS普及戦略を説明しています。

40以上の政府機関がSGTSを使用中で、200以上のクラウド基盤システムがこれを通じて構築されました。代表例として、国民デジタルID確認サービス**MyInfo**はSGTSを活用し、通常1年かかる開発期間を4カ月に短縮しました。SGTS傘下には、政府開発者向けのマルチテナントSaaS型CI/CDツールである**SHIP-HATS**(Secure Hybrid Integration Pipeline – Hive Agile Testing Solutions)も含まれます。

## 政府調達参加要件とMTCSの関係

GCC・IM8・SGTSは政府機関内部向けの体系ですが、これを支える商用クラウド・SaaSを供給する民間ベンダーには別途の参入要件が適用されます。

- 政府機関はクラウド・ICT調達を**GeBIZ**(Government Electronic Business System、政府統合電子調達ポータル)を通じて行う必要があります。これは政府調達法(Government Procurement Act)と各種Instruction Manualに基づく義務チャネルです。
- 政府クラウド調達では、ベンダーのクラウドサービスに**MTCS Level 3認証**が求められるケースが多いものの、正確な認証・資格要件は個別の入札公告、取り扱うデータの等級、サービスの種類によって異なるため、案件ごとに確認する必要があります。MTCS認証体系と等級構造は[MTCS (マルチティア・クラウドセキュリティ標準)](../mtcs/)文書で詳しく扱います。
- GCCは共通プラットフォームのレベルでPDPA・IM8・MTCS Level 3に適合するセキュリティ・ガバナンスのガードレールを提供しますが、公式資料は個々のワークロードが別途の手続きなしに認証を完全に自動継承することを保証するものではありません。共同責任モデル(shared responsibility model)に基づき、サービスごとに追加の設定・審査が必要になる場合があります。逆に、政府機関にSaaS・プラットフォームを供給しようとする民間ベンダーは、自らMTCS認証などの要件を満たして初めて調達対象に上がることができます。

## 実務上の示唆

- **GCCは「政府専用プライベートプラットフォーム」であり、別途の認証制度ではありません。** グローバル企業がシンガポール政府向け事業(SI、SaaS供給など)を検討する場合、GCC自体で認証を取得することが目標ではなく、GeBIZ登録と（入札ごとに求められる）MTCS認証の確保が実質的な参入手続きです。
- **IM8改革の流れを注視する価値があります。** 低リスクSaaSのGCC外部ホスティングが許可される方向に政策が緩和されつつあり、今後政府機関向けSaaS販売時にGCC内部インフラへの依存度が下がる可能性があります。ただし改革が完了していないため、個別の調達公告の要求事項をその都度確認する必要があります。
- **CODEX・GCC・SGTSの階層を区別して理解する必要があります。** GCC(インフラ)・SGTS(開発プラットフォーム)・政府データアーキテクチャ(データ)はそれぞれ異なる層を扱うため、政府機関向け提案書を作成する際にどの層に対応するソリューションなのかを明確にする必要があります。
- **コンプライアンスは民間市場と別トラックです。** 民間企業向けクラウド規制(PDPA、MTCS)と政府機関内部政策(IM8、GCC)は運営主体と適用対象が異なるため、両トラックを混同して一つの認証だけで双方を満たすと想定してはいけません。

## 参考資料

- [Government on Commercial Cloud (GCC) — GovTech Singapore](https://www.tech.gov.sg/products-and-services/for-government-agencies/software-development/government-on-commercial-cloud/)
- [Singapore Government Tech Stack (SGTS) — GovTech Singapore](https://www.tech.gov.sg/products-and-services/for-government-agencies/software-development/sg-tech-stack/)
- [About GCC 2.0 — Singapore Government Developer Portal](https://www.developer.tech.gov.sg/products/categories/infrastructure-and-hosting/gcc/about-gcc-2-0)
- [GCC Overview (GCC/GCC+分類基準) — Singapore Government Developer Portal](https://www.developer.tech.gov.sg/products/categories/infrastructure-and-hosting/gcc/overview)
- [Government on Commercial Cloud (GCC 2.0) Fact Sheet — GovTech Singapore](https://www.developer.tech.gov.sg/assets/files/gcc-factsheet-121222.pdf)
- [Singapore Government ICT&SS Policy Reform Portal — GovTech Singapore](https://info.standards.tech.gov.sg/)
- [GeBIZ — Singapore Government e-Procurement Portal](https://www.gebiz.gov.sg/)
- [Tech Stacks Driving Singapore's Smart Nation Journey — GovTech(政府取引オンライン完結率99%の出典)](https://www.tech.gov.sg/technews/tech-stacks-driving-singapore-smart-nation/)
- 金融業界・公共調達のMTCS要件は[MTCS (マルチティア・クラウドセキュリティ標準)](../mtcs/)を、個人情報関連規制は[PDPA (個人情報保護法)](../pdpa/)を参照してください。
