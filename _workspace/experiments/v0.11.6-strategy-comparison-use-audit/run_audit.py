#!/usr/bin/env python3
"""Audit strategy-comparison use in the frozen competitive evidence matrix."""

import argparse
import copy
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.4-operating-outcome-debrief-validation"
  / "capture.json"
)
SOURCE_AUDIT_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.5-operating-outcome-use-audit"
  / "run_audit.py"
)
SOURCE_SPEC = importlib.util.spec_from_file_location(
  "operating_outcome_use_audit",
  SOURCE_AUDIT_PATH,
)
SOURCE_AUDIT = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(SOURCE_AUDIT)


ARTIFACT_TYPE = "strategy_comparison_use_audit"
BATCH_ID = "v0.11.6-strategy-comparison-use-audit"
SOURCE_ARTIFACT_TYPE = "operating_outcome_debrief_validation"
SOURCE_BATCH_ID = "v0.11.4-operating-outcome-debrief-validation"
CODE_VERSION = "0.11.6"
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

COMMAND = re.compile(r"^\s*(?P<verb>[a-z_]+)")
ARGUMENTS = {
  "monitor": "target",
  "recruit": "role",
  "invest": "domain",
  "negotiate": "payer",
  "commit": "pledge_type",
  "project": "kind",
}
KNOWN_VERBS = set(ARGUMENTS) | {"hold"}


def load_artifact(path=SOURCE_PATH):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def make_minimal_artifact(run):
  runs = []
  for profile in PROFILES:
    for seed in SEEDS:
      for difficulty in DIFFICULTIES:
        fixture = copy.deepcopy(run)
        fixture["profile"] = profile
        fixture["seed"] = seed
        fixture["difficulty"] = difficulty
        runs.append(fixture)
  return {
    "artifact_type": SOURCE_ARTIFACT_TYPE,
    "batch_id": SOURCE_BATCH_ID,
    "code_version": SOURCE_CODE_VERSION,
    "campaign": CAMPAIGN,
    "ruleset": RULESET,
    "state_hash_schema": STATE_HASH_SCHEMA,
    "seeds": SEEDS,
    "difficulties": DIFFICULTIES,
    "profiles": PROFILES,
    "runs": runs,
    "fixture": True,
  }


def _family(verb, command):
  if verb == "hold":
    return "hold"
  argument = ARGUMENTS.get(verb)
  if not argument:
    return "unknown"
  match = re.search(rf"(?:^|\s){re.escape(argument)}=([^\s]+)", command)
  return f"{verb}:{match.group(1).lower()}" if match else verb


def command_families(command):
  families = []
  for raw in str(command or "").split(";"):
    text = raw.strip()
    if not text:
      continue
    match = COMMAND.match(text)
    if not match:
      families.append("unknown")
      continue
    verb = match.group("verb").lower()
    families.append(_family(verb, text) if verb in KNOWN_VERBS else "unknown")
  return families


def _trajectory(trace):
  return [
    {
      "turn": entry.get("turn"),
      "families": command_families(entry.get("submitted_command", "")),
    }
    for entry in trace
    if isinstance(entry, dict)
  ]


def _hold_rate(families):
  if not families:
    return 0
  return round(families.count("hold") / len(families), 4)


def audit_run(run):
  trace = [
    entry for entry in run.get("turn_trace", []) if isinstance(entry, dict)
  ]
  trajectory = _trajectory(trace)
  families = [family for turn in trajectory for family in turn["families"]]
  family_counts = Counter(families)
  unknown_count = family_counts.get("unknown", 0)
  base = SOURCE_AUDIT.audit_run(run)
  debrief_gap_count = max(
    base["transition_count"] - base["debrief_outcome_match_count"],
    0,
  )
  status = (
    "supported"
    if (
      run.get("completion_status") == "complete"
      and unknown_count == 0
      and base["observation_gap_count"] == 0
      and base["trace_hash_match_count"] == base["transition_count"]
      and debrief_gap_count == 0
      and base["response_gap_count"] == 0
    )
    else "limited"
  )
  return {
    **base,
    "status": status,
    "profile": run.get("profile", "unknown"),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty", "unknown"),
    "trajectory": trajectory,
    "distinct_action_family_count": len(
      {family for family in families if family != "unknown"}
    ),
    "action_family_counts": dict(sorted(family_counts.items())),
    "hold_rate": _hold_rate(families),
    "first_turn_families": trajectory[0]["families"] if trajectory else [],
    "unknown_command_count": unknown_count,
    "multi_action_command_count": sum(
      len(turn["families"]) > 1 for turn in trajectory
    ),
    "debrief_gap_count": debrief_gap_count,
    "operating_outcome_match_count": base["debrief_outcome_match_count"],
  }


