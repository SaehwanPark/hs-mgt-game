#!/usr/bin/env python3
"""Audit turn-level decision-load proxies from the v0.10.50 capture."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH_ID = "v0.10.52-decision-load-evidence"
CODE_VERSION = "0.10.52"
CAMPAIGN = "competitive-regional-v1"
SOURCE_BATCH_ID = "v0.10.50-teachability-observation-capture"
SOURCE_CODE_VERSION = "0.10.50"
SOURCE_DIFFICULTY = "hard"
SOURCE_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.50-teachability-observation-capture"
  / "results.json"
)
EXPECTED_SEEDS = [42, 43, 44]
EXPECTED_PROFILES = [
  "fiscal_steward",
  "access_expansion_advocate",
  "first_time_executive",
]
EXPECTED_TRANSITIONS = 24
EXPECTED_RUN_COUNT = len(EXPECTED_SEEDS) * len(EXPECTED_PROFILES)
METRIC_KEYS = [
  "action_commands",
  "active_months",
  "hold_commands",
  "max_actions_in_month",
  "multi_action_months",
]
LIMITATIONS = [
  "This audit is deterministic simulated-policy evidence, not human or classroom evidence.",
  "Action concentration and active-month cadence are pacing and action-overload proxies, not cognitive-load measurements.",
  "Profile trajectories and endpoint metrics do not establish strategy quality, causality, balance, winnability, or optimality.",
  "Runtime and interface promotion remains deferred until a player-facing, instructor-facing, or domain-review gap is identified.",
]


def load_artifact(path=SOURCE_PATH):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def command_verbs(command_text):
  if not isinstance(command_text, str):
    return []
  return [
    part.strip().split(maxsplit=1)[0].lower()
    for part in command_text.split(";")
    if part.strip()
  ]


def _longest_streak(values):
  longest = 0
  current = 0
  for value in values:
    if value:
      current += 1
      longest = max(longest, current)
    else:
      current = 0
  return longest


def _empty_summary(run=None):
  run = run if isinstance(run, dict) else {}
  return {
    "profile_id": run.get("profile_id", "unknown"),
    "profile_name": run.get("profile_name", "unknown"),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty", "unknown"),
    "completion_status": run.get("completion_status", "unknown"),
    "transition_count": run.get("transition_count", 0),
    "trace_count": 0,
    "validation_failure_count": len(run.get("validation_failures", [])) if isinstance(run.get("validation_failures", []), list) else 0,
    "retry_count": run.get("retry_count", 0),
    "action_commands": 0,
    "active_months": 0,
    "hold_commands": 0,
    "max_actions_in_month": 0,
    "multi_action_months": 0,
    "longest_active_streak": 0,
    "action_counts_by_month": [],
  }


def summarize_run(run):
  """Return descriptive turn-level command counts for one captured run."""
  summary = _empty_summary(run)
  if not isinstance(run, dict):
    return summary

  trace = run.get("turn_trace")
  if not isinstance(trace, list):
    return summary

  summary["trace_count"] = len(trace)
  action_counts = []
  active_flags = []
  for entry in trace:
    if not isinstance(entry, dict):
      continue
    turn = entry.get("turn")
    verbs = command_verbs(entry.get("submitted_command", ""))
    action_count = sum(verb != "hold" for verb in verbs)
    summary["action_commands"] += action_count
    summary["hold_commands"] += sum(verb == "hold" for verb in verbs)
    if action_count:
      action_counts.append({"turn": turn, "actions": action_count})
    active_flags.append(action_count > 0)

  summary["action_counts_by_month"] = action_counts
  summary["active_months"] = len(action_counts)
  summary["multi_action_months"] = sum(
    item["actions"] > 1 for item in action_counts
  )
  summary["max_actions_in_month"] = max(
    (item["actions"] for item in action_counts),
    default=0,
  )
  summary["longest_active_streak"] = _longest_streak(active_flags)
  return summary


def audit_run(run, source_path):
  summary = summarize_run(run)
  issues = []
  if not isinstance(run, dict):
    issues.append("run record is not an object")
    return {
      "source_path": source_path,
      "status": "limited",
      "issues": issues,
      **summary,
    }

  trace = run.get("turn_trace")
  if run.get("completion_status") != "complete":
    issues.append("completion_status is not complete")
  if not isinstance(trace, list):
    issues.append("turn_trace is missing or not a list")
  else:
    if len(trace) != EXPECTED_TRANSITIONS:
      issues.append("turn_trace does not contain 24 entries")
    turns = [entry.get("turn") for entry in trace if isinstance(entry, dict)]
    if turns != list(range(1, EXPECTED_TRANSITIONS + 1)):
      issues.append("turn_trace does not cover turns 1 through 24 in order")
    if any(
      not isinstance(entry, dict)
      or not isinstance(entry.get("submitted_command"), str)
      or not entry.get("submitted_command", "").strip()
      for entry in trace
    ):
      issues.append("turn_trace contains a missing or empty submitted command")
  if run.get("transition_count") != EXPECTED_TRANSITIONS:
    issues.append("transition_count is not 24")
  if not isinstance(run.get("state_hashes"), list) or len(run["state_hashes"]) != EXPECTED_TRANSITIONS:
    issues.append("state_hashes does not contain 24 entries")
  if run.get("validation_failures") != []:
    issues.append("validation failures are present")
  if run.get("retry_count") != 0:
    issues.append("retry_count is not zero")
  if not isinstance(run.get("debrief"), list) or not run["debrief"]:
    issues.append("debrief is missing")

  return {
    "source_path": source_path,
    "status": "supported" if not issues else "limited",
    "issues": issues,
    **summary,
  }


def _source_identity_gaps(source):
  expected = {
    "batch_id": SOURCE_BATCH_ID,
    "code_version": SOURCE_CODE_VERSION,
    "campaign": CAMPAIGN,
    "difficulty": SOURCE_DIFFICULTY,
    "seeds": EXPECTED_SEEDS,
  }
  actual = {key: source.get(key) for key in expected}
  if actual == expected:
    return []
  return [{"type": "source identity", "expected": expected, "actual": actual}]


def _profile_summaries(reports):
  summaries = {}
  for profile_id in EXPECTED_PROFILES:
    profile_reports = [
      report for report in reports if report.get("profile_id") == profile_id
    ]
    metric_values = [
      {key: report[key] for key in METRIC_KEYS}
      for report in profile_reports
    ]
    seed_stable = bool(metric_values) and all(
      metrics == metric_values[0] for metrics in metric_values
    )
    summaries[profile_id] = {
      "status": (
        "supported"
        if len(profile_reports) == len(EXPECTED_SEEDS)
        and all(report["status"] == "supported" for report in profile_reports)
        and seed_stable
        else "limited"
      ),
      "run_count": len(profile_reports),
      "seeds": sorted(report.get("seed") for report in profile_reports),
      "seed_stable": seed_stable,
      "metrics": metric_values[0] if metric_values else {},
    }
  return summaries


def build_audit(source=None):
  source = load_artifact() if source is None else source
  source = source if isinstance(source, dict) else {}
  gaps = _source_identity_gaps(source)
  raw_runs = source.get("runs", [])
  runs = raw_runs if isinstance(raw_runs, list) else []
  if len(runs) != EXPECTED_RUN_COUNT:
    gaps.append({
      "type": "run coverage",
      "expected": EXPECTED_RUN_COUNT,
      "actual": len(runs),
    })

  reports = [
    audit_run(run, f"source run {index + 1}")
    for index, run in enumerate(runs)
  ]
  expected_members = {
    (profile_id, seed)
    for profile_id in EXPECTED_PROFILES
    for seed in EXPECTED_SEEDS
  }
  observed_members = {
    (report.get("profile_id"), report.get("seed"))
    for report in reports
  }
  if observed_members != expected_members:
    gaps.append({
      "type": "matrix continuity",
      "missing": sorted(expected_members - observed_members),
      "unexpected": sorted(observed_members - expected_members),
    })
  limited_runs = [
    report["source_path"] for report in reports if report["status"] != "supported"
  ]
  if limited_runs:
    gaps.append({"type": "run validation", "limited_runs": limited_runs})

  profile_summaries = _profile_summaries(reports)
  limited_profiles = [
    profile_id
    for profile_id, summary in profile_summaries.items()
    if summary["status"] != "supported"
  ]
  if limited_profiles:
    gaps.append({"type": "profile summary", "limited_profiles": limited_profiles})

  return {
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "source_artifact": str(SOURCE_PATH.relative_to(ROOT)),
    "source_batch_id": source.get("batch_id", "unknown"),
    "source_code_version": source.get("code_version", "unknown"),
    "source_run_count": len(runs),
    "complete_run_count": sum(
      report["status"] == "supported" for report in reports
    ),
    "matrix_continuity": {
      "expected_member_count": len(expected_members),
      "observed_member_count": len(observed_members),
      "status": "supported" if observed_members == expected_members else "limited",
    },
    "runs": reports,
    "profile_summaries": profile_summaries,
    "status": "supported" if not gaps else "limited",
    "unexplained_gaps": gaps,
    "unexplained_gap_count": len(gaps),
    "runtime_promotion": "deferred",
    "promotion_basis": (
      "Turn-level decision-load signals are descriptive pacing proxies. No "
      "player-facing, instructor-facing, or domain-review gap justifies "
      "runtime promotion from this artifact."
    ),
    "limitations": LIMITATIONS,
  }


def validate_audit(audit):
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["status"] == "supported"
  assert audit["source_run_count"] == EXPECTED_RUN_COUNT
  assert audit["complete_run_count"] == EXPECTED_RUN_COUNT
  assert audit["matrix_continuity"]["status"] == "supported"
  assert audit["unexplained_gap_count"] == 0
  assert audit["runtime_promotion"] == "deferred"


def render_markdown(audit):
  lines = [
    f"# Decision-Load and Pacing Proxy Evidence {audit['code_version']}",
    "",
    f"- **Status:** Phase 7 competitive teachability and validation evidence",
    f"- **Source artifact:** `{audit['source_artifact']}`",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Source runs:** {audit['complete_run_count']} complete of {audit['source_run_count']}",
    "",
    "This is a deterministic read-only audit of existing turn-level traces. It does not launch new sessions or change runtime behavior.",
    "",
    "## Profile summaries",
    "",
    "| Profile | Runs | Seeds stable | Action commands | Active months | Holds | Multi-action months | Max actions/month | Status |",
    "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |",
  ]
  for profile_id in EXPECTED_PROFILES:
    summary = audit["profile_summaries"][profile_id]
    metrics = summary["metrics"]
    lines.append(
      f"| {profile_id} | {summary['run_count']} | "
      f"{summary['seed_stable']} | {metrics.get('action_commands', 'N/A')} | "
      f"{metrics.get('active_months', 'N/A')} | {metrics.get('hold_commands', 'N/A')} | "
      f"{metrics.get('multi_action_months', 'N/A')} | "
      f"{metrics.get('max_actions_in_month', 'N/A')} | {summary['status']} |"
    )
  lines.extend([
    "",
    "## Run-level decision-load signals",
    "",
    "| Profile | Seed | Actions | Active months | Holds | Multi-action months | Max actions/month | Status |",
    "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
  ])
  for report in audit["runs"]:
    lines.append(
      f"| {report['profile_id']} | {report.get('seed', 'N/A')} | "
      f"{report['action_commands']} | {report['active_months']} | "
      f"{report['hold_commands']} | {report['multi_action_months']} | "
      f"{report['max_actions_in_month']} | {report['status']} |"
    )
  lines.extend([
    "",
    "## Promotion decision",
    "",
    f"Runtime promotion: {audit['runtime_promotion']}",
    "",
    audit["promotion_basis"],
    "",
    "The metrics expose temporal command concentration that aggregate action totals do not show. They do not establish that a player experienced overload, that one profile is superior, or that a runtime change is needed.",
    "",
    "## Structural gaps",
    "",
  ])
  if audit["unexplained_gaps"]:
    lines.extend(
      f"- {json.dumps(gap, sort_keys=True)}"
      for gap in audit["unexplained_gaps"]
    )
  else:
    lines.append("None identified in the source artifact.")
  lines.extend(["", "## Evidence limits", ""])
  lines.extend(f"- {limitation}" for limitation in audit["limitations"])
  lines.append("")
  return "\n".join(lines)


def main():
  output_dir = Path(__file__).resolve().parent
  audit = build_audit()
  validate_audit(audit)
  (output_dir / "results.json").write_text(
    json.dumps(audit, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (output_dir / "diagnostics.md").write_text(
    render_markdown(audit),
    encoding="utf-8",
  )


if __name__ == "__main__":
  main()
