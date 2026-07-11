#!/usr/bin/env python3
"""Audit operating-loss and bottleneck explainability from v0.11.1 traces."""

import argparse
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "_workspace" / "experiments" / (
  "v0.11.1-operating-loop-ai-validation"
)
SOURCE_ARTIFACT_PATH = SOURCE_DIR / "results.json"
SOURCE_AUDIT_PATH = SOURCE_DIR / "run_audit.py"
SOURCE_ARTIFACT_TYPE = "operating_loop_ai_validation"
SOURCE_BATCH_ID = "v0.11.1-operating-loop-ai-validation"
AUDIT_ARTIFACT_TYPE = "operating_loss_explainability_audit"
BATCH_ID = "v0.11.2-operating-loss-explainability"
CODE_VERSION = "0.11.2"
SOURCE_CODE_VERSION = "0.11.1"
CAMPAIGN = "competitive-regional-v1"
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
SIGNAL_NAMES = (
  "capacity_or_demand",
  "operating_loss",
  "workforce_capacity",
)
MONTH_OUTCOME = re.compile(
  r"treated \d+/\d+ demand units|operating revenue|operating cost|"
  r"operating margin|unmet demand",
  re.IGNORECASE,
)
MONTH_HEADER = re.compile(r"^--- Month (?P<month>\d+) ---$")
GLOBAL_DEBRIEF_MARKERS = (
  "Attributed mechanisms to inspect:",
  "Resolved events:",
)


def _load_source_audit():
  spec = importlib.util.spec_from_file_location(
    "v0111_operating_loop_audit", SOURCE_AUDIT_PATH
  )
  if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load source audit: {SOURCE_AUDIT_PATH}")
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


SOURCE_AUDIT = _load_source_audit()


def load_source_artifact(path=SOURCE_ARTIFACT_PATH):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _debrief_sections(debrief):
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
    if line.startswith(GLOBAL_DEBRIEF_MARKERS):
      global_summary_started = True
      current = None
      continue
    if current is not None:
      sections[current].append(line)
  return {
    "sections": sections,
    "global_attribution_present": any(
      str(line).startswith(GLOBAL_DEBRIEF_MARKERS[0])
      for line in debrief
    ),
  }


def _context_markers(observation):
  text = "\n".join(str(line) for line in observation).casefold()
  markers = {
    "cash_runway": "cash runway:" in text,
    "prior_operations": "prior-month operations:" in text,
    "workforce_trust": "workforce trust:" in text,
    "in_flight_projects": "in-flight projects:" in text,
    "labor_market_note": "policy: labor market note:" in text,
  }
  return markers


def _missing_context_markers(markers):
  return [
    f"missing_{name}"
    for name in (
      "cash_runway",
      "prior_operations",
      "workforce_trust",
      "in_flight_projects",
      "labor_market_note",
    )
    if not markers.get(name)
  ]


def _month_outcome_linked(lines):
  return any(MONTH_OUTCOME.search(line) for line in lines)


def _trace_matches_transition(trace, transition):
  latest = trace.get("latest_transition") if trace else None
  return (
    isinstance(latest, dict)
    and latest.get("turn") == transition.get("turn")
    and latest.get("state_hash") == transition.get("state_hash")
  )


