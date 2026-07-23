#!/usr/bin/env python3
"""Check the dependency-free tracked release-asset size budget."""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath


BUDGET_PATH = "assets/asset-budget.json"
SCHEMA_VERSION = "asset-budget-v1"
REPORT_SCHEMA_VERSION = "asset-budget-report-v1"
REQUIRED_CLASS_FIELDS = (
  "id", "root", "include", "exclude", "max_files", "max_file_bytes",
  "max_total_bytes",
)


def _is_nonnegative_int(value: object) -> bool:
  return type(value) is int and value >= 0


def _resolve_under_root(root: Path, value: str) -> Path:
  if Path(value).is_absolute():
    raise ValueError("path must be relative to repository root")
  candidate = (root / value).resolve()
  resolved_root = root.resolve()
  if candidate != resolved_root and resolved_root not in candidate.parents:
    raise ValueError("path escapes repository root")
  return candidate


def _matches(relative: str, patterns: list[str]) -> bool:
  path = PurePosixPath(relative)
  return any(pattern == "*" or path.match(pattern) for pattern in patterns)


def validate_definition(root: Path, document: dict) -> list[str]:
  if not isinstance(document, dict):
    return ["budget document must be an object"]
  errors: list[str] = []
  if document.get("schema_version") != SCHEMA_VERSION:
    errors.append("unsupported asset budget schema_version")
  if not isinstance(document.get("scope"), str) or not document["scope"].strip():
    errors.append("scope must be a non-empty string")
  budgets = document.get("budgets")
  if not isinstance(budgets, list) or not budgets:
    return errors + ["budgets must be a non-empty list"]

  ids: set[str] = set()
  for index, budget in enumerate(budgets):
    location = f"budgets[{index}]"
    if not isinstance(budget, dict):
      errors.append(f"{location} must be an object")
      continue
    for field in REQUIRED_CLASS_FIELDS:
      if field not in budget:
        errors.append(f"{location} missing field {field!r}")
    budget_id = budget.get("id")
    if not isinstance(budget_id, str) or not budget_id.strip():
      errors.append(f"{location}.id must be a non-empty string")
    elif budget_id in ids:
      errors.append(f"{location}.id is duplicated: {budget_id!r}")
    else:
      ids.add(budget_id)
    root_value = budget.get("root")
    if not isinstance(root_value, str) or not root_value.strip():
      errors.append(f"{location}.root must be a non-empty relative path")
    else:
      try:
        budget_root = _resolve_under_root(root, root_value)
      except ValueError as error:
        errors.append(f"{location}.root is invalid: {error}")
      else:
        if not budget_root.is_dir():
          errors.append(f"{location}.root is not a directory: {root_value}")
    for field in ("include", "exclude"):
      patterns = budget.get(field)
      if not isinstance(patterns, list) or not all(
        isinstance(pattern, str) and pattern.strip() for pattern in patterns
      ):
        errors.append(f"{location}.{field} must be a list of non-empty strings")
    for field in ("max_files", "max_file_bytes", "max_total_bytes"):
      if not _is_nonnegative_int(budget.get(field)):
        errors.append(f"{location}.{field} must be a non-negative integer")
  return errors


def _files_for_budget(root: Path, budget: dict) -> list[Path]:
  budget_root = _resolve_under_root(root, budget["root"])
  files = []
  for path in sorted(budget_root.rglob("*")):
    if not path.is_file():
      continue
    relative = path.relative_to(budget_root).as_posix()
    if not _matches(relative, budget["include"]):
      continue
    if _matches(relative, budget["exclude"]):
      continue
    files.append(path)
  return files


def build_report(root: Path, document: dict) -> dict:
  errors = validate_definition(root, document)
  budgets = []
  for budget in document.get("budgets", []):
    if not isinstance(budget, dict) or not all(field in budget for field in REQUIRED_CLASS_FIELDS):
      continue
    try:
      files = _files_for_budget(root, budget)
    except (KeyError, ValueError):
      continue
    records = [
      {
        "path": path.relative_to(root).as_posix(),
        "bytes": path.stat().st_size,
      }
      for path in files
    ]
    total_bytes = sum(record["bytes"] for record in records)
    largest = max(records, key=lambda record: (record["bytes"], record["path"]), default=None)
    class_errors = []
    if not records:
      class_errors.append("budget class matched no files")
    if len(records) > budget["max_files"]:
      class_errors.append(f"file count {len(records)} exceeds {budget['max_files']}")
    if largest and largest["bytes"] > budget["max_file_bytes"]:
      class_errors.append(
        f"largest file {largest['bytes']} bytes exceeds {budget['max_file_bytes']}"
      )
    if total_bytes > budget["max_total_bytes"]:
      class_errors.append(
        f"total size {total_bytes} bytes exceeds {budget['max_total_bytes']}"
      )
    errors.extend(f"{budget['id']}: {error}" for error in class_errors)
    budgets.append({
      "id": budget["id"],
      "root": budget["root"],
      "file_count": len(records),
      "total_bytes": total_bytes,
      "largest_file": largest,
      "limits": {
        "max_files": budget["max_files"],
        "max_file_bytes": budget["max_file_bytes"],
        "max_total_bytes": budget["max_total_bytes"],
      },
      "status": "pass" if not class_errors else "fail",
    })
  return {
    "schema_version": REPORT_SCHEMA_VERSION,
    "budget_schema_version": document.get("schema_version"),
    "scope": document.get("scope"),
    "status": "pass" if not errors else "fail",
    "errors": errors,
    "budgets": budgets,
  }


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  budget_path = root / BUDGET_PATH
  try:
    document = json.loads(budget_path.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    report = {
      "schema_version": REPORT_SCHEMA_VERSION,
      "status": "fail",
      "errors": [f"cannot read {BUDGET_PATH}: {error}"],
      "budgets": [],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1
  report = build_report(root, document)
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  raise SystemExit(main())
