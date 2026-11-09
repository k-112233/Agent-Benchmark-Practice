import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from checker import validate_task_package

class CheckerTests(unittest.TestCase):
    def create_package(self, root):
        (root / "environment").mkdir()
        (root / "tests").mkdir()
        (root / "task.json").write_text(json.dumps({
            "id": "t1", "title": "Test", "description": "Synthetic test",
            "difficulty": "medium", "timeout_seconds": 60
        }), encoding="utf-8")
        (root / "instruction.md").write_text("# Test", encoding="utf-8")
        (root / "environment" / "Dockerfile").write_text("FROM python:3.11-slim", encoding="utf-8")
        (root / "tests" / "test_one.py").write_text("def test_ok(): pass", encoding="utf-8")

    def test_valid_package(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "pkg"; p.mkdir(); self.create_package(p)
            errors, warnings = validate_task_package(p)
            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 1)

    def test_missing_instruction_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "pkg"; p.mkdir(); self.create_package(p)
            (p / "instruction.md").unlink()
            errors, _ = validate_task_package(p)
            self.assertTrue(any("instruction.md" in e for e in errors))

    def test_invalid_difficulty_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "pkg"; p.mkdir(); self.create_package(p)
            data = json.loads((p / "task.json").read_text())
            data["difficulty"] = "extreme"
            (p / "task.json").write_text(json.dumps(data))
            errors, _ = validate_task_package(p)
            self.assertTrue(any("difficulty" in e for e in errors))

    def test_boolean_timeout_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "pkg"; p.mkdir(); self.create_package(p)
            data = json.loads((p / "task.json").read_text())
            data["timeout_seconds"] = True
            (p / "task.json").write_text(json.dumps(data))
            errors, _ = validate_task_package(p)
            self.assertTrue(any("timeout_seconds" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
