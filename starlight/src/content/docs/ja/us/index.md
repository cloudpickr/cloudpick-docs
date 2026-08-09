---
title: "米国"
description: "FedRAMP、HIPAA、ITAR/EARなど、米国市場への進出・運用に必要な規制の概要と詳細ドキュメントへご案内します。"
---

> 文書基準: 2026年8月

## 概要

米国は連邦（federal）と州（state）の二元的な規制体系を持っており、そこに業界別規制（ヘルスケア、防衛・航空宇宙、金融など）が幾重にも重なる構造になっています。連邦機関にクラウドサービスを納入するにはFedRAMP認可が、ヘルスケアデータを扱うにはHIPAA/BAA体系が、防衛・航空宇宙の技術データを扱うにはITAR/EAR輸出管理が、それぞれ個別に適用され、互いに代替されるものではありません。本セクションでは、韓国のエンタープライズアーキテクトが米国市場への進出・運用を検討する際に直面する主要な規制3つを扱います。

## 扱うトピック

- **[FedRAMP](../us/fedramp/)** — 連邦機関のクラウド調達のためのセキュリティ認可制度です。Moderate/High基準、2026年に進行中のFedRAMP 20x改編の現況、GovCloudなどの分離リージョン、CMMC 2.0・DoD SRG Impact Levelを整理します。
- **[HIPAA/HITECH](../us/hipaa/)** — ヘルスケアデータ（PHI）保護規制です。BAA（Business Associate Agreement）締結の構造、ベンダー別適用範囲の確認方法、HITRUST CSFとの関係を扱います。
- **[ITAR/EAR](../us/itar/)** — 防衛・航空宇宙の技術データに関する輸出管理規定です。US Personsアクセス制限がクラウドアーキテクチャに持つ意味と、FedRAMPとの違いを整理します。

:::note
3つの規制は互いに独立しています。例えば、FedRAMP High認可を取得したクラウド環境だからといって自動的にITAR要件を満たすわけではなく、HIPAAも別途BAA締結が必要です。ワークロードの性質に合った規制を個別に確認する必要があります。
:::

## 関連ドキュメント

> 📄 [コンプライアンス（Compliance）](../../governance/compliance/)

> 📄 [データ保護とワークロードセキュリティ](../../security/data-protection/)

## 参考資料

- [FedRAMP公式サイト](https://www.fedramp.gov/)
- [HHS HIPAA公式ページ](https://www.hhs.gov/hipaa/)
- [DDTC（ITAR所管機関）](https://www.pmddtc.state.gov/)
- [BIS（EAR所管機関）](https://www.bis.gov/)
