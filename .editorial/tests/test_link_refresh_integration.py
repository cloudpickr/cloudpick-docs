"""A packet can be committed and verified against its actual head commit."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'scripts/link-refresh-manifest.py'
GUARD = ROOT / 'scripts/link-refresh-guard.py'


class TestCommittedRefresh(unittest.TestCase):
    def test_committed_packet_and_changed_document(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            env = {**os.environ, 'GIT_AUTHOR_NAME': 'Test', 'GIT_AUTHOR_EMAIL': 'test@example.com',
                   'GIT_COMMITTER_NAME': 'Test', 'GIT_COMMITTER_EMAIL': 'test@example.com'}
            def cmd(*args):
                return subprocess.check_output(args, cwd=root, env=env, text=True).strip()
            cmd('git', 'init', '-q')
            doc = root / 'src/content/docs/ko/test.md'
            doc.parent.mkdir(parents=True)
            doc.write_text('[source](https://old.example/doc)\n')
            cmd('git', 'add', '.')
            cmd('git', 'commit', '-qm', 'base')
            base = cmd('git', 'rev-parse', 'HEAD')
            mapping = {'https://old.example/doc': 'https://new.example/doc'}
            paths = root / 'paths.txt'
            paths.write_text('src/content/docs/ko/test.md\n')
            map_file = root / 'map.json'
            map_file.write_text(json.dumps(mapping))
            digest = cmd('python3', str(MANIFEST), 'compute', '--changed-paths', str(paths), '--url-map', str(map_file), '--base-sha', base)
            packet = root / '.editorial/packets/CLPKDOC-1.json'
            packet.parent.mkdir(parents=True)
            packet.write_text(json.dumps({'link_refresh': {'url_map': mapping, 'manifest_sha256': digest, 'changed_paths_count': 1}}))
            doc.write_text('[source](https://new.example/doc)\n')
            cmd('git', 'add', 'src', '.editorial')
            cmd('git', 'commit', '-qm', 'refresh')
            head = cmd('git', 'rev-parse', 'HEAD')
            self.assertNotEqual(base, head)
            cmd('python3', str(MANIFEST), 'verify', '--packet', str(packet), '--changed-paths', str(paths), '--base-sha', base)
            before = root / 'before.md'
            before.write_text(cmd('git', 'show', f'{base}:src/content/docs/ko/test.md') + '\n')
            cmd('python3', str(GUARD), '--base', str(before), '--head', str(doc), '--mapping', str(map_file))
            paths.write_text('src/content/docs/ko/test.md\nsrc/content/docs/en/extra.md\n')
            self.assertNotEqual(subprocess.run(['python3', str(MANIFEST), 'verify', '--packet', str(packet), '--changed-paths', str(paths), '--base-sha', base], cwd=root, capture_output=True).returncode, 0)


class TestFullGateIntegration(unittest.TestCase):
    """Real commits and packet; HTTP, reviewer and human identity are simulated."""

    def test_full_gate_and_c_approval_fail_closed(self):
        import hashlib
        import sys
        from types import SimpleNamespace
        from unittest.mock import patch
        sys.path.insert(0, str(ROOT / '.editorial'))
        import run_review_gate as gate
        import review_runner as reviewer
        import source_fetch

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            env = {**os.environ, 'GIT_AUTHOR_NAME': 'Test', 'GIT_AUTHOR_EMAIL': 'test@example.com',
                   'GIT_COMMITTER_NAME': 'Test', 'GIT_COMMITTER_EMAIL': 'test@example.com'}
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=root, env=env).decode()
            git('init', '-q')
            paths = [f'src/content/docs/{locale}/topic.md' for locale in ('ko', 'en', 'ja')]
            for path in paths:
                f = root / path
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text('[source](https://old.example/doc)\n\n```python\nurl = "https://old.example/doc"\n```\n')
            git('add', '.')
            git('commit', '-qm', 'base')
            base = git('rev-parse', 'HEAD').strip()
            mapping = {'https://old.example/doc': 'https://new.example/doc'}
            paths_file = root / 'paths.txt'
            paths_file.write_text('\n'.join(paths) + '\n')
            mapping_file = root / 'mapping.json'
            mapping_file.write_text(json.dumps(mapping))
            digest = subprocess.check_output(['python3', str(MANIFEST), 'compute', '--changed-paths', str(paths_file),
                                              '--url-map', str(mapping_file), '--base-sha', base], text=True).strip()
            packet_path = root / '.editorial/packets/CLPKDOC-1.json'
            packet_path.parent.mkdir(parents=True)
            packet = {'schema_version': 1, 'jira_key': 'CLPKDOC-1', 'policy_action': 'link-refresh',
                      'tier_hint': 'C', 'target_path': paths[0], 'changed_paths': paths,
                      'claim_ledger': [], 'generated_by_llm': True,
                      'writer': {'model': 'writer', 'provider': 'a'},
                      'link_refresh': {'url_map': mapping, 'manifest_sha256': digest, 'changed_paths_count': len(paths)}}
            packet_path.write_text(json.dumps(packet) + '\n')
            for path in paths:
                f = root / path
                f.write_text(f.read_text().replace('[source](https://old.example/doc)', '[source](https://new.example/doc)'))
            git('add', 'src', '.editorial')
            git('commit', '-qm', 'url refresh')
            head = git('rev-parse', 'HEAD').strip()
            def inputs(rev):
                outputs = {}
                for label, options in [('numstat', ['--numstat']), ('name_status', ['--name-status']),
                                       ('diff', []), ('link_refresh_diff', ['--', 'src/content/docs/'])]:
                    file = root / (label + '.txt')
                    args = ['diff', *options, base, rev] if label != 'link_refresh_diff' else ['diff', base, rev, *options]
                    file.write_text(git(*args))
                    outputs[label] = str(file)
                return SimpleNamespace(**outputs, packet=str(packet_path),
                    packet_repo_path='.editorial/packets/CLPKDOC-1.json', repo='example/test', pr='1',
                    base_sha=base, head_sha=rev, now=None, expires=None, link_refresh_repo=str(root))
            args = inputs(head)
            review_result = reviewer.ReviewResult('approve', ['ok'], 1, True)
            with patch.object(reviewer, 'run_review', return_value=review_result), \
                 patch.object(source_fetch, 'fetch_source', return_value=SimpleNamespace(url=mapping['https://old.example/doc'], status=200)):
                out = gate.run(args)
                self.assertEqual((out['tier'], out['state']), ('C', 'success'), out)
                self.assertIn('link-refresh full-file verification: ok', out['reasons'])
                original_envelope = out['envelope_key']
                with patch.object(reviewer, 'run_review', return_value=reviewer.ReviewResult('error', ['unavailable'], 0, False)):
                    self.assertEqual(gate.run(args)['state'], 'pending')
                # Tampering with the committed manifest is blocked even if other inputs are valid.
                original_packet = packet_path.read_text()
                invalid_packet = json.loads(original_packet)
                invalid_packet['link_refresh']['manifest_sha256'] = '0' * 64
                packet_path.write_text(json.dumps(invalid_packet) + '\n')
                self.assertEqual(gate.run(args)['state'], 'failure')
                packet_path.write_text(original_packet)
                hash_value = hashlib.sha256(packet_path.read_bytes()).hexdigest()
                js = "const g=require(process.argv[1]); let h=process.argv[2]; console.log(JSON.stringify([g.evaluateApproval({tier:'C',packetSha256:h,allowlist:['alice'],confirmations:[]}),g.evaluateApproval({tier:'C',packetSha256:h,allowlist:['alice'],confirmations:[{user:'alice',body:'/approve '+h,isBot:false}]})]));"
                states = json.loads(subprocess.check_output(['node', '-e', js, str(ROOT / '.github/scripts/c_approval_gate.cjs'), hash_value], text=True))
                self.assertEqual([x['state'] for x in states], ['pending', 'success'])
                # A changed head must rebind the review even if the packet stays the same.
                (root / 'unrelated.txt').write_text('new')
                git('add', 'unrelated.txt'); git('commit', '-qm', 'unrelated')
                next_head = git('rev-parse', 'HEAD').strip()
                self.assertNotEqual(original_envelope, gate.run(inputs(next_head))['envelope_key'])
                # A URL change inside a fenced block is indistinguishable to diff-only reconstruction,
                # but the trusted full-file guard must reject it.
                target = root / paths[0]
                target.write_text(target.read_text().replace('url = "https://old.example/doc"', 'url = "https://new.example/doc"'))
                git('add', paths[0]); git('commit', '-qm', 'tamper protected block')
                tampered = gate.run(inputs(git('rev-parse', 'HEAD').strip()))
                self.assertEqual(tampered['state'], 'failure', tampered)
                self.assertTrue(any('full-file verification failed' in x for x in tampered['reasons']))
                args.link_refresh_repo = str(root / 'missing')
                self.assertEqual(gate.run(args)['state'], 'pending')
