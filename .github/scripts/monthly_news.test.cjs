const {test} = require('node:test');
const assert = require('node:assert/strict');
const news = require('./monthly_news.cjs');
test('outage backlog is bounded, and current and previous day are always refreshed', () => {
  const p = news.initialize('2026-11-10', null), first = news.plan(p, '2026-11-10');
  assert.equal(p.started_on, '2026-10-01');
  assert.equal(p.before_start, 'unverified');
  assert.deepEqual(first.aws, ['2026-10-01','2026-10-02','2026-11-09','2026-11-10']);
  const next = news.apply(p, [{date:'2026-10-01',vendor:'aws',state:'complete'}, {date:'2026-10-02',vendor:'aws',state:'failed'}]);
  assert.deepEqual(news.plan(next,'2026-11-10').aws, ['2026-10-02','2026-10-03','2026-11-09','2026-11-10']);
  assert.ok(news.pending(next,'2026-11-10') > 0);
});
test('failed refresh leaves the day pending because late releases may be missing', () => {
  const p = news.initialize('2026-11-01', null);
  const a = news.apply(p, [{date:'2026-10-31',vendor:'oci',state:'complete'}]);
  const b = news.apply(a, [{date:'2026-10-31',vendor:'oci',state:'failed'}]);
  assert.equal(b.days['2026-10-31'].oci,'failed');
});
test('bad progress never turns into an empty successful plan', () => {
  assert.throws(() => news.plan({version:1,started_on:'2026-99-01',before_start:'unverified',days:{}},'2026-11-01'));
});
