#!/usr/bin/env python3
"""Audit the v0.11.1 operating-loop AI validation matrix."""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ARTIFACT_TYPE = "operating_loop_ai_validation"
BATCH_ID = "v0.11.1-operating-loop-ai-validation"
CODE_VERSION = "0.11.1"
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

OPERATING_EFFECTS = {
  "monthly demand allocation changed monthly_demand by ": "demand",
  "staffed volume resolution changed monthly_treated_volume by ": "treated",
  "capacity shortfall changed monthly_unmet_demand by ": "unmet",
  "revenue realization changed monthly_operating_revenue by ": "revenue",
  "operating expense changed monthly_operating_cost by ": "cost",
  "monthly operating cycle changed cash by ": "cash_delta",
}
OPERATING_EVENT = re.compile(
  r"Riverside Community Health: treated (?P<treated>-?\d+)/(?P<demand>-?\d+) "
  r"demand units; operating revenue (?P<revenue>-?\d+), cost "
  r"(?P<cost>-?\d+), margin (?P<margin>[+-]?\d+)"
)
COMMAND = re.compile(r"^\s*(?P<verb>[a-z_]+)")
FINAL_TRADEOFF = re.compile(
  r"cash moved from -?\d+ to (?P<cash>-?\d+), access from -?\d+ to "
  r"(?P<access>-?\d+), quality from -?\d+ to (?P<quality>-?\d+), "
  r"workforce trust from -?\d+ to (?P<workforce_trust>-?\d+), "
  r"community trust from -?\d+ to (?P<community_trust>-?\d+), and "
  r"market share from -?\d+ to (?P<market_share>-?\d+)"
)


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _history(run):
  history = run.get("history") if isinstance(run, dict) else None
  if isinstance(history, list):
    return history
  return [
    entry.get("latest_transition")
    for entry in run.get("turn_trace", [])
    if isinstance(entry, dict) and isinstance(entry.get("latest_transition"), dict)
  ]


def _command_families(run):
  families = []
  for entry in run.get("turn_trace", []) if isinstance(run, dict) else []:
    if not isinstance(entry, dict):
      continue
    command = str(entry.get("submitted_command", ""))
    for raw in command.split(";"):
      match = COMMAND.match(raw)
      if match:
        families.append(match.group("verb"))
  return families


def _final_outcomes(run):
  text = "\n".join(str(line) for line in run.get("debrief", []))
  match = FINAL_TRADEOFF.search(text)
  if not match:
    return None
  return {key: int(value) for key, value in match.groupdict().items()}


def parse_operating_transition(transition):
  values = {}
  evidence_gaps = []
  rival_event_count = 0

  for effect in transition.get("effects", []) if isinstance(transition, dict) else []:
    text = str(effect)
    for prefix, field in OPERATING_EFFECTS.items():
      if text.startswith(prefix):
        raw_value = text[len(prefix):].strip()
        try:
          values[field] = int(raw_value)
        except ValueError:
          evidence_gaps.append({"reason": f"malformed operating effect: {text}"})
        break

  event_values = None
  for event in transition.get("events", []) if isinstance(transition, dict) else []:
    text = str(event)
    match = OPERATING_EVENT.search(text)
    if match:
      event_values = {
        key: int(value)
        for key, value in match.groupdict().items()
      }
    elif "treated " in text and "operating revenue" in text:
      rival_event_count += 1

  required = ("demand", "treated", "unmet", "revenue", "cost", "cash_delta")
  for field in required:
    if field not in values:
      evidence_gaps.append({"reason": f"missing operating field: {field}"})

  if event_values is None:
    evidence_gaps.append({"reason": "missing Riverside operating event"})
  else:
    values["margin"] = event_values["margin"]
    if values.get("demand") != event_values["demand"]:
      evidence_gaps.append({"reason": "demand effect does not match operating event"})
    if values.get("treated") != event_values["treated"]:
      evidence_gaps.append({"reason": "treated effect does not match operating event"})
    if values.get("revenue") != event_values["revenue"]:
      evidence_gaps.append({"reason": "revenue effect does not match operating event"})
    if values.get("cost") != event_values["cost"]:
      evidence_gaps.append({"reason": "cost effect does not match operating event"})
    if values.get("cash_delta") != event_values["margin"]:
      evidence_gaps.append({"reason": "cash effect does not match operating margin"})

  if all(field in values for field in required):
    if values["unmet"] != values["demand"] - values["treated"]:
      evidence_gaps.append({"reason": "demand-flow identity failed"})
    if values["cash_delta"] != values["revenue"] - values["cost"]:
      evidence_gaps.append({"reason": "cash-margin identity failed"})
  if not transition.get("state_hash"):
    evidence_gaps.append({"reason": "missing committed state hash"})

  return {
    **values,
    "turn": transition.get("turn"),
    "state_hash": transition.get("state_hash"),
    "bottlenecks": _bottlenecks(transition, values),
    "accounting_status": "supported" if not evidence_gaps else "limited",
    "evidence_gaps": evidence_gaps,
    "rival_operating_event_count": rival_event_count,
  }


