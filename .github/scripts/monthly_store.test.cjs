const {test} = require('node:test');
const assert = require('node:assert/strict');
const store = require('./monthly_store.cjs');
const ledger = require('./monthly_ledger.cjs');
const path = 'src/content/docs/ko/test.md';
const ctx = {repo:{owner:'org',repo:'repo'}};

function fixture(body) {
  const state = {body, comments: [], failAt: 0, changed: false};
  const github = {rest:{issues:{
    listComments: {},
    createComment: async ({body}) => { if (state.failAt && state.comments.length + 1 === state.failAt) throw Error('network failure'); state.comments.push({body, user:{login:'github-actions[bot]'}}); },
    get: async () => ({data:{number:1,body:state.changed ? state.body+' human edit' : state.body}}),
    update: async ({body}) => {state.body = body;},
  }}, paginate: async () => state.comments};
  return {state,github};
}

test('large ledger splits into bounded human-readable comments and round trips', async () => {
  const rows = Array.from({length:1500}, (_,i) => ({path, axis:2, reason:`news ${i} ${'x'.repeat(100)}`}));
  const data = ledger.build('2026-10',[path],null,null,rows);
  const parts = store.makeParts(data, 'a'.repeat(32));
  assert.ok(parts.length > 3);
  for (const part of parts) assert.ok(Buffer.byteLength(store.partBody(part)) < 60000);
  const comments = parts.map(part => ({body:store.partBody(part),user:{login:'github-actions[bot]'}}));
  assert.deepEqual(store.assemble({id:'a'.repeat(32),count:parts.length,month:'2026-10'},comments),data);
  assert.throws(() => store.assemble({id:'a'.repeat(32),count:parts.length,month:'2026-10'},comments.slice(1)));
});

test('partial snapshot write leaves legacy ledger authoritative and retry succeeds', async () => {
  const data = ledger.build('2026-10',[path],null,null);
  const {state,github} = fixture(ledger.render('user text',data));
  const issue = {number:1,body:state.body}; state.failAt = 2;
  await assert.rejects(store.save(github,ctx,issue,data), /network failure/);
  assert.deepEqual(await store.load(github,ctx,issue),data);
  state.failAt = 0;
  await store.save(github,ctx,issue,data,{expected:data});
  assert.ok(state.body.includes('user text'));
  assert.deepEqual(await store.load(github,ctx,{number:1,body:state.body}),data);
});

test('body change during save keeps old snapshot authoritative', async () => {
  const data = ledger.build('2026-10',[path],null,null);
  const {state,github} = fixture(ledger.render('body',data));
  const issue = {number:1,body:state.body}; state.changed = true;
  await assert.rejects(store.save(github,ctx,issue,data), /changed/);
  assert.deepEqual(ledger.parse(state.body),data);
});

test('unknown or non-bot parts cannot silently complete a snapshot', () => {
  const data = ledger.build('2026-10',[path],null,null), parts = store.makeParts(data,'b'.repeat(32));
  const comments = parts.map(part => ({body:store.partBody(part),user:{login:'human'}}));
  assert.throws(() => store.assemble({id:'b'.repeat(32),count:parts.length,month:'2026-10'},comments));
});
test('news coverage metadata survives snapshot sharding', () => {
  const data = ledger.build('2026-10',[path],null,null);
  data.news_progress = {version:1,started_on:'2026-09-01',before_start:'unverified',days:{'2026-09-01':{aws:'complete'},'2026-09-02':{aws:'failed'}}};
  const parts = store.makeParts(data,'c'.repeat(32));
  const comments = parts.map(part => ({body:store.partBody(part),user:{login:'github-actions[bot]'}}));
  assert.deepEqual(store.assemble({id:'c'.repeat(32),count:parts.length,month:'2026-10'},comments),data);
});
test('part size limit accounts for escaped marker and fence characters', () => {
  const rows = Array.from({length:100}, (_,i) => ({path, axis:2, reason:`news ${i} ${'<`'.repeat(250)}`}));
  const parts = store.makeParts(ledger.build('2026-10',[path],null,null,rows),'d'.repeat(32));
  for (const part of parts) assert.ok(Buffer.byteLength(store.partBody(part)) < 60000);
});