def _group_summary(reports, key):
  groups = {}
  for report in reports:
    value = report[key]
    summary = groups.setdefault(
      value,
      {
        "seeds": set(),
        "difficulties": set(),
        "run_count": 0,
        "supported_run_count": 0,
        "distinct_trajectories": set(),
        "action_families": set(),
        "first_turn_families": set(),
        "command_count": 0,
        "hold_count": 0,
        "signal_counts": Counter(),
        "signal_to_command_counts": defaultdict(Counter),
      },
    )
    summary["seeds"].add(report["seed"])
    summary["difficulties"].add(report["difficulty"])
    summary["run_count"] += 1
    summary["supported_run_count"] += report["status"] == "supported"
    summary["distinct_trajectories"].add(
      json.dumps(report["trajectory"], sort_keys=True)
    )
    summary["action_families"].update(report["action_family_counts"])
    summary["first_turn_families"].update(report["first_turn_families"])
    summary["command_count"] += sum(report["action_family_counts"].values())
    summary["hold_count"] += report["action_family_counts"].get("hold", 0)
    summary["signal_counts"].update(report["signal_counts"])
    for category, counts in report["signal_to_command_counts"].items():
      summary["signal_to_command_counts"][category].update(counts)

  result = {}
  for value, summary in sorted(groups.items(), key=lambda item: str(item[0])):
    command_count = summary["command_count"]
    result[str(value)] = {
      "seeds": sorted(summary["seeds"]),
      "difficulties": sorted(summary["difficulties"]),
      "run_count": summary["run_count"],
      "supported_run_count": summary["supported_run_count"],
      "distinct_trajectory_count": len(summary["distinct_trajectories"]),
      "action_families": sorted(summary["action_families"]),
      "first_turn_families": sorted(summary["first_turn_families"]),
      "command_count": command_count,
      "hold_rate": round(summary["hold_count"] / command_count, 4)
      if command_count else 0,
      "signal_counts": dict(sorted(summary["signal_counts"].items())),
      "signal_to_command_counts": {
        category: dict(sorted(counts.items()))
        for category, counts in sorted(
          summary["signal_to_command_counts"].items()
        )
      },
    }
  return result


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
  unexplained_gaps = []
  for report in reports:
    if report["status"] != "supported":
      unexplained_gaps.append({
        "coordinate": [report["profile"], report["seed"], report["difficulty"]],
        "reasons": [
          key for key, value in {
            "incomplete_run": report["completion_status"] != "complete",
            "observation_gap": report["observation_gap_count"] > 0,
            "trace_hash_gap": report["trace_hash_match_count"]
            != report["transition_count"],
            "debrief_gap": report["debrief_gap_count"] > 0,
            "response_gap": report["response_gap_count"] > 0,
            "unknown_command": report["unknown_command_count"] > 0,
          }.items() if value
        ],
      })
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
    "operating_outcome_match_count": sum(
      report["operating_outcome_match_count"] for report in reports
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
    "response_gap_count": sum(
      report["response_gap_count"] for report in reports
    ),
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
      coordinate for coordinate, count in Counter(coordinates).items()
      if count > 1
    ),
    "missing_coordinates": sorted(expected_coordinates - set(coordinates)),
    "profile_summary": _group_summary(reports, "profile"),
    "difficulty_summary": _group_summary(reports, "difficulty"),
    "unexplained_gaps": unexplained_gaps,
    "runtime_promotion": "deferred",
    "evidence_limits": [
      "This is deterministic simulated-policy traceability evidence, not human comprehension or learning evidence.",
      "Trajectory and signal-to-command differences are descriptive and do not establish causal strategy value.",
      "Operating quantities remain visible integer game abstractions, not calibrated units.",
      "The audit does not establish balance, winnability, calibration, or policy validity.",
    ],
    "run_reports": reports,
    "fixture": bool(artifact.get("fixture")),
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
  assert audit["trace_count"] == audit["transition_count"]
  assert audit["duplicate_coordinates"] == []
  assert audit["missing_coordinates"] == []
  assert audit["unknown_command_count"] == 0
  assert audit["observation_gap_count"] == 0
  assert audit["trace_hash_match_count"] == audit["transition_count"]
  assert audit["debrief_outcome_gap_count"] == 0
  assert audit["response_gap_count"] == 0
  assert audit["unexplained_gaps"] == []
  if not audit["fixture"]:
    assert audit["transition_count"] == EXPECTED_RUN_COUNT * EXPECTED_MONTHS
    assert audit["prior_observation_match_count"] == 1380
    assert audit["debrief_outcome_match_count"] == 1440
    assert audit["response_opportunity_count"] == 441
    assert audit["terminal_signal_count"] == 28
    assert audit["rival_operating_result_count"] == 0


