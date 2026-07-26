#!/usr/bin/env python3
"""Audit the documented browser support boundary for the live GUI."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


POLICY_PATH = "assets/browser-compatibility-policy.json"
REPORT_SCHEMA_VERSION = "browser-compatibility-report-v1"
REQUIRED_FIELDS = (
  "schema_version",
  "status",
  "surface",
  "entrypoint",
  "supported_targets",
  "not_certified_targets",
  "capabilities",
  "boundary_checks",
  "evidence_limits",
)
ENGINE_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")


def _load_checker(root: Path, filename: str, module_name: str):
  path = root / "scripts" / filename
  spec = importlib.util.spec_from_file_location(module_name, path)
  if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load {filename}")
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def _resolve(root: Path, relative: str) -> Path:
  candidate = Path(relative)
  if candidate.is_absolute():
    raise ValueError("path must be relative to repository root")
  resolved = (root / candidate).resolve()
  root_path = root.resolve()
  if resolved != root_path and root_path not in resolved.parents:
    raise ValueError("path escapes repository root")
  return resolved


def validate_definition(root: Path, document: object) -> list[str]:
  if not isinstance(document, dict):
    return ["browser compatibility policy document must be an object"]
  errors = []
  for field in REQUIRED_FIELDS:
    if field not in document:
      errors.append(f"missing field {field!r}")
  if document.get("schema_version") != "browser-compatibility-v1":
    errors.append("unsupported browser compatibility schema_version")
  if document.get("status") != "completed-technical-matrix":
    errors.append("status must record the completed technical matrix")
  entrypoint = document.get("entrypoint")
  if not isinstance(entrypoint, str) or not entrypoint.strip():
    errors.append("entrypoint must be a non-empty path")
  else:
    try:
      if not _resolve(root, entrypoint).is_file():
        errors.append(f"entrypoint does not exist: {entrypoint}")
    except ValueError as error:
      errors.append(f"entrypoint is invalid: {error}")

  capabilities = document.get("capabilities")
  capability_ids = set()
  if not isinstance(capabilities, list) or not capabilities:
    errors.append("capabilities must be a non-empty list")
    capabilities = []
  for capability in capabilities:
    if not isinstance(capability, dict):
      errors.append("capability entries must be objects")
      continue
    capability_id = capability.get("id")
    if not isinstance(capability_id, str) or not ENGINE_ID_PATTERN.fullmatch(capability_id):
      errors.append("capability IDs must be lowercase kebab-case")
    elif capability_id in capability_ids:
      errors.append(f"duplicate capability ID: {capability_id}")
    else:
      capability_ids.add(capability_id)
    if not isinstance(capability.get("required"), bool):
      errors.append(f"capability {capability_id!r} has invalid required")
    for field in ("source", "fallback"):
      if not isinstance(capability.get(field), str) or not capability[field].strip():
        errors.append(f"capability {capability_id!r} has invalid {field}")

  supported = document.get("supported_targets")
  supported_ids = set()
  if not isinstance(supported, list) or not supported:
    errors.append("supported_targets must be a non-empty list")
    supported = []
  for target in supported:
    if not isinstance(target, dict):
      errors.append("supported target entries must be objects")
      continue
    target_id = target.get("id")
    if not isinstance(target_id, str) or not ENGINE_ID_PATTERN.fullmatch(target_id):
      errors.append("supported target IDs must be lowercase kebab-case")
    elif target_id in supported_ids:
      errors.append(f"duplicate supported target ID: {target_id}")
    else:
      supported_ids.add(target_id)
    if target.get("support") != "supported":
      errors.append(f"supported target {target_id!r} must have support=supported")
    if not isinstance(target.get("minimum_major_version"), int) or target["minimum_major_version"] < 1:
      errors.append(f"supported target {target_id!r} needs a positive minimum_major_version")
    evidence = target.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
      errors.append(f"supported target {target_id!r} needs evidence entries")
    required = target.get("required_capabilities")
    expected_required = {
      item["id"] for item in capabilities
      if isinstance(item, dict) and item.get("required") is True
    }
    if not isinstance(required, list) or not all(isinstance(item, str) and item.strip() for item in required):
      errors.append(f"supported target {target_id!r} must list required capabilities as strings")
    elif len(required) != len(set(required)) or set(required) != expected_required:
      errors.append(f"supported target {target_id!r} must list every required capability exactly once")

  not_certified = document.get("not_certified_targets")
  if not isinstance(not_certified, list) or not not_certified:
    errors.append("not_certified_targets must be a non-empty list")
    not_certified = []
  all_target_ids = set(supported_ids)
  for target in not_certified:
    if not isinstance(target, dict):
      errors.append("not-certified target entries must be objects")
      continue
    target_id = target.get("id")
    if not isinstance(target_id, str) or not ENGINE_ID_PATTERN.fullmatch(target_id):
      errors.append("not-certified target IDs must be lowercase kebab-case")
    elif target_id in all_target_ids:
      errors.append(f"duplicate target ID: {target_id}")
    else:
      all_target_ids.add(target_id)
    if target.get("support") not in {"not-certified", "unsupported"}:
      errors.append(f"target {target_id!r} needs an explicit unsupported status")
    if not isinstance(target.get("reason"), str) or not target["reason"].strip():
      errors.append(f"target {target_id!r} needs a reason")

  boundary_checks = document.get("boundary_checks")
  if not isinstance(boundary_checks, dict):
    errors.append("boundary_checks must be an object")
  else:
    for key in ("loading_policy", "offline_policy"):
      value = boundary_checks.get(key)
      if not isinstance(value, str) or not value.strip():
        errors.append(f"boundary_checks.{key} must be a path")
      else:
        try:
          if not _resolve(root, value).is_file():
            errors.append(f"boundary check does not exist: {value}")
        except ValueError as error:
          errors.append(f"boundary check is invalid: {error}")
    markers = boundary_checks.get("forbidden_client_authority_markers")
    if not isinstance(markers, list) or not markers or not all(isinstance(item, str) and item.strip() for item in markers):
      errors.append("forbidden client-authority markers must be a non-empty string list")
  limits = document.get("evidence_limits")
  if not isinstance(limits, list) or not limits or not all(isinstance(item, str) and item.strip() for item in limits):
    errors.append("evidence_limits must be a non-empty string list")
  return errors


def build_report(root: Path, document: object) -> dict:
  errors = validate_definition(root, document)
  report = {
    "schema_version": REPORT_SCHEMA_VERSION,
    "status": "fail",
    "errors": errors,
    "entrypoint": document.get("entrypoint") if isinstance(document, dict) else None,
    "supported_targets": [],
    "not_certified_targets": [],
    "capabilities": [],
    "loading_policy_status": "not-run",
    "offline_policy_status": "not-run",
    "syntax_status": "not-run",
    "boundary_status": "not-run",
  }
  if not isinstance(document, dict) or errors:
    return report

  loading_checker = _load_checker(root, "check_loading_policy.py", "browser_loading_policy")
  offline_checker = _load_checker(root, "check_offline_availability.py", "browser_offline_policy")
  loading_path = _resolve(root, document["boundary_checks"]["loading_policy"])
  offline_path = _resolve(root, document["boundary_checks"]["offline_policy"])
  loading_document = json.loads(loading_path.read_text(encoding="utf-8"))
  offline_document = json.loads(offline_path.read_text(encoding="utf-8"))
  if document["entrypoint"] != loading_document.get("live_entrypoint"):
    errors.append("compatibility entrypoint must match the loading-policy live_entrypoint")
  loading_report = loading_checker.build_report(root, loading_document)
  offline_report = offline_checker.build_report(root, offline_document)
  report["loading_policy_status"] = loading_report["status"]
  report["offline_policy_status"] = offline_report["status"]
  if loading_report["status"] != "pass":
    errors.extend(f"loading policy: {error}" for error in loading_report.get("errors", []))
  if offline_report["status"] != "pass":
    errors.extend(f"offline policy: {error}" for error in offline_report.get("errors", []))

  live_files = loading_document.get("live_files", [])
  audited_files = list(dict.fromkeys([*live_files, "gui/host-adapter.mjs"]))
  syntax_errors = []
  for relative in audited_files:
    if not relative.endswith(".mjs"):
      continue
    result = subprocess.run(["node", "--check", str(root / relative)], capture_output=True, text=True, check=False)
    if result.returncode != 0:
      syntax_errors.append(f"{relative}: {result.stderr.strip() or 'node syntax check failed'}")
  report["syntax_status"] = "pass" if not syntax_errors else "fail"
  report["syntax_files"] = audited_files
  errors.extend(syntax_errors)

  markers = document["boundary_checks"]["forbidden_client_authority_markers"]
  boundary_errors = []
  for relative in audited_files:
    path = root / relative
    if not path.is_file():
      continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
      if marker in text:
        boundary_errors.append(f"forbidden client-authority marker {marker!r} in {relative}")
  report["boundary_status"] = "pass" if not boundary_errors else "fail"
  errors.extend(boundary_errors)
  report["supported_targets"] = document["supported_targets"]
  report["not_certified_targets"] = document["not_certified_targets"]
  report["capabilities"] = document["capabilities"]
  report["status"] = "pass" if not errors else "fail"
  return report


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  try:
    document = json.loads((root / POLICY_PATH).read_text(encoding="utf-8"))
    report = build_report(root, document)
  except (OSError, json.JSONDecodeError, RuntimeError) as error:
    report = {"schema_version": REPORT_SCHEMA_VERSION, "status": "fail", "errors": [str(error)]}
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  raise SystemExit(main())
