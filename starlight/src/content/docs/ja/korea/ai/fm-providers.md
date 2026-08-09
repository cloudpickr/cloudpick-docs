---
title: "国内ファウンデーションモデル提供社比較"
description: "ネイバー、LG AI研究院、カカオ、KT、アップステージ、NC AI、SKTなど国内FM提供社のモデル・ライセンス・提供チャネルを比較します。"
---

> 文書基準: 2026年8月

## 概要

韓国には大企業系列会社からスタートアップまで、多数のファウンデーションモデル(FM)提供社が存在します。本文書では主要提供社の最新モデル、ライセンス構造、提供チャネルを整理し、グローバルモデルと比較して国内モデルを選択する際に考慮すべき基準を扱います。

:::note
モデルバージョンとライセンス条件は急速に変化します。以下の表は2026年8月時点のものであり、導入前に各社の公式文書で最新の条件を再確認してください。
:::

## 提供社別現況

| 提供社 | 代表モデル | 最新バージョン(2026.8時点) | ライセンス | 主な提供チャネル |
| --- | --- | --- | --- | --- |
| ネイバー(クラウド) | HyperCLOVA X | SEED(軽量・オープン)、THINK(推論特化)、DASH(軽量・高速)のラインナップ。2025.12にSEED 32B THINK/8B Omni、2026年上半期にSEED 4Bオムニモーダル(国防特化)を公開 | SEEDシリーズの一部(0.5B~3B級)はオープンソース公開、上位モデルはAPI専用 | ネイバークラウド CLOVA Studio API (Basic/Exclusive/Neurocloud料金プラン) |
| LG AI研究院 | EXAONE | EXAONE 4.0(ハイブリッド推論)、EXAONE 4.5(マルチモーダル) | 研究・教育目的は無料公開、**商用利用はLG AI Researchとの別途ライセンス契約が必要** | Hugging Faceでのモデル公開、LG AI Research独自API、教育機関向けライセンス拡大 |
| カカオ | Kanana | Kanana-2シリーズ(2026.1アップデート4種)、Kanana-2軽量SLM 4種(2026.7、1.3B/3B) | Apache 2.0ベースのKanana Open License — **商用利用可** | Hugging Faceでのオープンソース配布。オンデバイス動作最適化 |
| KT | 믿:음(Mi:dm) | 믿:음 K 2.5 Pro(2026.2、MWC26で公開)。従来のMi:dm K 2.0(2025.7)はBase 11.5B + オンデバイスMini 2.3B構成 | 自社サービス・B2B供給中心(公開ライセンス情報は限定的) | KT独自のエンタープライズAIプラットフォームを通じたB2B・B2G供給(AICC、チャットボット、文書認識、法律・金融特化など) |
| アップステージ | Solar | Solar Pro 2(31B、ハイブリッドチャット/推論、2025.7正式リリース) | クローズドAPIサービス(オープンソースではない) | Upstage Console API、Amazon Bedrock Marketplace、AWS SageMaker JumpStart、AWS Marketplace |
| NC AI | VARCO | VARCO-VISION 2.0(2025.7、マルチモーダル4種オープンソース)、VARCO 3D 2.0、VARCO Voice(多言語音声) | オープンソース公開(モデルごとに異なる) | Hugging Face、AWS SageMakerベースのインフラ。AWS Private Cloudを通じたドメインデータのカスタマイズ対応を予定 |
| SKテレコム | A.X | A.X 4.0(2025.4.30オープンソース公開)。Qwen2.5ベースに韓国語データを大規模追加学習 | オープンソース公開 | GitHub/Hugging Face、SKT独自サービス('エイダット')との連携 |

## 韓国語性能とベンチマーク

韓国語LLM評価にはKMMLU(韓国語知識理解)、KoBEST、HAE-RAEなどが用いられます。例えばSKテレコムは、A.X 4.0がKMMLUで78.3点を記録し、GPT-4o(72.5点)を上回ったと発表しています。ただし、ベンチマークスコアは提供社独自の発表に基づく場合が多いため、導入前に自社の業務データに基づく別途評価(RAG精度、ドメイン用語処理など)を並行して実施することを推奨します。

## ベンダーエコシステムの構図

これらのうち、ネイバークラウド、アップステージ、SKテレコム、NC AI、LG AI研究院は政府の「独自AIファウンデーションモデル」プロジェクトの1次精鋭チームとして選定されたことがありますが、2025年12月の1次段階評価でネイバークラウドとNC AIが脱落し、モティーフテクノロジーズが追加合流するなど、構図は変化し続けています。詳しい選定経緯は[ソブリンAI・独自AIファウンデーションモデル政策](../sovereign-fm-policy/)文書を参照してください。NC AIはその後、汎用LLMよりも3D・音声・翻訳などバーティカル生成AIへとポジショニングを移す様子が見られます。

## グローバルモデルとの比較選択基準

国内FMとGPT・Gemini・Claudeなどグローバルモデルのいずれを選択するかは、ベンダーの優劣ではなく**ワークロード要件**によって判断すべきです。

