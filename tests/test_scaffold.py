import json
from pathlib import Path
import tempfile
import unittest

from hermes_workflow.scaffold import build_scaffold_plan, write_scaffold


class ScaffoldTests(unittest.TestCase):
    def test_scaffold_plan_contains_hermes_instructions(self):
        plan = build_scaffold_plan("workspace")
        markdown = plan.hermes_markdown()

        self.assertIn("HERMES.md", markdown)
        self.assertIn("Do not delete or archive", markdown)
        self.assertIn("00-inbox", markdown)

    def test_manifest_is_valid_json(self):
        plan = build_scaffold_plan("workspace")
        payload = json.loads(plan.manifest_json())

        self.assertEqual(payload["preset"], "starter")
        self.assertIn("00-inbox", payload["directories"])

    def test_write_scaffold_creates_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            created = write_scaffold(build_scaffold_plan(root))

            self.assertTrue((root / "HERMES.md").exists())
            self.assertTrue((root / "hermes-primitives.json").exists())
            self.assertTrue((root / "00-inbox").is_dir())
            self.assertIn(root / "HERMES.md", created)

    def test_write_scaffold_does_not_overwrite_hermes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            root.mkdir()
            (root / "HERMES.md").write_text("existing", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                write_scaffold(build_scaffold_plan(root))