def _bottlenecks(transition, values):
  bottlenecks = []
  if values.get("unmet", 0) > 0:
    bottlenecks.append("capacity_or_demand")
  if values.get("cash_delta", 0) < 0:
    bottlenecks.append("operating_loss")
  text = "\n".join(
    str(item)
    for item in transition.get("events", []) + transition.get("effects", [])
  ).casefold()
  if "understaff" in text or "staffing capacity constraint" in text:
    bottlenecks.append("workforce_capacity")
  return bottlenecks


def audit_run(run):
  transitions = _history(run)
  operating = [parse_operating_transition(item) for item in transitions]
  gaps = [
    {"turn": item.get("turn"), **gap}
    for item in operating
    for gap in item.get("evidence_gaps", [])
  ]
  state_hashes = [item.get("state_hash") for item in transitions]
  command_families = _command_families(run)
  trace = run.get("turn_trace", []) if isinstance(run, dict) else []
  debrief = run.get("debrief", []) if isinstance(run, dict) else []
  debrief_text = "\n".join(str(line) for line in debrief).casefold()
  debrief_months = sum(
    line.casefold().startswith("--- month ")
    for line in debrief
    if isinstance(line, str)
  )
  debrief_players = sum(
    line.casefold().startswith("player:")
    for line in debrief
    if isinstance(line, str)
  )
  explanation_supported = (
    len(trace) == len(transitions)
    and all(
      isinstance(entry, dict)
      and entry.get("observation")
      and entry.get("submitted_command") is not None
      and isinstance(entry.get("latest_transition"), dict)
      and entry["latest_transition"].get("state_hash")
      for entry in trace
    )
    and debrief_months >= len(transitions)
    and debrief_players >= len(transitions)
    and "decision quality and outcome quality remain separate" in debrief_text
  )
  return {
    "profile": run.get("profile", run.get("profile_name", "unknown")),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty", "unknown"),
    "completion_status": run.get("completion_status", "unknown"),
    "transition_count": run.get("transition_count", len(transitions)),
    "operating_month_count": len(operating),
    "operating_status": "supported" if not gaps else "limited",
    "operating_gaps": gaps,
    "operating": operating,
    "state_hash_count": len(state_hashes),
    "command_families": command_families,
    "first_command_family": command_families[0] if command_families else None,
    "trajectory_signature": tuple(command_families),
    "final_outcomes": _final_outcomes(run),
    "validation_failure_count": len(run.get("validation_failures", [])),
    "explanation_status": "supported" if explanation_supported else "limited",
    "rival_operating_event_count": sum(
      item.get("rival_operating_event_count", 0) for item in operating
    ),
  }


def _metric_summary(values):
  unique = sorted(set(values))
  return {
    "count": len(values),
    "min": min(values) if values else None,
    "max": max(values) if values else None,
    "unique_count": len(unique),
    "stable": bool(values) and len(unique) == 1,
  }


def _threshold_crossings(operating):
  crossings = []
  for previous, current in zip(operating, operating[1:]):
    if (previous.get("unmet", 0) == 0) != (current.get("unmet", 0) == 0):
      crossings.append({
        "from_turn": previous.get("turn"),
        "to_turn": current.get("turn"),
        "metric": "monthly_unmet_demand",
        "kind": "zero_to_positive_boundary",
      })
    if (previous.get("cash_delta", 0) >= 0) != (current.get("cash_delta", 0) >= 0):
      crossings.append({
        "from_turn": previous.get("turn"),
        "to_turn": current.get("turn"),
        "metric": "monthly_operating_margin",
        "kind": "nonnegative_to_negative_boundary",
      })
  return crossings


