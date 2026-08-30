// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLlmsTxt from 'starlight-llms-txt';
import mermaid from 'astro-mermaid';
import { STARLIGHT_LOCALES, DEFAULT_LOCALE } from './config/locales.mjs';

// https://astro.build/config
// 정적 사이트 — 어댑터 불필요. @astrojs/cloudflare 사용 금지(satori wasm 빌드 오류).
export default defineConfig({
	site: 'https://docs.cloudpick.kr',
	output: 'static',
	trailingSlash: 'always',
	integrations: [
		mermaid({
			// Starlight 다크모드 연동: html[data-theme] 감지
			autoTheme: true,
		}),
		starlight({
			title: 'CloudPick',
			description: '멀티클라우드 환경에서 올바른 의사결정을 내리기 위한 벤더 중립 가이드',
			defaultLocale: DEFAULT_LOCALE,
			locales: STARLIGHT_LOCALES,
			plugins: [starlightLlmsTxt()],
			routeMiddleware: './src/routeData.ts',
			components: {
				Head: './src/components/Head.astro',
			},
			customCss: [
				'@fontsource-variable/inter/wght.css',
				'@fontsource-variable/space-grotesk/wght.css',
				'@fontsource/jetbrains-mono/latin-400.css',
				'@fontsource/jetbrains-mono/latin-700.css',
				'./src/styles/custom.css',
			],
			head: [
				{
					tag: 'link',
					attrs: { rel: 'stylesheet', href: '/fonts/pretendard/pretendardvariable-dynamic-subset.css' },
				},
				{
					tag: 'script',
					attrs: { src: '/mobile-select-menu.js', defer: true },
				},
				// ─── .netlify.app → docs.cloudpick.kr 리디렉트 ───
				{
					tag: 'script',
					content: `if(location.hostname.endsWith('.netlify.app')){location.replace('https://docs.cloudpick.kr'+location.pathname+location.search);}`,
				},
				// ─── Google Analytics (GA4) ───
				...(process.env.PUBLIC_GA_ID ? [
					{
						tag: 'script',
						attrs: { src: `https://www.googletagmanager.com/gtag/js?id=${process.env.PUBLIC_GA_ID}`, async: true },
					},
					{
						tag: 'script',
						content: `window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${process.env.PUBLIC_GA_ID}');`,
					},
				] : []),
				// ─── OpenGraph 메타 태그 (소셜 공유용) ───
				{
					tag: 'meta',
					attrs: { property: 'og:type', content: 'website' },
				},
				{
					tag: 'meta',
					attrs: { property: 'og:site_name', content: 'CloudPick' },
				},
				{
					tag: 'meta',
					attrs: { property: 'og:image', content: 'https://docs.cloudpick.kr/og-image.png' },
				},
				{
					tag: 'meta',
					attrs: { property: 'og:image:width', content: '1200' },
				},
				{
					tag: 'meta',
					attrs: { property: 'og:image:height', content: '630' },
				},
				{
					tag: 'meta',
					attrs: { property: 'og:image:alt', content: 'CloudPick — Vendor-neutral multi-cloud decision guide' },
				},
				// og:locale / og:locale:alternate 는 src/routeData.ts 가 로케일별로 주입
				// ─── Twitter/X Card 메타 태그 ───
				{
					tag: 'meta',
					attrs: { name: 'twitter:card', content: 'summary_large_image' },
				},
				{
					tag: 'meta',
					attrs: { name: 'twitter:image', content: 'https://docs.cloudpick.kr/og-image.png' },
				},
				{
					tag: 'meta',
					attrs: { name: 'twitter:image:alt', content: 'CloudPick — Vendor-neutral multi-cloud decision guide' },
				},
			],
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/cloudpickr/cloudpick-docs' },
			],
			sidebar: [
				{
					label: '소개',
					translations: { en: 'Introduction', ja: 'CloudPickについて' },
					link: 'introduction',
				},
				{
					label: '용어집',
					translations: { en: 'Glossary', ja: '用語集' },
					link: 'glossary',
				},
				{
					label: 'AI 에이전트 연동 (MCP)',
					translations: { en: 'AI Agent Integration (MCP)', ja: 'AIエージェント連携 (MCP)' },
					link: 'mcp',
				},
				{
					label: 'Getting Started',
					translations: { ko: '시작하기', ja: 'はじめに' },
					items: [
						{
							label: '클라우드 기초·의사결정',
							translations: { en: 'Cloud basics & decisions', ja: '基礎と意思決定' },
							items: [
								{ slug: 'about-cloud/getting-started' },
								{ slug: 'about-cloud/compare-clouds' },
								{ slug: 'about-cloud/decision-framework' },
								{ slug: 'about-cloud/why-multicloud' },
							],
						},
						{
							label: '핵심 개념',
							translations: { en: 'Core concepts', ja: 'コア概念' },
							items: [
								{ slug: 'about-cloud/regions-and-zones' },
								{ slug: 'about-cloud/shared-responsibility' },
								{ slug: 'about-cloud/accounts-and-organizations' },
								{ slug: 'about-cloud/iam-overview' },
								{ slug: 'about-cloud/console-cli-sdk' },
								{ slug: 'about-cloud/pricing-model' },
							],
						},
						{
							label: '운영 프레임워크',
							translations: { en: 'Operating frameworks', ja: '運用フレームワーク' },
							items: [
								{ slug: 'about-cloud/well-architected' },
								{ slug: 'about-cloud/support-plans' },
								{ slug: 'about-cloud/field-deployment' },
							],
						},
					],
				},
				{
					label: 'Compute',
					translations: { ko: '컴퓨팅', ja: 'コンピューティング' },
					items: [
						{ slug: 'compute/virtual-machines' },
						{ slug: 'compute/containers' },
						{ slug: 'compute/auto-scaling' },
						{ slug: 'compute/serverless' },
						{ slug: 'compute/service-mesh' },
						{ slug: 'compute/hybrid-and-edge' },
						{ slug: 'compute/migration' },
						{ slug: 'compute/modernization' },
					],
				},
				{
					label: 'Networking',
					translations: { ko: '네트워킹', ja: 'ネットワーキング' },
					items: [
						{ slug: 'networking/vpc-subnet' },
						{ slug: 'networking/load-balancer' },
						{ slug: 'networking/dns' },
						{ slug: 'networking/cdn' },
						{ slug: 'networking/api-gateway' },
						{ slug: 'networking/multicloud-networking' },
						{ slug: 'networking/multicloud-connectivity' },
					],
				},
				{
					label: 'Storage',
					translations: { ko: '스토리지', ja: 'ストレージ' },
					items: [
						{ slug: 'storage/object-storage' },
						{ slug: 'storage/block-and-file' },
						{ slug: 'storage/backup' },
						{ slug: 'storage/migration' },
					],
				},
				{
					label: 'Database',
					translations: { ko: '데이터베이스', ja: 'データベース' },
					items: [
						{ slug: 'database/managed-rdb' },
						{ slug: 'database/nosql' },
						{ slug: 'database/cache' },
						{ slug: 'database/operations' },
						{ slug: 'database/messaging' },
						{ slug: 'database/analytics' },
						{ slug: 'database/data-pipeline' },
						{ slug: 'database/search' },
						{ slug: 'database/migration' },
					],
				},
				{
					label: 'DevOps',
					translations: { ko: 'DevOps', ja: 'DevOps' },
					items: [
						{
							label: '기초·파이프라인',
							translations: { en: 'Foundations & pipelines', ja: '基礎とパイプライン' },
							items: [
								{ slug: 'devops/getting-started' },
								{ slug: 'devops/cicd' },
								{ slug: 'devops/iac' },
								{ slug: 'devops/devsecops' },
							],
						},
						{
							label: '관측·운영',
							translations: { en: 'Observability & ops', ja: '観測と運用' },
							items: [
								{ slug: 'devops/monitoring' },
								{ slug: 'devops/slo' },
								{ slug: 'devops/observability' },
								{ slug: 'devops/remote-access' },
								{ slug: 'devops/patch-and-vulnerability' },
							],
						},
						{
							label: '플랫폼',
							translations: { en: 'Platform', ja: 'プラットフォーム' },
							items: [
								{ slug: 'devops/kubernetes-operations' },
								{ slug: 'devops/platform-engineering' },
							],
						},
					],
				},
				{
					label: 'Security',
					translations: { ko: '보안', ja: 'セキュリティ' },
					items: [
						{ slug: 'security/getting-started' },
						{ slug: 'security/iam' },
						{ slug: 'security/secrets' },
						{ slug: 'security/data-protection' },
						{ slug: 'security/network-isolation' },
						{ slug: 'security/zero-trust' },
						{ slug: 'security/security-posture' },
						{ slug: 'security/incident-response' },
						{ slug: 'security/ai-security' },
					],
				},
				{
					label: 'Governance',
					translations: { ko: '거버넌스', ja: 'ガバナンス' },
					items: [
						{ slug: 'governance/getting-started' },
						{ slug: 'governance/landing-zone' },
						{ slug: 'governance/finops' },
						{ slug: 'governance/dr' },
						{ slug: 'governance/compliance' },
						{ slug: 'governance/exit-strategy' },
						{ slug: 'governance/sustainability' },
					],
				},
				{
					label: 'AI',
					translations: { ko: 'AI', ja: 'AI' },
					items: [
						{
							label: '기초·모델',
							translations: { en: 'Foundations & models', ja: '基礎とモデル' },
							items: [
								{ slug: 'ai/getting-started' },
								{ slug: 'ai/ai-ml' },
								{ slug: 'ai/prompt-engineering' },
							],
						},
						{
							label: '데이터·RAG',
							translations: { en: 'Data & RAG', ja: 'データとRAG' },
							items: [
								{ slug: 'ai/rag-patterns' },
								{ slug: 'ai/vector-store' },
							],
						},
						{
							label: '에이전트·도입',
							translations: { en: 'Agents & adoption', ja: 'エージェントと導入' },
							items: [
								{ slug: 'ai/agents' },
								{ slug: 'ai/agent-adoption' },
								{ slug: 'ai/1p-vs-3p' },
								{ slug: 'ai/licensing' },
							],
						},
						{
							label: '운영·멀티클라우드',
							translations: { en: 'Ops & multicloud', ja: '運用とマルチクラウド' },
							items: [
								{ slug: 'ai/llmops' },
								{ slug: 'ai/multicloud-ai' },
								{ slug: 'ai/physical-ai' },
							],
						},
					],
				},
				{
					label: '국가별 가이드',
					translations: { en: 'Country Guides', ja: '国別ガイド' },
					items: [
						{
							label: '한국',
							translations: { en: 'Korea', ja: '韓国' },
							collapsed: true,
							items: [
								{ slug: 'korea', label: '개요', translations: { en: 'Overview', ja: '概要' } },
								{ slug: 'korea/governance/compliance' },
								{ slug: 'korea/security/csap' },
								{ slug: 'korea/security/network-isolation' },
								{ slug: 'korea/ai/sovereign-fm-policy' },
								{ slug: 'korea/ai/fm-providers' },
							],
						},
						{
							label: '미국',
							translations: { en: 'United States', ja: '米国' },
							collapsed: true,
							items: [
								{ slug: 'us', label: '개요', translations: { en: 'Overview', ja: '概要' } },
								{ slug: 'us/fedramp' },
								{ slug: 'us/hipaa' },
								{ slug: 'us/itar' },
								{ slug: 'us/state-privacy' },
								{ slug: 'us/ai-policy' },
							],
						},
						{
							label: 'EU',
							collapsed: true,
							items: [
								{ slug: 'eu', label: '개요', translations: { en: 'Overview', ja: '概要' } },
								{ slug: 'eu/gdpr-sovereignty' },
								{ slug: 'eu/dora' },
								{ slug: 'eu/nis2-ai-act' },
								{ slug: 'eu/national-schemes' },
								{ slug: 'eu/sovereign-ai' },
							],
						},
						{
							label: '일본',
							translations: { en: 'Japan', ja: '日本' },
							collapsed: true,
							items: [
								{ slug: 'japan', label: '개요', translations: { en: 'Overview', ja: '概要' } },
								{ slug: 'japan/ismap' },
								{ slug: 'japan/appi' },
								{ slug: 'japan/government-cloud' },
								{ slug: 'japan/ai-landscape' },
							],
						},
						{
							label: '싱가포르',
							translations: { en: 'Singapore', ja: 'シンガポール' },
							collapsed: true,
							items: [
								{ slug: 'singapore', label: '개요', translations: { en: 'Overview', ja: '概要' } },
								{ slug: 'singapore/mtcs' },
								{ slug: 'singapore/pdpa' },
								{ slug: 'singapore/government-cloud' },
								{ slug: 'singapore/ai-governance' },
							],
						},
					],
				},
			],
		}),
	],
});
