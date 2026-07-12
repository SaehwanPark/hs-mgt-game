#!/usr/bin/env python3
"""Audit current-code teachability and pacing traces."""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT_TYPE = "current_code_teachability_capture"
BATCH_ID = "v0.11.12-phase7-current-code-teachability-capture"
EXPECTED_CODE_VERSION = "0.11.12"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTY = "hard"
RULESET = "competitive-ruleset-0.2.0"
STATE_HASH_SCHEMA = "competitive-state-hash-v9"
SEEDS = [42, 43, 44]
PROFILES = [
  "fiscal_steward",
  "access_expansion_advocate",
  "first_time_executive",
]
EXPECTED_TRANSITIONS = 24
EXPECTED_RUN_COUNT = len(SEEDS) * len(PROFILES)
GOLDEN_CONTROL_HASH = "61357596d8800592"
REQUIRED_TRACE_FIELDS = {
  "turn",
  "observation",
  "legal_commands",
  "submitted_command",
  "validation_failures",
  "retry_commands",
  "latest_transition",
  "done_after_submit",
}
OPERATING_EVENT = re.compile(
  r"treated (?P<treated>-?\d+)/(?P<demand>-?\d+) demand units; "
  r"operating revenue (?P<revenue>-?\d+), cost (?P<cost>-?\d+), "
  r"margin (?P<margin>[+-]?\d+)"
)
COMMAND = re.compile(r"^\s*(?P<verb>[a-z_]+)")
LIMITATIONS = [
  "This artifact is deterministic simulated-policy evidence, not human or classroom evidence.",
  "Action cadence, multi-action months, and retries are pacing and friction proxies, not cognitive-load or comprehension measurements.",
  "Profile trajectories and endpoint metrics do not establish strategy quality, causality, balance, winnability, or optimality.",
  "Runtime promotion remains deferred until a player-facing, instructor-facing, or domain-review gap is identified.",
]


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def expected_matrix():
  return {
    (profile_id, seed)
    for profile_id in PROFILES
    for seed in SEEDS
  }


def command_verbs(command_text):
  if not isinstance(command_text, str):
    return []
  return [
    match.group("verb")
    for part in command_text.split(";")
    if (match := COMMAND.match(part))
  ]


def _history(run):
  history = run.get("history") if isinstance(run, dict) else None
  return history if isinstance(history, list) else []


def summarize_run(run):
  run = run if isinstance(run, dict) else {}
  trace = run.get("turn_trace")
  trace = trace if isinstance(trace, list) else []
  action_commands = 0
  hold_commands = 0
  action_counts = []
  active_flags = []
  retry_count = 0
  for entry in trace:
    if not isinstance(entry, dict):
      active_flags.append(False)
      continue
    verbs = command_verbs(entry.get("submitted_command", ""))
    action_count = sum(verb != "hold" for verb in verbs)
    action_commands += action_count
    hold_commands += sum(verb == "hold" for verb in verbs)
    active_flags.append(action_count > 0)
    if action_count:
      action_counts.append({"turn": entry.get("turn"), "actions": action_count})
    retries = entry.get("retry_commands", [])
    if isinstance(retries, list):
      retry_count += len(retries)

  longest_active_streak = 0
  current_streak = 0
  for active in active_flags:
    current_streak = current_streak + 1 if active else 0
    longest_active_streak = max(longest_active_streak, current_streak)

  return {
    "profile_id": run.get("profile_id", "unknown"),
    "profile_name": run.get("profile_name", "unknown"),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty", "unknown"),
    "completion_status": run.get("completion_status", "unknown"),
    "transition_count": run.get("transition_count", len(_history(run))),
    "trace_count": len(trace),
    "validation_failure_count": (
      len(run.get("validation_failures", []))
      if isinstance(run.get("validation_failures", []), list)
      else 0
    ),
    "retry_count": retry_count,
    "action_commands": action_commands,
    "active_months": len(action_counts),
    "hold_commands": hold_commands,
    "max_actions_in_month": max(
      (item["actions"] for item in action_counts),
      default=0,
    ),
    "multi_action_months": sum(
      item["actions"] > 1 for item in action_counts
    ),
    "longest_active_streak": longest_active_streak,
    "action_counts_by_month": action_counts,
  }


