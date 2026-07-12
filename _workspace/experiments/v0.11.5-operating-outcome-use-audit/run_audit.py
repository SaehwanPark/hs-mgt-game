#!/usr/bin/env python3
"""Audit operating-outcome visibility and next-command trace continuity."""

import argparse
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_AUDIT_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.4-operating-outcome-debrief-validation"
  / "run_audit.py"
)
SOURCE_SPEC = importlib.util.spec_from_file_location(
  "operating_outcome_debrief_validation", SOURCE_AUDIT_PATH
)
SOURCE_AUDIT = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(SOURCE_AUDIT)
OPERATING_AUDIT = SOURCE_AUDIT.SOURCE_AUDIT


ARTIFACT_TYPE = "operating_outcome_use_audit"
BATCH_ID = "v0.11.5-operating-outcome-use-audit"
SOURCE_ARTIFACT_TYPE = "operating_outcome_debrief_validation"
SOURCE_BATCH_ID = "v0.11.4-operating-outcome-debrief-validation"
CODE_VERSION = "0.11.5"
SOURCE_CODE_VERSION = "0.11.4"
CAMPAIGN = "competitive-regional-v1"
RULESET = "competitive-ruleset-0.2.0"
STATE_HASH_SCHEMA = "competitive-state-hash-v9"
SEEDS = [42, 43, 44]
DIFFICULTIES = ["easy", "normal", "hard", "expert"]
PROFILES = [
  "Access First",
  "Commercial Focus",
  "Workforce Resilience",
  "Capital Modernization",
  "Coalition/Legitimacy",
]
EXPECTED_RUN_COUNT = len(SEEDS) * len(DIFFICULTIES) * len(PROFILES)
EXPECTED_MONTHS = 24

PRIOR_OPERATIONS = re.compile(
  r"^Prior-month operations: treated (?P<treated>-?\d+)/(?P<demand>-?\d+) "
  r"demand units \((?P<unmet>-?\d+) unmet\); revenue (?P<revenue>-?\d+), "
  r"cost (?P<cost>-?\d+), margin (?P<margin>[+-]?\d+)$"
)
PLAYER_RESULT = re.compile(
  r"^Operating result: treated (?P<treated>-?\d+)/(?P<demand>-?\d+) "
  r"demand units \((?P<unmet>-?\d+) unmet\); operating revenue "
  r"(?P<revenue>-?\d+), operating cost (?P<cost>-?\d+), "
  r"operating margin (?P<margin>[+-]?\d+)\."
)
RESULT_LINE = re.compile(r"^Operating result: ")
COMMAND = re.compile(r"^\s*(?P<verb>[a-z_]+)")


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def make_minimal_artifact(run):
  return {
    "artifact_type": SOURCE_ARTIFACT_TYPE,
    "batch_id": SOURCE_BATCH_ID,
    "code_version": SOURCE_CODE_VERSION,
    "campaign": CAMPAIGN,
    "ruleset": RULESET,
    "state_hash_schema": STATE_HASH_SCHEMA,
    "seeds": [42],
    "difficulties": ["normal"],
    "profiles": ["Access First"],
    "runs": [run],
  }


def _parse_values(match):
  return {key: int(value) for key, value in match.groupdict().items()}


def parse_prior_operations(observation):
  matches = [
    _parse_values(match)
    for line in observation
    for match in [PRIOR_OPERATIONS.match(str(line))]
    if match
  ]
  if len(matches) != 1:
    return None, "expected exactly one prior-month operations line"
  return matches[0], None


def parse_player_result(lines):
  matches = [
    _parse_values(match)
    for line in lines
    for match in [PLAYER_RESULT.match(str(line))]
    if match
  ]
  if len(matches) != 1:
    return None, "expected exactly one player operating-result line"
  return matches[0], None


def command_family(command):
  parts = [part.strip() for part in str(command).split(";") if part.strip()]
  verbs = []
  for part in parts:
    match = COMMAND.match(part)
    if not match:
      return "unknown"
    verbs.append(match.group("verb"))
  if not verbs:
    return "unknown"
  return verbs[0] if len(verbs) == 1 else "multi_action"


def _operating_values(transition):
  parsed = OPERATING_AUDIT.parse_operating_transition(transition)
  return {
    key: parsed.get(key)
    for key in ("treated", "demand", "unmet", "revenue", "cost", "margin")
  }


