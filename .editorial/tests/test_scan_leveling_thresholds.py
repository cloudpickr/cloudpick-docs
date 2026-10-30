"""The advisory scanner must expose configuration read failures."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'scripts' / 'scan-leveling-candidates.py'
spec = importlib.util.spec_from_file_location('scan_leveling_candidates', SCRIPT)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class ThresholdsTest(unittest.TestCase):
    def test_missing_configuration_warns_and_returns_documented_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / 'missing.yaml'
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(scanner.load_thresholds(missing), (80, 120))
            self.assertIn('cannot read leveling thresholds', stderr.getvalue())
            self.assertIn('using defaults 80/120', stderr.getvalue())

    def test_existing_configuration_uses_configured_thresholds(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'rules.yaml'
            config.write_text('sentence_chars_soft: 41\nsentence_chars_hard: 92\n', encoding='utf-8')
            self.assertEqual(scanner.load_thresholds(config), (41, 92))
