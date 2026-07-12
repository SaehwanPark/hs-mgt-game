#!/usr/bin/env python3
"""Audit visible difficulty pressure in committed Phase 7 artifacts."""

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
ARTIFACT_TYPE = "difficulty_depth_evidence_review"
BATCH_ID = "v0.12.4-difficulty-depth-evidence"
CODE_VERSION = "0.12.4"
CAMPAIGN = "competitive-regional-v1"
ALL_TIER_PATH = (
  "_workspace/experiments/"
  "v0.11.11-phase7-post-change-all-tier-validation/results.json"
)
EXPERT_PATH = (
  "_workspace/experiments/"
  "v0.11.9-expert-difficulty-validation/results.json"
)
SEEDS = [42, 43, 44]
DIFFICULTIES = ["easy", "normal", "hard", "expert"]
PROFILES = [
  "Access First",
  "Commercial Focus",
  "Workforce Resilience",
  "Capital Modernization",
  "Coalition/Legitimacy",
]
EXPECTED_MONTHS = 24
EXPECTED_ALL_TIER_RUNS = len(SEEDS) * len(DIFFICULTIES) * len(PROFILES)
EXPECTED_EXPERT_RUNS = len(SEEDS) * len(PROFILES)
GOLDEN_CONTROL_HASH = "61357596d8800592"

LIMITATIONS = [
  "This is deterministic simulated-policy evidence, not human or classroom evidence.",
  "Bottleneck counts, action trajectories, and endpoint ranges are descriptive signals, not causal marginal effects, validated strategy classes, balance proof, or equilibrium outcomes.",
  "Expert completion is a bounded clearability proxy for the named profiles and seeds, not general winnability.",
  "The all-tier and Expert sources were produced at different code versions, so their endpoint values are not treated as a causal comparison.",
  "Integer operating quantities are gameplay abstractions, not calibrated financial, clinical, legal, or policy units.",
]

REQUIRED_TRACE_FIELDS = {
  "turn",
  "observation",
  "legal_commands",
  "submitted_command",
  "validation_failures",
  "latest_transition",
  "done_after_submit",
}
COMMAND = re.compile(r"^\s*(?P<verb>[a-z_]+)")


SOURCE_PATH = ROOT / "_workspace/experiments/v0.11.1-operating-loop-ai-validation/run_audit.py"
SOURCE_SPEC = importlib.util.spec_from_file_location("difficulty_operating_source", SOURCE_PATH)
SOURCE = importlib.util.module_from_spec(SOURCE_SPEC)
assert SOURCE_SPEC.loader is not None
SOURCE_SPEC.loader.exec_module(SOURCE)


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _history(run):
  value = run.get("history") if isinstance(run, dict) else None
  return value if isinstance(value, list) else []


def _trace(run):
  value = run.get("turn_trace") if isinstance(run, dict) else None
  return value if isinstance(value, list) else []


def _command_families(run):
  families = []
  for entry in _trace(run):
    if not isinstance(entry, dict):
      continue
    for part in str(entry.get("submitted_command", "")).split(";"):
      match = COMMAND.match(part)
      if match:
        families.append(match.group("verb"))
  return families


def _final_outcomes(run):
  return SOURCE._final_outcomes(run)


def _metric_range(values):
  values = list(values)
  unique = sorted(set(values))
  return {
    "count": len(values),
    "min": min(values) if values else None,
    "max": max(values) if values else None,
    "unique_count": len(unique),
  }


def _debrief_supported(run):
  debrief = run.get("debrief") if isinstance(run, dict) else None
  if not isinstance(debrief, list) or not debrief:
    return False
  month_count = sum(
    isinstance(line, str) and line.casefold().startswith("--- month ")
    for line in debrief
  )
  player_count = sum(
    isinstance(line, str) and line.casefold().startswith("  player:")
    for line in debrief
  )
  text = "\n".join(str(line) for line in debrief).casefold()
  return (
    month_count >= EXPECTED_MONTHS
    and player_count >= EXPECTED_MONTHS
    and "decision quality and outcome quality remain separate" in text
  )


