#!/usr/bin/env python3
"""Capture and validate provenance metadata for future local generation outputs."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORDS_ROOT = ROOT / "assets" / "generation" / "records"
WORKFLOW_PATH = ROOT / "assets" / "generation" / "generation-workflow.json"
APPROVED_MODELS_PATH = ROOT / "assets" / "generation" / "approved-models.json"
REGISTRY_PATHS = (
  ROOT / "assets" / "registry" / "visual-assets.json",
  ROOT / "assets" / "registry" / "audio-assets.json",
)
APPROVED_MODEL_STATUS = "approved-for-local-prototype"
MODEL_REVISION_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def load_json(path: Path):
  return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
  digest = hashlib.sha256()
  with path.open("rb") as stream:
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
      digest.update(chunk)
  return f"sha256:{digest.hexdigest()}"


def repo_path(root: Path, value, field: str, required: bool = True) -> tuple[Path | None, list[str]]:
  if value is None and not required:
    return None, []
  if not isinstance(value, str) or not value.strip():
    return None, [f"{field}: required repository-relative path"]
  candidate = Path(value)
  if candidate.is_absolute():
    return None, [f"{field}: absolute paths are not allowed"]
  resolved = (root / candidate).resolve()
  if root.resolve() not in resolved.parents:
    return None, [f"{field}: path escapes repository root"]
  return resolved, []


def scalar_text(value) -> bool:
  return isinstance(value, str) and bool(value.strip())


def approved_models() -> dict[str, dict]:
  document = load_json(APPROVED_MODELS_PATH)
  if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
    return {}
  return {entry.get("id"): entry for entry in document["entries"] if isinstance(entry, dict)}


def registry_entries() -> dict[str, dict]:
  result = {}
  for path in REGISTRY_PATHS:
    document = load_json(path)
    if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
      continue
    for entry in document["entries"]:
      if isinstance(entry, dict) and entry.get("id"):
        result[entry["id"]] = entry
  return result


def validate_record(root: Path, record: dict, *, check_source: bool = True) -> list[str]:
  if not isinstance(record, dict):
    return ["record: must be a JSON object"]
  errors: list[str] = []
  try:
    workflow = load_json(WORKFLOW_PATH)
  except (OSError, json.JSONDecodeError) as error:
    return [f"workflow: cannot read configuration ({error})"]
  if not isinstance(workflow, dict):
    return ["workflow: top-level JSON must be an object"]
  required = workflow.get("required_metadata_fields")
  if not isinstance(required, list):
    return ["workflow.required_metadata_fields: must be a list"]
  for field in required:
    if field not in record:
      errors.append(f"missing field: {field}")
  if record.get("schema_version") != "generation-record-v1":
    errors.append("schema_version: unsupported generation-record schema")
  for field in ("asset_id", "asset_type", "semantic_role", "model_id", "model_name", "model_version", "model_revision", "model_license", "model_card_url", "generation_application", "prompt", "negative_prompt", "sampler", "generation_date", "contributor", "post_processing", "accessible_equivalent"):
    if not scalar_text(record.get(field)):
      errors.append(f"{field}: required non-empty text")
  if record.get("asset_type") not in {"visual", "audio"}:
    errors.append("asset_type: must be visual or audio")
  if not isinstance(record.get("seed"), int) or isinstance(record.get("seed"), bool) or record.get("seed") < 0:
    errors.append("seed: must be a non-negative integer")
  settings = record.get("settings")
  if not isinstance(settings, dict) or not settings:
    errors.append("settings: must be a non-empty object")
  dimensions = record.get("dimensions")
  if not isinstance(dimensions, dict) or not all(isinstance(dimensions.get(key), int) and not isinstance(dimensions[key], bool) and dimensions[key] > 0 for key in ("width", "height")):
    errors.append("dimensions: width and height must be positive integers")
  references = record.get("source_image_references")
  if not isinstance(references, list) or not all(isinstance(value, str) and value.strip() for value in references):
    errors.append("source_image_references: must be a list of non-empty strings")
  try:
    dt.date.fromisoformat(str(record.get("generation_date")))
  except ValueError:
    errors.append("generation_date: must be an ISO date")
  try:
    dt.date.fromisoformat(str(record.get("captured_at")))
  except ValueError:
    errors.append("captured_at: must be an ISO date")

  try:
    models = approved_models()
    entries = registry_entries()
  except (OSError, json.JSONDecodeError) as error:
    return [f"provenance registry: cannot read configuration ({error})"]
  model = models.get(record.get("model_id"))
  if not model:
    errors.append("model_id: not present in approved model registry")
  else:
    if record.get("model_license") != model.get("model_license"):
      errors.append("model_license: does not match approved model registry")
    if record.get("model_name") != model.get("model_name"):
      errors.append("model_name: does not match approved model registry")
    if record.get("model_version") != model.get("model_version"):
      errors.append("model_version: does not match approved model registry")
    if record.get("model_revision") != model.get("model_revision"):
      errors.append("model_revision: does not match approved model registry")
    if not MODEL_REVISION_PATTERN.fullmatch(str(model.get("model_revision", ""))):
      errors.append("model_revision: approved model registry must use a 40-character commit SHA")
    if record.get("model_card_url") != model.get("model_card_url"):
      errors.append("model_card_url: does not match approved model registry")
    if model.get("approval_status") != APPROVED_MODEL_STATUS:
      errors.append("model_id: model is not approved for local prototype use")
  allowed_licenses = workflow.get("allowed_licenses")
  if not isinstance(allowed_licenses, list):
    errors.append("workflow.allowed_licenses: must be a list")
    allowed_licenses = []
  if record.get("model_license") not in allowed_licenses:
    errors.append("model_license: not allowlisted")

  human_review = record.get("human_review")
  required_review = workflow.get("required_human_review_fields")
  if not isinstance(required_review, list):
    errors.append("workflow.required_human_review_fields: must be a list")
    required_review = []
  if not isinstance(human_review, dict):
    errors.append("human_review: required object")
  else:
    for field in required_review:
      if not isinstance(human_review.get(field), bool):
        errors.append(f"human_review.{field}: must be boolean")

  source, source_errors = repo_path(root, record.get("source_output_path"), "source_output_path")
  errors.extend(source_errors)
  if source is not None and not source.is_file():
    errors.append(f"source_output_path: file does not exist: {record.get('source_output_path')}")
  if source is not None and source.is_file() and check_source:
    actual = sha256(source)
    if record.get("source_hash") != actual:
      errors.append("source_hash: does not match source output")

  release, release_errors = repo_path(root, record.get("release_output_path"), "release_output_path", required=False)
  errors.extend(release_errors)
  if release is not None:
    if record.get("approval_status") != "approved":
      errors.append("release_output_path: requires approval_status approved")
    if not release.is_file():
      errors.append(f"release_output_path: file does not exist: {record.get('release_output_path')}")
    elif check_source and record.get("release_hash") != sha256(release):
      errors.append("release_hash: does not match release output")
  elif record.get("release_hash") is not None:
    errors.append("release_hash: must be null without release_output_path")

  status = record.get("approval_status")
  approval_statuses = workflow.get("approval_statuses")
  if not isinstance(approval_statuses, list):
    errors.append("workflow.approval_statuses: must be a list")
    approval_statuses = []
  if status not in approval_statuses:
    errors.append("approval_status: invalid")
  all_reviewed = isinstance(human_review, dict) and all(human_review.get(field) is True for field in required_review)
  if status == "approved" or release is not None:
    if not all_reviewed:
      errors.append("approval/release: every human review field must be true")
    if not scalar_text(record.get("asset_registry_id")):
      errors.append("asset_registry_id: required for approved/release record")
  registry_id = record.get("asset_registry_id")
  if registry_id is not None:
    registry_entry = entries.get(registry_id)
    if not registry_entry:
      errors.append("asset_registry_id: not found in visual/audio asset registries")
    elif registry_id != record.get("asset_id"):
      errors.append("asset_registry_id: must match asset_id")
    elif registry_entry.get("asset_type") != record.get("asset_type"):
      errors.append("asset_registry_id: asset type does not match captured record")
    elif (record.get("approval_status") == "approved" or release is not None) and registry_entry.get("approval_status") != "approved":
      errors.append("asset_registry_id: linked release entry must be approved")
    else:
      registry_pairs = (
        ("source_output_path", "source_path"),
        ("source_hash", "original_hash"),
        ("release_output_path", "release_path"),
        ("release_hash", "release_hash"),
      )
      for record_field, registry_field in registry_pairs:
        if record.get(record_field) != registry_entry.get(registry_field):
          errors.append(f"asset_registry_id: {record_field} does not match linked registry {registry_field}")
  return errors


def capture(request_path: Path, output_path: Path) -> int:
  try:
    request = load_json(request_path)
  except (OSError, json.JSONDecodeError) as error:
    print(f"error: cannot read request ({error})", file=sys.stderr)
    return 1
  if not isinstance(request, dict):
    print("error: request must be a JSON object", file=sys.stderr)
    return 1
  output_value = output_path.as_posix()
  if output_path.is_absolute():
    try:
      output_value = output_path.relative_to(ROOT).as_posix()
    except ValueError:
      pass
  output, output_errors = repo_path(ROOT, output_value, "output_path")
  if output_errors or output is None:
    for error in output_errors or ["output_path: must be inside repository root"]:
      print(f"error: {error}", file=sys.stderr)
    return 1
  if RECORDS_ROOT.resolve() not in output.parents:
    print("error: output_path: must be inside assets/generation/records", file=sys.stderr)
    return 1
  if output.exists():
    print("error: output_path: refusing to overwrite an existing record", file=sys.stderr)
    return 1
  record = dict(request)
  record["schema_version"] = "generation-record-v1"
  record["captured_at"] = dt.date.today().isoformat()
  source, source_errors = repo_path(ROOT, record.get("source_output_path"), "source_output_path")
  if source_errors or source is None or not source.is_file():
    for error in source_errors or ["source_output_path: source file must exist before capture"]:
      print(f"error: {error}", file=sys.stderr)
    return 1
  if output == source:
    print("error: output_path must not overwrite source_output_path", file=sys.stderr)
    return 1
  record["source_output_path"] = source.relative_to(ROOT).as_posix()
  record["source_hash"] = sha256(source)
  release_value = record.get("release_output_path")
  release, release_errors = repo_path(ROOT, release_value, "release_output_path", required=False)
  if release_errors:
    for error in release_errors:
      print(f"error: {error}", file=sys.stderr)
    return 1
  if release is not None:
    if output == release:
      print("error: output_path must not overwrite release_output_path", file=sys.stderr)
      return 1
    if not release.is_file():
      print("error: release_output_path: file must exist before capture", file=sys.stderr)
      return 1
    record["release_output_path"] = release.relative_to(ROOT).as_posix()
    record["release_hash"] = sha256(release)
  else:
    record["release_output_path"] = None
    record["release_hash"] = None
  errors = validate_record(ROOT, record)
  if errors:
    for error in errors:
      print(f"error: {error}", file=sys.stderr)
    return 1
  output.parent.mkdir(parents=True, exist_ok=True)
  output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
  print(f"generation metadata captured: {output}")
  return 0


def validate_record_file(record_path: Path) -> int:
  try:
    record = load_json(record_path)
  except (OSError, json.JSONDecodeError) as error:
    print(f"error: cannot read record ({error})", file=sys.stderr)
    return 1
  errors = validate_record(ROOT, record)
  if errors:
    for error in errors:
      print(f"error: {error}", file=sys.stderr)
    return 1
  print("generation metadata check: passed")
  return 0


def main() -> int:
  parser = argparse.ArgumentParser(description=__doc__)
  subparsers = parser.add_subparsers(dest="command", required=True)
  capture_parser = subparsers.add_parser("capture", help="capture hashes and normalized metadata")
  capture_parser.add_argument("--request", type=Path, required=True)
  capture_parser.add_argument("--output", type=Path, required=True)
  validate_parser = subparsers.add_parser("validate", help="validate one captured record")
  validate_parser.add_argument("--record", type=Path, required=True)
  args = parser.parse_args()
  if args.command == "capture":
    return capture(args.request, args.output)
  return validate_record_file(args.record)


if __name__ == "__main__":
  raise SystemExit(main())
