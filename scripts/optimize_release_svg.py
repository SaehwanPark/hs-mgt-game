#!/usr/bin/env python3
"""Normalize tracked release SVG formatting without changing SVG semantics."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


RELEASE_ROOT = Path("assets/release/visual/svg")
VISUAL_REGISTRY = Path("assets/registry/visual-assets.json")
REPORT_SCHEMA_VERSION = "svg-optimization-report-v1"
TAG_WHITESPACE = re.compile(r">\s+<")


def normalize_svg(document: str) -> str:
  normalized = document.lstrip("\ufeff").strip()
  normalized = TAG_WHITESPACE.sub("><", normalized)
  return f"{normalized}\n"


def _semantic_projection(document: str) -> tuple:
  root = ET.fromstring(document)

  def project(element: ET.Element) -> tuple:
    tag = element.tag.rsplit("}", 1)[-1]
    attributes = tuple(sorted(element.attrib.items()))
    text = (element.text or "").strip()
    return (tag, attributes, text, tuple(project(child) for child in element))

  return project(root)


def _sha256(path: Path) -> str:
  digest = hashlib.sha256(path.read_bytes()).hexdigest()
  return f"sha256:{digest}"


def _release_files(root: Path) -> list[Path]:
  release_root = root / RELEASE_ROOT
  return sorted(path for path in release_root.glob("*.svg") if path.is_file())


def _manifest_module():
  module_path = Path(__file__).with_name("verify_asset_release.py")
  spec = importlib.util.spec_from_file_location("verify_asset_release", module_path)
  if spec is None or spec.loader is None:
    raise RuntimeError("could not load release manifest helper")
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def _hash_alignment_errors(root: Path) -> list[str]:
  registry_path = root / VISUAL_REGISTRY
  try:
    document = json.loads(registry_path.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    return [f"cannot read {VISUAL_REGISTRY}: {error}"]
  if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
    return [f"{VISUAL_REGISTRY}: entries must be a list"]
  errors = []
  for index, entry in enumerate(document.get("entries", [])):
    if not isinstance(entry, dict) or entry.get("release_path") is None:
      continue
    release_path = entry["release_path"]
    if not isinstance(release_path, str):
      errors.append(f"visual-assets.json:entries[{index}] release_path must be a string")
      continue
    path = root / release_path
    if not path.is_file():
      errors.append(f"visual-assets.json:entries[{index}] missing {release_path}")
      continue
    if entry.get("release_hash") != _sha256(path):
      errors.append(f"visual-assets.json:entries[{index}] stale hash for {release_path}")
  return errors


def build_report(root: Path) -> dict:
  files = _release_files(root)
  errors = []
  records = []
  for path in files:
    relative = path.relative_to(root).as_posix()
    before = path.read_text(encoding="utf-8")
    optimized = normalize_svg(before)
    try:
      before_projection = _semantic_projection(before)
      after_projection = _semantic_projection(optimized)
    except ET.ParseError as error:
      errors.append(f"{relative}: malformed SVG/XML ({error})")
      before_projection = after_projection = None
    if before_projection != after_projection:
      errors.append(f"{relative}: semantic projection changed")
    if before != optimized:
      errors.append(f"{relative}: release SVG is not normalized")
    if normalize_svg(optimized) != optimized:
      errors.append(f"{relative}: normalization is not idempotent")
    records.append({
      "path": relative,
      "before_bytes": len(before.encode("utf-8")),
      "after_bytes": len(optimized.encode("utf-8")),
      "bytes_saved": len(before.encode("utf-8")) - len(optimized.encode("utf-8")),
      "status": "pass" if before == optimized and before_projection == after_projection else "fail",
    })
  if not files:
    errors.append(f"no release SVGs found under {RELEASE_ROOT}")
  errors.extend(_hash_alignment_errors(root))
  try:
    errors.extend(_manifest_module().check_manifest(root))
  except (OSError, RuntimeError) as error:
    errors.append(f"could not check release manifest: {error}")
  before_total = sum(record["before_bytes"] for record in records)
  after_total = sum(record["after_bytes"] for record in records)
  return {
    "schema_version": REPORT_SCHEMA_VERSION,
    "scope": RELEASE_ROOT.as_posix() + "/*.svg",
    "file_count": len(records),
    "before_total_bytes": before_total,
    "after_total_bytes": after_total,
    "bytes_saved": before_total - after_total,
    "status": "pass" if not errors else "fail",
    "errors": errors,
    "files": records,
  }


def _update_registry(root: Path) -> None:
  path = root / VISUAL_REGISTRY
  document = json.loads(path.read_text(encoding="utf-8"))
  for entry in document["entries"]:
    release_path = entry.get("release_path")
    if release_path and release_path.startswith(RELEASE_ROOT.as_posix()):
      entry["release_hash"] = _sha256(root / release_path)
  path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def _write_manifest(root: Path) -> None:
  module = _manifest_module()
  output, errors = module.render_manifest(root)
  if errors or output is None:
    raise RuntimeError("; ".join(errors))
  (root / module.MANIFEST_PATH).write_text(output, encoding="utf-8")


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  write = "--write" in sys.argv[1:]
  if write:
    initial = build_report(root)
    if any("malformed" in error or "semantic" in error for error in initial["errors"]):
      print(json.dumps(initial, indent=2, sort_keys=True))
      return 1
    for path in _release_files(root):
      path.write_text(normalize_svg(path.read_text(encoding="utf-8")), encoding="utf-8")
    _update_registry(root)
    _write_manifest(root)
  report = build_report(root)
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  raise SystemExit(main())