def _run_report(run, profile_key):
  issues = []
  history = _history(run)
  trace = _trace(run)
  hashes = [
    transition.get("state_hash")
    for transition in history
    if isinstance(transition, dict)
  ]
  if not isinstance(run, dict):
    return {
      "profile": None,
      "seed": None,
      "difficulty": None,
      "status": "limited",
      "issues": ["run is not an object"],
    }

  if run.get("completion_status") != "complete":
    issues.append("completion_status is not complete")
  if run.get("transition_count") != EXPECTED_MONTHS:
    issues.append("transition_count is not 24")
  if len(history) != EXPECTED_MONTHS:
    issues.append("history does not contain 24 transitions")
  if len(trace) != EXPECTED_MONTHS:
    issues.append("turn_trace does not contain 24 entries")
  if run.get("state_hashes") != hashes:
    issues.append("state_hashes do not match history")
  if not hashes or run.get("final_hash") != hashes[-1]:
    issues.append("final_hash does not match history")
  if run.get("validation_failures") != []:
    issues.append("validation failures are present")

  for index, entry in enumerate(trace):
    if not isinstance(entry, dict):
      issues.append(f"turn_trace entry {index + 1} is malformed")
      continue
    if not REQUIRED_TRACE_FIELDS <= set(entry):
      issues.append(f"turn_trace entry {index + 1} is missing required fields")
    if not isinstance(entry.get("observation"), list) or not entry.get("observation"):
      issues.append(f"turn_trace entry {index + 1} has no observation")
    if not isinstance(entry.get("legal_commands"), list) or not entry.get("legal_commands"):
      issues.append(f"turn_trace entry {index + 1} has no legal command surface")
    if not isinstance(entry.get("submitted_command"), str):
      issues.append(f"turn_trace entry {index + 1} has no submitted command")
    transition = entry.get("latest_transition")
    if not isinstance(transition, dict) or not transition.get("state_hash"):
      issues.append(f"turn_trace entry {index + 1} has no committed transition hash")
    elif index >= len(hashes) or transition.get("state_hash") != hashes[index]:
      issues.append(f"turn_trace entry {index + 1} hash is out of alignment")

  turns = [entry.get("turn") for entry in trace if isinstance(entry, dict)]
  if turns != list(range(1, EXPECTED_MONTHS + 1)):
    issues.append("turn_trace turns are not contiguous")

  operating = [SOURCE.parse_operating_transition(item) for item in history]
  if any(item.get("accounting_status") != "supported" for item in operating):
    issues.append("operating accounting contract is incomplete")
  if not _debrief_supported(run):
    issues.append("debrief month/player or decision-quality coverage is incomplete")

  action_families = _command_families(run)
  bottlenecks = Counter(
    bottleneck
    for item in operating
    for bottleneck in item.get("bottlenecks", [])
  )
  outcomes = _final_outcomes(run)
  if outcomes is None:
    issues.append("final tradeoff outcome is missing")

  return {
    "profile": run.get(profile_key),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty"),
    "status": "supported" if not issues else "limited",
    "issues": sorted(set(issues)),
    "completion_status": run.get("completion_status"),
    "transition_count": len(history),
    "validation_failure_count": len(run.get("validation_failures", [])),
    "trajectory_signature": ";".join(action_families),
    "action_families": dict(sorted(Counter(action_families).items())),
    "bottleneck_counts": dict(sorted(bottlenecks.items())),
    "final_outcomes": outcomes,
  }


def _expected_all_tier_coordinates():
  return {
    (profile, seed, difficulty)
    for profile in PROFILES
    for seed in SEEDS
    for difficulty in DIFFICULTIES
  }


def _expected_expert_coordinates():
  return {(profile, seed) for profile in PROFILES for seed in SEEDS}


def classify_pressure_signal(counts, supported):
  monotonic = all(left <= right for left, right in zip(counts, counts[1:]))
  candidate = supported and monotonic and counts[-1] > counts[0]
  return (
    "candidate_visible_pressure_signal" if candidate else "no_candidate_signal",
    monotonic,
  )


