#!/usr/bin/env python3
"""Compare repeated gui-playtest-v1 captures without interpreting strategy."""

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC_PATH = ROOT / "scripts" / "diagnose_gui_playtests.py"
SPEC = importlib.util.spec_from_file_location("diagnose_gui_playtests", DIAGNOSTIC_PATH)
if SPEC is None or SPEC.loader is None:
  raise RuntimeError("Unable to load the Phase 8 capture validator.")
DIAGNOSTICS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DIAGNOSTICS)

SCHEMA_BLOCKERS = {"capture_invalid", "unsupported_schema"}
TASK_EVIDENCE_BLOCKERS = {"missing_control", "task_incomplete"}
SESSION_DIMENSIONS = (
  "campaign",
  "role",
  "task",
  "seed",
  "interface_mode",
  "accessibility_mode",
)
EVENT_TYPES = (
  "onboarding_opened",
  "onboarding_next",
  "settings_changed",
  "recovery_retry",
  "semantic_snapshot",
  "session_loaded",
  "command_submitted",
  "validation_result",
  "audio_cue",
  "history_observed",
  "failure",
  "task_completed",
)


def display_path(path: Path) -> str:
  absolute = path.resolve()
  try:
    return absolute.relative_to(Path.cwd().resolve()).as_posix()
  except ValueError:
    return absolute.as_posix()


def discover_paths(inputs: Iterable[Path]) -> tuple[list[Path], list[tuple[Path, str]]]:
  discovered = set()
  invalid_inputs = []
  for input_path in inputs:
    if input_path.is_dir():
      matches = [path.resolve() for path in input_path.rglob("*.json") if path.is_file()]
      if matches:
        discovered.update(matches)
      else:
        invalid_inputs.append((input_path, "No JSON captures were found."))
    elif input_path.is_file() and input_path.suffix == ".json":
      discovered.add(input_path.resolve())
    elif input_path.exists():
      invalid_inputs.append((input_path, "Input is not a JSON capture or directory."))
    else:
      invalid_inputs.append((input_path, "Input path does not exist."))
  return sorted(discovered, key=display_path), sorted(invalid_inputs, key=lambda item: display_path(item[0]))


def validation_error(message: str) -> dict[str, Any]:
  return {
    "schema_version": None,
    "session": {},
    "event_count": 0,
    "issues": [{
      "class": "capture_invalid",
      "message": message,
      "evidence_lane": "technical_correctness",
    }],
    "evidence_lanes": {
      "technical_correctness": "blocked",
      "interface_task_proxy": "missing",
      "strategic_trace": "missing",
      "document_grounded_domain_consistency": "unresolved",
      "human_question": "unresolved",
    },
  }