def build_audit(artifact):
  runs = artifact.get("runs", []) if isinstance(artifact, dict) else []
  reports = [audit_run(run) for run in runs if isinstance(run, dict)]
  all_operating = [item for report in reports for item in report["operating"]]
  metric_values = defaultdict(list)
  for item in all_operating:
    for metric in ("demand", "treated", "unmet", "revenue", "cost", "margin", "cash_delta"):
      if metric in item:
        metric_values[metric].append(item[metric])

  effect_stability = {
    metric: _metric_summary(values)
    for metric, values in sorted(metric_values.items())
  }
  bottlenecks = Counter(
    bottleneck
    for item in all_operating
    for bottleneck in item.get("bottlenecks", [])
  )
  action_families = Counter(
    family for report in reports for family in report["command_families"]
  )
  trajectories = Counter(
    ";".join(report["trajectory_signature"])
    for report in reports
  )
  action_counts_by_profile = defaultdict(Counter)
  action_counts_by_difficulty = defaultdict(Counter)
  action_counts_by_month = defaultdict(Counter)
  first_command_families = Counter()
  for report in reports:
    action_counts_by_profile[report["profile"]].update(report["command_families"])
    action_counts_by_difficulty[report["difficulty"]].update(report["command_families"])
    first_command_families[report["first_command_family"]] += 1
    for month, family in enumerate(report["command_families"], start=1):
      action_counts_by_month[str(month)][family] += 1
  low_variation = [
    metric
    for metric, summary in effect_stability.items()
    if summary["unique_count"] <= 2
  ]
  threshold_crossings = [
    {
      "profile": report["profile"],
      "seed": report["seed"],
      "difficulty": report["difficulty"],
      **crossing,
    }
    for report in reports
    for crossing in _threshold_crossings(report["operating"])
  ]
  coordinates = [
    (report["profile"], report["seed"], report["difficulty"])
    for report in reports
  ]
  duplicate_coordinates = [
    coordinate
    for coordinate, count in Counter(coordinates).items()
    if count > 1
  ]
  expected_coordinates = {
    (profile, seed, difficulty)
    for profile in PROFILES
    for seed in SEEDS
    for difficulty in DIFFICULTIES
  }
  missing_coordinates = sorted(expected_coordinates - set(coordinates))
  rival_events = sum(report["rival_operating_event_count"] for report in reports)
  completed = sum(report["completion_status"] == "complete" for report in reports)
  supported = sum(report["operating_status"] == "supported" for report in reports)
  explanation_supported = sum(
    report["explanation_status"] == "supported" for report in reports
  )
  outcome_values = defaultdict(list)
  for report in reports:
    for metric, value in (report["final_outcomes"] or {}).items():
      outcome_values[metric].append(value)
  return {
    "artifact_type": artifact.get("artifact_type", "unknown"),
    "batch_id": artifact.get("batch_id", "unknown"),
    "code_version": artifact.get("code_version", "unknown"),
    "campaign": artifact.get("campaign", "unknown"),
    "seeds": artifact.get("seeds", []),
    "difficulties": artifact.get("difficulties", []),
    "profiles": artifact.get("profiles", []),
    "run_count": len(reports),
    "completed_run_count": completed,
    "supported_run_count": supported,
    "explanation_supported_run_count": explanation_supported,
    "expected_run_count": EXPECTED_RUN_COUNT,
    "duplicate_coordinates": duplicate_coordinates,
    "missing_coordinates": missing_coordinates,
    "run_reports": reports,
    "action_family_counts": dict(sorted(action_families.items())),
    "action_counts_by_profile": {
      key: dict(sorted(value.items()))
      for key, value in sorted(action_counts_by_profile.items())
    },
    "action_counts_by_difficulty": {
      key: dict(sorted(value.items()))
      for key, value in sorted(action_counts_by_difficulty.items())
    },
    "action_counts_by_month": {
      key: dict(sorted(value.items()))
      for key, value in sorted(action_counts_by_month.items())
    },
    "final_outcome_ranges": {
      metric: _metric_summary(values)
      for metric, values in sorted(outcome_values.items())
    },
    "trajectory_count": len(trajectories),
    "trajectory_signatures": dict(sorted(trajectories.items())),
    "bottleneck_counts": dict(sorted(bottlenecks.items())),
    "effect_stability": effect_stability,
    "low_variation_candidates": sorted(low_variation),
    "threshold_crossings": threshold_crossings,
    "rival_operating_event_count": rival_events,
    "candidate_common_actions": [
      family for family, count in sorted(first_command_families.items())
      if reports and family and count == len(reports)
    ],
    "candidate_near_dominance_actions": [
      family for family, count in sorted(first_command_families.items())
      if reports and family and count >= (len(reports) * 9 + 9) // 10
    ],
    "runtime_promotion": "deferred",
    "evidence_limits": [
      "These are deterministic simulated-policy traces, not human or classroom evidence.",
      "Observed effect stability and common actions are not causal marginal effects or dominance proof.",
      "Integer operating quantities are gameplay abstractions, not calibrated financial or clinical units.",
      "The matrix does not establish enjoyment, learning, winnability, or policy validity.",
    ],
  }


