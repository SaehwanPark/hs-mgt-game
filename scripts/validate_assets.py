#!/usr/bin/env python3
"""Validate the dependency-free visual/audio asset registries."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ALLOWLIST = {
  "project-generated", "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0",
  "MIT", "Apache-2.0", "GPL-3.0-or-later", "OFL-1.1",
}
DENYLIST_MARKERS = (
  "all-rights-reserved", "personal-use", "non-commercial", "noncommercial",
  "redistribution-hostile", "unclear", "proprietary", "capitalism 2",
)
SEMANTIC_ROLES = {
  "identity", "marker", "status", "facility", "map", "overlay", "ui-cue",
  "event-cue", "ambience", "music-state", "decorative",
}
REQUIRED_FIELDS = (
  "id", "asset_type", "semantic_role", "source_path", "release_path",
  "creator", "creation_method", "license", "modifications", "original_hash",
  "release_hash", "attribution_text", "accessible_equivalent", "visible_source",
  "approval_status",
)
REGISTRIES = (
  ("assets/registry/visual-assets.json", "visual"),
  ("assets/registry/audio-assets.json", "audio"),
)
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _sha256(path: Path) -> str:
  digest = hashlib.sha256()
  with path.open("rb") as stream:
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
      digest.update(chunk)
  return f"sha256:{digest.hexdigest()}"


def _non_empty(value) -> bool:
  return isinstance(value, str) and bool(value.strip())


def _path_from_registry(root: Path, value: str) -> Path:
  path = (root / value).resolve()
  if root.resolve() not in path.parents and path != root.resolve():
    raise ValueError("path escapes repository root")
  return path


def _validate_entry(root: Path, entry: dict, expected_type: str, location: str) -> list[str]:
  errors: list[str] = []
  for field in REQUIRED_FIELDS:
    if field not in entry:
      errors.append(f"{location}: missing field {field!r}")

  asset_id = entry.get("id")
  if not isinstance(asset_id, str) or not ID_PATTERN.fullmatch(asset_id):
    errors.append(f"{location}: id must be a non-empty token")
  if entry.get("asset_type") != expected_type:
    errors.append(f"{location}: asset_type must be {expected_type!r}")
  if entry.get("semantic_role") not in SEMANTIC_ROLES:
    errors.append(f"{location}: unknown semantic role {entry.get('semantic_role')!r}")
  for field in ("creator", "creation_method", "modifications", "attribution_text", "accessible_equivalent", "visible_source"):
    if not _non_empty(entry.get(field)):
      errors.append(f"{location}: {field} is required")

  license_name = entry.get("license")
  if license_name not in ALLOWLIST:
    errors.append(f"{location}: license is not allowlisted: {license_name!r}")
  searchable = json.dumps(entry, sort_keys=True).lower()
  for marker in DENYLIST_MARKERS:
    if marker in searchable:
      errors.append(f"{location}: denylisted provenance marker {marker!r}")

  if entry.get("approval_status") not in {"approved", "pending", "rejected"}:
    errors.append(f"{location}: invalid approval_status")
  if entry.get("release_path") and entry.get("approval_status") != "approved":
    errors.append(f"{location}: release asset must be approved")

  source_path = entry.get("source_path")
  if source_path is not None and not isinstance(source_path, str):
    errors.append(f"{location}: source_path must be a string or null")
  elif source_path:
    try:
      resolved = _path_from_registry(root, source_path)
    except ValueError as error:
      errors.append(f"{location}: invalid source_path ({error})")
    else:
      if not resolved.is_file():
        errors.append(f"{location}: source_path does not exist: {source_path}")
      elif entry.get("original_hash") != _sha256(resolved):
        errors.append(f"{location}: original_hash does not match {source_path}")
  elif entry.get("original_hash") is not None:
    errors.append(f"{location}: original_hash must be null without source_path")

  release_path = entry.get("release_path")
  if release_path is not None and not isinstance(release_path, str):
    errors.append(f"{location}: release_path must be a string or null")
  elif release_path:
    try:
      resolved = _path_from_registry(root, release_path)
    except ValueError as error:
      errors.append(f"{location}: invalid release_path ({error})")
    else:
      if not resolved.is_file():
        errors.append(f"{location}: release_path does not exist: {release_path}")
      elif entry.get("release_hash") != _sha256(resolved):
        errors.append(f"{location}: release_hash does not match {release_path}")
  elif entry.get("release_hash") is not None:
    errors.append(f"{location}: release_hash must be null without release_path")
  return errors


def validate_registry(root: Path, relative_path: str, expected_type: str) -> tuple[list[str], list[dict]]:
  path = root / relative_path
  try:
    document = json.loads(path.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    return [f"{relative_path}: cannot read JSON ({error})"], []
  errors: list[str] = []
  if document.get("schema_version") != "asset-registry-v1":
    errors.append(f"{relative_path}: unsupported schema_version")
  if document.get("asset_type") != expected_type:
    errors.append(f"{relative_path}: registry asset_type must be {expected_type!r}")
  entries = document.get("entries")
  if not isinstance(entries, list):
    return errors + [f"{relative_path}: entries must be a list"], []
  ids: set[str] = set()
  for index, entry in enumerate(entries):
    location = f"{relative_path}:entries[{index}]"
    if not isinstance(entry, dict):
      errors.append(f"{location}: entry must be an object")
      continue
    asset_id = entry.get("id")
    if asset_id in ids:
      errors.append(f"{location}: duplicate asset ID {asset_id!r}")
    ids.add(asset_id)
    errors.extend(_validate_entry(root, entry, expected_type, location))
  return errors, entries


def validate(root: Path) -> list[str]:
  errors: list[str] = []
  all_ids: set[str] = set()
  registered_release_paths: set[str] = set()
  for relative_path, expected_type in REGISTRIES:
    registry_errors, entries = validate_registry(root, relative_path, expected_type)
    errors.extend(registry_errors)
    for entry in entries:
      asset_id = entry.get("id")
      if asset_id in all_ids:
        errors.append(f"duplicate asset ID across registries: {asset_id!r}")
      all_ids.add(asset_id)
      if entry.get("release_path"):
        registered_release_paths.add(entry["release_path"])

  release_root = root / "assets" / "release"
  if release_root.is_dir():
    for path in sorted(release_root.rglob("*")):
      if path.is_file() and path.name != "README.md":
        relative_path = path.relative_to(root).as_posix()
        if relative_path not in registered_release_paths:
          errors.append(f"unregistered release asset: {relative_path}")
  return errors


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  errors = validate(root)
  if errors:
    for error in errors:
      print(f"error: {error}", file=sys.stderr)
    return 1
  print("asset registry check: passed")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
