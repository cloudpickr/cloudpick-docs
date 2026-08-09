---
title: "AIガバナンス"
description: "シンガポールAIガバナンス体系 — NAIS 2.0国家AI戦略、Model AI Governance Framework、AI Verify、IMDAのツール中心アプローチ、PDPAとの関係、ASEAN・東南アジア連携を整理します。"
---

> 文書基準: 2026年8月

## 概要

シンガポールのAIガバナンスは、**単一の包括的AI法律を制定する代わりに、既存法制(PDPAなど)の上に自律遵守型フレームワークと実務ツールを重ねる方式**で設計されています。情報通信メディア開発庁(Infocomm Media Development Authority、IMDA)と個人情報保護委員会(PDPC)が共同で政策を主導しており、国家戦略(NAIS)・ガバナンスフレームワーク(Model AI Governance Framework)・テスティングツール(AI Verify)の3段階が相互補完的に機能しています。

:::note
シンガポールはEU AI法のようにリスク等級別の法的義務を課す方式ではなく、「規制よりもツール(tools over regulation)」を標榜しています。AI自体を規律する単一の法律は2026年8月時点で存在せず、既存のPDPA・部門別法律(金融規制など)がAI活用にも適用される構造です。
:::

## NAIS・NAIS 2.0 — 国家AI戦略

シンガポールは2019年に最初の国家AI戦略(National AI Strategy、NAIS)を発表し、**2023年12月**「AI for the Public Good, for Singapore and the World」を副題とした**NAIS 2.0**を発表して範囲を大きく拡大しました。その後**2026年5月20日**、NAIS 2.0以降の成果を踏まえた**10大更新優先課題**が発表されました。

- 国家AIミッション(製造・金融・通信・ヘルスケア分野)を通じた産業転換と全分野でのAI導入の主流化
- 政府全体にわたるAI内在化を通じた公共部門イノベーション
- AI研究能力全般の構築とバイリンガルAI人材の育成・海外研究者誘致
- 包摂的成長のための全国民の基礎AIリテラシー拡大
- 資源効率的なAI開発とコンピューティングインフラアクセス性の拡大(ワンノース地区**Kampong AI**、国家スーパーコンピューティングセンター**ASPIRE 2B**など)
- ガバナンス・社会的信頼を通じた安全なAI導入の促進とASEAN域内AIハブとしての地位強化(シンガポールは2027年ASEAN議長国)

**2025~2030年の公共AI研究・人材開発に総額10億シンガポールドル(S$1B)以上**が投入され、**2026年2月**にはローレンス・ウォン(Lawrence Wong)首相が議長を務める**国家AI委員会(National AI Council、NAIC)**が新設され、国家AIアジェンダの戦略的方向性を統括します。

## Model AI Governance Framework — 生成AI版(2024)

IMDA・PDPCは2019年に**Model AI Governance Framework**(従来型AI対象、民間企業の責任あるAI展開のための自発的参考文書)を世界経済フォーラム(WEF)ダボス会議で初めて発表し、2020年に改訂しました。生成AI(Generative AI)の急速な普及に対応し、IMDAと**AI Verify Foundation**は**2024年1月16日に草案(提案版)**を公開し、業界の意見聴取を経て**2024年5月30日に最終版**である**Model AI Governance Framework for Generative AI**を発表しました。

このフレームワークは、生成AI特有のリスク(幻覚、著作権、ディープフェイクなど)に対応するための**9つの次元(dimension)**を提示します。

| 次元 | 核心内容 |
| --- | --- |
| 責任性(Accountability) | 利害関係者が責任を持って行動するようにするインセンティブ構造 |
| データ(Data) | 学習データの品質管理・ガバナンス |
| 信頼できる開発・展開 | 安全性の実践に対する透明性 |
| インシデント報告(Incident Reporting) | 迅速な通知と是正体系 |
| テスティング・保証(Testing and Assurance) | 第三者検証と標準化されたテストプロトコル |
| セキュリティ(Security) | AI特有の新たな脅威ベクトルへの対応 |
| コンテンツの出所(Content Provenance) | 生成コンテンツの出所の透明性 |
| 安全性・アラインメントR&D | モデルアラインメント(alignment)に関する国際協力 |
| 公共善のためのAI | アクセス性の拡大と持続可能な開発 |

フレームワークは、「単一の介入だけでは既存・新規のAIリスクに対応するには不十分である」という前提の下、実務ガイドラインとして段階的に具体化されうる**初期実行段階**を提示する性格を持ちます。法的拘束力のない自発的参考文書です。

## Model AI Governance Framework — エージェンティックAI版(2026)