def _signal_categories(transition):
  return OPERATING_AUDIT.parse_operating_transition(transition).get(
    "bottlenecks", []
  )


def _record_signal_responses(
  signal_counts,
  response_counts,
  categories,
  family,
):
  for category in categories:
    signal_counts[category] += 1
    response_counts[category][family] += 1


def audit_run(run):
  transitions = [
    transition
    for transition in run.get("history", [])
    if isinstance(transition, dict)
  ]
  transition_by_turn = {
    transition.get("turn"): transition for transition in transitions
  }
  traces = [
    trace for trace in run.get("turn_trace", []) if isinstance(trace, dict)
  ]
  trace_by_turn = {trace.get("turn"): trace for trace in traces}
  signal_counts = Counter()
  response_counts = defaultdict(Counter)
  observation_gap_count = 0
  prior_observation_match_count = 0
  initial_baseline_count = 0
  trace_hash_match_count = 0
  response_opportunity_count = 0
  response_link_count = 0
  response_gap_count = 0
  terminal_signal_count = 0
  debrief_outcome_match_count = 0
  debrief_outcome_gap_count = 0
  debrief = SOURCE_AUDIT.debrief_sections(run.get("debrief", []))
  rival_operating_result_count = 0

  for month_lines in debrief.values():
    rival_operating_result_count += sum(
      1
      for line in month_lines
      if RESULT_LINE.match(str(line)) and not PLAYER_RESULT.match(str(line))
    )

  for turn, trace in sorted(trace_by_turn.items()):
    current = transition_by_turn.get(turn)
    if not current:
      observation_gap_count += 1
      continue
    if trace.get("latest_transition", {}).get("state_hash") == current.get(
      "state_hash"
    ):
      trace_hash_match_count += 1
    else:
      trace_hash_match_count += 0

    prior, prior_gap = parse_prior_operations(trace.get("observation", []))
    if prior_gap:
      observation_gap_count += 1
    elif turn == 1:
      expected_baseline = {
        "treated": 0,
        "demand": 0,
        "unmet": 0,
        "revenue": 0,
        "cost": 0,
        "margin": 0,
      }
      if prior == expected_baseline:
        initial_baseline_count += 1
      else:
        observation_gap_count += 1
    else:
      previous = transition_by_turn.get(turn - 1)
      if prior == _operating_values(previous):
        prior_observation_match_count += 1
      else:
        observation_gap_count += 1

    categories = []
    if turn > 1:
      previous = transition_by_turn.get(turn - 1)
      categories = _signal_categories(previous) if previous else []
    if turn == len(transitions):
      terminal_signal_count += len(_signal_categories(current))
    if categories:
      response_opportunity_count += len(categories)
      family = command_family(trace.get("submitted_command", ""))
      _record_signal_responses(signal_counts, response_counts, categories, family)
      if family == "unknown":
        response_gap_count += len(categories)
      else:
        response_link_count += len(categories)

  for turn, lines in sorted(debrief.items()):
    current = transition_by_turn.get(turn)
    if not current:
      debrief_outcome_gap_count += 1
      continue
    result, result_gap = parse_player_result(lines)
    if result_gap or result != _operating_values(current):
      debrief_outcome_gap_count += 1
    else:
      debrief_outcome_match_count += 1

  command_families = Counter(
    command_family(trace.get("submitted_command", "")) for trace in traces
  )
  return {
    "profile": run.get("profile"),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty"),
    "completion_status": run.get("completion_status"),
    "transition_count": len(transitions),
    "trace_count": len(traces),
    "initial_baseline_count": initial_baseline_count,
    "prior_observation_match_count": prior_observation_match_count,
    "observation_gap_count": observation_gap_count,
    "trace_hash_match_count": trace_hash_match_count,
    "debrief_outcome_match_count": debrief_outcome_match_count,
    "debrief_outcome_gap_count": debrief_outcome_gap_count,
    "signal_counts": dict(sorted(signal_counts.items())),
    "signal_to_command_counts": {
      category: dict(sorted(counts.items()))
      for category, counts in sorted(response_counts.items())
    },
    "response_opportunity_count": response_opportunity_count,
    "response_link_count": response_link_count,
    "response_gap_count": response_gap_count,
    "terminal_signal_count": terminal_signal_count,
    "rival_operating_result_count": rival_operating_result_count,
    "command_family_counts": dict(sorted(command_families.items())),
    "multi_action_command_count": command_families.get("multi_action", 0),
    "unknown_command_count": command_families.get("unknown", 0),
    "validation_failure_count": len(run.get("validation_failures", [])),
  }


