#!/usr/bin/env python3
"""Check the current file-backed audio packaging boundary."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SCOPE_PATH = "assets/audio-packaging-scope.json"
REPORT_SCHEMA_VERSION = "audio-packaging-report-v1"
REQUIRED_FIELDS = (
  "schema_version",
  "release_root",
  "supported_extensions",
  "expected_release_audio_count",
  "max_release_audio_total_bytes",
  "compression_decision",
  "runtime_generated_sources",
  "registry_paths",
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


def _nonnegative_int(value: object) -> bool:
  return type(value) is int and value >= 0


def _relative(root: Path, path: Path) -> str:
  return path.absolute().relative_to(root.resolve()).as_posix()


def validate_definition(root: Path, document: object) -> list[str]:
  if not isinstance(document, dict):
    return ["audio packaging scope document must be an object"]
  errors = []
  if document.get("schema_version") != "audio-packaging-scope-v1":
    errors.append("unsupported audio packaging scope schema_version")
  for field in REQUIRED_FIELDS:
    if field not in document:
      errors.append(f"missing field {field!r}")

  release_root = document.get("release_root")
  if not isinstance(release_root, str) or not release_root.strip():
    errors.append("release_root must be a non-empty relative path")
  else:
    try:
      resolved = _resolve(root, release_root)
    except ValueError as error:
      errors.append(f"release_root is invalid: {error}")
    else:
      if not resolved.is_dir():
        errors.append(f"release_root directory does not exist: {release_root}")
      elif (root / release_root).is_symlink():
        errors.append("release_root cannot be a symlink")

  extensions = document.get("supported_extensions")
  if not isinstance(extensions, list) or not extensions or not all(
    isinstance(extension, str) and extension.startswith(".") and extension == extension.lower()
    for extension in extensions
  ):
    errors.append("supported_extensions must be non-empty lowercase suffixes")

  for field in ("expected_release_audio_count", "max_release_audio_total_bytes"):
    if not _nonnegative_int(document.get(field)):
      errors.append(f"{field} must be a non-negative integer")

  if document.get("compression_decision") != "not-applicable-runtime-generated":
    errors.append("compression_decision must record the runtime-generated decision")

  for field in ("runtime_generated_sources", "registry_paths"):
    paths = document.get(field)
    if not isinstance(paths, list) or not paths or not all(isinstance(path, str) and path.strip() for path in paths):
      errors.append(f"{field} must be a non-empty list of paths")
      continue
    for path in paths:
      try:
        resolved = _resolve(root, path)
      except ValueError as error:
        errors.append(f"{field} path is invalid: {error}")
      else:
        if not resolved.is_file():
          errors.append(f"{field} path does not exist: {path}")
  return errors


def _files(root: Path, relative_root: str, extensions: set[str]) -> list[Path]:
  directory = _resolve(root, relative_root)
  if not directory.is_dir():
    return []
  return sorted(
    path for path in directory.rglob("*")
    if path.is_file() and path.suffix.lower() in extensions
  )


def _symlinks(root: Path, relative_root: str) -> list[Path]:
  directory = _resolve(root, relative_root)
  if not directory.is_dir():
    return []
  return sorted(path for path in directory.rglob("*") if path.is_symlink())


def release_audio_errors(root: Path, files: list[Path]) -> list[str]:
  return [f"release audio file is not allowed in current scope: {_relative(root, path)}" for path in files]


def release_symlink_errors(root: Path, paths: list[Path]) -> list[str]:
  return [f"release tree symlink is not allowed in current scope: {_relative(root, path)}" for path in paths]


def registry_release_errors(
  root: Path,
  registry_paths: list[str],
  runtime_generated_sources: set[str],
) -> tuple[list[str], int]:
  errors = []
  entry_count = 0
  for registry_path in registry_paths:
    path = _resolve(root, registry_path)
    try:
      document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
      errors.append(f"cannot read audio registry {_relative(root, path)}: {error}")
      continue
    if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
      errors.append(f"audio registry entries must be a list: {_relative(root, path)}")
      continue
    entries = document["entries"]
    entry_count += len(entries)
    for index, entry in enumerate(entries):
      if not isinstance(entry, dict):
        errors.append(f"audio registry entry {index} must be an object: {_relative(root, path)}")
        continue
      source = entry.get("source_path", entry.get("source"))
      if not isinstance(source, str) or source not in runtime_generated_sources:
        errors.append(
          f"audio registry entry {index} source is outside the declared runtime-generated scope: "
          f"{_relative(root, path)}"
        )
      if "release_path" not in entry or entry.get("release_path") is not None:
        errors.append(
          f"audio registry entry {index} must have an explicit null release_path in current runtime-generated scope: "
          f"{_relative(root, path)}"
        )
    if registry_path == "gui/audio-catalog.json" and document.get("third_party_assets") != []:
      errors.append("gui audio catalog third_party_assets must be empty in current scope")
  return errors, entry_count


def build_report(root: Path, document: object) -> dict:
  errors = validate_definition(root, document)
  if not isinstance(document, dict) or errors:
    return {
      "schema_version": REPORT_SCHEMA_VERSION,
      "status": "fail",
      "errors": errors,
      "compression_decision": None,
      "release_audio_count": 0,
      "release_audio_total_bytes": 0,
      "release_audio_files": [],
      "registry_entry_count": 0,
    }

  extensions = set(document["supported_extensions"])
  release_files = _files(root, document["release_root"], extensions)
  errors.extend(release_audio_errors(root, release_files))
  release_symlinks = _symlinks(root, document["release_root"])
  errors.extend(release_symlink_errors(root, release_symlinks))
  total_bytes = sum(path.stat().st_size for path in release_files)
  if len(release_files) != document["expected_release_audio_count"]:
    errors.append("release audio file count does not match scope")
  if total_bytes > document["max_release_audio_total_bytes"]:
    errors.append("release audio total bytes exceed scope")
  registry_errors, registry_entry_count = registry_release_errors(
    root,
    document["registry_paths"],
    set(document["runtime_generated_sources"]),
  )
  errors.extend(registry_errors)
  return {
    "schema_version": REPORT_SCHEMA_VERSION,
    "status": "pass" if not errors else "fail",
    "errors": errors,
    "compression_decision": document["compression_decision"],
    "release_audio_count": len(release_files),
    "release_audio_total_bytes": total_bytes,
    "release_audio_files": [_relative(root, path) for path in release_files],
    "release_symlinks": [_relative(root, path) for path in release_symlinks],
    "registry_entry_count": registry_entry_count,
    "runtime_generated_sources": document["runtime_generated_sources"],
  }


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  try:
    document = json.loads((root / SCOPE_PATH).read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    report = {"schema_version": REPORT_SCHEMA_VERSION, "status": "fail", "errors": [str(error)]}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1
  report = build_report(root, document)
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  raise SystemExit(main())
