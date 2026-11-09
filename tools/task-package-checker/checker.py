#!/usr/bin/env python3
"""Basic validator for this repository's generic practice-task format."""
import argparse
import json
import sys
from pathlib import Path

FIELDS = {"id": str, "title": str, "description": str, "difficulty": str, "timeout_seconds": int}
DIFFICULTIES = {"easy", "medium", "hard"}

def validate_task_package(package_dir: Path):
    errors, warnings = [], []
    if not package_dir.exists():
        return [f"Package directory does not exist: {package_dir}"], warnings
    if not package_dir.is_dir():
        return [f"Package path is not a directory: {package_dir}"], warnings

    metadata_path = package_dir / "task.json"
    instruction = package_dir / "instruction.md"
    dockerfile = package_dir / "environment" / "Dockerfile"
    tests_dir = package_dir / "tests"

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

    if metadata is not None:
        if not isinstance(metadata, dict):
            errors.append("task.json must contain a JSON object.")
        else:
            for field, expected in FIELDS.items():
                if field not in metadata:
                    errors.append(f"task.json is missing required field: {field}")
                    continue
                value = metadata[field]
                valid = (isinstance(value, int) and not isinstance(value, bool)) if expected is int else isinstance(value, expected)
                if not valid:
                    errors.append(f"task.json field '{field}' must be {expected.__name__}.")
                elif expected is str and not value.strip():
                    errors.append(f"task.json field '{field}' must not be empty.")
            difficulty = metadata.get("difficulty")
            if isinstance(difficulty, str) and difficulty not in DIFFICULTIES:
                errors.append("task.json field 'difficulty' must be one of: easy, medium, hard.")
            timeout = metadata.get("timeout_seconds")
            if isinstance(timeout, int) and not isinstance(timeout, bool) and timeout <= 0:
                errors.append("task.json field 'timeout_seconds' must be greater than 0.")
            if "tags" not in metadata:
                warnings.append("Optional field 'tags' is not present in task.json.")

    if not instruction.is_file():
        errors.append("Missing required file: instruction.md")
    else:
        try:
            if not instruction.read_text(encoding="utf-8").strip():
                errors.append("instruction.md must not be empty.")
        except OSError as exc:
            errors.append(f"Could not read instruction.md: {exc}")
    if not dockerfile.is_file():
        errors.append("Missing required file: environment/Dockerfile")
    if not tests_dir.is_dir():
        errors.append("Missing required directory: tests/")
    elif not any(p.is_file() and p.suffix == ".py" for p in tests_dir.iterdir()):
        errors.append("tests/ must contain at least one Python test file.")
    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Check a generic practice-task package.")
    parser.add_argument("package_dir", type=Path)
    args = parser.parse_args()
    errors, warnings = validate_task_package(args.package_dir)
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"FAIL: {item}")
    if errors:
        print(f"\\nRESULT: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print("PASS: package structure and required metadata are valid.")
    print("RESULT: " + ("PASS WITH WARNINGS" if warnings else "PASS"))
    return 0

if __name__ == "__main__":
    sys.exit(main())
