import json
import sys
import tempfile
import unittest
from pathlib import Path

# unittest discover 默认把 tests/ 加入搜索路径。
# checker.py 在它的上一级目录，所以这里手动把工具目录加入 sys.path。
TOOL_DIR = Path(__file__).resolve().parents[1]
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from checker import validate_task_package


class CheckerTests(unittest.TestCase):
    """Task Package Checker 的基础回归测试。"""

    def create_package(self, root: Path) -> None:
        """在临时目录创建一个最小、合法的练习任务包。"""

        (root / "environment").mkdir()
        (root / "tests").mkdir()

        metadata = {
            "id": "t1",
            "title": "Test",
            "description": "Synthetic test",
            "difficulty": "medium",
            "timeout_seconds": 60,
        }
        (root / "task.json").write_text(
            json.dumps(metadata), encoding="utf-8"
        )
        (root / "instruction.md").write_text("# Test", encoding="utf-8")
        (root / "environment" / "Dockerfile").write_text(
            "FROM python:3.11-slim", encoding="utf-8"
        )
        (root / "tests" / "test_one.py").write_text(
            "def test_ok(): pass", encoding="utf-8"
        )

    def test_valid_package(self):
        # 合法结构应该没有 error；因为没写 tags，所以会有一个 warning。
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "pkg"
            package.mkdir()
            self.create_package(package)

            errors, warnings = validate_task_package(package)
            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 1)

    def test_missing_instruction_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "pkg"
            package.mkdir()
            self.create_package(package)
            (package / "instruction.md").unlink()

            errors, _ = validate_task_package(package)
            self.assertTrue(any("instruction.md" in error for error in errors))

    def test_invalid_difficulty_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "pkg"
            package.mkdir()
            self.create_package(package)

            metadata_path = package / "task.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["difficulty"] = "extreme"
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

            errors, _ = validate_task_package(package)
            self.assertTrue(any("difficulty" in error for error in errors))

    def test_boolean_timeout_fails(self):
        # True 在 Python 中属于 int 的子类，所以专门测试这个边界情况。
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "pkg"
            package.mkdir()
            self.create_package(package)

            metadata_path = package / "task.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["timeout_seconds"] = True
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

            errors, _ = validate_task_package(package)
            self.assertTrue(any("timeout_seconds" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
