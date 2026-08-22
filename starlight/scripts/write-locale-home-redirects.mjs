/**
 * Starlight generates real splash pages at /, /ko/, /en/, /ja/.
 * Locale-home HTTP redirects are host-dependent (Netlify needs force;
 * Cloudflare Pages serves matching files first), so we replace those
 * four HTML files with an explicit client+meta redirect after every build.
 */
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');

/** @type {Array<[string, string, string]>} dest path, target URL, html lang */
const stubs = [
	['index.html', '/ko/introduction/', 'ko'],
	['ko/index.html', '/ko/introduction/', 'ko'],
	['en/index.html', '/en/introduction/', 'en'],
	['ja/index.html', '/ja/introduction/', 'ja'],
];

function stub(target, lang) {
	const safe = target.replace(/"/g, '');
	return `<!DOCTYPE html>
<html lang="${lang}">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0;url=${safe}">
<link rel="canonical" href="${safe}">
<title>Redirecting…</title>
<script>location.replace(${JSON.stringify(safe)});</script>
</head>
<body>
<p><a href="${safe}">Continue to CloudPick Docs</a></p>
</body>
</html>
`;
}

for (const [rel, target, lang] of stubs) {
	const file = join(dist, rel);
	mkdirSync(dirname(file), { recursive: true });
	writeFileSync(file, stub(target, lang));
}
