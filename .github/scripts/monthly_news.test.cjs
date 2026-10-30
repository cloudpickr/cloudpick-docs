const {test} = require('node:test');
const assert = require('node:assert/strict');
const news = require('./monthly_news.cjs');
test('outage backlog is bounded, and current and previous day are always refreshed', () => {
  const p = news.initialize('2026-11-10', null), first = news.plan(p, '2026-11-10');
  assert.equal(p.started_on, '2026-10-01');
  assert.equal(p.before_start, 'unverified');
  assert.deepEqual(first.aws, ['2026-10-01','2026-10-02','2026-11-09','2026-11-10']);
  const next = news.apply(p, [{date:'2026-10-01',vendor:'aws',state:'complete'}, {date:'2026-10-02',vendor:'aws',state:'failed'}]);
  assert.deepEqual(news.plan(next,'2026-11-10').aws, ['2026-10-03','2026-10-04','2026-11-09','2026-11-10']);
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
  assert.throws(() => news.validate({version:1,started_on:'2026-10-01',before_start:'unverified',days:{},attempted:{'2026-10-01':{aws:'2026-10-02T00:00:00Z'}}}));
});
test('an unfinished day is retried after a skipped run', () => {
  const p = news.initialize('2026-10-10', null);
  const a = news.apply(p, [{date:'2026-10-10',vendor:'aws',state:'provisional'}], '2026-10-10T00:15:00Z');
  assert.ok(news.plan(a,'2026-10-12',10).aws.includes('2026-10-10'));
});
test('repeatedly failing dates do not starve other missing days', () => {
  let p = {version:1,started_on:'2026-10-01',before_start:'unverified',days:{},attempted:{}};
  p = news.apply(p, ['2026-10-01','2026-10-02'].map(date => ({date,vendor:'aws',state:'failed'})), '2026-10-10T00:15:00Z');
  assert.deepEqual(news.plan(p,'2026-10-10').aws.slice(0,2),['2026-10-03','2026-10-04']);
});
test('malformed, error and truncated source responses never count as complete', () => {
  const response = text => ({result:{content:[{text}]}});
  assert.deepEqual(news.parseResponse(response('[]'),50),[]);
  assert.throws(() => news.parseResponse({result:{isError:true,content:[{text:'[]'}]}},50));
  assert.throws(() => news.parseResponse(response('invalid'),50));
  assert.throws(() => news.parseResponse(response('[1,2] 10건 중 2건'),50));
  try { news.parseResponse(response('[1,2] 10건 중 2건'),50); } catch (e) { assert.deepEqual(e.partialRows,[1,2]); }
  assert.throws(() => news.parseResponse(response('[1,2]'),2));
});
test('provisional late-arrival checks and older gaps both get capacity', () => {
  const p = {version:1,started_on:'2026-10-01',before_start:'unverified',days:{'2026-10-08':{aws:'provisional'}},attempted:{'2026-10-08':{aws:'2026-10-09T00:00:00Z'}}};
  const plan = news.plan(p,'2026-10-10').aws;
  assert.ok(plan.includes('2026-10-08'));
  assert.ok(plan.includes('2026-10-01'));
});
test('dates remain provisional for a week, and truncation never completes', () => {
  assert.equal(news.stateFor('2026-10-10','2026-10-10'),'provisional');
  assert.equal(news.stateFor('2026-10-04','2026-10-10'),'provisional');
  assert.equal(news.stateFor('2026-10-03','2026-10-10'),'complete');
  assert.equal(news.stateFor('2026-10-03','2026-10-10',true),'failed');
  assert.throws(() => news.stateFor('2026-10-11','2026-10-10'));
});
