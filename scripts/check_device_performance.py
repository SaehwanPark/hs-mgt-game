#!/usr/bin/env python3
"""Check the bounded emulated low-power GUI profile evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


POLICY_PATH = "assets/device-performance-policy.json"
REPORT_SCHEMA_VERSION = "device-performance-report-v1"
PROFILE_ID = "low-power-browser-proxy"
PROFILE_VIEWPORT = {"width": 1024, "height": 768}
REQUIRED_FIELDS = (
  "schema_version", "status", "surface", "live_entrypoint",
  "loading_policy", "profile", "limits", "measurements", "evidence",
  "certification", "evidence_limits",
)
METRIC_LIMITS = (
  "live_source_bytes", "dom_elements", "svg_elements", "shell_reload_ms",
  "host_start_ms", "adapter_command_ms",
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


def _positive_int(value: object) -> bool:
  return type(value) is int and value > 0


def _nonnegative_int(value: object) -> bool:
  return type(value) is int and value >= 0


def validate_definition(root: Path, document: object) -> list[str]:
  if not isinstance(document, dict):
    return ["device performance policy document must be an object"]
  errors: list[str] = []
  for field in REQUIRED_FIELDS:
    if field not in document:
      errors.append(f"missing field {field!r}")
  if document.get("schema_version") != "device-performance-v1":
    errors.append("unsupported device performance schema_version")
  if document.get("status") != "completed-emulated-proxy":
    errors.append("status must record a completed emulated proxy")
  for field in ("surface", "live_entrypoint", "loading_policy"):
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
      errors.append(f"{field} must be a non-empty string")
  for field in ("live_entrypoint", "loading_policy"):
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
      continue
    try:
      resolved = _resolve(root, value)
    except ValueError as error:
      errors.append(f"{field} is invalid: {error}")
    else:
      if not resolved.is_file():
        errors.append(f"{field} does not exist: {value}")

  profile = document.get("profile")
  if not isinstance(profile, dict):
    errors.append("profile must be an object")
  else:
    if profile.get("id") != PROFILE_ID:
      errors.append(f"profile.id must be {PROFILE_ID!r}")
    viewport = profile.get("viewport")
    if not isinstance(viewport, dict):
      errors.append("profile.viewport must be an object")
    else:
      for field in ("width", "height"):
        if not _positive_int(viewport.get(field)):
          errors.append(f"profile.viewport.{field} must be a positive integer")
      if viewport != PROFILE_VIEWPORT:
        errors.append("profile.viewport must be 1024x768 for the low-power proxy")
    expected_modes = {
      "motion": "reduced",
      "audio": "off",
      "storage": "unavailable",
      "network": "loopback-only",
    }
    for field, expected in expected_modes.items():
      if profile.get(field) != expected:
        errors.append(f"profile.{field} must be {expected!r}")

  limits = document.get("limits")
  if not isinstance(limits, dict):
    errors.append("limits must be an object")
  else:
    for field in METRIC_LIMITS:
      if not _positive_int(limits.get(field)):
        errors.append(f"limits.{field} must be a positive integer")

  measurements = document.get("measurements")
  if not isinstance(measurements, dict):
    errors.append("measurements must be an object")
  else:
    viewport = measurements.get("viewport")
    if not isinstance(viewport, dict):
      errors.append("measurements.viewport must be an object")
    else:
      for field in ("width", "height"):
        if not _positive_int(viewport.get(field)):
          errors.append(f"measurements.viewport.{field} must be a positive integer")
    for field in ("live_source_bytes", "dom_elements", "svg_elements", "shell_reload_max_ms", "host_start_ms", "adapter_command_ms"):
      if not _nonnegative_int(measurements.get(field)):
        errors.append(f"measurements.{field} must be a non-negative integer")
    samples = measurements.get("shell_reload_samples_ms")
    if not isinstance(samples, list) or not samples or not all(_nonnegative_int(value) for value in samples):
      errors.append("measurements.shell_reload_samples_ms must be a non-empty list of non-negative integers")
    elif measurements.get("shell_reload_max_ms") != max(samples):
      errors.append("measurements.shell_reload_max_ms must equal the sample maximum")
    for field in ("written_equivalent_present", "audio_off_present", "reduced_motion_language_present"):
      if not isinstance(measurements.get(field), bool):
        errors.append(f"measurements.{field} must be boolean")

  evidence = document.get("evidence")
  if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
    errors.append("evidence must be a non-empty string list")
  limits_text = document.get("evidence_limits")
  if not isinstance(limits_text, list) or not limits_text or not all(isinstance(item, str) and item.strip() for item in limits_text):
    errors.append("evidence_limits must be a non-empty string list")

  certification = document.get("certification")
  if not isinstance(certification, dict):
    errors.append("certification must be an object")
  else:
    if certification.get("real_device") is not False:
      errors.append("certification.real_device must be false")
    if certification.get("hardware_target") is not None:
      errors.append("certification.hardware_target must be null for an emulated proxy")
    if not isinstance(certification.get("claim"), str) or not certification["claim"].strip():
      errors.append("certification.claim must be a non-empty string")
  return errors


def _load_json(root: Path, relative: str, label: str) -> tuple[object | None, list[str]]:
  try:
    path = _resolve(root, relative)
    return json.loads(path.read_text(encoding="utf-8")), []
  except (OSError, json.JSONDecodeError, ValueError) as error:
    return None, [f"cannot read {label}: {error}"]


def build_report(root: Path, document: object) -> dict:
  errors = validate_definition(root, document)
  base = {
    "schema_version": REPORT_SCHEMA_VERSION,
    "status": "fail",
    "errors": errors,
    "profile": document.get("profile") if isinstance(document, dict) else None,
    "measurements": document.get("measurements") if isinstance(document, dict) else None,
    "source_files": [],
  }
  if not isinstance(document, dict) or errors:
    return base

  loading_document, loading_errors = _load_json(root, document["loading_policy"], "loading policy")
  errors.extend(loading_errors)
  if not isinstance(loading_document, dict):
    return base | {"errors": errors}
  live_files = loading_document.get("live_files")
  if not isinstance(live_files, list) or not live_files or not all(isinstance(path, str) and path.strip() for path in live_files):
    errors.append("loading policy live_files must be a non-empty string list")
    return base | {"errors": errors}
  source_files = []
  for relative in live_files:
    try:
      path = _resolve(root, relative)
    except ValueError as error:
      errors.append(f"loading policy live file is invalid: {error}")
      continue
    if not path.is_file():
      errors.append(f"loading policy live file does not exist: {relative}")
      continue
    source_files.append({"path": relative, "bytes": path.stat().st_size})
  source_bytes = sum(item["bytes"] for item in source_files)
  measurements = document["measurements"]
  limits = document["limits"]
  if document["live_entrypoint"] != loading_document.get("live_entrypoint"):
    errors.append("live_entrypoint must match the loading policy")
  if source_bytes != measurements["live_source_bytes"]:
    errors.append(f"live source bytes {source_bytes} do not match captured measurement {measurements['live_source_bytes']}")
  if measurements["dom_elements"] > limits["dom_elements"]:
    errors.append("DOM element measurement exceeds limit")
  if measurements["svg_elements"] > limits["svg_elements"]:
    errors.append("SVG element measurement exceeds limit")
  if source_bytes > limits["live_source_bytes"]:
    errors.append("live source bytes exceed limit")
  for field in ("host_start_ms", "adapter_command_ms"):
    if measurements[field] > limits[field]:
      errors.append(f"{field} measurement exceeds limit")
  if measurements["shell_reload_max_ms"] > limits["shell_reload_ms"]:
    errors.append("shell reload measurement exceeds limit")
  if measurements["viewport"] != document["profile"]["viewport"]:
    errors.append("measurement viewport must match profile viewport")
  for field in ("written_equivalent_present", "audio_off_present", "reduced_motion_language_present"):
    if measurements[field] is not True:
      errors.append(f"{field} must be true")
  base.update({
    "errors": errors,
    "source_files": source_files,
    "source_bytes": source_bytes,
    "limits": limits,
    "status": "pass" if not errors else "fail",
  })
  return base


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  document, errors = _load_json(root, POLICY_PATH, "device performance policy")
  if errors:
    report = {
      "schema_version": REPORT_SCHEMA_VERSION,
      "status": "fail",
      "errors": errors,
      "source_files": [],
    }
  else:
    report = build_report(root, document)
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  raise SystemExit(main())
