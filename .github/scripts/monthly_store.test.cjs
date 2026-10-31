const {test} = require('node:test');
const assert = require('node:assert/strict');
const store = require('./monthly_store.cjs');
const ledger = require('./monthly_ledger.cjs');
const path = 'src/content/docs/ko/test.md';
const ctx = {repo:{owner:'org',repo:'repo'}};

test('monthly issue summary shows recorded PRs and carried work without claiming merge', () => {
  const data = ledger.build('2026-10',[path],null,null,[
    {path, axis:1, reason:'completed'}, {path, axis:1, reason:'carried'}
  ]);
  data.items[0].status = 'done'; data.items[0].pr = 'https://github.com/org/repo/pull/12';
  data.items[1].carried_from = '2026-09';
  const body = store.renderPointer('기존 기록', data, store.makeParts(data));
  assert.match(body, /완료로 기록된 후보 1개, 처리 대기 1개\(그중 이전 달 이월 1개\)/);
  assert.ok(body.includes(data.items[0].pr));
  assert.match(body, /실제 머지 여부는 담당자가 확인/);
  assert.match(body, /기존 기록/);
});

function fixture(body) {
  const state = {body, comments: [], failAt: 0, failComment: false, changed: false, head:null, blobs:{}, trees:{base:{}}, commits:{base:{tree:{sha:'base'}}}, next:0};
  const notFound = () => Object.assign(new Error('missing'), {status:404});
  const github = {rest:{issues:{
    listComments: {},
    createComment: async ({body}) => { if (state.failComment) throw Error('comment failed'); state.comments.push({id:10000+state.comments.length,body, user:{login:'github-actions[bot]'}}); },
    updateComment: async ({comment_id,body}) => { if (state.failComment) throw Error('comment failed'); const c=state.comments.find(c=>c.id===comment_id); if (!c) throw Error('missing comment'); c.body=body; },
    get: async () => ({data:{number:1,body:state.changed ? state.body+' human edit' : state.body}}),
    update: async () => {throw Error('issue body must not be updated');},
  },repos:{
    get:async()=>({data:{default_branch:'master'}}),
    getContent:async({path,ref})=>{const sha=state.trees[state.commits[ref]?.tree.sha]?.[path]; if (!sha) throw notFound(); return {data:{type:'file',sha}};},
  },git:{
    getRef:async({ref})=>{const sha=ref==='heads/master'?'base':state.head; if(!sha) throw notFound(); return {data:{object:{sha}}};},
    createRef:async({sha})=>{state.head=sha;},
    getCommit:async({commit_sha})=>({data:state.commits[commit_sha]}),
    createBlob:async({content})=>{const sha=`blob${++state.next}`;state.blobs[sha]=content;return {data:{sha}};},
    getBlob:async({file_sha})=>({data:{encoding:'base64',content:state.blobs[file_sha]}}),
    createTree:async({base_tree,tree})=>{const sha=`tree${++state.next}`;state.trees[sha]={...state.trees[base_tree],...Object.fromEntries(tree.map(x=>[x.path,x.sha]))};return {data:{sha}};},
    createCommit:async({tree,parents})=>{const sha=`commit${++state.next}`;state.commits[sha]={tree:{sha:tree},parent:parents[0]};return {data:{sha}};},
    updateRef:async({sha})=>{if(state.failAt) throw Error('network failure'); if(state.commits[sha].parent!==state.head) throw Error('non-fast-forward');state.head=sha;},
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
test('entire corpus and source inventory survive large multi-part snapshots', () => {
  const docs = Array.from({length:119},(_,i)=>`src/content/docs/ko/category/doc-${i}.md`);
  const rows = Array.from({length:1500},(_,i)=>({path:docs[i%docs.length],axis:2,reason:`update ${i} ${'x'.repeat(100)}`}));
  const data = ledger.build('2026-10',docs,null,null,rows);
  data.source_progress = {version:1,refs:Object.fromEntries(Array.from({length:1301},(_,i)=>[`https://example.org/${i}`,{paths:[docs[i%docs.length]],status:'observed',hash:'a'.repeat(64),checked_at:'2026-10-01T00:00:00Z'}]))};
  const parts=store.makeParts(data,'1'.repeat(32));
  assert.ok(parts.length > 10);
  const comments=parts.map(part=>({body:store.partBody(part),user:{login:'github-actions[bot]'}}));
  assert.deepEqual(store.assemble({id:'1'.repeat(32),count:parts.length,month:'2026-10'},comments),data);
});

test('state write failure leaves legacy ledger authoritative and retry succeeds', async () => {
  const data = ledger.build('2026-10',[path],null,null);
  const {state,github} = fixture(ledger.render('user text',data));
  const issue = {number:1,body:state.body}; state.failAt = 1;
  await assert.rejects(store.save(github,ctx,issue,data,{expected:data}), /network failure/);
  assert.deepEqual(await store.load(github,ctx,issue),data);
  state.failAt = 0;
  await store.save(github,ctx,issue,data,{expected:data});
  assert.ok(state.body.includes('user text'));
  assert.ok(state.comments[0].body.includes('monthly-ledger-v3:2026-10'));
  assert.equal(state.comments.length, 1);
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
test('source coverage survives sharding and distinguishes failed from unseen', () => {
  const data = ledger.build('2026-10',[path],null,null);
  data.source_progress = {version:1, refs:{'https://example.org/a':{paths:[path],status:'unverified'},'https://example.org/b':{paths:[path]}}};
  const parts=store.makeParts(data,'e'.repeat(32));
  const comments=parts.map(part => ({body:store.partBody(part),user:{login:'github-actions[bot]'}}));
  assert.deepEqual(store.assemble({id:'e'.repeat(32),count:parts.length,month:'2026-10'},comments),data);
});
test('an edit to an older snapshot after publication is detected', () => {
  const data = ledger.build('2026-10',[path],null,null);
  const old=store.makeParts(data,'a'.repeat(32)), current=store.makeParts(data,'b'.repeat(32));
  const comments=[...old,...current].map((part,i) => ({id:i+1,body:store.partBody(part),user:{login:'github-actions[bot]'},created_at:'2026-10-01T00:50:00Z',updated_at:part.id.startsWith('a') ? '2026-10-01T01:01:00Z' : '2026-10-01T00:59:00Z'}));
  assert.throws(() => store.assemble({id:'b'.repeat(32),count:current.length,month:'2026-10',published:'2026-10-01T01:00:00Z'},comments), /non-current snapshot/);
  const acknowledgements=comments.filter(c=>c.updated_at==='2026-10-01T01:01:00Z').map(store.acknowledgement).join('\n');
  assert.deepEqual(store.assemble({id:'b'.repeat(32),count:current.length,month:'2026-10',published:'2026-10-01T01:00:00Z'},comments,acknowledgements),data);
  comments[0].body += '\nchanged again';
  assert.throws(() => store.assemble({id:'b'.repeat(32),count:current.length,month:'2026-10',published:'2026-10-01T01:00:00Z'},comments,acknowledgements), /non-current snapshot/);
});
test('new orphan snapshot from a failed save does not block recovery', () => {
  const data = ledger.build('2026-10',[path],null,null);
  const current=store.makeParts(data,'a'.repeat(32)), orphan=store.makeParts(data,'b'.repeat(32));
  const comments=[...current,...orphan].map((part,i) => ({id:i+1,body:store.partBody(part),user:{login:'github-actions[bot]'},created_at:part.id.startsWith('a') ? '2026-10-01T00:50:00Z' : '2026-10-01T01:01:00Z',updated_at:part.id.startsWith('a') ? '2026-10-01T00:50:00Z' : '2026-10-01T01:01:00Z'}));
  assert.deepEqual(store.assemble({id:'a'.repeat(32),count:current.length,month:'2026-10',published:'2026-10-01T01:00:00Z'},comments),data);
  comments[comments.length-1].updated_at='2026-10-01T01:02:00Z';
  assert.throws(() => store.assemble({id:'a'.repeat(32),count:current.length,month:'2026-10',published:'2026-10-01T01:00:00Z'},comments), /non-current snapshot/);
});
test('empty and populated news attempt history survive snapshot storage', () => {
  for (const attempted of [{},{'2026-09-01':{aws:'2026-10-01T00:00:00.000Z'}}]) {
    const data = ledger.build('2026-10',[path],null,null);
    data.news_progress = {version:1,started_on:'2026-09-01',before_start:'unverified',days:{'2026-09-01':{aws:'failed'}},attempted};
    const parts=store.makeParts(data,'f'.repeat(32));
    const comments=parts.map(part => ({body:store.partBody(part),user:{login:'github-actions[bot]'}}));
    assert.deepEqual(store.assemble({id:'f'.repeat(32),count:parts.length,month:'2026-10'},comments),data);
  }
});
test('invalid metadata cannot publish an unreadable snapshot', async () => {
  const data = ledger.build('2026-10',[path],null,null);
  const {state,github} = fixture(ledger.render('body',data));
  data.news_progress = {version:1,started_on:'2026-10-01',before_start:'unverified',days:{},attempted:{'2026-10-01':{aws:'2026-10-02T00:00:00Z'}}};
  await assert.rejects(store.save(github,ctx,{number:1,body:state.body},data), /orphaned/);
  assert.equal(state.comments.length,0);
  assert.ok(ledger.parse(state.body));
});

test('state branch preserves concurrent human edits and prior snapshots', async () => {
  const data = ledger.build('2026-10',[path],null,null);
  const {state,github} = fixture('issue');
  await store.save(github,ctx,{number:1,body:state.body},data);
  const first = structuredClone(data);
  const human = structuredClone(data); human.documents[0].status='unverified';
  const issue = {number:1,body:state.body};
  await store.writeState(github,ctx,human,first,{version:3},1);
  await assert.rejects(store.save(github,ctx,issue,first,{expected:first}), /changed/);
  assert.equal((await store.load(github,ctx,issue)).documents[0].status,'unverified');
  assert.ok(state.commits[state.head].parent.startsWith('commit'));
});

test('legacy comment snapshot migrates to branch without losing records', async () => {
  const data = ledger.build('2026-10',[path],null,null,[{path,axis:1,reason:'candidate'}]);
  const parts=store.makeParts(data,'a'.repeat(32));
  const body=store.renderPointer('existing notes',data,parts);
  const {state,github}=fixture(body);
  state.comments=parts.map((part,i)=>({id:i+1,body:store.partBody(part),user:{login:'github-actions[bot]'},created_at:'2026-01-01T00:00:00Z',updated_at:'2026-01-01T00:00:00Z'}));
  const issue={number:1,body};
  await store.save(github,ctx,issue,data,{expected:data});
  assert.deepEqual(await store.load(github,ctx,{number:1,body:state.body}),data);
  assert.equal(state.comments.length,parts.length+1);
  assert.ok(state.body.includes('existing notes'));
  state.comments[0].updated_at='2099-01-01T00:00:00Z';
  await assert.rejects(store.load(github,ctx,{number:1,body:state.body}), /migrated snapshot comment/);
  state.body += '\n' + store.acknowledgement(state.comments[0]);
  assert.deepEqual(await store.load(github,ctx,{number:1,body:state.body}),data);
});

test('failed summary creation preserves state and permits retry with new data', async () => {
  const data=ledger.build('2026-10',[path],null,null);
  const body=ledger.render('human notes',data);
  const {state,github}=fixture(body);
  state.failComment=true;
  await assert.rejects(store.save(github,ctx,{number:1,body},data,{expected:data}), /comment failed/);
  assert.deepEqual(await store.stateAt(github,ctx,'2026-10',state.head),data);
  assert.deepEqual(await store.load(github,ctx,{number:1,body:state.body}),data);
  state.failComment=false;
  const next=structuredClone(data); next.documents[0].status='unverified';
  await store.save(github,ctx,{number:1,body:state.body},next,{expected:data});
  assert.deepEqual(await store.load(github,ctx,{number:1,body:state.body}),next);
});

test('branch storage round trips a corpus-sized ledger with one summary comment', async () => {
  const docs=Array.from({length:119},(_,i)=>`src/content/docs/ko/doc-${i}.md`);
  const rows=Array.from({length:1500},(_,i)=>({path:docs[i%docs.length],axis:2,reason:`release ${i} ${'x'.repeat(50)}`}));
  const data=ledger.build('2026-11',docs,null,null,rows);
  data.source_progress={version:1,refs:Object.fromEntries(Array.from({length:1301},(_,i)=>[`https://example.org/${i}`,{paths:[docs[i%docs.length]],status:'unverified'}]))};
  const {state,github}=fixture('monthly issue');
  await store.save(github,ctx,{number:1,body:state.body},data);
  assert.deepEqual(await store.load(github,ctx,{number:1,body:state.body}),data);
  assert.equal(state.comments.length,1);
});

test('a concurrent branch advance cannot be overwritten', async () => {
  const data=ledger.build('2026-10',[path],null,null);
  const body=ledger.render('notes',data);
  const {state,github}=fixture(body);
  const update=github.rest.git.updateRef;
  github.rest.git.updateRef=async args => {
    state.commits.concurrent={tree:{sha:'base'},parent:state.head};
    state.head='concurrent';
    return update(args);
  };
  await assert.rejects(store.save(github,ctx,{number:1,body},data,{expected:data}), /non-fast-forward/);
  assert.equal(state.head,'concurrent');
  assert.equal(state.body,body);
});

test('a new month remains readable and can be carried over when the first summary fails', async () => {
  const data=ledger.build('2026-11',[path],null,null,[{path,axis:1,reason:'review'}]);
  const {state,github}=fixture('human notes');
  state.failComment=true;
  await assert.rejects(store.save(github,ctx,{number:1,body:state.body},data), /comment failed/);
  const recovered=await store.load(github,ctx,{number:1,body:state.body});
  assert.equal(ledger.build('2026-12',[path],recovered,null).items[0].status,'open');
  state.failComment=false;
  const next=structuredClone(recovered); next.documents[0].status='unverified';
  await store.save(github,ctx,{number:1,body:state.body},next,{expected:recovered});
  assert.deepEqual(await store.load(github,ctx,{number:1,body:state.body}),next);
});

test('a person editing the issue body during branch save is never overwritten', async () => {
  const data=ledger.build('2026-10',[path],null,null);
  const {state,github}=fixture('original');
  const create=github.rest.git.createCommit;
  github.rest.git.createCommit=async args=>{state.body='human update'; return create(args);};
  await store.save(github,ctx,{number:1,body:'original'},data);
  assert.equal(state.body,'human update');
  assert.deepEqual(await store.load(github,ctx,{number:1,body:state.body}),data);
});

test('a changed legacy source after interrupted migration is not silently discarded', async () => {
  const data=ledger.build('2026-10',[path],null,null);
  const body=ledger.render('notes',data);
  const {state,github}=fixture(body);
  state.failComment=true;
  await assert.rejects(store.save(github,ctx,{number:1,body},data,{expected:data}), /comment failed/);
  const edited=structuredClone(data); edited.documents[0].status='unverified';
  state.body=ledger.render('notes',edited);
  await assert.rejects(store.load(github,ctx,{number:1,body:state.body}), /legacy.*changed/);
  assert.equal((await store.stateAt(github,ctx,'2026-10',state.head)).documents[0].status,'unreviewed');
});
