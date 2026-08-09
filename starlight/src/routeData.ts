// 국가 특화(korea/ 등) 그룹은 현재 모든 로케일에 노출한다.
// (과거에는 en/ja에서 숨겼으나, 국가별 콘텐츠를 3개 언어로 제공하기로 결정)
// 로케일별 사이드바 조작이 다시 필요해지면 이 미들웨어에서 처리한다.
import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

export const onRequest = defineRouteMiddleware(() => {});
