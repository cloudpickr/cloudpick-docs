/**
 * Edge Function: Accept-Language 기반 로케일 자동 리디렉트
 * / 경로에서만 동작하여 사용자 브라우저 언어에 따라 적절한 로케일로 안내합니다.
 */

const SUPPORTED_LOCALES = ["ko", "en", "ja"] as const;
const DEFAULT_LOCALE = "ko";

function parseAcceptLanguage(header: string | null): string {
  if (!header) return DEFAULT_LOCALE;

  const langs = header
    .split(",")
    .map((part) => {
      const [lang, qStr] = part.trim().split(";q=");
      return { lang: lang.split("-")[0].toLowerCase(), q: qStr ? parseFloat(qStr) : 1.0 };
    })
    .sort((a, b) => b.q - a.q);

  for (const { lang } of langs) {
    if ((SUPPORTED_LOCALES as readonly string[]).includes(lang)) {
      return lang;
    }
  }
  return DEFAULT_LOCALE;
}

export default async function handler(request: Request) {
  const url = new URL(request.url);

  // / 경로에서만 동작
  if (url.pathname !== "/") {
    return;
  }

  const acceptLang = request.headers.get("accept-language");
  const locale = parseAcceptLanguage(acceptLang);

  return new Response(null, {
    status: 302,
    headers: {
      Location: `/${locale}/introduction/`,
      "Cache-Control": "no-cache",
    },
  });
}

export const config = {
  path: "/",
};
