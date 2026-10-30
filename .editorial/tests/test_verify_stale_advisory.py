import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('verify_stale_advisory', ROOT / 'scripts/verify-stale-candidates.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AdvisoryTests(unittest.TestCase):
    def test_llm_quote_cannot_promote_ambiguous_to_contradiction_or_support(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'candidates.json'
            path.write_text(json.dumps({'high': [], 'medium': [{'path':'doc.md','line':1,'excerpt':'Preview'}]}))
            for verdict in ('contradicts', 'supports'):
                out = io.StringIO()
                with patch.object(module, 'read_doc', return_value='doc'), \
                     patch.object(module, 'section_links_for', return_value=['https://example.org']), \
                     patch.object(module, 'classify', return_value=('ambiguous', {'url':'https://example.org'})), \
                     patch.object(module.vc, 'llm_adjudicate', return_value={'verdict':verdict,'quote_ok':True}), \
                     patch.dict('sys.modules', {'source_fetch':SimpleNamespace(fetch_source=lambda _:SimpleNamespace(text_sample='body'))}), \
                     contextlib.redirect_stdout(out):
                    self.assertEqual(module.main(['--candidates',str(path),'--fetch','--with-llm','--json']),0)
                result=json.loads(out.getvalue())
                self.assertEqual(result['summary']['ambiguous'],1)
                self.assertEqual(result['summary']['contradicted'],0)
                self.assertEqual(result['supports_count'],0)


if __name__ == '__main__':
    unittest.main()
