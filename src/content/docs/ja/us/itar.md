---
title: "ITAR/EAR"
description: "防衛・航空宇宙の技術データに関する輸出管理規定ITAR/EARがクラウドアーキテクチャに持つ意味と、FedRAMPとの違いを整理します。"
---

> 文書基準: 2026年8月

## 概要

ITAR(International Traffic in Arms Regulations)とEAR(Export Administration Regulations)は米国の輸出管理規定であり、防衛・航空宇宙・デュアルユース(dual-use)技術が国外に流出することを規制します。

- **ITAR**: 国務省(State Department)傘下のDDTC(Directorate of Defense Trade Controls)が所管し、USML(United States Munitions List)に掲載された防衛物資・サービス・技術データを規律します。
- **EAR**: 商務省(Commerce Department)傘下のBIS(Bureau of Industry and Security)が所管し、商用・デュアルユース品目・技術(先端半導体、暗号化ソフトウェアなど)をECCN(Export Control Classification Number)体系で分類・管理します。

一つの品目・技術はITARまたはEARのいずれか一方にのみ分類され、一般にITARはEARよりもはるかに厳格です。ITAR違反は刑事罰として1件あたり最大100万ドルの罰金および最大20年の懲役に処される可能性があります。EARの刑事罰も同水準（1件あたり最大100万ドル・最大20年の懲役）であり、行政（民事）制裁は1件あたり最大約37万ドル（インフレ調整済み、2025年時点で374,474ドル）または取引額の2倍のいずれか大きい方です。

| 区分 | ITAR | EAR |
| --- | --- | --- |
| **所管機関** | 国務省DDTC | 商務省BIS |
| **対象品目** | 防衛物資・サービス・技術データ(USML) | 商用・デュアルユース品目・技術(ECCN) |
| **登録義務** | 製造・輸出業者の事前登録が必須 | 別途の事前登録要件なし |
| **ライセンス例外** | 非常に限定的 | 相対的に多様な例外が存在 |

:::note
品目・技術がITARとEARのどちらに該当するかを判断すること(Jurisdiction/Classification)は、それ自体が専門的な法律判断の領域です。自社での判断が難しい場合は、DDTCのCJ(Commodity Jurisdiction)手続きや輸出管理専門の弁護士への相談を経るのが安全です。
:::

## US Personsアクセス制限がクラウドに持つ意味

ITARで管理される技術データ(technical data)は、原則として**US Person**(米国市民権者、永住権者、特定の保護対象者、米国内に設立された法人など)のみがアクセスでき、外国人(Foreign Person)がアクセスするにはDDTCの別途の許可(ライセンス、TAAなど)が必要です。これをクラウド環境に適用すると、以下を意味します。

- 別段の例外がない限り、技術データが保存されるサーバーは米国内(CONUS)に置き、運用・保守要員もUS Personに限定することが基本前提です。ただし、§120.54のエンドツーエンド暗号化要件を満たしたデータの国外への移転・保存は「輸出」とはみなされない例外があるため、法律上一律に米国内保存が義務付けられているわけではありません(後述のエンドツーエンド暗号化例外を参照)。
- クラウドコンソールへのログイン、ファイルのアップロード、画面共有などによって外国人が未許可の状態でデータを閲覧することも「輸出」(deemed export)とみなされる可能性があります。
- したがって、IAMポリシーだけで国籍ベースのアクセス統制を完全に実装することは難しく、組織構造(US Person専任チーム・子会社の別途構成)とクラウド環境の選択を併せて設計してこそ、実効性のある統制が可能になります。
- **2020年の暗号化例外規定(End-to-End Encryption Carve-out)**: 2020年3月25日に発効した改正規則によれば、ITAR技術データがFIPS 140-2水準のエンドツーエンド(end-to-end)暗号化で保護され、復号手段(鍵)がクラウドベンダーを含む第三者に提供されない場合、当該データが国外サーバーを経由・保存されても「輸出」とはみなされません。ただし、ベンダーが鍵を保有するサーバー側暗号化(server-side encryption)はこの例外に該当せず、未許可の外国人が平文の状態でデータにアクセスすれば、暗号化の有無にかかわらず輸出とみなされます。中国、ロシア、イラン、北朝鮮などの武器禁輸国は、この例外からも除外されます。

## FedRAMPとの違い

ITARとFedRAMPは性質の異なる別個の要件です。

- FedRAMPはクラウドサービスのセキュリティ統制を評価・認可する**認証プログラム**である一方、ITARは特定の技術データの輸出を規律する**法規制**です。ITARには「ITAR認証」という公式な資格自体が存在せず、遵守責任はデータを扱う企業(輸出者)自身にあります。
- **FedRAMP認可を取得したからといってITARを遵守していることにはなりません。**例えば、FedRAMP ModerateレベルのCUI処理要件を満たしていても、エンドツーエンド暗号化などの追加措置なしにはITAR要件を満たせない場合があります。
- 実務上は、AWS GovCloud、Azure GovernmentのようにITAR対応環境として設計されたリージョンが同時にFedRAMP High認可も保有している場合が多いため、両要件が併せて言及されますが、これはベンダーが両要件を満たすようインフラを設計したためであり、FedRAMP認可自体がITAR遵守を保証するためではありません。ITAR遵守の有無は最終的にデータを扱う企業自身が証明する必要があります。

