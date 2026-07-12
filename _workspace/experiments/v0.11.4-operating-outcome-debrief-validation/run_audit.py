#!/usr/bin/env python3
"""Audit post-v0.11.3 monthly operating-outcome debrief linkage."""

import argparse
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_AUDIT_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.1-operating-loop-ai-validation"
  / "run_audit.py"
)
SOURCE_SPEC = importlib.util.spec_from_file_location(
  "operating_loop_ai_validation_audit", SOURCE_AUDIT_PATH
)
SOURCE_AUDIT = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(SOURCE_AUDIT)


ARTIFACT_TYPE = "operating_outcome_debrief_validation"
BATCH_ID = "v0.11.4-operating-outcome-debrief-validation"
CODE_VERSION = "0.11.4"
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
SIGNAL_NAMES = ("capacity_or_demand", "operating_loss", "workforce_capacity")
MONTH_HEADER = re.compile(r"^--- Month (?P<month>\d+) ---$")
RESULT_LINE = re.compile(r"^Operating result: ")
PLAYER_RESULT = re.compile(r"^Operating result: treated ")


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def debrief_sections(debrief):
  sections = {}
  current = None
  global_summary_started = False
  for raw_line in debrief:
    line = str(raw_line)
    match = MONTH_HEADER.match(line)
    if match and not global_summary_started:
      current = int(match.group("month"))
      sections[current] = []
      continue
    if line.startswith("Attributed mechanisms to inspect:") or line.startswith("Resolved events:"):
      global_summary_started = True
      current = None
      continue
    if current is not None:
      sections[current].append(line)
  return sections


def outcome_counts(debrief):
  player = 0
  rival = 0
  sections = debrief_sections(debrief)
  missing = []
  for month in sorted(sections):
    player_lines = [line for line in sections[month] if PLAYER_RESULT.match(line)]
    result_lines = [line for line in sections[month] if RESULT_LINE.match(line)]
    player += len(player_lines)
    rival += len(result_lines) - len(player_lines)
    if len(player_lines) != 1:
      missing.append(month)
  return {
    "sections": sections,
    "player_operating_result_count": player,
    "rival_operating_result_count": rival,
    "missing_months": missing,
  }


def audit_run(run):
  transitions = run.get("history", [])
  trace_by_turn = {
    entry.get("turn"): entry
    for entry in run.get("turn_trace", [])
    if isinstance(entry, dict)
  }
  operating = []
  trace_mismatches = []
  for transition in transitions:
    parsed = SOURCE_AUDIT.parse_operating_transition(transition)
    operating.append(parsed)
    trace = trace_by_turn.get(transition.get("turn"))
    latest = trace.get("latest_transition") if trace else None
    if not isinstance(latest, dict) or latest.get("state_hash") != transition.get("state_hash"):
      trace_mismatches.append(transition.get("turn"))

  counts = outcome_counts(run.get("debrief", []))
  signal_counts = Counter(
    signal
    for item in operating
    for signal in item.get("bottlenecks", [])
    if signal in SIGNAL_NAMES
  )
  signal_months_with_outcomes = sum(
    1
    for item in operating
    if item.get("bottlenecks")
    and item.get("turn") in counts["sections"]
    and len([line for line in counts["sections"][item["turn"]] if PLAYER_RESULT.match(line)]) == 1
  )
  return {
    "profile": run.get("profile"),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty"),
    "completion_status": run.get("completion_status"),
    "transition_count": len(transitions),
    "operating": operating,
    "signal_counts": dict(sorted(signal_counts.items())),
    "signal_month_count": sum(signal_counts.values()),
    "signal_months_with_outcomes": signal_months_with_outcomes,
    "month_count": len(counts["sections"]),
    "player_operating_result_count": counts["player_operating_result_count"],
    "rival_operating_result_count": counts["rival_operating_result_count"],
    "missing_months": counts["missing_months"],
    "trace_mismatches": trace_mismatches,
    "validation_failure_count": len(run.get("validation_failures", [])),
    "operating_limited_count": sum(
      item.get("accounting_status") != "supported" for item in operating
    ),
    "debrief_alignment_mismatch": (
      len(counts["sections"]) != len(transitions)
      or counts["player_operating_result_count"] > len(transitions)
    ),
  }


