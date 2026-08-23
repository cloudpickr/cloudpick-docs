---
title: "欧州ソブリンAI・モデル地形"
description: "EU AI Continent Action Plan・AI Factories、Mistral AI・Aleph Alphaなど欧州ファウンデーションモデル提供企業、ハイパースケーラーのソブリンクラウドにおけるAIサービス範囲を整理します。"
---

> 文書基準: 2026年8月

## 概要

EUはクラウドインフラのデータ主権を超え、**AIモデル・コンピューティング能力そのものの域内確保**を政策目標として明示しています。米国・中国系ファウンデーションモデル(FM)への依存を下げ、欧州産AIエコシステムを育成しようとするこの流れは、政府主導のインフラ投資(AI Factories/Gigafactories)と民間FM提供企業の育成(Mistral AI、Aleph Alphaなど)が並行する構造です。本文書は、2026年8月現在のEU AI戦略の進捗状況と欧州FMエコシステム、ハイパースケーラーのソブリンクラウドにおけるAIサービス範囲を整理します。

## EU AI戦略 — AI Continent Action Plan

**AI Continent Action Plan**は、EU欧州委員会が推進するAI競争力強化のロードマップで、インフラ投資・データアクセス性・人材育成・規制整合性を軸としています。

### InvestAI — 資金動員体系

- 2025年2月のパリAIアクションサミットで、フォンデアライエンEU欧州委員会委員長が**InvestAIイニシアチブを通じて総額2,000億ユーロ規模のAI投資を動員する**という目標を発表しました。この中には、AI Gigafactories設立のための新規EU基金**200億ユーロ**が含まれます。
- InvestAIは、EU予算が設備投資(CapEx)の最大17%を支援し、加盟国が最低同額をマッチングする官民協力の構造です。
- 2025年6月の提案公募には**16加盟国から77件の提案(候補地60カ所)** が寄せられ、当初の想定を大きく上回りました。

### AI Factories・Gigafactories — EuroHPC基盤のコンピューティングインフラ

**EuroHPC共同事業(Joint Undertaking)** が運営するAI Factoriesは、スーパーコンピューティングインフラをスタートアップ・中小企業・研究機関に開放し、信頼できる生成AIモデル開発を支援する拠点です。

| 時期 | 拡張内容 |
| --- | --- |
| 2024年12月 | 第1次AI Factories 7カ所を選定(フィンランド・ドイツ・ギリシャ・イタリア・ルクセンブルク・スペイン・スウェーデン) |
| 2025年3月 | 第2次6カ所を追加(オーストリア・ブルガリア・フランス・ドイツ・ポーランド・スロベニア) |
| 2025年10月 | 第3次6カ所を追加 + AI Factory Antenna 13カ所を新設 |
| 2026年8月時点 | **19のAI Factories + 13のAntenna**が15以上の加盟国・準加盟国で稼働中 |

EuroHPCは2025~2026年の間に少なくとも9基のAI特化型スーパーコンピュータを新規調達し、既存のAIコンピューティング能力を3倍以上に拡大する計画で、EUと参加国はAI Factories・Antennaに26億ユーロ以上を共同投入しました。

これより上位等級の**AI Gigafactories**は、施設あたり10万基以上のAIアクセラレーターを備えた超大型フロンティアモデル学習拠点で、EU欧州委員会はAI Gigafactory専用基金を通じて総額**200億ユーロ**規模の投資動員を目標としています(公共・民間資金の正確な分担比率は公式発表による別途確認が必要です)。2026年1月、EU理事会がEuroHPC規則を改正し、Gigafactoriesの開発・運用までEuroHPCの任務に含めました。**最初のGigafactoryの着工は2027年と見込まれています**。

:::note
AI Factories(多数・中規模、既に19カ所稼働)とAI Gigafactories(少数・超大型、まだ着工前)は**別等級の事業**です。この2つの用語を混同しないよう注意が必要です。
:::

## 欧州ファウンデーションモデル提供企業

### Mistral AI — 欧州最大の商用FM提供企業

フランス・パリに本社を置くMistral AIは、欧州で最も先進的な商用FM提供企業とされています。

- **最新モデル**: Mistral Medium 3.5、OCR 4などを公開しており、Microsoft Foundry・Copilot Studioなどハイパースケーラーのチャネルを通じても配信されています。
- **Microsoftとのパートナーシップ拡大**: 2026年7月21日、Microsoftとの戦略的パートナーシップ拡大を発表し、**数十億ドル規模のAIインフラ投資**に合意しました。Azureを通じてクラウド、クラウド接続型、**完全隔離(fully disconnected)環境**まで多様な展開形態でMistralモデルを提供し、規制産業・公共部門顧客のデータ統制要求に対応しています。
- **独自インフラ投資**: 2026年2月、EcoDataCenterと共に**12億ユーロ規模のAIデータセンター投資**を発表し、Nvidia GB300 GPU 13,800基を搭載した施設を通じて2027年末までに欧州全域で合計200MWのコンピューティング容量確保を目指しています。
- Mistralは規制産業・公共部門顧客向けに、欧州管轄区域内でのみ実行される「ソブリン推論(Sovereign Inference)」サービスも別途提供しています。

