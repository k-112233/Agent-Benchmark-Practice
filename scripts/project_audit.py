#!/usr/bin/env python3
"""对仓库做一次发布前的自动检查。

这个脚本只检查“能自动判断”的项目，例如文件是否存在、测试是否通过。
它不能替代人工内容审查。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# scripts/ 的上一级目录就是仓库根目录。
ROOT = Path(__file__).resolve().parents[1]

EXPECTED_DIRS = [
    "01-benchmark-fundamentals",
    "02-task-design",
    "03-prompt-engineering",
    "04-environment-and-execution",
    "05-testing-and-evaluation",
    "06-quality-assurance",
    "tools/task-package-checker",
    "tools/evaluation-summary",
    "references",
]

EXPECTED_FILES = [
    "README.md",
    "01-benchmark-fundamentals/benchmark-overview.md",
    "01-benchmark-fundamentals/agent-evaluation.md",
    "01-benchmark-fundamentals/evaluation-metrics.md",
    "02-task-design/task-abstraction.md",
    "02-task-design/task-specification.md",
    "02-task-design/difficulty-design.md",
    "03-prompt-engineering/prompt-design-principles.md",
    "03-prompt-engineering/constraint-design.md",
    "03-prompt-engineering/iterative-refinement.md",
    "04-environment-and-execution/docker-basics.md",
    "04-environment-and-execution/reproducible-environment.md",
    "05-testing-and-evaluation/test-design.md",
    "05-testing-and-evaluation/verifier-design.md",
    "05-testing-and-evaluation/model-evaluation.md",
    "05-testing-and-evaluation/failure-analysis.md",
    "06-quality-assurance/task-validation.md",
    "06-quality-assurance/delivery-checklist.md",
    "tools/task-package-checker/checker.py",
    "tools/task-package-checker/README.md",
    "tools/evaluation-summary/summary.py",
    "tools/evaluation-summary/README.md",
    "references/open-source-projects.md",
]

# 这些文件类型不一定有问题，但公开前通常值得人工确认来源和内容。
REVIEW_EXTENSIONS = {
    ".zip",
    ".7z",
    ".rar",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".sav",
    ".ppt",
    ".pptx",
    ".log",
    ".har",
    ".pcap",
    ".sqlite",
    ".db",
}

# 这里只匹配“文件名”，不会扫描普通文档正文。
REVIEW_NAME_KEYWORDS = {
    "private",
    "confidential",
    "secret",
    "credential",
    "token",
    "worklog",
    "acceptance",
    "机密",
    "凭据",
    "日志",
}


def run(command: list[str]) -> tuple[bool, str]:
    """在仓库根目录运行命令，返回 (是否成功, 合并后的输出)。"""

    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def main() -> int:
    print("=== Agent-Benchmark-Practice Final Audit ===\n")

    failures: list[str] = []
    warnings: list[str] = []

    # 1. 目录和主要文件完整性。
    print("[1/4] Structure")
    for relative_path in EXPECTED_DIRS:
        if not (ROOT / relative_path).is_dir():
            failures.append(f"Missing directory: {relative_path}")

    for relative_path in EXPECTED_FILES:
        if not (ROOT / relative_path).is_file():
            failures.append(f"Missing file: {relative_path}")

    if failures:
        for item in failures:
            print("  FAIL:", item)
    else:
        print("  PASS: expected project structure is present.")

    # 2. 分别运行两个工具自己的单元测试。
    print("\n[2/4] Tool tests")
    tests = [
        (
            "Task Package Checker",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tools/task-package-checker/tests",
                "-v",
            ],
        ),
        (
            "Evaluation Summary",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tools/evaluation-summary/tests",
                "-v",
            ],
        ),
    ]

    for name, command in tests:
        ok, output = run(command)
        print(f"\n--- {name} ---")
        print(output)
        if not ok:
            failures.append(f"{name} unit tests failed")

    # 3. 再按 README 中的方式运行两个示例，防止“测试能过但命令跑不通”。
    print("\n[3/4] Sample runs")
    samples = [
        (
            "Task Package Checker sample",
            [
                sys.executable,
                "tools/task-package-checker/checker.py",
                "tools/task-package-checker/sample-task",
            ],
        ),
        (
            "Evaluation Summary sample",
            [
                sys.executable,
                "tools/evaluation-summary/summary.py",
                "tools/evaluation-summary/sample-data/sample-results.csv",
            ],
        ),
    ]

    for name, command in samples:
        ok, output = run(command)
        print(f"\n--- {name} ---")
        print(output)
        if not ok:
            failures.append(f"{name} failed")

    # 4. 找“值得人工看一眼”的文件，不自动删除任何东西。
    print("\n[4/4] Public-repository review")
    review_files: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(ROOT)
        lower_name = str(relative_path).lower()

        if path.suffix.lower() in REVIEW_EXTENSIONS:
            review_files.append(str(relative_path))
            continue

        if any(keyword.lower() in lower_name for keyword in REVIEW_NAME_KEYWORDS):
            review_files.append(str(relative_path))

    if review_files:
        warnings.append(
            "Some files require manual review before publishing. "
            "Their presence is not automatically an error."
        )
        print("  REVIEW:")
        for item in sorted(set(review_files)):
            print("   -", item)
    else:
        print("  PASS: no obvious review-target files found.")

    print("\n=== RESULT ===")

    for item in warnings:
        print("WARNING:", item)

    if failures:
        for item in failures:
            print("FAIL:", item)
        print("\nFINAL STATUS: NOT READY")
        return 1

    print("FINAL STATUS: STRUCTURE AND AUTOMATED CHECKS PASSED")
    print("Manual content review is still recommended before publication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