def render_json(audit):
  return json.dumps(audit, indent=2, sort_keys=True) + "\n"


def render_markdown(audit):
  lines = [
    f"# Strategy-Comparison Use Audit {audit['code_version']}",
    "",
    f"- Source artifact: `{audit['source_batch_id']}`",
    f"- Runs: {audit['completed_run_count']}/{audit['expected_run_count']}",
    f"- Committed months: {audit['transition_count']}/{audit['expected_month_count']}",
    f"- Prior-month observation matches: {audit['prior_observation_match_count']}",
    f"- Operating-result debrief matches: {audit['operating_outcome_match_count']}",
    f"- Signal-to-next-command opportunities: {audit['response_opportunity_count']}",
    f"- Terminal signals: {audit['terminal_signal_count']}",
    f"- Promotion decision: {audit['runtime_promotion']}",
    "",
    "## Profile comparison",
    "",
    "| Profile | Runs | Supported | Distinct trajectories | Action families | Hold rate |",
    "| --- | ---: | ---: | ---: | ---: | ---: |",
  ]
  for profile, summary in audit["profile_summary"].items():
    lines.append(
      f"| {profile} | {summary['run_count']} | "
      f"{summary['supported_run_count']} | "
      f"{summary['distinct_trajectory_count']} | "
      f"{len(summary['action_families'])} | {summary['hold_rate']:.4f} |"
    )
  lines.extend([
    "",
    "## Unexplained gaps",
    "",
    "No structural gaps identified." if not audit["unexplained_gaps"]
    else "The following evidence gaps require follow-up:",
  ])
  for gap in audit["unexplained_gaps"]:
    lines.append(f"- `{gap['coordinate']}`: {', '.join(gap['reasons'])}.")
  lines.extend(["", "## Evidence limits", ""])
  lines.extend(f"- {limit}" for limit in audit["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--source", default=str(SOURCE_PATH))
  parser.add_argument(
    "--output",
    default=str(Path(__file__).with_name("results.json")),
  )
  parser.add_argument(
    "--diagnostics",
    default=str(Path(__file__).with_name("diagnostics.md")),
  )
  args = parser.parse_args()
  audit = build_audit(load_artifact(Path(args.source)))
  validate_audit(audit)
  Path(args.output).write_text(render_json(audit), encoding="utf-8")
  Path(args.diagnostics).write_text(render_markdown(audit), encoding="utf-8")
  print(
    f"Audited {audit['run_count']} runs and {audit['transition_count']} months; "
    f"promotion={audit['runtime_promotion']}"
  )


if __name__ == "__main__":
  main()