### Aleph Alpha — ソブリンAIの象徴からカナダとの合弁へ

ドイツ・ハイデルベルクに本社を置くAleph Alpha(2019年設立)は、欧州の政府・規制機関が米国ビッグテックにデータ統制権を渡すことなく高性能AIを運用できるようにすることを目標に成長してきた、代表的な「ソブリンAI」企業でした。PhariaAIプラットフォームは、ドイツ連邦省庁の機密等級業務環境でも使用されています。

:::caution
**2026年4月、カナダのAI企業CohereとAleph Alphaが結合のための取引("join forces")を発表しました。** 公式資料は2026年8月時点でもこれを完結した買収ではなく計画中の取引として説明しており、報道されている約200億ドルという金額も、公開された買収価格ではなく取引後の合算企業価値とされています。ドイツ・カナダ両国のデジタル担当大臣が発表イベントに参加し、これは2026年初頭のミュンヘン安全保障会議を契機に発足した**独加ソブリンテクノロジー同盟(Sovereign Technology Alliance)** の延長線上にある、両国政府の支持を受けた取引として報じられました。ドイツデジタル省はこの取引を「地政学的・経済的に重要な価値」を持つと評価しました。

ただしこの事例は、**「欧州ソブリンAI」の定義自体が流動的であることを示しています。** Aleph Alphaは依然としてドイツに本社と人員を置き政府ワークロードにサービスを提供していますが、支配構造上はカナダ企業との合併体となりました。「ソブリン」が地理的なデータ処理場所を意味するのか、資本・支配構造まで含むのかは、フランスのSecNumCloudのように国ごとに基準が異なり([EU加盟国別クラウドセキュリティスキーム](../national-schemes/)参照)、Aleph Alphaの事例に見られるように市場状況に応じてその境界は絶えず再定義されています。
:::

### EuroLLM・OpenEuroLLM — 公開型多言語モデルプロジェクト

民間の商用モデルとは別に、EUは学界・産業界・EuroHPCセンターが共同参加する**公開(open)FMプロジェクト**も支援しています。

- **OpenEuroLLM**: 3,740万ユーロ規模のプロジェクトで、チェコのカレル大学(Jan Hajič)が統括し、AMD Silo AIが共同主導する20機関のコンソーシアムが参加します。EUの公用語すべてに対応する完全公開型(データ・コード・重みを公開)LLMファミリーの開発を目標とし、LUMI・Leonardo・MareNostrumなどEuroHPCスーパーコンピュータの学習データを共同でキュレーションします。
- 2026年3月に発表された1年目の進捗報告によると、80億(8B)パラメータモデルを**2026年夏中**に公開する計画で、大型モデルはその後順次公開される予定です。**この計画の実際の達成有無は、文書基準日(2026年8月)時点でプロジェクトの公式発表による別途確認が必要です。**
- EU AI法の遵守、欧州の中小企業・スタートアップのアクセス性をプロジェクト設計の目標に明示的に含めている点が、商用モデルとの差別化点です。

## ハイパースケーラーEUソブリンクラウドのAIサービス範囲