def _audit_run(run):
  source_report = SOURCE_AUDIT.audit_run(run)
  trace_by_turn = {
    entry.get("turn"): entry
    for entry in run.get("turn_trace", [])
    if isinstance(entry, dict) and entry.get("turn") is not None
  }
  history_by_turn = {
    transition.get("turn"): transition
    for transition in run.get("history", [])
    if isinstance(transition, dict) and transition.get("turn") is not None
  }
  debrief = _debrief_sections(run.get("debrief", []))
  signal_counts = Counter()
  limited_reasons = Counter()
  limited_records = []
  decision_context_supported_count = 0
  transition_attribution_supported_count = 0
  month_decision_link_count = 0
  month_outcome_link_count = 0
  rival_event_count = 0

  for operating in source_report["operating"]:
    signals = [
      signal
      for signal in SIGNAL_NAMES
      if signal in operating.get("bottlenecks", [])
    ]
    if not signals:
      continue

    turn = operating.get("turn")
    for signal in signals:
      signal_counts[signal] += 1

    trace = trace_by_turn.get(turn)
    transition = history_by_turn.get(turn)
    missing = []
    if not trace or not isinstance(trace.get("observation"), list):
      missing.append("missing_actor_observation")
      markers = {}
    else:
      markers = _context_markers(trace["observation"])
      missing.extend(_missing_context_markers(markers))
    if not trace or trace.get("submitted_command") is None:
      missing.append("missing_submitted_command")

    if not transition:
      missing.append("missing_transition")
      player_event_present = False
    else:
      player_event_present = any(
        "operations: Riverside Community Health:" in str(event)
        and "treated " in str(event)
        for event in transition.get("events", [])
      )
      if not player_event_present:
        missing.append("missing_player_operating_event")
      if not _trace_matches_transition(trace, transition):
        missing.append("trace_transition_mismatch")

    rival_event_count += operating.get("rival_operating_event_count", 0)
    if operating.get("accounting_status") != "supported":
      missing.append("limited_operating_accounting")

    section = debrief["sections"].get(turn, [])
    has_decision_link = any(line.startswith("Player:") for line in section)
    has_outcome_link = _month_outcome_linked(section)
    if has_decision_link:
      month_decision_link_count += len(signals)
    else:
      missing.append("missing_month_debrief_decision")
    if has_outcome_link:
      month_outcome_link_count += len(signals)
    else:
      missing.append("missing_month_debrief_outcome")

    context_missing = _missing_context_markers(markers)
    if not context_missing and trace and trace.get("submitted_command") is not None:
      decision_context_supported_count += len(signals)
    if (
      transition
      and player_event_present
      and _trace_matches_transition(trace, transition)
      and operating.get("accounting_status") == "supported"
    ):
      transition_attribution_supported_count += len(signals)

    if missing:
      limited_reasons.update(missing)
      limited_records.append({
        "profile": run.get("profile", "unknown"),
        "seed": run.get("seed"),
        "difficulty": run.get("difficulty", "unknown"),
        "turn": turn,
        "signals": signals,
        "missing_markers": sorted(set(missing)),
      })

  candidate_signal_count = sum(signal_counts.values())
  return {
    "profile": run.get("profile", run.get("profile_name", "unknown")),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty", "unknown"),
    "completion_status": run.get("completion_status", "unknown"),
    "transition_count": len(source_report["operating"]),
    "candidate_signal_count": candidate_signal_count,
    "candidate_signal_counts": dict(sorted(signal_counts.items())),
    "decision_context_supported_count": decision_context_supported_count,
    "decision_context_limited_count": (
      candidate_signal_count - decision_context_supported_count
    ),
    "transition_attribution_supported_count": (
      transition_attribution_supported_count
    ),
    "transition_attribution_limited_count": (
      candidate_signal_count - transition_attribution_supported_count
    ),
    "month_debrief_decision_link_count": month_decision_link_count,
    "month_debrief_outcome_link_count": month_outcome_link_count,
    "global_debrief_attribution_present": debrief[
      "global_attribution_present"
    ],
    "rival_operating_event_count": rival_event_count,
    "limited_reasons": dict(sorted(limited_reasons.items())),
    "limited_records": limited_records,
  }


def build_audit(artifact):
  runs = artifact.get("runs", [])
  reports = [_audit_run(run) for run in runs if isinstance(run, dict)]
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
  candidate_counts = Counter()
  limited_reasons = Counter()
  limited_records = []
  for report in reports:
    candidate_counts.update(report["candidate_signal_counts"])
    limited_reasons.update(report["limited_reasons"])
    limited_records.extend(report["limited_records"])

  return {
    "artifact_type": AUDIT_ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "source_artifact_type": artifact.get("artifact_type"),
    "source_batch_id": artifact.get("batch_id"),
    "source_code_version": artifact.get("code_version"),
    "campaign": artifact.get("campaign"),
    "seeds": artifact.get("seeds", []),
    "difficulties": artifact.get("difficulties", []),
    "profiles": artifact.get("profiles", []),
    "run_count": len(reports),
    "transition_count": sum(report["transition_count"] for report in reports),
    "expected_run_count": EXPECTED_RUN_COUNT,
    "expected_month_count": EXPECTED_RUN_COUNT * EXPECTED_MONTHS,
    "duplicate_coordinates": sorted(
      coordinate
      for coordinate, count in Counter(coordinates).items()
      if count > 1
    ),
    "missing_coordinates": sorted(expected_coordinates - set(coordinates)),
    "candidate_signal_count": sum(candidate_counts.values()),
    "candidate_signal_counts": dict(sorted(candidate_counts.items())),
    "decision_context_supported_count": sum(
      report["decision_context_supported_count"] for report in reports
    ),
    "transition_attribution_supported_count": sum(
      report["transition_attribution_supported_count"] for report in reports
    ),
    "month_debrief_decision_link_count": sum(
      report["month_debrief_decision_link_count"] for report in reports
    ),
    "month_debrief_outcome_link_count": sum(
      report["month_debrief_outcome_link_count"] for report in reports
    ),
    "global_debrief_attribution_run_count": sum(
      report["global_debrief_attribution_present"] for report in reports
    ),
    "rival_operating_event_count": sum(
      report["rival_operating_event_count"] for report in reports
    ),
    "limited_reasons": dict(sorted(limited_reasons.items())),
    "limited_records": limited_records,
    "run_reports": reports,
    "runtime_promotion": "deferred",
    "evidence_limits": [
      "This is a deterministic traceability audit, not a causal effect estimate.",
      "Simulated-policy traces do not establish human comprehension, learning, or enjoyment.",
      "Operating quantities remain visible integer game abstractions, not calibrated units.",
      "A missing debrief marker is a product-evidence gap, not proof of poor decisions.",
    ],
  }


