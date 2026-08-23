---
title: "PDPA（個人データ保護法）"
description: "シンガポールPDPAの概要、国境間移転制限と2026年4月のガイド改正、ASEANリージョン設計への示唆、DNCなどの実務上の留意点を整理します。"
---

> 文書基準: 2026年8月

## 概要

PDPA（Personal Data Protection Act、個人データ保護法）は、2012年に制定されたシンガポールの個人データ保護に関する一般法です。個人データ保護委員会（Personal Data Protection Commission、PDPC）が執行機関としての役割を担っており、法律上はIMDA（情報通信メディア開発庁）がPDPCとして指定され、個人情報保護の機能を遂行する構造です。

PDPAは、同意（Consent）、目的制限（Purpose Limitation）、通知（Notification）、アクセス・訂正（Access & Correction）、正確性（Accuracy）、保護（Protection）、保有期間制限（Retention Limitation）、**移転制限（Transfer Limitation）**、責任性（Accountability）、漏えい通知（Breach Notification）などの義務を規定しています。2020年の改正法で導入された**データポータビリティ義務（Data Portability Obligation、Part 6B）**は、まだ施行細則が整備されておらず発効していない状態のため、現時点では遵守義務の対象ではありません。

:::note
漏えい通知義務の届出基準は、(1) 個人に重大な被害（財産上の損失、なりすまし、身体的被害、名誉毀損など）をもたらす、またはもたらす恐れがある場合、(2) 影響を受ける個人が500人以上の場合、のいずれか一方を満たすだけで適用されます。PDPCは、評価完了時点から遅くとも3日以内（営業日ではなく暦日ベース）の届出を期待するとしています。
:::

違反時、PDPCは最大**100万シンガポールドル（S$1M）**、または年間売上高が1,000万シンガポールドル（S$10M）を超える企業の場合は**年間シンガポール売上高の10%**のうち、いずれか大きい金額を課徴金として賦課することができます。

## 国境間移転制限（Transfer Limitation Obligation）

PDPA Part 4に規定された移転制限義務は、組織が個人データをシンガポール国外へ移転しようとする場合、**移転先がPDPAに相当する水準の保護を提供していることを確認するための適切な措置**を講じない限り、移転を禁止するというものです。つまり、データが国境を越える瞬間にも原本と同等の保護水準が維持されなければならないという「同等の保護（comparable protection）」の原則が核心です。

従来から認められている移転メカニズムは次のとおりです。

- 個人による移転への同意
- 契約上の措置（Contractual Clauses）
- 拘束力のある企業規則（Binding Corporate Rules、BCR）
- 個人との契約履行に必要な移転など法定の例外事由
- 大臣がPDPAに準ずる保護水準を備えていると告示した国・地域への移転

### 2026年4月ガイド改正 — CBPR・PRP認証経路の整備

PDPCは**2026年4月14日**、国境間データ移転ガイドを改正して発表しました。これは同時期に施行されたPDPA改正施行規則（PDPA Amendment Regulations 2026）に合わせて規制当局の期待水準を整理したものであり、その核心は、認められる移転メカニズム全体を最新の規定に合わせて再整理したことです。CBPR・PRP認証経路そのものは**2020年6月の認定発表、2021年2月の施行規則への反映により既に存在していたものであり**、今回の改正はこれを含めた全体の体系を整備したものです。

- **APEC CBPR（Cross-Border Privacy Rules、国境間プライバシールール）認証**を保有する移転先組織（個人データ処理者、controllerの性格を持つ）は、移転制限義務の要件を満たしたものとみなされます。
- **APEC PRP（Privacy Recognition for Processors、処理者プライバシー認証）認証**を保有する受託組織（データ仲介者、data intermediaryの性格を持つ）も同様に要件充足として認められます。データ仲介者はCBPRまたはPRPのいずれか一方、あるいは両方を保有すればよいとされています。
- 個別の契約書（SCC類似の条項）を取引ごとに締結・レビューする代わりに、**認証取得のみで国境間移転の法的根拠を確保**する経路が明確に整理されています。

:::caution
CBPR・PRPはAPEC加盟国間でのみ通用する認証体系です。移転先の国・企業がAPEC CBPR/PRP認証システムに参加していない場合は、引き続き契約上の措置やBCRなど従来のメカニズムを活用する必要があります。韓国はAPEC CBPRシステムの参加国であるため、韓国リージョン・韓国所在の関連会社とのデータ移転設計において、この認証経路の実益を検討する価値があります。
:::

## ASEANリージョン設計における実務上の示唆