- **規制・主権要件**: 網分離規制([網分離とネットワーク隔離](../../security/network-isolation/)参照)や公共調達([CSAP](../../security/csap/)参照)対象のワークロードは、国内リージョンでサービスされるモデルが有利な場合が多いです。データが海外に移転してはならないワークロードは、国内提供社の国内データセンターベースのAPIを優先的に検討してください。
- **韓国語・ドメイン特化性能**: 一般常識・推論ではグローバルトップクラスのモデルが依然として先行する場合が多いものの、韓国語語彙・敬語・業界用語処理では国内モデルが強みを示す事例が報告されています。必ず自社ベンチマークで検証してください。
- **ライセンスとカスタマイズ**: カカオKanana、NC AI VARCO、SKT A.Xは商用利用可能なオープンソースであり、自社インフラでのファインチューニング・デプロイが可能です。一方EXAONEは商用利用時に別途契約が必要であり、SolarとHyperCLOVA X上位モデルはAPI利用が基本的な経路です。オンプレミス・VPC閉域網へのデプロイが必要な場合は、ライセンス条件を最優先で確認する必要があります。
- **ベンダーの持続可能性**: ソブリンAIプロジェクトの段階評価結果に見られるように、国内FMエコシステムはまだ流動的です。特定ベンダーに長期的に依存するアーキテクチャよりも、APIゲートウェイを通じてモデルを交換可能に構成することがリスクを軽減します。
- **コスト**: アップステージSolar Pro 2は100万トークンあたり0.5ドル水準で公開されるなど、国内モデルが価格競争力を打ち出す場合があります。ただし秒間処理量、コンテキスト長などの条件が異なるため、単純なトークン単価だけで比較しないでください。
- **エージェント型・マルチモーダル対応**: カカオKanana-2、KT믿:음K、NC AI VARCO-VISIONなどは、エージェント型AI・マルチモーダルを別ラインナップとして強化する傾向にあります。単純なテキスト生成を超えるユースケースであれば、該当ラインナップの成熟度を別途確認してください。

## 導入チェックリスト

- [ ] ワークロードが網分離・CSAP対象かどうかを確認したか (対象であれば国内リージョンAPIを優先的に検討)
- [ ] 自社の業務データで韓国語・ドメインベンチマークを再現したか (提供社発表の数値のみで判断しない)
- [ ] オンプレミス/VPC閉域網へのデプロイが必要な場合、当該モデルのライセンスが商用ファインチューニング・再配布を許可しているか確認したか
- [ ] 特定ベンダーのAPIに強く結合されないよう、ゲートウェイ・抽象化レイヤーを設けたか
- [ ] 選定したベンダーがソブリンAIプロジェクト評価などの政策変数にさらされているか確認したか
- [ ] トークン単価だけでなく、コンテキスト長、処理量(TPS)、SLAを併せて比較したか

## 関連ドキュメント

> 📄 [ソブリンAI・独自AIファウンデーションモデル政策](../sovereign-fm-policy/)

> 📄 [CSAP (クラウドセキュリティ認証)](../../security/csap/)

> 📄 [網分離とネットワーク隔離 (韓国)](../../security/network-isolation/)

> 📄 [ソブリンランディングゾーン](../../../governance/landing-zone/)

## 参考資料

- [ネイバークラウド、軽量オムニモーダルモデルを公開…「国防環境に最適化」 — 電子新聞](https://www.etnews.com/20260615000237)
- [ネイバー、最上級の言語能力を備えた推論モデル「HyperCLOVA X」 — ネイバークラウド](https://www.navercloudcorp.com/ko/media/pressrelease/view/?seq=33058)
- [次世代ハイブリッドAI、EXAONE 4.0を公開 — LG AI Research](https://www.lgresearch.ai/blog/view?seq=575)
- [LG Reveals Next-Gen Multimodal AI 'EXAONE 4.5' — PR Newswire](https://www.prnewswire.com/news-releases/lg-reveals-next-gen-multimodal-ai-exaone-4-5-302736993.html)
- [カカオ、アップデートされた「Kanana-2」モデル4種をオープンソースで追加公開 — カカオ](https://www.kakaocorp.com/page/detail/11904)
- [カカオ、軽量言語モデル4種をオープンソースで公開…「グローバル水準の性能」 — カカオ](https://www.kakaocorp.com/page/detail/12089)
- [より賢くなったカカオの言語モデルKanana 1.5、商用利用可能なオープンソースとして公開 — tech.kakao.com](https://tech.kakao.com/posts/706)
- [KT、MWC26で「믿:음 K」を公開…エージェンティックAIパートナーを宣言 — アジュ経済](https://www.ajunews.com/view/20260226085637155)
- [Solar Pro 2 — 最先端の推論・ツール活用・多言語性能を備えた310億パラメータLLM — Upstage](https://www.upstage.ai/blog/ko/solar-pro-2-launch)
- [Upstage Releases Next-Generation "Solar Pro" Generative AI LLM on AWS — AWS Press Center](https://press.aboutamazon.com/aws/2024/12/upstage-releases-next-generation-solar-pro-generative-ai-llm-on-aws)
- [「国内元祖LLM『バルコ』、より強力で賢いマルチモーダルとして帰ってきた」…NC AI、「VARCO-VISION 2.0」を公開 — 人工知能新聞](https://www.aitimes.kr/news/articleView.html?idxno=35689)
- [SKテレコム、エイダットエックス4.0知識型モデルをオープンソースで公開 — SKテレコムニュースルーム](https://news.sktelecom.com/213534)
- [GitHub - SKT-AI/A.X-4.0](https://github.com/SKT-AI/A.X-4.0)
