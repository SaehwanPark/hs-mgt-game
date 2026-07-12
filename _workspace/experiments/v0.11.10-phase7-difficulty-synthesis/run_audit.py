#!/usr/bin/env python3
"""Synthesize post-difficulty Phase 7 evidence without launching new sessions."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
STRATEGY_SOURCE_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.6-strategy-comparison-use-audit"
  / "results.json"
)
EXPERT_SOURCE_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.9-expert-difficulty-validation"
  / "results.json"
)

ARTIFACT_TYPE = "phase7_difficulty_evidence_synthesis"
BATCH_ID = "v0.11.10-phase7-difficulty-synthesis"
CODE_VERSION = "0.11.10"
CAMPAIGN = "competitive-regional-v1"
RULESET = "competitive-ruleset-0.2.0"
STATE_HASH_SCHEMA = "competitive-state-hash-v9"
GOLDEN_CONTROL_HASH = "61357596d8800592"
SEEDS = [42, 43, 44]
DIFFICULTIES = ["easy", "normal", "hard", "expert"]
PROFILES = [
  "Access First",
  "Commercial Focus",
  "Workforce Resilience",
  "Capital Modernization",
  "Coalition/Legitimacy",
]
EXPECTED_STRATEGY_RUNS = len(SEEDS) * len(DIFFICULTIES) * len(PROFILES)
EXPECTED_EXPERT_RUNS = len(SEEDS) * len(PROFILES)
EXPECTED_MONTHS = 24
REQUIRED_EXPERT_TRACE_FIELDS = {
  "turn",
  "observation",
  "legal_commands",
  "submitted_command",
  "validation_failures",
  "latest_transition",
  "done_after_submit",
}


def load_json(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _assert_metadata(source, expected_batch, expected_version):
  assert source["campaign"] == CAMPAIGN
  assert source["batch_id"] == expected_batch
  assert source["code_version"] == expected_version


def _expected_coordinates(difficulties):
  return {
    (profile, seed, difficulty)
    for profile in PROFILES
    for seed in SEEDS
    for difficulty in difficulties
  }


def validate_strategy_source(source):
  _assert_metadata(
    source,
    "v0.11.6-strategy-comparison-use-audit",
    "0.11.6",
  )
  assert source["ruleset"] == RULESET
  assert source["state_hash_schema"] == STATE_HASH_SCHEMA
  assert source["seeds"] == SEEDS
  assert source["difficulties"] == DIFFICULTIES
  assert source["profiles"] == PROFILES
  assert source["run_count"] == EXPECTED_STRATEGY_RUNS
  assert source["expected_run_count"] == EXPECTED_STRATEGY_RUNS
  assert source["completed_run_count"] == EXPECTED_STRATEGY_RUNS
  assert source["transition_count"] == EXPECTED_STRATEGY_RUNS * EXPECTED_MONTHS
  assert source["expected_month_count"] == EXPECTED_STRATEGY_RUNS * EXPECTED_MONTHS
  assert source["trace_count"] == source["transition_count"]
  assert source["prior_observation_match_count"] == 1380
  assert source["debrief_outcome_match_count"] == source["transition_count"]
  assert source["debrief_outcome_gap_count"] == 0
  assert source["trace_hash_match_count"] == source["transition_count"]
  assert source["observation_gap_count"] == 0
  assert source["response_gap_count"] == 0
  assert source["validation_failure_count"] == 0
  assert source["unexplained_gaps"] == []

  reports = source["run_reports"]
  assert len(reports) == EXPECTED_STRATEGY_RUNS
  coordinates = {
    (report["profile"], report["seed"], report["difficulty"])
    for report in reports
  }
  assert len(coordinates) == len(reports)
  assert coordinates == _expected_coordinates(DIFFICULTIES)
  assert all(report["status"] == "supported" for report in reports)


def validate_expert_source(source):
  _assert_metadata(
    source,
    "v0.11.9-expert-difficulty-validation",
    "0.11.9",
  )
  assert source["seeds"] == SEEDS
  assert source["difficulty"] == "expert"
  assert source["profiles"] == PROFILES

  runs = source["runs"]
  assert len(runs) == EXPECTED_EXPERT_RUNS
  coordinates = set()
  for run in runs:
    coordinate = (run["profile_name"], run["seed"])
    assert coordinate not in coordinates
    coordinates.add(coordinate)
    assert run["difficulty"] == "expert"
    assert run["completion_status"] == "complete"
    assert run["validation_failures"] == []
    assert run["transition_count"] == EXPECTED_MONTHS
    assert len(run["history"]) == EXPECTED_MONTHS
    assert len(run["state_hashes"]) == EXPECTED_MONTHS
    assert len(run["turn_trace"]) == EXPECTED_MONTHS
    assert run["final_observation"] is not None
    assert run["debrief"] is not None
    for entry in run["turn_trace"]:
      assert REQUIRED_EXPERT_TRACE_FIELDS <= set(entry)

  assert coordinates == {(profile, seed) for profile in PROFILES for seed in SEEDS}


def _source_summary(source, kind):
  if kind == "strategy_comparison":
    return {
      "batch_id": source["batch_id"],
      "code_version": source["code_version"],
      "run_count": source["run_count"],
      "transition_count": source["transition_count"],
      "seeds": source["seeds"],
      "difficulties": source["difficulties"],
      "profiles": source["profiles"],
      "supported_run_count": source["completed_run_count"],
      "observation_gap_count": source["observation_gap_count"],
      "debrief_outcome_gap_count": source["debrief_outcome_gap_count"],
      "response_gap_count": source["response_gap_count"],
      "validation_failure_count": source["validation_failure_count"],
    }

  return {
    "batch_id": source["batch_id"],
    "code_version": source["code_version"],
    "run_count": len(source["runs"]),
    "transition_count": sum(run["transition_count"] for run in source["runs"]),
    "seeds": source["seeds"],
    "difficulty": source["difficulty"],
    "profiles": source["profiles"],
    "completed_run_count": sum(
      run["completion_status"] == "complete" for run in source["runs"]
    ),
    "validation_failure_count": sum(
      len(run["validation_failures"]) for run in source["runs"]
    ),
    "trace_contract": "observation, legal commands, submitted command, validation failures, transition, and debrief",
  }


def build_synthesis(strategy_source, expert_source):
  validate_strategy_source(strategy_source)
  validate_expert_source(expert_source)

  expert_coordinates = {
    (run["profile_name"], run["seed"])
    for run in expert_source["runs"]
  }
  expected_expert_coordinates = {
    (profile, seed) for profile in PROFILES for seed in SEEDS
  }
  assert expert_coordinates == expected_expert_coordinates

  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "ruleset": RULESET,
    "state_hash_schema": STATE_HASH_SCHEMA,
    "golden_control_hash": GOLDEN_CONTROL_HASH,
    "source_artifacts": [
      _source_summary(strategy_source, "strategy_comparison"),
      _source_summary(expert_source, "expert_validation"),
    ],
    "coverage": {
      "strategy_comparison_all_tiers": {
        "run_count": EXPECTED_STRATEGY_RUNS,
        "transition_count": EXPECTED_STRATEGY_RUNS * EXPECTED_MONTHS,
        "coordinate_count": EXPECTED_STRATEGY_RUNS,
      },
      "expert_validation": {
        "run_count": EXPECTED_EXPERT_RUNS,
        "transition_count": EXPECTED_EXPERT_RUNS * EXPECTED_MONTHS,
        "coordinate_count": EXPECTED_EXPERT_RUNS,
      },
      "expert_profile_seed_overlap_count": len(expert_coordinates),
    },
    "contract_findings": [
      "The all-tier strategy-comparison artifact covers five profiles, three seeds, and four difficulty tiers with complete traceability.",
      "The post-change Expert artifact covers the same five profiles and three seeds with complete observations, commands, histories, hashes, and debriefs.",
      "The two artifacts retain source-specific contracts; no shared raw evidence schema is inferred.",
      "No structural evidence gap was identified in the overlapping profile and seed coordinates.",
    ],
    "gap_status": "no_structural_gap",
    "runtime_promotion": "deferred",
    "evidence_limits": [
      "This is deterministic simulated-policy traceability evidence, not human comprehension or learning evidence.",
      "Coverage and contract continuity do not establish causal strategy value, balance, or general Expert winnability.",
      "The source artifacts were produced at different code versions, so endpoint outcomes are not treated as a causal comparison.",
      "Operating quantities remain visible integer game abstractions rather than calibrated policy or financial units.",
    ],
    "next_gate": "Require a concrete unexplained player-facing, instructor-facing, or domain-review gap before runtime promotion.",
  }


def validate_synthesis(synthesis):
  assert synthesis["artifact_type"] == ARTIFACT_TYPE
  assert synthesis["batch_id"] == BATCH_ID
  assert synthesis["code_version"] == CODE_VERSION
  assert synthesis["campaign"] == CAMPAIGN
  assert synthesis["ruleset"] == RULESET
  assert synthesis["state_hash_schema"] == STATE_HASH_SCHEMA
  assert synthesis["golden_control_hash"] == GOLDEN_CONTROL_HASH
  assert len(synthesis["source_artifacts"]) == 2
  assert synthesis["coverage"]["strategy_comparison_all_tiers"]["run_count"] == EXPECTED_STRATEGY_RUNS
  assert synthesis["coverage"]["expert_validation"]["run_count"] == EXPECTED_EXPERT_RUNS
  assert synthesis["coverage"]["expert_profile_seed_overlap_count"] == EXPECTED_EXPERT_RUNS
  assert synthesis["gap_status"] == "no_structural_gap"
  assert synthesis["runtime_promotion"] == "deferred"
  assert synthesis["contract_findings"]
  assert synthesis["evidence_limits"]


def render_json(synthesis):
  return json.dumps(synthesis, indent=2, sort_keys=True) + "\n"


def render_markdown(synthesis):
  strategy, expert = synthesis["source_artifacts"]
  lines = [
    f"# Phase 7 Difficulty Evidence Synthesis {synthesis['code_version']}",
    "",
    "## Sources",
    "",
    f"- `{strategy['batch_id']}`: {strategy['run_count']} runs and {strategy['transition_count']} committed months.",
    f"- `{expert['batch_id']}`: {expert['run_count']} Expert runs and {expert['transition_count']} committed months.",
    "",
    "## Coverage",
    "",
    "| Source | Profiles | Seeds | Difficulties | Complete runs |",
    "| --- | ---: | ---: | --- | ---: |",
    f"| `{strategy['batch_id']}` | {len(strategy['profiles'])} | {len(strategy['seeds'])} | {', '.join(strategy['difficulties'])} | {strategy['supported_run_count']} |",
    f"| `{expert['batch_id']}` | {len(expert['profiles'])} | {len(expert['seeds'])} | {expert['difficulty']} | {expert['completed_run_count']} |",
    "",
    "## Findings",
    "",
  ]
  lines.extend(f"- {finding}" for finding in synthesis["contract_findings"])
  lines.extend([
    "",
    "## Interpretation and Routing",
    "",
    "No structural gap identified.",
    "Runtime promotion remains deferred.",
    "",
    "## Evidence Limits",
    "",
  ])
  lines.extend(f"- {limit}" for limit in synthesis["evidence_limits"])
  lines.extend(["", "## Next Gate", "", f"{synthesis['next_gate']}", ""])
  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--strategy-source", default=str(STRATEGY_SOURCE_PATH))
  parser.add_argument("--expert-source", default=str(EXPERT_SOURCE_PATH))
  parser.add_argument(
    "--output",
    default=str(Path(__file__).with_name("results.json")),
  )
  parser.add_argument(
    "--diagnostics",
    default=str(Path(__file__).with_name("diagnostics.md")),
  )
  args = parser.parse_args()

  synthesis = build_synthesis(
    load_json(args.strategy_source),
    load_json(args.expert_source),
  )
  validate_synthesis(synthesis)
  Path(args.output).write_text(render_json(synthesis), encoding="utf-8")
  Path(args.diagnostics).write_text(
    render_markdown(synthesis),
    encoding="utf-8",
  )
  print(
    f"Synthesized {len(synthesis['source_artifacts'])} artifacts; "
    f"gap_status={synthesis['gap_status']}; "
    f"promotion={synthesis['runtime_promotion']}"
  )


if __name__ == "__main__":
  main()
