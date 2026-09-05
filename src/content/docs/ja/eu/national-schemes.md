---
title: "EU加盟国別クラウドセキュリティスキーム"
description: "ドイツBSI C5、フランスANSSI SecNumCloud、スペインENS、イタリアACNなどEU加盟国のクラウドセキュリティ認証・調達スキームとハイパースケーラーの対応状況を整理します。"
---

> 文書基準: 2026年8月

## 概要

EUレベルで統一されたクラウドセキュリティ認証スキーム(EUCS)がまだ確定していない状況で、各加盟国はそれぞれの国別スキームで公共調達・規制産業のクラウド利用を統制しています。ドイツのBSI C5、フランスのANSSI SecNumCloudが最も成熟し国際的にも参照されるスキームであり、スペインのENSとイタリアのACN体系もそれぞれの方式で自国の公共部門クラウド調達をゲートキーピングしています。本文書は、EU市場に公共・規制産業ワークロードを展開しようとするアーキテクトが、国別に何を準備すべきかを整理します。

:::note
国家スキームは**EU規則(Regulation)ではなく各国の法令・行政手続き**に基づいています。したがって、特定の加盟国で通過した認証が他の加盟国で自動的に認められるわけではなく、スキーム間の相互承認はEUCSなどEUレベルのフレームワークが完成して初めて可能になります。
:::

## ドイツ — BSI C5

**C5(Cloud Computing Compliance Criteria Catalogue)** は、ドイツ連邦情報セキュリティ庁(BSI, Bundesamt für Sicherheit in der Informationstechnik)が運用するクラウドセキュリティ準拠基準カタログです。

- **C5:2020**: 121の基準で構成され、2020年以降事実上ドイツの標準クラウドセキュリティ監査基準として定着しました。ENISAがEUCS Substantial等級の要件を設計する際、C5:2020を基礎資料としました。
- **C5:2026**: 2026年4月初旬(一部報道では3月末とも)に最終版が公開された改訂版で、C5:2020の基準を継承しつつ168の基準(17領域)へと細分化・拡張しました。**新基準は2027年6月1日から始まる評価期間から拘束力を持ち**、それ以前の早期適用も認められます。
- **調達上の位置づけ**: C5は法律ではないため違反しても直接的な法的制裁はありませんが、**ドイツ連邦機関向けのクラウド調達ではC5準拠が事実上必須の要件**です。金融・ヘルスケアなどの規制産業でも、ベンダー選定時にC5準拠の有無を標準的に求めます。
- **ハイパースケーラーの対応**: AWS、Microsoft Azure、Google Cloud、SAP、IONOSなどがC5準拠確認書(attestation)を保有しており、主要ベンダーは毎年監査を更新しています。

## フランス — ANSSI SecNumCloud

