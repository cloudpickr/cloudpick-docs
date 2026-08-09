// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLlmsTxt from 'starlight-llms-txt';

// https://astro.build/config
// 정적 사이트이므로 어댑터 불필요 — Cloudflare Pages에는 dist/를 wrangler pages deploy로 올린다.
export default defineConfig({
	site: 'https://docs.cloudpick.kr',
	output: 'static',
	integrations: [
		starlight({
			title: 'CloudPick',
			description: '멀티클라우드 환경에서 올바른 의사결정을 내리기 위한 벤더 중립 가이드',
			defaultLocale: 'ko',
			locales: {
				ko: { label: '한국어', lang: 'ko' },
				en: { label: 'English', lang: 'en' },
				ja: { label: '日本語', lang: 'ja' },
			},
			plugins: [starlightLlmsTxt()],
			routeMiddleware: './src/routeData.ts',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/cloudpick-docs/cloudpick-docs' },
			],
			sidebar: [
				{
					label: 'Getting Started',
					translations: { ko: '시작하기', ja: 'はじめに' },
					items: [
						{ slug: 'about-cloud/getting-started' },
						{ slug: 'about-cloud/compare-clouds' },
						{ slug: 'about-cloud/decision-framework' },
						{ slug: 'about-cloud/regions-and-zones' },
						{ slug: 'about-cloud/shared-responsibility' },
						{ slug: 'about-cloud/accounts-and-organizations' },
						{ slug: 'about-cloud/iam-overview' },
						{ slug: 'about-cloud/console-cli-sdk' },
						{ slug: 'about-cloud/pricing-model' },
						{ slug: 'about-cloud/why-multicloud' },
						{ slug: 'about-cloud/well-architected' },
						{ slug: 'about-cloud/support-plans' },
						{ slug: 'about-cloud/field-deployment' },
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
						{ slug: 'devops/getting-started' },
						{ slug: 'devops/cicd' },
						{ slug: 'devops/iac' },
						{ slug: 'devops/devsecops' },
						{ slug: 'devops/monitoring' },
						{ slug: 'devops/slo' },
						{ slug: 'devops/observability' },
						{ slug: 'devops/remote-access' },
						{ slug: 'devops/patch-and-vulnerability' },
						{ slug: 'devops/kubernetes-operations' },
						{ slug: 'devops/platform-engineering' },
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
						{ slug: 'ai/getting-started' },
						{ slug: 'ai/ai-ml' },
						{ slug: 'ai/prompt-engineering' },
						{ slug: 'ai/rag-patterns' },
						{ slug: 'ai/vector-store' },
						{ slug: 'ai/agents' },
						{ slug: 'ai/agent-adoption' },
						{ slug: 'ai/1p-vs-3p' },
						{ slug: 'ai/licensing' },
						{ slug: 'ai/llmops' },
						{ slug: 'ai/multicloud-ai' },
					],
				},
				{
					label: '용어집',
					translations: { en: 'Glossary', ja: '用語集' },
					link: 'glossary',
				},
				{
					label: '한국 특화',
					translations: { en: 'Korea-Specific', ja: '韓国特化' },
					items: [
						{ slug: 'korea' },
						{ slug: 'korea/security/csap' },
						{ slug: 'korea/security/network-isolation' },
						{ slug: 'korea/ai/sovereign-fm-policy' },
						{ slug: 'korea/ai/fm-providers' },
					],
				},
			],
		}),
	],
});
