#!/usr/bin/env python3
"""Generate and verify a deterministic manifest for approved release assets."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


REGISTRIES = (
  Path("assets/registry/visual-assets.json"),
  Path("assets/registry/audio-assets.json"),
)
MANIFEST_PATH = Path("assets/ASSET_RELEASE_MANIFEST.json")
SCHEMA_VERSION = "asset-release-manifest-v1"
RELEASE_PREFIX = "assets/release/"


def _sha256(path: Path) -> str:
  digest = hashlib.sha256()
  with path.open("rb") as stream:
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
      digest.update(chunk)
  return f"sha256:{digest.hexdigest()}"


def _canonical_bytes(document: dict) -> bytes:
  return json.dumps(document, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _safe_path(root: Path, relative_path: str) -> Path:
  resolved_root = root.resolve()
  resolved = (root / relative_path).resolve()
  if resolved_root not in resolved.parents and resolved != resolved_root:
    raise ValueError("path escapes repository root")
  return resolved


def _contains_symlink(root: Path, path: Path) -> bool:
  try:
    relative = path.relative_to(root)
  except ValueError:
    return False
  current = root
  for part in relative.parts:
    current /= part
    if current.is_symlink():
      return True
  return False


def _release_path(root: Path, release_path: str) -> Path:
  if not release_path.startswith(RELEASE_PREFIX):
    raise ValueError(f"release_path must be under {RELEASE_PREFIX}")
  candidate = root / release_path
  if _contains_symlink(root, candidate):
    raise ValueError("release_path cannot contain symlinks")
  resolved = _safe_path(root, release_path)
  if not resolved.relative_to(root.resolve()).as_posix().startswith(RELEASE_PREFIX):
    raise ValueError(f"resolved release_path must remain under {RELEASE_PREFIX}")
  return resolved


def _release_records(root: Path) -> tuple[list[dict], list[str]]:
  records_by_path: dict[str, dict] = {}
  errors: list[str] = []
  for registry in REGISTRIES:
    path = root / registry
    try:
      document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
      errors.append(f"{registry.as_posix()}: cannot read JSON ({error})")
      continue
    if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
      errors.append(f"{registry.as_posix()}: entries must be a list")
      continue
    for index, entry in enumerate(document["entries"]):
      location = f"{registry.as_posix()}:entries[{index}]"
      if not isinstance(entry, dict):
        errors.append(f"{location}: entry must be an object")
        continue
      release_path = entry.get("release_path")
      if release_path is None:
        continue
      if not isinstance(release_path, str) or not release_path:
        errors.append(f"{location}: release_path must be a non-empty string or null")
        continue
      if entry.get("approval_status") != "approved":
        errors.append(f"{location}: release asset must be approved")
      try:
        release_file = _release_path(root, release_path)
      except ValueError as error:
        errors.append(f"{location}: invalid release_path ({error})")
        continue
      if not release_file.is_file():
        errors.append(f"{location}: release_path does not exist: {release_path}")
        continue
      actual_hash = _sha256(release_file)
      if entry.get("release_hash") != actual_hash:
        errors.append(f"{location}: release_hash does not match {release_path}")
      record = {
        "path": release_path,
        "bytes": release_file.stat().st_size,
        "sha256": actual_hash,
      }
      previous = records_by_path.get(release_path)
      if previous is not None and previous != record:
        errors.append(f"{location}: release_path has conflicting manifest records: {release_path}")
      records_by_path[release_path] = record
  return [records_by_path[path] for path in sorted(records_by_path)], errors


def render_manifest(root: Path) -> tuple[str | None, list[str]]:
  records, errors = _release_records(root)
  if errors:
    return None, errors
  payload = {"schema_version": SCHEMA_VERSION, "files": records}
  digest = hashlib.sha256(_canonical_bytes(payload)).hexdigest()
  document = {**payload, "manifest_sha256": f"sha256:{digest}"}
  return json.dumps(document, indent=2) + "\n", []


def check_manifest(root: Path, manifest_path: Path | None = None) -> list[str]:
  output, errors = render_manifest(root)
  if errors:
    return errors
  target = manifest_path or root / MANIFEST_PATH
  try:
    current = target.read_text(encoding="utf-8")
  except OSError as error:
    return [f"{target.relative_to(root)}: cannot read manifest ({error})"]
  if current != output:
    return [f"{target.relative_to(root)}: generated manifest is stale"]
  return []


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  output, errors = render_manifest(root)
  if errors:
    for error in errors:
      print(f"error: {error}", file=sys.stderr)
    return 1
  target = root / MANIFEST_PATH
  if "--check" in sys.argv[1:]:
    errors = check_manifest(root, target)
    if errors:
      for error in errors:
        print(f"error: {error}", file=sys.stderr)
      return 1
    print(f"asset release manifest check: passed ({len(json.loads(output)['files'])} files)")
    return 0
  target.write_text(output, encoding="utf-8")
  print(f"asset release manifest: wrote {target.relative_to(root)}")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
