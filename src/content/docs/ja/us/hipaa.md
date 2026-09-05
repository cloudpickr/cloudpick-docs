---
title: "HIPAA/HITECH"
description: "米国のヘルスケアデータ保護規制HIPAA/HITECHのPHIの定義、BAA締結の構造、HITRUST CSFとの関係、暗号化・監査ログ要件を整理します。"
---

> 文書基準: 2026年8月

## 概要

:::note[前提知識と関連ドキュメント]
米国のクラウド規制全般は[米国ガイド](../../us/)、データ保護の一般原則は[データ保護](../../security/data-protection/)を先に参照してください。本ドキュメントは、米国のヘルスケア情報保護法制であるHIPAA/HITECHに焦点を当てます。
:::

HIPAA(Health Insurance Portability and Accountability Act、1996年)は米国のヘルスケア情報保護に関する連邦法であり、HHS(保健福祉省)傘下のOCR(公民権局、Office for Civil Rights)が執行を担当します。2009年に制定されたHITECH(Health Information Technology for Economic and Clinical Health Act)は、電子医療記録の普及に合わせてHIPAAの執行力を強化し、データ漏洩時の通知義務(Breach Notification Rule)を新設しました。両法は通常、まとめて「HIPAA/HITECH」と呼ばれます。

HIPAAは単一の認証制度ではなく、遵守すべき法的要件の体系であり、「HIPAA認証」という公式な資格は存在しません。組織自らが要件を満たし、それを文書・監査によって証明する構造です。

## PHI(保護対象医療情報)の定義

PHI(Protected Health Information)とは、次の条件をすべて満たす情報を指します。

- 医療提供者、健康保険、雇用主、医療情報交換機関などが作成・受領した情報
- 個人の過去・現在・将来の身体的・精神的健康状態、医療サービスの提供、それに対する費用の支払いに関連する情報
- 個人を特定できる(individually identifiable)情報

電子形式(ePHI)だけでなく、書面記録、検査結果、画像、請求書、さらには個人識別情報を含む口頭での会話まで含まれます。クラウドアーキテクチャの観点では、主にePHIが保存・伝送・処理の対象となります。

## Covered Entity、Business Associate、BAA締結の構造

HIPAAは規制対象を2つのグループに分けます。

- **Covered Entity(適用対象機関)**: 医療を提供する、または費用を支払う機関 — 医療提供者、健康保険会社、医療情報交換機関
- **Business Associate(業務委託対象者)**: Covered Entityに代わってPHIを収集・保存・伝送する第三者 — クラウドベンダー、SaaSプロバイダー、データ処理業者の大半がこれに該当

Covered EntityがPHI処理を外部に委託する場合は、**BAA(Business Associate Agreement)** という法的契約を必ず締結する必要があり、BAAはBusiness AssociateがPHIをどのような目的で扱えるか、どのようなセキュリティ・プライバシー要件を遵守すべきかを明記します。Business Associateがさらに下位ベンダー(Subcontractor)に委託する場合も、同様に下位BAAの締結が必要です。

:::note
クラウドサービスプロバイダーの大半はBusiness Associateの地位にあるとみなされます。つまり、クラウドベンダーとBAAを締結することが、PHIを当該クラウドに載せるための法的な前提条件です。
:::

## ベンダー別BAA適用サービス範囲の確認方法

主要クラウドベンダーは標準契約の一部としてBAAを提供していますが、**BAAの締結がすべてのサービスを自動的にカバーするわけではありません。**

- **AWS**: AWS Artifactを通じてアカウント単位でBAAを締結でき、「HIPAA適格(HIPAA-eligible)サービス」リストに含まれるサービスのみがBAAの保護範囲に入ります。
- **Azure**: 標準オンラインサービス利用規約(Online Services Terms)の一部としてBAAを提供しており、比較的幅広いサービスをカバーしているとされていますが、こちらもサービスごとにリストの確認が必要です。
- **Google Cloud**: 標準規約を通じてBAAを提供しており、指定された適格サービスのみが対象です。

アーキテクチャ設計時には、必ず各ベンダーの最新の「HIPAA適格サービスリスト」の公式ページで、使用しようとするサービスが含まれているかを確認する必要があり、リストにないサービスでPHIを処理・保存すると、BAAの保護を受けられません。また、BAAは責任共有モデルにおけるベンダー側の分だけを扱うため、サービスを安全に構成し、PHIへのアクセスを制限し、暗号化することは依然として顧客(Covered Entity/Business Associate)の責任です。

