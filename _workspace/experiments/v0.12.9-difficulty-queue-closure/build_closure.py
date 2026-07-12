#!/usr/bin/env python3
"""Close the difficulty-depth queue item without promoting runtime tuning."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
ARTIFACT_TYPE = "difficulty_depth_queue_closure"
BATCH_ID = "v0.12.9-difficulty-queue-closure"
CODE_VERSION = "0.12.9"
DIFFICULTY_EVIDENCE_PATH = (
  "_workspace/experiments/v0.12.4-difficulty-depth-evidence/results.json"
)
OBSERVATION_EVIDENCE_PATH = (
  "_workspace/experiments/v0.12.6-workforce-capacity-observation/results.json"
)

SOURCE_MARKERS = {
  "docs/playtest-findings-v0.12.5.md": [
    "- Runtime difficulty change: not authorized",
    "v0.12.4 workforce-capacity signal",
    "No difficulty values, transition formulas, balance",
  ],
  "docs/playtest-findings-v0.12.6.md": [
    "Runs: 75 complete.",
    "Transitions: 1,800.",
    "Source comparison: 60 all-tier histories and 15 Expert histories match",
    "Runtime difficulty and balance promotion remain deferred.",
  ],
  "_workspace/experiments/v0.12.4-difficulty-depth-evidence/diagnostics.md": [
    "candidate `workforce_capacity` pressure signal",
    "- **Runtime promotion:** deferred",
  ],
}


def _source_markers():
  result = {}
  for relative_path, markers in SOURCE_MARKERS.items():
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    assert not missing, f"{relative_path} missing markers: {missing}"
    result[relative_path] = {"markers": markers, "status": "supported"}
  return result


def _difficulty_evidence():
  artifact = json.loads((ROOT / DIFFICULTY_EVIDENCE_PATH).read_text(encoding="utf-8"))
  assert artifact["artifact_type"] == "difficulty_depth_evidence_review"
  assert artifact["runtime_promotion"] == "deferred"
  aggregate = artifact["aggregate"]
  pressure = artifact["pressure_signal"]
  clearability = artifact["clearability"]
  assert aggregate == {
    "expert_profile_seed_overlap_count": 15,
    "run_count": 75,
    "source_version_mismatch": True,
    "supported_run_count": 75,
    "transition_count": 1800,
  }
  assert pressure["dimension"] == "workforce_capacity"
  assert pressure["classification"] == "candidate_visible_pressure_signal"
  assert pressure["all_tier_counts"] == {
    "easy": 0,
    "normal": 15,
    "hard": 30,
    "expert": 160,
  }
  assert clearability["overlap_supported"] is True
  assert clearability["expected_runs"] == 15
  return {
    "path": DIFFICULTY_EVIDENCE_PATH,
    "code_version": artifact["code_version"],
    "run_count": aggregate["run_count"],
    "transition_count": aggregate["transition_count"],
    "pressure_dimension": pressure["dimension"],
    "pressure_classification": pressure["classification"],
    "tier_counts": pressure["all_tier_counts"],
    "expert_clearability_runs": clearability["expected_runs"],
    "source_version_mismatch": aggregate["source_version_mismatch"],
    "runtime_promotion": artifact["runtime_promotion"],
  }


def _observation_evidence():
  artifact = json.loads((ROOT / OBSERVATION_EVIDENCE_PATH).read_text(encoding="utf-8"))
  assert artifact["artifact_type"] == "workforce_capacity_observation_validation"
  assert artifact["runtime_promotion"] == "deferred"
  assert artifact["difficulty_change_authorized"] is False
  projection = artifact["observation_projection"]
  comparisons = artifact["source_comparisons"]
  assert len(artifact["runs"]) == 75
  assert projection["trace_entry_count"] == 1800
  assert projection["hidden_marker_count"] == 0
  assert all(item["history_match"] for item in comparisons)
  assert all(item["state_hashes_match"] for item in comparisons)
  return {
    "path": OBSERVATION_EVIDENCE_PATH,
    "code_version": artifact["code_version"],
    "run_count": len(artifact["runs"]),
    "transition_count": projection["trace_entry_count"],
    "staffing_lines": projection["staffing_line_count"],
    "physical_capacity_lines": projection["physical_capacity_line_count"],
    "hidden_marker_count": projection["hidden_marker_count"],
    "exact_history_match": all(item["history_match"] for item in comparisons),
    "exact_state_hash_match": all(item["state_hashes_match"] for item in comparisons),
    "runtime_promotion": artifact["runtime_promotion"],
  }


def build_closure():
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "closure_status": "complete_no_unexplained_gap",
    "difficulty_evidence": _difficulty_evidence(),
    "observation_evidence": _observation_evidence(),
    "source_marker_contract": _source_markers(),
    "runtime_difficulty_change_authorized": False,
    "runtime_promotion": "deferred",
    "queue_action": "remove_item_from_future_queue",
    "next_action": (
      "Require a new unexplained pressure, clearability, or player-facing "
      "difficulty gap and a separate design gate before changing difficulty "
      "or balance values."
    ),
    "evidence_limits": [
      "The workforce-capacity counts are descriptive simulated-policy evidence, not causal difficulty or balance evidence.",
      "Expert completion is a bounded clearability proxy for named profiles and seeds, not general winnability.",
      "Exact observation histories and hashes support an observation-only change classification, not a human-perceived difficulty claim.",
      "The source artifacts were produced at different code versions and retain that provenance limitation.",
    ],
  }


def validate_closure(closure):
  assert closure["artifact_type"] == ARTIFACT_TYPE
  assert closure["batch_id"] == BATCH_ID
  assert closure["code_version"] == CODE_VERSION
  assert closure["closure_status"] == "complete_no_unexplained_gap"
  assert closure["runtime_difficulty_change_authorized"] is False
  assert closure["runtime_promotion"] == "deferred"
  assert closure["queue_action"] == "remove_item_from_future_queue"
  difficulty = closure["difficulty_evidence"]
  assert difficulty["run_count"] == 75
  assert difficulty["transition_count"] == 1800
  assert difficulty["pressure_dimension"] == "workforce_capacity"
  assert difficulty["expert_clearability_runs"] == 15
  observation = closure["observation_evidence"]
  assert observation["run_count"] == 75
  assert observation["transition_count"] == 1800
  assert observation["exact_history_match"] is True
  assert observation["exact_state_hash_match"] is True
  assert all(
    value["status"] == "supported"
    for value in closure["source_marker_contract"].values()
  )


def render_diagnostics(closure):
  difficulty = closure["difficulty_evidence"]
  observation = closure["observation_evidence"]
  lines = [
    "# Difficulty Depth Queue Closure — v0.12.9",
    "",
    "- **Closure status:** complete; no unexplained difficulty gap",
    "- **Runtime difficulty change authorized:** no",
    "- **Runtime promotion:** deferred",
    "",
    "The v0.12.4 evidence identified workforce capacity as a candidate visible "
    "pressure signal, and v0.12.6 made its safe typed context visible without "
    "changing histories or hashes. The tested Expert paths remain clearable for "
    "the named profiles and seeds. No unexplained gap authorizes difficulty or "
    "balance tuning in this queue item.",
    "",
    "## Evidence",
    "",
    f"- Difficulty source: `{difficulty['path']}` ({difficulty['run_count']} runs, {difficulty['transition_count']} transitions).",
    f"- Candidate signal: `{difficulty['pressure_dimension']}`; tier counts Easy {difficulty['tier_counts']['easy']}, Normal {difficulty['tier_counts']['normal']}, Hard {difficulty['tier_counts']['hard']}, Expert {difficulty['tier_counts']['expert']}.",
    f"- Expert clearability overlap: {difficulty['expert_clearability_runs']} named profile/seed runs.",
    f"- Current observation source: {observation['run_count']} runs and {observation['transition_count']} trace entries with exact history/hash equality.",
    f"- Hidden-marker occurrences: {observation['hidden_marker_count']}.",
    "",
    "## Queue decision",
    "",
    "Remove the difficulty-depth and winnability item from the Future queue. "
    "Reopen it only after a new unexplained pressure, clearability, or "
    "player-facing difficulty gap is evidenced.",
    "",
    "## Evidence limits",
    "",
  ]
  lines.extend(f"- {limit}" for limit in closure["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  closure = build_closure()
  validate_closure(closure)
  (OUTPUT_DIR / "closure.json").write_text(
    json.dumps(closure, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (OUTPUT_DIR / "diagnostics.md").write_text(
    render_diagnostics(closure),
    encoding="utf-8",
  )
  print(f"Wrote closure artifact to {OUTPUT_DIR / 'closure.json'}")


if __name__ == "__main__":
  main()
