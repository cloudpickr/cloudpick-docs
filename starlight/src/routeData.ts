import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

// '한국 특화(korea/)' 사이드바 그룹은 ko 로케일에서만 노출한다.
// 페이지 자체는 폴백으로 en/ja URL에서도 접근 가능하지만 내비게이션에는 표시하지 않는다.
export const onRequest = defineRouteMiddleware((context) => {
	const { starlightRoute } = context.locals;
	if (starlightRoute.locale === 'ko') return;
	starlightRoute.sidebar = starlightRoute.sidebar.filter(
		(entry) =>
			!(
				entry.type === 'group' &&
				entry.entries.some((e) => e.type === 'link' && e.href.includes('/korea/'))
			),
	);
});