[GDPRとデータ主権](../gdpr-sovereignty/#ソブリンクラウドオプションの比較)で扱ったソブリンクラウドオプションはAIサービスの範囲を拡大している最中ですが、**一般商用リージョンと同一のAIサービスポートフォリオがそのまま提供されるわけではありません。**

- **AWS European Sovereign Cloud**: 2026年1月のGA発表時点で、AIを含む90以上のサービスカテゴリの提供を明示しましたが、Bedrock・SageMakerなど個別のAI/MLサービスの具体的な提供範囲は発表資料に明示されていません。
- **Microsoft EU Data Boundary / Bleu・Delos**: EU Data BoundaryはMicrosoft 365・Dynamics 365・Power Platformと大部分のAzureサービスの顧客データのEU域内処理を保証しますが、Azure OpenAIなど生成AIサービスが同一範囲に含まれるかはサービスごとに別途確認が必要です。
- **S3NS(Google Cloud × Thales)**: 2025年12月にSecNumCloud資格を取得したPREMI3NSは、IaaS・CaaS・PaaSの20あまりのサービスから開始し、2026年上半期の第2次拡張審査にはCloud Run・Dataproc・Confidential VMなどが含まれました。Vertex AI・Geminiなど生成AIサービスのSecNumCloud認証への組み込み有無は公式確認が必要です。

:::caution
ソブリンリージョン・パートナーシップの**AIサービス提供範囲は現在も拡大し続けており、公式発表のたびに変わる可能性があります。**「ソブリンクラウドを使えばすべてのAIサービスを同様に使える」と前提とせず、利用しようとするAIサービスが対象リージョン・パートナーシップの認証・提供範囲に実際に含まれているかを、ベンダーの公式文書でサービス単位まで確認する必要があります。
:::

## 韓国のソブリンFM政策との比較

EUと韓国はいずれも「グローバルFM依存の緩和」という目標を共有していますが、アプローチは異なります。韓国の[独自AIファウンデーションモデルプロジェクト](../../korea/ai/sovereign-fm-policy/)は、政府が少数精鋭チームを選抜し、予算・GPUを集中支援して最終的に2チームへ絞り込む**トーナメント型の国家代表選抜構造**です。2026年8月時点で2次段階評価が完了し、アップステージ・SKテレコム・LG AI研究院の3チームが3次に進出しています。また政府はフロンティア級AI開発への戦略再編を検討中です。一方EUは、Mistral AIのような民間商用企業へのハイパースケーラーとのパートナーシップ・投資を誘導すると同時に、OpenEuroLLMのような多国間・多機関の公開協力プロジェクトを並行させ、AI Factoriesを通じて少数のチャンピオンではなく多数のスタートアップ・研究機関にコンピューティングアクセス性を広げる**分散・開放型エコシステム形成方式**を取っています。ただしAleph AlphaのCohere合併事例が示すように、欧州もまた自国のチャンピオンを市場論理から完全に切り離すことはできませんでした — これは、特定企業を「国家代表」に指定して支援する政策が、長期的には支配構造・資本変動リスクにさらされうるという点で、韓国の政策設計にも参考になる示唆といえます。

## 実務上の示唆

- **FMを交換可能な構成要素として扱うゲートウェイ層を設けましょう。** 欧州FM地形は、Mistralのハイパースケーラーへの編入、Aleph Alphaの支配構造変更のように急速に再編されています。特定ベンダーのAPIにアーキテクチャを直接結合するより、抽象化層を設ける方がリスク管理上有利です。
- **「完全隔離展開」が必要な規制ワークロードは、Mistral類のオンプレミス・エアギャップオプションを検討してください。** 公共部門・金融などデータが外部に出せないワークロードには、ハイパースケーラーAPI呼び出し型よりも隔離展開が可能な欧州FM提供企業のオプションが適している場合があります。
- **ソブリンクラウドのAIサービス範囲を、リージョン・パートナーシップごとにサービス単位まで確認してください。** 「ソブリン」がデータ保存場所のみを保証するのか、AIサービス全体を含むのかはベンダー・時点によって異なります。
- **公開型プロジェクト(EuroLLMなど)は、商用SLA・サポート体制がまだ商用モデルと同水準ではない場合があります。** プロダクション導入前にライセンス・サポート水準を別途確認する必要があります。
- **最新状況の再確認が必須です。** AI Factoriesの拡張、Mistral・Aleph Alphaなどのパートナーシップ・支配構造の変化、ソブリンクラウドのAIサービス組み込み範囲はいずれも急速に更新される事案のため、プロジェクト着手時点で公式情報源から再確認するプロセスを設けることが安全です。

## 参考資料

- [EU欧州委員会 — AI Continent](https://commission.europa.eu/topics/competitiveness/ai-continent_en)
- [EU欧州委員会 — AI Factories](https://digital-strategy.ec.europa.eu/en/policies/ai-factories)
- [EU欧州委員会 — AI Gigafactories](https://commission.europa.eu/topics/competitiveness/competitiveness-coordination-tool-projects/ai-gigafactories_en)
- [Microsoft — Mistralパートナーシップ拡大発表 (2026.7)](https://news.microsoft.com/source/2026/07/21/microsoft-and-mistral-expand-strategic-partnership-to-give-enterprises-and-regulated-industries-frontier-ai-they-can-control/)
- [CNBC — CohereによるAleph Alpha買収発表 (2026.4)](https://www.cnbc.com/2026/04/24/cohere-aleph-alpha-germany-ai-europe-expansion.html)
- [OpenEuroLLM 公式サイト](https://openeurollm.eu/)
- [OpenEuroLLM — 1年目の進捗報告](https://openeurollm.eu/blog/first-year-progress-and-next-steps)
- [AWS — European Sovereign Cloudリリース発表 (2026.1)](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe)
- [Thales — S3NS SecNumCloud資格取得発表 (2025.12)](https://www.thalesgroup.com/en/news-centre/press-releases/s3ns-announces-secnumcloud-qualification-premi3ns-its-trusted-cloud)
- [Cohere — Aleph Alphaとの結合取引公式発表 (2026.4)](https://cohere.com/blog/cohere-alephalpha-join-forces)