## GovCloud、GCC Highなどの対応環境

| 環境 | ITAR/EAR対応の特徴 |
| --- | --- |
| **AWS GovCloud (US)** | 米国内の物理的所在地、AWS運用スタッフを米国市民権者に限定。アカウント所有者はUS Personである必要があり、有効なDDTC登録を維持する必要がある。ただし、GovCloud内のアプリケーションユーザー(IAMユーザー)自体が必ずしもUS Personである必要はない — データアクセス統制は顧客が設計 |
| **Microsoft GCC High** | Microsoft 365をAzure Governmentインフラ上に展開した環境。米国内のデータセンター、審査済みの米国市民権者のみアクセス可能。DFARS 252.204-7012、ITAR、EAR、CMMC Level 2/3要件を満たす唯一のMicrosoft 365環境。標準GCC(GCC Highの前段階)はITAR/EARに対応していないため混同しないよう注意 |
| **Google Cloud Assured Workloads (ITAR制御パッケージ)** | 米国リージョンへのデータレジデンシー制限、顧客管理暗号鍵(CMEK)が必須、ITAR関連の技術サポートは米国内のUS Personにルーティング。Premium等級で提供 |
| **OCI Government Cloud** | Oracleの政府専用リージョンで、同様の米国人スタッフ・データレジデンシー統制を提供 |

## 防衛・航空宇宙分野での協業における実務上の留意点

- 海外企業が米国の防衛・航空宇宙プライム企業と技術データをやり取りする場合、米国国籍でない役職員は原則としてForeign Personに該当し、ITAR技術データに直接アクセスすることはできません(例: 米国籍を持たない役職員)。TAA(Technical Assistance Agreement)、MLA(Manufacturing License Agreement)などのDDTC許可を事前に取得するか、米国内のUS Personで構成された別組織・子会社を通じてのみデータを取り扱う体制が必要です。
- クラウドへのアップロード・ダウンロード行為自体が「輸出」とみなされる可能性があるため、コラボレーションツール・ファイル共有サービスの選定時にはITAR対応の有無(GCC Highなど)を先に確認する必要があります。標準的な商用クラウド(GCC、一般Microsoft 365、一般Google Workspaceなど)はITAR技術データの保存には適していません。
- エンドツーエンド暗号化の例外規定を活用すれば、必ずしも米国インフラを使わなくても遵守できる余地がありますが、鍵管理をベンダーではなく自社(または信頼できるUS Person)が全面的に統制する必要があるため、実装難易度は高くなります。導入前に輸出管理専門の法律顧問を受けるのが安全です。
- 同じCUI(統制対象非分類情報)を扱う契約では、ITARとは別にCMMC/NIST SP 800-171要件が併せて課される場合が多くあります。詳細は[FedRAMP](../fedramp/)ドキュメントのCMMC 2.0セクションを参照してください。
- EAR対象のデュアルユース技術(例:先端半導体設計データ、特定の暗号化技術)はITARに比べて相対的に柔軟ですが、依然としてライセンスが必要な場合があるため、データがITAR・EARのどちらに分類されるかを事前に確認する必要があります。
- FedRAMP認可の取得自体を目標とする場合とは異なり、ITAR/EAR対応は別途の「認可取得」プロジェクトではなく、組織のデータ取り扱いプロセス全般(契約、人事、アクセス統制、クラウドアーキテクチャ)にわたる継続的な遵守体制として取り組む必要があります。

:::caution
ITAR/EAR違反は刑事処罰にまで至りうる重大な法的リスクです。本ドキュメントはアーキテクチャ観点の一般的な概要であり、実際の契約・プロジェクトを進める前には必ず輸出管理専門の法律顧問を受ける必要があります。
:::

## 関連ドキュメント

- [コンプライアンス（Compliance）](../../governance/compliance/)
- [網分離とネットワーク隔離](../../security/network-isolation/)

## 参考資料

- [DDTC（ITAR所管機関）](https://www.pmddtc.state.gov/)
- [BIS EAR公式ページ](https://www.bis.gov/)
- [AWS GovCloud ITAR準拠ガイド](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-itar.html)
- [AWS ITARコンプライアンス](https://aws.amazon.com/compliance/itar/)
- [Google Cloud Assured Workloads — ITARデータ境界](https://docs.cloud.google.com/assured-workloads/docs/control-packages/itar)
- [Microsoft GCC High概要](https://learn.microsoft.com/en-us/office365/servicedescriptions/office-365-platform-service-description/office-365-us-government/gcc-high-and-dod)
