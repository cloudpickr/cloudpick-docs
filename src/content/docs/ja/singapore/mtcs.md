---
title: "MTCS（マルチティア・クラウドセキュリティ標準）"
description: "シンガポールMTCS（SS 584）クラウドセキュリティ標準の等級体系、運営機関、ハイパースケーラーの認証状況、金融業界の追加要件を整理します。"
---

> 文書基準: 2026年8月

## 概要

MTCS（Multi-Tier Cloud Security、マルチティア・クラウドセキュリティ）は、シンガポール標準**SS 584**として制定されたクラウドセキュリティ認証制度です。情報通信技術標準委員会（Information Technology Standards Committee、ITSC）が開発し、情報通信メディア開発庁（Infocomm Media Development Authority、IMDA）とエンタープライズ・シンガポール（Enterprise Singapore）が支援しており、複数の等級でクラウドセキュリティレベルを区分した世界初の多段階クラウドセキュリティ標準として紹介されています。

2013年の初制定以降、SS 584:2015を経て、現在の基準となる最新版は**SS 584:2020**です。ISO/IEC 27001:2013との整合性を強化し、ゼロトラスト・継続的モニタリングなど最新のセキュリティ概念に対する統制項目を追加しました。

認証は、シンガポール認定委員会（Singapore Accreditation Council、SAC）が認可したMTCS認証機関（Certifying Body、CB）が審査を行い、有効期間は3年で、毎年サーベイランス（事後管理）審査を受けなければ維持されません。

:::note
MTCSは、法律上強制される単一の参入障壁というよりも、**公共調達および金融業界のベンダーデューデリジェンスで広く求められる要件**として機能する国家標準（SS 584）に基づく認証体系です。IMDAが発注する政府クラウド調達（Government Commercial Cloudなど）では、MTCS認証が要求事項として明記されるのが一般的です。
:::

## 等級区分（Level 1〜3）

| 等級 | 対象ワークロード | 特徴 |
| --- | --- | --- |
| **Level 1** | ウェブサイトホスティング、テスト・開発環境、シミュレーションなど非重要業務 | 最小限の基本セキュリティ統制のみを要求する低コストの等級 |
| **Level 2** | 大多数の企業の一般業務システム、ミッションクリティカルなアプリケーションを含む | データセキュリティの脅威に対応するより強化された統制セット。商用クラウドを利用する企業の大半が目標とする等級 |
| **Level 3** | 規制産業、政府調達対象システム、機微・高影響データを処理するシステム | Level 1・2の統制に加え、厳格な追加統制を要求。**高リスク・機密性の高いシステムを対象とした政府調達でLevel 3が求められることが多い（すべての政府調達に一律適用されるわけではない）** |

3つの等級はいずれもサービス種別（IaaS/PaaS/SaaS）ごとに個別の認証範囲を指定できるため、ベンダーが自社サービスの一部のみを特定の等級で認証取得しているケースも珍しくありません。導入検討時には等級だけでなく、**認証範囲（どのサービス・リージョンが含まれるか）**を必ず確認する必要があります。

## IMDA運営体制

- **ITSC（情報通信技術標準委員会）**がSS 584標準そのものを制定・改定し、IMDAとエンタープライズ・シンガポールがこれを支援します。
- **SAC（シンガポール認定委員会）**が審査を行う認証機関（CB）を認可します。CBは国際認証機関（BSI、DNV、TÜV、Ernst & Young Certify Pointなど）が多数を占めます。
- 認証取得後は**3年周期の更新＋毎年のサーベイランス審査**を通じて認証状態を維持する必要があり、審査に不合格となった場合は認証が停止・取消される可能性があります。
- IMDAはMTCS認証済みクラウドサービスの一覧と認証書（QRコード付き）を公式ウェブサイトに掲載し、調達担当者が検証できるようにしています。

## ハイパースケーラー認証状況（2026年8月時点）

| ベンダー | 認証等級 | 備考 |
| --- | --- | --- |
| AWS | Level 3（SS 584:2020） | 2014年に業界初のLevel 3を取得。2024年12月にSS 584:2020基準へ更新し、認証範囲をアジアパシフィック（シンガポール）、アジアパシフィック（ソウル）、米国リージョンまで拡大 |
| Microsoft Azure | Level 3 | IaaS・PaaSに対してLevel 3認証を、世界初となる3つのサービス分類（IaaS/PaaS/SaaS）すべてで取得したCSPとして紹介される。Microsoft 365（Office 365）も2021年にSS 584:2020基準でLevel 3認証を別途取得 |
| Google Cloud | Level 3（Tier 3） | Google CloudおよびGoogle Workspaceのサービス・データセンターサイトの一部を対象にTier 3認証を取得 |
| Oracle Cloud Infrastructure（OCI） | Level 3 | シンガポール・日本リージョンを対象にLevel 3認証を取得。Oracle Fusion Cloud Applications Suiteも2021年12月に別途Level 3認証を取得 |

主要ハイパースケーラー4社はいずれも、少なくとも一部のサービス・リージョンについてMTCS Level 3認証を保有しています。ただし認証範囲はベンダーごとに異なるため、実際に利用しようとするサービスとリージョンが認証書に明記された範囲（スコープ）に含まれるかを、契約前に必ず確認する必要があります。

## 金融業界の追加要件

シンガポールの金融業界でクラウドを導入するには、MTCS認証だけでは不十分であり、シンガポール通貨庁（Monetary Authority of Singapore、MAS）が提示する別のフレームワークを併せて満たす必要があります。