## HITRUST CSFとの関係

HITRUST CSFは、政府ではなく民間組織(HITRUST Alliance)が運営するセキュリティフレームワークであり、HIPAAを含む40以上のセキュリティ・規制標準を一つに統合して提供します。

- HIPAAは法律であり、HITRUST CSFはその法律を含む複数の標準を遵守するための実務的なフレームワークです。
- HITRUST CSF認証を取得したからといって自動的に「HIPAA準拠」になるわけではありません(そもそもHIPAAには公式な認証制度が存在しません)が、第三者監査を経たHITRUST認証は、HIPAA要件を満たしていることの強力な状況証拠として広く活用されています。
- 米国の病院の相当数と多くの健康保険会社がHITRUSTをベンダー評価・自己準拠証明の手段として採用しており、米国のエンタープライズ顧客にヘルスケアSaaSを販売しようとする場合、HITRUST CSF認証が事実上の市場要求事項として機能することが多くあります。

## 暗号化・監査ログ要件

現行のHIPAA Security Ruleは、多くの保護措置を「必須(Required)」と「推奨(Addressable、代替措置の採用可)」に区分してきました。しかしHHSは2024年12月に、この区分を廃止し、大半の保護措置を義務化する改正案(NPRM)を発表しました(連邦官報への掲載は2025年1月)。

:::caution
この改正案は2026年8月現在**確定していません。**2025年3月に意見募集が終了した後、OMB Unified Agendaの基準で最終規則の目標時期が2027年7月に再調整された状態です。以下の内容は提案段階であり、実際の施行の有無・時期はHHSの公式発表で再確認する必要があります。
:::

提案されている主な変更事項:

- ePHIの保存(at rest)および伝送(in transit)時の暗号化を原則として義務化(限定的な例外のみ許可)
- PHIシステムへのアクセスに対する多要素認証(MFA)の義務化
- ほぼリアルタイムでの自動化された監査ログモニタリング、ログ保護統制の強化
- ログの長期保管の強化 — 既存の6年保存要件はポリシー・手順などの文書に適用されるものであり、これをログの領域まで拡張しようとする提案
- 最低6か月周期の脆弱性スキャン、年1回の侵入テスト

改正案の確定の有無にかかわらず、保存・伝送区間の暗号化とアクセスログの記録はすでに業界標準の慣行として定着しており、新規アーキテクチャには先んじて反映しておくのが安全です。

## ヘルスケアSaaSアーキテクチャへの示唆

- **適格サービスのみを使用**: PHIが流れるすべてのサービスが、ベンダーのBAA適格リストに含まれているかを設計段階から確認します。
- **暗号化のデフォルト化**: 現行規定が「推奨」に分類していても、保存・伝送区間の暗号化を基本アーキテクチャ要件として採用します。今後の義務化に備えることができます。
- **アクセス統制と監査ログ**: PHIアクセスの最小権限の原則、MFA、一元化された監査ログ(SIEM連携)および長期保管ポリシーを備えます。関連アーキテクチャは[データ保護とワークロードセキュリティ](../../security/data-protection/)および[セキュリティインシデント対応](../../security/incident-response/)を参照してください。
- **HITRUST認証の検討**: 米国のヘルスケアエンタープライズ顧客向けの営業において、HITRUST CSF認証が事実上必要条件となる場合が多いため、初期段階から認証取得のロードマップを検討します。
- **下位ベンダーBAAチェーンの管理**: 自社が使用するすべての下位クラウド・SaaSベンダーとのBAA締結状況を、契約管理の観点から追跡します。

## 参考資料

- [HHS HIPAA公式ページ](https://www.hhs.gov/hipaa/)
- [HHS Covered Entities and Business Associates](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html)
- [HHS HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [AWS HIPAAコンプライアンス](https://aws.amazon.com/compliance/hipaa-compliance/)
- [Microsoft Azure HIPAA/HITECH](https://learn.microsoft.com/azure/compliance/offerings/offering-hipaa-us)
- [Google Cloud HIPAAコンプライアンス](https://cloud.google.com/security/compliance/hipaa)
- [HITRUST Alliance](https://hitrustalliance.net/)
