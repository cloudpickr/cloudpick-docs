import assert from 'node:assert/strict';
import test from 'node:test';

import {
  checkChunks,
  extractKoreanUrls,
  getGithubOidcToken,
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
    'header.payload.signature',
    async (_endpoint, options) => {
      const body = JSON.parse(options.body);
      sizes.push(body.urls.length);
      assert.equal(options.headers.Authorization, 'Bearer header.payload.signature');
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

test('requests a repository identity token with a fixed audience', async () => {
  const token = await getGithubOidcToken(
    {
      ACTIONS_ID_TOKEN_REQUEST_URL: 'https://token.actions.githubusercontent.com/request?job=1',
      ACTIONS_ID_TOKEN_REQUEST_TOKEN: 'runtime-token',
    },
    async (endpoint, options) => {
      assert.equal(endpoint.searchParams.get('audience'), 'ncp://cloudpick-link-checker');
      assert.equal(options.headers.Authorization, 'Bearer runtime-token');
      return { ok: true, json: async () => ({ value: 'header.payload.signature' }) };
    },
  );
  assert.equal(token, 'header.payload.signature');
});