def load_capture(path: Path) -> tuple[Any, dict[str, Any]]:
  try:
    capture = json.loads(path.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    return None, validation_error(f"Unable to read capture: {error}")
  return capture, DIAGNOSTICS.validate_capture(capture)


def event_counts(capture: Any) -> Counter[str]:
  if not isinstance(capture, dict) or not isinstance(capture.get("events"), list):
    return Counter()
  return Counter(
    event.get("type")
    for event in capture["events"]
    if isinstance(event, dict) and event.get("type") in EVENT_TYPES
  )


def run_record(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
  capture, validation = load_capture(path)
  return build_record(path, capture, validation), validation


def build_record(path: Path, capture: Any, validation: dict[str, Any]) -> dict[str, Any]:
  session = validation.get("session", {})
  counts = event_counts(capture)
  issues = validation.get("issues", [])
  schema_valid = not any(issue.get("class") in SCHEMA_BLOCKERS for issue in issues)
  task_evidence_valid = schema_valid and not any(issue.get("class") in TASK_EVIDENCE_BLOCKERS for issue in issues)
  record = {
    "capture": display_path(path),
    "valid": task_evidence_valid,
    "schema_valid": schema_valid,
    "task_evidence_valid": task_evidence_valid,
    "session": {dimension: session.get(dimension) for dimension in SESSION_DIMENSIONS},
    "event_counts": {event_type: counts.get(event_type, 0) for event_type in EVENT_TYPES if counts.get(event_type, 0)},
    "failure_classes": sorted({
      event.get("class")
      for event in (capture.get("events", []) if isinstance(capture, dict) else [])
      if isinstance(event, dict) and event.get("type") == "failure" and event.get("class")
    }),
    "issues": sorted({issue.get("class") for issue in issues if issue.get("class")}),
    "evidence_lanes": validation.get("evidence_lanes", {}),
  }
  return record


def finding(priority: int, category: str, capture: str, code: str, evidence: str, hypothesis: str, limit: str) -> dict[str, Any]:
  return {
    "priority": priority,
    "category": category,
    "capture": capture,
    "code": code,
    "observable_evidence": evidence,
    "hypothesis": hypothesis,
    "evidence_limit": limit,
  }


def revision_findings(record: dict[str, Any], validation: dict[str, Any]) -> list[dict[str, Any]]:
  findings = []
  capture = record["capture"]
  for issue in validation.get("issues", []):
    issue_class = issue.get("class")
    message = str(issue.get("message", ""))
    if issue_class in SCHEMA_BLOCKERS:
      findings.append(finding(
        0,
        "capture_contract",
        capture,
        issue_class,
        message,
        "Repair or discard this artifact before interpreting task evidence.",
        "This is an artifact-quality finding, not interface or human evidence.",
      ))
    elif issue_class in {"missing_control", "task_incomplete"}:
      findings.append(finding(
        1,
        "task_recovery",
        capture,
        issue_class,
        message,
        "Review the declared task path and recovery instrumentation before changing UI behavior.",
        "The capture cannot distinguish harness omission, adapter failure, task mismatch, or interface friction.",
      ))
  failures = set(record["failure_classes"])
  if failures & {"adapter_error", "submit_rejected"} and record["event_counts"].get("recovery_retry", 0) == 0:
    findings.append(finding(
      1,
      "recovery_evidence",
      capture,
      "failure_without_retry",
      ", ".join(sorted(failures & {"adapter_error", "submit_rejected"})),
      "Add or exercise a read-only recovery step before considering a product revision.",
      "A failed trace alone does not establish that the recovery UI was unclear.",
    ))
  if record["task_evidence_valid"] and record["event_counts"].get("semantic_snapshot", 0) == 0:
    findings.append(finding(
      2,
      "evidence_completeness",
      capture,
      "missing_semantic_snapshot",
      "No semantic_snapshot event was recorded.",
      "Require a semantic snapshot in the harness task protocol before comparing interface-task traces.",
      "No interpretation of visible controls is possible from this artifact alone.",
    ))
  if (
    record["task_evidence_valid"]
    and record["event_counts"].get("command_submitted", 0)
    and not record["event_counts"].get("history_observed", 0)
    and not failures & {"adapter_error", "submit_rejected"}
  ):
    findings.append(finding(
      2,
      "evidence_completeness",
      capture,
      "command_without_history",
      "A command_submitted event has no history_observed event.",
      "Retain committed history/hash evidence when a task includes a submission.",
      "The analyzer cannot infer whether the command committed or was only locally attempted.",
    ))
  return findings


def analyze_paths(inputs: Iterable[Path]) -> dict[str, Any]:
  paths, invalid_inputs = discover_paths(inputs)
  records = []
  findings = []
  for path in paths:
    record, validation = run_record(path)
    records.append(record)
    findings.extend(revision_findings(record, validation))
  for path, message in invalid_inputs:
    validation = validation_error(message)
    record = build_record(path, None, validation)
    records.append(record)
    findings.extend(revision_findings(record, validation))
  records.sort(key=lambda record: record["capture"])

  coverage = {
    dimension: sorted({
      record["session"].get(dimension)
      for record in records
      if record["session"].get(dimension) is not None
    }, key=lambda value: (str(type(value)), str(value)))
    for dimension in SESSION_DIMENSIONS
  }
  matrix = sorted({
    tuple(record["session"].get(dimension) for dimension in SESSION_DIMENSIONS)
    for record in records
  }, key=lambda row: tuple((str(type(value)), str(value)) for value in row))
  matrix_rows = [
    {dimension: row[index] for index, dimension in enumerate(SESSION_DIMENSIONS)}
    for row in matrix
  ]
  event_union = sorted({event_type for record in records for event_type in record["event_counts"]})
  findings = sorted(
    findings,
    key=lambda item: (item["priority"], item["category"], item["code"], item["capture"]),
  )
  return {
    "schema_version": "gui-playtest-analysis-v1",
    "input_count": len(paths) + len(invalid_inputs),
    "valid_count": sum(record["task_evidence_valid"] for record in records),
    "invalid_count": sum(not record["task_evidence_valid"] for record in records),
    "schema_valid_count": sum(record["schema_valid"] for record in records),
    "coverage": coverage,
    "declared_matrix": matrix_rows,
    "event_union": event_union,
    "captures": records,
    "revision_findings": findings,
    "evidence_limits": [
      "Findings are observable artifact hypotheses, not human usability or learning evidence.",
      "No strategy ranking, optimal-action score, causal inference, calibration, balance, or policy-validity claim is emitted.",
      "Invalid captures cannot be treated as valid task evidence until repaired or replaced.",
    ],
  }


def main() -> int:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("inputs", nargs="+", type=Path)
  parser.add_argument("--output", type=Path)
  args = parser.parse_args()
  result = analyze_paths(args.inputs)
  rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
  if args.output:
    args.output.write_text(rendered, encoding="utf-8")
  print(rendered, end="")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
