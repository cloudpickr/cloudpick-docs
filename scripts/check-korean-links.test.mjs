import assert from 'node:assert/strict';
import test from 'node:test';

import {
  checkChunks,
  extractKoreanUrls,
  hostnameAllowed,
  validateEndpoint,
} from './check-korean-links.mjs';

test('extracts only allowlisted Korean links', () => {
  const urls = extractKoreanUrls(`
    [law](https://www.law.go.kr/test)
    [cloud](https://docs.aws.amazon.com/test)
    [spoof](https://go.kr.evil.example/test)
  `);
  assert.deepEqual(urls, ['https://www.law.go.kr/test']);
  assert.equal(hostnameAllowed('isms.kisa.or.kr'), true);
});

test('invocation endpoint cannot exfiltrate the API key', () => {
  assert.equal(validateEndpoint('https://abc.apigw.ntruss.com/link-checker/v1').hostname, 'abc.apigw.ntruss.com');
  assert.throws(() => validateEndpoint('https://example.com/steal'), /apigw\.ntruss\.com/);
  assert.throws(() => validateEndpoint('http://abc.apigw.ntruss.com/test'), /HTTPS/);
});

test('chunks requests at ten URLs', async () => {
  const sizes = [];
  const urls = Array.from({ length: 11 }, (_, index) => `https://law.go.kr/${index}`);
  const results = await checkChunks(
    urls,
    new URL('https://abc.apigw.ntruss.com/link-checker/v1'),
    'secret',
    async (_endpoint, options) => {
      const body = JSON.parse(options.body);
      sizes.push(body.urls.length);
      return {
        ok: true,
        json: async () => ({
          results: body.urls.map((url) => ({ url, status: 200, classification: 'alive' })),
        }),
      };
    },
  );
  assert.deepEqual(sizes, [10, 1]);
  assert.equal(results.length, 11);
});
