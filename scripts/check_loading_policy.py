#!/usr/bin/env python3
"""Check the current live GUI asset-loading policy."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


POLICY_PATH = "assets/loading-policy.json"
REPORT_SCHEMA_VERSION = "loading-policy-report-v1"
REQUIRED_FIELDS = (
  "schema_version",
  "live_entrypoint",
  "live_files",
  "lazy_loading_decision",
  "preloading_decision",
  "forbidden_markers",
  "future_asset_requirements",
)
SCRIPT_SOURCE_PATTERN = re.compile(r"<script\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
MODULE_SOURCE_PATTERNS = (
  re.compile(r"^\s*import\s+(?:[^;\n]*?\sfrom\s+)?[\"']([^\"']+)[\"']", re.MULTILINE),
  re.compile(r"^\s*export\s+[^;\n]*?\sfrom\s+[\"']([^\"']+)[\"']", re.MULTILINE),
  re.compile(r"\bimport\s*\(\s*[\"']([^\"']+)[\"']\s*\)"),
)


def _resolve(root: Path, relative: str) -> Path:
  candidate = Path(relative)
  if candidate.is_absolute():
    raise ValueError("path must be relative to repository root")
  resolved = (root / candidate).resolve()
  resolved_root = root.resolve()
  if resolved != resolved_root and resolved_root not in resolved.parents:
    raise ValueError("path escapes repository root")
  return resolved


def _symlink_components(root: Path, relative: str) -> list[Path]:
  current = root
  symlinks = []
  for part in Path(relative).parts:
    if part in ("", "."):
      continue
    current /= part
    if current.is_symlink():
      symlinks.append(current)
  return symlinks


def _relative(root: Path, path: Path) -> str:
  return path.resolve().relative_to(root.resolve()).as_posix()


def _valid_string_list(value: object) -> bool:
  return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def validate_definition(root: Path, document: object) -> list[str]:
  if not isinstance(document, dict):
    return ["loading policy document must be an object"]
  errors = []
  if document.get("schema_version") != "loading-policy-v1":
    errors.append("unsupported loading policy schema_version")
  for field in REQUIRED_FIELDS:
    if field not in document:
      errors.append(f"missing field {field!r}")

  entrypoint = document.get("live_entrypoint")
  if not isinstance(entrypoint, str) or not entrypoint.strip():
    errors.append("live_entrypoint must be a non-empty relative path")
  else:
    try:
      resolved = _resolve(root, entrypoint)
    except ValueError as error:
      errors.append(f"live_entrypoint is invalid: {error}")
    else:
      if not resolved.is_file():
        errors.append(f"live_entrypoint does not exist: {entrypoint}")
      elif _symlink_components(root, entrypoint):
        errors.append("live_entrypoint path cannot contain symlinks")

  live_files = document.get("live_files")
  if not _valid_string_list(live_files):
    errors.append("live_files must be a non-empty list of paths")
    live_files = []
  for path in live_files:
    try:
      resolved = _resolve(root, path)
    except ValueError as error:
      errors.append(f"live_files path is invalid: {error}")
    else:
      if not resolved.is_file():
        errors.append(f"live_files path does not exist: {path}")
      elif _symlink_components(root, path):
        errors.append(f"live_files path cannot contain symlinks: {path}")
  if isinstance(entrypoint, str) and entrypoint not in live_files:
    errors.append("live_entrypoint must be included in live_files")

  if document.get("lazy_loading_decision") != "no-lazy-loading-needed":
    errors.append("lazy_loading_decision must record the current no-lazy decision")
  if document.get("preloading_decision") != "no-preload-directives":
    errors.append("preloading_decision must record the current no-preload decision")

  markers = document.get("forbidden_markers")
  if not _valid_string_list([item.get("id") for item in markers] if isinstance(markers, list) and all(isinstance(item, dict) for item in markers) else []):
    errors.append("forbidden_markers must be a non-empty list of objects with IDs and patterns")
  else:
    marker_ids = set()
    for marker in markers:
      marker_id = marker.get("id")
      pattern = marker.get("pattern")
      if marker_id in marker_ids:
        errors.append(f"duplicate forbidden marker ID: {marker_id}")
      marker_ids.add(marker_id)
      if not isinstance(pattern, str) or not pattern:
        errors.append(f"forbidden marker pattern must be non-empty: {marker_id}")
      else:
        try:
          re.compile(pattern, re.IGNORECASE)
        except re.error as error:
          errors.append(f"forbidden marker pattern is invalid for {marker_id}: {error}")

  requirements = document.get("future_asset_requirements")
  if not _valid_string_list(requirements):
    errors.append("future_asset_requirements must be a non-empty list of strings")
  else:
    required = {
      "registry_id", "live_consumer", "load_trigger",
      "preload_justification_or_lazy_trigger", "byte_budget", "fallback",
      "written_equivalent", "provenance",
    }
    if len(requirements) != len(set(requirements)):
      errors.append("future_asset_requirements must not contain duplicates")
    if set(requirements) != required:
      errors.append("future_asset_requirements must cover the complete loading contract")
  return errors


def _markers(document: dict) -> list[dict]:
  return [
    {"id": marker["id"], "pattern": re.compile(marker["pattern"], re.IGNORECASE)}
    for marker in document["forbidden_markers"]
  ]


def scan_markers(root: Path, relative_path: str, markers: list[dict]) -> list[str]:
  path = _resolve(root, relative_path)
  text = path.read_text(encoding="utf-8")
  errors = []
  for marker in markers:
    for match in marker["pattern"].finditer(text):
      line = text.count("\n", 0, match.start()) + 1
      errors.append(f"forbidden loading marker {marker['id']} in {relative_path}:{line}")
  return errors


def entrypoint_sources(root: Path, entrypoint: str) -> tuple[list[str], list[str]]:
  entrypoint_path = _resolve(root, entrypoint)
  text = entrypoint_path.read_text(encoding="utf-8")
  paths = []
  errors = []
  for source in SCRIPT_SOURCE_PATTERN.findall(text):
    if "://" in source or source.startswith("/"):
      errors.append(f"live entrypoint source is not local: {source}")
      continue
    source_path = (entrypoint_path.parent / source).resolve()
    try:
      paths.append(_relative(root, source_path))
    except ValueError:
      errors.append(f"live entrypoint source escapes repository root: {source}")
  return sorted(set(paths)), errors


def module_sources(root: Path, live_files: list[str]) -> tuple[list[str], list[str]]:
  paths = []
  errors = []
  for relative_path in live_files:
    source_path = _resolve(root, relative_path)
    text = source_path.read_text(encoding="utf-8")
    for pattern in MODULE_SOURCE_PATTERNS:
      for source in pattern.findall(text):
        if "://" in source or source.startswith("/") or not source.startswith("./"):
          errors.append(f"module source is not local: {relative_path} -> {source}")
          continue
        resolved = (source_path.parent / source).resolve()
        try:
          paths.append(_relative(root, resolved))
        except ValueError:
          errors.append(f"module source escapes repository root: {relative_path} -> {source}")
  return sorted(set(paths)), errors


def build_report(root: Path, document: object) -> dict:
  errors = validate_definition(root, document)
  if not isinstance(document, dict) or errors:
    return {
      "schema_version": REPORT_SCHEMA_VERSION,
      "status": "fail",
      "errors": errors,
      "live_file_count": 0,
      "marker_hits": [],
      "entrypoint_sources": [],
    }

  live_files = document["live_files"]
  marker_rules = _markers(document)
  marker_hits = []
  for path in live_files:
    marker_hits.extend(scan_markers(root, path, marker_rules))
  entrypoint_module_sources, source_errors = entrypoint_sources(root, document["live_entrypoint"])
  discovered_modules, module_errors = module_sources(root, live_files)
  discovered_sources = sorted(set(entrypoint_module_sources + discovered_modules))
  declared_sources = {_relative(root, _resolve(root, path)) for path in live_files}
  for source in discovered_sources:
    if source not in declared_sources:
      errors.append(f"live entrypoint source is not declared in policy: {source}")
  errors.extend(marker_hits)
  errors.extend(source_errors)
  errors.extend(module_errors)
  return {
    "schema_version": REPORT_SCHEMA_VERSION,
    "status": "pass" if not errors else "fail",
    "errors": errors,
    "live_file_count": len(live_files),
    "live_files": live_files,
    "entrypoint_sources": entrypoint_module_sources,
    "module_sources": discovered_modules,
    "discovered_sources": discovered_sources,
    "marker_hits": marker_hits,
    "decisions": {
      "lazy_loading": document["lazy_loading_decision"],
      "preloading": document["preloading_decision"],
    },
    "future_asset_requirements": document["future_asset_requirements"],
  }


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  try:
    document = json.loads((root / POLICY_PATH).read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    report = {"schema_version": REPORT_SCHEMA_VERSION, "status": "fail", "errors": [str(error)]}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1
  report = build_report(root, document)
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  raise SystemExit(main())
