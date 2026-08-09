---
title: "データ保護とワークロードセキュリティ"
description: "転送中/保存時の暗号化、WAF、ネットワークセキュリティをベンダー別に比較します。"
---

> 文書基準: 2026年8月

## 概要

クラウドセキュリティは大きく3つの領域に分かれます。

- **転送中のセキュリティ (In Transit)** — ネットワークを移動するデータの保護
- **保存時のセキュリティ (At Rest)** — ストレージ/DBに保存されたデータの保護
- **ワークロードセキュリティ** — 実行中のサーバー/コンテナ/アプリケーションの保護

## 転送中のセキュリティ (Encryption in Transit)

データがネットワークを移動する際の盗聴や改ざんを防止します。

| 区間 | 方法 | 備考 |
| --- | --- | --- |
| **ユーザー ↔ サービス** | TLS/HTTPS | CDN、LBでTLS終端。無料証明書の提供 (ACM、Let's Encryptなど) |
| **サービス ↔ サービス** | mTLS、VPC内部通信 | サービスメッシュ(Istio、App Mesh)による自動mTLS |
| **リージョン ↔ リージョン** | ベンダーバックボーン暗号化 | AWS/Azure/Google Cloudいずれもリージョン間トラフィックを自動暗号化 |
| **オンプレミス ↔ クラウド** | VPN (IPsec) / 専用線 | Direct Connect、ExpressRoute、Cloud Interconnect |

各ベンダーとも、マネージドサービス間の通信はデフォルトでTLSにより暗号化されます。

## 保存時のセキュリティ (Encryption at Rest)

保存されたデータが物理的に奪取されても読み取れないように暗号化します。主要なCSPはすべてデフォルトの暗号化を提供しており、鍵管理のレベルによってセキュリティと運用の複雑さが変わります:

- **ベンダー管理鍵** — 最もシンプル。ベンダーが鍵の生成/ローテーション/管理を行う。大半のワークロードに適する。
- **顧客管理鍵** (CMK) — 鍵のローテーション周期、アクセスポリシーを直接制御。規制要件を充足。
- **自己管理鍵** (BYOK/EKM/HYOK) — 鍵をオンプレミスのHSMで管理。最も厳格な規制対応。

:::note
ベンダー別のKMSサービス比較、CMK/BYOK/EKMの詳細、HSMオプションは[シークレット管理 — 暗号化鍵管理モデル](../../security/secrets/)を参照してください。
:::

## 量子耐性暗号 (Post-Quantum Cryptography)

:::note
**このセクションが必要な読者:** 10年以上保管する機密データ(金融、医療、公共)がある、または規制機関がPQC移行ロードマップを要求している組織。短期保管データのみを扱う場合は、即座の対応よりも動向把握として読んでください。
:::

今日、HTTPS、VPN、データ暗号化に使用されているRSA、ECDHなどのアルゴリズムは、量子コンピュータが十分に大規模化すると解読される可能性があります。問題は量子コンピュータが登場した「後」ではなく「今」です。攻撃者が暗号化されたトラフィックを今のうちに収集しておき、量子コンピュータの登場後に復号する**Harvest Now, Decrypt Later**攻撃が、すでに可能だからです。

これに対応して、NISTが新しい暗号化標準を確定し、主要クラウドベンダーが移行を開始しています。

### NIST PQC標準

| 標準 | 用途 | アルゴリズム | 状態 |
| --- | --- | --- | --- |
| **FIPS 203** (ML-KEM) | 鍵交換 | Kyberベースの格子暗号 | 2024年8月に最終確定 |
| **FIPS 204** (ML-DSA) | デジタル署名 | Dilithiumベースの格子暗号 | 2024年8月に最終確定 |
| **FIPS 205** (SLH-DSA) | デジタル署名 (ステートレス) | SPHINCS+ベースのハッシュ署名 | 2024年8月に最終確定 |
| **HQC** | バックアップKEM | 符号ベース暗号 | 2025年3月に選定 |

### ベンダー別PQC移行状況

| ベンダー | 状況 | 参考 |
| --- | --- | --- |
| AWS | KMSでML-KEMハイブリッドTLSに対応。S3、ACMなどサービス間通信にPQハイブリッド鍵交換を適用中 | [AWS Post-Quantum Cryptography](https://aws.amazon.com/security/post-quantum-cryptography/) |
| Azure | Microsoft Quantum Safe Program。SymCryptライブラリにML-KEM/ML-DSAを実装。TLS 1.3ハイブリッド鍵交換に対応 | [Microsoft Quantum Safe](https://www.microsoft.com/en-us/security/blog/topic/quantum-safe/) |
| Google Cloud | Cloud KMSでPQCデジタル署名(ML-DSA)をプレビュー提供。Chrome/BoringSSLへML-KEMハイブリッドの展開完了 | [Google Cloud PQC](https://cloud.google.com/blog/products/identity-security/quantum-safe-digital-signatures-in-cloud-kms) |
| OCI | OCI VaultなどでPQCアルゴリズムのロードマップを発表。Oracle Database TLSハイブリッドモードなどは公式ロードマップ・リリースノートに基づき確認 (具体的な製品ドキュメントが公開され次第リンクを差し替え) | [Oracle Security](https://www.oracle.com/security/) (総合ハブ。PQC専用ページは公式ドキュメントで確認) |

### PQC移行戦略

1. **インベントリ** — 使用中の暗号化アルゴリズム、証明書、鍵サイズを識別します (Crypto Agility Inventory)
2. **ハイブリッドモード** — 既存アルゴリズム＋PQCアルゴリズムを同時に使用し、互換性を維持しながら移行します
3. **優先順位付け** — 長期保管データ(10年以上の寿命)と署名インフラから移行します
4. **テスト** — PQCアルゴリズムは鍵/署名サイズが大きいため、ネットワークオーバーヘッドとハンドシェイク遅延を測定します

:::caution
PQC移行は数年単位のプロジェクトです。今すぐすべてのシステムを変更する必要はありませんが、**暗号アジリティ(Crypto Agility)** を確保し、アルゴリズムを交換できるアーキテクチャをあらかじめ備えておくことが重要です。
:::

## 機密コンピューティング (Confidential Computing)

従来の暗号化が「保存時」と「転送中」を保護するのに対し、機密コンピューティングは**「使用中(In Use)」**のデータを保護します。ハードウェアベースの信頼実行環境(TEE)でデータを処理することで、クラウドベンダーの管理者であっても処理中のデータにアクセスできません。

| ベンダー | 製品 | GPU機密コンピューティング | 参考 |
| --- | --- | --- | --- |
| AWS | [Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/) | — (Nitroアーキテクチャ自体がハイパーバイザー分離) | [AWS Nitro](https://aws.amazon.com/ec2/nitro/) |
| Azure | [Confidential VMs (AMD SEV-SNP, Intel TDX)](https://learn.microsoft.com/azure/confidential-computing/) | **NCC H100 v5** — NVIDIA H100機密GPU | [Azure Confidential Computing](https://azure.microsoft.com/solutions/confidential-compute/) |
| Google Cloud | [Confidential VMs (AMD SEV, Intel TDX)](https://cloud.google.com/confidential-computing) | **A3 Confidential VM** — H100機密GPU | [GCP Confidential Computing](https://cloud.google.com/confidential-computing/docs) |
| OCI | [Confidential Computing (AMD SEV)](https://docs.oracle.com/en-us/iaas/Content/Compute/References/confidential-compute.htm) | — | [OCI Compute](https://docs.oracle.com/en-us/iaas/Content/Compute/home.htm) |

**主な活用事例:**
- AI/ML推論におけるモデルIPと入力データの同時保護 (機密GPU)
- マルチパーティデータ分析 — 元データを公開せずに共同演算
- データ主権が厳格なワークロード (ソブリンクラウド＋機密コンピューティングの組み合わせ)

:::note
機密コンピューティングを活用したAIワークロード保護については[AIセキュリティ — 機密AI推論](../../security/ai-security/)を、データ主権関連のソブリンクラウドについては[ランディングゾーン — ソブリンランディングゾーン](../../governance/landing-zone/#소버린-랜딩존-sovereign-landing-zone)を参照してください。
:::

## ワークロードセキュリティ

実行中のインフラとアプリケーションを保護します。

### ネットワークセキュリティ

転送中のデータを保護するには、ネットワークレベルのアクセス制御が不可欠です。

:::note
Security Groups/NSG/Firewall Rulesなどネットワークファイアウォールのベンダー別比較は[VPCとサブネット](../../networking/vpc-subnet/)を、ネットワーク隔離アーキテクチャパターン(エアギャップ、予防的ガードレール)は[網分離とネットワーク隔離](../../security/network-isolation/)を参照してください。
:::

### Webアプリケーションファイアウォール (WAF)

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | [AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html) | ALB/CloudFront/API Gatewayに接続。マネージドルール＋カスタムルール |
| Azure | [Azure WAF](https://learn.microsoft.com/azure/web-application-firewall/overview) (Front Door / App Gateway) | OWASP CRS 3.2を標準提供。ポリシーベースの管理 |
| Google Cloud | [Cloud Armor](https://cloud.google.com/armor/docs) | DDoS＋WAF統合。事前構成済みWAFルール＋適応型保護(ML) |
| OCI | [OCI WAF](https://docs.oracle.com/en-us/iaas/Content/WAF/home.htm) | Load Balancer/Edge連携。OWASPルールセットを提供 |

#### OWASPとWAFルール

[OWASP Top 10](https://owasp.org/www-project-top-ten/)は、Webアプリケーションで最も一般的なセキュリティ脅威をまとめた業界標準です。各ベンダーのWAFは、これらの脅威に対応する**マネージドルールセット**を提供しています。

以下は、OWASP Top 10のうち**WAFルールで緩和可能な主要項目**を抜粋したものです:

| OWASP Top 10脅威 | WAFルールでの対応 | ベンダー別マネージドルール |
| --- | --- | --- |
| A01 — Broken Access Control | パストラバーサル、強制ブラウジングの遮断 | AWS Managed Rules (Core)、Azure CRS、Cloud Armor事前構成ルール |
| A03 — Injection (SQL/XSS) | SQL Injection、XSSパターンマッチング | AWS SQLi/XSS Rule Group、Azure CRS、Cloud Armor `sqli-v33-stable` |
| A05 — Security Misconfiguration | 既知の脆弱な経路の遮断 | AWS Known Bad Inputs、Azure CRS |
| A06 — Vulnerable Components | 既知のCVEエクスプロイトの遮断 | AWS Managed Rules (CVE)、Azure Bot Manager |
| A07 — Authentication Failures | ブルートフォース、クレデンシャルスタッフィングの遮断 | AWS Account Takeover Prevention、Azure Rate Limiting |

#### マネージドルール vs カスタムルール

| 区分 | マネージドルール (Managed Rules) | カスタムルール |
| --- | --- | --- |
| **管理主体** | ベンダーまたはセキュリティパートナーが更新 | ユーザーが直接作成・維持 |
| **適した場合** | OWASP Top 10の基本防御、迅速な適用 | アプリケーション特化のロジック、ビジネスルール |
| **更新** | 新たな脅威発見時にベンダーが自動更新 | ユーザーが直接更新 |
| **コスト** | ルールグループ単位で課金 (AWS)、標準で含まれる (Azure/Google Cloud/OCI) | ルール数に応じて課金 |

**実務上の推奨:**

- **第1段階** — マネージドOWASPルールセットをまず適用 (Countモードで開始し誤検知を確認した後Blockへ切り替え)
- **第2段階** — アプリケーション特化のカスタムルールを追加 (特定APIパスの保護、地域ベースの遮断など)
- **第3段階** — Rate LimitingルールでDDoS/ブルートフォースを緩和
- **ロギング** — WAFログをS3/Log Analytics/Cloud Loggingに保存し、攻撃パターンを分析

脅威検知(GuardDuty、Defender、SCC、Cloud Guard)とコンテナ/ランタイムセキュリティ(Inspector、Defender for Containersなど)については、[セキュリティ態勢管理](../../security/security-posture/)で詳しく扱います。

## よくある間違い

- **WAFをいきなりBlockモードで適用** — 誤検知(False Positive)を確認せずに遮断モードへ切り替え、正常なトラフィックが遮断される。まずCountモードで検証すべき
- **ベンダー管理鍵で十分なのにBYOKを導入** — 規制要件がないまま自己管理鍵を選択し、運用の複雑さと障害リスクのみが増加
- **VPC Endpointなしでマネージドサービスへアクセス** — S3、KMSなどをNAT Gateway経由でアクセスし、不要なインターネット露出とコストが発生
- **PQC移行を「量子コンピュータ登場後」に先送り** — Harvest Now, Decrypt Later攻撃にすでにさらされている。長期保管データは今からハイブリッドモードの適用が必要

## チェックリスト

- [ ] 保存時暗号化がすべてのストレージ/DBで有効化されているか (デフォルト暗号化を確認)
- [ ] WAFマネージドルールをまずCountモードで適用し、誤検知を確認した後にBlockへ切り替えたか
- [ ] マネージドサービス(S3、KMSなど)へのアクセスにVPC Endpoint / Private Linkを使用しているか
- [ ] 使用中の暗号化アルゴリズムをインベントリ化し、PQC移行ロードマップを策定したか
- [ ] 機密性の高いAI推論ワークロードへの機密コンピューティング適用を検討したか

## 関連ドキュメント

> 📄 [セキュリティ態勢管理](../../security/security-posture/)

> 📄 [シークレット管理](../../security/secrets/)

> 📄 [IAM実務設計とセキュリティ運用](../../security/iam/)

> 📄 [VPCとサブネット](../../networking/vpc-subnet/)

## 参考資料

### AWS

- [AWS セキュリティドキュメント](https://docs.aws.amazon.com/ko_kr/security/)
- [AWS KMS ドキュメント](https://docs.aws.amazon.com/ko_kr/kms/)
- [AWS WAF ドキュメント](https://docs.aws.amazon.com/ko_kr/waf/)

### Azure

- [Azure セキュリティドキュメント](https://learn.microsoft.com/ko-kr/azure/security/)
- [Azure Key Vault ドキュメント](https://learn.microsoft.com/ko-kr/azure/key-vault/)
- [Azure WAF ドキュメント](https://learn.microsoft.com/ko-kr/azure/web-application-firewall/)

### Google Cloud

- [Google Cloud セキュリティドキュメント](https://cloud.google.com/security)
- [Cloud KMS ドキュメント](https://cloud.google.com/kms/docs)
- [Cloud Armor ドキュメント](https://cloud.google.com/armor/docs)

### OCI

- [OCI Vault ドキュメント](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/home.htm)
- [OCI WAF ドキュメント](https://docs.oracle.com/en-us/iaas/Content/WAF/home.htm)

### 量子耐性暗号 / 機密コンピューティング

- [NIST FIPS 203 — ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- [NIST FIPS 204 — ML-DSA](https://csrc.nist.gov/pubs/fips/204/final)
- [AWS Post-Quantum Cryptography](https://aws.amazon.com/security/post-quantum-cryptography/)
- [Azure Confidential Computing](https://learn.microsoft.com/azure/confidential-computing/)
- [Google Cloud Confidential Computing](https://cloud.google.com/confidential-computing)
