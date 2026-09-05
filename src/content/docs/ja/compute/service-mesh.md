---
title: "サービスメッシュ"
description: "サービスメッシュの概念、サイドカー vs サイドカーレスモデル、ベンダー別マネージドサービスを比較します。"
---

> 文書基準: 2026年8月

## 概要

[コンテナサービス](../../compute/containers/)でマイクロサービスを運用すると、サービス間通信が複雑になります。**サービスメッシュ** (Service Mesh)は、この通信をインフラ層で管理し、アプリケーションコードの変更なしにセキュリティ、可観測性、トラフィック制御を提供します。

### サービスメッシュが解決する課題

| 課題 | サービスメッシュによる解決 |
| --- | --- |
| サービス間の暗号化 (mTLS) | 証明書の自動発行/更新、すべての通信を暗号化 |
| トラフィックルーティング | Canaryデプロイ、A/Bテスト、トラフィック分割 |
| サーキットブレーカー | 障害サービスの自動隔離、リトライ/タイムアウト |
| 可観測性 | サービス間の遅延/エラー率を自動収集(コード変更なし) |
| アクセス制御 | サービス間通信ポリシー(どのサービスがどのサービスを呼び出せるか) |

## サイドカー vs サイドカーレス

| モデル | 方式 | 利点 | 欠点 |
| --- | --- | --- | --- |
| **サイドカー** (Sidecar) | 各Podにプロキシコンテナ(Envoyなど)を注入 | 成熟したエコシステム、機能が豊富 | リソースオーバーヘッド(メモリ/CPU)、レイテンシ増加 |
| **サイドカーレス** (Sidecarless) | ノードレベルまたはカーネルレベルで処理 | リソース節約、レイテンシ最小 | まだ初期段階、機能が限定的 |

代表的な実装:
- サイドカー: Istio (Envoy)、Linkerd (linkerd2-proxy)
- サイドカーレス: Istio Ambient Mesh (ztunnel)、Cilium Service Mesh (eBPF)

## 主要ソリューション比較

| ソリューション | プロキシ | 特徴 |
| --- | --- | --- |
| [Istio](https://istio.io/) | Envoy | 最も機能が豊富。Ambient Meshでサイドカーレスをサポート。複雑度は高い |
| [Linkerd](https://linkerd.io/) | linkerd2-proxy (Rust) | 軽量、シンプル。リソースオーバーヘッド最小。機能はIstioに比べ限定的 |
| [Consul Connect](https://www.consul.io/docs/connect) | Envoy | HashiCorpエコシステム統合。マルチプラットフォーム(K8s + VM) |

## ベンダーマネージドサービス

| ベンダー | サービス | 基盤 | 特徴 |
| --- | --- | --- | --- |
| AWS | [App Mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html) (メンテナンスモード) / ECS Service Connect | Envoy | App Meshは新規導入非推奨。ECS Service ConnectまたはVPC Latticeを推奨 |
| AWS | [VPC Lattice](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html) | AWSネイティブ | サービス間接続をVPCレベルで管理。サイドカー不要 |
| Azure | [Istio add-on for AKS](https://learn.microsoft.com/azure/aks/istio-about) | Istio | AKSネイティブ統合。コントロールプレーンはマネージド |
| Google Cloud | [Cloud Service Mesh](https://cloud.google.com/service-mesh/docs) | Istioベース | GKE統合。マネージドコントロールプレーン + データプレーン |
| OCI | 自社マネージドなし | — | OKEでIstio/Linkerdを直接インストール |

## いつ導入すべきか

| 基準 | 導入推奨 | 導入不要 |
| --- | --- | --- |
| サービス数 | 10個以上、チーム間の境界が存在 | モノリスまたはサービス3～5個 |
| セキュリティ要件 | サービス間mTLS必須(規制/監査) | 内部通信の暗号化不要 |
| トラフィック制御 | Canary/A-Bデプロイ、きめ細かなルーティングが必要 | シンプルなローリングデプロイで十分 |
| 可観測性 | サービス間の遅延/エラー追跡が必要 | APMで十分 |

:::note
**サービスメッシュは複雑さを追加します。** サービス数が少ないか、チームが小さい場合は、サービスメッシュなしでネイティブ機能(Security Group、IAM、ALBルーティング)で十分な場合があります。「必要なとき」に導入してください。
:::

## よくある間違い

- **サービス数が少ないのにサービスメッシュを導入** — サービス3～5個規模では複雑さが増すだけです。ネイティブ機能(Security Group、IAM、ALBルーティング)で十分かをまず検討してください。
- **サイドカーのリソースオーバーヘッドを無視** — Envoyプロキシが Podごとに追加されると、メモリ/CPU使用量がかなり増えます。リソースリクエスト/制限を設定しないとノードのリソースが不足します。
- **mTLS導入後のデバッグの難しさに備えない** — すべての通信が暗号化されると、既存のパケットキャプチャツールが機能しません。メッシュレベルのロギングと分散トレーシングを併せて構成してください。

## チェックリスト

- [ ] サービスメッシュ導入が必要な明確な要件(mTLS、トラフィック分割、可観測性)があるか
- [ ] サイドカープロキシのリソースリクエスト/制限を設定し、ノード容量を確認したか
- [ ] メッシュコントロールプレーン障害時にデータプレーン(既存接続)が維持されるか確認したか

## 参考資料

### AWS

- [AWS VPC Lattice ドキュメント](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html)

### Azure

- [Azure AKS Istio add-on](https://learn.microsoft.com/azure/aks/istio-about)

### Google Cloud

- [Google Cloud Cloud Service Mesh](https://cloud.google.com/service-mesh/docs)

### 標準とコミュニティ

- [Istio ドキュメント](https://istio.io/latest/docs/)
- [Linkerd ドキュメント](https://linkerd.io/2/overview/)
- [CNCF Service Mesh Landscape](https://landscape.cncf.io/card-mode?category=service-mesh)
