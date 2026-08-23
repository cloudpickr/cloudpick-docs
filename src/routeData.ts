// 국가 특화(korea/ 등) 그룹은 현재 모든 로케일에 노출한다.
// (과거에는 en/ja에서 숨겼으나, 국가별 콘텐츠를 3개 언어로 제공하기로 결정)
import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

const OG_LOCALE: Record<string, string> = {
	ko: 'ko_KR',
	en: 'en_US',
	ja: 'ja_JP',
};

export const onRequest = defineRouteMiddleware(({ locals }) => {
	const lang = locals.starlightRoute.lang || 'ko';
	const primary = OG_LOCALE[lang] ?? 'ko_KR';
	const head = locals.starlightRoute.head;

	const localeTag = head.find((h) => h.tag === 'meta' && h.attrs?.property === 'og:locale');
	if (localeTag?.attrs) {
		localeTag.attrs.content = primary;
	} else {
		head.push({ tag: 'meta', attrs: { property: 'og:locale', content: primary } });
	}

	for (let i = head.length - 1; i >= 0; i--) {
		if (head[i].tag === 'meta' && head[i].attrs?.property === 'og:locale:alternate') {
			head.splice(i, 1);
		}
	}
	for (const [code, locale] of Object.entries(OG_LOCALE)) {
		if (code === lang) continue;
		head.push({ tag: 'meta', attrs: { property: 'og:locale:alternate', content: locale } });
	}
});
