---
title: "コンプライアンス（韓国）"
description: "ISMS-P、CSAP、金融業界規制など、韓国のクラウドコンプライアンス認証と要件を整理します。"
---

> 文書基準: 2026年8月

## 概要

韓国でクラウドを導入する際には、国際認証（ISO 27001、SOC 2など）に加えて、韓国固有の認証・規制を満たす必要があります。共同責任モデル、コンプライアンス運用の自動化など**コンプライアンスの一般原則**については[コンプライアンス（Compliance）](../../../governance/compliance/)で扱っており、本ドキュメントはその上に重なる**韓国固有の規制レイヤー**です。

## ISMS-P（情報保護・個人情報保護管理体系認証）


- **根拠法**: 情報通信網法、個人情報保護法
- **運営**: [KISA（韓国インターネット振興院）](https://isms.kisa.or.kr/)
- **対象**: 情報通信サービス部門売上高100億ウォン以上、または1日平均利用者100万人以上の情報通信サービス提供者等（売上高1,500億ウォン基準は上級総合病院・大学等の別途類型に適用）
- **有効期間**: 3年間、年1回の事後審査
- **クラウドへの影響**: クラウドで機密情報を保存・処理する場合、ベンダーのISMS-P認証範囲内のリージョンを使用する必要があります

公式ベンダー別ページ:

- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
- OCI: 公式コンプライアンスページで認証状況をご確認ください


### ISMS-P と ISO 27001 の主な違い


| 区分 | ISMS-P | ISO 27001 |
| --- | --- | --- |
| **適用範囲** | 80+22項目の基準すべてを満たす必要あり | 適用範囲を組織が選択可能（SoAで「該当なし」も可能） |
| **個人情報保護** | 含む（個人情報の処理段階別要求事項） | 含まない（別途ISO 27701が必要） |
| **性格** | 韓国法上の義務対象あり（情報通信サービス提供者など） | 国際的な任意認証 |
| **共通点** | 技術だけでなく業務プロセス（ポリシー、人員、変更管理）も審査 | ← 同左 |


## CSAP（クラウドセキュリティ認証制度）


- **根拠法**: クラウドコンピューティング発展法 第23条の2
- **運営**: [KISA](https://isms.kisa.or.kr/main/csap/intro/)
- **対象**: 公共機関にクラウドサービスを提供しようとするすべてのCSP
- **等級体系**（2024年に上・中・下の等級制を全面施行）:

| 等級 | 対象システム | 要求水準 |
| --- | --- | --- |
| **上** | 安全保障・外交等国家の重大利益に関わるシステム、行政機関内部業務システム | 物理的網分離、国内リージョン、国内人員による運用など厳格な要件 |
| **中** | 個人情報・重要情報を処理する一般公共システム | 論理的網分離など、上等級と比べて緩和 |
| **下** | 個人情報を含まない公開データシステム（グローバルCSPの参入が可能） | 最小限のセキュリティ要件 |

**グローバルCSPのCSAP認証状況（2025年時点）:**

| ベンダー | 等級 | リージョン | 参考 |
| --- | --- | --- | --- |
| AWS | 下（Low-tier） | ソウル `ap-northeast-2` | [AWS CSAP発表](https://aws.amazon.com/blogs/security/aws-achieves-cloud-security-assurance-program-csap-low-tier-certification-in-aws-seoul-region/) |
| Azure | 下（Low-tier） | Korea Central / South | [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap) |
| Google Cloud | 下（Low-tier） | Seoul `asia-northeast3` | [Google Cloud CSAP](https://cloud.google.com/security/compliance/csap) |
| OCI | —（公式ページを確認） | Seoul, Chuncheon | [Oracleコンプライアンス](https://www.oracle.com/corporate/cloud-compliance/) |

:::note
CSAP制度は、N²SF（国家網セキュリティ体系）1.0の公開（2025年9月）に伴い、等級別の差別化されたセキュリティ体系との連携が進められています。導入前に[KISA公式サイト](https://isms.kisa.or.kr/main/csap/intro/)および[NCSC](https://www.ncsc.go.kr)で最新の状況をご確認ください。
:::


:::note
CSAP等級別の詳細要件、ハイパースケーラー・国内CSPの認証状況、2027年に予定されている国家情報院の単一検証体系への改編動向については、[CSAP（クラウドセキュリティ認証）](../../../korea/security/csap/)で詳しく扱っています。
:::

## 金融業界に関する規制


金融分野には追加の規制が適用されます。

- **電子金融取引法 / 電子金融監督規定** — 金融会社がクラウドを利用する際の安全性確保要件
- **金融保安院（FSI）** — 金融業界向けクラウド利用ガイドの発行、セキュリティコンサルティングの提供
- **網分離規制** — 個人信用情報を処理するシステムは、一般業務網と分離して運用する必要があります。N²SFの1.0に基づき、等級別の差別化適用へと移行が進んでいます（[網分離とネットワーク隔離](../../security/network-isolation/)を参照）

公式資料:

- [金融保安院クラウド利用ガイド](https://www.fsec.or.kr/)（統合インデックスをご活用ください）
- [金融委員会](https://www.fsc.go.kr/)


## 参考資料

- [KISA認証・認定](https://isms.kisa.or.kr/)
- [個人情報保護委員会](https://www.pipc.go.kr/)
- [金融保安院](https://www.fsec.or.kr/)
- [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/) / [AWS CSAP](https://aws.amazon.com/compliance/csap/)
- [Azure K-ISMS](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-k-isms) / [Azure CSAP](https://learn.microsoft.com/azure/compliance/offerings/offering-korea-csap)
- [Google Cloud K-ISMS](https://cloud.google.com/security/compliance/k-isms)