def validate_audit(audit, strict=False):
  assert audit["artifact_type"] == ARTIFACT_TYPE
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["seeds"] == SEEDS
  assert audit["difficulties"] == DIFFICULTIES
  assert audit["profiles"] == PROFILES
  assert audit["run_count"] == EXPECTED_RUN_COUNT
  assert audit["completed_run_count"] == EXPECTED_RUN_COUNT
  assert audit["supported_run_count"] == EXPECTED_RUN_COUNT
  assert audit["explanation_supported_run_count"] == EXPECTED_RUN_COUNT
  assert audit["duplicate_coordinates"] == []
  assert audit["missing_coordinates"] == []
  assert audit["rival_operating_event_count"] == 0
  for report in audit["run_reports"]:
    assert report["operating_status"] == "supported"
    assert report["validation_failure_count"] == 0
    if strict:
      assert report["transition_count"] == EXPECTED_MONTHS
      assert report["operating_month_count"] == EXPECTED_MONTHS


def render_markdown(audit):
  lines = [
    f"# {audit['batch_id']}",
    "",
    f"- Code version: `{audit['code_version']}`",
    f"- Campaign: `{audit['campaign']}`",
    f"- Runs: {audit['completed_run_count']}/{audit['expected_run_count']} complete",
    f"- Operating months audited: {sum(report['operating_month_count'] for report in audit['run_reports'])}",
    f"- Distinct command trajectories: {audit['trajectory_count']}",
    f"- Decision-to-debrief trace coverage: {audit['explanation_supported_run_count']}/{audit['expected_run_count']} runs",
    f"- Runtime promotion: {audit['runtime_promotion']}",
    "",
    "## Matrix",
    "",
    f"Seeds: {', '.join(str(seed) for seed in audit['seeds'])}",
    f"Difficulties: {', '.join(audit['difficulties'])}",
    f"Profiles: {', '.join(audit['profiles'])}",
    "",
    "## Operating evidence",
    "",
    "| Metric | Count | Range | Unique values | Stable observed effect |",
    "| --- | ---: | ---: | ---: | --- |",
  ]
  for metric, summary in audit["effect_stability"].items():
    lines.append(
      f"| {metric} | {summary['count']} | {summary['min']}–{summary['max']} | "
      f"{summary['unique_count']} | {'yes' if summary['stable'] else 'no'} |"
    )
  lines.extend([
    "",
    "## Final outcome ranges",
    "",
    "| Metric | Range | Unique values |",
    "| --- | ---: | ---: |",
  ])
  for metric, summary in audit["final_outcome_ranges"].items():
    lines.append(
      f"| {metric} | {summary['min']}–{summary['max']} | {summary['unique_count']} |"
    )
  lines.extend([
    "",
    "### Bottlenecks",
    "",
  ])
  if audit["bottleneck_counts"]:
    for name, count in audit["bottleneck_counts"].items():
      lines.append(f"- `{name}`: {count} operating months")
  else:
    lines.append("- None observed in the audited player-owned traces.")
  lines.extend([
    "",
    "### Candidate signals",
    "",
    f"- Low-variation operating variables: {', '.join(audit['low_variation_candidates']) or 'none'}.",
    f"- Candidate common first-month actions: {', '.join(audit['candidate_common_actions']) or 'none'}.",
    f"- Candidate near-dominance first-month actions: {', '.join(audit['candidate_near_dominance_actions']) or 'none'}.",
    f"- Threshold-crossing candidates: {len(audit['threshold_crossings'])}.",
    "- No dominance, causal marginal-effect, calibration, or balance claim is made.",
    "",
    "## Evidence limits",
    "",
  ])
  lines.extend(f"- {limit}" for limit in audit["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "input",
    nargs="?",
    default=str(Path(__file__).with_name("results.json")),
  )
  parser.add_argument(
    "--output",
    default=str(Path(__file__).with_name("diagnostics.md")),
  )
  args = parser.parse_args()
  audit = build_audit(load_artifact(args.input))
  validate_audit(audit, strict=True)
  Path(args.output).write_text(render_markdown(audit), encoding="utf-8")
  print(f"Operating-loop diagnostics written to {args.output}")


if __name__ == "__main__":
  main()