- **MAS TRMガイドライン（Technology Risk Management Guidelines）** — 2021年1月改定版では、金融機関（FI）によるクラウド・API・アジャイル開発の活用拡大に対応し、第三者（アウトソーシング）プロバイダーに対する監督強化を明示的に求めています。法的拘束力のないガイドラインですが、MASの検査時には事実上の遵守基準として機能します。
- **MAS Notice 655（サイバー・ハイジーン、Cyber Hygiene）** — TRMガイドラインとは別に法的拘束力を持つ通知であり、最低限のセキュリティベースラインを規定します。
- **OSPAR（Outsourced Service Provider's Audit Report）** — シンガポール銀行協会（Association of Banks in Singapore、ABS）が制定した監査フレームワークであり、外部監査人がクラウドなどのアウトソーシングサービスプロバイダーの統制をABSガイドライン基準で検証した報告書です。金融機関はこのOSPAR報告書を受け取り、自社のベンダーデューデリジェンス資料として活用します。2024年3月に公開された**OSPAR v2.0**は2025年1月1日から毎年の監査を要求し、クラウドサービスプロバイダー（IaaS/PaaS/SaaS）に特化した補完統制基準を追加しました。

主要ハイパースケーラーは毎年OSPAR監査報告書を発行し、シンガポールの金融機関顧客が活用できるよう提供しており、この報告書の対象サービス範囲は年々拡大する傾向にあります。

## 公共・金融分野進出時のゲート的性格

- **公共調達**: IMDA傘下の政府クラウド調達体系では、MTCS Level 3認証が事実上の参加条件として機能します。認証を持たないベンダーやサービスは、入札参加自体が制限される可能性があります。
- **金融業界**: MTCS認証は出発点にすぎず、実際の導入可否はMAS TRMガイドラインの遵守状況とOSPAR監査報告書の確保状況によって決まる場合が多く見られます。導入初期段階でベンダーの最新OSPAR報告書を要求し、監査範囲と例外事項を確認する手順を推奨します。
- **グローバル企業進出の示唆**: 自国で既にISO/IEC 27001やSOC 2など国際認証体系に精通しているアーキテクトであっても、シンガポールは独自のクラウドセキュリティ標準（MTCS）と独自の金融業界監査体系（OSPAR）を運用している点に留意する必要があります。国際標準と完全に相互承認されるわけではないため、シンガポールの公共・金融市場進出時には別途の認証・監査取得ロードマップを策定する必要があります。

## 導入前の確認チェックリスト

- **等級と範囲を併せて確認**: ベンダーが提示する認証書において、等級（Level）だけでなく認証対象のサービス一覧・リージョンが、実際に導入しようとするサービスと一致しているかを確認します。IMDA公式ウェブサイトに掲載された認証書（QRコード付き）で有効性をクロスチェックできます。
- **更新周期の追跡**: MTCS認証は3年周期であり、毎年サーベイランス審査を経ます。長期契約を締結する場合は、ベンダーの直近の更新・サーベイランス履歴を契約条件やSLA付属書に反映することを推奨します。
- **金融業界はOSPARを別途要求**: MTCS Level 3認証だけではMAS規制対応が完結しません。ベンダーの最新OSPAR報告書（v2.0基準）を別途確保し、監査範囲・例外事項・統制上の不備（もしあれば）を社内リスク評価に反映する必要があります。
- **公共調達は事前協議**: 政府調達への参加を目指す場合は、IMDA・発注機関との事前協議を通じて、要求される正確な認証等級と範囲を確認することが望ましいです。調達公告ごとに要求水準が異なる場合があります。

## 参考資料

- [Cloud Computing and Services — Infocomm Media Development Authority (IMDA)](https://www.imda.gov.sg/regulations-and-licensing-listing/ict-standards-and-quality-of-service/it%20standards%20and%20frameworks/cloud%20computing%20and%20services)
- [MTCS Tier 3 — AWS Compliance](https://aws.amazon.com/compliance/aws-multitiered-cloud-security-standard-certification/)
- [AWS renews MTCS Level 3 certification under the SS584:2020 standard — AWS Security Blog](https://aws.amazon.com/blogs/security/aws-renews-mtcs-level-3-certification-under-the-ss5842020-standard)
- [Multi-Tier Cloud Security (MTCS) Standard for Singapore — Microsoft Learn](https://learn.microsoft.com/en-us/compliance/regulatory/offering-mtcs-singapore)
- [MTCS — Compliance | Google Cloud](https://cloud.google.com/security/compliance/mtcs)
- [Oracle's MTCS certification creates new opportunities for customers in Singapore — Oracle Cloud Infrastructure Blog](https://blogs.oracle.com/cloud-infrastructure/oracle-mtcs-certification-creates-new-opportunities-for-customers-in-singapore)
- [MAS Enhances Guidelines to Combat Heightened Cyber Risks — Monetary Authority of Singapore](https://www.mas.gov.sg/news/media-releases/2021/mas-enhances-guidelines-to-combat-heightened-cyber-risks)
- [OSPAR (Singapore) — Microsoft Azure Compliance](https://learn.microsoft.com/en-us/azure/compliance/offerings/offering-ospar-singapore)
- [OSPAR — Compliance | Google Cloud](https://cloud.google.com/security/compliance/ospar)
- [ABS OSPAR Guidelines v2.0 — Association of Banks in Singapore](https://abs.org.sg/docs/library/abs-ospar-guidelines-v2-0.pdf)
