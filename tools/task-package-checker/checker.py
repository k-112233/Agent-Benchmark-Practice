#!/usr/bin/env python3
"""检查本仓库自定义练习任务包的基础结构。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# task.json 中必须出现的字段，以及每个字段应该是什么 Python 类型。
REQUIRED_FIELDS = {
    "id": str,
    "title": str,
    "description": str,
    "difficulty": str,
    "timeout_seconds": int,
}

# 这是本练习自己定义的三个难度值，不是外部 Benchmark 的官方枚举。
VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def validate_task_package(package_dir: Path) -> tuple[list[str], list[str]]:
    """检查一个任务目录，返回 (errors, warnings)。

    errors 代表任务包不满足当前练习格式；
    warnings 代表可以继续使用，但有值得提醒的地方。
    """

    errors: list[str] = []
    warnings: list[str] = []

    # 第一步：先确认用户传入的路径确实是一个目录。
    if not package_dir.exists():
        return [f"Package directory does not exist: {package_dir}"], warnings
    if not package_dir.is_dir():
        return [f"Package path is not a directory: {package_dir}"], warnings

    metadata_path = package_dir / "task.json"
    instruction_path = package_dir / "instruction.md"
    dockerfile_path = package_dir / "environment" / "Dockerfile"
    tests_dir = package_dir / "tests"

    # 第二步：读取 task.json。
    metadata = None
    if not metadata_path.is_file():
        errors.append("Missing required file: task.json")
    else:
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"task.json is not valid JSON: {exc}")
        except OSError as exc:
            errors.append(f"Could not read task.json: {exc}")

    # 第三步：检查元数据字段和类型。
    if metadata is not None:
        if not isinstance(metadata, dict):
            errors.append("task.json must contain a JSON object.")
        else:
            for field, expected_type in REQUIRED_FIELDS.items():
                if field not in metadata:
                    errors.append(f"task.json is missing required field: {field}")
                    continue

                value = metadata[field]

                # Python 里 bool 是 int 的子类，所以这里要单独排除 True / False。
                if expected_type is int:
                    valid_type = isinstance(value, int) and not isinstance(value, bool)
                else:
                    valid_type = isinstance(value, expected_type)

                if not valid_type:
                    errors.append(
                        f"task.json field '{field}' must be "
                        f"{expected_type.__name__}."
                    )
                elif expected_type is str and not value.strip():
                    errors.append(f"task.json field '{field}' must not be empty.")

            difficulty = metadata.get("difficulty")
            if isinstance(difficulty, str) and difficulty not in VALID_DIFFICULTIES:
                errors.append(
                    "task.json field 'difficulty' must be one of: "
                    "easy, medium, hard."
                )

            timeout = metadata.get("timeout_seconds")
            if (
                isinstance(timeout, int)
                and not isinstance(timeout, bool)
                and timeout <= 0
            ):
                errors.append(
                    "task.json field 'timeout_seconds' must be greater than 0."
                )

            if "tags" not in metadata:
                warnings.append("Optional field 'tags' is not present in task.json.")

    # 第四步：检查说明文件和环境文件。
    if not instruction_path.is_file():
        errors.append("Missing required file: instruction.md")
    else:
        try:
            if not instruction_path.read_text(encoding="utf-8").strip():
                errors.append("instruction.md must not be empty.")
        except OSError as exc:
            errors.append(f"Could not read instruction.md: {exc}")

    if not dockerfile_path.is_file():
        errors.append("Missing required file: environment/Dockerfile")

    # 第五步：tests/ 至少要有一个 Python 测试文件。
    if not tests_dir.is_dir():
        errors.append("Missing required directory: tests/")
    elif not any(
        path.is_file() and path.suffix == ".py" for path in tests_dir.iterdir()
    ):
        errors.append("tests/ must contain at least one Python test file.")

    return errors, warnings


def main() -> int:
    """命令行入口。"""

    parser = argparse.ArgumentParser(
        description="Check a generic practice-task package."
    )
    parser.add_argument("package_dir", type=Path)
    args = parser.parse_args()

    errors, warnings = validate_task_package(args.package_dir)

    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"FAIL: {item}")

    if errors:
        print(
            f"\nRESULT: FAIL "
            f"({len(errors)} error(s), {len(warnings)} warning(s))"
        )
        return 1

    print("PASS: package structure and required metadata are valid.")
    print("RESULT: " + ("PASS WITH WARNINGS" if warnings else "PASS"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
