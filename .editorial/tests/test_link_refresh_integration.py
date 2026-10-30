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