**SecNumCloud**は、フランス国家サイバーセキュリティ庁(ANSSI, Agence nationale de la sécurité des systèmes d'information)が発行するクラウドサービス資格(qualification)です。現行基準は**バージョン3.2**(2022年改訂)で、360以上の技術・運用要件をPASSI(ANSSI承認監査機関)が審査します。

### 主権要件が核心的な差別化ポイント

SecNumCloud 3.2が他の国別スキームと最も大きく異なる点は、**資本・支配構造の主権要件**です。

- 本社がフランスまたはEU域内にあること
- EU域外の持分は個別株主基準で24%、合算基準で39%を超えられないこと
- サービスに排他的にEU法のみが適用されること(米国CLOUD Act・FISA 702など域外法によるデータアクセス要求からの遮断)

:::caution
この要件のため、**AWS・Microsoft・Googleなど米国系ハイパースケーラーは自社名義でSecNumCloud資格を直接取得することができません。** 代わりに、これらの企業はフランスのパートナーとの合弁会社を通じた迂回経路を取っており、その進捗状況はベンダーごとに異なります(下記「パートナーシップによる認証取得状況」を参照)。
:::

### パートナーシップによる認証取得状況 (2026年7月時点)

| パートナーシップ | ベンダー | 状況 |
| --- | --- | --- |
| **S3NS** (Thales × Google Cloud 合弁会社) | Google Cloud | **2025年12月17日にSecNumCloud 3.2資格を取得** — PREMI3NSサービスでIaaS・CaaS・PaaSの20以上のサービスを同時に認証取得した最初の事例。2026年上半期中にCloud Run・Cloud Build・Cloud Spanner・Bigtableなどを含む第2次拡張審査を実施中 |
| **Bleu** (Capgemini × Orange 合弁会社) | Microsoft Azure/M365 | 審査第1段階(J0、申請受理)を通過し、2026年上半期の資格取得を目標に審査を進行中。**2026年8月時点で完全なSecNumCloud 3.2資格はまだ取得していない** |

全体として2026年7月時点で**9～10社**(OVHcloud、3DS Outscale、Cloud Temple、Orange Business、Cegedim.cloud、Worldline、Oodrive、Whaller、S3NSなど — 集計基準によって異なり、ANSSI公式カタログのサービス種別ごとの集計では10社の事業者名まで確認されている)がSecNumCloud 3.2資格を保有しており、Bleu・Scaleway・NumSpotなど**12社**が審査中です。

## スペイン — ENS

**ENS(Esquema Nacional de Seguridad、国家セキュリティ体系)** は、王令(Royal Decree)311/2022に基づきスペイン公共部門の情報システムに要求されるセキュリティフレームワークで、**基本(Basic)・中間(Medium)・上位(High)** の3段階で構成されます。

- スペイン公共機関と契約しようとするクラウドベンダーは、取り扱う情報の機微度に応じて該当等級のENS認証を求められます。
- **ハイパースケーラーの対応**: AWS(174サービス、31リージョン対象のENS High更新認証)、Microsoft Azure(BDO監査によるENS High準拠確認)、Google Cloud(Google Cloud・Google WorkspaceのENS High認証)がいずれも**最高等級であるENS High認証を保有**しています。これは資本主権要件を課すSecNumCloudとは異なり、ENSが技術・運用セキュリティ統制中心のスキームであるためです。

## イタリア — ACNと国家戦略クラウド(PSN)

イタリアはドイツ・フランスと異なり、**認証型スキームと物理的なソブリンインフラを組み合わせた**二元構造を取ります。

1. **ACNクラウド資格分類(qualificazione)**: 2023年1月19日からサイバーセキュリティ庁(ACN, Agenzia per la Cybersicurezza Nazionale)がAgIDから業務を引き継ぎ、公共部門向けクラウドサービスの資格分類を担当しています。機密性・完全性・可用性への影響度を評価するアンケート方式の手続きで、公共機関が利用するクラウドサービス・インフラのリスク等級を分類します。「Strategia Cloud Italia」の一環として、イタリア公共行政の約75%を資格分類されたクラウドへ移行することが目標です。
2. **PSN(Polo Strategico Nazionale、国家戦略クラウド)**: 最高水準の信頼性・レジリエンスが求められる公共ワークロードのための物理的なソブリンインフラです。「Public Cloud PSN Managed」構成を通じて、ハイパースケーラープラットフォームをPSNデータセンター内の公共行政専用リージョンに組み込み、レガシー移行が必要な機関も段階的に移行できるようにしています。**2026年7月21日時点で280以上の中央行政機関・地域保健機構・病院機関がPSNへの移行を完了**しました(PNRR目標達成)。

:::note
イタリアモデルでは、ハイパースケーラーがACNから**ドイツC5・フランスSecNumCloud方式の個別資格を直接取得する**というより、**PSNというイタリアの管理下にある物理的ゲートウェイを通じてサービスを提供する**方式に近いといえます。個別サービス単位の認証範囲については、ベンダー・PSNの公式発表で別途確認が必要です。
:::

## EUCSとの関係 — 統合議論は進行中

上記4つの国別スキームはそれぞれ独自に運用されていますが、EUレベルの**EUCS(European Cybersecurity Certification Scheme for Cloud Services)** が完成すれば、相互承認の基礎になると見込まれています。

- C5:2020は、EUCS Substantial等級要件の設計基礎資料として既に反映されています。
- EUCSの作業は、最高等級(High+)の「主権性要件」を含めるかどうかをめぐる加盟国間の意見対立で数年間停滞していましたが、2026年1月20日に発表された**Cybersecurity Act 2(CSA2)** 改正の流れの中で再開されつつあります。
- **2026年8月現在、EUCSは依然として確定しておらず、主権性要件を含めるかどうかは議論が続いています。**(詳しい経緯は[GDPRとデータ主権 — EUCS認証スキームの流動性](../gdpr-sovereignty/#eucs認証スキームの流動性)を参照)

それまでの間、国別スキームは「暫定的だが市場で信頼される証跡」として機能しており、特にBSI C5とSecNumCloudはEUCS移行期の事実上の基準として参照されています。

## 国別調達ゲート — まとめ

国別スキームは、認証そのものが目的ではなく**公共・規制産業調達の通過要件**として機能する点が共通しています。ただし、ゲートの性格は国によって異なります。

| 国 | スキーム | 性格 | ハイパースケーラーの直接取得可否 |
| --- | --- | --- | --- |
| ドイツ | BSI C5 | 技術・運用統制監査(資本要件なし) | 可能 — AWS・Azure・Google Cloudなど取得済み |
| フランス | SecNumCloud 3.2 | 技術・運用統制 + **資本・支配構造の主権要件** | 不可 — パートナーシップ(S3NSは取得済み、Bleuは審査中)経由が必要 |
| スペイン | ENS (Basic/Medium/High) | 技術・運用統制監査(資本要件なし) | 可能 — AWS・Azure・Google CloudいずれもENS High取得 |
| イタリア | ACN資格分類 + PSN | アンケート方式の等級分類 + 物理的ソブリンインフラの組み合わせ | PSNパートナーシップ経由方式 |

## 実務上の示唆

- **国ごとに個別の検討が必要です。** EU単一認証が存在しない現状では、「EU進出」を単一要件として一括りにせず、対象加盟国(公共調達の相手先・規制当局)ごとに求められるスキームを個別に確認する必要があります。
- **フランス向けワークロードはベンダー選択自体が制約されます。** フランス公共機関・重要インフラ事業者(OIV/OSE)向けの機微データを扱う場合、SecNumCloud資格を直接保有している(S3NSなど)か取得が間近なベンダーへと選択肢が絞られます。Bleuのように審査中のオプションについては、**完全な資格取得時期を契約・移行スケジュールの前提にしないよう**注意が必要です。
- **ドイツ・スペインは相対的にハイパースケーラーの選択の幅が広いです。** 資本主権要件のないこの2つのスキームでは、既に主要ベンダーが最高等級の認証を保有しているため、ベンダー選定よりも認証範囲(サービス一覧)とリージョンカバレッジの確認が実務の要点となります。
- **イタリアは認証書ではなくインフラ経路を確認する必要があります。** ACN資格分類等級と併せて、ワークロードがPSN経由で提供されるか、その場合に運用統制・SLAがどう変わるかを、ベンダー・PSNの公式文書で確認します。
- **国別スキームをEUCS確定までの暫定的な代替手段として活用しつつ、固定前提として設計しないでください。** EUCSが最終確定すれば相互承認の範囲や要件が変わる可能性があるため、特定の国別スキームのみに依存するアーキテクチャよりも、転換の余地を残した設計の方が安全です。

## 参考資料

- [BSI — C5紹介](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/C5_Einfuehrung/C5_Einfuehrung_node.html)
- [BSI — C5:2026カタログ](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/C5_2025/C5_2025_node.html)
- [cyber.gouv.fr — SecNumCloud (ANSSI)](https://cyber.gouv.fr/)
- [Thales — S3NS SecNumCloud資格取得発表 (2025.12)](https://www.thalesgroup.com/en/news-centre/press-releases/s3ns-announces-secnumcloud-qualification-premi3ns-its-trusted-cloud)
- [Bleu — SecNumCloud 3.2 J0審査通過のお知らせ](https://www.bleucloud.fr/bleu-valide-le-j0-de-la-qualification-secnumcloud-3-2/)
- [AWS — Esquema Nacional de Seguridad(ENS) 準拠](https://aws.amazon.com/compliance/esquema-nacional-de-seguridad)
- [Google Cloud — ENS準拠](https://cloud.google.com/security/compliance/ens)
- [ACN — Strategia Cloud Italia / クラウド資格分類](https://www.acn.gov.it/en/strategia/strategia-cloud-italia/qualificazione-cloud)
- [Polo Strategico Nazionale 公式サイト](https://www.polostrategiconazionale.it/en/)
- [ENISA — EUCS候補スキーム](https://certification.enisa.europa.eu/)
- [ANSSI — SecNumCloud認証・資格カタログ](https://messervices.cyber.gouv.fr/visas/catalogue-produits-services-profils-de-protection-sites-certifies-qualifies-agrees-anssi.pdf)