生成AI版の発表以降、エージェンティック(Agentic)AIの普及に対応し、IMDAは**2026年1月22日**、エージェンティックAIに特化した**Model AI Governance Framework for Agentic AI**を新たに発表しました。これは、AIシステムが自ら計画を立てて行動を実行するエージェンティックワークフローで生じる責任所在・権限委譲・モニタリングに関するガバナンス課題を扱うもので、既存の生成AI版フレームワークを補完します。2026年8月の文書基準日時点で最新のガバナンスフレームワークを確認しようとする組織は、生成AI版とエージェンティックAI版を併せて参照する必要があります。

## AI Verify — テスティングフレームワークと財団

**AI Verify**は、IMDA・PDPCが**2022年5月**MVPとして国際パイロットに公開したAIガバナンステスティングフレームワーク・ソフトウェアツールキットで、**2023年6月**にオープンソースへ転換されました。これと併せてIMDAは**2023年6月**、オープンソースコミュニティ運営を専担する独立した非営利財団**AI Verify Foundation**を発足させました(法的にはIMDAの子会社ではなく、別個の非営利法人です)。

AI Verifyテスティングフレームワークは、以下の**11のAIガバナンス原則**を基準にAIシステムを評価します。

透明性、説明可能性、反復可能性(Repeatability)、安全性、セキュリティ、堅牢性(Robustness)、公正性、データガバナンス、責任性、人間の関与と監督(Human Agency and Oversight)、包摂的成長・社会的・環境的ウェルビーイング。

この原則体系は、EU・G7・OECD・米国など主要な国際フレームワーク(米国NIST AI RMF、広島プロセス国際行動規範、ISO/IEC 42001など)とマッピングされ、相互参照が可能なよう設計されています。AI Verify FoundationはAWS・Dell・Google・IBM・Microsoft・Red Hat・Salesforceなどをプレミアメンバーとして擁しており、大規模言語モデル評価ツールキット**Project Moonshot**、実環境生成AIテスト環境である**Global AI Assurance Sandbox**、アジア初の第三者テスト機関認定プログラムである**AI Tester Accreditation Programme**などを運営しています。

## IMDAのアプローチ — 規制よりもツール

シンガポールAIガバナンスの特徴は、**強制的な単一立法の代わりに自律フレームワークと実務ツールを積み上げる方式**です。IMDAはAIを規律する別途の包括的法律を制定せず、既存法(PDPA、部門別規制)に加えてModel AI Governance Framework(自発的参考文書)とAI Verify(自発的テストツール)を通じて、企業が自ら信頼できるAIを構築するよう誘導します。

:::caution
「規制がない」ことと「法的義務がない」ことは異なります。AIシステムが個人情報を処理する場合、PDPA上の義務(同意・目的制限・移転制限など)はそのまま適用され、金融業界など規制産業ではMAS(通貨庁)の既存の技術リスク管理規制がAI活用にも適用されます。「AI専用の法律がない」を「AIに規制が適用されない」と誤解してはいけません。
:::

## PDPAとAIの関係

PDPCは**2024年3月1日**、「AI推薦・意思決定システムにおける個人情報活用に関するアドバイザリーガイドライン(Advisory Guidelines on Use of Personal Data in AI Recommendation and Decision Systems)」を発表しました。このガイドラインは新たな義務を新設するものではなく、**既存のPDPA義務(同意、告知、正確性、責任性など)がAIを活用した推薦・意思決定システムにどのように適用されるか**を具体的に解説する文書です。個人情報を学習・推論に活用するAIシステムを運用する組織は、PDPA上の目的制限・告知義務をAIパイプライン設計段階から反映すべきであることを明確にしました。

つまりシンガポールでは、AIガバナンスと個人情報保護は別トラックではなく、**PDPAがAIシステムにもそのまま適用される基盤法制**であり、Model AI Governance Framework・AI Verifyはその上に重なる自発的補完装置であるという構造で理解する必要があります。

## ASEAN AIガバナンスガイドとの連携

シンガポールIMDAは、**ASEAN AIガバナンス作業部会(ASEAN Working Group on AI Governance、WG-AI)**を2024年から議長国として率いています。この作業部会の成果物が**「ASEAN Guide on AI Governance and Ethics」**で、ASEAN加盟国が従来型AI技術を設計・開発・展開する際に参考にできる域内整合(regional alignment)フレームワークです。2025年には生成AIを包含するよう**拡張版(Generative AI付属書)**が整備されました。

