# CloudPick Docs

[한국어](README.md) | **English** | [日本語](README.ja.md)

CloudPick is a **vendor-neutral guide for making the right decisions in
multi-cloud environments**.

We do not recommend multi-cloud as a default. Single-vendor, hybrid, and
multi-cloud each carry their own costs and responsibilities, and the choice
should follow your workload and organizational context.

## Tech stack

- [Astro](https://astro.build/) + [Starlight](https://starlight.astro.build/) — static documentation site
- Three locales: Korean (ko, default), English (en), Japanese (ja)
- Deployed on Netlify (static build + MCP serverless function)
- Document data is stored in Netlify Blobs per language — accessible only through the multilingual MCP (ko/en/ja)

## Development

```bash
npm install
npm run dev       # dev server (localhost:4321)
npm run build     # dist/ static build + blob upload
npm run preview   # local preview of the build output
```

## Project structure

```
src/
  content/
    docs/
      ko/          ← Korean content (default locale, SOT)
      en/          ← English translation
      ja/          ← Japanese translation
  styles/          ← custom CSS
public/            ← static assets (fonts, images)
netlify/           ← Netlify Functions (MCP endpoint, blob health check)
plugins/           ← build plugins (per-language llms blob upload)
scripts/           ← post-build steps (redirect stubs, per-language llms generation), doc linters
config/            ← single locale definition (locales.mjs — language list SOT)
astro.config.mjs   ← site config, sidebar, locales
netlify.toml       ← Netlify build + redirect config
```

## Content structure

| Section | Description |
|------|------|
| about-cloud/ | Cloud fundamentals, decision-making, core concepts |
| compute/ | VMs, containers, serverless, autoscaling |
| networking/ | VPC, LB, DNS, CDN, API Gateway |
| storage/ | Object, block/file, backup |
| database/ | RDB, NoSQL, cache, messaging, analytics |
| devops/ | CI/CD, IaC, monitoring, SLO |
| security/ | IAM, secrets, data protection, zero trust |
| governance/ | Landing zone, FinOps, DR, compliance |
| ai/ | AI/ML, RAG, agents, LLMOps |
| korea/ us/ eu/ japan/ singapore/ | Country-specific regulatory guides |

## i18n

- Default locale: `ko` (Korean), the SOT
- Full-prefix routing: `/ko/`, `/en/`, `/ja/`
- Any document present in ko is kept fully translated with identical content in en and ja — the three locales are symmetric in file structure and content
- The content source of truth (SOT) is `src/content/docs/ko/`

## MCP (AI agent integration)

Provides an MCP endpoint through which AI agents can search and read the docs.
Full-text document data is stored per language in Netlify Blobs
(`llms-full-{ko,en,ja}`) and is accessible only through the MCP function.

- Endpoint: `https://docs.cloudpick.kr/mcp` (a single URL regardless of language)
- Available tools:
  - `list_docs` — list all page titles
  - `search_docs` — keyword search
  - `get_doc` — fetch the full text of a specific document
- **Multilingual**: all three tools accept an optional `lang` parameter (`ko`, `en`, `ja`). When unspecified, the language is inferred from the characters in the query/title (Hangul → ko, kana → ja); with no signal it **falls back to the default ko (SOT)**. The response begins with a header stating the language used and how to re-request.
- For detailed configuration and behavior, see the [MCP page in the docs](https://docs.cloudpick.kr/en/mcp/).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