def build_audit(artifact):
  reports = [
    audit_run(run) for run in artifact.get("runs", []) if isinstance(run, dict)
  ]
  coordinates = [
    (report["profile"], report["seed"], report["difficulty"])
    for report in reports
  ]
  expected_coordinates = {
    (profile, seed, difficulty)
    for profile in PROFILES
    for seed in SEEDS
    for difficulty in DIFFICULTIES
  }
  signal_counts = Counter()
  response_counts = defaultdict(Counter)
  for report in reports:
    signal_counts.update(report["signal_counts"])
    for category, counts in report["signal_to_command_counts"].items():
      response_counts[category].update(counts)
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "source_artifact_type": artifact.get("artifact_type"),
    "source_batch_id": artifact.get("batch_id"),
    "source_code_version": artifact.get("code_version"),
    "campaign": artifact.get("campaign"),
    "ruleset": artifact.get("ruleset"),
    "state_hash_schema": artifact.get("state_hash_schema"),
    "seeds": artifact.get("seeds", []),
    "difficulties": artifact.get("difficulties", []),
    "profiles": artifact.get("profiles", []),
    "run_count": len(reports),
    "completed_run_count": sum(
      report["completion_status"] == "complete" for report in reports
    ),
    "expected_run_count": EXPECTED_RUN_COUNT,
    "transition_count": sum(report["transition_count"] for report in reports),
    "trace_count": sum(report["trace_count"] for report in reports),
    "expected_month_count": EXPECTED_RUN_COUNT * EXPECTED_MONTHS,
    "initial_baseline_count": sum(
      report["initial_baseline_count"] for report in reports
    ),
    "prior_observation_match_count": sum(
      report["prior_observation_match_count"] for report in reports
    ),
    "observation_gap_count": sum(
      report["observation_gap_count"] for report in reports
    ),
    "trace_hash_match_count": sum(
      report["trace_hash_match_count"] for report in reports
    ),
    "debrief_outcome_match_count": sum(
      report["debrief_outcome_match_count"] for report in reports
    ),
    "debrief_outcome_gap_count": sum(
      report["debrief_outcome_gap_count"] for report in reports
    ),
    "signal_counts": dict(sorted(signal_counts.items())),
    "signal_count": sum(signal_counts.values()),
    "signal_to_command_counts": {
      category: dict(sorted(counts.items()))
      for category, counts in sorted(response_counts.items())
    },
    "response_opportunity_count": sum(
      report["response_opportunity_count"] for report in reports
    ),
    "response_link_count": sum(
      report["response_link_count"] for report in reports
    ),
    "response_gap_count": sum(report["response_gap_count"] for report in reports),
    "terminal_signal_count": sum(
      report["terminal_signal_count"] for report in reports
    ),
    "rival_operating_result_count": sum(
      report["rival_operating_result_count"] for report in reports
    ),
    "multi_action_command_count": sum(
      report["multi_action_command_count"] for report in reports
    ),
    "unknown_command_count": sum(
      report["unknown_command_count"] for report in reports
    ),
    "validation_failure_count": sum(
      report["validation_failure_count"] for report in reports
    ),
    "duplicate_coordinates": sorted(
      coordinate for coordinate, count in Counter(coordinates).items() if count > 1
    ),
    "missing_coordinates": sorted(expected_coordinates - set(coordinates)),
    "run_reports": reports,
    "runtime_promotion": "deferred",
    "evidence_limits": [
      "This is deterministic traceability evidence, not human comprehension or learning evidence.",
      "Signal-to-command counts are descriptive and do not establish causal response or strategy value.",
      "Operating quantities remain visible integer game abstractions, not calibrated units.",
      "The audit does not establish balance, winnability, calibration, or policy validity.",
    ],
  }


