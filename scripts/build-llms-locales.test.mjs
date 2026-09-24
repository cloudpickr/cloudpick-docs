/**
 * build-llms-locales.mjs cleanBody 회귀 테스트 — FENCE-AWARE 검증.
 *
 * 핵심 회귀: cleanBody가 코드펜스를 추적하지 않으면 펜스 내부의 코드 예제(`import ...`,
 * `<Component/>` 등)가 훼손되어 en/ja llms-full의 코드 샘플이 깨진다. 이 테스트는
 * 펜스 밖은 정리하고 펜스 안은 원문 보존하는지 고정한다.
 *
 * 실행: node --test scripts/build-llms-locales.test.mjs
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

// build-llms-locales.mjs는 import 시 main()을 자동 실행하므로, cleanBody 함수 소스만
// 추출해 평가한다(부작용 없이 순수 함수만 테스트).
const here = dirname(fileURLToPath(import.meta.url));
const src = readFileSync(join(here, 'build-llms-locales.mjs'), 'utf-8');
const start = src.indexOf('function cleanBody');
assert.ok(start > 0, 'cleanBody 함수를 찾을 수 없음');
// 함수 끝: 최상위 닫는 중괄호 다음 줄
const end = src.indexOf('\n}\n', start) + 3;
const cleanBody = new Function(src.slice(start, end) + '\nreturn cleanBody;')();

test('펜스 밖 import/JSX는 제거된다(기존 동작 유지)', () => {
  const out = cleanBody('import Foo from "bar";\n\n<Tabs>\ncontent\n</Tabs>\n\n실제 문단.');
  assert.ok(!out.includes('import Foo'), '펜스 밖 import 제거');
  assert.ok(!out.includes('<Tabs>'), '펜스 밖 Tabs 제거');
  assert.ok(out.includes('실제 문단'), '산문 유지');
});

test('펜스 안 코드는 원문 보존된다(fence-aware 수정)', () => {
  const body = [
    '```js',
    'import X from "y";',
    '<Component prop="1" />',
    'const a = 1;',
    '```',
  ].join('\n');
  const out = cleanBody(body);
  assert.ok(out.includes('import X from "y";'), '펜스 안 import 보존');
  assert.ok(out.includes('<Component prop="1" />'), '펜스 안 JSX 보존');
  assert.ok(out.includes('const a = 1;'), '펜스 안 코드 보존');
});

test('~~~ 펜스와 혼합 본문도 올바르게 처리', () => {
  const body = [
    'import Outside from "x";',   // 제거 대상
    '',
    '~~~python',
    'import os  # 보존 대상',
    '~~~',
  ].join('\n');
  const out = cleanBody(body);
  assert.ok(!out.includes('import Outside'), '펜스 밖 import 제거');
  assert.ok(out.includes('import os  # 보존 대상'), '~~~ 펜스 안 import 보존');
});