- **シンガポールは開放型の移転政策を採用しています。** インドネシア・ベトナムなど近隣国がデータローカライゼーション（国内保存義務）を強化する傾向にあるのとは対照的に、シンガポールは「同等の保護が確認されれば移転を許可する」という原則ベースのアプローチを維持しています。したがって、シンガポールをASEANのデータハブとして活用しつつ、個別の進出国のローカライゼーション規制は別途確認する必要があります。
- **リージョンアーキテクチャ設計時に移転メカニズムを事前に確定してください。** 韓国本社・シンガポールリージョン・第三国関連会社の間でデータが行き来するマルチリージョン構造の場合、区間ごとに契約上の措置・CBPR/PRP認証・同意のいずれのメカニズムを適用するかを、データフロー図の段階であらかじめ設計しておくと監査対応が容易になります。
- **認証ロードマップを早期に検討してください。** CBPR/PRPは自己宣言型の認証ではなく、APECが認可した責任機関（Accountability Agent）の審査を経る必要があるため、取得までに相当のリードタイムを要します。ASEAN複数国への進出を計画している場合は、契約ベースのアプローチと並行して認証取得を早期に検討する方が有利です。
- **PDPAには域外適用の余地があります。** シンガポールに所在していなくても、シンガポール国内の個人データを収集・処理する海外企業（例: シンガポールの顧客を対象としたSaaS）にはPDPAが適用され得るため、単に「リージョンをシンガポールに置いていない」という理由だけで適用対象外と断定してはなりません。

## DNC（Do Not Call）などの実務上の留意点

PDPAには、個人データ処理義務とは別に**DNC（Do Not Call）条項**が含まれています。個人は自身のシンガポールの電話番号を、次の3つの登録簿のうち1つ以上に登録することで、特定の種類のマーケティング連絡を拒否できます。

- No Voice Call Register（音声通話の受信拒否）
- No Text Message Register（テキストメッセージの受信拒否）
- No Fax Message Register（ファックスの受信拒否）

組織がシンガポールの電話番号（携帯電話・固定電話・住居用・事業用を含む）宛てにマーケティング目的の音声通話・テキストメッセージ・ファックスを送信しようとする場合、**明示的な同意を得ているか、PDPA上の例外・除外事由に該当しない限り**、事前にDNC登録簿を照会し、対象者が登録されているかを確認する必要があります。登録済みの番号に連絡した場合は違反とみなされ、PDPCに通報される可能性があります。

:::note
DNC照会義務は、B2Cマーケティングキャンペーン、コールセンターのアウトバウンド、テキストメッセージによるプロモーションなど、シンガポールの顧客を対象としたマーケティングチャネルを運営する海外企業（特にEコマース・フィンテック・SaaS）において、実務上見落とされがちな項目です。CRM・マーケティングオートメーションのパイプラインにDNC照会ステップを組み込むことを推奨します。
:::

## 責任性の証明 — DPTM（Data Protection Trustmark）認証

PDPCとIMDAが共同開発した**DPTM（Data Protection Trustmark）**は、組織のPDPA遵守水準と個人データガバナンスの成熟度を第三者が検証する任意の認証制度です。2025年にはシンガポール標準**SS 714:2025**として編入され、国家標準としての位置づけが強化されました。

- 法定義務ではありませんが、認証を通じてガバナンス・責任性・顧客対応体制を対外的に証明できるため、**B2B契約や政府調達のベンダーデューデリジェンス段階で加点要素**として機能することが多くあります。
- シンガポールに現地法人・子会社を置き、消費者向けサービスを運営する海外企業であれば、PDPAの責任性（Accountability）義務を履行する手続きの一つとしてDPTM取得を検討できます。
- 認証はPDPC・IMDAが認可した認証機関が実施し、組織全体（enterprise-wide）または特定の事業単位を単位として範囲を選択できます。

## 参考資料

- [Individual's Guide to the Do Not Call (DNC) Registry — PDPC](https://www.pdpc.gov.sg/individuals/e-services/how-to-register-with-the-do-not-call-dnc-registry-for-individuals/individuals-guide-to-the-do-not-call-dnc-registry)
- [Organisation's Guide to Singapore's Do Not Call (DNC) Provisions — PDPC](https://www.pdpc.gov.sg/about/do-not-call-registry/do-not-call-registry-for-organisations/organisations-guide-to-singapores-do-not-call-dnc-provisions)
- [The Transfer Limitation Obligation — PDPC](https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/advisory-guidelines/the-transfer-limitation-obligation---ch-19-(270717).pdf)
- [Data Protection Trustmark (DPTM) Certification — IMDA](https://www.imda.gov.sg/how-we-can-help/data-protection-trustmark-certification)
- [Accountability Within Industry — PDPC](https://www.pdpc.gov.sg/help-and-resources/2021/09/accountability/accountability-within-industry)
- [Fintech Singapore: PDPA Cross-border Data Transfers (2026) — Global Law Experts](https://globallawexperts.com/pdpa-crossborder-data-transfers-fintech-singapore-2026/)
- [Data Protection & Privacy 2026 - Singapore — Chambers and Partners](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/singapore/trends-and-developments)
- [Data Protection Laws and Regulations 2026 | Singapore — ICLG](https://iclg.com/practice-areas/data-protection-laws-and-regulations/singapore/)
