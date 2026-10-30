import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('scan_sources', ROOT / 'scripts/scan-source-changes.py')
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


class SourceWatchTests(unittest.TestCase):
    def test_inventory_excludes_protected_and_normalizes_fragments(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / 'src/content/docs/ko/a.md'; p.parent.mkdir(parents=True)
            p.write_text('---\nurl: https://secret.example/a\n---\n[x](https://example.org/a#x)\n`https://example.org/code`\n```\nhttps://example.org/fence\n```\n')
            self.assertEqual(source.inventory(root), {'https://example.org/a':['src/content/docs/ko/a.md']})

    def test_change_is_advisory_and_failures_preserve_previous_hash(self):
        url = 'https://example.org/a'; refs = {url:['src/content/docs/ko/a.md']}
        old = {url:{'hash':'a'*64,'hash_kind':'visible-v1','final_url':url,'checked_at':'2026-01-01','status':'observed'}}
        result = source.scan(refs,old,'2026-10-01',lambda _:SimpleNamespace(status=200,visible_sha256='b'*64,url=url))
        self.assertEqual(result['candidates'][0]['source_status'],'unverified')
        def broken(_): raise TimeoutError()
        failed = source.scan(refs,result['refs'],'2026-10-02',broken)
        self.assertEqual(failed['refs'][url]['hash'],'b'*64)
        self.assertEqual(failed['refs'][url]['status'],'unverified')
        self.assertEqual(failed['candidates'],[])

    def test_limit_and_oldest_first_cover_all_references(self):
        refs = {f'https://example.org/{i}':['src/content/docs/ko/a.md'] for i in range(8)}
        fetch = lambda u:SimpleNamespace(status=200,visible_sha256='a'*64,url=u)
        a = source.scan(refs,{},'2026-10-01',fetch,limit=3,workers=1)
        b = source.scan(refs,a['refs'],'2026-10-02',fetch,limit=3,workers=1)
        c = source.scan(refs,b['refs'],'2026-10-03',fetch,limit=3,workers=1)
        self.assertTrue(all(v.get('checked_at') for v in c['refs'].values()))
        self.assertEqual(c['total'],8)

    def test_http_error_is_unverified_not_a_current_document(self):
        u='https://example.org/a'
        r=source.scan({u:['src/content/docs/ko/a.md']},{},'2026-10-01',lambda _:SimpleNamespace(status=404),workers=1)
        self.assertEqual(r['failed'],1)
        self.assertEqual(r['refs'][u]['status'],'unverified')

    def test_legacy_raw_hash_is_rebaselined_without_false_change(self):
        u='https://example.org/a'; refs={u:['src/content/docs/ko/a.md']}
        old={u:{'hash':'a'*64,'final_url':u,'status':'observed'}}
        r=source.scan(refs,old,'2026-10-01',lambda _:SimpleNamespace(status=200,visible_sha256='b'*64,url=u))
        self.assertEqual(r['candidates'],[])
        self.assertEqual(r['refs'][u]['hash_kind'],'visible-v1')

    def test_unselected_legacy_hash_is_not_reported_as_observed(self):
        a,b='https://example.org/a','https://example.org/b'
        refs={a:['src/content/docs/ko/a.md'],b:['src/content/docs/ko/a.md']}
        old={b:{'hash':'a'*64,'checked_at':'2026-10-01','status':'observed'}}
        r=source.scan(refs,old,'2026-10-02',lambda u:SimpleNamespace(status=200,visible_sha256='b'*64,url=u),limit=1,workers=1)
        self.assertEqual(r['refs'][b]['status'],'unverified')
        self.assertEqual(r['refs'][b]['error'],'legacy-baseline-not-comparable')

    def test_unsupported_content_is_unverified(self):
        u='https://example.org/a'
        r=source.scan({u:['src/content/docs/ko/a.md']},{},'2026-10-01',lambda _:SimpleNamespace(status=200,visible_sha256=None,url=u))
        self.assertEqual(r['refs'][u]['status'],'unverified')


if __name__ == '__main__':
    unittest.main()
