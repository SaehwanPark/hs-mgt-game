#!/usr/bin/env python3
"""Validate the approved local-generation workflow and empty manifest."""

from __future__ import annotations

import json
import hashlib
import struct
import sys
import datetime as dt
from pathlib import Path

from capture_generation_metadata import APPROVED_MODEL_STATUS, MODEL_REVISION_PATTERN, ROOT, approved_models, registry_entries, validate_record


WORKFLOW = ROOT / "assets" / "generation" / "generation-workflow.json"
MODELS = ROOT / "assets" / "generation" / "approved-models.json"
MANIFEST = ROOT / "assets" / "generation" / "generation-manifest.json"
PORTRAIT_SET = ROOT / "assets" / "generation" / "portrait-set.json"
PORTRAIT_PREVIEWS = ROOT / "assets" / "generation" / "portrait-previews.json"
PORTRAIT_REVIEW_QUEUE = ROOT / "assets" / "generation" / "portrait-review-queue.json"
PORTRAIT_PREVIEW_ROOT = ROOT / "assets" / "generation" / "portrait-previews"
PORTRAIT_REVIEW_FIELDS = (
  "identity_only_reviewed",
  "role_consistency_reviewed",
  "generic_fallback_reviewed",
  "small_size_reviewed",
  "grayscale_reviewed",
)
PORTRAIT_NULLABLE_PROVENANCE_FIELDS = (
  "model_id",
  "model_revision",
  "model_license",
  "model_card_url",
  "sampler",
  "release_path",
  "release_hash",
  "asset_registry_id",
)
PORTRAIT_REVIEW_QUEUE_GATES = (
  "identity_only",
  "role_consistency",
  "real_person_resemblance",
  "protected_marks_and_text",
  "artifact_quality",
  "accessible_equivalent",
  "small_size",
  "grayscale",
  "model_and_seed_provenance",
  "release_derivative",
  "registry_bridge",
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
CURRENT_PORTRAIT_ROLES = EXPECTED_PORTRAIT_ROLES - {"rival-system-executive"}


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
    if not isinstance(role.get("target_in_current_slice"), bool):
      errors.append(f"{location}: target_in_current_slice must be boolean")
  if set(role_ids) != EXPECTED_PORTRAIT_ROLES or len(role_ids) != len(EXPECTED_PORTRAIT_ROLES):
    errors.append("portrait-set.roles: must contain the exact seven unique roadmap roles")
  if sum(role.get("target_in_first_slice") is True for role in roles if isinstance(role, dict)) != 1:
    errors.append("portrait-set.roles: exactly one first-slice target is required")
  current_target_ids = {
    role.get("id")
    for role in roles
    if isinstance(role, dict)
    and role.get("target_in_current_slice") is True
    and isinstance(role.get("id"), str)
  }
  if current_target_ids != CURRENT_PORTRAIT_ROLES:
    errors.append("portrait-set.roles: current slice must target the six remaining roles")
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
  preview_role_ids = []
  source_paths = set()
  for index, entry in enumerate(entries):
    location = f"portrait-previews.entries[{index}]"
    if not isinstance(entry, dict):
      errors.append(f"{location}: entry must be an object")
      continue
    role_id = entry.get("role_id")
    if not isinstance(role_id, str) or role_id not in EXPECTED_PORTRAIT_ROLES:
      errors.append(f"{location}: unknown role_id")
    else:
      preview_role_ids.append(role_id)
    if entry.get("asset_id") != f"visual.portrait.{role_id}":
      errors.append(f"{location}: asset_id must match role_id")
    for field in ("source_output_path", "source_hash", "captured_at", "generation_date", "contributor", "generation_application", "model_identity_status", "seed_status", "sampler_status", "provenance_note", "prompt", "negative_prompt", "post_processing", "accessible_equivalent", "generic_fallback", "approval_status", "preview_status"):
      if not isinstance(entry.get(field), str) or not entry[field].strip():
        errors.append(f"{location}: missing {field}")
    source_output_path = entry.get("source_output_path")
    if isinstance(source_output_path, str):
      if Path(source_output_path).is_absolute():
        errors.append(f"{location}: source_output_path must be repository-relative")
      if isinstance(role_id, str):
        expected_path = f"assets/generation/portrait-previews/{role_id}-preview.png"
        if source_output_path != expected_path:
          errors.append(f"{location}: source_output_path must match role_id")
      if source_output_path in source_paths:
        errors.append(f"{location}: source_output_path must be unique")
      source_paths.add(source_output_path)
    source_image_references = entry.get("source_image_references")
    if not isinstance(source_image_references, list) or not all(isinstance(value, str) and value.strip() for value in source_image_references):
      errors.append(f"{location}: source_image_references must be a list of strings")
    settings = entry.get("settings")
    if not isinstance(settings, dict) or not settings:
      errors.append(f"{location}: settings must be a non-empty object")
    for field in PORTRAIT_NULLABLE_PROVENANCE_FIELDS:
      value = entry.get(field)
      if value is not None and (not isinstance(value, str) or not value.strip()):
        errors.append(f"{location}: {field} must be non-empty text or null")
    for field in ("captured_at", "generation_date"):
      try:
        dt.date.fromisoformat(str(entry.get(field)))
      except ValueError:
        errors.append(f"{location}: {field} must be an ISO date")
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
    if entry.get("release_path") is None and entry.get("release_hash") is not None:
      errors.append(f"{location}: release_hash requires release_path")
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
      for field in ("model_license", "model_card_url", "sampler"):
        if not isinstance(entry.get(field), str) or not entry[field].strip():
          errors.append(f"{location}: promoted portrait requires {field}")
      if not all(portrait_review.get(field) is True for field in PORTRAIT_REVIEW_FIELDS):
        errors.append(f"{location}: promoted portrait requires complete portrait review")
    elif entry.get("preview_status") != "unverified-preview" or entry.get("approval_status") != "pending":
      errors.append(f"{location}: unpromoted portrait must remain an unverified pending preview")
    elif any(entry.get(field) is not None for field in ("model_id", "model_revision", "model_license", "model_card_url", "sampler", "seed")):
      errors.append(f"{location}: unverified preview must keep model/license/card/sampler/seed provenance null")
    if entry.get("model_id") is not None and not isinstance(entry.get("model_id"), str):
      errors.append(f"{location}: model_id must be text or null")
    if entry.get("seed") is not None and (not isinstance(entry.get("seed"), int) or isinstance(entry.get("seed"), bool) or entry["seed"] < 0):
      errors.append(f"{location}: seed must be a non-negative integer or null")
  if set(preview_role_ids) != EXPECTED_PORTRAIT_ROLES or len(preview_role_ids) != len(EXPECTED_PORTRAIT_ROLES):
    errors.append("portrait-previews.entries: must contain exactly one preview for each canonical role")
  return errors


def validate_portrait_review_queue(portrait_set, previews, queue, registry_ids: set[str], root: Path = ROOT) -> list[str]:
  errors: list[str] = []
  if not isinstance(queue, dict):
    return ["portrait-review-queue: top-level JSON must be an object"]
  if queue.get("schema_version") != "fictional-portrait-review-queue-v1":
    errors.append("portrait-review-queue: unsupported schema")
  if queue.get("release_eligible") is not False:
    errors.append("portrait-review-queue: release_eligible must remain false")
  if queue.get("review_status") != "pending-human-review":
    errors.append("portrait-review-queue: review_status must remain pending-human-review")
  if queue.get("required_gates") != list(PORTRAIT_REVIEW_QUEUE_GATES):
    errors.append("portrait-review-queue.required_gates: must match the canonical gate list")
  entries = queue.get("entries")
  if not isinstance(entries, list) or not entries:
    errors.append("portrait-review-queue.entries: must be a non-empty list")
    entries = []
  preview_entries = previews.get("entries") if isinstance(previews, dict) else None
  if not isinstance(preview_entries, list):
    errors.append("portrait-review-queue: previews.entries must be a list")
    preview_entries = []
  previews_by_role = {
    entry.get("role_id"): entry
    for entry in preview_entries
    if isinstance(entry, dict) and isinstance(entry.get("role_id"), str)
  }
  queue_role_ids = []
  source_paths = set()
  for index, entry in enumerate(entries):
    location = f"portrait-review-queue.entries[{index}]"
    if not isinstance(entry, dict):
      errors.append(f"{location}: entry must be an object")
      continue
    role_id = entry.get("role_id")
    if not isinstance(role_id, str) or role_id not in EXPECTED_PORTRAIT_ROLES:
      errors.append(f"{location}: unknown role_id")
      preview = None
    else:
      queue_role_ids.append(role_id)
      preview = previews_by_role.get(role_id)
    if entry.get("asset_id") != f"visual.portrait.{role_id}":
      errors.append(f"{location}: asset_id must match role_id")
    for field in ("source_output_path", "source_hash", "accessible_equivalent", "generic_fallback", "decision", "approval_status", "block_reason"):
      if field not in entry or not isinstance(entry.get(field), str) or not entry[field].strip():
        errors.append(f"{location}: missing {field}")
    source_output_path = entry.get("source_output_path")
    if isinstance(source_output_path, str):
      if Path(source_output_path).is_absolute():
        errors.append(f"{location}: source_output_path must be repository-relative")
      if isinstance(role_id, str) and source_output_path != f"assets/generation/portrait-previews/{role_id}-preview.png":
        errors.append(f"{location}: source_output_path must match role_id")
      if source_output_path in source_paths:
        errors.append(f"{location}: source_output_path must be unique")
      source_paths.add(source_output_path)
      try:
        source = (root / source_output_path).resolve()
      except (OSError, TypeError):
        source = None
      if source is None or PORTRAIT_PREVIEW_ROOT.resolve() not in source.parents or not source.is_file():
        errors.append(f"{location}: source_output_path must identify an existing portrait preview")
      elif entry.get("source_hash") != sha256(source):
        errors.append(f"{location}: source_hash does not match source output")
    if isinstance(entry.get("asset_id"), str) and entry["asset_id"] in registry_ids:
      errors.append(f"{location}: review packet must remain outside the visual registry")
    if preview is None:
      errors.append(f"{location}: matching preview entry is required")
    else:
      for field in ("asset_id", "source_output_path", "source_hash", "accessible_equivalent", "generic_fallback"):
        if entry.get(field) != preview.get(field):
          errors.append(f"{location}: {field} must match portrait-previews")
      if previews.get("release_eligible") is not False:
        errors.append(f"{location}: portrait-previews release_eligible must remain false")
      if preview.get("preview_status") != "unverified-preview" or preview.get("approval_status") != "pending":
        errors.append(f"{location}: matching preview must remain unverified and pending")
      if any(preview.get(field) is not None for field in ("release_path", "release_hash", "asset_registry_id")):
        errors.append(f"{location}: matching preview release fields must remain null")
    reviewer = entry.get("reviewer")
    if not isinstance(reviewer, dict) or set(reviewer) != {"name", "type", "reviewed_at", "notes"}:
      errors.append(f"{location}: reviewer must contain name, type, reviewed_at, and notes")
    else:
      if reviewer.get("name") is not None and (not isinstance(reviewer["name"], str) or not reviewer["name"].strip()):
        errors.append(f"{location}: reviewer.name must be non-empty text or null")
      if reviewer.get("type") != "human-review-required":
        errors.append(f"{location}: reviewer.type must be human-review-required")
      if reviewer.get("reviewed_at") is not None:
        try:
          dt.date.fromisoformat(str(reviewer["reviewed_at"]))
        except ValueError:
          errors.append(f"{location}: reviewer.reviewed_at must be an ISO date or null")
      if reviewer.get("notes") is not None and (not isinstance(reviewer["notes"], str) or not reviewer["notes"].strip()):
        errors.append(f"{location}: reviewer.notes must be non-empty text or null")
    gates = entry.get("gates")
    if not isinstance(gates, dict) or set(gates) != set(PORTRAIT_REVIEW_QUEUE_GATES):
      errors.append(f"{location}: gates must contain the canonical review gates")
      gates = {}
    else:
      for gate in PORTRAIT_REVIEW_QUEUE_GATES:
        if not isinstance(gates.get(gate), bool):
          errors.append(f"{location}: gates.{gate} must be boolean")
    if entry.get("decision") != "pending" or entry.get("approval_status") != "pending":
      errors.append(f"{location}: review packet must remain pending")
    for field in ("release_path", "release_hash", "asset_registry_id"):
      if field not in entry:
        errors.append(f"{location}: missing {field}")
      elif entry[field] is not None:
        errors.append(f"{location}: {field} must remain null before human approval")
    if any(gates.get(gate) is True for gate in PORTRAIT_REVIEW_QUEUE_GATES) and (
      not isinstance(reviewer, dict) or not isinstance(reviewer.get("name"), str) or not reviewer.get("name").strip() or reviewer.get("reviewed_at") is None
    ):
      errors.append(f"{location}: completed review gates require a named human reviewer and date")
  if set(queue_role_ids) != EXPECTED_PORTRAIT_ROLES or len(queue_role_ids) != len(EXPECTED_PORTRAIT_ROLES):
    errors.append("portrait-review-queue.entries: must contain exactly one packet for each canonical role")
  return errors


def validate() -> list[str]:
  errors: list[str] = []
  try:
    workflow = load(WORKFLOW)
    models = load(MODELS)
    manifest = load(MANIFEST)
    portrait_set = load(PORTRAIT_SET)
    portrait_previews = load(PORTRAIT_PREVIEWS)
    portrait_review_queue = load(PORTRAIT_REVIEW_QUEUE)
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
  errors.extend(validate_portrait_review_queue(portrait_set, portrait_previews, portrait_review_queue, registry_ids))
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
