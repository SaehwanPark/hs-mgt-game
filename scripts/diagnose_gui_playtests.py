#!/usr/bin/env python3
"""Validate and classify dependency-free GUI playtest capture artifacts."""

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA = "gui-playtest-v1"
FAILURE_CLASSES = {
  "adapter_error",
  "submit_rejected",
  "unsupported_schema",
  "missing_control",
  "semantic_gap",
  "capture_invalid",
  "task_incomplete",
}
SESSION_FIELDS = {
  "session_id",
  "campaign",
  "seed",
  "role",
  "task",
  "viewport",
  "interface_mode",
  "accessibility_mode",
  "capture_method",
  "screenshot_refs",
}
EVENT_FIELDS = {
  "onboarding_opened": {"campaign", "next_action"},
  "onboarding_next": {"target"},
  "settings_changed": {"setting", "value"},
  "recovery_retry": {"target"},
  "semantic_snapshot": {"sections", "controls", "status"},
  "session_loaded": {"campaign", "turn", "done", "schema"},
  "command_submitted": {"campaign", "command", "turn"},
  "validation_result": {"valid", "code", "message"},
  "audio_cue": {"id", "source", "equivalent"},
  "history_observed": {"turn", "state_hash", "transition_count"},
  "failure": {"class", "message", "recoverable"},
  "task_completed": {"role", "task", "result"},
}
SNAPSHOT_SECTION_FIELDS = {"id", "hidden", "text"}
SNAPSHOT_CONTROL_FIELDS = {"id", "role", "label", "disabled", "hidden"}
EVIDENCE_FIELDS = {
  "commands": {"sequence", "type", "campaign", "command", "turn"},
  "validations": {"sequence", "type", "valid", "code", "message"},
  "audio_cues": {"sequence", "type", "id", "source", "equivalent"},
  "history_hashes": {"sequence", "type", "turn", "state_hash", "transition_count"},
  "failures": {"sequence", "type", "class", "message", "recoverable"},
}
ROOT_FIELDS = {"schema_version", "session", "events", "evidence"}
FORBIDDEN_KEYS = {
  "worldstate",
  "world_state",
  "affiliationworldstate",
  "affiliation_world_state",
  "resolvedinputs",
  "resolved_inputs",
  "effect_queue",
  "effectqueue",
  "true_state",
  "truestate",
  "hidden_state",
  "hiddenstate",
  "private_rival",
  "privaterival",
  "raw_envelope",
  "raw_payload",
  "chain_of_thought",
  "chainofthought",
}


def normalize_key(value: Any) -> str:
  text = str(value).replace("-", "_")
  text = "".join(f"_{char.lower()}" if char.isupper() else char for char in text)
  return text.lower()


def forbidden_paths(value: Any, path: str = "$") -> list[str]:
  found = []
  if isinstance(value, dict):
    for key, child in value.items():
      if normalize_key(key) in FORBIDDEN_KEYS:
        found.append(f"{path}.{key}")
      found.extend(forbidden_paths(child, f"{path}.{key}"))
  elif isinstance(value, list):
    for index, child in enumerate(value):
      found.extend(forbidden_paths(child, f"{path}[{index}]"))
  return found


def issue(issue_class: str, message: str, lane: str) -> dict[str, str]:
  return {"class": issue_class, "message": message, "evidence_lane": lane}