def _event_counts(history):
  player_count = 0
  rival_count = 0
  for transition in history:
    for event in transition.get("events", []) if isinstance(transition, dict) else []:
      text = str(event)
      if "treated " not in text or "operating revenue" not in text:
        continue
      if "Riverside Community Health:" in text:
        player_count += 1
      else:
        rival_count += 1
  return player_count, rival_count


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

  history = _history(run)
  trace = run.get("turn_trace")
  if run.get("completion_status") != "complete":
    issues.append("completion_status is not complete")
  if run.get("transition_count") != EXPECTED_TRANSITIONS:
    issues.append("transition_count is not 24")
  if any(not isinstance(item, dict) for item in history):
    issues.append("history contains a malformed transition")
  history_hashes = [item.get("state_hash") for item in history if isinstance(item, dict)]
  if run.get("state_hashes") != history_hashes:
    issues.append("state_hashes do not match committed history")
  if run.get("final_hash") != (history_hashes[-1] if history_hashes else None):
    issues.append("final_hash does not match committed history")
  if not isinstance(trace, list) or len(trace) != EXPECTED_TRANSITIONS:
    issues.append("turn_trace does not contain 24 entries")
  else:
    turns = []
    for index, entry in enumerate(trace):
      if not isinstance(entry, dict):
        issues.append("turn_trace contains a malformed entry")
        continue
      turns.append(entry.get("turn"))
      if not REQUIRED_TRACE_FIELDS <= set(entry):
        issues.append("turn_trace entry is missing required fields")
      if not isinstance(entry.get("retry_commands"), list):
        issues.append("retry_commands is not a list")
      latest_transition = entry.get("latest_transition")
      if not isinstance(latest_transition, dict):
        issues.append("turn_trace entry is missing latest_transition")
      elif index >= len(history_hashes):
        issues.append("turn_trace transition has no matching history entry")
      elif latest_transition.get("state_hash") != history_hashes[index]:
        issues.append("turn_trace transition hash is out of alignment")
    if turns != list(range(1, EXPECTED_TRANSITIONS + 1)):
      issues.append("turn_trace does not cover turns 1 through 24 in order")

  debrief = run.get("debrief")
  if not isinstance(debrief, list) or not debrief:
    issues.append("debrief is missing")
  else:
    month_count = sum(
      isinstance(line, str) and line.casefold().startswith("--- month ")
      for line in debrief
    )
    player_count = sum(
      isinstance(line, str) and line.casefold().startswith("player:")
      for line in debrief
    )
    if month_count < EXPECTED_TRANSITIONS or player_count < EXPECTED_TRANSITIONS:
      issues.append("debrief does not cover all committed months")
    if not any(
      isinstance(line, str)
      and "decision quality and outcome quality remain separate" in line.casefold()
      for line in debrief
    ):
      issues.append("debrief is missing decision/outcome quality framing")

  player_events, rival_events = _event_counts(history)
  return {
    "source_path": source_path,
    "status": "supported" if not issues else "limited",
    "issues": issues,
    "player_operating_month_count": player_events,
    "rival_operating_event_count": rival_events,
    **summary,
  }


def validate_artifact(artifact):
  assert artifact["artifact_type"] == ARTIFACT_TYPE
  assert artifact["batch_id"] == BATCH_ID
  assert artifact["code_version"] == EXPECTED_CODE_VERSION
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["ruleset"] == RULESET
  assert artifact["state_hash_schema"] == STATE_HASH_SCHEMA
  assert artifact["difficulty"] == DIFFICULTY
  assert artifact["seeds"] == SEEDS
  assert artifact["profiles"] == PROFILES
  assert artifact["runtime_promotion"] == "deferred"
  assert artifact["control"]["first_transition_hash"] == GOLDEN_CONTROL_HASH

  runs = artifact.get("runs")
  assert isinstance(runs, list)
  assert all(isinstance(run, dict) for run in runs)
  coordinates = [(run.get("profile_id"), run.get("seed")) for run in runs]
  assert len(runs) == EXPECTED_RUN_COUNT
  assert len(set(coordinates)) == len(coordinates)
  assert set(coordinates) == expected_matrix()
  for run in runs:
    assert run.get("campaign") == CAMPAIGN
    assert run.get("difficulty") == DIFFICULTY
    assert run.get("completion_status") in {"complete", "incomplete", "failed"}
    history = _history(run)
    assert all(isinstance(transition, dict) for transition in history)
    assert run.get("state_hashes") == [
      transition.get("state_hash")
      for transition in history
    ]
    assert run.get("final_hash") == (
      history[-1].get("state_hash") if history else None
    )


