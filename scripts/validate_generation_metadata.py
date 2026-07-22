#!/usr/bin/env python3
"""Validate the approved local-generation workflow and empty manifest."""

from __future__ import annotations

import json
import hashlib
import struct
import sys
from pathlib import Path

from capture_generation_metadata import APPROVED_MODEL_STATUS, MODEL_REVISION_PATTERN, ROOT, approved_models, registry_entries, validate_record


WORKFLOW = ROOT / "assets" / "generation" / "generation-workflow.json"
MODELS = ROOT / "assets" / "generation" / "approved-models.json"
MANIFEST = ROOT / "assets" / "generation" / "generation-manifest.json"
PORTRAIT_SET = ROOT / "assets" / "generation" / "portrait-set.json"
PORTRAIT_PREVIEWS = ROOT / "assets" / "generation" / "portrait-previews.json"
PORTRAIT_PREVIEW_ROOT = ROOT / "assets" / "generation" / "portrait-previews"
PORTRAIT_REVIEW_FIELDS = (
  "identity_only_reviewed",
  "role_consistency_reviewed",
  "generic_fallback_reviewed",
  "small_size_reviewed",
  "grayscale_reviewed",
)
EXPECTED_PORTRAIT_ROLES = {
  "rival-system-executive",
  "payer-negotiator",
  "regulator",
  "labor-representative",
  "community-leader",
  "board-chair",
  "affiliation-partner-executive",
}


def load(path: Path):
  return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
  return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def png_dimensions(path: Path) -> tuple[int, int] | None:
  signature = b"\x89PNG\r\n\x1a\n"
  data = path.read_bytes()
  if len(data) < 24 or data[:8] != signature or data[12:16] != b"IHDR":
    return None
  return struct.unpack(">II", data[16:24])


