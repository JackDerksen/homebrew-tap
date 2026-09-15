import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from update_formula import stable_version, update_formula

FORMULA = (Path(__file__).resolve().parents[2] / "Formula/redox.rb").read_text()


class FormulaUpdateTest(unittest.TestCase):
    def test_updates_only_to_a_newer_stable_release_and_hashes_the_archive(self):
        current = FORMULA.split('/refs/tags/')[1].split('.tar.gz')[0]
        for tag, changes in [(current, False), ("v0.0.1", False), ("v999.0.0", True)]:
            with self.subTest(tag=tag), tempfile.TemporaryDirectory() as directory:
                original_directory = Path.cwd()
                try:
                    os.chdir(directory)
                    Path("Formula").mkdir()
                    Path("Formula/redox.rb").write_text(FORMULA)
                    release = dict(tag_name=tag, draft=False, prerelease=False)
                    responses = [io.BytesIO(json.dumps(release).encode()), io.BytesIO(b"archive")]
                    with patch("urllib.request.urlopen", side_effect=responses) as fetch:
                        update_formula()
                    result = Path("Formula/redox.rb").read_text()
                    self.assertEqual(result != FORMULA, changes)
                    self.assertEqual(fetch.call_count, 2 if changes else 1)
                    if changes:
                        self.assertIn(f"/refs/tags/{tag}.tar.gz", result)
                        self.assertIn(hashlib.sha256(b"archive").hexdigest(), result)
                        self.assertIsInstance(fetch.call_args.args[0], str)
                finally:
                    os.chdir(original_directory)
        for tag in ["v1.0.0-beta.1", "v01.0.0", "v1.0.0;echo bad", "v1.0"]:
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                stable_version(tag)
