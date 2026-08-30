/**
 * CloudPick 로케일 단일 정의 지점 (Single Source of Truth for build-time consumers).
 *
 * 배경:
 *   과거에는 언어 목록이 4곳에 중복 하드코딩되어 새 언어 추가 시 누락·드리프트가 발생했다:
 *   astro.config.mjs / scripts/build-llms-locales.mjs / plugins/upload-llms-blob/index.js /
 *   netlify/functions/blob-healthcheck.mts.
 *
 *   이 모듈이 그 목록의 유일한 정의 지점이다. 위 4곳은 여기서 import 한다.
 *
 * 새 언어 추가 방법:
 *   1. 아래 LOCALE_DEFS 에 항목 추가 (id/label/lang). 이것만으로 빌드·업로드·헬스체크가 자동 반영됨.
 *   2. 그리고 MCP 함수(netlify/functions/mcp.mts)의 SUPPORTED_LANGS + detectScriptLang 정규식 +
 *      LANG_PARAM.enum + 빈 결과 메시지를 함께 갱신한다. (언어별 스크립트 감지 규칙은 자동화 불가 —
 *      사람이 직접 작성/검증해야 한다. MCP 함수는 서버리스 런타임 격리 때문에 자체 상수를 유지하며,
 *      startup 단언으로 이 모듈과의 드리프트를 방지한다.)
 *
 * ⚠️ 이 파일은 의존성이 없어야 하고(순수 데이터), astro.config가 로드할 수 있도록 ESM·부작용 없음을 유지할 것.
 */

/**
 * @typedef {Object} LocaleDef
 * @property {string} id      로케일 ID (경로/blob 키에 사용). 예: 'ko'
 * @property {string} label   Starlight 언어 선택기 라벨. 예: '한국어'
 * @property {string} lang    BCP-47 lang 코드. 예: 'ko'
 */

/** @type {LocaleDef[]} 순서 = 우선순위. 첫 항목이 기본 로케일(SOT). */
export const LOCALE_DEFS = [
  { id: 'ko', label: '한국어', lang: 'ko' },
  { id: 'en', label: 'English', lang: 'en' },
  { id: 'ja', label: '日本語', lang: 'ja' },
];

/** 로케일 ID 배열. 예: ['ko','en','ja'] */
export const LOCALES = LOCALE_DEFS.map((l) => l.id);

/** 기본 로케일(폴백·SOT). 첫 항목. */
export const DEFAULT_LOCALE = LOCALE_DEFS[0].id;

/** Starlight `locales` 객체 형태: { ko: { label, lang }, ... } */
export const STARLIGHT_LOCALES = Object.fromEntries(
  LOCALE_DEFS.map(({ id, label, lang }) => [id, { label, lang }]),
);

/** 언어별 llms-full blob 키. 예: llms-full-ko */
export const blobKeyFor = (id) => `llms-full-${id}`;

/** 모든 언어의 blob 키 배열. 헬스체크가 사용. */
export const LANG_BLOB_KEYS = LOCALES.map(blobKeyFor);
