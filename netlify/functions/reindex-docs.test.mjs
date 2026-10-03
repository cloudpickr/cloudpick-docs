/**
 * /api/reindex 인증 fail-closed 회귀 테스트.
 *
 * REINDEX_TOKEN이 없거나 빈 문자열이면 401이고 Blob을 읽지 않는다.
 * 토큰이 있으면 Authorization Bearer 일치 시에만 기존 Blob 조회를 유지한다.
 *
 * 실행:
 *   node --experimental-test-module-mocks --test netlify/functions/reindex-docs.test.mjs
 */
import { mock, test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';

const blob = {
  getDeployStoreCalls: 0,
  getCalls: 0,
  value: null,
  error: null,
  storeName: undefined,
  key: undefined,
  opts: undefined,
};

mock.module('@netlify/blobs', {
  exports: {
    getDeployStore(name) {
      blob.getDeployStoreCalls += 1;
      blob.storeName = name;
      return {
        async get(key, opts) {
          blob.getCalls += 1;
          blob.key = key;
          blob.opts = opts;
          if (blob.error) throw blob.error;
          return blob.value;
        },
      };
    },
  },
});

const env = {};
globalThis.Netlify = {
  env: {
    get(name) {
      return env[name];
    },
  },
};

const { default: handler } = await import('./reindex-docs.mts');

function resetBlob() {
  blob.getDeployStoreCalls = 0;
  blob.getCalls = 0;
  blob.value = null;
  blob.error = null;
  blob.storeName = undefined;
  blob.key = undefined;
  blob.opts = undefined;
}

beforeEach(() => {
  resetBlob();
  delete env.REINDEX_TOKEN;
});

function makeRequest(authorization) {
  const init = {};
  if (authorization !== undefined) {
    init.headers = { authorization };
  }
  return new Request('https://docs.cloudpick.kr/api/reindex', init);
}

function assertBlobUntouched() {
  assert.equal(blob.getDeployStoreCalls, 0);
  assert.equal(blob.getCalls, 0);
}

test('REINDEX_TOKEN이 없으면 401이고 Blob을 읽지 않는다', async () => {
  const res = await handler(makeRequest('Bearer anything'));
  assert.equal(res.status, 401);
  assert.deepEqual(await res.json(), { error: 'Unauthorized' });
  assertBlobUntouched();
});

test('REINDEX_TOKEN이 빈 문자열이면 401이고 Blob을 읽지 않는다', async () => {
  env.REINDEX_TOKEN = '';
  const res = await handler(makeRequest('Bearer '));
  assert.equal(res.status, 401);
  assert.deepEqual(await res.json(), { error: 'Unauthorized' });
  assertBlobUntouched();
});

test('토큰이 있으면 Bearer가 없거나 다르면 401이고 Blob을 읽지 않는다', async () => {
  env.REINDEX_TOKEN = 'secret';

  const missing = await handler(makeRequest());
  assert.equal(missing.status, 401);
  assert.deepEqual(await missing.json(), { error: 'Unauthorized' });
  assertBlobUntouched();

  const wrong = await handler(makeRequest('Bearer other'));
  assert.equal(wrong.status, 401);
  assert.deepEqual(await wrong.json(), { error: 'Unauthorized' });
  assertBlobUntouched();
});

test('Bearer가 일치하면 기존 Blob 조회와 응답을 유지한다', async () => {
  env.REINDEX_TOKEN = 'secret';
  blob.value = 'abcdef';

  const res = await handler(makeRequest('Bearer secret'));
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), {
    status: 'ok',
    message: 'Blob data exists and is accessible',
    size: 6,
  });
  assert.equal(blob.getDeployStoreCalls, 1);
  assert.equal(blob.storeName, 'mcp-docs');
  assert.equal(blob.getCalls, 1);
  assert.equal(blob.key, 'llms-full');
  assert.deepEqual(blob.opts, { type: 'text' });
});

test('Bearer가 일치하고 Blob이 없으면 기존 empty 응답을 유지한다', async () => {
  env.REINDEX_TOKEN = 'secret';
  blob.value = null;

  const res = await handler(makeRequest('Bearer secret'));
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), {
    status: 'empty',
    message: 'Blob data not found. Push a commit to trigger rebuild.',
  });
  assert.equal(blob.getDeployStoreCalls, 1);
  assert.equal(blob.getCalls, 1);
});

test('Bearer가 일치하고 Blob 조회가 실패하면 기존 500 응답을 유지한다', async () => {
  env.REINDEX_TOKEN = 'secret';
  blob.error = new Error('blob down');

  const res = await handler(makeRequest('Bearer secret'));
  assert.equal(res.status, 500);
  assert.deepEqual(await res.json(), { error: 'Error: blob down' });
  assert.equal(blob.getDeployStoreCalls, 1);
  assert.equal(blob.getCalls, 1);
});
