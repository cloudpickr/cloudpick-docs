# CloudPick Docs

[한국어](README.md) | [English](README.en.md) | **日本語**

CloudPick は、**マルチクラウド環境で正しい意思決定を下すためのベンダー中立ガイド**です。

マルチクラウドを既定として推奨するものではありません。単一ベンダー、ハイブリッド、
マルチクラウドにはそれぞれのコストと責任があり、ワークロードと組織の状況に応じて選択する
べきです。

## 技術スタック

- [Astro](https://astro.build/) + [Starlight](https://starlight.astro.build/) — 静的ドキュメントサイト
- 3 つのロケール: 韓国語（ko、既定）、English（en）、日本語（ja）
- Netlify にデプロイ（静的ビルド + MCP サーバーレス関数）
- ドキュメントデータは言語ごとに Netlify Blobs へ保存 — 多言語 MCP（ko/en/ja）経由でのみアクセス可能

## 開発

```bash
npm install
npm run dev       # 開発サーバー (localhost:4321)
npm run build     # dist/ 静的ビルド + Blob アップロード
npm run preview   # ビルド結果のローカルプレビュー
```

## プロジェクト構成

```
src/
  content/
    docs/
      ko/          ← 韓国語コンテンツ（既定ロケール、SOT）
      en/          ← 英語翻訳
      ja/          ← 日本語翻訳
  styles/          ← カスタム CSS
public/            ← 静的アセット（フォント、画像）
netlify/           ← Netlify Functions（MCP エンドポイント、Blob ヘルスチェック）
plugins/           ← ビルドプラグイン（言語別 llms Blob アップロード）
scripts/           ← ビルド後処理（リダイレクト stub、言語別 llms 生成）、ドキュメントリンター
config/            ← ロケールの単一定義（locales.mjs — 言語リストの SOT）
astro.config.mjs   ← サイト設定、サイドバー、ロケール
netlify.toml       ← Netlify ビルド + リダイレクト設定
```

## コンテンツ構成

| セクション | 説明 |
|------|------|
| about-cloud/ | クラウドの基礎・意思決定・中核概念 |
| compute/ | VM、コンテナ、サーバーレス、オートスケーリング |
| networking/ | VPC、LB、DNS、CDN、API Gateway |
| storage/ | オブジェクト、ブロック／ファイル、バックアップ |
| database/ | RDB、NoSQL、キャッシュ、メッセージング、分析 |
| devops/ | CI/CD、IaC、モニタリング、SLO |
| security/ | IAM、シークレット、データ保護、ゼロトラスト |
| governance/ | ランディングゾーン、FinOps、DR、コンプライアンス |
| ai/ | AI/ML、RAG、エージェント、LLMOps |
| korea/ us/ eu/ japan/ singapore/ | 国別の規制ガイド |

## i18n

- 既定ロケール: `ko`（韓国語）、SOT
- 全接頭辞方式: `/ko/`、`/en/`、`/ja/`
- ko に存在するドキュメントは en・ja も同一内容で完全翻訳して維持 — 3 ロケールのファイル構成・内容が対称
- コンテンツ原本（SOT）は `src/content/docs/ko/`

## MCP（AI エージェント連携）

AI エージェントがドキュメントを検索・参照できる MCP エンドポイントを提供します。
ドキュメントの全文データは言語ごとに Netlify Blobs へ保存され
（`llms-full-{ko,en,ja}`）、MCP 関数経由でのみアクセス可能です。

- エンドポイント: `https://docs.cloudpick.kr/mcp`（言語に関わらず単一 URL）
- 利用できるツール:
  - `list_docs` — 全ページのタイトル一覧
  - `search_docs` — キーワード検索
  - `get_doc` — 特定ドキュメントの全文参照
- **多言語**: 3 つのツールはいずれも任意の `lang`（`ko`・`en`・`ja`）パラメータを受け取ります。未指定の場合は検索語／タイトルの文字から言語を判別し（ハングル→ko、かな→ja）、手がかりが無ければ**既定値 ko（SOT）にフォールバック**します。応答は使用言語と再リクエスト方法を記したヘッダーで始まります。
- 詳細な設定・動作は[ドキュメントの MCP ページ](https://docs.cloudpick.kr/ja/mcp/)を参照してください。

## 貢献

[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。
