import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[2] / 'scripts/prepare-link-refresh.py'
spec = importlib.util.spec_from_file_location('prepare_link_refresh', SCRIPT)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
OLD = 'https://cloud.google.com/run/docs'
NEW = 'https://docs.cloud.google.com/run/docs'
BASE = 'a' * 40


class TestPreparation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.editorial/packets').mkdir(parents=True)
        for locale in ('ko', 'en', 'ja'):
            path = self.root / f'src/content/docs/{locale}/compute/containers.md'
            path.parent.mkdir(parents=True)
            path.write_bytes(f'---\r\ntitle: Test\r\n---\r\n[Docs]({OLD})\r\n`{OLD}`\r\n```\r\n{OLD}\r\n```\r\n'.encode())

    def fetch(self, url):
        return SimpleNamespace(status=200, url=NEW)

    def test_real_manifest_schema_guards_and_crlf(self):
        report = tool.scan(self.root, 'compute/containers.md', self.fetch)
        self.assertEqual(report['checked_urls'], 1)
        tool.write_candidate(self.root, report, BASE, 'LINKREFRESH-1')
        packet = json.loads((self.root / '.editorial/packets/LINKREFRESH-1.json').read_text())
        self.assertEqual(packet['tier_hint'], 'C')
        self.assertEqual(packet['claim_ledger'], [])
        self.assertEqual(len(packet['changed_paths']), 3)
        self.assertEqual(packet['link_refresh']['manifest_sha256'],
                         tool.MANIFEST.compute_manifest(packet['changed_paths'], {OLD: NEW}, BASE))
        for name in packet['changed_paths']:
            raw = (self.root / name).read_bytes()
            self.assertIn(f'[Docs]({NEW})\r\n'.encode(), raw)
            self.assertIn(f'`{OLD}`'.encode(), raw)
            self.assertIn(f'```\r\n{OLD}\r\n```'.encode(), raw)
            self.assertNotIn(b'\n', raw.replace(b'\r\n', b''))

    def test_missing_locale_never_partially_writes(self):
        (self.root / 'src/content/docs/ja/compute/containers.md').unlink()
        report = tool.scan(self.root, 'compute/containers.md', self.fetch)
        self.assertIsNone(report['candidate'])
        self.assertEqual(report['findings'][0]['status'], 'hold')
        self.assertIn(OLD.encode(), (self.root / 'src/content/docs/ko/compute/containers.md').read_bytes())
        self.assertEqual(list((self.root / '.editorial/packets').iterdir()), [])

    def test_partial_prefix_replacement_is_rejected(self):
        path = self.root / 'src/content/docs/en/compute/containers.md'
        path.write_text(path.read_text() + f'\n[Other]({OLD}/different-page)\n')
        report = tool.scan(self.root, 'compute/containers.md', self.fetch)
        self.assertIsNone(report['candidate'])

    def test_fetch_failure_and_http_failure_stay_unverified(self):
        def broken(_):
            raise TimeoutError('fetch unavailable')
        for fetch in (broken, lambda _: SimpleNamespace(status=404, url=OLD)):
            report = tool.scan(self.root, 'compute/containers.md', fetch)
            self.assertIsNone(report['candidate'])
            self.assertEqual(report['findings'][0]['status'], 'unverified')

    def test_selector_path_locale_and_host_changes_are_held(self):
        for new in (NEW + '?view=v2', NEW + '/v2', NEW.replace('/run/', '/en-us/run/'),
                    'https://docs.cloud.google.com/', 'https://evil.example/run/docs'):
            report = tool.scan(self.root, 'compute/containers.md', lambda _, new=new: SimpleNamespace(status=200, url=new))
            self.assertIsNone(report['candidate'], new)
            self.assertEqual(report['findings'][0]['status'], 'unverified')

    def test_regulatory_and_traversal_targets_are_rejected(self):
        for target in ('korea/guide.md', '../en/compute/containers.md', '/tmp/file.md'):
            with self.assertRaises(ValueError):
                tool.scan(self.root, target, self.fetch)

    def test_url_budget_is_bounded(self):
        path = self.root / 'src/content/docs/ko/compute/containers.md'
        path.write_text(''.join(f'[D](https://cloud.google.com/p{i}/docs)\n' for i in range(30)))
        calls = []
        def fetch(url):
            calls.append(url)
            return SimpleNamespace(status=200, url=url)
        report = tool.scan(self.root, 'compute/containers.md', fetch)
        self.assertEqual(len(calls), tool.MAX_URLS)
        self.assertTrue(report['budget_exhausted'])

    def test_deadline_stops_requests(self):
        values = iter([0, tool.MAX_SECONDS + 1])
        with patch.object(tool, 'MAX_URLS', 1):
            report = tool.scan(self.root, 'compute/containers.md', self.fetch, now=lambda: next(values))
        self.assertEqual(report['checked_urls'], 0)
        self.assertTrue(report['budget_exhausted'])

    def test_packet_collision_does_not_write_documents(self):
        report = tool.scan(self.root, 'compute/containers.md', self.fetch)
        (self.root / '.editorial/packets/LINKREFRESH-1.json').write_text('{}')
        with self.assertRaises(ValueError):
            tool.write_candidate(self.root, report, BASE, 'LINKREFRESH-1')
        self.assertIn(OLD.encode(), (self.root / 'src/content/docs/ko/compute/containers.md').read_bytes())

    def test_symlinked_locale_is_held(self):
        path = self.root / 'src/content/docs/ja/compute/containers.md'
        path.unlink()
        path.symlink_to(self.root / 'src/content/docs/ko/compute/containers.md')
        report = tool.scan(self.root, 'compute/containers.md', self.fetch)
        self.assertIsNone(report['candidate'])
        self.assertEqual(report['findings'][0]['status'], 'hold')

    def test_closed_candidate_is_not_reopened_or_pushed(self):
        report = tool.scan(self.root, 'compute/containers.md', self.fetch)
        report['base_sha'] = BASE
        with patch.object(tool, 'gh', return_value='[{"url":"https://example/pr/1","state":"CLOSED"}]'), \
             patch.object(tool, 'write_candidate') as write, patch.object(tool, 'git') as git:
            tool.publish(report, 'owner/repo')
        write.assert_not_called()
        git.assert_not_called()
        self.assertIn('already proposed', report['skipped'])

    def test_dismissed_candidate_does_not_starve_later_document(self):
        first = self.root / 'src/content/docs/ko/compute/containers.md'
        for locale in ('ko', 'en', 'ja'):
            original = self.root / f'src/content/docs/{locale}/compute/containers.md'
            original.with_name('second.md').write_bytes(original.read_bytes())
        previous = lambda candidate: 'https://example/pr/old' if candidate['path'] == 'compute/containers.md' else None
        with patch.object(tool, 'candidate_paths', return_value=[first, first.with_name('second.md')]):
            report = tool.scan(self.root, fetch=self.fetch, previous_pr=previous)
        self.assertEqual(report['candidate']['path'], 'compute/second.md')
        self.assertEqual(report['findings'][0]['previous_pr'], 'https://example/pr/old')
        self.assertEqual(report['checked_urls'], 1)  # Cache and batch budget survive the skip.

    def test_all_dismissed_candidates_produce_hold_without_changes(self):
        report = tool.scan(self.root, 'compute/containers.md', self.fetch,
                           previous_pr=lambda _: 'https://example/pr/old')
        self.assertIsNone(report['candidate'])
        self.assertEqual(report['findings'][0]['status'], 'hold')
        self.assertEqual(list((self.root / '.editorial/packets').iterdir()), [])

    def test_active_pilot_prevents_another_draft(self):
        with patch.object(tool, 'gh', return_value='[{"headRefName":"docs/link-refresh-pilot-271","url":"https://example/pr/272"}]'):
            self.assertEqual(tool.has_active_pr('owner/repo'), 'https://example/pr/272')

    def test_publish_is_one_draft_and_never_approves_or_merges(self):
        report = tool.scan(self.root, 'compute/containers.md', self.fetch)
        report['base_sha'] = BASE
        with patch.object(tool, 'ROOT', self.root), \
             patch.object(tool, 'gh', side_effect=['[]', 'https://example/pr/1', '']) as gh, \
             patch.object(tool, 'git') as git:
            tool.publish(report, 'owner/repo')
        args = gh.call_args_list[1].args
        self.assertEqual(args[:2], ('pr', 'create'))
        self.assertIn('--draft', args)
        self.assertEqual(report['pr_url'], 'https://example/pr/1')
        self.assertFalse(any('merge' in call.args or '--force' in call.args for call in git.call_args_list))
        self.assertFalse(any('approve' in call.args for call in gh.call_args_list))


if __name__ == '__main__':
    unittest.main()