def validate_audit(audit):
  assert audit["artifact_type"] == AUDIT_ARTIFACT_TYPE
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["source_artifact_type"] == SOURCE_ARTIFACT_TYPE
  assert audit["source_batch_id"] == SOURCE_BATCH_ID
  assert audit["source_code_version"] == SOURCE_CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["seeds"] == SEEDS
  assert audit["difficulties"] == DIFFICULTIES
  assert audit["profiles"] == PROFILES
  assert audit["run_count"] == EXPECTED_RUN_COUNT
  assert audit["transition_count"] == EXPECTED_RUN_COUNT * EXPECTED_MONTHS
  assert audit["duplicate_coordinates"] == []
  assert audit["missing_coordinates"] == []
  assert audit["candidate_signal_counts"] == {
    "capacity_or_demand": 140,
    "operating_loss": 269,
    "workforce_capacity": 60,
  }
  assert audit["candidate_signal_count"] == 469
  assert audit["decision_context_supported_count"] == 469
  assert audit["transition_attribution_supported_count"] == 469
  assert audit["month_debrief_decision_link_count"] == 469
  assert audit["month_debrief_outcome_link_count"] == 0
  assert audit["global_debrief_attribution_run_count"] == 60
  assert audit["rival_operating_event_count"] == 0
  for record in audit["limited_records"]:
    assert set(record) == {
      "profile",
      "seed",
      "difficulty",
      "turn",
      "signals",
      "missing_markers",
    }


def render_json(audit):
  return json.dumps(audit, indent=2, sort_keys=True) + "\n"


def render_markdown(audit):
  counts = audit["candidate_signal_counts"]
  lines = [
    f"# {audit['batch_id']}",
    "",
    f"- Source batch: `{audit['source_batch_id']}`",
    f"- Campaign: `{audit['campaign']}`",
    f"- Runs audited: {audit['run_count']}/{audit['expected_run_count']}",
    f"- Transitions audited: {audit['transition_count']}/{audit['expected_month_count']}",
    f"- Runtime promotion: {audit['runtime_promotion']}",
    "",
    "## Question",
    "",
    "Whether player-owned operating loss and bottleneck signals retain "
    "decision-time context, transition attribution, and month-level debrief linkage.",
    "",
    "## Candidate signals",
    "",
    f"- Capacity or demand: {counts.get('capacity_or_demand', 0)} months.",
    f"- Operating loss: {counts.get('operating_loss', 0)} months.",
    f"- Workforce capacity: {counts.get('workforce_capacity', 0)} months.",
    f"- Total categorized signals: {audit['candidate_signal_count']}.",
    "",
    "## Traceability",
    "",
    f"- Decision context supported: {audit['decision_context_supported_count']}/{audit['candidate_signal_count']}.",
    f"- Transition attribution supported: {audit['transition_attribution_supported_count']}/{audit['candidate_signal_count']}.",
    f"- Month-level debrief decision linkage: {audit['month_debrief_decision_link_count']}/{audit['candidate_signal_count']}.",
    f"- Month-level debrief outcome linkage: {audit['month_debrief_outcome_link_count']}/{audit['candidate_signal_count']}.",
    f"- Runs with global debrief attribution: {audit['global_debrief_attribution_run_count']}/{audit['run_count']}.",
    "",
    "Global attribution summaries are reported separately and are not counted as month-level debrief explanations.",
    "",
    "## Evidence limits",
    "",
  ]
  lines.extend(f"- {limit}" for limit in audit["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--source", default=str(SOURCE_ARTIFACT_PATH))
  parser.add_argument(
    "--json-output",
    default=str(Path(__file__).with_name("results.json")),
  )
  parser.add_argument(
    "--markdown-output",
    default=str(Path(__file__).with_name("diagnostics.md")),
  )
  args = parser.parse_args()

  source = load_source_artifact(args.source)
  source_audit = SOURCE_AUDIT.build_audit(source)
  SOURCE_AUDIT.validate_audit(source_audit, strict=True)
  audit = build_audit(source)
  validate_audit(audit)
  Path(args.json_output).write_text(render_json(audit), encoding="utf-8")
  Path(args.markdown_output).write_text(
    render_markdown(audit), encoding="utf-8"
  )
  print(f"Operating explainability audit written to {args.json_output}")
  print(f"Markdown diagnostics written to {args.markdown_output}")


if __name__ == "__main__":
  main()