シンガポールのModel AI Governance Frameworkが事実上ASEANガイドの原型(prototype)の役割を果たしており、IMDAが国家レベルのフレームワークを地域レベルへ拡散させる構造です。ASEAN域内の多国にサービスを提供する企業であれば、シンガポールのフレームワークを遵守することが他のASEAN加盟国の政策方向とも相当程度整合する可能性が高いといえます。

## 東南アジア地域モデル — SEA-LION

国家AI戦略の研究・インフラ軸を代表する事例が**SEA-LION(Southeast Asian Languages In One Network)**です。国立研究財団(National Research Foundation)の支援を受け、シンガポール国立大学(NUS)が主管する国家プログラム**AI Singapore**が開発したオープンソース多言語・マルチモーダル言語モデル系列で、東南アジア11以上の言語の言語的・文化的ニュアンス(低資源言語を含む)を反映するよう設計されています。最新版である**SEA-LION v4.5**はエージェント的機能と推論効率を高めたカスタムスペキュレイティブデコーダーを搭載しており、東南アジアの文化的文脈に合わせた安全性フィルタリングモデル群**SEA-Guard**も併せて提供されます。

SEA-LIONは、西側諸国で開発された汎用LLMに全面的に依存せず、東南アジアの言語・文化的文脈を反映した自国・域内モデル能力を確保しようとするシンガポールの国家戦略を象徴するプロジェクトとして評価されています。

## 実務上の示唆

- **AI専用法がないからといってコンプライアンス負担がないわけではありません。** シンガポールでAIサービスを運用しようとする韓国企業は、PDPA(個人情報)、金融業界であればMAS規制など既存法制をAIパイプラインに合わせて再解釈する必要があり、PDPCのAI推薦・意思決定システムガイドラインが実務チェックリストとして有用です。
- **AI Verifyを自律規制準備ツールとして活用できます。** 法的義務ではありませんが、AI Verifyテスティングフレームワークで自社のAIシステムを事前評価しておけば、今後他国のAI規制(例: EU AI法)への対応時にも国際フレームワークのマッピングを活用して履行負担を軽減できます。
- **シンガポールのフレームワークはASEAN進出の参考点になります。** ASEAN域内の複数国にAIサービスを提供する計画があれば、シンガポールのModel AI Governance FrameworkとASEAN Guide on AI Governance and Ethicsを併せて検討し、域内の共通分母を把握するのが効率的です。
- **SEA-LIONなど東南アジア特化モデルの活用を検討する価値があります。** 東南アジアの低資源言語・文化的文脈が重要なサービス(顧客対応、コンテンツローカライゼーションなど)であれば、西側汎用LLMの代わりにSEA-LION系列モデルをベンチマークに含め、性能・コストを比較することを推奨します。

## 参考資料

- [National AI Strategy — Smart Nation Singapore](https://www.smartnation.gov.sg/initiatives/national-ai-strategy/)
- [Update to Singapore's National AI Strategy: Refreshed Priorities to Harness AI for the Public Good — Ministry of Digital Development and Information (MDDI)](https://www.mddi.gov.sg/newsroom/update-to-singapore-s-national-ai-strategy--refreshed-priorities-to-harness-ai-for-the-public-good-factsheet/)
- [Model AI Governance Framework for Generative AI — AI Verify Foundation](https://aiverifyfoundation.sg/resources/mgf-gen-ai/)
- [New Model AI Governance Framework for Agentic AI — IMDA (2026年1月22日)](https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2026/new-model-ai-governance-framework-for-agentic-ai)
- [AI Verify Foundation — 紹介およびテスティングフレームワーク](https://aiverifyfoundation.sg/)
- [Singapore's Approach to AI Governance — PDPC](https://www.pdpc.gov.sg/organisations/resources/guidance-by-topic/singapores-approach-to-ai-governance)
- [Advisory Guidelines on Use of Personal Data in AI Recommendation and Decision Systems — PDPC](https://www.pdpc.gov.sg/organisations/regulations-decisions/regulatory-guidance/advisory-guidelines-on-use-of-personal-data-in-ai-recommendation-and-decision-systems)
- [ASEAN Working Group on AI Governance — IMDA](https://www.imda.gov.sg/about-imda/international-relations/asean-working-group-on-ai-governance)
- [ASEAN Guide on AI Governance and Ethics — ASEAN](https://asean.org/book/asean-guide-on-ai-governance-and-ethics/)
- [SEA-LION — AI Singapore](https://sea-lion.ai/)
- 個人情報保護一般義務は[PDPA (個人情報保護法)](../pdpa/)を、政府システムのAI導入コンテキストは[政府クラウド](../government-cloud/)を参照してください。