def build_audit(artifact):
  reports = [audit_run(run) for run in artifact.get("runs", []) if isinstance(run, dict)]
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
  for report in reports:
    signal_counts.update(report["signal_counts"])
  return {
    "artifact_type": artifact.get("artifact_type"),
    "batch_id": artifact.get("batch_id"),
    "code_version": artifact.get("code_version"),
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
    "expected_month_count": EXPECTED_RUN_COUNT * EXPECTED_MONTHS,
    "month_count": sum(report["month_count"] for report in reports),
    "player_operating_result_count": sum(
      report["player_operating_result_count"] for report in reports
    ),
    "rival_operating_result_count": sum(
      report["rival_operating_result_count"] for report in reports
    ),
    "month_debrief_outcome_link_count": sum(
      report["signal_months_with_outcomes"] for report in reports
    ),
    "candidate_signal_count": sum(signal_counts.values()),
    "candidate_signal_counts": dict(sorted(signal_counts.items())),
    "missing_month_outcome_count": sum(
      len(report["missing_months"]) for report in reports
    ),
    "trace_mismatch_count": sum(len(report["trace_mismatches"]) for report in reports),
    "validation_failure_count": sum(
      report["validation_failure_count"] for report in reports
    ),
    "operating_limited_count": sum(
      report["operating_limited_count"] for report in reports
    ),
    "debrief_alignment_mismatch_count": sum(
      report["debrief_alignment_mismatch"] for report in reports
    ),
    "duplicate_coordinates": sorted(
      coordinate for coordinate, count in Counter(coordinates).items() if count > 1
    ),
    "missing_coordinates": sorted(expected_coordinates - set(coordinates)),
    "run_reports": reports,
    "runtime_promotion": "deferred",
    "evidence_limits": [
      "This is deterministic traceability evidence, not a causal effect estimate.",
      "Simulated-policy traces do not establish human comprehension, learning, or enjoyment.",
      "Operating quantities remain visible integer game abstractions, not calibrated units.",
      "Complete debrief linkage does not establish balance, winnability, or policy validity.",
    ],
  }


def validate_audit(audit):
  assert audit["artifact_type"] == ARTIFACT_TYPE
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["ruleset"] == RULESET
  assert audit["state_hash_schema"] == STATE_HASH_SCHEMA
  assert audit["seeds"] == SEEDS
  assert audit["difficulties"] == DIFFICULTIES
  assert audit["profiles"] == PROFILES
  assert audit["run_count"] == EXPECTED_RUN_COUNT
  assert audit["completed_run_count"] == EXPECTED_RUN_COUNT
  assert audit["transition_count"] == EXPECTED_RUN_COUNT * EXPECTED_MONTHS
  assert audit["month_count"] == EXPECTED_RUN_COUNT * EXPECTED_MONTHS
  assert audit["player_operating_result_count"] == EXPECTED_RUN_COUNT * EXPECTED_MONTHS
  assert audit["candidate_signal_counts"] == {
    "capacity_or_demand": 140,
    "operating_loss": 269,
    "workforce_capacity": 60,
  }
  assert audit["candidate_signal_count"] == 469
  assert audit["month_debrief_outcome_link_count"] == 469
  assert audit["rival_operating_result_count"] == 0
  assert audit["missing_month_outcome_count"] == 0
  assert audit["trace_mismatch_count"] == 0
  assert audit["validation_failure_count"] == 0
  assert audit["operating_limited_count"] == 0
  assert audit["debrief_alignment_mismatch_count"] == 0
  assert audit["duplicate_coordinates"] == []
  assert audit["missing_coordinates"] == []


def render_json(audit):
  return json.dumps(audit, indent=2, sort_keys=True) + "\n"


def render_markdown(audit):
  counts = audit["candidate_signal_counts"]
  lines = [
    f"# {audit['batch_id']}",
    "",
    f"- Campaign: `{audit['campaign']}`",
    f"- Runs: {audit['run_count']}/{audit['expected_run_count']} complete",
    f"- Committed months: {audit['transition_count']}/{audit['expected_month_count']}",
    f"- Player operating-result lines: {audit['player_operating_result_count']}",
    f"- Month-level operating-outcome linkage: {audit['month_debrief_outcome_link_count']}/{audit['candidate_signal_count']}",
    f"- Runtime promotion: {audit['runtime_promotion']}",
    "",
    "## Signal counts",
    "",
    f"- Capacity or demand: {counts.get('capacity_or_demand', 0)} months.",
    f"- Operating loss: {counts.get('operating_loss', 0)} months.",
    f"- Workforce capacity: {counts.get('workforce_capacity', 0)} months.",
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
    default=str(Path(__file__).with_name("capture.json")),
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
  Path(args.markdown_output).write_text(render_markdown(audit), encoding="utf-8")
  print(f"Operating-outcome audit written to {args.json_output}")
  print(f"Markdown diagnostics written to {args.markdown_output}")


if __name__ == "__main__":
  main()
