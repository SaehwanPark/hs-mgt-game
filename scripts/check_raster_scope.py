#!/usr/bin/env python3
"""Check release-raster absence and bounded preview-only raster scope."""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path


SCOPE_PATH = "assets/raster-scope.json"
REPORT_SCHEMA_VERSION = "raster-scope-report-v1"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
REQUIRED_FIELDS = (
  "schema_version", "release_root", "preview_root", "preview_metadata",
  "preview_expected_count",
  "supported_extensions", "preview_max_width", "preview_max_height",
  "preview_max_file_bytes", "preview_max_total_bytes",
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


def validate_definition(root: Path, document: object) -> list[str]:
  if not isinstance(document, dict):
    return ["raster scope document must be an object"]
  errors = []
  if document.get("schema_version") != "raster-scope-v1":
    errors.append("unsupported raster scope schema_version")
  for field in REQUIRED_FIELDS:
    if field not in document:
      errors.append(f"missing field {field!r}")
  for field in ("release_root", "preview_root", "preview_metadata"):
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
      errors.append(f"{field} must be a non-empty relative path")
    else:
      try:
        resolved = _resolve(root, value)
      except ValueError as error:
        errors.append(f"{field} is invalid: {error}")
      else:
        if field == "preview_metadata" and not resolved.is_file():
          errors.append(f"{field} does not exist: {value}")
        if field != "preview_metadata" and not resolved.is_dir():
          errors.append(f"{field} directory does not exist: {value}")
  if not _nonnegative_int(document.get("preview_expected_count")) or document.get("preview_expected_count") == 0:
    errors.append("preview_expected_count must be a positive integer")
  extensions = document.get("supported_extensions")
  if not isinstance(extensions, list) or not extensions or not all(
    isinstance(extension, str) and extension.startswith(".") and extension == extension.lower()
    for extension in extensions
  ):
    errors.append("supported_extensions must be non-empty lowercase suffixes")
  for field in (
    "preview_max_width", "preview_max_height", "preview_max_file_bytes",
    "preview_max_total_bytes",
  ):
    if not _nonnegative_int(document.get(field)) or document.get(field) == 0:
      errors.append(f"{field} must be a positive integer")
  return errors


def _files(root: Path, relative_root: str, extensions: set[str]) -> list[Path]:
  directory = _resolve(root, relative_root)
  if not directory.is_dir():
    return []
  return sorted(
    path for path in directory.rglob("*")
    if path.is_file() and path.suffix.lower() in extensions
  )


def release_raster_errors(root: Path, files: list[Path]) -> list[str]:
  return [f"release raster file is not allowed: {_relative(root, path)}" for path in files]


def png_dimensions(path: Path) -> tuple[int, int] | None:
  data = path.read_bytes()
  if len(data) < 24 or data[:8] != PNG_SIGNATURE or data[12:16] != b"IHDR":
    return None
  width, height = struct.unpack(">II", data[16:24])
  return width, height


def _relative(root: Path, path: Path) -> str:
  return path.resolve().relative_to(root.resolve()).as_posix()


def build_report(root: Path, document: object) -> dict:
  errors = validate_definition(root, document)
  if not isinstance(document, dict) or errors:
    return {
      "schema_version": REPORT_SCHEMA_VERSION,
      "status": "fail",
      "errors": errors,
      "release_raster_count": 0,
      "release_raster_files": [],
      "preview_count": 0,
      "preview_total_bytes": 0,
      "previews": [],
    }

  extensions = set(document["supported_extensions"])
  release_files = _files(root, document["release_root"], extensions)
  preview_files = _files(root, document["preview_root"], {".png"})
  errors.extend(release_raster_errors(root, release_files))

  metadata_path = _resolve(root, document["preview_metadata"])
  preview_metadata = None
  try:
    preview_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    errors.append(f"cannot read preview metadata: {error}")
  if not isinstance(preview_metadata, dict):
    errors.append("preview metadata must be an object")
    preview_entries = []
  else:
    if preview_metadata.get("release_eligible") is not False:
      errors.append("preview metadata release_eligible must be false")
    preview_entries = preview_metadata.get("entries")
    if not isinstance(preview_entries, list):
      errors.append("preview metadata entries must be a list")
      preview_entries = []
    elif len(preview_entries) != document["preview_expected_count"]:
      errors.append("preview metadata entry count does not match scope")

  metadata_paths = set()
  previews = []
  preview_total_bytes = 0
  for index, entry in enumerate(preview_entries):
    location = f"preview metadata entries[{index}]"
    if not isinstance(entry, dict):
      errors.append(f"{location} must be an object")
      continue
    source_path = entry.get("source_output_path")
    if not isinstance(source_path, str):
      errors.append(f"{location} source_output_path must be a string")
      continue
    try:
      path = _resolve(root, source_path)
    except ValueError as error:
      errors.append(f"{location} source_output_path is invalid: {error}")
      continue
    metadata_paths.add(path)
    if entry.get("release_path") is not None or entry.get("asset_registry_id") is not None:
      errors.append(f"{location} cannot carry release promotion fields")
    if entry.get("preview_status") != "unverified-preview" or entry.get("approval_status") != "pending":
      errors.append(f"{location} must remain an unverified pending preview")
    if not path.is_file():
      errors.append(f"{location} preview file is missing: {source_path}")
      continue
    dimensions = png_dimensions(path)
    size = path.stat().st_size
    preview_total_bytes += size
    record = {
      "path": _relative(root, path),
      "bytes": size,
      "dimensions": {"width": dimensions[0], "height": dimensions[1]} if dimensions else None,
      "status": "pass",
    }
    if dimensions is None:
      errors.append(f"{location} is not a valid PNG: {source_path}")
      record["status"] = "fail"
    else:
      width, height = dimensions
      if width > document["preview_max_width"] or height > document["preview_max_height"]:
        errors.append(f"{location} dimensions exceed preview bounds: {source_path}")
        record["status"] = "fail"
      if size > document["preview_max_file_bytes"]:
        errors.append(f"{location} bytes exceed preview bound: {source_path}")
        record["status"] = "fail"
    previews.append(record)

  if metadata_paths != set(preview_files):
    errors.append("preview metadata paths must exactly match preview PNG files")
  if preview_total_bytes > document["preview_max_total_bytes"]:
    errors.append("preview total bytes exceed preview bound")
  return {
    "schema_version": REPORT_SCHEMA_VERSION,
    "status": "pass" if not errors else "fail",
    "errors": errors,
    "release_raster_count": len(release_files),
    "release_raster_files": [_relative(root, path) for path in release_files],
    "preview_count": len(preview_files),
    "preview_total_bytes": preview_total_bytes,
    "preview_limits": {
      "max_width": document["preview_max_width"],
      "max_height": document["preview_max_height"],
      "max_file_bytes": document["preview_max_file_bytes"],
      "max_total_bytes": document["preview_max_total_bytes"],
    },
    "previews": previews,
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
