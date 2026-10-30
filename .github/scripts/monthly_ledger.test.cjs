const {test} = require('node:test');
const assert = require('node:assert/strict');
const ledger = require('./monthly_ledger.cjs');
const path = 'src/content/docs/ko/compute/test.md';

test('new inventory is unreviewed, never verified by scanning', () => {
  const l = ledger.build('2026-10', [path], null, null);
  assert.equal(l.documents[0].status, 'unreviewed');
  assert.deepEqual(ledger.parse(ledger.render('body', l)), l);
});
test('same month preserves human state and deduplicates repeated findings', () => {
  const c = {path, axis: 1, reason: 'Preview'};
  const l = ledger.build('2026-10', [path], null, null, [c]);
  l.documents[0].status = 'verified'; l.documents[0].evidence = ['https://example.org/official'];
  l.items[0].status = 'hold';
  const next = ledger.build('2026-10', [path], null, l, [c]);
  assert.equal(next.documents[0].status, 'verified');
  assert.equal(next.items.length, 1);
  assert.equal(next.items[0].status, 'hold');
});
test('new month carries unfinished items and retains closed IDs to prevent rediscovery', () => {
  const l = ledger.build('2026-10', [path], null, null, [{path, axis: 1, reason: 'a'}, {path, axis: 2, reason: 'b'}]);
  l.items[1].status = 'done'; l.items[1].pr = 'https://github.com/example/repo/pull/1';
  l.documents[0].status = 'verified'; l.documents[0].evidence = ['https://example.org'];
  const next = ledger.build('2026-11', [path], l, null);
  assert.equal(next.documents[0].status, 'unreviewed');
  assert.equal(next.items.length, 1);
  assert.equal(next.items.filter(i => i.status === 'open').length, 1);
  assert.deepEqual(next.resolved_ids, [l.items[1].id]);
  assert.equal(next.items[0].carried_from, '2026-10');
});
test('malformed ledgers and unsubstantiated verification fail closed', () => {
  assert.throws(() => ledger.parse('<!-- monthly-ledger:start --> invalid <!-- monthly-ledger:end -->'));
  const l = ledger.build('2026-10', [path], null, null); l.documents[0].status = 'verified';
  assert.throws(() => ledger.render('', l));
});
test('deleted paths remain visible for human reconciliation', () => {
  const l = ledger.build('2026-10', [path], null, null);
  const missing = ledger.build('2026-10', [], null, l);
  assert.equal(missing.documents[0].missing_from_inventory, true);
  assert.equal(ledger.build('2026-10', [path], null, missing).documents[0].missing_from_inventory, undefined);
});
test('unmapped topic and structure signals can be carried without inventing a document', () => {
  const l = ledger.build('2026-10', [path], null, null, [{path: null, axis: 3, reason: 'unmapped vendor update'}]);
  const next = ledger.build('2026-11', [path], l, null, [{path: null, axis: 3, reason: 'unmapped vendor update'}]);
  assert.equal(next.items.length, 1);
  assert.equal(next.items[0].status, 'open');
});
test('candidate text cannot inject a ledger delimiter', () => {
  const l = ledger.build('2026-10', [path], null, null, [{path, axis: 1, reason: 'example <!-- monthly-ledger:end -->'}]);
  assert.deepEqual(ledger.parse(ledger.render('issue body', l)), l);
});