def validate_portrait_documents(portrait_set, previews, manifest, registry_ids: set[str], root: Path = ROOT) -> list[str]:
  errors: list[str] = []
  if not isinstance(portrait_set, dict):
    return ["portrait-set: top-level JSON must be an object"]
  if not isinstance(previews, dict):
    return ["portrait-previews: top-level JSON must be an object"]
  if not isinstance(manifest, dict):
    return ["manifest: top-level JSON must be an object"]
  if portrait_set.get("schema_version") != "fictional-portrait-set-v1":
    errors.append("portrait-set: unsupported schema")
  if previews.get("schema_version") != "fictional-portrait-preview-v1":
    errors.append("portrait-previews: unsupported schema")
  if previews.get("release_eligible") is not False:
    errors.append("portrait-previews: release_eligible must remain false")

  roles = portrait_set.get("roles")
  if not isinstance(roles, list):
    errors.append("portrait-set.roles: must be a list")
    roles = []
  role_ids = []
  for index, role in enumerate(roles):
    location = f"portrait-set.roles[{index}]"
    if not isinstance(role, dict):
      errors.append(f"{location}: entry must be an object")
      continue
    role_id = role.get("id")
    role_ids.append(role_id if isinstance(role_id, str) else f"__invalid_role_{index}")
    for field in ("id", "label", "family", "alt_text_guidance", "fallback"):
      if not isinstance(role.get(field), str) or not role[field].strip():
        errors.append(f"{location}: missing {field}")
    if not isinstance(role.get("target_in_first_slice"), bool):
      errors.append(f"{location}: target_in_first_slice must be boolean")
  if set(role_ids) != EXPECTED_PORTRAIT_ROLES or len(role_ids) != len(EXPECTED_PORTRAIT_ROLES):
    errors.append("portrait-set.roles: must contain the exact seven unique roadmap roles")
  if sum(role.get("target_in_first_slice") is True for role in roles if isinstance(role, dict)) != 1:
    errors.append("portrait-set.roles: exactly one first-slice target is required")
  shared_style = portrait_set.get("shared_style")
  if not isinstance(shared_style, dict):
    errors.append("portrait-set.shared_style: must be an object")
  else:
    for field in ("medium", "composition", "background", "lighting", "small_size_target", "grayscale_target", "fallback"):
      if not isinstance(shared_style.get(field), str) or not shared_style[field].strip():
        errors.append(f"portrait-set.shared_style: missing {field}")
    if not isinstance(shared_style.get("palette"), list) or not shared_style["palette"]:
      errors.append("portrait-set.shared_style.palette: must be a non-empty list")
  prohibited = portrait_set.get("prohibited_content")
  if not isinstance(prohibited, list) or not all(isinstance(item, str) and item.strip() for item in prohibited):
    errors.append("portrait-set.prohibited_content: must be a non-empty list of strings")
  review_requirements = portrait_set.get("review_requirements")
  if not isinstance(review_requirements, list) or not all(isinstance(item, str) and item.strip() for item in review_requirements):
    errors.append("portrait-set.review_requirements: must be a non-empty list of strings")

  entries = previews.get("entries")
  if not isinstance(entries, list) or not entries:
    errors.append("portrait-previews.entries: must be a non-empty list")
    entries = []
  manifest_entries = manifest.get("entries")
  if not isinstance(manifest_entries, list):
    errors.append("manifest.entries: must be a list")
    manifest_entries = []
  manifest_ids = {entry.get("asset_id") for entry in manifest_entries if isinstance(entry, dict) and isinstance(entry.get("asset_id"), str)}
  approved_model_entries = approved_models()
  for index, entry in enumerate(entries):
    location = f"portrait-previews.entries[{index}]"
    if not isinstance(entry, dict):
      errors.append(f"{location}: entry must be an object")
      continue
    role_id = entry.get("role_id")
    if not isinstance(role_id, str) or role_id not in EXPECTED_PORTRAIT_ROLES:
      errors.append(f"{location}: unknown role_id")
    if entry.get("asset_id") != f"visual.portrait.{role_id}":
      errors.append(f"{location}: asset_id must match role_id")
    for field in ("source_output_path", "source_hash", "captured_at", "contributor", "generation_application", "model_identity_status", "seed_status", "provenance_note", "prompt", "negative_prompt", "post_processing", "accessible_equivalent", "generic_fallback", "approval_status", "preview_status"):
      if not isinstance(entry.get(field), str) or not entry[field].strip():
        errors.append(f"{location}: missing {field}")
    try:
      source = (root / entry.get("source_output_path", "")).resolve()
    except (OSError, TypeError):
      source = None
    if source is None or PORTRAIT_PREVIEW_ROOT.resolve() not in source.parents:
      errors.append(f"{location}: source_output_path must stay under portrait-previews")
    elif not source.is_file():
      errors.append(f"{location}: source_output_path does not exist")
    else:
      if entry.get("source_hash") != sha256(source):
        errors.append(f"{location}: source_hash does not match source output")
      dimensions = png_dimensions(source)
      declared_dimensions = entry.get("dimensions")
      if dimensions is None:
        errors.append(f"{location}: source output is not a PNG")
      elif not isinstance(declared_dimensions, dict) or tuple(declared_dimensions.get(key) for key in ("width", "height")) != dimensions:
        errors.append(f"{location}: dimensions do not match PNG source")
    if isinstance(entry.get("asset_id"), str) and (entry["asset_id"] in manifest_ids or entry["asset_id"] in registry_ids):
      errors.append(f"{location}: preview asset must remain outside manifest and visual registry")
    if previews.get("release_eligible") is False and (entry.get("release_path") is not None or entry.get("asset_registry_id") is not None):
      errors.append(f"{location}: unverified preview cannot carry release_path or asset_registry_id")
    human_review = entry.get("human_review")
    if not isinstance(human_review, dict):
      errors.append(f"{location}: human_review must be an object")
    else:
      for field in ("real_person_resemblance_reviewed", "logo_trademark_reviewed", "clinical_plausibility_reviewed", "accessibility_equivalent_written", "artifact_quality_reviewed", "source_output_preserved", "release_derivative_reviewed"):
        if not isinstance(human_review.get(field), bool):
          errors.append(f"{location}: human_review.{field} must be boolean")
    portrait_review = entry.get("portrait_review")
    if not isinstance(portrait_review, dict):
      errors.append(f"{location}: portrait_review must be an object")
      portrait_review = {}
    for field in PORTRAIT_REVIEW_FIELDS:
      if not isinstance(portrait_review.get(field), bool):
        errors.append(f"{location}: portrait_review.{field} must be boolean")
    promoted = entry.get("preview_status") == "approved" or entry.get("release_path") is not None or entry.get("asset_registry_id") is not None
    if promoted:
      if not isinstance(entry.get("model_id"), str) or not entry["model_id"].strip():
        errors.append(f"{location}: promoted portrait requires approved model_id")
      elif entry["model_id"] not in approved_model_entries or approved_model_entries[entry["model_id"]].get("approval_status") != APPROVED_MODEL_STATUS:
        errors.append(f"{location}: promoted portrait model_id is not approved")
      if not isinstance(entry.get("model_revision"), str) or not entry["model_revision"].strip():
        errors.append(f"{location}: promoted portrait requires model_revision")
      elif entry["model_id"] in approved_model_entries and entry["model_revision"] != approved_model_entries[entry["model_id"]].get("model_revision"):
        errors.append(f"{location}: promoted portrait model_revision does not match approved model")
      if not isinstance(entry.get("seed"), int) or isinstance(entry.get("seed"), bool) or entry["seed"] < 0:
        errors.append(f"{location}: promoted portrait requires non-negative seed")
      if not all(portrait_review.get(field) is True for field in PORTRAIT_REVIEW_FIELDS):
        errors.append(f"{location}: promoted portrait requires complete portrait review")
    elif entry.get("preview_status") != "unverified-preview" or entry.get("approval_status") != "pending":
      errors.append(f"{location}: unpromoted portrait must remain an unverified pending preview")
    if entry.get("model_id") is not None and not isinstance(entry.get("model_id"), str):
      errors.append(f"{location}: model_id must be text or null")
    if entry.get("seed") is not None and (not isinstance(entry.get("seed"), int) or isinstance(entry.get("seed"), bool) or entry["seed"] < 0):
      errors.append(f"{location}: seed must be a non-negative integer or null")
  return errors


def validate() -> list[str]:
  errors: list[str] = []
  try:
    workflow = load(WORKFLOW)
    models = load(MODELS)
    manifest = load(MANIFEST)
    portrait_set = load(PORTRAIT_SET)
    portrait_previews = load(PORTRAIT_PREVIEWS)
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
  try:
    registry_ids = set(registry_entries())
  except (OSError, json.JSONDecodeError) as error:
    errors.append(f"portrait registry: cannot read asset registries ({error})")
    registry_ids = set()
  errors.extend(validate_portrait_documents(portrait_set, portrait_previews, manifest, registry_ids))
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
