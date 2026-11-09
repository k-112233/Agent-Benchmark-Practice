#!/usr/bin/env python3
"""读取合成 Trial CSV，并输出基础评测汇总。"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from collections import Counter
from pathlib import Path

# 输入 CSV 必须包含这些列。
REQUIRED_COLUMNS = {
    "task_id",
    "agent",
    "trial",
    "status",
    "runtime_seconds",
    "failure_type",
}

# 为了让练习保持简单，这里只接受四种状态。
VALID_STATUSES = {"passed", "failed", "error", "timeout"}


def load_results(csv_path: Path) -> list[dict[str, object]]:
    """读取 CSV，并在汇总前完成基础数据校验。"""

    csv_path = Path(csv_path)
    if not csv_path.is_file():
        raise ValueError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)

        # 先检查表头，避免后面读取某列时才发现缺失。
        fields = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fields
        if missing:
            raise ValueError(
                "Missing required columns: " + ", ".join(sorted(missing))
            )

        rows: list[dict[str, object]] = []

        for line_no, raw in enumerate(reader, start=2):
            status = (raw.get("status") or "").strip().lower()
            if status not in VALID_STATUSES:
                raise ValueError(f"Line {line_no}: unknown status '{status}'.")

            # runtime 在 CSV 中是字符串，转成 float 后才能计算均值和中位数。
            try:
                runtime = float((raw.get("runtime_seconds") or "").strip())
            except ValueError as exc:
                raise ValueError(
                    f"Line {line_no}: runtime_seconds must be numeric."
                ) from exc
            if runtime < 0:
                raise ValueError(
                    f"Line {line_no}: runtime_seconds cannot be negative."
                )

            # trial 用正整数编号。
            try:
                trial = int((raw.get("trial") or "").strip())
            except ValueError as exc:
                raise ValueError(
                    f"Line {line_no}: trial must be an integer."
                ) from exc
            if trial <= 0:
                raise ValueError(
                    f"Line {line_no}: trial must be greater than zero."
                )

            task_id = (raw.get("task_id") or "").strip()
            agent = (raw.get("agent") or "").strip()
            if not task_id:
                raise ValueError(f"Line {line_no}: task_id cannot be empty.")
            if not agent:
                raise ValueError(f"Line {line_no}: agent cannot be empty.")

            rows.append(
                {
                    "task_id": task_id,
                    "agent": agent,
                    "trial": trial,
                    "status": status,
                    "runtime_seconds": runtime,
                    "failure_type": (raw.get("failure_type") or "").strip(),
                }
            )

    if not rows:
        raise ValueError("CSV contains no trial records.")

    return rows


def summarize_results(rows: list[dict[str, object]]) -> dict[str, object]:
    """计算通过率、运行时间和失败类型等描述性统计。"""

    if not rows:
        raise ValueError("No records to summarize.")

    total = len(rows)
    statuses = Counter(str(row["status"]) for row in rows)
    runtimes = [float(row["runtime_seconds"]) for row in rows]

    # 只有非 passed 记录才统计 failure_type；空字符串直接忽略。
    failures = Counter(
        str(row["failure_type"])
        for row in rows
        if str(row["status"]) != "passed" and str(row["failure_type"]).strip()
    )

    passed = statuses.get("passed", 0)

    return {
        "total_trials": total,
        "passed_trials": passed,
        "pass_rate": passed / total,
        "mean_runtime_seconds": statistics.fmean(runtimes),
        "median_runtime_seconds": statistics.median(runtimes),
        "status_counts": {
            status: statuses.get(status, 0) for status in sorted(VALID_STATUSES)
        },
        "failure_types": dict(sorted(failures.items())),
    }


def render_markdown(summary: dict[str, object]) -> str:
    """把汇总字典转换成可直接保存的 Markdown 文本。"""

    lines = [
        "# Evaluation Summary",
        "",
        "## Overall Metrics",
        "",
        f"- Total trials: {summary['total_trials']}",
        f"- Passed trials: {summary['passed_trials']}",
        f"- Pass rate: {summary['pass_rate']:.1%}",
        f"- Mean runtime: {summary['mean_runtime_seconds']:.2f} s",
        f"- Median runtime: {summary['median_runtime_seconds']:.2f} s",
        "",
        "## Status Distribution",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]

    status_counts = summary["status_counts"]
    for status in sorted(VALID_STATUSES):
        lines.append(f"| {status} | {status_counts.get(status, 0)} |")

    lines += ["", "## Failure Categories", ""]
    failure_types = summary["failure_types"]

    if failure_types:
        lines += ["| Failure type | Count |", "| --- | ---: |"]
        for name, count in failure_types.items():
            lines.append(f"| {name} | {count} |")
    else:
        lines.append("No failure categories were recorded.")

    lines += [
        "",
        "> Pass rate = passed trials / all trial records. "
        "Failed, error, and timeout records remain in the denominator.",
        "",
    ]

    return "\n".join(lines)


def main() -> int:
    """解析命令行参数并打印（或保存）汇总报告。"""

    parser = argparse.ArgumentParser(
        description="Summarize synthetic Agent evaluation results."
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        rows = load_results(args.csv_path)
        summary = summarize_results(rows)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    report = render_markdown(summary)
    print(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"\nReport written to: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