def _validate_all_tier_identity(artifact):
  assert artifact["artifact_type"] == "post_change_all_tier_difficulty_validation"
  assert artifact["batch_id"] == "v0.11.11-phase7-post-change-all-tier-validation"
  assert artifact["code_version"] == "0.11.11"
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["ruleset"] == "competitive-ruleset-0.2.0"
  assert artifact["state_hash_schema"] == "competitive-state-hash-v9"
  assert artifact["seeds"] == SEEDS
  assert artifact["difficulties"] == DIFFICULTIES
  assert artifact["profiles"] == PROFILES
  assert artifact["runtime_promotion"] == "deferred"


def _validate_expert_identity(artifact):
  assert artifact["batch_id"] == "v0.11.9-expert-difficulty-validation"
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["difficulty"] == "expert"
  assert artifact["seeds"] == SEEDS
  assert artifact["profiles"] == PROFILES
  assert artifact["runtime_promotion"] == "deferred"


def audit_all_tier(artifact):
  _validate_all_tier_identity(artifact)
  runs = artifact.get("runs")
  assert isinstance(runs, list)
  coordinates = {
    (run.get("profile"), run.get("seed"), run.get("difficulty"))
    for run in runs
    if isinstance(run, dict)
  }
  issues = []
  if len(runs) != EXPECTED_ALL_TIER_RUNS:
    issues.append("all-tier run count does not match the expected matrix")
  if coordinates != _expected_all_tier_coordinates():
    issues.append("all-tier coordinates do not match the expected matrix")

  reports = [_run_report(run, "profile") for run in runs]
  issues.extend(issue for report in reports for issue in report["issues"])
  by_difficulty = {}
  for difficulty in DIFFICULTIES:
    group = [report for report in reports if report["difficulty"] == difficulty]
    action_counts = Counter(
      family
      for report in group
      for family, count in report["action_families"].items()
      for _ in range(count)
    )
    bottleneck_counts = Counter(
      bottleneck
      for report in group
      for bottleneck, count in report["bottleneck_counts"].items()
      for _ in range(count)
    )
    outcomes = {
      metric: _metric_range(
        report["final_outcomes"][metric]
        for report in group
        if report["final_outcomes"] and metric in report["final_outcomes"]
      )
      for metric in (
        "cash",
        "access",
        "quality",
        "workforce_trust",
        "community_trust",
        "market_share",
      )
    }
    by_difficulty[difficulty] = {
      "run_count": len(group),
      "supported_run_count": sum(report["status"] == "supported" for report in group),
      "transition_count": sum(report["transition_count"] for report in group),
      "trajectory_count": len({report["trajectory_signature"] for report in group}),
      "action_family_counts": dict(sorted(action_counts.items())),
      "bottleneck_counts": dict(sorted(bottleneck_counts.items())),
      "final_outcome_ranges": outcomes,
    }

  high_tier_action_counts_equal = all(
    by_difficulty[difficulty]["action_family_counts"]
    == by_difficulty["normal"]["action_family_counts"]
    for difficulty in ("hard", "expert")
  )
  return {
    "source_id": "all_tiers",
    "source_path": ALL_TIER_PATH,
    "source_code_version": "0.11.11",
    "run_count": len(runs),
    "supported_run_count": sum(report["status"] == "supported" for report in reports),
    "transition_count": sum(report["transition_count"] for report in reports),
    "difficulty_summary": by_difficulty,
    "high_tier_action_counts_equal": high_tier_action_counts_equal,
    "competitive_control_hash": GOLDEN_CONTROL_HASH,
    "issues": sorted(set(issues)),
    "status": "supported" if not issues else "limited",
  }