def validate_capture(capture: Any) -> dict[str, Any]:
  issues = []
  if not isinstance(capture, dict):
    return {
      "schema_version": None,
      "session": {},
      "event_count": 0,
      "issues": [issue("capture_invalid", "Capture root must be an object.", "technical_correctness")],
    }
  schema = capture.get("schema_version")
  if schema != SCHEMA:
    issues.append(issue("unsupported_schema", f"Expected {SCHEMA}; found {schema!r}.", "technical_correctness"))
  forbidden = forbidden_paths(capture)
  if forbidden:
    issues.append(issue("capture_invalid", f"Forbidden fields: {', '.join(forbidden)}.", "technical_correctness"))
  unknown_root = sorted(set(capture) - ROOT_FIELDS)
  if unknown_root:
    issues.append(issue("capture_invalid", f"Unknown root fields: {', '.join(unknown_root)}.", "technical_correctness"))

  session = capture.get("session")
  if not isinstance(session, dict):
    session = {}
    issues.append(issue("capture_invalid", "Capture session metadata must be an object.", "technical_correctness"))
  unknown_session = sorted(set(session) - SESSION_FIELDS)
  if unknown_session:
    issues.append(issue("capture_invalid", f"Unknown session fields: {', '.join(unknown_session)}.", "technical_correctness"))
  for required in ("campaign", "role", "task"):
    if not session.get(required):
      issues.append(issue("capture_invalid", f"Missing session field: {required}.", "technical_correctness"))

  events = capture.get("events")
  if not isinstance(events, list):
    events = []
    issues.append(issue("capture_invalid", "Capture events must be a list.", "technical_correctness"))
  for expected_sequence, event in enumerate(events):
    if not isinstance(event, dict):
      issues.append(issue("capture_invalid", f"Event {expected_sequence} must be an object.", "technical_correctness"))
      continue
    if event.get("sequence") != expected_sequence:
      issues.append(issue("capture_invalid", f"Event {expected_sequence} has non-contiguous sequence.", "technical_correctness"))
    event_type = event.get("type")
    if event_type not in EVENT_FIELDS:
      issues.append(issue("capture_invalid", f"Unknown event type: {event_type!r}.", "technical_correctness"))
      continue
    unknown_fields = sorted(set(event) - ({"sequence", "type"} | EVENT_FIELDS[event_type]))
    if unknown_fields:
      issues.append(issue("capture_invalid", f"Unknown fields in {event_type}: {', '.join(unknown_fields)}.", "technical_correctness"))
    if event_type == "failure":
      failure_class = event.get("class")
      if failure_class not in FAILURE_CLASSES:
        issues.append(issue("capture_invalid", f"Unknown failure class: {failure_class!r}.", "technical_correctness"))
      elif failure_class in {"adapter_error", "submit_rejected", "unsupported_schema"}:
        issues.append(issue(failure_class, str(event.get("message", "Host/client failure.")), "interface_task_proxy"))
    if event_type == "semantic_snapshot":
      sections = event.get("sections")
      controls = event.get("controls")
      if not isinstance(sections, list) or not isinstance(controls, list):
        issues.append(issue("capture_invalid", "Semantic snapshot sections and controls must be lists.", "technical_correctness"))
      else:
        for name, entries, allowed in (
          ("sections", sections, SNAPSHOT_SECTION_FIELDS),
          ("controls", controls, SNAPSHOT_CONTROL_FIELDS),
        ):
          for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
              issues.append(issue("capture_invalid", f"Semantic snapshot {name}[{index}] must be an object.", "technical_correctness"))
              continue
            unknown_fields = sorted(set(entry) - allowed)
            if unknown_fields:
              issues.append(issue("capture_invalid", f"Unknown fields in semantic snapshot {name}: {', '.join(unknown_fields)}.", "technical_correctness"))
        if not controls:
          issues.append(issue("missing_control", "Semantic snapshot contains no controls.", "interface_task_proxy"))

  evidence = capture.get("evidence")
  if not isinstance(evidence, dict):
    issues.append(issue("capture_invalid", "Capture evidence must be an object.", "technical_correctness"))
  else:
    unknown_evidence = sorted(set(evidence) - set(EVIDENCE_FIELDS))
    if unknown_evidence:
      issues.append(issue("capture_invalid", f"Unknown evidence lanes: {', '.join(unknown_evidence)}.", "technical_correctness"))
    for lane, entries in evidence.items():
      if lane not in EVIDENCE_FIELDS:
        continue
      if not isinstance(entries, list):
        issues.append(issue("capture_invalid", f"Evidence lane {lane} must be a list.", "technical_correctness"))
        continue
      for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
          issues.append(issue("capture_invalid", f"Evidence entry {lane}[{index}] must be an object.", "technical_correctness"))
          continue
        unknown_fields = sorted(set(entry) - EVIDENCE_FIELDS[lane])
        if unknown_fields:
          issues.append(issue("capture_invalid", f"Unknown fields in evidence {lane}: {', '.join(unknown_fields)}.", "technical_correctness"))

  if not any(event.get("type") == "task_completed" for event in events if isinstance(event, dict)):
    issues.append(issue("task_incomplete", "No task_completed event was captured.", "interface_task_proxy"))

  command_count = sum(event.get("type") == "command_submitted" for event in events if isinstance(event, dict))
  history_count = sum(event.get("type") == "history_observed" for event in events if isinstance(event, dict))
  semantic_count = sum(event.get("type") == "semantic_snapshot" for event in events if isinstance(event, dict))
  invalid = any(entry["class"] in {"capture_invalid", "unsupported_schema"} for entry in issues)
  return {
    "schema_version": schema,
    "session": {key: session.get(key) for key in sorted(session)},
    "event_count": len(events),
    "issues": issues,
    "evidence_lanes": {
      "technical_correctness": "blocked" if invalid else "recorded",
      "interface_task_proxy": "recorded" if semantic_count else "missing",
      "strategic_trace": "recorded" if command_count and history_count else "missing",
      "document_grounded_domain_consistency": "unresolved",
      "human_question": "unresolved",
    },
  }


def main() -> int:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("capture", type=Path)
  parser.add_argument("--output", type=Path)
  args = parser.parse_args()
  try:
    capture = json.loads(args.capture.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    result = {
      "schema_version": None,
      "session": {},
      "event_count": 0,
      "issues": [issue("capture_invalid", f"Unable to read capture: {error}", "technical_correctness")],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    return 2
  result = validate_capture(capture)
  rendered = json.dumps(result, indent=2, sort_keys=True)
  if args.output:
    args.output.write_text(rendered + "\n", encoding="utf-8")
  print(rendered)
  return 2 if any(entry["class"] in {"capture_invalid", "unsupported_schema"} for entry in result["issues"]) else 0


if __name__ == "__main__":
  raise SystemExit(main())