def validate_audit(audit):
  assert audit["artifact_type"] == ARTIFACT_TYPE
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["source_artifact_type"] == SOURCE_ARTIFACT_TYPE
  assert audit["source_batch_id"] == SOURCE_BATCH_ID
  assert audit["source_code_version"] == SOURCE_CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["ruleset"] == RULESET
  assert audit["state_hash_schema"] == STATE_HASH_SCHEMA
  assert audit["seeds"] == SEEDS
  assert audit["difficulties"] == DIFFICULTIES
  assert audit["profiles"] == PROFILES
  assert audit["run_count"] == EXPECTED_RUN_COUNT
  assert audit["completed_run_count"] == EXPECTED_RUN_COUNT
  assert audit["transition_count"] == EXPECTED_RUN_COUNT * EXPECTED_MONTHS
  assert audit["trace_count"] == EXPECTED_RUN_COUNT * EXPECTED_MONTHS
  assert audit["initial_baseline_count"] == 60
  assert audit["prior_observation_match_count"] == 1380
  assert audit["observation_gap_count"] == 0
  assert audit["trace_hash_match_count"] == 1440
  assert audit["debrief_outcome_match_count"] == 1440
  assert audit["debrief_outcome_gap_count"] == 0
  assert audit["signal_counts"] == {
    "capacity_or_demand": 128,
    "operating_loss": 253,
    "workforce_capacity": 60,
  }
  assert audit["signal_count"] == 441
  assert audit["signal_to_command_counts"] == {
    "capacity_or_demand": {"hold": 20, "monitor": 28, "negotiate": 80},
    "operating_loss": {
      "commit": 48,
      "hold": 87,
      "invest": 40,
      "monitor": 14,
      "negotiate": 6,
      "recruit": 58,
    },
    "workforce_capacity": {"hold": 36, "monitor": 24},
  }
  assert audit["response_opportunity_count"] == 441
  assert audit["response_link_count"] == 441
  assert audit["response_gap_count"] == 0
  assert audit["terminal_signal_count"] == 28
  assert audit["rival_operating_result_count"] == 0
  assert audit["multi_action_command_count"] == 0
  assert audit["unknown_command_count"] == 0
  assert audit["validation_failure_count"] == 0
  assert audit["duplicate_coordinates"] == []
  assert audit["missing_coordinates"] == []


def render_json(audit):
  return json.dumps(audit, indent=2, sort_keys=True) + "\n"


def render_markdown(audit):
  signal_counts = audit["signal_counts"]
  lines = [
    f"# {audit['batch_id']}",
    "",
    f"- Source batch: `{audit['source_batch_id']}`",
    f"- Runs: {audit['run_count']}/{audit['expected_run_count']} complete",
    f"- Committed months: {audit['transition_count']}/{audit['expected_month_count']}",
    f"- Prior-month observation matches: {audit['prior_observation_match_count']}",
    f"- Debrief operating-result matches: {audit['debrief_outcome_match_count']}",
    f"- Signal count: {audit['signal_count']}",
    f"- Signal-to-next-command response opportunities: {audit['response_opportunity_count']}",
    f"- Terminal signals without a later command: {audit['terminal_signal_count']}",
    f"- Runtime promotion: {audit['runtime_promotion']}",
    "",
    "## Signal counts",
    "",
    f"- Capacity or demand: {signal_counts.get('capacity_or_demand', 0)}.",
    f"- Operating loss: {signal_counts.get('operating_loss', 0)}.",
    f"- Workforce capacity: {signal_counts.get('workforce_capacity', 0)}.",
    "",
    "## Evidence limits",
    "",
  ]
  lines.extend(f"- {limit}" for limit in audit["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--source",
    default=str(
      Path(__file__).parents[1]
      / "v0.11.4-operating-outcome-debrief-validation"
      / "capture.json"
    ),
  )
  parser.add_argument(
    "--json-output",
    default=str(Path(__file__).with_name("results.json")),
  )
  parser.add_argument(
    "--markdown-output",
    default=str(Path(__file__).with_name("diagnostics.md")),
  )
  args = parser.parse_args()
  audit = build_audit(load_artifact(args.source))
  validate_audit(audit)
  Path(args.json_output).write_text(render_json(audit), encoding="utf-8")
  Path(args.markdown_output).write_text(
    render_markdown(audit), encoding="utf-8"
  )
  print(f"Operating-outcome use audit written to {args.json_output}")
  print(f"Markdown diagnostics written to {args.markdown_output}")


if __name__ == "__main__":
  main()