def audit_expert(artifact):
  _validate_expert_identity(artifact)
  runs = artifact.get("runs")
  assert isinstance(runs, list)
  coordinates = {
    (run.get("profile_name"), run.get("seed"))
    for run in runs
    if isinstance(run, dict)
  }
  issues = []
  if len(runs) != EXPECTED_EXPERT_RUNS:
    issues.append("Expert run count does not match the expected matrix")
  if coordinates != _expected_expert_coordinates():
    issues.append("Expert coordinates do not match the expected matrix")

  reports = [_run_report(run, "profile_name") for run in runs]
  issues.extend(issue for report in reports for issue in report["issues"])
  return {
    "source_id": "expert",
    "source_path": EXPERT_PATH,
    "source_code_version": "0.11.9",
    "run_count": len(runs),
    "supported_run_count": sum(report["status"] == "supported" for report in reports),
    "transition_count": sum(report["transition_count"] for report in reports),
    "coordinate_count": len(coordinates),
    "issues": sorted(set(issues)),
    "status": "supported" if not issues else "limited",
  }


def build_report(artifacts=None):
  artifacts = artifacts or {
    "all_tiers": load_artifact(ROOT / ALL_TIER_PATH),
    "expert": load_artifact(ROOT / EXPERT_PATH),
  }
  all_tier = audit_all_tier(artifacts["all_tiers"])
  expert = audit_expert(artifacts["expert"])
  all_tier_counts = [
    all_tier["difficulty_summary"][difficulty]["bottleneck_counts"].get(
      "workforce_capacity",
      0,
    )
    for difficulty in DIFFICULTIES
  ]
  workforce_supported = all(
    all_tier["difficulty_summary"][difficulty]["supported_run_count"] == len(PROFILES) * len(SEEDS)
    for difficulty in DIFFICULTIES
  )
  classification, workforce_monotonic = classify_pressure_signal(
    all_tier_counts,
    workforce_supported,
  )
  candidate_signal = classification == "candidate_visible_pressure_signal"
  source_issues = all_tier["issues"] + expert["issues"]
  overlap_supported = (
    all_tier["difficulty_summary"]["expert"]["supported_run_count"] == EXPECTED_EXPERT_RUNS
    and expert["coordinate_count"] == EXPECTED_EXPERT_RUNS
  )
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "source_artifacts": [all_tier, expert],
    "aggregate": {
      "run_count": all_tier["run_count"] + expert["run_count"],
      "supported_run_count": all_tier["supported_run_count"] + expert["supported_run_count"],
      "transition_count": all_tier["transition_count"] + expert["transition_count"],
      "source_version_mismatch": True,
      "expert_profile_seed_overlap_count": EXPECTED_EXPERT_RUNS if overlap_supported else 0,
    },
    "pressure_signal": {
      "dimension": "workforce_capacity",
      "all_tier_counts": dict(zip(DIFFICULTIES, all_tier_counts)),
      "monotonic_easy_to_expert": workforce_monotonic,
      "supported_in_each_tier": workforce_supported,
      "classification": (
        "candidate_visible_pressure_signal"
        if candidate_signal
        else "no_candidate_signal"
      ),
      "interpretation": (
        "Workforce-capacity bottleneck counts rise across the tested tiers; "
        "this is a descriptive routing signal, not causal or balance evidence."
        if candidate_signal
        else "The source does not support a monotonic workforce-capacity signal."
      ),
    },
    "clearability": {
      "all_tier_expert_runs": all_tier["difficulty_summary"]["expert"]["supported_run_count"],
      "standalone_expert_runs": expert["supported_run_count"],
      "expected_runs": EXPECTED_EXPERT_RUNS,
      "overlap_supported": overlap_supported,
      "interpretation": "bounded clearability proxy for named profiles and seeds",
    },
    "finding": (
      "candidate_visible_pressure_signal"
      if candidate_signal
      else "no_candidate_signal"
    ),
    "runtime_promotion": "deferred",
    "evidence_limits": LIMITATIONS,
    "issues": sorted(set(source_issues)),
  }


