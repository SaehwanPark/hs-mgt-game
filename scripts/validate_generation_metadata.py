#!/usr/bin/env python3
"""Validate the approved local-generation workflow and empty manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from capture_generation_metadata import APPROVED_MODEL_STATUS, MODEL_REVISION_PATTERN, ROOT, validate_record


WORKFLOW = ROOT / "assets" / "generation" / "generation-workflow.json"
MODELS = ROOT / "assets" / "generation" / "approved-models.json"
MANIFEST = ROOT / "assets" / "generation" / "generation-manifest.json"


def load(path: Path):
  return json.loads(path.read_text(encoding="utf-8"))


def validate() -> list[str]:
  errors: list[str] = []
  try:
    workflow = load(WORKFLOW)
    models = load(MODELS)
    manifest = load(MANIFEST)
  except (OSError, json.JSONDecodeError) as error:
    return [f"cannot read generation workflow: {error}"]
  if not isinstance(workflow, dict): return ["workflow: top-level JSON must be an object"]
  if not isinstance(models, dict): return ["models: top-level JSON must be an object"]
  if not isinstance(manifest, dict): return ["manifest: top-level JSON must be an object"]
  if workflow.get("schema_version") != "generation-workflow-v1": errors.append("workflow: unsupported schema")
  if models.get("schema_version") != "approved-generation-models-v1": errors.append("models: unsupported schema")
  if manifest.get("schema_version") != "generation-manifest-v1": errors.append("manifest: unsupported schema")
  allowed_licenses = workflow.get("allowed_licenses")
  if not isinstance(allowed_licenses, list):
    errors.append("workflow.allowed_licenses: must be a list")
    allowed_licenses = []
  model_entries = models.get("entries")
  if not isinstance(model_entries, list) or not model_entries: errors.append("models: at least one approved candidate is required")
  else:
    seen = set()
    for index, model in enumerate(model_entries):
      location = f"models.entries[{index}]"
      if not isinstance(model, dict):
        errors.append(f"{location}: entry must be an object")
        continue
      model_id = model.get("id")
      if not isinstance(model_id, str) or not model_id.strip():
        errors.append(f"{location}: missing id")
      elif model_id in seen:
        errors.append(f"{location}: duplicate id")
      else:
        seen.add(model_id)
      for field in ("id", "model_name", "model_version", "model_revision", "model_license", "model_card_url", "generation_application", "scope", "access_conditions", "review_basis", "reviewer", "review_date"):
        if not isinstance(model.get(field), str) or not model[field].strip(): errors.append(f"{location}: missing {field}")
      if model.get("approval_status") != APPROVED_MODEL_STATUS: errors.append(f"{location}: not approved for prototype use")
      if model.get("model_license") not in allowed_licenses: errors.append(f"{location}: license not allowlisted")
      if not MODEL_REVISION_PATTERN.fullmatch(str(model.get("model_revision", ""))): errors.append(f"{location}: model_revision must be a 40-character commit SHA")
  entries = manifest.get("entries")
  if not isinstance(entries, list): errors.append("manifest.entries: must be a list")
  else:
    for index, record in enumerate(entries):
      for error in validate_record(ROOT, record): errors.append(f"manifest.entries[{index}]: {error}")
  return errors


def main() -> int:
  errors = validate()
  if errors:
    for error in errors: print(f"error: {error}", file=sys.stderr)
    return 1
  print("generation workflow check: passed")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