def build_audit(artifact):
  artifact = artifact if isinstance(artifact, dict) else {}
  runs = artifact.get("runs", [])
  runs = runs if isinstance(runs, list) else []
  gaps = []
  if any(artifact.get(key) != expected for key, expected in {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": EXPECTED_CODE_VERSION,
    "campaign": CAMPAIGN,
    "ruleset": RULESET,
    "state_hash_schema": STATE_HASH_SCHEMA,
    "difficulty": DIFFICULTY,
    "seeds": SEEDS,
    "profiles": PROFILES,
  }.items()):
    gaps.append({"type": "source identity"})

  reports = [
    audit_run(run, f"source run {index + 1}")
    for index, run in enumerate(runs)
  ]
  coordinates = [
    (report.get("profile_id"), report.get("seed"))
    for report in reports
  ]
  if len(runs) != EXPECTED_RUN_COUNT:
    gaps.append({"type": "run coverage", "expected": EXPECTED_RUN_COUNT, "actual": len(runs)})
  if len(set(coordinates)) != len(coordinates) or set(coordinates) != expected_matrix():
    gaps.append({
      "type": "matrix continuity",
      "missing": sorted(expected_matrix() - set(coordinates)),
      "unexpected": sorted(set(coordinates) - expected_matrix()),
    })
  limited_runs = [
    report["source_path"]
    for report in reports
    if report["status"] != "supported"
  ]
  if limited_runs:
    gaps.append({"type": "run validation", "limited_runs": limited_runs})

  action_counts_by_profile = defaultdict(Counter)
  for report in reports:
    action_counts_by_profile[report["profile_id"]]["actions"] += report["action_commands"]
    action_counts_by_profile[report["profile_id"]]["holds"] += report["hold_commands"]

  return {
    "artifact_type": artifact.get("artifact_type", "unknown"),
    "batch_id": artifact.get("batch_id", "unknown"),
    "code_version": artifact.get("code_version", "unknown"),
    "campaign": artifact.get("campaign", "unknown"),
    "difficulty": artifact.get("difficulty", "unknown"),
    "run_count": len(runs),
    "complete_run_count": sum(report["status"] == "supported" for report in reports),
    "transition_count": sum(report.get("transition_count", 0) for report in reports),
    "player_operating_month_count": sum(
      report.get("player_operating_month_count", 0) for report in reports
    ),
    "rival_operating_event_count": sum(
      report.get("rival_operating_event_count", 0) for report in reports
    ),
    "retry_count": sum(report.get("retry_count", 0) for report in reports),
    "reports": reports,
    "profile_summaries": {
      profile_id: dict(summary)
      for profile_id, summary in sorted(action_counts_by_profile.items())
    },
    "status": "supported" if not gaps else "limited",
    "unexplained_gaps": gaps,
    "unexplained_gap_count": len(gaps),
    "runtime_promotion": "deferred",
    "promotion_basis": (
      "Observation coverage, retries, and action cadence are descriptive "
      "teachability proxies. No runtime change is promoted by this artifact."
    ),
    "limitations": LIMITATIONS,
  }


def validate_audit(audit):
  assert audit["artifact_type"] == ARTIFACT_TYPE
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == EXPECTED_CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["status"] == "supported"
  assert audit["run_count"] == EXPECTED_RUN_COUNT
  assert audit["complete_run_count"] == EXPECTED_RUN_COUNT
  assert audit["transition_count"] == EXPECTED_RUN_COUNT * EXPECTED_TRANSITIONS
  assert audit["runtime_promotion"] == "deferred"


def render_markdown(audit):
  lines = [
    f"# Current-Code Teachability Evidence {audit['code_version']}",
    "",
    "- **Status:** Phase 7 competitive teachability and validation evidence",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Difficulty:** `{audit['difficulty']}`",
    f"- **Runs:** {audit['complete_run_count']} complete of {audit['run_count']}",
    f"- **Committed months:** {audit['transition_count']}",
    "",
    "This is deterministic simulated-policy evidence captured through the "
    "actor-visible MCP boundary. It does not change runtime behavior.",
    "",
    "## Profile summaries",
    "",
    "| Profile | Action commands | Holds |",
    "| --- | ---: | ---: |",
  ]
  for profile_id in PROFILES:
    summary = audit["profile_summaries"].get(profile_id, {})
    lines.append(
      f"| {profile_id} | {summary.get('actions', 0)} | "
      f"{summary.get('holds', 0)} |"
    )
  lines.extend([
    "",
    "## Trace and retry signals",
    "",
    f"- Player operating months: {audit['player_operating_month_count']}",
    f"- Rival operating events excluded from player evidence: {audit['rival_operating_event_count']}",
    f"- Recorded retry commands: {audit['retry_count']}",
    "",
    "## Promotion decision",
    "",
    "Runtime promotion: deferred",
    "",
    audit["promotion_basis"],
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
  validate_audit(audit)
  Path(args.output).write_text(render_markdown(audit), encoding="utf-8")
  print(f"Teachability diagnostics written to {args.output}")


if __name__ == "__main__":
  main()