def validate_report(report):
  assert report["artifact_type"] == ARTIFACT_TYPE
  assert report["batch_id"] == BATCH_ID
  assert report["code_version"] == CODE_VERSION
  assert report["campaign"] == CAMPAIGN
  assert report["aggregate"]["run_count"] == 75
  assert report["aggregate"]["supported_run_count"] == 75
  assert report["aggregate"]["transition_count"] == 1800
  assert report["aggregate"]["source_version_mismatch"] is True
  assert report["aggregate"]["expert_profile_seed_overlap_count"] == 15
  assert report["pressure_signal"]["all_tier_counts"] == {
    "easy": 0,
    "normal": 15,
    "hard": 30,
    "expert": 160,
  }
  assert report["pressure_signal"]["monotonic_easy_to_expert"] is True
  assert report["pressure_signal"]["classification"] == "candidate_visible_pressure_signal"
  assert report["clearability"]["all_tier_expert_runs"] == 15
  assert report["clearability"]["standalone_expert_runs"] == 15
  assert report["issues"] == []
  assert report["runtime_promotion"] == "deferred"
  for source in report["source_artifacts"]:
    assert source["status"] == "supported"


def render_markdown(report):
  all_tier, expert = report["source_artifacts"]
  lines = [
    "# Difficulty Depth Evidence Review v0.12.4",
    "",
    "- **Status:** supported",
    "- **Source artifacts:** 2",
    "- **Runs reviewed:** 75 of 75",
    "- **Committed transitions reviewed:** 1,800",
    "- **Runtime promotion:** deferred",
    "",
    "This deterministic read-only audit checks whether the existing difficulty "
    "artifacts expose a visible pressure signal and whether Expert completion "
    "remains a bounded clearability proxy.",
    "",
    "## Source coverage",
    "",
    "| Source | Code version | Runs | Transitions | Supported | Status |",
    "| --- | --- | ---: | ---: | ---: | --- |",
    f"| all-tier post-change | {all_tier['source_code_version']} | {all_tier['run_count']} | {all_tier['transition_count']} | {all_tier['supported_run_count']} | {all_tier['status']} |",
    f"| standalone Expert | {expert['source_code_version']} | {expert['run_count']} | {expert['transition_count']} | {expert['supported_run_count']} | {expert['status']} |",
    "",
    "## Difficulty pressure summary",
    "",
    "| Difficulty | Runs | Workforce capacity | Operating loss | Capacity/demand | Trajectories |",
    "| --- | ---: | ---: | ---: | ---: | ---: |",
  ]
  for difficulty in DIFFICULTIES:
    summary = all_tier["difficulty_summary"][difficulty]
    bottlenecks = summary["bottleneck_counts"]
    lines.append(
      f"| {difficulty} | {summary['run_count']} | "
      f"{bottlenecks.get('workforce_capacity', 0)} | "
      f"{bottlenecks.get('operating_loss', 0)} | "
      f"{bottlenecks.get('capacity_or_demand', 0)} | "
      f"{summary['trajectory_count']} |"
    )
  lines.extend(
    [
      "",
      "## Finding",
      "",
      "The all-tier artifact exposes a candidate `workforce_capacity` pressure "
      "signal: counts rise 0 → 15 → 30 → 160 from Easy through Expert. "
      "Normal, Hard, and Expert retain identical aggregate scripted action "
      "counts in this matrix, so the signal is routed as operating-pressure "
      "evidence rather than a claim about player-perceived difficulty.",
      "",
      "The all-tier Expert subset and standalone Expert artifact each complete "
      "15/15 named profile/seed runs. This is a bounded clearability proxy, not "
      "general Expert winnability.",
      "",
      "## Evidence limits",
      "",
    ]
  )
  lines.extend(f"- {limitation}" for limitation in report["evidence_limits"])
  return "\n".join(lines) + "\n"


def main():
  report = build_report()
  validate_report(report)
  (OUTPUT_DIR / "results.json").write_text(
    json.dumps(report, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (OUTPUT_DIR / "diagnostics.md").write_text(
    render_markdown(report),
    encoding="utf-8",
  )
  print(
    "validated all-tier and Expert sources: 75 runs, 1800 transitions; "
    "workforce-capacity candidate signal; runtime promotion deferred"
  )


if __name__ == "__main__":
  main()
