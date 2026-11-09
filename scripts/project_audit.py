#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

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

REVIEW_EXTENSIONS = {
    ".zip", ".7z", ".rar", ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".sav", ".ppt", ".pptx", ".log", ".har", ".pcap", ".sqlite", ".db"
}

REVIEW_NAME_KEYWORDS = {
    "internal", "private", "confidential", "client", "customer",
    "appen", "worklog", "acceptance", "验收", "日志", "客户", "内部",
}


def run(command: list[str]) -> tuple[bool, str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    text = (result.stdout + result.stderr).strip()
    return result.returncode == 0, text


def main() -> int:
    print("=== Agent-Benchmark-Practice Final Audit ===\n")

    failures = []
    warnings = []

    print("[1/4] Structure")
    for rel in EXPECTED_DIRS:
        if not (ROOT / rel).is_dir():
            failures.append(f"Missing directory: {rel}")
    for rel in EXPECTED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f"Missing file: {rel}")

    if failures:
        for item in failures:
            print("  FAIL:", item)
    else:
        print("  PASS: expected project structure is present.")

    print("\n[2/4] Tool tests")
    tests = [
        (
            "Task Package Checker",
            [sys.executable, "-m", "unittest", "discover",
             "-s", "tools/task-package-checker/tests", "-v"],
        ),
        (
            "Evaluation Summary",
            [sys.executable, "-m", "unittest", "discover",
             "-s", "tools/evaluation-summary/tests", "-v"],
        ),
    ]
    for name, command in tests:
        ok, output = run(command)
        print(f"\n--- {name} ---")
        print(output)
        if not ok:
            failures.append(f"{name} unit tests failed")

    print("\n[3/4] Sample runs")
    samples = [
        (
            "Task Package Checker sample",
            [sys.executable,
             "tools/task-package-checker/checker.py",
             "tools/task-package-checker/sample-task"],
        ),
        (
            "Evaluation Summary sample",
            [sys.executable,
             "tools/evaluation-summary/summary.py",
             "tools/evaluation-summary/sample-data/sample-results.csv"],
        ),
    ]
    for name, command in samples:
        ok, output = run(command)
        print(f"\n--- {name} ---")
        print(output)
        if not ok:
            failures.append(f"{name} failed")

    print("\n[4/4] Public-repository review")
    review_files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        lower_name = str(rel).lower()
        if path.suffix.lower() in REVIEW_EXTENSIONS:
            review_files.append(str(rel))
            continue
        if any(keyword.lower() in lower_name for keyword in REVIEW_NAME_KEYWORDS):
            review_files.append(str(rel))

    if review_files:
        warnings.append(
            "Files below require manual review before publishing; "
            "their presence is not automatically an error."
        )
        print("  REVIEW:")
        for item in sorted(set(review_files)):
            print("   -", item)
    else:
        print("  PASS: no obvious binary/archive/internal-named files found.")

    print("\n=== RESULT ===")
    if warnings:
        for item in warnings:
            print("WARNING:", item)

    if failures:
        for item in failures:
            print("FAIL:", item)
        print("\nFINAL STATUS: NOT READY")
        return 1

    print("FINAL STATUS: STRUCTURE AND AUTOMATED CHECKS PASSED")
    print("Manual public-content review is still required before GitHub publication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
